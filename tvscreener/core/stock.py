from tvscreener.core.base import Screener, default_market, default_sort_stocks
from tvscreener.field import Market, Type, SymbolType
from tvscreener.field.stock import StockField
from tvscreener.filter import FilterOperator
from tvscreener.util import get_url


class StockScreener(Screener):

    def __init__(self):
        super().__init__()
        # subtype = "stock"
        self.markets = [default_market]

        self.url = get_url("global")
        self.specific_fields = StockField  # {**self.columns, **tvdata.stock['columns']}
        self.sort_by(default_sort_stocks, False)

    def _build_payload(self, requested_columns_):
        payload = super()._build_payload(requested_columns_)
        if self.markets:
            payload["markets"] = [market.value for market in self.markets]
        return payload

    def _add_types(self, *types: Type):
        if len(types) > 1:
            operator = FilterOperator.IN_RANGE
        else:
            operator = FilterOperator.EQUAL

        for type_ in types:
            self.add_filter(StockField.TYPE, operator, type_.value)

    def set_symbol_types(self, *symbol_types: SymbolType):
        """
        Set the subtypes to be scanned
        :param symbol_types: list of subtypes
        :return: None
        """

        # If subtype is COMMON_STOCK, add STOCK to types
        if SymbolType.COMMON_STOCK in symbol_types:
            self._add_types(Type.STOCK)

        if SymbolType.DEPOSITORY_RECEIPT in symbol_types:
            self._add_types(Type.DEPOSITORY_RECEIPT)

        if SymbolType.ETF in symbol_types:
            self._add_types(Type.FUND)

        if SymbolType.MUTUAL_FUND in symbol_types:
            self._add_types(Type.FUND)

        if SymbolType.REIT in symbol_types:
            self._add_types(Type.FUND)

        if SymbolType.PREFERRED_STOCK in symbol_types:
            self._add_types(Type.STOCK)

        if SymbolType.ETN in symbol_types:
            self._add_types(Type.STRUCTURED)

        if SymbolType.STRUCTURED in symbol_types:
            self._add_types(Type.STRUCTURED)

        if SymbolType.UIT in symbol_types:
            self._add_types(Type.FUND)

        # If subtype is COMMON_STOCK and DEPOSITARY_RECEIPT not in subtypes add DEPOSITARY_RECEIPT to subtypes
        if SymbolType.COMMON_STOCK in symbol_types and SymbolType.DEPOSITORY_RECEIPT not in symbol_types:
            symbol_types = list(symbol_types)
            symbol_types.append(SymbolType.DEPOSITORY_RECEIPT)

        for symbol_type in symbol_types:
            self.add_filter(StockField.SUBTYPE, FilterOperator.IN_RANGE, symbol_type.value.copy())

    def set_markets(self, *markets: Market):
        """
        Set the markets to be scanned
        :param markets: list of markets
        :return: None
        """
        if Market.ALL in markets:
            self.markets = [market for market in Market]
        else:
            self.markets = [market for market in markets]
