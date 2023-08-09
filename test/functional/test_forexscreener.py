import unittest

from tvscreener import ForexScreener, TimeInterval


class TestForexScreener(unittest.TestCase):

    def test_len(self):
        ss = ForexScreener()
        df = ss.get()
        self.assertEqual(150, len(df))

    def test_time_interval(self):
        ss = ForexScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertEqual(150, len(df))
