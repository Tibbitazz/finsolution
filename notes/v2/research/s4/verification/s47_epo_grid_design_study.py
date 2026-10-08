"""S4.7 design study for decision S47-D2 (synthetic; about the resolution of a tuning protocol, NOT a ranking of methods).
PBL (2021) choose the simple-EPO shrinkage w out of sample as the grid value with the highest trailing Sharpe ratio
(expanding window; Fig. 2 notes, p. 138; the grid is not stated, PBL-2). Questions from the owner (2026-10-08):
  (1) how fine should the grid be?  (2) apply EPO to the raw risk model or to PBL's 5%-pre-shrunk one (theta = 0.05)?
Design: N = 15 asset classes, monthly; one global factor + 3 blocks; 60-month estimation window; 180-month burn-in before
the first selection (PBL: at least 15 years); 360 evaluation months; two signals: the trailing sample mean, and a
"noisy CMA" (true mean with 50% relative error). gamma = 1 (simple EPO's Sharpe ratio does not depend on gamma).
Gross returns, no transaction costs. Prints the results and asserts only the qualitative conclusions."""
import numpy as np, warnings
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
N, WARM, BURN, EVAL = 15, 60, 180, 360; T = WARM + BURN + EVAL
GRIDS = {'3': np.array([0, .5, 1]), '8 (PBL Table 2)': np.array([0, .1, .25, .5, .75, .9, .99, 1]),
         '11 logit-spaced': np.array([0, .01, .03, .1, .25, .5, .75, .9, .97, .99, 1]),
         '21 (step 0.05)': np.linspace(0, 1, 21), '101 (step 0.01)': np.linspace(0, 1, 101)}
ALLW = np.unique(np.concatenate(list(GRIDS.values())))
def history(seed, signal, theta):
    rng = np.random.default_rng(seed)
    vol = rng.uniform(0.04, 0.20, N) / np.sqrt(12); blk = rng.integers(0, 3, N)
    C = 0.25 + 0.35 * (blk[:, None] == blk[None, :]); np.fill_diagonal(C, 1); C = C + 0.05 * np.diag(rng.uniform(0, 1, N))
    d = np.sqrt(np.diag(C)); C = C / np.outer(d, d); S = np.outer(vol, vol) * C
    mu = rng.uniform(0.1, 0.45, N) / np.sqrt(12) * vol
    R = mu + rng.standard_normal((T, N)) @ np.linalg.cholesky(S).T; noise = rng.normal(0, 0.5, (T, N))
    Ret = np.full((T, len(ALLW)), np.nan)
    for t in range(WARM, T - 1):
        X = R[t - WARM:t]; Sh = np.cov(X, rowvar=False); sd = np.sqrt(np.diag(Sh))
        Om = (1 - theta) * Sh / np.outer(sd, sd) + theta * np.eye(N)
        s = X.mean(0) if signal == 'sample mean' else mu * (1 + noise[t])
        D, P = np.linalg.eigh(Om); z = P.T @ (s / sd)                                     # Sigma_w^-1 s via the eigenbasis
        Xw = ((P[:, :, None] * (z[:, None] / ((1 - ALLW)[None, :] * D[:, None] + ALLW[None, :]))[None]).sum(1)) / sd[:, None]
        Ret[t + 1] = R[t + 1] @ Xw
    return Ret
def select(Ret, g):
    idx = np.searchsorted(ALLW, g); ch, st = [], []
    for t in range(WARM + BURN, T):
        h = Ret[WARM + 1:t, idx]; j = int(np.argmax(h.mean(0) / h.std(0))); ch.append(g[j]); st.append(Ret[t, idx[j]])
    st = np.array(st); return st.mean() / st.std() * np.sqrt(12), np.mean(np.diff(ch) != 0)
SIMS = 120
print("(1) grid size, theta = 0: mean out-of-sample Sharpe (paired difference vs the 8-point grid) and how often w changes")
summary = {}
for signal in ('sample mean', 'noisy CMA'):
    sr = {k: [] for k in GRIDS}; sw = {k: [] for k in GRIDS}
    for seed in range(SIMS):
        Ret = history(seed, signal, 0.0)
        for k, g in GRIDS.items():
            a, b = select(Ret, g); sr[k].append(a); sw[k].append(b)
    base = np.array(sr['8 (PBL Table 2)'])
    for k in GRIDS:
        a = np.array(sr[k]); dd = a - base
        print(f"  {signal:12s} grid {k:16s} SR {a.mean():.3f}  diff {dd.mean():+.4f} (se {dd.std() / np.sqrt(SIMS):.4f})  w changes in {np.mean(sw[k]):.1%} of months")
    summary[signal] = (np.array(sr['101 (step 0.01)']) - base, np.mean(sw['8 (PBL Table 2)']), np.mean(sw['101 (step 0.01)']))
print("(2) theta = 0.05 minus theta = 0 on identical histories (8-point grid)")
g8 = GRIDS['8 (PBL Table 2)']; i8 = np.searchsorted(ALLW, g8); paired = {}
for signal in ('sample mean', 'noisy CMA'):
    d_sel, d_w0, d_best = [], [], []
    for seed in range(SIMS):
        R0, R5 = history(seed, signal, 0.0), history(seed, signal, 0.05)
        d_sel.append(select(R5, g8)[0] - select(R0, g8)[0])
        e0, e5 = R0[WARM + BURN:, i8], R5[WARM + BURN:, i8]; s0, s5 = e0.mean(0) / e0.std(0) * np.sqrt(12), e5.mean(0) / e5.std(0) * np.sqrt(12)
        d_w0.append(s5[0] - s0[0]); d_best.append(s5.max() - s0.max())
    paired[signal] = (np.array(d_sel), np.array(d_w0), np.array(d_best))
    for name, dd in (('past-only selected w', d_sel), ('w = 0 (plain MVO)', d_w0), ('best fixed w', d_best)):
        dd = np.array(dd); print(f"  {signal:12s} {name:22s} {dd.mean():+.4f} (se {dd.std() / np.sqrt(SIMS):.4f})")
# qualitative conclusions asserted
for signal, (dd, sw8, sw101) in summary.items():
    assert abs(dd.mean()) < 0.01 and sw101 > 3 * sw8                                     # finer grid: no material gain, many more switches
for signal, (d_sel, d_w0, d_best) in paired.items():
    assert d_w0.mean() > 0 and abs(d_best.mean()) < 0.005 and abs(d_sel.mean()) < 0.01    # pre-shrink helps plain MVO, not EPO
print("PASS design study: grids beyond ~8 points add < 0.01 Sharpe but multiply switching; 5% pre-shrink matters for plain MVO, not for EPO")
