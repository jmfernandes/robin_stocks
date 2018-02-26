Robinhood API Library
========================

Introduction
========================
This library aims to create simple to use functions to interact with the
Robinhood API. This is a pure python interface and it requires Python3.

Installing
========================
The library is installed by typing into terminal:

> pip install robin_stocks

Example Usage
========================
In your python code write:

> from robin_stocks import robin_stocks

| > r = robin_stocks()
| > login = r.login('joshsmith@email.com','password')
| > my_stocks = r.build_holdings()

This will build a dictionary where the keys are the symbols of all the my_stocks
you hold, and the items are another dictionary containing important information
about the stocks.

Functions Contained
========================
- login
- logout

- get_user_profile
- get_investment_profile
- get_basic_info
- get_international_info
- get_employment_info
- get_additional_info

- get_quotes
- get_latest_price
- get_instruments_by_symbols
- get_instruments_by_url
- query_instruments

- get_positions
- get_owned_positions
- get_portfolios
- get_accounts
- get_dividends
- get_total_dividends
- get_name_by_symbol
- get_name_by_url

- get_documents
- download_document
- download_all_documents

- build_holdings
- build_user_profile
