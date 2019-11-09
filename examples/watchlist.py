import sys
sys.path.insert(1,'/Users/Kevincheng96/Documents/Coding Projects/Python projects/robin_stocks')

import robin_stocks as r

'''
Robinhood includes dividends as part of your net gain. This script removes
dividends from net gain to figure out how much your stocks/options have paid
off.

Note: load_portfolio_profile() contains some other useful breakdowns of equity.
Print profileData and see what other values you can play around with.

'''

#!!! Fill out username and password
username = 'kevincheng96'
password = ''
#!!!

login = r.login(username,password)

profileData = r.load_portfolio_profile()
print(profileData)
watchlist = r.get_watchlist_by_name()
print(watchlist)
