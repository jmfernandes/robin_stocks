''' An example on how to set up logging in.
You can store your encryption password in .test.env 
or in a file named .env with the following value

tda_encryption_passcode=keep_this_key_somewhere_safe
'''

import robin_stocks.tda as t
##!!! Optionally load environment variables from .env or .test.env
import os
from dotenv import load_dotenv
load_dotenv()
keep_this_key_somewhere_safe = os.environ["tda_encryption_passcode"]
##!!!

keep_this_key_somewhere_safe = t.generate_encryption_passcode()
print("here is a key you can use for encryption: ", keep_this_key_somewhere_safe)

#!!! Only call login_first_time once! Delete this code after running the first time!
t.login_first_time(
    keep_this_key_somewhere_safe,
    "client_id_goes_here",
    "authorization_token_goes_here",
    "refresh_token_goes_here")
#!!!

# Call login as much as you want.
t.login(os.environ["tda_encryption_passcode"])
