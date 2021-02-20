from robin_stocks.gemini.authentication import generate_signature
from robin_stocks.gemini.helper import (format_inputs, login_required,
                                        request_get, request_post)
from robin_stocks.gemini.urls import URLS


@format_inputs
def get_pubticker(ticker, jsonify=None):
    """ Gets the pubticker information for a crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
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
    """ Gets the recent trading information for a crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
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
    """ Gets a list of all available crypto tickers.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a list of strings and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.symbols()
    data, error = request_get(url, None, jsonify)
    return data, error


@format_inputs
def get_symbol_details(ticker, jsonify=None):
    """ Gets detailed information for a crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
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


@login_required
@format_inputs
def get_notional_volume(jsonify=None):
    """ Gets information about notional volume

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.               
    :Dictionary Keys: * date - UTC date in yyyy-MM-dd format
                      * last_updated_ms - Unix timestamp in millisecond of the last update
                      * web_maker_fee_bps - Integer value representing the maker fee for all symbols in basis point for web orders
                      * web_taker_fee_bps - Integer value representing the taker fee for all symbols in basis point for web orders
                      * web_auction_fee_bps - Integer value representing the auction fee for all symbols in basis point for web orders
                      * api_maker_fee_bps - Integer value representing the maker fee for all symbols in basis point for API orders
                      * api_taker_fee_bps - Integer value representing the taker fee for all symbols in basis point for API orders
                      * api_auction_fee_bps - Integer value representing the auction fee for all symbols in basis point for API orders
                      * fix_maker_fee_bps - Integer value representing the maker fee for all symbols in basis point for FIX orders
                      * fix_taker_fee_bps - Integer value representing the taker fee for all symbols in basis point for FIX orders
                      * fix_auction_fee_bps - Integer value representing the auction fee for all symbols in basis point for FIX orders
                      * block_maker_fee_bps - Integer value representing the maker fee for all symbols in basis point for block orders
                      * block_taker_fee_bps - Integer value representing the taker fee for all symbols in basis point for block orders
                      * notional_30d_volume - Maker plus taker trading volume for the past 30 days, including auction volume
                      * notional_1d_volume - A list of 1 day notional volume for the past 30 days
    """
    url = URLS.notional_volume()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def get_trade_volume(jsonify=None):
    """ Gets information about trade volume. The response will be an array of up to 30 days of trade volume for each symbol.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.               
    :Dictionary Keys: * symbol - The symbol.
                      * base_currency - quantity is denominated in this currency.
                      * notional_currency - price is denominated as the amount of notional currency per one unit of base currency. Notional values are denominated in this currency.
                      * data_date - UTC date in yyyy-MM-dd format.
                      * total_volume_base - Total trade volume for this day.
                      * maker_buy_sell_ratio - Maker buy/sell ratio is the proportion of maker base volume on trades where the account was on the buy side versus all maker trades. If there is no maker base volume on the buy side, then this value is 0.
                      * buy_maker_base - Quantity for this day where the account was a maker on the buy side of the trade.
                      * buy_maker_notional - Notional value for this day where the account was a maker on the buy side of the trade.
                      * buy_maker_count - Number of trades for this day where the account was a maker on the buy side of the trade.
                      * sell_maker_base - Quantity for this day where the account was a maker on the sell side of the trade.
                      * sell_maker_notional - Notional value for this day where the account was a maker on the sell side of the trade.
                      * sell_maker_count - Number of trades for this day where the account was a maker on the sell side of the trade.
                      * buy_taker_base- Quantity for this day where the account was a taker on the buy side of the trade.
                      * buy_taker_notional - Notional value for this day where the account was a taker on the buy side of the trade.
                      * buy_taker_count - Number of trades for this day where the account was a taker on the buy side of the trade.
                      * sell_taker_base - Quantity for this day where the account was a taker on the sell side of the trade.
                      * sell_taker_notional - Notional value for this day where the account was a taker on the sell side of the trade.
                      * sell_taker_count - Number of trades for this day where the account was a taker on the sell side of the trade.
                      
    """
    url = URLS.trade_volume()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


def get_price(ticker, side):
    """ Returns either the bid or the ask price as a string.

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
