# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
from batemaneq import (
    bateman_full, bateman_full_arr, bateman_parent, bateman_parent_arr
)
import pytest

decay_analytic = {
    0: lambda y0, k, t: (
        y0[0] * np.exp(-k[0]*t)),
    1: lambda y0, k, t: (
        y0[1] * np.exp(-k[1] * t) + y0[0] * k[0] / (k[1] - k[0]) *
        (np.exp(-k[0]*t) - np.exp(-k[1]*t))),
    2: lambda y0, k, t: (
        y0[2] * np.exp(-k[2] * t) + y0[1] * k[1] / (k[2] - k[1]) *
        (np.exp(-k[1]*t) - np.exp(-k[2]*t)) +
        k[1] * k[0] * y0[0] / (k[1] - k[0]) *
        (1 / (k[2] - k[0]) * (np.exp(-k[0]*t) - np.exp(-k[2]*t)) -
         1 / (k[2] - k[1]) * (np.exp(-k[1]*t) - np.exp(-k[2]*t))))
}


def decay_get_Cref(k, y0, tout):
    coeffs = k + [0]*(3-len(k))
    return np.column_stack([
        decay_analytic[i](y0, coeffs, tout) for i in range(
            min(3, len(k)+1))])


def test_bateman_full():
    k0, k1, k2 = 2.0, 3.0, 4.0
    k = [k0, k1, k2]
    y0 = [0.7, 0.3, 0.5]
    t = np.linspace(0, 10, 17)
    yout = bateman_full(y0, k, t, exp=np.exp)
    yref = decay_get_Cref(k, y0, t)
    assert np.allclose(np.asarray(yout).T, yref)


def test_bateman_parent_arr():
    k = k0, k1, k2 = 2.0, 3.0, 4.0
    t = np.linspace(0, 10, 16).reshape((2, 2, 2, 2))
    yout = bateman_parent_arr(np.asarray(k), t)
    assert yout.shape == (2, 2, 2, 2, 3)
    yref = decay_get_Cref(list(k), np.array([1., 0, 0]), np.array(t.flat))
    assert np.allclose(yout, yref.reshape(yout.shape))


def test_bateman_full_arr():
    k0, k1, k2 = 2.0, 3.0, 4.0
    k = [k0, k1, k2]
    y0 = [0.7, 0.3, 0.5]
    t = np.linspace(0, 10, 10)
    yout = bateman_full_arr(np.asarray(y0), np.asarray(k), t.reshape((2, 5)))
    yref = decay_get_Cref(k, y0, t)
    assert np.allclose(yout, yref.reshape((2, 5, 3)))


def _yi1(i, p, a, binom):
    return binom(p+i-1, p) * a**(-1-p) * ((a-1)/a)**(i-1)


@pytest.mark.parametrize('p', (0, 1, 2, 3, 4, 5))
def test_bateman_parent(p):
    from scipy.special import binom
    from math import log
    N = 32
    a = 27
    lmbd = [(i+p+1)*log(a) for i in range(N)]
    bp = bateman_parent(lmbd, 1)
    for i, v in enumerate(bp, 1):
        assert abs(v - _yi1(i, p, a, binom)) < 1e-14
