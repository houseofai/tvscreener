import math

from tvscreener import tvdata
import json
from enum import Enum

import pandas as pd
import requests

default_market = ["america"]
default_min_range = 0
default_max_range = 150
default_sort_stocks = "market_cap_basic"


class Ratings(Enum):
    STRONG_BUY = 0.5, 1, "Strong Buy"
    BUY = 0.1, 0.5, "Buy"
    NEUTRAL = -0.1, 0.1, "Neutral"
    SELL = -0.5, -0.1, "Sell"
    STRONG_SELL = -1, -0.5, "Strong Sell"
    UNKNOWN = math.nan, math.nan, "Unknown"

    def __init__(self, min_, max_, label):
        self.min = min_
        self.max = max_
        self.label = label

    def __contains__(self, item):
        return self.min <= item <= self.max


def find_ratings(value: float) -> Ratings:
    for rating in Ratings:
        if value in rating:
            return rating
    return Ratings.UNKNOWN


class TimeInterval(Enum):
    ONE_MINUTE = "update_mode|1"
    FIVE_MINUTES = "update_mode|5"
    FIFTEEN_MINUTES = "update_mode|15"
    THIRTY_MINUTES = "update_mode|30"
    SIXTY_MINUTES = "update_mode|60"
    TWO_HOURS = "update_mode|120"
    FOUR_HOURS = "update_mode|240"
    ONE_DAY = "update_mode|1D"
    ONE_WEEK = "update_mode|1W"


class FilterOperation(Enum):
    BELOW = "less"
    BELOW_OR_EQUAL = "eless"
    ABOVE = "greater"
    ABOVE_OR_EQUAL = "egreater"
    CROSSES = "crosses"
    CROSSES_UP = "crosses_above"
    CROSSES_DOWN = "crosses_below"
    IN_RANGE = "in_range"
    NOT_IN_RANGE = "not_in_range"
    EQUAL = "equal"
    NOT_EQUAL = "nequal"


def clean_columns(columns):
    to_remove = ['change.60',
                 'change_abs.60',
                 'change.1',
                 'change_abs.1',
                 'change.1M',
                 'change_abs.1M',
                 'change.1W',
                 'change_abs.1W',
                 'change.240',
                 'change_abs.240',
                 'change.5',
                 'change_abs.5',
                 'change.15',
                 'change_abs.15',
                 'change_from_open',
                 'change_from_open_abs',
                 'candlestick',
                 'relative_volume_intraday.5']

    columns = [e for e in columns if e not in to_remove]
    return list(dict.fromkeys(columns))


def get_url(subtype):
    return f"https://scanner.tradingview.com/{subtype}/scan"


class Screener:

    def __init__(self):
        self.sort = None
        self.url = None
        self.filters = []
        self.options = {}
        # self.markets = set()
        self.symbols = None

        self.range = None
        self.set_range()
        self.columns = tvdata.main['columns']
        # self.add_filter("type", "equal", subtype)
        self.add_option("lang", "en")

    def _add_filter_in_range(self, filter_, values):
        filter_val = {"left": filter_, "operation": FilterOperation.IN_RANGE.value, "right": values}
        self.filters.append(filter_val)

    def _add_filter_equal(self, filter_, values):
        filter_val = {"left": filter_, "operation": FilterOperation.EQUAL.value, "right": values}
        self.filters.append(filter_val)

    def add_filter(self, filter_, operation: FilterOperation = None, values=None):
        if isinstance(values, list):
            self._add_filter_in_range(filter_, values)
        elif isinstance(values, bool):
            self._add_filter_equal(filter_, values)
        else:
            filter_val = {"left": filter_, "operation": operation.value, "right": values}
            self.filters.append(filter_val)

    def add_option(self, key, value):
        self.options[key] = value

    def set_range(self, from_range: int = default_min_range, to_range: int = default_max_range) -> None:
        self.range = [from_range, to_range]

    # def set_symbols(self, symbols):
    #    self.symbols = symbols

    def sort_by(self, sort_by, order="desc"):
        self.sort = {"sortBy": sort_by, "sortOrder": order}

    def _build_payload(self, requested_columns_):
        payload = {
            "filter": self.filters,
            "options": self.options,
            "symbols": self.symbols if self.symbols else {"query": {"types": []}, "tickers": []},
            "sort": self.sort,
            "range": self.range,
            "columns": requested_columns_
        }
        return payload

    def _build_columns(self):
        requested_columns = list(self.columns.keys())
        # requested_columns = clean_columns(requested_columns)
        return requested_columns

    def _build_dataframe(self, response, requested_columns, beautify=True):
        # Parse response
        data = [[d["s"]] + d["d"] for d in response.json()['data']]

        # Build labels for the dataframe
        requested_column_labels = ['Symbol'] + [self.columns[k]['label'] if k in self.columns else k for k in
                                                requested_columns]

        # Build dataframe
        df = pd.DataFrame(data, columns=requested_column_labels)  # payload["columns"])

        if beautify:
            df = Beautify(df, self.columns).df
        return df

    def get(self, time_interval=TimeInterval.ONE_DAY, beautify=True, print_request=False):

        requested_columns = self._build_columns()
        # requested_columns = clean_columns(requested_columns)

        # Time Interval
        requested_columns.append(time_interval.value)

        payload = self._build_payload(requested_columns)
        payload_json = json.dumps(payload, indent=4)

        if print_request:
            print(f"Request: {self.url}")
            print("Payload:")
            print(json.dumps(payload, indent=4))

        res = requests.post(self.url, data=payload_json)
        if res.status_code == 200:
            return self._build_dataframe(res, requested_columns, beautify)
        else:
            print(f"Error: {res.status_code}")
            print(res.text)
            return None


class StockScreener(Screener):

    def __init__(self):
        super().__init__()
        # self.subtype_columns = tvdata.stock['columns']
        # self.columns.extend(self.subtype_columns.keys())
        self.markets = set()

        self.url = get_url("global")
        self.columns = {**self.columns, **tvdata.stock['columns']}
        self.sort_by(default_sort_stocks, "desc")

    def _build_payload(self, requested_columns_):
        payload = super()._build_payload(requested_columns_)
        payload["markets"] = list(self.markets) if self.markets else default_market
        return payload

    def set_markets(self, *markets):
        """
        Set the markets to be scanned
        :param markets: list of markets
        :return: None
        """
        for market in markets:
            if market not in tvdata.stock['markets']:
                raise ValueError(f"Unknown market: {market}")
            self.markets.add(market)


class ForexScreener(Screener):
    def __init__(self):
        super().__init__()
        self.url = get_url("forex")
        self.columns = {**self.columns, **tvdata.forex['columns']}


class CryptoScreener(Screener):
    def __init__(self):
        super().__init__()
        self.url = get_url("crypto")
        self.columns = {**self.columns, **tvdata.crypto['columns']}


millnames = ['', '', 'M', 'B', '']


def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.3f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


class Beautify:
    def __init__(self, df, columns):
        self.df = df
        columns = {v.get('label'): v.get('format') for k, v in columns.items()}

        for column in self.df.columns:
            if column in columns:
                format_ = columns.get(column)
                if format_ is not None:
                    self._copy_column(column)
                    # fn = self.fn_mappings.get(format_)
                    self._format_column(format_, column)

    def _format_column(self, format_, column):
        if format_ is 'bool':
            self._to_bool(column)
        elif format_ is 'rating':
            self._rating(column)
        elif format_ is 'percent':
            self._percent(column)
        elif format_ is 'number_group':
            self._replace_nan(column)
            self._number_group(column)
        else:
            print(f"Unknown format: {format_} for column: {column}")

    def _rating(self, column):
        self.df[column] = self.df[column].apply(lambda x: find_ratings(x).label)

    def _number_group(self, column):
        self.df[column] = self.df[column].apply(lambda x: millify(x))

    def _percent(self, column):
        self.df[column] = self.df[column].apply(lambda x: f"{x:.2f}%")

    def _copy_column(self, column):
        raw_name = self._get_raw_name(column)
        self.df[raw_name] = self.df[column]

    def _get_raw_name(self, column):
        return column + " raw"

    def _replace_nan(self, column):
        self.df[column] = self.df[column].fillna(0)

    def _to_bool(self, column):
        self.df[column] = self.df[column].apply(lambda x: True if x is 'true' else False)
        self.df[column] = self.df[column].astype(bool)
