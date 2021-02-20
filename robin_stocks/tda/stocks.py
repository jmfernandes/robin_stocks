from robin_stocks.tda.helper import format_inputs, login_required, request_get
from robin_stocks.tda.urls import URLS


@login_required
@format_inputs
def get_quote(ticker, jsonify=None):
    """ Gets quote information for a single stock.

    :param ticker: The ticker of the stock.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.quote(ticker)
    data, error = request_get(url, None, jsonify)
    return data, error


@login_required
@format_inputs
def get_quotes(tickers, jsonify=None):
    """ Gets quote information for multiple stocks. The stock string should be comma separated with no spaces.

    :param ticker: The string list of stock tickers.
    :type ticker: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.quotes()
    payload = {
        "symbol": tickers
    }
    data, error = request_get(url, payload, jsonify)
    return data, error


@login_required
@format_inputs
def get_price_history(ticker, period_type, frequency_type, frequency,
                      period=None, start_date=None, end_date=None, needExtendedHoursData=True, jsonify=None):
    """ Gets the price history of a stock.

    :param ticker: The stock ticker.
    :type ticker: str
    :param period_type: The type of period to show. Valid values are day, month, year, or ytd (year to date). Default is day.
    :type period_type: str
    :param frequency_type: The type of frequency with which a new candle is formed. \
        Valid frequencyTypes by period_type (defaults marked with an asterisk):\n
        * day: minute*
        * month: daily, weekly* 
        * year: daily, weekly, monthly* 
        * ytd: daily, weekly*
    :type frequency_type: str
    :param frequency: The number of the frequencyType to be included in each candle. \
        Valid frequencies by frequencyType (defaults marked with an asterisk):\n
        * minute: 1*, 5, 10, 15, 30
        * daily: 1*
        * weekly: 1*
        * monthly: 1*
    :type frequency: str
    :param period: The number of periods to show. Valid periods by periodType (defaults marked with an asterisk):\n
        * day: 1, 2, 3, 4, 5, 10*
        * month: 1*, 2, 3, 6
        * year: 1*, 2, 3, 5, 10, 15, 20
        * ytd: 1*
    :type period: Optional[str]
    :param start_date: Start date as milliseconds since epoch. If startDate and endDate are provided, period should not be provided.
    :type start_date: Optional[str]
    :param end_date: End date as milliseconds since epoch. If startDate and endDate are provided, period should not be provided. Default is previous trading day.
    :type end_date: Optional[str]
    :param needExtendedHoursData: true to return extended hours data, false for regular market hours only. Default is true.
    :type needExtendedHoursData: Optional[str]
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    if (start_date or end_date) and period:
        raise ValueError(
            "If start_date and end_date are provided, period should not be provided.")
    url = URLS.price_history(ticker)
    payload = {
        "periodType": period_type,
        "frequencyType": frequency_type,
        "frequency": frequency,
        "needExtendedHoursData": needExtendedHoursData
    }
    if period:
        payload["period"] = period
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date
    data, error = request_get(url, payload, jsonify)
    return data, error


@login_required
@format_inputs
def search_instruments(ticker_string, projection, jsonify=None):
    """ Gets a list of all the instruments data for tickers that match a search string.

    :param ticker_string: Value to pass to the search. See projection description for more information.
    :type ticker_string: str
    :param projection: The type of request:\n
        * symbol-search: Retrieve instrument data of a specific symbol or cusip
        * symbol-regex: Retrieve instrument data for all symbols matching regex. Example: symbol=XYZ.* will return all symbols beginning with XYZ
        * desc-search: Retrieve instrument data for instruments whose description contains the word supplied. Example: symbol=FakeCompany will return all instruments with FakeCompany in the description.
        * desc-regex: Search description with full regex support. Example: symbol=XYZ.[A-C] returns all instruments whose descriptions contain a word beginning with XYZ followed by a character A through C.
        * fundamental: Returns fundamental data for a single instrument specified by exact symbol.
    :type projection: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.instruments()
    payload = {
        "symbol": ticker_string,
        "projection": projection
    }
    data, error = request_get(url, payload, jsonify)
    return data, error


@login_required
@format_inputs
def get_instrument(cusip, jsonify=None):
    """ Gets instrument data for a specific stock.

    :param cusip: The CUSIP for a stock.
    :type cusip: str
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.instrument(cusip)
    data, error = request_get(url, None, jsonify)
    return data, error


@login_required
@format_inputs
def get_option_chains(ticker, contract_type="ALL", strike_count="10", include_quotes="FALSE", strategy="SINGLE", interval=None, strike_price=None,
                      range_value="ALL", from_date=None, to_date=None, volatility=None, underlying_price=None, interest_rate=None, 
                      days_to_expiration=None, exp_month="ALL", option_type="ALL", jsonify=None):
    """ Gets instrument data for a specific stock.

    :param ticker: The stock ticker.
    :type ticker: str
    :param contract_type: Type of contracts to return in the chain. Can be CALL, PUT, or ALL. Default is ALL.
    :type contract_type: Optional[str]
    :param strike_count: The number of strikes to return above and below the at-the-money price.
    :type strike_count: Optional[str]
    :param include_quotes: Include quotes for options in the option chain. Can be TRUE or FALSE. Default is FALSE.
    :type include_quotes: Optional[str]
    :param strategy: Passing a value returns a Strategy Chain. Possible values are SINGLE, ANALYTICAL (allows use of the volatility, \
        underlyingPrice, interestRate, and daysToExpiration params to calculate theoretical values), COVERED, VERTICAL, CALENDAR, \
        STRANGLE, STRADDLE, BUTTERFLY, CONDOR, DIAGONAL, COLLAR, or ROLL. Default is SINGLE.
    :type strategy: Optional[str]
    :param interval: Strike interval for spread strategy chains (see strategy param).
    :type interval: Optional[str]
    :param strike_price: Provide a strike price to return options only at that strike price.
    :type strike_price: Optional[str]
    :param range_value: Returns options for the given range. Default is ALL. Possible values are:\n
        * ITM: In-the-money
        * NTM: Near-the-money
        * OTM: Out-of-the-money
        * SAK: Strikes Above Market
        * SBK: Strikes Below Market
        * SNK: Strikes Near Market
        * ALL: All Strikes
    :type range_value: Optional[str]
    :param from_date: Only return expirations after this date. For strategies, expiration refers to the \
        nearest term expiration in the strategy. Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.
    :type from_date: Optional[str]
    :param to_date: Only return expirations before this date. For strategies, expiration refers to the \
        nearest term expiration in the strategy. Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz.
    :type to_date: Optional[str]
    :param volatility: Volatility to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param).
    :type volatility: Optional[str]
    :param underlying_price: Underlying price to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param).
    :type underlying_price: Optional[str]
    :param interest_rate: Interest rate to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param).
    :type interest_rate: Optional[str]
    :param days_to_expiration: Days to expiration to use in calculations. Applies only to ANALYTICAL strategy chains (see strategy param).
    :type days_to_expiration: Optional[str]
    :param exp_month: Return only options expiring in the specified month. Month is given in the three character format. Example: JAN. Default is ALL.
    :type exp_month: Optional[str]
    :param option_type: Type of contracts to return. Default is ALL. Possible values are:\n
        * S: Standard contracts
        * NS: Non-standard contracts
        * ALL: All contracts
    :type option_type: Optional[str]
    :param jsonify: If set to false, will return the raw response object. \
        If set to True, will return a dictionary parsed using the JSON format.
    :type jsonify: Optional[str]
    :returns: Returns a tuple where the first entry in the tuple is a requests reponse object  \
        or a dictionary parsed using the JSON format and the second entry is an error string or \
        None if there was not an error.

    """
    url = URLS.option_chains()
    payload = {
        "symbol": ticker,
        "contractType": contract_type,
        "strikeCount": strike_count,
        "includeQuotes": include_quotes,
        "strategy": strategy,
        "range": range_value,
        "expMonth": exp_month,
        "optionType": option_type
    }
    if interval:
        payload["interval"] = interval
    if strike_price:
        payload["strike"] = strike_price
    if from_date:
        payload["fromDate"] = from_date
    if to_date: 
        payload["toDate"] = to_date
    if volatility:
        payload["volatility"] = volatility
    if underlying_price:
        payload["underlyingPrice"] = underlying_price
    if interest_rate:
        payload["interestRate"] = interest_rate
    if days_to_expiration:
        payload["daysToExpiration"] = days_to_expiration
    data, error = request_get(url, payload, jsonify)
    return data, error
