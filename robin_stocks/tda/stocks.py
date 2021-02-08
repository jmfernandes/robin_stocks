from robin_stocks.tda.helper import format_inputs, login_required, request_get
from robin_stocks.tda.urls import URLS


@login_required
@format_inputs
def get_quote(ticker, jsonify=None):
    url = URLS.quote(ticker)
    data, error = request_get(url, None, jsonify)
    return data, error
