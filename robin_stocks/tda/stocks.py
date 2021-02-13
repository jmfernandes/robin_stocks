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
