"""Contains functions for managing recurring investments."""
from datetime import datetime

from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.profiles import *
from robin_stocks.robinhood.stocks import *
from robin_stocks.robinhood.urls import *
from robin_stocks.robinhood.globals import SESSION


@login_required
def get_recurring_investments(info=None, account_number=None, asset_types=None, jsonify=True):
    """Returns a list of all recurring investments for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :param account_number: Filter by account number (optional).
    :type account_number: Optional[str]
    :param asset_types: Filter by asset types, e.g., ['equity', 'crypto'] (optional).
    :type asset_types: Optional[list]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[bool]
    :returns: Returns a list of dictionaries of key/value pairs for each recurring investment. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = recurring_schedules_url(account_number=account_number, asset_types=asset_types)
    data = request_get(url, 'pagination', jsonify_data=jsonify)
    return(filter_data(data, info))


@login_required
def create_recurring_investment(symbol, amount, frequency='weekly', start_date=None, 
                                account_number=None, source_of_funds='buying_power', jsonify=True):
    """Creates a new recurring investment schedule.

    :param symbol: Stock or ETF symbol to invest in.
    :type symbol: str
    :param amount: Dollar amount to invest per period (minimum $1.00).
    :type amount: float
    :param frequency: Investment frequency - 'daily', 'weekly', 'biweekly', or 'monthly'.
    :type frequency: Optional[str]
    :param start_date: Start date in YYYY-MM-DD format (defaults to today).
    :type start_date: Optional[str]
    :param account_number: Account number (optional, auto-detected if not provided).
    :type account_number: Optional[str]
    :param source_of_funds: Source of funds - 'buying_power' or 'ach_relationship'.
    :type source_of_funds: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[bool]
    :returns: Dictionary containing the created recurring investment details.

    """
    if not account_number:
        account_data = load_account_profile(account_number=account_number)
        account_number = account_data.get('account_number')
    
    if not account_number:
        print("ERROR: Could not get account number", file=get_output())
        return None
    
    # Get instrument ID
    instrument_data = get_instruments_by_symbols(symbol)
    if not instrument_data:
        print(f"ERROR: Could not find instrument for {symbol}", file=get_output())
        return None
    
    instrument_id = instrument_data[0].get('id')
    if not instrument_id:
        print(f"ERROR: Could not get instrument ID for {symbol}", file=get_output())
        return None
    
    # Format start date
    if not start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    # Build payload
    payload = {
        "amount": {
            "amount": str(amount),
            "currency_code": "USD"
        },
        "frequency": frequency,
        "start_date": start_date,
        "investment_target": {
            "instrument_id": instrument_id,
            "instrument_symbol": symbol.upper(),
            "target_type": "instrument"
        },
        "source_of_funds": source_of_funds
    }
    
    url = recurring_schedules_url(account_number=account_number)
    data = request_post(url, payload, json=True, jsonify_data=jsonify)
    return data


@login_required
def update_recurring_investment(schedule_id, account_number=None, amount=None, 
                                frequency=None, state=None, start_date=None, jsonify=True):
    """Updates an existing recurring investment.

    :param schedule_id: ID of the recurring investment to update.
    :type schedule_id: str
    :param account_number: Account number (optional).
    :type account_number: Optional[str]
    :param amount: New dollar amount (optional).
    :type amount: Optional[float]
    :param frequency: New frequency - 'daily', 'weekly', 'biweekly', 'monthly' (optional).
    :type frequency: Optional[str]
    :param state: New state - 'active' or 'paused' (optional).
    :type state: Optional[str]
    :param start_date: New start date in YYYY-MM-DD format (optional).
    :type start_date: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[bool]
    :returns: Dictionary containing updated recurring investment details.

    """
    if not account_number:
        account_data = load_account_profile(account_number=account_number)
        account_number = account_data.get('account_number')
        if not account_number:
            print("ERROR: Could not get account number", file=get_output())
            return None
    
    # Build payload with only provided fields
    payload = {}
    if amount is not None:
        payload["amount"] = {
            "amount": str(amount),
            "currency_code": "USD"
        }
    if frequency is not None:
        payload["frequency"] = frequency
    if state is not None:
        payload["state"] = state
    if start_date is not None:
        payload["start_date"] = start_date
    
    if not payload:
        print("ERROR: No fields to update", file=get_output())
        return None
    
    url = recurring_schedules_url(schedule_id=schedule_id)
    data = request_post(url, payload, json=True, jsonify_data=jsonify)
    return data


@login_required
def cancel_recurring_investment(schedule_id, jsonify=True):
    """Cancels/deletes a recurring investment by setting its state to "deleted".

    Note: Robinhood doesn't actually DELETE the recurring investment - it uses PATCH
    to set the state to "deleted". This is the correct way to cancel a recurring investment.

    :param schedule_id: ID of the recurring investment to cancel.
    :type schedule_id: str
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[bool]
    :returns: Dictionary containing the updated recurring investment with state="deleted", or None if failed.

    """
    # Robinhood uses PATCH with state="deleted" instead of DELETE
    url = recurring_schedules_url(schedule_id=schedule_id)
    payload = {"state": "deleted"}
    
    # Use SESSION.patch() directly since request_post doesn't support PATCH
    try:
        update_session('Content-Type', 'application/json')
        res = SESSION.patch(url, json=payload, timeout=16)
        update_session('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
        
        if res.status_code not in [200, 201, 202, 204]:
            print(f"Error canceling recurring investment: HTTP {res.status_code}", file=get_output())
            return None
        
        if jsonify:
            return res.json()
        else:
            return res
    except Exception as message:
        print(f"Error canceling recurring investment: {message}", file=get_output())
        return None


@login_required
def get_next_investment_date(frequency='weekly', start_date=None, jsonify=True):
    """Gets the next investment date for a given frequency and start date.

    :param frequency: Investment frequency - 'daily', 'weekly', 'biweekly', or 'monthly'.
    :type frequency: Optional[str]
    :param start_date: Start date in YYYY-MM-DD format (defaults to today).
    :type start_date: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[bool]
    :returns: Dictionary with next_investment_date, or None if failed.

    """
    if not start_date:
        start_date = datetime.now().strftime('%Y-%m-%d')
    
    url = next_investment_date_url(frequency, start_date)
    data = request_get(url, jsonify_data=jsonify)
    return data

