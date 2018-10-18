
Quick Start
============

----

.. image:: _static/pics/robinyell.jpg

Importing and Logging In
------------------------

The first thing you will need to do is to import Robin Stocks by typing:

>>> import robin_stocks

robin_stocks will need to added as a preface to every function call in the form of ``robin_stocks.function``.
If you don't want to have to type robin_stocks at the beginning of every call,
then import Robin Stocks by typing

>>> from robin_stocks import *

Keep in mind that this method is not considered good practice as it obfuscates the distinction between Robin Stocks'
functions and other functions. For the rest of the documentation, I will assume that Robin Stocks was imported as ``import robin_stocks``.

Once you have imported Robin Stocks, you will need to login in order to store an authentication token using

>>> robin_stocks.login(<username>,<password>)

Not all functions require authentication, but its good practice to log in to Robinhood at the beginning of your script.


Building Profile and User Data
------------------------------

The two most useful functions are ``build_holdings`` and ``build_user_profile``. These condense information from several
functions into a single dictionary. If you wanted to view all your holdings then type:

>>> my_stocks = robin_stocks.build_holdings()
>>> for key,value in my_stocks.items():
>>>     print(key,value)

Buying and Selling Stock
------------------------

Buying and selling stocks is one of the most powerful features of Robin Stocks. For example, if you wanted to buy 10 shares of Apple, you would type

>>> robin_stocks.order_buy_market('AAPL',10)

and if you wanted to sell half your Tesla stock if it fell to 200.00 you would type

>>> positions_data = robin_stocks.get_current_positions()
>>> TSLAData = [item for item in positions_data if
>>>            robin_stocks.get_name_by_url(item['instrument']) == robin_stocks.get_name_by_symbol('TSLA')][0]
>>> sellQuantity = float(TSLAData['quantity'])//2.0
>>> robin_stocks.order_sell_limit('TSLA',sellQuantity,200.00)

Also be aware that all the order functions default to 'gtc' or 'good until cancelled'. To change this, pass one of the following in as
the last parameter in the function: 'gfd'(good for the day), 'ioc'(immediate or cancel), or 'opg'(execute at opening).

Finding Options
---------------

Manually clicking on stocks and viewing available options can be a chore. Especially, when you also want to view additional information like the greeks.
Robin Stocks gives you the ability to view all the options for a specific expiration date by typing

>>> optionData = robin_stocks.find_options_for_list_of_stocks_by_expiration_date(['fb','aapl','tsla','nflx'],
>>>              expirationDate='2018-11-16',optionType='call')
>>> for item in optionData:
>>>     print(' price -',item['strike_price'],' exp - ',item['expiration_date'],' symbol - ',
>>>           item['chain_symbol'],' delta - ',item['delta'],' theta - ',item['theta'])
