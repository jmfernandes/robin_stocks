import configparser
import os
import unittest
import datetime

import requests
import robin_stocks as r


class TestProfiles(unittest.TestCase):

    def setUp(self):
        self.user = "api.robinhood.com/user/"
        self.account = config.get('account', 'account_number')
        self.zipcode = config.get('account', 'zipcode')
        self.username = config.get('account', 'username')

    def test_account_profile(self):
        profile = r.load_account_profile(info=None)
        self.assertEqual(profile['user'], self.user)
        self.assertEqual(profile['account_number'], self.account)

    def test_basic_profile(self):
        profile = r.load_basic_profile(info=None)
        self.assertEqual(profile['user'], self.user)
        self.assertEqual(profile['zipcode'], self.zipcode)

    def test_investment_profile(self):
        profile = r.load_investment_profile(info=None)
        self.assertEqual(profile['user'], self.user)

    def test_portfolio_profile(self):
        profile = r.load_portfolio_profile(info=None)
        self.assertEqual(profile['url'], "https://api.robinhood.com/portfolios/{}/".format(self.account))

    def test_security_profile(self):
        profile = r.load_security_profile(info=None)
        self.assertEqual(profile['user'], self.user)

    def test_user_profile(self):
        profile = r.load_user_profile(info=None)
        self.assertEqual(profile['url'], "https://{}".format(self.user))
        self.assertEqual(profile['username'], self.username)

    def test_crypto_profile(self):
        profile = r.load_crypto_profile(info=None)
        self.assertEqual(profile['apex_account_number'], self.account)


class TestStocks(unittest.TestCase):

    def setUp(self):
        self.single_stock = 'AAPL'
        self.event_stock = 'USO1'
        self.fake_stock = 'thisisfake'
        self.instrument = 'https://api.robinhood.com/instruments/450dfc6d-5510-4d40-abfb-f633b7d9be3e/'
        self.fake_instrument = 'https://api.robinhood.com/instruments/aaaaaaaa-0000-0000-0000-aaaaaaaaaaaa/'
        self.id = '450dfc6d-5510-4d40-abfb-f633b7d9be3e'
        self.list_stocks = ['tsla', 'f', 'plug', 'fB', 'SPY', 'botz', 'jnug']
        self.fake_stocks = ['87627273', 'ffffffffff']

    def test_quotes(self):
        quote = r.get_quotes(self.single_stock, info=None)
        self.assertEqual(len(quote), 1)
        quote = quote[0]
        self.assertEqual(quote['symbol'], self.single_stock)
        self.assertIn('ask_price', quote)
        self.assertIn('ask_size', quote)
        self.assertIn('bid_price', quote)
        self.assertIn('bid_size', quote)
        self.assertIn('last_trade_price', quote)
        self.assertIn('last_extended_hours_trade_price', quote)
        self.assertIn('previous_close', quote)
        self.assertIn('adjusted_previous_close', quote)
        self.assertIn('previous_close_date', quote)
        self.assertIn('symbol', quote)
        self.assertIn('trading_halted', quote)
        self.assertIn('has_traded', quote)
        self.assertIn('last_trade_price_source', quote)
        self.assertIn('updated_at', quote)
        self.assertIn('instrument', quote)
        #
        more_quotes = r.get_quotes(self.list_stocks, info=None)
        self.assertEqual(len(more_quotes), len(self.list_stocks))
        #
        fake_quotes = r.get_quotes(self.fake_stocks, info=None)
        self.assertEqual(len(fake_quotes), 1)
        self.assertEqual(fake_quotes[0], None)

    def test_fundamentals(self):
        quote = r.get_fundamentals(self.single_stock, info=None)
        self.assertEqual(len(quote), 1)
        self.assertEqual(quote[0]['symbol'], self.single_stock)
        quote = quote[0]
        self.assertIn('open', quote)
        self.assertIn('high', quote)
        self.assertIn('low', quote)
        self.assertIn('volume', quote)
        self.assertIn('average_volume_2_weeks', quote)
        self.assertIn('average_volume', quote)
        self.assertIn('high_52_weeks', quote)
        self.assertIn('dividend_yield', quote)
        self.assertIn('float', quote)
        self.assertIn('low_52_weeks', quote)
        self.assertIn('market_cap', quote)
        self.assertIn('pb_ratio', quote)
        self.assertIn('pe_ratio', quote)
        self.assertIn('shares_outstanding', quote)
        self.assertIn('description', quote)
        self.assertIn('instrument', quote)
        self.assertIn('ceo', quote)
        self.assertIn('headquarters_city', quote)
        self.assertIn('headquarters_state', quote)
        self.assertIn('sector', quote)
        self.assertIn('industry', quote)
        self.assertIn('num_employees', quote)
        self.assertIn('year_founded', quote)
        self.assertIn('symbol', quote)
        #
        more_quotes = r.get_fundamentals(self.list_stocks, info=None)
        self.assertEqual(len(more_quotes), len(self.list_stocks))
        #
        fake_quotes = r.get_fundamentals(self.fake_stocks, info=None)
        self.assertEqual(len(fake_quotes), 1)
        self.assertEqual(fake_quotes[0], None)

    def test_instruments(self):
        quote = r.get_instruments_by_symbols(self.single_stock)
        self.assertEqual(len(quote), 1)
        self.assertEqual(quote[0]['symbol'], self.single_stock)
        quote = quote[0]
        self.assertIn('id', quote)
        self.assertIn('url', quote)
        self.assertIn('quote', quote)
        self.assertIn('fundamentals', quote)
        self.assertIn('splits', quote)
        self.assertIn('state', quote)
        self.assertIn('market', quote)
        self.assertIn('simple_name', quote)
        self.assertIn('name', quote)
        self.assertIn('tradeable', quote)
        self.assertIn('tradability', quote)
        self.assertIn('symbol', quote)
        self.assertIn('bloomberg_unique', quote)
        self.assertIn('margin_initial_ratio', quote)
        self.assertIn('maintenance_ratio', quote)
        self.assertIn('country', quote)
        self.assertIn('day_trade_ratio', quote)
        self.assertIn('list_date', quote)
        self.assertIn('min_tick_size', quote)
        self.assertIn('type', quote)
        self.assertIn('tradable_chain_id', quote)
        self.assertIn('rhs_tradability', quote)
        self.assertIn('fractional_tradability', quote)
        self.assertIn('default_collar_fraction', quote)
        #
        more_quotes = r.get_fundamentals(self.list_stocks, info=None)
        self.assertEqual(len(more_quotes), len(self.list_stocks))
        #
        fake_quotes = r.get_fundamentals(self.fake_stocks, info=None)
        self.assertEqual(len(fake_quotes), 1)
        self.assertEqual(fake_quotes[0], None)

    def test_instrument_id(self):
        quote = r.get_instrument_by_url(self.instrument)
        self.assertEqual(quote['symbol'], self.single_stock)
        self.assertIn('id', quote)
        self.assertIn('url', quote)
        self.assertIn('quote', quote)
        self.assertIn('fundamentals', quote)
        self.assertIn('splits', quote)
        self.assertIn('state', quote)
        self.assertIn('market', quote)
        self.assertIn('simple_name', quote)
        self.assertIn('name', quote)
        self.assertIn('tradeable', quote)
        self.assertIn('tradability', quote)
        self.assertIn('symbol', quote)
        self.assertIn('bloomberg_unique', quote)
        self.assertIn('margin_initial_ratio', quote)
        self.assertIn('maintenance_ratio', quote)
        self.assertIn('country', quote)
        self.assertIn('day_trade_ratio', quote)
        self.assertIn('list_date', quote)
        self.assertIn('min_tick_size', quote)
        self.assertIn('type', quote)
        self.assertIn('tradable_chain_id', quote)
        self.assertIn('rhs_tradability', quote)
        self.assertIn('fractional_tradability', quote)
        self.assertIn('default_collar_fraction', quote)

    def test_latest_price(self):
        price = r.get_latest_price(self.single_stock)
        self.assertEqual(len(price), 1)
        more_prices = r.get_latest_price(self.list_stocks)
        self.assertEqual(len(more_prices), len(self.list_stocks))
        fake_prices = r.get_latest_price(self.fake_stocks)
        self.assertEqual(len(fake_prices), 1)
        self.assertEqual(fake_prices[0], None)

    def test_name_by_symbol(self):
        name = r.get_name_by_symbol(self.single_stock)
        self.assertEqual(name, 'Apple')
        fake_name = r.get_name_by_symbol(self.fake_stock)
        self.assertEqual(fake_name, '')

    def test_name_by_url(self):
        name = r.get_name_by_url(self.instrument)
        self.assertEqual(name, 'Apple')
        fake_name = r.get_name_by_url(self.fake_instrument)
        self.assertEqual(fake_name, '')

    def test_symbol_by_url(self):
        symbol = r.get_symbol_by_url(self.instrument)
        self.assertEqual(symbol, self.single_stock)
        fake_symbol = r.get_symbol_by_url(self.fake_instrument)
        self.assertEqual(fake_symbol, '')

    def test_get_ratings(self):
        ratings = r.get_ratings(self.single_stock)
        self.assertIn('summary', ratings)
        self.assertIn('ratings', ratings)
        self.assertIn('instrument_id', ratings)
        self.assertIn('ratings_published_at', ratings)
        fake_ratings = r.get_ratings(self.fake_stock)
        self.assertEqual(fake_ratings, '')

    def test_get_popularity(self):
        popularity = r.get_popularity(self.single_stock)
        self.assertEqual(popularity['instrument'], self.instrument)
        self.assertIn('instrument', popularity)
        self.assertIn('num_open_positions', popularity)
        fake_popularity = r.get_popularity(self.fake_stock)
        self.assertEqual(fake_popularity, '')

    def test_events(self):
        event = r.get_events(self.single_stock)
        self.assertEqual(len(event), 0)
        event = r.get_events(self.event_stock)
        self.assertEqual(len(event), 1)
        event = event[0]
        self.assertIn('account', event)
        self.assertIn('cash_component', event)
        self.assertIn('chain_id', event)
        self.assertIn('created_at', event)
        self.assertIn('direction', event)
        self.assertIn('equity_components', event)
        self.assertIn('event_date', event)
        self.assertIn('id', event)
        self.assertIn('option', event)
        self.assertIn('position', event)
        self.assertIn('quantity', event)
        self.assertIn('state', event)
        self.assertIn('total_cash_amount', event)
        self.assertIn('type', event)
        self.assertIn('underlying_price', event)
        self.assertIn('updated_at', event)
        fake_event = r.get_popularity(self.fake_stock)
        self.assertEqual(fake_event, '')

    def test_earning(self):
        earnings = r.get_earnings(self.single_stock)[0]
        self.assertEqual(earnings['symbol'], self.single_stock)
        self.assertIn('symbol', earnings)
        self.assertIn('instrument', earnings)
        self.assertIn('year', earnings)
        self.assertIn('quarter', earnings)
        self.assertIn('eps', earnings)
        self.assertIn('report', earnings)
        self.assertIn('call', earnings)
        fake_earnings = r.get_earnings(self.fake_stock)
        self.assertEqual(len(fake_earnings), 0)

    def test_news(self):
        news = r.get_news(self.single_stock)[0]
        self.assertIn('author', news)
        self.assertIn('num_clicks', news)
        self.assertIn('preview_image_url', news)
        self.assertIn('published_at', news)
        self.assertIn('relay_url', news)
        self.assertIn('source', news)
        self.assertIn('summary', news)
        self.assertIn('title', news)
        self.assertIn('updated_at', news)
        self.assertIn('url', news)
        self.assertIn('uuid', news)
        self.assertIn('related_instruments', news)
        self.assertIn('preview_text', news)
        self.assertIn('currency_id', news)
        fake_news = r.get_news(self.fake_stock)
        self.assertEqual(len(fake_news), 0)

    def test_split(self):
        split = r.get_splits(self.single_stock)[0]
        self.assertEqual(split['instrument'], self.instrument)
        fake_split = r.get_splits(self.fake_stock)
        self.assertEqual(len(fake_split), 0)

class TestOptions(unittest.TestCase):

    def setUp(self):
        now = datetime.datetime.now()
        self.expiration_date = third_friday(now.year, now.month, now.day).strftime("%Y-%m-%d")
        self.strike = 300
        self.symbol = 'AAPL'

    def test_find_tradable_options(self):
        info = r.find_options_by_expiration(self.symbol, self.expiration_date)
        first = info[0]
        self.assertEqual(first['expiration_date'], self.expiration_date)
        self.assertGreater(len(info), 100)
        info = r.find_options_by_expiration(self.symbol, self.expiration_date, info='strike_price')
        first = info[0]
        self.assertEqual(type(first), str)
        self.assertGreater(len(info), 100)
        info = r.find_options_by_expiration(self.symbol, self.expiration_date, info='expiration_date')
        self.assertEqual(len(set(info)), 1)

    def test_find_options_by_strike(self):
        info = r.find_options_by_strike(self.symbol, self.strike)
        self.assertGreater(len(info), 30)
        info = r.find_options_by_strike(self.symbol, self.strike,'call')
        self.assertEqual(info[0]['type'], 'call')
        info = r.find_options_by_strike(self.symbol, self.strike, info='expiration_date')
        self.assertGreater(len(set(info)), 1)
        info = r.find_options_by_strike(self.symbol, self.strike, info='strike_price')
        self.assertEqual(len(set(info)), 1)

    def test_find_options_by_expiration_and_strike(self):
        info = r.find_options_by_expiration_and_strike(self.symbol, self.expiration_date, self.strike)
        self.assertEqual(len(info), 2)
        self.assertEqual(info[0]['expiration_date'], self.expiration_date)
        self.assertEqual(float(info[0]['strike_price']), self.strike)
        info = r.find_options_by_expiration_and_strike(self.symbol, self.expiration_date, self.strike, 'call')
        self.assertEqual(len(info), 1)
        self.assertEqual(info[0]['type'], 'call')

class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.stock = 'AAPL'
        self.bitcoin = 'BTC'
        self.bitcoin_currency = 'BTC-USD'
        self.bitcoin_symbol = 'BTCUSD'
        self.fake = 'thisisafake'
        self.account = config.get('account', 'crypto_account')


    def test_crypto_positions(self):
        positions = r.get_crypto_positions(info=None)
        first = positions[0]
        self.assertEqual(first['account_id'], self.account)
        self.assertIn('account_id', first)
        self.assertIn('cost_bases', first)
        self.assertIn('created_at', first)
        self.assertIn('currency', first)
        self.assertIn('id', first)
        self.assertIn('quantity', first)
        self.assertIn('quantity_available', first)
        self.assertIn('quantity_held_for_buy', first)
        self.assertIn('quantity_held_for_sell', first)
        self.assertIn('updated_at', first)

    def test_get_crypto_currency_pairs(self):
        pairs = r.get_crypto_currency_pairs(info=None)
        btc = [x for x in pairs if x['symbol'] == self.bitcoin_currency ][0]
        self.assertIn('asset_currency', btc)
        self.assertIn('display_only', btc)
        self.assertIn('id', btc)
        self.assertIn('max_order_size', btc)
        self.assertIn('min_order_size', btc)
        self.assertIn('min_order_price_increment', btc)
        self.assertIn('min_order_quantity_increment', btc)
        self.assertIn('name', btc)
        self.assertIn('quote_currency', btc)
        self.assertIn('symbol', btc)
        self.assertIn('tradability', btc)
        fake = [x for x in pairs if x['symbol'] == self.fake]
        self.assertEqual(len(fake), 0)

    def test_crypto_info(self):
        crypto = r.get_crypto_info(self.bitcoin, info=None)
        self.assertIn('asset_currency', crypto)
        self.assertIn('display_only', crypto)
        self.assertIn('id', crypto)
        self.assertIn('max_order_size', crypto)
        self.assertIn('min_order_size', crypto)
        self.assertIn('min_order_price_increment', crypto)
        self.assertIn('min_order_quantity_increment', crypto)
        self.assertIn('name', crypto)
        self.assertIn('quote_currency', crypto)
        self.assertIn('symbol', crypto)
        self.assertIn('tradability', crypto)
        crypto = r.get_crypto_info(self.stock, info=None)
        self.assertEqual(crypto, None)

    def test_crypto_quote(self):
        crypto = r.get_crypto_quote(self.bitcoin, info=None)
        self.assertIn('ask_price', crypto)
        self.assertIn('bid_price', crypto)
        self.assertIn('mark_price', crypto)
        self.assertIn('high_price', crypto)
        self.assertIn('low_price', crypto)
        self.assertIn('open_price', crypto)
        self.assertIn('symbol', crypto)
        self.assertIn('id', crypto)
        self.assertIn('volume', crypto)
        crypto = r.get_crypto_quote(self.stock, info=None)
        self.assertEqual(crypto, None)
        crypto = r.get_crypto_quote(self.fake, info=None)
        self.assertEqual(crypto, None)

    def test_crypto_historical(self):
        crypto = r.get_crypto_historicals(self.bitcoin, 'day', 'week', '24_7', info=None)
        self.assertEqual(len(crypto), 7)
        first_point = crypto[0]
        # check keys
        self.assertIn('begins_at', first_point)
        self.assertIn('open_price', first_point)
        self.assertIn('close_price', first_point)
        self.assertIn('high_price', first_point)
        self.assertIn('low_price', first_point)
        self.assertIn('volume', first_point)
        self.assertIn('session', first_point)
        self.assertIn('interpolated', first_point)
        #
        crypto = r.get_crypto_historicals(self.bitcoin, 'hour', 'day', 'trading', info=None)
        self.assertEqual(len(crypto), 9)
        crypto = r.get_crypto_historicals(self.bitcoin, 'hour', 'day', 'regular', info=None)
        self.assertEqual(len(crypto), 6)
        crypto = r.get_crypto_historicals(self.bitcoin, 'hour', 'day', 'extended', info=None)
        self.assertEqual(len(crypto), 16)
        crypto = r.get_crypto_historicals(self.bitcoin, 'hour', 'day', '24_7', info=None)
        self.assertEqual(len(crypto), 24)

class TestAccounts(unittest.TestCase):

    def setUp(self):
        self.stock = 'AAPL'

    def test_open_stock(self):
        stock = r.get_open_stock_positions(info=None)
        self.assertNotEqual(len(stock), 0)

    def test_get_all_positionsself(self):
        stock = r.get_all_positions(info=None)
        self.assertNotEqual(len(stock), 0)

    def test_dividends(self):
        stock = r.get_dividends(info=None)
        self.assertNotEqual(len(stock), 0)

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

if __name__ == '__main__':
    config = configparser.ConfigParser()
    ini_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','config.ini'))
    config.read(ini_path)
    r.login(config.get('authentication', 'email'), config.get('authentication', 'password'), store_session=True)
    unittest.main()
