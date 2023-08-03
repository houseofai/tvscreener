import math

from tvscreener import tvdata
import json
from enum import Enum

import pandas as pd
import requests

from tvscreener.filter import FilterOperator, Filter, Ratings

default_market = ["america"]
default_min_range = 0
default_max_range = 150
default_sort_stocks = "market_cap_basic"
default_sort_crypto = "24h_vol|5"
default_sort_forex = "name"


def find_ratings(value: float) -> Ratings:
    for rating in Ratings:
        if value in rating:
            return rating
    return Ratings.UNKNOWN


class TimeInterval(Enum):
    ONE_MINUTE = "1"
    FIVE_MINUTES = "5"
    FIFTEEN_MINUTES = "15"
    THIRTY_MINUTES = "30"
    SIXTY_MINUTES = "60"
    TWO_HOURS = "120"
    FOUR_HOURS = "240"
    ONE_DAY = "1D"
    ONE_WEEK = "1W"

    def update_mode(self):
        return f"update_mode|{self.value}"


def get_url(subtype):
    return f"https://scanner.tradingview.com/{subtype}/scan"


class Screener:

    def __init__(self):
        self.sort = None
        self.url = None
        self.filters = []
        self.options = {}
        self.symbols = None
        self.misc = {}

        self.range = None
        self.set_range()
        self.columns = tvdata.main['columns']
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

    def _build_columns(self):
        requested_columns = list(self.columns.keys())
        # requested_columns = clean_columns(requested_columns)
        return requested_columns

    def _build_dataframe(self, response, requested_columns, time_interval: TimeInterval, beautify=True):
        # Parse response
        data = [[d["s"]] + d["d"] for d in response.json()['data']]

        # Build labels for the dataframe
        requested_column_labels = ['Symbol'] + [self.columns[k]['label'] if k in self.columns else k for k in
                                                requested_columns]

        # Default is one day, so there is no need to format the columns
        if time_interval is not TimeInterval.ONE_DAY:
            requested_column_labels.append('Time Interval')

        # Build dataframe
        df = pd.DataFrame(data, columns=requested_column_labels)  # payload["columns"])

        if beautify:
            df = Beautify(df, self.columns).df
        return df

    def _add_time_interval_to_columns(self, time_interval: TimeInterval, columns: list):
        # Default is one day, so there is no need to format the columns
        if time_interval is TimeInterval.ONE_DAY:
            return columns

        new_columns = []
        for column in columns:
            v = self.columns[column]
            if "interval" in v and v["interval"]:
                new_columns.append(f"{column}|{time_interval.value}")
            else:
                new_columns.append(column)
        new_columns.append(time_interval.update_mode())
        return new_columns

    def get(self, time_interval=TimeInterval.ONE_DAY, beautify=True, print_request=False):

        initial_columns = list(self.columns.keys())  # self._build_columns()

        # Time Interval
        timeframed_columns = self._add_time_interval_to_columns(time_interval, initial_columns)

        payload = self._build_payload(timeframed_columns)
        payload_json = json.dumps(payload, indent=4)

        if print_request:
            print(f"Request: {self.url}")
            print("Payload:")
            print(json.dumps(payload, indent=4))

        res = requests.post(self.url, data=payload_json)
        if res.status_code == 200:
            return self._build_dataframe(res, initial_columns, time_interval, beautify)
        else:
            print(f"Error: {res.status_code}")
            print(res.text)
            return None


class StockScreener(Screener):

    def __init__(self):
        super().__init__()
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
        # self.add_filter("sector", FilterOperation.IN_RANGE, ['Major', 'Minor'])
        self.sort_by(default_sort_forex, "asc")
        self.add_misc("symbols", {"query": {"types": ["forex"]}})
        self.add_misc("markets", ["forex"])


class CryptoScreener(Screener):
    def __init__(self):
        super().__init__()
        self.markets = set("crypto")
        self.url = get_url("crypto")
        self.columns = {**self.columns, **tvdata.crypto['columns']}
        self.sort_by(default_sort_crypto, "desc")
        self.add_misc("price_conversion", {"to_symbol": False})


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
