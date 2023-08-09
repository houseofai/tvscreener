import unittest

from tvscreener import ForexScreener, TimeInterval, Region


class TestForexScreener(unittest.TestCase):

    def test_len(self):
        ss = ForexScreener()
        df = ss.get()
        self.assertEqual(150, len(df))

    def test_time_interval(self):
        ss = ForexScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertEqual(150, len(df))

    def test_region(self):
        fs = ForexScreener()
        fs.set_regions(Region.AFRICA)
        df = fs.get()
        self.assertEqual(49, len(df))

        self.assertEqual(df.loc[0, "Symbol"], "FX_IDC:GHSNGN")
        self.assertEqual(df.loc[0, "Name"], "GHSNGN")
