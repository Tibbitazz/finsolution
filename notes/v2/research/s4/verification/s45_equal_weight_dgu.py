"""S4.5 PC-A1 equal weight (EQ-H-1): DeMiguel, Garlappi & Uppal (2009), RFS 22(5):1915-1953.
Checks: 1/N invariants; eq. (1) relative weights; Sec. 1.1 (p. 1922) 1/N = MV portfolio iff mu proportional to Sigma 1_N;
Proposition 1 (p. 1938) critical estimation windows reproduce every number stated on pp. 1939-1941 and in the abstract;
Monte Carlo check of the expected-utility terms behind eqs. (23)-(27) under DGU's distributional assumptions (p. 1937)."""
import numpy as np, warnings
from scipy.stats import wishart
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008)

# --- EQ-H-1: w = 1_N / N over the N risky assets ---
ew = lambda n: np.ones(n) / n
for n in (1, 2, 18, 500):
    w = ew(n); assert abs(w.sum() - 1) < 1e-12 and (w > 0).all() and np.allclose(w[rng.permutation(n)], w)

# --- eq. (1): relative weights w = x / |1'x| preserve the direction of x ---
x = np.array([0.4, -0.9, 0.2]); w = x / abs(x.sum()); assert np.isclose(abs(w.sum()), 1) and np.all(np.sign(w) == np.sign(x))

# --- Sec. 1.1: 1/N is the MV (tangency) portfolio iff mu = k Sigma 1_N ---
for t in range(200):
    n = int(rng.integers(2, 30)); A = rng.normal(size=(n, 2 * n)); S = A @ A.T / (2 * n) + 0.05 * np.eye(n)
    k = rng.uniform(0.1, 3); mu = k * S @ np.ones(n); x = np.linalg.solve(S, mu)
    assert np.allclose(x / x.sum(), ew(n), atol=1e-10)
    mu2 = mu + rng.normal(scale=0.1, size=n); x2 = np.linalg.solve(S, mu2)          # any other mu: not 1/N
    assert not np.allclose(x2 / x2.sum(), ew(n), atol=1e-6)

# --- Proposition 1, eqs. (23)-(27) ---
kf = lambda M, N: (M / (M - N - 2)) * (2 - M * (M - 2) / ((M - N - 1) * (M - N - 4)))   # eq. (25)
hf = lambda M, N: N * M * (M - 2) / ((M - N - 1) * (M - N - 2) * (M - N - 4))          # eq. (27)
def crit(N, Sp, Sew, case):                                                               # eq. (22)
    for M in range(N + 5, 10 ** 6):
        v = {1: Sp ** 2 - Sew ** 2 - N / M, 2: kf(M, N) * Sp ** 2 - Sew ** 2,
             3: kf(M, N) * Sp ** 2 - Sew ** 2 - hf(M, N)}[case]
        if v > 0: return M
assert all(kf(M, 25) < 1 for M in range(40, 5000))                                       # k < 1 (eq. 25)
panel = {'A': (.40, .20), 'B': (.40, .10), 'C': (.20, .10), 'D': (.20, .05), 'E': (.15, .12), 'F': (.15, .08)}
# (panel, N, relation, months) as stated in the text, case 3 (mu and Sigma unknown); monthly Sharpe ratios
claims = [('A', 25, '>', 200), ('A', 50, '~', 600), ('A', 100, '>', 1200),              # p. 1939
          ('B', 25, '=', 270), ('B', 50, '=', 530), ('B', 100, '=', 1060),               # p. 1940
          ('C', 25, '~', 1000), ('C', 50, '~', 2000), ('D', 50, '>', 1500),              # p. 1941
          ('E', 25, '>', 3000), ('E', 50, '>', 6000), ('F', 25, '>', 1600), ('F', 50, '>', 3200),
          ('E', 25, '~', 3000), ('E', 50, '~', 6000)]                                    # abstract ("around", "about")
got = {}
for p, N, rel, m in claims:
    c = got.setdefault((p, N), crit(N, *panel[p], 3))
    ok = {'>': c > m, '~': abs(c / m - 1) <= 0.10, '=': abs(c / m - 1) <= 0.01}[rel]
    assert ok, (p, N, rel, m, c)
for p in panel:                                                                           # Figure 1 ordering of the three cases
    for N in (10, 25, 50, 100):
        c1, c2, c3 = (crit(N, *panel[p], c) for c in (1, 2, 3)); assert c3 > max(c1, c2)

# --- Monte Carlo: E[U(x_hat)] terms behind Proposition 1 ---
# mu_hat ~ N(mu, Sigma/M), M Sigma_hat ~ W(M-1, Sigma), independent (p. 1937); U(x) = x'mu - (gamma/2) x'Sigma x (eq. 18)
N, M, gam, R = 3, 60, 1.0, 400_000
A = rng.normal(size=(N, N)); Sig = A @ A.T + np.eye(N); mu = rng.uniform(0.05, 0.3, N) * np.sqrt(np.diag(Sig))
S2 = mu @ np.linalg.solve(Sig, mu); Sew2 = mu.sum() ** 2 / Sig.sum()
L = np.linalg.cholesky(Sig); muh = mu + (rng.normal(size=(R, N)) @ L.T) / np.sqrt(M)
Sh = wishart(df=M - 1, scale=Sig).rvs(size=R, random_state=rng) / M
U = lambda X: X @ mu - gam / 2 * np.einsum('ri,ij,rj->r', X, Sig, X)
x1 = np.linalg.solve(Sig, muh.T).T / gam                                                 # case 1: Sigma known
x2 = np.linalg.solve(Sh, np.broadcast_to(mu, (R, N))[..., None])[..., 0] / gam            # case 2: mu known
x3 = np.linalg.solve(Sh, muh[..., None])[..., 0] / gam                                    # case 3: both estimated
for X, theory in ((x1, (S2 - N / M) / (2 * gam)), (x2, kf(M, N) * S2 / (2 * gam)),
                  (x3, (kf(M, N) * S2 - hf(M, N)) / (2 * gam))):
    u = U(X); se = u.std() / np.sqrt(R); assert abs(u.mean() - theory) < 4 * se, (u.mean(), theory, se)
xew = (mu.sum() / Sig.sum()) * np.ones(N) / gam                                           # optimally scaled 1/N
assert np.isclose(U(xew[None])[0], Sew2 / (2 * gam))                                      # => L_ew = (S+^2 - S_ew^2) / (2 gamma)
print("PASS DGU: 1/N invariants; mu ~ Sigma 1 optimality; Proposition 1 reproduces all 15 stated critical windows "
      f"(e.g. panel B {got[('B', 25)]}/{got[('B', 50)]}/{got[('B', 100)]} vs 270/530/1060; panel E {got[('E', 25)]}/{got[('E', 50)]}); "
      "Monte Carlo confirms the case 1-3 expected-utility terms")
