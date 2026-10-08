"""S4.5 PC-A5 volatility targeting (EQ-H-4): Moreira & Muir (2017), JF 72(4):1611-1644, on synthetic data.
  eq. (1), p. 1616: f_sigma_{t+1} = (c / sigma_hat_t^2) f_{t+1}; c set over the full sample so sd(f_sigma) = sd(f) (ex post)
  eq. (2), p. 1616: sigma_hat_t^2 = RV_t^2 from 22 daily returns. As printed, the sum runs over days t+1/22 ... t+1 (the month
          being scaled); the text says "previous month's". We implement the strictly-past reading and test it (MM-1)
  fn. 6: c does not change the Sharpe ratio; eq. (3), p. 1617 and p. 1620: SR_new = sqrt(SR_old^2 + (alpha/sigma_eps)^2)
  p. 1620: momentum example sqrt(12) * 12.5 / RMSE = 0.875 implies RMSE ~ 49.5 ("around 50")
  Table IV (p. 1625) / Table V (p. 1626) variants: 1/RV^2, 1/RV, min(c/RV^2, 1), min(c/RV^2, 1.5)
Plus the distinctions behind decision S45-D1: inverse-variance scaling is not volatility targeting; the engine form
w_t = min(sigma*/sigma_hat_t, L) with cash residual 1 - w_t."""
import numpy as np, warnings
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008)
T, D = 720, 22                                                                             # months, trading days per month
lv = np.empty(T); lv[0] = np.log(0.045 ** 2)                                               # log monthly variance, AR(1)
for t in range(1, T): lv[t] = np.log(0.045 ** 2) + 0.8 * (lv[t - 1] - np.log(0.045 ** 2)) + 0.45 * rng.normal()
sig = np.exp(lv / 2); mu_m = 0.006                                                        # constant mean: vol does not predict returns
daily = mu_m / D + (sig / np.sqrt(D))[:, None] * rng.standard_t(6, size=(T, D)) / np.sqrt(1.5)
f = daily.sum(1)                                                                           # monthly excess return

def rv2(daily):                                                                            # eq. (2) applied to one month's days
    return ((daily - daily.sum(-1, keepdims=True) / D) ** 2).sum(-1)
def managed(daily, kind='1/RV2', cap=None):                                                # weights for months 1..T-1, info to t
    r = rv2(daily)[:-1]; w = {'1/RV2': 1 / r, '1/RV': 1 / np.sqrt(r)}[kind]
    if cap is not None: w = np.minimum(w / np.median(w), cap)  # MM's capped variants keep the baseline c (Table V: P50 0.93 in
    return w                                                   # all three rows); median-1 scaling here is an illustration
w = managed(daily); fs_raw = w * f[1:]; c = f[1:].std() / fs_raw.std(); fs = c * fs_raw    # eq. (1), c ex post
assert np.isclose(fs.std(), f[1:].std())
sr = lambda x: x.mean() / x.std()
assert all(np.isclose(sr(k * fs), sr(fs)) for k in (0.3, 1, 7))                           # fn. 6: c does not change Sharpe

# MM-1: our weight for month t+1 uses only days of months <= t; perturbing month t+1 leaves it unchanged
d2 = daily.copy(); d2[400] = rng.normal(0, 0.05, D); assert np.isclose(managed(d2)[399], w[399]) and not np.isclose(managed(d2)[400], w[400])
literal = lambda dd: 1 / rv2(dd)[1:]                                                       # eq. (2) as printed: same-month RV
assert not np.isclose(literal(d2)[399], literal(daily)[399])                               # look-ahead: month 400's weight moves with month 400

# eq. (3) and the appraisal-ratio identity (exact in sample with consistent ddof = 0 moments)
x, y = f[1:], fs; b = np.cov(x, y, ddof=0)[0, 1] / x.var(); a = y.mean() - b * x.mean(); e = y - a - b * x
mu2 = np.array([x.mean(), y.mean()]); S2 = np.cov(np.vstack([x, y]), ddof=0)
sr_new = np.sqrt(mu2 @ np.linalg.solve(S2, mu2)); assert np.isclose(sr_new, np.sqrt(sr(x) ** 2 + (a / e.std()) ** 2))
dU = (sr_new ** 2 - sr(x) ** 2) / sr(x) ** 2                                               # eq. (4)
assert abs(np.sqrt(12) * 12.5 / 0.875 - 50) / 50 < 0.02                                    # p. 1620 example: RMSE ~ 49.5

# Table IV variants are well defined; inverse variance has the heavier leverage tail (cf. Table V)
w_iv, w_v = managed(daily, '1/RV2'), managed(daily, '1/RV')
tail = lambda w: np.percentile(w / np.median(w), 99)
assert tail(w_iv) > tail(w_v) > 1
for cap in (1.0, 1.5): assert managed(daily, cap=cap).max() <= cap + 1e-12

# oracle volatility, long sample: 1/sigma is volatility targeting, 1/sigma^2 is not; Sharpe ordering under constant mean
n = 400_000; lv = np.empty(n); lv[0] = np.log(0.045 ** 2)
z = rng.normal(size=n)
for t in range(1, n): lv[t] = np.log(0.045 ** 2) + 0.8 * (lv[t - 1] - np.log(0.045 ** 2)) + 0.45 * z[t]
s = np.exp(lv / 2); g = mu_m + s * rng.normal(size=n); tgt = 0.04
vt_ret, iv_ret = (tgt / s) * g, (tgt * 0.045 / s ** 2) * g
hi, lo = s > np.quantile(s, 2 / 3), s < np.quantile(s, 1 / 3)
assert abs(vt_ret[hi].std() / vt_ret[lo].std() - 1) < 0.03                                # constant risk in every regime
assert iv_ret[hi].std() / iv_ret[lo].std() < 0.6                                           # inverse variance: risk falls in turbulence
assert sr(iv_ret) > sr(vt_ret) > sr(g)                                                     # w ~ 1/(sigma^2 + mu^2) is Sharpe-optimal here
# engine form (decision S45-D1, option 1): w = min(sigma*/sigma_t, L), cash = 1 - w
L = 1.0; wr = np.minimum(tgt / s, L); cash = 1 - wr; port = wr * g
assert (wr >= 0).all() and (wr <= L).all() and (cash >= 0).all() and np.allclose(wr + cash, 1)
free = tgt / s < L; assert abs(port[free].std() / tgt - 1) < 0.02 and (port[~free].std() < tgt)
print(f"PASS MM: eq. (1) with ex-post c; fn. 6; strictly-past RV (printed eq. (2) is look-ahead, MM-1); appraisal identity "
      f"(SR {sr(x) * np.sqrt(12):.2f} -> {sr_new * np.sqrt(12):.2f} ann., dU {dU:.0%}); Table IV variants; 1/sigma targets risk, "
      f"1/sigma^2 does not; capped engine form keeps cash >= 0 (cap binds in {(~free).mean():.0%} of months)")
