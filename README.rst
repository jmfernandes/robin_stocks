Robinhood API Library
========================

Introduction
========================
This library aims to create simple to use functions to interact with the
Robinhood API. This is a pure python interface and it requires Python3.

Installing
========================
There is no need to download these files directly. This project is published on PyPi so it can be installed by typing into terminal:

>>> pip install robin_stocks

Example Usage
========================
In your python code write:

>>> from robin_stocks import robin_stocks
>>> r = robin_stocks()
>>> login = r.login('joshsmith@email.com','password')
>>> my_stocks = r.build_holdings()

This will build a dictionary called "my stocks" containing symbols of all the stocks
you hold as the keys, and another dictionary containing important information
about the stocks as the items.

Functions Contained
========================
- login
- logout

- get_user_profile
- get_investment_profile
- get_basic_profile
- get_international_profile [DOES NOT WORK]
- get_employment_profile [DOES NOT WORK]
- get_portfolios_profile
- get_accounts_profile
- get_security_profile

- get_quotes
- get_latest_price
- get_fundamentals
- get_instruments_by_symbols
- get_instruments_by_url
- query_instruments

- get_positions
- get_owned_positions
- get_dividends
- get_total_dividends
- get_name_by_symbol
- get_name_by_url

- get_documents
- download_document
- download_all_documents

- get_historicals
- get_all_watchlists
- get_watchlist_by_name
- post_symbols_to_watchlist
- delete_symbols_from_watchlist

- get_notifications
- get_markets
- get_wire_transfers

- get_all_orders
- get_all_open_orders
- get_order_info
- query_orders
- cancel_all_open_orders
- cancel_order

- order_buy_market
- order_sell_market

- build_holdings
- build_user_profile
