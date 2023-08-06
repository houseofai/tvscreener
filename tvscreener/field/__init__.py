from enum import Enum


class TimeInterval(Enum):
    ONE_MINUTE = "1"
    FIVE_MINUTES = "5"
    FIFTEEN_MINUTES = "15"
    THIRTY_MINUTES = "30"
    SIXTY_MINUTES = "60"
    TWO_HOURS = "120"
    FOUR_HOURS = "240"
    ONE_DAY = "1D"
    ONE_WEEK = "1W"

    def update_mode(self):
        return f"update_mode|{self.value}"

    def format_field(self, field):
        return f"{field}|{self.value}"


class Field(Enum):

    def __init__(self, label, field_name, format_=None, interval=False, recommendation=False):
        self.label = label
        self.field_name = field_name
        self.format = format_
        self.interval = interval
        self.recommendation = recommendation

    def get_field_name(self, timeinterval=TimeInterval.ONE_DAY):
        if self.interval and timeinterval != TimeInterval.ONE_DAY:
            return timeinterval.format_field(self.field_name)
        return self.field_name

    def get_rec_field(self, timeinterval=TimeInterval.ONE_DAY):
        if self.recommendation:
            return f"Rec.{self.get_field_name(timeinterval)}"
        return None

    def get_rec_label(self):
        if self.recommendation:
            return f"Reco. {self.label}"
        return None

    @classmethod
    def get_by_label(cls, specific_fields, label):
        for specific_field in specific_fields:
            if specific_field.label == label:
                return specific_field
        return None


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
