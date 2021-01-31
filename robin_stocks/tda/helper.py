from robin_stocks.tda.globals import SESSION


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
