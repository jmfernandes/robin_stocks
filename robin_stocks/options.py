"""Contains functions for getting information about options."""
from pprint import pprint as pp

import robin_stocks.helper as helper
import robin_stocks.urls as urls


@helper.login_required
def get_aggregate_positions(info=None):
    """Collapses all option orders for a stock into a single dictionary.

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.aggregate()
    data = helper.request_get(url, 'pagination')
    return helper.data_filter(data, info)


@helper.login_required
def get_market_options(info=None):
    """Returns a list of all options.

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.option_orders()
    data = helper.request_get(url, 'pagination')

    return helper.data_filter(data, info)


@helper.login_required
def get_all_option_positions(info=None):
    """Returns all option positions ever held for the account.

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.option_positions()
    data = helper.request_get(url, 'pagination')
    return helper.data_filter(data, info)


@helper.login_required
def get_open_option_positions(info=None):
    """Returns all open option positions for the account.

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.option_positions()
    payload = {'nonzero': 'True'}
    data = helper.request_get(url, 'pagination', payload)

    return helper.data_filter(data, info)


def get_chains(symbol, info=None):
    """Returns the chain information of an option.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = urls.chains(symbol)
    data = helper.request_get(url)

    return helper.data_filter(data, info)


def find_tradable_options_for_stock(symbol, option_type='both', info=None):
    """Returns a list of all available options for a stock.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param option_type: Can be either 'call' or 'put' or left blank to get both.
    :type option_type: Optional[str]
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all calls of the stock. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
        option_type = option_type.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    url = urls.option_instruments()
    if option_type == 'call' or option_type == 'put':
        payload = {'chain_id': helper.id_for_chain(symbol),
                   'state': 'active',
                   'tradability': 'tradable',
                   'type': option_type}
    else:
        payload = {'chain_id': helper.id_for_chain(symbol),
                   'state': 'active',
                   'tradability': 'tradable'}

    data = helper.request_get(url, 'pagination', payload)
    return helper.data_filter(data, info)


def id_of_options_to_close(symbol, expiration_date, strike, option_type, count=0, _type='long'):
    """

    :param symbol:
    :param expiration_date:
    :param strike:
    :param option_type:
    :param count:
    :param _type:
    :return: only when option exists in open position else return None
    """

    data = get_open_option_positions()
    msg = "ZERO holdings in open position to close"
    pp(data)
    for item in filter(lambda x: symbol == x['chain_symbol'] and _type == x['type'], data):
        per_data = helper.request_get(item['option'])
        if per_data['expiration_date'] == expiration_date and float(per_data["strike_price"]) == float(strike) and \
                per_data['type'] == option_type:
            if int(count) <= int(float(item['quantity'])):
                return per_data['id']
            else:
                msg = "NOT enough quantity to close. holding {} < {}".format(count, int(float(item['quantity'])))
    print(msg)
    return None


def find_options_for_stock_by_expiration(symbol, expiration_date, option_type='both', info=None):
    """Returns a list of all the option orders that match the seach parameters

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
    :type expiration_date: str
    :param option_type: Can be either 'call' or 'put' or leave blank to get both.
    :type option_type: Optional[str]
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
        option_type = option_type.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    all_options = find_tradable_options_for_stock(symbol, option_type)
    filtered_options = [item for item in all_options if item["expiration_date"] == expiration_date
                        and item['tradability'] == 'tradable']

    for item in filtered_options:
        market_data = get_option_market_data_by_id(item['id'])
        item.update(market_data)

    return helper.data_filter(filtered_options, info)


def find_options_for_stock_by_strike(symbol, strike, option_type='both', info=None):
    """Returns a list of all the option orders that match the seach parameters

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param option_type: Can be either 'call' or 'put' or leave blank to get both.
    :type option_type: Optional[str]
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
        option_type = option_type.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    all_options = find_tradable_options_for_stock(symbol, option_type)
    filtered_options = [item for item in all_options if float(item["strike_price"]) == float(strike)
                        and item['tradability'] == 'tradable']

    for item in filtered_options:
        market_data = get_option_market_data_by_id(item['id'])
        item.update(market_data)

    return helper.data_filter(filtered_options, info)


def find_options_for_stock_by_expiration_and_strike(symbol, expiration_date, strike, option_type='both', info=None):
    """Returns a list of all the option orders that match the seach parameters

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
    :type expiration_date: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param option_type: Can be either 'call' or 'put' or leave blank to get both.
    :type option_type: Optional[str]
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
        option_type = option_type.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    all_options = find_tradable_options_for_stock(symbol, option_type)
    filtered_options = [item for item in all_options if
                        item["expiration_date"] == expiration_date and float(item["strike_price"]) == float(strike)
                        and item['tradability'] == 'tradable']

    for item in filtered_options:
        market_data = get_option_market_data_by_id(item['id'])
        item.update(market_data)

    return helper.data_filter(filtered_options, info)


def find_options_for_list_of_stocks_by_expiration_date(input_symbols, expiration_date, option_type='both', info=None):
    """Returns a list of all the option orders that match the seach parameters

    :param input_symbols: May be a single stock ticker or a list of stock tickers.
    :type input_symbols: str or list
    :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
    :type expiration_date: str
    :param option_type: Can be either 'call' or 'put' or leave blank to get both.
    :type option_type: Optional[str]
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    symbols = helper.inputs_to_set(input_symbols)
    try:
        option_type = option_type.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    data = []
    url = urls.option_instruments()
    for symbol in symbols:
        if option_type == 'put' or option_type == 'call':
            payload = {'chain_id': helper.id_for_chain(symbol),
                       'expiration_date': expiration_date,
                       'state': 'active',
                       'tradability': 'tradable',
                       'rhs_tradability': 'tradable',
                       'type': option_type}
        else:
            payload = {'chain_id': helper.id_for_chain(symbol),
                       'expiration_date': expiration_date,
                       'state': 'active',
                       'tradability': 'tradable',
                       'rhs_tradability': 'tradable'}
        other_data = helper.request_get(url, 'pagination', payload)
        for item in other_data:
            if item['expiration_date'] == expiration_date and item['tradability'] == 'tradable':
                data.append(item)

    for item in data:
        market_data = get_option_market_data_by_id(item['id'])
        item.update(market_data)

    return helper.data_filter(data, info)


def get_list_market_data(input_symbols, expiration_date, info=None):
    """Returns a list of option market data for several stock tickers.

    :param input_symbols: May be a single stock ticker or a list of stock tickers.
    :type input_symbols: str or list
    :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
    :type expiration_date: str
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all stock option market data. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    symbols = helper.inputs_to_set(input_symbols)
    ids = []
    data = []
    url = urls.option_instruments()
    for symbol in symbols:
        payload = {'chain_id': helper.id_for_chain(symbol),
                   'expiration_date': expiration_date,
                   'state': 'active',
                   'tradability': 'tradable',
                   'rhs_tradability': 'tradable'}
        other_data = helper.request_get(url, 'pagination', payload)
        for item in other_data:
            if item['expiration_date'] == expiration_date and item['tradability'] == 'tradable':
                ids.append(item['id'])

    for _id in ids:
        url = urls.marketdata_options(_id)
        other_data = helper.request_get(url)
        data.append(other_data)

    return helper.data_filter(data, info)


def get_list_options_of_specific_profitability(input_symbols, expiration_date, type_profit="chance_of_profit_short",
                                               profit_floor=0.0, profit_ceiling=1.0, info=None):
    """Returns a list of option market data for several stock tickers that match a range of profitability.

    :param input_symbols: May be a single stock ticker or a list of stock tickers.
    :type input_symbols: str or list
    :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
    :type expiration_date: str
    :param type_profit: Will either be "chance_of_profit_short" or "chance_of_profit_long".
    :type type_profit: str
    :param profit_floor: The lower percentage on scale 0 to 1.
    :type profit_floor: int
    :param profit_ceiling: The higher percentage on scale 0 to 1.
    :type profit_ceiling: int
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all stock option market data. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    symbols = helper.inputs_to_set(input_symbols)
    ids = []
    data = []
    return_data = []
    url = urls.option_instruments()

    if type_profit != "chance_of_profit_short" and type_profit != "chance_of_profit_long":
        print("Invalid string for 'type_profit'. Defaulting to 'chance_of_profit_short'.")
        type_profit = "chance_of_profit_short"

    for symbol in symbols:
        payload = {'chain_id': helper.id_for_chain(symbol),
                   'expiration_date': expiration_date,
                   'state': 'active',
                   'tradability': 'tradable',
                   'rhs_tradability': 'tradable'}
        other_data = helper.request_get(url, 'pagination', payload)
        for item in other_data:
            if item['tradability'] == 'tradable':
                ids.append(item['id'])

    for _id in ids:
        url = urls.marketdata_options(_id)
        other_data = helper.request_get(url)
        data.append(other_data)

    for item in data:
        try:
            float_value = float(item[type_profit])
            if profit_floor < float_value < profit_ceiling:
                return_data.append(item)
        except Exception as e:
            # ToDo: check on exception handling
            msg = "Error string {}".format(e)
            print(msg)
            pass

    return helper.data_filter(return_data, info)


def get_option_market_data_by_id(_id, info=None):
    """Returns the option market data for a stock, including the greeks,
    open interest, change of profit, and adjusted mark price.

    :param _id: The id of the stock.
    :type _id: str
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the stock. \
    If info parameter is provided, the value of the key that matches info is extracted.

    """
    url = urls.marketdata_options(_id)
    data = helper.request_get(url)

    return helper.data_filter(data, info)


def get_option_market_data(symbol, expiration_date, strike, option_type, info=None):
    """Returns the option market data for the stock option, including the greeks,
    open interest, change of profit, and adjusted mark price.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
    :type expiration_date: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param option_type: Can be either 'call' or 'put'.
    :type option_type: str
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the stock. \
    If info parameter is provided, the value of the key that matches info is extracted.

    """
    try:
        symbol = symbol.upper().strip()
        option_type = option_type.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    option_id = helper.id_for_option(symbol, expiration_date, strike, option_type)
    url = urls.marketdata_options(option_id)
    data = helper.request_get(url)

    return helper.data_filter(data, info)


def get_option_instrument_data_by_id(_id, info=None):
    """Returns the option instrument information.

    :param _id: The id of the stock.
    :type _id: str
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the stock. \
    If info parameter is provided, the value of the key that matches info is extracted.

    """
    url = urls.option_instruments(_id)
    data = helper.request_get(url)
    return helper.data_filter(data, info)


def get_option_instrument_data(symbol, expiration_date, strike, option_type, info=None):
    """Returns the option instrument data for the stock option.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
    :type expiration_date: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param option_type: Can be either 'call' or 'put'.
    :type option_type: str
    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the stock. \
    If info parameter is provided, the value of the key that matches info is extracted.

    """
    try:
        symbol = symbol.upper().strip()
        option_type = option_type.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    option_id = helper.id_for_option(symbol, expiration_date, strike, option_type)
    url = urls.option_instruments(option_id)
    data = helper.request_get(url)

    return helper.data_filter(data, info)


def get_option_historicals(symbol, expiration_date, strike, option_type, span='week'):
    """Returns the data that is used to make the graphs.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expiration_date: Represents the expiration date in the format YYYY-MM-DD.
    :type expiration_date: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param option_type: Can be either 'call' or 'put'.
    :type option_type: str
    :param span: Sets the range of the data to be either 'day', 'week', 'year', or '5year'. Default is 'week'.
    :type span: Optional[str]
    :returns: Returns a list that contains a list for each symbol. \
    Each list contains a dictionary where each dictionary is for a different time.

    """
    try:
        symbol = symbol.upper().strip()
        option_type = option_type.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    span_check = ['day', 'week', 'year', '5year']
    if span not in span_check:
        print('ERROR: Span must be "day","week","year",or "5year"')
        return [None]

    if span == 'day':
        interval = '5minute'
    elif span == 'week':
        interval = '10minute'
    elif span == 'year':
        interval = 'day'
    else:
        interval = 'week'

    option_id = helper.id_for_option(symbol, expiration_date, strike, option_type)

    url = urls.option_historicals(option_id)
    payload = {'span': span,
               'interval': interval}
    data = helper.request_get(url, 'regular', payload)

    return data
