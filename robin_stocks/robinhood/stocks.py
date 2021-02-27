"""Contains information in regards to stocks."""
from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.urls import *

def get_quotes(inputSymbols, info=None):
    """Takes any number of stock tickers and returns information pertaining to its price.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [list] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * ask_price
                      * ask_size
                      * bid_price
                      * bid_size
                      * last_trade_price
                      * last_extended_hours_trade_price
                      * previous_close
                      * adjusted_previous_close
                      * previous_close_date
                      * symbol
                      * trading_halted
                      * has_traded
                      * last_trade_price_source
                      * updated_at
                      * instrument

    """
    symbols = inputs_to_set(inputSymbols)
    url = quotes_url()
    payload = {'symbols': ','.join(symbols)}
    data = request_get(url, 'results', payload)

    if (data == None or data == [None]):
        return data

    for count, item in enumerate(data):
        if item is None:
            print(error_ticker_does_not_exist(symbols[count]), file=get_output())

    data = [item for item in data if item is not None]

    return(filter_data(data, info))


def get_fundamentals(inputSymbols, info=None):
    """Takes any number of stock tickers and returns fundamental information
    about the stock such as what sector it is in, a description of the company, dividend yield, and market cap.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [list] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * open
                      * high
                      * low
                      * volume
                      * average_volume_2_weeks
                      * average_volume
                      * high_52_weeks
                      * dividend_yield
                      * float
                      * low_52_weeks
                      * market_cap
                      * pb_ratio
                      * pe_ratio
                      * shares_outstanding
                      * description
                      * instrument
                      * ceo
                      * headquarters_city
                      * headquarters_state
                      * sector
                      * industry
                      * num_employees
                      * year_founded
                      * symbol

    """ 
    symbols = inputs_to_set(inputSymbols)
    url = fundamentals_url()
    payload = {'symbols': ','.join(symbols)}
    data = request_get(url, 'results', payload)

    if (data == None or data == [None]):
        return data

    for count, item in enumerate(data):
        if item is None:
            print(error_ticker_does_not_exist(symbols[count]), file=get_output())
        else:
            item['symbol'] = symbols[count]

    data = [item for item in data if item is not None]

    return(filter_data(data, info))


def get_instruments_by_symbols(inputSymbols, info=None):
    """Takes any number of stock tickers and returns information held by the market
    such as ticker name, bloomberg id, and listing date.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [list] If info parameter is left as None then the list will a dictionary of key/value pairs for each ticker. \
    Otherwise, it will be a list of strings where the strings are the values of the key that corresponds to info.
    :Dictionary Keys: * id
                      * url
                      * quote
                      * fundamentals
                      * splits
                      * state
                      * market
                      * simple_name
                      * name
                      * tradeable
                      * tradability
                      * symbol
                      * bloomberg_unique
                      * margin_initial_ratio
                      * maintenance_ratio
                      * country
                      * day_trade_ratio
                      * list_date
                      * min_tick_size
                      * type
                      * tradable_chain_id
                      * rhs_tradability
                      * fractional_tradability
                      * default_collar_fraction

    """ 
    symbols = inputs_to_set(inputSymbols)
    url = instruments_url()
    data = []
    for item in symbols:
        payload = {'symbol': item}
        itemData = request_get(url, 'indexzero', payload)

        if itemData:
            data.append(itemData)
        else:
            print(error_ticker_does_not_exist(item), file=get_output())

    return(filter_data(data, info))


def get_instrument_by_url(url, info=None):
    """Takes a single url for the stock. Should be located at ``https://api.robinhood.com/instruments/<id>`` where <id> is the
    id of the stock.

    :param url: The url of the stock. Can be found in several locations including \
    in the dictionary returned from get_instruments_by_symbols(inputSymbols,info=None)
    :type url: str
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [dict or str] If info parameter is left as None then will return a dictionary of key/value pairs for a specific url. \
    Otherwise, it will be the string value of the key that corresponds to info.
    :Dictionary Keys: * id
                      * url
                      * quote
                      * fundamentals
                      * splits
                      * state
                      * market
                      * simple_name
                      * name
                      * tradeable
                      * tradability
                      * symbol
                      * bloomberg_unique
                      * margin_initial_ratio
                      * maintenance_ratio
                      * country
                      * day_trade_ratio
                      * list_date
                      * min_tick_size
                      * type
                      * tradable_chain_id
                      * rhs_tradability
                      * fractional_tradability
                      * default_collar_fraction

    """
    data = request_get(url, 'regular')

    return(filter_data(data, info))


def get_latest_price(inputSymbols, priceType=None, includeExtendedHours=True):
    """Takes any number of stock tickers and returns the latest price of each one as a string.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param priceType: Can either be 'ask_price' or 'bid_price'. If this parameter is set, then includeExtendedHours is ignored.
    :type priceType: str
    :param includeExtendedHours: Leave as True if you want to get extendedhours price if available. \
    False if you only want regular hours price, even after hours.
    :type includeExtendedHours: bool
    :returns: [list] A list of prices as strings.

    """ 
    symbols = inputs_to_set(inputSymbols)
    quote = get_quotes(symbols)

    prices = []
    for item in quote:
        if item:
            if priceType == 'ask_price':
                prices.append(item['ask_price'])
            elif priceType == 'bid_price':
                prices.append(item['bid_price'])
            else:
                if priceType:
                    print('WARNING: priceType should be "ask_price" or "bid_price". You entered "{0}"'.format(priceType), file=get_output())
                if item['last_extended_hours_trade_price'] is None or not includeExtendedHours:
                    prices.append(item['last_trade_price'])
                else:
                    prices.append(item['last_extended_hours_trade_price'])
        else:
            prices.append(None)
    return(prices)


@convert_none_to_string
def get_name_by_symbol(symbol):
    """Returns the name of a stock from the stock ticker.

    :param symbol: The ticker of the stock as a string.
    :type symbol: str
    :returns: [str] Returns the simple name of the stock. If the simple name does not exist then returns the full name.

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    url = instruments_url()
    payload = {'symbol': symbol}
    data = request_get(url, 'indexzero', payload)
    if not data:
        return(None)
    # If stock doesn't have a simple name attribute then get the full name.
    filter = filter_data(data, info='simple_name')
    if not filter or filter == "":
        filter = filter_data(data, info='name')
    return(filter)


@convert_none_to_string
def get_name_by_url(url):
    """Returns the name of a stock from the instrument url. Should be located at ``https://api.robinhood.com/instruments/<id>``
    where <id> is the id of the stock.

    :param url: The url of the stock as a string.
    :type url: str
    :returns: [str] Returns the simple name of the stock. If the simple name does not exist then returns the full name.

    """
    data = request_get(url)
    if not data:
        return(None)
    # If stock doesn't have a simple name attribute then get the full name.
    filter = filter_data(data, info='simple_name')
    if not filter or filter == "":
        filter = filter_data(data, info='name')
    return(filter)


@convert_none_to_string
def get_symbol_by_url(url):
    """Returns the symbol of a stock from the instrument url. Should be located at ``https://api.robinhood.com/instruments/<id>``
    where <id> is the id of the stock.

    :param url: The url of the stock as a string.
    :type url: str
    :returns: [str] Returns the ticker symbol of the stock.

    """
    data = request_get(url)
    return filter_data(data, info='symbol')

@convert_none_to_string
def get_ratings(symbol, info=None):
    """Returns the ratings for a stock, including the number of buy, hold, and sell ratings.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to contain a dictionary of values that correspond to the key that matches info. \
    Possible values are summary, ratings, and instrument_id
    :type info: Optional[str]
    :returns: [dict] If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker. \
    Otherwise, it will contain the values that correspond to the keyword that matches info.
    :Dictionary Keys: * summary - value is a dictionary
                      * ratings - value is a list of dictionaries
                      * instrument_id - value is a string
                      * ratings_published_at - value is a string

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    url = ratings_url(symbol)
    data = request_get(url)
    if not data:
        return(data)

    if (len(data['ratings']) == 0):
        return(data)
    else:
        for item in data['ratings']:
            oldText = item['text']
            item['text'] = oldText.encode('UTF-8')

    return(filter_data(data, info))
    

def get_events(symbol, info=None):
    """Returns the events related to a stock that the user owns. For example, if you owned options for USO and that stock \
    underwent a stock split resulting in you owning shares of newly created USO1, then that event will be returned when calling \
    get_events('uso1')

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] If the info parameter is provided, then the function will extract the value of the key \
    that matches the info parameter. Otherwise, the whole dictionary is returned.
    :Dictionary Keys: * account
                      * cash_component
                      * chain_id
                      * created_at
                      * direction
                      * equity_components
                      * event_date
                      * id
                      * option
                      * position
                      * quantity
                      * state
                      * total_cash_amount
                      * type
                      * underlying_price
                      * updated_at

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    payload = {'equity_instrument_id': id_for_stock(symbol)}
    url = events_url()
    data = request_get(url, 'results', payload)

    return(filter_data(data, info))


def get_earnings(symbol, info=None):
    """Returns the earnings for the different financial quarters.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries. If info parameter is provided, \
    a list of strings is returned where the strings are the value \
    of the key that matches info.
    :Dictionary Keys: * symbol
                      * instrument
                      * year
                      * quarter
                      * eps
                      * report
                      * call

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    url = earnings_url()
    payload = {'symbol': symbol}
    data = request_get(url, 'results', payload)

    return(filter_data(data, info))


def get_news(symbol, info=None):
    """Returns news stories for a stock.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries. If info parameter is provided, \
    a list of strings is returned where the strings are the value \
    of the key that matches info.
    :Dictionary Keys: * api_source
                      * author
                      * num_clicks
                      * preview_image_url
                      * published_at
                      * relay_url
                      * source
                      * summary
                      * title
                      * updated_at
                      * url
                      * uuid
                      * related_instruments
                      * preview_text
                      * currency_id

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    url = news_url(symbol)
    data = request_get(url, 'results')

    return(filter_data(data, info))


def get_splits(symbol, info=None):
    """Returns the date, divisor, and multiplier for when a stock split occureed.

    :param symbol: The stock ticker.
    :type symbol: str
    :param info: Will filter the results to get a specific value. Possible options are \
    url, instrument, execution_date, divsor, and multiplier.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries. If info parameter is provided, \
    a list of strings is returned where the strings are the value \
    of the key that matches info.
    :Dictionary Keys: * url
                      * instrument
                      * execution_date
                      * multiplier
                      * divisor

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    url = splits_url(symbol)
    data = request_get(url, 'results')
    return(filter_data(data, info))


def find_instrument_data(query):
    """Will search for stocks that contain the query keyword and return the instrument data.

    :param query: The keyword to search for.
    :type query: str
    :returns: [list] Returns a list of dictionaries that contain the instrument data for each stock that matches the query.
    :Dictionary Keys: * id
                      * url
                      * quote
                      * fundamentals
                      * splits
                      * state
                      * market
                      * simple_name
                      * name
                      * tradeable
                      * tradability
                      * symbol
                      * bloomberg_unique
                      * margin_initial_ratio
                      * maintenance_ratio
                      * country
                      * day_trade_ratio
                      * list_date
                      * min_tick_size
                      * type
                      * tradable_chain_id
                      * rhs_tradability
                      * fractional_tradability
                      * default_collar_fraction

    """ 
    url = instruments_url()
    payload = {'query': query}

    data = request_get(url, 'pagination', payload)

    if len(data) == 0:
        print('No results found for that keyword', file=get_output())
        return([None])
    else:
        print('Found ' + str(len(data)) + ' results', file=get_output())
        return(data)


def get_stock_historicals(inputSymbols, interval='hour', span='week', bounds='regular', info=None):
    """Represents the historicl data for a stock.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param interval: Interval to retrieve data for. Values are '5minute', '10minute', 'hour', 'day', 'week'. Default is 'hour'.
    :type interval: Optional[str]
    :param span: Sets the range of the data to be either 'day', 'week', 'month', '3month', 'year', or '5year'. Default is 'week'.
    :type span: Optional[str]
    :param bounds: Represents if graph will include extended trading hours or just regular trading hours. Values are 'extended', 'trading', or 'regular'. Default is 'regular'
    :type bounds: Optional[str]
    :param info: Will filter the results to have a list of the values that correspond to key that matches info.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries where each dictionary is for a different time. If multiple stocks are provided \
    the historical data is listed one after another.
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
    interval_check = ['5minute', '10minute', 'hour', 'day', 'week']
    span_check = ['day', 'week', 'month', '3month', 'year', '5year']
    bounds_check = ['extended', 'regular', 'trading']

    if interval not in interval_check:
        print(
            'ERROR: Interval must be "5minute","10minute","hour","day",or "week"', file=get_output())
        return([None])
    if span not in span_check:
        print('ERROR: Span must be "day","week","month","3month","year",or "5year"', file=get_output())
        return([None])
    if bounds not in bounds_check:
        print('ERROR: Bounds must be "extended","regular",or "trading"', file=get_output())
        return([None])
    if (bounds == 'extended' or bounds == 'trading') and span != 'day':
        print('ERROR: extended and trading bounds can only be used with a span of "day"', file=get_output())
        return([None])

    symbols = inputs_to_set(inputSymbols)
    url = historicals_url()
    payload = {'symbols': ','.join(symbols),
               'interval': interval,
               'span': span,
               'bounds': bounds}

    data = request_get(url, 'results', payload)
    if (data == None or data == [None]):
        return data

    histData = []
    for count, item in enumerate(data):
        if (len(item['historicals']) == 0):
            print(error_ticker_does_not_exist(symbols[count]), file=get_output())
            continue
        stockSymbol = item['symbol']
        for subitem in item['historicals']:
            subitem['symbol'] = stockSymbol
            histData.append(subitem)

    return(filter_data(histData, info))


def get_stock_quote_by_id(stock_id, info=None):
    """
    Represents basic stock quote information

    :param stock_id: robinhood stock id
    :type stock_id: str
    :param info: Will filter the results to get a specific value. Possible options are url, instrument, execution_date, \
    divsor, and multiplier.
    :type info: Optional[str]
    :return: [dict] If the info parameter is provided, then the function will extract the value of the key \
    that matches the info parameter. Otherwise, the whole dictionary is returned.
    :Dictionary Keys: * ask_price
                      * ask_size
                      * bid_price
                      * bid_size
                      * last_trade_price
                      * last_extended_hours_trade_price
                      * previous_close
                      * adjusted_previous_close
                      * previous_close_date
                      * symbol
                      * trading_halted
                      * has_traded
                      * last_trade_price_source
                      * updated_at
                      * instrument
    """
    url = marketdata_quotes_url(stock_id)
    data = request_get(url)

    return (filter_data(data, info))


def get_stock_quote_by_symbol(symbol, info=None):
    """
    Represents basic stock quote information

    :param symbol: robinhood stock id
    :type stock_id: str
    :param info: Will filter the results to get a specific value. Possible options are url, instrument, execution_date, \
    divsor, and multiplier.
    :type info: Optional[str]
    :return: [dict] If the info parameter is provided, then the function will extract the value of the key \
    that matches the info parameter. Otherwise, the whole dictionary is returned.
    :Dictionary Keys: * ask_price
                      * ask_size
                      * bid_price
                      * bid_size
                      * last_trade_price
                      * last_extended_hours_trade_price
                      * previous_close
                      * adjusted_previous_close
                      * previous_close_date
                      * symbol
                      * trading_halted
                      * has_traded
                      * last_trade_price_source
                      * updated_at
                      * instrument
    """

    return get_stock_quote_by_id(id_for_stock(symbol))


def get_pricebook_by_id(stock_id, info=None):
    """
    Represents Level II Market Data provided for Gold subscribers

    :param stock_id: robinhood stock id
    :type stock_id: str
    :param info: Will filter the results to get a specific value. Possible options are url, instrument, execution_date, \
    divsor, and multiplier.
    :type info: Optional[str]
    :return: Returns a dictionary of asks and bids.

    """
    url = marketdata_pricebook_url(stock_id)
    data = request_get(url)

    return (filter_data(data, info))


def get_pricebook_by_symbol(symbol, info=None):
    """
    Represents Level II Market Data provided for Gold subscribers

    :param symbol: symbol id
    :type symbol: str
    :param info: Will filter the results to get a specific value. Possible options are url, instrument, execution_date, \
    divsor, and multiplier.
    :type info: Optional[str]
    :return: Returns a dictionary of asks and bids.

    """

    return get_pricebook_by_id(id_for_stock(symbol))
