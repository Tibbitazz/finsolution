"""S4.7 PC-B3 robust mean-variance: Goldfarb & Iyengar (2003), Math. Oper. Res. 28(1):1-38 (published, JSTOR). Synthetic data.
Model (1)-(4), pp. 3-4: r = mu + V'f + eps, f ~ N(0, F), eps ~ N(0, D); S_d: d_i in [d_lo, d_hi]; S_v: V = V0 + W with
||W_i||_G <= rho_i; S_m: mu = mu0 + zeta, |zeta_i| <= gamma_i.
  eq. (15): worst-case mean = mu0'phi - gamma'|phi|;  worst-case residual variance = phi' D_hi phi
  Lemma 1 / eq. (26), pp. 8-9: max_{||y||_G <= r} ||y0 + y||_F^2 = min_{0 < s < 1/lmax(H)} r^2/s + sum w_i^2/(1 - s l_i),
      H = G^-1/2 F G^-1/2 = Q diag(l) Q', w = Q' H^1/2 G^1/2 y0, y0 = V0 phi, r = rho'|phi|
  eqs. (64)-(68), pp. 19-20: if F = kappa G, worst-case factor st.dev. = ||F^1/2 V0 phi|| + sqrt(kappa) rho'|phi|
  eqs. (31)-(32), p. 11: robust minimum variance (here solved with the exact worst-case objective; long-only, p. 11)
  eqs. (61)-(63), pp. 17-18: uncertainty sets from regression confidence regions (coverage checked by simulation)."""
import numpy as np, warnings
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import f as fdist
from itertools import product
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008)
def msqrt(M):
    e, U = np.linalg.eigh(M); return U @ np.diag(np.sqrt(e)) @ U.T
def wc_factor(y0, r, F, G):                                                                # Lemma 1, eq. (26)
    Gh = msqrt(G); Gih = np.linalg.inv(Gh); H = Gih @ F @ Gih; l, Q = np.linalg.eigh(H)
    w = Q.T @ msqrt(H) @ Gh @ y0
    if r == 0: return w @ w
    g = lambda s: r ** 2 / s + np.sum(w ** 2 / (1 - s * l))
    res = minimize_scalar(g, bounds=(1e-12, (1 - 1e-12) / l.max()), method='bounded', options={'xatol': 1e-14})
    return res.fun
def brute_factor(y0, r, F, G, starts=60):                                                  # maximise over the ellipsoid boundary
    m = len(y0); Gih = np.linalg.inv(msqrt(G)); best = -np.inf
    f = lambda u: -(y0 + r * Gih @ u) @ F @ (y0 + r * Gih @ u)
    for k in range(starts):
        u0 = rng.normal(size=m); u0 /= np.linalg.norm(u0)
        u = minimize(f, u0, method='SLSQP', constraints=[{'type': 'eq', 'fun': lambda u: u @ u - 1}], options={'ftol': 1e-15}).x
        best = max(best, -f(u))
    return best

# eq. (15): worst-case mean by vertex enumeration
for t in range(20):
    n = 6; mu0 = rng.normal(0.05, 0.02, n); gam = rng.uniform(0, 0.02, n); phi = rng.normal(size=n)
    vert = min((mu0 + np.array(sg) * gam) @ phi for sg in product((-1, 1), repeat=n))
    assert np.isclose(vert, mu0 @ phi - gam @ np.abs(phi))
# Lemma 1 against brute force; F = kappa G special case (eqs. 64-67); {W phi} = {y : ||y||_G <= rho'|phi|}
for t in range(25):
    m = 3; A = rng.normal(size=(m, m)); F = A @ A.T + 0.1 * np.eye(m); B = rng.normal(size=(m, m)); G = B @ B.T + 0.1 * np.eye(m)
    y0 = rng.normal(size=m); r = rng.uniform(0.1, 2)
    assert np.isclose(wc_factor(y0, r, F, G), brute_factor(y0, r, F, G), rtol=1e-6)
    kap = rng.uniform(0.2, 3); Fk = kap * G
    closed = (np.linalg.norm(msqrt(Fk) @ y0) + np.sqrt(kap) * r) ** 2
    assert np.isclose(wc_factor(y0, r, Fk, G), closed, rtol=1e-6) and np.isclose(brute_factor(y0, r, Fk, G), closed, rtol=1e-6)
    n = 5; phi = rng.normal(size=n); rho = rng.uniform(0.1, 1, n); Gih = np.linalg.inv(msqrt(G))
    u = rng.normal(size=m); u /= np.linalg.norm(u); W = np.column_stack([np.sign(phi[i]) * rho[i] * Gih @ u for i in range(n)])
    assert np.isclose(np.sqrt((W @ phi) @ G @ (W @ phi)), rho @ np.abs(phi))               # the bound rho'|phi| is attained

# robust minimum variance (31)-(32), long-only, with the exact worst-case objective
def robust_mv(mu0, gam, V0, F, G, rho, dhi, alpha):
    obj = lambda p: wc_factor(V0 @ p, rho @ p, F, G) + p @ np.diag(dhi) @ p
    cons = [{'type': 'eq', 'fun': lambda p: p.sum() - 1}, {'type': 'ineq', 'fun': lambda p: (mu0 - gam) @ p - alpha}]
    n = len(mu0); best = None
    for x0 in [np.ones(n) / n] + [rng.dirichlet(np.ones(n)) for _ in range(3)]:
        r_ = minimize(obj, x0, method='SLSQP', bounds=[(0, 1)] * n, constraints=cons, options={'ftol': 1e-14, 'maxiter': 500})
        if r_.success and (best is None or r_.fun < best.fun): best = r_
    return best.x, best.fun, obj
for t in range(8):
    n, m = 6, 2; V0 = rng.normal(0.5, 0.3, (m, n)); Fh = rng.normal(size=(m, m)); F = Fh @ Fh.T * 0.002 + 0.001 * np.eye(m); G = F / 0.01
    d = rng.uniform(0.001, 0.004, n); mu0 = rng.uniform(0.04, 0.10, n); alpha = 0.05
    # (a) no uncertainty: robust = classical Markowitz problem (5)
    p0, v0, _ = robust_mv(mu0, np.zeros(n), V0, F, G, np.zeros(n), d, alpha)
    S = V0.T @ F @ V0 + np.diag(d)
    pc = minimize(lambda p: p @ S @ p, np.ones(n) / n, method='SLSQP', bounds=[(0, 1)] * n, options={'ftol': 1e-15},
                  constraints=[{'type': 'eq', 'fun': lambda p: p.sum() - 1}, {'type': 'ineq', 'fun': lambda p: mu0 @ p - alpha}]).x
    assert np.allclose(p0, pc, atol=2e-4)
    # (b) with uncertainty: the worst case is a valid and attained bound; the robust optimum beats the classical portfolio's worst case
    gam = rng.uniform(0, 0.01, n); rho = rng.uniform(0.01, 0.2, n); dhi = d * 1.5
    pr, vr, obj = robust_mv(mu0, gam, V0, F, G, rho, dhi, alpha)
    Gih = np.linalg.inv(msqrt(G)); worst_seen = 0
    for k in range(2000):
        u = rng.normal(size=m); u /= np.linalg.norm(u); W = np.column_stack([rho[i] * rng.uniform(0, 1) * Gih @ u for i in range(n)])
        V = V0 + W; dd = rng.uniform(d, dhi); worst_seen = max(worst_seen, pr @ (V.T @ F @ V + np.diag(dd)) @ pr)
    assert worst_seen <= vr * (1 + 1e-6)
    if (mu0 - gam) @ pc >= alpha: assert vr <= obj(pc) + 1e-12

# robust maximum Sharpe (35)-(37), p. 12: homogenised = min worst-case variance s.t. (mu0 - gamma - rf 1)'phi >= 1, phi >= 0
n_ms = 0
for t in range(6):
    n, m = 6, 2; V0 = rng.normal(0.5, 0.3, (m, n)); Fh = rng.normal(size=(m, m)); F = Fh @ Fh.T * 0.002 + 0.001 * np.eye(m); G = F / 0.01
    d = rng.uniform(0.001, 0.004, n); dhi = 1.5 * d; mu0 = rng.uniform(0.04, 0.10, n); gam = rng.uniform(0, 0.01, n)
    rho = rng.uniform(0.01, 0.2, n); rf = 0.03
    wcv = lambda p: wc_factor(V0 @ p, rho @ p, F, G) + p @ np.diag(dhi) @ p
    hom = minimize(wcv, np.ones(n) * 5, method='SLSQP', bounds=[(0, None)] * n, options={'ftol': 1e-15, 'maxiter': 1000},
                   constraints=[{'type': 'ineq', 'fun': lambda p: (mu0 - gam - rf) @ p - 1}]).x
    p_h = hom / hom.sum(); wsr = lambda p: ((mu0 - gam) @ p - rf) / np.sqrt(wcv(p))
    p_d = max((minimize(lambda p: -wsr(p), x0, method='SLSQP', bounds=[(0, 1)] * n, options={'ftol': 1e-14},
                        constraints=[{'type': 'eq', 'fun': lambda p: p.sum() - 1}]).x
               for x0 in [np.ones(n) / n] + [rng.dirichlet(np.ones(n)) for _ in range(4)]), key=wsr)
    assert wsr(p_h) >= wsr(p_d) - 1e-6 and np.allclose(p_h, p_d, atol=2e-3); n_ms += 1

# eqs. (61)-(63): regression confidence regions have the stated coverage (simulation)
p, m, n, om, R = 120, 2, 4, 0.95, 4000
Bf = rng.normal(0, 0.04, (m, p)); Aan = np.vstack([np.ones(p), Bf]).T; AtAi = np.linalg.inv(Aan.T @ Aan)
Q = np.hstack([np.zeros((m, 1)), np.eye(m)]); Gr = np.linalg.inv(Q @ AtAi @ Q.T)
mu_t = rng.uniform(0.002, 0.01, n); V_t = rng.normal(0.8, 0.3, (m, n)); sig = rng.uniform(0.01, 0.03, n)
c1, cm = fdist.ppf(om, 1, p - m - 1), fdist.ppf(om, m, p - m - 1); hit_mu = hit_v = 0
for k in range(R):
    Y = mu_t + Bf.T @ V_t + rng.normal(size=(p, n)) * sig                                   # p x n asset returns
    X = AtAi @ Aan.T @ Y; res = Y - Aan @ X; s2 = (res ** 2).sum(0) / (p - m - 1)
    gam_i = np.sqrt(AtAi[0, 0] * c1 * s2); rho_i = np.sqrt(m * cm * s2)
    hit_mu += np.sum(np.abs(X[0] - mu_t) <= gam_i)
    hit_v += np.sum([np.sqrt((X[1:, i] - V_t[:, i]) @ Gr @ (X[1:, i] - V_t[:, i])) <= rho_i[i] for i in range(n)])
cov_mu, cov_v = hit_mu / (R * n), hit_v / (R * n); se = np.sqrt(om * (1 - om) / (R * n))
assert abs(cov_mu - om) < 4 * se and abs(cov_v - om) < 4 * se
print(f"PASS robust MV: eq. (15) by vertex enumeration; Lemma 1 worst-case factor variance = brute force; F = kappa G "
      f"closed form (66)-(67); attainment of rho'|phi|; robust min variance = Markowitz at zero uncertainty, worst case valid "
      f"and better than the classical portfolio's; robust max Sharpe homogenisation = direct ({n_ms} cases); regression-set coverage {cov_mu:.3f} / {cov_v:.3f} vs {om}")
