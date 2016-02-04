# -*- coding: utf-8 -*-

from __future__ import division


def bateman_parent(lmbd, t, one=1, zero=0, exp=None):
    """ Calculate daughter concentrations (number densities) from single parent

    Assumes an initial parent concentraion of one (and zero for all daughters)

    Parameters
    ----------
    lmbd: array_like
        decay constants (one per species)
    t: float
        time
    one: object
        object corresponding to one, default(int(1)),
        could e.g. be :py:func:`sympy.S('1')`
    zero: object
        object corresponding to zero, default(int(0))
        could e.g. be :py:func:`sympy.S('0')`
    exp: callback
        Callback calculating the exponential of an argument
        default: numpy.exp or math.exp, could e.g. be :py:func:`sympy.exp`

    """
    n = len(lmbd)
    N = [None]*n
    lmbd_prod = one
    if exp is None:
        try:
            from numpy import exp
        except ImportError:
            from math import exp
    for i in range(n):
        if i > 0:
            lmbd_prod *= lmbd[i-1]
        sum_k = zero
        for k in range(i+1):
            prod_l = one
            for l in range(i+1):
                if l == k:
                    continue
                prod_l *= lmbd[l] - lmbd[k]
            sum_k += exp(-lmbd[k]*t)/prod_l
        N[i] = lmbd_prod*sum_k
    return N


def bateman_full(y0s, lmbd, t, one=1, zero=0, exp=None):
    """ Calculates a linear combination of single-parent chains

    Generalized helper function for when y0 != [1, 0, 0, ... ]

    Parameters
    ----------
    y0s: array_like
        Initial concentrations
    t: float
        time
    one: object
        object corresponding to one, default(int(1)),
        could e.g. be :py:func:`sympy.S('1')`
    zero: object
        object corresponding to zero, default(int(0))
        could e.g. be :py:func:`sympy.S('0')`
    exp: callback
        Callback calculating the exponential of an argument
        default: math.exp, could e.g. be :py:func:`sympy.exp`

    """
    n = len(lmbd)
    if len(y0s) != n:
        raise ValueError("Please pass equal number of decay"
                         " constants as initial concentrations"
                         " (you may want to pad lmbd with zeroes)")
    N = [zero]*n
    for i, y0 in enumerate(y0s):
        if y0 == zero:
            continue
        Ni = bateman_parent(lmbd[i:], t, one, zero, exp)
        for j, yj in enumerate(Ni, i):
            N[j] += y0*yj
    return N
