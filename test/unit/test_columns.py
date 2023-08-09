import unittest

from tvscreener import StockField
from tvscreener.field import add_time_interval, TimeInterval, add_historical
from tvscreener.util import format_historical_field


class TestColumns(unittest.TestCase):

    def test_hist_1(self):
        field = format_historical_field(StockField.NEGATIVE_DIRECTIONAL_INDICATOR_14, TimeInterval.ONE_DAY)
        self.assertEqual(field, "ADX-DI[1]")

    def test_hist_2(self):
        field = format_historical_field(StockField.NEGATIVE_DIRECTIONAL_INDICATOR_14, TimeInterval.ONE_DAY, 2)
        self.assertEqual(field, "ADX-DI[2]")

    def test_hist_time_interval(self):
        field = format_historical_field(StockField.NEGATIVE_DIRECTIONAL_INDICATOR_14, TimeInterval.ONE_WEEK, 1)
        self.assertEqual(field, "ADX-DI[1]|1W")

    def test_add_time_interval(self):
        field = add_time_interval("change", TimeInterval.ONE_DAY)
        self.assertEqual(field, "change|1D")

    def test_add_historical(self):
        field = add_historical(StockField.POSITIVE_DIRECTIONAL_INDICATOR_14.field_name)
        self.assertEqual(field, "ADX+DI[1]")

    def test_add_historical_2(self):
        field = add_historical(StockField.POSITIVE_DIRECTIONAL_INDICATOR_14.field_name, 2)
        self.assertEqual(field, "ADX+DI[2]")
