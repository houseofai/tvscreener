import unittest

from tvscreener import StockScreener, TimeInterval, SymbolType


class TestScreener(unittest.TestCase):

    def test_stockscreener(self):
        ss = StockScreener()
        df = ss.get()
        self.assertEqual(len(df), 150)

    def test_stockscreener_4H(self):
        ss = StockScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertEqual(len(df), 150)

    def test_search(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.COMMON_STOCK)
        ss.search('AA')
        df = ss.get(print_request=True)
        self.assertEqual(len(df), 122)

