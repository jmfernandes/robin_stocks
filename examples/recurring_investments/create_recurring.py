#!/usr/bin/env python3
"""
Example: Create a Recurring Investment

This script demonstrates how to create a new recurring investment.
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
    
    # Create a recurring investment
    symbol = 'SPY'  # Change this to your desired symbol
    amount = 10.00  # Change this to your desired amount
    frequency = 'weekly'  # Options: 'daily', 'weekly', 'biweekly', 'monthly'
    
    print(f"Creating recurring investment: ${amount} {frequency} for {symbol}...")
    result = rh.create_recurring_investment(
        symbol=symbol,
        amount=amount,
        frequency=frequency
    )
    
    if result:
        print(f"\n✓ Successfully created recurring investment!")
        print(f"  Schedule ID: {result.get('id')}")
        print(f"  Symbol: {result.get('investment_target', {}).get('instrument_symbol')}")
        print(f"  Amount: ${result.get('amount', {}).get('amount')}")
        print(f"  Frequency: {result.get('frequency')}")
        print(f"  State: {result.get('state')}")
        print(f"  Next investment date: {result.get('next_investment_date')}")
    else:
        print("\n✗ Failed to create recurring investment")

if __name__ == '__main__':
    main()

