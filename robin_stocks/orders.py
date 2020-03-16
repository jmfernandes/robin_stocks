"""Contains all functions for placing orders for stocks, options, and crypto."""
from uuid import uuid4

import robin_stocks.crypto as crypto
import robin_stocks.helper as helper
import robin_stocks.profiles as profiles
import robin_stocks.stocks as stocks
import robin_stocks.urls as urls


@helper.login_required
def get_all_orders(info = None):
    """Returns a list of all the orders that have been processed for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.orders()
    data = helper.request_get(url, 'pagination')
    return(helper.filter(data, info))

@helper.login_required
def get_all_open_orders(info = None):
    """Returns a list of all the orders that are currently open.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.orders()
    data = helper.request_get(url, 'pagination')

    data = [item for item in data if item['cancel'] is not None]

    return(helper.filter(data, info))

@helper.login_required
def get_all_open_option_orders(info = None):
    """Returns a list of all the orders that are currently open.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.option_orders()
    data = helper.request_get(url, 'pagination')

    data = [item for item in data if item['cancel_url'] is not None]

    return(helper.filter(data, info))

@helper.login_required
def get_order_info(orderID):
    """Returns the information for a single order.

    :param orderID: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type orderID: str
    :returns: Returns a list of dictionaries of key/value pairs for the order.

    """
    url = urls.orders(orderID)
    data = helper.request_get(url)
    return(data)


@helper.login_required
def get_option_order_info(order_id):
    """Returns the information for a single option order.

    :param order_id: The ID associated with the option order.
    :type order_id: str
    :returns: Returns a list of dictionaries of key/value pairs for the order.

    """
    url = urls.option_orders(order_id)
    data = helper.request_get(url)
    return data


@helper.login_required
def find_orders(**arguments):
    """Returns a list of orders that match the keyword parameters.

    :param arguments: Variable length of keyword arguments. EX. find_orders(symbol='FB',cancel=None,quantity=1)
    :type arguments: str
    :returns: Returns a list of orders.

    """
    url = urls.orders()
    data = helper.request_get(url, 'pagination')

    if (len(arguments) == 0):
        return(data)

    for item in data:
        item['quantity'] = str(int(float(item['quantity'])))

    if 'symbol' in arguments.keys():
        arguments['instrument'] = stocks.get_instruments_by_symbols(arguments['symbol'], info='url')[0]
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

@helper.login_required
def cancel_all_open_orders():
    """Cancels all open orders.

    :returns: The list of orders that were cancelled.

    """
    url = urls.orders()
    items = helper.request_get(url, 'pagination')

    items = [item['id'] for item in items if item['cancel'] is not None]

    for item in items:
        cancel_url = urls.cancel(item)
        helper.request_post(cancel_url)

    print('All Orders Cancelled')
    return(items)

@helper.login_required
def cancel_order(orderID):
    """Cancels a specific order.

    :param orderID: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type orderID: str
    :returns: Returns the order information for the order that was cancelled.

    """
    url = urls.cancel(orderID)
    data = helper.request_post(url)

    if data:
        print('Order '+orderID+' cancelled')
    return(data)

@helper.login_required
def cancel_option_order(orderID):
    """Cancels a specific option order.

    :param orderID: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type orderID: str
    :returns: Returns the order information for the order that was cancelled.

    """
    url = urls.option_cancel(orderID)
    data = helper.request_post(url)

    if data:
        print('Order '+orderID+' cancelled')
    return(data)

@helper.login_required
def order_buy_market(symbol, quantity, timeInForce = 'gtc', extendedHours = False):
    """Submits a market order to be executed immediately.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': helper.round_price(stocks.get_latest_price(symbol)[0]),
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': 'market',
    'stop_price': None,
    'time_in_force': timeInForce,
    'trigger': 'immediate',
    'side': 'buy',
    "extended_hours":extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order_buy_limit(symbol, quantity, limitPrice, timeInForce = 'gtc', extendedHours = False):
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
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        limitPrice = helper.round_price(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': 'limit',
    'stop_price': None,
    'time_in_force': timeInForce,
    'trigger': 'immediate',
    'side': 'buy',
    'extended_hours': extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order_buy_stop_loss(symbol, quantity, stopPrice, timeInForce = 'gtc', extendedHours = False):
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
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        stopPrice = helper.round_price(stopPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': stopPrice,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': 'market',
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': 'stop',
    'side': 'buy',
    'extended_hours': extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order_buy_stop_limit(symbol, quantity, limitPrice, stopPrice, timeInForce = 'gtc', extendedHours = False):
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
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        stopPrice = helper.round_price(stopPrice)
        limitPrice = helper.round_price(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': 'limit',
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': 'stop',
    'side': 'buy',
    'extended_hours': extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order_sell_market(symbol, quantity, timeInForce = 'gtc', extendedHours = False):
    """Submits a market order to be executed immediately.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': helper.round_price(stocks.get_latest_price(symbol)[0]),
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': 'market',
    'stop_price': None,
    'time_in_force': timeInForce,
    'trigger': 'immediate',
    'side': 'sell',
    'extended_hours': extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order_sell_limit(symbol, quantity, limitPrice, timeInForce = 'gtc', extendedHours = False):
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
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        limitPrice = helper.round_price(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': 'limit',
    'stop_price': None,
    'time_in_force': timeInForce,
    'trigger': 'immediate',
    'side': 'sell',
    'extended_hours': extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order_sell_stop_loss(symbol, quantity, stopPrice, timeInForce='gtc', extendedHours = False):
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
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        stopPrice = helper.round_price(stopPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': stopPrice,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': 'market',
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': 'stop',
    'side': 'sell',
    'extended_hours': extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order_sell_stop_limit(symbol, quantity, limitPrice, stopPrice, timeInForce='gtc', extendedHours = False):
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
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        stopPrice = helper.round_price(stopPrice)
        limitPrice = helper.round_price(limitPrice)
    except AttributeError as message:
        print(message)
        return None

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': 'limit',
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': 'stop',
    'side': 'sell',
    'extended_hours': extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order(symbol, quantity, orderType, trigger, side, limitPrice = None, stopPrice = None, timeInForce = 'gtc', extendedHours = False):
    """A generic order function. All parameters must be supplied.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param orderType: Either 'market' or 'limit'
    :type orderType: str
    :param trigger: Either 'immediate' or 'stop'
    :type trigger: str
    :param side: Either 'buy' or 'sell'
    :type side: str
    :param limitPrice: The price to trigger the market order.
    :type limitPrice: float
    :param stopPrice: The price to trigger the limit or market order.
    :type stopPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: str
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :returns: Dictionary that contains information regarding the purchase or selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    if stopPrice:
        stopPrice = helper.round_price(stopPrice)

    if limitPrice:
        limitPrice = helper.round_price(limitPrice)
    else:
        limitPrice = helper.round_price(stocks.get_latest_price(symbol)[0])
    payload = {
    'account': profiles.load_account_profile(info='url'),
    'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
    'symbol': symbol,
    'price': limitPrice,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'type': orderType,
    'stop_price': stopPrice,
    'time_in_force': timeInForce,
    'trigger': trigger,
    'side': side,
    'extended_hours': extendedHours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return(data)

@helper.login_required
def order_option_credit_spread(price, symbol, quantity, spread, timeInForce='gfd'):
    """Submits a limit order for an option credit spread.

    :param price: The limit price to trigger a sell of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to sell.
    :type quantity: int
    :param spread: A dictionary of spread options with the following keys: \n
        - expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.\n
        - strike: The strike price of the option.\n
        - optionType: This should be 'call' or 'put'
    :type spread: dict
    :param timeInForce: Changes how long the order will be in effect for. \
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' = execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the trading of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    order_option_spread("credit", price, symbol, quantity, spread, timeInForce)

@helper.login_required
def order_option_debit_spread(price, symbol, quantity, spread, timeInForce='gfd'):
    """Submits a limit order for an option credit spread.

    :param price: The limit price to trigger a sell of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to sell.
    :type quantity: int
    :param spread: A dictionary of spread options with the following keys: \n
        - expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.\n
        - strike: The strike price of the option.\n
        - optionType: This should be 'call' or 'put'
    :type spread: dict
    :param timeInForce: Changes how long the order will be in effect for.
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the trading of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    order_option_spread("debit", price, symbol, quantity, spread, timeInForce)

@helper.login_required
def order_option_spread(direction, price, symbol, quantity, spread, timeInForce='gfd'):
    """Submits a limit order for an option spread. i.e. place a debit / credit spread

    :param direction: credit or debit spread
    :type direction: str
    :param price: The limit price to trigger a trade of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to trade.
    :type quantity: int
    :param spread: A dictionary of spread options with the following keys: \n
        - expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.\n
        - strike: The strike price of the option.\n
        - optionType: This should be 'call' or 'put'
    :type spread: dict
    :param timeInForce: Changes how long the order will be in effect for.
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the trading of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None
    legs = []
    for each in spread:
        optionID = helper.id_for_option(symbol,
                                        each['expirationDate'],
                                        each['strike'],
                                        each['optionType'])
        legs.append({'position_effect': each['effect'],
                     'side' : each['action'],
                     'ratio_quantity': 1,
                     'option': urls.option_instruments(optionID)})

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'direction': direction,
        'time_in_force': timeInForce,
        'legs': legs,
        'type': 'limit',
        'trigger': 'immediate',
        'price': price,
        'quantity': quantity,
        'override_day_trade_checks': False,
        'override_dtbp_checks': False,
        'ref_id': str(uuid4()),
    }

    url = urls.option_orders()
    data = helper.request_post(url, payload, json=True)

    return(data)


@helper.login_required
def order_buy_option_limit(positionEffect, price, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gfd'):
    """Submits a limit order for an option. i.e. place a long call or a long put.

    :param positionEffect: Either 'open' for a buy to open effect or 'close' for a buy to close effect.
    :type positionEffect: str
    :param price: The limit price to trigger a buy of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to buy.
    :type quantity: int
    :param expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.
    :type expirationDate: str
    :param strike: The strike price of the option.
    :type strike: float
    :param optionType: This should be 'call' or 'put'
    :type optionType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the buying of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    optionID = helper.id_for_option(symbol, expirationDate, strike, optionType)

    if (positionEffect == 'close'):
        direction = 'credit'
    else:
        direction = 'debit'

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'direction': direction,
    'time_in_force': timeInForce,
    'legs': [
        {'position_effect': positionEffect, 'side' : 'buy', 'ratio_quantity': 1, 'option': urls.option_instruments(optionID) },
    ],
    'type': 'limit',
    'trigger': 'immediate',
    'price': price,
    'quantity': quantity,
    'override_day_trade_checks': False,
	'override_dtbp_checks': False,
    'ref_id': str(uuid4()),
    }

    url = urls.option_orders()
    data = helper.request_post(url, payload, json=True)

    return(data)

@helper.login_required
def order_sell_option_limit(positionEffect, price, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gfd'):
    """Submits a limit order for an option. i.e. place a short call or a short put.

    :param positionEffect: Either 'open' for a sell to open effect or 'close' for a sell to close effect.
    :type positionEffect: str
    :param price: The limit price to trigger a sell of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to sell.
    :type quantity: int
    :param expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.
    :type expirationDate: str
    :param strike: The strike price of the option.
    :type strike: float
    :param optionType: This should be 'call' or 'put'
    :type optionType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    optionID = helper.id_for_option(symbol, expirationDate, strike, optionType)

    if (positionEffect == 'close'):
        direction = 'debit'
    else:
        direction = 'credit'

    payload = {
    'account': profiles.load_account_profile(info='url'),
    'direction': direction,
    'time_in_force': timeInForce,
    'legs': [
        {'position_effect': positionEffect, 'side' : 'sell', 'ratio_quantity': 1, 'option': urls.option_instruments(optionID) },
    ],
    'type': 'limit',
    'trigger': 'immediate',
    'price': price,
    'quantity': quantity,
    'override_day_trade_checks': False,
	'override_dtbp_checks': False,
    'ref_id': str(uuid4()),
    }

    url = urls.option_orders()
    data = helper.request_post(url, payload, json=True)

    return(data)

@helper.login_required
def order_buy_crypto_by_price(symbol, amountInDollars, priceType='ask_price', timeInForce='gtc'):
    """Submits a market order for a crypto by specifying the amount in dollars that you want to trade.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param amountInDollars: The amount in dollars of the crypto you want to buy.
    :type amountInDollars: float
    :param priceType: The type of price to get. Can be 'ask_price', 'bid_price', or 'mark_price'
    :type priceType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the buying of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    crypto_info = crypto.get_crypto_info(symbol)
    price = helper.round_price(crypto.get_crypto_quote_from_id(crypto_info['id'], info=priceType))
    # turn the money amount into decimal number of shares
    try:
        shares = round(amountInDollars/price,8)
    except:
        shares = 0

    payload = {
    'mimeType': 'application/json',
    'account_id': crypto.load_crypto_profile(info="id"),
    'currency_pair_id': crypto_info['id'],
    'price': price,
    'quantity': shares,
    'ref_id': str(uuid4()),
    'side': 'buy',
    'time_in_force': timeInForce,
    'type': 'market'
    }

    url = urls.order_crypto()
    data = helper.request_post(url,payload,json=True)

    return(data)

@helper.login_required
def order_buy_crypto_by_quantity(symbol, quantity, priceType='ask_price', timeInForce='gtc'):
    """Submits a market order for a crypto by specifying the decimal amount of shares to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to buy.
    :type quantity: float
    :param priceType: The type of price to get. Can be 'ask_price', 'bid_price', or 'mark_price'
    :type priceType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the buying of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    crypto_info = crypto.get_crypto_info(symbol)
    price = helper.round_price(crypto.get_crypto_quote_from_id(crypto_info['id'], info=priceType))

    payload = {
    'account_id': crypto.load_crypto_profile(info="id"),
    'currency_pair_id': crypto_info['id'],
    'price': price,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'side': 'buy',
    'time_in_force': timeInForce,
    'type': 'market'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return(data)

@helper.login_required
def order_buy_crypto_limit(symbol, quantity, price, timeInForce='gtc'):
    """Submits a limit order for a crypto by specifying the decimal amount of shares to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to buy.
    :type quantity: float
    :param price: The limit price to set for the crypto.
    :type price: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the buying of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    crypto_info = crypto.get_crypto_info(symbol)

    if crypto_info['display_only']:
        print("WARNING: The dictionary returned by crypto.get_crypto_info() for this crypto has key 'display_only' set to True. May not be able to trade this crypto.")

    payload = {
    'account_id': crypto.load_crypto_profile(info="id"),
    'currency_pair_id': crypto_info['id'],
    'price': price,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'side': 'buy',
    'time_in_force': timeInForce,
    'type': 'limit'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return(data)

@helper.login_required
def order_sell_crypto_by_price(symbol, amountInDollars, priceType='ask_price', timeInForce='gtc'):
    """Submits a market order for a crypto by specifying the amount in dollars that you want to trade.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param amountInDollars: The amount in dollars of the crypto you want to sell.
    :type amountInDollars: float
    :param priceType: The type of price to get. Can be 'ask_price', 'bid_price', or 'mark_price'
    :type priceType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the selling of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    crypto_info = crypto.get_crypto_info(symbol)
    price = helper.round_price(crypto.get_crypto_quote_from_id(crypto_info['id'], info=priceType))
    # turn the money amount into decimal number of shares
    try:
        shares = round(amountInDollars/float(price), 8)
    except:
        shares = 0

    payload = {
    'account_id': crypto.load_crypto_profile(info="id"),
    'currency_pair_id': crypto_info['id'],
    'price': price,
    'quantity': shares,
    'ref_id': str(uuid4()),
    'side': 'sell',
    'time_in_force': timeInForce,
    'type': 'market'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return(data)

@helper.login_required
def order_sell_crypto_by_quantity(symbol, quantity, priceType='ask_price', timeInForce='gtc'):
    """Submits a market order for a crypto by specifying the decimal amount of shares to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to sell.
    :type quantity: float
    :param priceType: The type of price to get. Can be 'ask_price', 'bid_price', or 'mark_price'
    :type priceType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the selling of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    crypto_info = crypto.get_crypto_info(symbol)
    price = helper.round_price(crypto.get_crypto_quote_from_id(crypto_info['id'], info=priceType))

    payload = {
    'account_id': crypto.load_crypto_profile(info="id"),
    'currency_pair_id': crypto_info['id'],
    'price': price,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'side': 'sell',
    'time_in_force': timeInForce,
    'type': 'market'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return(data)

@helper.login_required
def order_sell_crypto_limit(symbol, quantity, price, timeInForce='gtc'):
    """Submits a limit order for a crypto by specifying the decimal amount of shares to sell.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to sell.
    :type quantity: float
    :param price: The limit price to set for the crypto.
    :type price: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :returns: Dictionary that contains information regarding the selling of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    crypto_info = crypto.get_crypto_info(symbol)

    if crypto_info['display_only']:
        print("WARNING: The dictionary returned by crypto.get_crypto_info() for this crypto has key 'display_only' set to True. May not be able to trade this crypto.")

    payload = {
    'account_id': crypto.load_crypto_profile(info="id"),
    'currency_pair_id': crypto_info['id'],
    'price': price,
    'quantity': quantity,
    'ref_id': str(uuid4()),
    'side': 'sell',
    'time_in_force': timeInForce,
    'type': 'limit'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return(data)
