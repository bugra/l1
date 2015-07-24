import pandas as pd


def _strip_na(signal):
    """ Fill a numpy array's NA with first creating a left mask and
    a right mask using ffill and bfill methods
    """
    m = signal.min()
    lmask = pd.Series(signal).fillna(method='ffill').fillna(m-1) == m-1
    rmask = pd.Series(signal).fillna(method='bfill').fillna(m-1) == m-1
    mask = np.logical_or(lmask, rmask)
    filtered_series = signal[np.logical_not(mask)]

    return filtered_series
