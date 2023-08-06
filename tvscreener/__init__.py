import json

import pandas as pd
import requests

from tvscreener.field import TimeInterval, StocksMarket, Field
from tvscreener.field.crypto import CryptoField
from tvscreener.field.forex import ForexField
from tvscreener.field.stock import StockField
from tvscreener.filter import FilterOperator, Filter, Rating
from tvscreener.util import get_columns, is_status_code_ok, get_url, millify, get_recommendation

default_market = ["america"]
default_min_range = 0
default_max_range = 150
default_sort_stocks = "market_cap_basic"
default_sort_crypto = "24h_vol|5"
default_sort_forex = "name"


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

    def add_prebuilt_filter(self, filter_: Filter):
        self.filters.append(filter_.to_dict())

    def add_filter(self, filter_, operation: FilterOperator = None, values=None):
        filter_val = {"left": filter_, "operation": operation.value, "right": values}
        self.filters.append(filter_val)

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
            "filter": self.filters,
            "options": self.options,
            "symbols": self.symbols if self.symbols else {"query": {"types": []}, "tickers": []},
            "sort": self.sort,
            "range": self.range,
            "columns": requested_columns_,
            **self.misc
        }
        return payload

    def _build_dataframe(self, response, columns):
        # Parse response
        data = [[d["s"]] + d["d"] for d in response.json()['data']]

        # Build dataframe
        df = pd.DataFrame(data, columns=['Symbol'] + list(columns.values()))

        return df

    def get(self, time_interval=TimeInterval.ONE_DAY, print_request=False):

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
            return self._build_dataframe(response, columns)
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
        elif specific_field.format is 'recommendation':
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

    def _test(self, x):
        return f"{x:.2f}%"

    def _recommendation(self, column, specific_field):
        self.df[column] = self.df.apply(
            lambda x: f"{x[column]} - {get_recommendation(x[specific_field.get_rec_label()])}" if x[
                                                                                                      specific_field.get_rec_label()] is not None else None,
            axis=1)

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
