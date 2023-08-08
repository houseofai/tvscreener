import unittest

from tvscreener import StockScreener, CryptoScreener, ForexScreener, TimeInterval


class TestScreener(unittest.TestCase):

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