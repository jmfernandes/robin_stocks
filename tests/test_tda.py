import os

import robin_stocks.tda as t
from dotenv import load_dotenv

load_dotenv()


class TestAuthentication:

    def test_login(self):
        t.login(os.environ['tda_encryption_passcode'])
        assert t.get_login_state()

class TestStocks:

    ticker = "TSLA"

    @classmethod
    def setup_class(cls):
        t.login(os.environ['tda_encryption_passcode'])

    def test_quote(self):
        resp, err = t.get_quote(self.ticker)
        data = resp.json()
        assert resp.status_code == 200
        assert err is None
        assert self.ticker in data

