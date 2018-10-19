import os
import robin_stocks.helper as helper
import robin_stocks.urls as urls
import robin_stocks.stocks as stocks
import robin_stocks.profiles as profiles

def get_all_positions(info=None):
    """Returns a list containing every position ever traded.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.positions()
    data = helper.request_get(url,'pagination')

    return(helper.filter(data,info))

def get_current_positions(info=None):
    """Returns a list of stocks/options that are currently held.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each ticker. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.positions()
    payload = { 'nonzero' : 'true'}
    data = helper.request_get(url,'pagination',payload)

    return(helper.filter(data,info))

def get_dividends(info=None):
    """Returns a list of dividend trasactions that include information such as the percentage rate,
    amount, shares of held stock, and date paid.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each divident payment. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.dividends()
    data = helper.request_get(url,'pagination')

    return(helper.filter(data,info))

def get_total_dividends():
    """Returns a float number representing the total amount of dividends paid to the account.

    :returns: Total dollar amount of dividends paid to the account as a 2 precision float.

    """
    url = urls.dividends()
    data = helper.request_get(url,'pagination')

    dividend_total = 0
    for item in data:
        dividend_total += float(item['amount'])
    return(dividend_total)

def get_notifications(info=None):
    """Returns a list of notifications.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each notification. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.notifications()
    data = helper.request_get(url,'pagination')

    return(helper.filter(data,info))

def get_latest_notification():
    """Returns the time of the latest notification.

    :returns: Returns a dictionary of key/value pairs. But there is only one key, 'last_viewed_at'

    """
    url = urls.notifications(True)
    data = helper.request_get(url)
    return(data)

def get_wire_transfers(info=None):
    """Returns a list of wire transfers.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each wire transfer. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.wiretransfers()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_margin_calls(symbol=None):
    """Returns either all margin calls or margin calls for a specific stock.

    :param symbol: Will determine which stock to get margin calls for.
    :type symbol: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each margin call.

    """
    url = urls.margin()
    if symbol:
        try:
            symbol = symbol.upper().strip()
        except AttributeError as message:
            print(message)
            return None
        payload = { 'equity_instrument_id', helper.id_for_stock(symbol)}
        data = helper.request_get(url,'results',payload)
    else:
        data = helper.request_get(url,'results')

    return(data)

def get_linked_bank_accounts(info=None):
    """Returns all linked bank accounts.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each bank.

    """
    url = urls.linked()
    data = helper.request_get(url,'results')
    return(helper.filter(data,info))

def get_bank_account_info(id,info=None):
    """Returns a single dictionary of bank information

    :param id: The bank id.
    :type id: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictinoary of key/value pairs for the bank. If info parameter is provided, \
    the value of the key that matches info is extracted.

    """
    url = urls.linked(id)
    data = helper.request_get(url)
    return(helper.filter(data,info))

def unlink_bank_account(id):
    """Unlinks a bank account.

    :param id: The bank id.
    :type id: str
    :returns: Information returned from post request.

    """
    url = urls.linked(id,True)
    data = helper.request_post(url)
    return(data)

def get_bank_transfers(info=None):
    """Returns all bank transfers made for the account.

    :param info: Will filter the results to get a specific value. 'direction' gives if it was deposit or withdrawl.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each transfer. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.banktransfers()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_stock_loan_payments(info=None):
    """Returns a list of loan payments.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each payment. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.stockloan()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_margin_interest(info=None):
    """Returns a list of margin interest.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each interest. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.margininterest()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_subscription_fees(info=None):
    """Returns a list of subscription fees.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each fee. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.subscription()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_referrals(info=None):
    """Returns a list of referrals.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each referral. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.referral()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_day_trades(info=None):
    """Returns recent day trades.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each day trade. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    account = profiles.load_account_profile('account_number')
    url = urls.daytrades(account)
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_documents(info=None):
    """Returns a list of documents that have been released by Robinhood to the account.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each document. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.

    """
    url = urls.documents()
    data = helper.request_get(url,'pagination')

    return(helper.filter(data,info))

def download_document(url,name=None,dirpath=None):
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
    data = helper.request_document(url)

    print('Writing PDF...')
    if not name:
        name = url[36:].split('/',1)[0]

    if dirpath:
        directory = dirpath
    else:
        directory = 'robin_documents/'

    filename = directory+name+'.pdf'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    open(filename, 'wb').write(data.content)
    print('Done - Wrote file {}.pdf to {}'.format(name,os.path.abspath(filename)))

    return(data)

def download_all_documents(doctype=None,dirpath=None):
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
            data = helper.request_document(item['download_url'])
            if data:
                name = item['created_at'][0:10]+'-'+item['type']+'-'+item['id']
                filename = directory+name+'.pdf'
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                open(filename, 'wb').write(data.content)
                downloaded_files = True
                counter += 1
                print('Writing PDF {}...'.format(counter))
        else:
            if item['type'] == doctype:
                data = helper.request_document(item['download_url'])
                if data:
                    name = item['created_at'][0:10]+'-'+item['type']+'-'+item['id']
                    filename = directory+name+'.pdf'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    open(filename, 'wb').write(data.content)
                    downloaded_files = True
                    counter += 1
                    print('Writing PDF {}...'.format(counter))

    if downloaded_files == False:
        print('WARNING: Could not find files of that doctype to download')
    else:
        if counter == 1:
            print('Done - wrote {} file to {}'.format(counter,os.path.abspath(directory)))
        else:
            print('Done - wrote {} files to {}'.format(counter,os.path.abspath(directory)))

    return(documents)

def get_all_watchlists(info=None):
    """Returns a list of all watchlists that have been created. Everone has a 'default' watchlist.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of the watchlists. Keywords are 'url', 'user', and 'name'.

    """
    url = urls.watchlists()
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def get_watchlist_by_name(name='Default',info=None):
    """Returns a list of information related to the stocks in a single watchlist.

    :param name: The name of the watchlist to get data from.
    :type name: Optional[str]
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries that contain the instrument urls and a url that references itself.

    """
    url = urls.watchlists(name)
    data = helper.request_get(url,'pagination')
    return(helper.filter(data,info))

def post_symbols_to_watchlist(*inputSymbols,name='Default'):
    """Posts multiple stock tickers to a watchlist.

    :param inputSymbols: This is a variable length parameter that represents a stock ticker. \
    May be several tickers seperated by commas or a list of tickers.
    :type inputSymbols: str or list
    :param name: The name of the watchlist to post data to.
    :type name: Optional[str]
    :returns: Returns result of the post request.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    payload = {
    'symbols': ','.join(symbols)
    }
    url = urls.watchlists(name,True)
    data = helper.request_post(url,payload)

    return(data)

def delete_symbols_from_watchlist(*inputSymbols,name='Default'):
    """Deletes multiple stock tickers from a watchlist.

    :param inputSymbols: This is a variable length parameter that represents a stock ticker. \
    May be several tickers seperated by commas or a list of tickers.
    :type inputSymbols: str or list
    :param name: The name of the watchlist to delete data from.
    :type name: Optional[str]
    :returns: Returns result of the delete request.

    """
    symbols = helper.inputs_to_set(inputSymbols)
    symbols = stocks.get_fundamentals(symbols,info='instrument')

    watchlist = get_watchlist_by_name(name=name)

    items = []
    data = None

    for symbol in symbols:
        for list_ in watchlist:
            if symbol == list_['instrument']:
                items.append(symbol[37:])

    for item in items:
        url = urls.watchlists()+name+item
        data = helper.request_delete(url)

    return(data)

def build_holdings():
    """Builds a dictionary of important information regarding the stocks and positions owned by the user.

    :returns: Returns a dictionary where the keys are the stock tickers and the value is another dictionary \
    that has the stock price, quantity held, equity, percent change, equity change, type, name, id, pe ratio, \
    percentage of portfolio, and average buy price.

    """
    holdings = {}
    positions_data = get_current_positions()
    portfolios_data = profiles.load_portfolio_profile()
    accounts_data = profiles.load_account_profile()

    if portfolios_data['extended_hours_equity'] is not None:
        total_equity = max(float(portfolios_data['equity']),float(portfolios_data['extended_hours_equity']))
    else:
        total_equity = float(portfolios_data['equity'])

    cash = "{0:.2f}".format(float(accounts_data['cash'])+float(accounts_data['uncleared_deposits']))

    for item in positions_data:
        instrument_data = stocks.get_instrument_by_url(item['instrument'])
        symbol = instrument_data['symbol']
        fundamental_data = stocks.get_fundamentals(symbol)[0]

        price           = stocks.get_latest_price(instrument_data['symbol'])[0]
        quantity        = item['quantity']
        equity          = float(item['quantity'])*float(price)
        equity_change   = (float(quantity)*float(price))-(float(quantity)*float(item['average_buy_price']))
        percentage      = float(item['quantity'])*float(price)*100/(float(total_equity)-float(cash))
        if (float(item['average_buy_price']) == 0.0):
            percent_change = 0.0
        else:
            percent_change  = (float(price)-float(item['average_buy_price']))*100/float(item['average_buy_price'])

        holdings[symbol]=({'price': price })
        holdings[symbol].update({'quantity': quantity})
        holdings[symbol].update({'average_buy_price': item['average_buy_price']})
        holdings[symbol].update({'equity':"{0:.2f}".format(equity)})
        holdings[symbol].update({'percent_change': "{0:.2f}".format(percent_change)})
        holdings[symbol].update({'equity_change':"{0:2f}".format(equity_change)})
        holdings[symbol].update({'type': instrument_data['type']})
        holdings[symbol].update({'name': stocks.get_name_by_symbol(symbol)})
        holdings[symbol].update({'id': instrument_data['id']})
        holdings[symbol].update({'pe_ratio': fundamental_data['pe_ratio'] })
        holdings[symbol].update({'percentage': "{0:.2f}".format(percentage)})

    return(holdings)

def build_user_profile():
    """Builds a dictionary of important information regarding the user account.

    :returns: Returns a dictionary that has total equity, extended hours equity, cash, and divendend total.

    """
    user = {}

    portfolios_data = profiles.load_portfolio_profile()
    accounts_data = profiles.load_account_profile()

    user['equity'] = portfolios_data['equity']
    user['extended_hours_equity'] = portfolios_data['extended_hours_equity']

    cash = "{0:.2f}".format(float(accounts_data['cash'])+float(accounts_data['uncleared_deposits']))
    user['cash'] = cash

    user['dividend_total'] = get_total_dividends()

    return(user)
