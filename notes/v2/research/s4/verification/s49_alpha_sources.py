"""S4.9 addendum: source verification for the alpha mapping (EQ-MAP-3) and the transfer coefficient (EQ-TC-1).
  Grinold (1994), "Alpha is Volatility Times IC Times Score", JPM 20(4):9-16 (scan; exhibits typed from the pages)
  Grinold & Kahn, Advances in Active Portfolio Management (McGraw-Hill), ch. 3 eqs. (19)-(20), (35)-(37), Exhibit 11 and the
    four investment examples (governing, newest version of the forecasting rule and the fundamental law)
  Clarke, de Silva & Thorley (2002), FAJ 58(5):48-66, eqs. (6), (9), (11)-(12), Table 1, Appendix A
  Gallego, IEOR4706 Lecture 7 (Columbia, Autumn 2000), secs. 1.4-1.7 (secondary teaching note on Grinold & Kahn)
Synthetic data except the printed exhibits; prints PASS. Not reproducible without the authors' data: Grinold Exhibit 7
positions (BARRA covariance), CdST Figures 2-8 (Barra optimiser and S&P 500 risk model)."""
import numpy as np, warnings
from scipy.stats import norm
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261018); inv = np.linalg.inv
zs = lambda x: (x - x.mean()) / x.std()

# ===== Grinold 1994 =====
vol = np.array([13.41,14.42,15.89,16.29,16.93,17.29,18.92,18.97,19.17,19.20,19.83,20.17,20.43,20.44,20.54,21.13,22.33,23.26,23.46,30.32])
tot = np.array([23.13,25.77,24.40,25.32,25.98,25.15,26.89,29.36,29.77,26.98,22.68,31.64,31.52,24.36,28.92,24.95,33.90,33.31,33.16,38.63])
sc  = np.array([0.3507,0.7746,0.7094,-2.3165,-0.769,1.5844,-0.4825,-1.7717,0.3579,-0.0587,-0.0278,-0.8938,0.7404,-0.2455,-0.4458,-0.0043,0.8477,0.3482,1.9755,-0.6732])
a3  = np.array([0.42,1.01,1.01,-3.40,-1.17,2.47,-0.82,-3.02,0.62,-0.10,-0.05,-1.62,1.36,-0.45,-0.82,-0.01,1.70,0.73,4.17,-1.84])
assert np.allclose(np.round(vol * 0.09 * sc, 2), a3)                                      # Exhibit 3: eq. (1), IC 0.09
buy = np.array([-1,-1,1,-1,1,1,-1,1,-1,1,-1,1,-1,1,1,-1,-1,-1,1,1])
a5  = np.array([-1.21,-1.30,1.43,-1.47,1.52,1.56,-1.70,1.71,-1.73,1.73,-1.78,1.82,-1.84,1.84,1.85,-1.90,-2.01,-2.09,2.11,2.73])
assert np.allclose(np.round(vol * 0.09 * buy, 2), a5)                                     # Exhibit 5 (fn. 11: direction only, +-IC x vol)
assert np.allclose(np.round([20.17*.1, 20.17*.1*2, 20.17*.05, 20.17*.05*2], 2), [2.02, 4.03, 1.01, 2.02])   # Exhibit 4
assert abs((vol / tot).mean() - 0.70) < 0.01                                              # Exhibit 1: residual about 70% of total
real = np.array([4.38,2.65,4.40,-11.19,-5.74,10.38,-0.79,-6.71,2.93,-0.93,-0.99,-4.04,5.31,-4.25,-1.76,0.81,2.38,-0.71,7.45,-3.57])
edib = np.array([13.10,5.69,5.73,-4.29,-6.39,8.56,-4.85,-4.79,5.57,-6.37,-4.94,-5.13,4.97,-3.88,-4.74,-2.59,2.57,0.93,3.01,-2.18])
assert set(np.argsort(-np.abs(real))[:4]) == set(np.argsort(-np.abs(a3))[:4])             # Exhibit 7 text: largest positions = largest alphas
big = np.where(np.abs(edib) > 5)[0]; assert len(big) == 8 and (big < 10).sum() == 7        # "seven of the eight ... lower ten in residual volatility"
assert abs((0.07 - 0.35*0.04) / (1 - 0.35**2) - 0.0638) < 5e-5                            # eq. (3) example
assert abs((0.04 - 0.35*0.07) / (1 - 0.35**2) - 0.01766) < 5e-6                           # eq. (4) example: printed 0.0176 (GRI-1, truncation)
for ir, n, ic in ((1.33, 500, 0.06), (0.90, 500, 0.04), (0.44, 20, 0.098)): assert abs(ir / np.sqrt(n) - ic) < 6e-4   # fns. 6, 8
m = np.sqrt(2 / np.pi); rho9 = lambda k: m / np.sqrt(1 + k**2 * (1 - m**2))               # fn. 9
assert abs(rho9(3.4369) - 0.34682) < 2e-5 and abs(23.42 / 6.81 - 3.4391) < 1e-4            # GRI-2: printed k from unrounded inputs
om = rng.lognormal(np.log(0.25), 0.3, 400000); z_ = rng.standard_normal(400000)
assert abs(np.corrcoef(np.abs(om * z_), om)[0, 1] - rho9(om.mean() / om.std())) < 0.01
# eq. (1) is the regression of residual return on the score; eqs. (3)-(4) are the bivariate regression weights
T = 400000; g = rng.standard_normal(T); h = 0.35 * g + np.sqrt(1 - 0.35**2) * rng.standard_normal(T)
y = 0.0638 * g + 0.01766 * h + np.sqrt(1 - (0.0638*0.07 + 0.01766*0.04)) * rng.standard_normal(T)
assert abs(np.corrcoef(g, y)[0, 1] - 0.07) < 4e-3 and abs(np.corrcoef(h, y)[0, 1] - 0.04) < 4e-3
assert np.allclose(np.linalg.lstsq(np.c_[g, h], y, rcond=None)[0], [0.0638, 0.01766], atol=4e-3)
# averaging K standardised scores (pairwise correlation r) shrinks dispersion to sqrt((1+(K-1)r)/K): re-standardise composites
K, r = 4, 0.2; C = np.full((K, K), r) + (1 - r) * np.eye(K)
assert abs(np.sqrt(np.ones(K) @ C @ np.ones(K)) / K - np.sqrt((1 + (K - 1) * r) / K)) < 1e-12 and np.sqrt((1 + 3 * r) / 4) < 0.64
# Example 3 applied to momentum: |past return| correlates with volatility at the fn. 9 "proportional" level, so the
# volatility step applies; without it the implied per-stock skill rises with volatility
N = 20000; w_ = rng.uniform(0.15, 0.60, N); u = rng.standard_normal(N); raw = w_ * u
c_mom, c_prop = np.corrcoef(np.abs(raw), w_)[0, 1], rho9(w_.mean() / w_.std()); assert abs(c_mom - c_prop) < 0.03
lo_, hi_ = w_ < np.quantile(w_, 1/3), w_ > np.quantile(w_, 2/3)
a_raw, a_adj = 0.05 * w_ * zs(raw), 0.05 * w_ * zs(raw / w_)
assert np.std((a_raw / w_)[hi_]) > 1.8 * np.std((a_raw / w_)[lo_]) and abs(np.std((a_adj / w_)[hi_]) / np.std((a_adj / w_)[lo_]) - 1) < 0.05
# PBL EQ-MAP-2 s = c (R - Rbar) sigma^k with R - Rbar proportional to sigma: only k = 0 keeps alpha/sigma independent of sigma
cks = [np.corrcoef(np.abs((raw - raw.mean()) * w_**k / w_), w_)[0, 1] for k in (0, 1, 2)]
assert abs(cks[0]) < 0.05 and cks[1] > 0.3 and cks[2] > cks[1]

# ===== Grinold & Kahn, Advances, ch. 3 =====
n = 12; A = rng.normal(size=(n, 3 * n)); Vr = A @ A.T / (3 * n) * 0.04; al = rng.normal(0, 0.02, n); lam = 3.0
hQ = inv(Vr) @ al / (2 * lam); wQ = np.sqrt(hQ @ Vr @ hQ)
for _ in range(20):                                                                        # eqs. (35)-(37): IR_P = IR_Q x rho_PQ, any P
    hP = rng.normal(size=n) * 0.1; wP = np.sqrt(hP @ Vr @ hP); rho = (hP @ Vr @ hQ) / (wP * wQ)
    assert abs((hP @ al) / wP - (hQ @ al) / wQ * rho) < 1e-12 and abs((hQ @ al) / wQ - 2 * lam * wQ) < 1e-12
zz = rng.standard_normal(2_000_000)
assert abs(np.corrcoef(np.sign(zz), zz)[0, 1] - np.sqrt(2 / np.pi)) < 2e-3                # sign-only portfolio: TC = sqrt(2/pi) ~ 0.8
tc_keep = lambda f: np.sqrt(f + 2 * norm.ppf(1 - f / 2) * norm.pdf(norm.ppf(1 - f / 2)))  # Exhibit 11: keep the largest fraction f
for excl, val, tol in ((0.5, 0.96, 0.01), (0.8, 0.80, 0.02), (0.9, 0.66, 0.02), (0.99, 0.30, 0.02)):
    assert abs(tc_keep(1 - excl) - val) < tol
    keep = np.abs(zz) > np.quantile(np.abs(zz), excl); assert abs(np.corrcoef(zz * keep, zz)[0, 1] - tc_keep(1 - excl)) < 3e-3
for ic, br, tc_, ir in ((0.05, 2000, 0.35, 0.78), (0.1, 4, 0.6, 0.12), (0.1, 12, 0.5, 0.17), (0.08, 100, 0.9, 0.72)):
    assert abs(ic * np.sqrt(br) * tc_ - ir) < 0.005                                       # the four investment examples

# ===== Clarke, de Silva & Thorley 2002 =====
IR0 = 0.067 * np.sqrt(500); assert abs(IR0 - 1.50) < 0.005
for tc_, te, ir, er in [(0.98, 5, 1.47, 7.3), (0.73, 2, 1.09, 2.2), (0.58, 5, 0.87, 4.3), (0.48, 8, 0.72, 5.8), (0.67, 2, 1.00, 2.0),
                        (0.47, 5, 0.70, 3.5), (0.37, 8, 0.55, 4.4), (0.73, 5, 1.09, 5.5), (0.49, 5, 0.73, 3.7), (0.31, 5, 0.46, 2.3)]:
    assert abs(tc_ * IR0 - ir) < 0.006 and abs(tc_ * IR0 * te - er) < 0.06               # Table 1 follows from eq. (6) (table note)
N = 500; cap = rng.lognormal(0, 1.2, N); wB = cap / cap.sum(); sg = rng.uniform(0.15, 0.45, N); S0 = zs(rng.standard_normal(N))
alp = 0.067 * sg * S0                                                                      # eq. (9) / (A13)
def active_lo(lmb):                    # max a'dw - lmb sum dw^2 s^2, dw >= -wB, sum dw = 0 (diagonal residuals; KKT + bisection)
    f = lambda mu: np.maximum((alp - mu) / (2 * lmb * sg**2), -wB); lo, hi = -1.0, 1.0
    for _ in range(200):
        mu = (lo + hi) / 2; lo, hi = (mu, hi) if f(mu).sum() > 0 else (lo, mu)
    return f((lo + hi) / 2)
def at_te(fun, te=0.05):
    lo, hi = 1e-3, 1e4
    for _ in range(200):
        lmb = np.sqrt(lo * hi); dd = fun(lmb); lo, hi = (lmb, hi) if np.sqrt(dd**2 @ sg**2) > te else (lo, lmb)
    return fun(np.sqrt(lo * hi))
tc_of = lambda dd: np.corrcoef(dd * sg, alp / sg)[0, 1]
d_un = at_te(lambda lmb: alp / (2 * lmb * sg**2)); d_lo = at_te(active_lo)
assert tc_of(d_un) > 0.999 and 0.45 < tc_of(d_lo) < 0.70                                  # paper: 0.98 (non-diagonal Barra) and 0.58
ir_exact = (d_lo @ alp) / np.sqrt(d_lo**2 @ sg**2); assert abs(ir_exact - tc_of(d_lo) * 0.067 * np.sqrt(N)) < 0.03   # eq. (6)
dQ = alp / sg**2; tc_gk = (d_lo * sg) @ (dQ * sg) / np.sqrt((d_lo * sg) @ (d_lo * sg) * (dQ * sg) @ (dQ * sg))
assert abs(tc_gk - tc_of(d_lo)) < 0.02                                                     # G&K rho_PQ = CdST TC under the zero-mean approximation
pcs, ics = [], []
for _ in range(3000):                                                                      # eqs. (11)-(12): R^2 of PC on realised IC ~ TC^2
    rr = sg * (0.067 * S0 + np.sqrt(1 - 0.067**2) * rng.standard_normal(N))
    pcs.append(np.corrcoef(d_lo * sg, rr / sg)[0, 1]); ics.append(np.corrcoef(alp / sg, rr / sg)[0, 1])
r2 = np.corrcoef(pcs, ics)[0, 1]**2; assert abs(r2 - tc_of(d_lo)**2) < 0.05

# ===== Gallego lecture (secondary; Grinold & Kahn framework) =====
n = 7; A = rng.normal(size=(n, 3 * n)); V = A @ A.T / (3 * n) * 0.04; e = np.ones(n); q = V @ rng.uniform(0.5, 1.5, n) * 0.05
xq = inv(V) @ q / (e @ inv(V) @ q); sq2 = xq @ V @ xq; beta = V @ xq / sq2
a2 = rng.normal(0, 0.01, n); a2 = a2 - (a2 @ xq) / (beta @ xq) * beta; assert abs(a2 @ xq) < 1e-15   # benchmark alpha-neutral
xa = inv(V) @ a2 / abs(e @ inv(V) @ a2); assert abs(beta @ xa) < 1e-12                     # sec. 1.5: beta of x_alpha = 0
assert abs((a2 @ xa) / np.sqrt(xa @ V @ xa) - np.sqrt(a2 @ inv(V) @ a2)) < 1e-12            # IR = sqrt(alpha' V^-1 alpha)
tau = 2.0; ga = q + 0.01 * rng.normal(size=n); xg = inv(V) @ ga / (e @ inv(V) @ ga)          # sec. 1.4: beta_p = g_q / q_q
astar = (2 / (e @ inv(V) @ q)) * (ga @ xg) / (2 * (xg @ V @ xg)); assert abs(astar * (beta @ xg) - (ga @ xq) / (q @ xq)) < 1e-10
xe = inv(V) @ e / (e @ inv(V) @ e); be, ae = beta @ xe, a2 @ xe; xa1 = inv(V) @ a2 / (e @ inv(V) @ a2); aa1 = a2 @ xa1; bb = 0.02
swap = bb / ((1 - be) * aa1 - ae) * ((1 - be) * xa1 - xe + be * xq)                        # sec. 1.7 swap vector
Aeq = np.c_[a2, beta, e].T; assert np.allclose(swap, inv(V) @ Aeq.T @ np.linalg.solve(Aeq @ inv(V) @ Aeq.T, [bb, 0, 0]))

print("PASS S4.9 alpha sources: Grinold 1994 Exhibits 3-5 and 7 (text claims), eqs. (1)-(4) as regressions, fns. 6, 8, 9 "
      f"(GRI-1, GRI-2 rounding only); momentum |raw|-vol correlation {c_mom:.2f} vs proportional {c_prop:.2f} -> volatility step; "
      f"PBL k = 0 is the constant-IC member; G&K ch. 3 IR_P = IR_Q rho_PQ, sign-only TC sqrt(2/pi), Exhibit 11, four examples; "
      f"CdST Table 1 = eq. (6), own long-only TC {tc_of(d_lo):.2f} (paper 0.58), IR exact {ir_exact:.2f} vs law "
      f"{tc_of(d_lo) * 0.067 * np.sqrt(N):.2f}, R^2 {r2:.2f} vs TC^2 {tc_of(d_lo)**2:.2f}; Gallego secs. 1.4-1.7")
