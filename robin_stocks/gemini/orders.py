from robin_stocks.gemini.authentication import generate_signature
from robin_stocks.gemini.helper import request_post, format_inputs, login_required
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
    payload = {"request": "/v1/mytrades", "symbol": ticker}
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err
