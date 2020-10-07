"""Contains all the url endpoints for interacting with Robinhood API."""
from robin_stocks.helper import id_for_chain, id_for_stock

# Login


def login_url():
    return('https://api.robinhood.com/oauth2/token/')


def challenge_url(challenge_id):
    return('https://api.robinhood.com/challenge/{0}/respond/'.format(challenge_id))

# Profiles


def account_profile():
    return('https://api.robinhood.com/accounts/')


def basic_profile():
    return('https://api.robinhood.com/user/basic_info/')


def investment_profile():
    return('https://api.robinhood.com/user/investment_profile/')


def portfolio_profile():
    return('https://api.robinhood.com/portfolios/')


def security_profile():
    return('https://api.robinhood.com/user/additional_info/')


def user_profile():
    return('https://api.robinhood.com/user/')

def portfolis_historicals(account_number):
    return('https://api.robinhood.com/portfolios/historicals/{0}/'.format(account_number))

# Stocks


def earnings():
    return('https://api.robinhood.com/marketdata/earnings/')


def events():
    return('https://api.robinhood.com/options/events/')


def fundamentals():
    return('https://api.robinhood.com/fundamentals/')


def historicals():
    return('https://api.robinhood.com/quotes/historicals/')


def instruments():
    return('https://api.robinhood.com/instruments/')


def news(symbol):
    return('https://api.robinhood.com/midlands/news/{0}/?'.format(symbol))


def popularity(symbol):
    return('https://api.robinhood.com/instruments/{0}/popularity/'.format(id_for_stock(symbol)))

def quotes():
    return('https://api.robinhood.com/quotes/')


def ratings(symbol):
    return('https://api.robinhood.com/midlands/ratings/{0}/'.format(id_for_stock(symbol)))


def splits(symbol):
    return('https://api.robinhood.com/instruments/{0}/splits/'.format(id_for_stock(symbol)))

# account

def phoenix():
    return('https://phoenix.robinhood.com/accounts/unified')

def positions():
    return('https://api.robinhood.com/positions/')

def banktransfers():
    return('https://api.robinhood.com/ach/transfers/')

def cardtransactions():
   return('https://minerva.robinhood.com/history/transactions/')

def daytrades(account):
    return('https://api.robinhood.com/accounts/{0}/recent_day_trades/'.format(account))


def dividends():
    return('https://api.robinhood.com/dividends/')


def documents():
    return('https://api.robinhood.com/documents/')


def linked(id=None, unlink=False):
    if unlink:
        return('https://api.robinhood.com/ach/relationships/{0}/unlink/'.format(id))
    if id:
        return('https://api.robinhood.com/ach/relationships/{0}/'.format(id))
    else:
        return('https://api.robinhood.com/ach/relationships/')


def margin():
    return('https://api.robinhood.com/margin/calls/')


def margininterest():
    return('https://api.robinhood.com/cash_journal/margin_interest_charges/')


def notifications(tracker=False):
    if tracker:
        return('https://api.robinhood.com/midlands/notifications/notification_tracker/')
    else:
        return('https://api.robinhood.com/notifications/devices/')


def referral():
    return('https://api.robinhood.com/midlands/referral/')


def stockloan():
    return('https://api.robinhood.com/stock_loan/payments/')


def subscription():
    return('https://api.robinhood.com/subscription/subscription_fees/')


def wiretransfers():
    return('https://api.robinhood.com/wire/transfers')


def watchlists(name=None, add=False):
    if name:
        return('https://api.robinhood.com/midlands/lists/items/')
    else:
        return('https://api.robinhood.com/midlands/lists/default/')


# markets


def currency():
    return('https://nummus.robinhood.com/currency_pairs/')

def markets():
    return('https://api.robinhood.com/markets/')

def market_hours(market, date):
    return('https://api.robinhood.com/markets/{}/hours/{}/'.format(market, date))

def movers_sp500():
    return('https://api.robinhood.com/midlands/movers/sp500/')

def get_100_most_popular():
    return('https://api.robinhood.com/midlands/tags/tag/100-most-popular/')

def movers_top():
    return('https://api.robinhood.com/midlands/tags/tag/top-movers/')

def market_category(category):
    return('https://api.robinhood.com/midlands/tags/tag/{}/'.format(category))

# options


def aggregate():
    return('https://api.robinhood.com/options/aggregate_positions/')


def chains(symbol):
    return('https://api.robinhood.com/options/chains/{0}/'.format(id_for_chain(symbol)))


def option_historicals(id):
    return('https://api.robinhood.com/marketdata/options/historicals/{0}/'.format(id))


def option_instruments(id=None):
    if id:
        return('https://api.robinhood.com/options/instruments/{0}/'.format(id))
    else:
        return('https://api.robinhood.com/options/instruments/')


def option_orders(orderID=None):
    if orderID:
        return('https://api.robinhood.com/options/orders/{0}/'.format(orderID))
    else:
        return('https://api.robinhood.com/options/orders/')


def option_positions():
    return('https://api.robinhood.com/options/positions/')


def marketdata_options():
    return('https://api.robinhood.com/marketdata/options/')

# pricebook


def marketdata_quotes(id):
    return ('https://api.robinhood.com/marketdata/quotes/{0}/'.format(id))


def marketdata_pricebook(id):
    return ('https://api.robinhood.com/marketdata/pricebook/snapshots/{0}/'.format(id))

# crypto


def order_crypto():
    return('https://nummus.robinhood.com/orders/')


def crypto_account():
    return('https://nummus.robinhood.com/accounts/')


def crypto_currency_pairs():
    return('https://nummus.robinhood.com/currency_pairs/')


def crypto_quote(id):
    return('https://api.robinhood.com/marketdata/forex/quotes/{0}/'.format(id))


def crypto_holdings():
    return('https://nummus.robinhood.com/holdings/')


def crypto_historical(id):
    return('https://api.robinhood.com/marketdata/forex/historicals/{0}/'.format(id))


def crypto_orders(orderID=None):
    if orderID:
        return('https://nummus.robinhood.com/orders/{0}/'.format(orderID))
    else:
        return('https://nummus.robinhood.com/orders/')


def crypto_cancel(id):
    return('https://nummus.robinhood.com/orders/{0}/cancel/'.format(id))

# orders


def cancel(url):
    return('https://api.robinhood.com/orders/{0}/cancel/'.format(url))


def option_cancel(id):
    return('https://api.robinhood.com/options/orders/{0}/cancel/'.format(id))


def orders(orderID=None):
    if orderID:
        return('https://api.robinhood.com/orders/{0}/'.format(orderID))
    else:
        return('https://api.robinhood.com/orders/')
