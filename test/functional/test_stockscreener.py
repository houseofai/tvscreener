import io
import unittest
from unittest.mock import patch

import pandas as pd

from tvscreener import StockScreener, TimeInterval, SymbolType, SubMarket, Country, Exchange, MalformedRequestException, \
    ExtraFilter, FilterOperator, StocksMarket, StockField


class TestScreener(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_stdout(self, mock_stdout):
        ss = StockScreener()
        ss.get(print_request=True)
        self.assertIn("filter", mock_stdout.getvalue())

    def test_malformed_request(self):
        ss = StockScreener()
        ss.add_filter(StockField.TYPE, FilterOperator.ABOVE_OR_EQUAL, "test")
        with self.assertRaises(MalformedRequestException):
            ss.get()

    def test_range(self):
        ss = StockScreener()
        df = ss.get()
        self.assertEqual(150, len(df))

    def test_time_interval(self):
        ss = StockScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertEqual(150, len(df))

    def test_search(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.COMMON_STOCK)
        ss.search('AA')
        df = ss.get()
        self.assertEqual(102, len(df))

        self.assertEqual(df.loc[0, "Symbol"], "NASDAQ:AAPL")
        self.assertEqual(df.loc[0, "Name"], "AAPL")

    def test_column_order(self):
        ss = StockScreener()
        df = ss.get()

        self.assertEqual(df.columns[0], "Symbol")
        self.assertEqual(df.columns[1], "Name")
        self.assertEqual(df.columns[2], "Description")

        self.assertEqual(df.loc[0, "Symbol"], "NASDAQ:AAPL")
        self.assertEqual(df.loc[0, "Name"], "AAPL")

    def test_not_multiindex(self):
        ss = StockScreener()
        df = ss.get()
        self.assertIsInstance(df.index, pd.Index)

        self.assertEqual("Symbol", df.columns[0])
        self.assertEqual("Name", df.columns[1])
        self.assertEqual("Description", df.columns[2])

        self.assertEqual("NASDAQ:AAPL", df.loc[0, "Symbol"])
        self.assertEqual("AAPL", df.loc[0, "Name"])

    def test_multiindex(self):
        ss = StockScreener()
        df = ss.get()
        df.set_technical_columns()
        self.assertNotIsInstance(df.index, pd.MultiIndex)

        self.assertEqual(("symbol", "Symbol"), df.columns[0])
        self.assertEqual(("name", "Name"), df.columns[1])
        self.assertEqual(("description", "Description"), df.columns[2])

        self.assertEqual("NASDAQ:AAPL", df.loc[0, ("symbol", "Symbol")])
        self.assertEqual("AAPL", df.loc[0, ("name", "Name")])

    def test_technical_index(self):
        ss = StockScreener()
        df = ss.get()
        df.set_technical_columns(only=True)
        self.assertIsInstance(df.index, pd.Index)

        self.assertEqual(df.columns[0], "symbol")
        self.assertEqual(df.columns[1], "name")
        self.assertEqual(df.columns[2], "description")

        self.assertEqual("NASDAQ:AAPL", df.loc[0, "symbol"])
        self.assertEqual("AAPL", df.loc[0, "name"])

    def test_primary_filter(self):
        ss = StockScreener()
        ss.add_filter(ExtraFilter.PRIMARY, FilterOperator.EQUAL, True)
        df = ss.get()
        self.assertEqual(150, len(df))

        self.assertEqual("NASDAQ:AAPL", df.loc[0, "Symbol"])
        self.assertEqual("AAPL", df.loc[0, "Name"])

    def test_market(self):
        ss = StockScreener()
        ss.set_markets(StocksMarket.ARGENTINA)
        df = ss.get()
        self.assertEqual(150, len(df))

        self.assertEqual("BCBA:AAPL", df.loc[0, "Symbol"], )
        self.assertEqual("AAPL", df.loc[0, "Name"])

    def test_submarket(self):
        ss = StockScreener()
        ss.add_filter(StockField.SUBMARKET, FilterOperator.EQUAL, SubMarket.OTCQB)
        df = ss.get()
        self.assertEqual(150, len(df))

        self.assertEqual("OTC:PLDGP", df.loc[0, "Symbol"])
        self.assertEqual("PLDGP", df.loc[0, "Name"])

    def test_submarket_pink(self):
        ss = StockScreener()
        ss.add_filter(StockField.SUBMARKET, FilterOperator.EQUAL, SubMarket.PINK)
        df = ss.get()
        self.assertEqual(150, len(df))

        self.assertEqual("OTC:LVMHF", df.loc[0, "Symbol"])
        self.assertEqual("LVMHF", df.loc[0, "Name"])

    def test_country(self):
        ss = StockScreener()
        ss.add_filter(StockField.COUNTRY, FilterOperator.EQUAL, Country.ARGENTINA)
        df = ss.get()
        self.assertEqual(17, len(df))

        self.assertEqual("NYSE:YPF", df.loc[0, "Symbol"])
        self.assertEqual("YPF", df.loc[0, "Name"])

    def test_countries(self):
        ss = StockScreener()
        ss.add_filter(StockField.COUNTRY, FilterOperator.EQUAL, Country.ARGENTINA)
        ss.add_filter(StockField.COUNTRY, FilterOperator.EQUAL, Country.BERMUDA)
        df = ss.get()
        self.assertEqual(106, len(df))

        # WARNING: Order is not guaranteed
        # self.assertEqual("NASDAQ:ACGL", df.loc[0, "Symbol"])
        # self.assertEqual("ACGL", df.loc[0, "Name"])

    def test_exchange(self):
        ss = StockScreener()
        ss.add_filter(StockField.EXCHANGE, FilterOperator.EQUAL, Exchange.NYSE_ARCA)
        df = ss.get()
        self.assertEqual(150, len(df))

        self.assertEqual("AMEX:LNG", df.loc[0, "Symbol"])
        self.assertEqual("LNG", df.loc[0, "Name"])

    def test_current_trading_day(self):
        ss = StockScreener()
        ss.add_filter(ExtraFilter.CURRENT_TRADING_DAY, FilterOperator.EQUAL, True)
        df = ss.get()
        self.assertEqual(150, len(df))

        self.assertEqual("NASDAQ:AAPL", df.loc[0, "Symbol"])
        self.assertEqual("AAPL", df.loc[0, "Name"])
