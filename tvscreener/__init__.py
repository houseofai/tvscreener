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


def find_ratings(value):
    for rating in Ratings:
        if rating.min <= value <= rating.max:
            return rating


class Ratings(Enum):
    STRONG_BUY = 0.5, 1, "Strong Buy"
    BUY = 0.1, 0.5, "Buy"
    NEUTRAL = -0.1, 0.1, "Neutral"
    SELL = -0.5, -0.1, "Sell"
    STRONG_SELL = -1, -0.5, "Strong Sell"

    def __init__(self, min_, max_, label):
        self.min = min_
        self.max = max_
        self.label = label


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

    def __init__(self, subtype):
        self.sort = None
        self.url = get_url(subtype)
        self.filters = []
        self.options = {}
        self.markets = set()
        self.symbols = None
        self.market_columns = None

        self.range = None

        self.columns = list(tvdata.main['columns'].keys())
        self.set_range()
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

    def set_range(self, from_range: int = default_min_range, to_range: int = default_max_range) -> None:
        self.range = [from_range, to_range]

    # def set_symbols(self, symbols):
    #    self.symbols = symbols

    def sort_by(self, sort_by, order="desc"):
        self.sort = {"sortBy": sort_by, "sortOrder": order}

    def _build_payload(self):
        payload = {
            "filter": self.filters if self.filters else [],
            "options": self.options,
            "symbols": self.symbols if self.symbols else {"query": {"types": []}, "tickers": []},
            "markets": list(self.markets) if self.markets else default_market,
            "sort": self.sort,
            "range": self.range,
            "columns": clean_columns(self.columns)
        }
        return payload

    def get(self, time_interval=TimeInterval.ONE_DAY, beautify=True, print_request=False):

        # Time Interval
        self.columns.append(time_interval.value)

        payload = self._build_payload()
        payload_json = json.dumps(payload, indent=4)

        if print_request:
            print(f"Request: {self.url}")
            print("Payload:")
            print(json.dumps(payload, indent=4))

        res = requests.post(self.url, data=payload_json)
        if res.status_code == 200:
            r = [d["d"] for d in res.json()['data']]
            df = pd.DataFrame(r, columns=payload["columns"])
            if beautify:
                df = Beautify(df).df
            return df
        else:
            print(f"Error: {res.status_code}")
            print(res.text)
            return None


class StockScreener(Screener):
    def __init__(self):
        super().__init__("global")
        self.columns.extend(tvdata.stock['columns'].keys())
        self.sort_by(default_sort_stocks, "desc")

    def get(self, time_interval=TimeInterval.ONE_DAY, beautify=True, print_request=False):
        df = super().get(time_interval=time_interval, beautify=beautify, print_request=print_request)
        return df.rename(columns=tvdata.stock['columns'])


class ForexScreener(Screener):
    def __init__(self):
        super().__init__("forex")
        self.columns.extend(tvdata.forex['columns'].keys())

    def get(self, time_interval=TimeInterval.ONE_DAY, beautify=True, print_request=False):
        df = super().get(time_interval=time_interval, beautify=beautify, print_request=print_request)
        return df.rename(columns=tvdata.forex['columns'])


class CryptoScreener(Screener):
    def __init__(self):
        super().__init__("crypto")
        self.columns.extend(tvdata.crypto['columns'].keys())

    def get(self, time_interval=TimeInterval.ONE_DAY, beautify=True, print_request=False):
        df = super().get(time_interval=time_interval, beautify=beautify, print_request=print_request)
        return df.rename(columns=tvdata.crypto['columns'])


def get_number_group(number):
    for group in NumberGroup:
        if number in group:
            return group
    return None


millnames = ['', '', 'M', 'B', '']


def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.3f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


class NumberGroup(Enum):
    MILLION = 10e6, 10e9, "M",
    BILLION = 10e9, 10e12, "B",

    def __init__(self, min_, max_, label):
        self.min = min_
        self.max = max_
        self.label = label

    def __contains__(self, item):
        return self.min <= item < self.max


class Beautify:
    mappings = {
        'Recommend.All': 'Technical Rating raw',
        'Recommend.MA': 'Moving Averages Rating raw',
        'Recommend.Other': 'Oscillators Rating raw',
        'dividends_paid': 'Dividends Paid (FY) raw',
    }

    def __init__(self, df):
        self.df = df
        self._rating('Recommend.All')
        self._rating('Recommend.MA')
        self._rating('Recommend.Other')
        self._replace_nan('dividends_paid')
        self._number_group('dividends_paid')

    def _rating(self, column):
        self.df[self.mappings[column]] = self.df[column]
        self.df[column] = self.df[column].apply(lambda x: find_ratings(x).label)

    def _number_group(self, column):
        self.df[self.mappings[column]] = self.df[column]
        self.df[column] = self.df[column].apply(lambda x: millify(x))

    def _replace_nan(self, column):
        self.df[column] = self.df[column].fillna(0)
