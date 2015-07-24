from itertools import chain
from cvxopt import matrix, solvers, spmatrix
import numpy as np
solvers.options['show_progress'] = False


def _second_order_derivative_matrix(size_of_matrix):
    """ Return a second order derivative matrix
    for a given signal size
    Parameters:
        size_of_matrix(int): Size of matrix
    Returns:
        second_order(cvxopt.spmatrix): Sparse matrix
        that has the second order derivative matrix
    """
    temp = size_of_matrix - 2
    first = [1, -2, 1] * temp
    second = list(chain.from_iterable([[ii] * 3 for ii in range(temp)]))
    third = list(chain.from_iterable([[ii, ii + 1, ii + 2] for ii in range(temp)]))
    second_order = spmatrix(first, second, third)

    return second_order


def _l1(signal, regularizer):
    """
    Parameters:
        signal(np.ndarray): Original, volatile signal
        regularizer(float): regularizer to keep the balance between smoothing
            and 'truthfulness' of the signal
    Returns:
        trend(np.ndarray): Trend of the signal extracted from l1 regularization

    Problem Formulation:
        minimize    (1/2) * ||x - signal||_2^2 + regularizer * sum(y)
        subject to  | D*x | <= y

    """

    signal_size = signal.size[0]
    temp = signal_size - 2
    temp_ls = range(temp)

    D = _second_order_derivative_matrix(signal_size)
    P = D * D.T
    q = -D * signal

    G = spmatrix([], [], [], (2 * temp, temp))
    G[:temp, :temp] = spmatrix(1.0, temp_ls, temp_ls)
    G[temp:, :temp] = -spmatrix(1.0, temp_ls, temp_ls)
    h = matrix(regularizer, (2 * temp, 1), tc='d')
    residual = solvers.qp(P, q, G, h)
    trend =  signal - D.T * residual['x']

    return trend


def _mad(array):
    """
    The Median Absolute Deviation along given axis of an array

    Parameters
        array(np.array) : array

    Returns
        mad : float
            `mad` = median(abs(`a` - center))/`c`
    """
    c = .6745 # constant
    center = np.apply_over_axes(np.median, array, 0)
    absolute_difference = np.fabs(array - center) / c

    return np.median(absolute_difference, axis=0)
