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


class StockField(Field):
    # ----------------------------------
    # Common Fields
    # ----------------------------------
    ALL_TIME_HIGH = "All Time High", "High.All", None, False, False
    ALL_TIME_LOW = "All Time Low", "Low.All", None, False, False
    ALL_TIME_PERFORMANCE = "All Time Performance", "Perf.All", "percent", False, False
    AROON_DOWN_14 = "Aroon Down (14)", "Aroon.Down", None, True, False
    AROON_UP_14 = "Aroon Up (14)", "Aroon.Up", None, True, False
    AVERAGE_DAY_RANGE_14 = "Average Day Range (14)", "ADR", None, True, False
    AVERAGE_DIRECTIONAL_INDEX_14 = "Average Directional Index (14)", "ADX", None, True, False
    AVERAGE_TRUE_RANGE_14 = "Average True Range (14)", "ATR", None, True, False
    AWESOME_OSCILLATOR = "Awesome Oscillator", "AO", None, True, False
    BOLLINGER_LOWER_BAND_20 = "Bollinger Lower Band (20)", "BB.lower", None, True, False
    BOLLINGER_UPPER_BAND_20 = "Bollinger Upper Band (20)", "BB.upper", None, True, False
    BULL_BEAR_POWER = "Bull Bear Power", "BBPower", None, True, False
    CHANGE_PERCENT = "Change %", "change", None, True, False
    COMMODITY_CHANNEL_INDEX_20 = "Commodity Channel Index (20)", "CCI20", None, True, False
    CURRENCY = "Currency", "currency", None, False, False
    DESCRIPTION = "Description", "description", None, False, False
    DONCHIAN_CHANNELS_LOWER_BAND_20 = "Donchian Channels Lower Band (20)", "DonchCh20.Lower", None, True, False
    DONCHIAN_CHANNELS_UPPER_BAND_20 = "Donchian Channels Upper Band (20)", "DonchCh20.Upper", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_10 = "Exponential Moving Average (10)", "EMA10", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_100 = "Exponential Moving Average (100)", "EMA100", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_20 = "Exponential Moving Average (20)", "EMA20", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_200 = "Exponential Moving Average (200)", "EMA200", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_30 = "Exponential Moving Average (30)", "EMA30", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_5 = "Exponential Moving Average (5)", "EMA5", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_50 = "Exponential Moving Average (50)", "EMA50", None, True, False
    FRACTIONAL = "Fractional", "fractional", "bool", False, False
    FUNDAMENTAL_CURRENCY_CODE = "Fundamental Currency Code", "fundamental_currency_code", None, False, False
    GAP_PERCENT = "Gap %", "gap", None, True, False
    HIGH = "High", "high", None, True, False
    HULL_MOVING_AVERAGE_9 = "Hull Moving Average (9)", "HullMA9", None, True, False
    ICHIMOKU_BASE_LINE_9_26_52_26 = "Ichimoku Base Line (9, 26, 52, 26)", "Ichimoku.BLine", None, True, False
    ICHIMOKU_CONVERSION_LINE_9_26_52_26 = "Ichimoku Conversion Line (9, 26, 52, 26)", "Ichimoku.CLine", None, True, False
    ICHIMOKU_LEADING_SPAN_A_9_26_52_26 = "Ichimoku Leading Span A (9, 26, 52, 26)", "Ichimoku.Lead1", None, True, False
    ICHIMOKU_LEADING_SPAN_B_9_26_52_26 = "Ichimoku Leading Span B (9, 26, 52, 26)", "Ichimoku.Lead2", None, True, False
    KELTNER_CHANNELS_LOWER_BAND_20 = "Keltner Channels Lower Band (20)", "KltChnl.lower", None, True, False
    KELTNER_CHANNELS_UPPER_BAND_20 = "Keltner Channels Upper Band (20)", "KltChnl.upper", None, True, False
    LOW = "Low", "low", None, True, False
    MACD_LEVEL_12_26 = "MACD Level (12, 26)", "MACD.macd", None, True, False
    MACD_SIGNAL_12_26 = "MACD Signal (12, 26)", "MACD.signal", None, True, False
    MIN_MOVE = "Min Move", "minmov", None, False, False
    MIN_MOVE_2 = "Min Move 2", "minmove2", None, False, False
    MOMENTUM_10 = "Momentum (10)", "Mom", None, True, False
    MONTHLY_PERFORMANCE = "Monthly Performance", "Perf.1M", "percent", False, False
    MONTH_HIGH_1 = "1-Month High", "High.1M", None, False, False
    MONTH_HIGH_3 = "3-Month High", "High.3M", None, False, False
    MONTH_HIGH_6 = "6-Month High", "High.6M", None, False, False
    MONTH_LOW_1 = "1-Month Low", "Low.1M", None, False, False
    MONTH_LOW_3 = "3-Month Low", "Low.3M", None, False, False
    MONTH_LOW_6 = "6-Month Low", "Low.6M", None, False, False
    MONTH_PERFORMANCE_3 = "3-Month Performance", "Perf.3M", "percent", False, False
    MONTH_PERFORMANCE_6 = "6-Month Performance", "Perf.6M", "percent", False, False
    MOVING_AVERAGES_RATING = "Moving Averages Rating", "Recommend.MA", "rating", True, False
    NAME = "Name", "name", None, False, False
    NEGATIVE_DIRECTIONAL_INDICATOR_14 = "Negative Directional Indicator (14)", "ADX-DI", None, True, False
    OPEN = "Open", "open", None, True, False
    OSCILLATORS_RATING = "Oscillators Rating", "Recommend.Other", "rating", True, False
    PARABOLIC_SAR = "Parabolic SAR", "P.SAR", None, True, False
    PIVOT_CAMARILLA_P = "Pivot Camarilla P", "Pivot.M.Camarilla.Middle", None, True, False
    PIVOT_CAMARILLA_R1 = "Pivot Camarilla R1", "Pivot.M.Camarilla.R1", None, True, False
    PIVOT_CAMARILLA_R2 = "Pivot Camarilla R2", "Pivot.M.Camarilla.R2", None, True, False
    PIVOT_CAMARILLA_R3 = "Pivot Camarilla R3", "Pivot.M.Camarilla.R3", None, True, False
    PIVOT_CAMARILLA_S1 = "Pivot Camarilla S1", "Pivot.M.Camarilla.S1", None, True, False
    PIVOT_CAMARILLA_S2 = "Pivot Camarilla S2", "Pivot.M.Camarilla.S2", None, True, False
    PIVOT_CAMARILLA_S3 = "Pivot Camarilla S3", "Pivot.M.Camarilla.S3", None, True, False
    PIVOT_CLASSIC_P = "Pivot Classic P", "Pivot.M.Classic.Middle", None, True, False
    PIVOT_CLASSIC_R1 = "Pivot Classic R1", "Pivot.M.Classic.R1", None, True, False
    PIVOT_CLASSIC_R2 = "Pivot Classic R2", "Pivot.M.Classic.R2", None, True, False
    PIVOT_CLASSIC_R3 = "Pivot Classic R3", "Pivot.M.Classic.R3", None, True, False
    PIVOT_CLASSIC_S1 = "Pivot Classic S1", "Pivot.M.Classic.S1", None, True, False
    PIVOT_CLASSIC_S2 = "Pivot Classic S2", "Pivot.M.Classic.S2", None, True, False
    PIVOT_CLASSIC_S3 = "Pivot Classic S3", "Pivot.M.Classic.S3", None, True, False
    PIVOT_DM_P = "Pivot DM P", "Pivot.M.Demark.Middle", None, True, False
    PIVOT_DM_R1 = "Pivot DM R1", "Pivot.M.Demark.R1", None, True, False
    PIVOT_DM_S1 = "Pivot DM S1", "Pivot.M.Demark.S1", None, True, False
    PIVOT_FIBONACCI_P = "Pivot Fibonacci P", "Pivot.M.Fibonacci.Middle", None, True, False
    PIVOT_FIBONACCI_R1 = "Pivot Fibonacci R1", "Pivot.M.Fibonacci.R1", None, True, False
    PIVOT_FIBONACCI_R2 = "Pivot Fibonacci R2", "Pivot.M.Fibonacci.R2", None, True, False
    PIVOT_FIBONACCI_R3 = "Pivot Fibonacci R3", "Pivot.M.Fibonacci.R3", None, True, False
    PIVOT_FIBONACCI_S1 = "Pivot Fibonacci S1", "Pivot.M.Fibonacci.S1", None, True, False
    PIVOT_FIBONACCI_S2 = "Pivot Fibonacci S2", "Pivot.M.Fibonacci.S2", None, True, False
    PIVOT_FIBONACCI_S3 = "Pivot Fibonacci S3", "Pivot.M.Fibonacci.S3", None, True, False
    PIVOT_WOODIE_P = "Pivot Woodie P", "Pivot.M.Woodie.Middle", None, True, False
    PIVOT_WOODIE_R1 = "Pivot Woodie R1", "Pivot.M.Woodie.R1", None, True, False
    PIVOT_WOODIE_R2 = "Pivot Woodie R2", "Pivot.M.Woodie.R2", None, True, False
    PIVOT_WOODIE_R3 = "Pivot Woodie R3", "Pivot.M.Woodie.R3", None, True, False
    PIVOT_WOODIE_S1 = "Pivot Woodie S1", "Pivot.M.Woodie.S1", None, True, False
    PIVOT_WOODIE_S2 = "Pivot Woodie S2", "Pivot.M.Woodie.S2", None, True, False
    PIVOT_WOODIE_S3 = "Pivot Woodie S3", "Pivot.M.Woodie.S3", None, True, False
    POSITIVE_DIRECTIONAL_INDICATOR_14 = "Positive Directional Indicator (14)", "ADX+DI", None, True, False
    PRICE = "Price", "close", None, True, False
    PRICE_SCALE = "Price Scale", "pricescale", None, False, False
    RATE_OF_CHANGE_9 = "Rate Of Change (9)", "ROC", None, True, False
    RELATIVE_STRENGTH_INDEX_14 = "Relative Strength Index (14)", "RSI", None, True, False
    RELATIVE_STRENGTH_INDEX_7 = "Relative Strength Index (7)", "RSI7", None, True, False
    SIMPLE_MOVING_AVERAGE_10 = "Simple Moving Average (10)", "SMA10", None, True, False
    SIMPLE_MOVING_AVERAGE_100 = "Simple Moving Average (100)", "SMA100", None, True, False
    SIMPLE_MOVING_AVERAGE_20 = "Simple Moving Average (20)", "SMA20", None, True, False
    SIMPLE_MOVING_AVERAGE_200 = "Simple Moving Average (200)", "SMA200", None, True, False
    SIMPLE_MOVING_AVERAGE_30 = "Simple Moving Average (30)", "SMA30", None, True, False
    SIMPLE_MOVING_AVERAGE_5 = "Simple Moving Average (5)", "SMA5", None, True, False
    SIMPLE_MOVING_AVERAGE_50 = "Simple Moving Average (50)", "SMA50", None, True, False
    STOCHASTIC_PERCENTD_14_3_3 = "Stochastic %D (14, 3, 3)", "Stoch.D", None, True, False
    STOCHASTIC_PERCENTK_14_3_3 = "Stochastic %K (14, 3, 3)", "Stoch.K", None, True, False
    STOCHASTIC_RSI_FAST_3_3_14_14 = "Stochastic RSI Fast (3, 3, 14, 14)", "Stoch.RSI.K", None, True, False
    STOCHASTIC_RSI_SLOW_3_3_14_14 = "Stochastic RSI Slow (3, 3, 14, 14)", "Stoch.RSI.D", None, True, False
    SUBTYPE = "Subtype", "subtype", None, False, False
    TECHNICAL_RATING = "Technical Rating", "Recommend.All", "rating", True, False
    TYPE = "Type", "type", None, False, False
    ULTIMATE_OSCILLATOR_7_14_28 = "Ultimate Oscillator (7, 14, 28)", "UO", None, True, False
    VOLATILITY = "Volatility", "Volatility.D", None, False, False
    VOLATILITY_MONTH = "Volatility Month", "Volatility.M", None, False, False
    VOLATILITY_WEEK = "Volatility Week", "Volatility.W", None, False, False
    VOLUME_WEIGHTED_AVERAGE_PRICE = "Volume Weighted Average Price", "VWAP", None, True, False
    VOLUME_WEIGHTED_MOVING_AVERAGE_20 = "Volume Weighted Moving Average (20)", "VWMA", None, True, False
    WEEKLY_PERFORMANCE = "Weekly Performance", "Perf.W", "percent", False, False
    WEEK_HIGH_52 = "52 Week High", "price_52_week_high", None, False, False
    WEEK_LOW_52 = "52 Week Low", "price_52_week_low", None, False, False
    WILLIAMS_PERCENT_RANGE_14 = "Williams Percent Range (14)", "W.R", None, True, False
    YEARLY_PERFORMANCE = "Yearly Performance", "Perf.Y", "percent", False, False
    YTD_PERFORMANCE = "YTD Performance", "Perf.YTD", "percent", False, False
    Y_PERFORMANCE_5 = "5Y Performance", "Perf.5Y", "percent", False, False
    # ----------------------------------
    # Specifics Fields
    # ----------------------------------
    ABANDONEDBABY_BEARISH = "AbandonedBaby Bearish", "Candle.AbandonedBaby.Bearish", None, True, False
    ABANDONEDBABY_BULLISH = "AbandonedBaby Bullish", "Candle.AbandonedBaby.Bullish", None, True, False
    BASIC_EPS_FY = "Basic EPS (FY)", "basic_eps_net_income", None, False, False
    BASIC_EPS_TTM = "Basic EPS (TTM)", "earnings_per_share_basic_ttm", None, False, False
    BLACKCROWS_3 = "3BlackCrows", "Candle.3BlackCrows", None, True, False
    CASH_AND_EQUIVALENTS_FY = "Cash & Equivalents (FY)", "cash_n_equivalents_fy", None, False, False
    CASH_AND_EQUIVALENTS_MRQ = "Cash & Equivalents (MRQ)", "cash_n_equivalents_fq", None, False, False
    CASH_AND_SHORT_TERM_INVESTMENTS_FY = "Cash and short term investments (FY)", "cash_n_short_term_invest_fy", None, False, False
    CASH_AND_SHORT_TERM_INVESTMENTS_MRQ = "Cash and short term investments (MRQ)", "cash_n_short_term_invest_fq", None, False, False
    CHAIKIN_MONEY_FLOW_20 = "Chaikin Money Flow (20)", "ChaikinMoneyFlow", None, False, False
    CHANGE = "Change", "change_abs", None, True, False
    CHANGE_15MIN = "Change 15m", "change_abs|15", None, False, False
    CHANGE_15MIN_PERCENT = "Change 15m, %", "change|15", None, False, False
    CHANGE_1H = "Change 1h", "change_abs|60", None, False, False
    CHANGE_1H_PERCENT = "Change 1h, %", "change|60", None, False, False
    CHANGE_1MIN = "Change 1m", "change_abs|1", None, False, False
    CHANGE_1M = "Change 1M", "change_abs|1M", None, False, False
    CHANGE_1MIN_PERCENT = "Change 1m, %", "change|1", None, False, False
    CHANGE_1M_PERCENT = "Change 1M, %", "change|1M", None, False, False
    CHANGE_1W = "Change 1W", "change_abs|1W", None, False, False
    CHANGE_1W_PERCENT = "Change 1W, %", "change|1W", None, False, False
    CHANGE_4H = "Change 4h", "change_abs|240", None, False, False
    CHANGE_4H_PERCENT = "Change 4h, %", "change|240", None, False, False
    CHANGE_5MIN = "Change 5m", "change_abs|5", None, False, False
    CHANGE_5MIN_PERCENT = "Change 5m, %", "change|5", None, False, False
    CHANGE_FROM_OPEN = "Change from Open", "change_from_open_abs", None, True, False
    CHANGE_FROM_OPEN_PERCENT = "Change from Open %", "change_from_open", None, True, False
    CURRENT_RATIO_MRQ = "Current Ratio (MRQ)", "current_ratio", None, False, False
    DEBT_TO_EQUITY_RATIO_MRQ = "Debt to Equity Ratio (MRQ)", "debt_to_equity", None, False, False
    DIVIDENDS_PAID_FY = "Dividends Paid (FY)", "dividends_paid", None, False, False
    DIVIDENDS_PER_SHARE_ANNUAL_YOY_GROWTH = "Dividends per share (Annual YoY Growth)", "dps_common_stock_prim_issue_yoy_growth_fy", None, False, False
    DIVIDENDS_PER_SHARE_FY = "Dividends per Share (FY)", "dps_common_stock_prim_issue_fy", None, False, False
    DIVIDENDS_PER_SHARE_MRQ = "Dividends per Share (MRQ)", "dividends_per_share_fq", None, False, False
    DIVIDEND_YIELD_FORWARD = "Dividend Yield Forward", "dividend_yield_recent", None, False, False
    DOJI = "Doji", "Candle.Doji", None, True, False
    DOJI_DRAGONFLY = "Doji Dragonfly", "Candle.Doji.Dragonfly", None, True, False
    DOJI_GRAVESTONE = "Doji Gravestone", "Candle.Doji.Gravestone", None, True, False
    EBITDA_ANNUAL_YOY_GROWTH = "EBITDA (Annual YoY Growth)", "ebitda_yoy_growth_fy", None, False, False
    EBITDA_QUARTERLY_QOQ_GROWTH = "EBITDA (Quarterly QoQ Growth)", "ebitda_qoq_growth_fq", None, False, False
    EBITDA_QUARTERLY_YOY_GROWTH = "EBITDA (Quarterly YoY Growth)", "ebitda_yoy_growth_fq", None, False, False
    EBITDA_TTM = "EBITDA (TTM)", "ebitda", None, False, False
    EBITDA_TTM_YOY_GROWTH = "EBITDA (TTM YoY Growth)", "ebitda_yoy_growth_ttm", None, False, False
    ENGULFING_BEARISH = "Engulfing Bearish", "Candle.Engulfing.Bearish", None, True, False
    ENGULFING_BULLISH = "Engulfing Bullish", "Candle.Engulfing.Bullish", None, True, False
    ENTERPRISE_VALUEEBITDA_TTM = "Enterprise Value/EBITDA (TTM)", "enterprise_value_ebitda_ttm", None, False, False
    ENTERPRISE_VALUE_MRQ = "Enterprise Value (MRQ)", "enterprise_value_fq", None, False, False
    EPS_DILUTED_ANNUAL_YOY_GROWTH = "EPS Diluted (Annual YoY Growth)", "earnings_per_share_diluted_yoy_growth_fy", None, False, False
    EPS_DILUTED_FY = "EPS Diluted (FY)", "last_annual_eps", None, False, False
    EPS_DILUTED_MRQ = "EPS Diluted (MRQ)", "earnings_per_share_fq", None, False, False
    EPS_DILUTED_QUARTERLY_QOQ_GROWTH = "EPS Diluted (Quarterly QoQ Growth)", "earnings_per_share_diluted_qoq_growth_fq", None, False, False
    EPS_DILUTED_QUARTERLY_YOY_GROWTH = "EPS Diluted (Quarterly YoY Growth)", "earnings_per_share_diluted_yoy_growth_fq", None, False, False
    EPS_DILUTED_TTM = "EPS Diluted (TTM)", "earnings_per_share_diluted_ttm", None, False, False
    EPS_DILUTED_TTM_YOY_GROWTH = "EPS Diluted (TTM YoY Growth)", "earnings_per_share_diluted_yoy_growth_ttm", None, False, False
    EPS_FORECAST_MRQ = "EPS Forecast (MRQ)", "earnings_per_share_forecast_next_fq", None, False, False
    EVENINGSTAR = "EveningStar", "Candle.EveningStar", None, True, False
    FREE_CASH_FLOW_ANNUAL_YOY_GROWTH = "Free Cash Flow (Annual YoY Growth)", "free_cash_flow_yoy_growth_fy", None, False, False
    FREE_CASH_FLOW_MARGIN_FY = "Free Cash Flow Margin (FY)", "free_cash_flow_margin_fy", None, False, False
    FREE_CASH_FLOW_MARGIN_TTM = "Free Cash Flow Margin (TTM)", "free_cash_flow_margin_ttm", None, False, False
    FREE_CASH_FLOW_QUARTERLY_QOQ_GROWTH = "Free Cash Flow (Quarterly QoQ Growth)", "free_cash_flow_qoq_growth_fq", None, False, False
    FREE_CASH_FLOW_QUARTERLY_YOY_GROWTH = "Free Cash Flow (Quarterly YoY Growth)", "free_cash_flow_yoy_growth_fq", None, False, False
    FREE_CASH_FLOW_TTM_YOY_GROWTH = "Free Cash Flow (TTM YoY Growth)", "free_cash_flow_yoy_growth_ttm", None, False, False
    GOODWILL = "Goodwill", "goodwill", None, False, False
    GROSS_MARGIN_FY = "Gross Margin (FY)", "gross_profit_margin_fy", None, False, False
    GROSS_MARGIN_TTM = "Gross Margin (TTM)", "gross_margin", None, False, False
    GROSS_PROFIT_ANNUAL_YOY_GROWTH = "Gross Profit (Annual YoY Growth)", "gross_profit_yoy_growth_fy", None, False, False
    GROSS_PROFIT_FY = "Gross Profit (FY)", "gross_profit", None, False, False
    GROSS_PROFIT_MRQ = "Gross Profit (MRQ)", "gross_profit_fq", None, False, False
    GROSS_PROFIT_QUARTERLY_QOQ_GROWTH = "Gross Profit (Quarterly QoQ Growth)", "gross_profit_qoq_growth_fq", None, False, False
    GROSS_PROFIT_QUARTERLY_YOY_GROWTH = "Gross Profit (Quarterly YoY Growth)", "gross_profit_yoy_growth_fq", None, False, False
    GROSS_PROFIT_TTM_YOY_GROWTH = "Gross Profit (TTM YoY Growth)", "gross_profit_yoy_growth_ttm", None, False, False
    HAMMER = "Hammer", "Candle.Hammer", None, True, False
    HANGINGMAN = "HangingMan", "Candle.HangingMan", None, True, False
    HARAMI_BEARISH = "Harami Bearish", "Candle.Harami.Bearish", None, True, False
    HARAMI_BULLISH = "Harami Bullish", "Candle.Harami.Bullish", None, True, False
    INDUSTRY = "Industry", "industry", None, False, False
    INVERTEDHAMMER = "InvertedHammer", "Candle.InvertedHammer", None, True, False
    KICKING_BEARISH = "Kicking Bearish", "Candle.Kicking.Bearish", None, True, False
    KICKING_BULLISH = "Kicking Bullish", "Candle.Kicking.Bullish", None, True, False
    LAST_YEAR_REVENUE_FY = "Last Year Revenue (FY)", "last_annual_revenue", None, False, False
    LONGSHADOW_LOWER = "LongShadow Lower", "Candle.LongShadow.Lower", None, True, False
    LONGSHADOW_UPPER = "LongShadow Upper", "Candle.LongShadow.Upper", None, True, False
    MARKET_CAPITALIZATION = "Market Capitalization", "market_cap_basic", None, False, False
    MARUBOZU_BLACK = "Marubozu Black", "Candle.Marubozu.Black", None, True, False
    MARUBOZU_WHITE = "Marubozu White", "Candle.Marubozu.White", None, True, False
    MONEY_FLOW_14 = "Money Flow (14)", "MoneyFlow", None, True, False
    MORNINGSTAR = "MorningStar", "Candle.MorningStar", None, True, False
    NET_DEBT_MRQ = "Net Debt (MRQ)", "net_debt", None, False, False
    NET_INCOME_ANNUAL_YOY_GROWTH = "Net Income (Annual YoY Growth)", "net_income_yoy_growth_fy", None, False, False
    NET_INCOME_FY = "Net Income (FY)", "net_income", None, False, False
    NET_INCOME_QUARTERLY_QOQ_GROWTH = "Net Income (Quarterly QoQ Growth)", "net_income_qoq_growth_fq", None, False, False
    NET_INCOME_QUARTERLY_YOY_GROWTH = "Net Income (Quarterly YoY Growth)", "net_income_yoy_growth_fq", None, False, False
    NET_INCOME_TTM_YOY_GROWTH = "Net Income (TTM YoY Growth)", "net_income_yoy_growth_ttm", None, False, False
    NET_MARGIN_FY = "Net Margin (FY)", "net_income_bef_disc_oper_margin_fy", None, False, False
    NET_MARGIN_TTM = "Net Margin (TTM)", "after_tax_margin", None, False, False
    NUMBER_OF_EMPLOYEES = "Number of Employees", "number_of_employees", None, False, False
    NUMBER_OF_SHAREHOLDERS = "Number of Shareholders", "number_of_shareholders", None, False, False
    OPERATING_MARGIN_FY = "Operating Margin (FY)", "oper_income_margin_fy", None, False, False
    OPERATING_MARGIN_TTM = "Operating Margin (TTM)", "operating_margin", None, False, False
    PATTERN = "Pattern", "candlestick", None, True, False
    POSTMARKET_CHANGE = "Post-market Change", "postmarket_change_abs", None, False, False
    POSTMARKET_CHANGE_PERCENT = "Post-market Change %", "postmarket_change", None, False, False
    POSTMARKET_CLOSE = "Post-market Close", "postmarket_close", None, False, False
    POSTMARKET_HIGH = "Post-market High", "postmarket_high", None, False, False
    POSTMARKET_LOW = "Post-market Low", "postmarket_low", None, False, False
    POSTMARKET_OPEN = "Post-market Open", "postmarket_open", None, False, False
    POSTMARKET_VOLUME = "Post-market Volume", "postmarket_volume", None, False, False
    PREMARKET_CHANGE = "Pre-market Change", "premarket_change_abs", None, False, False
    PREMARKET_CHANGE_FROM_OPEN = "Pre-market Change from Open", "premarket_change_from_open_abs", None, False, False
    PREMARKET_CHANGE_FROM_OPEN_PERCENT = "Pre-market Change from Open %", "premarket_change_from_open", None, False, False
    PREMARKET_CHANGE_PERCENT = "Pre-market Change %", "premarket_change", None, False, False
    PREMARKET_CLOSE = "Pre-market Close", "premarket_close", None, False, False
    PREMARKET_GAP_PERCENT = "Pre-market Gap %", "premarket_gap", None, False, False
    PREMARKET_HIGH = "Pre-market High", "premarket_high", None, False, False
    PREMARKET_LOW = "Pre-market Low", "premarket_low", None, False, False
    PREMARKET_OPEN = "Pre-market Open", "premarket_open", None, False, False
    PREMARKET_VOLUME = "Pre-market Volume", "premarket_volume", None, False, False
    PRETAX_MARGIN_TTM = "Pretax Margin (TTM)", "pre_tax_margin", None, False, False
    PRICE_TO_BOOK_FY = "Price to Book (FY)", "price_book_ratio", None, False, False
    PRICE_TO_BOOK_MRQ = "Price to Book (MRQ)", "price_book_fq", None, False, False
    PRICE_TO_EARNINGS_RATIO_TTM = "Price to Earnings Ratio (TTM)", "price_earnings_ttm", None, False, False
    PRICE_TO_FREE_CASH_FLOW_TTM = "Price to Free Cash Flow (TTM)", "price_free_cash_flow_ttm", None, False, False
    PRICE_TO_REVENUE_RATIO_TTM = "Price to Revenue Ratio (TTM)", "price_revenue_ttm", None, False, False
    PRICE_TO_SALES_FY = "Price to Sales (FY)", "price_sales_ratio", None, False, False
    QUICK_RATIO_MRQ = "Quick Ratio (MRQ)", "quick_ratio", None, False, False
    RECENT_EARNINGS_DATE = "Recent Earnings Date", "earnings_release_date", None, False, False
    RELATIVE_VOLUME = "Relative Volume", "relative_volume_10d_calc", None, True, False
    RESEARCH_AND_DEVELOPMENT_RATIO_FY = "Research & development Ratio (FY)", "research_and_dev_ratio_fy", None, False, False
    RESEARCH_AND_DEVELOPMENT_RATIO_TTM = "Research & development Ratio (TTM)", "research_and_dev_ratio_ttm", None, False, False
    RETURN_ON_ASSETS_TTM = "Return on Assets (TTM)", "return_on_assets", None, False, False
    RETURN_ON_EQUITY_TTM = "Return on Equity (TTM)", "return_on_equity", None, False, False
    RETURN_ON_INVESTED_CAPITAL_TTM = "Return on Invested Capital (TTM)", "return_on_invested_capital", None, False, False
    REVENUE_ANNUAL_YOY_GROWTH = "Revenue (Annual YoY Growth)", "total_revenue_yoy_growth_fy", None, False, False
    REVENUE_PER_EMPLOYEE_FY = "Revenue per Employee (FY)", "revenue_per_employee", None, False, False
    REVENUE_QUARTERLY_QOQ_GROWTH = "Revenue (Quarterly QoQ Growth)", "total_revenue_qoq_growth_fq", None, False, False
    REVENUE_QUARTERLY_YOY_GROWTH = "Revenue (Quarterly YoY Growth)", "total_revenue_yoy_growth_fq", None, False, False
    REVENUE_TTM_YOY_GROWTH = "Revenue (TTM YoY Growth)", "total_revenue_yoy_growth_ttm", None, False, False
    SELLING_GENERAL_AND_ADMIN_EXPENSES_RATIO_FY = "Selling General & Admin expenses Ratio (FY)", "sell_gen_admin_exp_other_ratio_fy", None, False, False
    SELLING_GENERAL_AND_ADMIN_EXPENSES_RATIO_TTM = "Selling General & Admin expenses Ratio (TTM)", "sell_gen_admin_exp_other_ratio_ttm", None, False, False
    SHARES_FLOAT = "Shares Float", "float_shares_outstanding", None, False, False
    SHOOTINGSTAR = "ShootingStar", "Candle.ShootingStar", None, True, False
    SPINNINGTOP_BLACK = "SpinningTop Black", "Candle.SpinningTop.Black", None, True, False
    SPINNINGTOP_WHITE = "SpinningTop White", "Candle.SpinningTop.White", None, True, False
    SUBMARKET = "Submarket", "submarket", None, False, False
    TOTAL_ASSETS_ANNUAL_YOY_GROWTH = "Total Assets (Annual YoY Growth)", "total_assets_yoy_growth_fy", None, False, False
    TOTAL_ASSETS_MRQ = "Total Assets (MRQ)", "total_assets", None, False, False
    TOTAL_ASSETS_QUARTERLY_QOQ_GROWTH = "Total Assets (Quarterly QoQ Growth)", "total_assets_qoq_growth_fq", None, False, False
    TOTAL_ASSETS_QUARTERLY_YOY_GROWTH = "Total Assets (Quarterly YoY Growth)", "total_assets_yoy_growth_fq", None, False, False
    TOTAL_CURRENT_ASSETS_MRQ = "Total Current Assets (MRQ)", "total_current_assets", None, False, False
    TOTAL_DEBT_ANNUAL_YOY_GROWTH = "Total Debt (Annual YoY Growth)", "total_debt_yoy_growth_fy", None, False, False
    TOTAL_DEBT_MRQ = "Total Debt (MRQ)", "total_debt", None, False, False
    TOTAL_DEBT_QUARTERLY_QOQ_GROWTH = "Total Debt (Quarterly QoQ Growth)", "total_debt_qoq_growth_fq", None, False, False
    TOTAL_DEBT_QUARTERLY_YOY_GROWTH = "Total Debt (Quarterly YoY Growth)", "total_debt_yoy_growth_fq", None, False, False
    TOTAL_LIABILITIES_FY = "Total Liabilities (FY)", "total_liabilities_fy", None, False, False
    TOTAL_LIABILITIES_MRQ = "Total Liabilities (MRQ)", "total_liabilities_fq", None, False, False
    TOTAL_REVENUE_FY = "Total Revenue (FY)", "total_revenue", None, False, False
    TOTAL_SHARES_OUTSTANDING = "Total Shares Outstanding", "total_shares_outstanding_fundamental", None, False, False
    TRISTAR_BEARISH = "TriStar Bearish", "Candle.TriStar.Bearish", None, True, False
    TRISTAR_BULLISH = "TriStar Bullish", "Candle.TriStar.Bullish", None, True, False
    UPCOMING_EARNINGS_DATE = "Upcoming Earnings Date", "earnings_release_next_date", None, False, False
    VOLUME = "Volume", "volume", None, True, False
    VOLUMEXPRICE = "Volume*Price", "Value.Traded", None, True, False
    WHITESOLDIERS_3 = "3WhiteSoldiers", "Candle.3WhiteSoldiers", None, True, False
    YEAR_BETA_1 = "1-Year Beta", "beta_1_year", None, False, False


class ForexField(Field):
    # ----------------------------------
    # Common Fields
    # ----------------------------------
    ALL_TIME_HIGH = "All Time High", "High.All", None, False, False
    ALL_TIME_LOW = "All Time Low", "Low.All", None, False, False
    ALL_TIME_PERFORMANCE = "All Time Performance", "Perf.All", "percent", False, False
    AROON_DOWN_14 = "Aroon Down (14)", "Aroon.Down", None, True, False
    AROON_UP_14 = "Aroon Up (14)", "Aroon.Up", None, True, False
    AVERAGE_DAY_RANGE_14 = "Average Day Range (14)", "ADR", None, True, False
    AVERAGE_DIRECTIONAL_INDEX_14 = "Average Directional Index (14)", "ADX", None, True, False
    AVERAGE_TRUE_RANGE_14 = "Average True Range (14)", "ATR", None, True, False
    AWESOME_OSCILLATOR = "Awesome Oscillator", "AO", None, True, False
    BOLLINGER_LOWER_BAND_20 = "Bollinger Lower Band (20)", "BB.lower", None, True, False
    BOLLINGER_UPPER_BAND_20 = "Bollinger Upper Band (20)", "BB.upper", None, True, False
    BULL_BEAR_POWER = "Bull Bear Power", "BBPower", None, True, False
    CHANGE_PERCENT = "Change %", "change", None, True, False
    COMMODITY_CHANNEL_INDEX_20 = "Commodity Channel Index (20)", "CCI20", None, True, False
    CURRENCY = "Currency", "currency", None, False, False
    DESCRIPTION = "Description", "description", None, False, False
    DONCHIAN_CHANNELS_LOWER_BAND_20 = "Donchian Channels Lower Band (20)", "DonchCh20.Lower", None, True, False
    DONCHIAN_CHANNELS_UPPER_BAND_20 = "Donchian Channels Upper Band (20)", "DonchCh20.Upper", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_10 = "Exponential Moving Average (10)", "EMA10", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_100 = "Exponential Moving Average (100)", "EMA100", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_20 = "Exponential Moving Average (20)", "EMA20", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_200 = "Exponential Moving Average (200)", "EMA200", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_30 = "Exponential Moving Average (30)", "EMA30", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_5 = "Exponential Moving Average (5)", "EMA5", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_50 = "Exponential Moving Average (50)", "EMA50", None, True, False
    FRACTIONAL = "Fractional", "fractional", "bool", False, False
    FUNDAMENTAL_CURRENCY_CODE = "Fundamental Currency Code", "fundamental_currency_code", None, False, False
    GAP_PERCENT = "Gap %", "gap", None, True, False
    HIGH = "High", "high", None, True, False
    HULL_MOVING_AVERAGE_9 = "Hull Moving Average (9)", "HullMA9", None, True, False
    ICHIMOKU_BASE_LINE_9_26_52_26 = "Ichimoku Base Line (9, 26, 52, 26)", "Ichimoku.BLine", None, True, False
    ICHIMOKU_CONVERSION_LINE_9_26_52_26 = "Ichimoku Conversion Line (9, 26, 52, 26)", "Ichimoku.CLine", None, True, False
    ICHIMOKU_LEADING_SPAN_A_9_26_52_26 = "Ichimoku Leading Span A (9, 26, 52, 26)", "Ichimoku.Lead1", None, True, False
    ICHIMOKU_LEADING_SPAN_B_9_26_52_26 = "Ichimoku Leading Span B (9, 26, 52, 26)", "Ichimoku.Lead2", None, True, False
    KELTNER_CHANNELS_LOWER_BAND_20 = "Keltner Channels Lower Band (20)", "KltChnl.lower", None, True, False
    KELTNER_CHANNELS_UPPER_BAND_20 = "Keltner Channels Upper Band (20)", "KltChnl.upper", None, True, False
    LOW = "Low", "low", None, True, False
    MACD_LEVEL_12_26 = "MACD Level (12, 26)", "MACD.macd", None, True, False
    MACD_SIGNAL_12_26 = "MACD Signal (12, 26)", "MACD.signal", None, True, False
    MIN_MOVE = "Min Move", "minmov", None, False, False
    MIN_MOVE_2 = "Min Move 2", "minmove2", None, False, False
    MOMENTUM_10 = "Momentum (10)", "Mom", None, True, False
    MONTHLY_PERFORMANCE = "Monthly Performance", "Perf.1M", "percent", False, False
    MONTH_HIGH_1 = "1-Month High", "High.1M", None, False, False
    MONTH_HIGH_3 = "3-Month High", "High.3M", None, False, False
    MONTH_HIGH_6 = "6-Month High", "High.6M", None, False, False
    MONTH_LOW_1 = "1-Month Low", "Low.1M", None, False, False
    MONTH_LOW_3 = "3-Month Low", "Low.3M", None, False, False
    MONTH_LOW_6 = "6-Month Low", "Low.6M", None, False, False
    MONTH_PERFORMANCE_3 = "3-Month Performance", "Perf.3M", "percent", False, False
    MONTH_PERFORMANCE_6 = "6-Month Performance", "Perf.6M", "percent", False, False
    MOVING_AVERAGES_RATING = "Moving Averages Rating", "Recommend.MA", "rating", True, False
    NAME = "Name", "name", None, False, False
    NEGATIVE_DIRECTIONAL_INDICATOR_14 = "Negative Directional Indicator (14)", "ADX-DI", None, True, False
    OPEN = "Open", "open", None, True, False
    OSCILLATORS_RATING = "Oscillators Rating", "Recommend.Other", "rating", True, False
    PARABOLIC_SAR = "Parabolic SAR", "P.SAR", None, True, False
    PIVOT_CAMARILLA_P = "Pivot Camarilla P", "Pivot.M.Camarilla.Middle", None, True, False
    PIVOT_CAMARILLA_R1 = "Pivot Camarilla R1", "Pivot.M.Camarilla.R1", None, True, False
    PIVOT_CAMARILLA_R2 = "Pivot Camarilla R2", "Pivot.M.Camarilla.R2", None, True, False
    PIVOT_CAMARILLA_R3 = "Pivot Camarilla R3", "Pivot.M.Camarilla.R3", None, True, False
    PIVOT_CAMARILLA_S1 = "Pivot Camarilla S1", "Pivot.M.Camarilla.S1", None, True, False
    PIVOT_CAMARILLA_S2 = "Pivot Camarilla S2", "Pivot.M.Camarilla.S2", None, True, False
    PIVOT_CAMARILLA_S3 = "Pivot Camarilla S3", "Pivot.M.Camarilla.S3", None, True, False
    PIVOT_CLASSIC_P = "Pivot Classic P", "Pivot.M.Classic.Middle", None, True, False
    PIVOT_CLASSIC_R1 = "Pivot Classic R1", "Pivot.M.Classic.R1", None, True, False
    PIVOT_CLASSIC_R2 = "Pivot Classic R2", "Pivot.M.Classic.R2", None, True, False
    PIVOT_CLASSIC_R3 = "Pivot Classic R3", "Pivot.M.Classic.R3", None, True, False
    PIVOT_CLASSIC_S1 = "Pivot Classic S1", "Pivot.M.Classic.S1", None, True, False
    PIVOT_CLASSIC_S2 = "Pivot Classic S2", "Pivot.M.Classic.S2", None, True, False
    PIVOT_CLASSIC_S3 = "Pivot Classic S3", "Pivot.M.Classic.S3", None, True, False
    PIVOT_DM_P = "Pivot DM P", "Pivot.M.Demark.Middle", None, True, False
    PIVOT_DM_R1 = "Pivot DM R1", "Pivot.M.Demark.R1", None, True, False
    PIVOT_DM_S1 = "Pivot DM S1", "Pivot.M.Demark.S1", None, True, False
    PIVOT_FIBONACCI_P = "Pivot Fibonacci P", "Pivot.M.Fibonacci.Middle", None, True, False
    PIVOT_FIBONACCI_R1 = "Pivot Fibonacci R1", "Pivot.M.Fibonacci.R1", None, True, False
    PIVOT_FIBONACCI_R2 = "Pivot Fibonacci R2", "Pivot.M.Fibonacci.R2", None, True, False
    PIVOT_FIBONACCI_R3 = "Pivot Fibonacci R3", "Pivot.M.Fibonacci.R3", None, True, False
    PIVOT_FIBONACCI_S1 = "Pivot Fibonacci S1", "Pivot.M.Fibonacci.S1", None, True, False
    PIVOT_FIBONACCI_S2 = "Pivot Fibonacci S2", "Pivot.M.Fibonacci.S2", None, True, False
    PIVOT_FIBONACCI_S3 = "Pivot Fibonacci S3", "Pivot.M.Fibonacci.S3", None, True, False
    PIVOT_WOODIE_P = "Pivot Woodie P", "Pivot.M.Woodie.Middle", None, True, False
    PIVOT_WOODIE_R1 = "Pivot Woodie R1", "Pivot.M.Woodie.R1", None, True, False
    PIVOT_WOODIE_R2 = "Pivot Woodie R2", "Pivot.M.Woodie.R2", None, True, False
    PIVOT_WOODIE_R3 = "Pivot Woodie R3", "Pivot.M.Woodie.R3", None, True, False
    PIVOT_WOODIE_S1 = "Pivot Woodie S1", "Pivot.M.Woodie.S1", None, True, False
    PIVOT_WOODIE_S2 = "Pivot Woodie S2", "Pivot.M.Woodie.S2", None, True, False
    PIVOT_WOODIE_S3 = "Pivot Woodie S3", "Pivot.M.Woodie.S3", None, True, False
    POSITIVE_DIRECTIONAL_INDICATOR_14 = "Positive Directional Indicator (14)", "ADX+DI", None, True, False
    PRICE = "Price", "close", None, True, False
    PRICE_SCALE = "Price Scale", "pricescale", None, False, False
    RATE_OF_CHANGE_9 = "Rate Of Change (9)", "ROC", None, True, False
    RELATIVE_STRENGTH_INDEX_14 = "Relative Strength Index (14)", "RSI", None, True, False
    RELATIVE_STRENGTH_INDEX_7 = "Relative Strength Index (7)", "RSI7", None, True, False
    SIMPLE_MOVING_AVERAGE_10 = "Simple Moving Average (10)", "SMA10", None, True, False
    SIMPLE_MOVING_AVERAGE_100 = "Simple Moving Average (100)", "SMA100", None, True, False
    SIMPLE_MOVING_AVERAGE_20 = "Simple Moving Average (20)", "SMA20", None, True, False
    SIMPLE_MOVING_AVERAGE_200 = "Simple Moving Average (200)", "SMA200", None, True, False
    SIMPLE_MOVING_AVERAGE_30 = "Simple Moving Average (30)", "SMA30", None, True, False
    SIMPLE_MOVING_AVERAGE_5 = "Simple Moving Average (5)", "SMA5", None, True, False
    SIMPLE_MOVING_AVERAGE_50 = "Simple Moving Average (50)", "SMA50", None, True, False
    STOCHASTIC_PERCENTD_14_3_3 = "Stochastic %D (14, 3, 3)", "Stoch.D", None, True, False
    STOCHASTIC_PERCENTK_14_3_3 = "Stochastic %K (14, 3, 3)", "Stoch.K", None, True, False
    STOCHASTIC_RSI_FAST_3_3_14_14 = "Stochastic RSI Fast (3, 3, 14, 14)", "Stoch.RSI.K", None, True, False
    STOCHASTIC_RSI_SLOW_3_3_14_14 = "Stochastic RSI Slow (3, 3, 14, 14)", "Stoch.RSI.D", None, True, False
    SUBTYPE = "Subtype", "subtype", None, False, False
    TECHNICAL_RATING = "Technical Rating", "Recommend.All", "rating", True, False
    TYPE = "Type", "type", None, False, False
    ULTIMATE_OSCILLATOR_7_14_28 = "Ultimate Oscillator (7, 14, 28)", "UO", None, True, False
    VOLATILITY = "Volatility", "Volatility.D", None, False, False
    VOLATILITY_MONTH = "Volatility Month", "Volatility.M", None, False, False
    VOLATILITY_WEEK = "Volatility Week", "Volatility.W", None, False, False
    VOLUME_WEIGHTED_AVERAGE_PRICE = "Volume Weighted Average Price", "VWAP", None, True, False
    VOLUME_WEIGHTED_MOVING_AVERAGE_20 = "Volume Weighted Moving Average (20)", "VWMA", None, True, False
    WEEKLY_PERFORMANCE = "Weekly Performance", "Perf.W", "percent", False, False
    WEEK_HIGH_52 = "52 Week High", "price_52_week_high", None, False, False
    WEEK_LOW_52 = "52 Week Low", "price_52_week_low", None, False, False
    WILLIAMS_PERCENT_RANGE_14 = "Williams Percent Range (14)", "W.R", None, True, False
    YEARLY_PERFORMANCE = "Yearly Performance", "Perf.Y", "percent", False, False
    YTD_PERFORMANCE = "YTD Performance", "Perf.YTD", "percent", False, False
    Y_PERFORMANCE_5 = "5Y Performance", "Perf.5Y", "percent", False, False
    # ----------------------------------
    # Specifics Fields
    # ----------------------------------
    ASK = "Ask", "ask", None, False, False
    BID = "Bid", "bid", None, False, False
    GROUP = "Group", "sector", None, False, False
    REGION = "Region", "country", None, False, False


class CryptoField(Field):
    # ----------------------------------
    # Common Fields
    # ----------------------------------
    ALL_TIME_HIGH = "All Time High", "High.All", None, False, False
    ALL_TIME_LOW = "All Time Low", "Low.All", None, False, False
    ALL_TIME_PERFORMANCE = "All Time Performance", "Perf.All", "percent", False, False
    AROON_DOWN_14 = "Aroon Down (14)", "Aroon.Down", None, True, False
    AROON_UP_14 = "Aroon Up (14)", "Aroon.Up", None, True, False
    AVERAGE_DAY_RANGE_14 = "Average Day Range (14)", "ADR", None, True, False
    AVERAGE_DIRECTIONAL_INDEX_14 = "Average Directional Index (14)", "ADX", None, True, False
    AVERAGE_TRUE_RANGE_14 = "Average True Range (14)", "ATR", None, True, False
    AWESOME_OSCILLATOR = "Awesome Oscillator", "AO", None, True, False
    BOLLINGER_LOWER_BAND_20 = "Bollinger Lower Band (20)", "BB.lower", None, True, False
    BOLLINGER_UPPER_BAND_20 = "Bollinger Upper Band (20)", "BB.upper", None, True, False
    BULL_BEAR_POWER = "Bull Bear Power", "BBPower", None, True, False
    CHANGE_PERCENT = "Change %", "change", None, True, False
    COMMODITY_CHANNEL_INDEX_20 = "Commodity Channel Index (20)", "CCI20", None, True, False
    CURRENCY = "Currency", "currency", None, False, False
    DESCRIPTION = "Description", "description", None, False, False
    DONCHIAN_CHANNELS_LOWER_BAND_20 = "Donchian Channels Lower Band (20)", "DonchCh20.Lower", None, True, False
    DONCHIAN_CHANNELS_UPPER_BAND_20 = "Donchian Channels Upper Band (20)", "DonchCh20.Upper", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_10 = "Exponential Moving Average (10)", "EMA10", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_100 = "Exponential Moving Average (100)", "EMA100", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_20 = "Exponential Moving Average (20)", "EMA20", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_200 = "Exponential Moving Average (200)", "EMA200", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_30 = "Exponential Moving Average (30)", "EMA30", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_5 = "Exponential Moving Average (5)", "EMA5", None, True, False
    EXPONENTIAL_MOVING_AVERAGE_50 = "Exponential Moving Average (50)", "EMA50", None, True, False
    FRACTIONAL = "Fractional", "fractional", "bool", False, False
    FUNDAMENTAL_CURRENCY_CODE = "Fundamental Currency Code", "fundamental_currency_code", None, False, False
    GAP_PERCENT = "Gap %", "gap", None, True, False
    HIGH = "High", "high", None, True, False
    HULL_MOVING_AVERAGE_9 = "Hull Moving Average (9)", "HullMA9", None, True, False
    ICHIMOKU_BASE_LINE_9_26_52_26 = "Ichimoku Base Line (9, 26, 52, 26)", "Ichimoku.BLine", None, True, False
    ICHIMOKU_CONVERSION_LINE_9_26_52_26 = "Ichimoku Conversion Line (9, 26, 52, 26)", "Ichimoku.CLine", None, True, False
    ICHIMOKU_LEADING_SPAN_A_9_26_52_26 = "Ichimoku Leading Span A (9, 26, 52, 26)", "Ichimoku.Lead1", None, True, False
    ICHIMOKU_LEADING_SPAN_B_9_26_52_26 = "Ichimoku Leading Span B (9, 26, 52, 26)", "Ichimoku.Lead2", None, True, False
    KELTNER_CHANNELS_LOWER_BAND_20 = "Keltner Channels Lower Band (20)", "KltChnl.lower", None, True, False
    KELTNER_CHANNELS_UPPER_BAND_20 = "Keltner Channels Upper Band (20)", "KltChnl.upper", None, True, False
    LOW = "Low", "low", None, True, False
    MACD_LEVEL_12_26 = "MACD Level (12, 26)", "MACD.macd", None, True, False
    MACD_SIGNAL_12_26 = "MACD Signal (12, 26)", "MACD.signal", None, True, False
    MIN_MOVE = "Min Move", "minmov", None, False, False
    MIN_MOVE_2 = "Min Move 2", "minmove2", None, False, False
    MOMENTUM_10 = "Momentum (10)", "Mom", None, True, False
    MONTHLY_PERFORMANCE = "Monthly Performance", "Perf.1M", "percent", False, False
    MONTH_HIGH_1 = "1-Month High", "High.1M", None, False, False
    MONTH_HIGH_3 = "3-Month High", "High.3M", None, False, False
    MONTH_HIGH_6 = "6-Month High", "High.6M", None, False, False
    MONTH_LOW_1 = "1-Month Low", "Low.1M", None, False, False
    MONTH_LOW_3 = "3-Month Low", "Low.3M", None, False, False
    MONTH_LOW_6 = "6-Month Low", "Low.6M", None, False, False
    MONTH_PERFORMANCE_3 = "3-Month Performance", "Perf.3M", "percent", False, False
    MONTH_PERFORMANCE_6 = "6-Month Performance", "Perf.6M", "percent", False, False
    MOVING_AVERAGES_RATING = "Moving Averages Rating", "Recommend.MA", "rating", True, False
    NAME = "Name", "name", None, False, False
    NEGATIVE_DIRECTIONAL_INDICATOR_14 = "Negative Directional Indicator (14)", "ADX-DI", None, True, False
    OPEN = "Open", "open", None, True, False
    OSCILLATORS_RATING = "Oscillators Rating", "Recommend.Other", "rating", True, False
    PARABOLIC_SAR = "Parabolic SAR", "P.SAR", None, True, False
    PIVOT_CAMARILLA_P = "Pivot Camarilla P", "Pivot.M.Camarilla.Middle", None, True, False
    PIVOT_CAMARILLA_R1 = "Pivot Camarilla R1", "Pivot.M.Camarilla.R1", None, True, False
    PIVOT_CAMARILLA_R2 = "Pivot Camarilla R2", "Pivot.M.Camarilla.R2", None, True, False
    PIVOT_CAMARILLA_R3 = "Pivot Camarilla R3", "Pivot.M.Camarilla.R3", None, True, False
    PIVOT_CAMARILLA_S1 = "Pivot Camarilla S1", "Pivot.M.Camarilla.S1", None, True, False
    PIVOT_CAMARILLA_S2 = "Pivot Camarilla S2", "Pivot.M.Camarilla.S2", None, True, False
    PIVOT_CAMARILLA_S3 = "Pivot Camarilla S3", "Pivot.M.Camarilla.S3", None, True, False
    PIVOT_CLASSIC_P = "Pivot Classic P", "Pivot.M.Classic.Middle", None, True, False
    PIVOT_CLASSIC_R1 = "Pivot Classic R1", "Pivot.M.Classic.R1", None, True, False
    PIVOT_CLASSIC_R2 = "Pivot Classic R2", "Pivot.M.Classic.R2", None, True, False
    PIVOT_CLASSIC_R3 = "Pivot Classic R3", "Pivot.M.Classic.R3", None, True, False
    PIVOT_CLASSIC_S1 = "Pivot Classic S1", "Pivot.M.Classic.S1", None, True, False
    PIVOT_CLASSIC_S2 = "Pivot Classic S2", "Pivot.M.Classic.S2", None, True, False
    PIVOT_CLASSIC_S3 = "Pivot Classic S3", "Pivot.M.Classic.S3", None, True, False
    PIVOT_DM_P = "Pivot DM P", "Pivot.M.Demark.Middle", None, True, False
    PIVOT_DM_R1 = "Pivot DM R1", "Pivot.M.Demark.R1", None, True, False
    PIVOT_DM_S1 = "Pivot DM S1", "Pivot.M.Demark.S1", None, True, False
    PIVOT_FIBONACCI_P = "Pivot Fibonacci P", "Pivot.M.Fibonacci.Middle", None, True, False
    PIVOT_FIBONACCI_R1 = "Pivot Fibonacci R1", "Pivot.M.Fibonacci.R1", None, True, False
    PIVOT_FIBONACCI_R2 = "Pivot Fibonacci R2", "Pivot.M.Fibonacci.R2", None, True, False
    PIVOT_FIBONACCI_R3 = "Pivot Fibonacci R3", "Pivot.M.Fibonacci.R3", None, True, False
    PIVOT_FIBONACCI_S1 = "Pivot Fibonacci S1", "Pivot.M.Fibonacci.S1", None, True, False
    PIVOT_FIBONACCI_S2 = "Pivot Fibonacci S2", "Pivot.M.Fibonacci.S2", None, True, False
    PIVOT_FIBONACCI_S3 = "Pivot Fibonacci S3", "Pivot.M.Fibonacci.S3", None, True, False
    PIVOT_WOODIE_P = "Pivot Woodie P", "Pivot.M.Woodie.Middle", None, True, False
    PIVOT_WOODIE_R1 = "Pivot Woodie R1", "Pivot.M.Woodie.R1", None, True, False
    PIVOT_WOODIE_R2 = "Pivot Woodie R2", "Pivot.M.Woodie.R2", None, True, False
    PIVOT_WOODIE_R3 = "Pivot Woodie R3", "Pivot.M.Woodie.R3", None, True, False
    PIVOT_WOODIE_S1 = "Pivot Woodie S1", "Pivot.M.Woodie.S1", None, True, False
    PIVOT_WOODIE_S2 = "Pivot Woodie S2", "Pivot.M.Woodie.S2", None, True, False
    PIVOT_WOODIE_S3 = "Pivot Woodie S3", "Pivot.M.Woodie.S3", None, True, False
    POSITIVE_DIRECTIONAL_INDICATOR_14 = "Positive Directional Indicator (14)", "ADX+DI", None, True, False
    PRICE = "Price", "close", None, True, False
    PRICE_SCALE = "Price Scale", "pricescale", None, False, False
    RATE_OF_CHANGE_9 = "Rate Of Change (9)", "ROC", None, True, False
    RELATIVE_STRENGTH_INDEX_14 = "Relative Strength Index (14)", "RSI", None, True, False
    RELATIVE_STRENGTH_INDEX_7 = "Relative Strength Index (7)", "RSI7", None, True, False
    SIMPLE_MOVING_AVERAGE_10 = "Simple Moving Average (10)", "SMA10", None, True, False
    SIMPLE_MOVING_AVERAGE_100 = "Simple Moving Average (100)", "SMA100", None, True, False
    SIMPLE_MOVING_AVERAGE_20 = "Simple Moving Average (20)", "SMA20", None, True, False
    SIMPLE_MOVING_AVERAGE_200 = "Simple Moving Average (200)", "SMA200", None, True, False
    SIMPLE_MOVING_AVERAGE_30 = "Simple Moving Average (30)", "SMA30", None, True, False
    SIMPLE_MOVING_AVERAGE_5 = "Simple Moving Average (5)", "SMA5", None, True, False
    SIMPLE_MOVING_AVERAGE_50 = "Simple Moving Average (50)", "SMA50", None, True, False
    STOCHASTIC_PERCENTD_14_3_3 = "Stochastic %D (14, 3, 3)", "Stoch.D", None, True, False
    STOCHASTIC_PERCENTK_14_3_3 = "Stochastic %K (14, 3, 3)", "Stoch.K", None, True, False
    STOCHASTIC_RSI_FAST_3_3_14_14 = "Stochastic RSI Fast (3, 3, 14, 14)", "Stoch.RSI.K", None, True, False
    STOCHASTIC_RSI_SLOW_3_3_14_14 = "Stochastic RSI Slow (3, 3, 14, 14)", "Stoch.RSI.D", None, True, False
    SUBTYPE = "Subtype", "subtype", None, False, False
    TECHNICAL_RATING = "Technical Rating", "Recommend.All", "rating", True, False
    TYPE = "Type", "type", None, False, False
    ULTIMATE_OSCILLATOR_7_14_28 = "Ultimate Oscillator (7, 14, 28)", "UO", None, True, False
    VOLATILITY = "Volatility", "Volatility.D", None, False, False
    VOLATILITY_MONTH = "Volatility Month", "Volatility.M", None, False, False
    VOLATILITY_WEEK = "Volatility Week", "Volatility.W", None, False, False
    VOLUME_WEIGHTED_AVERAGE_PRICE = "Volume Weighted Average Price", "VWAP", None, True, False
    VOLUME_WEIGHTED_MOVING_AVERAGE_20 = "Volume Weighted Moving Average (20)", "VWMA", None, True, False
    WEEKLY_PERFORMANCE = "Weekly Performance", "Perf.W", "percent", False, False
    WEEK_HIGH_52 = "52 Week High", "price_52_week_high", None, False, False
    WEEK_LOW_52 = "52 Week Low", "price_52_week_low", None, False, False
    WILLIAMS_PERCENT_RANGE_14 = "Williams Percent Range (14)", "W.R", None, True, False
    YEARLY_PERFORMANCE = "Yearly Performance", "Perf.Y", "percent", False, False
    YTD_PERFORMANCE = "YTD Performance", "Perf.YTD", "percent", False, False
    Y_PERFORMANCE_5 = "5Y Performance", "Perf.5Y", "percent", False, False
    # ----------------------------------
    # Specifics Fields
    # ----------------------------------
    ASK = "Ask", "ask", None, False, False
    AVAILABLE_COINS = "Available Coins", "total_shares_outstanding", None, False, False
    AVERAGE_VOLUME_10_DAY = "Average Volume (10 day)", "average_volume_10d_calc", None, False, False
    AVERAGE_VOLUME_30_DAY = "Average Volume (30 day)", "average_volume_30d_calc", None, False, False
    AVERAGE_VOLUME_60_DAY = "Average Volume (60 day)", "average_volume_60d_calc", None, False, False
    AVERAGE_VOLUME_90_DAY = "Average Volume (90 day)", "average_volume_90d_calc", None, False, False
    BID = "Bid", "bid", None, False, False
    EXCHANGE = "Exchange", "exchange", None, False, False
    FULLY_DILUTED_MARKET_CAP = "Fully Diluted Market Cap", "market_cap_diluted_calc", None, False, False
    MARKET_CAPITALIZATION = "Market Capitalization", "market_cap_calc", None, False, False
    RELATIVE_VOLUME = "Relative Volume", "relative_volume_10d_calc", None, True, False
    RELATIVE_VOLUME_AT_TIME = "Relative Volume at Time", "relative_volume_intraday|5", None, False, False
    TOTAL_COINS = "Total Coins", "total_shares_diluted", None, False, False
    TRADED_VOLUME = "Traded Volume", "total_value_traded", None, False, False
    VOLUME = "Volume", "volume", None, True, False
    VOLUME_24H_CHANGE_PERCENT = "Volume 24h Change %", "24h_vol_change|5", None, False, False
    VOLUME_24H_IN_USD = "Volume 24h in USD", "24h_vol|5", None, False, False


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
