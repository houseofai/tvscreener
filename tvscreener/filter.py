from enum import Enum

from tvscreener import Field


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


class ExtraFilter(Enum):
    CURRENT_TRADING_DAY = "active_symbol"
    SEARCH = "name,description"
    PRIMARY = "is_primary"

    def __init__(self, value):
        self.field_name = value


class Filter:
    def __init__(self, field: Field | ExtraFilter, operation: FilterOperator, values):
        self.field = field
        self.operation = operation
        self.values = values if isinstance(values, list) else [values]

    #    def name(self):
    #        return self.field.field_name if isinstance(self.field, Field) else self.field.value

    def to_dict(self):
        right = [filter_enum.value if isinstance(filter_enum, Enum) else filter_enum for filter_enum in self.values]
        right = right[0] if len(right) == 1 else right
        left = self.field.field_name
        return {"left": left, "operation": self.operation.value, "right": right}
