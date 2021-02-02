
import base64
import datetime
import hashlib
import hmac
import json
import time
from random import random

from robin_stocks.gemini.helper import (get_api_key, get_nonce,
                                        increment_nonce, set_api_key,
                                        set_login_state, update_session)


def login(api_key, secret_key):
    """ Set the authorization token so the API can be used.
    """
    update_session("X-GEMINI-APIKEY", api_key)
    set_api_key(secret_key.encode())
    set_login_state(True)


def generate_signature(payload):
    """ Generate session header information needed to process Private API requests.

    :param payload: Dictionary of parameters to pass to encode.
    :type payload: dict

    """
    gemini_api_secret = get_api_key()
    t = datetime.datetime.now()
    payload["nonce"] = str(int(time.mktime(t.timetuple())*1000) + get_nonce())
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()
    update_session("X-GEMINI-PAYLOAD", b64)
    update_session("X-GEMINI-SIGNATURE", signature)
    increment_nonce()


def generate_order_id():
    """This function will generate a token used when placing orders.

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
