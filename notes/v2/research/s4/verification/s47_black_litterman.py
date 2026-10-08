"""S4.7 PC-B2 Black-Litterman: Black & Litterman (1992), FAJ 48(5):28-43, Appendix (p. 42) and text (p. 35). Synthetic data.
  item 6: Pi = delta Sigma W;  item 7: E[R] ~ prior centred on Pi with covariance tau Sigma; views P E[R] = Q + eps, eps ~ N(0, Omega),
  Omega diagonal;  item 8: E[R]bar = [(tau Sigma)^-1 + P' Omega^-1 P]^-1 [(tau Sigma)^-1 Pi + P' Omega^-1 Q]
  (printed with an unbalanced parenthesis, "(tau Sigma^-1 Pi"; BL-2). p. 35: with 100% confidence the conditional mean is
  Pi + tau Sigma P' [P tau Sigma P']^-1 [Q - P Pi].  He & Litterman and Idzorek conventions were reproduced at S4.4
  (verification/s44_black_litterman_*.py); the P = I special case equals PBL's Bayesian EPO (s47_epo_pbl.py)."""
import numpy as np, warnings
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261008); inv = np.linalg.inv
def bl(Pi, S, tau, P, Q, Om):
    return inv(inv(tau * S) + P.T @ inv(Om) @ P) @ (inv(tau * S) @ Pi + P.T @ inv(Om) @ Q)
for t in range(100):
    n = int(rng.integers(3, 10)); k = int(rng.integers(1, n)); A = rng.normal(size=(n, 2 * n)); S = A @ A.T / (2 * n) * 0.03
    W = rng.dirichlet(np.ones(n)); delta = rng.uniform(1.5, 4); Pi = delta * S @ W; tau = rng.uniform(0.01, 0.1)
    P = rng.normal(size=(k, n)); Q = P @ Pi + rng.normal(0, 0.02, k); Om = np.diag(rng.uniform(1e-4, 1e-2, k))
    # item 6 + reverse optimisation: holding Pi with Sigma and delta returns the market weights (BL Table VII logic)
    assert np.allclose(inv(delta * S) @ Pi, W)
    # no views (Omega -> infinity) gives Pi; views equal to Pi's implication leave Pi unchanged
    assert np.allclose(bl(Pi, S, tau, P, Q, Om * 1e12), Pi, atol=1e-10)
    assert np.allclose(bl(Pi, S, tau, P, P @ Pi, Om), Pi)
    # 100% confidence (Omega -> 0) gives the p. 35 conditional mean, which satisfies the views exactly
    upd = lambda O: Pi + tau * S @ P.T @ inv(P @ (tau * S) @ P.T + O) @ (Q - P @ Pi)          # equivalent update form
    assert np.allclose(upd(Om), bl(Pi, S, tau, P, Q, Om))                                    # = item 8 (Woodbury)
    cm = Pi + tau * S @ P.T @ inv(P @ (tau * S) @ P.T) @ (Q - P @ Pi)
    assert np.allclose(upd(np.zeros((k, k))), cm) and np.allclose(P @ cm, Q)                 # Omega = 0: p. 35 formula, views exact
    assert np.linalg.norm(upd(Om * 1e-6) - cm) < np.linalg.norm(upd(Om) - cm)                # continuity toward the limit
    # BL-2: the literal reading tau * Sigma^-1 * Pi fails the no-view limit (gives tau^2 Pi), so the intended term is (tau Sigma)^-1 Pi
    literal = inv(inv(tau * S) + P.T @ inv(Om * 1e12) @ P) @ (tau * inv(S) @ Pi + P.T @ inv(Om * 1e12) @ Q)
    assert np.allclose(literal, tau ** 2 * Pi, atol=1e-10) and not np.allclose(literal, Pi)
    # with Omega proportional to tau (He-Litterman tau diag(P S P'); Idzorek (1-C)/C tau p S p'), tau cancels from the posterior mean
    Om0 = np.diag(np.diag(P @ S @ P.T)) * rng.uniform(0.3, 3)
    assert np.allclose(bl(Pi, S, 0.01, P, Q, 0.01 * Om0), bl(Pi, S, 0.2, P, Q, 0.2 * Om0))
    C = rng.uniform(0.1, 0.95); p1 = P[:1]; om1 = lambda tau_: np.array([[(1 - C) / C * tau_ * (p1 @ S @ p1.T)[0, 0]]])
    assert np.allclose(bl(Pi, S, 0.01, p1, Q[:1], om1(0.01)), bl(Pi, S, 0.3, p1, Q[:1], om1(0.3)))
print("PASS Black-Litterman 1992: Pi = delta Sigma W reverses to W; no-view and consistent-view limits; 100%-confidence limit = "
      "p. 35 conditional mean (views hold exactly); the printed '(tau Sigma^-1 Pi' read literally gives tau^2 Pi (BL-2); tau cancels when Omega is proportional to tau")
