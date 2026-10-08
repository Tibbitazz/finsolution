"""S4.4 source reproduction: Idzorek (draft of 26 Apr 2005), Tables 4, 6, 7 and the confidence method (sec. 3.2).
Also verifies the closed form omega_k = (1-C_k)/C_k * tau * p_k Sigma p_k' against the paper's numerical step 6."""
import numpy as np
from scipy.optimize import minimize_scalar
Sig = np.array([
 [0.001005, 0.001328, -0.000579, -0.000675, 0.000121, 0.000128, -0.000445, -0.000437],
 [0.001328, 0.007277, -0.001307, -0.000610, -0.002237, -0.000989, 0.001442, -0.001535],
 [-0.000579, -0.001307, 0.059852, 0.027588, 0.063497, 0.023036, 0.032967, 0.048039],
 [-0.000675, -0.000610, 0.027588, 0.029609, 0.026572, 0.021465, 0.020697, 0.029854],
 [0.000121, -0.002237, 0.063497, 0.026572, 0.102488, 0.042744, 0.039943, 0.065994],
 [0.000128, -0.000989, 0.023036, 0.021465, 0.042744, 0.032056, 0.019881, 0.032235],
 [-0.000445, 0.001442, 0.032967, 0.020697, 0.039943, 0.019881, 0.028355, 0.035064],
 [-0.000437, -0.001535, 0.048039, 0.029854, 0.065994, 0.032235, 0.035064, 0.079958]])   # Table 5
wm = np.array([19.34, 26.13, 12.09, 12.09, 1.34, 1.34, 24.18, 3.49]) / 100
Pi_pub = np.array([0.08, 0.67, 6.41, 4.08, 7.43, 3.70, 4.80, 6.60]) / 100
s = Sig @ wm; lam = (Pi_pub @ s) / (s @ s); Pi = lam * s                  # eq. (1); lambda implied (~3.07)
assert abs(lam - 3.07) < 0.01
P = np.array([[0, 0, 0, 0, 0, 0, 1, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, 0, .9, -.9, .1, -.1, 0, 0]]); Q = np.array([.0525, .0025, .02]); tau = .025
assert np.allclose(100 * np.diag(P @ Sig @ P.T), [2.836, 0.563, 3.462], atol=2e-3)        # Table 4
def post(P, Q, Om):
    A = np.linalg.inv(tau * Sig) + P.T @ np.linalg.inv(Om) @ P
    return np.linalg.solve(A, np.linalg.inv(tau * Sig) @ Pi + P.T @ np.linalg.inv(Om) @ Q)   # eq. (3)
ER = post(P, Q, np.diag(tau * np.diag(P @ Sig @ P.T))); w = np.linalg.solve(lam * Sig, ER)  # eq. (2): uses Sigma
assert np.allclose(100 * ER, [0.07, 0.50, 6.50, 4.32, 7.59, 3.94, 4.93, 6.84], atol=0.01)
assert np.allclose(100 * w, [29.88, 15.59, 9.35, 14.82, 1.04, 1.65, 27.81, 3.49], atol=0.02)
ER100 = Pi + tau * Sig @ P.T @ np.linalg.solve(P @ (tau * Sig) @ P.T, Q - P @ Pi); w100 = np.linalg.solve(lam * Sig, ER100)  # eq. (9)
assert np.allclose(100 * w100, [43.82, 1.65, 3.81, 20.37, 0.42, 2.26, 35.21, 3.49], atol=0.02)
ic = (w - wm)[:7] / (w100 - wm)[:7]
assert np.allclose(100 * ic, [43.06, 43.06, 33.02, 33.02, 33.02, 33.02, 32.94], atol=0.05)   # Table 7
for k, C in enumerate([.25, .50, .65]):                                   # sec. 3.2, steps 1-6, per view
    p = P[k:k + 1]; q = Q[k:k + 1]
    D = np.linalg.solve(lam * Sig, Pi + tau * Sig @ p.T @ np.linalg.solve(p @ (tau * Sig) @ p.T, q - p @ Pi)) - wm
    target = wm + C * D * (np.abs(p[0]) > 0)
    wk = lambda om: np.linalg.solve(lam * Sig, post(p, q, np.array([[om]])))
    r = minimize_scalar(lambda lo: np.sum((target - wk(np.exp(lo))) ** 2), bounds=(-30, 5), method='bounded', options={'xatol': 1e-12})
    closed = (1 - C) / C * tau * (p @ Sig @ p.T)[0, 0]
    assert abs(np.exp(r.x) / closed - 1) < 1e-6
print("PASS Idzorek: lambda, Tables 4/6/7, and closed-form omega = (1-C)/C * tau * p Sigma p' (equals step-6 search)")
