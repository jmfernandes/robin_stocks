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

>>> pip install robin-stocks

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
>>>   print(key,value)

There is also the ability to buy and sell stocks. For example, if you wanted to buy 10 shares
of Apple, you would type

>>> r.order_buy_market('AAPL',10)

and if you wanted to sell half your Tesla stock if it fell to 200.00 you would type

>>> positions_data = r.get_current_positions()
>>> TSLAData = [item for item in positions_data if
>>>            r.get_name_by_url(item['instrument']) == r.get_name_by_symbol('TSLA')][0]
>>> sellQuantity = float(TSLAData['quantity'])//2.0
>>> r.order_sell_limit('TSLA',sellQuantity,200.00)

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
(NOTE: parameters that are equal to a value are optional when calling the function.)

Logging in and out
------------------

- login(username,password)
- logout()

Getting ids
-----------
- get_id(symbol)
- get_option_id(symbol)
- get_tradable_chain_id(symbol)
- get_specific_option_id(symbol)

Getting profile information
---------------------------

- load_user_profile(info=None)
- load_investment_profile(info=None)
- load_basic_profile(info=None)
- load_portfolios_profile(info=None)
- load_account_profile(info=None)
- load_security_profile(info=None)

Getting stock information
-------------------------

- get_quotes(\*inputSymbols,info=None)
- get_latest_price(\*inputSymbols)
- get_fundamentals(\*inputSymbols,info=None)
- get_instruments_by_symbols(\*inputSymbols,info=None)
- get_instruments_by_url(url,info=None)
- get_name_by_symbol(symbol)
- get_name_by_url(url)
- get_historicals(\*inputSymbols,span='week',bounds='regular')
- find_instruments(query)
- get_ratings(symbol,info=None)
- get_popularity(symbol,info=None)
- get_events(symbol,info=None)
- get_earnings(symbol,info=None)
- get_news(symbol,info=None)
- get_splits(symbol,info=None)

Getting position information
----------------------------

- get_positions(info=None)
- get_owned_positions(info=None)
- get_dividends(info=None)
- get_total_dividends()

Getting documents
-----------------

- get_documents(info=None)
- download_document(url,name=None,dirpath=None)
- download_all_documents(doctype=None,dirpath=None)

Manipulating watchlists
-----------------------

- get_all_watchlists(info=None)
- get_watchlist_by_name(name='Default',info=None)
- post_symbols_to_watchlist(\*inputSymbols,name='Default')
- delete_symbols_from_watchlist(\*inputSymbols,name='Default')

Getting market information
--------------------------

- get_notifications(info=None)
- get_latest_notification()
- get_top_movers(direction,info=None)
- get_markets(info=None)
- get_wire_transfers(info=None)
- get_margin_calls(symbol)
- get_deposits()

Manipulating orders
-------------------

- get_all_orders(info=None)
- get_all_open_orders(info=None)
- get_order_info(order_id)
- find_orders(\*\*arguments)
- cancel_all_open_orders()
- cancel_order(order_id)

Placing orders
--------------

- order_buy_market(symbol,quantity,timeInForce='gtc')
- order_buy_limit(symbol,quantity,limitPrice,timeInForce='gtc')
- order_buy_stop_loss(symbol,quantity,stopPrice,timeInForce='gtc')
- order_buy_stop_limit(symbol,quantity,limitPrice,stopPrice,timeInForce='gtc')
- order_sell_market(symbol,quantity,timeInForce='gtc')
- order_sell_limit(symbol,quantity,limitPrice,timeInForce='gtc')
- order_sell_stop_loss(symbol,quantity,stopPrice,timeInForce='gtc')
- order_sell_stop_limit(symbol,quantity,limitPrice,stopPrice,timeInForce='gtc')
- order(symbol,quantity,type,limitPrice,stopPrice,trigger,side,timeInForce)

Options
-------

- get_aggregate_positions(info=None)
- get_market_options(info=None)
- get_open_option_positions(info=None)
- get_all_option_positions(info=None)
- get_chains(symbol,info=None)
- find_options_for_stock_by_expiration(symbol,expirationDate,type='both',info=None)
- find_options_for_stock_by_strike(symbol,strike,type='both',info=None)
- find_options_for_stock_by_expiration_and_strike(symbol,expirationDate,strike,type='both',info=None)
- find_options_for_list_of_stocks_by_expiration_date(\*inputSymbols,expirationDate,optionType='both',info=None)
- get_available_option_calls(symbol,info=None)
- get_available_option_puts(symbol,info=None)
- get_list_market_data(\*inputSymbols,info=None)
- get_option_market_data_by_id(id,info=None)
- get_option_market_data(symbol,expirationDate,strike,type,info=None)
- get_option_instrument_data_by_id(id,info=None)
- get_option_instrument_data(symbol,expirationDate,strike,type,info=None)
- get_option_historicals(symbol,expirationDate,strike,optionType,span='week')

Building core user info
-----------------------

- build_holdings()
- build_user_profile()
