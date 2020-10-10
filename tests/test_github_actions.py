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
        assert (len(info) >= 24)
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

class TestMarkets:

    today = datetime.datetime.today().strftime('%Y-%m-%d')
    american_time = datetime.datetime.today().strftime('%m-%d-%Y')
    nyse = 'XNYS'
    amex = 'XASE'
    nasdaq = 'XNAS'
    fake = 'blah'

    @classmethod
    def setup_class(cls):
        totp  = pyotp.TOTP(os.environ['robin_mfa']).now()
        login = r.login(os.environ['robin_username'], os.environ['robin_password'], mfa_code=totp)

    @classmethod
    def teardown_class(cls):
        r.logout()

    def test_top_movers(self):
        movers = r.get_top_movers()
        assert (movers)
        first = movers[0]
        assert ('ask_price' in first)
        assert ('ask_size' in first)
        assert ('bid_price' in first)
        assert ('bid_size' in first)
        assert ('last_trade_price' in first)
        assert ('last_extended_hours_trade_price' in first)
        assert ('previous_close' in first)
        assert ('adjusted_previous_close' in first)
        assert ('previous_close_date' in first)
        assert ('symbol' in first)
        assert ('trading_halted' in first)
        assert ('has_traded' in first)
        assert ('last_trade_price_source' in first)
        assert ('updated_at' in first)
        assert ('instrument' in first)

    def test_top_100(self):
        movers = r.get_top_100()
        assert (movers)
        first = movers[0]
        assert ('ask_price' in first)
        assert ('ask_size' in first)
        assert ('bid_price' in first)
        assert ('bid_size' in first)
        assert ('last_trade_price' in first)
        assert ('last_extended_hours_trade_price' in first)
        assert ('previous_close' in first)
        assert ('adjusted_previous_close' in first)
        assert ('previous_close_date' in first)
        assert ('symbol' in first)
        assert ('trading_halted' in first)
        assert ('has_traded' in first)
        assert ('last_trade_price_source' in first)
        assert ('updated_at' in first)
        assert ('instrument' in first)

    def test_top_movers_sp500(self):
        # going up
        movers = r.get_top_movers_sp500('up')
        assert (movers)
        first = movers[0]
        assert ('instrument_url' in first)
        assert ('symbol' in first)
        assert ('updated_at' in first)
        assert ('price_movement' in first)
        assert ('description' in first)
        assert ('market_hours_last_movement_pct' in first['price_movement'])
        assert ('market_hours_last_price' in first['price_movement'])
        assert (float(first['price_movement']['market_hours_last_movement_pct']) > 0)
        # going down
        movers = r.get_top_movers_sp500('down')
        assert (movers)
        first = movers[0]
        assert (float(first['price_movement']['market_hours_last_movement_pct']) < 0)

    def test_get_all_stocks_from_market_tag(self):
        movers = r.get_all_stocks_from_market_tag('upcoming-earnings')
        assert (movers)
        first = movers[0]
        assert ('ask_price' in first)
        assert ('ask_size' in first)
        assert ('bid_price' in first)
        assert ('bid_size' in first)
        assert ('last_trade_price' in first)
        assert ('last_extended_hours_trade_price' in first)
        assert ('previous_close' in first)
        assert ('adjusted_previous_close' in first)
        assert ('previous_close_date' in first)
        assert ('symbol' in first)
        assert ('trading_halted' in first)
        assert ('has_traded' in first)
        assert ('last_trade_price_source' in first)
        assert ('updated_at' in first)
        assert ('instrument' in first)

    def test_get_markets(self):
        markets = r.get_markets()
        assert (markets)
        first = markets[0]
        assert ('url' in first)
        assert ('todays_hours' in first)
        assert ('mic' in first)
        assert ('operating_mic' in first)
        assert ('acronym' in first)
        assert ('name' in first)
        assert ('city' in first)
        assert ('country' in first)
        assert ('timezone' in first)
        assert ('website' in first)

    def test_get_market_today_hours(self):
        market = r.get_market_today_hours(self.nyse)
        assert ('date' in market)
        assert ('is_open' in market)
        assert ('opens_at' in market)
        assert ('closes_at' in market)
        assert ('extended_opens_at' in market)
        assert ('extended_closes_at' in market)
        assert ('previous_open_hours' in market)
        assert ('next_open_hours' in market)

    def test_get_market_next_open_hours(self):
        market = r.get_market_next_open_hours(self.amex)
        assert ('date' in market)
        assert ('is_open' in market)
        assert ('opens_at' in market)
        assert ('closes_at' in market)
        assert ('extended_opens_at' in market)
        assert ('extended_closes_at' in market)
        assert ('previous_open_hours' in market)
        assert ('next_open_hours' in market)

    def test_get_market_next_open_hours_after_date(self):
        market = r.get_market_next_open_hours_after_date(self.nasdaq, self.today)
        assert ('date' in market)
        assert ('is_open' in market)
        assert ('opens_at' in market)
        assert ('closes_at' in market)
        assert ('extended_opens_at' in market)
        assert ('extended_closes_at' in market)
        assert ('previous_open_hours' in market)
        assert ('next_open_hours' in market)

    def test_get_market_hours(self):
        market = r.get_market_hours(self.nasdaq, self.today)
        assert ('date' in market)
        assert ('is_open' in market)
        assert ('opens_at' in market)
        assert ('closes_at' in market)
        assert ('extended_opens_at' in market)
        assert ('extended_closes_at' in market)
        assert ('previous_open_hours' in market)
        assert ('next_open_hours' in market)
        todaymarket = r.get_market_today_hours(self.nasdaq)
        assert (market['date'] == todaymarket['date'])

    def test_currency_pairs(self):
        currency = r.get_currency_pairs()
        assert currency
        first = currency[0]
        assert ('asset_currency' in first)
        assert ('display_only' in first)
        assert ('id' in first)
        assert ('max_order_size' in first)
        assert ('min_order_size' in first)
        assert ('min_order_price_increment' in first)
        assert ('min_order_quantity_increment' in first)
        assert ('name' in first)
        assert ('quote_currency' in first)
        assert ('symbol' in first)
        assert ('tradability' in first)

    @pytest.mark.xfail()
    def test_market_fail(self):
        market = r.get_market_hours(self.fake, self.today)
        assert market

    @pytest.mark.xfail()
    def test_market_date_fail(self):
        market = r.get_market_hours(self.nasdaq, self.american_time)
        assert market

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
        assert ('url' in profile)
        assert ('portfolio_cash' in profile)
        assert ('can_downgrade_to_cash' in profile)
        assert ('user' in profile)
        assert ('account_number' in profile)
        assert ('type' in profile)
        assert ('created_at' in profile)
        assert ('updated_at' in profile)
        assert ('deactivated' in profile)
        assert ('deposit_halted' in profile)
        assert ('only_position_closing_trades' in profile)
        assert ('buying_power' in profile)
        assert ('cash_available_for_withdrawal' in profile)
        assert ('cash' in profile)
        assert ('cash_held_for_orders' in profile)
        assert ('uncleared_deposits' in profile)
        assert ('sma' in profile)
        assert ('sma_held_for_orders' in profile)
        assert ('unsettled_funds' in profile)
        assert ('unsettled_debit' in profile)
        assert ('crypto_buying_power' in profile)
        assert ('max_ach_early_access_amount' in profile)
        assert ('cash_balances' in profile)
        assert ('margin_balances' in profile)
        assert ('sweep_enabled' in profile)
        assert ('instant_eligibility' in profile)
        assert ('option_level' in profile)
        assert ('is_pinnacle_account' in profile)
        assert ('rhs_account_number' in profile)
        assert ('state' in profile)
        assert ('active_subscription_id' in profile)
        assert ('locked' in profile)
        assert ('permanently_deactivated' in profile)
        assert ('received_ach_debit_locked' in profile)
        assert ('drip_enabled' in profile)
        assert ('eligible_for_fractionals' in profile)
        assert ('eligible_for_drip' in profile)
        assert ('eligible_for_cash_management' in profile)
        assert ('cash_management_enabled' in profile)
        assert ('option_trading_on_expiration_enabled' in profile)
        assert ('cash_held_for_options_collateral' in profile)
        assert ('fractional_position_closing_only' in profile)
        assert ('user_id' in profile)
        assert ('rhs_stock_loan_consent_status' in profile)

    def test_basic_profile(self):
        profile = r.load_basic_profile(info=None)
        assert profile
        assert ('user' in profile)
        assert ('address' in profile)
        assert ('city' in profile)
        assert ('state' in profile)
        assert ('zipcode' in profile)
        assert ('phone_number' in profile)
        assert ('marital_status' in profile)
        assert ('date_of_birth' in profile)
        assert ('citizenship' in profile)
        assert ('country_of_residence' in profile)
        assert ('number_dependents' in profile)
        assert ('signup_as_rhs' in profile)
        assert ('tax_id_ssn' in profile)
        assert ('updated_at' in profile)

    def test_investment_profile(self):
        profile = r.load_investment_profile(info=None)
        assert profile
        assert ('user' in profile)
        assert ('total_net_worth' in profile)
        assert ('annual_income' in profile)
        assert ('source_of_funds' in profile)
        assert ('investment_objective' in profile)
        assert ('investment_experience' in profile)
        assert ('liquid_net_worth' in profile)
        assert ('risk_tolerance' in profile)
        assert ('tax_bracket' in profile)
        assert ('time_horizon' in profile)
        assert ('liquidity_needs' in profile)
        assert ('investment_experience_collected' in profile)
        assert ('suitability_verified' in profile)
        assert ('option_trading_experience' in profile)
        assert ('professional_trader' in profile)
        assert ('understand_option_spreads' in profile)
        assert ('interested_in_options' in profile)
        assert ('updated_at' in profile)

    def test_portfolio_profile(self):
        profile = r.load_portfolio_profile(info=None)
        assert profile
        assert ('url' in profile)
        assert ('account' in profile)
        assert ('start_date' in profile)
        assert ('market_value' in profile)
        assert ('equity' in profile)
        assert ('extended_hours_market_value' in profile)
        assert ('extended_hours_equity' in profile)
        assert ('extended_hours_portfolio_equity' in profile)
        assert ('last_core_market_value' in profile)
        assert ('last_core_equity' in profile)
        assert ('last_core_portfolio_equity' in profile)
        assert ('excess_margin' in profile)
        assert ('excess_maintenance' in profile)
        assert ('excess_margin_with_uncleared_deposits' in profile)
        assert ('excess_maintenance_with_uncleared_deposits' in profile)
        assert ('equity_previous_close' in profile)
        assert ('portfolio_equity_previous_close' in profile)
        assert ('adjusted_equity_previous_close' in profile)
        assert ('adjusted_portfolio_equity_previous_close' in profile)
        assert ('withdrawable_amount' in profile)
        assert ('unwithdrawable_deposits' in profile)
        assert ('unwithdrawable_grants' in profile)

    def test_security_profile(self):
        profile = r.load_security_profile(info=None)
        assert profile
        assert ('user' in profile)
        assert ('object_to_disclosure' in profile)
        assert ('sweep_consent' in profile)
        assert ('control_person' in profile)
        assert ('control_person_security_symbol' in profile)
        assert ('security_affiliated_employee' in profile)
        assert ('security_affiliated_firm_relationship' in profile)
        assert ('security_affiliated_firm_name' in profile)
        assert ('security_affiliated_person_name' in profile)
        assert ('security_affiliated_address' in profile)
        assert ('security_affiliated_address_subject' in profile)
        assert ('security_affiliated_requires_duplicates' in profile)
        assert ('stock_loan_consent_status' in profile)
        assert ('agreed_to_rhs' in profile)
        assert ('agreed_to_rhs_margin' in profile)
        assert ('rhs_stock_loan_consent_status' in profile)
        assert ('updated_at' in profile)

    def test_user_profile(self):
        profile = r.load_user_profile(info=None)
        assert profile
        assert ('url' in profile)
        assert ('id' in profile)
        assert ('id_info' in profile)
        assert ('username' in profile)
        assert ('email' in profile)
        assert ('email_verified' in profile)
        assert ('first_name' in profile)
        assert ('last_name' in profile)
        assert ('origin' in profile)
        assert ('profile_name' in profile)
        assert ('created_at' in profile)

    def test_crypto_profile(self):
        profile = r.load_crypto_profile(info=None)
        assert profile
        assert ('apex_account_number' in profile)
        assert ('created_at' in profile)
        assert ('id' in profile)
        assert ('rhs_account_number' in profile)
        assert ('status' in profile)
        assert ('status_reason_code' in profile)
        assert ('updated_at' in profile)
        assert ('user_id' in profile)

    @pytest.mark.xfail()
    def test_key_failed(self):
        profile = r.load_account_profile(info='cheese')
        assert profile

    @pytest.mark.xfail()
    def test_login_failed(self):
        r.logout()
        profile = r.load_account_profile(info=None)
        assert profile
