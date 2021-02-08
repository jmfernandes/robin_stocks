import os
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from json import dumps

from robin_stocks.tda.globals import DATA_DIR_NAME, PICKLE_NAME
from robin_stocks.tda.helper import set_login_state, update_session, request_post
from robin_stocks.tda.urls import URLS

def login_first_time(client_id, authorization_token, refresh_token):
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
                'authorization_token': authorization_token,
                'refresh_token': refresh_token,
                'client_id': client_id,
                'timestamp': datetime.now()
            }, pickle_file)


def login():
    """ Set the authorization token so the API can be used.
    """
    # Check that file exists before trying to read from it.
    data_dir = Path.home().joinpath(DATA_DIR_NAME)
    pickle_path = data_dir.joinpath(PICKLE_NAME)
    if not pickle_path.exists():
        raise FileExistsError(
            "Please Call login_first_time() to create pickle file.")
    # Read the information from the pickle file.
    with pickle_path.open("rb") as pickle_file:
        pickle_data = pickle.load(pickle_file)
        access_token = pickle_data['authorization_token']
        refresh_token = pickle_data['refresh_token']
        client_id = pickle_data['client_id']
        timestamp = pickle_data['timestamp']

    delta = timedelta(minutes=1800)
    if (datetime.now() - timestamp > delta):
        url = URLS.oauth()
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id
            }
        data, _ = request_post(url, payload, False)
        access_token = data["access_token"]

    auth_token = "Bearer {0}".format(access_token)
    update_session("Authorization", auth_token)
    update_session("apikey", client_id)
    set_login_state(True)