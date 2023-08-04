import math

from tvscreener import Field, TimeInterval


def get_columns(fields_: Field, time_interval: TimeInterval):
    columns = {field.get_field_name(time_interval): field.label for field in fields_}
    rec_columns = {field.get_rec_field(time_interval): field.get_rec_label() for field in fields_ if
                   field.recommendation}
    if time_interval is not TimeInterval.ONE_DAY:
        columns[time_interval.update_mode()] = "Update Mode"
    return {**columns, **rec_columns}


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


