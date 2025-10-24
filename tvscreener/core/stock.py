from tvscreener.core.base import Screener, default_market, default_sort_stocks
from tvscreener.field import Market, Type, SymbolType
from tvscreener.field.stock import StockField
from tvscreener.filter import FilterOperator
from tvscreener.util import get_url

# Mapping from SymbolType to Type for efficient lookup
SYMBOL_TYPE_TO_TYPE_MAP = {
    SymbolType.COMMON_STOCK: Type.STOCK,
    SymbolType.DEPOSITORY_RECEIPT: Type.DEPOSITORY_RECEIPT,
    SymbolType.ETF: Type.FUND,
    SymbolType.MUTUAL_FUND: Type.FUND,
    SymbolType.REIT: Type.FUND,
    SymbolType.PREFERRED_STOCK: Type.STOCK,
    SymbolType.ETN: Type.STRUCTURED,
    SymbolType.STRUCTURED: Type.STRUCTURED,
    SymbolType.UIT: Type.FUND,
}


class StockScreener(Screener):
    """Stock screener for querying stocks from TradingView."""

    def __init__(self):
        super().__init__()
        self.markets = [default_market]
        self.url = get_url("global")
        self.specific_fields = StockField
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
        Set the symbol types to be scanned.

        :param symbol_types: Symbol types to include in the screener results
        :raises ValueError: If an unknown symbol type is provided
        """
        # Validate all symbol types are known
        unknown_types = [st for st in symbol_types if st not in SYMBOL_TYPE_TO_TYPE_MAP]
        if unknown_types:
            raise ValueError(f"Unknown symbol types: {unknown_types}")

        # Collect unique Type values from symbol_types
        types_to_add = {SYMBOL_TYPE_TO_TYPE_MAP[symbol_type] for symbol_type in symbol_types}

        # Add Type filters (use IN_RANGE if multiple types, otherwise EQUAL)
        if types_to_add:
            self._add_types(*types_to_add)

        # Special case: COMMON_STOCK automatically includes DEPOSITORY_RECEIPT
        # This maintains backward compatibility with existing behavior
        symbol_types_list = list(symbol_types)
        if SymbolType.COMMON_STOCK in symbol_types and SymbolType.DEPOSITORY_RECEIPT not in symbol_types:
            symbol_types_list.append(SymbolType.DEPOSITORY_RECEIPT)

        # Add subtype filters
        for symbol_type in symbol_types_list:
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
