Robinhood API Library
========================

Introduction
========================
This library aims to create functions to interact with the
Robinhood API, which are simple to use, easy to understand, and easy to modify the source code.
This is a pure python interface and it requires Python3. The purpose
of this library is to allow people to make their own robo-investors or to view information on
stocks, options, and crypto-currencies in real time.

To join our Slack channel where you can discuss trading and coding, click the link https://join.slack.com/t/robin-stocks/shared_invite/zt-7up2htza-wNSil5YDa3zrAglFFSxRIA

Installing
========================
There is no need to download these files directly. This project is published on PyPi,
so it can be installed by typing into terminal (on Mac) or into command prompt (on PC):

>>> pip install robin_stocks

Also be sure that Python 3 is installed. If you need to install python you can download it from `Python.org <https://www.python.org/downloads/>`_.
Pip is the package installer for python, and is automatically installed when you install python. To learn more about Pip, you can go to `PyPi.org <https://pypi.org/project/pip/>`_.

If you would like to be able to make changes to the package yourself, clone the repository onto your computer by typing into terminal or command prompt:

>>> git clone https://github.com/jmfernandes/robin_stocks.git
>>> cd robin_stocks

Now that you have cd into the repository you can type

>>> pip install .

and this will install whatever you changed in the local files. This will allow you to make changes and experiment with your own code.

Functions Contained
========================

For a complete list of functions and how to use them, go to `robin-stocks.com <http://www.robin-stocks.com/en/latest/functions.html>`_.

Example Usage
========================

When you write a new python script, you'll have to load the module and login to Robinhood. This is
accomplished by typing

>>> import robin_stocks as r
>>> login = r.login('joshsmith@email.com','password')

Not all of the functions contained in the module need the user to be authenticated. A lot of the functions
contained in the modules 'stocks' and 'options' do not require authentication, but it's still good practice
to log into Robinhood at the start of each script.

There is the ability to buy and sell stocks, options, and crypto-currencies.
There is also the ability to submit market orders, limit orders, and stop orders as long as
Robinhood supports it. Here is a list of possible trades you can make

>>> #Buy 10 shares of Apple at market price
>>> r.order_buy_market('AAPL',10)
>>> #Sell half a Bitcoin is price reaches 10,000
>>> r.order_sell_crypto_limit('BTC',0.5,10000)
>>> #Buy $500 worth of Bitcoin
>>> r.order_buy_crypto_by_price('BTC',500)
>>> #Buy 5 $150 May 1st, 2020 SPY puts if the price per contract is $1.00. Good until cancelled.
>>> r.order_buy_option_limit('open','debit',1.00,'SPY',5,'2020-05-01',150,'put','gtc')

Now let's try a slightly more complex example. Let's say you wanted to sell half your Tesla stock if it fell to 200.00.
To do this you would type

>>> positions_data = r.get_current_positions()
>>> ## Note: This for loop adds the stock ticker to every order, since Robinhood
>>> ## does not provide that information in the stock orders.
>>> ## This process is very slow since it is making a GET request for each order.
>>> for item in positions_data:
>>>     item['symbol'] = r.get_symbol_by_url(item['instrument'])
>>> TSLAData = [item for item in positions_data if item['symbol'] == 'TSLA']
>>> sellQuantity = float(TSLAData['quantity'])//2.0
>>> r.order_sell_limit('TSLA',sellQuantity,200.00)

You can also view all orders you have made. This includes filled orders, cancelled orders, and open orders.
Stocks, options, and cryptocurrencies are separated into three different locations.
For example, let's say that you have some limit orders to buy and sell Bitcoin and those orders have yet to be filled.
If you want to cancel all your limit sells, you would type

>>> positions_data = r.get_all_open_crypto_orders()
>>> ## Note: Again we are adding symbol to our list of orders because Robinhood
>>> ## does not include this with the order information.
>>> for item in positions_data:
>>>    item['symbol'] = r.get_crypto_quote_from_id(item['currency_pair_id'], 'symbol')
>>> btcOrders = [item for item in positions_data if item['symbol'] == 'BTCUSD' and item['side'] == 'sell']
>>> for item in btcOrders:
>>>    r.cancel_crypto_order(item['id'])

If you want to view all the call options for a list of stocks you could type

>>> optionData = r.find_options_for_list_of_stocks_by_expiration_date(['fb','aapl','tsla','nflx'],
>>>              expirationDate='2018-11-16',optionType='call')
>>> for item in optionData:
>>>     print(' price -',item['strike_price'],' exp - ',item['expiration_date'],' symbol - ',
>>>           item['chain_symbol'],' delta - ',item['delta'],' theta - ',item['theta'])

There is a lot more that you can do with this API. Be sure to check out the examples folder to
see even more examples. This folder will get updated periodically to demonstrate new functionality
and best practices.

Keep in mind that the functions contained in the library are just wrappers around a functional API,
and you are free to write your own functions that interact with the Robinhood API. I've
exposed the get and post methods so any call to the Robinhood API could be made. The syntax is

>>> url = 'https://api.robinhood.com/'
>>> payload = { 'key1' : 'value1', 'key2' : 'value2'}
>>> r.request_get(url,'regular',payload)

The above code would results in a get request to ``https://api.robinhood.com/?key1=value1&key2=value2`` (which is a
meaningless request). RobinHood returns most data as { 'previous' : None, 'results' : [], 'next' : None},
where ‘results’ is either a dictionary or a list of dictionaries. If a particular query returns more entries than can be stored
in 'results', then those will be stored in 'next', which is simply a url link to the next set of data.
Keep in mind that RobinHood will sometimes return the data in a different format.
To compensate for this, request_get takes either 'regular', 'results', 'pagination', or 'indexzero' as the second parameter.
In most cases, you want to use 'pagination' to get all the results.


New Features In The Works
=========================

- Trading using TD Ameritrade
