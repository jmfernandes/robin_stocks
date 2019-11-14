import robin_stocks as r
'''
This is an example script that will place an option spread.
'''

#!!! Fill out username and password
username = ''
password = ''
#!!!

login = r.login(username,password)

#!!! WARNING - Some option spreads have UNLIMITED risk.
#!!! An example bull call spread (net debit). For Plug Power currently at a price of 3.10 on October 20th, 2019.
leg1 = {"expirationDate":"2019-12-20",
        "strike":"2.00",
        "optionType":"call",
        "effect":"open",
        "action":"buy"}

leg2 = {"expirationDate":"2019-12-20",
        "strike":"4.00",
        "optionType":"call",
        "effect":"close",
        "action":"sell"}

spread = [leg1,leg2]
#!!!

order = r.order_option_spread("debit", 3.10, "PLUG", 1, spread)
print(order)
