import robin_stocks as r
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
symbol = 'V'
expirationDate = '2018-11-16'
strike = 150
optionType = 'call'
span = 'year' #available options are day,week,year, and 5year
#!!!

historicalData = r.get_option_historicals(symbol,expirationDate,strike,optionType,span)

dates = []
closingPrices = []
openPrices = []

for item in historicalData['data_points']:
    print(item)
    dates.append(item['begins_at'])
    closingPrices.append(item['close_price'])
    openPrices.append(item['open_price'])


#!!! I made it so it only got the last 30 days but you could delete these lines to get full year.
dates = dates[-30:]
closingPrices = closingPrices[-30:]
openPrices = openPrices[-30:]
#

# change the dates into a format that matplotlib can recognize.
x = [dt.datetime.strptime(d,'%Y-%m-%dT%H:%M:%SZ') for d in dates]

# plots the data.
plt.plot(x, closingPrices, 'ro')
plt.plot(x, openPrices, 'bo')
plt.title("Option price for "+r.get_name_by_symbol(symbol)+" over time")
plt.xlabel("Dates")
plt.ylabel("Price")
plt.show()
