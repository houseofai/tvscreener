from tvscreener.field.forex import ForexField
from tvscreener.util import get_url
from tvscreener.core.base import Screener, default_sort_forex


class ForexScreener(Screener):
    def __init__(self):
        super().__init__()
        subtype = "forex"
        self.url = get_url(subtype)
        self.markets = set(subtype)
        self.specific_fields = ForexField  # {**self.fields, **tvdata.forex['columns']}
        # self.add_filter("sector", FilterOperation.IN_RANGE, ['Major', 'Minor'])
        self.sort_by(default_sort_forex)
        self.add_misc("symbols", {"query": {"types": ["forex"]}})