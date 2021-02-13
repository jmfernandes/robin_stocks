from robin_stocks.tda.helper import format_inputs, login_required, request_get
from robin_stocks.tda.urls import URLS


@login_required
@format_inputs
def get_accounts(options=None, jsonify=None):
    """ Gets all accounts associated with your API keys.

    :param options: Balances displayed by default, additional fields can be added here by adding positions or orders\
        As a comma separated list. Example:"positions,orders"
    :type options: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.
    """
    url = URLS.accounts()
    if options:
        payload = {
            "fields": options
        }
    else:
        payload = None
    data, error = request_get(url, payload, jsonify)
    return data, error


@login_required
@format_inputs
def get_account(id, options=None, jsonify=None):
    """ Get account information for a specific account.

    :param id: The account id.
    :type id: str
    :param options: Balances displayed by default, additional fields can be added here by adding positions or orders\
        As a comma separated list. Example:"positions,orders"
    :type options: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.
    """
    url = URLS.account(id)
    if options:
        payload = {
            "fields": options
        }
    else:
        payload = None
    data, error = request_get(url, payload, jsonify)
    return data, error
