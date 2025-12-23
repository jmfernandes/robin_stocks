#!/usr/bin/env python3
"""
Example: Get All Recurring Investments

This script demonstrates how to fetch all your recurring investments from Robinhood.
"""

import argparse
import os
from collections import defaultdict
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import robin_stocks.robinhood as rh

# Load environment variables
load_dotenv()

console = Console()

def format_currency(amount):
    """Format amount as currency"""
    try:
        return f"${float(amount):.2f}"
    except:
        return f"${amount}"

def strip_rich_markup(text):
    """Remove Rich markup tags from text"""
    import re
    # Remove all Rich markup tags like [bold], [green], etc.
    return re.sub(r'\[/?[^\]]+\]', '', text)

def export_to_file(active_investments, paused_investments, summary_text, filename):
    """Export full data to a text file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RECURRING INVESTMENTS SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(strip_rich_markup(summary_text) + "\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"ACTIVE INVESTMENTS ({len(active_investments)})\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"{'Symbol':<10} {'Amount':>12} {'Frequency':<12} {'Sector':<30} {'Industry':<35} {'Description':<60} {'Next Date':<12} {'ID':<40}\n")
        f.write("-" * 80 + "\n")
        for inv in sorted(active_investments, key=lambda x: x['symbol']):
            desc = inv['description'].replace('\n', ' ').strip() if inv['description'] != 'N/A' else 'N/A'
            f.write(f"{inv['symbol']:<10} {format_currency(inv['amount']):>12} {inv['frequency']:<12} "
                   f"{inv['sector']:<30} {inv['industry']:<35} {desc:<60} {inv['next_date']:<12} {inv['schedule_id']:<40}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"PAUSED INVESTMENTS ({len(paused_investments)})\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"{'Symbol':<10} {'Amount':>12} {'Frequency':<12} {'Sector':<30} {'Industry':<35} {'Description':<60} {'ID':<40}\n")
        f.write("-" * 80 + "\n")
        for inv in sorted(paused_investments, key=lambda x: x['symbol']):
            desc = inv['description'].replace('\n', ' ').strip() if inv['description'] != 'N/A' else 'N/A'
            f.write(f"{inv['symbol']:<10} {format_currency(inv['amount']):>12} {inv['frequency']:<12} "
                   f"{inv['sector']:<30} {inv['industry']:<35} {desc:<60} {inv['schedule_id']:<40}\n")

def print_simple_format(active_investments, paused_investments, summary_text):
    """Print in simple, copy-paste friendly format"""
    console.print("\n[bold cyan]Simple Format (Full Text):[/bold cyan]\n")
    
    # Print summary
    console.print(summary_text)
    
    # Print active investments
    console.print(f"\n[bold green]ACTIVE INVESTMENTS ({len(active_investments)}):[/bold green]\n")
    console.print(f"{'Symbol':<10} {'Amount':>12} {'Frequency':<12} {'Sector':<30} {'Industry':<35} {'Description':<60} {'Next Date':<12} {'ID':<40}")
    console.print("-" * 80)
    for inv in sorted(active_investments, key=lambda x: x['symbol']):
        desc = inv['description'].replace('\n', ' ').strip() if inv['description'] != 'N/A' else 'N/A'
        console.print(f"{inv['symbol']:<10} {format_currency(inv['amount']):>12} {inv['frequency']:<12} "
                      f"{inv['sector']:<30} {inv['industry']:<35} {desc:<60} {inv['next_date']:<12} {inv['schedule_id']:<40}")
    
    # Print paused investments
    console.print(f"\n[bold yellow]PAUSED INVESTMENTS ({len(paused_investments)}):[/bold yellow]\n")
    console.print(f"{'Symbol':<10} {'Amount':>12} {'Frequency':<12} {'Sector':<30} {'Industry':<35} {'Description':<60} {'ID':<40}")
    console.print("-" * 80)
    for inv in sorted(paused_investments, key=lambda x: x['symbol']):
        desc = inv['description'].replace('\n', ' ').strip() if inv['description'] != 'N/A' else 'N/A'
        console.print(f"{inv['symbol']:<10} {format_currency(inv['amount']):>12} {inv['frequency']:<12} "
                      f"{inv['sector']:<30} {inv['industry']:<35} {desc:<60} {inv['schedule_id']:<40}")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Get all recurring investments from Robinhood',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Display formatted tables (default)
  %(prog)s --full-text         # Show full text without truncation
  %(prog)s --export output.txt # Export full data to file
  %(prog)s --simple            # Simple format for easy copy-paste
        """
    )
    parser.add_argument('--full-text', action='store_true',
                        help='Display full text without truncation (may wrap)')
    parser.add_argument('--export', metavar='FILE',
                        help='Export full data to a text file')
    parser.add_argument('--simple', action='store_true',
                        help='Output in simple, copy-paste friendly format')
    
    args = parser.parse_args()
    
    # Login
    username = os.getenv('robin_username')
    password = os.getenv('robin_password')
    mfa_secret = os.getenv('robin_mfa')
    
    console.print("[bold blue]Logging in...[/bold blue]")
    if mfa_secret:
        import pyotp
        totp = pyotp.TOTP(mfa_secret)
        mfa_code = totp.now()
        rh.login(username, password, mfa_code=mfa_code)
    else:
        rh.login(username, password)
    console.print("[bold green]✓ Logged in[/bold green]\n")
    
    # Enable rate limiting to avoid API throttling
    # Robinhood doesn't publish official rate limits, but community best practice is ~1 req/sec
    rh.enable_rate_limiting(delay=1.0)  # 1 second delay between requests
    console.print("[dim]Rate limiting enabled: 1 second delay between API calls[/dim]\n")
    
    # Get all recurring investments
    console.print("[bold blue]Fetching recurring investments...[/bold blue]")
    investments = rh.get_recurring_investments(asset_types=['equity', 'crypto'])
    
    # Handle response format
    if isinstance(investments, dict):
        results = investments.get('results', [])
    else:
        results = investments if isinstance(investments, list) else []
    
    if not results:
        console.print("[yellow]No recurring investments found.[/yellow]")
        return
    
    # Collect all unique symbols
    unique_symbols = set()
    for inv in results:
        symbol = inv.get('investment_target', {}).get('instrument_symbol', 'N/A')
        if symbol != 'N/A':
            unique_symbols.add(symbol)
    
    # Fetch fundamentals data for all symbols (batch calls in chunks of 50)
    console.print("[bold blue]Fetching company information...[/bold blue]")
    fundamentals_data = {}
    if unique_symbols:
        symbols_list = list(unique_symbols)
        # Process in chunks of 50 to avoid API limits
        # Rate limiting is already enabled, so each batch call will have 1s delay
        chunk_size = 50
        total_chunks = (len(symbols_list) + chunk_size - 1) // chunk_size
        for i in range(0, len(symbols_list), chunk_size):
            chunk = symbols_list[i:i + chunk_size]
            chunk_num = (i // chunk_size) + 1
            try:
                fundamentals_list = rh.get_fundamentals(chunk)
                if fundamentals_list:
                    for fund in fundamentals_list:
                        if fund and fund.get('symbol'):
                            fundamentals_data[fund['symbol']] = fund
                if chunk_num < total_chunks:
                    console.print(f"[dim]Processed chunk {chunk_num}/{total_chunks}...[/dim]")
            except Exception as e:
                error_msg = str(e)
                if '429' in error_msg or 'rate limit' in error_msg.lower():
                    console.print(f"[yellow]⚠ Rate limited! Waiting before retry...[/yellow]")
                    import time
                    time.sleep(5)  # Wait 5 seconds if rate limited
                else:
                    console.print(f"[yellow]Warning: Could not fetch fundamentals for some symbols: {e}[/yellow]")
                # Continue with next chunk even if one fails
    
    # Helper function to get company info
    def get_company_info(symbol):
        fund = fundamentals_data.get(symbol, {})
        return {
            'sector': fund.get('sector', 'N/A'),
            'industry': fund.get('industry', 'N/A'),
            'description': fund.get('description', 'N/A')
        }
    
    # Organize data
    active_investments = []
    paused_investments = []
    by_frequency = defaultdict(list)
    total_active_amount = 0
    total_paused_amount = 0
    
    for inv in results:
        symbol = inv.get('investment_target', {}).get('instrument_symbol', 'N/A')
        amount = float(inv.get('amount', {}).get('amount', 0))
        frequency = inv.get('frequency', 'N/A')
        state = inv.get('state', 'N/A')
        next_date = inv.get('next_investment_date', 'N/A')
        schedule_id = inv.get('id', 'N/A')
        
        # Get company info
        company_info = get_company_info(symbol)
        
        investment_data = {
            'symbol': symbol,
            'amount': amount,
            'frequency': frequency,
            'state': state,
            'next_date': next_date,
            'schedule_id': schedule_id,
            'sector': company_info['sector'],
            'industry': company_info['industry'],
            'description': company_info['description']
        }
        
        by_frequency[frequency].append(investment_data)
        
        if state == 'active':
            active_investments.append(investment_data)
            total_active_amount += amount
        elif state == 'paused':
            paused_investments.append(investment_data)
            total_paused_amount += amount
    
    # Print Summary Statistics in Rich Panel
    summary_text = f"[bold]Total Investments:[/bold] {len(results)}\n"
    summary_text += f"  [green]Active:[/green] {len(active_investments)}\n"
    summary_text += f"  [dim]Paused:[/dim] {len(paused_investments)}\n\n"
    summary_text += f"[bold]Total Weekly Investment Amount:[/bold]\n"
    summary_text += f"  [green]Active:[/green] {format_currency(total_active_amount)}\n"
    summary_text += f"  [dim]Paused:[/dim] {format_currency(total_paused_amount)}\n"
    summary_text += f"  [bold]Total:[/bold] {format_currency(total_active_amount + total_paused_amount)}\n\n"
    summary_text += f"[bold]By Frequency:[/bold]\n"
    for freq in sorted(by_frequency.keys()):
        count = len(by_frequency[freq])
        active_count = sum(1 for inv in by_frequency[freq] if inv['state'] == 'active')
        summary_text += f"  [cyan]{freq:12}[/cyan] : {count:3} total ([green]{active_count}[/green] active)\n"
    
    # Print summary (skip if simple format requested)
    if not args.simple:
        console.print(Panel(summary_text, title="[bold cyan]RECURRING INVESTMENTS SUMMARY[/bold cyan]", border_style="cyan"))
    
    # Print Active Investments in Rich Table (skip if simple format requested)
    if active_investments and not args.simple:
        # Determine column widths based on args
        sector_width = None if args.full_text else 20
        industry_width = None if args.full_text else 25
        desc_width = None if args.full_text else 35
        
        table = Table(
            title=f"[bold green]ACTIVE INVESTMENTS[/bold green] ({len(active_investments)})",
            box=box.ROUNDED,
            border_style="green",
            header_style="bold green"
        )
        table.add_column("Symbol", style="cyan", no_wrap=True)
        table.add_column("Amount", justify="right", style="green", no_wrap=True)
        table.add_column("Frequency", style="magenta", no_wrap=True)
        table.add_column("Sector", style="blue", max_width=sector_width, no_wrap=not args.full_text)
        table.add_column("Industry", style="blue", max_width=industry_width, no_wrap=not args.full_text)
        table.add_column("Description", style="dim", max_width=desc_width, no_wrap=not args.full_text)
        table.add_column("Next Date", style="yellow", no_wrap=True)
        table.add_column("ID", style="dim", no_wrap=True)
        
        # Sort by symbol
        for inv in sorted(active_investments, key=lambda x: x['symbol']):
            # Process description
            desc = inv['description']
            if desc != 'N/A':
                desc = desc.replace('\n', ' ').strip()
                if not args.full_text and len(desc) > 38:
                    desc = desc[:35] + "..."
            else:
                desc = "N/A"
            
            # Process sector and industry
            sector = inv['sector']
            if not args.full_text and len(sector) > 23:
                sector = sector[:20] + "..."
            
            industry = inv['industry']
            if not args.full_text and len(industry) > 28:
                industry = industry[:25] + "..."
            
            schedule_id = inv['schedule_id'] if args.full_text else inv['schedule_id'][:8] + "..."
            
            table.add_row(
                inv['symbol'],
                format_currency(inv['amount']),
                inv['frequency'],
                sector,
                industry,
                desc,
                inv['next_date'],
                schedule_id
            )
        
        console.print("\n")
        console.print(table)
    
    # Print Paused Investments in Rich Table (skip if simple format requested)
    if paused_investments and not args.simple:
        # Determine column widths based on args
        sector_width = None if args.full_text else 20
        industry_width = None if args.full_text else 25
        desc_width = None if args.full_text else 35
        
        table = Table(
            title=f"[bold yellow]PAUSED INVESTMENTS[/bold yellow] ({len(paused_investments)})",
            box=box.ROUNDED,
            border_style="yellow",
            header_style="bold yellow"
        )
        table.add_column("Symbol", style="dim cyan", no_wrap=True)
        table.add_column("Amount", justify="right", style="dim", no_wrap=True)
        table.add_column("Frequency", style="dim magenta", no_wrap=True)
        table.add_column("Sector", style="dim blue", max_width=sector_width, no_wrap=not args.full_text)
        table.add_column("Industry", style="dim blue", max_width=industry_width, no_wrap=not args.full_text)
        table.add_column("Description", style="dim", max_width=desc_width, no_wrap=not args.full_text)
        table.add_column("ID", style="dim", no_wrap=True)
        
        # Sort by symbol
        for inv in sorted(paused_investments, key=lambda x: x['symbol']):
            # Process description
            desc = inv['description']
            if desc != 'N/A':
                desc = desc.replace('\n', ' ').strip()
                if not args.full_text and len(desc) > 33:
                    desc = desc[:30] + "..."
            else:
                desc = "N/A"
            
            # Process sector and industry
            sector = inv['sector']
            if not args.full_text and len(sector) > 18:
                sector = sector[:15] + "..."
            
            industry = inv['industry']
            if not args.full_text and len(industry) > 23:
                industry = industry[:20] + "..."
            
            schedule_id = inv['schedule_id'] if args.full_text else inv['schedule_id'][:8] + "..."
            
            table.add_row(
                inv['symbol'],
                format_currency(inv['amount']),
                inv['frequency'],
                sector,
                industry,
                desc,
                schedule_id
            )
        
        console.print("\n")
        console.print(table)
    
    # Handle export or simple format
    if args.export:
        export_to_file(active_investments, paused_investments, summary_text, args.export)
        console.print(f"\n[bold green]✓ Data exported to {args.export}[/bold green]")
    
    if args.simple:
        print_simple_format(active_investments, paused_investments, summary_text)
    
    console.print()

if __name__ == '__main__':
    main()

