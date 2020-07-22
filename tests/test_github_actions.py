# Used by git Actions
import os
import robin_stocks as r
import pyotp
import pytest

class TestStocks:
    def test_quotes(self):
        profile_info = r.get_quotes('spy')
        assert profile_info

    def test_name_apple(self):
        name = r.get_name_by_symbol('aapl')
        assert name == "Apple"

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
