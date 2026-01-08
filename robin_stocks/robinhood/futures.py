"""Contains functions for getting futures information."""
from robin_stocks.robinhood.helper import (
    login_required, filter_data, request_get, update_session_for_futures,
    id_for_futures_contract, get_output
)
from robin_stocks.robinhood.urls import (
    futures_contract_url, futures_quotes_url, futures_orders_url,
    futures_account_url
)


# Contract Functions

@login_required
def get_futures_contract(symbol, info=None):
    """Get futures contract details by symbol.

    :param symbol: Futures symbol (e.g., 'ESH26', 'NQM26', 'GCG26')
    :type symbol: str
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: Dictionary with contract details or filtered value

    Contract details include:

    - id: Contract instrument ID
    - symbol: Full symbol with exchange (e.g., '/ESH26:XCME')
    - displaySymbol: Display symbol (e.g., '/ESH26')
    - description: Human-readable description
    - multiplier: Contract size multiplier
    - expiration: Expiration date (YYYY-MM-DD)
    - tradability: Trading status
    - state: Contract state

    """
    symbol = symbol.upper().strip()
    url = futures_contract_url(symbol)
    update_session_for_futures()
    data = request_get(url)

    if data and 'result' in data:
        return filter_data(data['result'], info)
    return None


@login_required
def get_futures_contracts_by_symbols(symbols, info=None):
    """Get contract details for multiple futures symbols.

    :param symbols: List of futures symbols
    :type symbols: list
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: List of dictionaries with contract details

    """
    if isinstance(symbols, str):
        symbols = [symbols]

    contracts = []
    for symbol in symbols:
        contract = get_futures_contract(symbol, info=None)
        if contract:
            contracts.append(contract)

    return filter_data(contracts, info)


# Quote Functions

@login_required
def get_futures_quote(symbol, info=None):
    """Get real-time quote for a futures contract.

    :param symbol: Futures symbol (e.g., 'ESH26')
    :type symbol: str
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: Dictionary with quote data

    Quote data includes:

    - bid_price, bid_size: Current bid
    - ask_price, ask_size: Current ask
    - last_trade_price, last_trade_size: Last trade
    - state: Market state (active, closed, etc.)
    - updated_at: Last update timestamp

    """
    contract_id = id_for_futures_contract(symbol)
    if not contract_id:
        print(f"Could not find contract for symbol {symbol}", file=get_output())
        return None

    return get_futures_quote_by_id(contract_id, info)


@login_required
def get_futures_quotes(symbols, info=None):
    """Get quotes for multiple futures contracts.

    :param symbols: List of futures symbols
    :type symbols: list
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: List of dictionaries with quote data

    """
    if isinstance(symbols, str):
        symbols = [symbols]

    # Get all contract IDs
    contract_ids = []
    for symbol in symbols:
        contract_id = id_for_futures_contract(symbol)
        if contract_id:
            contract_ids.append(contract_id)

    if not contract_ids:
        return []

    # Build URL with multiple IDs
    url = futures_quotes_url()
    ids_param = ','.join(contract_ids)
    payload = {'ids': ids_param}

    update_session_for_futures()
    data = request_get(url, payload=payload)

    # Futures quotes API returns {data: [{data: {...}}]}
    if data and 'data' in data:
        quotes = [item['data'] for item in data['data'] if 'data' in item]
        return filter_data(quotes, info)
    return []


@login_required
def get_futures_quote_by_id(contract_id, info=None):
    """Get quote by contract ID directly.

    :param contract_id: Futures contract instrument ID
    :type contract_id: str
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: Dictionary with quote data

    """
    url = futures_quotes_url()
    payload = {'ids': contract_id}

    update_session_for_futures()
    data = request_get(url, payload=payload)

    # Futures quotes API returns {data: [{data: {...}}]}
    if data and 'data' in data and len(data['data']) > 0:
        quote_data = data['data'][0].get('data')
        if quote_data:
            return filter_data(quote_data, info)
    return None


# Order Functions

@login_required
def get_all_futures_orders(account_id=None, info=None):
    """Get all historical futures orders with automatic pagination.

    :param account_id: Futures account ID (if None, will attempt to auto-detect)
    :type account_id: Optional[str]
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: List of order dictionaries

    Order data includes:

    - orderId: Unique order identifier
    - orderState: FILLED, CANCELLED, REJECTED, etc.
    - orderLegs: Array with contract details
    - quantity, filledQuantity: Contract quantities
    - averagePrice: Execution price
    - realizedPnl: Nested P&L data
    - totalFee, totalCommission, totalGoldSavings: Fee breakdown
    - orderExecutions: Execution details
    - createdAt, updatedAt: Timestamps

    """
    if account_id is None:
        account_id = get_futures_account_id()
        if account_id is None:
            print("Error: Futures account ID is required. Pass it as account_id parameter.", file=get_output())
            print("To find your futures account ID:", file=get_output())
            print("1. Log in to Robinhood web app", file=get_output())
            print("2. Open browser Developer Tools (F12)", file=get_output())
            print("3. Go to Network tab", file=get_output())
            print("4. Navigate to Futures section", file=get_output())
            print("5. Look for API calls to 'ceres/v1/accounts/'", file=get_output())
            print("6. The account ID will be in the URL path", file=get_output())
            return None

    # Futures API uses cursor-based pagination (not URL-based like stocks/options)
    all_orders = []
    cursor = None
    page = 1

    update_session_for_futures()

    while True:
        payload = {'contractType': 'OUTRIGHT'}
        if cursor:
            payload['cursor'] = cursor

        url = futures_orders_url(account_id)
        data = request_get(url, payload=payload)

        if not data or 'results' not in data:
            break

        results = data['results']
        all_orders.extend(results)

        # Check for next page
        cursor = data.get('next')
        if not cursor:
            break

        print(f'Loading page {page + 1} ...', file=get_output())
        page += 1

    return filter_data(all_orders, info)


@login_required
def get_futures_order_info(order_id, account_id=None, info=None):
    """Get details for a specific futures order.

    :param order_id: The futures order ID
    :type order_id: str
    :param account_id: Futures account ID
    :type account_id: Optional[str]
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: Dictionary with order details

    """
    all_orders = get_all_futures_orders(account_id, info=None)
    if not all_orders:
        return None

    for order in all_orders:
        if order.get('orderId') == order_id:
            return filter_data(order, info)

    return None


@login_required
def get_filled_futures_orders(account_id=None, info=None):
    """Get all filled futures orders with automatic pagination.

    :param account_id: Futures account ID
    :type account_id: Optional[str]
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: List of filled orders

    """
    if account_id is None:
        account_id = get_futures_account_id()
        if account_id is None:
            print("Error: Futures account ID is required.", file=get_output())
            return None

    # Futures API uses cursor-based pagination
    all_orders = []
    cursor = None
    page = 1

    update_session_for_futures()

    while True:
        payload = {'contractType': 'OUTRIGHT', 'orderState': 'FILLED'}
        if cursor:
            payload['cursor'] = cursor

        url = futures_orders_url(account_id)
        data = request_get(url, payload=payload)

        if not data or 'results' not in data:
            break

        results = data['results']
        all_orders.extend(results)

        # Check for next page
        cursor = data.get('next')
        if not cursor:
            break

        print(f'Loading page {page + 1} ...', file=get_output())
        page += 1

    return filter_data(all_orders, info)


# P&L Helper Functions

def _extract_amount(field):
    """Extract numeric amount from nested futures amount structure.

    :param field: The nested amount field from futures API
    :type field: dict or str or float or int
    :returns: Float value of the amount

    """
    if field is None:
        return 0.0
    if isinstance(field, (int, float)):
        return float(field)
    if isinstance(field, str):
        return float(field) if field else 0.0
    if isinstance(field, dict) and 'amount' in field:
        amount = field['amount']
        return float(amount) if amount else 0.0
    return 0.0


def extract_futures_pnl(order):
    """Extract P&L values from nested futures order structure.

    :param order: Futures order dictionary
    :type order: dict
    :returns: Dictionary with extracted P&L values

    Returns dictionary with keys:

    - realized_pnl: float
    - realized_pnl_without_fees: float
    - total_fee: float
    - total_commission: float
    - total_gold_savings: float

    """
    pnl_data = {
        'realized_pnl': 0.0,
        'realized_pnl_without_fees': 0.0,
        'total_fee': 0.0,
        'total_commission': 0.0,
        'total_gold_savings': 0.0
    }

    if not order:
        return pnl_data

    # Extract nested P&L (double-nested structure)
    if 'realizedPnl' in order and order['realizedPnl']:
        realized_pnl_obj = order['realizedPnl']
        if isinstance(realized_pnl_obj, dict):
            if 'realizedPnl' in realized_pnl_obj:
                pnl_data['realized_pnl'] = _extract_amount(realized_pnl_obj['realizedPnl'])
            if 'realizedPnlWithoutFees' in realized_pnl_obj:
                pnl_data['realized_pnl_without_fees'] = _extract_amount(realized_pnl_obj['realizedPnlWithoutFees'])

    # Extract fees
    if 'totalFee' in order:
        pnl_data['total_fee'] = _extract_amount(order['totalFee'])
    if 'totalCommission' in order:
        pnl_data['total_commission'] = _extract_amount(order['totalCommission'])
    if 'totalGoldSavings' in order:
        pnl_data['total_gold_savings'] = _extract_amount(order['totalGoldSavings'])

    return pnl_data


def calculate_total_futures_pnl(orders):
    """Calculate aggregate P&L from list of futures orders.

    :param orders: List of futures order dictionaries
    :type orders: list
    :returns: Dictionary with total P&L metrics

    Returns dictionary with keys:

    - total_pnl: Total realized P&L
    - total_pnl_without_fees: Total P&L before fees
    - total_fees: Total fees paid
    - total_commissions: Total commissions paid
    - total_gold_savings: Total savings from Gold membership
    - num_orders: Number of orders processed

    """
    totals = {
        'total_pnl': 0.0,
        'total_pnl_without_fees': 0.0,
        'total_fees': 0.0,
        'total_commissions': 0.0,
        'total_gold_savings': 0.0,
        'num_orders': 0
    }

    if not orders:
        return totals

    for order in orders:
        # Only count P&L from CLOSING orders to avoid double-counting
        # OPENING orders have realizedPnl = -fees (just the cost to open)
        # CLOSING orders have realizedPnl = actual position P&L
        position_effect = order.get('positionEffectAtPlacementTime', '')
        if position_effect != 'CLOSING':
            continue

        pnl = extract_futures_pnl(order)
        totals['total_pnl'] += pnl['realized_pnl']
        totals['total_pnl_without_fees'] += pnl['realized_pnl_without_fees']
        totals['total_fees'] += pnl['total_fee']
        totals['total_commissions'] += pnl['total_commission']
        totals['total_gold_savings'] += pnl['total_gold_savings']
        totals['num_orders'] += 1

    return totals


# Account Functions (Placeholders)

@login_required
def get_futures_account_id():
    """Get the futures account ID by filtering for accountType='FUTURES'.

    :returns: Futures account ID string or None

    """
    url = futures_account_url()
    update_session_for_futures()
    data = request_get(url, dataType='results')

    # Filter for the account with accountType='FUTURES'
    if data and len(data) > 0:
        for account in data:
            if isinstance(account, dict) and account.get('accountType') == 'FUTURES':
                return account.get('id')

    return None


@login_required
def get_futures_positions(account_id=None, info=None):
    """Get current futures positions.

    NOTE: Endpoint not yet discovered. This is a placeholder.

    :param account_id: Futures account ID
    :type account_id: Optional[str]
    :param info: Will filter the results to get a specific value
    :type info: Optional[str]
    :returns: List of position dictionaries

    """
    # TODO: Implement when positions endpoint is discovered
    print("Futures positions endpoint not yet discovered", file=get_output())
    return None
