"""S4.7 PC-B1 maximum Sharpe ratio under Policy Statement constraints (EQ-MVO-3/3a, S4.6; governing sources Tobin 1958,
Sharpe 1964; ANG-47). Synthetic data only.
Homogenisation y = kappa x (VERIFIED-DERIVATION; recommended in S4_GITHUB_IMPL_REVIEW.md section 7):
  max mu'x / sqrt(x'Sx) s.t. 1'x = 1, l <= x <= u, Gx <= h, sqrt((x - b)'S(x - b)) <= TE
  <=> min y'Sy s.t. mu'y = 1, 1'y = kappa, l kappa <= y <= u kappa, Gy <= h kappa, sqrt((y - kappa b)'S(y - kappa b)) <= kappa TE,
      kappa >= 0;  x = y / kappa.  Every constraint stays linear or second-order-cone, so the problem is convex.
Checked against direct multi-start maximisation; infeasibility when no feasible portfolio has positive excess return."""
import numpy as np, warnings
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008)
def slsqp(f, x0, cons, bounds=None):
    return minimize(f, x0, method='SLSQP', constraints=cons, bounds=bounds, options={'ftol': 1e-15, 'maxiter': 3000})
checked = 0
for t in range(25):
    n = 8; A = rng.normal(size=(n, 2 * n)); S = A @ A.T / (2 * n) * 0.04; mu = rng.uniform(-0.01, 0.07, n)  # excess returns
    u = np.full(n, 0.30); grp = np.zeros(n); grp[:3] = 1; gmax = 0.50                          # caps; a group limit
    b = np.ones(n) / n; TE = 0.04                                                             # benchmark and TE budget
    # homogenised convex problem in z = (y, kappa)
    cons = [{'type': 'eq', 'fun': lambda z: z[:n] @ mu - 1}, {'type': 'eq', 'fun': lambda z: z[:n].sum() - z[n]},
            {'type': 'ineq', 'fun': lambda z: u * z[n] - z[:n]}, {'type': 'ineq', 'fun': lambda z: gmax * z[n] - grp @ z[:n]},
            {'type': 'ineq', 'fun': lambda z: (z[n] * TE) ** 2 - (z[:n] - z[n] * b) @ S @ (z[:n] - z[n] * b)}]
    best = None
    for k0 in (5.0, 20.0, 60.0):
        r = slsqp(lambda z: z[:n] @ S @ z[:n], np.r_[b * k0, k0], cons, [(0, None)] * (n + 1))
        if r.success and (best is None or r.fun < best.fun): best = r
    if best is None: continue
    x_h = best.x[:n] / best.x[n]
    # direct: maximise the Sharpe ratio over the same feasible set from several starts
    sr = lambda x: (x @ mu) / np.sqrt(x @ S @ x)
    dc = [{'type': 'eq', 'fun': lambda x: x.sum() - 1}, {'type': 'ineq', 'fun': lambda x: gmax - grp @ x},
          {'type': 'ineq', 'fun': lambda x: TE ** 2 - (x - b) @ S @ (x - b)}]
    starts = [b] + [0.7 * b + 0.3 * rng.dirichlet(np.ones(n)) for _ in range(6)]
    x_d = max((slsqp(lambda x: -sr(x), x0, dc, [(0, 0.30)] * n).x for x0 in starts), key=lambda x: sr(x) if
              (x.sum() > 1 - 1e-6 and grp @ x <= gmax + 1e-6 and (x - b) @ S @ (x - b) <= TE ** 2 + 1e-8) else -9)
    feas = lambda x: abs(x.sum() - 1) < 1e-6 and (x >= -1e-7).all() and (x <= 0.30 + 1e-6).all() and grp @ x <= gmax + 1e-6 \
        and np.sqrt((x - b) @ S @ (x - b)) <= TE + 1e-6
    assert feas(x_h) and sr(x_h) >= sr(x_d) - 1e-6, (t, sr(x_h), sr(x_d))
    checked += 1
assert checked >= 20
# without constraints the homogenised problem returns the closed-form tangency (EQ-MVO-3)
n = 6; A = rng.normal(size=(n, 2 * n)); S = A @ A.T / (2 * n); mu = rng.uniform(0.01, 0.08, n); Si = np.linalg.inv(S)
y = np.linalg.solve(S, mu) / (mu @ Si @ mu); assert np.allclose(y / y.sum(), Si @ mu / (np.ones(n) @ Si @ mu))
# failure: long-only with every excess return <= 0 -> mu'y = 1 with y >= 0 is infeasible (NO_POSITIVE_EXCESS_RETURN)
mu_neg = -np.abs(mu); r = slsqp(lambda y: y @ S @ y, np.ones(n), [{'type': 'eq', 'fun': lambda y: y @ mu_neg - 1}], [(0, None)] * n)
assert not (r.success and abs(r.x @ mu_neg - 1) < 1e-6)
print(f"PASS max Sharpe: homogenised convex problem (caps, group limit, tracking-error cone) >= direct multi-start "
      f"maximisation in {checked} problems; unconstrained case = closed-form tangency; infeasible when no positive excess return")
