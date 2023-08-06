import math

from tvscreener import Field, TimeInterval


def get_columns(fields_: Field, time_interval: TimeInterval):
    columns = {field.get_field_name(time_interval): field.label for field in fields_}
    rec_columns = {field.get_rec_field(time_interval): field.get_rec_label() for field in fields_ if
                   field.format == 'recommendation'}
    if time_interval is not TimeInterval.ONE_DAY:
        columns[time_interval.update_mode()] = "Update Mode"

    columns = {**columns, **rec_columns}
    columns = {_format_timed_fields(k): v for k, v in columns.items()}
    return columns


def _format_timed_fields(field_):
    """Format fields that embed the time interval in the name
    e.g. 'change.1W' -> 'change|1W'"""
    # Split the field by '.'
    if '.' in field_:
        num = field_.split('.')[1]
        # is num a number?
        if num.isdigit():
            return field_.replace('.', '|')
        elif num in ['1W', '1M']:
            return field_.replace('.', '|')
    return field_


def _get_computed_recommendation_field(field):
    if field.format == 'computed_recommendation':
        return field.get_rec_field()


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
