"""S4.9 addendum (owner review 2026-10-18): EPO inputs, double counting (R-7), the D cells of the signal x PC matrix, and the
ex ante transfer coefficient of momentum compositions. SPECIFICATION VERIFICATION ONLY; synthetic data; prints PASS.
Sources: PBL 2021 p. 127 and eqs. (18)-(22) (EPO consumes expected returns; scale calibration eq. 21); Daniel & Moskowitz 2016
sec. 3, Fig. 3 (time-varying betas of momentum portfolios); Clarke, de Silva & Thorley 2002 (transfer coefficient
TC = corr(dw_i omega_i, alpha_i / omega_i)); Grinold 1994 eq. (1) and Example 3 (alpha construction). ERC: Spinu (2013) port
from s44_risk_parity_spinu.py; HRP: tree-split variant from s44_hrp_lopez_de_prado.py; min-CVaR: Rockafellar-Uryasev LP."""
import numpy as np, pandas as pd, warnings
from scipy.optimize import minimize, linprog
from scipy.stats import rankdata
import scipy.cluster.hierarchy as sch
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261018); inv = np.linalg.inv

# ---------- method implementations (reference only) ----------
def spinu(C, b=None, tol=1e-10, maxit=500):                  # ERC / risk budgeting, Spinu (2013) Newton
    n = len(C); b = np.ones(n) / n if b is None else b
    d = np.sqrt(np.diag(C)); R = C / np.outer(d, d); bb = b / b.min()
    x = np.sqrt(bb.sum()) / np.sqrt(R.sum()) * np.ones(n); lam_star = 0.95 * (3 - np.sqrt(5)) / 2
    for _ in range(maxit):
        u = R @ x - bb / x; dx = np.linalg.solve(R + np.diag(bb / x ** 2), u); lam = np.sqrt(u @ dx)
        if lam > lam_star: x = x - dx / (1 + np.max(np.abs(dx / x)))
        elif lam > tol: x = x - dx
        else: break
    y = x / d; return y / y.sum()
def ivp(c): w = 1. / np.diag(c); return w / w.sum()
def cluster_var(cov, items): c = cov.loc[items, items].values; w = ivp(c); return w @ c @ w
def hrp_tree(covm):                                            # HRP, order-invariant tree-split variant
    cov = pd.DataFrame(covm); dd = np.sqrt(np.diag(covm)); corr = pd.DataFrame(covm / np.outer(dd, dd))
    link = sch.linkage(((1 - corr.clip(-1, 1)) / 2.) ** .5, 'single'); n = len(cov); names = list(cov.index)
    mem = {i: [names[i]] for i in range(n)}
    for k, row in enumerate(link.astype(int)): mem[n + k] = mem[row[0]] + mem[row[1]]
    w = pd.Series(1.0, index=names)
    def split(node):
        if node < n: return
        a, b = link[node - n, :2].astype(int); v0, v1 = cluster_var(cov, mem[a]), cluster_var(cov, mem[b]); al = 1 - v0 / (v0 + v1)
        w[mem[a]] *= al; w[mem[b]] *= 1 - al; split(a); split(b)
    split(2 * n - 2); return w.values
def gmv_lo(C):                                                 # long-only global minimum variance
    n = len(C); return minimize(lambda v: v @ C @ v, np.ones(n) / n, jac=lambda v: 2 * C @ v, bounds=[(0, 1)] * n,
        constraints=[{'type': 'eq', 'fun': lambda v: v.sum() - 1}], method='SLSQP', options={'ftol': 1e-15, 'maxiter': 1000}).x
def mdp_lo(C):                                                 # long-only most diversified portfolio (C&C 2008)
    n = len(C); s = np.sqrt(np.diag(C))
    v = minimize(lambda v: v @ C @ v, np.ones(n) / n, jac=lambda v: 2 * C @ v, bounds=[(0, None)] * n,
        constraints=[{'type': 'eq', 'fun': lambda v: s @ v - 1}], method='SLSQP', options={'ftol': 1e-15, 'maxiter': 1000}).x
    return v / v.sum()
def min_cvar(Rs, beta=0.95):                                   # long-only, fully invested min-CVaR (Rockafellar-Uryasev)
    T, n = Rs.shape; c = np.r_[np.zeros(n), 1.0, np.ones(T) / ((1 - beta) * T)]
    A = np.c_[-Rs, -np.ones(T), -np.eye(T)]; Aeq = np.r_[np.ones(n), 0, np.zeros(T)][None]
    r = linprog(c, A_ub=A, b_ub=np.zeros(T), A_eq=Aeq, b_eq=[1], bounds=[(0, None)] * n + [(None, None)] + [(0, None)] * T, method='highs')
    return r.x[:n]
rc_share = lambda w, C: w * (C @ w) / (w @ C @ w)              # Euler risk-contribution shares

# ===== A. EPO consumes expected returns (owner, 2026-10-18) =====
n = 8; A_ = rng.normal(size=(n, 2 * n)); Cc = A_ @ A_.T / (2 * n); d = np.sqrt(np.diag(Cc)); sg = rng.uniform(.05, .3, n)
Sg = np.outer(sg, sg) * Cc / np.outer(d, d); V = np.diag(sg ** 2); aa = np.ones(n) / n; s = rng.normal(0, .02, n); wsh = 0.4
Sw = (1 - wsh) * Sg + wsh * V
epo18 = lambda s_, g: inv(Sw) @ ((1 - wsh) * s_ / g + wsh * V @ aa)                     # PBL eq. (18)
def epo22(s_):                                                                          # PBL eqs. (21)-(22)
    g = np.sqrt((s_ @ inv(Sw) @ Sg @ inv(Sw) @ s_) / (aa @ Sg @ aa)); return epo18(s_, g)
at_sigma = lambda x, sstar=0.10: sstar / np.sqrt(x @ Sg @ x) * x                         # EQ-SPLIT-1 return branch (unconstrained, cash)
g0 = 3.0
assert np.allclose(epo18(s, g0), inv(Sw) @ ((1 - wsh) * s + wsh * g0 * V @ aa) / g0)    # MVO on mu~ = (1-w)s + w gamma V a, with Sigma_w
assert np.allclose(at_sigma(inv(Sw) @ (5 * s)), at_sigma(inv(Sw) @ s))                  # simple EPO: scale absorbed by the risk target
assert not np.allclose(epo18(5 * s, g0), epo18(s, g0), atol=1e-3)                        # anchored EPO, fixed gamma: scale matters
assert np.allclose(epo22(5 * s), epo22(s))                                               # eq. (22): scale removed by risk matching
rk = rankdata(s)
assert not np.allclose(epo22(rk), epo22(rk - rk.mean()), atol=1e-3)                      # ...location is not removed (R-1 applies)
assert not np.allclose(at_sigma(inv(Sw) @ rk), at_sigma(inv(Sw) @ (rk - rk.mean())), atol=1e-3)

# ===== B. Exposure and risk double counting (R-7a, R-7b) =====
ns = 30; sec = np.repeat([0, 1, 2], 10); beta = rng.uniform(0.6, 1.6, ns)
Bf = np.zeros((ns + 2, 5)); Bf[:ns, 0] = beta; Bf[np.arange(ns), 1 + sec] = 0.5; Bf[ns] = [-0.1, 0, 0, 0, 0]; Bf[ns + 1] = [0.3, 0, 0, 0, 0]
S = Bf @ np.diag([0.16, 0.06, 0.06, 0.06, 0.0]) ** 2 @ Bf.T + np.diag(np.r_[rng.uniform(0.15, 0.35, ns), 0.05, 0.18] ** 2)
cap = rng.lognormal(0, 1, ns); wE = cap / cap.sum(); score = rng.standard_normal(ns)
h = (rankdata(score) > 20).astype(float); h /= h.sum()                                   # long-only momentum sleeve: EW top third
unit = lambda v: np.r_[v, 0, 0]; E, M = unit(wE), unit(h); Bv, Cv = np.eye(ns + 2)[ns], np.eye(ns + 2)[ns + 1]
# B1 exact redundancy: stocks plus a sleeve of the same stocks -> singular joint covariance; splits are the same portfolio
Hs = np.c_[np.eye(ns), h]; Sa = Hs.T @ S[:ns, :ns] @ Hs
assert np.linalg.matrix_rank(Sa, tol=1e-12) == ns
x1 = np.r_[wE, 0.0]; x2 = np.r_[wE - 0.3 * h, 0.3]
assert np.allclose(Hs @ x1, Hs @ x2) and abs(x1 @ Sa @ x1 - x2 @ Sa @ x2) < 1e-14
# B2 unit-counting methods inflate the overlapped class when the sleeve is a separate unit
def class_methods(units):
    H = np.column_stack(units); Su = H.T @ S @ H; r = {}
    for nm, f in (('1/N', lambda C: np.ones(len(C)) / len(C)), ('1/sig', lambda C: (1 / np.sqrt(np.diag(C))) / (1 / np.sqrt(np.diag(C))).sum()),
                  ('ERC', spinu), ('HRP', hrp_tree), ('GMV', gmv_lo)):
        lt = H @ f(Su); r[nm] = (lt[:ns].sum(), rc_share(lt, S)[:ns].sum())           # look-through equity weight, equity risk share
    return r
b3, b4 = class_methods([E, Bv, Cv]), class_methods([E, Bv, Cv, M])
assert abs(b3['1/N'][0] - 1 / 3) < 1e-12 and abs(b4['1/N'][0] - 0.5) < 1e-12
assert b4['1/sig'][1] > b3['1/sig'][1] + 0.2 and abs(b3['ERC'][1] - 1 / 3) < 1e-6 and abs(b4['ERC'][1] - 0.5) < 1e-6
# B3 the fix (R-7a): momentum as a tilt inside the host class; class exposure and class risk share do not move with the tilt
for x in (0.0, 0.5, 1.0):
    r = class_methods([unit((1 - x) * wE + x * h), Bv, Cv])
    assert abs(r['1/N'][0] - 1 / 3) < 1e-12 and abs(r['ERC'][1] - 1 / 3) < 1e-6
e = 0.4                                                                                  # zero-investment active sleeve h - wE held at x
for x in (0.0, 0.2, 0.4): assert (e * wE + x * (h - wE) >= -1e-15).all() and abs((e * wE + x * (h - wE)).sum() - e) < 1e-12
assert (e * wE + 0.41 * (h - wE) < 0).any()                                              # long-only iff 0 <= x <= e
# B4 (R-7b) a sleeve's own return history misstates the risk of its current holdings when holdings rotate (DM 2016 sec. 3)
T = 240; b2 = np.r_[np.full(15, 0.6), np.full(15, 1.5)]; lo, hi = np.arange(15), np.arange(15, 30)
mkt = rng.normal(0.006, 0.045, T); R = np.outer(mkt, b2) + rng.normal(0, 0.06, (T, ns))
reg = np.r_[(np.arange(T - 24) // 30) % 2, np.ones(24, int)]                            # winners alternate; last two years high-beta
sleeve = np.array([R[t, hi].mean() if reg[t] else R[t, lo].mean() for t in range(T)])
beta_hist = np.cov(sleeve, mkt)[0, 1] / mkt.var(ddof=1); beta_now = b2[hi].mean()
assert beta_now - beta_hist > 0.3

# ===== C. Signal double counting (R-7c) =====
sg10 = rng.uniform(.1, .35, 10); sign = np.where(rng.standard_normal(10) > 0, 1, -1)
epo_w1 = (0.1 * sg10 * sign) / sg10 ** 2                                                 # PBL w = 1, s = SR0 sigma sign: positions carry the sign
assert (np.sign(epo_w1) == sign).all() and (sign * epo_w1 > 0).all()                     # a direction rule applied again makes every position long

# ===== D. D cells =====
# D1 sign x 1/N, sign x 1/sigma, sign x 1/sigma^2 = EPO(w = 1) with s = c sigma^k sign, k = 2, 1, 0 (PBL eq. 23; sigma^k as in eqs. 24-27)
for k, base in ((2, lambda v: np.ones_like(v)), (1, lambda v: 1 / v), (0, lambda v: 1 / v ** 2)):
    w1 = sg10 ** k * sign / sg10 ** 2
    assert np.allclose(w1 / np.abs(w1).sum(), sign * base(sg10) / base(sg10).sum())
# D2 O2 for correlation-aware and scenario methods: re-solve on the selected sub-matrix; the score enters only via the set
Ss = S[:ns, :ns]; Rsc = rng.multivariate_normal(np.zeros(ns), Ss / 52, 600)
for sc in (score, np.exp(score), 3 * score + 7):
    sel = rankdata(sc) > 20; C_ = Ss[np.ix_(sel, sel)]
    res = dict(GMV=gmv_lo(C_), ERC=spinu(C_), HRP=hrp_tree(C_), MDP=mdp_lo(C_), minCVaR=min_cvar(Rsc[:, sel]))
    for nm, w in res.items(): assert abs(w.sum() - 1) < 1e-6 and (w >= -1e-9).all(), nm
    assert np.allclose(rc_share(res['ERC'], C_), 0.1, atol=1e-6)
    if sc is score: ref = res
    else:
        for nm in ref: assert np.allclose(ref[nm], res[nm], atol=1e-6), nm
# D3 O3 (cash version) on correlation-aware methods: zeroing the down-trend assets is not the method on the up-trend set
up = np.zeros(ns, bool); up[rng.choice(ns, 12, replace=False)] = True
gz = np.where(up, gmv_lo(Ss), 0); gz /= gz.sum(); assert np.abs(gz[up] - gmv_lo(Ss[np.ix_(up, up)])).max() > 0.05
rcz = rc_share(np.where(up, spinu(Ss), 0), Ss)[up]; assert rcz.max() - rcz.min() > 0.01   # ERC survivors lose equal contributions
for base in (np.ones(ns), 1 / np.sqrt(np.diag(Ss)), 1 / np.diag(Ss)):                    # separable methods: zeroing == re-solving
    z = np.where(up, base / base.sum(), 0); assert np.allclose(z[up] / z.sum(), base[up] / base[up].sum())
# D4 O3 long-short: flipping signs of a correlation-aware solution is not the method on signed assets D Sigma D
dvec = np.where(up, 1.0, -1.0); Dm = np.diag(dvec)
g_flip = dvec * np.linalg.solve(Ss, np.ones(ns)); g_flip /= np.abs(g_flip).sum()
g_sgn = np.linalg.solve(Ss, dvec); g_sgn /= dvec @ g_sgn                                 # min w'Sw s.t. d'w = 1 == MVO with mu = c * sign
assert np.allclose(Dm @ (inv(Dm @ Ss @ Dm) @ np.ones(ns)) / (np.ones(ns) @ inv(Dm @ Ss @ Dm) @ np.ones(ns)), g_sgn)
assert np.abs(g_flip - g_sgn / np.abs(g_sgn).sum()).max() > 0.05
xs = Dm @ spinu(Dm @ Ss @ Dm)                                                            # signed ERC: risk parity in the orthant set by signs
assert (np.sign(xs) == dvec).all() and np.allclose(rc_share(xs, Ss), 1 / ns, atol=1e-6)
rcf = rc_share(Dm @ spinu(Ss), Ss); assert rcf.min() < 0                                 # flipped ERC: negative risk contributions

# ===== E. Ex ante transfer coefficient of momentum compositions (CdST 2002 definition; long-only security universe) =====
tc = {}
for seed in range(6):
    r_ = np.random.default_rng(1000 + seed); N = 300
    sec_ = r_.integers(0, 5, N); B = np.zeros((N, 6)); B[:, 0] = r_.uniform(0.6, 1.5, N); B[np.arange(N), 1 + sec_] = r_.uniform(0.3, 0.8, N)
    SS = B @ np.diag([0.16, .07, .07, .07, .07, .07]) ** 2 @ B.T + np.diag(r_.uniform(0.15, 0.40, N) ** 2)
    cp = r_.lognormal(0, 1.2, N); wB = cp / cp.sum(); vB = wB @ SS @ wB; bt = SS @ wB / vB; om = np.sqrt(np.diag(SS) - bt ** 2 * vB)
    raw = np.sqrt(np.diag(SS)) * r_.standard_normal(N)                                  # 12-1 returns: dispersion proportional to volatility
    xr = raw / om; Sc = (xr - xr.mean()) / xr.std(); al = 0.05 * om * Sc                 # Grinold: divide by vol, standardise, IC x vol x score
    sel = Sc > np.quantile(Sc, 2 / 3); Cs = SS[np.ix_(sel, sel)]; Rs = r_.multivariate_normal(np.zeros(sel.sum()), Cs / 52, 800)
    def full(ws): w = np.zeros(N); w[sel] = ws; return w
    comps = {'1/N (V)': full(np.ones(sel.sum()) / sel.sum()), 'cap (V)': full(cp[sel] / cp[sel].sum()),
             '1/sigma (V1)': full((1 / np.sqrt(np.diag(Cs))) / (1 / np.sqrt(np.diag(Cs))).sum()), 'ERC': full(spinu(Cs)),
             'GMV': full(gmv_lo(Cs)), 'HRP': full(hrp_tree(Cs)), 'MDP': full(mdp_lo(Cs)), 'min-CVaR': full(min_cvar(Rs))}
    for nm, w in comps.items():
        dd_ = w - wB; tc.setdefault(nm, []).append((np.corrcoef(dd_ * om, al / om)[0, 1], np.sqrt(dd_ @ SS @ dd_)))
tcm = {k: np.array(v).mean(0) for k, v in tc.items()}
assert min(tcm[k][0] for k in ('1/N (V)', '1/sigma (V1)', 'ERC')) > max(tcm[k][0] for k in ('GMV', 'HRP', 'MDP', 'min-CVaR')) + 0.1
assert max(tcm[k][1] for k in ('1/N (V)', '1/sigma (V1)', 'ERC')) < min(tcm[k][1] for k in ('GMV', 'HRP', 'MDP', 'min-CVaR'))

print("PASS S4.9 addendum: EPO = MVO on shrunk mean and covariance; PBL eq. 22 removes scale, not location; "
      f"sleeve as a unit: equity 1/N weight 0.33 -> 0.50, ERC risk share 0.33 -> 0.50, 1/sigma risk share {b3['1/sig'][1]:.2f} -> "
      f"{b4['1/sig'][1]:.2f}; tilt inside the host class leaves both unchanged; long-only active sleeve iff 0 <= x <= e; "
      f"history beta {beta_hist:.2f} vs holdings beta {beta_now:.2f}; sign rule on a signed output erases the trend; "
      "sign x 1/N, 1/sigma, 1/sigma^2 = EPO(w=1) with s ~ sigma^k sign (k = 2, 1, 0); O2 re-solves well defined and rank-only; "
      "O3 zeroing/flipping breaks GMV and ERC (signed GMV = MVO on sign; signed ERC = D x ERC(D Sigma D), equal contributions); TC "
      + ", ".join(f"{k} {v[0]:.2f}" for k, v in tcm.items()))
