import unittest

from tvscreener import StockField, TimeInterval, get_columns_to_request


class TestUtil(unittest.TestCase):

    def test_get_columns_type(self):
        columns = get_columns_to_request(StockField, TimeInterval.ONE_DAY)
        self.assertIsInstance(columns, dict)
        self.assertEqual(len(columns), 301)

    def test_get_columns_len(self):
        columns = get_columns_to_request(StockField, TimeInterval.ONE_DAY)
        self.assertIsInstance(columns, dict)

