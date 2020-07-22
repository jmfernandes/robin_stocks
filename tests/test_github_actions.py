# Used by git Actions
import os
import robin_stocks as r
import pyotp

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
        totp  = pyotp.TOTP(robin_mfa).now()
        login = r.login(robin_username, robin_password, mfa_code=totp)

    @classmethod
    def teardown_class(cls):
        r.logout()

    def test_load_account_profile(self):
        info = r.load_account_profile()
        assert info
