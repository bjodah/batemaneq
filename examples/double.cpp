#include <cmath>
#include <iostream>
#include <iomanip>
#include <vector>
#include "bateman.hpp"

using vec_t = std::vector<double>;
double exp_cb(double arg){
    return std::exp(arg);
}

int main(){
   double one = 1;
   double d = one/365;
   double h = d/24;
   double ln2 = std::log(2);
   vec_t lmbd {{ ln2/1.405e10, ln2/5.75, ln2/(6.25*h),
       ln2/1.9116, ln2/(3.6319*d), ln2/(10.64*h), ln2/(60.55/60*h) }};
   auto p = bateman::bateman_parent(lmbd, 100.0, exp_cb);
   std::cout << std::setprecision(17);  // all significant digits
   for (auto v : p)
       std::cout << v << " ";
   std::cout << std::endl;
   return 0;
}
