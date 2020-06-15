# Used by git Actions
import os
import robin_stocks as r

class TestStocks:
    def test_quotes(self):
        profile_info = r.get_quotes('spy')
        assert profile_info

    def test_name_apple(self):
        name = r.get_name_by_symbol('aapl')
        assert name == "Apple"
