from cvxopt import base
from l1 import algos
import numpy as np
import pytest


@pytest.mark.algos
def test_second_order_derivative_matrix():

    def _check_size_zero(m, ii):
        assert bool(repr(m))
        if ii < 3:
            assert m.size == (0, 0)
        else:
            first = ii - 2
            assert m.size == (first, ii)
        assert m.typecode == 'd'
        assert isinstance(m.CCS, tuple)
        assert len(m.CCS) == 3
        for item in m.CCS:
            assert isinstance(item, base.matrix)

    # For size 0, 1, 2; the sizes should be (0, 0) tuple
    for ii in range(800):
        _check_size_zero(algos._second_order_derivative_matrix(ii), ii)


@pytest.mark.algos
@pytest.xfail(reason='Signal should be a ndarray')
def test_l1():
    signal = np.array(range(100))
    regularizer = 2.5
    values = algos._l1(signal, regularizer)
    assert values
    assert isinstance(values, np.ndarray)




