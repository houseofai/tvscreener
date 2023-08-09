import unittest

import pandas as pd

from tvscreener import StockScreener, TimeInterval, SymbolType


class TestScreener(unittest.TestCase):

    def test_stockscreener(self):
        ss = StockScreener()
        df = ss.get()
        self.assertEqual(150, len(df))

    def test_stockscreener_4H(self):
        ss = StockScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertEqual(150, len(df))

    def test_search(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.COMMON_STOCK)
        ss.search('AA')
        df = ss.get()
        self.assertEqual(102, len(df))

        self.assertEqual(df.loc[0, "Symbol"], "NASDAQ:AAPL")
        self.assertEqual(df.loc[0, "Name"], "AAPL")

    def test_stockscreener_column_order(self):
        ss = StockScreener()
        df = ss.get()

        self.assertEqual(df.columns[0], "Symbol")
        self.assertEqual(df.columns[1], "Name")
        self.assertEqual(df.columns[2], "Description")

        self.assertEqual(df.loc[0, "Symbol"], "NASDAQ:AAPL")
        self.assertEqual(df.loc[0, "Name"], "AAPL")

    def test_stockscreener_not_multiindex(self):
        ss = StockScreener()
        df = ss.get()
        self.assertIsInstance(df.index, pd.Index)

        self.assertEqual(df.columns[0], "Symbol")
        self.assertEqual(df.columns[1], "Name")
        self.assertEqual(df.columns[2], "Description")

        self.assertEqual(df.loc[0, "Symbol"], "NASDAQ:AAPL")
        self.assertEqual(df.loc[0, "Name"], "AAPL")

    def test_stockscreener_multiindex(self):
        ss = StockScreener()
        df = ss.get()
        df.set_technical_columns()
        self.assertNotIsInstance(df.index, pd.MultiIndex)

        self.assertEqual(df.columns[0], ("symbol", "Symbol"))
        self.assertEqual(df.columns[1], ("name", "Name"))
        self.assertEqual(df.columns[2], ("description", "Description"))

        self.assertEqual(df.loc[0, ("symbol", "Symbol")], "NASDAQ:AAPL")
        self.assertEqual(df.loc[0, ("name", "Name")], "AAPL")

    def test_stockscreener_technical_index(self):
        ss = StockScreener()
        df = ss.get()
        df.set_technical_columns(only=True)
        self.assertIsInstance(df.index, pd.Index)

        self.assertEqual(df.columns[0], "symbol")
        self.assertEqual(df.columns[1], "name")
        self.assertEqual(df.columns[2], "description")

        self.assertEqual(df.loc[0, "symbol"], "NASDAQ:AAPL")
        self.assertEqual(df.loc[0, "name"], "AAPL")
