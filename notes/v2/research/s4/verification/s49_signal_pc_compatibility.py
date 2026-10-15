"""S4.9 signal x PC compatibility: toy examples showing which constructions are well defined, and unit checks.
Sources: Michaud & Michaud 2008 ch. 12 pp. 109-111 (forecasts need scaling: IC x volatility; consistent units; index-weighted
active returns sum to zero); PBL 2021 eqs. (8), (23)-(27) and Prop. 3; JT 1993 (equal-weighted deciles); AMP 2013
(terciles; rank weights); MOP 2012 eq. (5) (sign x 1/sigma); EQ-SPLIT-1 (S47-D6). Synthetic data only; prints PASS."""
import numpy as np, warnings
from scipy.stats import rankdata
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS

rng = np.random.default_rng(20261015)
n = 10
sig = rng.uniform(0.10, 0.35, n)                                      # annual volatilities
C = np.corrcoef(rng.standard_normal((n, 400))); Sig = np.outer(sig, sig) * C
score = rng.standard_normal(n)                                         # a raw signal (e.g. 12-1 returns)
mvo = lambda mu, S, gam=3.0: np.linalg.solve(S, mu) / gam            # unconstrained, cash residual

# 1. INVALID: feeding ranks (or any unscaled score) to a mu-consuming method. The weights depend on arbitrary choices
#    (rank origin 1..N vs 0..N-1 vs centred) and are not in return units (Michaud pp. 109-110: relative valuations
#    "need scaling in order to be useful as inputs to most optimizers").
rk = rankdata(score)
w_a, w_b, w_c = mvo(rk, Sig), mvo(rk - 1, Sig), mvo(rk - rk.mean(), Sig)
assert np.abs(w_a - w_b).max() > 0.1 and np.abs(w_a - w_c).max() > 0.1

# 2. VALID after a mapping: alpha = IC * sigma * z (Michaud p. 110; Ambachtsheer 1977). z removes location and scale, so
#    the mapped alpha is invariant to every affine relabelling of the raw score and, for ranks, to any monotone transform.
def alpha_map(raw, ic=0.05, vol=sig):
    z = (raw - raw.mean()) / raw.std(); return ic * vol * z
assert np.allclose(alpha_map(score), alpha_map(7 + 3 * score))
assert np.allclose(alpha_map(rankdata(score)), alpha_map(rankdata(np.exp(score))))

# 3. Benchmark neutrality (Michaud p. 111): index-weighted active returns sum to zero. Adjust alpha - (w_b'alpha)*1
#    (w_b sums to 1) so that w_b'alpha = 0.
wb = rng.dirichlet(np.ones(n)); a = alpha_map(score); a_adj = a - wb @ a
assert abs(wb @ a_adj) < 1e-15

# 4. Units (Michaud p. 110): monthly returns with annual risk misstate the optimum by a factor 12; consistent units
#    (both monthly or both annual) give identical weights.
mu_ann = alpha_map(score); mu_m, Sig_m = mu_ann / 12, Sig / 12
assert np.allclose(mvo(mu_ann, Sig), mvo(mu_m, Sig_m)) and np.allclose(mvo(mu_m, Sig), mvo(mu_ann, Sig) / 12)

# 5. VALID, source-native: PBL signals into EPO. EPO_s(w) = (1/gamma) [(1-w) Sigma + w V]^{-1} s (eq. 8):
#    w = 0 is MVO on s (Prop. 3); w = 1 with the TSMOM signal s = 0.1 sigma sign(r) is proportional to MOP's
#    sign x 1/sigma (PBL-3), i.e. PC-A3 with a direction rule.
def epo(s, wsh, gam=3.0): return np.linalg.solve((1 - wsh) * Sig + wsh * np.diag(np.diag(Sig)), s) / gam
s_ts = 0.1 * sig * np.sign(score)
assert np.allclose(epo(s_ts, 0.0), mvo(s_ts, Sig))
r = epo(s_ts, 1.0) / (np.sign(score) / sig); assert np.allclose(r, r[0])

# 6. VALID: signal-conditioned universe with a mu-free heuristic. JT's winner decile is 1/N within the selected set; AMP
#    value-weight stock terciles (cap weights within the set); MOP/HOP size by 1/sigma. Each is a long-only
#    portfolio summing to 1 and depends on the signal only through the selection (invariant to monotone transforms).
N = 60; s60 = rng.standard_normal(N); cap = rng.lognormal(0, 1, N); vol60 = rng.uniform(0.15, 0.6, N)
def top(sc, frac): return rankdata(sc) > N * (1 - frac)
for sc in (s60, np.exp(s60)):
    sel = top(sc, 1 / 3)
    ew = sel / sel.sum(); vw = sel * cap / (sel * cap).sum(); iv = sel / vol60 / (sel / vol60).sum()
    for w in (ew, vw, iv): assert abs(w.sum() - 1) < 1e-12 and (w >= 0).all()
assert np.allclose(top(s60, 1 / 3), top(np.exp(s60), 1 / 3))

# 7. Direction rule vs the engine-level target (EQ-SPLIT-1). Long-only TSMOM keeps a 1/sigma position where the trend
#    is up and holds cash where it is down. If the engine scales every mu-free portfolio to sigma* AFTER the rule, a
#    risk-off state is levered back up (here: 2 of 10 assets up -> exposure raised toward the target, capped only by L);
#    applying the rule AFTER the scaling lets the trend rule cut risk below sigma*, never raise it.
sig_star, L = 0.10, 1.0
trend_up = np.zeros(n, bool); trend_up[:2] = True
base = (1 / sig) / (1 / sig).sum()                                     # PC-A3 base portfolio
def port_vol(w): return np.sqrt(w @ Sig @ w)
def scale_to(w):                                                        # EQ-SPLIT-1, mu-free branch: risky mix p
    p = w / w.sum(); k = min(sig_star / port_vol(p), L); return k * p   # (sums to 1), exposure k, cash 1 - k
w_rule_then_scale = scale_to(np.where(trend_up, base, 0.0))
w_scale_then_rule = np.where(trend_up, scale_to(base), 0.0)
assert w_rule_then_scale.sum() > w_scale_then_rule.sum() + 0.05        # risk-off state partly undone
assert port_vol(w_scale_then_rule) <= sig_star + 1e-12
w_all_down = np.where(np.zeros(n, bool), scale_to(base), 0.0); assert w_all_down.sum() == 0   # all down -> all cash

# 8. Linear identity behind S48-D1: (1/N) r_i = (1/N)(r_i - rbar) + rbar/N -- magnitude TSMOM = XSMOM tilt + common
#    position sized by the average trend.
rr = rng.normal(0.05, 0.2, n)
assert np.allclose(rr / n, (rr - rr.mean()) / n + rr.mean() / n)

print("PASS S4.9 signal x PC compatibility: unscaled ranks into MVO ill-defined; alpha = IC*sigma*z invariant to "
      "relabelling; benchmark-neutral alpha; unit consistency (factor 12); PBL EPO w=0 = MVO on s, w=1 = sign x 1/sigma; "
      "conditioned universes with 1/N, cap and 1/sigma well defined; direction rule must follow the engine-level "
      f"scaling (risk-off exposure {w_scale_then_rule.sum():.2f} vs {w_rule_then_scale.sum():.2f} if scaled after); "
      "S48-D1 identity")
