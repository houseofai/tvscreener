import json
from enum import Enum

import pandas as pd
import requests
from typing import List

from tvscreener.field import TimeInterval, Field
from tvscreener.field.crypto import CryptoField
from tvscreener.field.forex import ForexField
from tvscreener.field.stock import StockField
from tvscreener.filter import FilterOperator, Filter, Rating, StocksMarket, FilterType, SymbolType, Type
from tvscreener.util import get_columns, is_status_code_ok, get_url, millify, get_recommendation

default_market = ["america"]
default_min_range = 0
default_max_range = 150
default_sort_stocks = "market_cap_basic"
default_sort_crypto = "24h_vol|5"
default_sort_forex = "name"


def _build_dataframe(response, columns, with_tech_fields=False):
    # Parse response
    data = [[d["s"]] + d["d"] for d in response.json()['data']]

    # Build dataframe
    df = pd.DataFrame(data, columns=['Symbol'] + list(columns.values()))

    if with_tech_fields:
        df.columns = pd.MultiIndex.from_tuples([('Symbol', '')] + list(columns.items()))

    # Order columns by setting symbol, name, description first
    df = df[['Symbol', 'Name', 'Description'] + [c for c in df.columns if c not in ['Symbol', 'Description', 'Name']]]
    return df


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
        return None

    def add_filter(self, filter_: Filter):

        # filter_val = {"left": filter_, "operation": operation.value, "right": values}
        # Case where the filter already exists, and we want to add more values
        existing_filter = self._get_filter(filter_.filter_type)
        if existing_filter and not set(filter_.values).issubset(set(existing_filter.values)):
            # Set the operation is IN_RANGE with multiple values
            existing_filter.operation = FilterOperator.IN_RANGE
            existing_filter.values.extend(filter_.values)
        elif not existing_filter:
            # Case where the filter does not exist
            # If the filter contains values array with only one value, we can use EQUAL instead of IN_RANGE
            if len(filter_.values) == 1:
                filter_.operation = FilterOperator.EQUAL
            self.filters.append(filter_)

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

    def get(self, time_interval=TimeInterval.ONE_DAY,
            with_tech_fields=False,
            print_request=False
            ):

        # Time Interval
        columns = get_columns(self.specific_fields, time_interval)

        payload = self._build_payload(list(columns.keys()))
        payload_json = json.dumps(payload, indent=4)

        if print_request:
            print(f"Request: {self.url}")
            print("Payload:")
            print(json.dumps(payload, indent=4))

        response = requests.post(self.url, data=payload_json)
        if is_status_code_ok(response):
            return _build_dataframe(response, columns, with_tech_fields)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None


class StockScreener(Screener):

    def __init__(self):
        super().__init__()
        subtype = "stock"
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

    def _add_types(self, *types: Type):
        if len(types) > 1:
            operator = FilterOperator.IN_RANGE
        else:
            operator = FilterOperator.EQUAL

        for type_ in types:
            self.add_filter(Filter(FilterType.TYPE, operator, type_.value))


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


class CryptoScreener(Screener):
    def __init__(self):
        super().__init__()
        subtype = "crypto"
        self.markets = set(subtype)
        self.url = get_url(subtype)
        self.specific_fields = CryptoField
        self.sort_by(default_sort_crypto, "desc")
        self.add_misc("price_conversion", {"to_symbol": False})


def beautify(df, specific_fields):
    df = Beautify(df, specific_fields).df
    return df


class Beautify:
    def __init__(self, df, specific_fields: Field):
        self.df = df.copy()

        for column in self.df.columns:
            # Find the enum with the column name
            specific_field = specific_fields.get_by_label(specific_fields, column)
            if specific_field is not None and specific_field.format is not None:
                # self._copy_column(column)
                # fn = self.fn_mappings.get(format_)
                self._format_column(specific_field, column)

    def _format_column(self, specific_field, column):
        if specific_field.format is 'bool':
            self._to_bool(column)
        elif specific_field.format is 'rating':
            self._rating(column)
        elif specific_field.format is 'round':
            self._round(column)
        elif specific_field.format is 'percent':
            self._percent(column)
        elif specific_field.has_recommendation():
            self._recommendation(column, specific_field)
        elif specific_field.format is 'computed_recommendation':
            # TODO
            pass
        elif specific_field.format is 'text':
            # TODO
            pass
        elif specific_field.format is 'date':
            # TODO
            pass
        elif specific_field.format is 'missing':
            # TODO
            pass
        elif specific_field.format is 'currency':
            # TODO
            pass
        elif specific_field.format is 'float':
            # TODO
            pass
        elif specific_field.format is 'number_group':
            self._replace_nan(column)
            self._number_group(column)
        else:
            print(f"Unknown format: {specific_field.format} for column: {column}")

    def _rating(self, column):
        self.df[column] = self.df[column].apply(lambda x: Rating.find(x).label)

    def _recommendation(self, column, specific_field):
        self.df[column] = self.df.apply(
            lambda x: f"{x[column]} - {get_recommendation(x[specific_field.get_rec_label()])}", axis=1)

    def _number_group(self, column):
        self.df[column] = self.df[column].apply(lambda x: millify(x))

    def _percent(self, column):
        self.df[column] = self.df[column].apply(lambda x: f"{x:.2f}%" if x is not None else None)

    def _round(self, column):
        self.df[column] = self.df[column].apply(lambda x: round(x, 2) if x is not None else None)

    def _copy_column(self, column):
        raw_name = column + " raw"
        self.df[raw_name] = self.df[column]

    def _replace_nan(self, column):
        self.df[column] = self.df[column].fillna(0)

    def _to_bool(self, column):
        self.df[column] = self.df[column].apply(lambda x: True if x is 'true' else False)
        self.df[column] = self.df[column].astype(bool)
