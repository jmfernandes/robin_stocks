import robin_stocks.helper as helper
import robin_stocks.urls as urls

def get_quotes(*inputSymbols,info=None):
    """Takes any number of stock tickers and returns information pertaining to its price.

    :param inputSymbols: This is a variable length parameter that represents a stock ticker. \
    May be several tickers seperated by commas or a list of tickers.
    :type inputSymbols: str or list
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    url = urls.quotes()
    payload = { 'symbols' : ','.join(symbols)}
    data = helper.request_get(url,'results',payload)

    if (data == None or data == [None]):
        return data

    for count,item in enumerate(data):
        if item is None:
            print(helper.error_ticker_does_not_exist(symbols[count]))

    data = [item for item in data if item is not None]

    return(helper.filter(data,info))

def get_fundamentals(*inputSymbols,info=None):
    """Takes any number of stock tickers and returns fundamental information
    about the stock such as what sector it is in, a description of the company, dividend yield, and market cap.

    :param inputSymbols: This is a variable length parameter that represents a stock ticker. \
    May be several tickers seperated by commas or a list of tickers.
    :type inputSymbols: str or list
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    url = urls.fundamentals()
    payload = { 'symbols' : ','.join(symbols)}
    data = helper.request_get(url,'results',payload)

    if (data == None or data == [None]):
        return data

    for count,item in enumerate(data):
        if item is None:
            print(helper.error_ticker_does_not_exist(symbols[count]))

    data = [item for item in data if item is not None]

    return(helper.filter(data,info))

def get_instruments_by_symbols(*inputSymbols,info=None):
    """Takes any number of stock tickers and returns information held by the market
    such as ticker name, bloomberg id, and listing date.

    :param inputSymbols: This is a variable length parameter that represents a stock ticker. \
    May be several tickers seperated by commas or a list of tickers.
    :type inputSymbols: str or list
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    url = urls.instruments()
    data = []
    for item in symbols:
        payload = { 'symbol' : item}
        itemData = helper.request_get(url,'indexzero',payload)

        if itemData:
            data.append(itemData)
        else:
            print(helper.error_ticker_does_not_exist(item))

    return(helper.filter(data,info))

def get_instrument_by_url(url,info=None):
    """Takes a single url for the stock. Should be located at ``https://api.robinhood.com/instruments/<id>`` where <id> is the
    id of the stock.

    :param url: The url of the stock. Can be found in several locations including \
    in the dictionary returned from get_instruments_by_symbols(\*inputSymbols,info=None)
    :type url: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.

    """
    data = helper.request_get(url,'regular')

    return(helper.filter(data,info))

def get_latest_price(*inputSymbols):
    """Takes any number of stock tickers and returns the latest price of each one as a string.

    :param inputSymbols: This is a variable length parameter that represents a stock ticker. \
    May be several tickers seperated by commas or a list of tickers.
    :type inputSymbols: str or list
    :returns: A list of prices as strings.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    quote = get_quotes(symbols)

    prices = []
    for item in quote:
        if item['last_extended_hours_trade_price'] is None:
            prices.append(item['last_trade_price'])
        else:
            prices.append(item['last_extended_hours_trade_price'])
    return(prices)

def get_name_by_symbol(symbol):
    """Returns the name of a stock from the stock ticker.

    :param symbol: The ticker of the stock as a string.
    :type symbol: str
    :returns: Returns the simple name of the stock. If the simple name does not exist then returns the full name.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = urls.instruments()
    payload = { 'symbol' : symbol}
    data = helper.request_get(url,'indexzero',payload)

    if not data['simple_name']:
        return data['name']
    else:
        return data['simple_name']

def get_name_by_url(url):
    """Returns the name of a stock from the instrument url. Should be located at ``https://api.robinhood.com/instruments/<id>``
    where <id> is the id of the stock.

    :param symbol: The url of the stock as a string.
    :type symbol: str
    :returns: Returns the simple name of the stock. If the simple name does not exist then returns the full name.

    """
    data = helper.request_get(url)

    if not data['simple_name']:
        return data['name']
    else:
        return data['simple_name']

def get_ratings(symbol,info=None):
    """Returns the ratings for a stock, including the number of buy, hold, and sell ratings.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to contain a dictionary of values that correspond to the key that matches info. \
    Possible values are summary, ratings, and instrument_id
    :type info: Optional[str]
    :returns: If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will contain the values that correspond to the keyword that matches info. In this case, \
    the value will also be a dictionary.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = urls.ratings(symbol)
    data = helper.request_get(url)
    if (len(data['ratings']) == 0):
        return(data)
    else:
        for item in data['ratings']:
            oldText = item['text']
            item['text'] = oldText.encode('UTF-8')

    return(helper.filter(data,info))

def get_popularity(symbol,info=None):
    """Returns the number of open positions.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to be a string value.
    :type info: Optional[str]
    :returns: If the info parameter is provided, then the function will extract the value of the key \
    that matches the info parameter. Otherwise, the whole dictionary is returned.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = urls.popularity(symbol)
    data = helper.request_get(url)

    return(helper.filter(data,info))

def get_events(symbol,info=None):
    """Returns the events related to a stock.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: If the info parameter is provided, then the function will extract the value of the key \
    that matches the info parameter. Otherwise, the whole dictionary is returned.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    payload = {'equity_instrument_id' : helper.id_for_stock(symbol)}
    url = urls.events()
    data = helper.request_get(url,'results',payload)

    return(helper.filter(data,info))

def get_earnings(symbol,info=None):
    """Returns the earnings for the differenct financial quarters.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries. If info parameter is provided, \
    a list of strings is returned where the strings are the value \
    of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = urls.earnings()
    payload = {'symbol' : symbol}
    data = helper.request_get(url,'results',payload)

    return(helper.filter(data,info))

def get_news(symbol,info=None):
    """Returns news stories for a stock.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries. If info parameter is provided, \
    a list of strings is returned where the strings are the value \
    of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = urls.news(symbol)
    data = helper.request_get(url,'results')

    return(helper.filter(data,info))

def get_splits(symbol,info=None):
    """Returns the date, divisor, and multiplier for when a stock split occureed.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to get a specific value. Possible options are \
    url, instrument, execution_date, divsor, and multiplier.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries. If info parameter is provided, \
    a list of strings is returned where the strings are the value \
    of the key that matches info.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = urls.splits(symbol)
    data = helper.request_get(url,'results')
    return(helper.filter(data,info))

def find_instrument_data(query):
    """Will search for stocks that contain the query keyword and return the instrument data.

    :param query: The keyword to search for.
    :type query: str
    :returns: Returns a list of dictionaries that contain the instrument data for each stock that matches the query.

    """
    url = urls.instruments()
    payload = { 'query' : query}

    data = helper.request_get(url,'pagination',payload)

    if len(data) == 0:
        print('No results found for that keyword')
        return([None])
    else:
        print('Found '+str(len(data))+' results')
        return(data)

def get_historicals(*inputSymbols,span='week',bounds='regular'):
    """Represents the data that is used to make the graphs.

    :param inputSymbols: This is a variable length parameter that represents a stock ticker. \
    May be several tickers seperated by commas or a list of tickers.
    :type inputSymbols: str or list
    :param span: Sets the range of the data to be either 'day', 'week', 'year', or '5year'. Default is 'week'.
    :type span: Optional[str]
    :param bounds: Represents if graph will include extended trading hours or just regular trading hours. Values are 'extended' or 'regular'.
    :type bounds: Optional[str]
    :returns: Returns a list of dictionaries where each dictionary is for a different time. If multiple stocks are provided \
    the historical data is listed one after another.

    """
    span_check = ['day','week','year','5year']
    bounds_check =['extended','regular','trading']
    if span not in span_check:
        print('ERROR: Span must be "day","week","year",or "5year"')
        return([None])
    if bounds not in bounds_check:
        print('ERROR: Bounds must be "extended","regular",or "trading"')
        return([None])
    if (bounds == 'extended' or bounds == 'trading') and span != 'day':
        print('ERROR: extended and trading bounds can only be used with a span of "day"')
        return([None])

    if span=='day':
        interval = '5minute'
    elif span=='week':
        interval = '10minute'
    elif span=='year':
        interval = 'day'
    else:
        interval = 'week'

    symbols = helper.inputs_to_set(inputSymbols)
    url = urls.historicals()
    payload = { 'symbols' : ','.join(symbols),
                'interval' : interval,
                'span' : span,
                'bounds' : bounds}

    data = helper.request_get(url,'results',payload)
    if (data == None or data == [None]):
        return data
    histData = []
    for count,item in enumerate(data):
        if (len(item['historicals']) == 0):
            print(helper.error_ticker_does_not_exist(symbols[count]))
            continue
        for subitem in item['historicals']:
            histData.append(subitem)

    return(histData)
