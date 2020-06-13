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
        self.list_stocks = ['tsla', 'f', 'plug', 'fB', 'SPY', 'botz', 'jnug']
        self.fake_stocks = ['87627273', 'ffffffffff']

    def test_quotes(self):
        quote = r.get_quotes(self.single_stock, info=None)[0]
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


if __name__ == '__main__':
    config = configparser.ConfigParser()
    ini_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','config.ini'))
    config.read(ini_path)
    r.login(config.get('authentication', 'email'), config.get('authentication', 'password'), store_session=True)
    unittest.main()
