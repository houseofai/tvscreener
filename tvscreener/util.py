import math
from typing import Type

from tvscreener import Field, TimeInterval
from tvscreener.field import add_historical, add_time_interval, add_rec, add_rec_to_label, add_historical_to_label


class MalformedRequestException(Exception):
    def __init__(self, code, response_msg, url, payload):
        message = f"Error: {code}: {response_msg}\n"
        message += f"Request: {url}\n"
        message += "Payload:\n"
        message += payload
        super().__init__(message)


def format_historical_field(field_, time_interval, historical=1):
    assert field_.historical, f"{field_} is not a historical field"
    """
    Format the technical field to the time interval
    :param field_:
    :param time_interval:
    :return:
    """
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
    return response.status_code == 200


def get_url(subtype):
    return f"https://scanner.tradingview.com/{subtype}/scan"


millnames = ['', '', 'M', 'B', '']


def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.3f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


def get_recommendation(rating):
    if rating < 0:
        return "S"
    elif rating == 0:
        return "N"
    elif rating > 0:
        return "B"
