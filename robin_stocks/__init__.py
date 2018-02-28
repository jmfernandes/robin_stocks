import requests
import os

class robin_stocks:

    def __init__(self):
        '''Initialize class with a session'''
        self.session = requests.Session()
        self.session.headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,defalte",
        "Accept-Language": "en;q=1",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "X-Robinhood-API-Version": "1.0.0",
        "Connection": "keep-alive",
        "User-Agent": "Robinhood/823 (iphone; iOS 7.1.2, Scale/2.00)"
        }


    def login(self,username,password):
        '''Attemps to log in to Robinhood API and store token in seesion header'''
        data = {
        'username': username,
        'password': password
        }
        try:
            res_login = self.session.post('https://api.robinhood.com/api-token-auth/',data=data)
            res_login.raise_for_status()
            login_data = res_login.json()
            self.session.headers['Authorization'] = 'Token ' + login_data['token']
            return res_login
        except requests.exceptions.HTTPError:
            raise

    def logout(self):
        '''Attempts to log out of Loginhood API'''
        try:
            res_logout = self.session.post('https://api.robinhood.com/api-token-logout/')
            res_logout.raise_for_status()
        except requests.exceptions.HTTPError as err_msg:
            raise

        self.session.headers['Authorization'] = None

        return res_logout

    def error_argument_not_key_in_dictionary(self,keyword):
        '''Returns an error message when called'''
        return('ERROR: The keyword "'+keyword+'" is not a key value in the dictionary.')

    def error_api_endpoint_not_loaded(self,url):
        '''Returns an error message when called'''
        return('ERROR: The url "'+url+'" is either missing (404) or could not be loaded.')

    def inputs_to_set(self,inputsymbols,*othersymbols):
        '''Takes any number of strings,lists of strings, or tuples of strings and makes a single set'''
        symbols = set()
        if isinstance(inputsymbols,str):
            symbols.add(inputsymbols.upper().strip())
        else:
            for item in inputsymbols:
                symbols.add(item.upper().strip())

        for item in othersymbols:
            if type(item) is list or type(item) is tuple:
                for subitem in item:
                    symbols.add(subitem.upper().strip())
            else:
                symbols.add(item.upper().strip())
        return symbols

    def append_dataset_with_pagination(self,res,res_data):

        counter = 2
        if res.json()['next']:
            print('Found Additional pages.')
        while res.json()['next']:
            print('Loading page '+str(counter)+' ...')
            counter += 1
            res = self.session.get(res.json()['next'])
            for item in res.json()['results']:
                res_data.append(item)

        return(res_data)


    def get_user_profile(self,*,info=None):
        '''Get user account information'''
        url = 'https://api.robinhood.com/user/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def get_investment_profile(self,*,info=None):
        '''Gets investment profile information'''
        url = 'https://api.robinhood.com/user/investment_profile/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def get_basic_info(self,*,info=None):
        '''Gets basic profile information'''
        url = 'https://api.robinhood.com/user/basic_info/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def get_international_info(self,*,info=None):
        '''Gets international profile information'''
        url = 'https://api.robinhood.com/user/international_info/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def get_employment_info(self,*,info=None):
        '''Gets employment profile information'''
        url = 'https://api.robinhood.com/user/employment_info/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def get_additional_info(self,*,info=None):
        '''Gets additional profile information'''
        url = 'https://api.robinhood.com/user/additional_info/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def get_quotes(self,inputsymbols,*othersymbols, info=None):
        '''Takes any number of strings,lists of strings, or tuples of strings and gets stock quote data'''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        url = 'https://api.robinhood.com/quotes/?symbols='+','.join(symbols)
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        if None in res_data['results']:
            print('WARING: SOME TICKERS WERE WRONG. THEY ARE BEING IGNORED')

        res_data = [item for item in res_data['results'] if item is not None]

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_latest_price(self,inputsymbols,*othersymbols):
        '''Gets either the after hours price or the last trading price'''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        myquote = self.get_quotes(symbols)

        price_list = []
        for item in myquote:
            if item['last_extended_hours_trade_price'] is None:
                price_list.append(item['last_trade_price'])
            else:
                price_list.append(item['last_extended_hours_trade_price'])
        return(price_list)

    def get_instruments_by_symbols(self,inputsymbols,*othersymbols,info=None):
        '''Takes any number of strings,lists of strings, or tuples of strings and gets stock instrument data'''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        res_data = []
        for item in symbols:
            url = 'https://api.robinhood.com/instruments/?symbol='+item
            try:
                res = self.session.get(url)
                res.raise_for_status()
                res_other = res.json()
            except:
                print(self.error_api_endpoint_not_loaded(url))
                return([None])

            res_data = self.append_dataset_with_pagination(res,res_data)

            if len(res_other['results']) == 0:
                print('WARING: SOME TICKERS WERE WRONG. THEY ARE BEING IGNORED')
            else:
                res_data.append(res_other['results'][0])

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_instruments_by_url(self,url,*,info=None):
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def query_instruments(self,*,query):
        '''Will search all stocks for a certain query keyword'''
        url = 'https://api.robinhood.com/instruments/?query='+query
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        if len(res_data) == 0:
            print('No results found for that keyword')
            return([])
        else:
            print('Found '+str(len(res_data))+' results')
            return(res_data)

    def get_positions(self,*,info=None):
        '''Get all poistions ever held'''
        url = 'https://api.robinhood.com/positions/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_owned_positions(self,*,info=None):
        '''Get all positions currently held'''
        url = 'https://api.robinhood.com/positions/?nonzero=true'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_portfolios(self,*,info=None):
        '''Get user portfolio'''
        url = 'https://api.robinhood.com/portfolios/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results'][0]
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def get_accounts(self,*,info=None):
        '''Get user account'''
        url = 'https://api.robinhood.com/accounts/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results'][0]
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if info and info in res_data:
            return(res_data[info])
        elif info and info not in res_data:
            print(self.error_argument_not_key_in_dictionary(info))
            return(None)
        else:
            return(res_data)

    def get_fundamentals(self,inputsymbols,*othersymbols, info=None):
        '''Takes any number of strings,lists of strings, or tuples of strings and gets stock fundamental data'''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        url = 'https://api.robinhood.com/fundamentals/?symbols='+','.join(symbols)
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        if None in res_data['results']:
            print('WARING: SOME TICKERS WERE WRONG. THEY ARE BEING IGNORED')

        res_data = [item for item in res_data['results'] if item is not None]

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_dividends(self,*,info=None):
        '''Returns list of dividend transactions'''
        url = 'https://api.robinhood.com/dividends/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_total_dividends(self):
        '''Returns 2 percision float of total divident amount'''
        url = 'https://api.robinhood.com/dividends/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        res_data = self.append_dataset_with_pagination(res,res_data)

        dividend_total = 0
        for item in res_data:
            dividend_total += float(item['amount'])
        return("{0:.2f}".format(dividend_total))

    def get_name_by_symbol(self,symbol):
        '''Returns the name of a stock if given the stock symbol'''
        url = 'https://api.robinhood.com/instruments/?symbol='+symbol
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results'][0]
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if not res_data['simple_name']:
            name_data = res_data['name']
        else:
            name_data = res_data['simple_name']

        return(name_data)

    def get_name_by_url(self,url):
        '''Returns the name of a stock if given the instrument url'''
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        if not res_data['simple_name']:
            name_data = res_data['name']
        else:
            name_data = res_data['simple_name']

        return(name_data)

    def get_documents(self,*,info=None):
        '''Returns list of Document transactions'''
        url = 'https://api.robinhood.com/documents/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def download_document(self,*,url,name=None,dirpath=None):
        '''Downloads a document and saves as a PDF when given download URL. Must
           choose a name and may choose a directory to save it in - otherwise
           it saves in the root directory of code.'''
        try:
            res_data = self.session.get(url)
            res_data.raise_for_status()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        print('Writing PDF...')
        if not name:
            name = url[36:].split('/',1)[0]
        if dirpath:
            directory = dirpath
        else:
            directory = 'robin_documents/'
        filename = directory+name+'.pdf'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        open(filename, 'wb').write(res_data.content)
        print('Done - Wrote file '+name+'.pdf'+' to '+os.path.abspath(filename))

        return(None)

    def download_all_documents(self,*,doctype=None,dirpath=None):
        '''Download all documents or all documents of a cetain doctype i.e. account_statement'''
        documents = self.get_documents()

        downloaded_files = False
        print('Writing PDF...')
        if dirpath:
            directory = dirpath
        else:
            directory = 'robin_documents/'
        counter = 0
        for item in documents:
            if doctype == None:
                res_data = self.session.get(item['download_url'])
                name = item['created_at'][0:10]+'-'+item['type']+'-'+item['id']
                filename = directory+name+'.pdf'
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                open(filename, 'wb').write(res_data.content)
                downloaded_files = True
                counter += 1
            else:
                if item['type'] == doctype:
                    res_data = self.session.get(item['download_url'])
                    name = item['created_at'][0:10]+'-'+item['type']+'-'+item['id']
                    filename = directory+name+'.pdf'
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    open(filename, 'wb').write(res_data.content)
                    downloaded_files = True
                    counter += 1

        if downloaded_files == False:
            print('WARNING: Could not find files of that doctype to download')
        else:
            if counter == 1:
                print('Done - wrote '+str(counter)+' file to '+os.path.abspath(directory))
            else:
                print('Done - wrote '+str(counter)+' files to '+os.path.abspath(directory))

        return(None)

    def get_historicals(self,inputsymbols,*othersymbols,span='week',bounds='regular'):
        span_check = ['day','week','year','5year']
        bounds_check =['extended','regular','trading']
        if span not in span_check:
            print('ERROR: Span must be "day","week","year",or "5year"')
            return([None])
        if bounds not in bounds_check:
            print('ERROR: Bounds must be "extended","regular",or "trading"')
            return([None])
        if (bounds == 'extended' or bounds == 'trading') and span != 'day':
            print('ERROR: extended and trading bounds can only be used with a span of "day"')
            return([None])

        if span=='day':
            interval = '5minute'
        elif span=='week':
            interval = '10minute'
        elif span=='year':
            interval = 'day'
        else:
            interval = 'week'

        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        symbols = ','.join(symbols)

        url = 'https://api.robinhood.com/quotes/historicals/'+ \
               '?symbols='+symbols+'&interval='+interval+'&span='+span+'&bounds='+bounds

        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        check = [item for item in res_data if len(item['historicals']) is 0]
        if (len(check) != 0):
            print('WARING: SOME TICKERS WERE WRONG. THEY ARE BEING IGNORED')

        res_data = [item['historicals'] for item in res_data if len(item['historicals']) is not 0]

        return(res_data)

    def get_all_watchlists(self,*,info=None):
        '''Get a list of all watchlists'''
        url = 'https://api.robinhood.com/watchlists/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_watchlist_by_name(self,*,name='Default',info=None):
        '''Get the list of all stocks in a single watchlist'''
        url = 'https://api.robinhood.com/watchlists/'+name+'/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def build_holdings(self):
        holdings = {}
        positions_data = self.get_owned_positions()
        portfolios_data = self.get_portfolios()
        accounts_data = self.get_accounts()

        if portfolios_data['extended_hours_equity'] is not None:
            total_equity = max(float(portfolios_data['equity']),float(portfolios_data['extended_hours_equity']))
        else:
            total_equity = float(portfolios_data['equity'])

        cash = "{0:.2f}".format(float(accounts_data['cash'])+float(accounts_data['uncleared_deposits']))

        for item in positions_data:
            instrument_data = self.get_instruments_by_url(item['instrument'])
            symbol = instrument_data['symbol']
            fundamental_data = self.get_fundamentals(symbol, info=None)[0]
            #
            price           = self.get_latest_price(instrument_data['symbol'])[0]
            quantity        = item['quantity']
            equity          = float(item['quantity'])*float(price)
            equity_change   = (float(quantity)*float(price))-(float(quantity)*float(item['average_buy_price']))
            percentage      = float(item['quantity'])*float(price)*100/(float(total_equity)-float(cash))
            percent_change  = (float(price)-float(item['average_buy_price']))*100/float(item['average_buy_price'])
            #
            holdings[symbol]=({'price': price })
            holdings[symbol].update({'quantity': quantity})
            holdings[symbol].update({'average_buy_price': item['average_buy_price']})
            holdings[symbol].update({'equity':"{0:.2f}".format(equity)})
            holdings[symbol].update({'percent_change': "{0:.2f}".format(percent_change)})
            holdings[symbol].update({'equity_change':"{0:2f}".format(equity_change)})
            holdings[symbol].update({'type': instrument_data['type']})
            holdings[symbol].update({'name': self.get_name_by_symbol(symbol)})
            holdings[symbol].update({'id': instrument_data['id']})
            holdings[symbol].update({'pe_ratio': fundamental_data['pe_ratio'] })
            holdings[symbol].update({'percentage': "{0:.2f}".format(percentage)})

        return(holdings)

    def build_user_profile(self):
        user = {}

        portfolios_data = self.get_portfolios()
        accounts_data = self.get_accounts()

        user['equity'] = portfolios_data['equity']
        user['extended_hours_equity'] = portfolios_data['extended_hours_equity']

        cash = "{0:.2f}".format(float(accounts_data['cash'])+float(accounts_data['uncleared_deposits']))
        user['cash'] = cash

        user['dividend_total'] = self.get_total_dividends()

        return(user)
