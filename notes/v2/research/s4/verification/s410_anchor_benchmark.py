"""S4.10 anchors and benchmarks. SPECIFICATION VERIFICATION ONLY; synthetic data except printed exhibits; prints PASS.
Sources:
  PBL 2021 eqs. (18)-(22), Prop. 3 (anchored EPO; anchors 1/N and 1/sigma in Equity 6/7, p. 136)
  Roll (1992), "A Mean/Variance Analysis of Tracking Error", JPM 18(4):13-22, eqs. (1)-(5), App. A.1-A.6, fn. 10
  Jorion (2003), "Portfolio Optimization with Tracking-Error Constraints", FAJ 59(5):70-82, eqs. (B3)-(B6), (C6), (C17),
    Theorems 2a-2d, Tables 1-3
  Grinold & Kahn, Advances in Active Portfolio Management, ch. 20 (Grinold 1992, revised 2018): GRS test eq. (4), fn. 8
    identity SR_H^2 = SR_B^2 + IR_H^2, Exhibits 5-6
  Account eligibility: registry fact no.wrapper.ask.eligible_holdings (Skatteetaten; V-full)."""
import numpy as np, itertools, warnings
from scipy.optimize import linprog, minimize
from scipy.stats import f as fdist
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # spurious numpy/Accelerate matmul warnings on macOS
rng = np.random.default_rng(20261018); inv = np.linalg.inv

# ---------- synthetic asset-class universe (annual): NO, US, Europe, EM equity; global gov bonds; global high yield ----------
names = ['NO eq', 'US eq', 'EU eq', 'EM eq', 'Gov bonds', 'HY bonds']
vol = np.array([0.20, 0.16, 0.17, 0.22, 0.045, 0.09])
C = np.array([[1, .65, .70, .65, -.10, .55], [.65, 1, .80, .70, -.15, .60], [.70, .80, 1, .72, -.10, .60],
              [.65, .70, .72, 1, -.05, .60], [-.10, -.15, -.10, -.05, 1, .20], [.55, .60, .60, .60, .20, 1]])
S = np.outer(vol, vol) * C; V = np.diag(vol ** 2); n = len(vol)
assert np.all(np.linalg.eigvalsh(S) > 0)
equity = np.array([1, 1, 1, 1, 0, 0], bool)
cap = np.array([0.4, 45, 15, 10, 50, 3.0]); cap = cap / cap.sum()                     # synthetic market values
anchors = {'1/N': np.ones(n) / n, '1/sigma': (1 / vol) / (1 / vol).sum(), 'cap': cap,
           '60/40': np.r_[0.6 * cap[:4] / cap[:4].sum(), 0.4 * np.array([0.75, 0.25])]}
for a in anchors.values(): assert abs(a.sum() - 1) < 1e-12 and (a >= 0).all()
sd = lambda w, M=S: np.sqrt(w @ M @ w)

# ===== A. Anchored EPO with each anchor (PBL eqs. 18-22) =====
wsh = 0.5; Sw = (1 - wsh) * S + wsh * V
epo18 = lambda s, a, g, w=wsh: inv((1 - w) * S + w * V) @ ((1 - w) * s / g + w * V @ a)
def epo22(s, a, w=wsh):
    Swl = (1 - w) * S + w * V
    g = np.sqrt((s @ inv(Swl) @ S @ inv(Swl) @ s) / (a @ S @ a)); return epo18(s, a, g, w), g
s = rng.normal(0, 0.02, n)
for nm, a in anchors.items():
    assert np.allclose(epo18(s, a, 3.0, 1.0), a)                                       # w = 1 returns the anchor
    g = 2.5; s_imp = g * S @ a                                                           # anchor-implied returns (reverse MVO)
    for w in (0.0, 0.3, 0.7, 1.0): assert np.allclose(epo18(s_imp, a, g, w), a)          # anchor-consistent signal -> anchor for every w
    x, g22 = epo22(s, a)
    sig_port = inv(Sw) @ s / g22; assert abs(sd(sig_port) - sd(a)) < 1e-12              # eq. (21): signal portfolio risk = anchor risk
    x0, _ = epo22(s, a, 0.0)                                                             # w = 0: direction is anchor-free, scale = sigma(a)
    m0 = inv(S) @ s; assert np.allclose(x0 / sd(x0), m0 / sd(m0)) and abs(sd(x0) - sd(a)) < 1e-12
# relative (cross-sectionally centred) signals carry no level; the anchor supplies it (1/N anchor: a's = 0)
sc = s - s.mean(); a1 = anchors['1/N']; g = 2.5
for w in (0.2, 0.5, 0.8):
    mu_t = (1 - w) * sc + w * g * V @ a1                                                  # mu~ of eq. (18)
    assert abs(a1 @ sc) < 1e-15 and abs(a1 @ mu_t - w * g * a1 @ V @ a1) < 1e-15
# different anchors give different portfolios at intermediate w (the anchor is a modelling choice, not a detail)
xs = {nm: epo18(s, a, 3.0) for nm, a in anchors.items()}
assert min(np.abs(xs[i] - xs[j]).max() for i, j in itertools.combinations(xs, 2)) > 0.01

# ===== B. Feasibility of anchors and benchmarks =====
ask_ok = np.array([1, 1, 1, 1, 0, 0], bool)                       # ASK: EEA shares and EEA equity funds (>80% shares) only; bonds,
b6040 = anchors['60/40']                                           # bond funds and HY funds are not eligible (registry fact)
assert b6040[~ask_ok].sum() > 0.39                                 # 60/40 needs 40% outside the ASK-eligible set
# B1 projections of an infeasible anchor onto the ASK-feasible set (cash = residual, zero volatility)
p_renorm = np.where(ask_ok, b6040, 0); p_renorm /= p_renorm.sum()                       # (i) renormalise equities to 100%
p_cash = np.where(ask_ok, b6040, 0)                                                     # (ii) ineligible weight to cash
k = sd(b6040) / sd(p_renorm); p_risk = k * p_renorm                                    # (iii) risk-matched equity + cash
assert sd(p_renorm) / sd(b6040) > 1.4 and abs(sd(p_risk) - sd(b6040)) < 1e-12
proj = {'60/40': sd(b6040), 'renormalised': sd(p_renorm), 'bonds->cash': sd(p_cash), 'risk-matched': sd(p_risk)}
# B2 household feasibility: an anchor over all accounts is feasible iff a transportation problem is feasible; equivalently
#    (supply-demand theorem) for every set J of classes, sum_J a_j <= wealth of accounts eligible for at least one class in J
def lp_feasible(a, W, E):                       # y_kj >= 0, sum_j y_kj = W_k, sum_k y_kj = a_j, y_kj = 0 where not eligible
    K, J = E.shape; Aeq = []; beq = []
    for k_ in range(K): row = np.zeros(K * J); row[k_ * J:(k_ + 1) * J] = 1; Aeq.append(row); beq.append(W[k_])
    for j in range(J): row = np.zeros(K * J); row[j::J] = 1; Aeq.append(row); beq.append(a[j])
    bnds = [(0, None) if E[k_, j] else (0, 0) for k_ in range(K) for j in range(J)]
    return linprog(np.zeros(K * J), A_eq=np.array(Aeq), b_eq=beq, bounds=bnds, method='highs').status == 0
def cut_condition(a, W, E):
    J = len(a)
    return all(a[list(Js)].sum() <= W[E[:, list(Js)].any(1)].sum() + 1e-12 for r in range(1, J + 1) for Js in itertools.combinations(range(J), r))
a7 = np.r_[b6040, 0.0]                                             # classes incl. cash (eligible everywhere)
E2 = np.array([np.r_[ask_ok, True], np.ones(n + 1, bool)])         # account 1 = ASK, account 2 = ordinary account
for wask, expect in ((0.70, False), (0.60, True), (0.50, True)):
    W = np.array([wask, 1 - wask]); assert lp_feasible(a7, W, E2) == cut_condition(a7, W, E2) == expect
for _ in range(300):                                               # random accounts and anchors: LP feasibility == cut condition
    K = rng.integers(2, 4); J = 5; E_ = rng.random((K, J)) < 0.6; E_[:, -1] = True; W = rng.dirichlet(np.ones(K)); a_ = rng.dirichlet(np.ones(J))
    assert lp_feasible(a_, W, E_) == cut_condition(a_, W, E_)

# ===== C. Roll 1992: minimum tracking-error-variance (TEV) portfolios =====
R = np.array([0.075, 0.070, 0.072, 0.085, 0.030, 0.050])           # expected returns (synthetic)
one = np.ones(n); A_ = R @ inv(S) @ R; B_ = R @ inv(S) @ one; C_ = one @ inv(S) @ one
q0 = inv(S) @ one / C_; q1 = inv(S) @ R / B_; R0, R1 = B_ / C_, A_ / B_; s0, s1 = 1 / C_, A_ / B_ ** 2    # App. table
assert np.isclose(q0 @ R, R0) and np.isclose(q1 @ R, R1) and np.isclose(sd(q0) ** 2, s0) and np.isclose(sd(q1) ** 2, s1)
def min_var(Arows, cvec):                                          # min x'Sx s.t. Arows x = cvec (KKT)
    Am = np.array(Arows); return inv(S) @ Am.T @ np.linalg.solve(Am @ inv(S) @ Am.T, cvec)
sig2_eff = lambda m: (A_ - 2 * B_ * m + C_ * m ** 2) / (A_ * C_ - B_ ** 2)     # efficient-frontier variance at mean m
G = 0.02
for qB in (anchors['60/40'], anchors['1/N'], rng.dirichlet(np.ones(n))):
    RB, sB2 = qB @ R, qB @ S @ qB; D = G / (R1 - R0)
    x = min_var([one, R], [0, G]); assert np.allclose(x, D * (q1 - q0))                  # eq. (1): independent of the benchmark
    qP = qB + x; T_ = x @ S @ x
    assert np.isclose(T_, D ** 2 * (s1 - s0))                                            # eq. (2)
    assert np.isclose(qP @ S @ qP, sB2 + T_ + 2 * D * s0 * (RB / R0 - 1))                # eq. (3)
    beta = (qP @ S @ qB) / sB2; assert np.isclose(beta, 1 + D * (s0 / sB2) * (RB / R0 - 1))   # eq. (4)
    if RB > R0: assert beta > 1                                                          # benchmark above GMV mean -> beta > 1
    assert np.isclose(sB2 - sig2_eff(RB), qP @ S @ qP - sig2_eff(RB + G))                # A.4: constant variance distance
    for b_ in (0.9, 1.0, 1.1):                                                           # A.6 beta-constrained TEV portfolio
        xb = min_var([one, R, S @ qB], [0, G, sB2 * (b_ - 1)])
        den = (R1 - R0) * (sB2 - sig2_eff(RB))
        g1 = (G * (sB2 - s0) + sB2 * (b_ - 1) * (R0 - RB)) / den
        g0 = (G * (RB / B_ - sB2) + sB2 * (b_ - 1) * (RB - R1)) / den
        gB = (G * (s0 - RB / B_) + sB2 * (b_ - 1) * (R1 - R0)) / den
        assert abs(g1 + g0 + gB) < 1e-10 and np.allclose(xb, g1 * q1 + g0 * q0 + gB * qB)   # '+ gB' as in eq. (5) and fn. 8
        assert not np.allclose(xb, g1 * q1 + g0 * q0 - gB * qB)                         # ROLL-1: '- gB' in (A-10) is a sign slip
for _ in range(2000):                                                                    # A.5: portfolios dominating B have beta < 1
    qB = anchors['60/40']; qP = rng.dirichlet(np.ones(n))
    if qP @ R > qB @ R and sd(qP) < sd(qB): assert (qP @ S @ qB) / (qB @ S @ qB) < 1
for sP, sB_, rho in ((0.15, 0.14, 0.6), (0.15, 0.14, 0.4)):                              # fn. 10: SE(mean diff) < SE(P) iff rho > sB/(2 sP)
    assert ((sP ** 2 + sB_ ** 2 - 2 * rho * sP * sB_) < sP ** 2) == (rho > sB_ / (2 * sP))

# ===== D. Jorion 2003: TEV frontier, constant-TEV ellipse, total-risk constraint =====
d_ = A_ - B_ ** 2 / C_; muMV = R0; sMV2 = s0
for qB in (anchors['60/40'], anchors['cap']):
    muB, sB2 = qB @ R, qB @ S @ qB
    for TEV in (0.01, 0.03):
        T_ = TEV ** 2; x = np.sqrt(T_ / d_) * inv(S) @ (R - muMV * one)                 # (B3): independent of q
        assert abs(x @ one) < 1e-12 and np.isclose(x @ S @ x, T_) and np.isclose(x @ R, np.sqrt(d_ * T_))   # (B4): IR = sqrt(d)
        assert np.isclose((qB + x) @ S @ (qB + x), sB2 + 2 * np.sqrt(T_ / d_) * (muB - muMV) + T_)    # (B6)
        D1, D2 = muB - muMV, sB2 - sMV2
        for sP2 in np.linspace(sB2 + T_ - 0.5 * np.sqrt(T_ * D2), sB2 + T_ + 0.5 * np.sqrt(T_ * D2), 3):   # (C6) ellipse, numerically
            cons = [{'type': 'eq', 'fun': lambda v: v @ one}, {'type': 'eq', 'fun': lambda v: v @ S @ v - T_},
                    {'type': 'eq', 'fun': lambda v, s2=sP2: (qB + v) @ S @ (qB + v) - s2}]
            best = None
            for _ in range(6):
                r = minimize(lambda v: -(v @ R), rng.normal(0, 0.05, n), constraints=cons, method='SLSQP', options={'ftol': 1e-14, 'maxiter': 2000})
                if r.success and (best is None or r.fun < best.fun): best = r
            y = sP2 - sB2 - T_; z = best.x @ R
            assert abs(d_ * y ** 2 + 4 * D2 * z ** 2 - 4 * D1 * y * z - 4 * T_ * (d_ * D2 - D1 ** 2)) < 1e-9
        zc = -T_ * D1 / (2 * D2) + np.sqrt(T_ * (d_ - D1 ** 2 / D2) * (1 - T_ / (4 * D2)))    # (C17): total risk = benchmark risk
        cons = [{'type': 'eq', 'fun': lambda v: v @ one}, {'type': 'eq', 'fun': lambda v: v @ S @ v - T_},
                {'type': 'eq', 'fun': lambda v: (qB + v) @ S @ (qB + v) - sB2}]
        best = min((minimize(lambda v: -(v @ R), rng.normal(0, 0.05, n), constraints=cons, method='SLSQP', options={'ftol': 1e-14, 'maxiter': 2000})
                    for _ in range(6)), key=lambda r: r.fun if r.success else 1e9)
        assert abs(best.x @ R - zc) < 1e-7 and zc < np.sqrt(d_ * T_)
# printed example (Tables 1-3, Theorems 2a-2d): d = 0.25 (IR 0.5), muB 10%, muMV 8%, sigmaMV 6.4%, rf 5%; sigmaB = 13.76%
# reproduces every printed figure to rounding (Table 1 prints 13.8%)
d, muB, muMV, sMV, sB = 0.25, 0.10, 0.08, 0.064, 0.1376; D1, D2 = muB - muMV, sB ** 2 - sMV ** 2; T_ = 0.04 ** 2
sP = np.sqrt(sB ** 2 + 2 * np.sqrt(T_ / d) * D1 + T_)
assert round(100 * (muB + np.sqrt(d * T_)), 1) == 12.0 and round(100 * sP, 1) == 15.4                     # Table 1, P
assert round(100 * (0.05 + (muB - 0.05) * sP / sB), 1) == 10.6                                            # Table 1, L
assert round(100 * (muMV + np.sqrt(d * (sB ** 2 - sMV ** 2))), 1) == 14.1                                # Table 1, E
assert [round(100 * v, 1) for v in (np.sqrt(D2 - D1 ** 2 / d), np.sqrt(D2), 2 * np.sqrt(D2 - D1 ** 2 / d), 2 * np.sqrt(D2))] == [11.5, 12.2, 23.0, 24.4]
zc = -T_ * D1 / (2 * D2) + np.sqrt(T_ * (d - D1 ** 2 / D2) * (1 - T_ / (4 * D2))); assert round(100 * zc, 1) == 1.8   # Table 3
t2_mu = {0: {6: [0, 0, -.01, -.03, -.05, -.09, -.14, -.21, -.31, -.43], 8: [0, 0, -.01, -.03, -.06, -.11, -.18, -.26, -.38, -.53],
             10: [0, -.01, -.02, -.05, -.09, -.16, -.25, -.38, -.54, -.76]},
         1: {6: [-.01, -.03, -.06, -.10, -.17, -.25, -.35, -.47, -.63, -.81], 8: [-.01, -.04, -.07, -.13, -.20, -.30, -.43, -.58, -.77, -1.00],
             10: [-.02, -.05, -.10, -.18, -.28, -.42, -.60, -.82, -1.09, -1.42]},
         2: {6: [-.03, -.08, -.15, -.24, -.35, -.48, -.64, -.84, -1.06, -1.32], 8: [-.04, -.10, -.18, -.29, -.42, -.59, -.79, -1.02, -1.30, -1.62],
             10: [-.06, -.14, -.26, -.41, -.60, -.83, -1.11, -1.44, -1.83, -2.28]}}
t2_sig = {0: [-.04, -.14, -.32, -.57, -.88, -1.25, -1.68, -2.16, -2.68, -3.25], 1: [-.18, -.43, -.74, -1.12, -1.55, -2.03, -2.56, -3.13, -3.74, -4.39],
          2: [-.32, -.71, -1.15, -1.65, -2.19, -2.77, -3.40, -4.06, -4.74, -5.46]}
for D1p in (0, 1, 2):                                                                   # Table 2 (drop in mu and in sigma)
    for te in range(1, 11):
        T_ = (te / 100) ** 2; D1 = D1p / 100
        assert abs(-100 * (np.sqrt(sB ** 2 + 2 * np.sqrt(T_ / d) * D1 + T_) - sB) - t2_sig[D1p][te - 1]) < 0.0065
        for sMVp in (6, 8, 10):
            D2 = sB ** 2 - (sMVp / 100) ** 2
            z = -T_ * D1 / (2 * D2) + np.sqrt(T_ * (d - D1 ** 2 / D2) * (1 - T_ / (4 * D2)))
            assert abs(-100 * (np.sqrt(d * T_) - z) - t2_mu[D1p][sMVp][te - 1]) < 0.0095
E3 = np.array([14.7, 5.7, 14.7, 9.8, 8.0]); q3 = np.array([6.6, 17.5, 12.2, 63.7, 0.0]) / 100     # Table 3
xT = np.array([10.5, -10.6, 17.5, -6.7, -10.7]) / 100; xR = np.array([9.8, -13.4, 16.3, -16.8, 4.1]) / 100
assert abs(q3.sum() - 1) < 1e-12 and abs(xT.sum()) < 1e-12 and abs(xR.sum()) < 1e-12
assert round(q3 @ E3, 1) == 10.0 and round(xT @ E3, 1) == 2.0 and round(xR @ E3, 1) == 1.8

# ===== E. Benchmark efficiency (Grinold & Kahn ch. 20; GRS 1989) =====
mu_t = rng.normal(0.05, 0.02, 5); A5 = rng.normal(size=(5, 9)); Sg5 = A5 @ A5.T / 9 * 0.02; b5 = rng.dirichlet(np.ones(5))
SRmax2 = mu_t @ inv(Sg5) @ mu_t; SRB2 = (b5 @ mu_t) ** 2 / (b5 @ Sg5 @ b5)
beta5 = Sg5 @ b5 / (b5 @ Sg5 @ b5); alpha5 = mu_t - beta5 * (b5 @ mu_t)
Res = Sg5 - np.outer(beta5, beta5) * (b5 @ Sg5 @ b5)                                   # residual covariance (singular along b5)
IR2 = alpha5 @ np.linalg.pinv(Res) @ alpha5
assert np.isclose(SRmax2, SRB2 + IR2)                                                   # fn. 8: SR_H^2 = SR_B^2 + IR_H^2 (ex ante)
ex5 = {'AUS': (116, 5.71, 23.42, 12.00, 7.43, 11.73, 7.34, 6.00), 'GER': (67, 3.46, 23.53, 12.00, 11.12, 11.78, 11.09, 1.52),
       'JPN': (148, 6.96, 17.19, 12.00, 7.10, 11.31, 6.89, 8.02), 'UK': (122, 8.70, 18.45, 12.00, 5.02, 11.54, 4.92, 13.44),
       'US': (220, 4.12, 16.65, 12.00, 6.40, 11.79, 6.35, 15.40)}                       # Exhibit 5 rows B and H; Exhibit 6 F
for c, (T, mB, sB_, mH, sH, aH, oH, Fp) in ex5.items():
    SRb, SRh, IRh = mB / sB_, mH / sH, aH / oH
    assert abs(SRh - np.sqrt(SRb ** 2 + IRh ** 2)) < 0.02                               # identity holds in the exhibit data
    F4 = (T - 4 - 1) / 4 * IRh ** 2 / 12 / (1 + SRb ** 2 / 12); F5 = (T - 5 - 1) / 5 * IRh ** 2 / 12 / (1 + SRb ** 2 / 12)
    assert abs(F4 / Fp - 1) < 0.05 and F5 / Fp < 0.82                                  # GKA-1: printed F uses N = 4 (four tilts)
rej4 = rej5 = 0; Tn, Kn = 120, 4                                                         # null simulation: the benchmark is not a test asset
for _ in range(3000):
    rB = rng.normal(0.006, 0.045, Tn); Rt = np.outer(rB, rng.uniform(0.8, 1.2, Kn)) + rng.multivariate_normal(np.zeros(Kn), 0.0004 * (0.5 * np.eye(Kn) + 0.5), Tn)
    X = np.c_[np.ones(Tn), rB]; Bh = np.linalg.lstsq(X, Rt, rcond=None)[0]; res = Rt - X @ Bh; a_h = Bh[0]
    Fst = (Tn - Kn - 1) / Kn * (a_h @ np.linalg.solve(res.T @ res / Tn, a_h)) / (1 + rB.mean() ** 2 / rB.var())
    rej4 += fdist.sf(Fst, Kn, Tn - Kn - 1) < 0.05; rej5 += fdist.sf(Fst * Kn / 5 * (Tn - 6) / (Tn - Kn - 1), 5, Tn - 6) < 0.05
assert abs(rej4 / 3000 - 0.05) < 0.015 and rej5 / 3000 < 0.04                          # N = 4 has the right size; N = 5 under-rejects
assert abs(1.85 * np.sqrt(220 / 12) - 7.92) < 0.01                                      # fn. 12: t = IR x sqrt(years)

print("PASS S4.10 anchors and benchmarks: anchored EPO returns the anchor at w = 1 and for anchor-implied signals at every w; "
      "eq. 21 matches signal risk to anchor risk; centred signals take their level from the anchor; "
      f"60/40 in ASK infeasible (40% ineligible); projections sigma: " + ", ".join(f"{k} {100*v:.1f}%" for k, v in proj.items()) +
      "; household feasibility LP == supply-demand cut condition; Roll eqs. (1)-(4), A.4-A.6 (ROLL-1 sign slip in A-10), fn. 10; "
      "Jorion (B3)-(B6), ellipse (C6) and (C17) by optimisation, Tables 1-3 and Theorems 2a-2d reproduced (sigma_B 13.76%); "
      "GRS identity; Exhibit 6 F uses N = 4 (GKA-1), N = 4 has correct size in simulation")
