import math
from enum import Enum

from tvscreener import Field


class StocksMarket(Enum):
    ALL = "ALL"
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


class Sector(Enum):
    ANY = "Any"
    COMMERCIAL_SERVICES = "Commercial Services"
    COMMUNICATIONS = "Communications"
    CONSUMER_DURABLES = "Consumer Durables"
    CONSUMER_NON_DURABLES = "Consumer Non-Durables"
    CONSUMER_SERVICES = "Consumer Services"
    DISTRIBUTION_SERVICES = "Distribution Services"
    ELECTRONIC_TECHNOLOGY = "Electronic Technology"
    ENERGY_MINERALS = "Energy Minerals"
    FINANCE = "Finance"
    GOVERNMENT = "Government"
    HEALTH_SERVICES = "Health Services"
    HEALTH_TECHNOLOGY = "Health Technology"
    INDUSTRIAL_SERVICES = "Industrial Services"
    MISCELLANEOUS = "Miscellaneous"
    NON_ENERGY_MINERALS = "Non-Energy Minerals"
    PROCESS_INDUSTRIES = "Process Industries"
    PRODUCER_MANUFACTURING = "Producer Manufacturing"
    RETAIL_TRADE = "Retail Trade"
    TECHNOLOGY_SERVICES = "Technology Services"
    TRANSPORTATION = "Transportation"
    UTILITIES = "Utilities"


class Country(Enum):
    ANY = "Any"
    ALBANIA = "Albania"
    ARGENTINA = "Argentina"
    AUSTRALIA = "Australia"
    AUSTRIA = "Austria"
    AZERBAIJAN = "Azerbaijan"
    BAHAMAS = "Bahamas"
    BARBADOS = "Barbados"
    BELGIUM = "Belgium"
    BERMUDA = "Bermuda"
    BRAZIL = "Brazil"
    BRITISH_VIRGIN_ISLANDS = "British Virgin Islands"
    CAMBODIA = "Cambodia"
    CANADA = "Canada"
    CAYMAN_ISLANDS = "Cayman Islands"
    CHILE = "Chile"
    CHINA = "China"
    COLOMBIA = "Colombia"
    COSTA_RICA = "Costa Rica"
    CYPRUS = "Cyprus"
    CZECH_REPUBLIC = "Czech Republic"
    DENMARK = "Denmark"
    DOMINICAN_REPUBLIC = "Dominican Republic"
    EGYPT = "Egypt"
    FAROE_ISLANDS = "Faroe Islands"
    FINLAND = "Finland"
    FRANCE = "France"
    GERMANY = "Germany"
    GIBRALTAR = "Gibraltar"
    GREECE = "Greece"
    HONG_KONG = "Hong Kong"
    HUNGARY = "Hungary"
    ICELAND = "Iceland"
    INDIA = "India"
    INDONESIA = "Indonesia"
    IRELAND = "Ireland"
    ISRAEL = "Israel"
    ITALY = "Italy"
    JAMAICA = "Jamaica"
    JAPAN = "Japan"
    JORDAN = "Jordan"
    KAZAKHSTAN = "Kazakhstan"
    LUXEMBOURG = "Luxembourg"
    MACAU = "Macau"
    MACEDONIA = "Macedonia"
    MALAYSIA = "Malaysia"
    MALTA = "Malta"
    MAURITIUS = "Mauritius"
    MEXICO = "Mexico"
    MONACO = "Monaco"
    MONGOLIA = "Mongolia"
    MONTENEGRO = "Montenegro"
    NETHERLANDS = "Netherlands"
    NEW_ZEALAND = "New Zealand"
    NORWAY = "Norway"
    PANAMA = "Panama"
    PAPUA_NEW_GUINEA = "Papua New Guinea"
    PERU = "Peru"
    PHILIPPINES = "Philippines"
    POLAND = "Poland"
    PORTUGAL = "Portugal"
    PUERTO_RICO = "Puerto Rico"
    ROMANIA = "Romania"
    RUSSIAN_FEDERATION = "Russian Federation"
    SINGAPORE = "Singapore"
    SOUTH_AFRICA = "South Africa"
    SOUTH_KOREA = "South Korea"
    SPAIN = "Spain"
    SWEDEN = "Sweden"
    SWITZERLAND = "Switzerland"
    TAIWAN = "Taiwan"
    TANZANIA = "Tanzania"
    THAILAND = "Thailand"
    TURKEY = "Turkey"
    US_VIRGIN_ISLANDS = "U.S. Virgin Islands"
    UNITED_ARAB_EMIRATES = "United Arab Emirates"
    UNITED_KINGDOM = "United Kingdom"
    UNITED_STATES = "United States"
    URUGUAY = "Uruguay"
    VIETNAM = "Vietnam"


class Region(Enum):
    AFRICA = "Africa"
    AMERICAS = "Americas"
    ASIA = "Asia"
    EUROPE = "Europe"
    MIDDLE_EAST = "Middle East"
    PACIFIC = "Pacific"


class SubMarket(Enum):
    OTCQB = "OTCQB"
    OTCQX = "OTCQX"
    PINK = "PINK"


class Exchange(Enum):
    OTC = "OTC"
    NYSE_ARCA = "AMEX"
    NASDAQ = "NASDAQ"
    NYSE = "NYSE"


class Type(Enum):
    STOCK = "stock"
    DEPOSITORY_RECEIPT = "dr"
    FUND = "fund"
    STRUCTURED = "structured"


class SymbolType(Enum):
    CLOSED_END_FUND = ["closedend"]
    COMMON_STOCK = ["common"]
    DEPOSITORY_RECEIPT = ["foreign-issuer"]
    ETF = ["etf", "etf,odd", "etf,otc", "etf,cfd"]
    ETN = ["etn"]
    MUTUAL_FUND = ["mutual"]
    PREFERRED_STOCK = ["preferred"]
    REIT = ["reit", "reit,cfd", "trust,reit"]
    STRUCTURED = [""]  # ["SP"]
    TRUST_FUND = ["trust"]
    UIT = ["unit"]


class Rating(Enum):
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

    @classmethod
    def find(cls, value: float):
        if value is not None:
            for rating in Rating:
                if value in rating:
                    return rating
        return Rating.UNKNOWN

    @classmethod
    def names(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))


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
