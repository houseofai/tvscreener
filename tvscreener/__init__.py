
from tvscreener import tvdata
import json
from enum import Enum

import pandas as pd
import requests


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


main_columns = [
    # "logoid",
    "name",
    "description",
    "type", "subtype",
    "pricescale",
    "minmov",
    "fractional",
    "minmove2",
    "currency",
    "fundamental_currency_code"
]


class FilterOperation(Enum):
    BELOW = "less"
    BELOW_OR_EQUAL = "eless"
    ABOVE = "greater"
    ABOVE_OR_EQUAL = "egreater"
    EQUAL = "equal"
    IN_RANGE = "in_range"
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
    default_market = ["america"]

    def __init__(self, subtype):
        self.sort = None
        self.url = get_url(subtype)
        self.filters = []
        self.options = {}
        self.markets = []
        self.symbols = None
        self.market_columns = None

        self.range = None

        self.columns = main_columns.copy()
        self.set_range()
        # self.add_filter("type", "equal", subtype)
        self.add_option("lang", "en")

    def add_filter(self, filter_, operation: FilterOperation = None, values=None):

        # if values is a list then the operation is 'in_range'
        if isinstance(values, list):
            filter_val = {"left": filter_, "operation": FilterOperation.IN_RANGE.value, "right": values}
        elif isinstance(values, bool):
            filter_val = {"left": filter_, "operation": FilterOperation.EQUAL.value, "right": values}
        else:
            filter_val = {"left": filter_, "operation": operation.value, "right": values}
        self.filters.append(filter_val)

    def add_option(self, key, value):
        self.options[key] = value

    def set_markets(self, *market):
        """
        Set the markets to be scanned
        :param market: list of markets
        :return: None
        """
        self.markets.extend(market)

    def set_range(self, from_range=0, to_range=150):
        self.range = [from_range, to_range]

    # def set_symbols(self, symbols):
    #    self.symbols = symbols

    def sort_by(self, sort_by, order="desc"):
        self.sort = {"sortBy": sort_by, "sortOrder": order}

    def _build_payload(self):
        payload = {"filter": self.filters if self.filters else [], "options": self.options,
                   "symbols": self.symbols if self.symbols else {"query": {"types": []}, "tickers": []},
                   "markets": self.markets if self.markets else self.default_market, "sort": self.sort,
                   "range": self.range}

        return payload

    def get(self, time_interval=TimeInterval.ONE_DAY, print_request=False):

        # Time Interval
        self.columns.append(time_interval.value)

        payload = self._build_payload()
        payload["columns"] = clean_columns(self.columns)

        payload_json = json.dumps(payload)
        if print_request:
            print(f"Request: {self.url}")
            print("Payload:")
            print(json.dumps(payload, indent=4))

        res = requests.post(self.url, data=payload_json)
        if res.status_code == 200:
            res_data = [d["d"] for d in res.json()['data']]
            return pd.DataFrame(res_data, columns=payload["columns"])
        else:
            print(f"Error: {res.status_code}")
            print(res.text)
            return None


class StockScreener(Screener):
    def __init__(self):
        super().__init__("global")
        self.columns.extend(tvdata.stock['columns'].keys())
        self.sort_by("market_cap_basic", "desc")


class ForexScreener(Screener):
    def __init__(self):
        super().__init__("forex")
        self.columns.extend(tvdata.forex['columns'].keys())


class CryptoScreener(Screener):
    def __init__(self):
        super().__init__("crypto")
        self.columns.extend(tvdata.crypto['columns'].keys())


