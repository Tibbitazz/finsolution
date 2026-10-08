"""S4.7 PC-B4 resampled efficient frontier: Michaud & Michaud (2008), Efficient Asset Management, 2nd ed., OUP.
SPECIFICATION VERIFICATION ONLY (decision D-2: the IP check precedes implementation; the book states RE optimisation and
the Forecast Confidence level are patented / patent pending, pp. 42 fn. 1 and 52 fn. 30). Not production code.
Inputs: Tables 2.3-2.4 (eight asset classes, monthly return premiums Jan 1978-Dec 1995, %), p. 16.
  Table 5.1 (p. 36): linear-constrained MV max Sharpe (SR 0.216 monthly) and min variance; unbounded max SR 0.253 (p. 36)
  Procedure (pp. 37-39, 42-44 fn. 4): simulate 18 years of monthly returns; re-estimate; 51 long-only efficient portfolios
  equally spaced in return from min variance to max return; 500 replications; RE portfolio = average of rank-associated
  portfolios. Table 6.1 (p. 45): RE and MV min variance, middle and max return portfolios (whole percentages).
  fn. 7 (p. 44): the RE max-return weight of an asset = probability that it is the maximum-return asset."""
import numpy as np, warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
names = ['EuroBonds', 'USBonds', 'Canada', 'France', 'Germany', 'Japan', 'UK', 'US']
mu = np.array([0.27, 0.25, 0.39, 0.88, 0.53, 0.88, 0.79, 0.71])
sd = np.array([1.56, 2.01, 5.50, 7.03, 6.22, 7.04, 6.01, 4.30])
R = np.array([[1.00, .92, .33, .26, .28, .16, .29, .42], [.92, 1.00, .26, .22, .27, .14, .25, .36],
              [.33, .26, 1.00, .41, .30, .25, .58, .71], [.26, .22, .41, 1.00, .62, .42, .54, .44],
              [.28, .27, .30, .62, 1.00, .35, .48, .34], [.16, .14, .25, .42, .35, 1.00, .40, .22],
              [.29, .25, .58, .54, .48, .40, 1.00, .56], [.42, .36, .71, .44, .34, .22, .56, 1.00]])
S = np.outer(sd, sd) * R; n = 8; one = np.ones(n); B = [(0, 1)] * n
def qp(Sig, m, target=None, x0=None):
    cons = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}]
    if target is not None: cons.append({'type': 'eq', 'fun': lambda w: w @ m - target})
    return minimize(lambda w: w @ Sig @ w, one / n if x0 is None else x0, jac=lambda w: 2 * Sig @ w, method='SLSQP',
                    bounds=B, constraints=cons, options={'ftol': 1e-14, 'maxiter': 500}).x
def frontier(Sig, m, k=51):
    g = qp(Sig, m); lo, hi = g @ m, m.max(); W = [g]
    for tg in np.linspace(lo, hi, k)[1:-1]: W.append(qp(Sig, m, tg, W[-1]))
    top = np.zeros(n); top[np.argmax(m)] = 1; W.append(top); return np.array(W)
sr = lambda w: (w @ mu) / np.sqrt(w @ S @ w)

# classical MV, Table 5.1 and p. 36
gmv = qp(S, mu); assert abs(gmv[0] - 0.987) < 0.002 and abs(gmv[5] - 0.013) < 0.002 and gmv[[1, 2, 3, 4, 6, 7]].max() < 1e-3
cands = [minimize(lambda w: -sr(w), x0, method='SLSQP', bounds=B, constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}],
                  options={'ftol': 1e-14}).x for x0 in (one / n, gmv)]
msr = max(cands, key=sr)
tab51 = np.array([0.678, 0.0, 0.0, 0.026, 0.0, 0.097, 0.017, 0.182])                      # Euro, US bonds, CA, FR, DE, JP, UK, US
# inputs are printed rounded (2 decimals): the book's own Table 5.1 portfolio has SR 0.2180 on these inputs, as does ours;
# the printed 0.216 reflects unrounded inputs. Weights agree within 0.6 pp
assert np.abs(msr - tab51).max() < 0.006 and abs(sr(msr) - sr(tab51)) < 1e-4 and abs(sr(msr) - 0.216) < 0.003
assert abs(np.sqrt(mu @ np.linalg.solve(S, mu)) - 0.253) < 0.002  # unbounded: 0.2538; rounding alone moves it 0.245-0.264
F = frontier(S, mu)
tab61_mv_mid = np.array([.44, 0, 0, .05, 0, .15, .03, .32])
# Table 6.1 does not define "middle" exactly (MCH-1): the printed MV middle portfolio is efficient on our frontier at
# return ~0.552 (rank 24 of 51; the return midpoint would be rank 26). Use the matching rank for both MV and RE
r_mid = min(range(51), key=lambda r: np.abs(F[r] - tab61_mv_mid).max())
mv_dev = np.abs(F[r_mid] - tab61_mv_mid).max(); assert mv_dev < 0.011 and 22 <= r_mid <= 26
# MV max return: France and Japan tie at 0.88 in the rounded inputs; the book's MV max-return portfolio is 100% France

# RE: 500 replications of 216 simulated months, rank association
rng = np.random.default_rng(20261008); L = np.linalg.cholesky(S); T, K = 216, 500
Wsum = np.zeros((51, n)); top_count = np.zeros(n)
for k in range(K):
    X = mu + rng.standard_normal((T, n)) @ L.T; m_k = X.mean(0); S_k = np.cov(X, rowvar=False)
    Wsum += frontier(S_k, m_k); top_count[np.argmax(m_k)] += 1
RE = Wsum / K
assert np.allclose(RE.sum(1), 1, atol=1e-6) and (RE >= -1e-8).all()
assert np.allclose(RE[50], top_count / K)                                                  # fn. 7
tab61_re = {0: np.array([.98, 0, 0, 0, 0, .02, 0, 0]), r_mid: np.array([.37, .09, .01, .08, .03, .13, .07, .22]),
            50: np.array([0, 0, .01, .34, .04, .33, .16, .12])}
dev = {r: np.abs(RE[r] - v).max() for r, v in tab61_re.items()}
assert dev[0] < 0.02 and dev[r_mid] < 0.04 and dev[50] < 0.05, dev                            # Monte Carlo + rounding tolerance
# REF lies below the MV frontier in the original inputs' mean-variance space (p. 45; fn. 8 allows rare exceptions)
below = sum(np.sqrt(w @ S @ w) >= np.sqrt(F[np.argmin(np.abs(F @ mu - w @ mu))] @ S @ F[np.argmin(np.abs(F @ mu - w @ mu))]) - 1e-6 for w in RE)
assert below >= 49
# Forecast-confidence limits (p. 52): long simulated samples approach MV; short ones diversify the max-return portfolio
def re_top(Tn, K2=300):
    c = np.zeros(n)
    for k in range(K2): c[np.argmax((mu + rng.standard_normal((Tn, n)) @ L.T).mean(0))] += 1
    return c / K2
ent = lambda p: -(p[p > 0] * np.log(p[p > 0])).sum()
p_short, p_long = re_top(24), re_top(20000)
assert ent(p_short) > ent(p_long) and p_long[[3, 5]].sum() > 0.9                           # long T: mass on the France/Japan tie
print(f"PASS REF (specification check; D-2): Table 5.1 MV max Sharpe (SR {sr(msr):.3f}) and min variance, unbounded SR 0.253, "
      f"Table 6.1 MV middle efficient at rank {r_mid + 1} (dev {mv_dev:.3f}); RE min/middle/max vs Table 6.1 max deviation "
      f"{dev[0]:.3f}/{dev[r_mid]:.3f}/{dev[50]:.3f}; "
      f"fn. 7 identity; REF below MV ({below}/51); forecast-confidence limits")
