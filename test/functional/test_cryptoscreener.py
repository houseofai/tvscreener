import unittest

from tvscreener import CryptoScreener, TimeInterval


class TestScreener(unittest.TestCase):

    def test_range(self):
        ss = CryptoScreener()
        df = ss.get()
        self.assertEqual(150, len(df))

    def test_timeinterval(self):
        ss = CryptoScreener()
        df = ss.get(time_interval=TimeInterval.FOUR_HOURS)
        self.assertEqual(150, len(df))
