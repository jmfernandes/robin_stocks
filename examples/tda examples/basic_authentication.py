''' An example on how to set up logging in.
'''
import os

import robin_stocks.tda as t
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

keep_this_key_somewhere_safe = t.generate_encryption_passcode()
print("here is a key you can use for encryption: ", keep_this_key_somewhere_safe)

#!!! Only call login_first_time once! Delete this code after running the first time!
t.login_first_time(
    os.environ["tda_encryption_passcode"],
    "client_id_goes_here",
    "authorization_token_goes_here",
    "refresh_token_goes_here")
#!!!

# Call login as much as you want.
t.login(os.environ["tda_encryption_passcode"])
