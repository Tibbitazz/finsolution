"""S4.5 PC-A2 market-cap weight (EQ-H-2). Governing citation: Sharpe (1964), JF 19(3):425-442.
Sharpe gives no weighting rule: the capital market line (Part III) and E(R_i) = P + B_ig [E(R_g) - P] for any efficient
combination g (fns. 22, 25, 26, pp. 438-441). Checks here:
  (1) cap-weight invariants;
  (2) cap weights are self-financing between issuance events: drifted weights equal the next cap weights, so turnover is 0;
  (3) reverse optimisation: if excess returns are mu = lam * Sigma w_m, the tangency portfolio is w_m (the identity behind
      Black-Litterman's Pi = delta Sigma w_mkt, verified at S4.4);
  (4) Sharpe's linear relation holds with g = the tangency portfolio and B_ig the regression slope cov(R_i, R_g)/var(R_g)."""
import numpy as np, warnings
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008)
cap_w = lambda cap: cap / cap.sum()                                                      # EQ-H-2

# (1) invariants: sum 1, positive, invariant to the currency unit of capitalisation, permutation-equivariant
cap = rng.lognormal(3, 1.2, 18); w = cap_w(cap)
assert abs(w.sum() - 1) < 1e-12 and (w > 0).all() and np.allclose(cap_w(7.3 * cap), w)
p = rng.permutation(18); assert np.allclose(cap_w(cap[p]), w[p])

# (2) buy-and-hold: shares fixed, prices move -> cap weights at t+1 equal the drifted weights (DGU eq. 15, w_{t+}); turnover 0
shares = rng.uniform(1, 5, 18); price = rng.uniform(10, 100, 18); turn = []
for t in range(120):
    w_t = cap_w(shares * price); r = rng.normal(0.006, 0.05, 18); price = price * (1 + r)
    w_drift = w_t * (1 + r) / (w_t * (1 + r)).sum(); w_next = cap_w(shares * price)
    turn.append(np.abs(w_next - w_drift).sum())
assert max(turn) < 1e-12
j = np.argmax(w_next); shares[j] *= 1.10                                                  # an issuance event forces trading
w_iss = cap_w(shares * price); g = 0.10 * w_next[j]                                       # exact: |dw| sum = 2 g (1 - w_j) / (1 + g)
assert np.isclose(np.abs(w_iss - w_next).sum(), 2 * g * (1 - w_next[j]) / (1 + g)) and g > 0.01

# (3) reverse optimisation and (4) Sharpe's linear relation
for t in range(200):
    n = int(rng.integers(2, 25)); A = rng.normal(size=(n, 2 * n)); S = A @ A.T / (2 * n) + 0.02 * np.eye(n)
    wm = cap_w(rng.lognormal(0, 1, n)); lam = rng.uniform(1, 5); mu = lam * S @ wm       # mu = excess returns over P
    x = np.linalg.solve(S, mu); assert np.allclose(x / x.sum(), wm, atol=1e-10)          # tangency = w_m
    beta = S @ wm / (wm @ S @ wm); mu_m = wm @ mu
    assert np.allclose(mu, beta * mu_m, atol=1e-12)                                       # E(R_i) - P = B_im [E(R_m) - P]
print("PASS market cap: invariants; zero turnover between issuance events; tangency = w_m when mu = lam Sigma w_m; "
      "Sharpe (1964) linear relation in B_im holds")
