import robin_stocks.robinhood as r
import matplotlib.pyplot as plt
import datetime as dt

'''
This is example code that gets the past 30 days of opening and closing prices
for a specific option call or put. As far as I know, there is no way to view
past prices for options, so this is a very useful piece of code. This code also
plots the data using matplotlib, but the data is contained in the
historicalData list and you are free to do whatever you want with it.

NOTE: closing prices are plotted in red and opening prices plotted in blue.
Matplotlib also has a candlestick option that you can use.
'''

#!!! Fill out username and password
username = ''
password = ''
#!!!

login = r.login(username,password)

#!!! fill out the specific option information
symbol = 'AAPL'
symbol_name = r.get_name_by_symbol(symbol)
expirationDate = '2020-07-02' # format is YYYY-MM-DD.
strike = 300
optionType = 'call' # available options are 'call' or 'put' or None.
interval = 'hour' # available options are '5minute', '10minute', 'hour', 'day', and 'week'.
span = 'week' # available options are 'day', 'week', 'year', and '5year'.
bounds = 'regular' # available options are 'regular', 'trading', and 'extended'.
info = None
#!!!

historicalData = r.get_option_historicals(symbol, expirationDate, strike, optionType, interval, span, bounds, info)

dates = []
closingPrices = []
openPrices = []

for data_point in historicalData:
    dates.append(data_point['begins_at'])
    closingPrices.append(data_point['close_price'])
    openPrices.append(data_point['open_price'])

# change the dates into a format that matplotlib can recognize.
x = [dt.datetime.strptime(d,'%Y-%m-%dT%H:%M:%SZ') for d in dates]

# plot the data.
plt.plot(x, closingPrices, 'ro')
plt.plot(x, openPrices, 'bo')
plt.title("Option price for {} over time".format(symbol_name))
plt.xlabel("Dates")
plt.ylabel("Price")
plt.show()
