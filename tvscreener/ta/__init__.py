from tvscreener.field import Rating


def crossesup(x1, x2, y1, y2):
    if x1 > y1 and x2 < y2:
        return True
    else:
        return False


def adx(adx_, dminus, dplus, dminus_old, dplus_old):
    if crossesup(dplus, dplus_old, dminus, dminus_old) and adx_ > 20:
        return "B"
    elif crossesup(dminus, dminus_old, dplus, dplus_old) and adx_ > 20:
        return "S"
    else:
        return "N"
