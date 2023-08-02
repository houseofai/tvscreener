import unittest

from tvscreener import StockScreener, CryptoScreener, ForexScreener


class TestScreener(unittest.TestCase):

    def test_stockscreener(self):
        ss = StockScreener()
        df = ss.get()
        self.assertTrue(len(df) > 0)

    def test_cryptoscreener(self):
        ss = CryptoScreener()
        df = ss.get()
        self.assertTrue(len(df) > 0)

    def test_forexscreener(self):
        ss = ForexScreener()
        df = ss.get()
        self.assertTrue(len(df) > 0)
