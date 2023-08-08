import unittest

from tvscreener import StockScreener


class TestMarkets(unittest.TestCase):
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
