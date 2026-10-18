"""S4.12a derivations and tests for PC-D2 (drawdown; Chekhlov-Uryasev-Zabarankin, UF report 2003-15) and PC-D3 (tail-risk
parity; Boudt-Carl-Peterson, version of 24 May 2012): drawdown definitions and the convex relative form (CDD-3), the
feasibility boundary gamma_min (CDD-2), scenario location (NT-1), ERC-CVaR existence (BCP-4), MCC vs ERC-CVaR (BCP-1),
modified-CVaR accuracy (BCP-5), determinism (BCP-3), and D3 x O2."""
import numpy as np, warnings
from scipy.optimize import linprog, minimize, differential_evolution
from scipy.stats import norm, skew, kurtosis
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
rng = np.random.default_rng(20261018)

# ============================ PC-D2 drawdown ============================
def dd_abs(r): w = np.r_[0, np.cumsum(r)]; return (np.maximum.accumulate(w) - w).max()            # CUZ eqs. 6-7
def dd_log(r): w = np.r_[0, np.cumsum(np.log1p(r))]; return (np.maximum.accumulate(w) - w).max()
def dd_rel(r): v = np.r_[1, np.cumprod(1 + r)]; return (1 - v / np.maximum.accumulate(v)).max()     # ANG p. 15 (compounded)
P = rng.normal(.006, .045, (1000, 120))
a_, l_, r_ = (np.array([f(p) for p in P]) for f in (dd_abs, dd_log, dd_rel))
assert np.abs(r_ - (1 - np.exp(-l_))).max() < 1e-12                       # relative MaxDD = 1 - exp(-MaxDD of log wealth), exact
assert (l_ >= a_ - 1e-15).all()                                            # ln(1+r) <= r: log drawdown >= CUZ absolute drawdown
alt = np.tile([.2, -.2], 20); assert abs(dd_abs(alt) - .2) < 1e-12 and dd_rel(alt) > .63   # choppy path: CUZ 20%, relative 63%
crash = np.r_[np.full(24, .03), np.full(10, -.06)]; assert dd_abs(crash) > dd_rel(crash) + .05   # trend decline: the reverse
# CDD-1 quantified: neither measure bounds the other, so gamma has no exact mapping between them.

T, m = 60, 4; R = rng.normal(0, [.02, .045, .07, .012], (T, m)); R += np.array([.004, .006, .008, .003]) - R.mean(0)   # recentred
def path_rows(R):
    T, m = R.shape; A = np.zeros((T, m + T))
    for k in range(T):
        A[k, :m] = -R[k]; A[k, m + k] = -1
        if k: A[k, m + k - 1] = 1                                          # y_k >= y_{k-1} - r_k'x  (drawdown recursion)
    return A
def maxdd_lp(R, gam):                                                       # CUZ eq. (55): max mean s.t. MaxDD <= gam
    T, m = R.shape
    return linprog(np.r_[-R.sum(0), np.zeros(T)], A_ub=path_rows(R), b_ub=np.zeros(T), A_eq=[np.r_[np.ones(m), np.zeros(T)]],
                   b_eq=[1], bounds=[(0, 1)] * m + [(0, gam)] * T, method='highs')
def gamma_min_abs(R):                                                       # min over x of MaxDD: LP with one extra variable
    T, m = R.shape; A = np.c_[path_rows(R), np.zeros(T)]; B = np.c_[np.zeros((T, m)), np.eye(T), -np.ones((T, 1))]
    res = linprog(np.r_[np.zeros(m + T), 1], A_ub=np.r_[A, B], b_ub=np.zeros(2 * T), A_eq=[np.r_[np.ones(m), np.zeros(T + 1)]],
                  b_eq=[1], bounds=[(0, 1)] * m + [(0, None)] * (T + 1), method='highs')
    return res.fun, res.x[:m]
gmin, xg = gamma_min_abs(R); assert abs(dd_abs(R @ xg) - gmin) < 1e-9
assert maxdd_lp(R, gmin + 1e-7).status == 0 and maxdd_lp(R, gmin - 1e-4).status == 2   # CDD-2: infeasible exactly below gamma_min

# CDD-3: the relative (compounded) MaxDD constraint is convex in x: over every window (j,k], -sum ln(1 + r_t'x) is convex.
J = np.array([(j, k) for k in range(1, T + 1) for j in range(k)])
def logdd_windows(x): L = np.r_[0, np.cumsum(np.log1p(R @ x))]; return L[J[:, 0]] - L[J[:, 1]]
def logdd_jac(x): G = R / (1 + R @ x)[:, None]; CG = np.r_[np.zeros((1, m)), np.cumsum(G, 0)]; return CG[J[:, 0]] - CG[J[:, 1]]
for _ in range(2000):
    x1, x2 = rng.dirichlet(np.ones(m), 2)
    assert dd_log(R @ ((x1 + x2) / 2)) <= (dd_log(R @ x1) + dd_log(R @ x2)) / 2 + 1e-12   # midpoint convexity
def cdd_log(x, al):                                                         # CDD (CUZ eq. 14) on log drawdowns
    L = np.r_[0, np.cumsum(np.log1p(R @ x))]; Dk = (np.maximum.accumulate(L) - L)[1:]; q_ = len(Dk); c_ = np.r_[1.0, np.full(q_, 1 / ((1 - al) * q_))]
    return linprog(c_, A_ub=np.c_[-np.ones(q_), -np.eye(q_)], b_ub=-Dk, bounds=[(None, None)] + [(0, None)] * q_, method='highs').fun
for _ in range(300):
    x1, x2 = rng.dirichlet(np.ones(m), 2)
    for al in (0.5, 0.8, 0.95): assert cdd_log((x1 + x2) / 2, al) <= (cdd_log(x1, al) + cdd_log(x2, al)) / 2 + 1e-12
g_rel = 0.15; cap = -np.log(1 - g_rel)
res = minimize(lambda x: -R.sum(0) @ x, np.ones(m) / m, jac=lambda x: -R.sum(0), method='SLSQP', bounds=[(0, 1)] * m,
               constraints=[{'type': 'eq', 'fun': lambda x: x.sum() - 1},
                            {'type': 'ineq', 'fun': lambda x: cap - logdd_windows(x), 'jac': lambda x: -logdd_jac(x)}],
               options={'ftol': 1e-14, 'maxiter': 500})
x_rel = res.x; assert res.success and abs(dd_rel(R @ x_rel) - g_rel) < 1e-7                      # binds exactly at 15% relative
x_cuz = maxdd_lp(R, g_rel).x[:m]; assert abs(dd_abs(R @ x_cuz) - g_rel) < 1e-7 and abs(dd_rel(R @ x_cuz) - g_rel) > 2e-3 and np.abs(x_cuz - x_rel).max() > .02
# NT-1 for D2: drawdowns depend on drift; recentring the same paths moves gamma_min.
assert abs(gamma_min_abs(R - R.mean(0) + .002)[0] - gamma_min_abs(R - R.mean(0) + .008)[0]) > 0.01

# ============================ PC-D3 tail-risk parity ============================
a = 0.05; c2 = norm.pdf(norm.ppf(a)) / a
gcv = lambda w, mu, S: -w @ mu + c2 * np.sqrt(w @ S @ w)                                     # BCP eq. (7), Gaussian CVaR
gct = lambda w, mu, S: w * (-mu + c2 * (S @ w) / np.sqrt(w @ S @ w))                        # Euler contributions, eq. (3)
cs = {'type': 'eq', 'fun': lambda w: w.sum() - 1}
starts = lambda N: [np.ones(N) / N] + [np.random.default_rng(k).dirichlet(np.ones(N)) for k in range(12)]   # deterministic
def erc_cvar(mu, S):
    N = len(mu); best = None
    for x0 in starts(N):
        r = minimize(lambda w: 1e4 * ((gct(w, mu, S) - gcv(w, mu, S) / N) ** 2).sum(), x0, method='SLSQP', bounds=[(0, 1)] * N,
                     constraints=[cs], options={'ftol': 1e-18, 'maxiter': 1000})
        best = r if best is None or r.fun < best.fun else best
    return best.x, best.fun
def mcc(mu, S, st=None):                                                                     # BCP eq. (10), epigraph form
    N = len(mu); best = None
    for x0 in (st or starts(N)):
        r = minimize(lambda z: z[-1], np.r_[x0, gct(x0, mu, S).max()], method='SLSQP', bounds=[(0, 1)] * N + [(None, None)],
                     constraints=[{'type': 'eq', 'fun': lambda z: z[:N].sum() - 1},
                                  {'type': 'ineq', 'fun': lambda z: z[-1] - gct(z[:N], mu, S)}], options={'ftol': 1e-15, 'maxiter': 2000})
        ok = r.x[:N].min() > -1e-9 and abs(r.x[:N].sum() - 1) < 1e-8 and (gct(r.x[:N], mu, S) - r.x[-1]).max() < 1e-9
        if ok and (best is None or r.fun < best.fun): best = r
    return best.x[:N], best.fun
def erc_vol(S):                                                                              # C2 (Spinu objective), for comparison
    N = len(S); r = minimize(lambda y: .5 * y @ S @ y - np.log(y).sum() / N, np.ones(N), method='L-BFGS-B',
                             bounds=[(1e-12, None)] * N, options={'ftol': 1e-15, 'gtol': 1e-12})
    return r.x / r.x.sum()
vol = np.array([.16, .18, .05]); Cr = np.array([[1, .8, -.2], [.8, 1, -.2], [-.2, -.2, 1]]); S3 = np.outer(vol, vol) * Cr
mu3 = np.array([.06, .07, .02])
w0, f0 = erc_cvar(np.zeros(3), S3); assert f0 < 1e-12 and np.allclose(w0, erc_vol(S3), atol=1e-5)   # mu = 0: ERC-CVaR = ERC (C2)
w1, f1 = erc_cvar(mu3, S3); assert f1 < 1e-12 and np.abs(w1 - w0).max() > 0.005                   # with the mean: different
# BCP-4 existence: if mu_i >= c2*sigma_i then C_i < 0 for every w_i > 0 (Cauchy-Schwarz: (Sw)_i/sigma_p <= sigma_i), so no
# long-only portfolio has equal positive contributions. A cash-like asset in total-return CVaR meets the condition.
mu_c = np.array([.06, .025, .012]); vol_c = np.array([.16, .06, .005]); S_c = np.outer(vol_c, vol_c) * np.array([[1, .1, 0], [.1, 1, .1], [0, .1, 1]])
assert mu_c[2] >= c2 * vol_c[2]
W = rng.dirichlet(np.ones(3), 20000); assert (np.array([gct(w, mu_c, S_c)[2] for w in W]) < 0).all()
assert erc_cvar(mu_c, S_c)[1] > 1e-3 and erc_cvar(np.zeros(3), S_c)[1] < 1e-12                     # none exists; demeaned: exists
# BCP-1: MCC = ERC-CVaR in the BCP-like case; a valid case where they differ (both CVaR > 0, ERC exists).
wm, _ = mcc(mu3, S3); assert np.allclose(wm, w1, atol=1e-5)
mu_d = np.array([.02, .06, .07]); vol_d = np.array([.20, .10, .04])
C_d = np.array([[1, 0, .8], [0, 1, .5], [.8, .5, 1]]); assert np.linalg.eigvalsh(C_d).min() > .05
S_d = np.outer(vol_d, vol_d) * C_d; we, fe = erc_cvar(mu_d, S_d); wmd, tmd = mcc(mu_d, S_d)
assert fe < 1e-12 and gcv(we, mu_d, S_d) > 0 and gcv(wmd, mu_d, S_d) > 0
assert np.abs(we - wmd).max() > 0.04 and wmd[0] < 1e-6 and tmd < gcv(we, mu_d, S_d) / 3 - 1e-5     # MCC drops asset 1
# BCP-3 determinism: seeded DE reproduces exactly; deterministic multistart reproduces; two start sets agree.
de = lambda: differential_evolution(lambda v: np.max(gct(v / v.sum(), mu_d, S_d)), [(1e-6, 1)] * 3, seed=1, tol=1e-12,
                                    maxiter=3000, polish=True).x
d1, d2 = de(), de(); assert np.array_equal(d1, d2) and abs(np.max(gct(d1 / d1.sum(), mu_d, S_d)) - tmd) < 1e-7
alt_starts = [np.random.default_rng(100 + k).dirichlet(np.ones(3)) for k in range(13)]
assert abs(mcc(mu_d, S_d, alt_starts)[1] - tmd) < 1e-9

# BCP-5: modified CVaR (Appendix eqs. 21-22) vs large-sample historical CVaR, one asset.
def Iq(q, g):
    if q % 2 == 0:
        p = q // 2; full = np.prod([2 * j for j in range(1, p + 1)]); I = full * norm.pdf(g)
        for i in range(1, p + 1): I += full / np.prod([2 * j for j in range(1, i + 1)]) * g ** (2 * i) * norm.pdf(g)
    else:
        p = (q - 1) // 2; full = np.prod([2 * j + 1 for j in range(p + 1)]); I = -full * norm.cdf(g)
        for i in range(p + 1): I += full / np.prod([2 * j + 1 for j in range(i + 1)]) * g ** (2 * i + 1) * norm.pdf(g)
    return I
def mcvar1(m_, sd, s, k, al):
    z = norm.ppf(al); g = z + (z ** 2 - 1) * s / 6 + (z ** 3 - 3 * z) * k / 24 - (2 * z ** 3 - 5 * z) * s ** 2 / 36
    d = (norm.pdf(g) + (Iq(4, g) - 6 * Iq(2, g) + 3 * norm.pdf(g)) * k / 24 + (Iq(3, g) - 3 * Iq(1, g)) * s / 6
         + (Iq(6, g) - 15 * Iq(4, g) + 45 * Iq(2, g) - 15 * norm.pdf(g)) * s ** 2 / 72) / al
    return -m_ + sd * d
n_ = 4_000_000; r1 = np.random.default_rng(1)
X = {'crash mixture': np.where(r1.random(n_) < .05, r1.normal(-.06, .06, n_), r1.normal(.01, .035, n_)),
     't5': r1.standard_t(5, n_) * .04 + .007, 'normal': r1.normal(.007, .045, n_)}
err = {}
for nm, x in X.items():
    mm, sd, s, k = x.mean(), x.std(), skew(x), kurtosis(x); xs = np.sort(x)
    err[nm] = [(mcvar1(mm, sd, s, k, al) / -xs[:int(al * n_)].mean() - 1) * 100 for al in (.05, .025, .01)]
    if nm == 't5': mono = [mcvar1(mm, sd, s, k, al) for al in (.05, .025, .01)]
assert max(abs(e) for e in err['normal']) < 0.5                                 # exact in the normal case (sampling noise)
assert abs(err['crash mixture'][0]) > 5 and abs(err['t5'][0]) > 5               # > 5% off at alpha = 5% under fat tails
assert mono[2] < mono[1]                                                         # not monotone in alpha (t5: 1% < 2.5%)

# Historical-CVaR ERC through the convex log-barrier min CVaR_hist(y) - (1/N) sum ln y (unique minimiser):
q = 2000; vh = np.array([.045, .012, .06]); Lh = np.linalg.cholesky(np.outer(vh, vh) * np.array([[1, .1, .7], [.1, 1, .05], [.7, .05, 1]]))
Y = r1.standard_t(4, (q, 3)) @ Lh.T * np.sqrt(.5); Y[:, 2] -= 0.03 * (r1.random(q) < .05); Y -= Y.mean(0)
kq = int(round(q * a))
hcv = lambda w: np.sort(-Y @ w)[-kq:].mean()
hct = lambda w: w * (-Y[np.argsort(-Y @ w)[-kq:]].mean(0))
sol = []
for s_ in range(6):
    r = minimize(lambda y: hcv(y) - np.log(y).sum() / 3 if (y > 0).all() else 1e9, np.random.default_rng(s_).uniform(.2, 3, 3),
                 method='Powell', options={'xtol': 1e-12, 'ftol': 1e-14, 'maxiter': 200000})
    sol.append(r.x / r.x.sum())
sol = np.array(sol); assert np.ptp(sol, 0).max() < 1e-3                          # same solution from every start
assert np.abs(hct(sol[0]) / hcv(sol[0]) - 1 / 3).max() < 0.01                    # equal to +-0.01 (piecewise-linear CVaR)

# D3 x O2: ERC-CVaR (demeaned Gaussian) re-solved on a signal-selected subset of a 5-asset authoritative Sigma.
vol5 = np.array([.16, .18, .05, .12, .20]); C5 = np.full((5, 5), .3) + .7 * np.eye(5); C5[2, :2] = C5[:2, 2] = -.2
S5 = np.outer(vol5, vol5) * C5; score = np.array([.4, -.1, .9, .2, 1.3])
def d3_o2(sc, k=3):
    idx = np.sort(np.argsort(sc)[-k:]); w = np.zeros(5); w[idx] = erc_cvar(np.zeros(k), S5[np.ix_(idx, idx)])[0]; return w
w_a = d3_o2(score)
for tf in (np.exp, lambda v: v ** 3, lambda v: 2 * v + 7): assert np.allclose(d3_o2(tf(score)), w_a, atol=1e-8)
assert abs(w_a.sum() - 1) < 1e-12 and w_a.min() >= -1e-12 and (w_a > 0).sum() == 3

print(f"PASS CUZ/BCP S4.12a: relative DD = 1-exp(-log DD); CUZ vs relative differ both ways (CDD-1); gamma_min LP boundary "
      f"{gmin:.4f} (CDD-2); relative MaxDD convex, binds at 15% (CDD-3; CUZ at gamma=15% gives relative "
      f"{dd_rel(R @ x_cuz):.4f}); ERC-CVaR = ERC at mu=0, none exists with a cash-like asset (BCP-4); MCC != ERC case "
      f"(max |dw| {np.abs(we - wmd).max():.3f}); modified-CVaR error % at 5/2.5/1%: crash {np.round(err['crash mixture'], 1)}, "
      f"t5 {np.round(err['t5'], 1)} (BCP-5); seeded DE and multistart deterministic; historical ERC-CVaR unique; D3 x O2 rank-only")
