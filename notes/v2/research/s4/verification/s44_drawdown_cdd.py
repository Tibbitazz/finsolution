"""S4.4 source reproduction: Chekhlov, Uryasev & Zabarankin (UF report 2003-15, 25 Jun 2003): drawdown (eqs. 6-7),
CV@R (14), LP (25), knapsack (30), path LP (31), limits (17), and the MaxDD-constrained LP (55)."""
import numpy as np, warnings
from scipy.optimize import linprog
warnings.filterwarnings('ignore')
def drawdowns(r): w = np.concatenate([[0], np.cumsum(r)]); return (np.maximum.accumulate(w) - w)[1:]   # uncompounded, absolute
def cvar_def(xi, a):
    if a == 0: return xi.mean()
    N = len(xi); zeta = np.sort(xi)[int(np.ceil(a * N)) - 1]
    return (np.mean(xi <= zeta) - a) / (1 - a) * zeta + xi[xi > zeta].sum() / ((1 - a) * N)
def cvar_lp(xi, a):
    N = len(xi); res = linprog(np.r_[1, np.full(N, 1 / ((1 - a) * N))], A_ub=np.c_[-np.ones(N), -np.eye(N)], b_ub=-xi,
                               bounds=[(None, None)] + [(0, None)] * N, method='highs'); return res.fun
def cvar_knap(xi, a):
    cap = 1 / ((1 - a) * len(xi)); rem = 1.0; tot = 0.0
    for v in np.sort(xi)[::-1]:
        q = min(cap, rem); tot += q * v; rem -= q
        if rem <= 1e-15: break
    return tot
def cdd_path_lp(r, a):
    N = len(r); A = []; b = []
    for k in range(N):
        row = np.zeros(1 + 2 * N); row[0] = -1; row[1 + k] = -1; row[1 + N + k] = 1; A.append(row); b.append(0)
        row = np.zeros(1 + 2 * N); row[1 + N + k] = -1
        if k: row[N + k] = 1
        A.append(row); b.append(r[k])
    return linprog(np.r_[1, np.full(N, 1 / ((1 - a) * N)), np.zeros(N)], A_ub=np.array(A), b_ub=np.array(b),
                   bounds=[(None, None)] + [(0, None)] * (2 * N), method='highs').fun
rng = np.random.default_rng(20261008); r = rng.normal(.0004, .01, 400); xi = drawdowns(r)
for a in (0.0, 0.5, 0.8, 0.95):
    vals = [cvar_def(xi, a), cvar_lp(xi, a), cvar_knap(xi, a), cdd_path_lp(r, a)]; assert np.ptp(vals) < 1e-9, a
assert abs(cvar_def(xi, 1 - 0.5 / len(xi)) - xi.max()) < 1e-12 and abs(cvar_def(xi, 0) - xi.mean()) < 1e-12   # eq. (17)
def maxdd_lp(R, gam):  # eq. (55), long-only, fully invested
    T, m = R.shape; A = []
    for k in range(T):
        row = np.zeros(m + T); row[:m] = -R[k]; row[m + k] = -1
        if k: row[m + k - 1] = 1
        A.append(row)
    return linprog(np.r_[-R.sum(0), np.zeros(T)], A_ub=np.array(A), b_ub=np.zeros(T), A_eq=[np.r_[np.ones(m), np.zeros(T)]], b_eq=[1],
                   bounds=[(0, 1)] * m + [(0, gam)] * T, method='highs')
R = rng.normal([.0003, .0004, .0005, .0006, .0002], [.004, .008, .012, .016, .006], (500, 5))
res = maxdd_lp(R, 0.03); dd = drawdowns(R @ res.x[:5]); assert abs(dd.max() - 0.03) < 1e-7        # binding, exact
assert maxdd_lp(R, 0.02).status == 2                                                              # infeasible (CDD-2)
print("PASS Chekhlov-Uryasev-Zabarankin: CV@R definition = LP(25) = knapsack(30) = path-LP(31); limits MaxDD/AvDD; LP(55) exact and infeasible at tight gamma")
