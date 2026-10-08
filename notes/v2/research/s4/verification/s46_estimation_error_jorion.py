"""S4.6 estimation error (EQ-MVO-E1): Jorion (1986), JFQA 21(3):279-292, reproduced from Table 1 (p. 287).
  Table 1 efficient-set statistics c, b, Y0, a, d(Y0) from the printed means and covariance matrix (7 countries, %/month)
  eq. (14)-(15), p. 285: E[r] = (1-w) Ybar + w 1 Y0, Y0 = GMV mean; V[r] = S(1 + 1/(T+lam)) + lam/(T(T+1+lam)) 11'/(1'S^-1 1)
  eq. (16)-(18), p. 286: diffuse prior; w_hat = (N+2)/((N+2) + T d_hat); Sigma_hat = (T-1)/(T-N-2) S
  Table 2, p. 288: empirical risk (F_MAX - F_bar)/|F_MAX| of four estimators and the shrinkage factor's mean and SD
Conventions that reproduce Table 2 (recorded as INFERENCE): negative exponential utility with risk tolerance
52.2%/12 per month (A = 12/52.2 per %), weights summing to one, eq. (18) scaling in both the diffuse and Bayes-Stein rules,
lam_hat = T w_hat / (1 - w_hat). The certainty-equivalence column at T = 25 is too heavy-tailed to test and is skipped."""
import numpy as np, warnings
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
mu = np.array([1.287, 1.096, 0.501, 1.524, 0.763, 1.854, 0.620])
low = [[42.18], [20.18, 70.89], [10.88, 21.58, 25.51], [5.30, 15.41, 9.60, 22.33], [12.32, 23.24, 22.63, 10.32, 30.01],
       [23.84, 23.80, 13.22, 10.46, 16.36, 42.23], [17.41, 12.62, 4.70, 1.00, 7.20, 9.90, 16.42]]
N = 7; S = np.zeros((N, N))
for i, r in enumerate(low):
    for j, v in enumerate(r): S[i, j] = S[j, i] = v
one = np.ones(N); Si = np.linalg.inv(S)
c, b, a = one @ Si @ one, mu @ Si @ one, mu @ Si @ mu; Y0 = b / c; d = (mu - Y0) @ Si @ (mu - Y0)
for got, pub, tol in ((c, 0.11838, 5e-5), (b, 0.0953, 5e-5), (Y0, 0.805, 5e-4), (a, 0.15849, 5e-5), (d, 0.08171, 1e-4)):
    assert abs(got - pub) <= tol, (got, pub)                                              # Table 1, rounding of printed inputs

A = 12 / 52.2                                                                              # per % per month
def qopt(m, V):                                                                            # max m'q - A/2 q'Vq s.t. 1'q = 1
    Vi = np.linalg.inv(V); g = Vi @ one / (one @ Vi @ one); P = Vi - np.outer(Vi @ one, Vi @ one) / (one @ Vi @ one)
    return g + P @ m / A
e = lambda q: np.exp(-A * (q @ mu - A / 2 * q @ S @ q))                                    # -F, under the true parameters
eMAX = e(qopt(mu, S)); assert abs(eMAX - 0.99734) < 1e-4                                   # Table 2 note: F_MAX = 0.99734

Lc = np.linalg.cholesky(S); rng = np.random.default_rng(20261008); K = 4000
table2 = {25: (None, 0.3452, 0.1337, 0.1815, 0.5883, 0.1564), 50: (0.1578, 0.1137, 0.0762, 0.0722, 0.5199, 0.1386),
          100: (0.0569, 0.0493, 0.0577, 0.0375, 0.4275, 0.1221), 200: (0.0253, 0.0236, 0.0484, 0.0205, 0.3164, 0.0906)}
for T, pub in table2.items():
    E = {k: [] for k in ('CE', 'DP', 'MV', 'BS')}; W = []
    for k in range(K):
        Y = mu + rng.standard_normal((T, N)) @ Lc.T; Yb = Y.mean(0); Sm = np.cov(Y, rowvar=False)
        Sh = (T - 1) / (T - N - 2) * Sm; Shi = np.linalg.inv(Sh)                           # eq. (18)
        E['CE'].append(e(qopt(Yb, Sm)))                                                    # certainty equivalence
        E['DP'].append(e(qopt(Yb, Sh * (1 + 1 / T))))                                      # diffuse prior, eq. (16)
        g = Shi @ one / (one @ Shi @ one); E['MV'].append(e(g))                            # minimum variance (w = 1)
        y0 = g @ Yb; dv = Yb - y0; w = (N + 2) / ((N + 2) + T * dv @ Shi @ dv); lam = T * w / (1 - w)   # eq. (17)
        V = Sh * (1 + 1 / (T + lam)) + lam / (T * (T + 1 + lam)) * np.outer(one, one) / (one @ Shi @ one)  # eq. (15)
        E['BS'].append(e(qopt((1 - w) * Yb + w * y0, V))); W.append(w)                     # eq. (14)
    risk = {k: (np.mean(v) - eMAX) / eMAX for k, v in E.items()}
    se_pub = {k: np.std(v) / np.sqrt(1000) / eMAX for k, v in E.items()}                   # the paper used K = 1000
    for k, p in zip(('CE', 'DP', 'MV', 'BS'), pub[:4]):
        if p is not None: assert abs(risk[k] - p) <= 3 * se_pub[k] + 0.03 * p, (T, k, risk[k], p)
    assert abs(np.mean(W) - pub[4]) <= 3 * np.std(W) / np.sqrt(1000) and abs(np.std(W) / pub[5] - 1) < 0.10
    if T >= 50: assert risk['BS'] < risk['DP'] < risk['CE']                                # p. 288: BS below CE and DP; DP below CE
    if T == 200: assert risk['MV'] > max(risk['BS'], risk['DP'], risk['CE'])               # MV dominated for large samples
    if T == 50: assert risk['MV'] < risk['DP'] < risk['CE']
print(f"PASS Jorion: Table 1 statistics; F_MAX {eMAX:.5f} (0.99734); Table 2 risk functions and shrinkage factors at "
      f"T = 25/50/100/200 within the paper's Monte Carlo error; orderings as stated on p. 288")
