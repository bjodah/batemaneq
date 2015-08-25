# -*- coding: utf-8 -*-
# distutils: language = c++
# distutils: extra_compile_args = -std=c++11

cimport numpy as cnp
import numpy as np

cdef extern from "bateman_double.h":
    void bateman_double_parent(const int n,
                               const double * const lmbd,
                               const double t,
                               double * const out)
    void bateman_double_full(const int n,
                             const double * const y,
                             const double * const lmbd,
                             const double t,
                             double * const out)


def bateman_parent(cnp.ndarray[cnp.float64_t, ndim=1] lmbd, tout):
    cdef int i, nt
    cdef double t
    if not hasattr(tout, '__len__'):
        tout = [tout]
        nt = 1
    else:
        nt = len(tout)
    cdef cnp.ndarray[cnp.float64_t, ndim=2] out = np.empty((nt, lmbd.size))
    for i in range(nt):
        bateman_double_parent(lmbd.size, &lmbd[0], tout[i], &out[i, 0])

    if nt == 1:
        return out.reshape(lmbd.size)
    else:
        return out


def bateman_full(cnp.ndarray[cnp.float64_t, ndim=1] y,
                 cnp.ndarray[cnp.float64_t, ndim=1] lmbd,
                 tout):
    if y.size != lmbd.size:
        raise ValueError("y and lmbd of mismatching length")
    cdef int i, nt
    cdef double t
    if not hasattr(tout, '__len__'):
        tout = [tout]
        nt = 1
    else:
        nt = len(tout)
    cdef cnp.ndarray[cnp.float64_t, ndim=2] out = np.empty((nt, y.size))
    for i in range(nt):
        bateman_double_full(y.size, &y[0], &lmbd[0], tout[i], &out[i, 0])

    if nt == 1:
        return out.reshape(y.size)
    else:
        return out
