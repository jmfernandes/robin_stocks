import robin_stocks.robinhood as r
'''
This is an example script that will place an option spread.
'''

#!!! Fill out username and password
username = ''
password = ''
#!!!

login = r.login(username,password)

#!!! WARNING - Some option spreads have UNLIMITED risk.
#!!! Note - Make sure to check the prices of option legs before placing a spread order. Some vertical spreads carry more risk.
#!!! Note- When you open a sell position, in order to close it out you have to "buy to close" or in other words, you have to
#!!! buy the same call option but with effet : close. In contrast, when you buy a call you then have to "sell to close".

#!!! An example bull call spread (net debit). For Plug Power currently at a price of 3.10 on October 20th, 2019.
leg1 = {"expirationDate":"2019-12-20",
        "strike":"2.00",
        "optionType":"call",
        "effect":"open",
        "action":"buy"}

leg2 = {"expirationDate":"2019-12-20",
        "strike":"4.00",
        "optionType":"call",
        "effect":"open",
        "action":"sell"}

spread = [leg1,leg2]
#!!!

order = r.order_option_spread("debit", 3.10, "PLUG", 1, spread)
print(order)
