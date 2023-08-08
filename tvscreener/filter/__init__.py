import math
from enum import Enum

from tvscreener import Field


class StocksMarket(Enum):
    AMERICA = "america"
    UK = "uk"
    INDIA = "india"
    SPAIN = "spain"
    RUSSIA = "russia"
    AUSTRALIA = "australia"
    BRAZIL = "brazil"
    JAPAN = "japan"
    NEWZEALAND = "newzealand"
    TURKEY = "turkey"
    SWITZERLAND = "switzerland"
    HONGKONG = "hongkong"
    TAIWAN = "taiwan"
    NETHERLANDS = "netherlands"
    BELGIUM = "belgium"
    PORTUGAL = "portugal"
    FRANCE = "france"
    MEXICO = "mexico"
    CANADA = "canada"
    COLOMBIA = "colombia"
    UAE = "uae"
    NIGERIA = "nigeria"
    SINGAPORE = "singapore"
    GERMANY = "germany"
    PAKISTAN = "pakistan"
    PERU = "peru"
    POLAND = "poland"
    ITALY = "italy"
    ARGENTINA = "argentina"
    ISRAEL = "israel"
    EGYPT = "egypt"
    SRILANKA = "srilanka"
    SERBIA = "serbia"
    CHILE = "chile"
    CHINA = "china"
    MALAYSIA = "malaysia"
    MOROCCO = "morocco"
    KSA = "ksa"
    BAHRAIN = "bahrain"
    QATAR = "qatar"
    INDONESIA = "indonesia"
    FINLAND = "finland"
    ICELAND = "iceland"
    DENMARK = "denmark"
    ROMANIA = "romania"
    HUNGARY = "hungary"
    SWEDEN = "sweden"
    SLOVAKIA = "slovakia"
    LITHUANIA = "lithuania"
    LUXEMBOURG = "luxembourg"
    ESTONIA = "estonia"
    LATVIA = "latvia"
    VIETNAM = "vietnam"
    RSA = "rsa"
    THAILAND = "thailand"
    TUNISIA = "tunisia"
    KOREA = "korea"
    KENYA = "kenya"
    KUWAIT = "kuwait"
    NORWAY = "norway"
    PHILIPPINES = "philippines"
    GREECE = "greece"
    VENEZUELA = "venezuela"
    CYPRUS = "cyprus"
    BANGLADESH = "bangladesh"

    @classmethod
    def names(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))


class Type(Enum):
    STOCK = "stock"
    DEPOSITORY_RECEIPT = "dr"
    FUND = "fund"
    STRUCTURED = "structured"


class SymbolType(Enum):
    CLOSED_END_FUND = ["closedend"]
    COMMON_STOCK = ["common"]
    DEPOSITORY_RECEIPT = ["foreign-issuer"]
    ETF = ["etf", "etf,odd", "etf,otc", "etf,cfd"]
    ETN = ["etn"]
    MUTUAL_FUND = ["mutual"]
    PREFERRED_STOCK = ["preferred"]
    REIT = ["reit", "reit,cfd", "trust,reit"]
    STRUCTURED = [""]  # ["SP"]
    TRUST_FUND = ["trust"]
    UIT = ["unit"]


class Rating(Enum):
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

    def range(self):
        return [self.min, self.max]

    @classmethod
    def find(cls, value: float):
        if value is not None:
            for rating in Rating:
                if value in rating:
                    return rating
        return Rating.UNKNOWN

    @classmethod
    def names(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))


class FilterOperator(Enum):
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
    MATCH = "match"


class FilterType(Enum):
    SEARCH = "name,description"
    PRIMARY = "is_primary"
    EXCHANGE = "exchange"
    TYPE = "type"
    SUBTYPE = "subtype"


class Filter:
    def __init__(self, filter_type: FilterType, operation: FilterOperator, values):
        self.filter_type = filter_type
        self.operation = operation
        self.values = values if isinstance(values, list) else [values]

    def to_dict(self):
        right = self.values[0] if len(self.values) == 1 else self.values
        return {"left": self.filter_type.value, "operation": self.operation.value, "right": right}


class PrimaryFilter(Filter):
    def __init__(self):
        super().__init__(FilterType.PRIMARY, FilterOperator.EQUAL, True)


class ExchangeFilter(Filter):
    def __init__(self, exchanges: list):
        super().__init__(FilterType.EXCHANGE, FilterOperator.IN_RANGE, exchanges)


class RatingFilter(Filter):
    def __init__(self, field: Field, rating: Rating):
        super().__init__(field, FilterOperator.IN_RANGE, rating.range())
