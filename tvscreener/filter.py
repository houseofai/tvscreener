import math
from enum import Enum


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

    def range(self):
        return [self.min, self.max]


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


class Filter:
    def __init__(self, name: str, operation: FilterOperator, values):
        self.name = name
        self.operation = operation
        self.values = values

    def to_dict(self):
        return {"left": self.name, "operation": self.operation.value, "right": self.values}


class SearchFilter(Filter):
    def __init__(self, value):
        super().__init__("name,description", FilterOperator.MATCH, value)


class PrimaryFilter(Filter):
    def __init__(self):
        super().__init__("is_primary", FilterOperator.EQUAL, True)


class ExchangeFilter(Filter):
    def __init__(self, exchanges: list):
        super().__init__("exchange", FilterOperator.IN_RANGE, exchanges)


class TypeFilter(Filter):
    def __init__(self, types: list):
        super().__init__("type", FilterOperator.IN_RANGE, types)


class RatingFilter(Filter):
    def __init__(self, field: str, rating: Ratings):
        super().__init__(field, FilterOperator.IN_RANGE, rating.range())
