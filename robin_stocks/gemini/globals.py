"""Holds the session header and other global variables."""
from requests import Session

NONCE = 1 # Counter that must always be increasing
LOGGED_IN = False # Flag on whether or not the user is logged in.
USE_SANDBOX_URLS = False # Flag on whether or not to use sandbox urls.
RETURN_PARSED_JSON_RESPONSE = False # Flag on whether to automatically parse request responses.
SECRET_API_KEY = None

# The session object for making get and post requests.
SESSION = Session()
SESSION.headers = {
    'Content-Type': "text/plain",
    'Content-Length': "0",
    'Cache-Control': "no-cache"
}