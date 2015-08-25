#ifndef _BATEMAN_H_AWQNYTMWHFHS3GMQNUCC7ROM5E
#define _BATEMAN_H_AWQNYTMWHFHS3GMQNUCC7ROM5E


namespace bateman{
    template<typename T, template<typename, typename...> class C, typename... Args>
    C<T, Args...> bateman_parent(const C<T, Args...>& lmbd, const T& t,
                                 T (*exp)(T), int offset=0) {
        auto n = lmbd.size();
        C<T, Args...> N(n);
        T lmbd_prod = 1;
        for(unsigned int i=0; i<n; ++i){
            if (i > 0)
                lmbd_prod *= lmbd[offset+i-1];
            T sum_k = 0;
            for (unsigned int k=0; k<=i; ++k){
                T prod_l = 1;
                for (unsigned int l=0; l<=i; ++l){
                    if (l == k)
                        continue;
                    prod_l *= lmbd[offset+l] - lmbd[offset+k];
                }
                sum_k += exp(-lmbd[offset+k]*t)/prod_l;
            }
            N[i] = lmbd_prod*sum_k;
        }
        return N;
    }

    template<typename T, template<typename, typename...> class C, typename... Args>
    C<T, Args...> bateman_full(const C<T, Args...>& y0s, const C<T, Args...>& lmbd,
                               const T& t, T (*exp)(T)) {
        auto n = lmbd.size();
        C<T, Args...> N(n);
        for (unsigned int i=0; i<n; ++i)
            N[i] = 0;
        for (unsigned int i=0; i<n; ++i){
            auto y0 = y0s[i];
            if (y0 == 0)
                continue;
            auto Ni = bateman_parent<T,C>(lmbd, t, exp, i);
            for (unsigned int j=0; j<n; ++j)
                N[j+i] += y0*Ni[j];
        }
        return N;
    }
}
#endif /* _BATEMAN_H_AWQNYTMWHFHS3GMQNUCC7ROM5E */
