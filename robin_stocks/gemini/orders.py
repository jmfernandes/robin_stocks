from robin_stocks.gemini.authentication import (generate_order_id,
                                                generate_signature)
from robin_stocks.gemini.helper import (format_inputs, login_required,
                                        request_post)
from robin_stocks.gemini.crypto import get_price
from robin_stocks.gemini.urls import URLS


@login_required
@format_inputs
def get_trades_for_crypto(ticker, jsonify=None):
    """ gets a list of all transactions for a certain crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a requests reponse object or a list of dictionaries parsed using the JSON format. \
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

    """
    url = URLS.mytrades()
    payload = {
        "request": "/v1/mytrades",
        "symbol": ticker
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def order_market(ticker, quantity, side, jsonify=None):
    """ Gemini does not directly support market orders. This function will try to immediately
    place an order or it will cancel it.
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
    url = URLS.order_new()
    payload = {
        "client_order_id": generate_order_id(),
        "request": "/v1/order/new",
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
