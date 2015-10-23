#include <cmath>
#include <iostream>
#include <vector>
#include <boost/multiprecision/cpp_dec_float.hpp>
#include "bateman.hpp"

using Real_t = boost::multiprecision::cpp_dec_float_50;
using vec_t = std::vector<Real_t>;
Real_t exp_cb(Real_t arg){
    return boost::multiprecision::exp(arg);
}

int main(){
   Real_t one = 1;
   Real_t d = one/365;
   Real_t h = d/24;
   Real_t ln2 = boost::multiprecision::log(2*one);
   vec_t lmbd {{ ln2/1.405e10, ln2/5.75, ln2/(6.25*h),
       ln2/1.9116, ln2/(3.6319*d), ln2/(10.64*h), ln2/(60.55/60*h) }};
   auto p = bateman::bateman_parent(lmbd, static_cast<Real_t>(100), exp_cb);
   std::cout << std::setprecision(30);  // show 30 of our 50 digits
   for (auto v : p)
       std::cout << v << " ";
   std::cout << std::endl;
   return 0;
}
