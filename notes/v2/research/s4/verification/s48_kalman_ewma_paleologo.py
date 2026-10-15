"""Paleologo (2025), The Elements of Quantitative Investing, Wiley, 1st ed. (ISBN 9781394265466; owner upload, epub).
SOURCE VERIFICATION ONLY. Chapter 2 sec. 2.3 (pp. 40-45) and App. 2.4 (pp. 46-51): Kalman filter, Muth (1960) model,
mean-reverting (AR(1)) state; chapter 5 sec. 5.1.1 (p. 96) volatility losses; chapter 6 pp. 122-126 exponential weights.
Findings PAL-1 ... PAL-8 are recorded in ANG_ISSUES_REGISTER.md. Synthetic data only. Prints PASS.

Notation: state x_{t+1} = mu + a (x_t - mu) + tau_e eps;  observation y_t = x_t + tau_h eta;  Q = tau_e^2, R = tau_h^2,
kappa = tau_h / tau_e (book p. 42), P = stationary predicted variance (book: sigma-hat^2_{t+1|t}), K = P / (P + R) (gain)."""
import numpy as np

rng = np.random.default_rng(20261015)


def riccati(a, Q, R, it=20000):                       # predicted-variance recursion of App. 2.4 with A = a, B = 1
    P = Q
    for _ in range(it):
        P = a * a * P * R / (P + R) + Q
    return P


# 1. Muth model (Ex. 2.1, pp. 42 and 49): closed form, gain, and steady-state Kalman = EWMA
for kap in (0.5, 1.0, 3.0, 10.0, 30.0):
    Q, R = 1.0, kap ** 2
    P = riccati(1.0, Q, R)
    assert abs(P - Q * (1 + np.sqrt((2 * kap) ** 2 + 1)) / 2) < 1e-9 * P           # book's closed form
    q = Q / R
    assert abs(P / (P + R) - (-q + np.sqrt(q * q + 4 * q)) / 2) < 1e-12              # gain in signal-to-noise form
for q in (0.001, 0.01, 0.1):                                                         # filter from a diffuse start vs EWMA
    K = (-q + np.sqrt(q * q + 4 * q)) / 2
    y = np.cumsum(rng.standard_normal(4000) * np.sqrt(q)) + rng.standard_normal(4000)
    x, P, e, dmax = 0.0, 1e6, y[0], 0.0
    for t, yt in enumerate(y):
        Pp = P + q; Kt = Pp / (Pp + 1); x += Kt * (yt - x); P = (1 - Kt) * Pp
        e += K * (yt - e)
        if t > 1000: dmax = max(dmax, abs(x - e))
    assert dmax < 1e-6

# 2. PAL-5: the kappa >> 1 approximation K ~ 1/(1 + kappa) (pp. 42, 49) has relative error ~ 1/(2 kappa)
K10 = riccati(1.0, 1.0, 100.0); K10 = K10 / (K10 + 100.0)
assert 0.04 < abs(1 / 11 - K10) / K10 < 0.05 and abs(1 / 10.5 - K10) / K10 < 0.002

# 3. Mean-reverting state (Ex. 2.2, pp. 49-51)
def P_root(a, Q, R):                                  # middle line of the book's solution (correct)
    c = (a * a - 1) * R + Q
    return (c + np.sqrt(c * c + 4 * Q * R)) / 2
def P_factored(a, Q, R):                              # last line of the book's solution
    k = np.sqrt(R / Q); D = (a * a - 1) * k * k + 1
    return 0.5 * Q * D * (1 + np.sqrt(1 + (2 * k / D) ** 2))
for a, kap in ((0.9, 1.0), (0.9, 2.0), (0.9, 5.0), (0.98, 10.0), (0.5, 3.0)):
    Q, R = 1.0, kap ** 2
    P = riccati(a, Q, R)
    assert abs(P - P_root(a, Q, R)) < 1e-9 * P
    if (1 - a * a) * kap * kap < 1:
        assert abs(P - P_factored(a, Q, R)) < 1e-9 * P
    else:
        assert P_factored(a, Q, R) < 0                # PAL-2: factored form fails when (1 - a^2) kappa^2 > 1
grid = [0.5, 0.7, 0.9, 0.99, 1.0]
Ps = [riccati(a, 1.0, 4.0) for a in grid]
assert all(np.diff(Ps) > 0) and all(np.diff([P / (P + 4.0) for P in Ps]) > 0)        # PAL-3: increasing in a

# 4. PAL-1: the printed recursion x_{t+1|t} = (1-K) x_{t|t-1} + K y_t omits the time update A = a (eq. 2.33).
#    Correct steady state: x_{t+1|t} = (1-a) mu + a(1-K) x_{t|t-1} + aK y_t, i.e. GARCH(1,1) form, alpha + beta = a.
T, mu = 120000, 1.0
for a, kap, min_excess in ((0.95, 1.0, 0.02), (0.90, 3.0, 0.10), (0.98, 5.0, 0.03)):
    Q = 0.01; R = kap ** 2 * Q
    x = np.empty(T); x[0] = mu
    eps = rng.standard_normal(T); eta = rng.standard_normal(T)
    for t in range(1, T):
        x[t] = mu + a * (x[t - 1] - mu) + np.sqrt(Q) * eps[t]
    y = x + np.sqrt(R) * eta
    P = riccati(a, Q, R); K = P / (P + R)
    om, be, al = (1 - a) * mu, a * (1 - K), a * K
    assert abs(al + be - a) < 1e-15
    c = b = mu; ec = eb = 0.0; n = 0
    for t in range(T - 1):
        c = om + be * c + al * y[t]                   # correct filter (prediction of x_{t+1})
        b = (1 - K) * b + K * y[t]                    # printed recursion
        if t > 2000:
            ec += (c - x[t + 1]) ** 2; eb += (b - x[t + 1]) ** 2; n += 1
    assert abs(ec / n / P - 1) < 0.05                 # correct filter attains the Riccati variance
    assert eb / ec - 1 > min_excess                   # printed recursion is worse

# 5. PAL-4: p. 44 gives tau_e^2/(2 lam - lam^2) as the stationary standard deviation; it is the variance (p. 49 correct)
lam, te = 0.1, 0.1; xs = np.empty(400000); xs[0] = 0.0; z = rng.standard_normal(400000)
for t in range(1, len(xs)):
    xs[t] = (1 - lam) * xs[t - 1] + te * z[t]
assert abs(xs[1000:].std() / (te / np.sqrt(2 * lam - lam ** 2)) - 1) < 0.03
assert abs(xs[1000:].var() / (te ** 2 / (2 * lam - lam ** 2)) - 1) < 0.06

# 6. PAL-6: ch. 5 p. 96 prints MSE = (1/T) sum sigma_hat^2 (r^2/sigma_hat^2 - 1)^2; under r ~ N(0, h) its expected value
#    (m4 - 2 m2 f + f^2)/f is minimised at f = sqrt(m4) = sqrt(3) h. True MSE (sigma_hat^4 weight) and QLIKE: f = m2 = h.
h = 1.0; r2 = h * rng.standard_normal(4_000_000) ** 2
m2, m4 = r2.mean(), (r2 ** 2).mean()
assert abs(np.sqrt(m4) / h - np.sqrt(3)) < 0.01 and abs(m2 / h - 1) < 0.005
fs = np.linspace(0.5, 2.5, 2001); r2s = r2[:200000]
printed = [np.mean(f * (r2s / f - 1) ** 2) for f in fs]
true_mse = [np.mean((r2s - f) ** 2) for f in fs]
qlike = [np.mean(r2s / f - np.log(r2s / f) - 1) for f in fs]
assert abs(fs[int(np.argmin(printed))] - np.sqrt(3)) < 0.03
assert abs(fs[int(np.argmin(true_mse))] - 1) < 0.02 and abs(fs[int(np.argmin(qlike))] - 1) < 0.02

# 7. PAL-7: weights exp(-s/tau) (ch. 6) have half-life tau*ln 2, not tau; ch. 2 fn. a defines tau = -log 2 / log K
tau = 126.0
assert abs(np.exp(-(tau * np.log(2)) / tau) - 0.5) < 1e-15 and abs(-np.log(2) / np.log(np.exp(-1 / tau)) - tau * np.log(2)) < 1e-9

# 8. PAL-8: K is the decay (weight on the past) in eq. (2.20) and Insight 2.2, but the gain (weight on the new
#    observation) in the Kalman recursions. Half-life from the gain uses log(1 - K_gain), not log(K_gain).
Kg = (-0.01 + np.sqrt(0.01 ** 2 + 4 * 0.01)) / 2
hl_right, hl_wrong = -np.log(2) / np.log(1 - Kg), -np.log(2) / np.log(Kg)
assert abs(hl_right - 6.93) < 0.01 and hl_wrong < 0.3

print("PASS Paleologo ch. 2/5/6 (Kalman, EWMA, losses): Muth closed form and gain; steady-state Kalman = EWMA; "
      "AR(1) Riccati root; PAL-1 (time update omitted; correct form = GARCH(1,1) recursion), PAL-2 (factored root "
      "negative when (1-a^2)k^2 > 1), PAL-3 (P increasing in a), PAL-4 (variance, not s.d.), PAL-5 (1/(1+k) "
      "approximation), PAL-6 (printed MSE minimised at sqrt(3) h), PAL-7 (exp(-s/tau) half-life = tau ln 2), "
      "PAL-8 (K decay vs gain)")
