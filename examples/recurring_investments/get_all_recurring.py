#!/usr/bin/env python3
"""
Example: Get All Recurring Investments

This script demonstrates how to fetch all your recurring investments from Robinhood.
"""

import os
from dotenv import load_dotenv
import robin_stocks.robinhood as rh

# Load environment variables
load_dotenv()

def main():
    # Login
    username = os.getenv('robin_username')
    password = os.getenv('robin_password')
    mfa_secret = os.getenv('robin_mfa')
    
    print("Logging in...")
    if mfa_secret:
        import pyotp
        totp = pyotp.TOTP(mfa_secret)
        mfa_code = totp.now()
        rh.login(username, password, mfa_code=mfa_code)
    else:
        rh.login(username, password)
    print("✓ Logged in\n")
    
    # Get all recurring investments
    print("Fetching recurring investments...")
    investments = rh.get_recurring_investments(asset_types=['equity', 'crypto'])
    
    # Handle response format
    if isinstance(investments, dict):
        results = investments.get('results', [])
    else:
        results = investments if isinstance(investments, list) else []
    
    print(f"\nFound {len(results)} recurring investments:\n")
    
    for inv in results:
        symbol = inv.get('investment_target', {}).get('instrument_symbol', 'N/A')
        amount = inv.get('amount', {}).get('amount', 'N/A')
        frequency = inv.get('frequency', 'N/A')
        state = inv.get('state', 'N/A')
        next_date = inv.get('next_investment_date', 'N/A')
        schedule_id = inv.get('id', 'N/A')
        
        print(f"  {symbol}: ${amount} {frequency}")
        print(f"    State: {state}")
        print(f"    Next investment: {next_date}")
        print(f"    ID: {schedule_id[:8]}...")
        print()

if __name__ == '__main__':
    main()

