#!/usr/bin/env python3
"""
Compare Original Portfolio vs Current Portfolio

Analyzes the differences between the original portfolio and current portfolio
to identify removed positions, added positions, and amount changes.
"""

import json
import re
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Original portfolio from restore_full_diverse_portfolio.py
ORIGINAL_PORTFOLIO = {
    # China/Hong Kong (14 positions)
    'ASHR': 50, 'CNXT': 50, 'CQQQ': 50, 'CXSE': 50, 'ECNS': 50, 'FXI': 50,
    'KSTR': 50, 'KURE': 50, 'KWEB': 50, 'MCHI': 50, 'TCHI': 50,
    'EWH': 25, 'LI': 20, 'NIO': 20,
    
    # International ETFs (16 positions)
    'EIDO': 25, 'EIS': 25, 'EPOL': 25, 'EWS': 25, 'EWT': 25, 'EWY': 25,
    'FLKR': 25, 'FLTW': 25, 'FRDM': 25, 'GVAL': 25, 'IDX': 25, 'ISRA': 25, 'IZRL': 25,
    'QQQ': 10, 'SPY': 10, 'VEA': 10,
    
    # Technology - Software/Cloud (13 positions)
    'GOOG': 25, 'META': 25, 'MSFT': 25, 'PATH': 25, 'U': 25, 'ZM': 25,
    'COMP': 10, 'CRM': 10, 'GOOGL': 10, 'MSTR': 10, 'PLTR': 10, 'SNAP': 10,
    
    # Finance - Financial Services (8 positions)
    'AGM': 25, 'HOOD': 25, 'V': 25,
    'BCH': 10, 'CME': 10, 'MAIN': 10, 'RM': 10,
    
    # Defense/Aerospace (5 positions)
    'MISL': 25, 'PPA': 25, 'SHLD': 25,
    'ESLT': 10, 'HON': 10,
    
    # Finance - REITs (5 positions)
    'AHR': 25, 'O': 25, 'PLD': 25,
    'APLE': 10, 'LTC': 10,
    
    # Transportation - EV Manufacturers (5 positions)
    'DHI': 25, 'F': 25,
    'RIVN': 20, 'TSLA': 10,
    
    # Industrial - Infrastructure (4 positions)
    'ENB': 25, 'EPD': 25,
    'ACM': 10, 'WM': 10,
    
    # Technology - Quantum Computing (7 positions)
    'IONQ': 10, 'QBTS': 10, 'QTUM': 10, 'QUBT': 10, 'RGTI': 10,
    
    # Crypto - Cryptocurrency (7 positions)
    'BTC': 10, 'DOGE': 10, 'ETC': 10, 'ETH': 10, 'SHIB': 10, 'SOL': 10, 'XRP': 10,
    
    # Healthcare - Pharmaceuticals (5 positions)
    'IHE': 20, 'PFE': 20,
    'JNJ': 10, 'MRNA': 10, 'RARE': 10,
    
    # Commodities - Precious Metals (5 positions)
    'PAAS': 25,
    'GDX': 10, 'RING': 10, 'SLV': 10,
    
    # Technology - Innovation ETFs (5 positions)
    'ARKK': 25,
    'ARKG': 10, 'ARKW': 10, 'BOTZ': 10, 'METV': 10,
    
    # Consumer - Retail (5 positions)
    'GME': 25,
    'AMZN': 10, 'COST': 10, 'KR': 10, 'WMT': 10,
    
    # Technology - Semiconductors (4 positions)
    'NVDA': 25,
    'AAPL': 10, 'AMD': 10, 'LINK': 10,
    
    # Crypto - Mining (2 positions)
    'MARA': 25, 'RIOT': 25,
    
    # Consumer - Hospitality (3 positions)
    'DIS': 25,
    'ABNB': 10, 'HLT': 10,
    
    # Energy - Clean/Renewable (3 positions)
    'ICLN': 25, 'OKLO': 10,
    
    # Commodities - Base Metals (3 positions)
    'MP': 25,
    'DBB': 10, 'ICOP': 10,
    
    # Healthcare - Services (4 positions)
    'BKD': 10, 'UNH': 10, 'XLV': 10,
    
    # EV Supply Chain - Lithium/Batteries (2 positions)
    'LIT': 25, 'ALB': 10,
    
    # Transportation - Logistics (2 positions)
    'WERN': 25, 'DAC': 10,
    
    # Transportation - Aviation/Space (3 positions)
    'ACHR': 10, 'JOBY': 10, 'RKLB': 10,
    
    # Transportation - Mobility/Rideshare (2 positions)
    'LYFT': 10, 'UBER': 10,
    
    # Industrial - Materials/Chemicals (2 positions)
    'HUN': 10, 'MOS': 10,
    
    # Crypto - Infrastructure (1 position)
    'COIN': 10,
    
    # Additional positions
    'CORN': 3, 'SOYB': 5, 'WEAT': 5, 'LAC': 10,
}

def parse_current_portfolio():
    """Parse current portfolio from portfolio_summary_final.md"""
    current_portfolio = {}
    
    try:
        with open('portfolio_summary_final.md', 'r') as f:
            lines = f.readlines()
        
        # Extract all investment lines with pattern: - **$XX/week:** SYMBOL1, SYMBOL2, ...
        # Only match lines that start with "- **$"
        for line in lines:
            line = line.strip()
            if line.startswith('- **$') and '/week:**' in line:
                # Extract amount and symbols
                match = re.match(r'- \*\*\$(\d+)/week:\*\*\s*(.+)', line)
                if match:
                    amount_str, symbols_str = match.groups()
                    amount = int(amount_str)
                    # Split by comma and clean up symbols
                    symbols = [s.strip() for s in symbols_str.split(',')]
                    for symbol in symbols:
                        symbol = symbol.strip()
                        # Only add valid stock symbols (letters/numbers, 1-5 chars)
                        if symbol and re.match(r'^[A-Z0-9]{1,5}$', symbol):
                            current_portfolio[symbol] = amount
        
    except Exception as e:
        console.print(f"[red]Error parsing current portfolio: {e}[/red]")
    
    return current_portfolio

def compare_portfolios():
    """Compare original and current portfolios"""
    current_portfolio = parse_current_portfolio()
    
    original_total = sum(ORIGINAL_PORTFOLIO.values())
    current_total = sum(current_portfolio.values())
    
    original_symbols = set(ORIGINAL_PORTFOLIO.keys())
    current_symbols = set(current_portfolio.keys())
    
    removed = original_symbols - current_symbols
    added = current_symbols - original_symbols
    common = original_symbols & current_symbols
    
    # Find changed amounts
    changed = {}
    for symbol in common:
        orig_amount = ORIGINAL_PORTFOLIO[symbol]
        curr_amount = current_portfolio[symbol]
        if orig_amount != curr_amount:
            changed[symbol] = {
                'original': orig_amount,
                'current': curr_amount,
                'change': curr_amount - orig_amount
            }
    
    # Calculate removed total
    removed_total = sum(ORIGINAL_PORTFOLIO[s] for s in removed)
    
    # Calculate added total
    added_total = sum(current_portfolio[s] for s in added)
    
    # Calculate net change from modified positions
    modified_change = sum(c['change'] for c in changed.values())
    
    # Total change
    total_change = current_total - original_total
    
    return {
        'original_total': original_total,
        'current_total': current_total,
        'total_change': total_change,
        'original_positions': len(ORIGINAL_PORTFOLIO),
        'current_positions': len(current_portfolio),
        'position_change': len(current_portfolio) - len(ORIGINAL_PORTFOLIO),
        'removed': removed,
        'removed_total': removed_total,
        'added': added,
        'added_total': added_total,
        'changed': changed,
        'modified_change': modified_change,
        'original_portfolio': ORIGINAL_PORTFOLIO,
        'current_portfolio': current_portfolio
    }

def main():
    console.print("[bold blue]Portfolio Comparison Analysis[/bold blue]\n")
    
    results = compare_portfolios()
    
    # Summary Panel
    summary_text = f"""
[bold]Original Portfolio:[/bold]
  Positions: {results['original_positions']}
  Total Weekly Investment: ${results['original_total']}/week

[bold]Current Portfolio:[/bold]
  Positions: {results['current_positions']}
  Total Weekly Investment: ${results['current_total']}/week

[bold]Changes:[/bold]
  Position Count Change: {results['position_change']:+d} ({results['current_positions']} vs {results['original_positions']})
  Total Weekly Investment Change: ${results['total_change']:+.0f}/week ({results['current_total']} vs {results['original_total']})
  
[bold]Breakdown:[/bold]
  Removed Positions: {len(results['removed'])} (${results['removed_total']}/week)
  Added Positions: {len(results['added'])} (${results['added_total']}/week)
  Modified Amounts: {len(results['changed'])} (${results['modified_change']:+.0f}/week net change)
    """
    
    console.print(Panel(summary_text, title="Summary", border_style="cyan"))
    
    # Removed Positions Table
    if results['removed']:
        console.print("\n[bold red]Removed Positions[/bold red]")
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Symbol", style="cyan")
        table.add_column("Original Amount", justify="right", style="green")
        
        removed_sorted = sorted(results['removed'], key=lambda s: ORIGINAL_PORTFOLIO[s], reverse=True)
        for symbol in removed_sorted:
            table.add_row(symbol, f"${ORIGINAL_PORTFOLIO[symbol]}/week")
        
        console.print(table)
        console.print(f"[dim]Total removed: ${results['removed_total']}/week[/dim]\n")
    
    # Added Positions Table
    if results['added']:
        console.print("\n[bold green]Added Positions[/bold green]")
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Symbol", style="cyan")
        table.add_column("Current Amount", justify="right", style="green")
        
        added_sorted = sorted(results['added'], key=lambda s: results['current_portfolio'][s], reverse=True)
        for symbol in added_sorted:
            table.add_row(symbol, f"${results['current_portfolio'][symbol]}/week")
        
        console.print(table)
        console.print(f"[dim]Total added: ${results['added_total']}/week[/dim]\n")
    
    # Changed Amounts Table
    if results['changed']:
        console.print("\n[bold yellow]Modified Positions (Amount Changes)[/bold yellow]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Symbol", style="cyan")
        table.add_column("Original", justify="right", style="green")
        table.add_column("Current", justify="right", style="blue")
        table.add_column("Change", justify="right", style="yellow")
        
        changed_sorted = sorted(results['changed'].items(), 
                               key=lambda x: abs(x[1]['change']), reverse=True)
        for symbol, change_info in changed_sorted:
            change = change_info['change']
            style = "red" if change < 0 else "green"
            table.add_row(
                symbol,
                f"${change_info['original']}/week",
                f"${change_info['current']}/week",
                f"[{style}]{change:+.0f}[/{style}]"
            )
        
        console.print(table)
        console.print(f"[dim]Net change from modifications: ${results['modified_change']:+.0f}/week[/dim]\n")
    
    # Save detailed JSON report
    report = {
        'summary': {
            'original_total': results['original_total'],
            'current_total': results['current_total'],
            'total_change': results['total_change'],
            'original_positions': results['original_positions'],
            'current_positions': results['current_positions'],
            'position_change': results['position_change']
        },
        'removed': {
            'count': len(results['removed']),
            'total_weekly': results['removed_total'],
            'positions': {s: ORIGINAL_PORTFOLIO[s] for s in sorted(results['removed'])}
        },
        'added': {
            'count': len(results['added']),
            'total_weekly': results['added_total'],
            'positions': {s: results['current_portfolio'][s] for s in sorted(results['added'])}
        },
        'changed': {
            'count': len(results['changed']),
            'net_change': results['modified_change'],
            'positions': {s: change_info for s, change_info in sorted(results['changed'].items())}
        }
    }
    
    with open('portfolio_comparison_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    console.print(f"[green]✓ Detailed report saved to portfolio_comparison_report.json[/green]")

if __name__ == '__main__':
    main()

