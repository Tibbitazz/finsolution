"""S4.4 source reproduction: He & Litterman (1999; GSAM working paper, 2002 copy), Tables 2 and 4-8.
Own implementation of eqs. (2), (8), (9), (13), (17), (18). Published inputs (Tables 1-2) are rounded, so
tolerances are 0.1 pp (returns), 0.3 pp (weights) and 0.02 (Lambda). Not production code."""
import numpy as np
lower = [[.488], [.478, .664], [.515, .655, .861], [.439, .310, .355, .354],
         [.512, .608, .783, .777, .405], [.491, .779, .668, .653, .306, .652]]
R = np.eye(7)
for i, row in enumerate(lower, 1):
    for j, v in enumerate(row): R[i, j] = R[j, i] = v
sig = np.array([16.0, 20.3, 24.8, 27.1, 21.0, 20.0, 18.7]) / 100      # AUS CAN FRA GER JPN UK USA
weq = np.array([1.6, 2.2, 5.2, 5.5, 11.6, 12.4, 61.5]) / 100
Sig = np.outer(sig, sig) * R; delta, tau = 2.5, 0.05
Pi = delta * Sig @ weq                                                   # eq. (2)
assert np.allclose(100 * Pi, [3.9, 6.9, 8.4, 9.0, 4.3, 6.8, 7.6], atol=0.05)
def bl(P, Q, om_tau):
    Om = np.diag(np.array(om_tau) * tau); Oi = np.linalg.inv(Om); Ti = np.linalg.inv(tau * Sig)
    Minv = np.linalg.inv(Ti + P.T @ Oi @ P)                              # eq. (9)
    mu = Minv @ (Ti @ Pi + P.T @ Oi @ np.array(Q))                       # eq. (8)
    w = np.linalg.solve(delta * (Sig + Minv), mu)                        # eq. (13), posterior covariance
    A = Om / tau + P @ Sig @ P.T / (1 + tau); Ai = np.linalg.inv(A); q = tau * Oi @ np.array(Q) / delta
    Lam = q - Ai @ P @ Sig / (1 + tau) @ weq - Ai @ P @ Sig / (1 + tau) @ P.T @ q     # eq. (18)
    assert np.allclose(w, (weq + P.T @ Lam) / (1 + tau))                 # eq. (17) == eq. (13)
    return mu, w, Lam
v1 = np.array([0, 0, -.295, 1, 0, -.705, 0]); v2 = np.array([0, 1, 0, 0, 0, 0, -1]); v3 = np.array([0, 1, 0, 0, -1, 0, 0])
# Recovered convention: the published omega/tau equal the view-portfolio variances p' Sigma p
assert np.allclose([v @ Sig @ v for v in (v1, v2, v3)], [.021, .017, .059], atol=6e-4)
cases = {'T4': ([v1], [.05], [.021], [4.3, 7.6, 9.3, 11.0, 4.5, 7.0, 8.1], [1.5, 2.1, -4.0, 35.4, 11.0, -9.5, 58.6], None),
         'T5': ([v1, v2], [.05, .03], [.021, .017], [4.4, 8.7, 9.5, 11.2, 4.6, 7.0, 7.5], [1.5, 41.9, -3.4, 33.6, 11.0, -8.2, 18.8], [.298, .418]),
         'T6': ([v1, v2], [.05, .04], [.021, .017], [4.4, 9.1, 9.5, 11.3, 4.6, 7.0, 7.3], [1.5, 53.3, -3.3, 33.1, 11.0, -7.8, 7.3], [.292, .538]),
         'T7': ([v1, v2], [.05, .04], [.043, .017], [4.3, 8.9, 9.3, 10.6, 4.6, 6.9, 7.2], [1.5, 53.9, -0.5, 23.6, 11.0, -1.1, 6.8], [.193, .544]),
         'T8': ([v1, v2, v3], [.05, .04, .0412], [.043, .017, .059], [4.3, 8.9, 9.3, 10.6, 4.6, 6.9, 7.2], [1.5, 53.9, -0.5, 23.6, 11.0, -1.1, 6.8], [.193, .544, .0])}
for k, (P, Q, ot, mu_p, w_p, lam_p) in cases.items():
    mu, w, Lam = bl(np.array(P), Q, ot)
    assert np.abs(100 * mu - mu_p).max() < 0.1 and np.abs(100 * w - w_p).max() < 0.3, k
    if lam_p is not None: assert np.abs(Lam - lam_p).max() < 0.02, k
# Table 4 text reports 0.302, which is Lambda/(1+tau) (HL-1); Tables 5-8 report Lambda
mu, w, Lam = bl(np.array([v1]), [.05], [.021]); assert abs(Lam[0] / (1 + tau) - .302) < .005
print("PASS He & Litterman: Pi, Tables 4-8, eq.(17)=eq.(13), Omega = tau*diag(P Sigma P'), Property 3.1 (lambda_3 = 0)")
