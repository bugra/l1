from algos import _l1
from cvxopt import matrix
import numpy as np
import pandas as pd
from statsmodels.robust.scale import mad

__all__ = ['l1', 'strip_outliers']

def l1(signal, regularizer):
    """
    Fits the l1 trend on top of the `signal` with a particular
    `regularizer`
    Parameters:
            signal(np.ndarray): Original Signal that we want to fit l1
                trend
            regularizer(float): Regularizer which provides a balance between
                smoothing of a signal and truthfulness of signal
    Returns:
        values(np.array): L1 Trend of a signal that is extracted from the signal
    """

    if not isinstance(signal, np.ndarray):
        raise TypeError("Signal Needs to be a numpy array")

    m = float(signal.min())
    M = float(signal.max())
    difference = M - m
    if not difference: # If signal is constant
        difference = 1
    t = (signal - m) / difference

    values = matrix(t)
    values = _l1(values, regularizer)
    values = values * difference + m
    values = np.asarray(values).squeeze()

    return values


def strip_outliers(original_signal, delta, mad_coef=3):
    """
    Based on l1 trend filtering, this function provides an endpoint
    """
    filtered_t = l1(original_signal, delta)

    diff = original_signal - filtered_t.squeeze()
    median_of_difference = np.median(diff)
    mad_of_difference = mad(diff)
    filtered_signal = original_signal.copy()
    threshold = mad_coef * mad_of_difference
    filtered_signal[np.abs(diff - median_of_difference) > threshold] = np.nan
    #filtered_signal = pd.Series(filtered_signal).fillna(method='ffill').fillna(method='bfill')

    return filtered_signal
