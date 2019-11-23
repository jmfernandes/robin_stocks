"""Contains all functions for placing orders for stocks, options, and crypto."""
from uuid import uuid4

import robin_stocks.crypto as crypto
import robin_stocks.helper as helper
import robin_stocks.options as options
import robin_stocks.profiles as profiles
import robin_stocks.stocks as stocks
import robin_stocks.urls as urls


@helper.login_required
def get_all_orders(info=None):
    """Returns a list of all the orders that have been processed for the account.

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.orders()
    data = helper.request_get(url, 'pagination')
    return helper.data_filter(data, info)


@helper.login_required
def get_all_open_orders(info=None):
    """Returns a list of all the orders that are currently open.

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.orders()
    data = helper.request_get(url, 'pagination')

    data = [item for item in data if item['cancel'] is not None]

    return helper.data_filter(data, info)


@helper.login_required
def close_all_open_option_positions(symbol=None, _type=None):
    """
    *** WIP: WORK IN PROGRESS ***
    data_filter by symbol and type
    1) cancel all OPEN option orders
    2) confirm all OPEN orders cancelled
    3) close open "short" options around MID and ASK (target price is median of ASK & MID)
    4) ensure all the SHORT options closed
    5) close open "long" options around BID and MID
    6) ensure all the LONG options closed
    :param symbol: Optional - when filtered will close all open positions
    :param _type: put or call or None==both
    :return:
    """
    open_pos = options.get_open_option_positions()
    if symbol:
        open_pos = filter(lambda x: x.get['chain_symbol'] == symbol, open_pos)
        print(open_pos)
    cancel_all_open_orders()
    print("*** DO NOT USE *** WORK IN PROGRESS ***")
    pass


@helper.login_required
def get_all_open_option_orders(info=None):
    """Returns a list of all the orders that are currently open.

    :param info: Will data_filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.option_orders()
    data = helper.request_get(url, 'pagination')

    data = [item for item in data if item['cancel_url'] is not None]

    return helper.data_filter(data, info)


@helper.login_required
def get_order_info(order_id):
    """Returns the information for a single order.

    :param order_id: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type order_id: str
    :returns: Returns a list of dictionaries of key/value pairs for the order.

    """
    url = urls.orders(order_id)
    data = helper.request_get(url)
    return data


@helper.login_required
def get_option_order_info(order_id):
    """Returns the information for a single order.

    :param order_id: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
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

    if len(arguments) == 0:
        return data

    for item in data:
        item['quantity'] = str(int(float(item['quantity'])))

    if 'symbol' in arguments.keys():
        arguments['instrument'] = stocks.get_instruments_by_symbols(arguments['symbol'], info='url')[0]
        del arguments['symbol']

    if 'quantity' in arguments.keys():
        arguments['quantity'] = str(arguments['quantity'])

    stop = len(arguments.keys()) - 1
    list_of_orders = []
    for item in data:
        for i, (key, value) in enumerate(arguments.items()):
            if key not in item:
                print(helper.error_argument_not_key_in_dictionary(key))
                return [None]
            if value != item[key]:
                break
            if i == stop:
                list_of_orders.append(item)

    return list_of_orders


@helper.login_required
def cancel_all_open_option_orders():
    """Cancels all open orders.

    :returns: The list of orders that were cancelled.

    """
    items = get_all_open_option_orders()
    for item in items:
        cancel_url = item.get('cancel_url')
        helper.request_post(cancel_url)

    print('All Orders Cancelled')
    return items


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
    return items


@helper.login_required
def cancel_order(order_id):
    """Cancels a specific order.

    :param order_id: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type order_id: str
    :returns: Returns the order information for the order that was cancelled.

    """
    url = urls.cancel(order_id)
    data = helper.request_post(url)

    if data:
        print('Order ' + order_id + ' cancelled')
    return data


@helper.login_required
def cancel_option_order(order_id):
    """Cancels a specific option order.

    :param order_id: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type order_id: str
    :returns: Returns the order information for the order that was cancelled.

    """
    url = urls.option_cancel(order_id)
    data = helper.request_post(url)

    if data:
        print('Order ' + order_id + ' cancelled')
    return data


@helper.login_required
def order_buy_market(symbol, quantity, time_in_force='gtc', extended_hours='false'):
    """Submits a market order to be executed immediately.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :param extended_hours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extended_hours: str
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
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': helper.round_price(stocks.get_latest_price(symbol)[0]),
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'market',
        'stop_price': None,
        'time_in_force': time_in_force,
        'trigger': 'immediate',
        'side': 'buy',
        'extended_hours': extended_hours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return data


@helper.login_required
def order_buy_limit(symbol, quantity, limit_price, time_in_force='gtc'):
    """Submits a limit order to be executed once a certain price is reached.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param limit_price: The price to trigger the buy order.
    :type limit_price: float
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        limit_price = helper.round_price(limit_price)
    except AttributeError as message:
        print(message)
        return None

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': limit_price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'limit',
        'stop_price': None,
        'time_in_force': time_in_force,
        'trigger': 'immediate',
        'side': 'buy'
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return data


@helper.login_required
def order_buy_stop_loss(symbol, quantity, stop_price, time_in_force='gtc'):
    """Submits a stop order to be turned into a market order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param stop_price: The price to trigger the market order.
    :type stop_price: float
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        latest_price = helper.round_price(stocks.get_latest_price(symbol)[0])
        stop_price = helper.round_price(stop_price)
    except AttributeError as msg:
        print(msg)
        return None

    if latest_price > stop_price:
        print('Error: stop_price must be above the current price.')
        return None

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': stop_price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'market',
        'stop_price': stop_price,
        'time_in_force': time_in_force,
        'trigger': 'stop',
        'side': 'buy'
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return data


@helper.login_required
def order_buy_stop_limit(symbol, quantity, limit_price, stop_price, time_in_force='gtc'):
    """Submits a stop order to be turned into a limit order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param limit_price: The price to trigger the market order.
    :type limit_price: float
    :param stop_price: The price to trigger the limit order.
    :type stop_price: float
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        latest_price = helper.round_price(stocks.get_latest_price(symbol)[0])
        stop_price = helper.round_price(stop_price)
        limit_price = helper.round_price(limit_price)
    except AttributeError as message:
        print(message)
        return None

    if latest_price > stop_price:
        print('Error: stop_price must be above the current price.')
        return None

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': limit_price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'limit',
        'stop_price': stop_price,
        'time_in_force': time_in_force,
        'trigger': 'stop',
        'side': 'buy'
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return data


@helper.login_required
def order_sell_market(symbol, quantity, time_in_force='gtc', extended_hours='false'):
    """Submits a market order to be executed immediately.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :param extended_hours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extended_hours: str
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
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': helper.round_price(stocks.get_latest_price(symbol)[0]),
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'market',
        'stop_price': None,
        'time_in_force': time_in_force,
        'trigger': 'immediate',
        'side': 'sell',
        'extended_hours': extended_hours
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return data


@helper.login_required
def order_sell_limit(symbol, quantity, limit_price, time_in_force='gtc'):
    """Submits a limit order to be executed once a certain price is reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param limit_price: The price to trigger the sell order.
    :type limit_price: float
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        limit_price = helper.round_price(limit_price)
    except AttributeError as message:
        print(message)
        return None

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': limit_price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'limit',
        'stop_price': None,
        'time_in_force': time_in_force,
        'trigger': 'immediate',
        'side': 'sell'
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return data


@helper.login_required
def order_sell_stop_loss(symbol, quantity, stop_price, time_in_force='gtc'):
    """Submits a stop order to be turned into a market order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param stop_price: The price to trigger the market order.
    :type stop_price: float
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        latest_price = helper.round_price(stocks.get_latest_price(symbol)[0])
        stop_price = helper.round_price(stop_price)
    except AttributeError as message:
        print(message)
        return None

    if latest_price < stop_price:
        print('Error: stop_price must be below the current price.')
        return None

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': stop_price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'market',
        'stop_price': stop_price,
        'time_in_force': time_in_force,
        'trigger': 'stop',
        'side': 'sell'
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return data


@helper.login_required
def order_sell_stop_limit(symbol, quantity, limit_price, stop_price, time_in_force='gtc'):
    """Submits a stop order to be turned into a limit order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param limit_price: The price to trigger the market order.
    :type limit_price: float
    :param stop_price: The price to trigger the limit order.
    :type stop_price: float
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        latest_price = helper.round_price(stocks.get_latest_price(symbol)[0])
        stop_price = helper.round_price(stop_price)
        limit_price = helper.round_price(limit_price)
    except AttributeError as message:
        print(message)
        return None

    if latest_price < stop_price:
        print('Error: stop_price must be below the current price.')
        return None

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': limit_price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'limit',
        'stop_price': stop_price,
        'time_in_force': time_in_force,
        'trigger': 'stop',
        'side': 'sell'
    }

    url = urls.orders()
    data = helper.request_post(url, payload)

    return data


@helper.login_required
def order(symbol, quantity, order_type, limit_price, stop_price, trigger, side, time_in_force, extended_hours):
    """A generic order function. All parameters must be supplied.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param order_type: Either 'market' or 'limit'
    :type order_type: str
    :param limit_price: The price to trigger the market order.
    :type limit_price: float
    :param stop_price: The price to trigger the limit or market order.
    :type stop_price: float
    :param trigger: Either 'immediate' or 'stop'
    :type trigger: str
    :param side: Either 'buy' or 'sell'
    :type side: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: str
    :param extended_hours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extended_hours: str
    :returns: Dictionary that contains information regarding the purchase or selling of stocks, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        stop_price = helper.round_price(stop_price)
        limit_price = helper.round_price(limit_price)
    except AttributeError as message:
        print(message)
        return None

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'instrument': stocks.get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': limit_price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': order_type,
        'stop_price': stop_price,
        'time_in_force': time_in_force,
        'trigger': trigger,
        'side': side,
        'extended_hours': extended_hours
    }
    url = urls.orders()
    data = helper.request_post(url, payload)
    return data


@helper.login_required
def order_option_credit_spread(price, symbol, quantity, spread, time_in_force='gfd'):
    """Submits a limit order for an option credit spread.

    :param price: The limit price to trigger a sell of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to sell.
    :type quantity: int
    :param spread: A dictionary of spread options with the following keys: \n
        - expiration_date: The expiration date of the option in 'YYYY-MM-DD' format.\n
        - strike: The strike price of the option.\n
        - option_type: This should be 'call' or 'put'
    :type spread: dict
    :param time_in_force: Changes how long the order will be in effect for.
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    order_option_spread("credit", price, symbol, quantity, spread, time_in_force)


@helper.login_required
def order_option_debit_spread(price, symbol, quantity, spread, time_in_force='gfd'):
    """Submits a limit order for an option credit spread.

    :param price: The limit price to trigger a sell of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to sell.
    :type quantity: int
    :param spread: A dictionary of spread options with the following keys: \n
    :type spread: dict
      param expiration_date: The expiration date of the option in 'YYYY-MM-DD' format.
      type expiration_date: str
      param strike: The strike price of the option.
      type strike: float
      param option_type: This should be 'call' or 'put'
      type option_type: str
    :param time_in_force: Changes how long the order will be in effect for.
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    order_option_spread("debit", price, symbol, quantity, spread, time_in_force)


@helper.login_required
def order_option_spread(direction, price, symbol, quantity, spread, time_in_force='gfd'):
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
    :type spread: dict
      param expiration_date: The expiration date of the option in 'YYYY-MM-DD' format.
      type expiration_date: str
      param strike: The strike price of the option.
      type strike: float
      param option_type: This should be 'call' or 'put'
      type option_type: str
    :param time_in_force: Changes how long the order will be in effect for.
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    """
    param expiration_date: The expiration date of the option in 'YYYY-MM-DD' format.
    type expiration_date: str
    param strike: The strike price of the option.
    type strike: float
    param option_type: This should be 'call' or 'put'
    type option_type: str
    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None
    legs = []
    for each in spread:
        if each['effect'] == 'close':
            option_id = options.id_of_options_to_close(symbol,
                                                       each['expiration_date'],
                                                       each['strike'],
                                                       each['option_type'])
        else:
            option_id = helper.id_for_option(symbol,
                                             each['expiration_date'],
                                             each['strike'],
                                             each['option_type'])
        legs.append({'position_effect': each['effect'],
                     'side': each['action'],
                     'ratio_quantity': 1,
                     'option': urls.option_instruments(option_id)})

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'direction': direction,
        'time_in_force': time_in_force,
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

    return data


@helper.login_required
def order_option_buy_to_open(price, symbol, quantity, expiration_date, strike, option_type='both', time_in_force='gfd'):
    order_buy_option_limit(price, symbol, quantity, expiration_date, strike, option_type, time_in_force)


@helper.login_required
def order_buy_option_limit(price, symbol, quantity, expiration_date, strike, option_type='both', time_in_force='gfd'):
    """Submits a limit order for an option. i.e. place a long call or a long put.

    :param price: The limit price to trigger a buy of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to buy.
    :type quantity: int
    :param expiration_date: The expiration date of the option in 'YYYY-MM-DD' format.
    :type expiration_date: str
    :param strike: The strike price of the option.
    :type strike: float
    :param option_type: This should be 'call' or 'put'
    :type option_type: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    option_id = helper.id_for_option(symbol, expiration_date, str(strike), option_type)

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'direction': 'debit',
        'time_in_force': time_in_force,
        'legs': [
            {'position_effect': 'open', 'side': 'buy', 'ratio_quantity': 1,
             'option': urls.option_instruments(option_id)},
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

    return data


@helper.login_required
def order_option_sell_to_close(price, symbol, quantity, expiration_date, strike, option_type='both',
                               time_in_force='gfd'):
    """
    all close option order - do the lookup on the existing positions
    :param price:
    :param symbol:
    :param quantity:
    :param expiration_date:
    :param strike:
    :param option_type:
    :param time_in_force:
    :return:
    """
    _id = options.id_of_options_to_close(symbol, expiration_date, strike, option_type, count=quantity, _type='long')
    if _id:
        return order_option_by_id(_id, price, quantity, direction='credit', effect='close', side='sell', time_in_force=time_in_force)


@helper.login_required
def order_option_by_id(option_id, price, quantity, direction='credit', effect='close', side='sell',
                       time_in_force='gfd'):
    """

    :param option_id:
    :param price:
    :param quantity:
    :param direction:
    :param effect:
    :param side:
    :param time_in_force:
    :return:
    """

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'direction': direction,
        'time_in_force': time_in_force,
        'legs': [
            {'position_effect': effect, 'side': side, 'ratio_quantity': 1,
             'option': urls.option_instruments(option_id)},
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
    print(data)
    return data


@helper.login_required
def order_sell_option_limit(price, symbol, quantity, expiration_date, strike, option_type='both', time_in_force='gfd'):
    """Submits a limit order for an option. i.e. place a short call or a short put.

    :param price: The limit price to trigger a sell of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to sell.
    :type quantity: int
    :param expiration_date: The expiration date of the option in 'YYYY-MM-DD' format.
    :type expiration_date: str
    :param strike: The strike price of the option.
    :type strike: float
    :param option_type: This should be 'call' or 'put'
    :type option_type: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    option_id = helper.id_for_option(symbol, expiration_date, str(strike), option_type)

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'direction': 'credit',
        'time_in_force': time_in_force,
        'legs': [
            {'position_effect': 'close', 'side': 'sell', 'ratio_quantity': 1,
             'option': urls.option_instruments(option_id)},
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

    return data


@helper.login_required
def order_option_buy_to_close(price, symbol, quantity, expiration_date, strike, option_type='both',
                              time_in_force='gfd'):
    """Submits a limit order for an option. i.e. place a long call or a long put.

    :param price: The limit price to trigger a buy of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to buy.
    :type quantity: int
    :param expiration_date: The expiration date of the option in 'YYYY-MM-DD' format.
    :type expiration_date: str
    :param strike: The strike price of the option.
    :type strike: float
    :param option_type: This should be 'call' or 'put'
    :type option_type: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    _id = options.id_of_options_to_close(symbol, expiration_date, strike, option_type, count=quantity, _type='short')
    if _id:
        order_option_by_id(_id, price, quantity, direction='debit', effect='close', side='buy',
                           time_in_force=time_in_force)


@helper.login_required
def order_option_sell_to_open(price, symbol, quantity, expiration_date, strike, option_type='both',
                              time_in_force='gfd'):
    """Submits a limit order for an option. i.e. place a short call or a short put.

    :param price: The limit price to trigger a sell of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to sell.
    :type quantity: int
    :param expiration_date: The expiration date of the option in 'YYYY-MM-DD' format.
    :type expiration_date: str
    :param strike: The strike price of the option.
    :type strike: float
    :param option_type: This should be 'call' or 'put'
    :type option_type: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    option_id = helper.id_for_option(symbol, expiration_date, str(strike), option_type)

    payload = {
        'account': profiles.load_account_profile(info='url'),
        'direction': 'credit',
        'time_in_force': time_in_force,
        'legs': [
            {'position_effect': 'open', 'side': 'sell', 'ratio_quantity': 1,
             'option': urls.option_instruments(option_id)},
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

    return data


@helper.login_required
def order_buy_crypto_by_price(symbol, amount_in_dollars, price_type='ask_price', time_in_force='gtc'):
    """Submits a market order for a crypto by specifying the amount in dollars that you want to trade.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param amount_in_dollars: The amount in dollars of the crypto you want to buy.
    :type amount_in_dollars: float
    :param price_type: The type of price to get. Can be 'ask_price', 'bid_price', or 'mark_price'
    :type price_type: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    crypto_info = crypto.get_crypto_info(symbol)
    price = helper.round_price(crypto.get_crypto_quote_from_id(crypto_info['id'], info=price_type))
    # turn the money amount into decimal number of shares
    try:
        shares = round(amount_in_dollars / price, 8)
    except Exception as e:
        print(repr(e))
        shares = 0

    payload = {
        'mimeType': 'application/json',
        'account_id': crypto.load_crypto_profile(info="id"),
        'currency_pair_id': crypto_info['id'],
        'price': price,
        'quantity': shares,
        'ref_id': str(uuid4()),
        'side': 'buy',
        'time_in_force': time_in_force,
        'type': 'market'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return data


@helper.login_required
def order_buy_crypto_by_quantity(symbol, quantity, price_type='ask_price', time_in_force='gtc'):
    """Submits a market order for a crypto by specifying the decimal amount of shares to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to buy.
    :type quantity: float
    :param price_type: The type of price to get. Can be 'ask_price', 'bid_price', or 'mark_price'
    :type price_type: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """

    crypto_info = crypto.get_crypto_info(symbol)

    price = helper.round_price(crypto.get_crypto_quote_from_id(crypto_info['id'], info=price_type))

    payload = {
        'account_id': crypto.load_crypto_profile(info="id"),
        'currency_pair_id': crypto_info['id'],
        'price': price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'side': 'buy',
        'time_in_force': time_in_force,
        'type': 'market'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return data


@helper.login_required
def order_sell_crypto_by_price(symbol, amount_in_dollars, price_type='ask_price', time_in_force='gtc'):
    """Submits a market order for a crypto by specifying the amount in dollars that you want to trade.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param amount_in_dollars: The amount in dollars of the crypto you want to sell.
    :type amount_in_dollars: float
    :param price_type: The type of price to get. Can be 'ask_price', 'bid_price', or 'mark_price'
    :type price_type: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    crypto_info = crypto.get_crypto_info(symbol)
    price = helper.round_price(crypto.get_crypto_quote_from_id(crypto_info['id'], info=price_type))
    # turn the money amount into decimal number of shares
    try:
        shares = round(amount_in_dollars / float(price), 8)
    except Exception as e:
        print(repr(e))
        shares = 0

    payload = {
        'account_id': crypto.load_crypto_profile(info="id"),
        'currency_pair_id': crypto_info['id'],
        'price': price,
        'quantity': shares,
        'ref_id': str(uuid4()),
        'side': 'sell',
        'time_in_force': time_in_force,
        'type': 'market'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return data


@helper.login_required
def order_sell_crypto_by_quantity(symbol, quantity, price_type='ask_price', time_in_force='gtc'):
    """Submits a market order for a crypto by specifying the decimal amount of shares to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to sell.
    :type quantity: float
    :param price_type: The type of price to get. Can be 'ask_price', 'bid_price', or 'mark_price'
    :type price_type: str
    :param time_in_force: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type time_in_force: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.), \
    the price, and the quantity.

    """

    crypto_info = crypto.get_crypto_info(symbol)
    price = helper.round_price(crypto.get_crypto_quote_from_id(crypto_info['id'], info=price_type))

    payload = {
        'account_id': crypto.load_crypto_profile(info="id"),
        'currency_pair_id': crypto_info['id'],
        'price': price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'side': 'sell',
        'time_in_force': time_in_force,
        'type': 'market'
    }

    url = urls.order_crypto()
    data = helper.request_post(url, payload, json=True)

    return data
