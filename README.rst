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
In your python code write:

>>> from robin_stocks.robin_stocks import robin_stocks
>>> r = robin_stocks()
>>> login = r.login('joshsmith@email.com','password')
>>> my_stocks = r.build_holdings()

This will build a dictionary called "my_stocks" where the keys are the ticker symbols of
all the stocks you hold, and the values of those keys are another dictionary containing
important information about the stocks. If you then wanted to print this dictionary, you could type

>>> for key,value in my_stocks.items():
>>>   print(key,value)

Keep in mind that the functions contained in the library are just helper functions,
and you are free to write your own functions that interact with the Robinhood API.

Functions Contained
========================
(NOTE: parameters that are equal to a value are optional when calling the function.)

- login(username,password)
- logout()

- get_user_profile(info=None)
- get_investment_profile(info=None)
- get_basic_profile(info=None)
- get_portfolios_profile(info=None)
- get_accounts_profile(info=None)
- get_security_profile(info=None)

- get_quotes(\*inputSymbols,info=None)
- get_latest_price(\*inputSymbols)
- get_fundamentals(\*inputSymbols,info=None)
- get_instruments_by_symbols(\*inputSymbols,info=None)
- get_instruments_by_url(url,info=None)
- query_instruments(query)

- get_positions(info=None)
- get_owned_positions(info=None)
- get_dividends(info=None)
- get_total_dividends()
- get_name_by_symbol(symbol)
- get_name_by_url(url)

- get_documents(info=None)
- download_document(url,name=None,dirpath=None)
- download_all_documents(doctype=None,dirpath=None)

- get_historicals(\*inputSymbols,span='week',bounds='regular')
- get_all_watchlists(info=None)
- get_watchlist_by_name(name='Default',info=None)
- post_symbols_to_watchlist(\*inputSymbols,name='Default')
- delete_symbols_from_watchlist(\*inputSymbols,name='Default')

- get_notifications(info=None)
- get_markets(info=None)
- get_wire_transfers(info=None)

- get_all_orders(info=None)
- get_all_open_orders(info=None)
- get_order_info(order_id)
- query_orders(\*\*arguments)
- cancel_all_open_orders()
- cancel_order(order_id)

- order_buy_market(symbol,quantity,time_in_force='gtc')
- order_sell_market(symbol,quantity,time_in_force='gtc')

- build_holdings()
- build_user_profile()
