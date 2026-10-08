"""S4.4 source reproduction: Boudt, Carl & Peterson (version of 24 May 2012): modified CVaR (Appendix eqs. 21-22),
the I^q terms, the Gaussian limit (eq. 7), Euler allocation (eq. 3), Proposition (15), and MCC (eq. 10) vs ERC (eq. 11)."""
import numpy as np, warnings
from scipy.stats import norm
from scipy.integrate import quad
from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
def Iq(q, g):   # as printed (identical to the PerformanceAnalytics routine)
    if q % 2 == 0:
        p = q // 2; full = np.prod([2 * j for j in range(1, p + 1)]); I = full * norm.pdf(g)
        for i in range(1, p + 1): I += full / np.prod([2 * j for j in range(1, i + 1)]) * g ** (2 * i) * norm.pdf(g)
    else:
        p = (q - 1) // 2; full = np.prod([2 * j + 1 for j in range(p + 1)]); I = -full * norm.cdf(g)
        for i in range(p + 1): I += full / np.prod([2 * j + 1 for j in range(i + 1)]) * g ** (2 * i + 1) * norm.pdf(g)
    return I
for q in (1, 2, 3, 4, 6):   # identity: I^q = -int_{-inf}^g u^(q+1) phi(u) du  (Edgeworth/Hermite construction)
    assert abs(Iq(q, -1.7) + quad(lambda u: u ** (q + 1) * norm.pdf(u), -np.inf, -1.7)[0]) < 1e-9
def mcvar(w, mu, S, M3, M4, a=.05):
    m2 = w @ S @ w; s = w @ M3 @ np.kron(w, w) / m2 ** 1.5; k = w @ M4 @ np.kron(np.kron(w, w), w) / m2 ** 2 - 3
    z = norm.ppf(a); g = z + (z ** 2 - 1) * s / 6 + (z ** 3 - 3 * z) * k / 24 - (2 * z ** 3 - 5 * z) * s ** 2 / 36   # eq. (21)
    d = (norm.pdf(g) + (Iq(4, g) - 6 * Iq(2, g) + 3 * norm.pdf(g)) * k / 24 + (Iq(3, g) - 3 * Iq(1, g)) * s / 6
         + (Iq(6, g) - 15 * Iq(4, g) + 45 * Iq(2, g) - 15 * norm.pdf(g)) * s ** 2 / 72) / a
    return -w @ mu + np.sqrt(m2) * d                                                                               # eq. (22)
rng = np.random.default_rng(20261008); N, T = 4, 5000
X = rng.standard_t(5, size=(T, N)) * np.array([.01, .03, .04, .05]); X[:, 2] -= 0.012 * np.abs(rng.normal(size=T))
mu = X.mean(0); C = X - mu; S = C.T @ C / T
M3 = np.einsum('ti,tj,tk->ijk', C, C, C).reshape(N, N * N) / T; M4 = np.einsum('ti,tj,tk,tl->ijkl', C, C, C, C).reshape(N, N ** 3) / T
w = np.array([.4, .3, .2, .1]); gauss4 = (np.einsum('ij,kl->ijkl', S, S) + np.einsum('ik,jl->ijkl', S, S) + np.einsum('il,jk->ijkl', S, S)).reshape(N, N ** 3)
assert abs(mcvar(w, mu, S, np.zeros((N, N * N)), gauss4) - (-w @ mu + np.sqrt(w @ S @ w) * norm.pdf(norm.ppf(.05)) / .05)) < 1e-12
f = lambda v: mcvar(v, mu, S, M3, M4); h = 1e-6
comps = lambda v: v * np.array([(f(v + h * e) - f(v - h * e)) / (2 * h) for e in np.eye(N)])
assert abs(comps(w).sum() - f(w)) < 1e-8                                                                            # Euler, eq. (3)
gc = lambda v: -v @ mu + np.sqrt(v @ S @ v) * norm.pdf(norm.ppf(.05)) / .05
v = minimize(gc, np.ones(N) / N, constraints=[{'type': 'eq', 'fun': lambda v: v.sum() - 1}], method='SLSQP', options={'ftol': 1e-14}).x
pc = v * (-mu + (S @ v) / np.sqrt(v @ S @ v) * norm.pdf(norm.ppf(.05)) / .05) / gc(v); assert np.allclose(pc, v, atol=1e-5)   # Prop. (15)
best = None
for _ in range(20):
    r = minimize(lambda v: np.max(comps(v)), rng.dirichlet(np.ones(N)), bounds=[(0, 1)] * N,
                 constraints=[{'type': 'eq', 'fun': lambda v: v.sum() - 1}], method='SLSQP')
    best = r if best is None or r.fun < best.fun else best
print(f"PASS Boudt-Carl-Peterson: I^q identity, Gaussian limit, Euler, Prop.(15); MCC % contributions {(comps(best.x) / f(best.x)).round(3)}")
