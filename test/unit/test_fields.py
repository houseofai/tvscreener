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
        self.assertEqual("computed_recommendation", StockField.AVERAGE_DIRECTIONAL_INDEX_14.format)
        self.assertEqual("computed_recommendation", StockField.BOLLINGER_LOWER_BAND_20.format)
        self.assertEqual("computed_recommendation", StockField.BOLLINGER_UPPER_BAND_20.format)
        self.assertEqual("computed_recommendation", StockField.SIMPLE_MOVING_AVERAGE_10.format)

    def test_rec_label(self):
        self.assertEqual(None, StockField.AVERAGE_DIRECTIONAL_INDEX_14.get_rec_label())
        self.assertEqual("Reco. Bull Bear Power", StockField.BULL_BEAR_POWER.get_rec_label())
        self.assertEqual("Reco. Hull Moving Average (9)", StockField.HULL_MOVING_AVERAGE_9.get_rec_label())
        self.assertEqual("Reco. Ultimate Oscillator (7, 14, 28)", StockField.ULTIMATE_OSCILLATOR_7_14_28.get_rec_label())

    def test_get_by_label(self):
        self.assertEqual(StockField.VOLUME, StockField.get_by_label(StockField, StockField.VOLUME.label))
