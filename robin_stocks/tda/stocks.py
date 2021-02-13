from robin_stocks.tda.helper import format_inputs, login_required, request_get
from robin_stocks.tda.urls import URLS


@login_required
@format_inputs
def get_quote(ticker, jsonify=None):
    url = URLS.quote(ticker)
    data, error = request_get(url, None, jsonify)
    return data, error


@login_required
@format_inputs
def get_quotes(tickers, jsonify=None):
    """ make sure tickers is a comma separated string with no spaces.
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
    if (start_date or end_date) and period:
        raise ValueError("If start_date and end_date are provided, period should not be provided.")
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
