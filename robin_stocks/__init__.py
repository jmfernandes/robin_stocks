########################################
#
# robin-stocks
#
# Description: API library to interact with robinhood API
#
# Author: Josh Fernandes
#
# Created: Feb 20, 2018
#
# Updated:
#
########################################
import requests
import os

class robin_stocks:

    def __init__(self):
        '''
        Summary
        -------
        Initializes the class with session information.

        '''
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
        '''
        Summary
        -------
        Attempts to log in to Robinhood API and store token in session headers.

        Parameters
        ----------
        username : string
            Username for the robinhood account - usually the email address.
        password : string
            Password for the robinhood account.

        Returns
        -------
        dictionary
            Returns a dictionary with key/value pairs pertaining to the login, notably the access token and refresh token

        '''
        payload = {
        'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
        'expires_in': 86400,
        'grant_type': 'password',
        'password': password,
        'scope': 'internal',
        'username': username
        }
        try:
            res_login = self.session.post('https://api.robinhood.com/oauth2/token/', data=payload, timeout=15)
            res_login.raise_for_status()
            login_data = res_login.json()
            self.oauth_token = login_data['access_token']
            self.session.headers['Authorization'] = 'Bearer ' + self.oauth_token
            return login_data
        except requests.exceptions.HTTPError:
            raise

    def logout(self):
        '''
        Summary
        -------
        Deletes stored token from session header.

        '''
        self.session.headers['Authorization'] = None

    def error_argument_not_key_in_dictionary(self,keyword):
        '''
        Summary
        -------
        Returns an error message for a given keyword.

        Parameters
        ----------
        keyword : string
            Represents a keyword that the user was trying to search for.

        Returns
        -------
        string
            Returns an string representing an error message.

        '''
        return('ERROR: The keyword "'+keyword+'" is not a key value in the dictionary.')

    def error_api_endpoint_not_loaded(self,url):
        '''
        Summary
        -------
        Returns an error message for a missing url.

        Parameters
        ----------
        url : string
            Represents a url that the user was trying to search for.

        Returns
        -------
        string
            Returns an string representing an error message.

        '''
        return('ERROR: The url "'+url+'" is either missing (404) or could not be loaded.')

    def error_api_endpoint_not_posted(self,url):
        '''
        Summary
        -------
        Returns an error message for a missing url.

        Parameters
        ----------
        url : string
            Represents a url that the user was trying to search for.

        Returns
        -------
        string
            Returns an string representing an error message.

        '''
        return('ERROR: The POST request to the url "'+url+'" could not be completed.')

    def error_ticker_does_not_exist(self,ticker):
        '''
        Summary
        -------
        Returns an error message for a given ticker.

        Parameters
        ----------
        ticker : string
            Represents a keyword that the user was trying to search for.

        Returns
        -------
        string
            Returns an string representing an error message.

        '''
        return('WARNING: "'+ticker+'" is not a valid stock ticker. It is being ignored')

    def error_not_a_string(self,info):
        '''
        Summary
        -------
        Returns an error message for an input info.

        Parameters
        ----------
        info : string
            Represents a keyword that the user was passing as a parameter.

        Returns
        -------
        String
            Returns an string representing an error message.

        '''
        return('Error: The input parameter "'+str(info)+'" must be a string')

    def error_not_a_integer(self,info):
        '''
        Summary
        -------
        Returns an error message for an input info.

        Parameters
        ----------
        info : string
            Represents a keyword that the user was passing as a parameter.

        Returns
        -------
        String
            Returns an string representing an error message.

        '''
        return('Error: The input parameter "'+str(info)+'" must be an integer')

    def error_must_be_nonzero(self,info):
        '''
        Summary
        -------
        Returns an error message for an input info.

        Parameters
        ----------
        info : string
            Represents a keyword that the user was passing as a parameter.

        Returns
        -------
        String
            Returns an string representing an error message.

        '''
        return('Error: "'+str(info)+'" must be larger than zero and non-negative')

    def inputs_to_set(self,inputsymbols,*othersymbols):
        '''
        Summary
        -------
        Takes any number of string items, makes them all uppercase, and removes all duplicates.

        Parameters
        ----------
        inputsymbols : string
            May be a single string, a list of strings, or a tuple of strings.
        *othersymbols : string
            May be a single string, a list of strings, or a tuple of strings.

        Returns
        -------
        set
            Returns a set of strings that are all uppercase.

        '''
        symbols = set()

        if type(inputsymbols) is str:
            symbols.add(inputsymbols.upper().strip())
        elif type(inputsymbols) is list or type(inputsymbols) is tuple or type(inputsymbols) is set:
            inputsymbols = [comp for comp in inputsymbols if type(comp) is str]
            for item in inputsymbols:
                symbols.add(item.upper().strip())

        for symbol in othersymbols:
            if type(symbol) is str:
                symbols.add(symbol.upper().strip())
            elif type(symbol) is list or type(symbol) is tuple or type(symbol) is set:
                symbol = [comp for comp in symbol if type(comp) is str]
                for item in symbol:
                    symbols.add(item.upper().strip())

        return list(symbols)

    def append_dataset_with_pagination(self,res,data):
        '''
        Summary
        -------
        Takes any number of stock tickers and returns information held by the market such as ticker name, bloomberg id, and listing date.

        Parameters
        ----------
        res : requests.models.Response
            What is returned by session.get(url)
        data : List
            List to be appeneded with new information.

        Returns
        -------
        list
            Contains a list with the value that corresponds to the 'results' keyword. If the 'next' keyword is not none,
            then the results from that page are added to the list.

        '''
        counter = 2
        res_json = res.json()

        if res_json['next']:
            print('Found Additional pages.')
        while res_json['next']:
            print('Loading page '+str(counter)+' ...')
            counter += 1
            res = self.session.get(res_json['next'])
            res_json = res.json()
            for item in res_json['results']:
                data.append(item)

        return(data)

    def get_user_profile(self,*,info=None):
        '''
        Summary
        -------
        Gets the information associated with the user profile, such as username, email, and links to the urls for other profiles.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to return the value for the key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the function returns a dictionary of key/value pairs.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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
        '''
        Summary
        -------
        Gets the information associated with the investment profile. These are the answers to the questionaire you filled out
        when you made your profile.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to return the value for the key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the function returns a dictionary of key/value pairs.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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

    def get_basic_profile(self,*,info=None):
        '''
        Summary
        -------
        Gets the information associated with the personal profile, such as phone number, city, marital status, and date of birth.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to return the value for the key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the function returns a dictionary of key/value pairs.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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

    def get_international_profile(self,*,info=None):
        '''
        Summary
        -------
        [DOES NOT WORK] Gets the information associated with the international profile.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to return the value for the key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the function returns a dictionary of key/value pairs.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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

    def get_employment_profile(self,*,info=None):
        '''
        Summary
        -------
        [DOES NOT WORK]Gets the information associated with the employment profile.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to return the value for the key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the function returns a dictionary of key/value pairs.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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

    def get_portfolios_profile(self,*,info=None):
        '''
        Summary
        -------
        Gets the information associated with the portfolios profile, such as withdrawable amount, market value of account, and excess margin.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to return the value for the key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the function returns a dictionary of key/value pairs.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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

    def get_accounts_profile(self,*,info=None):
        '''
        Summary
        -------
        Gets the information associated with the accounts profile, including day trading information and cash being held by robinhood

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to return the value for the key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the function returns a dictionary of key/value pairs.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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

    def get_security_profile(self,*,info=None):
        '''
        Summary
        -------
        Gets the information associated with the security profile.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to return the value for the key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the function returns a dictionary of key/value pairs.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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
        '''
        Summary
        -------
        Takes any number of stock tickers and returns information pertaining to its price.

        Parameters
        ----------
        inputsymbols : string
            Stock tickers. May be a single ticker or could be a list of tickers.
        *othersymbols : string
            This is a variable length parameter. May be several tickers seperated by commas or a list of tickers.
        info : string, optional
            This is a keyword only parameter. Will filter the results to have a list of the values that correspond to key that matches info.

        Returns
        -------
        List
            If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker.
            Otherwise will be a list of strings where the strings are the values of the key that corresponds to info.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        url = 'https://api.robinhood.com/quotes/?symbols='+','.join(symbols)
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        for count,item in enumerate(res_data['results']):
            if item is None:
                print(self.error_ticker_does_not_exist(symbols[count]))

        res_data = [item for item in res_data['results'] if item is not None]

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_latest_price(self,inputsymbols,*othersymbols):
        '''
        Summary
        -------
        Takes any number of stock tickers and returns the latest price of each one as a string.

        Parameters
        ----------
        inputsymbols : string
            Stock tickers. May be a single ticker or could be a list of tickers.
        *othersymbols : string
            This is a variable length parameter. May be several tickers seperated by commas or a list of tickers.

        Returns
        -------
        List
            Returns a list of strings of the latest price of each ticker.

        '''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        myquote = self.get_quotes(symbols)

        price_list = []
        for item in myquote:
            if item['last_extended_hours_trade_price'] is None:
                price_list.append(item['last_trade_price'])
            else:
                price_list.append(item['last_extended_hours_trade_price'])
        return(price_list)

    def get_fundamentals(self,inputsymbols,*othersymbols, info=None):
        '''
        Summary
        -------
        Takes any number of stock tickers and returns fundamental information about the stock such as what sector it is in,
        a description of the company, dividend yield, and market cap.

        Parameters
        ----------
        inputsymbols : string
            Stock tickers. May be a single ticker or could be a list of tickers.
        *othersymbols : string
            This is a variable length parameter. May be several tickers seperated by commas or a list of tickers.
        info : string, optional
            This is a keyword only parameter. Will filter the results to have a list of the values that correspond to key that matches info.

        Returns
        -------
        List
            If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker.
            Otherwise will be a list of strings where the strings are the values of the key that corresponds to info.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        url = 'https://api.robinhood.com/fundamentals/?symbols='+','.join(symbols)
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        for count,item in enumerate(res_data['results']):
            if item is None:
                print(self.error_ticker_does_not_exist(symbols[count]))

        res_data = [item for item in res_data['results'] if item is not None]

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_instruments_by_symbols(self,inputsymbols,*othersymbols,info=None):
        '''
        Summary
        -------
        Takes any number of stock tickers and returns information held by the market such as ticker name, bloomberg id, and listing date.

        Parameters
        ----------
        inputsymbols : string
            Stock tickers. May be a single ticker or could be a list of tickers.
        *othersymbols : string
            This is a variable length parameter. May be several tickers seperated by commas or a list of tickers.
        info : string, optional
            This is a keyword only parameter. Will filter the results to have a list of the values that correspond to key that matches info.

        Returns
        -------
        List
            If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker.
            Otherwise will be a list of strings where the strings are the values of the key that corresponds to info.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        res_data = []
        for item in symbols:
            url = 'https://api.robinhood.com/instruments/?symbol='+item
            try:
                res = self.session.get(url)
                res.raise_for_status()
                res_data = res.json()['results']
            except:
                print(self.error_api_endpoint_not_loaded(url))
                return([None])

            if len(res_data) == 0:
                print(self.error_ticker_does_not_exist(item))
            else:
                res_data = self.append_dataset_with_pagination(res,res_data)

        if (len(res_data) == 0):
            return([None])

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_instrument_by_url(self,url,*,info=None):
        '''
        Summary
        -------
        Takes a single url for the stock. Should be located at https://api.robinhood.com/instruments/<id> where <id> is the
        id of the stock.

        Parameters
        ----------
        url : string
            Url of the stock.
        info : string, optional
            This is a keyword only parameter. Will filter the results to have a list of the values that correspond to key that matches info.

        Returns
        -------
        dictionary or string
            If info parameter is left as None then the list will contain a dictionary of key/value pairs for the stock.
            Otherwise, the function will return a string corresponding to the value of the key that matches the info parameter.

        '''
        if (type(url) is not str):
            print(self.error_not_a_string(url))
            return(None)
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return(None)

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
        '''
        Summary
        -------
        Will search the stocks for that contain the query keyword and return the instrument data.

        Parameters
        ----------
        query : string,
            This is a keyword only parameter. Will filter the results to have a list of the dictionaries that contain the query keyword.

        Returns
        -------
        List
            Will be a list of dictionaries that contain the instrument data for each stock that matches the query.

        '''
        if (type(query) is not str):
            print(self.error_not_a_string(query))
            return([None])

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
            return([None])
        else:
            print('Found '+str(len(res_data))+' results')
            return(res_data)

    def get_positions(self,*,info=None):
        '''
        Summary
        -------
        Will return a list containing every position ever traded.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to have a list of the values that correspond to key that matches info.

        Returns
        -------
        List
            If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker.
            Otherwise will be a list of strings where the strings are the values of the key that corresponds to info.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

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
        '''
        Summary
        -------
        Same as get_positions() but will only return stocks/options that are currently held.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to have a list of the values that correspond to key that matches info.

        Returns
        -------
        List
            If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker.
            Otherwise will be a list of strings where the strings are the values of the key that corresponds to info.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

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

    def get_dividends(self,*,info=None):
        '''
        Summary
        -------
        Returns a list of dividend trasactions that include information such as the percentage rate, amount, shares of held stock,
        and date paid.

        Parameters
        ----------
        info : string, optional
            This is a keyword only parameter. Will filter the results to have a list of the values that correspond to key that matches info.

        Returns
        -------
        List
            If info parameter is left as None then the list will contain a dictionary of key/value pairs for each ticker.
            Otherwise will be a list of strings where the strings are the values of the key that corresponds to info.

        '''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

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
        '''
        Summary
        -------
        Returns a double number representing the total amount of dividends paid to the account.

        Returns
        -------
        Float
            Total dollar amount of dividends paid to the account as a 2 precision float.

        '''
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
        '''
        Summary
        -------
        Returns the name of a stock if given the symbol.

        Parameters
        ----------
        symbol : string
            The ticker of the stock as a string.

        Returns
        -------
        String
            Returns the simple name of the stock. If the simple name does not exist then returns the full name.

        '''
        if (type(symbol) is not str):
            print(self.error_not_a_string(symbol))
            return(None)

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
        '''
        Summary
        -------
        Returns the name of a stock if given the instrument url.

        Parameters
        ----------
        url : string
            The url of the stock as a string.

        Returns
        -------
        String
            Returns the simple name of the stock. If the simple name does not exist then returns the full name.

        '''
        if (type(url) is not str):
            print(self.error_not_a_string(url))
            return(None)

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
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

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
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

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
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

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

    def post_symbols_to_watchlist(self,inputsymbols,*othersymbols,name='Default'):
        '''Post multiple symbols to your watchlist'''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        data = {
        'symbols': ','.join(symbols)
        }
        url = 'https://api.robinhood.com/watchlists/'+name+'/bulk_add/'
        try:
            res = self.session.post(url,data=data)
            res.raise_for_status()
        except:
            raise

        return(res)

    def delete_symbols_from_watchlist(self,inputsymbols,*othersymbols,name='Default'):
        '''Delete multiple symbols from your watchlist'''
        symbols = self.inputs_to_set(inputsymbols,*othersymbols)
        symbols = self.get_fundamentals(symbols,info='instrument')

        watchlist = self.get_watchlist_by_name(name=name)

        data = []

        for symbol in symbols:
            for list_ in watchlist:
                if symbol == list_['instrument']:
                    data.append(symbol[37:])

        for item in data:
            url = 'https://api.robinhood.com/watchlists/'+name+item
            try:
                res = self.session.delete(url)
                res.raise_for_status()
            except:
                raise

        return(res)

    def get_notifications(self,*,info=None):
        '''Get notifications'''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

        url = 'https://api.robinhood.com/notifications/devices/'
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

    def get_markets(self,*,info=None):
        '''Get markets'''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

        url = 'https://api.robinhood.com/markets/'
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

    def get_wire_transfers(self,*,info=None):
        '''Get wire transfers'''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

        url = 'https://api.robinhood.com/wire/transfers'
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

    def get_all_orders(self,*,info=None):
        '''Returns all orders'''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

        url = 'https://api.robinhood.com/orders/'
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

    def get_all_open_orders(self,*,info=None):
        '''Returns all orders'''
        if (type(info) is not str and info is not None):
            print(self.error_not_a_string(info))
            return([None])

        url = 'https://api.robinhood.com/orders/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        res_data = [item for item in res_data if item['cancel'] is not None]

        if info and info in res_data[0]:
            return([item[info]for item in res_data])
        elif info and info not in res_data[0]:
            print(self.error_argument_not_key_in_dictionary(info))
            return([None])
        else:
            return(res_data)

    def get_order_info(self,*,order_id):
        '''Get order information'''
        if (type(order_id) is not str):
            print(self.error_not_a_string(order_id))
            return([None])

        url = 'https://api.robinhood.com/orders/'+order_id+'/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        return(res_data)

    def query_orders(self,**arguments):
        '''Find all orders that meet keyword parameters. EX. find_orders(symbol='FB',cancel='none',quantity=1)'''
        url = 'https://api.robinhood.com/orders/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return([None])

        res_data = self.append_dataset_with_pagination(res,res_data)

        for item in res_data:
            item['quantity'] = str(int(float(item['quantity'])))

        if 'symbol' in arguments.keys():
            arguments['instrument'] = self.get_instruments_by_symbols(arguments['symbol'],info='url')[0]
            del arguments['symbol']

        if 'quantity' in arguments.keys():
            arguments['quantity'] = str(arguments['quantity'])

        stop = len(arguments.keys())-1
        list_of_orders=[]
        for item in res_data:
            for i,(key,value) in enumerate(arguments.items()):
                if key not in item:
                    print(self.error_argument_not_key_in_dictionary(key))
                    return([None])
                if value != item[key]:
                    break
                if i == stop:
                    list_of_orders.append(item)

        return(list_of_orders)

    def cancel_all_open_orders(self):
        '''Cancels all open orders'''
        url = 'https://api.robinhood.com/orders/'
        try:
            res = self.session.get(url)
            res.raise_for_status()
            res_data = res.json()['results']
        except:
            print(self.error_api_endpoint_not_loaded(url))
            return(None)

        res_data = self.append_dataset_with_pagination(res,res_data)

        res_data = [item['id'] for item in res_data if item['cancel'] is not None]

        for item in res_data:
            cancel_url = 'https://api.robinhood.com/orders/'+item+'/cancel/'
            try:
                res = self.session.post(cancel_url)
                res.raise_for_status()
                res_data = res.json()
            except:
                print(self.error_api_endpoint_not_posted(cancel_url))
                return(None)

        print('All Orders Cancelled')
        return(None)

    def cancel_order(self,*,order_id):
        '''Cancel an order'''
        if (type(order_id) is not str):
            print(self.error_not_a_string(order_id))
            return([None])

        url = 'https://api.robinhood.com/orders/'+order_id+'/cancel/'
        try:
            res = self.session.post(url)
            res.raise_for_status()
            res_data = res.json()
        except:
            print(self.error_api_endpoint_not_posted(url) + ' \nOrder may not be open, or order_id may be wrong')
            return(None)

        print('Order '+order_id+' cancelled')
        return(None)

    def order_buy_market(self,*,symbol,quantity,time_in_force='gtc'):
        '''
        Summary
        -------
        Buys a certain quantity of a stock.

        Parameters
        ----------
        symbol : string
            The symbol of the stock as a string.
        quantity : int
            The amount to buy of the stock as an integer.
        time_in_force : string, optional
            This is a keyword only parameter. Changes how long the order will be in effect forself. 'gtc' = good until cancelled.
            'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.

        Returns
        -------
        Dictionary
            Contains information regarding the purchase of stocks, such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.),
            the price, and the quantity.

        '''
        if (type(symbol) is not str):
            print(self.error_not_a_string(order_id))
            return(None)

        if (type(time_in_force) is not str):
            print(self.error_not_a_string(order_id))
            return(None)

        if (type(quantity) is not int):
            print(self.error_not_a_integer(quantity))
            return(None)
        elif (quantity < 1):
            print(self.error_must_be_nonzero('quantity'))
            return(None)

        symbol = symbol.upper()

        data = {
        'account': self.get_accounts_profile(info='url'),
        'instrument': self.get_instruments_by_symbols(symbol,info='url')[0],
        'symbol': symbol,
        'price': float(self.get_latest_price(symbol)[0]),
        'quantity': quantity,
        'type': 'market',
        'stop_price': None,
        'time_in_force': time_in_force,
        'trigger': 'immediate',
        'side': 'buy'
        }

        url = "https://api.robinhood.com/orders/"
        res_json = None
        try:
            res = self.session.post(url,data=data)
            res.raise_for_status()
            res_json = res.json()
        except:
            raise

        return(res_json)

    def order_sell_market(self,*,symbol,quantity,time_in_force='gtc'):
        '''
        Summary
        -------
        Sells a certain quantity of a stock.

        Parameters
        ----------
        symbol : string
            The symbol of the stock as a string.
        quantity : int
            The amount to sell of the stock as an integer.
        time_in_force : string, optional
            This is a keyword only parameter. Changes how long the order will be in effect forself. 'gtc' = good until cancelled.
            'gfd' = good for the day. 'ioc' = immediate or cancel. 'opg' execute at opening.

        Returns
        -------
        Dictionary
            Contains information regarding the selling of stocks, such as the order id, the state of order (queued,confired,filled, failed, canceled, etc.),
            the price, and the quantity.

        '''
        if (type(symbol) is not str):
            print(self.error_not_a_string(order_id))
            return(None)

        if (type(time_in_force) is not str):
            print(self.error_not_a_string(order_id))
            return(None)

        if (type(quantity) is not int):
            print(self.error_not_a_integer(quantity))
            return(None)
        elif (quantity < 1):
            print(self.error_must_be_nonzero('quantity'))
            return(None)

        symbol = symbol.upper()

        data = {
        'account': self.get_accounts_profile(info='url'),
        'instrument': self.get_instruments_by_symbols(symbol,info='url')[0],
        'symbol': symbol,
        'price': float(self.get_latest_price(symbol)[0]),
        'quantity': quantity,
        'type': 'market',
        'stop_price': None,
        'time_in_force': time_in_force,
        'trigger': 'immediate',
        'side': 'sell'
        }

        url = "https://api.robinhood.com/orders/"
        res_json = None
        try:
            res = self.session.post(url,data=data)
            res.raise_for_status()
            res_json = res.json()
        except:
            raise

        return(res_json)

    def build_holdings(self):
        holdings = {}
        positions_data = self.get_owned_positions()
        portfolios_data = self.get_portfolios_profile()
        accounts_data = self.get_accounts_profile()

        if portfolios_data['extended_hours_equity'] is not None:
            total_equity = max(float(portfolios_data['equity']),float(portfolios_data['extended_hours_equity']))
        else:
            total_equity = float(portfolios_data['equity'])

        cash = "{0:.2f}".format(float(accounts_data['cash'])+float(accounts_data['uncleared_deposits']))

        for item in positions_data:
            instrument_data = self.get_instrument_by_url(item['instrument'])
            symbol = instrument_data['symbol']
            fundamental_data = self.get_fundamentals(symbol)[0]
            #
            price           = self.get_latest_price(instrument_data['symbol'])[0]
            quantity        = item['quantity']
            equity          = float(item['quantity'])*float(price)
            equity_change   = (float(quantity)*float(price))-(float(quantity)*float(item['average_buy_price']))
            percentage      = float(item['quantity'])*float(price)*100/(float(total_equity)-float(cash))
            if (float(item['average_buy_price']) == 0.0):
                percent_change = 0.0
            else:
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

        portfolios_data = self.get_portfolios_profile()
        accounts_data = self.get_accounts_profile()

        user['equity'] = portfolios_data['equity']
        user['extended_hours_equity'] = portfolios_data['extended_hours_equity']

        cash = "{0:.2f}".format(float(accounts_data['cash'])+float(accounts_data['uncleared_deposits']))
        user['cash'] = cash

        user['dividend_total'] = self.get_total_dividends()

        return(user)
