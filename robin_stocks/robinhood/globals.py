"""Holds the session header and other global variables."""
import sys
import os

from requests import Session

# Keeps track on if the user is logged in or not.
LOGGED_IN = False
# The session object for making get and post requests.
SESSION = Session()
SESSION.headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "en-US,en;q=1",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "X-Robinhood-API-Version": "1.315.0",
    "Connection": "keep-alive",
    "User-Agent": "*"
}

#All print() statement direct their output to this stream
#by default, we use stdout which is the existing behavior
#but a client can change to any normal Python stream that
#print() accepts.  Common options are
#sys.stderr for standard error
#open(os.devnull,"w") for dev null
#io.StringIO() to go to a string for the client to inspect
OUTPUT=sys.stdout
