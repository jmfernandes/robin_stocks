from robin_stocks.gemini.helper import request_get, format_inputs
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
    :Dictionary Keys: * bid
                      * ask
                      * volume
                      * last

    """
    url = URLS.pubticker(ticker)
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
