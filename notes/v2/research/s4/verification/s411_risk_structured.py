"""S4.11 risk-structured methods PC-C1 ... PC-C5. SPECIFICATION VERIFICATION ONLY; synthetic data except printed examples; PASS.
Sources:
  C1 GMV: Clarke, de Silva & Thorley 2006, JPM 33(1):10-24 (long-only, 3% cap, budget; long/short = budget only);
     CdST 2011, JPM 37(2):31-45, eqs. (1)-(2), (A-2)-(A-7) (single-index closed forms; supporting)
  C2 ERC: Maillard, Roncalli & Teiletche (working version May 2009; JPM 2010 governs), eqs. (1)-(8), sec. 4.1 example,
     App. A.1, A.3; Spinu 2013 (solver; port of s44_risk_parity_spinu.py)
  C3 HRP: Lopez de Prado 2016 (port of s44_hrp_lopez_de_prado.py: V0 list bisection, V1 tree split)
  C4 MDP: Choueifaty & Coignard 2008, JPM 35(1):40-51, eqs. (1)-(8), (11)-(12), Examples 1-2
  C5 MinCorr: Varadi, Kapler, Bee & Rittenhouse 2012, pp. 13-16 (transcription of Kapler's min.corr / min.corr2; MCA-1..3)"""
import numpy as np, pandas as pd, warnings
from math import erf, sqrt, log
from scipy.optimize import minimize
from scipy.stats import rankdata
import scipy.cluster.hierarchy as sch
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261018); inv = np.linalg.inv
sd = lambda w, S: np.sqrt(w @ S @ w); rc = lambda w, S: w * (S @ w) / (w @ S @ w)          # Euler risk-contribution shares
def cov_from(vol, C): return np.outer(vol, vol) * C
def rand_cov(n, k=None):
    A = rng.normal(size=(n, k or 2 * n)); C = A @ A.T / (k or 2 * n); d = np.sqrt(np.diag(C))
    return cov_from(rng.uniform(0.05, 0.35, n), C / np.outer(d, d))
def gmv_lo(S, ub=1.0):
    n = len(S); return minimize(lambda w: w @ S @ w, np.ones(n) / n, jac=lambda w: 2 * S @ w, bounds=[(0, ub)] * n,
        constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}], method='SLSQP', options={'ftol': 1e-16, 'maxiter': 2000}).x
def spinu(C, b=None, tol=1e-12, maxit=500):
    n = len(C); b = np.ones(n) / n if b is None else b
    d = np.sqrt(np.diag(C)); R = C / np.outer(d, d); bb = b / b.min()
    x = np.sqrt(bb.sum()) / np.sqrt(R.sum()) * np.ones(n); lam_star = 0.95 * (3 - np.sqrt(5)) / 2
    for _ in range(maxit):
        u = R @ x - bb / x; dx = np.linalg.solve(R + np.diag(bb / x ** 2), u); lam = np.sqrt(u @ dx)
        if lam > lam_star: x = x - dx / (1 + np.max(np.abs(dx / x)))
        elif lam > tol: x = x - dx
        else: break
    y = x / d; return y / y.sum()
def mdp_lo(S):                                                     # max DR long-only <=> min w'Sw s.t. sigma'w = 1, w >= 0
    n = len(S); s = np.sqrt(np.diag(S))
    v = minimize(lambda w: w @ S @ w, np.ones(n) / n, jac=lambda w: 2 * S @ w, bounds=[(0, None)] * n,
        constraints=[{'type': 'eq', 'fun': lambda w: s @ w - 1}], method='SLSQP', options={'ftol': 1e-16, 'maxiter': 2000}).x
    return v / v.sum()
DR = lambda w, S: (w @ np.sqrt(np.diag(S))) / sd(w, S)

# ===== C1 GMV =====
for _ in range(20):
    n = 8; S = rand_cov(n); one = np.ones(n)
    g = inv(S) @ one / (one @ inv(S) @ one)                                                  # EQ-MVO-4 closed form
    assert np.allclose(g, minimize(lambda w: w @ S @ w, one / n, constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}],
                                   method='SLSQP', options={'ftol': 1e-16}).x, atol=1e-6)
    gv = minimize(lambda w: np.sqrt(w @ S @ w), one / n, bounds=[(0, 1)] * n, constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}],
                  method='SLSQP', options={'ftol': 1e-16}).x
    assert np.allclose(gv, gmv_lo(S), atol=1e-5)                                             # ANG-07: argmin sigma = argmin sigma^2
# CdST 2011 single-index closed forms (A-5), (A-6), (1), (2), (A-7)
N = 150; sM = 0.16; beta = rng.uniform(0.5, 1.6, N); se = rng.uniform(0.15, 0.45, N); S1 = sM ** 2 * np.outer(beta, beta) + np.diag(se ** 2)
bLS = (1 + sM ** 2 * np.sum(beta ** 2 / se ** 2)) / (sM ** 2 * np.sum(beta / se ** 2))
gu = inv(S1) @ np.ones(N) / (np.ones(N) @ inv(S1) @ np.ones(N)); sMV2 = gu @ S1 @ gu
assert np.allclose(gu, sMV2 / se ** 2 * (1 - beta / bLS))                                     # eq. (1)
assert np.isclose(gu @ beta, sMV2 / (sM ** 2 * bLS))                                         # (A-7)
order = np.argsort(beta); bL = None
for m in range(1, N + 1):                                                                    # (A-6): running sums over the lowest betas
    h = order[:m]; cand = (1 + sM ** 2 * np.sum(beta[h] ** 2 / se[h] ** 2)) / (sM ** 2 * np.sum(beta[h] / se[h] ** 2))
    if m == N or beta[order[m]] >= cand: bL = cand; break
held = beta < bL; wl = np.where(held, (1 - beta / bL) / se ** 2, 0); wl /= wl.sum()
glo = gmv_lo(S1); assert np.abs(glo - wl).max() < 2e-4 and held.sum() < N                    # eq. (2) = numerical long-only GMV
assert abs(0.76 ** 2 - 0.578) < 1e-3                                                          # CdST 2006 p. 16: variance-ratio test statistic
gcap = gmv_lo(S1, ub=0.03); assert gcap.max() <= 0.03 + 1e-6 and abs(gcap.sum() - 1) < 1e-8 and sd(gcap, S1) >= sd(glo, S1) - 1e-10

# ===== C2 ERC (MRT) =====
vol4 = np.array([0.10, 0.20, 0.30, 0.40])
for rho, mv_expect in ((0.5, [1, 0, 0, 0]), (0.3, [0.895, 0.105, 0, 0]), (0.0, [0.702, 0.176, 0.078, 0.044])):
    S = cov_from(vol4, np.full((4, 4), rho) + (1 - rho) * np.eye(4))
    assert np.allclose(np.round(spinu(S), 2), [0.48, 0.24, 0.16, 0.12])                     # eq. (3): ERC = 1/sigma
    assert np.allclose(np.round(gmv_lo(S), 3), mv_expect, atol=1.5e-3)                     # sec. 4.1 MV weights
C4 = np.array([[1, .8, 0, 0], [.8, 1, 0, 0], [0, 0, 1, -.5], [0, 0, -.5, 1]]); S = cov_from(vol4, C4)
ew = np.ones(4) / 4; assert round(100 * sd(ew, S), 1) == 11.5 and np.allclose(100 * rc(ew, S), [12.3, 26.4, 14.1, 47.2], atol=0.06)   # 14.15 printed as 14.1
mv = gmv_lo(S); assert round(100 * sd(mv, S), 1) == 8.6 and np.allclose(np.round(100 * mv, 1), [74.5, 0, 15.2, 10.3], atol=0.051)
erc = spinu(S); assert round(100 * sd(erc, S), 1) == 10.3 and np.allclose(np.round(100 * erc, 1), [38.4, 19.2, 24.3, 18.2])
assert np.allclose(np.round((S @ erc) / sd(erc, S), 3), [0.067, 0.134, 0.106, 0.141], atol=1.5e-3) and np.allclose(rc(erc, S), 0.25)
bet = (S @ erc) / (erc @ S @ erc); assert np.allclose(erc, (1 / bet) / 4)                     # eq. (5): x_i = 1/(n beta_i)
cstar = np.sum(np.log(erc))                                                                   # eq. (8): min vol s.t. sum ln x >= c
lb = minimize(lambda w: w @ S @ w, ew, bounds=[(1e-9, 1)] * 4, method='SLSQP', options={'ftol': 1e-16, 'maxiter': 2000},
              constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}, {'type': 'ineq', 'fun': lambda w: np.sum(np.log(w)) - cstar}]).x
assert np.allclose(lb, erc, atol=1e-4)
f6 = lambda x: np.sum((x * (S @ x) - (x * (S @ x))[:, None]) ** 2)                            # eq. (6) objective is 0 at ERC
assert f6(erc) < 1e-16
for _ in range(200):                                                                          # A.3 ordering; uniqueness (Spinu = SLSQP on eq. 6)
    S = rand_cov(6); e = spinu(S); m = gmv_lo(S)
    assert sd(m, S) <= sd(e, S) + 1e-9 <= sd(np.ones(6) / 6, S) + 2e-9
S = rand_cov(5); e = spinu(S)
alt = minimize(lambda x: np.sum((x * (S @ x) - (x * (S @ x))[:, None]) ** 2) * 1e6, rng.dirichlet(np.ones(5)), bounds=[(0, 1)] * 5,
               constraints=[{'type': 'eq', 'fun': lambda x: x.sum() - 1}], method='SLSQP', options={'ftol': 1e-20, 'maxiter': 5000}).x
assert np.allclose(alt, e, atol=1e-4)
s2 = np.array([0.12, 0.30])                                                                   # sec. 3.1: two assets, independent of rho
for rho in (-0.5, 0.2, 0.9): assert np.allclose(spinu(cov_from(s2, np.array([[1, rho], [rho, 1]]))), (1 / s2) / (1 / s2).sum())
n = 5; rmin = -1 / (n - 1) + 1e-7; vol5 = rng.uniform(0.1, 0.4, n)                               # App. A.1: ERC = MV at the lowest constant rho
Sm = cov_from(vol5, np.full((n, n), rmin) + (1 - rmin) * np.eye(n)); gm = inv(Sm) @ np.ones(n); gm /= gm.sum()
assert np.allclose(gm, (1 / vol5) / (1 / vol5).sum(), atol=1e-5)
mu_eq = 0.4 * vol5; Sc = cov_from(vol5, np.full((n, n), 0.3) + 0.7 * np.eye(n)); t = inv(Sc) @ mu_eq; t /= t.sum()
assert np.allclose(t, spinu(Sc))                                                               # sec. 3.5: constant rho + equal Sharpe -> ERC = MSR
Sv = cov_from(np.full(4, 0.2), C4); xe = spinu(Sv); avg = C4 @ xe                              # eq. (4) (equal vols): x_i ∝ 1/sum_k x_k rho_ik
assert np.allclose(xe, (1 / avg) / (1 / avg).sum())
# ERC under a weight cap: the long-only ERC is unique, so a cap below an ERC weight makes exact ERC infeasible
assert erc.max() > 0.30

# ===== C3 HRP (V0 published list bisection; V1 tree split) =====
def ivp(c): w = 1. / np.diag(c); return w / w.sum()
def cvar_(cov, items): c = cov.loc[items, items].values; w = ivp(c); return w @ c @ w
def dist(corr): return ((1 - corr.clip(-1, 1)) / 2.) ** .5                                    # HRP-2: clip
def quasi_diag(link):
    link = link.astype(int); o = [link[-1, 0], link[-1, 1]]; nn = link[-1, 3]
    while max(o) >= nn: o = [x for q in o for x in ((link[q - nn, 0], link[q - nn, 1]) if q >= nn else (q,))]
    return o
def hrp_v0(S):
    cov = pd.DataFrame(S); d = np.sqrt(np.diag(S)); corr = pd.DataFrame(S / np.outer(d, d))
    order = corr.index[quasi_diag(sch.linkage(dist(corr), 'single'))].tolist(); w = pd.Series(1.0, index=order); items = [order]
    while items:
        items = [i[j:k] for i in items for j, k in ((0, len(i) // 2), (len(i) // 2, len(i))) if len(i) > 1]
        for a in range(0, len(items), 2):
            v0, v1 = cvar_(cov, items[a]), cvar_(cov, items[a + 1]); al = 1 - v0 / (v0 + v1); w[items[a]] *= al; w[items[a + 1]] *= 1 - al
    return w.sort_index().values
def hrp_v1(S):
    cov = pd.DataFrame(S); d = np.sqrt(np.diag(S)); corr = pd.DataFrame(S / np.outer(d, d)); link = sch.linkage(dist(corr), 'single')
    nn = len(S); mem = {i: [i] for i in range(nn)}
    for k, row in enumerate(link.astype(int)): mem[nn + k] = mem[row[0]] + mem[row[1]]
    w = pd.Series(1.0, index=range(nn))
    def split(node):
        if node < nn: return
        a, b = link[node - nn, :2].astype(int); v0, v1 = cvar_(cov, mem[a]), cvar_(cov, mem[b]); al = 1 - v0 / (v0 + v1)
        w[mem[a]] *= al; w[mem[b]] *= 1 - al; split(a); split(b)
    split(2 * nn - 2); return w.values
v0_changed = 0
for _ in range(60):
    S = rand_cov(10, 4); p = rng.permutation(10)
    for f in (hrp_v0, hrp_v1): w = f(S); assert abs(w.sum() - 1) < 1e-12 and (w > 0).all()
    w1, w1p = hrp_v1(S), hrp_v1(S[np.ix_(p, p)]); assert np.allclose(w1[p], w1p)              # V1 invariant to input order
    v0_changed += not np.allclose(hrp_v0(S)[p], hrp_v0(S[np.ix_(p, p)]))                    # V0 depends on input order (HRP-1)
    key = np.argsort(np.diag(S)); kp = np.argsort(np.diag(S[np.ix_(p, p)]))                   # V0 with a canonical order is deterministic
    assert np.allclose(hrp_v0(S[np.ix_(key, key)]), hrp_v0(S[np.ix_(p, p)][np.ix_(kp, kp)]))
assert v0_changed > 0
Sd = np.diag(rng.uniform(0.01, 0.1, 7))                                                        # uncorrelated assets: HRP = 1/sigma^2 = GMV
for f in (hrp_v0, hrp_v1): assert np.allclose(f(Sd), ivp(Sd)) and np.allclose(f(Sd), inv(Sd) @ np.ones(7) / (np.ones(7) @ inv(Sd) @ np.ones(7)))
S2 = cov_from(np.array([0.1, 0.25]), np.array([[1, .6], [.6, 1]]))
for f in (hrp_v0, hrp_v1): assert np.allclose(f(S2), ivp(S2))                                 # two assets: inverse variance
Cbad = np.array([[1, 1 + 2e-16], [1 + 2e-16, 1]]); assert not np.isnan(dist(pd.DataFrame(Cbad)).values).any()

# ===== C4 MDP (Choueifaty & Coignard) =====
S = cov_from(np.array([0.15, 0.30]), np.array([[1, .4], [.4, 1]])); assert np.allclose(np.round(100 * mdp_lo(S), 1), [66.7, 33.3])   # Example 1
S = cov_from(np.full(3, 0.2), np.array([[1, .9, .1], [.9, 1, .1], [.1, .1, 1]])); assert np.allclose(np.round(100 * mdp_lo(S), 1), [25.7, 25.7, 48.6])  # Example 2
for _ in range(50):
    n = 6; S = rand_cov(n); s = np.sqrt(np.diag(S)); C = S / np.outer(s, s)
    M = (inv(C) @ np.ones(n)) / s; M /= M.sum()                                              # eq. (4): M ∝ sigma^-1 C^-1 1 (unconstrained)
    num = minimize(lambda w: -DR(w, S), M + rng.normal(0, 0.01, n), constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}],
                   method='SLSQP', options={'ftol': 1e-14, 'maxiter': 2000}).x
    assert abs(DR(num, S) - DR(M, S)) < 1e-8
    rho_iM = (S @ M) / (s * sd(M, S)); assert np.allclose(rho_iM, 1 / DR(M, S))                # eqs. (6)-(7)
    P = rng.dirichlet(np.ones(n)); assert np.isclose((P @ S @ M) / (sd(P, S) * sd(M, S)), DR(P, S) / DR(M, S))   # eq. (8)
    Ml = mdp_lo(S); r = (S @ Ml) / (s * sd(Ml, S)); h = Ml > 1e-6                                # long-only: held equal, excluded higher
    assert np.ptp(r[h]) < 1e-5 and (r[~h] >= r[h].min() - 1e-6).all() and DR(Ml, S) >= 1
    Se = cov_from(np.full(n, 0.2), C); assert np.allclose(mdp_lo(Se), gmv_lo(Se), atol=1e-5)      # equal vols: MDP = GMV
    Scc = cov_from(s, np.full((n, n), 0.4) + 0.6 * np.eye(n))                                    # constant rho: MDP = 1/sigma = ERC
    assert np.allclose(mdp_lo(Scc), (1 / s) / (1 / s).sum(), atol=1e-5) and np.allclose(spinu(Scc), (1 / s) / (1 / s).sum())
    k = 0.3; t = inv(S) @ (k * s); t /= t.sum(); assert np.allclose(t, M)                        # tangency iff mu ∝ sigma
    wB = rng.dirichlet(np.ones(n)); muB = S @ wB; t = inv(S) @ muB; t /= t.sum(); assert np.allclose(t, wB)   # eq. (11): mu_i ∝ rho_iB sigma_i
    t = inv(S) @ np.ones(n); t /= t.sum(); assert np.allclose(t, inv(S) @ np.ones(n) / (np.ones(n) @ inv(S) @ np.ones(n)))  # eq. (12)
assert abs(DR(np.r_[1.0, np.zeros(5)], S) - 1) < 1e-12

# ===== C5 MinCorr / MinCorr2 (Varadi et al.; Kapler's code) =====
Phi = lambda x, m, s_: 0.5 * (1 + erf((x - m) / (s_ * sqrt(2))))
def rank_desc(x): o = np.argsort(-np.asarray(x)); r = np.empty(len(x)); r[o] = np.arange(1, len(x) + 1); return r
def min_corr(R, sig, power=1):
    n = len(sig); iu = np.triu_indices(n, 1); c = R[iu]; mu, sdv = c.mean(), c.std(ddof=1)
    if not np.isfinite(sdv) or sdv < 1e-12: return None                                      # MCA-4: undefined (N = 2 or constant rho)
    A = np.zeros((n, n)); A[iu] = [1 - Phi(v, mu, sdv) for v in c]; A = A + A.T
    avg = A.sum(1) / (n - 1); wr = rank_desc(avg) ** power; wr = wr / wr.sum(); w = wr @ A; w = w / w.sum(); x = w / sig; return x / x.sum()
def min_corr2(R, sig, power=1):
    C = R.copy(); np.fill_diagonal(C, 0); avg = C.mean(1); mu, sdv = avg.mean(), avg.std(ddof=1)
    if not np.isfinite(sdv) or sdv < 1e-12: return None                                      # MCA-4: also any equal row averages
    t = np.array([1 - Phi(v, mu, sdv) for v in avg]); wr = rank_desc(t) ** power; wr = wr / wr.sum(); w = wr @ (1 - C); w = w / w.sum(); x = w / sig; return x / x.sum()
R3 = np.array([[1, .90, .85], [.90, 1, .70], [.85, .70, 1]]); sig3 = np.array([14, 18, 22.])
iu = np.triu_indices(3, 1); assert abs(R3[iu].mean() - 0.817) < 5e-4 and abs(R3[iu].std(ddof=1) - 0.104) < 5e-4    # pp. 15-16 intermediates
assert np.allclose(min_corr(R3, sig3).round(2), [0.21, 0.31, 0.48]) and np.allclose(min_corr2(R3, sig3).round(2), [0.50, 0.30, 0.20])   # MCA-1
for _ in range(50):
    n = 7; S = rand_cov(n); s = np.sqrt(np.diag(S)); R = S / np.outer(s, s); p = rng.permutation(n)
    for f in (min_corr, min_corr2):
        w = f(R, s); assert abs(w.sum() - 1) < 1e-12 and (w > 0).all()
        assert np.allclose(w[p], f(R[np.ix_(p, p)], s[p]))                                      # permutation equivariant
        assert np.allclose(w, f(R, 3 * s))                                                       # invariant to a common volatility scale
assert min_corr(np.array([[1, .3], [.3, 1]]), np.array([.1, .2])) is None and min_corr2(np.array([[1, .3], [.3, 1]]), np.array([.1, .2])) is None
Rc = np.full((4, 4), 0.5) + 0.5 * np.eye(4); assert min_corr(Rc, vol4) is None and min_corr2(Rc, vol4) is None   # constant rho: undefined
Rb = np.array([[1, .8, .2, .2], [.8, 1, .2, .2], [.2, .2, 1, .8], [.2, .2, .8, 1]])                               # equal row averages, rho not constant:
assert min_corr(Rb, vol4) is not None and min_corr2(Rb, vol4) is None                                          # MinCorr defined, MinCorr2 not
# C5 x O2 (S4.9 pending cell): MinCorr on a momentum-selected set is defined (N_sel >= 3, non-constant rho) and rank-only
S = rand_cov(30); s = np.sqrt(np.diag(S)); R = S / np.outer(s, s); score = rng.standard_normal(30)
outs = []
for sc in (score, np.exp(score), 3 * score + 7):
    sel = rankdata(sc) > 20; outs.append(min_corr(R[np.ix_(sel, sel)], s[sel]))
    assert outs[-1] is not None and abs(outs[-1].sum() - 1) < 1e-12
assert all(np.allclose(outs[0], o) for o in outs[1:])

print("PASS S4.11 risk-structured: GMV closed form and CdST 2011 single-index long-only formula (threshold beta) = numerical QP; "
      "MRT sec. 4.1 (1/n, MV, ERC tables), eqs. (3)-(8), A.1, A.3 ordering, MSR optimality; ERC unique (Spinu = SLSQP); "
      f"HRP V1 order-invariant, V0 order-dependent in {v0_changed}/60 cases but deterministic under a canonical order, HRP = 1/sigma^2 "
      "for uncorrelated assets; MDP C&C Examples 1-2, eqs. (4), (6)-(8), (11)-(12), long-only KKT, MDP = GMV (equal vols), "
      "MDP = ERC = 1/sigma (constant rho); MinCorr/MinCorr2 paper example (MCA-1), equivariance, undefined for N = 2 or constant rho "
      "(MCA-4; MinCorr2 also for equal row averages); C5 x O2 defined and rank-only")
