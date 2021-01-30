import os

import pyotp
import robin_stocks.robinhood as r
from dotenv import load_dotenv
'''
This is an example script that will get all stocks that are part 
of the "technology" tag. 

NOTE: View the two_factor_log_in.py script to see how automatic
two-factor loggin in works.
'''
# load environment variables.
load_dotenv()
# Login using two-factor code.
totp = pyotp.TOTP(os.environ['robin_mfa']).now()
login = r.login(os.environ['robin_username'],
                os.environ['robin_password'], store_session=True, mfa_code=totp)
# Get 500 technology stocks data.
stocks = r.request_get(
    "https://api.robinhood.com/midlands/tags/tag/technology/")
print(
    f"\nthere are a total of {stocks['membership_count']} technology stocks, currently viewing {len(stocks['instruments'])}")
# Turn the raw dictionary into a list of strings using the filter_data function.
# This list of strings are the urls for the quote data of each stock.
# The quote data can be retrieved using get_instrument_by_url() or
# by using request_get to query the url directly.
data = r.filter_data(stocks, 'instruments')
first = data[0]
first_data = r.request_get(first)
print("\n======the quote data for the first entry is=====\n")
print(first_data)
print("\ngetting the rest of the quote data now. This may take a minute....")
full_quote_data = [r.request_get(x) for x in data]
print("Now I am getting the filter data...")
#I can also filter the data
margin_quote_data = []
for entry in data:
    quote_data = r.request_get(entry)
    if float(quote_data['margin_initial_ratio']) > 0.5:
        margin_quote_data.append(quote_data)
print(f"There are {len(margin_quote_data)} entries that fit the criteria.")
