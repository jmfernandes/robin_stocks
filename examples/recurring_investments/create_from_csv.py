#!/usr/bin/env python3
"""
Create Multiple Recurring Investments from CSV

This script reads investments from a CSV file and creates recurring investments.
Supports two CSV formats:
  1. Simple: symbol,amount,frequency
  2. Detailed: No,Company,Symbol,Amount (USD),Period

Features:
  - Rate limiting (2s delay between requests)
  - Automatic retry with exponential backoff
  - Duplicate detection (skips existing investments)
  - Rich progress bars and formatted output
  - Detailed logging
"""

import os
import sys
import csv
import time
import logging
import importlib
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table
from rich.panel import Panel
from rich.logging import RichHandler

# ============================================================================
# CONFIGURATION
# ============================================================================

# Import rate limiting settings from config (in same directory)
_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.py')
if os.path.exists(_config_path):
    # Add parent directory to path for import
    _config_dir = os.path.dirname(_config_path)
    if _config_dir not in sys.path:
        sys.path.insert(0, _config_dir)
    try:
        import config as _config_module
        ENABLE_CORE_RATE_LIMITING = _config_module.ENABLE_CORE_RATE_LIMITING
        CORE_RATE_LIMIT_DELAY = _config_module.CORE_RATE_LIMIT_DELAY
        MAX_RETRIES = _config_module.MAX_RETRIES
        INITIAL_RETRY_DELAY = _config_module.INITIAL_RETRY_DELAY
        RETRYABLE_ERROR_CODES = _config_module.RETRYABLE_ERROR_CODES
        DELAY_BETWEEN_REQUESTS = getattr(_config_module, 'DELAY_BETWEEN_REQUESTS', _config_module.CORE_RATE_LIMIT_DELAY)
    except (ImportError, AttributeError):
        # Fallback if config not found or missing attributes (backward compatibility)
        ENABLE_CORE_RATE_LIMITING = True
        CORE_RATE_LIMIT_DELAY = 5.0
        DELAY_BETWEEN_REQUESTS = 5.0
        MAX_RETRIES = 3
        INITIAL_RETRY_DELAY = 10
        RETRYABLE_ERROR_CODES = ['429', '502', '503', '504']
else:
    # Fallback if config file doesn't exist (backward compatibility)
    ENABLE_CORE_RATE_LIMITING = True
    CORE_RATE_LIMIT_DELAY = 5.0
    DELAY_BETWEEN_REQUESTS = 5.0
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 10
    RETRYABLE_ERROR_CODES = ['429', '502', '503', '504']

# CSV file path (can be overridden with INVESTMENTS_CSV env var)
# Defaults to 'recurring.csv' in the same directory as this script
DEFAULT_CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recurring.csv')

# Logging setup - minimal logging to avoid clutter
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f'recurring_investments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# Setup logging with Rich - only WARNING and above to console, INFO to file
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True, console=Console(stderr=True), level=logging.WARNING),
        logging.FileHandler(LOG_FILE)
    ]
)
logger = logging.getLogger(__name__)

# Rich console for output
console = Console()

# ============================================================================
# SETUP: Add repo root to Python path
# ============================================================================

def setup_path():
    """Add repository root to Python path to use local robin_stocks code."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    return repo_root

setup_path()

# Import robin_stocks after path setup
import robin_stocks.robinhood as rh
from robin_stocks.robinhood.urls import recurring_schedules_url
from robin_stocks.robinhood.helper import request_get
importlib.reload(rh)

# ============================================================================
# CSV PARSING
# ============================================================================

def parse_simple_format(reader):
    """Parse simple CSV format: symbol,amount,frequency"""
    investments = []
    for row in reader:
        if len(row) >= 2:
            symbol = row[0].strip().upper()
            amount = float(row[1].strip())
            frequency = row[2].strip().lower() if len(row) > 2 else 'weekly'
            investments.append({
                'symbol': symbol,
                'amount': amount,
                'frequency': frequency
            })
    return investments

def parse_detailed_format(reader, header):
    """Parse detailed CSV format: No,Company,Symbol,Amount (USD),Period"""
    investments = []
    
    symbol_idx = header.index('Symbol')
    amount_idx = header.index('Amount (USD)') if 'Amount (USD)' in header else header.index('Amount')
    period_idx = header.index('Period') if 'Period' in header else None
    
    frequency_map = {
        'weekly': 'weekly',
        'monthly': 'monthly',
        'biweekly': 'biweekly',
        'daily': 'daily'
    }
    
    for row in reader:
        if len(row) <= max(symbol_idx, amount_idx):
            continue
            
        symbol = row[symbol_idx].strip().upper()
        symbol = symbol.split('(')[0].strip() if '(' in symbol else symbol
        symbol = symbol.split(',')[0].strip() if ',' in symbol else symbol
        
        try:
            amount = float(row[amount_idx].strip().replace('$', '').replace(',', ''))
            
            if period_idx and len(row) > period_idx:
                period = row[period_idx].strip().lower()
                frequency = frequency_map.get(period, 'weekly')
            else:
                frequency = 'weekly'
            
            if symbol and amount >= 1.0:
                investments.append({
                    'symbol': symbol,
                    'amount': amount,
                    'frequency': frequency
                })
        except (ValueError, IndexError) as e:
            logger.warning(f"Skipping row with symbol '{symbol}': {e}")
            continue
    
    return investments

def load_investments_from_csv(csv_file):
    """Load investments from CSV file, auto-detecting format."""
    investments = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            
            if not header:
                console.print("[red]Error: CSV file appears to be empty[/red]")
                return investments
            
            header = [h.strip() for h in header]
            
            if 'Symbol' in header and ('Amount' in str(header) or 'Amount (USD)' in str(header)):
                investments = parse_detailed_format(reader, header)
            else:
                investments = parse_simple_format(reader)
                
    except FileNotFoundError:
        console.print(f"[red]Error: CSV file not found: {csv_file}[/red]")
    except Exception as e:
        console.print(f"[red]Error reading CSV: {e}[/red]")
        logger.exception("Error reading CSV")
    
    return investments

# ============================================================================
# API CALLS WITH RETRY LOGIC
# ============================================================================

def check_fractional_tradability(symbol):
    """Check if a symbol is fractionally tradable (required for recurring investments)."""
    try:
        instruments = rh.get_instruments_by_symbols(symbol)
        if not instruments or len(instruments) == 0:
            return False, "Symbol not found"
        
        instrument = instruments[0]
        fractional_tradability = instrument.get('fractional_tradability', '')
        
        # Check if fractionally tradable
        # Only 'tradable' means it can be used for recurring investments
        if fractional_tradability == 'tradable':
            return True, None
        elif fractional_tradability == 'position_closing_only':
            return False, "Not fractionally tradable (position closing only)"
        elif fractional_tradability:
            return False, f"Not fractionally tradable ({fractional_tradability})"
        else:
            # If fractional_tradability is empty/None, assume not tradable
            return False, "Fractional trading not supported"
    except Exception as e:
        # If we can't check, assume it might be tradable and let the API call fail
        logger.warning(f"Could not check fractional tradability for {symbol}: {e}")
        return None, None  # Unknown - let API call determine

def create_with_retry(symbol, amount, frequency, retry_count=0):
    """Create recurring investment with retry logic for rate limits."""
    try:
        result = rh.create_recurring_investment(
            symbol=symbol,
            amount=amount,
            frequency=frequency
        )
        if result and result.get('id'):
            return result, None
        else:
            return None, f"API returned invalid response: {result}"
    except Exception as e:
        error_str = str(e).lower()
        error_msg = str(e)
        
        # Check if error is retryable using config
        is_retryable = any(code in error_msg for code in RETRYABLE_ERROR_CODES)
        is_rate_limit = '429' in error_msg or 'rate limit' in error_str or 'throttle' in error_str
        is_server_error = any(code in error_msg for code in ['502', '503', '504'])
        
        if is_retryable and retry_count < MAX_RETRIES:
            delay = INITIAL_RETRY_DELAY * (2 ** retry_count)
            if is_rate_limit:
                logger.warning(f"Rate limited. Waiting {delay}s before retry {retry_count + 1}/{MAX_RETRIES}...")
            elif is_server_error:
                logger.warning(f"Server error ({error_msg}). Waiting {delay}s before retry {retry_count + 1}/{MAX_RETRIES}...")
            else:
                logger.warning(f"Retryable error ({error_msg}). Waiting {delay}s before retry {retry_count + 1}/{MAX_RETRIES}...")
            time.sleep(delay)
            return create_with_retry(symbol, amount, frequency, retry_count + 1)
        
        # After retries exhausted or non-retryable error, check fractional tradability
        is_tradable, tradability_msg = check_fractional_tradability(symbol)
        if is_tradable is False:
            return None, f"Not eligible for recurring investments: {tradability_msg}"
        
        if is_rate_limit:
            return None, f"Rate limit exceeded after {MAX_RETRIES} retries"
        elif is_server_error:
            return None, f"Server error after {MAX_RETRIES} retries: {error_msg}"
        else:
            return None, error_msg

def get_existing_investments():
    """Fetch existing recurring investments and return as a set for duplicate checking."""
    existing_set = set()
    
    all_existing = []
    next_page = True
    url = None
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Loading existing investments...", total=None)
        
        while next_page:
            try:
                if url:
                    # Use request_get directly for pagination URLs
                    existing_page = request_get(url, 'pagination', jsonify_data=True)
                else:
                    existing_page = rh.get_recurring_investments(asset_types=['equity', 'crypto'], jsonify=True)
                
                if isinstance(existing_page, dict):
                    results = existing_page.get('results', [])
                    next_page = existing_page.get('next')
                    url = next_page
                else:
                    results = existing_page if isinstance(existing_page, list) else []
                    next_page = None
                
                all_existing.extend(results)
                progress.update(task, description=f"[cyan]Loaded {len(all_existing)} existing investments...")
                
                if next_page:
                    time.sleep(0.5)  # Small delay between pages
                else:
                    break
            except Exception as e:
                logger.error(f"Error fetching existing investments: {e}")
                break
    
    for inv in all_existing:
        symbol = inv.get('investment_target', {}).get('instrument_symbol', '').upper()
        amount = float(inv.get('amount', {}).get('amount', 0))
        frequency = inv.get('frequency', '')
        state = inv.get('state', '')
        
        if state != 'deleted':
            existing_set.add((symbol, amount, frequency))
    
    logger.info(f"Found {len(existing_set)} existing recurring investments.")
    return existing_set

# ============================================================================
# AUTHENTICATION
# ============================================================================

def login_to_robinhood():
    """Login to Robinhood using credentials from .env file."""
    load_dotenv()
    
    username = os.getenv('robin_username')
    password = os.getenv('robin_password')
    mfa_secret = os.getenv('robin_mfa')
    
    if not username or not password:
        console.print("[red]Error: robin_username and robin_password must be set in .env file[/red]")
        return False
    
    console.print("[cyan]Logging in...[/cyan]")
    try:
        if mfa_secret:
            import pyotp
            totp = pyotp.TOTP(mfa_secret)
            mfa_code = totp.now()
            rh.login(username, password, mfa_code=mfa_code)
        else:
            rh.login(username, password)
        console.print("[green]✓ Logged in[/green]\n")
        logger.info("Successfully logged in")
        return True
    except Exception as e:
        console.print(f"[red]✗ Login failed: {e}[/red]")
        logger.error(f"Login failed: {e}")
        return False

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to create recurring investments from CSV."""
    console.print(Panel.fit(
        "[bold cyan]Create Recurring Investments from CSV[/bold cyan]",
        border_style="cyan"
    ))
    console.print(f"[dim]Log file: {LOG_FILE}[/dim]\n")
    
    # Step 1: Login
    if not login_to_robinhood():
        return
    
    # Step 1.5: Enable core rate limiting if configured
    if ENABLE_CORE_RATE_LIMITING:
        rh.enable_rate_limiting(CORE_RATE_LIMIT_DELAY)
        console.print(f"[dim]Core rate limiting enabled: {CORE_RATE_LIMIT_DELAY}s delay[/dim]\n")
        logger.info(f"Core rate limiting enabled with {CORE_RATE_LIMIT_DELAY}s delay")
    
    # Step 2: Load investments from CSV
    csv_file = os.getenv('INVESTMENTS_CSV', DEFAULT_CSV_FILE)
    investments = load_investments_from_csv(csv_file)
    
    if not investments:
        console.print("[yellow]No investments found in CSV file.[/yellow]")
        console.print(f"\nExpected CSV file: [cyan]{csv_file}[/cyan]")
        console.print("\nSupported formats:")
        console.print("  1. Simple: symbol,amount,frequency")
        console.print("  2. Detailed: No,Company,Symbol,Amount (USD),Period")
        return
    
    # Step 3: Display investments to create
    table = Table(title="Investments to Create", show_header=True, header_style="bold magenta")
    table.add_column("Symbol", style="cyan")
    table.add_column("Amount", style="green")
    table.add_column("Frequency", style="yellow")
    
    for inv in investments:
        table.add_row(
            inv['symbol'],
            f"${inv['amount']:.2f}",
            inv['frequency']
        )
    
    console.print(table)
    console.print(f"\n[dim]Total: {len(investments)} investments[/dim]")
    
    # Step 4: Estimate time
    estimated_time = len(investments) * DELAY_BETWEEN_REQUESTS
    estimated_minutes = estimated_time / 60
    console.print(f"\n[dim]⏱ Estimated time: ~{estimated_time:.0f}s ({estimated_minutes:.1f} min) | Delay: {DELAY_BETWEEN_REQUESTS}s between requests[/dim]")
    console.print(f"[yellow]⚠ This will take a while to avoid rate limits. Please be patient![/yellow]\n")
    
    # Step 5: Get existing investments
    console.print("[cyan]Checking existing recurring investments...[/cyan]")
    existing_set = get_existing_investments()
    console.print(f"[green]Found {len(existing_set)} existing recurring investments[/green]\n")
    
    # Step 6: Create investments with progress bar
    console.print(Panel.fit(
        "[bold cyan]Creating Recurring Investments[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    created = []
    skipped = []
    failed = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed}/{task.total})"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Processing investments...", total=len(investments))
        
        for i, inv in enumerate(investments, 1):
            symbol = inv['symbol']
            amount = inv['amount']
            frequency = inv['frequency']
            
            # Update progress description with current symbol
            progress.update(
                task, 
                description=f"[cyan]Processing {symbol} (${amount:.2f} {frequency})...",
                advance=0  # Don't advance yet
            )
            
            # Check if already exists
            if (symbol, amount, frequency) in existing_set:
                skipped.append(inv)
                console.print(f"  [yellow]⚠ Skipped[/yellow] {symbol}: ${amount:.2f} {frequency} - [dim]already exists[/dim]")
                logger.info(f"Skipped {symbol} ${amount} {frequency} - already exists")
                progress.advance(task)
                continue
            
            # Pre-check fractional tradability (optional - provides better error messages)
            is_tradable, tradability_msg = check_fractional_tradability(symbol)
            if is_tradable is False:
                failed.append({**inv, 'error': f"Not eligible: {tradability_msg}"})
                console.print(f"  [red]✗ Skipped[/red] {symbol}: ${amount:.2f} {frequency} - [dim]not eligible for recurring investments ({tradability_msg})[/dim]")
                logger.warning(f"Skipped {symbol} ${amount} {frequency} - not eligible: {tradability_msg}")
                progress.advance(task)
                continue
            
            # Create with retry logic
            result, error = create_with_retry(symbol, amount, frequency)
            
            if result and result.get('id'):
                created.append({**inv, 'id': result.get('id')})
                console.print(f"  [green]✓ Created[/green] {symbol}: ${amount:.2f} {frequency} [dim](ID: {result.get('id', 'N/A')[:8]}...)[/dim]")
                logger.info(f"Created {symbol} ${amount} {frequency} - ID: {result.get('id')}")
            else:
                failed.append({**inv, 'error': error or 'Unknown error'})
                # Determine error category for better display
                error_msg = error or 'Unknown error'
                if 'not eligible' in error_msg.lower() or 'not fractionally tradable' in error_msg.lower():
                    console.print(f"  [red]✗ Skipped[/red] {symbol}: ${amount:.2f} {frequency} - [dim]{error_msg}[/dim]")
                else:
                    console.print(f"  [red]✗ Failed[/red] {symbol}: ${amount:.2f} {frequency} - [dim]{error_msg}[/dim]")
                logger.error(f"Failed {symbol} ${amount} {frequency} - {error}")
            
            progress.advance(task)
            
            # Rate limiting - always wait between requests (including last one for safety)
            if i < len(investments):
                time.sleep(DELAY_BETWEEN_REQUESTS)
            else:
                # Small delay after last request too
                time.sleep(1.0)
    
    # Step 7: Detailed Summary
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Summary[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    # Summary table
    summary_table = Table(show_header=True, header_style="bold", box=None)
    summary_table.add_column("Status", style="bold", width=12)
    summary_table.add_column("Count", justify="right", style="bold", width=8)
    summary_table.add_column("Details", style="dim")
    
    summary_table.add_row(
        "[green]✓ Created[/green]",
        f"[green]{len(created)}[/green]",
        f"[dim]{len(created)} new recurring investments set up[/dim]"
    )
    summary_table.add_row(
        "[yellow]⚠ Skipped[/yellow]",
        f"[yellow]{len(skipped)}[/yellow]",
        f"[dim]Already exist in your account[/dim]"
    )
    summary_table.add_row(
        "[red]✗ Failed[/red]",
        f"[red]{len(failed)}[/red]",
        f"[dim]Need to retry or check manually[/dim]"
    )
    
    console.print(summary_table)
    console.print()
    
    # Show created investments
    if created:
        created_table = Table(title="[green]✓ Successfully Created[/green]", show_header=True, header_style="bold green", box=None)
        created_table.add_column("#", style="dim", width=4, justify="right")
        created_table.add_column("Symbol", style="cyan", width=10)
        created_table.add_column("Amount", style="green", width=12)
        created_table.add_column("Frequency", style="yellow", width=10)
        created_table.add_column("ID", style="dim", width=12)
        
        for idx, inv in enumerate(created, 1):
            created_table.add_row(
                str(idx),
                inv['symbol'],
                f"${inv['amount']:.2f}",
                inv['frequency'],
                inv['id'][:8] + "..."
            )
        console.print(created_table)
        console.print()
    
    # Show skipped investments
    if skipped:
        skipped_table = Table(title="[yellow]⚠ Skipped (Already Exist)[/yellow]", show_header=True, header_style="bold yellow", box=None)
        skipped_table.add_column("#", style="dim", width=4, justify="right")
        skipped_table.add_column("Symbol", style="cyan", width=10)
        skipped_table.add_column("Amount", style="green", width=12)
        skipped_table.add_column("Frequency", style="yellow", width=10)
        
        for idx, inv in enumerate(skipped[:20], 1):  # Show first 20
            skipped_table.add_row(
                str(idx),
                inv['symbol'],
                f"${inv['amount']:.2f}",
                inv['frequency']
            )
        if len(skipped) > 20:
            skipped_table.add_row("...", f"[dim]({len(skipped) - 20} more)[/dim]", "", "")
        console.print(skipped_table)
        console.print()
    
    # Show failed investments with actionable info
    if failed:
        # Separate permanent failures (not eligible) from temporary failures
        not_eligible = [inv for inv in failed if 'not eligible' in inv.get('error', '').lower() or 'not fractionally tradable' in inv.get('error', '').lower()]
        temporary_failures = [inv for inv in failed if inv not in not_eligible]
        
        if not_eligible:
            not_eligible_table = Table(title="[red]✗ Not Eligible for Recurring Investments[/red]", show_header=True, header_style="bold red", box=None)
            not_eligible_table.add_column("#", style="dim", width=4, justify="right")
            not_eligible_table.add_column("Symbol", style="cyan", width=10)
            not_eligible_table.add_column("Amount", style="green", width=12)
            not_eligible_table.add_column("Frequency", style="yellow", width=10)
            not_eligible_table.add_column("Reason", style="red", width=40)
            
            for idx, inv in enumerate(not_eligible, 1):
                error = inv.get('error', 'Unknown error')
                if len(error) > 37:
                    error = error[:34] + "..."
                not_eligible_table.add_row(
                    str(idx),
                    inv['symbol'],
                    f"${inv['amount']:.2f}",
                    inv['frequency'],
                    error
                )
            console.print(not_eligible_table)
            console.print()
        
        if temporary_failures:
            failed_table = Table(title="[red]✗ Failed (May Retry)[/red]", show_header=True, header_style="bold red", box=None)
            failed_table.add_column("#", style="dim", width=4, justify="right")
            failed_table.add_column("Symbol", style="cyan", width=10)
            failed_table.add_column("Amount", style="green", width=12)
            failed_table.add_column("Frequency", style="yellow", width=10)
            failed_table.add_column("Error", style="red", width=40)
            
            for idx, inv in enumerate(temporary_failures, 1):
                error = inv.get('error', 'Unknown error')
                if len(error) > 37:
                    error = error[:34] + "..."
                failed_table.add_row(
                    str(idx),
                    inv['symbol'],
                    f"${inv['amount']:.2f}",
                    inv['frequency'],
                    error
                )
            console.print(failed_table)
            console.print()
        
        if temporary_failures:
            console.print(Panel(
                "[yellow]💡 Tip:[/yellow] Failed investments can be retried by running this script again.\n"
                "The script will automatically skip investments that already exist,\n"
                "so you can safely re-run it to process only the failed ones.",
                title="[bold yellow]Retry Information[/bold yellow]",
                border_style="yellow"
            ))
            console.print()
        elif not_eligible:
            console.print(Panel(
                "[yellow]💡 Note:[/yellow] These symbols are not eligible for recurring investments.\n"
                "They may not support fractional trading or have other restrictions.\n"
                "Consider removing them from your CSV file.",
                title="[bold yellow]Not Eligible[/bold yellow]",
                border_style="yellow"
            ))
            console.print()
    
    # Final status message
    if failed:
        console.print(f"[yellow]⚠ {len(failed)} investment(s) failed. Check the log file for details.[/yellow]")
        console.print(f"[dim]Log file: {LOG_FILE}[/dim]\n")
    else:
        console.print("[green]✓ All investments processed successfully![/green]")
        console.print(f"[dim]Log file: {LOG_FILE}[/dim]\n")

if __name__ == '__main__':
    main()
