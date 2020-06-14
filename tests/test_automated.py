import configparser
import os
import unittest

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


if __name__ == '__main__':
    config = configparser.ConfigParser()
    ini_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','config.ini'))
    config.read(ini_path)
    r.login(config.get('authentication', 'email'), config.get('authentication', 'password'), store_session=True)
    unittest.main()
