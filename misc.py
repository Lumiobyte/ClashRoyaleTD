def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def para_multiplier(x, bottom, top):
    """
    Parabolic multiplier
    Return a larger y when x is at the bottom or top of the range.
    Used as a multiplier for scrolling
    """

    x = clamp(x, bottom, top)

    return abs(((2*x) / (top - bottom)) ** 2) + 1
