from robin_stocks.tda.helper import (format_inputs, login_required,
                                     request_delete, request_headers)
from robin_stocks.tda.urls import URLS


@login_required
@format_inputs
def place_order(account_id, order_payload, jsonify=None):
    """ Place an order for a given account.

    :param account_id: The account id.
    :type account_id: str
    :param order_payload: A dictionary of key value pairs for the infromation you want to send to order.
    :type order_payload: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.place_order(account_id)
    data, error = request_headers(url, order_payload, jsonify)
    return data, error


@login_required
@format_inputs
def cancel_order(account_id, order_id, jsonify=None):
    """ Cancel an order for a given accoun.

    :param account_id: The account id.
    :type account_id: str
    :param order_id: The order id.
    :type order_id: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.cancel_order(account_id, order_id)
    data, error = request_delete(url, jsonify)
    return data, error
