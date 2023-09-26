import robin_stocks.robinhood as r

'''
This is an example script that will show you how to close option positions.
'''

#!!! Fill out username and password
username = ''
password = ''
#!!!

login = r.login(username=username, password=password)

# Let's say you bought five 4/20/20 calls of spy at 300 for 1.00 per contract.
# You would like to sell the calls for 2.00 per contract so you double your money (minus premium).
# Also, you want the order to last until you cancel it. You would sell to close like this.

r.order_sell_option_limit(positionEffect="close", creditOrDebit="credit", price="2.0", symbol="SPY", quantity=5, expirationDate="2020-04-20", strike=300, optionType="call", timeInForce="gtc")

# Let's say you sold one 4/20/20 put of spy at 200 for 5.00 per contract.
# You would like to buy the puts for 2.50 per contract so you double your money (plus premium).
# Also, you only want the order to last the day. You would buy to close like this.

r.order_buy_option_limit(positionEffect="close", creditOrDebit="debit", price="2.5", symbol="SPY", quantity=1, expirationDate="2020-04-20", strike=200, optionType="put", timeInForce="gfd")

# if you don't already own these contracts then robinhood should return an error and not let the order go through.
