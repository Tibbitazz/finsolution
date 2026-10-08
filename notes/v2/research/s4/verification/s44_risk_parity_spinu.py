"""S4.4 source reproduction: Spinu (2013) Theorem 3.4 (Newton with damped phase) for C x = b / x,
plus the Maillard-Roncalli-Teiletche ordering sigma(long-only MV) <= sigma(ERC) <= sigma(1/N)."""
import numpy as np, warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
def spinu(C, b, tol=1e-6, maxit=500):
    d = np.sqrt(np.diag(C)); R = C / np.outer(d, d); bb = b / b.min()          # eqs. (8), (10)
    x = np.sqrt(bb.sum()) / np.sqrt(R.sum()) * np.ones(len(b)); lam_star = 0.95 * (3 - np.sqrt(5)) / 2
    for it in range(maxit):
        u = R @ x - bb / x; dx = np.linalg.solve(R + np.diag(bb / x ** 2), u); lam = np.sqrt(u @ dx)
        if lam > lam_star: x = x - dx / (1 + np.max(np.abs(dx / x)))           # damped phase, eq. (20)
        elif lam > tol: x = x - dx                                             # quadratic phase
        else: break
    y = x / d; return y / y.sum(), it
rng = np.random.default_rng(20261008); worst = 0; steps = []
for t in range(500):
    n = 50; A = rng.normal(size=(n, 2 * n)); C = A @ A.T / (2 * n); b = rng.uniform(size=n); b /= b.sum()
    w, it = spinu(C, b); rc = w * (C @ w) / (w @ C @ w); worst = max(worst, np.max(np.abs(rc - b) / b)); steps.append(it)
assert worst < 1e-5 and max(steps) < 16                                      # paper: < 16 iterations at N = 50
viol = 0
for t in range(300):
    n = 10; A = rng.normal(size=(n, 3 * n)); sc = rng.uniform(.5, 2, n); C = A @ A.T / (3 * n) * np.outer(sc, sc)
    erc, _ = spinu(C, np.ones(n) / n); ew = np.ones(n) / n
    mv = minimize(lambda v: v @ C @ v, ew, jac=lambda v: 2 * C @ v, bounds=[(0, 1)] * n,
                  constraints=[{'type': 'eq', 'fun': lambda v: v.sum() - 1}], method='SLSQP', options={'ftol': 1e-15}).x
    s = lambda v: np.sqrt(v @ C @ v); viol += not (s(mv) <= s(erc) + 1e-9 and s(erc) <= s(ew) + 1e-9)
assert viol == 0
print(f"PASS Spinu: budgets met (max rel. error {worst:.1e}), max {max(steps)} iterations at N=50; MRT volatility ordering holds")
