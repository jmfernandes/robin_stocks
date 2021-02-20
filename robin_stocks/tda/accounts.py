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


@login_required
@format_inputs
def get_transactions(id, type_value=None, symbol=None, start_date=None, end_date=None, jsonify=None):
    """ Get account information for a specific account.

    :param id: The account id.
    :type id: str
    :param type_value: Only transactions with the specified type will be returned. ALL, TRADE, \
        BUY_ONLY, SELL_ONLY, CASH_IN_OR_CASH_OUT, CHECKING, DIVIDEND, INTEREST, OTHER, ADVISOR_FEES
    :type type_value: Optional[str]
    param symbol: Only transactions with the specified symbol will be returned.
    :type symbol: Optional[str]
    param start_date: Only transactions after the Start Date will be returned. \
        Note: The maximum date range is one year. Valid ISO-8601 formats are :yyyy-MM-dd.
    :type start_date: Optional[str]
    param end_date: Only transactions before the End Date will be returned. \
        Note: The maximum date range is one year. Valid ISO-8601 formats are :yyyy-MM-dd.
    :type end_date: Optional[str]
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.
    """
    url = URLS.transactions(id)
    payload = {}
    if type_value:
        payload["type"] = type_value
    if symbol:
        payload["symbol"] = symbol
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date
    data, error = request_get(url, payload, jsonify)
    return data, error


@login_required
@format_inputs
def get_transaction(account_id, transaction_id, jsonify=None):
    """ Get account information for a specific account.

    :param account_id: The account id.
    :type account_id: str
    :param transaction_id: The transaction id.
    :type transaction_id: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.
    """
    url = URLS.transaction(account_id, transaction_id)
    data, error = request_get(url, None, jsonify)
    return data, error
