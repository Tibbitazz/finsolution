"""S4.12a source reproduction and derivations for PC-B5 (mean-downside risk): Sortino & van der Meer (JPM 17(4), 1991,
fn. 3 and Figure 4); Kahn & Stefek (Advances ch. 27, eqs. A7-A10, fn. 12); Markowitz, Todd, Xu & Yamane (Ann. OR 45,
1993, eqs. 3.1-3.8); Estrada (J. Appl. Finance 18(1), 2008, eqs. 5, 10-11); Cesarone et al. (FRL 91, 2026, eqs. 1, 15).
Maximum Sortino ratio by homogenisation, and its reduction to the tangency portfolio under normality."""
import numpy as np, warnings
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.stats import norm
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
rng = np.random.default_rng(20261018)

# --- Definitions. S&vdM fn. 3: DR = int_{-inf}^{M} (M - r)^2 f(r) dr = K&S (A7) TSV with t = M. Normal closed form (A10). ----
def tsv_normal(m, s, t):                                                    # E[((t - r)^+)^2], r ~ N(m, s^2); d = m - t
    d = m - t; return (s ** 2 + d ** 2) * norm.cdf(-d / s) - s * d * norm.pdf(d / s)
for m, s, t in [(.08, .16, 0.), (.01, .045, -.0289), (.05, .10, .09)]:
    num = quad(lambda r: (t - r) ** 2 * norm.pdf(r, m, s), -np.inf, t)[0]
    assert abs(tsv_normal(m, s, t) - num) < 1e-12                           # (A9) normal integral = (A10) closed form
    assert abs(tsv_normal(m, s, m) - s ** 2 / 2) < 1e-15                    # target at the mean: half the variance
# KS-1 (fn. 12): an annual return target converted with sqrt(12), a volatility scaling, instead of a return scaling.
assert abs(-.10 / np.sqrt(12) + .02887) < 1e-5 and abs(-.10 / 12 + .00833) < 1e-5 and abs(.9 ** (1 / 12) - 1 + .00874) < 1e-5

# --- SVDM-1: Figure 4. Printed downside variances 6.4 and 25.6 (%^2) = SP x (average shortfall)^2 with SP = 0.40 and
# average shortfalls 4% and 8%. For a lower tail rising linearly from a to the MAR M, fn. 3 gives SP (M - a)^2 / 6 while the
# average shortfall is (M - a)/3, i.e. fn. 3 = 1.5 x the printed figure; the A:B ratio of 4 is unchanged.
assert np.isclose(.4 * 4 ** 2, 6.4) and np.isclose(.4 * 8 ** 2, 25.6)
for a in (-3., -15.):                                                       # drawn left vertices of A and B, MAR 9
    M = 9.; pdf = lambda r: 2 * (r - a) / (M - a) ** 2                      # tail density shape, normalised to mass 1 on [a, M]
    avg = quad(lambda r: (M - r) * pdf(r), a, M)[0]; dr = quad(lambda r: (M - r) ** 2 * pdf(r), a, M)[0]
    assert np.isclose(avg, (M - a) / 3) and np.isclose(dr, 1.5 * avg ** 2)
tri = lambda a, c, b: ((a + b + c) / 3, np.sqrt((a * a + b * b + c * c - a * b - a * c - b * c) / 18))
assert np.allclose(tri(-3, 12, 25), (11.33, 5.72), atol=.01) and np.allclose(tri(-15, 13, 19), (5.67, 7.41), atol=.01)   # not 10/12

# --- MTXY (3.1b) with a constant benchmark c: S_c(x) = (1/T) sum ((r_t'x - c)^-)^2. QP (3.7)-(3.8) vs direct convex (15). ---
T, n = 120, 4; vol = np.array([.045, .03, .012, .06]) ; Cm = np.full((n, n), .35) + .65 * np.eye(n); Cm[2, :2] = Cm[:2, 2] = -.1
Lc = np.linalg.cholesky(np.outer(vol, vol) * Cm)
Zs = rng.standard_t(5, (T, n)) @ Lc.T * np.sqrt(3 / 5); Zs[:, 3] -= .04 * (rng.random(T) < .06)    # crash jumps: skew
mu = np.array([.007, .005, .002, .009]); Rs = Zs - Zs.mean(0) + mu                                 # Grinold-recentred on mu
c = 0.0
S_c = lambda x, R=Rs, c=c: np.mean(np.minimum(R @ x - c, 0) ** 2)
S_c_grad = lambda x, R=Rs, c=c: 2 * (np.minimum(R @ x - c, 0)[:, None] * R).mean(0)
cons = [{'type': 'eq', 'fun': lambda x: x.sum() - 1}]
def direct(E):
    return minimize(S_c, np.ones(n) / n, jac=S_c_grad, method='SLSQP', bounds=[(0, 1)] * n,
                    constraints=cons + [{'type': 'eq', 'fun': lambda x: mu @ x - E}], options={'ftol': 1e-16, 'maxiter': 1000}).x
def mtxy_qp(E):                                         # variables (x, Z): min sum Z^2/T s.t. B x + Z >= 0, Z >= 0 (Y = Bx + Z)
    B = (Rs - c) / np.sqrt(T)
    f = lambda v: v[n:] @ v[n:]; g = lambda v: np.r_[np.zeros(n), 2 * v[n:]]
    v0 = np.r_[np.ones(n) / n, np.maximum(-(B @ (np.ones(n) / n)), 0)]
    r = minimize(f, v0, jac=g, method='SLSQP', bounds=[(0, 1)] * n + [(0, None)] * T,
                 constraints=[{'type': 'eq', 'fun': lambda v: v[:n].sum() - 1}, {'type': 'eq', 'fun': lambda v: mu @ v[:n] - E},
                              {'type': 'ineq', 'fun': lambda v: B @ v[:n] + v[n:], 'jac': lambda v: np.c_[B, np.eye(T)]}],
                 options={'ftol': 1e-16, 'maxiter': 2000})
    return r.x[:n], r.fun
for E in (.004, .006, .008):
    xd = direct(E); xq, fq = mtxy_qp(E)
    assert abs(S_c(xd) - fq) < 1e-10 and np.abs(xd - xq).max() < 1e-4      # exact QP = direct convex problem
for _ in range(2000):                                                        # convexity (Cesarone Remark 4; Bawa 1978)
    x1, x2 = rng.dirichlet(np.ones(n), 2); assert S_c((x1 + x2) / 2) <= (S_c(x1) + S_c(x2)) / 2 + 1e-15

# --- Estrada (2008) eq. (5): Sigma_B,ij = (1/T) sum min(R_i - B, 0) min(R_j - B, 0); exogenous approximation of eq. (10). ---
D = np.minimum(Rs - c, 0); SB = D.T @ D / T
gaps = [abs(x @ SB @ x - S_c(x)) / S_c(x) for x in rng.dirichlet(np.ones(n), 500)]
assert max(gaps) > .05                                                       # not exact in general (endogeneity)
Rcon = np.where(rng.random((T, 1)) < .3, -np.abs(rng.normal(.03, .02, (T, n))), np.abs(rng.normal(.02, .01, (T, n))))
Dc = np.minimum(Rcon, 0); SBc = Dc.T @ Dc / T                                # all assets below B together, or none
for x in rng.dirichlet(np.ones(n), 200): assert abs(x @ SBc @ x - S_c(x, Rcon, 0.)) < 1e-15   # exact under concordance
xh = minimize(lambda x: x @ SB @ x, np.ones(n) / n, method='SLSQP', bounds=[(0, 1)] * n, constraints=cons, options={'ftol': 1e-16}).x
xe = minimize(S_c, np.ones(n) / n, jac=S_c_grad, method='SLSQP', bounds=[(0, 1)] * n, constraints=cons, options={'ftol': 1e-16}).x
assert S_c(xe) <= S_c(xh) and np.abs(xe - xh).max() > .01                    # heuristic optimum is not the exact optimum

# --- Maximum Sortino ratio (mu'x - c)/sqrt(S_c(x)): homogenise x = y / sum y, fix (mu - c)'y = 1, minimise S_c-type QP. ----
def max_sortino_hom(R, m, c):
    f = lambda y: np.mean(np.minimum((R - c) @ y, 0) ** 2); g = lambda y: 2 * (np.minimum((R - c) @ y, 0)[:, None] * (R - c)).mean(0)
    y0 = np.ones(len(m)) / ((m - c).sum())
    y = minimize(f, y0, jac=g, method='SLSQP', bounds=[(0, None)] * len(m), constraints=[{'type': 'eq', 'fun': lambda y: (m - c) @ y - 1}],
                 options={'ftol': 1e-18, 'maxiter': 2000}).x
    return y / y.sum()
sortino = lambda x, R=Rs, m=mu, c=c: (m @ x - c) / np.sqrt(np.mean(np.minimum(R @ x - c, 0) ** 2))
xs = max_sortino_hom(Rs, mu, c)
best = max((minimize(lambda x: -sortino(x), x0, method='SLSQP', bounds=[(0, 1)] * n, constraints=cons, options={'ftol': 1e-15}).x
            for x0 in [np.ones(n) / n] + list(rng.dirichlet(np.ones(n), 15))), key=sortino)
assert sortino(xs) >= sortino(best) - 1e-9 and np.abs(xs - best).max() < 1e-3   # homogenised convex form = global maximum
E_s = mu @ xs; assert abs(S_c(direct(E_s)) - S_c(xs)) < 1e-10                    # and it lies on the MTXY frontier
# EQ-SPLIT-1 fit: with MAR = the cash rate, the Sortino ratio of k*p + (1-k)*cash does not depend on k (as for Sharpe);
# with MAR != cash rate it does, so scaling to sigma* would change the objective.
rf = .002; rp = Rs @ xs; mp = mu @ xs
srt_k = lambda k, mar: (k * mp + (1 - k) * rf - mar) / np.sqrt(np.mean(np.minimum(k * rp + (1 - k) * rf - mar, 0) ** 2))
assert np.ptp([srt_k(k, rf) for k in (.5, 1, 1.5, 2)]) < 1e-12 and np.ptp([srt_k(k, 0.) for k in (.5, 1, 1.5, 2)]) > 1e-3

# --- Normality: Sortino(x) = k / sqrt(g(k)) with k = (mu'x - c)/sigma(x), g(k) = (1+k^2)N(-k) - k phi(k) decreasing for k > 0,
# so maximum Sortino = maximum Sharpe at rate c (tangency), and the mean-TSV frontier = the MV frontier.
gk = lambda k: (1 + k ** 2) * norm.cdf(-k) - k * norm.pdf(k); ks = np.linspace(0.01, 3, 300)
assert np.all(np.diff(ks / np.sqrt(gk(ks))) > 0) and np.allclose(gk(ks) * 1, [tsv_normal(k, 1, 0) for k in ks])
V = np.outer(vol, vol) * Cm
sr_n = lambda x: (mu @ x - c) / np.sqrt(tsv_normal(mu @ x, np.sqrt(x @ V @ x), c))
sh = lambda x: (mu @ x - c) / np.sqrt(x @ V @ x)
opt = lambda f: max((minimize(lambda x: -f(x), x0, method='SLSQP', bounds=[(0, 1)] * n, constraints=cons, options={'ftol': 1e-16}).x
                     for x0 in [np.ones(n) / n] + list(rng.dirichlet(np.ones(n), 10))), key=f)
assert np.abs(opt(sr_n) - opt(sh)).max() < 1e-5                                     # max Sortino = tangency (normal)
for E in (.004, .006, .008):
    ex = lambda E=E: [{'type': 'eq', 'fun': lambda x: mu @ x - E}]
    a1 = minimize(lambda x: tsv_normal(mu @ x, np.sqrt(x @ V @ x), c), np.ones(n) / n, method='SLSQP', bounds=[(0, 1)] * n,
                  constraints=cons + ex(), options={'ftol': 1e-18}).x
    a2 = minimize(lambda x: x @ V @ x, np.ones(n) / n, method='SLSQP', bounds=[(0, 1)] * n, constraints=cons + ex(), options={'ftol': 1e-18}).x
    assert np.abs(a1 - a2).max() < 1e-5                                              # same frontier portfolio
print(f"PASS B5 downside: fn. 3 = (A7), (A10) exact; KS-1; SVDM-1 (Figure 4 = SP x avg^2, fn. 3 is 1.5x, ratio 4 kept); "
      f"MTXY QP = direct convex; Estrada heuristic inexact (max rel. gap {max(gaps):.2f}) except under concordant shortfalls; "
      f"max Sortino by homogenisation {xs.round(3)} on the frontier; under normality max Sortino = tangency, mean-TSV = MV frontier")
