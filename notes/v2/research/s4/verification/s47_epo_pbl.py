"""S4.7 PC-B6 Simple EPO and PC-B7 Anchored EPO: Pedersen, Babu & Levine (2021), FAJ 77(2):124-151 (published version,
open access; equations read from the rendered pages). Synthetic data only.
  eqs. (3), (5)-(8), pp. 128-129: MVO and the problem portfolios (principal components of the correlation matrix)
  eqs. (9)-(11), p. 130: shrinking PC variances = shrinking correlations; simple EPO with a shrunk risk matrix
  Prop. 1, eqs. (12)-(14), pp. 130-131: Bayesian anchor; Prop. 2, eqs. (15)-(16), p. 131: robust optimisation
  eqs. (17)-(22), pp. 132-133: general, simple and anchored EPO; Prop. 3, p. 133; proof pp. 147-148 (BL, Tikhonov, Lavrentiev)
  eq. (23) and (27), pp. 136-137: fully shrunk EPO with TSMOM-type signals = equal-volatility weights
Plus the constrained variant used by the engine (V1): the same quadratic objective with Policy Statement constraints."""
import numpy as np, warnings
from scipy.optimize import minimize, minimize_scalar
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008)
def problem(n):
    A = rng.normal(size=(n, 2 * n)); C = A @ A.T / (2 * n); d = np.sqrt(np.diag(C))
    Om = C / np.outer(d, d); sig = rng.uniform(0.05, 0.3, n); S = np.outer(sig, sig) * Om
    s = rng.normal(0, 0.03, n); return S, Om, sig, s
inv = np.linalg.inv
for t in range(60):
    n = int(rng.integers(3, 15)); S, Om, sig, s = problem(n); V = np.diag(sig ** 2); g = rng.uniform(1, 10); one = np.ones(n)
    # eqs. (5)-(8): PC portfolios of unit-volatility assets; z = D^-1 s_P / gamma; same portfolio as eq. (3)
    D, P = np.linalg.eigh(Om); sP = P.T @ (s / sig); z = sP / D / g
    assert np.allclose((P @ z) / sig, inv(S) @ s / g)
    assert np.allclose(z, (sP / np.sqrt(D)) * (1 / np.sqrt(D)) / g)                       # Sharpe x leverage, eq. (8)
    # eqs. (9)-(10): shrinking PC variances toward 1 = multiplying all correlations by 1 - theta
    th = rng.uniform(0, 1); Omt = P @ np.diag((1 - th) * D + th) @ P.T
    assert np.allclose(Omt, (1 - th) * Om + th * np.eye(n))
    off = ~np.eye(n, dtype=bool); assert np.allclose(Omt[off], (1 - th) * Om[off])
    St = np.outer(sig, sig) * Omt                                                          # Sigma~ = sigma Omega~ sigma
    # Prop. 1, eq. (13): Gaussian conditioning with prior mu ~ N(gamma S a, tau S) and s | mu ~ N(mu, Lambda)
    a = rng.dirichlet(np.ones(n)); tau = rng.uniform(0.05, 2); B = rng.normal(size=(n, n)); Lam = B @ B.T / n * 0.001 + 1e-4 * np.eye(n)
    post = g * S @ a + tau * S @ inv(tau * S + Lam) @ (s - g * S @ a)                      # standard conditional mean
    assert np.allclose(post, S @ inv(tau * S + Lam) @ (tau * s + g * Lam @ a))             # eq. (13)
    x14 = inv(tau * S + Lam) @ (tau * s + g * Lam @ a) / g
    assert np.allclose(x14, inv(S) @ post / g)                                             # eq. (14) = MVO on E(mu|s)
    # Prop. 3 part 3 / proof p. 148: Black-Litterman posterior with Pi = gamma S a, Q = s, P = I, Omega = Lambda
    bl = inv(inv(tau * S) + inv(Lam)) @ (inv(tau * S) @ (g * S @ a) + inv(Lam) @ s)
    assert np.allclose(bl, post)
    # Prop. 3 parts 1-2: Lambda -> 0 gives MVO; tau -> 0 gives the anchor (reverse MVO)
    assert np.allclose(inv(tau * S + 1e-12 * np.eye(n)) @ (tau * s) / g, inv(S) @ s / g, rtol=1e-6)
    assert np.allclose(inv(1e-12 * S + Lam) @ (1e-12 * s + g * Lam @ a) / g, a, atol=1e-8)
    # eqs. (17)-(19): Lambda = lam V, w = lam / (tau + lam)
    lam = rng.uniform(0.01, 3); w = lam / (tau + lam)
    x17 = inv(tau * St + lam * V) @ (tau * s + g * lam * V @ a) / g
    Sw = (1 - w) * St + w * V; x18 = inv(Sw) @ ((1 - w) * s / g + w * V @ a)
    assert np.allclose(x17, x18) and np.allclose(Sw, np.outer(sig, sig) * ((1 - w) * Omt + w * np.eye(n)))
    # effective correlation shrinkage of theta then w: correlations times (1 - theta)(1 - w)
    Rw = Sw / np.outer(sig, sig); assert np.allclose(Rw[off], (1 - th) * (1 - w) * Om[off])
    # eq. (20): simple EPO = eq. (18) with anchor a = V^-1 s / gamma; limits w = 0 (MVO on Sigma~) and w = 1 (V^-1 s / gamma)
    xs = inv(Sw) @ s / g; assert np.allclose(xs, inv(Sw) @ ((1 - w) * s / g + w * V @ (inv(V) @ s / g)))
    assert np.allclose(inv(St) @ s / g, inv((1 - 0) * St + 0 * V) @ s / g)
    assert np.allclose(inv(1e-15 * St + (1 - 1e-15) * V) @ s / g, s / sig ** 2 / g)
    # simple EPO is linear in 1/gamma: Sharpe ratio independent of gamma (p. 132)
    shp = lambda x: x @ s / np.sqrt(x @ S @ x); assert np.isclose(shp(inv(Sw) @ s / 2), shp(inv(Sw) @ s / 9))
    # Prop. 3 part 5: Tikhonov (S + lam V)^-1 s / gamma is proportional to simple EPO with w = lam / (1 + lam)
    xt = inv(St + lam * V) @ s / g; ws = lam / (1 + lam); xw = inv((1 - ws) * St + ws * V) @ s / g
    assert np.allclose(xt * (1 + lam), xw)
    # Lavrentiev: (S + Lambda/tau)^-1 (s/gamma + Lambda a / tau) = general EPO (17)
    assert np.allclose(inv(St + lam * V / tau) @ (s / g + lam * V @ a / tau), x17)
    # eqs. (21)-(22): anchored EPO; gamma equalises the Sigma~-variance of Sw^-1 s / gamma and of the anchor
    gA = np.sqrt(s @ inv(Sw) @ St @ inv(Sw) @ s) / np.sqrt(a @ St @ a); comp = inv(Sw) @ s / gA
    assert np.isclose(comp @ St @ comp, a @ St @ a)
    x22 = inv(Sw) @ ((1 - w) * np.sqrt(a @ St @ a) / np.sqrt(s @ inv(Sw) @ St @ inv(Sw) @ s) * s + w * V @ a)
    assert np.allclose(x22, inv(Sw) @ ((1 - w) * s / gA + w * V @ a))
    assert np.allclose(inv(V) @ (V @ a), a)                                                # w = 1: anchored EPO = anchor
    x0 = inv(St) @ s * np.sqrt(a @ St @ a) / np.sqrt(s @ inv(St) @ s)                    # w = 0: MVO scaled to anchor risk
    assert np.isclose(x0 @ St @ x0, a @ St @ a)

# Prop. 2, eqs. (15)-(16): max_x min_{mu in ellipsoid} (x-a)'mu - g/2 x'Sx = (x-a)'s - c sqrt((x-a)'L(x-a)) - g/2 x'Sx.
# For c < c* = sqrt((s - g S a)' L^-1 (s - g S a)) the solution equals eq. (16) for some tau(c) in (0, inf); for c >= c*
# the kink at x = a is optimal (subgradient condition) and the solution is the anchor itself, i.e. tau = 0 (PBL-1)
n_lo = n_hi = 0
for t in range(12):
    n = 6; S, Om, sig, s = problem(n); g = 3.0; a = rng.dirichlet(np.ones(n)); B = rng.normal(size=(n, n)); L = B @ B.T * 0.0005 + 1e-4 * np.eye(n)
    v = s - g * S @ a; cstar = np.sqrt(v @ inv(L) @ v)
    for c in (0.3, 1.0, 3.0, 1.2 * cstar):
        f = lambda x: -((x - a) @ s - c * np.sqrt((x - a) @ L @ (x - a) + 1e-30) - g / 2 * x @ S @ x)
        xr = min((minimize(f, x0, method='BFGS', options={'gtol': 1e-13, 'maxiter': 10000})
                  for x0 in (inv(S) @ s / g, a + 1e-3 * rng.normal(size=n))), key=lambda r: r.fun).x
        if c < cstar:
            x16 = lambda tau: inv(tau * S + L) @ (tau * s + g * L @ a) / g
            res = minimize_scalar(lambda lt: np.sum((x16(np.exp(lt)) - xr) ** 2), bounds=(-30, 8), method='bounded', options={'xatol': 1e-12})
            assert np.sqrt(res.fun) < 1e-6 * max(1, np.linalg.norm(xr)), (c, cstar, np.sqrt(res.fun)); n_lo += 1
        else:
            assert f(a) <= f(xr) + 1e-9 and np.linalg.norm(xr - a) < 1e-4; n_hi += 1   # anchor optimal
assert n_lo >= 30 and n_hi >= 12

# eq. (23) and (27): TSMOM-type signal s_i = 0.1 sigma_i sign(r_i): the fully shrunk EPO is equal-volatility weighted
n = 20; S, Om, sig, s = problem(n); sgn = np.sign(rng.normal(size=n)); s = 0.1 * sig * sgn; g = n / 0.40
x1 = s / sig ** 2 / g; assert np.allclose(np.abs(x1) * sig, 0.1 / g)                      # equal risk weight per asset
assert np.allclose(np.abs(x1) / np.abs(x1).sum(), (1 / sig) / (1 / sig).sum())            # = inverse volatility (PC-A3) in size

# V1 (engine): constrained EPO = max x'm_w - 1/2 x'S_w x with m_w = (1-w) s/g + w V a, under Policy Statement constraints
for t in range(20):
    n = 8; S, Om, sig, s = problem(n); V = np.diag(sig ** 2); g = 4.0; a = np.ones(n) / n; w = rng.uniform(0.1, 0.9)
    Sw = (1 - w) * S + w * V; m = (1 - w) * s / g + w * V @ a
    xu = minimize(lambda x: -(x @ m - 0.5 * x @ Sw @ x), np.zeros(n), method='BFGS', options={'gtol': 1e-12}).x
    assert np.allclose(xu, inv(Sw) @ m, atol=1e-6)                                         # unconstrained optimum = eq. (18)
    xc = minimize(lambda x: -(x @ m - 0.5 * x @ Sw @ x), a, method='SLSQP', bounds=[(0, 0.3)] * n,
                  constraints=[{'type': 'ineq', 'fun': lambda x: 1 - x.sum()}], options={'ftol': 1e-15}).x
    grad = m - Sw @ xc; free = (xc > 1e-7) & (xc < 0.3 - 1e-7)                            # KKT: equal gradient on free assets
    if free.sum() >= 2 and xc.sum() > 1 - 1e-7: assert np.ptp(grad[free]) < 1e-5
    if free.sum() >= 1 and xc.sum() < 1 - 1e-6: assert np.abs(grad[free]).max() < 1e-5
print("PASS EPO: problem portfolios (eqs. 5-8); PC-variance shrinkage = correlation shrinkage (9-10); Prop. 1 posterior "
      "and Prop. 3 BL / MVO / reverse-MVO / Tikhonov / Lavrentiev equivalences; eqs. (17)-(22) and limits; Prop. 2 robust "
      f"solution = eq. (16) for c < c* ({n_lo} cases) and = anchor for c >= c* ({n_hi} cases, PBL-1); fully shrunk TSMOM EPO = equal-volatility weights; constrained V1 KKT")
