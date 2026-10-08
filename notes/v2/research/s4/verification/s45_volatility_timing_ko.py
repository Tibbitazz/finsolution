"""S4.5 PC-A3 inverse volatility and PC-A4 inverse variance (EQ-H-3): Kirby & Ostdiek volatility timing VT(eta),
working version 9 May 2010 (JFQA 2012 governs; printed page = PDF page - 1).
  eq. (14), p. 14: w_i = (1/s_i^2)^eta / sum_j (1/s_j^2)^eta, eta >= 0;  A3 = VT(1/2), A4 = VT(1)
  eq. (12), p. 13: VT(1) = sample MV (minimum-variance) portfolio when Sigma_hat is diagonal
  eq. (13), p. 14: N = 2 MV weights and the worked example (s1 doubles: (0,1) at rho = 1/2, (1/5,4/5) at rho = 0)
  p. 14: eta = 0 -> 1/N; eta -> infinity -> all weight on the lowest-volatility asset
  eqs. (5)-(6), p. 6: turnover including the risk-free leg; compared with DGU (2009) eq. (15), p. 1929.
Also demonstrates why a near-riskless asset (cash) cannot sit inside the VT universe (decision S45-D4)."""
import numpy as np, warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008)
def vt(var, eta):                                                                          # eq. (14), computed in logs
    z = -eta * np.log(var); z -= z.max(); e = np.exp(z); return e / e.sum()

for t in range(300):
    n = int(rng.integers(2, 30)); s = rng.uniform(0.01, 0.4, n); v = s ** 2
    for eta in (0, 0.5, 1, 2, 4):
        w = vt(v, eta); assert abs(w.sum() - 1) < 1e-12 and (w > 0).all()
        assert np.allclose(vt(v * rng.uniform(0.1, 50), eta), w)                           # common rescaling (units) invariance
        p = rng.permutation(n); assert np.allclose(vt(v[p], eta), w[p])                    # permutation equivariance
        if eta > 0: assert np.all(np.diff(w[np.argsort(s)]) < 0)                          # lower volatility -> higher weight
    assert np.allclose(vt(v, 0), np.ones(n) / n)                                           # eta = 0 -> 1/N
    assert np.allclose(vt(v, 0.5), (1 / s) / (1 / s).sum())                                # A3 = inverse volatility
    assert np.allclose(vt(v, 1), (1 / v) / (1 / v).sum())                                  # A4 = inverse variance
    assert vt(v, 400)[np.argmin(s)] > 0.999 or np.sort(s)[1] / np.sort(s)[0] < 1.01        # eta -> infinity (distinct vols)
    i, j = 0, 1; assert np.isclose(vt(v, 2)[i] / vt(v, 2)[j], (v[j] / v[i]) ** 2)          # weight ratio (s_j^2/s_i^2)^eta

# eq. (12): VT(1) solves min w'Dw s.t. 1'w = 1 for diagonal D (numerical solve, independent of the closed form)
for t in range(50):
    n = int(rng.integers(2, 12)); v = rng.uniform(0.0004, 0.16, n); D = np.diag(v)
    sol = minimize(lambda w: w @ D @ w, np.ones(n) / n, jac=lambda w: 2 * D @ w, method='SLSQP',
                   constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}], options={'ftol': 1e-16}).x
    assert np.allclose(sol, vt(v, 1), atol=1e-7)
    A = rng.normal(size=(n, 2 * n)); C = A @ A.T / (2 * n); d = np.sqrt(np.diag(C))       # correlation-blindness: VT ignores
    C2 = C.copy(); C2[0, 1] = C2[1, 0] = 0.0                                               # off-diagonals of Sigma
    assert np.allclose(vt(np.diag(C), 1), vt(np.diag(C2), 1))

# A3 = equal risk contribution (PC-C2) when all pairwise correlations are equal; not otherwise
for t in range(100):
    n = int(rng.integers(2, 20)); s = rng.uniform(0.02, 0.3, n); rho = rng.uniform(-0.9 / (n - 1), 0.95)
    C = np.outer(s, s) * (rho + (1 - rho) * np.eye(n)); w = vt(s ** 2, 0.5); rc = w * (C @ w)
    assert np.allclose(rc / rc.sum(), 1 / n)
    R = np.full((n, n), rho); R[0, 1:] = R[1:, 0] = rho / 2; np.fill_diagonal(R, 1)        # one asset's correlations differ
    if n >= 3 and np.linalg.eigvalsh(R).min() > 0 and rho > 0.05:                    # n = 2 has a single correlation
        rc2 = w * ((np.outer(s, s) * R) @ w); assert not np.allclose(rc2 / rc2.sum(), 1 / n)

# eq. (13) and the worked example on p. 14
def mv2(s1, s2, rho):
    w1 = (s2 ** 2 - s1 * s2 * rho) / (s1 ** 2 + s2 ** 2 - 2 * s1 * s2 * rho); return np.array([w1, 1 - w1])
assert np.allclose(mv2(0.1, 0.1, 0.3), [0.5, 0.5])
assert np.allclose(mv2(0.2, 0.1, 0.5), [0, 1]) and np.allclose(mv2(0.2, 0.1, 0.0), [0.2, 0.8])
assert np.allclose(vt(np.array([0.04, 0.01]), 1), mv2(0.2, 0.1, 0.0))                     # VT(1) = the rho = 0 case

# turnover: KO eqs. (5)-(6) vs DGU eq. (15)
def ko_turnover(w_prev, w_new, R, rf):
    g = w_prev * (1 + R); wt = g / (g.sum() + (1 - w_prev.sum()) * (1 + rf))              # eq. (5)
    return np.abs(w_new - wt).sum() + abs((w_new - wt).sum()), wt                         # eq. (6)
for t in range(200):
    n = 8; R = rng.normal(0.005, 0.05, n); rf = 0.002
    wp = rng.dirichlet(np.ones(n)); wn = rng.dirichlet(np.ones(n))                         # fully invested: cash term is 0
    tau, wt = ko_turnover(wp, wn, R, rf); assert np.isclose(tau, np.abs(wn - wt).sum())    # = DGU eq. (15)
    wp = 0.7 * rng.dirichlet(np.ones(n)); wn = 0.9 * rng.dirichlet(np.ones(n))             # with a cash leg
    tau, wt = ko_turnover(wp, wn, R, rf); cash_t = 1 - wt.sum(); cash_n = 1 - wn.sum()
    assert np.isclose(tau, np.abs(wn - wt).sum() + abs(cash_n - cash_t))                   # = sum |dw| over N risky + cash

# cash inside the universe: a near-zero-variance asset absorbs almost all VT weight (illustrative vols, not data)
vols = np.array([0.16, 0.18, 0.06, 0.07, 0.15, 0.005])                                   # 5 risky classes + a cash-like asset
w_a3, w_a4 = vt(vols ** 2, 0.5), vt(vols ** 2, 1)
assert w_a3[-1] > 0.80 and w_a4[-1] > 0.98
print(f"PASS KO VT(eta): limits, invariants, eq. (12) = diagonal minimum variance, VT(1/2) = ERC under equal correlations, eq. (13) example (0,1) and (1/5,4/5), "
      f"turnover eq. (6) = DGU eq. (15) plus the cash leg; with a 0.5%-vol cash asset A3 puts {w_a3[-1]:.1%} and A4 {w_a4[-1]:.1%} in cash")
