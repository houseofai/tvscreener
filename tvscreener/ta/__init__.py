from tvscreener.field import Rating

buy_char = "&#x2303; B"
sell_char = "&#x2304; S"
neutral_char = "- N"


def crossesup(x1, x2, y1, y2):
    if x1 > y1 and x2 < y2:
        return True
    else:
        return False


def adx(adx_, dminus, dplus, dminus_old, dplus_old):
    if crossesup(dplus, dplus_old, dminus, dminus_old) and adx_ > 20:
        return buy_char
    elif crossesup(dminus, dminus_old, dplus, dplus_old) and adx_ > 20:
        return sell_char
    else:
        return neutral_char


def ao(ao_, ao_old_1, ao_old_2):
    if ao_ > ao_old_1 and ao_old_1 < ao_old_2:
        return buy_char
    elif ao_ < ao_old_1 and ao_old_1 > ao_old_2:
        return sell_char
    else:
        return neutral_char
