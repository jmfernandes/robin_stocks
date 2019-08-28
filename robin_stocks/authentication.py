import robin_stocks.urls as urls
import robin_stocks.helper as helper
import random

TEMP_DEVICE_TOKEN = None
LOGIN_DATA = None

def generate_device_token():
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

def base_login(username,password,device_token,expiresIn=86400,scope='internal',by_sms=True):
    """This function will try to log the user in and will return the response data.
    It may contain a challenge (sms) or the access token.

    :param username: The username for your robinhood account. Usually your email.
    :type username: str
    :param password: The password for your robinhood account.
    :type password: str
    :param device_token: The device_token you should re-use (can be saved with "robin_stocks.get_new_device_token()").
    :type device_token: str
    :param expiresIn: The time until your login session expires. This is in seconds.
    :type expiresIn: Optional[int]
    :param scope: Specifies the scope of the authentication.
    :type scope: Optional[str]
    :param by_sms: Specifies whether to send an email(False) or an sms(True)
    :type by_sms: Optional[boolean]
    :returns:  A dictionary with response information.


    """
    if not username or not password:
        raise Exception('login must be called with a non-empty username and '
            'password')

    if by_sms:
        challenge_type = "sms"
    else:
        challenge_type = "email"

    url = urls.login_url()
    payload = {
    'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
    'expires_in': expiresIn,
    'grant_type': 'password',
    'password': password,
    'scope': scope,
    'username': username,
    'challenge_type': challenge_type,
    'device_token': device_token
    }
    data = helper.request_post(url,payload)
    return(data)

def respond_to_challenge(challenge_id, sms_code):
    """This functino will post to the challenge url.

    :param challenge_id: The challenge id.
    :type challenge_id: str
    :param sms_code: The sms code.
    :type sms_code: str
    :returns:  The response from requests.

    """
    url = urls.challenge_url(challenge_id)
    payload = {
        'response': sms_code
    }
    return(helper.request_post(url,payload=payload))

def get_new_device_token(username, password,by_sms=True):
    """This function will create and activate a new device token for the user, which should be stored
    and used for future login attempts.

    :param username: The username for your robinhood account. Usually your email.
    :type username: str
    :param password: The password for your robinhood account.
    :type password: str
    :param by_sms: Specifies whether to send an email(False) or an sms(True) for auth.
    :type by_sms: Optional[boolean]
    :returns:  A string which is the device token or None if the token could not be validated with an sms code.

    """
    device_token = generate_device_token()
    initial_login = base_login(username, password, device_token,by_sms=by_sms)
    if 'challenge' not in initial_login:
        global LOGIN_DATA
        LOGIN_DATA = initial_login
        helper.set_device_token(device_token)
        return(device_token)
    challenge_id = initial_login['challenge']['id']
    sms_code = input('Enter sms code for validating device_token: ')
    res = respond_to_challenge(challenge_id, sms_code)
    while 'challenge' in res and res['challenge']['remaining_attempts'] > 0:
        sms_code = input('Incorrect code, try again: ')
        res = respond_to_challenge(challenge_id, sms_code)
    if 'status' in res and res['status'] == 'validated':
        helper.update_session('X-ROBINHOOD-CHALLENGE-RESPONSE-ID', challenge_id)
        helper.set_device_token(device_token)
        return(device_token)
    else:
        raise Exception(res['detail'])

def login(username,password,device_token=TEMP_DEVICE_TOKEN,expiresIn=86400,scope='internal',by_sms=True):
    """This function will effectivly log the user into robinhood by getting an
    authentication token and saving it to the session header.

    :param username: The username for your robinhood account. Usually your email.
    :type username: str
    :param password: The password for your robinhood account.
    :type password: str
    :param device_token: The device_token you should re-use (can be saved with "robin_stocks.get_new_device_token()").
    :type device_token: str
    :param expiresIn: The time until your login session expires. This is in seconds.
    :type expiresIn: Optional[int]
    :param scope: Specifies the scope of the authentication.
    :type scope: Optional[str]
    :param by_sms: Specifies whether to send an email(False) or an sms(True)
    :type by_sms: Optional[boolean]
    :returns:  A dictionary with log in information.

    """
    if not device_token:
        TEMP_DEVICE_TOKEN = get_new_device_token(username, password,by_sms=by_sms)
        device_token = TEMP_DEVICE_TOKEN
    if not LOGIN_DATA:
        data = base_login(username, password, device_token,by_sms=by_sms)
    if LOGIN_DATA:
        token = 'Bearer {}'.format(LOGIN_DATA['access_token'])
        helper.update_session('Authorization',token)
        helper.set_login_state(True)
        data = LOGIN_DATA
    elif 'access_token' in data:
        token = 'Bearer {}'.format(data['access_token'])
        helper.update_session('Authorization',token)
        helper.set_login_state(True)
    else:
        print(data)
    return(data)

@helper.login_required
def logout():
    """Removes authorization from the session header.

    :returns: None

    """
    helper.set_login_state(False)
    helper.update_session('Authorization',None)
