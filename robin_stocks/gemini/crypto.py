from robin_stocks.gemini.helper import format_inputs, request_get
from robin_stocks.gemini.urls import URLS


@format_inputs
def get_pubticker(ticker, jsonify=None):
    """ gets the pubticker information for a crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a requests reponse object or a dictionary parsed using the JSON format. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * bid - The highest bid currently available
                      * ask - The lowest ask currently available
                      * last - The price of the last executed trade
                      * volume - Information about the 24 hour volume on the exchange

    """
    url = URLS.pubticker(ticker)
    data, error = request_get(url, None, jsonify)
    return data, error


@format_inputs
def get_ticker(ticker, jsonify=None):
    """ gets the recent trading information for a crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a requests reponse object or a dictionary parsed using the JSON format. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * symbol - BTCUSD etc.
                      * open - Open price from 24 hours ago
                      * high - High price from 24 hours ago
                      * low - Low price from 24 hours ago
                      * close - Close price (most recent trade)
                      * changes - Hourly prices descending for past 24 hours
                      * bid - Current best bid
                      * ask - Current best offer
                      

    """
    url = URLS.ticker(ticker)
    data, error = request_get(url, None, jsonify)
    return data, error


@format_inputs
def get_symbols(jsonify=None):
    """ gets a list of all available crypto tickers.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a requests reponse object or a list of strings of crypto tickers.

    """
    url = URLS.symbols()
    data, error = request_get(url, None, jsonify)
    return data, error

@format_inputs
def get_symbol_details(ticker, jsonify=None):
    """ gets detailed information for a crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a requests reponse object or a dictionary parsed using the JSON format. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * symbol - BTCUSD etc.
                      * base_currency - CCY1 or the top currency. (ie BTC in BTCUSD)
                      * quote_currency - CCY2 or the quote currency. (ie USD in BTCUSD)
                      * tick_size - The number of decimal places in the quote_currency
                      * quote_increment - The number of decimal places in the base_currency
                      * min_order_size - The minimum order size in base_currency units.
                      * status - Status of the current order book. Can be open, closed, cancel_only, post_only, limit_only.
                      

    """
    url = URLS.symbol_details(ticker)
    data, error = request_get(url, None, jsonify)
    return data, error


def get_price(ticker, side):
    """ returns either the bid or the ask price as a string

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param side: Either 'buy' or 'sell'.
    :type side: str
    :returns: Returns the bid or ask price as a string.

    """
    data, _ = get_pubticker(ticker, jsonify=True)
    if side == "buy":
        return data["ask"]
    else:
        return data["bid"]
