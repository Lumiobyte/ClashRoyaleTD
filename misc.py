import sys
import os


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


def lerp(a, b, c):
    """ Linear interpolation enables smooth movement of an object between two points a and b at speed c.
        The return value of this function is the number of pixels to move in that frame """
    return a+(b-a)*c


def format_timedelta(duration):
    """ Convert a datetime.timedelta to human-readable hours, minutes, and seconds """
    seconds = duration.total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"  # Don't show 0 hours


def check_exe():
    """ Returns true if the script is running as an executable """

    try:
        base_path = sys._MEIPASS
        return True
    except Exception:
        return False


def resource_path(relative_path):
    """ Helper to get filepaths to game assets """
    try:
        base_path = sys._MEIPASS # Get the temporary assets folder created by the PyInstaller executable
    except Exception:
        base_path = os.path.abspath(".") # Not running as compiled, search files normally

    return os.path.join(base_path, relative_path)