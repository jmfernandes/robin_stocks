#!/usr/bin/env python3
"""
Generate Final Portfolio Summary with Improved Categorization

Creates a comprehensive portfolio summary grouped by investment themes
"""

import os
import sys
from collections import defaultdict
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import robin_stocks.robinhood as rh

# Add repo root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(os.path.dirname(script_dir))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

console = Console()

# Theme-based categorization
THEMES = {
    'china_hong_kong': {
        'name': '🇨🇳 China/Hong Kong',
        'keywords': ['china', 'chinese', 'hong kong', 'shenzhen', 'shanghai', 'a-shares'],
        'symbols': ['KURE', 'CNXT', 'KSTR', 'ECNS', 'CXSE', 'ASHR', 'KWEB', 'TCHI', 'CQQQ', 'MCHI', 'FXI', 'EWH', 'LI', 'NIO']
    },
    'international_etfs': {
        'name': '🌍 International ETFs',
        'keywords': ['singapore', 'taiwan', 'south korea', 'israel', 'indonesia', 'poland', 'emerging markets', 'developed markets'],
        'symbols': ['EWS', 'FLTW', 'ISRA', 'FLKR', 'IDX', 'EIDO', 'GVAL', 'FRDM', 'EPOL', 'EWY', 'EIS', 'IZRL', 'EWT', 'VEA', 'QQQ', 'SPY']
    },
    'defense_aerospace': {
        'name': '🛡️ Defense/Aerospace',
        'keywords': ['defense', 'aerospace', 'military'],
        'symbols': ['MISL', 'PPA', 'SHLD', 'ESLT', 'HON']
    },
    'technology_semiconductors': {
        'name': '💻 Technology - Semiconductors',
        'keywords': ['semiconductor'],
        'symbols': ['NVDA', 'AMD', 'AAPL', 'LINK']
    },
    'technology_quantum': {
        'name': '⚛️ Technology - Quantum Computing',
        'keywords': ['quantum'],
        'symbols': ['QUBT', 'IONQ', 'RGTI', 'QBTS', 'QTUM']
    },
    'technology_software': {
        'name': '🔧 Technology - Software/Cloud',
        'keywords': ['software', 'cloud', 'automation'],
        'symbols': ['MSFT', 'GOOG', 'GOOGL', 'META', 'PLTR', 'PATH', 'ZM', 'CRM', 'MSTR', 'COMP', 'SNAP', 'U']
    },
    'technology_innovation_etfs': {
        'name': '🚀 Technology - Innovation ETFs',
        'keywords': ['innovation', 'disruption', 'metaverse'],
        'symbols': ['ARKK', 'ARKW', 'METV', 'BOTZ', 'ARKG']
    },
    'transportation_ev': {
        'name': '🚗 Transportation - EV Manufacturers',
        'keywords': ['electric vehicle', 'ev', 'automotive'],
        'symbols': ['TSLA', 'F', 'LI', 'RIVN', 'NIO', 'DHI']
    },
    'transportation_mobility': {
        'name': '🚕 Transportation - Mobility/Rideshare',
        'keywords': ['rideshare', 'mobility'],
        'symbols': ['LYFT', 'UBER']
    },
    'transportation_aviation': {
        'name': '✈️ Transportation - Aviation/Space',
        'keywords': ['aviation', 'space', 'rocket'],
        'symbols': ['ACHR', 'JOBY', 'RKLB']
    },
    'transportation_logistics': {
        'name': '📦 Transportation - Logistics',
        'keywords': ['logistics', 'shipping', 'transportation'],
        'symbols': ['WERN', 'DAC']
    },
    'ev_supply_chain': {
        'name': '🔋 EV Supply Chain - Lithium/Batteries',
        'keywords': ['lithium', 'battery'],
        'symbols': ['LIT', 'ALB']
    },
    'finance_reits': {
        'name': '🏢 Finance - REITs',
        'keywords': ['reit', 'real estate'],
        'symbols': ['PLD', 'AHR', 'O', 'APLE', 'LTC']
    },
    'finance_services': {
        'name': '💳 Finance - Financial Services',
        'keywords': ['financial services', 'banking', 'payment'],
        'symbols': ['HOOD', 'V', 'AGM', 'RM', 'CME', 'BCH', 'MAIN']
    },
    'crypto_infrastructure': {
        'name': '₿ Crypto - Infrastructure',
        'keywords': ['crypto exchange'],
        'symbols': ['COIN']
    },
    'cryptocurrency': {
        'name': '₿ Crypto - Cryptocurrency',
        'keywords': ['bitcoin', 'ethereum', 'crypto'],
        'symbols': ['BTC', 'ETH', 'XRP', 'SOL', 'SHIB', 'DOGE', 'ETC']
    },
    'crypto_mining': {
        'name': '⛏️ Crypto - Mining',
        'keywords': ['mining'],
        'symbols': ['RIOT', 'MARA']
    },
    'precious_metals': {
        'name': '💎 Commodities - Precious Metals',
        'keywords': ['gold', 'silver', 'precious metals'],
        'symbols': ['GDX', 'SLV', 'RING', 'PAAS']
    },
    'base_metals': {
        'name': '🔩 Commodities - Base Metals',
        'keywords': ['copper', 'metals', 'materials'],
        'symbols': ['DBB', 'ICOP', 'MP']
    },
    'healthcare_pharma': {
        'name': '💊 Healthcare - Pharmaceuticals',
        'keywords': ['pharmaceutical', 'pharma'],
        'symbols': ['IHE', 'PFE', 'JNJ', 'MRNA', 'RARE']
    },
    'healthcare_services': {
        'name': '🏥 Healthcare - Services',
        'keywords': ['healthcare', 'health services', 'medical'],
        'symbols': ['UNH', 'BKD', 'XLV', 'KURE']
    },
    'consumer_retail': {
        'name': '🛒 Consumer - Retail',
        'keywords': ['retail', 'e-commerce'],
        'symbols': ['WMT', 'COST', 'KR', 'AMZN', 'GME']
    },
    'consumer_hospitality': {
        'name': '🏨 Consumer - Hospitality',
        'keywords': ['hospitality', 'hotel', 'travel'],
        'symbols': ['HLT', 'ABNB', 'DIS']
    },
    'industrial_infrastructure': {
        'name': '🏭 Industrial - Infrastructure',
        'keywords': ['infrastructure', 'construction', 'waste'],
        'symbols': ['WM', 'ACM', 'ENB', 'EPD']
    },
    'industrial_materials': {
        'name': '🧪 Industrial - Materials/Chemicals',
        'keywords': ['chemicals', 'materials', 'process'],
        'symbols': ['HUN', 'MOS', 'ALB']
    },
    'energy_clean': {
        'name': '⚡ Energy - Clean/Renewable',
        'keywords': ['clean energy', 'renewable', 'nuclear', 'solar', 'wind'],
        'symbols': ['ICLN', 'OKLO']
    },
    'us_broad_market': {
        'name': '🇺🇸 US - Broad Market ETFs',
        'keywords': ['s&p', 'nasdaq', 'broad market', 'total market'],
        'symbols': ['SPY', 'QQQ', 'VEA']
    }
}

def get_theme(symbol, description, sector, industry):
    """Determine theme for an investment"""
    symbol_upper = symbol.upper()
    text = f"{symbol} {description or ''} {sector or ''} {industry or ''}".lower()
    
    # Check symbol matches first (more specific) - check in order of specificity
    # Check crypto first (most specific)
    if symbol_upper in ['BTC', 'ETH', 'XRP', 'SOL', 'SHIB', 'DOGE', 'ETC']:
        return 'cryptocurrency'
    if symbol_upper in ['RIOT', 'MARA']:
        return 'crypto_mining'
    if symbol_upper == 'COIN':
        return 'crypto_infrastructure'
    
    # Check other symbol matches
    for theme_key, theme_data in THEMES.items():
        if symbol_upper in theme_data['symbols']:
            return theme_key
    
    # Then check keywords (but skip if already matched)
    for theme_key, theme_data in THEMES.items():
        for keyword in theme_data['keywords']:
            if keyword in text:
                return theme_key
    
    # If still not found, try to infer from sector/industry
    if 'etf' in text or 'investment trust' in text or 'mutual fund' in text:
        if 'china' in text or 'chinese' in text or 'hong kong' in text:
            return 'china_hong_kong'
        elif 'international' in text or 'global' in text or 'emerging' in text:
            return 'international_etfs'
        elif 'us' in text or 's&p' in text or 'nasdaq' in text:
            return 'us_broad_market'
    
    return 'other'

def main():
    # Login
    load_dotenv()
    username = os.getenv('robin_username')
    password = os.getenv('robin_password')
    mfa_secret = os.getenv('robin_mfa')
    
    console.print("[cyan]Logging in...[/cyan]")
    if mfa_secret:
        import pyotp
        totp = pyotp.TOTP(mfa_secret)
        mfa_code = totp.now()
        rh.login(username, password, mfa_code=mfa_code)
    else:
        rh.login(username, password)
    console.print("[green]✓ Logged in[/green]\n")
    
    # Enable rate limiting
    rh.enable_rate_limiting(delay=1.0)
    
    # Get all recurring investments
    console.print("[cyan]Fetching recurring investments...[/cyan]")
    investments = rh.get_recurring_investments(asset_types=['equity', 'crypto'])
    
    if isinstance(investments, dict):
        results = investments.get('results', [])
    else:
        results = investments if isinstance(investments, list) else []
    
    # Fetch fundamentals for all symbols
    unique_symbols = set()
    for inv in results:
        if inv.get('state', '').lower() == 'active':
            symbol = inv.get('investment_target', {}).get('instrument_symbol', 'N/A')
            if symbol != 'N/A':
                unique_symbols.add(symbol)
    
    console.print("[cyan]Fetching company information...[/cyan]")
    fundamentals_data = {}
    symbols_list = list(unique_symbols)
    chunk_size = 50
    for i in range(0, len(symbols_list), chunk_size):
        chunk = symbols_list[i:i + chunk_size]
        try:
            fundamentals_list = rh.get_fundamentals(chunk)
            if fundamentals_list:
                for fund in fundamentals_list:
                    if fund and fund.get('symbol'):
                        fundamentals_data[fund['symbol']] = fund
        except Exception as e:
            pass
    
    # Organize by theme
    by_theme = defaultdict(list)
    total_weekly = 0
    
    for inv in results:
        state = inv.get('state', '').lower()
        if state == 'active':
            symbol = inv.get('investment_target', {}).get('instrument_symbol', 'N/A')
            amount = float(inv.get('amount', {}).get('amount', 0))
            frequency = inv.get('frequency', '').lower()
            schedule_id = inv.get('id', 'N/A')
            
            if frequency == 'weekly':
                weekly_amount = amount
            else:
                continue  # Skip non-weekly (shouldn't happen)
            
            # Get company info
            fund = fundamentals_data.get(symbol, {})
            description = fund.get('description', 'N/A')
            sector = fund.get('sector', 'N/A')
            industry = fund.get('industry', 'N/A')
            
            theme = get_theme(symbol, description, sector, industry)
            by_theme[theme].append({
                'symbol': symbol,
                'amount': weekly_amount,
                'schedule_id': schedule_id
            })
            total_weekly += weekly_amount
    
    # Generate summary
    output_lines = []
    output_lines.append("# 📊 FINAL PORTFOLIO SUMMARY")
    output_lines.append("")
    output_lines.append(f"**Total Weekly Investment:** ${total_weekly:.0f}/week")
    output_lines.append(f"**Total Active Positions:** {sum(len(inv) for inv in by_theme.values())} positions")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    
    # Sort themes by total amount
    theme_totals = {}
    for theme, invs in by_theme.items():
        theme_totals[theme] = sum(inv['amount'] for inv in invs)
    
    sorted_themes = sorted(theme_totals.items(), key=lambda x: x[1], reverse=True)
    
    for theme_key, theme_total in sorted_themes:
        if theme_key == 'other':
            continue
        
        theme_name = THEMES[theme_key]['name']
        invs = by_theme[theme_key]
        total = sum(inv['amount'] for inv in invs)
        percentage = (total / total_weekly * 100) if total_weekly > 0 else 0
        
        output_lines.append(f"### {theme_name} ({percentage:.1f}% - ${total:.0f}/week)")
        output_lines.append(f"**{len(invs)} positions**")
        output_lines.append("")
        
        # Group by amount tier
        by_tier = defaultdict(list)
        for inv in invs:
            by_tier[inv['amount']].append(inv['symbol'])
        
        for tier in sorted(by_tier.keys(), reverse=True):
            symbols = sorted(by_tier[tier])
            output_lines.append(f"- **${tier:.0f}/week:** {', '.join(symbols)}")
        
        output_lines.append("")
    
    # Handle 'other' theme - only show if there are any
    if 'other' in by_theme and len(by_theme['other']) > 0:
        invs = by_theme['other']
        total = sum(inv['amount'] for inv in invs)
        percentage = (total / total_weekly * 100) if total_weekly > 0 else 0
        
        output_lines.append(f"### ❓ Other/Uncategorized ({percentage:.1f}% - ${total:.0f}/week)")
        output_lines.append(f"**{len(invs)} positions** - *These investments need manual categorization*")
        output_lines.append("")
        
        by_tier = defaultdict(list)
        for inv in invs:
            by_tier[inv['amount']].append(inv['symbol'])
        
        for tier in sorted(by_tier.keys(), reverse=True):
            symbols = sorted(by_tier[tier])
            output_lines.append(f"- **${tier:.0f}/week:** {', '.join(symbols)}")
        
        output_lines.append("")
    
    # Summary statistics
    output_lines.append("---")
    output_lines.append("")
    output_lines.append("## 📈 SUMMARY STATISTICS")
    output_lines.append("")
    
    # Combined crypto total
    crypto_themes = ['cryptocurrency', 'crypto_mining', 'crypto_infrastructure']
    crypto_total = sum(theme_totals.get(theme, 0) for theme in crypto_themes)
    crypto_count = sum(len(by_theme.get(theme, [])) for theme in crypto_themes)
    crypto_percentage = (crypto_total / total_weekly * 100) if total_weekly > 0 else 0
    
    output_lines.append("### 💰 Combined Crypto Exposure:")
    output_lines.append(f"- **Total:** {crypto_percentage:.1f}% (${crypto_total:.0f}/week) across {crypto_count} positions")
    output_lines.append(f"  - Cryptocurrency: ${theme_totals.get('cryptocurrency', 0):.0f}/week ({len(by_theme.get('cryptocurrency', []))} positions)")
    output_lines.append(f"  - Mining: ${theme_totals.get('crypto_mining', 0):.0f}/week ({len(by_theme.get('crypto_mining', []))} positions)")
    output_lines.append(f"  - Infrastructure: ${theme_totals.get('crypto_infrastructure', 0):.0f}/week ({len(by_theme.get('crypto_infrastructure', []))} positions)")
    output_lines.append("")
    
    # Top 10 themes (excluding crypto subcategories for cleaner view)
    non_crypto_themes = [(k, v) for k, v in sorted_themes if k not in crypto_themes]
    output_lines.append("### Top 10 Themes by Investment:")
    for i, (theme_key, theme_total) in enumerate(non_crypto_themes[:10], 1):
        theme_name = THEMES.get(theme_key, {}).get('name', theme_key.replace('_', ' ').title())
        percentage = (theme_total / total_weekly * 100) if total_weekly > 0 else 0
        output_lines.append(f"{i}. **{theme_name}:** {percentage:.1f}% (${theme_total:.0f}/week)")
    
    output_lines.append("")
    
    # Tier breakdown
    all_amounts = []
    for invs in by_theme.values():
        for inv in invs:
            all_amounts.append(inv['amount'])
    
    tier_counts = defaultdict(int)
    for amount in all_amounts:
        tier_counts[amount] += 1
    
    output_lines.append("### Investment Tiers:")
    for tier in sorted(tier_counts.keys(), reverse=True):
        count = tier_counts[tier]
        total_tier = tier * count
        output_lines.append(f"- **${tier:.0f}/week:** {count} investments (${total_tier:.0f}/week total)")
    
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    output_lines.append("**Note:** All investments are weekly frequency with whole dollar amounts on standard tiers ($10, $20, $25, $50, $100).")
    
    # Write to file
    output_file = os.path.join(repo_root, 'portfolio_summary_final.md')
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))
    
    console.print(f"\n[green]✓ Portfolio summary generated![/green]")
    console.print(f"[dim]Saved to: {output_file}[/dim]\n")
    
    # Display summary
    console.print(Panel.fit(
        f"[bold]Portfolio Summary[/bold]\n\n"
        f"Total Weekly: [green]${total_weekly:.0f}/week[/green]\n"
        f"Total Positions: [cyan]{sum(len(inv) for inv in by_theme.values())}[/cyan]\n"
        f"Themes: [yellow]{len(sorted_themes)}[/yellow]",
        border_style="cyan"
    ))

if __name__ == '__main__':
    main()

