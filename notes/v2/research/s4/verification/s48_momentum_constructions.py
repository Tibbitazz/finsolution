"""S4.8 momentum signal constructions (SIG-1 XSMOM, SIG-2 TSMOM, variants per S4_PLAN amendment 19).
Governing: Jegadeesh & Titman 1993 (JT); Moskowitz, Ooi & Pedersen 2012 (MOP); Asness, Moskowitz & Pedersen 2013 (AMP);
Hurst, Ooi & Pedersen 2017 (HOP); Daniel & Moskowitz 2016 (DM); Barroso & Santa-Clara 2015 (B&SC).
Variants: Blitz, Huij & Martens 2011 (BHM); Gupta & Kelly 2019 (G&K); Ehsani & Linnainmaa 2019 NBER (E&L).
Link: Pedersen, Babu & Levine 2021 (PBL) eqs. (23)-(27). SPECIFICATION VERIFICATION ONLY; synthetic data; prints PASS."""
import numpy as np, warnings
from scipy.stats import rankdata
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS

rng = np.random.default_rng(20261015)

# 1. JT sec. I (p. 68): J/K strategy with overlapping cohorts. Return = average of the K active cohorts'
#    returns = return of the aggregated weights; each month 1/K of the book is replaced.
N, T, J, K = 50, 120, 6, 6
R = rng.normal(0.01, 0.08, (T, N))
def jt_cohort(t, skip=0):                      # formed at the start of month t from months t-J-skip .. t-1-skip
    past = np.prod(1 + R[t - J - skip:t - skip], axis=0) - 1
    order, n10 = np.argsort(past), N // 10
    w = np.zeros(N); w[order[-n10:]] = 1 / n10; w[order[:n10]] = -1 / n10
    return w
for t in range(J + K + 1, T):
    coh = [jt_cohort(t - k) for k in range(K)]
    w_t = np.mean(coh, axis=0)
    assert abs(np.mean([c @ R[t] for c in coh]) - w_t @ R[t]) < 1e-14
    w_prev = np.mean([jt_cohort(t - 1 - k) for k in range(K)], axis=0)
    assert np.allclose(w_t - w_prev, (coh[0] - jt_cohort(t - K)) / K, atol=1e-15)

# 2. AMP eq. (1): w = c_t (rank(S) - mean rank); sums to zero; $1 long and $1 short; invariant to monotone transforms
def amp_weights(S):
    d = rankdata(S) - rankdata(S).mean()
    return d / d[d > 0].sum()
S = rng.standard_normal(N)
w = amp_weights(S)
assert abs(w.sum()) < 1e-12 and abs(w[w > 0].sum() - 1) < 1e-12 and abs(w[w < 0].sum() + 1) < 1e-12
assert np.allclose(w, amp_weights(3 * np.exp(S) + 7))
w_odd = amp_weights(rng.standard_normal(51)); assert np.sum(np.abs(w_odd) < 1e-15) == 1    # median rank gets zero

# 3. PBL eqs. (24)-(27): XSMOM signal s = c (r12 - mean), positives sum to 1, negatives to -1; with s = XSMOM*sigma
#    the fully shrunk EPO (w = 100%, diagonal risk) holds XSMOM/(gamma*sigma); risk weights sum to 2/gamma every period.
#    Eq. (23): TSMOM signal 0.1*sigma*sign(r12) with gamma = n/40% gives weights proportional to MOP's sign/sigma (PBL-3:
#    proportional, not equal; the Sharpe ratio is scale-free).
n = 12; r12 = rng.normal(0.08, 0.25, n); sig = rng.uniform(0.08, 0.40, n)
C = np.corrcoef(rng.standard_normal((n, 300))); Sigma = np.outer(sig, sig) * C; gamma = 3.0
def epo(s, wsh, g=gamma):                      # PBL eq. (8): (1/g) [(1-w) Sigma + w V]^{-1} s, V = diag(Sigma)
    return np.linalg.solve((1 - wsh) * Sigma + wsh * np.diag(np.diag(Sigma)), s) / g
x = r12 - r12.mean(); xs = x / x[x > 0].sum()
assert abs(xs[xs > 0].sum() - 1) < 1e-12 and abs(xs[xs < 0].sum() + 1) < 1e-12
assert np.allclose(epo(xs * sig, 1.0), xs / (gamma * sig)) and abs(np.abs(sig * epo(xs * sig, 1.0)).sum() - 2 / gamma) < 1e-12
assert np.allclose(epo(xs * sig ** 2, 1.0), xs / gamma)
s23 = 0.1 * sig * np.sign(r12); w23 = epo(s23, 1.0, g=n / 0.40)
mop_pos = np.sign(r12) * 0.40 / sig / n
ratio = w23 / mop_pos; assert np.allclose(ratio, ratio[0]) and abs(ratio[0] - 0.1) < 1e-12

# 4. MOP eq. (1): EWMA weights (1-d) d^i with centre of mass d/(1-d) = 60 days, annualised by 261, demeaned by the EW mean,
#    sigma at t uses returns through t-1 only. Conversions: half-life ln(1/2)/ln(d) = 41.9 days; e-folding 1/(1-d) = 61.
d = 60 / 61; i = np.arange(20000); wts = (1 - d) * d ** i
assert abs(wts.sum() - 1) < 1e-10 and abs((i * wts).sum() - 60) < 1e-6
assert abs(np.log(0.5) / np.log(d) - 41.9) < 0.05
def mop_sigma(daily, t):
    x = daily[:t][::-1]; ww = (1 - d) * d ** np.arange(len(x)); ww /= ww.sum()
    m = (ww * x).sum(); return np.sqrt(261 * (ww * (x - m) ** 2).sum())
daily = rng.normal(0, 0.01, 4000)
s_t = mop_sigma(daily, 3000); d2 = daily.copy(); d2[3000:] *= 50
assert mop_sigma(d2, 3000) == s_t and abs(s_t / (0.01 * np.sqrt(261)) - 1) < 0.15

# 5. MOP eqs. (6)-(7): decompositions of linear XSMOM w = (r_lag - mean)/N and TSMOM w = r_lag/N. With sample moments
#    (1/T) the identities are exact; with m_lag = 12 mu they are MOP's printed forms.
Nn, Tt = 8, 3000
A = 0.05 * rng.standard_normal((Nn, Nn)); Lg = rng.standard_normal((Tt, Nn)) * 0.3
F = Lg @ A.T / 12 + 0.04 * rng.standard_normal((Tt, Nn)) + rng.normal(0.006, 0.003, Nn)
mF = F.mean(0); Lg = Lg - Lg.mean(0) + 12 * mF                  # impose m_lag = 12 mu exactly
mL = Lg.mean(0); Om = (Lg - mL).T @ (F - mF) / Tt
pi_ts = np.mean(np.sum(Lg * F, 1)) / Nn
pi_xs = np.mean(np.sum((Lg - Lg.mean(1, keepdims=True)) * F, 1)) / Nn
assert abs(pi_ts - (np.trace(Om) / Nn + 12 * mF @ mF / Nn)) < 1e-12                                   # eq. (7)
s2mu = ((mF - mF.mean()) ** 2).mean()
assert abs(pi_xs - ((Nn - 1) / Nn ** 2 * np.trace(Om) - (Om.sum() - np.trace(Om)) / Nn ** 2 + 12 * s2mu)) < 1e-12  # eq. (6)

# 6. JT eq. (3): E[(r_i - rbar)(r_i,lag - rbar_lag)] = s2_mu + s2_b Cov(f_t, f_t-1) + mean_i Cov(e_it, e_it-1)
#    (large-N form; with N finite the last term carries (N-1)/N). Population check by simulation.
Nb, Tb = 200, 30000; mu = rng.normal(0.01, 0.01, Nb); b = rng.uniform(0.5, 1.5, Nb)
f = np.zeros(Tb); e = np.zeros((Tb, Nb)); rho_f, rho_e = 0.3, 0.1
zf, ze = rng.standard_normal(Tb), rng.standard_normal((Tb, Nb)) * 0.05
for t in range(1, Tb):
    f[t] = rho_f * f[t - 1] + 0.04 * zf[t]; e[t] = rho_e * e[t - 1] + ze[t]
r = mu + np.outer(f, b) + e
lhs = np.mean(np.sum((r[1:] - r[1:].mean(1, keepdims=True)) * (r[:-1] - r[:-1].mean(1, keepdims=True)), 1)) / Nb
cov_f = np.mean((f[1:] - f.mean()) * (f[:-1] - f.mean())); cov_e = np.mean(np.sum(e[1:] * e[:-1], 1)) / Nb
rhs = mu.var() + b.var() * cov_f + (Nb - 1) / Nb * cov_e
assert abs(lhs / rhs - 1) < 0.03

# 7. BHM (pp. 10-12): residual momentum. Betas from a 36-month regression (t-36 .. t-1) with intercept; score = sum of
#    residual returns over t-12 .. t-2 divided by their standard deviation over the same months. Text vs example (BHM-1):
#    the example (alpha "included" makes stocks with high t-36 .. t-13 returns rank low) implies the score uses
#    r - beta'f (alpha NOT subtracted). Property: residual momentum is nearly free of factor exposure; total momentum is not.
Ns, Ts = 600, 37
bet = rng.uniform(0.3, 1.7, (Ns, 3)) * np.array([1, 0.6, 0.6])
fac = rng.normal(0.0, 0.04, (Ts, 3)); fac[Ts - 13:Ts - 1, 0] += 0.04          # market trends during formation
ret = fac @ bet.T + rng.normal(0, 0.06, (Ts, Ns))
X = np.column_stack([np.ones(36), fac[:36]])
coef = np.linalg.lstsq(X, ret[:36], rcond=None)[0]                            # 4 x Ns: alpha, betas
form = slice(Ts - 13, Ts - 2)                                                 # t-12 .. t-2 (t = Ts index 36)
u_B = ret[form] - fac[form] @ coef[1:]                                        # V0 (BHM example): alpha not subtracted
u_A = u_B - coef[0]                                                           # V1: alpha subtracted
score_B = u_B.sum(0) / u_B.std(0, ddof=1); score_A = u_A.sum(0) / u_A.std(0, ddof=1)
total = np.prod(1 + ret[Ts - 13:Ts - 1], axis=0) - 1
assert np.corrcoef(total, bet[:, 0])[0, 1] > 0.4 and abs(np.corrcoef(score_B, bet[:, 0])[0, 1]) < 0.15
assert np.allclose(rankdata(score_B), rankdata((3 * u_B).sum(0) / (3 * u_B).std(0, ddof=1)))  # scale invariance
early = ret.copy(); early[:24, 0] += 0.05                                     # stock 0: large returns in t-36 .. t-13
cf = np.linalg.lstsq(X, early[:36, :1], rcond=None)[0][:, 0]
uB0 = early[form, 0] - fac[form] @ cf[1:]; uA0 = uB0 - cf[0]
assert uA0.sum() < uB0.sum()                                                  # subtracting alpha lowers its score

# 8. G&K eq. (1): s = clip(sum_{tau=1..j} f / sigma_ann, -2, 2); legs rescaled to $1 long and $1 short.
#    GK-1: dividing a j-month sum by an annual sigma is a z-score only for j = 12; the +-2 cap rarely binds at j = 1
#    and often at j = 60.
sa = 0.10; m = rng.normal(0, sa / np.sqrt(12), (200000, 60))
frac = {j: np.mean(np.abs(m[:, :j].sum(1) / sa) > 2) for j in (1, 12, 60)}
assert frac[1] < 1e-3 and 0.035 < frac[12] < 0.06 and frac[60] > 0.35
fr = rng.normal(0.003, 0.03, 20); past = rng.normal(0.02, 0.1, 20)
s = np.clip(past / 0.1, -2, 2); lw = np.where(s > 0, s, 0) / s[s > 0].sum(); sw = np.where(s <= 0, s, 0) / -s[s <= 0].sum()
assert abs(lw.sum() - 1) < 1e-12 and abs(sw.sum() + 1) < 1e-12
# E&L (NBER 2019, p. 7): long factors with positive prior-year return, short those with negative, equal-weighted legs
win, los = past > 0, past <= 0
el_ret = fr[win].mean() - fr[los].mean()
assert abs(el_ret - ((win / win.sum() - los / los.sum()) @ fr)) < 1e-15        # E&L-2: undefined if a leg is empty

# 9. B&SC eqs. (5)-(6): sigma^2_t = 21 * sum_{j=0..125} r^2_{d_{t-1}-j} / 126 (uncentred daily, last 126 sessions before the
#    month); scaled return = (sigma_target / sigma_t) r_t with sigma_target = 12% a year (monthly 12%/sqrt(12)). No look-ahead.
dd = rng.normal(0, 0.012, 3000)
def bsc_sigma(daily, d_end): return np.sqrt(21 * np.sum(daily[d_end - 126:d_end] ** 2) / 126)
st = bsc_sigma(dd, 2000); dd2 = dd.copy(); dd2[2000:] *= 10
assert bsc_sigma(dd2, 2000) == st and abs(st / (0.012 * np.sqrt(21)) - 1) < 0.15

# 10. DM eq. (6) / App. C eq. (23): w* = (1/2 lambda) mu/sigma^2 rests on App. C's approximation E[(r_p - rbar)^2] ~ sigma_t^2.
#     DM-1: the exact maximiser of the unconditional Sharpe ratio is w ∝ mu/(sigma^2 + mu^2) (Cauchy-Schwarz); the gap is
#     negligible at monthly frequency and grows with |mu|/sigma. When mu/sigma is constant, dyn = cvol (B&SC).
def sharpe(wv, p, mu_, sg):
    m1 = np.sum(p * wv * mu_); m2 = np.sum(p * wv ** 2 * (sg ** 2 + mu_ ** 2)); return m1 / np.sqrt(m2 - m1 ** 2)
p = np.full(6, 1 / 6); sg = np.array([0.03, 0.04, 0.05, 0.07, 0.10, 0.15])
gaps = {}
for scale, tol in ((1.0, 2e-3), (6.0, None)):
    mu_ = scale * np.array([0.012, 0.010, 0.008, 0.004, -0.002, -0.010])
    s_dm, s_ex = sharpe(mu_ / sg ** 2, p, mu_, sg), sharpe(mu_ / (sg ** 2 + mu_ ** 2), p, mu_, sg)
    best = max(sharpe(mu_ / (sg ** 2 + mu_ ** 2) * np.exp(0.05 * rng.standard_normal(6)), p, mu_, sg) for _ in range(2000))
    assert s_ex >= s_dm - 1e-12 and s_ex >= best - 1e-12
    gaps[scale] = (s_ex - s_dm) / s_ex
    if tol: assert (s_ex - s_dm) / s_ex < tol
    else: assert (s_ex - s_dm) / s_ex > 1e-2
mu_c = 0.2 * sg; assert np.allclose((mu_c / sg ** 2) / (mu_c / sg ** 2)[0], (1 / sg) / (1 / sg)[0])

# 11. HOP (pp. 4-5): equal-weighted 1-, 3- and 12-month TSMOM; each signal is +-1 per market, so the combined
#     risk position is in {-1, -1/3, 1/3, 1} per unit of market volatility before portfolio scaling to 10%.
sigs = np.sign(rng.standard_normal((1000, 3))); comb = sigs.mean(1)
assert all(np.min(np.abs(comb[:, None] - np.array([-1, -1 / 3, 1 / 3, 1])), axis=1) < 1e-12)

print("PASS S4.8 momentum constructions: JT overlapping cohorts; AMP rank weights; PBL (24)-(27) and PBL-3; MOP eq. (1) "
      "centre of mass 60 d = half-life 41.9 d, no look-ahead; MOP eqs. (6)-(7) exact; JT eq. (3); BHM residual momentum "
      "(factor-neutral; BHM-1 alpha reading); G&K eq. (1) caps (GK-1) and unit leverage; E&L legs; B&SC eqs. (5)-(6); "
      "DM eq. (6) vs exact maximiser (DM-1); HOP combination\n"
      f"  JT eq. (3) lhs/rhs = {lhs / rhs:.4f}; BHM corr(total, beta) = {np.corrcoef(total, bet[:, 0])[0, 1]:.2f}, "
      f"corr(residual, beta) = {np.corrcoef(score_B, bet[:, 0])[0, 1]:.2f}; GK-1 share |s| > 2: j=1 {frac[1]:.4f}, "
      f"j=12 {frac[12]:.3f}, j=60 {frac[60]:.3f}; DM-1 relative Sharpe gap {gaps[1.0]:.2e} (monthly scale), "
      f"{gaps[6.0]:.2e} (mu x 6)")
