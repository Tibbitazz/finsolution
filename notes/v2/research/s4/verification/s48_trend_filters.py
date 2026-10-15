"""S4.8 trend-filter family (S4_PLAN amendment 19): Bruder, Dao, Richard & Roncalli (2011), "Trend Filtering Methods for
Momentum Strategies", Lyxor (BRU); Paleologo (2025) ch. 2 pp. 37-39 (drift precision). SPECIFICATION VERIFICATION ONLY;
synthetic data; prints PASS. Shows that TSMOM, moving-average crossovers and the Kalman (local-level) filter are linear
causal filters of returns; that HP and L1 smoothers are two-sided (look-ahead unless re-estimated on expanding windows);
records BRU-1 and BRU-2."""
import numpy as np, warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS

rng = np.random.default_rng(20261015)
Rl = rng.normal(0.0004, 0.012, 3000)                 # daily log returns
y = np.cumsum(Rl)                                     # log price

# 1. BRU sec. 2.2.3: the uniform moving average of returns gives mu_hat = (1/n) * cumulative log return, so its sign is
#    the TSMOM sign (MOP eq. 5) exactly, also with simple returns (sign(prod(1+r) - 1) = sign(sum log(1+r))).
for n in (21, 63, 252):
    for t in range(n, 3000, 97):
        mu_hat = Rl[t - n:t].mean()
        assert np.sign(mu_hat) == np.sign(np.prod(np.exp(Rl[t - n:t])) - 1)

# 2. BRU eq. (4): moving-average crossover mu_hat = 2/(n1 - n2) * (ybar_n2 - ybar_n1), n1 > n2, is a weighted sum of past
#    returns with weights a_i = (n1-1-i)/n1 1{i <= n1-2} - (n2-1-i)/n2 1{i <= n2-2}; largest weight at the short horizon;
#    with a constant drift m the difference of averages is exactly (n1 - n2)/2 * m. BRU-1: the text says "when the
#    short-term horizon n1 is one"; with n1 > n2 the short horizon is n2.
n1, n2 = 100, 20
def ybar(path, t, k): return path[t - k + 1:t + 1].mean()
a = np.array([((n1 - 1 - i) / n1 if i <= n1 - 2 else 0) - ((n2 - 1 - i) / n2 if i <= n2 - 2 else 0) for i in range(n1)])
for t in range(n1, 3000, 131):
    direct = ybar(y, t, n2) - ybar(y, t, n1)
    assert abs(direct - a[:n1 - 1] @ Rl[t - np.arange(n1 - 1)]) < 1e-12
assert np.argmax(a) in (n2 - 1, n2 - 2)
m = 0.001; yd = m * np.arange(500)
assert abs((ybar(yd, 400, n2) - ybar(yd, 400, n1)) - (n1 - n2) / 2 * m) < 1e-12

# 3. BRU eq. (6) and p. 11-12: returns R_t = mu_t + s_z z_t, mu_t = mu_{t-1} + s_e e_t. Stationary predicted variance
#    P* = s_e/2 (s_e + sqrt(s_e^2 + 4 s_z^2)); gain kappa = 2 s_e / (s_e + sqrt(s_e^2 + 4 s_z^2)) = Muth's gain
#    (-q + sqrt(q^2 + 4q))/2 with q = s_e^2/s_z^2 (Paleologo ex. 2.1); the filter is an EWMA of returns with
#    lambda = -ln(1 - kappa); half-life of e^(-lambda i) is ln 2 / lambda (14 days at lambda = 5%, as BRU state).
for s_e, s_z in ((0.0005, 0.012), (0.001, 0.01), (0.003, 0.012)):
    P = s_e ** 2
    for _ in range(200000):
        K = P / (P + s_z ** 2); P = P + s_e ** 2 - P * K
    P_bru = s_e / 2 * (s_e + np.sqrt(s_e ** 2 + 4 * s_z ** 2)); kap = 2 * s_e / (s_e + np.sqrt(s_e ** 2 + 4 * s_z ** 2))
    q = s_e ** 2 / s_z ** 2
    assert abs(P / P_bru - 1) < 1e-9 and abs(P / (P + s_z ** 2) - kap) < 1e-9 and abs(kap - (-q + np.sqrt(q * q + 4 * q)) / 2) < 1e-12
    lam = -np.log(1 - kap); mu_f, Pf = 0.0, 1.0
    ew = (1 - np.exp(-lam)) * np.exp(-lam * np.arange(3000))
    for t, rt in enumerate(Rl):
        Kt = Pf / (Pf + s_z ** 2); mu_f = (1 - Kt) * mu_f + Kt * rt; Pf = Pf + s_e ** 2 - Pf * Kt
    assert abs(mu_f - ew[:3000] @ Rl[::-1]) < 1e-6
assert int(np.ceil(np.log(2) / 0.05)) == 14 and int(np.ceil((1 / 0.05 - 0.5) * np.log(2))) == 14

# 4. Two-sided smoothers. HP / L2 filter (BRU p. 11): x = (I + 2 lam D'D)^{-1} y. L1 filter (BRU sec. 2.3.2):
#    min 1/2 ||y - x||^2 + lam ||D x||_1, solved through its box-constrained dual (Kim et al. 2009): x = y - D'nu,
#    |nu| <= lam. Both change past estimates when future data change; the end point of an expanding-window fit is the
#    only point-in-time (one-sided) estimate.
def D2(n):
    Dm = np.zeros((n - 2, n))
    for i in range(n - 2): Dm[i, i:i + 3] = [1, -2, 1]
    return Dm
def hp(yv, lam): Dm = D2(len(yv)); return np.linalg.solve(np.eye(len(yv)) + 2 * lam * Dm.T @ Dm, yv)
def l1(yv, lam):
    Dm = D2(len(yv)); Q = Dm @ Dm.T; c = Dm @ yv
    res = minimize(lambda v: 0.5 * v @ Q @ v - c @ v, np.zeros(len(yv) - 2), jac=lambda v: Q @ v - c,
                   method='L-BFGS-B', bounds=[(-lam, lam)] * (len(yv) - 2), options={'ftol': 1e-15, 'gtol': 1e-12, 'maxiter': 20000})
    return yv - Dm.T @ res.x
yy = y[:300].copy(); yy_future = yy.copy(); yy_future[250:] += 0.05
for filt, lam in ((hp, 1000.0), (l1, 0.05)):
    full, alt = filt(yy, lam), filt(yy_future, lam)
    assert np.abs(full[200:250] - alt[200:250]).max() > 1e-4               # smoothed past moves with future data
    one_sided = filt(yy[:240], lam)[-1]; one_sided_alt = filt(yy_future[:240], lam)[-1]
    assert one_sided == one_sided_alt and abs(one_sided - full[239]) > 1e-6  # end-point estimate is point-in-time
pw = np.concatenate([np.linspace(0, 1, 60), np.linspace(1, 0.4, 60)]) + rng.normal(0, 0.02, 120)
x1 = l1(pw, 0.5); dx = np.abs(D2(120) @ x1)
assert np.mean(dx < 1e-6) > 0.8                                            # L1: piecewise linear (sparse kinks)

# 5. Trend detection (BRU sec. 3.2.2): Mann statistic S = sum_{i<j} sgn(y_{t-i} - y_{t-j}) over n points; under no trend
#    Var(S) = n(n-1)(2n+5)/18. BRU-2: the bounds are +-n(n-1)/2 (number of pairs), not +-n(n+1)/2, so the normalised score
#    is 2S/(n(n-1)); BRU's 2S/(n(n+1)) cannot reach +-1.
def mann(v):
    n_ = len(v); return sum(np.sign(v[i] - v[j]) for i in range(n_ - 1) for j in range(i + 1, n_))
for n_ in (10, 30):
    sims = np.array([mann(rng.standard_normal(n_)) for _ in range(6000)])
    assert abs(sims.var() / (n_ * (n_ - 1) * (2 * n_ + 5) / 18) - 1) < 0.06
    assert abs(mann(np.arange(n_, 0, -1.0))) == n_ * (n_ - 1) / 2
    assert 2 * abs(mann(np.arange(n_, 0, -1.0))) / (n_ * (n_ + 1)) < 1

# 6. Paleologo pp. 38-39: for log price dp = a dt + s dW on [0, 1], the drift estimator sum_j r_j = p(1) - p(0) has variance
#    s^2 whatever the number of intervals n; the uncentred variance estimator has variance about 2 s^4 / n. Sampling more
#    often sharpens volatility, never the drift: any trend filter is limited by calendar span.
s, a_ = 0.2, 0.05
for n_ in (12, 252, 2520):
    r_ = a_ / n_ + s / np.sqrt(n_) * rng.standard_normal((20000, n_))
    assert abs(r_.sum(1).var() / s ** 2 - 1) < 0.04
    assert abs((r_ ** 2).sum(1).var() / (2 * s ** 4 / n_) - 1) < 0.08

print("PASS S4.8 trend filters: uniform MA of returns = TSMOM sign; MA crossover = triangular return weights, "
      "E = (n1-n2)/2*m (BRU-1 text slip); BRU Kalman gain = Muth gain = EWMA, half-life 14 d at 5%; HP and L1 are two-sided "
      "(end point of expanding fit is point-in-time); L1 piecewise linear; Mann variance n(n-1)(2n+5)/18, bound n(n-1)/2 "
      "(BRU-2); drift precision independent of sampling frequency (Paleologo pp. 38-39)")
