import pickle
from datetime import datetime, timedelta
from pathlib import Path

from cryptography.fernet import Fernet
from robin_stocks.tda.globals import DATA_DIR_NAME, PICKLE_NAME
from robin_stocks.tda.helper import (request_data, set_login_state,
                                     update_session)
from robin_stocks.tda.urls import URLS


def login_first_time(encryption_passcode, client_id, authorization_token, refresh_token):
    """ Stores log in information in a pickle file on the computer. After being used once,
    user can call login() to automatically read in information from pickle file and refresh
    authorization tokens when needed.

    :param encryption_passcode: Encryption key created by generate_encryption_passcode().
    :type encryption_passcode: str
    :param client_id: The Consumer Key for the API account.
    :type client_id: str
    :param authorization_token: The authorization code returned from post request to https://developer.tdameritrade.com/authentication/apis/post/token-0
    :type authorization_token: str
    :param refresh_token: The refresh code returned from post request to https://developer.tdameritrade.com/authentication/apis/post/token-0
    :type refresh_token: str

    """
    if type(encryption_passcode) is str:
        encryption_passcode = encryption_passcode.encode()
    cipher_suite = Fernet(encryption_passcode)
    # Create necessary folders and paths for pickle file as defined in globals.
    data_dir = Path.home().joinpath(DATA_DIR_NAME)
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
    pickle_path = data_dir.joinpath(PICKLE_NAME)
    if not pickle_path.exists():
        Path.touch(pickle_path)
    # Write information to the file.
    with pickle_path.open("wb") as pickle_file:
        pickle.dump(
            {
                'authorization_token': cipher_suite.encrypt(authorization_token.encode()),
                'refresh_token': cipher_suite.encrypt(refresh_token.encode()),
                'client_id': cipher_suite.encrypt(client_id.encode()),
                'authorization_timestamp': datetime.now(),
                'refresh_timestamp': datetime.now()
            }, pickle_file)


def login(encryption_passcode):
    """ Set the authorization token so the API can be used. Gets a new authorization token
    every 30 minutes using the refresh token. Gets a new refresh token every 60 days.

    :param encryption_passcode: Encryption key created by generate_encryption_passcode().
    :type encryption_passcode: str
    
    """
    if type(encryption_passcode) is str:
        encryption_passcode = encryption_passcode.encode()
    cipher_suite = Fernet(encryption_passcode)
    # Check that file exists before trying to read from it.
    data_dir = Path.home().joinpath(DATA_DIR_NAME)
    pickle_path = data_dir.joinpath(PICKLE_NAME)
    if not pickle_path.exists():
        raise FileExistsError(
            "Please Call login_first_time() to create pickle file.")
    # Read the information from the pickle file.
    with pickle_path.open("rb") as pickle_file:
        pickle_data = pickle.load(pickle_file)
        access_token = cipher_suite.decrypt(pickle_data['authorization_token']).decode()
        refresh_token = cipher_suite.decrypt(pickle_data['refresh_token']).decode()
        client_id = cipher_suite.decrypt(pickle_data['client_id']).decode()
        authorization_timestamp = pickle_data['authorization_timestamp']
        refresh_timestamp = pickle_data['refresh_timestamp']
    # Authorization tokens expire after 30 mins. Refresh tokens expire after 90 days,
    # but you need to request a fresh authorization and refresh token before it expires.
    authorization_delta = timedelta(seconds=1800)
    refresh_delta = timedelta(days=60)
    url = URLS.oauth()
    # If it has been longer than 60 days. Get a new refresh and authorization token.
    # Else if it has been longer than 30 minutes, get only a new authorization token.
    if (datetime.now() - refresh_timestamp > refresh_delta):
        payload = {
            "grant_type": "refresh_token",
            "access_type": "offline",
            "refresh_token": refresh_token,
            "client_id": client_id
        }
        data, _ = request_data(url, payload, True)
        if "access_token" not in data and "refresh_token" not in data:
            raise ValueError(
                "Refresh token is no longer valid. Call login_first_time() to get a new refresh token.")
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]
        with pickle_path.open("wb") as pickle_file:
            pickle.dump(
                {
                    'authorization_token': cipher_suite.encrypt(access_token.encode()),
                    'refresh_token': cipher_suite.encrypt(refresh_token.encode()),
                    'client_id': cipher_suite.encrypt(client_id.encode()),
                    'authorization_timestamp': datetime.now(),
                    'refresh_timestamp': datetime.now()
                }, pickle_file)
    elif (datetime.now() - authorization_timestamp > authorization_delta):
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id
        }
        data, _ = request_data(url, payload, True)
        if "access_token" not in data:
            raise ValueError(
                "Refresh token is no longer valid. Call login_first_time() to get a new refresh token.")
        access_token = data["access_token"]
        # Write new data to file. Do not replace the refresh timestamp.
        with pickle_path.open("wb") as pickle_file:
            pickle.dump(
                {
                    'authorization_token': cipher_suite.encrypt(access_token.encode()),
                    'refresh_token': cipher_suite.encrypt(refresh_token.encode()),
                    'client_id': cipher_suite.encrypt(client_id.encode()),
                    'authorization_timestamp': datetime.now(),
                    'refresh_timestamp': refresh_timestamp
                }, pickle_file)
    # Store authorization token in session information to be used with API calls.
    auth_token = "Bearer {0}".format(access_token)
    update_session("Authorization", auth_token)
    update_session("apikey", client_id)
    set_login_state(True)
    return auth_token


def generate_encryption_passcode():
    """ Returns an encryption key to be used for logging in.

    :returns: Returns a byte object to be used with cryptography.

    """
    return Fernet.generate_key().decode()
