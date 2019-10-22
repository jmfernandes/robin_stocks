"""Contains decorator functions and functions for interacting with global data.

Functions
---------
    - request_document
    - request_get
    - request_post
    - update_session
"""
from functools import wraps

import requests

from robin_stocks.globals import SESSION


def set_login_state(logged_in):
    """Sets the login state"""
    global LOGGED_IN
    LOGGED_IN = logged_in


def login_required(func):
    """A decorator for indicating which methods require the user to be logged
       in."""

    @wraps(func)
    def login_wrapper(*args, **kwargs):
        global LOGGED_IN
        if not LOGGED_IN:
            raise Exception('{} can only be called when logged in'.format(
                func.__name__))
        return func(*args, **kwargs)

    return login_wrapper


def convert_none_to_string(func):
    """A decorator for converting a None Type into a blank string"""

    @wraps(func)
    def string_wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            return result
        else:
            return ""

    return string_wrapper


def id_for_stock(symbol):
    """Takes a stock ticker and returns the instrument id associated with the stock.

    :param symbol: The symbol to get the id for.
    :type symbol: str
    :returns:  A string that represents the stocks instrument id.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = 'https://api.robinhood.com/instruments/'
    payload = {'symbol': symbol}
    data = request_get(url, 'indexzero', payload)

    return data_filter(data, 'id')


def id_for_chain(symbol):
    """Takes a stock ticker and returns the chain id associated with a stocks option.

    :param symbol: The symbol to get the id for.
    :type symbol: str
    :returns:  A string that represents the stocks options chain id.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = 'https://api.robinhood.com/instruments/'

    payload = {'symbol': symbol}
    data = request_get(url, 'indexzero', payload)

    return data.get('tradable_chain_id')


def id_for_group(symbol):
    """Takes a stock ticker and returns the id associated with the group.

    :param symbol: The symbol to get the id for.
    :type symbol: str
    :returns:  A string that represents the stocks group id.

    """
    try:
        symbol = symbol.upper().strip()
    except AttributeError as message:
        print(message)
        return None

    url = 'https://api.robinhood.com/options/chains/' + id_for_chain(symbol) + '/'
    data = request_get(url)
    return data.get('underlying_instruments')[0]['id']


def id_for_option(symbol, expiration_date, strike, option_type='both'):
    """Returns the id associated with a specific option order.

    :param symbol: The symbol to get the id for.
    :type symbol: str
    :param expiration_date: The expiration date as YYYY-MM-DD
    :type expiration_date: str
    :param strike: The strike price.
    :type strike: str
    :param option_type: Either call or put.
    :type option_type: str
    :returns:  A string that represents the stocks option id.

    """
    symbol = symbol.upper()
    payload = {'chain_id': id_for_chain(symbol),
               'state': 'active',
               'tradability': 'tradable',
               'type': option_type}
    url = 'https://api.robinhood.com/options/instruments/'
    data = request_get(url, 'pagination', payload)

    list_of_options = [item for item in data if
                       item["expiration_date"] == expiration_date and float(item["strike_price"]) == float(strike)]
    if len(list_of_options) == 0:
        print(
            'Getting the option ID failed. Perhaps the expiration date is wrong format, or the strike price is wrong.')
        return None

    return list_of_options[0]['id']


def round_price(price):
    """Takes a price and rounds it to an appropriate decimal place that Robinhood will accept.

    :param price: The input price to round.
    :type price: float or int
    :returns: The rounded price as a float.

    """
    price = float(price)
    if price <= 1e-2:
        return_price = round(price, 6)
    elif price <= 0:
        return_price = round(price, 4)
    else:
        return_price = round(price, 2)

    return return_price


def data_filter(data, info):
    """Takes the data and extracts the value for the keyword that matches info.

    :param data: The data returned by request_get.
    :type data: dict or list
    :param info: The keyword to data_filter from the data.
    :type info: str
    :returns:  A list or string with the values that correspond to the info keyword.

    """
    compare_dict = None
    none_type = None
    if data is None:
        return data
    elif data == [None]:
        return []
    elif isinstance(data, list):
        if len(data) == 0:
            return []
        compare_dict = data[0]
        none_type = []
    elif isinstance(data, dict):
        compare_dict = data
        none_type = None

    if info is not None:
        if info in compare_dict and isinstance(data, list):
            return [x[info] for x in data]
        elif info in compare_dict and isinstance(data, dict):
            return data[info]
        else:
            print(error_argument_not_key_in_dictionary(info))
            return none_type
    else:
        return data


def inputs_to_set(input_symbols):
    """Takes in the parameters passed to *args and puts them in a set and a list.
    The set will make sure there are no duplicates, and then the list will keep
    the original order of the input.

    :param input_symbols: A list, dict, or tuple of stock tickers.
    :type input_symbols: list or dict or tuple or str
    :returns:  A list of strings that have been capitalized and stripped of white space.

    """

    symbols_list = []
    symbols_set = set()

    def add_symbol(symbol):
        symbol = symbol.upper().strip()
        if symbol not in symbols_set:
            symbols_set.add(symbol)
            symbols_list.append(symbol)

    if isinstance(input_symbols, str):
        add_symbol(input_symbols)
    elif isinstance(input_symbols, list) or isinstance(input_symbols, tuple) or isinstance(input_symbols, set):
        input_symbols = [comp for comp in input_symbols if isinstance(comp, str)]
        for item in input_symbols:
            add_symbol(item)

    return symbols_list


def request_document(url, payload=None):
    """Using a document url, makes a get request and returnes the session data.

    :param url: The url to send a get request to.
    :type url: str
    :param payload:
    :type payload: optional[dict]
    :returns: Returns the session.get() data as opppose to session.get().json() data.

    """
    try:
        res = SESSION.get(url, params=payload)
        res.raise_for_status()
    except requests.exceptions.HTTPError as message:
        print(message)
        return None

    return res


def request_get(url, data_type='regular', payload=None, jsonify_data=True):
    """For a given url and payload, makes a get request and returns the data.

    :param url: The url to send a get request to.
    :type url: str
    :param data_type: Determines how to data_filter the data. 'regular' returns the unfiltered data. \
    'results' will return data['results']. 'pagination' will return data['results'] and append it with any \
    data that is in data['next']. 'indexzero' will return data['results'][0].
    :type data_type: Optional[str]
    :param payload: Dictionary of parameters to pass to the url. Will append the requests url as url/?key1=value1&key2=value2.
    :type payload: Optional[dict]
    :param jsonify_data: If this is true, will return requests.post().json(), otherwise will return response from requests.post().
    :type jsonify_data: bool
    :returns: Returns the data from the get request. If jsonify_data=True and requests returns an http code other than <200> \
    then either '[None]' or 'None' will be returned based on what the data_type parameter was set as.

    """
    if data_type == 'results' or data_type == 'pagination':
        data = [None]
    else:
        data = None
    if jsonify_data:
        try:
            res = SESSION.get(url, params=payload)
            res.raise_for_status()
            data = res.json()
        except (requests.exceptions.HTTPError, AttributeError) as message:
            print(message)
            return data
    else:
        res = SESSION.get(url, params=payload)
        return res
    # Only continue to data_filter data if jsonify_data=True, and Session.get returned status code <200>.
    if data_type == 'results':
        try:
            data = data['results']
        except KeyError as message:
            print("{0} is not a key in the dictionary".format(message))
            return [None]
    elif data_type == 'pagination':
        counter = 2
        next_data = data
        try:
            data = data['results']
        except KeyError as message:
            print("{0} is not a key in the dictionary".format(message))
            return [None]

        if next_data['next']:
            print('Found Additional pages.')
        while next_data['next']:
            try:
                res = SESSION.get(next_data['next'])
                res.raise_for_status()
                next_data = res.json()
            except Exception as e:
                print('Additional pages exist but could not be loaded.'.format(e))
                return data
            print('Loading page ' + str(counter) + ' ...')
            counter += 1
            for item in next_data['results']:
                data.append(item)
    elif data_type == 'indexzero':
        try:
            data = data['results'][0]
        except KeyError as message:
            print("{0} is not a key in the dictionary".format(message))
            return None
        except IndexError as message:
            print("{0} is not found in iterable".format(message))
            return None

    return data


def request_post(url, payload=None, timeout=16, json=False, jsonify_data=True):
    """For a given url and payload, makes a post request and returns the response. Allows for responses other than 200.

    :param url: The url to send a post request to.
    :type url: str
    :param payload: Dictionary of parameters to pass to the url as url/?key1=value1&key2=value2.
    :type payload: Optional[dict]
    :param timeout: The time for the post to wait for a response. Should be slightly greater than multiples of 3.
    :type timeout: Optional[int]
    :param json: This will set the 'content-type' parameter of the session header to 'application/json'
    :type json: bool
    :param jsonify_data: If this is true, will return requests.post().json(), otherwise will return response from requests.post().
    :type jsonify_data: bool
    :returns: Returns the data from the post request.

    """
    data = None
    res = None
    try:
        if json:
            update_session('Content-Type', 'application/json')
            res = SESSION.post(url, json=payload, timeout=timeout)
            update_session('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
        else:
            res = SESSION.post(url, data=payload, timeout=timeout)
        data = res.json()
    except Exception as message:
        print("Error in request_post: {0}".format(message))
    # Either return response <200,401,etc.> or the data that is returned from requests.
    if jsonify_data:
        return data
    else:
        return res


def request_delete(url):
    """For a given url and payload, makes a delete request and returns the response.

    :param url: The url to send a delete request to.
    :type url: str
    :returns: Returns the data from the delete request.

    """
    data = None
    try:
        res = SESSION.delete(url)
        res.raise_for_status()
    except Exception as message:
        print("Error in request_delete: {0}".format(message))

    return data


def update_session(key, value):
    """Updates the session header used by the requests library.

    :param key: The key value to update or add to session header.
    :type key: str
    :param value: The value that corresponds to the key.
    :type value: str
    :returns: None. Updates the session header with a value.

    """
    SESSION.headers[key] = value


def error_argument_not_key_in_dictionary(keyword):
    return 'Error: The keyword "{0}" is not a key in the dictionary.'.format(keyword)


def error_ticker_does_not_exist(ticker):
    return 'Warning: "{0}" is not a valid stock ticker. It is being ignored'.format(ticker)


def error_must_be_nonzero(keyword):
    return 'Error: The input parameter "{0}" must be an integer larger than zero and non-negative'.format(keyword)
