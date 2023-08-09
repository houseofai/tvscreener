import unittest

from tvscreener import StockScreener, Type, FilterType, SymbolType, FilterOperator


class TestFilters(unittest.TestCase):

    def test_stock_additional_subtypes(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.COMMON_STOCK)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertTrue(set(SymbolType.COMMON_STOCK.value).issubset(set(subtypes.values)))
        self.assertTrue(set(SymbolType.DEPOSITORY_RECEIPT.value).issubset(set(subtypes.values)))
        self.assertEqual(subtypes.operation, FilterOperator.IN_RANGE)

        types = ss._get_filter(FilterType.TYPE)
        self.assertIn(Type.STOCK.value, types.values)
        self.assertIn(Type.DEPOSITORY_RECEIPT.value, types.values)
        self.assertEqual(types.operation, FilterOperator.IN_RANGE)

    def test_depository_subtype(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.DEPOSITORY_RECEIPT)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.DEPOSITORY_RECEIPT.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(FilterType.TYPE)
        self.assertIn(Type.DEPOSITORY_RECEIPT.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_etf_subtype(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.ETF)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.ETF.value)
        self.assertEqual(subtypes.operation, FilterOperator.IN_RANGE)

        types = ss._get_filter(FilterType.TYPE)
        self.assertIn(Type.FUND.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_etn_subtype(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.ETN)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.ETN.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(FilterType.TYPE)
        self.assertIn(Type.STRUCTURED.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_preferred_subtype(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.PREFERRED_STOCK)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.PREFERRED_STOCK.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(FilterType.TYPE)
        self.assertIn(Type.STOCK.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_reit_subtype(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.REIT)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.REIT.value)
        self.assertEqual(subtypes.operation, FilterOperator.IN_RANGE)

        types = ss._get_filter(FilterType.TYPE)
        self.assertIn(Type.FUND.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_structured_subtype(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.STRUCTURED)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(subtypes.values,   SymbolType.STRUCTURED.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(FilterType.TYPE)
        self.assertIn(Type.STRUCTURED.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_uit_subtype(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.UIT)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.UIT.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(FilterType.TYPE)
        self.assertIn(Type.FUND.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_duplicates(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.UIT)
        ss.set_subtypes(SymbolType.UIT)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(1, len(subtypes.values))

        types = ss._get_filter(FilterType.TYPE)
        self.assertEqual(1, len(types.values))

    def test_double_duplicates(self):
        ss = StockScreener()
        ss.set_subtypes(SymbolType.UIT)
        ss.set_subtypes(SymbolType.STRUCTURED)
        ss.set_subtypes(SymbolType.UIT)
        ss.set_subtypes(SymbolType.STRUCTURED)

        subtypes = ss._get_filter(FilterType.SUBTYPE)
        self.assertEqual(2, len(subtypes.values))

        types = ss._get_filter(FilterType.TYPE)
        self.assertEqual(2, len(types.values))
