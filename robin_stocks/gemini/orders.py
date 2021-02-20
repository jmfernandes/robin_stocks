from robin_stocks.gemini.authentication import (generate_order_id,
                                                generate_signature)
from robin_stocks.gemini.crypto import get_price
from robin_stocks.gemini.helper import (format_inputs, login_required,
                                        request_post)
from robin_stocks.gemini.urls import URLS


@login_required
@format_inputs
def get_trades_for_crypto(ticker, limit_trades=50, timestamp=None, jsonify=None):
    """ Gets a list of all transactions for a certain crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param limit_trades: The maximum number of trades to return. Default is 50, max is 500.
    :type limit_trades: Optional[int]
    :param timestamp: Only return trades on or after this timestamp. If not present, will show the most recent orders
    :type timestamp: Optional[str]
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a list of dictionaries parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionaries are listed below.
    :Dictionary Keys: * price
                      * amount
                      * timestamp
                      * timestampms
                      * type
                      * aggressor
                      * fee_currency
                      * fee_amount
                      * tid
                      * order_id
                      * exchange
                      * is_auction_fill
                      * client_order_id

    """
    url = URLS.mytrades()
    payload = {
        "request": URLS.get_endpoint(url),
        "symbol": ticker,
        "limit_trades": limit_trades
    }
    if timestamp:
        payload["timestamp"] = timestamp

    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def cancel_all_session_orders(jsonify=None):
    """ Cancel all orders opened by the session.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * result
                      * details

    """
    url = URLS.cancel_session_orders()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def cancel_all_active_orders(jsonify=None):
    """ Cancel all orders for all sessions opened by the account.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * result
                      * details

    """
    url = URLS.cancel_active_orders()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def cancel_order(order_id, jsonify=None):
    """ Cancel a specific order based on ID.

    :param order_id: The id of the order. This is not the same as the client order ID.
    :type order_id: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * order_id - The order id
                      * client_order_id - An optional client-specified order id
                      * symbol - The symbol of the order
                      * exchange - Will always be "gemini"
                      * price - The price the order was issued at
                      * avg_execution_price - The average price at which this order as been executed so far. 0 if the order has not been executed at all.
                      * side - Either "buy" or "sell".
                      * type - Description of the order.
                      * options - An array containing at most one supported order execution option.
                      * timestamp - The timestamp the order was submitted. Note that for compatibility reasons, this is returned as a string. We recommend using the timestampms field instead.
                      * timestampms - The timestamp the order was submitted in milliseconds.
                      * is_live - true if the order is active on the book (has remaining quantity and has not been canceled)
                      * is_cancelled - true if the order has been canceled. Note the spelling, "cancelled" instead of "canceled". This is for compatibility reasons.
                      * reason - Populated with the reason your order was canceled, if available.
                      * was_forced - Will always be false.
                      * executed_amount - The amount of the order that has been filled.
                      * remaining_amount - The amount of the order that has not been filled.
                      * original_amount - The originally submitted amount of the order.
                      * is_hidden - Will always return false unless the order was placed with the indication-of-interest execution option.

    """
    url = URLS.cancel_order()
    payload = {
        "request": URLS.get_endpoint(url),
        "order_id": order_id
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def order_status(order_id, jsonify=None):
    """ Get the status for an order.

    :param order_id: The id of the order. This is not the same as the client order ID.
    :type order_id: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * order_id - The order id
                      * client_order_id - An optional client-specified order id
                      * symbol - The symbol of the order
                      * exchange - Will always be "gemini"
                      * price - The price the order was issued at
                      * avg_execution_price - The average price at which this order as been executed so far. 0 if the order has not been executed at all.
                      * side - Either "buy" or "sell".
                      * type - Description of the order.
                      * options - An array containing at most one supported order execution option.
                      * timestamp - The timestamp the order was submitted. Note that for compatibility reasons, this is returned as a string. We recommend using the timestampms field instead.
                      * timestampms - The timestamp the order was submitted in milliseconds.
                      * is_live - true if the order is active on the book (has remaining quantity and has not been canceled)
                      * is_cancelled - true if the order has been canceled. Note the spelling, "cancelled" instead of "canceled". This is for compatibility reasons.
                      * reason - Populated with the reason your order was canceled, if available.
                      * was_forced - Will always be false.
                      * executed_amount - The amount of the order that has been filled.
                      * remaining_amount - The amount of the order that has not been filled.
                      * original_amount - The originally submitted amount of the order.
                      * is_hidden - Will always return false unless the order was placed with the indication-of-interest execution option.

    """
    url = URLS.order_status()
    payload = {
        "request": URLS.get_endpoint(url),
        "order_id": order_id
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def active_orders(jsonify=None):
    """ Get a list of all active orders.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a list of dictionaries parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionaries are listed below.
    :Dictionary Keys: * order_id - The order id
                      * client_order_id - An optional client-specified order id
                      * symbol - The symbol of the order
                      * exchange - Will always be "gemini"
                      * price - The price the order was issued at
                      * avg_execution_price - The average price at which this order as been executed so far. 0 if the order has not been executed at all.
                      * side - Either "buy" or "sell".
                      * type - Description of the order.
                      * options - An array containing at most one supported order execution option.
                      * timestamp - The timestamp the order was submitted. Note that for compatibility reasons, this is returned as a string. We recommend using the timestampms field instead.
                      * timestampms - The timestamp the order was submitted in milliseconds.
                      * is_live - true if the order is active on the book (has remaining quantity and has not been canceled)
                      * is_cancelled - true if the order has been canceled. Note the spelling, "cancelled" instead of "canceled". This is for compatibility reasons.
                      * reason - Populated with the reason your order was canceled, if available.
                      * was_forced - Will always be false.
                      * executed_amount - The amount of the order that has been filled.
                      * remaining_amount - The amount of the order that has not been filled.
                      * original_amount - The originally submitted amount of the order.
                      * is_hidden - Will always return false unless the order was placed with the indication-of-interest execution option.
    """
    url = URLS.active_orders()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def order_market(ticker, quantity, side, jsonify=None):
    """ Gemini does not directly support market orders. This function will try to immediately
    place an order or it will cancel it.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param quantity: The amount to trade.
    :type quantity: str
    :param side: Either "buy" or "sell".
    :type side: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * order_id - The order id
                      * client_order_id - An optional client-specified order id
                      * symbol - The symbol of the order
                      * exchange - Will always be "gemini"
                      * price - The price the order was issued at
                      * avg_execution_price - The average price at which this order as been executed so far. 0 if the order has not been executed at all.
                      * side - Either "buy" or "sell".
                      * type - Description of the order.
                      * options - An array containing at most one supported order execution option.
                      * timestamp - The timestamp the order was submitted. Note that for compatibility reasons, this is returned as a string. We recommend using the timestampms field instead.
                      * timestampms - The timestamp the order was submitted in milliseconds.
                      * is_live - true if the order is active on the book (has remaining quantity and has not been canceled)
                      * is_cancelled - true if the order has been canceled. Note the spelling, "cancelled" instead of "canceled". This is for compatibility reasons.
                      * reason - Populated with the reason your order was canceled, if available.
                      * was_forced - Will always be false.
                      * executed_amount - The amount of the order that has been filled.
                      * remaining_amount - The amount of the order that has not been filled.
                      * original_amount - The originally submitted amount of the order.
                      * is_hidden - Will always return false unless the order was placed with the indication-of-interest execution option.
    """
    if side == "buy":
        far_limit_price = float(get_price(ticker, side)) * 10
    else:
        far_limit_price = float(get_price(ticker, side)) / 10
    price = str(round(far_limit_price, 2))
    return order(ticker, quantity, side, price, None, None, ["immediate-or-cancel"], jsonify=jsonify)


@login_required
@format_inputs
def order(ticker, quantity, side, price=None, stop_limit_price=None, min_amount=None, options=None, jsonify=None):
    """ A generic order that can be used for any cryptocurrency.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param quantity: The amount to trade.
    :type quantity: str
    :param side: Either "buy" or "sell".
    :type side: str
    :param price: Set this value to set a limit price.
    :type price: Optional[str]
    :param stop_limit_price: Set this value to set a stop price.
    :type stop_limit_price: Optional[str]
    :param min_amount: Minimum decimal amount to purchase, for block trades only.
    :type min_amount: Optional[str]
    :param options: An optional array containing at most one supported order execution option.
    :type options: Optional[str]
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * order_id - The order id
                      * client_order_id - An optional client-specified order id
                      * symbol - The symbol of the order
                      * exchange - Will always be "gemini"
                      * price - The price the order was issued at
                      * avg_execution_price - The average price at which this order as been executed so far. 0 if the order has not been executed at all.
                      * side - Either "buy" or "sell".
                      * type - Description of the order.
                      * options - An array containing at most one supported order execution option.
                      * timestamp - The timestamp the order was submitted. Note that for compatibility reasons, this is returned as a string. We recommend using the timestampms field instead.
                      * timestampms - The timestamp the order was submitted in milliseconds.
                      * is_live - true if the order is active on the book (has remaining quantity and has not been canceled)
                      * is_cancelled - true if the order has been canceled. Note the spelling, "cancelled" instead of "canceled". This is for compatibility reasons.
                      * reason - Populated with the reason your order was canceled, if available.
                      * was_forced - Will always be false.
                      * executed_amount - The amount of the order that has been filled.
                      * remaining_amount - The amount of the order that has not been filled.
                      * original_amount - The originally submitted amount of the order.
                      * is_hidden - Will always return false unless the order was placed with the indication-of-interest execution option.
    """
    url = URLS.order_new()
    payload = {
        "client_order_id": generate_order_id(),
        "request": URLS.get_endpoint(url),
        "symbol": ticker,
        "amount": str(quantity),
        "side": side
    }
    #
    if price:
        payload["price"] = price
    else:
        payload["price"] = get_price(ticker, side)
    #
    if stop_limit_price:
        payload["type"] = "exchange stop limit"
        payload["stop_price"] = stop_limit_price
    else:
        payload["type"] = "exchange limit"
    #
    if min_amount:
        payload["min_amount"] = min_amount
    #
    if options:
        payload["options"] = options

    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err
