import robin_stocks.gemini as g

class TestTrades:

    def test_pubticker_btc(self):
        data, err = g.get_pubticker("btcusd")
        assert err == None
        assert data.status_code == 200
