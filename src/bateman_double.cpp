#include <algorithm>
#include <cmath>
#include <vector>

#include "bateman_double.h"
#include "bateman.hpp"

using vec = std::vector<double>;

double exp_cb(double arg) { return std::exp(arg); }

#ifdef __cplusplus
extern "C" {
#endif

    void bateman_double_parent(const int n,
                               const double * const lmbd,
                               const double t,
                               double * const out){
        auto v = bateman::bateman_parent(vec(lmbd, lmbd+n), t, exp_cb);
        std::copy(v.begin(), v.end(), out);
    }
    void bateman_double_full(const int n,
                             const double * const y,
                             const double * const lmbd,
                             const double t,
                             double * const out){
        auto v = bateman::bateman_full(vec(y, y+n), vec(lmbd, lmbd+n), t, exp_cb);
        std::copy(v.begin(), v.end(), out);
    }

#ifdef __cplusplus
}
#endif
