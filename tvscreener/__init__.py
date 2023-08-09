import json
from typing import List

import pandas as pd
import requests

from tvscreener.field import TimeInterval, Field
from tvscreener.field.crypto import CryptoField
from tvscreener.field.forex import ForexField
from tvscreener.field.stock import StockField
from tvscreener.filter import FilterOperator, Filter, Rating, StocksMarket, FilterType, SymbolType, Type, SubMarket, \
    Country, Exchange, Region
from tvscreener.util import get_columns_to_request, is_status_code_ok, get_url, millify, get_recommendation, \
    MalformedRequestException

default_market = ["america"]
default_min_range = 0
default_max_range = 150
default_sort_stocks = "market_cap_basic"
default_sort_crypto = "24h_vol|5"
default_sort_forex = "name"


class ScreenerDataFrame(pd.DataFrame):
    def __init__(self, data, columns: dict, *args, **kwargs):
        # Add the extra received columns
        columns = {"symbol": "Symbol", **columns}
        super().__init__(data, columns=columns.values(), *args, **kwargs)

        # Reorder columns
        first_columns = ['symbol', 'name', 'description']
        ordered_columns = {k: columns.get(k) for k in first_columns}
        ordered_columns.update({k: v for k, v in columns.items() if k not in first_columns})
        self.attrs['original_columns'] = ordered_columns
        self._update_inplace(self[ordered_columns.values()])

    def set_technical_columns(self, only: bool = False):
        if only:
            self.columns = pd.Index(self.attrs['original_columns'].keys())
        else:
            self.columns = pd.MultiIndex.from_tuples(self.attrs['original_columns'].items())


class Screener:

    def __init__(self):
        self.sort = None
        self.url = None
        self.filters = []
        self.options = {}
        self.symbols = None
        self.misc = {}
        self.specific_fields = None

        self.range = None
        self.set_range()
        self.add_option("lang", "en")

    # def add_prebuilt_filter(self, filter_: Filter):
    #    self.filters.append(filter_.to_dict())

    # def add_filter(self, filter_: Filter, operation: FilterOperator = None, values=None):
    #    filter_val = {"left": filter_, "operation": operation.value, "right": values}
    #    self.filters.append(filter_val)

    def search(self, value: str):
        self.add_filter(Filter(FilterType.SEARCH, FilterOperator.MATCH, value))

    def _get_filter(self, filter_type: FilterType) -> Filter:
        for filter_ in self.filters:
            if filter_.filter_type == filter_type:
                return filter_

    def remove_filter(self, filter_type: FilterType):
        self.filters = [filter_ for filter_ in self.filters if filter_.filter_type != filter_type]

    @staticmethod
    def _merge_filters(current_filter: Filter, new_filter: Filter):
        if not set(new_filter.values).issubset(set(current_filter.values)):
            # Set the operation is IN_RANGE with multiple values
            current_filter.operation = FilterOperator.IN_RANGE
            current_filter.values.extend(new_filter.values)
        return current_filter

    def _add_new_filter(self, filter_: Filter):
        # Case where the filter does not exist
        # If the filter contains values array with only one value, we can use EQUAL instead of IN_RANGE
        if len(filter_.values) == 1 and filter_.operation == FilterOperator.IN_RANGE:
            filter_.operation = FilterOperator.EQUAL
        self.filters.append(filter_)

    def add_filter(self, filter_: Filter):
        # filter_val = {"left": filter_, "operation": operation.value, "right": values}
        # Case where the filter already exists, and we want to add more values
        existing_filter = self._get_filter(filter_.filter_type)
        if existing_filter:
            self._merge_filters(existing_filter, filter_)
        else:
            self._add_new_filter(filter_)

    def add_option(self, key, value):
        self.options[key] = value

    def add_misc(self, key, value):
        self.misc[key] = value

    def set_range(self, from_range: int = default_min_range, to_range: int = default_max_range) -> None:
        self.range = [from_range, to_range]

    def sort_by(self, sort_by, order="desc"):
        self.sort = {"sortBy": sort_by, "sortOrder": order}

    def _build_payload(self, requested_columns_):
        payload = {
            "filter": [f.to_dict() for f in self.filters],
            "options": self.options,
            "symbols": self.symbols if self.symbols else {"query": {"types": []}, "tickers": []},
            "sort": self.sort,
            "range": self.range,
            "columns": requested_columns_,
            **self.misc
        }
        return payload

    def get(self, time_interval=TimeInterval.ONE_DAY, print_request=False):

        # Build columns
        columns = get_columns_to_request(self.specific_fields, time_interval)

        payload = self._build_payload(list(columns.keys()))
        payload = json.dumps(payload, indent=4)

        if print_request:
            print(f"Request: {self.url}")
            print("Payload:")
            print(payload)

        response = requests.post(self.url, data=payload)
        if is_status_code_ok(response):
            data = [[d["s"]] + d["d"] for d in response.json()['data']]
            return ScreenerDataFrame(data, columns)
        else:
            raise MalformedRequestException(response.status_code, response.text, self.url, payload)


class StockScreener(Screener):

    def __init__(self):
        super().__init__()
        # subtype = "stock"
        self.markets = set(default_market)

        self.url = get_url("global")
        self.specific_fields = StockField  # {**self.columns, **tvdata.stock['columns']}
        self.sort_by(default_sort_stocks, "desc")

    def _build_payload(self, requested_columns_):
        payload = super()._build_payload(requested_columns_)
        if self.markets:
            payload["markets"] = list(self.markets)
        return payload

    def set_subtypes(self, *symbol_types: SymbolType):
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
            self.add_filter(Filter(FilterType.SUBTYPE, FilterOperator.IN_RANGE, symbol_type.value.copy()))

    def set_markets(self, *markets):
        """
        Set the markets to be scanned
        :param markets: list of markets
        :return: None
        """
        self.markets = set()
        market_labels = [market.value for market in StocksMarket]
        for market in markets:
            if market not in market_labels:
                raise ValueError(f"Unknown market: {market}")
            self.markets.add(market)

    def set_submarkets(self, *submarkets: SubMarket):
        """
        Set the submarkets to be scanned
        :param submarkets: list of submarkets
        :return: None
        """
        for submarket in submarkets:
            self.add_filter(Filter(FilterType.SUBMARKET, FilterOperator.EQUAL, submarket.value))

    def set_primary_listing(self, primary: bool = True):
        """
        Set the primary filter
        :param primary: True or False
        :return: None
        """
        if primary:
            self.add_filter(Filter(FilterType.PRIMARY, FilterOperator.EQUAL, True))
        else:
            self.remove_filter(FilterType.PRIMARY)

    def _add_types(self, *types: Type):
        if len(types) > 1:
            operator = FilterOperator.IN_RANGE
        else:
            operator = FilterOperator.EQUAL

        for type_ in types:
            self.add_filter(Filter(FilterType.TYPE, operator, type_.value))

    def set_countries(self, *countries: Country):
        """
        Set the country to be scanned
        :param countries: list of countries
        :return: None
        """
        for country in countries:
            self.add_filter(Filter(FilterType.COUNTRY, FilterOperator.EQUAL, country.value))

    def set_exchanges(self, *exchanges: Exchange):
        """
        Set the exchanges to be scanned
        :param exchanges: list of exchanges
        :return: None
        """
        for exchange in exchanges:
            self.add_filter(Filter(FilterType.EXCHANGE, FilterOperator.EQUAL, exchange.value))


class ForexScreener(Screener):
    def __init__(self):
        super().__init__()
        subtype = "forex"
        self.url = get_url(subtype)
        self.markets = set(subtype)
        self.specific_fields = ForexField  # {**self.fields, **tvdata.forex['columns']}
        # self.add_filter("sector", FilterOperation.IN_RANGE, ['Major', 'Minor'])
        self.sort_by(default_sort_forex, "asc")
        self.add_misc("symbols", {"query": {"types": ["forex"]}})

    def set_regions(self, *regions: Region):
        """
        Set the regions to be scanned
        :param regions: list of regions
        :return: None
        """
        for region in regions:
            self.add_filter(Filter(FilterType.REGION, FilterOperator.EQUAL, region.value))


class CryptoScreener(Screener):
    def __init__(self):
        super().__init__()
        subtype = "crypto"
        self.markets = set(subtype)
        self.url = get_url(subtype)
        self.specific_fields = CryptoField
        self.sort_by(default_sort_crypto, "desc")
        self.add_misc("price_conversion", {"to_symbol": False})
