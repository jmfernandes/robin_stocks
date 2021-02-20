from robin_stocks.gemini.authentication import generate_signature
from robin_stocks.gemini.helper import (format_inputs, login_required,
                                        request_post)
from robin_stocks.gemini.urls import URLS


@login_required
@format_inputs
def get_account_detail(jsonify=None):
    """ Gets information about the profile attached to your API key.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * account - Contains information on the requested account
                        -- accountName - The name of the account provided upon creation. Will default to Primary
                        -- shortName - Nickname of the specific account (will take the name given, remove all symbols, replace all " " with "-" and make letters lowercase)
                        -- type - The type of account. Will return either exchange or custody
                        -- created - The timestamp of account creation, displayed as number of milliseconds since 1970-01-01 UTC. This will be transmitted as a JSON number
                      * users - Contains an array of JSON objects with user information for the requested account
                        -- name - Full legal name of the user
                        -- lastSignIn - Timestamp of the last sign for the user. Formatted as yyyy-MM-dd'T'HH:mm:ss.SSS'Z'
                        -- status - Returns user status. Will inform of active users or otherwise not active
                        -- countryCode - 2 Letter country code indicating residence of user.
                        -- isVerified - Returns verification status of user.
                      * memo_reference_code - Returns wire memo reference code for linked bank account.

    """
    url = URLS.account_detail()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def check_available_balances(jsonify=None):
    """ Gets a list of all available balances in every currency.

    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a list of dictionaries parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
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
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a list of dictionaries parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.\
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


@login_required
@format_inputs
def check_transfers(timestamp=None, limit_transfers=10, show_completed_deposit_advances=False, jsonify=None):
    """ Gets a list of all transfers.

    :param timestamp: Only return transfers on or after this timestamp. If not present, will show the most recent transfers.
    :type timestamp: Optional[str]
    :param limit_transfers: The maximum number of transfers to return. Default is 10, max is 50.
    :type limit_transfers: Optional[int]
    :param show_completed_deposit_advances: Whether to display completed deposit advances. False by default. Must be set True to activate.
    :type show_completed_deposit_advances: Optional[int]
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a list of dictionaries parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionaries are listed below.
    :Dictionary Keys: * type - Transfer type. Deposit or Withdrawal.
                      * status - Transfer status. Advanced or Complete.
                      * timestampms - The time that the trade was executed in milliseconds
                      * eid - Transfer event id
                      * advanceEid - Deposit advance event id
                      * currency - Currency code
                      * amount - The transfer amount
                      * method - Optional. When currency is a fiat currency, the method field will attempt to supply ACH, Wire, or SEN. If the transfer is an internal transfer between subaccounts the method field will return Internal.
                      * txHash - Optional. When currency is a cryptocurrency, supplies the transaction hash when available.
                      * outputIdx - Optional. When currency is a cryptocurrency, supplies the output index in the transaction when available.
                      * destination - Optional. When currency is a cryptocurrency, supplies the destination address when available.
                      * purpose - Optional. Administrative field used to supply a reason for certain types of advances.
    """
    url = URLS.transfers()
    payload = {
        "request": URLS.get_endpoint(url),
        "show_completed_deposit_advances": show_completed_deposit_advances
    }
    if timestamp:
        payload["timestamp"] = timestamp
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def get_deposit_addresses(network, timestamp=None,  jsonify=None):
    """ Gets a list of all deposit addresses.

    :param network: network can be bitcoin, ethereum, bitcoincash, litecoin, zcash, filecoin.
    :type network: str
    :param timestamp: Only returns addresses created on or after this timestamp.
    :type timestamp: Optional[str]
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a list of dictionaries parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionaries are listed below.
    :Dictionary Keys: * address - String representation of the new cryptocurrency address.
                      * timestamp - Creation date of the address.
                      * label - Optional. if you provided a label when creating the address, it will be echoed back here.

    """
    url = URLS.deposit_addresses(network)
    payload = {
        "request": URLS.get_endpoint(url)
    }
    if timestamp:
        payload["timestamp"] = timestamp
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def get_approved_addresses(network, jsonify=None):
    """ Allows viewing of Approved Address list.

    :param network: The network of the approved address. Network can be bitcoin, ethereum, bitcoincash, litecoin, zcash, or filecoin
    :type network: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * approvedAddresses - Array of approved addresses on both the account and group level.
                        -- network - The network of the approved address. Network can be bitcoin, ethereum, bitcoincash, litecoin, zcash, or filecoin
                        -- scope - Will return the scope of the address as either "account" or "group"
                        -- label - The label assigned to the address
                        -- status - The status of the address that will return as "active", "pending-time" or "pending-mua". The remaining time is exactly 7 days after the initial request. "pending-mua" is for multi-user accounts and will require another administator or fund manager on the account to approve the address.
                        -- createdAt - UTC timestamp in millisecond of when the address was created.
                        -- address - The address on the approved address list.

    """
    url = URLS.approved_addresses(network)
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err


@login_required
@format_inputs
def withdraw_crypto_funds(currency_code, address, amount, jsonify=None):
    """ Before you can withdraw cryptocurrency funds to an approved address, you need three things:

        1. You must have an approved address list for your account
        2. The address you want to withdraw funds to needs to already be on that approved address list
        3. An API key with the Fund Manager role added

    :param currency_code: the three-letter currency code of a supported crypto-currency, e.g. btc or eth. 
    :type currency_code: str
    :param address: Standard string format of cryptocurrency address.
    :type address: str
    :param amount: 	Quoted decimal amount to withdraw.
    :type amount: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error. \
        The keys for the dictionary are listed below.
    :Dictionary Keys: * address - Standard string format of the withdrawal destination address.
                      * amount - The withdrawal amount.
                      * txHash - Standard string format of the transaction hash of the withdrawal transaction. Only shown for ETH and GUSD withdrawals.
                      * withdrawalID - A unique ID for the withdrawal. Only shown for BTC, ZEC, LTC and BCH withdrawals.
                      * message - A human-readable English string describing the withdrawal. Only shown for BTC, ZEC, LTC and BCH withdrawals.

    """
    url = URLS.withdrawl_crypto(currency_code)
    payload = {
        "request": URLS.get_endpoint(url),
        "address": address,
        "amount": amount
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err
