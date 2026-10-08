"""S4.6 mean-variance foundation (EQ-MVO-1 ... EQ-MVO-4): closed forms against numerical solvers, on synthetic data.
Sources: Markowitz (1952) JF 7(1):77-91 (efficient set; long-only critical lines, p. 87); Tobin (1958) RES 25(2):65-86
(eqs. 3.22-3.25, pp. 83-84: dominant sets on a ray, composition independent of the cash share, linear opportunity locus);
Sharpe (1964) (capital market line); DeMiguel, Garlappi & Uppal (2009) eqs. (2)-(3); Jorion (1986) Table 1 constants;
DeMiguel, Garlappi, Nogales & Uppal (2009) Mgmt Sci 55(5) p. 802: eq. (3) Jagannathan-Ma shrinkage, Proposition 1.
Closed-form frontier algebra (A, B, C, D) is VERIFIED-DERIVATION: checked here against independent numerical solutions."""
import numpy as np, warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008)
def cov(n, kappa=None):
    A = rng.normal(size=(n, 3 * n)); S = A @ A.T / (3 * n)
    if kappa:                                                                              # impose a condition number
        e, V = np.linalg.eigh(S); e = np.geomspace(1, kappa, n)[::-1] * 0.002; S = V @ np.diag(e) @ V.T
    return S
def slsqp(f, x0, cons, bounds=None):
    return minimize(f, x0, method='SLSQP', constraints=cons, bounds=bounds, options={'ftol': 1e-15, 'maxiter': 2000}).x
def consts(S, mu):
    Si = np.linalg.inv(S); one = np.ones(len(mu)); A = one @ Si @ one; B = one @ Si @ mu; C = mu @ Si @ mu
    return Si, one, A, B, C, A * C - B ** 2

for t in range(40):
    n = int(rng.integers(3, 12)); S = cov(n); mu = rng.uniform(0.02, 0.12, n); Si, one, A, B, C, D = consts(S, mu)
    # EQ-MVO-4: GMV closed form = numerical minimum; variance 1/A
    g = Si @ one / A; gs = slsqp(lambda w: w @ S @ w, one / n, [{'type': 'eq', 'fun': lambda w: w.sum() - 1}])
    assert np.allclose(g, gs, atol=1e-6) and np.isclose(g @ S @ g, 1 / A)
    # EQ-MVO-2: frontier w(m) = [(C - B m) S^-1 1 + (A m - B) S^-1 mu] / D ; sigma^2(m) = (A m^2 - 2 B m + C) / D
    for m in np.linspace(mu.min(), mu.max(), 5):
        w = ((C - B * m) * Si @ one + (A * m - B) * Si @ mu) / D
        ws = slsqp(lambda w: w @ S @ w, one / n, [{'type': 'eq', 'fun': lambda w: w.sum() - 1},
                                                 {'type': 'eq', 'fun': lambda w, m=m: w @ mu - m}])
        assert np.allclose(w, ws, atol=1e-6) and np.isclose(w @ S @ w, (A * m * m - 2 * B * m + C) / D)
    # two-fund separation: any two frontier portfolios span the frontier
    wf = lambda m: ((C - B * m) * Si @ one + (A * m - B) * Si @ mu) / D
    m1, m2, m3 = np.sort(rng.uniform(mu.min(), mu.max(), 3)); a = (m3 - m2) / (m1 - m2)
    assert np.allclose(wf(m3), a * wf(m1) + (1 - a) * wf(m2))
    # EQ-MVO-1 utility form (budget only): q(gam) = g + (1/gam) P mu lies on the frontier at m = B/A + D/(A gam)
    P = Si - np.outer(Si @ one, Si @ one) / A
    for gam in (1, 3, 10):
        q = g + P @ mu / gam; assert np.allclose(q, wf(B / A + D / (A * gam)))
    # EQ-MVO-3: tangency with a riskless rate rf < m_g = B/A; max Sharpe = sqrt(mu_e' S^-1 mu_e) (Tobin 3.25)
    rf = B / A * rng.uniform(0.1, 0.8); me = mu - rf; tan = Si @ me / (one @ Si @ me)
    sr = lambda w: (w @ me) / np.sqrt(w @ S @ w)
    best = max((slsqp(lambda w: -sr(w), x0, [{'type': 'eq', 'fun': lambda w: w.sum() - 1}])
                for x0 in (one / n, g, rng.dirichlet(np.ones(n)))), key=sr)
    assert np.isclose(sr(tan), np.sqrt(me @ Si @ me)) and sr(best) <= sr(tan) + 1e-9 and np.allclose(best, tan, atol=1e-4)
    m_t = tan @ mu; assert np.isclose(tan @ S @ tan, (A * m_t ** 2 - 2 * B * m_t + C) / D)  # tangency is on the frontier
    for gam in (2, 5, 20):                                     # Tobin: risky composition independent of risk aversion
        x = Si @ me / gam; assert np.allclose(x / x.sum(), tan)
    rf_bad = B / A * 1.2; me_bad = mu - rf_bad                 # rf above the GMV mean: the formula lands on the lower branch
    tb = Si @ me_bad / (one @ Si @ me_bad); assert (one @ Si @ me_bad) < 0 and tb @ me_bad < 0  # negative excess return: must fail

# long-only maximum Sharpe: convex reformulation (min y'Sy s.t. mu_e'y = 1, y >= 0; w = y / 1'y) vs direct maximisation
for t in range(30):
    n = 8; S = cov(n); me = rng.uniform(-0.03, 0.08, n); one = np.ones(n)
    y = slsqp(lambda y: y @ S @ y, np.full(n, 1.0), [{'type': 'eq', 'fun': lambda y: y @ me - 1}], [(0, None)] * n)
    w_cvx = y / y.sum(); sr = lambda w: (w @ me) / np.sqrt(w @ S @ w)
    w_dir = max((slsqp(lambda w: -sr(w), x0, [{'type': 'eq', 'fun': lambda w: w.sum() - 1}], [(0, 1)] * n)
                 for x0 in [one / n] + [rng.dirichlet(np.ones(n)) for _ in range(4)]), key=sr)
    assert sr(w_cvx) >= sr(w_dir) - 1e-7 and np.allclose(w_cvx, w_dir, atol=2e-3)

# Markowitz (1952) p. 87: long-only efficient weights are piecewise linear in m (critical lines); variance piecewise quadratic
n = 6; S = cov(n); mu = np.linspace(0.03, 0.11, n); one = np.ones(n)
g_lo = slsqp(lambda w: w @ S @ w, one / n, [{'type': 'eq', 'fun': lambda w: w.sum() - 1}], [(0, 1)] * n)
ms = np.linspace(g_lo @ mu + 1e-4, mu.max() - 1e-4, 121); W = []
for m in ms:
    W.append(slsqp(lambda w: w @ S @ w, g_lo, [{'type': 'eq', 'fun': lambda w: w.sum() - 1},
                                              {'type': 'eq', 'fun': lambda w, m=m: w @ mu - m}], [(0, 1)] * n))
W = np.array(W); act = (W > 1e-7)
seg_ok = 0
for k in range(1, len(ms) - 1):
    if (act[k - 1] == act[k]).all() and (act[k] == act[k + 1]).all():
        assert np.allclose(W[k - 1] + W[k + 1], 2 * W[k], atol=1e-5); seg_ok += 1
corners = int((np.abs(np.diff(act.astype(int), axis=0)).sum(1) > 0).sum())
assert seg_ok > 100 and 1 <= corners <= 2 * n

# Jagannathan-Ma via KKT (DGNU eq. 3): long-only GMV w* = unconstrained GMV of S_JM = S - (lam 1' + 1 lam'), lam >= 0
for t in range(40):
    n = 10; S = cov(n); one = np.ones(n)
    w = slsqp(lambda w: w @ S @ w, one / n, [{'type': 'eq', 'fun': lambda w: w.sum() - 1}], [(0, 1)] * n)
    w[w < 1e-9] = 0; v = w @ S @ w; lam = S @ w - v * one                                  # KKT multipliers (objective w'Sw / 2 scale)
    assert lam.min() > -1e-6 and np.abs(lam * w).max() < 1e-6                              # dual feasibility, complementary slackness
    SJ = S - np.outer(lam, one) - np.outer(one, lam); assert np.allclose(SJ @ w, v * one, atol=1e-6)
    if np.linalg.eigvalsh(SJ).min() > 1e-10:
        gJ = np.linalg.solve(SJ, one); assert np.allclose(gJ / gJ.sum(), w, atol=1e-5)
    # DGNU Proposition 1: 1-norm <= 1 constrained GMV equals the long-only GMV (w = u - v, u, v >= 0)
    uv = slsqp(lambda z: (z[:n] - z[n:]) @ S @ (z[:n] - z[n:]), np.r_[one / n, np.zeros(n)],
               [{'type': 'eq', 'fun': lambda z: (z[:n] - z[n:]).sum() - 1}, {'type': 'ineq', 'fun': lambda z: 1 - z.sum()}],
               [(0, None)] * (2 * n))
    assert np.allclose(uv[:n] - uv[n:], w, atol=1e-4)

# condition-number sensitivity: ||dx||/||x|| <= kappa(S) ||dmu||/||mu|| for x = S^-1 mu, attained in the worst direction
for kappa in (10, 1e3, 1e5):
    n = 8; S = cov(n, kappa); e, V = np.linalg.eigh(S); k_hat = e[-1] / e[0]
    for t in range(200):
        m = rng.normal(size=n); dm = 1e-6 * rng.normal(size=n)
        x = np.linalg.solve(S, m); dx = np.linalg.solve(S, m + dm) - x
        assert np.linalg.norm(dx) / np.linalg.norm(x) <= k_hat * np.linalg.norm(dm) / np.linalg.norm(m) * (1 + 1e-6)
    m = V[:, -1]; dm = 1e-6 * V[:, 0]; x = np.linalg.solve(S, m); dx = np.linalg.solve(S, m + dm) - x
    assert np.isclose(np.linalg.norm(dx) / np.linalg.norm(x) / (np.linalg.norm(dm) / np.linalg.norm(m)), k_hat, rtol=1e-6)
# cash as a row of Sigma (decision S46-D1 option b): GMV collapses into cash and kappa explodes (illustrative vols, not data)
vols = np.array([0.16, 0.18, 0.06, 0.07, 0.15]); R = np.full((5, 5), 0.3); np.fill_diagonal(R, 1)
Sr = np.outer(vols, vols) * R; Sc = np.zeros((6, 6)); Sc[:5, :5] = Sr; Sc[5, 5] = 0.005 ** 2         # cash uncorrelated
gc = np.linalg.solve(Sc, np.ones(6)); gc /= gc.sum()
kap_r, kap_c = np.linalg.cond(Sr), np.linalg.cond(Sc)
assert gc[5] > 0.95 and kap_c > 50 * kap_r
print(f"PASS MVO: GMV, frontier w(m) and sigma^2(m), two-fund separation, utility form, tangency (= numerical max Sharpe; "
      f"Tobin separation; rf >= m_g failure), long-only max Sharpe via convex form, Markowitz critical lines ({corners} corners), "
      f"Jagannathan-Ma KKT shrinkage and DGNU Prop. 1, condition-number bound attained; cash in Sigma: GMV {gc[5]:.1%} cash, "
      f"kappa {kap_r:.0f} -> {kap_c:.0f}")
