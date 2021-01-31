from robin_stocks.gemini.helper import request_get, get_default_json_flag
from robin_stocks.gemini.urls import URLS


def get_pubticker(ticker, jsonify=None):
    """ gets the pubticker information for a crypto.

    :param ticker: The ticker of the crypto.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a requests reponse object or a dictionary parsed using the JSON format. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * bid
                      * ask
                      * volume
                      * last

    """
    if not jsonify:
        jsonify = get_default_json_flag()
    url = URLS.pubticker(ticker)
    data, error = request_get(url, None, jsonify)
    return data, error
