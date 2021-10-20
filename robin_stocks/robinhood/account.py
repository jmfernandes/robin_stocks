"""Contains functions for getting information related to the user account."""
import os
from uuid import uuid4

from robin_stocks.robinhood.helper import *
from robin_stocks.robinhood.profiles import *
from robin_stocks.robinhood.stocks import *
from robin_stocks.robinhood.urls import *


@login_required
def load_phoenix_account(info=None):
    """Returns unified information about your account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries of key/value pairs. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * account_buying_power
                      * cash_available_from_instant_deposits
                      * cash_held_for_currency_orders
                      * cash_held_for_dividends
                      * cash_held_for_equity_orders
                      * cash_held_for_options_collateral
                      * cash_held_for_orders
                      * crypto
                      * crypto_buying_power
                      * equities
                      * extended_hours_portfolio_equity
                      * instant_allocated
                      * levered_amount
                      * near_margin_call
                      * options_buying_power
                      * portfolio_equity
                      * portfolio_previous_close
                      * previous_close
                      * regular_hours_portfolio_equity
                      * total_equity
                      * total_extended_hours_equity
                      * total_extended_hours_market_value
                      * total_market_value
                      * total_regular_hours_equity
                      * total_regular_hours_market_value
                      * uninvested_cash
                      * withdrawable_cash

    """
    url = phoenix_url()
    data = request_get(url, 'regular')
    return(filter_data(data, info))

@login_required
def get_historical_portfolio(interval=None, span='week', bounds='regular',info=None):
    interval_check = ['5minute', '10minute', 'hour', 'day', 'week']
    span_check = ['day', 'week', 'month', '3month', 'year', '5year', 'all']
    bounds_check = ['extended', 'regular', 'trading']

    if interval not in interval_check:
        if interval is None and (bounds != 'regular' and span != 'all'):
            print ('ERROR: Interval must be None for "all" span "regular" bounds', file=get_output())
            return ([None])
        print(
            'ERROR: Interval must be "5minute","10minute","hour","day",or "week"', file=get_output())
        return([None])
    if span not in span_check:
        print('ERROR: Span must be "day","week","month","3month","year",or "5year"', file=get_output())
        return([None])
    if bounds not in bounds_check:
        print('ERROR: Bounds must be "extended","regular",or "trading"')
        return([None])
    if (bounds == 'extended' or bounds == 'trading') and span != 'day':
        print('ERROR: extended and trading bounds can only be used with a span of "day"', file=get_output())
        return([None])

    account = load_account_profile('account_number')
    url = portfolis_historicals_url(account)
    payload = {
        'interval': interval,
        'span': span,
        'bounds': bounds
    }
    data = request_get(url, 'regular', payload)

    return(filter_data(data, info))

@login_required
def get_all_positions(info=None):
    """Returns a list containing every position ever traded.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * url
                      * instrument
                      * account
                      * account_number
                      * average_buy_price
                      * pending_average_buy_price
                      * quantity
                      * intraday_average_buy_price
                      * intraday_quantity
                      * shares_held_for_buys
                      * shares_held_for_sells
                      * shares_held_for_stock_grants
                      * shares_held_for_options_collateral
                      * shares_held_for_options_events
                      * shares_pending_from_options_events
                      * updated_at
                      * created_at

    """
    url = positions_url()
    data = request_get(url, 'pagination')

    return(filter_data(data, info))


@login_required
def get_open_stock_positions(info=None):
    """Returns a list of stocks that are currently held.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * url
                      * instrument
                      * account
                      * account_number
                      * average_buy_price
                      * pending_average_buy_price
                      * quantity
                      * intraday_average_buy_price
                      * intraday_quantity
                      * shares_held_for_buys
                      * shares_held_for_sells
                      * shares_held_for_stock_grants
                      * shares_held_for_options_collateral
                      * shares_held_for_options_events
                      * shares_pending_from_options_events
                      * updated_at
                      * created_at

    """
    url = positions_url()
    payload = {'nonzero': 'true'}
    data = request_get(url, 'pagination', payload)

    return(filter_data(data, info))


@login_required
def get_dividends(info=None):
    """Returns a list of dividend trasactions that include information such as the percentage rate,
    amount, shares of held stock, and date paid.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: [list] Returns a list of dictionaries of key/value pairs for each divident payment. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * id
                      * url
                      * account
                      * instrument
                      * amount
                      * rate
                      * position
                      * withholding
                      * record_date
                      * payable_date
                      * paid_at
                      * state
                      * nra_withholding
                      * drip_enabled

    """
    url = dividends_url()
    data = request_get(url, 'pagination')

    return(filter_data(data, info))


@login_required
def get_total_dividends():
    """Returns a float number representing the total amount of dividends paid to the account.

    :returns: Total dollar amount of dividends paid to the account as a 2 precision float.

    """
    url = dividends_url()
    data = request_get(url, 'pagination')

    dividend_total = 0
    for item in data:
        dividend_total += float(item['amount']) if (item['state'] == 'paid' or item['state'] == 'reinvested') else 0
    return(dividend_total)


@login_required
def get_dividends_by_instrument(instrument, dividend_data):
    """Returns a dictionary with three fields when given the instrument value for a stock

    :param instrument: The instrument to get the dividend data.
    :type instrument: str
    :param dividend_data: The information returned by get_dividends().
    :type dividend_data: list
    :returns: dividend_rate       -- the rate paid for a single share of a specified stock \
              total_dividend      -- the total dividend paid based on total shares for a specified stock \
              amount_paid_to_date -- total amount earned by account for this particular stock
    """
    #global dividend_data
    try:
        data = list(
            filter(lambda x: x['instrument'] == instrument, dividend_data))

        dividend = float(data[0]['rate'])
        total_dividends = float(data[0]['amount'])
        total_amount_paid = float(sum([float(d['amount']) for d in data]))

        return {
            'dividend_rate': "{0:.2f}".format(dividend),
            'total_dividend': "{0:.2f}".format(total_dividends),
            'amount_paid_to_date': "{0:.2f}".format(total_amount_paid)
        }
    except:
        pass


@login_required
def get_notifications(info=None):
    """Returns a list of notifications.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each notification. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = notifications_url()
    data = request_get(url, 'pagination')

    return(filter_data(data, info))


@login_required
def get_latest_notification():
    """Returns the time of the latest notification.

    :returns: Returns a dictionary of key/value pairs. But there is only one key, 'last_viewed_at'

    """
    url = notifications_url(True)
    data = request_get(url)
    return(data)


@login_required
def get_wire_transfers(info=None):
    """Returns a list of wire transfers.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each wire transfer. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = wiretransfers_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


@login_required
def get_margin_calls(symbol=None):
    """Returns either all margin calls or margin calls for a specific stock.

    :param symbol: Will determine which stock to get margin calls for.
    :type symbol: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each margin call.

    """
    url = margin_url()
    if symbol:
        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message, file=get_output())
            return None
        payload = {'equity_instrument_id', id_for_stock(symbol)}
        data = request_get(url, 'results', payload)
    else:
        data = request_get(url, 'results')

    return(data)


@login_required
def withdrawl_funds_to_bank_account(ach_relationship, amount, info=None):
    """Submits a post request to withdraw a certain amount of money to a bank account.

    :param ach_relationship: The url of the bank account you want to withdrawl the money to.
    :type ach_relationship: str
    :param amount: The amount of money you wish to withdrawl.
    :type amount: float
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for the transaction.

    """
    url = banktransfers_url()
    payload = {
        "amount": amount,
        "direction": "withdraw",
        "ach_relationship": ach_relationship,
        "ref_id": str(uuid4())
    }
    data = request_post(url, payload)
    return(filter_data(data, info))


@login_required
def deposit_funds_to_robinhood_account(ach_relationship, amount, info=None):
    """Submits a post request to deposit a certain amount of money from a bank account to Robinhood.

    :param ach_relationship: The url of the bank account you want to deposit the money from.
    :type ach_relationship: str
    :param amount: The amount of money you wish to deposit.
    :type amount: float
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for the transaction.

    """
    url = banktransfers_url()
    payload = {
        "amount": amount,
        "direction": "deposit",
        "ach_relationship": ach_relationship,
        "ref_id": str(uuid4())
    }
    data = request_post(url, payload)
    return(filter_data(data, info))

@login_required
def get_linked_bank_accounts(info=None):
    """Returns all linked bank accounts.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each bank.

    """
    url = linked_url()
    data = request_get(url, 'results')
    return(filter_data(data, info))


@login_required
def get_bank_account_info(id, info=None):
    """Returns a single dictionary of bank information

    :param id: The bank id.
    :type id: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictinoary of key/value pairs for the bank. If info parameter is provided, \
    the value of the key that matches info is extracted.

    """
    url = linked_url(id)
    data = request_get(url)
    return(filter_data(data, info))


@login_required
def unlink_bank_account(id):
    """Unlinks a bank account.

    :param id: The bank id.
    :type id: str
    :returns: Information returned from post request.

    """
    url = linked_url(id, True)
    data = request_post(url)
    return(data)


@login_required
def get_bank_transfers(direction=None, info=None):
    """Returns all bank transfers made for the account.

    :param direction: Possible values are 'received'. If left blank, function will return all withdrawls and deposits \
        that are initiated from Robinhood. If the value is 'received', funciton will return transfers intiated from \
        your bank rather than Robinhood.
    :type direction: Optional[str]
    :param info: Will filter the results to get a specific value. 'direction' gives if it was deposit or withdrawl.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each transfer. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = banktransfers_url(direction)
    data = request_get(url, 'pagination')
    return(filter_data(data, info))

@login_required
def get_card_transactions(cardType=None, info=None):
    """Returns all debit card transactions made on the account

    :param cardType: Will filter the card transaction types. Can be 'pending' or 'settled'.
    :type cardType: Optional[str]
    :param info: Will filter the results to get a specific value. 'direction' gives if it was debit or credit.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each transfer. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    payload = None
    if type:
        payload = { 'type': type }

    url = cardtransactions_url()
    data = request_get(url, 'pagination', payload)
    return(filter_data(data, info))

@login_required
def get_stock_loan_payments(info=None):
    """Returns a list of loan payments.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each payment. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = stockloan_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


@login_required
def get_margin_interest(info=None):
    """Returns a list of margin interest.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each interest. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = margininterest_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


@login_required
def get_subscription_fees(info=None):
    """Returns a list of subscription fees.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each fee. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = subscription_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


@login_required
def get_referrals(info=None):
    """Returns a list of referrals.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each referral. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = referral_url()
    data = request_get(url, 'pagination')
    return(filter_data(data, info))


@login_required
def get_day_trades(info=None):
    """Returns recent day trades.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each day trade. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    account = load_account_profile('account_number')
    url = daytrades_url(account)
    data = request_get(url, 'regular')
    return(filter_data(data, info))


@login_required
def get_documents(info=None):
    """Returns a list of documents that have been released by Robinhood to the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each document. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = documents_url()
    data = request_get(url, 'pagination')

    return(filter_data(data, info))


@login_required
def download_document(url, name=None, dirpath=None):
    """Downloads a document and saves as it as a PDF. If no name is given, document is saved as
    the name that Robinhood has for the document. If no directory is given, document is saved in the root directory of code.

    :param url: The url of the document. Can be found by using get_documents(info='download_url').
    :type url: str
    :param name: The name to save the document as.
    :type name: Optional[str]
    :param dirpath: The directory of where to save the document.
    :type dirpath: Optional[str]
    :returns: Returns the data from the get request.

    """
    data = request_document(url)

    print('Writing PDF...', file=get_output())
    if not name:
        name = url[36:].split('/', 1)[0]

    if dirpath:
        directory = dirpath
    else:
        directory = 'robin_documents/'

    filename = directory + name + ' .pdf'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    open(filename, 'wb').write(data.content)
    print('Done - Wrote file {}.pdf to {}'.format(name, os.path.abspath(filename)))

    return(data)


@login_required
def download_all_documents(doctype=None, dirpath=None):
    """Downloads all the documents associated with an account and saves them as a PDF.
    If no name is given, document is saved as a combination of the data of creation, type, and id.
    If no directory is given, document is saved in the root directory of code.

    :param doctype: The type of document to download, such as account_statement.
    :type doctype: Optional[str]
    :param dirpath: The directory of where to save the documents.
    :type dirpath: Optional[str]
    :returns: Returns the list of documents from get_documents(info=None)

    """
    documents = get_documents()

    downloaded_files = False
    if dirpath:
        directory = dirpath
    else:
        directory = 'robin_documents/'

    counter = 0
    for item in documents:
        if doctype == None:
            data = request_document(item['download_url'])
            if data:
                name = item['created_at'][0:10] + '-' + \
                    item['type'] + '-' + item['id']
                filename = directory + name + '.pdf'
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                open(filename, 'wb').write(data.content)
                downloaded_files = True
                counter += 1
                print('Writing PDF {}...'.format(counter), file=get_output())
        else:
            if item['type'] == doctype:
                data = request_document(item['download_url'])
                if data:
                    name = item['created_at'][0:10] + '-' + \
                        item['type'] + '-' + item['id']
                    filename = directory + name + '.pdf'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    open(filename, 'wb').write(data.content)
                    downloaded_files = True
                    counter += 1
                    print('Writing PDF {}...'.format(counter), file=get_output())

    if downloaded_files == False:
        print('WARNING: Could not find files of that doctype to download', file=get_output())
    else:
        if counter == 1:
            print('Done - wrote {} file to {}'.format(counter,
                                                      os.path.abspath(directory)), file=get_output())
        else:
            print('Done - wrote {} files to {}'.format(counter,
                                                       os.path.abspath(directory)), file=get_output())

    return(documents)


@login_required
def get_all_watchlists(info=None):
    """Returns a list of all watchlists that have been created. Everyone has a 'My First List' watchlist.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of the watchlists. Keywords are 'url', 'user', and 'name'.

    """
    url = watchlists_url()
    data = request_get(url, 'result')
    return(filter_data(data, info))


@login_required
def get_watchlist_by_name(name="My First List", info=None):
    """Returns a list of information related to the stocks in a single watchlist.

    :param name: The name of the watchlist to get data from.
    :type name: Optional[str]
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries that contain the instrument urls and a url that references itself.

    """

    #Get id of requested watchlist
    all_watchlists = get_all_watchlists()
    watchlist_id = ''
    for wl in all_watchlists['results']:
        if wl['display_name'] == name:
            watchlist_id = wl['id']

    url = watchlists_url(name)
    data = request_get(url,'list_id',{'list_id':watchlist_id})
    return(filter_data(data, info))


@login_required
def post_symbols_to_watchlist(inputSymbols, name="My First List"):
    """Posts multiple stock tickers to a watchlist.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param name: The name of the watchlist to post data to.
    :type name: Optional[str]
    :returns: Returns result of the post request.

    """
    symbols = inputs_to_set(inputSymbols)
    ids = get_instruments_by_symbols(symbols, info='id')
    data = []
    #Get id of requested watchlist
    all_watchlists = get_all_watchlists()
    watchlist_id = ''
    for wl in all_watchlists['results']:
        if wl['display_name'] == name:
            watchlist_id = wl['id']

    for id in ids:
        payload = {
            watchlist_id: [{
                "object_type" : "instrument",
                "object_id" : id,
                "operation" : "create"
            }]
        }
        url = watchlists_url(name, True)
        data.append(request_post(url, payload, json=True))

    return(data)


@login_required
def delete_symbols_from_watchlist(inputSymbols, name="My First List"):
    """Deletes multiple stock tickers from a watchlist.

    :param inputSymbols: May be a single stock ticker or a list of stock tickers.
    :type inputSymbols: str or list
    :param name: The name of the watchlist to delete data from.
    :type name: Optional[str]
    :returns: Returns result of the delete request.

    """
    symbols = inputs_to_set(inputSymbols)
    ids = get_instruments_by_symbols(symbols, info='id')
    data = []

    #Get id of requested watchlist
    all_watchlists = get_all_watchlists()
    watchlist_id = ''
    for wl in all_watchlists['results']:
        if wl['display_name'] == name:
            watchlist_id = wl['id']

    for id in ids:
        payload = {
            watchlist_id: [{
                "object_type" : "instrument",
                "object_id" : id,
                "operation" : "delete"
            }]
        }
        url = watchlists_url(name, True)
        data.append(request_post(url, payload, json=True))

    return(data)


@login_required
def build_holdings(with_dividends=False):
    """Builds a dictionary of important information regarding the stocks and positions owned by the user.

    :param with_dividends: True if you want to include divident information.
    :type with_dividends: bool
    :returns: Returns a dictionary where the keys are the stock tickers and the value is another dictionary \
    that has the stock price, quantity held, equity, percent change, equity change, type, name, id, pe ratio, \
    percentage of portfolio, and average buy price.

    """
    positions_data = get_open_stock_positions()
    portfolios_data = load_portfolio_profile()
    accounts_data = load_account_profile()

    # user wants dividend information in their holdings
    if with_dividends is True:
        dividend_data = get_dividends()

    if not positions_data or not portfolios_data or not accounts_data:
        return({})

    if portfolios_data['extended_hours_equity'] is not None:
        total_equity = max(float(portfolios_data['equity']), float(
            portfolios_data['extended_hours_equity']))
    else:
        total_equity = float(portfolios_data['equity'])

    cash = "{0:.2f}".format(
        float(accounts_data['cash']) + float(accounts_data['uncleared_deposits']))

    holdings = {}
    for item in positions_data:
        # It is possible for positions_data to be [None]
        if not item:
            continue

        try:
            instrument_data = get_instrument_by_url(item['instrument'])
            symbol = instrument_data['symbol']
            fundamental_data = get_fundamentals(symbol)[0]

            price = get_latest_price(instrument_data['symbol'])[0]
            quantity = item['quantity']
            equity = float(item['quantity']) * float(price)
            equity_change = (float(quantity) * float(price)) - \
                (float(quantity) * float(item['average_buy_price']))
            percentage = float(item['quantity']) * float(price) * \
                100 / (float(total_equity) - float(cash))
            if (float(item['average_buy_price']) == 0.0):
                percent_change = 0.0
            else:
                percent_change = (float(
                    price) - float(item['average_buy_price'])) * 100 / float(item['average_buy_price'])
            if (float(item['intraday_average_buy_price']) == 0.0):
                intraday_percent_change = 0.0
            else:
                intraday_percent_change = (float(
                    price) - float(item['intraday_average_buy_price'])) * 100 / float(item['intraday_average_buy_price'])
            holdings[symbol] = ({'price': price})
            holdings[symbol].update({'quantity': quantity})
            holdings[symbol].update(
                {'average_buy_price': item['average_buy_price']})
            holdings[symbol].update({'equity': "{0:.2f}".format(equity)})
            holdings[symbol].update(
                {'percent_change': "{0:.2f}".format(percent_change)})
            holdings[symbol].update(
                {'intraday_percent_change': "{0:.2f}".format(intraday_percent_change)})
            holdings[symbol].update(
                {'equity_change': "{0:2f}".format(equity_change)})
            holdings[symbol].update({'type': instrument_data['type']})
            holdings[symbol].update(
                {'name': get_name_by_symbol(symbol)})
            holdings[symbol].update({'id': instrument_data['id']})
            holdings[symbol].update({'pe_ratio': fundamental_data['pe_ratio']})
            holdings[symbol].update(
                {'percentage': "{0:.2f}".format(percentage)})

            if with_dividends is True:
                # dividend_data was retrieved earlier
                holdings[symbol].update(get_dividends_by_instrument(
                    item['instrument'], dividend_data))

        except:
            pass

    return(holdings)


@login_required
def build_user_profile():
    """Builds a dictionary of important information regarding the user account.

    :returns: Returns a dictionary that has total equity, extended hours equity, cash, and divendend total.

    """
    user = {}

    portfolios_data = load_portfolio_profile()
    accounts_data = load_account_profile()

    if portfolios_data:
        user['equity'] = portfolios_data['equity']
        user['extended_hours_equity'] = portfolios_data['extended_hours_equity']

    if accounts_data:
        cash = "{0:.2f}".format(
            float(accounts_data['cash']) + float(accounts_data['uncleared_deposits']))
        user['cash'] = cash

    user['dividend_total'] = get_total_dividends()

    return(user)
