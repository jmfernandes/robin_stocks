
from base64 import b64encode
from datetime import datetime
from hashlib import sha384
from hmac import new
from json import dumps
from random import random
from time import mktime

from robin_stocks.gemini.helper import (format_inputs, get_secret_key, get_nonce,
                                        increment_nonce, login_required,
                                        request_post, set_secret_key,
                                        set_login_state, update_session)
from robin_stocks.gemini.urls import URLS


def login(api_key, secret_key):
    """ Set the authorization token so the API can be used.
    """
    update_session("X-GEMINI-APIKEY", api_key)
    set_secret_key(secret_key.encode())
    set_login_state(True)


def logout():
    """ Removes the API and Secret key from session and global variables.
    """
    update_session("X-GEMINI-APIKEY", "")
    set_secret_key("".encode())
    set_login_state(False)


def generate_signature(payload):
    """ Generate session header information needed to process Private API requests.

    :param payload: Dictionary of parameters to pass to encode.
    :type payload: dict

    """
    gemini_api_secret = get_secret_key()
    t = datetime.now()
    payload["nonce"] = str(int(mktime(t.timetuple())*1000) + get_nonce())
    encoded_payload = dumps(payload).encode()
    b64 = b64encode(encoded_payload)
    signature = new(gemini_api_secret, b64, sha384).hexdigest()
    update_session("X-GEMINI-PAYLOAD", b64)
    update_session("X-GEMINI-SIGNATURE", signature)
    increment_nonce()


def generate_order_id():
    """ This function will generate a token used when placing orders.

    :returns: A string representing the token.

    """
    rands = []
    for i in range(0, 16):
        r = random()
        rand = 4294967296.0 * r
        rands.append((int(rand) >> ((3 & i) << 3)) & 255)

    hexa = []
    for i in range(0, 256):
        hexa.append(str(hex(i+256)).lstrip("0x").rstrip("L")[1:])

    id = ""
    for i in range(0, 16):
        id += hexa[rands[i]]

        if (i == 3) or (i == 5) or (i == 7) or (i == 9):
            id += "-"

    return(id)


@login_required
@format_inputs
def heartbeat(jsonify=None):
    """ Generate a heartbeat response to keep a session alive.

    :returns: {"result": "ok"}

    """
    url = URLS.heartbeat()
    payload = {
        "request": URLS.get_endpoint(url)
    }
    generate_signature(payload)
    data, err = request_post(url, payload, jsonify)
    return data, err
