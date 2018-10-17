import robin_stocks.helper as helper
import robin_stocks.urls as urls
import robin_stocks.stocks as stocks
import robin_stocks.profiles as profiles

def get_all_orders(info=None):
    """Returns a list of all the orders that have been processed for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.orders()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_all_open_orders(info=None):
    """Returns a list of all the orders that are currently open.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.orders()
    data = helper.request_get(url,'pagination')

    data = [item for item in data if item['cancel'] is not None]

    return(helper.filter(data,info))

def get_order_info(orderID):
    """Returns the information for a single order.

    :param orderID: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type orderID: str
    :returns: Returns a list of dictionaries of key/value pairs for the order.

    """
    url = urls.orders(orderID)
    data = helper.request_get(url)
    return(res_data)

def find_orders(**arguments):
    """Returns a list of orders that match the keyword parameters.

    :param arguments: Variable length of keyword arguments. EX. find_orders(symbol='FB',cancel=None,quantity=1)
    :type arguments: str
    :returns: Returns a list of orders.

    """
    url = urls.orders()
    data = helper.request_get(url,'pagination')

    if (len(arguments) == 0):
        return(data)

    for item in data:
        item['quantity'] = str(int(float(item['quantity'])))

    if 'symbol' in arguments.keys():
        arguments['instrument'] = stocks.get_instruments_by_symbols(arguments['symbol'],info='url')[0]
        del arguments['symbol']

    if 'quantity' in arguments.keys():
        arguments['quantity'] = str(arguments['quantity'])

    stop = len(arguments.keys())-1
    list_of_orders=[]
    for item in data:
        for i,(key,value) in enumerate(arguments.items()):
            if key not in item:
                print(helper.error_argument_not_key_in_dictionary(key))
                return([None])
            if value != item[key]:
                break
            if i == stop:
                list_of_orders.append(item)

    return(list_of_orders)

def cancel_all_open_orders():
    """Cancels all open orders.

    :returns: The list of orders taht were cancelled.

    """
    url = urls.orders()
    items = helper.request_get(url,'pagination')

    items = [item['id'] for item in items if item['cancel'] is not None]

    for item in items:
        cancel_url = urls.cancel(item)
        data = helper.request_post(cancel_url)

    print('All Orders Cancelled')
    return(items)

def cancel_order(orderID):
    """Cancels a specific order.

    :param orderID: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type orderID: str
    :returns: Returns the order information for the order that was cancelled.

    """
    url = urls.cancel(orderID)
    data = helper.request_post(url)

    if data:
        print('Order '+order_id+' cancelled')
    return(data)

def order_buy_market(symbol,quantity,timeInForce='gtc'):
    """Submits a market order to be executed immediately.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': float(stocks.get_latest_price(symbol)[0]),
    'quantity': quantity,
    'type': 'market',
    'stop_price': None,
    'time_in_force': timeInForce,
    'trigger': 'immediate',
    'side': 'buy'
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)

def order_buy_limit(symbol,quantity,limitPrice,timeInForce='gtc'):
    """Submits a limit order to be executed once a certain price is reached.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param limitPrice: The price to trigger the buy order.
    :type limitPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        limitPrice = float(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'type': 'limit',
    'stop_price': None,
    'time_in_force': timeInForce,
    'trigger': 'immediate',
    'side': 'buy'
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)

def order_buy_stop_loss(symbol,quantity,stopPrice,timeInForce='gtc'):
    """Submits a stop order to be turned into a market order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param stopPrice: The price to trigger the market order.
    :type stopPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        latestPrice = float(stocks.get_latest_price(symbol)[0])
        stopPrice = float(stopPrice)
    except AttributeError as message:
        print(message)
        return None

    if (latestPrice > stopPrice):
        print('Error: stopPrice must be above the current price.')
        return(None)

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': stopPrice,
    'quantity': quantity,
    'type': 'market',
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': 'stop',
    'side': 'buy'
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)

def order_buy_stop_limit(symbol,quantity,limitPrice,stopPrice,timeInForce='gtc'):
    """Submits a stop order to be turned into a limit order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param limitPrice: The price to trigger the market order.
    :type limitPrice: float
    :param stopPrice: The price to trigger the limit order.
    :type stopPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        latestPrice = float(stocks.get_latest_price(symbol)[0])
        stopPrice = float(stopPrice)
        limitPrice = float(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    if (latestPrice > stopPrice):
        print('Error: stopPrice must be above the current price.')
        return(None)

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'type': 'limit',
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': 'stop',
    'side': 'buy'
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)

def order_sell_market(symbol,quantity,timeInForce='gtc'):
    """Submits a market order to be executed immediately.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': float(stocks.get_latest_price(symbol)[0]),
    'quantity': quantity,
    'type': 'market',
    'stop_price': None,
    'time_in_force': timeInForce,
    'trigger': 'immediate',
    'side': 'sell'
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)

def order_sell_limit(symbol,quantity,limitPrice,timeInForce='gtc'):
    """Submits a limit order to be executed once a certain price is reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param limitPrice: The price to trigger the sell order.
    :type limitPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        limitPrice = float(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'type': 'limit',
    'stop_price': None,
    'time_in_force': timeInForce,
    'trigger': 'immediate',
    'side': 'sell'
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)

def order_sell_stop_loss(symbol,quantity,stopPrice,timeInForce='gtc'):
    """Submits a stop order to be turned into a market order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param stopPrice: The price to trigger the market order.
    :type stopPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        latestPrice = float(stocks.get_latest_price(symbol)[0])
        stopPrice = float(stopPrice)
    except AttributeError as message:
        print(message)
        return None

    if (latestPrice > stopPrice):
        print('Error: stopPrice must be above the current price.')
        return(None)

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': stopPrice,
    'quantity': quantity,
    'type': 'market',
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': 'stop',
    'side': 'sell'
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)

def order_sell_stop_limit(symbol,quantity,limitPrice,stopPrice,timeInForce='gtc'):
    """Submits a stop order to be turned into a limit order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param limitPrice: The price to trigger the market order.
    :type limitPrice: float
    :param stopPrice: The price to trigger the limit order.
    :type stopPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        latestPrice = float(stocks.get_latest_price(symbol)[0])
        stopPrice = float(stopPrice)
        limitPrice = float(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    if (latestPrice > stopPrice):
        print('Error: stopPrice must be above the current price.')
        return(None)

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'type': 'limit',
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': 'stop',
    'side': 'sell'
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)

def order(symbol,quantity,orderType,limitPrice,stopPrice,trigger,side,timeInForce):
    """A generic order function. All parameters must be supplied.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param orderType: Either 'market' or 'limit'
    :type orderType: str
    :param limitPrice: The price to trigger the market order.
    :type limitPrice: float
    :param stopPrice: The price to trigger the limit or market order.
    :type stopPrice: float
    :param trigger: Either 'immediate' or 'stop'
    :type trigger: str
    :param side: Either 'buy' or 'sell'
    :type side: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: str
    :returns: Dictionary that contains information regarding the purchase or selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        stopPrice = float(stopPrice)
        limitPrice = float(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol,info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'type': orderType,
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': trigger,
    'side': side
    }

    url = urls.orders()
    data = helper.request_post(url,payload)

    return(data)
