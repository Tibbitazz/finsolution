"""Reference specification of the multifactor composite (Renshaw, Gu, Candar & Ang 2026; iSTOXX methodology guide §118,
version of 13 Oct 2026; owner decisions REN-D1 ... REN-D7, 2026-10-25). Synthetic data only; construction, not replication.

Checks (record `S4_SCORING_RENSHAW_ANG.md` §6):
P-R1  transform: parent-weighted z has zero parent-weighted mean; truncation at +/-3; available-signal mean; re-z.
P-R2  active exposure (w - b)'s is invariant to the centring of s (sum of active weights is zero).
P-R3  missing-signal rule: the composite of k available signals has dispersion ~ sqrt((1 + (k - 1)rho)/k) relative to
      one signal, so sparsely covered names land in the tails unless corrected.
P-R4  EQ-MAP-5: max s'a s.t. a'Sa <= TE^2, 1'a = 0 equals the closed form a ~ S^-1(s - sbar 1); invariant to positive
      scaling and shifts of s, not to monotone non-linear transforms.
P-R5  alpha eating: with diagonal residual risk EQ-MAP-5 positions scale as z/omega^2, EQ-MAP-3 as z/omega.
P-R6  timing rules: doubling/halving against each of the other three factors; renormalised weights stay within
      [0.4x, 2.0x] of nominal per model; effective number of factors 3.6 static, 3.32 / 2.58 as in the source.
P-R7  factor momentum (18-month IR, margin 0.15) and factor-of-factors (EWMA 10%, +/-0.3 pp) worked examples;
      ensemble 50/25/25 never eliminates a factor.
P-R8  market similarity (July paper App. C; guide §118.1.2): training uses only realised labels (m + 3 <= t); the
      paper-literal burn-in (36-month windows, 36-month z, 36 PCA rows, 36 labelled rows, 3-month embargo) gives the
      first forecast 143 months after daily data start: 24 Jun 2002 + 143 months = May 2014 (source: June 2014).
Run: python3 s4ren_multifactor_reference.py"""
import warnings
import numpy as np
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # numpy 2.0 matmul raises spurious FP warnings on macOS Accelerate
rng = np.random.default_rng(20261025)
errors = []
def err(m): errors.append(m)

# ---------------------------------------------------------------- P-R1 ... P-R3 transform
def wz(x, b):
    """z against the parent universe with parent (capitalisation) weights; missing values (nan) omitted."""
    ok = ~np.isnan(x); bb = b[ok] / b[ok].sum(); mu = bb @ x[ok]; sd = np.sqrt(bb @ (x[ok] - mu) ** 2)
    return (x - mu) / sd
trunc = lambda z: np.clip(z, -3, 3)
def factor_score(signals, b):
    Z = np.column_stack([trunc(wz(s, b)) for s in signals])
    comp = np.nanmean(Z, axis=1)                                   # equal weights over available signals
    return trunc(wz(comp, b)), Z
N = 500; b = rng.lognormal(0, 1.2, N); b /= b.sum()
sig = [rng.standard_normal(N) for _ in range(3)]; sig[0][7] = 40.0; sig[1][rng.random(N) < .2] = np.nan
f, Z = factor_score(sig, b)
z0 = wz(sig[2], b)
if abs(b @ z0) > 1e-12 or abs(np.sqrt(b @ z0 ** 2) - 1) > 1e-12: err('P-R1: parent-weighted z does not have mean 0 and s.d. 1')
if np.nanmax(np.abs(Z)) > 3 + 1e-12 or np.abs(f).max() > 3 + 1e-12: err('P-R1: truncation at +/-3 not applied')
if not np.isfinite(f).all(): err('P-R1: a missing signal should be omitted, not propagate')
miss = np.where(np.isnan(sig[1]))[0]; comp_chk = np.nanmean(Z, axis=1)
if not np.allclose(comp_chk[miss], Z[miss][:, [0, 2]].mean(1)): err('P-R1: a missing signal must be omitted, not imputed')
if not np.allclose(f, trunc(wz(comp_chk, b))): err('P-R1: factor score is not the re-z of the available-signal mean')
w = np.clip(b + rng.normal(0, .002, N), 0, None); w /= w.sum(); s = rng.standard_normal(N)
if abs((w - b) @ s - (w - b) @ (s + 7.3)) > 1e-12: err('P-R2: active exposure depends on centring')
rho, n = .3, 200000
C = rho + (1 - rho) * np.eye(6); X = rng.standard_normal((n, 6)) @ np.linalg.cholesky(C).T
ratio = X[:, :1].mean(1).std() / X.mean(1).std(); theory = np.sqrt(1 / ((1 + 5 * rho) / 6))
if abs(ratio - theory) > .01 or abs(theory - 1.55) > .01: err(f'P-R3: dispersion ratio {ratio:.3f} vs {theory:.3f}')

# ---------------------------------------------------------------- P-R4, P-R5 EQ-MAP-5
n = 8; A = rng.standard_normal((n, n)); S = A @ A.T / n + .05 * np.eye(n); s = rng.standard_normal(n); te = .01
def maxexp(score):
    cons = [{'type': 'ineq', 'fun': lambda a: te ** 2 - np.einsum('i,ij,j->', a, S, a)}, {'type': 'eq', 'fun': lambda a: a.sum()}]
    return minimize(lambda a: -score @ a, np.zeros(n), constraints=cons, method='SLSQP', options={'ftol': 1e-15, 'maxiter': 1000}).x
Si, o = np.linalg.inv(S), np.ones(n)
d = Si @ (s - (o @ Si @ s) / (o @ Si @ o)); d *= te / np.sqrt(d @ S @ d)
a1, a2, a3 = maxexp(s), maxexp(5 * s + 2), maxexp(np.exp(s))
if np.abs(a1 - d).max() > 1e-6: err('P-R4: maximum exposure differs from the closed form')
if np.abs(a2 - a1).max() > 1e-6: err('P-R4: positive scaling and shift should not change the solution')
if np.abs(a3 - a1).max() < 1e-4: err('P-R4: a non-linear monotone transform should change the solution')
om = np.array([.20, .40]); z = np.array([1., 1.])
pos5 = z / om ** 2; pos3 = (om * z) / om ** 2                      # unconstrained a = D^-1 alpha with D = diag(omega^2)
if abs(pos5[0] / pos5[1] - 4) > 1e-12 or abs(pos3[0] / pos3[1] - 2) > 1e-12: err('P-R5: alpha-eating ratios differ from 4 and 2')

# ---------------------------------------------------------------- P-R6, P-R7 timing rules
NOM = np.array([1/3, 1/3, 1/6, 1/6]); F4 = ['MOM', 'QLT', 'EVAL', 'CVAL']
def rule(x, thr):
    w = NOM.copy()
    for i in range(4):
        oth = np.delete(x, i)
        if (x[i] >= oth + thr).all(): w[i] *= 2
        if (x[i] <= oth - thr).all(): w[i] /= 2
    return w / w.sum()
enb = lambda v: 1 / (v ** 2).sum()
def model(dbl=None, hlf=None):
    v = NOM.copy()
    if dbl is not None: v[dbl] *= 2
    if hlf is not None: v[hlf] /= 2
    return v / v.sum()
ratios = [model(i, j)[k] / NOM[k] for i in [None, 0, 1, 2, 3] for j in [None, 0, 1, 2, 3] if i != j or i is None for k in range(4)]
if abs(min(ratios) - .4) > 1e-12 or abs(max(ratios) - 2) > 1e-12: err('P-R6: per-model bounds differ from [0.4x, 2.0x]')
ext = min(enb(model(i, j)) for i in range(4) for j in range(4) if i != j)
if abs(enb(NOM) - 3.6) > 1e-9 or abs(enb(.5 * model(0) + .5 * NOM) - 3.32) > .005 or abs(ext - 2.58) > .005: err('P-R6: effective numbers differ')
p = np.array([.72, .55, .60, .41])                                  # market similarity: MOM +12 pts over each, CVAL -14 under each
if not np.allclose(rule(p, .10), model(0, 3)): err('P-R6: market-similarity rule (each of the other three) not reproduced')
if not np.allclose(rule(np.array([.72, .65, .60, .41]), .10), model(None, 3)): err('P-R6: no doubling when the lead over one factor is < 10 pts')
fir = np.array([.9, .3, .7, -.4]); w_fm = rule(fir, .15)          # factor momentum: 0.9 - 0.7 = 0.2 >= 0.15; -0.4 is 0.7 below
if not np.allclose(w_fm, model(0, 3)): err('P-R7: factor-momentum rule not reproduced')
e_prev = {'MOM': 25.0, 'CVAL': 5.0}; act = {'MOM': 29.0, 'CVAL': 1.0}
e_now = {k: .1 * act[k] + .9 * e_prev[k] for k in e_prev}        # +0.4 pp for MOM, -0.4 pp for CVAL
v = NOM.copy()
if e_now['MOM'] - e_prev['MOM'] >= .3: v[0] *= 2
if e_now['CVAL'] - e_prev['CVAL'] <= -.3: v[3] /= 2
w_ff = v / v.sum()
if not np.allclose(w_ff, model(0, 3)): err('P-R7: factor-of-factors rule not reproduced')
w_final = .5 * rule(p, .10) + .25 * w_fm + .25 * w_ff
if abs(w_final.sum() - 1) > 1e-12 or w_final.min() <= 0: err('P-R7: the 50/25/25 ensemble must sum to 1 and keep every factor')

# ---------------------------------------------------------------- P-R8 market similarity: embargo and burn-in
DPM, H = 22, 3
def first_forecast_month(n_months, rescore=False, embargo=True):
    """Months available for each stage when daily data start at month 0 (structure only; data values irrelevant)."""
    feat0 = 36 - 1                                    # 36-month long windows (vol, beta, skew)
    z0 = feat0 + 36 - 1                               # 36 monthly feature values for the rolling z-score
    pca0 = z0 + 36 - 1                                # PCA scores start after 36 complete months
    first_scored = z0 if rescore else pca0            # paper-literal: own-date scores exist only from pca0
    for t in range(n_months):
        if t < pca0: continue
        last_label = t - H if embargo else t - 1
        n_lab = max(0, last_label - first_scored + 1)
        if n_lab >= 36: return t
    return None
t_lit, t_res = first_forecast_month(300), first_forecast_month(300, rescore=True)
if t_lit != 143: err(f'P-R8: paper-literal first forecast at month {t_lit}, expected 143')
if t_res != 108: err(f'P-R8: re-scored first forecast at month {t_res}, expected 108')
y0, m0 = 2002, 6; tot = (m0 - 1) + t_lit; y1, m1 = y0 + tot // 12, tot % 12 + 1
if (y1, m1) != (2014, 5): err(f'P-R8: base date + burn-in = {y1}-{m1:02d}, expected 2014-05')
def training_rows(t, rows, embargo=True):
    return [m for m in rows if (m + H <= t if embargo else m <= t - 1)]
rows = list(range(100, 150))
if any(m + H > 149 for m in training_rows(149, rows)): err('P-R8: a training label extends beyond the forecast date')
if not any(m + H > 149 for m in training_rows(149, rows, embargo=False)): err('P-R8: the leaky variant should be detectable')
Hs = rng.standard_normal((60, 5)); dd = np.sqrt(((Hs[:, None] - Hs[None]) ** 2).sum(-1))[np.triu_indices(60, 1)]
h = np.percentile(dd, 25); wk = np.exp(-np.sqrt(((Hs - Hs[-1]) ** 2).sum(1)) ** 2 / (2 * h ** 2))
if not (wk.max() <= 1 and (dd <= h).mean() > .249 and (dd <= h).mean() < .251): err('P-R8: bandwidth is not the 25th percentile of pairwise distances')

assert not errors, 'Reference-specification check failed:\n  - ' + '\n  - '.join(errors)
print(f'PASS Renshaw et al. reference specification: parent-weighted z/truncation/available-signal mean; centring-invariant active '
      f'exposure; missing-signal dispersion x{theory:.2f} (k = 1 vs 6, rho = 0.3); EQ-MAP-5 = closed form, scale/shift invariant, not '
      f'transform-invariant; alpha eating 4x vs 2x; per-model bounds [0.4x, 2.0x], ENB 3.6/3.32/{ext:.2f}; timing rules and 50/25/25 '
      f'ensemble reproduced; market similarity embargo enforced, first forecast month {t_lit} (paper-literal; {t_res} re-scored) = '
      f'{y1}-{m1:02d} from the 24 Jun 2002 base date.')
