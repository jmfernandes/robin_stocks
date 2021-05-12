"""Contains all functions for placing orders for stocks, options, and crypto."""
from uuid import uuid4

from robin_stocks.robinhood.crypto import *
from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.profiles import *
from robin_stocks.robinhood.stocks import *
from robin_stocks.robinhood.urls import *

@login_required
def get_all_stock_orders(info=None):
    """Returns a list of all the orders that have been processed for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = orders_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


@login_required
def get_all_option_orders(info=None):
    """Returns a list of all the option orders that have been processed for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = option_orders_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


@login_required
def get_all_crypto_orders(info=None):
    """Returns a list of all the crypto orders that have been processed for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = crypto_orders_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


@login_required
def get_all_open_stock_orders(info=None):
    """Returns a list of all the orders that are currently open.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = orders_url()
    data = request_get(url, 'pagination')

    data = [item for item in data if item['cancel'] is not None]

    return(filter_data(data, info))


@login_required
def get_all_open_option_orders(info=None):
    """Returns a list of all the orders that are currently open.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = option_orders_url()
    data = request_get(url, 'pagination')

    data = [item for item in data if item['cancel_url'] is not None]

    return(filter_data(data, info))


@login_required
def get_all_open_crypto_orders(info=None):
    """Returns a list of all the crypto orders that have been processed for the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each option order. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = crypto_orders_url()
    data = request_get(url, 'pagination')

    data = [item for item in data if item['cancel_url'] is not None]

    return(filter_data(data, info))


@login_required
def get_stock_order_info(orderID):
    """Returns the information for a single order.

    :param orderID: The ID associated with the order. Can be found using get_all_orders(info=None) or get_all_orders(info=None).
    :type orderID: str
    :returns: Returns a list of dictionaries of key/value pairs for the order.

    """
    url = orders_url(orderID)
    data = request_get(url)
    return(data)


@login_required
def get_option_order_info(order_id):
    """Returns the information for a single option order.

    :param order_id: The ID associated with the option order.
    :type order_id: str
    :returns: Returns a list of dictionaries of key/value pairs for the order.

    """
    url = option_orders_url(order_id)
    data = request_get(url)
    return data


@login_required
def get_crypto_order_info(order_id):
    """Returns the information for a single crypto order.

    :param order_id: The ID associated with the option order.
    :type order_id: str
    :returns: Returns a list of dictionaries of key/value pairs for the order.

    """
    url = crypto_orders_url(order_id)
    data = request_get(url)
    return data


@login_required
def find_stock_orders(**arguments):
    """Returns a list of orders that match the keyword parameters.

    :param arguments: Variable length of keyword arguments. EX. find_orders(symbol='FB',cancel=None,quantity=1)
    :type arguments: str
    :returns: Returns a list of orders.

    """ 
    url = orders_url()
    data = request_get(url, 'pagination')

    if (len(arguments) == 0):
        return(data)

    for item in data:
        item['quantity'] = str(int(float(item['quantity'])))

    if 'symbol' in arguments.keys():
        arguments['instrument'] = get_instruments_by_symbols(
            arguments['symbol'], info='url')[0]
        del arguments['symbol']

    if 'quantity' in arguments.keys():
        arguments['quantity'] = str(arguments['quantity'])

    stop = len(arguments.keys())-1
    list_of_orders = []
    for item in data:
        for i, (key, value) in enumerate(arguments.items()):
            if key not in item:
                print(error_argument_not_key_in_dictionary(key), file=get_output())
                return([None])
            if value != item[key]:
                break
            if i == stop:
                list_of_orders.append(item)

    return(list_of_orders)


@login_required
def cancel_stock_order(orderID):
    """Cancels a specific order.

    :param orderID: The ID associated with the order. Can be found using get_all_stock_orders(info=None).
    :type orderID: str
    :returns: Returns the order information for the order that was cancelled.

    """ 
    url = cancel_url(orderID)
    data = request_post(url)

    if data:
        print('Order '+str(orderID)+' cancelled', file=get_output())
    return(data)


@login_required
def cancel_option_order(orderID):
    """Cancels a specific option order.

    :param orderID: The ID associated with the order. Can be found using get_all_option_orders(info=None).
    :type orderID: str
    :returns: Returns the order information for the order that was cancelled.

    """ 
    url = option_cancel_url(orderID)
    data = request_post(url)

    if data:
        print('Order '+str(orderID)+' cancelled', file=get_output())
    return(data)


@login_required
def cancel_crypto_order(orderID):
    """Cancels a specific crypto order.

    :param orderID: The ID associated with the order. Can be found using get_all_crypto_orders(info=None).
    :type orderID: str
    :returns: Returns the order information for the order that was cancelled.

    """ 
    url = crypto_cancel_url(orderID)
    data = request_post(url)

    if data:
        print('Order '+str(orderID)+' cancelled', file=get_output())
    return(data)


@login_required
def cancel_all_stock_orders():
    """Cancels all stock orders.

    :returns: The list of orders that were cancelled.

    """ 
    url = orders_url()
    data = request_get(url, 'pagination')

    data = [item for item in data if item['cancel'] is not None]

    for item in data:
        request_post(item['cancel'])

    print('All Stock Orders Cancelled', file=get_output())
    return(data)


@login_required
def cancel_all_option_orders():
    """Cancels all option orders.

    :returns: Returns the order information for the orders that were cancelled.

    """ 
    url = option_orders_url()
    data = request_get(url, 'pagination')

    data = [item for item in data if item['cancel_url'] is not None]

    for item in data:
        request_post(item['cancel_url'])

    print('All Option Orders Cancelled', file=get_output())
    return(data)


@login_required
def cancel_all_crypto_orders():
    """Cancels all crypto orders.

    :returns: Returns the order information for the orders that were cancelled.

    """ 
    url = crypto_orders_url()
    data = request_get(url, 'pagination')

    data = [item for item in data if item['cancel_url'] is not None]

    for item in data:
        request_post(item['cancel_url'])

    print('All Crypto Orders Cancelled', file=get_output())
    return(data)


@login_required
def order_buy_market(symbol, quantity, timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a market order to be executed immediately.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "buy", None, None, timeInForce, extendedHours, jsonify)


@login_required
def order_buy_fractional_by_quantity(symbol, quantity, timeInForce='gfd', extendedHours=False, jsonify=True):
    """Submits a market order to be executed immediately for fractional shares by specifying the amount that you want to trade.
    Good for share fractions up to 6 decimal places. Robinhood does not currently support placing limit, stop, or stop loss orders
    for fractional trades.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The amount of the fractional shares you want to buy.
    :type quantity: float
    :param timeInForce: Changes how long the order will be in effect for. 'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "buy", None, None, timeInForce, extendedHours, jsonify)


@login_required
def order_buy_fractional_by_price(symbol, amountInDollars, timeInForce='gfd', extendedHours=False, jsonify=True):
    """Submits a market order to be executed immediately for fractional shares by specifying the amount in dollars that you want to trade.
    Good for share fractions up to 6 decimal places. Robinhood does not currently support placing limit, stop, or stop loss orders
    for fractional trades.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param amountInDollars: The amount in dollars of the fractional shares you want to buy.
    :type amountInDollars: float
    :param timeInForce: Changes how long the order will be in effect for. 'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    if amountInDollars < 1:
        print("ERROR: Fractional share price should meet minimum 1.00.", file=get_output())
        return None

    # turn the money amount into decimal number of shares
    price = next(iter(get_latest_price(symbol, 'ask_price', extendedHours)), 0.00)
    fractional_shares = 0 if (price == 0.00) else round_price(amountInDollars/float(price))

    return order(symbol, fractional_shares, "buy", None, None, timeInForce, extendedHours, jsonify)


@login_required
def order_buy_limit(symbol, quantity, limitPrice, timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a limit order to be executed once a certain price is reached.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param limitPrice: The price to trigger the buy order.
    :type limitPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "buy", limitPrice, None, timeInForce, extendedHours, jsonify)


@login_required
def order_buy_stop_loss(symbol, quantity, stopPrice, timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a stop order to be turned into a market order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param stopPrice: The price to trigger the market order.
    :type stopPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "buy", None, stopPrice, timeInForce, extendedHours, jsonify)


@login_required
def order_buy_stop_limit(symbol, quantity, limitPrice, stopPrice, timeInForce='gtc', extendedHours=False, jsonify=True):
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
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "buy", limitPrice, stopPrice, timeInForce, extendedHours, jsonify)


@login_required
def order_buy_trailing_stop(symbol, quantity, trailAmount, trailType='percentage', timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a trailing stop buy order to be turned into a market order when traling stop price reached.

    :param symbol: The stock ticker of the stock to buy.
    :type symbol: str
    :param quantity: The number of stocks to buy.
    :type quantity: int
    :param trailAmount: how much to trail by; could be percentage or dollar value depending on trailType
    :type trailAmount: float
    :param trailType: could be "amount" or "percentage"
    :type trailType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    return order_trailing_stop(symbol, quantity, "buy", trailAmount, trailType, timeInForce, extendedHours, jsonify)


@login_required
def order_sell_market(symbol, quantity, timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a market order to be executed immediately.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "sell", None, None, timeInForce, extendedHours, jsonify)


@login_required
def order_sell_fractional_by_quantity(symbol, quantity, timeInForce='gfd', priceType='bid_price', extendedHours=False, jsonify=True):
    """Submits a market order to be executed immediately for fractional shares by specifying the amount that you want to trade.
    Good for share fractions up to 6 decimal places. Robinhood does not currently support placing limit, stop, or stop loss orders
    for fractional trades.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param quantity: The amount of the fractional shares you want to buy.
    :type quantity: float
    :param timeInForce: Changes how long the order will be in effect for. 'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "sell", None, None, timeInForce, extendedHours, jsonify)


@login_required
def order_sell_fractional_by_price(symbol, amountInDollars, timeInForce='gfd', extendedHours=False, jsonify=True):
    """Submits a market order to be executed immediately for fractional shares by specifying the amount in dollars that you want to trade.
    Good for share fractions up to 6 decimal places. Robinhood does not currently support placing limit, stop, or stop loss orders
    for fractional trades.

    :param symbol: The stock ticker of the stock to purchase.
    :type symbol: str
    :param amountInDollars: The amount in dollars of the fractional shares you want to buy.
    :type amountInDollars: float
    :param timeInForce: Changes how long the order will be in effect for. 'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    if amountInDollars < 1:
        print("ERROR: Fractional share price should meet minimum 1.00.", file=get_output())
        return None
    # turn the money amount into decimal number of shares
    price = next(iter(get_latest_price(symbol, 'bid_price', extendedHours)), 0.00)
    fractional_shares = 0 if (price == 0.00) else round_price(amountInDollars/float(price))

    return order(symbol, fractional_shares, "sell", None, None, timeInForce, extendedHours, jsonify)


@login_required
def order_sell_limit(symbol, quantity, limitPrice, timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a limit order to be executed once a certain price is reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param limitPrice: The price to trigger the sell order.
    :type limitPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "sell", limitPrice, None, timeInForce, extendedHours, jsonify)


@login_required
def order_sell_stop_loss(symbol, quantity, stopPrice, timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a stop order to be turned into a market order once a certain stop price is reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param stopPrice: The price to trigger the market order.
    :type stopPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "sell", None, stopPrice, timeInForce, extendedHours, jsonify)


@login_required
def order_sell_stop_limit(symbol, quantity, limitPrice, stopPrice, timeInForce='gtc', extendedHours=False, jsonify=True):
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
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order(symbol, quantity, "sell", limitPrice, stopPrice, timeInForce, extendedHours, jsonify)


@login_required
def order_sell_trailing_stop(symbol, quantity, trailAmount, trailType='percentage', timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a trailing stop sell order to be turned into a market order when traling stop price reached.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param trailAmount: how much to trail by; could be percentage or dollar value depending on trailType
    :type trailAmount: float
    :param trailType: could be "amount" or "percentage"
    :type trailType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    return order_trailing_stop(symbol, quantity, "sell", trailAmount, trailType, timeInForce, extendedHours, jsonify)


@login_required
def order_trailing_stop(symbol, quantity, side, trailAmount, trailType='percentage', timeInForce='gtc', extendedHours=False, jsonify=True):
    """Submits a trailing stop order to be turned into a market order when traling stop price reached.

    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of stocks to trade.
    :type quantity: int
    :param side: buy or sell
    :type side: str
    :param trailAmount: how much to trail by; could be percentage or dollar value depending on trailType
    :type trailAmount: float
    :param trailType: could be "amount" or "percentage"
    :type trailType: str
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: Optional[str]
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
        trailAmount = float(trailAmount)
    except AttributeError as message:
        print(message)
        return None

    stock_price = round_price(get_latest_price(symbol, extendedHours)[0])

    # find stop price based on whether trailType is "amount" or "percentage" and whether its buy or sell
    percentage = 0
    try:
        if trailType == 'amount':
            margin = trailAmount
        else:
            margin = stock_price * trailAmount * 0.01
            percentage = trailAmount
    except Exception as e:
        print('ERROR: {}'.format(e))
        return None

    stopPrice = stock_price + margin if side == "buy" else stock_price - margin
    stopPrice = round_price(stopPrice)

    payload = {
        'account': load_account_profile(info='url'),
        'instrument': get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': 'market',
        'stop_price': stopPrice,
        'time_in_force': timeInForce,
        'trigger': 'stop',
        'side': side,
        'extended_hours': extendedHours
    }

    if side == "buy":
        # price should be greater than stopPrice, adding a 5% threshold
        payload['price'] = round_price(stopPrice * 1.05)

    if trailType == 'amount':
        payload['trailing_peg'] = {'type': 'price', 'price': {'amount': trailAmount, 'currency_code': 'USD'}}
    else:
        payload['trailing_peg'] = {'type': 'percentage', 'percentage': str(percentage)}

    url = orders_url()
    data = request_post(url, payload, json=True, jsonify_data=jsonify)

    return (data)


@login_required
def order(symbol, quantity, side, limitPrice=None, stopPrice=None, timeInForce='gtc', extendedHours=False, jsonify=True):
    """A generic order function.

    :param symbol: The stock ticker of the stock to sell.
    :type symbol: str
    :param quantity: The number of stocks to sell.
    :type quantity: int
    :param side: Either 'buy' or 'sell'
    :type side: str
    :param limitPrice: The price to trigger the market order.
    :type limitPrice: float
    :param stopPrice: The price to trigger the limit or market order.
    :type stopPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled. \
    'gfd' = good for the day.
    :type timeInForce: str
    :param extendedHours: Premium users only. Allows trading during extended hours. Should be true or false.
    :type extendedHours: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the purchase or selling of stocks, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    orderType = "market"
    trigger = "immediate"

    if side == "buy":
        priceType = "ask_price"
    else:
        priceType = "bid_price"

    if limitPrice and stopPrice:
        price = round_price(limitPrice)
        stopPrice = round_price(stopPrice)
        orderType = "limit"
        trigger = "stop"
    elif limitPrice:
        price = round_price(limitPrice)
        orderType = "limit"
    elif stopPrice:
        stopPrice = round_price(stopPrice)
        if side == "buy":
            price = stopPrice
        else:
            price = None
        trigger = "stop"
    else:
        price = round_price(next(iter(get_latest_price(symbol, priceType, extendedHours)), 0.00))

    payload = {
        'account': load_account_profile(info='url'),
        'instrument': get_instruments_by_symbols(symbol, info='url')[0],
        'symbol': symbol,
        'price': price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'type': orderType,
        'stop_price': stopPrice,
        'time_in_force': timeInForce,
        'trigger': trigger,
        'side': side,
        'extended_hours': extendedHours
    }

    url = orders_url()
    data = request_post(url, payload, jsonify_data=jsonify)

    return(data)


@login_required
def order_option_credit_spread(price, symbol, quantity, spread, timeInForce='gtc', jsonify=True):
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
        - optionType: This should be 'call' or 'put'.\n
        - effect: This should be 'open' or 'close'.\n
        - action: This should be 'buy' or 'sell'.
    :type spread: dict
    :param timeInForce: Changes how long the order will be in effect for. \
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' = execute at opening.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the trading of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    return(order_option_spread("credit", price, symbol, quantity, spread, timeInForce, jsonify))


@login_required
def order_option_debit_spread(price, symbol, quantity, spread, timeInForce='gtc', jsonify=True):
    """Submits a limit order for an option debit spread.

    :param price: The limit price to trigger a sell of the option.
    :type price: float
    :param symbol: The stock ticker of the stock to trade.
    :type symbol: str
    :param quantity: The number of options to sell.
    :type quantity: int
    :param spread: A dictionary of spread options with the following keys: \n
        - expirationDate: The expiration date of the option in 'YYYY-MM-DD' format.\n
        - strike: The strike price of the option.\n
        - optionType: This should be 'call' or 'put'.\n
        - effect: This should be 'open' or 'close'.\n
        - action: This should be 'buy' or 'sell'.
    :type spread: dict
    :param timeInForce: Changes how long the order will be in effect for.
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the trading of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.
    """
    return(order_option_spread("debit", price, symbol, quantity, spread, timeInForce, jsonify))


@login_required
def order_option_spread(direction, price, symbol, quantity, spread, timeInForce='gtc', jsonify=True):
    """Submits a limit order for an option spread. i.e. place a debit / credit spread

    :param direction: Can be "credit" or "debit".
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
        - optionType: This should be 'call' or 'put'.\n
        - effect: This should be 'open' or 'close'.\n
        - action: This should be 'buy' or 'sell'.
    :type spread: dict
    :param timeInForce: Changes how long the order will be in effect for.
     'gtc' = good until cancelled. \
     'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the trading of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.
    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None
    legs = []
    for each in spread:
        optionID = id_for_option(symbol,
                                        each['expirationDate'],
                                        each['strike'],
                                        each['optionType'])
        legs.append({'position_effect': each['effect'],
                     'side': each['action'],
                     'ratio_quantity': 1,
                     'option': option_instruments_url(optionID)})

    payload = {
        'account': load_account_profile(info='url'),
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

    url = option_orders_url()
    data = request_post(url, payload, json=True, jsonify_data=jsonify)

    return(data)


@login_required
def order_buy_option_limit(positionEffect, creditOrDebit, price, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gtc', jsonify=True):
    """Submits a limit order for an option. i.e. place a long call or a long put.

    :param positionEffect: Either 'open' for a buy to open effect or 'close' for a buy to close effect.
    :type positionEffect: str
    :param creditOrDebit: Either 'debit' or 'credit'.
    :type creditOrDebit: str
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
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the buying of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    optionID = id_for_option(symbol, expirationDate, strike, optionType)

    payload = {
        'account': load_account_profile(info='url'),
        'direction': creditOrDebit,
        'time_in_force': timeInForce,
        'legs': [
            {'position_effect': positionEffect, 'side': 'buy',
                'ratio_quantity': 1, 'option': option_instruments_url(optionID)},
        ],
        'type': 'limit',
        'trigger': 'immediate',
        'price': price,
        'quantity': quantity,
        'override_day_trade_checks': False,
        'override_dtbp_checks': False,
        'ref_id': str(uuid4()),
    }

    url = option_orders_url()
    data = request_post(url, payload, json=True, jsonify_data=jsonify)

    return(data)


@login_required
def order_buy_option_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gtc', jsonify=True):
    """Submits a stop order to be turned into a limit order once a certain stop price is reached.

    :param positionEffect: Either 'open' for a buy to open effect or 'close' for a buy to close effect.
    :type positionEffect: str
    :param creditOrDebit: Either 'debit' or 'credit'.
    :type creditOrDebit: str
    :param limitPrice: The limit price to trigger a buy of the option.
    :type limitPrice: float
    :param stopPrice: The price to trigger the limit order.
    :type stopPrice: float
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
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the buying of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    optionID = id_for_option(symbol, expirationDate, strike, optionType)

    payload = {
        'account': load_account_profile(info='url'),
        'direction': creditOrDebit,
        'time_in_force': timeInForce,
        'legs': [
            {'position_effect': positionEffect, 'side': 'buy',
                'ratio_quantity': 1, 'option': option_instruments_url(optionID)},
        ],
        'type': 'limit',
        'trigger': 'stop',
        'price': limitPrice,
        'stop_price': stopPrice,
        'quantity': quantity,
        'override_day_trade_checks': False,
        'override_dtbp_checks': False,
        'ref_id': str(uuid4()),
    }

    url = option_orders_url()
    data = request_post(url, payload, json=True, jsonify_data=jsonify)

    return(data)


def order_sell_option_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gtc', jsonify=True):
    """Submits a stop order to be turned into a limit order once a certain stop price is reached.

    :param positionEffect: Either 'open' for a buy to open effect or 'close' for a buy to close effect.
    :type positionEffect: str
    :param creditOrDebit: Either 'debit' or 'credit'.
    :type creditOrDebit: str
    :param limitPrice: The limit price to trigger a buy of the option.
    :type limitPrice: float
    :param stopPrice: The price to trigger the limit order.
    :type stopPrice: float
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
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the buying of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    optionID = id_for_option(symbol, expirationDate, strike, optionType)

    payload = {
        'account': load_account_profile(info='url'),
        'direction': creditOrDebit,
        'time_in_force': timeInForce,
        'legs': [
            {'position_effect': positionEffect, 'side': 'sell',
                'ratio_quantity': 1, 'option': option_instruments_url(optionID)},
        ],
        'type': 'limit',
        'trigger': 'stop',
        'price': limitPrice,
        'stop_price': stopPrice,
        'quantity': quantity,
        'override_day_trade_checks': False,
        'override_dtbp_checks': False,
        'ref_id': str(uuid4()),
    }

    url = option_orders_url()
    data = request_post(url, payload, json=True, jsonify_data=jsonify)

    return(data)


@login_required
def order_sell_option_limit(positionEffect, creditOrDebit, price, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gtc', jsonify=True):
    """Submits a limit order for an option. i.e. place a short call or a short put.

    :param positionEffect: Either 'open' for a sell to open effect or 'close' for a sell to close effect.
    :type positionEffect: str
    :param creditOrDebit: Either 'debit' or 'credit'.
    :type creditOrDebit: str
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
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of options, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    optionID = id_for_option(symbol, expirationDate, strike, optionType)

    payload = {
        'account': load_account_profile(info='url'),
        'direction': creditOrDebit,
        'time_in_force': timeInForce,
        'legs': [
            {'position_effect': positionEffect, 'side': 'sell',
                'ratio_quantity': 1, 'option': option_instruments_url(optionID)},
        ],
        'type': 'limit',
        'trigger': 'immediate',
        'price': price,
        'quantity': quantity,
        'override_day_trade_checks': False,
        'override_dtbp_checks': False,
        'ref_id': str(uuid4()),
    }

    url = option_orders_url()
    data = request_post(url, payload, json=True, jsonify_data=jsonify)

    return(data)


@login_required
def order_buy_crypto_by_price(symbol, amountInDollars, timeInForce='gtc', jsonify=True):
    """Submits a market order for a crypto by specifying the amount in dollars that you want to trade.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param amountInDollars: The amount in dollars of the crypto you want to buy.
    :type amountInDollars: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the buying of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order_crypto(symbol, "buy", amountInDollars, "price", None, timeInForce, jsonify)


@login_required
def order_buy_crypto_by_quantity(symbol, quantity, timeInForce='gtc', jsonify=True):
    """Submits a market order for a crypto by specifying the decimal amount of shares to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to buy.
    :type quantity: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the buying of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order_crypto(symbol, "buy", quantity, "quantity", None, timeInForce, jsonify)


@login_required
def order_buy_crypto_limit(symbol, quantity, limitPrice, timeInForce='gtc', jsonify=True):
    """Submits a limit order for a crypto by specifying the decimal amount of shares to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to buy.
    :type quantity: float
    :param limitPrice: The limit price to set for the crypto.
    :type limitPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the buying of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order_crypto(symbol, "buy", quantity, "quantity", limitPrice, timeInForce, jsonify)


@login_required
def order_buy_crypto_limit_by_price(symbol, amountInDollars, limitPrice, timeInForce='gtc', jsonify=True):
    """Submits a limit order for a crypto by specifying the decimal price to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param amountInDollars: The amount in dollars of the crypto you want to buy.
    :type amountInDollars: float
    :param limitPrice: The limit price to set for the crypto.
    :type limitPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the buying of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    return order_crypto(symbol, "buy", amountInDollars, "price", limitPrice, timeInForce, jsonify)


@login_required
def order_sell_crypto_by_price(symbol, amountInDollars, timeInForce='gtc', jsonify=True):
    """Submits a market order for a crypto by specifying the amount in dollars that you want to trade.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param amountInDollars: The amount in dollars of the crypto you want to sell.
    :type amountInDollars: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order_crypto(symbol, "sell", amountInDollars, "price", None, timeInForce, jsonify)


@login_required
def order_sell_crypto_by_quantity(symbol, quantity, timeInForce='gtc', jsonify=True):
    """Submits a market order for a crypto by specifying the decimal amount of shares to buy.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to sell.
    :type quantity: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """ 
    return order_crypto(symbol, "sell", quantity, "quantity", None, timeInForce, jsonify)


@login_required
def order_sell_crypto_limit(symbol, quantity, limitPrice, timeInForce='gtc', jsonify=True):
    """Submits a limit order for a crypto by specifying the decimal amount of shares to sell.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param quantity: The decimal amount of shares to sell.
    :type quantity: float
    :param limitPrice: The limit price to set for the crypto.
    :type limitPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    return order_crypto(symbol, "sell", quantity, "quantity", limitPrice, timeInForce, jsonify)


@login_required
def order_sell_crypto_limit_by_price(symbol, amountInDollars, limitPrice, timeInForce='gtc', jsonify=True):
    """Submits a limit order for a crypto by specifying the decimal price to sell.
    Good for share fractions up to 8 decimal places.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param amountInDollars: The amount in dollars of the crypto you want to sell.
    :type amountInDollars: float
    :param limitPrice: The limit price to set for the crypto.
    :type limitPrice: float
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the buying of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    return order_crypto(symbol, "sell", amountInDollars, "price", limitPrice, timeInForce, jsonify)


@login_required
def order_crypto(symbol, side, quantityOrPrice, amountIn="quantity", limitPrice=None, timeInForce="gtc", jsonify=True):
    """Submits an order for a crypto.

    :param symbol: The crypto ticker of the crypto to trade.
    :type symbol: str
    :param side: Either 'buy' or 'sell'
    :type side: str
    :param quantityOrPrice: Either the decimal price of shares to trade or the decimal quantity of shares.
    :type quantityOrPrice: float
    :param amountIn: If left default value of 'quantity', order will attempt to trade cryptos by the amount of crypto \
        you want to trade. If changed to 'price', order will attempt to trade cryptos by the price you want to buy or sell.
    :type amountIn: Optional[str]
    :param limitPrice: The price to trigger the market order.
    :type limitPrice: Optional[float]
    :param timeInForce: Changes how long the order will be in effect for. 'gtc' = good until cancelled.
    :type timeInForce: Optional[str]
    :param jsonify: If set to False, function will return the request object which contains status code and headers.
    :type jsonify: Optional[str]
    :returns: Dictionary that contains information regarding the selling of crypto, \
    such as the order id, the state of order (queued, confired, filled, failed, canceled, etc.), \
    the price, and the quantity.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message, file=get_output())
        return None

    crypto_id = get_crypto_id(symbol)
    orderType = "market"

    if side == "buy":
        priceType = "ask_price"
    else:
        priceType = "bid_price"

    if limitPrice:
        price = limitPrice
        orderType = "limit"
    else:
        price = round_price(get_crypto_quote_from_id(crypto_id, info=priceType))

    if amountIn == "quantity":
        quantity = quantityOrPrice
    else:
        quantity = round_price(quantityOrPrice/price)

    payload = {
        'account_id': load_crypto_profile(info="id"),
        'currency_pair_id': crypto_id,
        'price': price,
        'quantity': quantity,
        'ref_id': str(uuid4()),
        'side': side,
        'time_in_force': timeInForce,
        'type': orderType
    }

    url = order_crypto_url()

    # This is safe because 'ref_id' guards us from duplicate orders
    attempts = 3
    while attempts > 0:
        data = request_post(url, payload, json=True, jsonify_data=jsonify)
        if data is not None:
            break

        attempts -= 1

    return(data)
