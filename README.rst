Robinhood API Library
========================

Introduction
========================
This library aims to create simple to use functions to interact with the
Robinhood API. This is a pure python interface and it requires Python3. The purpose
of this library is to allow people to make their own robo-investors or to view
stock information in real time.

Installing
========================
There is no need to download these files directly. This project is published on PyPi,
so it can be installed by typing into terminal:

>>> pip install robin_stocks

Example Usage
========================

When you write a new python script, you'll have to load the module and login to Robinhood. This is
accomplished by typing

>>> import robin_stocks as r
>>> login = r.login('joshsmith@email.com','password')

Not all of the functions contained in the module need the user to be authenticated. A lot of the functions
contained in the modules 'stocks' and 'options' do not require authentication, but it's still good practice
to log into Robinhood at the start of each script.

The code provides a lot of ways to view information about your Robinhood account. One way in particular is to type

>>> my_stocks = r.build_holdings()

This will build a dictionary called "my_stocks" where the keys are the ticker symbols of
all the stocks you hold, and the values of those keys are another dictionary containing
important information about the stocks. If you then wanted to print this dictionary, you could type

>>> for key,value in my_stocks.items():
>>>     print(key,value)

There is also the ability to buy and sell stocks. For example, if you wanted to buy 10 shares
of Apple, you would type

>>> r.order_buy_market('AAPL',10)

and if you wanted to sell half your Tesla stock if it fell to 200.00 you would type

>>> positions_data = r.get_current_positions()
>>> TSLAData = [item for item in positions_data if
>>>            r.get_name_by_url(item['instrument']) == r.get_name_by_symbol('TSLA')][0]
>>> sellQuantity = float(TSLAData['quantity'])//2.0
>>> r.order_sell_limit('TSLA',sellQuantity,200.00)

If you want to view all the call options for a list of stocks you could type

>>> optionData = r.find_options_for_list_of_stocks_by_expiration_date(['fb','aapl','tsla','nflx'],
>>>              expirationDate='2018-11-16',optionType='call')
>>> for item in optionData:
>>>     print(' price -',item['strike_price'],' exp - ',item['expiration_date'],' symbol - ',
>>>           item['chain_symbol'],' delta - ',item['delta'],' theta - ',item['theta'])

Keep in mind that the functions contained in the library are just wrappers around a functional API,
and you are free to write your own functions that interact with the Robinhood API. I've
exposed the get and post methods so any call to the Robinhood API could be made. The syntax is

>>> url = 'https://api.robinhood.com/'
>>> payload = { 'key1', 'value1'}
>>> r.request_get(url,'regular',payload)

The above code would results in a get request to ``https://api.robinhood.com/?key1=value1`` (which is a
meaningless request).

Functions Contained
========================

For a complete list of functions and how to use them, go to http://www.robin-stocks.com/
