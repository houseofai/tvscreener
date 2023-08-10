import unittest

from tvscreener import ForexScreener, TimeInterval, Region, ForexField, FilterOperator


class TestForexScreener(unittest.TestCase):

    def test_len(self):
        fs = ForexScreener()
        df = fs.get()
        self.assertEqual(150, len(df))

    def test_time_interval(self):
        fs = ForexScreener()
        df = fs.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertEqual(150, len(df))

    def test_region(self):
        fs = ForexScreener()
        fs.add_filter(ForexField.REGION, FilterOperator.EQUAL, Region.AFRICA)
        df = fs.get()
        self.assertEqual(49, len(df))

        self.assertEqual(df.loc[0, "Symbol"], "FX_IDC:GHSNGN")
        self.assertEqual(df.loc[0, "Name"], "GHSNGN")
