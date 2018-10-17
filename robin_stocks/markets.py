import robin_stocks.helper as helper
import robin_stocks.urls as urls

def get_top_movers(direction,info=None):
    """Returns a list of the top movers up or down for the day.

    :param direction: The direction of movement either 'up' or 'down'
    :type direction: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each mover. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    try:
        direction = direction.lower().strip()
    except AttributeError as message:
        print(message)
        return None

    if (direction != 'up' and direction != 'down'):
        print('Error: direction must be "up" or "down"')
        return([None])

    url = urls.movers()
    payload = { 'direction' : direction}
    data = helper.request_get(url,'pagination',payload)

    return(helper.filter(data,info))

def get_markets(info=None):
    """Returns a list of available markets.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each market. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.markets()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_currency_pairs(info=None):
    """Returns currency pairs

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each currency pair. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """

    url = urls.currency()
    data = helper.request_get(url,'results')
    return(helper.filter(data,info))
