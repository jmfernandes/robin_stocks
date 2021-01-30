
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

Once you have imported Robin Stocks, you will need to login in order to store an authentication token.

Basic
^^^^^

>>> import robin_stocks.robinhood as r
>>> login = r.login(<username>,<password>)

You will be prompted for your MFA token if you have MFA enabled and choose to do the above basic example.

With MFA entered programmatically from Time-based One-Time Password (TOTP)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NOTE: to use this feature, you will have to sign into your robinhood account and turn on two factor authentication.
Robinhood will ask you which two factor authorization app you want to use. Select "other". Robinhood will present you with
an alphanumeric code. This code is what you will use for "My2factorAppHere" in the code below. Run the following code and put
the resulting MFA code into the prompt on your robinhood app.

>>> import pyotp
>>> totp  = pyotp.TOTP("My2factorAppHere").now()
>>> print("Current OTP:", totp)

Once you have entered the above MFA code (the totp variable that is printed out) into your Robinhood account, it will give you a backup code.
Make sure you do not lose this code or you may be locked out of your account!!! You can also take the exact same "My2factorAppHere" from above
and enter it into your phone's authentication app, such as Google Authenticator. This will cause the exact same MFA code to be generated on your phone
as well as your python code. This is important to do if you plan on being away from your computer and need to access your Robinhood account from your phone.

Now you should be able to login with the following code,

>>> import pyotp
>>> import robin_stocks.robinhood as r
>>> totp  = pyotp.TOTP("My2factorAppHere").now()
>>> login = r.login('joshsmith@email.com','password', mfa_code=totp)

Not all of the functions contained in the module need the user to be authenticated. A lot of the functions
contained in the modules 'stocks' and 'options' do not require authentication, but it's still good practice
to log into Robinhood at the start of each script.


Building Profile and User Data
------------------------------

The two most useful functions are ``build_holdings`` and ``build_user_profile``. These condense information from several
functions into a single dictionary. If you wanted to view all your stock holdings then type:

>>> my_stocks = robin_stocks.build_holdings()
>>> for key,value in my_stocks.items():
>>>     print(key,value)

Buying and Selling
------------------

Trading stocks, options, and crypto-currencies is one of the most powerful features of Robin Stocks. There is the ability to submit market orders, limit orders, and stop orders as long as
Robinhood supports it. Here is a list of possible trades you can make

>>> #Buy 10 shares of Apple at market price
>>> robin_stocks.order_buy_market('AAPL',10)
>>> #Sell half a Bitcoin is price reaches 10,000
>>> robin_stocks.order_sell_crypto_limit('BTC',0.5,10000)
>>> #Buy $500 worth of Bitcoin
>>> robin_stocks.order_buy_crypto_by_price('BTC',500)
>>> #Buy 5 $150 May 1st, 2020 SPY puts if the price per contract is $1.00. Good until cancelled.
>>> robin_stocks.order_buy_option_limit('open','debit',1.00,'SPY',5,'2020-05-01',150,'put','gtc')

Now let's try a slightly more complex example. Let's say you wanted to sell half your Tesla stock if it fell to 200.00.
To do this you would type

>>> positions_data = robin_stocks.get_current_positions()
>>> ## Note: This for loop adds the stock ticker to every order, since Robinhood
>>> ## does not provide that information in the stock orders.
>>> ## This process is very slow since it is making a GET request for each order.
>>> for item in positions_data:
>>>     item['symbol'] = robin_stocks.get_symbol_by_url(item['instrument'])
>>> TSLAData = [item for item in positions_data if item['symbol'] == 'TSLA']
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

Working With Orders
-------------------

You can also view all orders you have made. This includes filled orders, cancelled orders, and open orders.
Stocks, options, and cryptocurrencies are separated into three different locations.
For example, let's say that you have some limit orders to buy and sell Bitcoin and those orders have yet to be filled.
If you want to cancel all your limit sells, you would type

>>> positions_data = robin_stocks.get_all_open_crypto_orders()
>>> ## Note: Again we are adding symbol to our list of orders because Robinhood
>>> ## does not include this with the order information.
>>> for item in positions_data:
>>>    item['symbol'] = robin_stocks.get_crypto_quote_from_id(item['currency_pair_id'], 'symbol')
>>> btcOrders = [item for item in positions_data if item['symbol'] == 'BTCUSD' and item['side'] == 'sell']
>>> for item in btcOrders:
>>>    robin_stocks.cancel_crypto_order(item['id'])

Saving to CSV File
------------------
Users can also export a list of all orders to a CSV file. There is a function for stocks and options. Each function
takes a directory path and an optional filename. If no filename is provided, a date stamped filename will be generated. The directory path
can be either absolute or relative. To save the file in the current directory, simply pass in "." as the directory. Note that ".csv" is the only valid
file extension. If it is missing it will be added, and any other file extension will be automatically changed. Below are example calls.

>>> # let's say that I am running code from C:/Users/josh/documents/
>>> r.export_completed_stock_orders(".") # saves at C:/Users/josh/documents/stock_orders_Jun-28-2020.csv
>>> r.export_completed_option_orders("../", "toplevel") # save at C:/Users/josh/toplevel.csv

Using Option Spreads
--------------------
When viewing a spread in the robinhood app, it incorrectly identifies both legs as either "buy" or "sell" when closing a position.
The "direction" has to reverse when you try to close a spread position.

I.e.
direction="credit"
when
"action":"sell","effect":"close"

in the case of a long call or put spread.
