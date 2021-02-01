
import base64
import datetime
import hashlib
import hmac
import json
import time

from robin_stocks.gemini.helper import (get_api_key, set_api_key,
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
    payload["nonce"] = str(int(time.mktime(t.timetuple())*1000))
    encoded_payload = json.dumps(payload).encode()
    b64 = base64.b64encode(encoded_payload)
    signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()
    update_session("X-GEMINI-PAYLOAD", b64)
    update_session("X-GEMINI-SIGNATURE", signature)
