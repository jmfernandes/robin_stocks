import requests

class robin_stocks:

    def __init__(self):
        '''Initialize with a session'''
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
        '''Attemps to log in to Robinhood API'''
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
            print('Failed to log out ' + repr(err_msg))
            return None

        self.session.headers['Authorization'] = None

        return res_logout

    def error_keyword(self,keyword):
        return('ERROR: The keyword "'+keyword+'" is not a parameter in the dataset')

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

    def get_user_profile(self,*,info=None):
        '''Get user account information'''
        try:
            res = self.session.get('https://api.robinhood.com/user/')
            res.raise_for_status()
            res_data = res.json()
        except:
            print('Investment profile could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def get_investment_profile(self,*,info=None):
        '''Gets investment profile information'''
        try:
            res = self.session.get('https://api.robinhood.com/user/investment_profile/')
            res.raise_for_status()
            res_data = res.json()
        except:
            print('Investment profile could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def get_basic_info(self,*,info=None):
        '''Gets basic profile information'''
        try:
            res = self.session.get('https://api.robinhood.com/user/basic_info/')
            res.raise_for_status()
            res_data = res.json()
        except:
            print('Basic profile could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def get_international_info(self,*,info=None):
        '''Gets international profile information'''
        try:
            res = self.session.get('https://api.robinhood.com/user/international_info/')
            res.raise_for_status()
            res_data = res.json()
        except:
            print('International profile could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def get_employment_info(self,*,info=None):
        '''Gets employment profile information'''
        try:
            res = self.session.get('https://api.robinhood.com/user/employment_info/')
            res.raise_for_status()
            res_data = res.json()
        except:
            print('Employment profile could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def get_additional_info(self,*,info=None):
        '''Gets additional profile information'''
        try:
            res = self.session.get('https://api.robinhood.com/user/additional_info/')
            res.raise_for_status()
            res_data = res.json()
        except:
            print('Additional profile could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def get_quotes(self,inputsymbols,*othersymbols, info=None):
        '''Takes any number of strings,lists of strings, or tuples of strings and gets stock quote data'''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)

        try:
            res_url = 'https://api.robinhood.com/quotes/?symbols='+','.join(symbols)
            res = self.session.get(res_url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print('Quotes could not be loaded')
            return None

        if None in res_data['results']:
            print('WARING: SOME TICKERS WERE WRONG. THEY ARE BEING IGNORED')

        res_data = [x for x in res_data['results'] if x is not None]

        if info:
            give_data = []
            if info not in res_data[0]:
                print(self.error_keyword(info))
                return([None])
            for value in res_data:
                give_data.append(value[info])
            return(give_data)
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
            try:
                res = self.session.get('https://api.robinhood.com/instruments/?symbol='+item)
                res.raise_for_status()
                res_other = res.json()
            except:
                print('Instrument data could not be loaded')
                return None

            if len(res_other['results']) == 0:
                print('WARING: SOME TICKERS WERE WRONG. THEY ARE BEING IGNORED')
            else:
                res_data.append(res_other['results'][0])

        if info:
            give_data = []
            if info not in res_data[0]:
                print(self.error_keyword(info))
                return([None])
            for value in res_data:
                give_data.append(value[info])
            return(give_data)
        else:
            return(res_data)

    def get_instruments_by_url(self,url,*,info=None):
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print('Instrument data could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def query_instruments(self,*,query):
        '''Will search all stocks for a certain query keyword'''
        try:
            res = self.session.get('https://api.robinhood.com/instruments/?query='+query)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print('Query could not be completed')
            return None

        if len(res_data) == 0:
            print('No results found for that keyword')
            return([])
        else:
            print('Found '+str(len(res_data))+' results')
            return(res_data)

    def get_positions(self,*,info=None):
        '''Get all poistions ever held'''
        try:
            res = self.session.get('https://api.robinhood.com/positions/')
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print('Positions could not be loaded')
            return None

        if info:
            give_data = []
            if info not in res_data[0]:
                print(self.error_keyword(info))
                return([None])
            for value in res_data:
                give_data.append(value[info])
            return(give_data)
        else:
            return(res_data)

    def get_owned_positions(self,*,info=None):
        '''Get all positions currently held'''
        try:
            res = self.session.get('https://api.robinhood.com/positions/?nonzero=true')
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print('Positions could not be loaded')
            return None

        if info:
            give_data = []
            if info not in res_data[0]:
                print(self.error_keyword(info))
                return([None])
            for value in res_data:
                give_data.append(value[info])
            return(give_data)
        else:
            return(res_data)

    def get_portfolios(self,*,info=None):
        '''Get user portfolio'''
        try:
            res = self.session.get('https://api.robinhood.com/portfolios/')
            res.raise_for_status()
            res_data = res.json()['results'][0]
        except:
            print('Portfolio profile could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def get_accounts(self,*,info=None):
        '''Get user account'''
        try:
            res = self.session.get('https://api.robinhood.com/accounts/')
            res.raise_for_status()
            res_data = res.json()['results'][0]
        except:
            print('Account could not be loaded')
            return None

        if info:
            if info in res_data:
                return(res_data[info])
            else:
                print(self.error_keyword(info))
                return(None)
        else:
            return(res_data)

    def get_fundamentals(self,inputsymbols,*othersymbols, info=None):
        '''Takes any number of strings,lists of strings, or tuples of strings and gets stock fundamental data'''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)

        try:
            res_url = 'https://api.robinhood.com/fundamentals/?symbols='+','.join(symbols)
            res = self.session.get(res_url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print('Fundamentals could not be loaded')
            return None

        if None in res_data['results']:
            print('WARING: SOME TICKERS WERE WRONG. THEY ARE BEING IGNORED')

        res_data = [x for x in res_data['results'] if x is not None]

        if info:
            give_data = []
            if info not in res_data[0]:
                print(self.error_keyword(info))
                return([None])
            for value in res_data:
                give_data.append(value[info])
            return(give_data)
        else:
            return(res_data)

    def get_dividends(self,*,info=None):
        '''Returns list of dividend transactions'''
        try:
            res = self.session.get('https://api.robinhood.com/dividends/')
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print('Dividends could not be loaded')
            return None

        if info:
            give_data = []
            assert info in res_data[0], self.error_keyword(info)
            for value in res_data:
                give_data.append(value[info])
            return(give_data)
        else:
            return(res_data)

    def get_total_dividends(self):
        '''Returns 2 percision float of total divident amount'''
        try:
            res = self.session.get('https://api.robinhood.com/dividends/')
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print('Dividends could not be loaded')
            return None

        dividend_total = 0
        for item in res_data:
            dividend_total += float(item['amount'])
        return("{0:.2f}".format(dividend_total))

    def get_name_by_symbol(self,symbol):
        '''Returns the name of a stock if given the stock symbol'''
        res_url = 'https://api.robinhood.com/instruments/?symbol='+symbol

        try:
            res = self.session.get(res_url)
            res.raise_for_status()
            res_data = res.json()['results'][0]
        except:
            print('Name from Instruments could not be loaded')
            return None

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
            print('Name from Instruments could not be loaded')
            return None

        if not res_data['simple_name']:
            name_data = res_data['name']
        else:
            name_data = res_data['simple_name']

        return(name_data)


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
