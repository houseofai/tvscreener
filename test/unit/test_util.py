import unittest

from tvscreener import StockField, TimeInterval, get_columns_to_request, get_recommendation, millify


class TestUtil(unittest.TestCase):

    def test_get_columns_type(self):
        columns = get_columns_to_request(StockField, TimeInterval.ONE_DAY)
        self.assertIsInstance(columns, dict)
        self.assertEqual(len(columns), 301)

    def test_get_columns_len(self):
        columns = get_columns_to_request(StockField, TimeInterval.ONE_DAY)
        self.assertIsInstance(columns, dict)

    def test_get_recommendation(self):
        self.assertEqual("S", get_recommendation(-1))
        self.assertEqual("N", get_recommendation(0))
        self.assertEqual("B", get_recommendation(1))

    def test_millify(self):
        self.assertEqual("1.000M", millify(10 ** 6))
        self.assertEqual("10.000M", millify(10 ** 7))
        self.assertEqual("1.000B", millify(10 ** 9))
