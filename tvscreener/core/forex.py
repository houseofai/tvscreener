from tvscreener.core.base import Screener, default_sort_forex
from tvscreener.field.forex import ForexField
from tvscreener.util import get_url


class ForexScreener(Screener):
    """Forex screener for querying forex/currency pairs from TradingView."""

    def __init__(self):
        super().__init__()
        subtype = "forex"
        self.url = get_url(subtype)
        self.markets = {subtype}  # Fixed: set literal instead of set(string)
        self.specific_fields = ForexField
        self.sort_by(default_sort_forex)
        self.add_misc("symbols", {"query": {"types": ["forex"]}})
