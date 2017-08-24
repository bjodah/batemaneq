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
    cdef int skip = 0
    cdef double t
    cdef tuple tout_shape = tuple([tout.shape[i] for i in range(tout.ndim)])
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out = np.empty(tout.size*lmbd.size)
    for idx, t in np.ndenumerate(tout):
        bateman_double_parent(lmbd.size, &lmbd[0], t, &out[skip])
        skip += lmbd.size
    return out.reshape(tout_shape + (lmbd.size,))


def bateman_full(cnp.ndarray[cnp.float64_t, ndim=1] y,
                 cnp.ndarray[cnp.float64_t, ndim=1] lmbd, tout):
    if y.size != lmbd.size:
        raise ValueError("y and lmbd of mismatching length")
    cdef int i, skip=0
    cdef double t
    cdef tuple tout_shape = tuple([tout.shape[i] for i in range(tout.ndim)])
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out = np.empty(tout.size*lmbd.size)

    for idx, t in np.ndenumerate(tout):
        print(skip, out.size)
        bateman_double_full(y.size, &y[0], &lmbd[0], t, &out[skip])
        skip += lmbd.size
    return out.reshape(tout_shape + (y.size,))
