from tvscreener.util import get_url
from tvscreener.core.base import Screener, default_sort_crypto
from tvscreener.field.crypto import CryptoField


class CryptoScreener(Screener):
    def __init__(self):
        super().__init__()
        subtype = "crypto"
        self.markets = set(subtype)
        self.url = get_url(subtype)
        self.specific_fields = CryptoField
        self.sort_by(default_sort_crypto, False)
        self.add_misc("price_conversion", {"to_symbol": False})