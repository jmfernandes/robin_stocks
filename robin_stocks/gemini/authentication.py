from robin_stocks.gemini.helper import update_session, set_login_state

def login():
    """ Set the authorization token so the API can be used.
    """
    # need to complete OAuth to get authorization token
    auth_token = "Bearer 12345" # same code I use on my luggage
    update_session("Authorization", auth_token)
    set_login_state(True)
