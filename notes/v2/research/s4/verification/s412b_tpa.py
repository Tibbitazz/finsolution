"""S4.12b source reproduction and distinctness test for PC-D4 (Total Portfolio Approach): Treynor & Black (J. Business
46(1), 1973) eqs. (10)-(32) and p. 78; AQR (Alternative Thinking 2026 Issue 2) fns. 11-12; Ang, Brandt & Denison (2014)
eq. (4) and App. C (A.3); the reference-relative TPA candidate (TPA-R) and its comparison with PC-B1, B1 with a tracking-error
budget, Roll's benchmark-relative optimum and Anchored EPO. Findings TB-1, TPA-1, TPA-2."""
import numpy as np, warnings
from scipy.optimize import minimize, brentq
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
rng = np.random.default_rng(20261018)

# ============================ Treynor & Black ============================
# n securities r_i = b_i r_M + z_i (independent z, eq. 2) plus the market asset M (eq. 5). Excess returns.
n = 6; b = rng.uniform(.6, 1.4, n); s = rng.uniform(.15, .35, n); app = rng.normal(0, .02, n)   # appraisal premiums
mm, sm = .06, .16
S = np.zeros((n + 1, n + 1)); S[:n, :n] = sm ** 2 * np.outer(b, b) + np.diag(s ** 2); S[:n, n] = S[n, :n] = sm ** 2 * b; S[n, n] = sm ** 2
mu = np.r_[b * mm + app, mm]
tan = np.linalg.solve(S, mu)                                                    # Markowitz, unconstrained
lam = 1.0; h = lam * app / s ** 2                                               # eq. (10)/(13): active positions
hm = lam * mm / sm ** 2 - h @ b                                                 # eq. (16): explicit market position
assert np.allclose(np.r_[h, hm], tan * lam / 1.0)                               # = Markowitz (eq. 17 statement), lambda = 1
SR2 = mu @ tan                                                                  # squared Sharpe ratio of the tangency
MR, AR2 = mm ** 2 / sm ** 2, np.sum(app ** 2 / s ** 2)                          # T&B's "market ratio" and "appraisal ratio"
assert abs(SR2 - (MR + AR2)) < 1e-12                                            # eq. (19): squared ratios add (TB-1)
mu_a, var_a = h @ app, h @ (s ** 2 * h); hM_tot = hm + h @ b                    # eq. (20) with the active portfolio as one asset
assert np.isclose((mu_a / (hM_tot * mm)), var_a / (hM_tot ** 2 * sm ** 2)) and np.isclose(var_a / (hM_tot ** 2 * sm ** 2), AR2 / MR)
w = np.r_[h, hm]; rho2 = (hM_tot * sm) ** 2 / (w @ S @ w)
assert np.isclose(rho2, 1 / (1 + AR2 / MR))                                     # eq. (25)
# eqs. (28)-(32): bivariate normal (z, e); conditional mean rho (s_z/s_e) e = IC * omega * standardised score (EQ-MAP-3).
r_, sz, se, T = 0.1, .2, 1.7, 2_000_000
e = rng.normal(0, se, T); z = r_ * sz / se * e + rng.normal(0, sz * np.sqrt(1 - r_ ** 2), T)
slope = np.cov(z, e)[0, 1] / e.var(); resid = z - slope * e
assert abs(slope - r_ * sz / se) < 1e-3 and abs(resid.var() / ((1 - r_ ** 2) * sz ** 2) - 1) < 5e-3       # (28), (29)
zbar = r_ * sz * (e / se); assert abs(np.mean(zbar ** 2 / ((1 - r_ ** 2) * sz ** 2)) / (r_ ** 2 / (1 - r_ ** 2)) - 1) < 5e-3   # (32)
# p. 78: without short selling half the terms of eq. (26) are suppressed: the squared ratio halves, AR falls by 1/sqrt(2).
A = rng.normal(0, .02, (20000, 40)); sig = rng.uniform(.1, .3, (20000, 40))
full, lo = (A ** 2 / sig ** 2).sum(1), (np.maximum(A, 0) ** 2 / sig ** 2).sum(1)
assert abs(lo.mean() / full.mean() - .5) < 5e-3 and abs(np.sqrt(lo).mean() / np.sqrt(full).mean() - 1 / np.sqrt(2)) < 1e-2

# ============================ AQR fns. 11-12 ============================
# Existing optimal stock/bond portfolio; a new asset regressed on stock and bond excess returns (unconstrained betas).
Sf = np.array([[.16 ** 2, .1 * .16 * .06], [.1 * .16 * .06, .06 ** 2]]); mf = np.array([.05, .02])
bet, se_new, al = np.array([.4, -.6]), .17, .03                                 # e.g. commodities (Exhibit 1-type betas)
S3 = np.zeros((3, 3)); S3[:2, :2] = Sf; S3[2, :2] = S3[:2, 2] = Sf @ bet; S3[2, 2] = bet @ Sf @ bet + se_new ** 2
m3 = np.r_[mf, bet @ mf + al]
x_old = np.linalg.solve(Sf, mf); x_new = np.linalg.solve(S3, m3)
assert abs(m3 @ x_new - (mf @ x_old + (al / se_new) ** 2)) < 1e-12                 # fn. 11: SR^2_max = SR^2_current + AR^2
assert np.isclose(x_new[2], al / se_new ** 2) and np.allclose(x_new[:2], x_old - bet * x_new[2])   # fn. 12

# ============================ ABD and the TPA-R candidate ============================
assert np.isclose(1.3 * .07 - .3 * .02 - (.02 + 1.3 * (.07 - .02)), 0)          # eq. (4): beta 1.3 = $1.30 stocks - $0.30 bonds
N = 8                                                                          # Eq, Bd (reference assets), HY, RE, Cmd, EM, SC, AR
sE, sF, rEF = .16, .06, .1
Sf = np.array([[sE ** 2, rEF * sE * sF], [rEF * sE * sF, sF ** 2]])
Bm = np.array([[1, 0], [0, 1], [.45, .35], [.55, .45], [.35, -.5], [1.15, -.1], [1.1, -.05], [.05, .1]])   # model loadings
res = np.array([0, 0, .05, .10, .17, .12, .08, .06]); Rc = np.eye(N); Rc[2, 3] = Rc[3, 2] = .3; Rc[5, 6] = Rc[6, 5] = .2
D = np.outer(res, res) * Rc; S = Bm @ Sf @ Bm.T + D
alpha_model = np.array([0, 0, .003, -.002, .02, .006, .004, .02]); mu = Bm @ np.array([.05, .02]) + alpha_model
wref = np.r_[.6, .4, np.zeros(N - 2)]
# ABD (A.3): betas on stocks and bonds constrained to sum to one = regression of (r_i - r_F) on (r_E - r_F).
dEF = np.r_[1, -1, np.zeros(N - 2)]
bE = np.array([(S[i] - S[1]) @ dEF / (dEF @ S @ dEF) for i in range(N)]); Bc = np.c_[bE, 1 - bE]
Xs = rng.multivariate_normal(np.zeros(N), S, 400000)                            # sample check of the constrained OLS
for i in (2, 4, 7):
    yv, xv = Xs[:, i] - Xs[:, 1], Xs[:, 0] - Xs[:, 1]; assert abs(np.cov(yv, xv)[0, 1] / xv.var() - bE[i]) < .01
M = np.eye(N); M[0, :] -= Bc[:, 0]; M[1, :] -= Bc[:, 1]                         # funding: w = wref + M a
alpha_abd = mu - Bc @ mu[:2]
# TPA-1: residuals of the sum-to-one regression are correlated with the reference, so total variance is not additive.
Eres = M.T @ S @ M; cov_ref = M.T @ S @ wref
assert np.abs(cov_ref[2:]).max() > 1e-4
# TPA-2: the funding set changes the alpha. With cash as a funding leg (unconstrained betas, AQR) the alpha is the model alpha;
# with stocks and bonds only (ABD) the bond premium of the forced funding is subtracted.
assert np.allclose(mu - Bm @ mu[:2], alpha_model) and abs(alpha_abd[7] - .0005) < 2e-4 and alpha_abd[4] < 0 < alpha_model[4]

TE = .03
te = lambda w: np.sqrt((w - wref) @ S @ (w - wref)); vol = lambda w: np.sqrt(w @ S @ w); sr = lambda w: mu @ w / vol(w)
starts = [np.r_[0, 0, np.random.default_rng(k).uniform(0, .05, N - 2)] for k in range(8)]
def tpa_r(long_only=True):                                                      # max alpha'a s.t. TE <= budget (ABD funding)
    cons = [{'type': 'ineq', 'fun': lambda a: TE ** 2 - (M @ a) @ S @ (M @ a)}]
    if long_only: cons.append({'type': 'ineq', 'fun': lambda a: wref + M @ a})
    best = None
    for a0 in starts:
        r = minimize(lambda a: -alpha_abd @ a, a0, method='SLSQP', bounds=[(0, 0)] * 2 + [(0, 1) if long_only else (None, None)] * (N - 2),
                     constraints=cons, options={'ftol': 1e-15, 'maxiter': 2000})
        if r.success and (best is None or r.fun < best.fun): best = r
    return wref + M @ best.x
w_tpa = tpa_r()
assert abs(te(w_tpa) - TE) < 1e-6 and w_tpa.min() > -1e-9 and abs(w_tpa.sum() - 1) < 1e-12
assert np.allclose(Bc.T @ w_tpa, Bc.T @ wref, atol=1e-9)                        # ABD exposures pinned at the reference
assert abs(w_tpa @ S @ w_tpa - (wref @ S @ wref + te(w_tpa) ** 2)) > 5e-5        # TPA-1 in the solution
# Unconstrained TPA-R: a = TE * E^-1 alpha / sqrt(alpha' E^-1 alpha) on the non-reference block (T&B / AQR multivariate form).
Enr = Eres[2:, 2:]; anr = alpha_abd[2:]; a_cf = TE * np.linalg.solve(Enr, anr) / np.sqrt(anr @ np.linalg.solve(Enr, anr))
assert np.allclose(tpa_r(long_only=False), wref + M @ np.r_[0, 0, a_cf], atol=1e-5)
cs = {'type': 'eq', 'fun': lambda w: w.sum() - 1}
def opt(f, cons=(), k=10, budget=True):
    best = None
    for s_ in range(k):
        r = minimize(f, np.random.default_rng(s_).dirichlet(np.ones(N)), method='SLSQP', bounds=[(0, 1)] * N,
                     constraints=([cs] if budget else []) + list(cons), options={'ftol': 1e-15, 'maxiter': 2000})
        if r.success and (best is None or r.fun < best.fun): best = r
    return best.x
te_con = {'type': 'ineq', 'fun': lambda w: TE ** 2 - (w - wref) @ S @ (w - wref)}
expo_con = {'type': 'eq', 'fun': lambda w: Bc.T @ (w - wref)}
w_roll_neutral = opt(lambda w: -mu @ w, (te_con, expo_con), budget=False)   # budget implied: betas sum to one (keeping both
assert np.abs(w_roll_neutral - w_tpa).max() < 1e-4                              # stalls SLSQP; a solver artefact, not a difference)
assert abs(w_roll_neutral.sum() - 1) < 1e-10                                    # TPA-R = Roll's problem + exposure neutrality
# Distinctness at the same tracking error: B1 long-only (also factor-MVO here: S is factor-structured), B1 with the TE budget,
# Roll's benchmark-relative optimum without neutrality, Anchored EPO (anchor = reference, w set so TE = 3%).
w_b1 = opt(lambda w: -sr(w)); w_b1te = opt(lambda w: -sr(w), (te_con,)); w_roll = opt(lambda w: -mu @ w, (te_con,))
V = np.diag(np.diag(S))
def epo_a(t):
    Sw = (1 - t) * S + t * V; x = np.linalg.solve(Sw, mu); g = np.sqrt(x @ S @ x) / np.sqrt(wref @ S @ wref)
    return np.linalg.solve(Sw, (1 - t) * mu / g + t * V @ wref)
w_epo = epo_a(brentq(lambda t: te(epo_a(t)) - TE, 1e-6, 1 - 1e-9))
gaps = {nm: np.abs(x - w_tpa).max() for nm, x in [('B1', w_b1), ('B1+TE', w_b1te), ('Roll', w_roll), ('AnchoredEPO', w_epo)]}
assert min(gaps.values()) > .15
# Coincidence: cash-funded betas (AQR), reference = factor tangency (mu_f = lam Sf w_f), no constraints -> TPA = tangency.
lam_ = 2.5; mf_t = lam_ * Sf @ np.array([.6, .4]); mu_t = Bm @ mf_t + alpha_model
x_tan = np.linalg.solve(S, mu_t)
Dnr = D[2:, 2:]; act = np.zeros(N); act[2:] = np.linalg.solve(Dnr, alpha_model[2:]); act[:2] = -Bm[2:].T @ act[2:]
assert np.allclose(x_tan, lam_ * wref + act)                                   # tangency = lam * reference + funded active portfolio
print(f"PASS TPA S4.12b: T&B (10)-(17) = Markowitz, (19) squared ratios add (TB-1), (20), (25), (28)-(32), p. 78 halving; "
      f"AQR fns. 11-12; ABD (4), (A.3); TPA-1 (non-additive total risk), TPA-2 (funding set changes alpha: AR "
      f"{alpha_model[7]:.3f} -> {alpha_abd[7]:.4f}); TPA-R = Roll + exposure neutrality; distinct at TE 3%: "
      f"{ {k: round(v, 2) for k, v in gaps.items()} }; = tangency only unconstrained with a factor-efficient reference and cash funding")
