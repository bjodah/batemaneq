#include "bateman.hpp"
#include <vector>
#include <cassert>

#if defined(MULTIPRECISION_DIGITS10)
#include <boost/multiprecision/cpp_dec_float.hpp>
using Real_t = boost::multiprecision::number<
    boost::multiprecision::cpp_dec_float<MULTIPRECISION_DIGITS10> >;
Real_t abs_cb(Real_t arg){
    return boost::multiprecision::abs(arg);
}
Real_t exp_cb(Real_t arg){
    return boost::multiprecision::exp(arg);
}
#else
#include <cmath>
using Real_t = double;
Real_t abs_cb(Real_t arg){
    return std::abs(arg);
}
Real_t exp_cb(Real_t arg){
    return std::exp(arg);
}
#endif

int main(int argc, char *argv[]){
    std::vector<Real_t> y0 {{ 1.0, 1.0, 1.0 }};
    std::vector<Real_t> lmbd {{ 2.0, 3.0, 4.0 }};
    Real_t t = 1.0;
    //    Real_t (*exp_ptr)(Real_t) = &(exp_cb);
    auto y = bateman::bateman_full(y0, lmbd, t, exp_cb);

    std::vector<Real_t> yref
    {{ 0.1353352832366127, 0.22088349810536145, 0.2749602834949804 }};

    assert (abs_cb(y[0] - yref[0]) < 1e-16);
    assert (abs_cb(y[1] - yref[1]) < 1e-16);
    assert (abs_cb(y[2] - yref[2]) < 1e-16);

    auto p = bateman::bateman_parent(lmbd, t, exp_cb);
    std::vector<Real_t> pref
    {{ 0.1353352832366127, 0.1710964297374975, 0.16223035616885698 }};

    assert (abs_cb(p[0] - pref[0]) < 1e-16);
    assert (abs_cb(p[1] - pref[1]) < 1e-16);
    assert (abs_cb(p[2] - pref[2]) < 1e-16);


    return 0;
}
