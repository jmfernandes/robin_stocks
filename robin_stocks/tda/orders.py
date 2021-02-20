from robin_stocks.tda.helper import (format_inputs, login_required,
                                     request_delete, request_get,
                                     request_headers)
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
    url = URLS.orders(account_id)
    data, error = request_headers(url, order_payload, jsonify)
    return data, error


@login_required
@format_inputs
def cancel_order(account_id, order_id, jsonify=None):
    """ Cancel an order for a given account.

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
    url = URLS.order(account_id, order_id)
    data, error = request_delete(url, jsonify)
    return data, error


@login_required
@format_inputs
def get_order(account_id, order_id, jsonify=None):
    """ Gets information for an order for a given account.

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
    url = URLS.order(account_id, order_id)
    data, error = request_get(url, None, jsonify)
    return data, error


@login_required
@format_inputs
def get_orders_for_account(account_id, max_results=None, from_time=None, to_time=None, status=None, jsonify=None):
    """ Gets all the orders for a given account.

    :param account_id: The account id.
    :type account_id: Optional[str]
    :param max_results: The max number of orders to retrieve.
    :type max_results: Optional[str]
    :param from_time: Specifies that no orders entered before this time should be returned. Valid ISO-8601 formats are : \
yyyy-MM-dd. Date must be within 60 days from today's date. 'toEnteredTime' must also be set.
    :type from_time: Optional[str]
    :param to_time: Specifies that no orders entered after this time should be returned.Valid ISO-8601 formats are : \
yyyy-MM-dd. 'fromEnteredTime' must also be set.
    :type to_time: Optional[str]
    :param status: Specifies that only orders of this status should be returned. Possible values are \
        AWAITING_PARENT_ORDER, AWAITING_CONDITION, AWAITING_MANUAL_REVIEW, ACCEPTED, AWAITING_UR_OUT, PENDING_ACTIVATION, QUEUED \
        WORKING, REJECTED, PENDING_CANCEL, CANCELED, PENDING_REPLACE, REPLACED, FILLED, EXPIRED
    :type status: Optional[str]
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.orders(account_id)
    payload = {}
    if max_results:
        payload["maxResults"] = max_results
    if from_time:
        payload["fromEnteredTime"] = from_time
    if to_time:
        payload["toEnteredTime"] = to_time
    if status:
        payload["status"] = status
    data, error = request_get(url, payload, jsonify)
    return data, error
