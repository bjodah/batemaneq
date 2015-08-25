#include "bateman.hpp"
#include <vector>
#include <cassert>

#if defined(MULTIPRECISION_DIGITS10)
#include <boost/multiprecision/cpp_dec_float.hpp>
using Real_t = boost::multiprecision::number<boost::multiprecision::cpp_dec_float<MULTIPRECISION_DIGITS10> >;
#define abs_cb boost::multiprecision::abs
#define exp_cb boost::multiprecision::exp
#else
#include <cmath>
using Real_t = double;
#define abs_cb std::abs
#define exp_cb std::exp
#endif

int main(int argc, char *argv[]){
    std::vector<Real_t> y0 {{ 1.0, 0.0, 0.0 }};
    std::vector<Real_t> lmbd {{ 1.0, 2.0, 3.0 }};
    Real_t t = 1.0;
    Real_t (*exp_ptr)(Real_t) = &(exp_cb);
    auto y = bateman::bateman_full(y0, lmbd, t, exp_ptr);

    std::vector<Real_t> yref
    {{ 0.36787944117144233, 0.23254415793482963, 0.14699594306608088}};

    assert (abs_cb(y[0] - yref[0]) < 1e-14);
    assert (abs_cb(y[1] - yref[1]) < 1e-14);
    assert (abs_cb(y[2] - yref[2]) < 1e-14);
    return 0;
}
