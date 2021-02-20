from robin_stocks.tda.helper import format_inputs, login_required, request_get
from robin_stocks.tda.urls import URLS


@login_required
@format_inputs
def get_hours_for_markets(markets, date, jsonify=None):
    """ Gets market hours for various markets.

    :param markets: The markets for which you're requesting market hours, comma-separated. \
        Valid markets are EQUITY, OPTION, FUTURE, BOND, or FOREX.
    :type markets: str
    :param date: The date for which market hours information is requested. Valid ISO-8601 formats are : \
        yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.
    :type date: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.markets()
    payload = {
        "markets": markets,
        "date": date
    }
    data, error = request_get(url, payload, jsonify)
    return data, error


@login_required
@format_inputs
def get_hours_for_market(market, date, jsonify=None):
    """ Gets market hours for a specific market.

    :param market: The market for which you're requesting market hours, comma-separated. \
        Valid markets are EQUITY, OPTION, FUTURE, BOND, or FOREX.
    :type market: str
    :param date: The date for which market hours information is requested. Valid ISO-8601 formats are : \
        yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.
    :type date: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.market(market)
    payload = {
        "date": date
    }
    data, error = request_get(url, payload, jsonify)
    return data, error


@login_required
@format_inputs
def get_movers(market, direction, change, jsonify=None):
    """ Gets market hours for a specific market.

    :param market: The market for which you're requesting market hours, comma-separated. \
        Valid markets are $DJI, $COMPX, or $SPX.X.
    :type market: str
    :param direction: To return movers with the specified directions of "up" or "down".
    :type direction: str
    :param change: To return movers with the specified change types of "percent" or "value".
    :type change: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.movers(market)
    payload = {
        "direction": direction,
        "change": change
    }
    data, error = request_get(url, payload, jsonify)
    return data, error
