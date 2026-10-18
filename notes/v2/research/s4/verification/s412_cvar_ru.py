"""S4.12a source reproduction and derivations for PC-D1 (CVaR): Rockafellar & Uryasev, "Optimization of Conditional
Value-at-Risk" (preprint of 5 Sep 1999; published J. Risk 2(3), 2000). Tables 3-6, eqs. (17)-(19), the Proposition,
the discrete-scenario case (RU-2), the Table 5 sign check (RU-3), and the scenario-location dependence of min-CVaR (NT-1)."""
import numpy as np, warnings
from scipy.optimize import linprog, minimize
from scipy.special import erfinv
from scipy.stats import norm, qmc
warnings.filterwarnings('ignore')

mu = np.array([0.0101110, 0.0043532, 0.0137058])                                   # Table 1
S = np.array([[0.00324625, 0.00022983, 0.00420395],
              [0.00022983, 0.00049937, 0.00019247],
              [0.00420395, 0.00019247, 0.00764097]])                               # Table 2
R = 0.011                                                                            # constraint (15): mu'x >= R
n = 3; cons_sum = {'type': 'eq', 'fun': lambda x: x.sum() - 1}

# --- Table 3: minimum-variance portfolio with mu'x >= R, x >= 0, sum x = 1 -------------------------------------
mv = minimize(lambda x: x @ S @ x, np.ones(n) / n, method='SLSQP', bounds=[(0, 1)] * n,
              constraints=[cons_sum, {'type': 'ineq', 'fun': lambda x: mu @ x - R}], options={'ftol': 1e-16, 'maxiter': 500}).x
assert np.allclose(mv, [0.452013, 0.115573, 0.432414], atol=2e-6) and abs(mv @ S @ mv - 0.00378529) < 1e-8
sig = np.sqrt(mv @ S @ mv)

# --- eqs. (18)-(19) and Table 4; RU-1: the printed exp(erf^-1(2b-1))^2 means exp([erf^-1(2b-1)]^2) -------------------
c1 = lambda b: np.sqrt(2) * erfinv(2 * b - 1)
c2 = lambda b: 1 / (np.sqrt(2 * np.pi) * np.exp(erfinv(2 * b - 1) ** 2) * (1 - b))
c2_alt = lambda b: 1 / (np.sqrt(2 * np.pi) * np.exp(erfinv(2 * b - 1)) ** 2 * (1 - b))      # the other reading
T4 = {0.90: (0.067847, 0.096975), 0.95: (0.090200, 0.115908), 0.99: (0.132128, 0.152977)}
for b, (var_p, cvar_p) in T4.items():
    assert abs(c1(b) - norm.ppf(b)) < 1e-12 and abs(c2(b) - norm.pdf(norm.ppf(b)) / (1 - b)) < 1e-12
    assert abs(-R + c1(b) * sig - var_p) < 1e-6 and abs(-R + c2(b) * sig - cvar_p) < 1e-6
    assert abs(-R + c2_alt(b) * sig - cvar_p) > 1e-2                                 # the other reading fails Table 4

# --- LP (17): min alpha + 1/(q(1-b)) sum u_k, u_k >= -x'y_k - alpha, u >= 0, x >= 0, sum x = 1, mu'x >= R ---------
def min_cvar(Y, b, ret=None, mvec=None):
    q, m = Y.shape; c = np.r_[np.zeros(m), 1.0, np.full(q, 1 / (q * (1 - b)))]
    A = np.c_[-Y, -np.ones(q), -np.eye(q)]; bu = np.zeros(q)                         # loss f = -x'y
    if ret is not None:
        A = np.r_[A, np.r_[-mvec, 0, np.zeros(q)][None]]; bu = np.r_[bu, -ret]
    res = linprog(c, A_ub=A, b_ub=bu, A_eq=np.r_[np.ones(m), 0, np.zeros(q)][None], b_eq=[1],
                  bounds=[(0, None)] * m + [(None, None)] + [(0, None)] * q, method='highs')
    return res.x[:m], res.x[m], res.fun                                             # x, alpha (a VaR), CVaR
L = np.linalg.cholesky(S)

# Tables 5-6 within sampling error. Pseudo-random (Table 5): average over seeds; quasi-random (Table 6): Sobol.
for b, (var_p, cvar_p) in T4.items():
    if b == 0.99: continue                                                             # 1% tails need far larger q
    cv = [min_cvar(mu + np.random.default_rng(s).standard_normal((10000, n)) @ L.T, b, R, mu)[2] for s in range(6)]
    assert abs(np.mean(cv) / cvar_p - 1) < 0.01                                        # mean of 6 MC runs within 1%
    z = norm.ppf(qmc.Sobol(n, scramble=True, seed=20261018).random(2 ** 14)); x, a, cvs = min_cvar(mu + z @ L.T, b, R, mu)
    assert abs(cvs / cvar_p - 1) < 0.01 and np.abs(x - mv).max() < 0.03              # Sobol 16384: within 1%, weights near Table 3
z = norm.ppf(qmc.Sobol(n, scramble=True, seed=20261018).random(2 ** 16)); x, a, cvs = min_cvar(mu + z @ L.T, 0.99, R, mu)
assert abs(cvs / T4[0.99][1] - 1) < 0.015                                              # 99%: Sobol 65536 within 1.5%

# RU-3: Table 5 "VaR Dif(%)" vs the printed VaR column. Printed rows (beta, VaR, Dif%):
t5 = [(.90, .06795, .154), (.90, .06537, 3.645), (.90, .06662, 1.809), (.90, .06622, 2.398), (.90, .06629, -2.299),
      (.95, .09224, 2.259), (.95, .09428, 4.524), (.95, .09175, 1.715), (.95, .08927, -1.03), (.95, .09136, 1.284),
      (.99, .13454, 1.829), (.99, .12791, -3.187), (.99, .13176, -0.278), (.99, .12881, -2.51), (.99, .13153, -0.451)]
recomputed = [(v / T4[b][0] - 1) * 100 for b, v, _ in t5]
sign_bad = [i for i, ((b, v, d), r) in enumerate(zip(t5, recomputed)) if np.sign(d) != np.sign(r)]
mag_ok = all(abs(abs(d) - abs(r)) < 0.06 for (b, v, d), r in zip(t5, recomputed))
assert sign_bad == [1, 2, 3] and mag_ok                                                # magnitudes right; three signs flipped

# --- RU-2: discrete scenarios. The 2000 paper assumes a continuous distribution (eq. 27); with q equally likely
# scenarios the LP still equals CVaR as the quantile integral (1/(1-b)) int_b^1 VaR_u du, including b*q non-integer and ties.
def cvar_quantile_integral(loss, b):
    s = np.sort(loss); q = len(s); tot = 0.0
    for k in range(q):                                                                  # VaR_u = s[k] on u in (k/q, (k+1)/q]
        lo, hi = max(k / q, b), (k + 1) / q
        if hi > lo: tot += s[k] * (hi - lo)
    return tot / (1 - b)
rng = np.random.default_rng(7); Yd = np.round(rng.standard_t(4, (397, 3)) * 0.04 + mu, 3)    # rounded: ties present
xd = np.array([.5, .2, .3]); loss = -Yd @ xd
for b in (0.9, 0.95, 0.951, 0.99):
    q = len(loss); c = np.r_[1.0, np.full(q, 1 / (q * (1 - b)))]
    lp = linprog(c, A_ub=np.c_[-np.ones(q), -np.eye(q)], b_ub=-loss, bounds=[(None, None)] + [(0, None)] * q, method='highs')
    assert abs(lp.fun - cvar_quantile_integral(loss, b)) < 1e-12
    tail_mean = loss[loss >= np.sort(loss)[int(np.ceil(b * q)) - 1]].mean()            # naive "mean beyond VaR"
    if b == 0.951: assert abs(tail_mean - lp.fun) > 1e-4                                # differs when b*q is not an integer

# --- NT-1: min-CVaR is not location-free. Normal losses: CVaR_b(x) = -mu'x + c2(b)*sigma(x). With no return
# constraint the minimiser is GMV only when the scenario mean is zero; the gap grows with horizon (mu ~ h, sigma ~ sqrt(h)).
b = 0.95
def gmv_and_mincvar(m, V):
    g = minimize(lambda x: x @ V @ x, np.ones(n) / n, method='SLSQP', bounds=[(0, 1)] * n, constraints=[cons_sum],
                 options={'ftol': 1e-16}).x
    c = minimize(lambda x: -m @ x + c2(b) * np.sqrt(x @ V @ x), np.ones(n) / n, method='SLSQP', bounds=[(0, 1)] * n,
                 constraints=[cons_sum], options={'ftol': 1e-16}).x
    return g, c
gaps = [np.abs(np.subtract(*gmv_and_mincvar(mu * h, S * h))).max() for h in (1, 3, 12, 36, 60)]
assert gaps[0] > 0.01 and all(np.diff(gaps) > 0) and gaps[2] > 0.05                     # 1.9 pp monthly, 6.2 pp annual, 14 pp 5y
mu12, S12 = mu * 12, S * 12; gmv, mc = gmv_and_mincvar(mu12, S12); L12 = np.linalg.cholesky(S12)
z = norm.ppf(qmc.Sobol(n, scramble=True, seed=1).random(2 ** 15)); Z = z - z.mean(0)
x0, _, _ = min_cvar(Z @ L12.T, b)                                                       # demeaned scenarios, no return constraint
assert np.abs(x0 - gmv).max() < 0.02                                                    # -> GMV
xm, _, _ = min_cvar(mu12 + Z @ L12.T, b); assert np.abs(xm - mc).max() < 0.02           # centred on mu -> the mean-CVaR point
alt = mu12[::-1].copy(); xa, _, _ = min_cvar(alt + Z @ L12.T, b)                         # same dispersion, different centre
assert np.abs(xa - xm).max() > 0.05                                                     # weights move with the scenario location
# Grinold (Advances ch. 32, eq. 10) recentring r = rF + mu*dt + sigma*z*sqrt(dt), sum pi z = 0, sum pi z^2 = 1:
hist = mu + rng.standard_t(5, (600, n)) @ L.T * np.sqrt(3 / 5)
zs = (hist - hist.mean(0)) / hist.std(0); sd = np.sqrt(np.diag(S))
target_mu = np.array([0.006, 0.003, 0.008]); rec = target_mu + zs * sd
assert np.allclose(rec.mean(0), target_mu) and np.allclose(rec.std(0), sd)              # location/scale injected exactly
assert np.allclose(np.corrcoef(rec.T), np.corrcoef(hist.T))                              # dependence kept from history

print("PASS Rockafellar-Uryasev: Table 3 exact; eqs. (18)-(19) and Table 4 to 1e-6 (RU-1 reading confirmed); "
      "Tables 5-6 within sampling error; RU-3 three sign errors in Table 5 VaR Dif; RU-2 LP = quantile integral on "
      f"discrete scenarios; NT-1 min-CVaR depends on scenario location (annual: GMV {gmv.round(3)} vs centred-on-mu "
      f"{mc.round(3)}; max gap by horizon 1/3/12/36/60 m: {np.round(gaps, 3)})")
