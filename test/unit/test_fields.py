import unittest

from tvscreener import StockField


class TestFields(unittest.TestCase):

    def test_recommendation(self):
        self.assertTrue(StockField.BULL_BEAR_POWER.has_recommendation())

    def test_historical(self):
        self.assertTrue(StockField.NEGATIVE_DIRECTIONAL_INDICATOR_14.historical)
        self.assertTrue(StockField.COMMODITY_CHANNEL_INDEX_20.historical)
        self.assertTrue(StockField.MOMENTUM_10.historical)

    def test_interval(self):
        self.assertTrue(StockField.VOLUME.interval)
        self.assertTrue(StockField.AVERAGE_DIRECTIONAL_INDEX_14.interval)
        self.assertTrue(StockField.NEGATIVE_DIRECTIONAL_INDICATOR_14.interval)
        self.assertTrue(StockField.POSITIVE_DIRECTIONAL_INDICATOR_14.interval)

    def test_format_computed_reco(self):
        self.assertTrue(StockField.AVERAGE_DIRECTIONAL_INDEX_14.format == "computed_recommendation")
        self.assertTrue(StockField.BOLLINGER_LOWER_BAND_20.format == "computed_recommendation")
        self.assertTrue(StockField.BOLLINGER_UPPER_BAND_20.format == "computed_recommendation")
        self.assertTrue(StockField.SIMPLE_MOVING_AVERAGE_10.format == "computed_recommendation")

