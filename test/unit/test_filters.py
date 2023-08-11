import unittest

from tvscreener import StockScreener, ExtraFilter, FilterOperator, ForexScreener, StockField, ForexField
from tvscreener.field import Market, Country, Exchange, Rating, SymbolType, Type, SubMarket, Region


class TestStockFilters(unittest.TestCase):
    def test_set_markets(self):
        ss = StockScreener()
        ss.set_markets(Market.JAPAN, Market.FRANCE)
        self.assertEqual([Market.JAPAN, Market.FRANCE], ss.markets)

    def test_set_markets_unique(self):
        ss = StockScreener()
        ss.set_markets(Market.JAPAN)
        self.assertEqual([Market.JAPAN], ss.markets)

    def test_set_markets_all(self):
        ss = StockScreener()
        ss.set_markets(Market.ALL)
        self.assertEqual([m for m in Market], ss.markets)

    def test_stock_additional_subtypes(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.COMMON_STOCK)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertTrue(set(SymbolType.COMMON_STOCK.value).issubset(set(subtypes.values)))
        self.assertTrue(set(SymbolType.DEPOSITORY_RECEIPT.value).issubset(set(subtypes.values)))
        self.assertEqual(subtypes.operation, FilterOperator.IN_RANGE)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.STOCK.value, types.values)
        # self.assertIn(Type.DEPOSITORY_RECEIPT.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_depository_subtype(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.DEPOSITORY_RECEIPT)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.DEPOSITORY_RECEIPT.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.DEPOSITORY_RECEIPT.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_etf_subtype(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.ETF)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.ETF.value)
        self.assertEqual(subtypes.operation, FilterOperator.IN_RANGE)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.FUND.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_etn_subtype(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.ETN)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.ETN.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.STRUCTURED.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_mutual_subtype(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.MUTUAL_FUND)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.MUTUAL_FUND.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.FUND.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_preferred_subtype(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.PREFERRED_STOCK)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.PREFERRED_STOCK.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.STOCK.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_reit_subtype(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.REIT)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.REIT.value)
        self.assertEqual(subtypes.operation, FilterOperator.IN_RANGE)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.FUND.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_structured_subtype(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.STRUCTURED)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.STRUCTURED.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.STRUCTURED.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_uit_subtype(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.UIT)
        self.assertEqual(len(ss.filters), 2)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(subtypes.values, SymbolType.UIT.value)
        self.assertEqual(subtypes.operation, FilterOperator.EQUAL)

        types = ss._get_filter(StockField.TYPE)
        self.assertIn(Type.FUND.value, types.values)
        self.assertEqual(types.operation, FilterOperator.EQUAL)

    def test_duplicates(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.UIT)
        ss.set_symbol_types(SymbolType.UIT)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(1, len(subtypes.values))

        types = ss._get_filter(StockField.TYPE)
        self.assertEqual(1, len(types.values))

    def test_double_duplicates(self):
        ss = StockScreener()
        ss.set_symbol_types(SymbolType.UIT)
        ss.set_symbol_types(SymbolType.STRUCTURED)
        ss.set_symbol_types(SymbolType.UIT)
        ss.set_symbol_types(SymbolType.STRUCTURED)

        subtypes = ss._get_filter(StockField.SUBTYPE)
        self.assertEqual(2, len(subtypes.values))

        types = ss._get_filter(StockField.TYPE)
        self.assertEqual(2, len(types.values))

    def test_primary(self):
        ss = StockScreener()
        ss.add_filter(ExtraFilter.PRIMARY, FilterOperator.EQUAL, True)
        self.assertEqual(len(ss.filters), 1)

        subtypes = ss._get_filter(ExtraFilter.PRIMARY)
        self.assertEqual(1, len(subtypes.values))
        self.assertEqual(True, subtypes.values[0])

    def test_submarkets(self):
        ss = StockScreener()
        ss.add_filter(StockField.SUBMARKET, FilterOperator.EQUAL, SubMarket.PINK)
        self.assertEqual(len(ss.filters), 1)
        ss.add_filter(StockField.SUBMARKET, FilterOperator.EQUAL, SubMarket.PINK)
        self.assertEqual(len(ss.filters), 1)
        ss.add_filter(StockField.SUBMARKET, FilterOperator.EQUAL, SubMarket.OTCQB)

        subtypes = ss._get_filter(StockField.SUBMARKET)
        self.assertEqual(2, len(subtypes.values))
        self.assertEqual([SubMarket.PINK, SubMarket.OTCQB], subtypes.values)

    def test_country(self):
        ss = StockScreener()
        ss.add_filter(StockField.COUNTRY, FilterOperator.EQUAL, Country.ARGENTINA)
        self.assertEqual(len(ss.filters), 1)

        country = ss._get_filter(StockField.COUNTRY)
        self.assertEqual(1, len(country.values))
        self.assertEqual(Country.ARGENTINA, country.values[0])

    def test_countries(self):
        ss = StockScreener()
        ss.add_filter(StockField.COUNTRY, FilterOperator.EQUAL, Country.ARGENTINA)
        ss.add_filter(StockField.COUNTRY, FilterOperator.EQUAL, Country.BERMUDA)
        self.assertEqual(len(ss.filters), 1)

        country = ss._get_filter(StockField.COUNTRY)
        self.assertEqual(2, len(country.values))
        self.assertEqual(Country.ARGENTINA, country.values[0])
        self.assertEqual(Country.BERMUDA, country.values[1])

    def test_exchange(self):
        ss = StockScreener()
        ss.add_filter(StockField.EXCHANGE, FilterOperator.EQUAL, Exchange.NASDAQ)
        self.assertEqual(len(ss.filters), 1)

        exchange = ss._get_filter(StockField.EXCHANGE)
        self.assertEqual(1, len(exchange.values))
        self.assertEqual(Exchange.NASDAQ, exchange.values[0])

    def test_exchanges(self):
        ss = StockScreener()
        ss.add_filter(StockField.EXCHANGE, FilterOperator.EQUAL, Exchange.NASDAQ)
        ss.add_filter(StockField.EXCHANGE, FilterOperator.EQUAL, Exchange.NYSE)
        self.assertEqual(len(ss.filters), 1)

        exchange = ss._get_filter(StockField.EXCHANGE)
        self.assertEqual(2, len(exchange.values))
        self.assertEqual(Exchange.NASDAQ, exchange.values[0])
        self.assertEqual(Exchange.NYSE, exchange.values[1])

    def test_stockmarket_names(self):
        self.assertIn("GREECE", Market.names())

    def test_stockmarket_values(self):
        self.assertIn("venezuela", Market.values())

    def test_rating(self):
        self.assertIn(0.63, Rating.STRONG_BUY)
        self.assertNotIn(0.4, Rating.STRONG_SELL)

    def test_rating_range(self):
        self.assertEqual([-0.5, -0.1], Rating.SELL.range())

    def test_rating_find(self):
        self.assertEqual(Rating.STRONG_BUY, Rating.find(0.63))
        self.assertEqual(Rating.UNKNOWN, Rating.find(1.5))
        self.assertEqual(Rating.UNKNOWN, Rating.find(None))

    def test_rating_names(self):
        self.assertIn("STRONG_BUY", Rating.names())

    def test_rating_values(self):
        self.assertIn(Rating.STRONG_BUY.value, Rating.values())

    def test_current_trading_days(self):
        ss = StockScreener()
        ss.add_filter(ExtraFilter.CURRENT_TRADING_DAY, FilterOperator.EQUAL, True)
        self.assertEqual(len(ss.filters), 1)

        current_trading_day = ss._get_filter(ExtraFilter.CURRENT_TRADING_DAY)
        self.assertEqual(True, current_trading_day.values[0])


class TestForexFilters(unittest.TestCase):
    def test_region(self):
        ss = ForexScreener()
        ss.add_filter(ForexField.REGION, FilterOperator.EQUAL, Region.AFRICA)
        self.assertEqual(len(ss.filters), 1)

        region = ss._get_filter(ForexField.REGION)
        self.assertEqual(1, len(region.values))
        self.assertEqual(Region.AFRICA, region.values[0])
