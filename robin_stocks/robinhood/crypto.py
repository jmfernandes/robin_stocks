"""Contains functions to get information about crypto-currencies."""
from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.urls import *

@login_required
def load_crypto_profile(info=None):
    """Gets the information associated with the crypto account.

    :param info: The name of the key whose value is to be returned from the function.
    :type info: Optional[str]
    :returns: [dict] The function returns a dictionary of key/value pairs. \
    If a string is passed in to the info parameter, then the function will return \
    a string corresponding to the value of the key whose name matches the info parameter.
    :Dictionary Keys: * apex_account_number
                      * created_at
                      * id
                      * rhs_account_number
                      * status
                      * status_reason_code
                      * updated_at
                      * user_id

    """
    url = crypto_account_url()
    data = request_get(url, 'indexzero')
    return(filter_data(data, info))


@login_required
def get_crypto_positions(info=None):
    """Returns crypto positions for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * account_id
                      * cost_basis
                      * created_at
                      * currency
                      * id
                      * quantity
                      * quantity_available
                      * quantity_held_for_buy
                      * quantity_held_for_sell
                      * updated_at

    """
    url = crypto_holdings_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


def get_crypto_currency_pairs(info=None):
    """Gets a list of all the cypto currencies that you can trade.

    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [list] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * asset_currency
                      * display_only
                      * id
                      * max_order_size
                      * min_order_size
                      * min_order_price_increment
                      * min_order_quantity_increment
                      * name
                      * quote_currency
                      * symbol
                      * tradability

    """
    url = crypto_currency_pairs_url()
    data = request_get(url, 'results')
    return(filter_data(data, info))


def get_crypto_info(symbol, info=None):
    """Gets information about a crpyto currency.

    :param symbol: The crypto ticker.
    :type symbol: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [dict] If info parameter is left as None then will return a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a strings representing the value of the key.
    :Dictionary Keys: * asset_currency
                      * display_only
                      * id
                      * max_order_size
                      * min_order_size
                      * min_order_price_increment
                      * min_order_quantity_increment
                      * name
                      * quote_currency
                      * symbol
                      * tradability

    """
    url = crypto_currency_pairs_url()
    data = request_get(url, 'results')
    data = [x for x in data if x['asset_currency']['code'] == symbol]
    if len(data) > 0:
        data = data[0]
    else:
        data = None
    return(filter_data(data, info))


SYMBOL_TO_ID_CACHE = {}
def get_crypto_id(symbol):
    """Gets the Robinhood ID of the given cryptocurrency used to make trades.
    This function uses an in-memory cache of the IDs to save a network round-trip when possible.

    :param symbol: The crypto ticker.
    :type symbol: str
    :returns: [str] The symbol's Robinhood ID.
    """
    if symbol in SYMBOL_TO_ID_CACHE:
        return SYMBOL_TO_ID_CACHE[symbol]

    id = get_crypto_info(symbol, 'id')
    if id:
        SYMBOL_TO_ID_CACHE[symbol] = id
    return id


@login_required
def get_crypto_quote(symbol, info=None):
    """Gets information about a crypto including low price, high price, and open price

    :param symbol: The crypto ticker.
    :type symbol: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [dict] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * ask_price
                      * bid_price
                      * high_price
                      * id
                      * low_price
                      * mark_price
                      * open_price
                      * symbol
                      * volume
 
    """
    id = get_crypto_info(symbol, info='id')
    url = crypto_quote_url(id)
    data = request_get(url)
    return(filter_data(data, info))


@login_required
def get_crypto_quote_from_id(id, info=None):
    """Gets information about a crypto including low price, high price, and open price. Uses the id instead of crypto ticker.

    :param id: The id of a crypto.
    :type id: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [dict] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * ask_price
                      * bid_price
                      * high_price
                      * id
                      * low_price
                      * mark_price
                      * open_price
                      * symbol
                      * volume

    """
    url = crypto_quote_url(id)
    data = request_get(url)
    return(filter_data(data, info))


@login_required
def get_crypto_historicals(symbol, interval='hour', span='week', bounds='24_7', info=None):
    """Gets historical information about a crypto including open price, close price, high price, and low price.

    :param symbol: The crypto ticker.
    :type symbol: str
    :param interval: The time between data points. Can be '15second', '5minute', '10minute', 'hour', 'day', or 'week'. Default is 'hour'.
    :type interval: str
    :param span: The entire time frame to collect data points. Can be 'hour', 'day', 'week', 'month', '3month', 'year', or '5year'. Default is 'week'
    :type span: str
    :param bound: The times of day to collect data points. 'Regular' is 6 hours a day, 'trading' is 9 hours a day, \
    'extended' is 16 hours a day, '24_7' is 24 hours a day. Default is '24_7'
    :type bound: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [list] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * begins_at
                      * open_price
                      * close_price
                      * high_price
                      * low_price
                      * volume
                      * session
                      * interpolated
                      * symbol

    """
    interval_check = ['15second', '5minute', '10minute', 'hour', 'day', 'week']
    span_check = ['hour', 'day', 'week', 'month', '3month', 'year', '5year']
    bounds_check = ['24_7', 'extended', 'regular', 'trading']

    if interval not in interval_check:
        print(
            'ERROR: Interval must be "15second","5minute","10minute","hour","day",or "week"', file=get_output())
        return([None])
    if span not in span_check:
        print('ERROR: Span must be "hour","day","week","month","3month","year",or "5year"', file=get_output())
        return([None])
    if bounds not in bounds_check:
        print('ERROR: Bounds must be "24_7","extended","regular",or "trading"', file=get_output())
        return([None])
    if (bounds == 'extended' or bounds == 'trading') and span != 'day':
        print('ERROR: extended and trading bounds can only be used with a span of "day"', file=get_output())
        return([None])


    symbol = inputs_to_set(symbol)
    id = get_crypto_info(symbol[0], info='id')
    url = crypto_historical_url(id)
    payload = {'interval': interval,
               'span': span,
               'bounds': bounds}
    data = request_get(url, 'regular', payload)

    histData = []
    cryptoSymbol = data['symbol']
    for subitem in data['data_points']:
        subitem['symbol'] = cryptoSymbol
        histData.append(subitem)

    return(filter_data(histData, info))
