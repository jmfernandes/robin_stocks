import robin_stocks.gemini as g

class TestTrades:

    ticker = "btcusd"

    def test_pubticker_btc(self):
        response, err = g.get_pubticker(self.ticker)
        data = response.json()
        assert err == None
        assert response.status_code == 200
        assert "bid" in data
        assert "ask" in data
        assert "volume" in data
        assert "last" in data


    def test_get_symbols(self):
        response, err = g.get_symbols()
        data = response.json()
        assert err == None
        assert response.status_code == 200
        assert len(data) > 1
        assert self.ticker in data
