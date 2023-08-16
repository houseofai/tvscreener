from tvscreener.field import Rating


def isred(x1, x2):
    return x1 < x2


def isgreen(x1, x2):
    return x1 > x2


def crossesup(x1, x2, y1, y2):
    if x1 > y1 and x2 < y2:
        return True
    else:
        return False


def adx(adx_, dminus, dplus, dminus_old, dplus_old):
    if crossesup(dplus, dplus_old, dminus, dminus_old) and adx_ > 20:
        return Rating.BUY
    elif crossesup(dminus, dminus_old, dplus, dplus_old) and adx_ > 20:
        return Rating.SELL
    else:
        return Rating.NEUTRAL


def is_ao_bearish_cross(ao_, ao_old_1, ao_old_2):
    """
    Zero Line Cross:
    When AO crosses above the Zero Line, short term momentum is now rising faster than the long term momentum.
    This can present a bullish buying opportunity.
    """
    return ao_ < 0 < ao_old_1 and ao_old_2 > 0


def is_ao_bullish_cross(ao_, ao_old_1, ao_old_2):
    """
    Zero Line Cross:
    When AO crosses below the Zero Line, short term momentum is now falling faster than the long term momentum.
    This can present a bearish selling opportunity.
    """
    return ao_ > 0 > ao_old_1 and ao_old_2 < 0


def is_ao_bullish_saucer(ao_, ao_old_1, ao_old_2):
    """
    Saucer Setup:
    A Bullish Saucer setup occurs when the AO is above the Zero Line. It entails two consecutive red bars
    (with the second bar being lower than the first bar) being followed by a green Bar.
    """
    # Note: TradingView doesn't provide with a fourth bar, so we can't check if the third bar is red
    return ao_ > 0 and isgreen(ao_, ao_old_1) and isred(ao_old_1, ao_old_2)


def is_ao_bearish_saucer(ao_, ao_old_1, ao_old_2):
    """
    Saucer Setup:
    A Bearish Saucer setup occurs when the AO is below the Zero Line. It entails two consecutive green bars
    (with the second bar being higher than the first bar) being followed by a red bar.
    """
    # Note: TradingView doesn't provide with a fourth bar, so we can't check if the third bar is red
    return ao_ < 0 and isred(ao_, ao_old_1) and isgreen(ao_old_1, ao_old_2)


def ao(ao_, ao_old_1, ao_old_2):
    # TODO Twin Peaks: https://www.tradingview.com/scripts/awesomeoscillator/
    if is_ao_bullish_saucer(ao_, ao_old_1, ao_old_2) or is_ao_bullish_cross(ao_, ao_old_1, ao_old_2):
        return Rating.BUY
    elif is_ao_bearish_saucer(ao_, ao_old_1, ao_old_2) or is_ao_bearish_cross(ao_, ao_old_1, ao_old_2):
        return Rating.SELL
    else:
        return Rating.NEUTRAL


def bb_lower(low_limit, close):
    if close < low_limit:
        return Rating.BUY
    else:
        return Rating.NEUTRAL


def bb_upper(up_limit, close):
    if close > up_limit:
        return Rating.SELL
    else:
        return Rating.NEUTRAL