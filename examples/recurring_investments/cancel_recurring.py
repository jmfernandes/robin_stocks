#!/usr/bin/env python3
"""
Example: Cancel a Recurring Investment

This script demonstrates how to cancel a recurring investment by its schedule ID.
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
    
    # First, get all recurring investments to find the one you want to cancel
    print("Fetching recurring investments...")
    investments = rh.get_recurring_investments(asset_types=['equity', 'crypto'])
    
    if isinstance(investments, dict):
        results = investments.get('results', [])
    else:
        results = investments if isinstance(investments, list) else []
    
    if not results:
        print("No recurring investments found.")
        return
    
    print(f"\nFound {len(results)} recurring investments:\n")
    for i, inv in enumerate(results[:10]):  # Show first 10
        symbol = inv.get('investment_target', {}).get('instrument_symbol', 'N/A')
        amount = inv.get('amount', {}).get('amount', 'N/A')
        frequency = inv.get('frequency', 'N/A')
        state = inv.get('state', 'N/A')
        schedule_id = inv.get('id', 'N/A')
        
        print(f"  {i+1}. {symbol}: ${amount} {frequency} ({state})")
        print(f"     ID: {schedule_id}")
        print()
    
    # Example: Cancel the first active investment
    # In a real script, you'd ask the user which one to cancel
    active_investments = [inv for inv in results if inv.get('state') == 'active']
    
    if not active_investments:
        print("No active recurring investments to cancel.")
        return
    
    # Cancel the first active one (you can modify this logic)
    to_cancel = active_investments[0]
    schedule_id = to_cancel.get('id')
    symbol = to_cancel.get('investment_target', {}).get('instrument_symbol', 'Unknown')
    
    print(f"\nCancelling recurring investment for {symbol} (ID: {schedule_id[:8]}...)...")
    result = rh.cancel_recurring_investment(schedule_id)
    
    if result and result.get('state') == 'deleted':
        print(f"\n✓ Successfully cancelled recurring investment for {symbol}!")
    else:
        print(f"\n✗ Failed to cancel recurring investment")

if __name__ == '__main__':
    main()

