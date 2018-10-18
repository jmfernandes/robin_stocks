import robin_stocks.helper as helper

### Login

def login_url():
    return('https://api.robinhood.com/oauth2/token/')

### Profiles

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

### Stocks

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
    return('https://api.robinhood.com/midlands/news/{}/?'.format(symbol))

def popularity(symbol):
    return('https://api.robinhood.com/instruments/{}/popularity/'.format(helper.id_for_stock(symbol)))

def quotes():
    return('https://api.robinhood.com/quotes/')

def ratings(symbol):
    return('https://api.robinhood.com/midlands/ratings/{}/'.format(helper.id_for_stock(symbol)))

def splits(symbol):
    return('https://api.robinhood.com/instruments/{}/splits/'.format(helper.id_for_stock(symbol)))

### account

def positions():
    return('https://api.robinhood.com/positions/')

def banktransfers():
    return('https://api.robinhood.com/ach/transfers/')

def daytrades(account):
    return('https://api.robinhood.com/accounts/{}/recent_day_trades/'.format(account))

def dividends():
    return('https://api.robinhood.com/dividends/')

def documents():
    return('https://api.robinhood.com/documents/')

def linked(id=None,unlink=False):
    if unlink:
        return('https://api.robinhood.com/ach/relationships/{}/unlink/'.format(id))
    if id:
        return('https://api.robinhood.com/ach/relationships/{}/'.format(id))
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

def watchlists(name=None,add=False):
    if add:
        return('https://api.robinhood.com/watchlists/{}/bulk_add/'.format(name))

    if name:
        return('https://api.robinhood.com/watchlists/{}/'.format(name))
    else:
        return('https://api.robinhood.com/watchlists/')

### markets

def currency():
    return('https://nummus.robinhood.com/currency_pairs/')

def markets():
    return('https://api.robinhood.com/markets/')

def movers():
    return('https://api.robinhood.com/midlands/movers/sp500/')

### options

def aggregate():
    return('https://api.robinhood.com/options/aggregate_positions/')

def chains():
    return('https://api.robinhood.com/options/chains/{}/'.format(helper.id_for_chain(symbol)))

def option_historicals(id):
    return('https://api.robinhood.com/marketdata/options/historicals/{}/'.format(id))

def option_instruments(id=None):
    if id:
        return('https://api.robinhood.com/options/instruments/{}/'.format(id))
    else:
        return('https://api.robinhood.com/options/instruments/')

def option_orders():
    return('https://api.robinhood.com/options/orders/')

def option_positions():
    return('https://api.robinhood.com/options/positions/')

def marketdata(id):
    return('https://api.robinhood.com/marketdata/options/{}/'.format(id))

### orders

def cancel(url):
    return('https://api.robinhood.com/orders/{}/cancel/'.format(url))

def orders(orderID = None):
    if orderID:
        return('https://api.robinhood.com/orders/{}/'.format(orderID))
    else:
        return('https://api.robinhood.com/orders/')
