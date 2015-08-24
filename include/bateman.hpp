#ifndef _BATEMAN_H_AWQNYTMWHFHS3GMQNUCC7ROM5E
#define _BATEMAN_H_AWQNYTMWHFHS3GMQNUCC7ROM5E


namespace bateman{
    template<typename T, class C>
    C<T> bateman_parent(const C<T>& lmbd, const T& t, (*T)(T) exp, int offset=0) {
        auto n = lmbd.size();
        C<T> N(n);
        T lmbd_prod = 1;
        for(int i=0; i<n; ++i){
            if (i > 0)
                lmbd_prod *= lmbd[offset+i-1];
            T sum_k = 0;
            for (int k=0; k<=i; ++k){
                T prod_l = 1;
                for (int l=0; l<=i; ++l){
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

    template<typename T, class C>
    C<T> bateman_full(const C<T>& y0s, const C<T>& lmbd, const T& t, (*T)(T) exp) {
        auto n = lmbd.size();
        C<T> N(n);
        for (int i=0; i<n; ++i)
            N[i] = 0;
        for (int i=0; i<n; ++i){
            auto y0 = y0s[i];
            if (y0 == 0)
                continue;
            auto Ni = bateman_parent<T,C>(lmbd, t, exp, i);
            for (int j=0; j<n; ++j)
                N[j+i] += y0*Ni[j];
        }
    }
}
#endif /* _BATEMAN_H_AWQNYTMWHFHS3GMQNUCC7ROM5E */
