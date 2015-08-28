#include <cassert>
#include <limits>
#include <vector>

#include "bateman.hpp"

#if defined(MULTIPRECISION_DIGITS10)
#include <boost/multiprecision/cpp_dec_float.hpp>
using Real_t = boost::multiprecision::number<
    boost::multiprecision::cpp_dec_float<MULTIPRECISION_DIGITS10> >;
#ifndef CHAIN_LENGTH
// cpp_dec_float is more precise than double even with ~16 digits.
#define CHAIN_LENGTH 200
#endif
Real_t abs_cb(Real_t arg){
    return boost::multiprecision::abs(arg);
}
Real_t exp_cb(Real_t arg){
    return boost::multiprecision::exp(arg);
}
Real_t log_cb(Real_t arg){
    return boost::multiprecision::log(arg);
}
Real_t pow_cb(Real_t arg, Real_t ex){
    return boost::multiprecision::pow(arg, ex);
}
#else
#include <cmath>
using Real_t = double;
#ifndef CHAIN_LENGTH
// IEEE754 seem to handle up to 130 decays
#define CHAIN_LENGTH 130
#endif
Real_t abs_cb(Real_t arg){
    return std::abs(arg);
}
Real_t exp_cb(Real_t arg){
    return std::exp(arg);
}
Real_t log_cb(Real_t arg){
    return std::log(arg);
}
Real_t pow_cb(Real_t arg, Real_t ex){
    return std::pow(arg, ex);
}
#endif

int main(int argc, char *argv[]){
    std::vector<Real_t> y0 {{ 1.0, 1.0, 1.0 }};
    std::vector<Real_t> lmbd {{ 2.0, 3.0, 4.0 }};
    Real_t t = 1.0;
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

    const int N = CHAIN_LENGTH;
    const Real_t NN = static_cast<Real_t>(CHAIN_LENGTH);
    Real_t logN = log_cb(N);
    auto lmbd2 = std::vector<Real_t>(N);
    std::vector<Real_t> p2ref(N);
    for (int i=0; i<N; ++i){
        lmbd2[i] = (i+1)*logN;
        //p2ref[i] = pow_cb(N-1, i)/pow(N, i+1);
        p2ref[i] = pow_cb((NN-1)/NN, i)/NN;
    }
    auto p2 = bateman::bateman_parent(lmbd2, static_cast<Real_t>(1), exp_cb);
    Real_t atol = std::numeric_limits<Real_t>::epsilon()*10;
    for (int i=0; i<N; ++i)
        assert (abs_cb(p2[i] - p2ref[i]) < atol);
    return 0;
}
