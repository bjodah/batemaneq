# -*- coding: utf-8 -*-
import numpy as np
from batemaneq import bateman_full

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
