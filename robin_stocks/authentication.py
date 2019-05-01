import robin_stocks.urls as urls
import robin_stocks.helper as helper
import random

def GenerateDeviceToken():
    """This function will generate a token used when loggin on.

    :returns: A string representing the token.
    
    """
    rands = []
    for i in range(0,16):
        r = random.random()
        rand = 4294967296.0 * r
        rands.append((int(rand) >> ((3 & i) << 3)) & 255)

    hexa = []
    for i in range(0,256):
        hexa.append(str(hex(i+256)).lstrip("0x").rstrip("L")[1:])

    id = ""
    for i in range(0,16):
        id += hexa[rands[i]]

        if (i == 3) or (i == 5) or (i == 7) or (i == 9):
            id += "-"

    return(id)

def login(username,password,expiresIn=86400,scope='internal'):
    """This function will effectivly log the user into robinhood by getting an
    authentication token and saving it to the session header.

    :param username: The username for your robinhood account. Usually your email.
    :type username: str
    :param password: The password for your robinhood account.
    :type password: str
    :param expiresIn: The time until your login session expires. This is in seconds.
    :type expiresIn: Optional[int]
    :param scope: Specifies the scope of the authentication.
    :type scope: Optional[str]
    :returns:  A dictionary with log in information.

    """
    if not username or not password:
        raise Exception('login must be called with a non-empty username and '
            'password')

    url = urls.login_url()
    payload = {
    'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
    'expires_in': expiresIn,
    'grant_type': 'password',
    'password': password,
    'scope': scope,
    'username': username,
    'challenge_type': 'sms',
    'device_token': GenerateDeviceToken()
    }
    data = helper.request_post(url,payload)
    token = 'Bearer {}'.format(data['access_token'])
    helper.update_session('Authorization',token)
    helper.set_login_state(True)
    return(data)

@helper.login_required
def logout():
    """Removes authorization from the session header.

    :returns: None

    """
    helper.set_login_state(False)
    helper.update_session('Authorization',None)
