import math
from typing import Type

from tvscreener.field import Field, TimeInterval, add_historical, add_time_interval, add_rec, add_rec_to_label, \
    add_historical_to_label


def format_historical_field(field_, time_interval, historical=1):
    """
    Format the technical field to the time interval
    :param field_: Field to format
    :param time_interval: Time interval for the field
    :param historical: Historical offset (default 1)
    :return: Formatted field name
    :raises ValueError: If field is not a historical field
    """
    # Fixed: Use proper exception instead of assert
    if not field_.historical:
        raise ValueError(f"{field_} is not a historical field")
    formatted_technical_field = add_historical(field_.field_name, historical)

    if field_.interval and time_interval != TimeInterval.ONE_DAY:
        formatted_technical_field = add_time_interval(formatted_technical_field, time_interval)

    return formatted_technical_field


def get_columns_to_request(fields_: Type[Field], time_interval: TimeInterval):
    """
    Assemble the technical columns for the request
    :param fields_: type of fields to be requested (StockField, ForexField, CryptoField)
    :param time_interval:
    :return:
    """

    # Build a dict of technical label and field label
    # Format the technical field to the time interval
    columns = {add_time_interval(field.field_name, time_interval)
               if time_interval != TimeInterval.ONE_DAY and field.interval
               else field.field_name: field.label
               for field in fields_}

    # Drop column that starts with "pattern"
    columns = {k: v for k, v in columns.items() if not k.startswith("candlestick")}

    # Add the time interval update mode column
    if time_interval is not TimeInterval.ONE_DAY:
        columns[time_interval.update_mode()] = "Update Mode"

    # Format the fields that embed the time interval in the name
    columns = {_format_timed_fields(k): v for k, v in columns.items()}

    # Add the recommendation columns
    rec_columns = {add_rec(field.field_name): add_rec_to_label(field.field_name)
                   for field in fields_ if field.has_recommendation()}

    # Add the historical columns
    hist_columns = {format_historical_field(field, time_interval): add_historical_to_label(field.label)
                    for field in fields_ if field.historical}

    # Merge the dicts
    columns = {**columns, **rec_columns, **hist_columns}

    return columns


def _format_timed_fields(field_):
    """Format fields that embed the time interval in the name
    e.g. 'change.1W' -> 'change|1W'"""
    # Split the field by '.'
    if (field_.startswith("change") or field_.startswith("relative_volume_intraday")) and '.' in field_:
        num = field_.split('.')[1]
        # is num a number?
        if num.isdigit():
            return field_.replace('.', '|')
        elif num in ['1W', '1M']:
            return field_.replace('.', '|')
    return field_


def is_status_code_ok(response):
    """Check if HTTP response status code indicates success."""
    return response.ok  # Simplified: use built-in ok property


def get_url(subtype):
    return f"https://scanner.tradingview.com/{subtype}/scan"


# Fixed: Use proper abbreviations including K for thousands
millnames = ['', 'K', 'M', 'B', 'T']


def millify(n):
    """
    Convert a number to abbreviated form (e.g., 1000 -> 1.000K, 1000000 -> 1.000M).

    :param n: Number to convert
    :return: String representation with abbreviation
    """
    n = float(n)
    # Handle negative numbers
    is_negative = n < 0
    n = abs(n)

    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(n) / 3))))

    result = '{:.3f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])
    return '-' + result if is_negative else result


def get_recommendation(rating):
    """
    Convert a numeric rating to a recommendation string.

    :param rating: Numeric rating value
    :return: "SELL" for negative, "NEUTRAL" for zero, "BUY" for positive
    :raises ValueError: If rating is not a valid number
    """
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid rating: {rating}. Rating should be a number.")

    if rating < 0:
        return "SELL"
    elif rating == 0:
        return "NEUTRAL"
    else:  # rating > 0
        return "BUY"
