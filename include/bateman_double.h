#ifdef __cplusplus
extern "C" {
#endif

    void bateman_double_parent(const int n,
                               const double * const lmbd,
                               const double t,
                               double * const out);
    void bateman_double_full(const int n,
                             const double * const y,
                             const double * const lmbd,
                             const double t,
                             double * const out);

#ifdef __cplusplus
}
#endif
