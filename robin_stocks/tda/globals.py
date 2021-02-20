"""Holds the session header and other global variables."""
from requests import Session

DATA_DIR_NAME = ".tokens"
PICKLE_NAME = "tda.pickle"
RETURN_PARSED_JSON_RESPONSE = False # Flag on whether to automatically parse request responses.
LOGGED_IN = False  # Flag on whether or not the user is logged in.

# The session object for making get and post requests.
SESSION = Session()
SESSION.headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip",
    "Accept-Language": "en-US",
    "Host": "api.tdameritrade.com",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "User-Agent": "*",
    "sec-ch-ua-mobile":"?0",
    "Sec-Fetch-Dest":"empty",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"same-site"
}
