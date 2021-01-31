import os

import pyotp
import robin_stocks.robinhood as r
from dotenv import load_dotenv
'''
This is an example script that will automatically log you in with two factor authentication.
This script also adds security by using dotenv to store credentials in a safe .env file.
To use this script, create a new file in the same directory with the name ".env" and
put all your credentials in the file. An example is in github named ".test.env".

OR, you can explicitly providing path to ".env"
>>>from pathlib import Path  # Python 3.6+ only
>>>env_path = Path(".") / put the path to the ".env" file here instead of the "."
>>>load_dotenv(dotenv_path=env_path)

Note: must have two factor turned on in robinhood app. README on github has info on
how to do that.
'''

load_dotenv()

totp = pyotp.TOTP(os.environ['robin_mfa']).now()
print("Current OTP:", totp)
# Here I am setting store_session=False so no pickle file is used.
login = r.login(os.environ['robin_username'],
                os.environ['robin_password'], store_session=False, mfa_code=totp)
# In the login dictionary, you will see that 'detail' is 
# 'logged in with brand new authentication code.' to show that I am not using a pickle file.
print(login)
