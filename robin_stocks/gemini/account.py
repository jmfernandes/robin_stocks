from robin_stocks.gemini.authentication import generate_signature
from robin_stocks.gemini.helper import (format_inputs, login_required,
                                        request_post)
from robin_stocks.gemini.urls import URLS

@login_required
@format_inputs
def check_available_balances(jsonify=None):
    """ Gets a list of all available balances in every currency.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a requests reponse object or a list of dictionaries parsed using the JSON format. \
        The keys for the dictionaries are listed below.
    :Dictionary Keys: * currency - The currency code.
                      * amount - The current balance
                      * available - The amount that is available to trade
                      * availableForWithdrawal - The amount that is available to withdraw
                      * type - "exchange"

    """
    url = URLS.available_balances()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def check_notional_balances(jsonify=None):
    """ Gets a list of all available balances in every currency.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a requests reponse object or a list of dictionaries parsed using the JSON format. \
        The keys for the dictionaries are listed below.
    :Dictionary Keys: * currency - The currency code.
                      * amount - The current balance
                      * amountNotional - Amount, in notional
                      * available - The amount that is available to trade
                      * availableNotional - Available, in notional
                      * availableForWithdrawal - The amount that is available to withdraw
                      * availableForWithdrawalNotional - AvailableForWithdrawal, in notional

    """
    url = URLS.notional_balances()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err
