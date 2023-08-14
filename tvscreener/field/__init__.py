import math
from enum import Enum


def add_time_interval(field_name, time_interval):
    return f"{field_name}|{time_interval.value}"


def add_historical(field_name, historical=1):
    return f"{field_name}[{historical}]"


def add_historical_to_label(field_name, historical=1):
    return f"Prev. {field_name}"


def add_rec(field_name):
    return f"Rec.{field_name}"


def add_rec_to_label(label):
    return f"Reco. {label}"


class Field(Enum):

    def __init__(self, label, field_name, format_=None, interval=False, historical=False):
        self.label = label
        self.field_name = field_name
        self.format = format_
        self.interval = interval
        self.historical = historical

    def has_recommendation(self):
        return self.format == 'recommendation'

    def get_rec_label(self):
        if self.has_recommendation():
            return add_rec_to_label(self.label)
        return None

    def get_rec_field(self):
        if self.has_recommendation():
            return add_rec(self.field_name)
        return None

    @classmethod
    def get_by_label(cls, specific_fields, label):
        for specific_field in specific_fields:
            if specific_field.label == label:
                return specific_field
        return None


class Type(Enum):
    STOCK = "stock"
    DEPOSITORY_RECEIPT = "dr"
    FUND = "fund"
    STRUCTURED = "structured"


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


class Country(Enum):
    ALBANIA = 'Albania'
    ARGENTINA = 'Argentina'
    AUSTRALIA = 'Australia'
    AUSTRIA = 'Austria'
    AZERBAIJAN = 'Azerbaijan'
    BAHAMAS = 'Bahamas'
    BARBADOS = 'Barbados'
    BELGIUM = 'Belgium'
    BERMUDA = 'Bermuda'
    BRAZIL = 'Brazil'
    BRITISH_VIRGIN_ISLANDS = 'British Virgin Islands'
    CAMBODIA = 'Cambodia'
    CANADA = 'Canada'
    CAYMAN_ISLANDS = 'Cayman Islands'
    CHILE = 'Chile'
    CHINA = 'China'
    COLOMBIA = 'Colombia'
    COSTA_RICA = 'Costa Rica'
    CYPRUS = 'Cyprus'
    CZECH_REPUBLIC = 'Czech Republic'
    DENMARK = 'Denmark'
    DOMINICAN_REPUBLIC = 'Dominican Republic'
    EGYPT = 'Egypt'
    FAROE_ISLANDS = 'Faroe Islands'
    FINLAND = 'Finland'
    FRANCE = 'France'
    GERMANY = 'Germany'
    GIBRALTAR = 'Gibraltar'
    GREECE = 'Greece'
    HONG_KONG = 'Hong Kong'
    HUNGARY = 'Hungary'
    ICELAND = 'Iceland'
    INDIA = 'India'
    INDONESIA = 'Indonesia'
    IRELAND = 'Ireland'
    ISRAEL = 'Israel'
    ITALY = 'Italy'
    JAMAICA = 'Jamaica'
    JAPAN = 'Japan'
    JORDAN = 'Jordan'
    KAZAKHSTAN = 'Kazakhstan'
    LUXEMBOURG = 'Luxembourg'
    MACAU = 'Macau'
    MACEDONIA = 'Macedonia'
    MALAYSIA = 'Malaysia'
    MALTA = 'Malta'
    MAURITIUS = 'Mauritius'
    MEXICO = 'Mexico'
    MONACO = 'Monaco'
    MONGOLIA = 'Mongolia'
    MONTENEGRO = 'Montenegro'
    NETHERLANDS = 'Netherlands'
    NEW_ZEALAND = 'New Zealand'
    NORWAY = 'Norway'
    PANAMA = 'Panama'
    PERU = 'Peru'
    PHILIPPINES = 'Philippines'
    POLAND = 'Poland'
    PORTUGAL = 'Portugal'
    PUERTO_RICO = 'Puerto Rico'
    ROMANIA = 'Romania'
    RUSSIAN_FEDERATION = 'Russian Federation'
    SINGAPORE = 'Singapore'
    SOUTH_AFRICA = 'South Africa'
    SOUTH_KOREA = 'South Korea'
    SPAIN = 'Spain'
    SWEDEN = 'Sweden'
    SWITZERLAND = 'Switzerland'
    TAIWAN = 'Taiwan'
    TANZANIA = 'Tanzania'
    THAILAND = 'Thailand'
    TURKEY = 'Turkey'
    U_S__VIRGIN_ISLANDS = 'U.S. Virgin Islands'
    UNITED_ARAB_EMIRATES = 'United Arab Emirates'
    UNITED_KINGDOM = 'United Kingdom'
    UNITED_STATES = 'United States'
    URUGUAY = 'Uruguay'
    VIETNAM = 'Vietnam'


class Exchange(Enum):
    OTC = "OTC"
    NYSE_ARCA = "AMEX"
    NASDAQ = "NASDAQ"
    NYSE = "NYSE"


class Index(Enum):
    DOW_JONES_COMPOSITE_AVERAGE = 'Dow Jones Composite Average'
    DOW_JONES_INDUSTRIAL_AVERAGE = 'Dow Jones Industrial Average'
    DOW_JONES_TRANSPORTATION_AVERAGE = 'Dow Jones Transportation Average'
    DOW_JONES_UTILITY_AVERAGE = 'Dow Jones Utility Average'
    KBW_NASDAQ_BANK_INDEX = 'KBW NASDAQ BANK INDEX'
    MINI_RUSSELL_2000_INDEX = 'MINI RUSSELL 2000 INDEX'
    NASDAQ_100 = 'NASDAQ 100'
    NASDAQ_100_TECHNOLOGY_SECTOR = 'NASDAQ 100 TECHNOLOGY SECTOR'
    NASDAQ_BANK = 'NASDAQ BANK'
    NASDAQ_BIOTECHNOLOGY = 'NASDAQ BIOTECHNOLOGY'
    NASDAQ_COMPOSITE = 'NASDAQ COMPOSITE'
    NASDAQ_COMPUTER = 'NASDAQ COMPUTER'
    NASDAQ_GOLDEN_DRAGON_CHINA_INDEX = 'NASDAQ GOLDEN DRAGON CHINA INDEX'
    NASDAQ_INDUSTRIAL = 'NASDAQ INDUSTRIAL'
    NASDAQ_INSURANCE = 'NASDAQ INSURANCE'
    NASDAQ_OTHER_FINANCE = 'NASDAQ OTHER FINANCE'
    NASDAQ_TELECOMMUNICATIONS = 'NASDAQ TELECOMMUNICATIONS'
    NASDAQ_TRANSPORTATION = 'NASDAQ TRANSPORTATION'
    NASDAQ_US_BENCHMARK_FOOD_PRODUCERS_INDEX = 'NASDAQ US BENCHMARK FOOD PRODUCERS INDEX'
    NYSE_ARCA_MAJOR_MARKET = 'NYSE ARCA MAJOR MARKET'
    PHLX_GOLD_AND_SILVER_SECTOR_INDEX = 'PHLX GOLD AND SILVER SECTOR INDEX'
    PHLX_HOUSING_SECTOR = 'PHLX HOUSING SECTOR'
    PHLX_OIL_SERVICE_SECTOR = 'PHLX OIL SERVICE SECTOR'
    PHLX_SEMICONDUCTOR = 'PHLX SEMICONDUCTOR'
    PHLX_UTILITY_SECTOR = 'PHLX UTILITY SECTOR'
    RUSSELL_1000 = 'RUSSELL 1000'
    RUSSELL_2000 = 'RUSSELL 2000'
    RUSSELL_3000 = 'RUSSELL 3000'
    SANDP_100 = 'S&P 100'
    SANDP_400 = 'S&P 400'
    SANDP_500 = 'S&P 500'
    SANDP_500_COMMUNICATION_SERVICES = 'S&P 500 Communication Services'
    SANDP_500_CONSUMER_DISCRETIONARY = 'S&P 500 Consumer Discretionary'
    SANDP_500_CONSUMER_STAPLES = 'S&P 500 Consumer Staples'
    SANDP_500_ESG_INDEX = 'S&P 500 ESG INDEX'
    SANDP_500_ENERGY = 'S&P 500 Energy'
    SANDP_500_FINANCIALS = 'S&P 500 Financials'
    SANDP_500_HEALTH_CARE = 'S&P 500 Health Care'
    SANDP_500_INDUSTRIALS = 'S&P 500 Industrials'
    SANDP_500_INFORMATION_TECHNOLOGY = 'S&P 500 Information Technology'
    SANDP_500_MATERIALS = 'S&P 500 Materials'
    SANDP_500_REAL_ESTATE = 'S&P 500 Real Estate'
    SANDP_500_UTILITIES = 'S&P 500 Utilities'


class Industry(Enum):
    ADVERTISINGMARKETING_SERVICES = 'Advertising/Marketing Services'
    AEROSPACE_AND_DEFENSE = 'Aerospace & Defense'
    AGRICULTURAL_COMMODITIESMILLING = 'Agricultural Commodities/Milling'
    AIR_FREIGHTCOURIERS = 'Air Freight/Couriers'
    AIRLINES = 'Airlines'
    ALTERNATIVE_POWER_GENERATION = 'Alternative Power Generation'
    ALUMINUM = 'Aluminum'
    APPARELFOOTWEAR = 'Apparel/Footwear'
    APPARELFOOTWEAR_RETAIL = 'Apparel/Footwear Retail'
    AUTO_PARTS_OEM = 'Auto Parts: OEM'
    AUTOMOTIVE_AFTERMARKET = 'Automotive Aftermarket'
    BEVERAGES_ALCOHOLIC = 'Beverages: Alcoholic'
    BEVERAGES_NONALCOHOLIC = 'Beverages: Non-Alcoholic'
    BIOTECHNOLOGY = 'Biotechnology'
    BROADCASTING = 'Broadcasting'
    BUILDING_PRODUCTS = 'Building Products'
    CABLESATELLITE_TV = 'Cable/Satellite TV'
    CASINOSGAMING = 'Casinos/Gaming'
    CATALOGSPECIALTY_DISTRIBUTION = 'Catalog/Specialty Distribution'
    CHEMICALS_AGRICULTURAL = 'Chemicals: Agricultural'
    CHEMICALS_MAJOR_DIVERSIFIED = 'Chemicals: Major Diversified'
    CHEMICALS_SPECIALTY = 'Chemicals: Specialty'
    COAL = 'Coal'
    COMMERCIAL_PRINTINGFORMS = 'Commercial Printing/Forms'
    COMPUTER_COMMUNICATIONS = 'Computer Communications'
    COMPUTER_PERIPHERALS = 'Computer Peripherals'
    COMPUTER_PROCESSING_HARDWARE = 'Computer Processing Hardware'
    CONSTRUCTION_MATERIALS = 'Construction Materials'
    CONSUMER_SUNDRIES = 'Consumer Sundries'
    CONTAINERSPACKAGING = 'Containers/Packaging'
    CONTRACT_DRILLING = 'Contract Drilling'
    DATA_PROCESSING_SERVICES = 'Data Processing Services'
    DEPARTMENT_STORES = 'Department Stores'
    DISCOUNT_STORES = 'Discount Stores'
    DRUGSTORE_CHAINS = 'Drugstore Chains'
    ELECTRIC_UTILITIES = 'Electric Utilities'
    ELECTRICAL_PRODUCTS = 'Electrical Products'
    ELECTRONIC_COMPONENTS = 'Electronic Components'
    ELECTRONIC_EQUIPMENTINSTRUMENTS = 'Electronic Equipment/Instruments'
    ELECTRONIC_PRODUCTION_EQUIPMENT = 'Electronic Production Equipment'
    ELECTRONICS_DISTRIBUTORS = 'Electronics Distributors'
    ELECTRONICSAPPLIANCE_STORES = 'Electronics/Appliance Stores'
    ELECTRONICSAPPLIANCES = 'Electronics/Appliances'
    ENGINEERING_AND_CONSTRUCTION = 'Engineering & Construction'
    ENVIRONMENTAL_SERVICES = 'Environmental Services'
    FINANCERENTALLEASING = 'Finance/Rental/Leasing'
    FINANCIAL_CONGLOMERATES = 'Financial Conglomerates'
    FINANCIAL_PUBLISHINGSERVICES = 'Financial Publishing/Services'
    FOOD_DISTRIBUTORS = 'Food Distributors'
    FOOD_RETAIL = 'Food Retail'
    FOOD_MAJOR_DIVERSIFIED = 'Food: Major Diversified'
    FOOD_MEATFISHDAIRY = 'Food: Meat/Fish/Dairy'
    FOOD_SPECIALTYCANDY = 'Food: Specialty/Candy'
    FOREST_PRODUCTS = 'Forest Products'
    GAS_DISTRIBUTORS = 'Gas Distributors'
    GENERAL_GOVERNMENT = 'General Government'
    HOME_FURNISHINGS = 'Home Furnishings'
    HOME_IMPROVEMENT_CHAINS = 'Home Improvement Chains'
    HOMEBUILDING = 'Homebuilding'
    HOSPITALNURSING_MANAGEMENT = 'Hospital/Nursing Management'
    HOTELSRESORTSCRUISE_LINES = 'Hotels/Resorts/Cruise lines'
    HOUSEHOLDPERSONAL_CARE = 'Household/Personal Care'
    INDUSTRIAL_CONGLOMERATES = 'Industrial Conglomerates'
    INDUSTRIAL_MACHINERY = 'Industrial Machinery'
    INDUSTRIAL_SPECIALTIES = 'Industrial Specialties'
    INFORMATION_TECHNOLOGY_SERVICES = 'Information Technology Services'
    INSURANCE_BROKERSSERVICES = 'Insurance Brokers/Services'
    INTEGRATED_OIL = 'Integrated Oil'
    INTERNET_RETAIL = 'Internet Retail'
    INTERNET_SOFTWARESERVICES = 'Internet Software/Services'
    INVESTMENT_BANKSBROKERS = 'Investment Banks/Brokers'
    INVESTMENT_MANAGERS = 'Investment Managers'
    INVESTMENT_TRUSTSMUTUAL_FUNDS = 'Investment Trusts/Mutual Funds'
    LIFEHEALTH_INSURANCE = 'Life/Health Insurance'
    MAJOR_BANKS = 'Major Banks'
    MAJOR_TELECOMMUNICATIONS = 'Major Telecommunications'
    MANAGED_HEALTH_CARE = 'Managed Health Care'
    MARINE_SHIPPING = 'Marine Shipping'
    MEDIA_CONGLOMERATES = 'Media Conglomerates'
    MEDICAL_DISTRIBUTORS = 'Medical Distributors'
    MEDICAL_SPECIALTIES = 'Medical Specialties'
    MEDICALNURSING_SERVICES = 'Medical/Nursing Services'
    METAL_FABRICATION = 'Metal Fabrication'
    MISCELLANEOUS = 'Miscellaneous'
    MISCELLANEOUS_COMMERCIAL_SERVICES = 'Miscellaneous Commercial Services'
    MISCELLANEOUS_MANUFACTURING = 'Miscellaneous Manufacturing'
    MOTOR_VEHICLES = 'Motor Vehicles'
    MOVIESENTERTAINMENT = 'Movies/Entertainment'
    MULTILINE_INSURANCE = 'Multi-Line Insurance'
    OFFICE_EQUIPMENTSUPPLIES = 'Office Equipment/Supplies'
    OIL_AND_GAS_PIPELINES = 'Oil & Gas Pipelines'
    OIL_AND_GAS_PRODUCTION = 'Oil & Gas Production'
    OIL_REFININGMARKETING = 'Oil Refining/Marketing'
    OILFIELD_SERVICESEQUIPMENT = 'Oilfield Services/Equipment'
    OTHER_CONSUMER_SERVICES = 'Other Consumer Services'
    OTHER_CONSUMER_SPECIALTIES = 'Other Consumer Specialties'
    OTHER_METALSMINERALS = 'Other Metals/Minerals'
    OTHER_TRANSPORTATION = 'Other Transportation'
    PACKAGED_SOFTWARE = 'Packaged Software'
    PERSONNEL_SERVICES = 'Personnel Services'
    PHARMACEUTICALS_GENERIC = 'Pharmaceuticals: Generic'
    PHARMACEUTICALS_MAJOR = 'Pharmaceuticals: Major'
    PHARMACEUTICALS_OTHER = 'Pharmaceuticals: Other'
    PRECIOUS_METALS = 'Precious Metals'
    PROPERTYCASUALTY_INSURANCE = 'Property/Casualty Insurance'
    PUBLISHING_BOOKSMAGAZINES = 'Publishing: Books/Magazines'
    PUBLISHING_NEWSPAPERS = 'Publishing: Newspapers'
    PULP_AND_PAPER = 'Pulp & Paper'
    RAILROADS = 'Railroads'
    REAL_ESTATE_DEVELOPMENT = 'Real Estate Development'
    REAL_ESTATE_INVESTMENT_TRUSTS = 'Real Estate Investment Trusts'
    RECREATIONAL_PRODUCTS = 'Recreational Products'
    REGIONAL_BANKS = 'Regional Banks'
    RESTAURANTS = 'Restaurants'
    SAVINGS_BANKS = 'Savings Banks'
    SEMICONDUCTORS = 'Semiconductors'
    SERVICES_TO_THE_HEALTH_INDUSTRY = 'Services to the Health Industry'
    SPECIALTY_INSURANCE = 'Specialty Insurance'
    SPECIALTY_STORES = 'Specialty Stores'
    SPECIALTY_TELECOMMUNICATIONS = 'Specialty Telecommunications'
    STEEL = 'Steel'
    TELECOMMUNICATIONS_EQUIPMENT = 'Telecommunications Equipment'
    TEXTILES = 'Textiles'
    TOBACCO = 'Tobacco'
    TOOLS_AND_HARDWARE = 'Tools & Hardware'
    TRUCKING = 'Trucking'
    TRUCKSCONSTRUCTIONFARM_MACHINERY = 'Trucks/Construction/Farm Machinery'
    WATER_UTILITIES = 'Water Utilities'
    WHOLESALE_DISTRIBUTORS = 'Wholesale Distributors'
    WIRELESS_TELECOMMUNICATIONS = 'Wireless Telecommunications'


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


class Market(Enum):
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
