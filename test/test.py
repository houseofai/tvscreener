import unittest

from tvscreener import StockScreener, CryptoScreener, ForexScreener, TimeInterval


class TestScreener(unittest.TestCase):

    def test_set_markets(self):
        ss = StockScreener()
        ss.set_markets("japan", "france")
        self.assertEqual(ss.markets, {"japan", "france"})

    def test_set_markets_unique(self):
        ss = StockScreener()
        ss.set_markets("japan", "japan")
        self.assertEqual(ss.markets, {"japan"})

    def test_set_markets_exception(self):
        ss = StockScreener()
        with self.assertRaises(ValueError):
            ss.set_markets("moon")

    def test_stockscreener(self):
        ss = StockScreener()
        df = ss.get()
        self.assertTrue(len(df) == 150)

    def test_stockscreener_4H(self):
        ss = StockScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertTrue(len(df) == 150)

    def test_cryptoscreener(self):
        ss = CryptoScreener()
        df = ss.get()
        self.assertTrue(len(df) == 150)

    def test_cryptoscreener_4H(self):
        ss = CryptoScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertTrue(len(df) == 150)

    def test_forexscreener(self):
        ss = ForexScreener()
        df = ss.get()
        self.assertTrue(len(df) == 150)

    def test_forexscreener_4H(self):
        ss = ForexScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertTrue(len(df) == 150)

