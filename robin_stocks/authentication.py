import robin_stocks.urls as urls
import robin_stocks.helper as helper

def login(username,password,expiresIn=86400,scope='internal'):
    """This function will effectivly log the user into robinhood by getting an
    authentication token and saving it to the session header.

    :param name: The username.
    :type name: str
    :param password: The password.
    :type state: str
    :returns:  A dictionary with log in information.

    """
    url = urls.login_url()
    payload = {
    'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
    'expires_in': expiresIn,
    'grant_type': 'password',
    'password': password,
    'scope': scope,
    'username': username
    }
    data = helper.request_post(url,payload)
    token = 'Bearer {}'.format(data['access_token'])
    helper.update_session('Authorization',token)
    return(data)

def logout():
    """Removes authorization from the session header.

    :returns: None

    """
    helper.update_session('Authorization',None)
