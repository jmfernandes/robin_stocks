# Used by git Actions
import os
import datetime
import robin_stocks as r
import pyotp
import pytest

def third_friday(year, month, day):
    """Return datetime.date for monthly option expiration given year and
    month
    """
    # The 15th is the lowest third day in the month
    third = datetime.date(year, month, 15)
    # What day of the week is the 15th?
    w = third.weekday()
    # Friday is weekday 4
    if w != 4:
        # Replace just the day (of month)
        third = third.replace(day=(15 + (4 - w) % 7))

    if day > third.day:
        month += 1
        third = datetime.date(year, month, 15)
        w = third.weekday()
        if w != 4:
            third = third.replace(day=(15 + (4 - w) % 7))

    return third


def round_up_price(ticker, multiplier):
    price = float(r.get_latest_price(ticker)[0])
    num = price + (multiplier - 1)
    return num - (num % multiplier)

class TestStocks:

    # Set up variables for class
    single_stock = 'AAPL'
    event_stock = 'USO1'
    fake_stock = 'thisisfake'
    instrument = 'https://api.robinhood.com/instruments/450dfc6d-5510-4d40-abfb-f633b7d9be3e/'
    fake_instrument = 'https://api.robinhood.com/instruments/aaaaaaaa-0000-0000-0000-aaaaaaaaaaaa/'
    id = '450dfc6d-5510-4d40-abfb-f633b7d9be3e'
    list_stocks = ['tsla', 'f', 'plug', 'fB', 'SPY', 'botz', 'jnug']
    fake_stocks = ['87627273', 'ffffffffff']

    @classmethod
    def setup_class(cls):
        totp  = pyotp.TOTP(os.environ['robin_mfa']).now()
        login = r.login(os.environ['robin_username'], os.environ['robin_password'], mfa_code=totp)

    @classmethod
    def teardown_class(cls):
        r.logout()

    def test_name_apple(self):
        name = r.get_name_by_symbol('aapl')
        assert name == "Apple"

    def test_quotes(self):
        quote = r.get_quotes(self.single_stock, info=None)
        assert (len(quote) == 1)
        quote = quote[0]
        assert (quote['symbol'] == self.single_stock)
        assert ('ask_price' in quote)
        assert ('ask_size' in quote)
        assert ('bid_price' in quote)
        assert ('bid_size' in quote)
        assert ('last_trade_price' in quote)
        assert ('last_extended_hours_trade_price' in quote)
        assert ('previous_close' in quote)
        assert ('adjusted_previous_close' in quote)
        assert ('previous_close_date' in quote)
        assert ('symbol' in quote)
        assert ('trading_halted' in quote)
        assert ('has_traded' in quote)
        assert ('last_trade_price_source' in quote)
        assert ('updated_at' in quote)
        assert ('instrument' in quote)
        #
        more_quotes = r.get_quotes(self.list_stocks, info=None)
        assert (len(more_quotes) ==  len(self.list_stocks))
        #
        fake_quotes = r.get_quotes(self.fake_stocks, info=None)
        assert (len(fake_quotes) == 1)
        assert (fake_quotes[0] == None)

    def test_fundamentals(self):
        quote = r.get_fundamentals(self.single_stock, info=None)
        assert (len(quote) == 1)
        assert (quote[0]['symbol'] == self.single_stock)
        quote = quote[0]
        assert ('open' in quote)
        assert ('high' in quote)
        assert ('low' in quote)
        assert ('volume' in quote)
        assert ('average_volume_2_weeks' in quote)
        assert ('average_volume' in quote)
        assert ('high_52_weeks' in quote)
        assert ('dividend_yield' in quote)
        assert ('float' in quote)
        assert ('low_52_weeks' in quote)
        assert ('market_cap' in quote)
        assert ('pb_ratio' in quote)
        assert ('pe_ratio' in quote)
        assert ('shares_outstanding' in quote)
        assert ('description' in quote)
        assert ('instrument' in quote)
        assert ('ceo' in quote)
        assert ('headquarters_city' in quote)
        assert ('headquarters_state' in quote)
        assert ('sector' in quote)
        assert ('industry' in quote)
        assert ('num_employees' in quote)
        assert ('year_founded' in quote)
        assert ('symbol' in quote)
        #
        more_quotes = r.get_fundamentals(self.list_stocks, info=None)
        assert (len(more_quotes) == len(self.list_stocks))
        #
        fake_quotes = r.get_fundamentals(self.fake_stocks, info=None)
        assert (len(fake_quotes) == 1)
        assert (fake_quotes[0] == None)

    def test_instruments(self):
        quote = r.get_instruments_by_symbols(self.single_stock)
        assert (len(quote) == 1)
        assert (quote[0]['symbol'] == self.single_stock)
        quote = quote[0]
        assert ('id' in quote)
        assert ('url' in quote)
        assert ('quote' in quote)
        assert ('fundamentals' in quote)
        assert ('splits' in quote)
        assert ('state' in quote)
        assert ('market' in quote)
        assert ('simple_name' in quote)
        assert ('name' in quote)
        assert ('tradeable' in quote)
        assert ('tradability' in quote)
        assert ('symbol' in quote)
        assert ('bloomberg_unique' in quote)
        assert ('margin_initial_ratio' in quote)
        assert ('maintenance_ratio' in quote)
        assert ('country' in quote)
        assert ('day_trade_ratio' in quote)
        assert ('list_date' in quote)
        assert ('min_tick_size' in quote)
        assert ('type' in quote)
        assert ('tradable_chain_id' in quote)
        assert ('rhs_tradability' in quote)
        assert ('fractional_tradability' in quote)
        assert ('default_collar_fraction' in quote)
        #
        more_quotes = r.get_fundamentals(self.list_stocks, info=None)
        assert (len(more_quotes) == len(self.list_stocks))
        #
        fake_quotes = r.get_fundamentals(self.fake_stocks, info=None)
        assert (len(fake_quotes) == 1)
        assert (fake_quotes[0] == None)

    def test_instrument_id(self):
        quote = r.get_instrument_by_url(self.instrument)
        assert (quote['symbol'] == self.single_stock)
        assert ('id' in quote)
        assert ('url' in quote)
        assert ('quote' in quote)
        assert ('fundamentals' in quote)
        assert ('splits' in quote)
        assert ('state' in quote)
        assert ('market' in quote)
        assert ('simple_name' in quote)
        assert ('name' in quote)
        assert ('tradeable' in quote)
        assert ('tradability' in quote)
        assert ('symbol' in quote)
        assert ('bloomberg_unique' in quote)
        assert ('margin_initial_ratio' in quote)
        assert ('maintenance_ratio' in quote)
        assert ('country' in quote)
        assert ('day_trade_ratio' in quote)
        assert ('list_date' in quote)
        assert ('min_tick_size' in quote)
        assert ('type' in quote)
        assert ('tradable_chain_id' in quote)
        assert ('rhs_tradability' in quote)
        assert ('fractional_tradability' in quote)
        assert ('default_collar_fraction' in quote)

    def test_latest_price(self):
        price = r.get_latest_price(self.single_stock)
        assert (len(price) == 1)
        more_prices = r.get_latest_price(self.list_stocks)
        assert (len(more_prices) == len(self.list_stocks))
        fake_prices = r.get_latest_price(self.fake_stocks)
        assert (len(fake_prices) == 1)
        assert (fake_prices[0] == None)

    def test_name_by_symbol(self):
        name = r.get_name_by_symbol(self.single_stock)
        assert (name == 'Apple')
        fake_name = r.get_name_by_symbol(self.fake_stock)
        assert (fake_name == '')

    def test_name_by_url(self):
        name = r.get_name_by_url(self.instrument)
        assert (name == 'Apple')
        fake_name = r.get_name_by_url(self.fake_instrument)
        assert (fake_name == '')

    def test_symbol_by_url(self):
        symbol = r.get_symbol_by_url(self.instrument)
        assert (symbol == self.single_stock)
        fake_symbol = r.get_symbol_by_url(self.fake_instrument)
        assert (fake_symbol == '')

    def test_get_ratings(self):
        ratings = r.get_ratings(self.single_stock)
        assert ('summary' in ratings)
        assert ('ratings' in ratings)
        assert ('instrument_id' in ratings)
        assert ('ratings_published_at' in ratings)
        fake_ratings = r.get_ratings(self.fake_stock)
        assert (fake_ratings == '')

    def test_get_popularity(self):
        popularity = r.get_popularity(self.single_stock)
        assert (popularity['instrument'] == self.instrument)
        assert ('instrument' in popularity)
        assert ('num_open_positions' in popularity)
        fake_popularity = r.get_popularity(self.fake_stock)
        assert (fake_popularity == '')

    def test_events(self):
        event = r.get_events(self.single_stock)
        assert (len(event) == 0)
        event = r.get_events(self.event_stock)
        assert (len(event) == 1)
        event = event[0]
        assert ('account' in event)
        assert ('cash_component' in event)
        assert ('chain_id' in event)
        assert ('created_at' in event)
        assert ('direction' in event)
        assert ('equity_components' in event)
        assert ('event_date' in event)
        assert ('id' in event)
        assert ('option' in event)
        assert ('position' in event)
        assert ('quantity' in event)
        assert ('state' in event)
        assert ('total_cash_amount' in event)
        assert ('type' in event)
        assert ('underlying_price' in event)
        assert ('updated_at' in event)
        fake_event = r.get_popularity(self.fake_stock)
        assert (fake_event == '')

    def test_earning(self):
        earnings = r.get_earnings(self.single_stock)[0]
        assert (earnings['symbol'] == self.single_stock)
        assert ('symbol' in earnings)
        assert ('instrument' in earnings)
        assert ('year' in earnings)
        assert ('quarter' in earnings)
        assert ('eps' in earnings)
        assert ('report' in earnings)
        assert ('call' in earnings)
        fake_earnings = r.get_earnings(self.fake_stock)
        assert (len(fake_earnings) == 0)

    def test_news(self):
        news = r.get_news(self.single_stock)[0]
        assert ('author' in news)
        assert ('num_clicks' in news)
        assert ('preview_image_url' in news)
        assert ('published_at' in news)
        assert ('relay_url' in news)
        assert ('source' in news)
        assert ('summary' in news)
        assert ('title' in news)
        assert ('updated_at' in news)
        assert ('url' in news)
        assert ('uuid' in news)
        assert ('related_instruments' in news)
        assert ('preview_text' in news)
        assert ('currency_id' in news)
        fake_news = r.get_news(self.fake_stock)
        assert (len(fake_news) == 0)

    def test_split(self):
        split = r.get_splits(self.single_stock)[0]
        assert (split['instrument'] == self.instrument)
        fake_split = r.get_splits(self.fake_stock)
        assert (len(fake_split) == 0)

    def test_stock_historicals(self):
        historicals = r.get_stock_historicals(self.single_stock, interval='hour', span='day', bounds='regular', info=None)
        assert (len(historicals) <= 6) # 6 regular hours in a day
        historicals = r.get_stock_historicals(self.single_stock, interval='hour', span='day', bounds='trading', info=None)
        assert (len(historicals) <= 9) # 9 trading hours total in a day
        historicals = r.get_stock_historicals(self.single_stock, interval='hour', span='day', bounds='extended', info=None)
        assert (len(historicals) <= 16) # 16 extended hours total in a day

class TestCrypto:

    stock = 'AAPL'
    bitcoin = 'BTC'
    bitcoin_currency = 'BTC-USD'
    bitcoin_symbol = 'BTCUSD'
    fake = 'thisisafake'
    account = os.environ['crypto_account']

    @classmethod
    def setup_class(cls):
        totp  = pyotp.TOTP(os.environ['robin_mfa']).now()
        login = r.login(os.environ['robin_username'], os.environ['robin_password'], mfa_code=totp)

    @classmethod
    def teardown_class(cls):
        r.logout()

    def test_crypto_positions(self):
        positions = r.get_crypto_positions(info=None)
        first = positions[0]
        assert (first['account_id'] == self.account)
        assert ('account_id' in first)
        assert ('cost_bases' in first)
        assert ('created_at' in first)
        assert ('currency' in first)
        assert ('id' in first)
        assert ('quantity' in first)
        assert ('quantity_available' in first)
        assert ('quantity_held_for_buy' in first)
        assert ('quantity_held_for_sell' in first)
        assert ('updated_at' in first)

    def test_get_crypto_currency_pairs(self):
        pairs = r.get_crypto_currency_pairs(info=None)
        btc = [x for x in pairs if x['symbol'] == self.bitcoin_currency][0]
        assert ('asset_currency' in btc)
        assert ('display_only' in btc)
        assert ('id' in btc)
        assert ('max_order_size' in btc)
        assert ('min_order_size' in btc)
        assert ('min_order_price_increment' in btc)
        assert ('min_order_quantity_increment' in btc)
        assert ('name' in btc)
        assert ('quote_currency' in btc)
        assert ('symbol' in btc)
        assert ('tradability' in btc)
        fake = [x for x in pairs if x['symbol'] == self.fake]
        assert (len(fake) == 0)

    def test_crypto_info(self):
        crypto = r.get_crypto_info(self.bitcoin, info=None)
        assert ('asset_currency' in crypto)
        assert ('display_only' in crypto)
        assert ('id' in crypto)
        assert ('max_order_size' in crypto)
        assert ('min_order_size' in crypto)
        assert ('min_order_price_increment' in crypto)
        assert ('min_order_quantity_increment' in crypto)
        assert ('name' in crypto)
        assert ('quote_currency' in crypto)
        assert ('symbol' in crypto)
        assert ('tradability' in crypto)
        crypto = r.get_crypto_info(self.stock, info=None)
        assert (crypto == None)

    def test_crypto_quote(self):
        crypto = r.get_crypto_quote(self.bitcoin, info=None)
        assert ('ask_price' in crypto)
        assert ('bid_price' in crypto)
        assert ('mark_price' in crypto)
        assert ('high_price' in crypto)
        assert ('low_price' in crypto)
        assert ('open_price' in crypto)
        assert ('symbol' in crypto)
        assert ('id' in crypto)
        assert ('volume' in crypto)
        crypto = r.get_crypto_quote(self.stock, info=None)
        assert (crypto == None)
        crypto = r.get_crypto_quote(self.fake, info=None)
        assert (crypto == None)

    def test_crypto_historicals(self):
        crypto = r.get_crypto_historicals(self.bitcoin, 'day', 'week', '24_7', info=None)
        assert (len(crypto) == 7)
        first_point = crypto[0]
        # check keys
        assert ('begins_at' in first_point)
        assert ('open_price' in first_point)
        assert ('close_price' in first_point)
        assert ('high_price' in first_point)
        assert ('low_price' in first_point)
        assert ('volume' in first_point)
        assert ('session' in first_point)
        assert ('interpolated' in first_point)
        #
        crypto = r.get_crypto_historicals(self.bitcoin, 'hour', 'day', 'regular', info=None)
        assert (len(crypto) <= 6) # 6 regular hours in a day
        crypto = r.get_crypto_historicals(self.bitcoin, 'hour', 'day', 'trading', info=None)
        assert (len(crypto) <= 9) # 9 trading hours in a day
        crypto = r.get_crypto_historicals(self.bitcoin, 'hour', 'day', 'extended', info=None)
        assert (len(crypto) <= 16) # 16 extended hours in a day
        crypto = r.get_crypto_historicals(self.bitcoin, 'hour', 'day', '24_7', info=None)
        assert (len(crypto) <= 24) # 24 24_7 hours in a day

class TestOptions:

    # have to login to use round_up_price
    totp  = pyotp.TOTP(os.environ['robin_mfa']).now()
    login = r.login(os.environ['robin_username'], os.environ['robin_password'], mfa_code=totp)
    #
    now = datetime.datetime.now()
    expiration_date = third_friday(now.year, now.month, now.day).strftime("%Y-%m-%d")
    symbol = 'AAPL'
    strike = round_up_price(symbol, 100)

    def test_find_tradable_options(self):
        info = r.find_options_by_expiration(self.symbol, self.expiration_date)
        first = info[0]
        assert (first['expiration_date'] == self.expiration_date)
        assert (len(info) > 100)
        info = r.find_options_by_expiration(self.symbol, self.expiration_date, info='strike_price')
        first = info[0]
        assert (type(first) == str)
        assert (len(info) > 100)
        info = r.find_options_by_expiration(self.symbol, self.expiration_date, info='expiration_date')
        assert (len(set(info)) == 1)

    def test_find_options_by_strike(self):
        info = r.find_options_by_strike(self.symbol, self.strike)
        assert (len(info) > 30)
        info = r.find_options_by_strike(self.symbol, self.strike,'call')
        assert (info[0]['type'] == 'call')
        info = r.find_options_by_strike(self.symbol, self.strike, info='expiration_date')
        assert (len(set(info)) > 1)
        info = r.find_options_by_strike(self.symbol, self.strike, info='strike_price')
        assert (len(set(info)) == 1)

    def test_find_options_by_expiration_and_strike(self):
        info = r.find_options_by_expiration_and_strike(self.symbol, self.expiration_date, self.strike)
        assert (len(info) == 2)
        assert (info[0]['expiration_date'] == self.expiration_date)
        assert (float(info[0]['strike_price']) == self.strike)
        info = r.find_options_by_expiration_and_strike(self.symbol, self.expiration_date, self.strike, 'call')
        assert (len(info) == 1)
        assert (info[0]['type'] == 'call')

class TestProfiles:
    @classmethod
    def setup_class(cls):
        totp  = pyotp.TOTP(os.environ['robin_mfa']).now()
        login = r.login(os.environ['robin_username'], os.environ['robin_password'], mfa_code=totp)

    @classmethod
    def teardown_class(cls):
        r.logout()

    def test_load_account_profile(self):
        profile = r.load_account_profile(info=None)
        assert profile

    def test_basic_profile(self):
        profile = r.load_basic_profile(info=None)
        assert profile

    def test_investment_profile(self):
        profile = r.load_investment_profile(info=None)
        assert profile

    def test_portfolio_profile(self):
        profile = r.load_portfolio_profile(info=None)
        assert profile

    def test_security_profile(self):
        profile = r.load_security_profile(info=None)
        assert profile

    def test_user_profile(self):
        profile = r.load_user_profile(info=None)
        assert profile

    def test_crypto_profile(self):
        profile = r.load_crypto_profile(info=None)
        assert profile

    @pytest.mark.xfail()
    def test_key_failed(self):
        profile = r.load_account_profile(info='cheese')
        assert profile

    @pytest.mark.xfail()
    def test_login_failed(self):
        r.logout()
        profile = r.load_account_profile(info=None)
        assert profile
