"""Contains functions for getting information about options."""
import robin_stocks.helper as helper
import robin_stocks.urls as urls


@helper.login_required
def get_aggregate_positions(info=None):
    """Collapses all option orders for a stock into a single dictionary.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.aggregate()
    data = helper.request_get(url, 'pagination')
    return(helper.filter(data, info))


@helper.login_required
def get_market_options(info=None):
    """Returns a list of all options.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.option_orders()
    data = helper.request_get(url, 'pagination')

    return(helper.filter(data, info))


@helper.login_required
def get_all_option_positions(info=None):
    """Returns all option positions ever held for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.option_positions()
    data = helper.request_get(url, 'pagination')
    return(helper.filter(data, info))


@helper.login_required
def get_open_option_positions(info=None):
    """Returns all open option positions for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.option_positions()
    payload = {'nonzero': 'True'}
    data = helper.request_get(url, 'pagination', payload)

    return(helper.filter(data, info))


def get_chains(symbol, info=None):
    """Returns the chain information of an option.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param info: Will filter the results to get a specific value.
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

    return(helper.filter(data, info))


def find_tradable_options_for_stock(symbol, optionType='both', info=None):
    """Returns a list of all available options for a stock.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param optionType: Can be either 'call' or 'put' or left blank to get both.
    :type optionType: Optional[str]
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all calls of the stock. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
        optionType = optionType.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    url = urls.option_instruments()
    if not helper.id_for_chain(symbol):
        print("Symbol {} is not valid for finding options.".format(symbol))

    if (optionType == 'call' or optionType == 'put'):
        payload = {'chain_id': helper.id_for_chain(symbol),
                   'chain_symbol': symbol,
                   'state': 'active',
                   'tradability': 'tradable',
                   'type': optionType}
    else:
        payload = {'chain_id': helper.id_for_chain(symbol),
                   'chain_symbol': symbol,
                   'state': 'active',
                   'tradability': 'tradable'}

    data = helper.request_get(url, 'pagination', payload)
    return(helper.filter(data, info))


def find_options_for_stock_by_expiration(symbol, expirationDate, optionType='both', info=None):
    """Returns a list of all the option orders that match the seach parameters

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expirationDate: Represents the expiration date in the format YYYY-MM-DD.
    :type expirationDate: str
    :param optionType: Can be either 'call' or 'put' or leave blank to get both.
    :type optionType: Optional[str]
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
        optionType = optionType.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    allOptions = find_tradable_options_for_stock(symbol, optionType)
    filteredOptions = [item for item in allOptions if item.get("expiration_date") == expirationDate
                       and item.get('tradability') == 'tradable']

    for item in filteredOptions:
        marketData = get_option_market_data_by_id(item['id'])
        item.update(marketData)

    return(helper.filter(filteredOptions, info))


def find_options_for_stock_by_strike(symbol, strike, optionType='both', info=None):
    """Returns a list of all the option orders that match the seach parameters

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param optionType: Can be either 'call' or 'put' or leave blank to get both.
    :type optionType: Optional[str]
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
        optionType = optionType.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    allOptions = find_tradable_options_for_stock(symbol, optionType)
    filteredOptions = [item for item in allOptions if float(item.get("strike_price")) == float(strike)
                       and item.get('tradability') == 'tradable']

    for item in filteredOptions:
        marketData = get_option_market_data_by_id(item['id'])
        item.update(marketData)

    return(helper.filter(filteredOptions, info))


def find_options_for_stock_by_expiration_and_strike(symbol, expirationDate, strike, optionType='both', info=None):
    """Returns a list of all the option orders that match the seach parameters

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expirationDate: Represents the expiration date in the format YYYY-MM-DD.
    :type expirationDate: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param optionType: Can be either 'call' or 'put' or leave blank to get both.
    :type optionType: Optional[str]
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
        option_type = optionType.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    url = urls.option_instruments()
    payload = {'chain_id': helper.id_for_chain(symbol),
               'expiration_date': expirationDate,
               'strike_price': strike,
               'state': 'active',
               'tradability': 'tradable',
               'rhs_tradability': 'tradable'}
    if option_type == 'put' or option_type == 'call':
        payload['type'] = option_type

    data = helper.request_get(url, 'pagination', payload)
    data = [item for item in data if item['expiration_date'] ==
            expirationDate and item['tradability'] == 'tradable']
    for item in data:
        market_data = get_option_market_data_by_id(item['id'])
        item.update(market_data)

    return helper.filter(data, info)


def find_options_for_list_of_stocks_by_expiration_date(inputSymbols, expirationDate, optionType='both', info=None):
    """Returns a list of all the option orders that match the seach parameters

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param expirationDate: Represents the expiration date in the format YYYY-MM-DD.
    :type expirationDate: str
    :param optionType: Can be either 'call' or 'put' or leave blank to get both.
    :type optionType: Optional[str]
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all options of the stock that match the search parameters. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    try:
        optionType = optionType.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    data = []
    url = urls.option_instruments()
    for symbol in symbols:
        if (optionType == 'put' or optionType == 'call'):
            payload = {'chain_id': helper.id_for_chain(symbol),
                       'expiration_date': expirationDate,
                       'state': 'active',
                       'tradability': 'tradable',
                       'rhs_tradability': 'tradable',
                       'type': optionType}
        else:
            payload = {'chain_id': helper.id_for_chain(symbol),
                       'expiration_date': expirationDate,
                       'state': 'active',
                       'tradability': 'tradable',
                       'rhs_tradability': 'tradable'}
        otherData = helper.request_get(url, 'pagination', payload)
        for item in otherData:
            if (item['expiration_date'] == expirationDate and item['tradability'] == 'tradable'):
                data.append(item)

    for item in data:
        marketData = get_option_market_data_by_id(item['id'])
        item.update(marketData)

    return(helper.filter(data, info))


def get_list_market_data(inputSymbols, expirationDate, info=None):
    """Returns a list of option market data for several stock tickers.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param expirationDate: Represents the expiration date in the format YYYY-MM-DD.
    :type expirationDate: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all stock option market data. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    ids = []
    data = []
    url = urls.option_instruments()
    for symbol in symbols:
        payload = {'chain_id': helper.id_for_chain(symbol),
                   'expiration_date': expirationDate,
                   'state': 'active',
                   'tradability': 'tradable',
                   'rhs_tradability': 'tradable'}
        otherData = helper.request_get(url, 'pagination', payload)
        for item in otherData:
            if (item['expiration_date'] == expirationDate and item['tradability'] == 'tradable'):
                ids.append(item['id'])

    for id in ids:
        url = urls.marketdata_options(id)
        otherData = helper.request_get(url)
        data.append(otherData)

    return(helper.filter(data, info))


def get_list_options_of_specific_profitability(inputSymbols, expirationDate, typeProfit="chance_of_profit_short", profitFloor=0.0, profitCeiling=1.0, info=None):
    """Returns a list of option market data for several stock tickers that match a range of profitability.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param expirationDate: Represents the expiration date in the format YYYY-MM-DD.
    :type expirationDate: str
    :param typeProfit: Will either be "chance_of_profit_short" or "chance_of_profit_long".
    :type typeProfit: str
    :param profitFloor: The lower percentage on scale 0 to 1.
    :type profitFloor: int
    :param profitCeiling: The higher percentage on scale 0 to 1.
    :type profitCeiling: int
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for all stock option market data. \
    If info parameter is provided, a list of strings is returned where the strings are the value of the key that matches info.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    ids = []
    data = []
    returnData = []
    url = urls.option_instruments()

    if (typeProfit != "chance_of_profit_short" and typeProfit != "chance_of_profit_long"):
        print("Invalid string for 'typeProfit'. Defaulting to 'chance_of_profit_short'.")
        typeProfit = "chance_of_profit_short"

    for symbol in symbols:
        payload = {'chain_id': helper.id_for_chain(symbol),
                   'expiration_date': expirationDate,
                   'state': 'active',
                   'tradability': 'tradable',
                   'rhs_tradability': 'tradable'}
        otherData = helper.request_get(url, 'pagination', payload)
        for item in otherData:
            if (item['tradability'] == 'tradable'):
                ids.append(item['id'])

    for id in ids:
        url = urls.marketdata_options(id)
        otherData = helper.request_get(url)
        data.append(otherData)

    for item in data:
        try:
            floatValue = float(item[typeProfit])
            if (floatValue > profitFloor and floatValue < profitCeiling):
                returnData.append(item)
        except:
            pass

    return(helper.filter(returnData, info))


def get_option_market_data_by_id(id, info=None):
    """Returns the option market data for a stock, including the greeks,
    open interest, change of profit, and adjusted mark price.

    :param id: The id of the stock.
    :type id: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the stock. \
    If info parameter is provided, the value of the key that matches info is extracted.

    """
    url = urls.marketdata_options(id)
    data = helper.request_get(url)

    return(helper.filter(data, info))


def get_option_market_data(symbol, expirationDate, strike, optionType, info=None):
    """Returns the option market data for the stock option, including the greeks,
    open interest, change of profit, and adjusted mark price.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expirationDate: Represents the expiration date in the format YYYY-MM-DD.
    :type expirationDate: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param optionType: Can be either 'call' or 'put'.
    :type optionType: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the stock. \
    If info parameter is provided, the value of the key that matches info is extracted.

    """
    try:
        symbol = symbol.upper().strip()
        optionType = optionType.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    optionID = helper.id_for_option(symbol, expirationDate, strike, optionType)
    url = urls.marketdata_options(optionID)
    data = helper.request_get(url)

    return(helper.filter(data, info))


def get_option_instrument_data_by_id(id, info=None):
    """Returns the option instrument information.

    :param id: The id of the stock.
    :type id: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the stock. \
    If info parameter is provided, the value of the key that matches info is extracted.

    """
    url = urls.option_instruments(id)
    data = helper.request_get(url)
    return(helper.filter(data, info))


def get_option_instrument_data(symbol, expirationDate, strike, optionType, info=None):
    """Returns the option instrument data for the stock option.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expirationDate: Represents the expiration date in the format YYYY-MM-DD.
    :type expirationDate: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param optionType: Can be either 'call' or 'put'.
    :type optionType: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the stock. \
    If info parameter is provided, the value of the key that matches info is extracted.

    """
    try:
        symbol = symbol.upper().strip()
        optionType = optionType.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    optionID = helper.id_for_option(symbol, expirationDate, strike, optionType)
    url = urls.option_instruments(optionID)
    data = helper.request_get(url)

    return(helper.filter(data, info))


def get_option_historicals(symbol, expirationDate, strike, optionType, span='week'):
    """Returns the data that is used to make the graphs.

    :param symbol: The ticker of the stock.
    :type symbol: str
    :param expirationDate: Represents the expiration date in the format YYYY-MM-DD.
    :type expirationDate: str
    :param strike: Represents the price of the option.
    :type strike: str
    :param optionType: Can be either 'call' or 'put'.
    :type optionType: str
    :param span: Sets the range of the data to be either 'day', 'week', 'year', or '5year'. Default is 'week'.
    :type span: Optional[str]
    :returns: Returns a list that contains a list for each symbol. \
    Each list contains a dictionary where each dictionary is for a different time.

    """
    try:
        symbol = symbol.upper().strip()
        optionType = optionType.lower().strip()
    except AttributeError as message:
        print(message)
        return [None]

    span_check = ['day', 'week', 'year', '5year']
    if span not in span_check:
        print('ERROR: Span must be "day", "week", "year", or "5year"')
        return([None])

    if span == 'day':
        interval = '5minute'
    elif span == 'week':
        interval = '10minute'
    elif span == 'year':
        interval = 'day'
    else:
        interval = 'week'

    optionID = helper.id_for_option(symbol, expirationDate, strike, optionType)

    url = urls.option_historicals(optionID)
    payload = {'span': span,
               'interval': interval}
    data = helper.request_get(url, 'regular', payload)

    return(data)
