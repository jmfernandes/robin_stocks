from functools import wraps
from inspect import signature
from json import dumps
from re import IGNORECASE, split

import requests
from robin_stocks.tda.globals import (LOGGED_IN, RETURN_PARSED_JSON_RESPONSE,
                                      SESSION)


def get_order_number(data):
    """ Gets the 
    """
    try:
        if type(data) is requests.models.Response:
            parse_string = data.headers["Location"]
        elif type(data) is dict or type(data) is requests.structures.CaseInsensitiveDict:
            parse_string = data["Location"]
        else:
            parse_string = data
    except Exception as e:
        raise ValueError("{0} is not a value in the dictionary".format(e))

    _, order_id = split("orders/", parse_string, IGNORECASE)
    return(order_id)


def format_inputs(func):
    """ A decorator for formatting inputs. For any function decorated by this,
        the value of jsonify=None will be replaced with the global value stored at 
        RETURN_PARSED_JSON_RESPONSE.
    """
    @wraps(func)
    def format_wrapper(*args, **kwargs):
        bound_args = signature(func).bind(*args, **kwargs)
        bound_args.apply_defaults()
        target_args = dict(bound_args.arguments)
        if target_args['jsonify'] is None:
            kwargs["jsonify"] = get_default_json_flag()
        return(func(*args, **kwargs))
    return(format_wrapper)


def set_default_json_flag(parse_json):
    """ Sets whether you want all functions to return the json parsed response or not.

    :param parse_json: Set to change value of global variable.
    :type parse_json: bool
    """
    global RETURN_PARSED_JSON_RESPONSE
    RETURN_PARSED_JSON_RESPONSE = parse_json


def get_default_json_flag():
    """ Gets the boolean flag on the default JSON setting.
    """
    return RETURN_PARSED_JSON_RESPONSE


def update_session(key, value):
    """Updates the session header used by the requests library.

    :param key: The key value to update or add to session header.
    :type key: str
    :param value: The value that corresponds to the key.
    :type value: str

    """
    SESSION.headers[key] = value


def set_login_state(logged_in):
    """ Sets the login state

    :param logged_in: Set to change value of global variable.
    :type logged_in: bool
    """
    global LOGGED_IN
    LOGGED_IN = logged_in


def get_login_state():
    """ Gets the login state
    """
    return LOGGED_IN


def login_required(func):
    """ A decorator for indicating which methods require the user to be logged in.
    """
    @wraps(func)
    def login_wrapper(*args, **kwargs):
        global LOGGED_IN
        if not LOGGED_IN:
            raise Exception('{} can only be called when logged in'.format(
                func.__name__))
        return(func(*args, **kwargs))
    return(login_wrapper)


def request_get(url, payload, parse_json):
    """ Generic function for sending a get request.

    :param url: The url to send a get request to.
    :type url: str
    :param payload: Dictionary of parameters to pass to the url. Will append the requests url as url/?key1=value1&key2=value2.
    :type payload: dict
    :param parse_json: Requests serializes data in the JSON format. Set this parameter true to parse the data to a dictionary \
        using the JSON format.
    :type parse_json: bool
    :returns: Returns a tuple where the first entry is the response and the second entry will be an error message from the \
        get request. If there was no error then the second entry in the tuple will be None. The first entry will either be \
        the raw request response or the parsed JSON response based on whether parse_json is True or not.
    """
    response_error = None
    try:
        response = SESSION.get(url, params=payload)
        response.raise_for_status()
    except Exception as e:
        response_error = e
    # Return either the raw request object so you can call response.text, response.status_code, response.headers, or response.json()
    # or return the JSON parsed information if you don't care to check the status codes.
    if parse_json:
        return response.json(), response_error
    else:
        return response, response_error


def request_post(url, payload, parse_json):
    """ Generic function for sending a post request.

    :param url: The url to send a post request to.
    :type url: str
    :param payload: Dictionary of parameters to pass to the url. Will append the requests url as url/?key1=value1&key2=value2.
    :type payload: dict
    :param parse_json: Requests serializes data in the JSON format. Set this parameter true to parse the data to a dictionary \
        using the JSON format.
    :type parse_json: bool
    :returns: Returns a tuple where the first entry is the response and the second entry will be an error message from the \
        get request. If there was no error then the second entry in the tuple will be None. The first entry will either be \
        the raw request response or the parsed JSON response based on whether parse_json is True or not.
    """
    response_error = None
    try:
        response = SESSION.post(url, params=payload)
        response.raise_for_status()
    except Exception as e:
        response_error = e
    # Return either the raw request object so you can call response.text, response.status_code, response.headers, or response.json()
    # or return the JSON parsed information if you don't care to check the status codes.
    if parse_json:
        return response.json(), response_error
    else:
        return response, response_error


def request_data(url, payload, parse_json):
    """ Generic function for sending a post request. Does not use any Session information. Encodes the data as x-www-form-urlencoded form data.

    :param url: The url to send a post request to.
    :type url: str
    :param payload: Dictionary of parameters to pass to the url. Will append the requests url as data in the session headers.
    :type payload: dict
    :param parse_json: Requests serializes data in the JSON format. Set this parameter true to parse the data to a dictionary \
        using the JSON format.
    :type parse_json: bool
    :returns: Returns a tuple where the first entry is the response and the second entry will be an error message from the \
        get request. If there was no error then the second entry in the tuple will be None. The first entry will either be \
        the raw request response or the parsed JSON response based on whether parse_json is True or not.
    """
    response_error = None
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        response_error = e
    # Return either the raw request object so you can call response.text, response.status_code, response.headers, or response.json()
    # or return the JSON parsed information if you don't care to check the status codes.
    if parse_json:
        return response.json(), response_error
    else:
        return response, response_error


def request_headers(url, payload, parse_json):
    """ Generic function for sending a post request. Encodes the data as x-www-form-urlencoded form data and appends to Session data.

    :param url: The url to send a post request to.
    :type url: str
    :param payload: Dictionary of parameters to pass to the url. Will append the requests url as data in the session headers.
    :type payload: dict
    :param parse_json: Requests serializes data in the JSON format. Set this parameter true to parse the data to a dictionary \
        using the JSON format.
    :type parse_json: bool
    :returns: Returns a tuple where the first entry is the response and the second entry will be an error message from the \
        get request. If there was no error then the second entry in the tuple will be None. The first entry will either be \
        the raw request response or the parsed JSON response based on whether parse_json is True or not.
    """
    response_error = None
    try:
        response = SESSION.post(url, data=dumps(payload))
        response.raise_for_status()
    except Exception as e:
        response_error = e
    # Return either the raw request object so you can call response.text, response.status_code, response.headers, or response.json()
    # or return the JSON parsed information if you don't care to check the status codes.
    if parse_json:
        return response.headers, response_error
    else:
        return response, response_error


def request_delete(url, parse_json):
    """ Generic function for sending a delete request.

    :param url: The url to send a post request to.
    :type url: str
    :param parse_json: Requests serializes data in the JSON format. Set this parameter true to parse the data to a dictionary \
        using the JSON format.
    :type parse_json: bool
    :returns: Returns a tuple where the first entry is the response and the second entry will be an error message from the \
        get request. If there was no error then the second entry in the tuple will be None. The first entry will either be \
        the raw request response or the parsed JSON response based on whether parse_json is True or not.
    """
    response_error = None
    try:
        response = SESSION.delete(url)
        response.raise_for_status()
    except Exception as e:
        response_error = e
    # Return either the raw request object so you can call response.text, response.status_code, response.headers, or response.json()
    # or return the JSON parsed information if you don't care to check the status codes.
    if parse_json:
        return response.headers, response_error
    else:
        return response, response_error
