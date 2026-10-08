# S4 Equation Register

**Document status:** LIVING (created at S4.5, 2026-10-08; S4.6 and S4.7 entries added 2026-10-08; appended at every Section 2 step; reconciled at S4.19) · **Basis:** S4_PLAN §F (equation checklist), `S4_METHODS_OUTLINE.md` §1 stage 2 · **Verification:** `verification/s45_*.py` (and later steps' scripts)

**What this register is:**
- One entry per equation a roster method needs, with the fields set in the outline: source equation and page, source notation, canonical notation, dimensions, units, assumptions, constraints, parameter authority, limiting cases, numerical tests.
- Entries carry the source's own equation numbers and printed pages. Where a source is internally inconsistent, the register states it and gives the reading we implement (V0 = the source's intended meaning, with the inconsistency recorded).
- Sub-equations (e.g. EQ-H-1a) are supporting results used by verification, diagnostics or later steps. They keep the S4_PLAN §F numbering intact.

**What it is not:**
- Not a contract. Typed contracts are written at S4.20.
- Not a selection. No equation here ranks methods.

---

## 0. Canonical notation (provisional; S4.19 reconciles across all steps)

| Symbol | Meaning | Dimension | Units |
|---|---|---|---|
| N | Number of risky assets in the method's universe (cash excluded unless stated) | scalar | count |
| i, j | Risky-asset index, 1 … N; index 0 = cash | — | — |
| w_t | Risky-asset weights decided at t for the period (t, t+1] | N × 1 | fraction of wealth |
| w_{0,t} | Cash weight, 1 − 1′w_t | scalar | fraction of wealth |
| w̃_t | Weights just before rebalancing at t (drifted from w_{t−1}) | N × 1 | fraction of wealth |
| r_{t+1} | Risky-asset returns in excess of the cash rate over (t, t+1] | N × 1 | decimal per period |
| r_{f,t+1} | Cash (risk-free) rate over (t, t+1] | scalar | decimal per period |
| μ_t, Σ_t | Conditional mean and covariance of r_{t+1} given F_t | N × 1, N × N | per period, per period² |
| σ_{i,t} | √(Σ_t)_{ii} | scalar | per √period |
| 1 | Vector of ones | N × 1 | — |
| F_t | Information available at t; every weight for (t, t+1] must be F_t-measurable | — | — |
| m_{i,t} | Market capitalisation of asset i at t | scalar | currency |

**Conventions:**
- **Risk object.** Σ_t and σ_{i,t} come from the authoritative risk model of the method's problem (universe × horizon × risk object; ADR-0027 D3). The method does not estimate them itself.
- **Units.** Weights are dimensionless. A ratio of variances is unit-free, so annualised and per-period inputs give the same heuristic weights (EQ-H-3 tests this). EQ-H-4's target σ* must use the same horizon unit as σ̂_t.

---

## Index

| ID | Equation | Method(s) | Source | Status |
|---|---|---|---|---|
| EQ-H-1 | Equal weight | PC-A1 | DGU 2009 §1.1, p. 1922 | EXTRACTED · VERIFIED |
| EQ-H-1a | 1/N is mean–variance optimal iff μ ∝ Σ1 | PC-A1 (diagnostic) | DGU 2009 §1.1, p. 1922 | EXTRACTED · VERIFIED |
| EQ-H-1b | Critical estimation window, Proposition 1 | PC-A1 vs sample MV (diagnostic) | DGU 2009 eqs. (18)–(27), pp. 1937–1938 | EXTRACTED · VERIFIED (reproduces the paper) |
| EQ-H-2 | Capitalisation weight | PC-A2 | Convention; Sharpe 1964 states no weighting rule (see entry) | EXTRACTED · VERIFIED |
| EQ-H-2a | Reverse optimisation: μ = λΣw_m ⇔ tangency = w_m; E(R_i) − P = B_im[E(R_m) − P] | PC-A2, links to EQ-BL-1 | Sharpe 1964 fns. 22, 25, 26, pp. 438–441 | EXTRACTED · VERIFIED |
| EQ-H-3 | Volatility timing VT(η) | PC-A3 (η = ½), PC-A4 (η = 1) | Kirby & Ostdiek eq. (14), p. 14 (working version) | EXTRACTED · VERIFIED |
| EQ-H-3a | VT(1) = minimum variance under diagonal Σ | PC-A4 | KO eq. (12), p. 13 | EXTRACTED · VERIFIED |
| EQ-H-4 | Volatility-managed scaling (V0) and the volatility-target engine form (V1) | PC-A5 | Moreira & Muir 2017 eqs. (1)–(2), p. 1616; Tables IV–V, pp. 1625–1626 | EXTRACTED · VERIFIED (V1 decided: S45-D1) |
| EQ-H-4a | Spanning alpha and Sharpe expansion | PC-A5 (diagnostic) | MM eq. (3), p. 1617; p. 1620; eq. (4), p. 1621 | EXTRACTED · VERIFIED |
| EQ-H-T | Turnover including the cash leg | All PC methods (shared) | KO eqs. (5)–(6), p. 6; DGU eq. (15), p. 1929 | EXTRACTED · VERIFIED |
| EQ-MVO-1 | Mean–variance problem: risk form (min variance for a target mean) and utility form (max w′μ − (γ/2)w′Σw); constraint sets | PC-B family, PC-C1 | Markowitz 1952 pp. 81–82; DGU 2009 eqs. (2)–(3), (18); Jorion 1986 eq. (4) | EXTRACTED · VERIFIED (S4.6) |
| EQ-MVO-2 | Budget-only frontier in closed form; two-fund separation | PC-B family | VERIFIED-DERIVATION; constants as in Jorion 1986 Table 1 | EXTRACTED · VERIFIED (S4.6) |
| EQ-MVO-2a | Long-only frontier: piecewise-linear weights (critical lines), piecewise-quadratic variance | PC-B family | Markowitz 1952 p. 87 | EXTRACTED · VERIFIED (S4.6) |
| EQ-MVO-3 | Riskless asset: tangency, capital market line, separation | PC-B1 | Tobin 1958 eqs. (3.21)–(3.25), pp. 83–85; Sharpe 1964 Part III | EXTRACTED · VERIFIED (S4.6) |
| EQ-MVO-3a | Long-only maximum Sharpe via a convex reformulation; failure conditions | PC-B1 | VERIFIED-DERIVATION | EXTRACTED · VERIFIED (S4.6) |
| EQ-MVO-4 | Global minimum variance, closed form | PC-C1 | Jorion 1986 fn. 5, eq. (14); DGNU 2009 eqs. (1)–(2) | EXTRACTED · VERIFIED (S4.6) |
| EQ-MVO-4a | Long-only GMV = unconstrained GMV of a shrunk matrix (Jagannathan–Ma); 1-norm equivalence | PC-C1 | DGNU 2009 eq. (3), Proposition 1, p. 802 | EXTRACTED · VERIFIED (S4.6) |
| EQ-MVO-E1 | Error amplification: relative weight error ≤ κ(Σ) × relative input error | Diagnostic | VERIFIED-DERIVATION; Michaud 1989 (error maximisation) | EXTRACTED · VERIFIED (S4.6) |
| EQ-MVO-E2 | Bayes–Stein expected returns and predictive covariance | Estimator (→ S4.15/S9); diagnostic | Jorion 1986 eqs. (14)–(18), pp. 285–286 | EXTRACTED · VERIFIED (Tables 1–2 reproduced) |
| EQ-MVO-3b | Maximum Sharpe under linear and tracking-error constraints (homogenisation) | PC-B1 | VERIFIED-DERIVATION; G&I 2003 eq. (39), p. 13 | EXTRACTED · VERIFIED (S4.7) |
| EQ-MVO-5 | Problem portfolios: principal components of the correlation matrix | PC-B6/B7; diagnostic | PBL 2021 eqs. (5)–(8), p. 129 | EXTRACTED · VERIFIED (S4.7) |
| EQ-EPO-1 | Shrunk correlation and risk matrices Ω̃, Σ̃, Σ_w | PC-B6/B7 | PBL eqs. (9)–(10), (19), pp. 130, 132 | EXTRACTED · VERIFIED (S4.7) |
| EQ-EPO-2 | General and simple EPO | PC-B6 | PBL eqs. (17), (18), (20), p. 132 | EXTRACTED · VERIFIED (S4.7) |
| EQ-EPO-3 | Anchored EPO with risk-matched γ | PC-B7 | PBL eqs. (21)–(22), p. 133 | EXTRACTED · VERIFIED (S4.7) |
| EQ-EPO-4 | Limits and equivalences: MVO, reverse MVO, Bayesian (BL), robust, ridge | PC-B6/B7 | PBL Props. 1–3, pp. 130–133; proofs pp. 147–148 | EXTRACTED · VERIFIED (S4.7; PBL-1) |
| EQ-EPO-5 | Signal scaling and the fully shrunk portfolio | PC-B6/B7 | PBL eqs. (23)–(27), pp. 136–137 | EXTRACTED · VERIFIED (S4.7) |
| EQ-BL-1 | Equilibrium returns Π = δΣW | PC-B2, CMA-3 | BL 1992 Appendix item 6, p. 42 | EXTRACTED · VERIFIED (S4.4, S4.7) |
| EQ-BL-2 | Posterior mean; full-confidence limit | PC-B2 | BL 1992 Appendix item 8, p. 42; text p. 35 | EXTRACTED · VERIFIED (S4.4, S4.7; BL-2) |
| EQ-BL-3 | Optimisation on the posterior: Σ (BL 1992, Idzorek) vs Σ + M̄⁻¹ (He & Litterman) | PC-B2 | BL 1992 fn. 4, 6, p. 43; S4.4 reproductions | EXTRACTED · VERIFIED (S4.4) |
| EQ-ROB-1 | Uncertainty sets and their regression calibration | PC-B3 | G&I 2003 eqs. (2)–(4), p. 4; (61)–(63), pp. 17–18 | EXTRACTED · VERIFIED (S4.7) |
| EQ-ROB-2 | Robust counterparts: worst cases, robust minimum variance, robust maximum Sharpe | PC-B3 | G&I eqs. (15), (26), (31)–(39), (64)–(68), pp. 7–13, 19–20 | EXTRACTED · VERIFIED (S4.7) |
| EQ-REF-1 | Resampled efficient frontier: resampling, rank association, averaging | PC-B4 | Michaud & Michaud 2008 pp. 37–39, 42–45, 51–52, 56 | EXTRACTED · VERIFIED (S4.7; specification check under D-2) |

---

## EQ-H-1 Equal weight (PC-A1)

- **Source equation and page:** DGU 2009 §1.1, p. 1922: "holding a portfolio weight w^ew_t = 1/N in each of the N risky assets". No equation number. Relative weights are defined in eq. (1), p. 1921: w_t = x_t / |1′_N x_t|.
- **Source notation:** w^ew_t; x_t = weights in the N risky assets, with 1 − 1′x_t in the risk-free asset; R_t = excess returns.
- **Canonical:** w_{i,t} = 1/N, i = 1 … N; w_{0,t} = 0 unless a cash allocation is set outside the method (decision S45-D4).
- **Dimensions:** N × 1. **Units:** fraction of wealth.
- **Assumptions:** none about returns. "Does not involve any optimization or estimation and completely ignores the data" (p. 1922).
- **Constraints:** long-only and fully invested by construction. Policy Statement bounds are not native (post-processing; S4.20).
- **Parameter authority:** no method parameters. N is set by the universe (S5): system/user.
- **Limiting cases:** N = 1 → w = 1. Rebalancing to 1/N each period trades because prices drift (w̃ ≠ 1/N; DGU p. 1929).
- **Numerical tests:** sum, positivity, permutation equivariance; eq. (1) sign preservation (`s45_equal_weight_dgu.py`).

## EQ-H-1a 1/N optimality condition

- **Source:** DGU §1.1, p. 1922: 1/N is the strategy that "does estimate the moments … but imposes the restriction that μ_t ∝ Σ_t 1_N", i.e. expected returns proportional to total risk.
- **Canonical:** Σ^{-1}μ / 1′Σ^{-1}μ = 1/N ⇔ μ = kΣ1, k > 0.
- **Use:** a diagnostic. 1/N is the MV portfolio exactly when the CMA vector is proportional to each asset's covariance with the 1/N portfolio. S4.16 can report how far the CMAs are from this condition.
- **Numerical tests:** 200 random Σ: equality when μ = kΣ1; inequality after a perturbation of μ.

## EQ-H-1b Critical estimation window (DGU Proposition 1)

- **Source equations and pages:**
  - Utility U(x) = x′μ − (γ/2)x′Σx, eq. (18), p. 1937.
  - Expected loss L(x*, x̂) = U(x*) − E[U(x̂)], eq. (21).
  - Critical window M*_mv = inf{M : L_mv < L_ew}, eq. (22), p. 1938.
  - Conditions (23)–(27), p. 1938, with S²* = μ′Σ^{-1}μ and S²_ew = (1′μ)²/1′Σ1:
    - (23) μ unknown, Σ known: S²* − S²_ew − N/M > 0.
    - (24) μ known, Σ unknown: kS²* − S²_ew > 0, with k = (M/(M−N−2))·(2 − M(M−2)/((M−N−1)(M−N−4))) < 1 (eq. 25).
    - (26) both unknown: kS²* − S²_ew − h > 0, with h = NM(M−2)/((M−N−1)(M−N−2)(M−N−4)) (eq. 27).
- **Assumptions:** i.i.d. jointly normal excess returns; μ̂ ~ N(μ, Σ/M) and MΣ̂ ~ W(M−1, Σ), independent (p. 1937); the sample-based MV rule (1/γ)Σ̂^{-1}μ̂. 1/N is compared at its optimal scale.
- **Units:** Sharpe ratios per period (monthly in DGU); M in periods.
- **Domain:** M > N + 4.
- **Use:** a diagnostic only, for S4.6, S4.16 and S7. It is not a method and not a selection rule.
- **Numerical tests (`s45_equal_weight_dgu.py`):**
  - All 15 critical windows stated in the text and abstract are reproduced. Case 3 examples:
    - panel B (S* = 0.40, S_ew = 0.10): 270 / 534 / 1061 months for N = 25 / 50 / 100, vs 270 / 530 / 1060 in the text (p. 1940);
    - panel E (S* = 0.15, S_ew = 0.12): 3239 / 6470, vs "more than 3000" / "more than 6000" (p. 1941) and "around 3000" / "about 6000" (abstract).
  - Monte Carlo (400,000 draws, N = 3, M = 60) of E[U(x̂)] matches (S²* − N/M)/2γ, kS²*/2γ and (kS²* − h)/2γ within 4 standard errors. A 10% error in h would sit about 46 standard errors away.

## EQ-H-2 Capitalisation weight (PC-A2)

- **Source equation and page:** none. ANG cites Sharpe (1964) for "market-cap weight". Sharpe derives the capital market line (Part III, pp. 433–436) and the linear relation between expected return and B_ig for any efficient combination g (fns. 22, 25, 26, pp. 438–441).
  - Sharpe never mentions market capitalisation or a market portfolio.
  - p. 435: the theory "does not imply that all investors will hold the same combination" (fn. 19 sets this against Tobin's unique optimum).
  - The step from the efficient combination g to a capitalisation-weighted portfolio rests on market clearing under homogeneous expectations. That step is not in this source (ANG-43).
- **Canonical:** w_{i,t} = m_{i,t} / Σ_j m_{j,t}, i = 1 … N.
- **Dimensions:** N × 1. **Units:** fraction of wealth (currency units cancel).
- **Assumptions:** capitalisations exist and are measurable for every asset class in the universe. For asset classes they are proxies (index float-adjusted market value, amount outstanding for bonds, and so on), set by the data contract (S6). Cash has no capitalisation in this sense (S45-D4).
- **Constraints:** long-only and fully invested by construction.
- **Parameter authority:**
  - the capitalisation source and proxy per asset class: user-authorised data-contract choice (S45-D3);
  - the numbers: system-estimated data;
  - no agent-selectable parameters.
- **Limiting cases:** between issuance and redemption events, the drifted weights equal the next cap weights, so turnover is zero.
- **Numerical tests (`s45_market_cap.py`):**
  - invariants; invariance to the currency unit;
  - 120 months of buy-and-hold with turnover < 1e-12;
  - an issuance event produces exactly 2g(1 − w_j)/(1 + g) turnover.

## EQ-H-2a Reverse optimisation and Sharpe's linear relation

- **Source:** Sharpe 1964 fn. 25, p. 439: B_ig = −P/(E_Rg − P) + E_Ri/(E_Rg − P), i.e. E(R_i) = P + B_ig[E(R_g) − P], where P = pure rate and B_ig = slope of R_i on R_g. fn. 26 (p. 441): any efficient combination may serve as g.
- **Canonical:** with g = w_m and μ = λΣw_m:
  - Σ^{-1}μ / 1′Σ^{-1}μ = w_m;
  - μ_i = β_im·(w_m′μ), with β_im = (Σw_m)_i / (w_m′Σw_m).
- **Use:** this identity makes PC-A2 the mean–variance portfolio whenever the CMAs equal equilibrium returns. It is the same identity behind Black–Litterman's Π = δΣw_mkt (EQ-BL-1; He & Litterman reproduced at S4.4).
- **Numerical tests:** 200 random (Σ, w_m, λ) cases, exact to 1e-10 (`s45_market_cap.py`).

## EQ-H-3 Volatility timing VT(η) (PC-A3, PC-A4)

- **Source equation and page:** Kirby & Ostdiek eq. (14), printed p. 14 (working version 9 May 2010; the JFQA 2012 version governs, D-3; differences unchecked).
  - Source form: ω̂_it = (1/σ̂²_it)^η / Σ_i (1/σ̂²_it)^η, η ≥ 0.
  - σ̂_it = "estimated conditional volatility of the excess return".
- **Canonical:** w_{i,t} = σ_{i,t}^{−2η} / Σ_j σ_{j,t}^{−2η}.
  - PC-A3 inverse volatility: η = ½.
  - PC-A4 inverse variance: η = 1.
- **Dimensions:** N × 1. **Units:** fraction of wealth; invariant to the variance unit.
- **Assumptions:** only the diagonal of Σ is used. Correlations are ignored by design, "an aggressive form of shrinkage" (p. 14). No μ, no optimisation, no matrix inversion.
- **Constraints:** long-only, fully invested; weights strictly positive.
- **Parameter authority:**
  - η: fixed per method (A3 ½, A4 1; S45-D2);
  - σ_{i,t}: system-estimated, from the diagonal of the authoritative risk model (ADR-0027 D3). KO used 120-month rolling sample variances of monthly excess returns, rebalanced monthly (§3.1, p. 16; §5.1, p. 23). That is their implementation, not a requirement of the method.
- **Limiting cases (p. 14):**
  - η = 0 → 1/N (EQ-H-1);
  - η → ∞ → all weight on the lowest-volatility asset;
  - weight ratio w_i/w_j = (σ_j²/σ_i²)^η.
- **Numerical tests (`s45_volatility_timing_ko.py`):**
  - sum, positivity, permutation equivariance, scale invariance, monotonicity in σ;
  - limits at η = 0 and η = 400;
  - the eq. (13) worked example (p. 14);
  - the cash-degeneracy demonstration for S45-D4: with illustrative volatilities 16/18/6/7/15% and a 0.5%-volatility cash-like asset, A3 puts 80.2% and A4 98.5% in cash.

## EQ-H-3a VT(1) is minimum variance under a diagonal Σ

- **Source:** KO eq. (12), p. 13; eq. (13), p. 14 (N = 2, with correlation ρ).
  - Worked example: σ₁ = σ₂ gives (½, ½). If σ₁ doubles, the weights become (0, 1) at ρ = ½ and (1/5, 4/5) at ρ = 0.
- **Canonical:** argmin_w w′Dw s.t. 1′w = 1, with D = diag(Σ), equals VT(1).
- **Use:** PC-A4 is GMV (PC-C1, S4.11) with the off-diagonals set to zero. This relation feeds S4.11's minimum-variance record and S4.13's risk-dependency inventory (A4 needs only the variances).
- **Numerical tests:**
  - 50 numerical QP solves (SLSQP) agree with VT(1) to 1e-7;
  - eq. (13) reproduces both stated weight vectors;
  - VT(1) equals eq. (13) at ρ = 0.

## EQ-H-4 Volatility-managed scaling (PC-A5)

- **Source equations and pages:** Moreira & Muir 2017.
  - eq. (1), p. 1616: f^σ_{t+1} = (c / σ̂²_t(f)) · f_{t+1}. Here f is the excess return of a buy-and-hold portfolio, and c is chosen "so that the managed portfolio has the same unconditional standard deviation as the buy-and-hold portfolio". c uses the full sample; fn. 6: c does not affect the Sharpe ratio.
  - eq. (2), p. 1616: σ̂²_t = RV²_t = Σ_{d=1/22}^{1} (f_{t+d} − Σ_{d=1/22}^{1} f_{t+d}/22)².
  - Motivation (p. 1616): w*_t ∝ E_t[f_{t+1}]/σ²_t. Volatility "does not predict returns", so inverse variance approximates the conditional risk–return trade-off.
  - Multifactor (eq. 5, p. 1621): the same scaling applied to the in-sample MVE combination b′F_{t+1}, with b static.
- **Source inconsistency (MM-1).**
  - As printed, eq. (2) sums the days t + 1/22, …, t + 1, which are the days of the month being scaled. The text says "the previous month's realized variance" (p. 1616), and a real-time strategy requires F_t-measurability.
  - **V0 (implemented) = the text's meaning:** RV² of month t's 22 daily returns scales month t+1.
  - The literal reading is look-ahead (`s45_volatility_managed_mm.py` shows the weight moving with the scaled month's own data).
- **Variants reported by MM** (market portfolio; Table IV, p. 1625; Table V, p. 1626; |Δw| = average absolute monthly weight change; α in % p.a.):

  | Weight | Description | \|Δw\| | α Table IV | α Table V | Break-even cost | Sharpe | Weights P50 / P99 |
  |---|---|---|---|---|---|---|---|
  | c/RV²_t | Baseline | 0.73 | 4.86 | 4.86 | 56 bp | 0.52 | 0.93 / 6.39 |
  | c/RV_t | Realized vol | 0.38 | 3.85 | 3.30 | 84 bp | 0.53 | 1.23 / 3.36 |
  | c/E_t[RV²_{t+1}] | AR(1) on log variance | 0.37 | 3.30 | 3.85 | 74 bp | 0.51 | 1.11 / 4.58 |
  | min(c/RV²_t, 1) | No leverage | 0.16 | 2.12 | 2.12 | 110 bp | 0.52 | 0.93 / 1 |
  | min(c/RV²_t, 1.5) | — | 0.16 | 3.10 | 3.10 | 161 bp | 0.53 | 0.93 / 1.5 |

  - **MM-2 (source inconsistency):** the α values of the 1/RV and expected-variance rows are swapped between Table IV and Table V. The data needed to tell which is right are not in hand. Not material to our specification, because no α is used as a parameter.
  - **c in the capped variants:** not stated in the text. Table V's P50 of 0.93 for both capped variants equals the baseline's, which implies the baseline c is used before capping.
- **Engine form V1 (owner decision S45-D1, 2026-10-08):** for a base portfolio b (1′b = 1, long-only):
  - risky scale s_t = min(σ* / σ̂_t(b), L);
  - weights w_t = s_t·b, cash w_{0,t} = 1 − s_t.
  - σ̂_t(b) = √(b′Σ̂_t b) is the ex-ante volatility of b from the short-horizon authoritative risk model (ADR-0027 D3).
  - With L ≤ 1, cash is non-negative.
  - Compared with V0, V1 makes three changes:
    1. 1/σ instead of 1/σ², so ex-ante volatility equals σ* whenever the cap does not bind;
    2. an ex-ante target in place of the ex-post c;
    3. a leverage cap with a cash residual.
- **Dimensions:** s_t scalar; w_t N × 1. **Units:** σ* and σ̂_t on the same horizon (e.g. annualised).
- **Assumptions:**
  - V0: volatility is persistent and does not predict returns (p. 1617).
  - V1: the same, plus a declared risk target.
- **Constraints:** with L ≤ 1, long-only plus cash. Policy Statement asset bounds apply to s_t·b, so post-processing is needed if the bounds bind (S4.20).
- **Parameter authority (V1):**
  - σ*: system-estimated, the long-run volatility of b from the long-horizon risk problem (S45-D1). *[2026-10-08]* The draft classed σ* as user-authorised; the owner accepted the system-estimated target. The Policy Statement's risk controls (`S2_RISK_PREFERENCE_RESEARCH.md`; `INV.volatility_range`) apply to the final portfolio, not inside A5.
  - L: user-authorised, min(1, effective `POL.leverage` maximum) (narrowed by account capability, FX-06 / FX2-18).
  - b: A2 market cap; A1 as the declared fallback while S45-D3 is open (S45-D1).
  - σ̂_t: system-estimated (risk model).
  - Exponent (1 vs 2): S45-D1.
  - Rebalancing frequency: S13.
  - Nothing is agent-selectable.
- **Limiting cases:**
  - σ̂_t constant → constant exposure (A5 = scaled b);
  - L → ∞ with exponent 2 → MM V0;
  - cap binding in calm periods → ex-ante volatility L·σ̂_t < σ*.
- **Numerical tests (`s45_volatility_managed_mm.py`; synthetic daily data with persistent stochastic volatility):**
  - c ex post gives sd(f^σ) = sd(f);
  - fn. 6 invariance;
  - no look-ahead in V0, and the literal eq. (2) fails;
  - Table IV variants well defined; the inverse-variance leverage tail is heavier than inverse volatility's (P99/P50 7.6 vs 2.8 here; Table V gives 6.39/0.93 = 6.9 vs 3.36/1.23 = 2.7);
  - oracle-volatility check (400,000 periods): under 1/σ scaling, risk is the same in high- and low-volatility terciles (ratio 1.000). Under 1/σ², the ratio is 0.43, so risk falls when volatility rises. Sharpe ordering 1/σ² > 1/σ > unscaled when the mean is constant;
  - V1: weights in [0, L], cash ≥ 0, and realised volatility σ* (±2%) where the cap does not bind.

## EQ-H-4a Spanning alpha and Sharpe expansion (diagnostic)

- **Source:**
  - eq. (3), p. 1617: f^σ_{t+1} = α + βf_{t+1} + ε_{t+1};
  - p. 1620: SR_new = √(SR²_old + (α/σ_ε)²);
  - eq. (4), p. 1621: ΔU_MV = (SR²_new − SR²_old)/SR²_old;
  - annualisation: monthly appraisal ratio × √12 (fn. 11).
- **Published example:** scaled momentum, α = 12.5, RMSE "around 50", appraisal 0.875 (p. 1620). This implies RMSE = 12.5·√12/0.875 = 49.5, consistent.
- **Use:** in-sample diagnostic for S4.16 and S7. Not a selection rule (I-9).
- **Numerical tests:** the identity holds exactly in sample with consistent (ddof = 0) moments. On the synthetic series: SR 0.19 → 0.35 annualised (synthetic, not evidence).

## EQ-H-T Turnover including the cash leg (shared)

- **Source:**
  - KO eq. (5), p. 6: w̃_{i,t} = ω_{i,t−1}(1 + R_{i,t}) / [Σ_i ω_{i,t−1}(1 + R_{i,t}) + (1 − Σ_i ω_{i,t−1})(1 + R_{f,t})].
  - KO eq. (6): τ_t = Σ_i |ω_{i,t} − w̃_{i,t}| + |Σ_i (ω_{i,t} − w̃_{i,t})|.
  - DGU eq. (15), p. 1929: average Σ_j |ŵ_{j,t+1} − ŵ_{j,t+}| over risky assets.
- **Canonical:** τ_t = Σ_{i=0}^{N} |w_{i,t} − w̃_{i,t}|, cash included as i = 0.
- **Identity (verified):**
  - KO's second term equals the change in the cash weight, so KO eq. (6) is the canonical form.
  - For fully invested portfolios the cash term is zero and KO equals DGU.
  - For PC-A5 the cash leg is material and must be counted.
- **Units:** fraction of wealth traded per rebalancing (one-way plus the other side; no halving).
- **Numerical tests:** 200 random cases each, fully invested and with cash (`s45_volatility_timing_ko.py`).

---

## S4.6 entries — mean–variance foundation

Notation: μ = expected returns in excess of the cash rate r_f (decision S46-D1); μ_raw = μ + r_f·1 where a raw form is needed. With Σ invertible: A = 1′Σ⁻¹1, B = 1′Σ⁻¹μ_raw, C = μ_raw′Σ⁻¹μ_raw, D = AC − B² > 0 (Jorion's c, b, a; his d(Y₀) = D/A).

## EQ-MVO-1 The mean–variance problem

- **Source equations and pages:**
  - Markowitz 1952: E = Σ X_i μ_i, V = Σ Σ σ_ij X_i X_j, Σ X_i = 1, **X_i ≥ 0** ("we will exclude negative values of the X_i (i.e., short sales)", p. 81). Efficient = "minimum V for given E or more and maximum E for given V or less" (p. 82). Inputs may be "aggregates such as, say, bonds, stocks and real estate" (p. 91).
  - Utility form: DGU eqs. (2)–(3), p. 1922, and eq. (18), p. 1937: max x′μ − (γ/2)x′Σx; Jorion eq. (4), p. 282 (derived utility of mean and variance).
- **Canonical:**
  - risk form: min_w w′Σw s.t. w′μ_raw = m, 1′w = 1, w ∈ 𝒲;
  - utility form: max_w w′μ − (γ/2)w′Σw s.t. 1′w = 1, w ∈ 𝒲;
  - 𝒲 = the Policy Statement constraint set (bounds, group limits, long-only), applied natively as linear constraints.
- **Dimensions / units:** w N × 1 (fraction of wealth); μ per period; Σ per period²; γ per period⁻¹ (scale-dependent: γ's value depends on the units of μ and Σ).
- **Assumptions:** preferences over mean and variance only (Markowitz p. 89–90 discusses the third moment); moments treated as known (the certainty-equivalence step criticised by Jorion pp. 279–281).
- **Parameter authority:**
  - 𝒲: user-authorised (Policy Statement);
  - m or a target volatility, where the risk form is used: user-authorised or derived by a declared rule (per method, S4.7);
  - γ: system-estimated by an accepted calibration method, specific to this formulation and its units (`S2_RISK_PREFERENCE_RESEARCH.md`: model γ is "D (derived)", never a portable investor attribute; RQ-02).
- **Limiting cases:** γ → ∞ gives GMV (EQ-MVO-4); m = m_g gives GMV.
- **Numerical tests:** the utility form lies on the risk-form frontier at m = B/A + D/(Aγ) (`s46_mvo_closed_forms.py`).

## EQ-MVO-2 Budget-only frontier; two-fund separation

- **Source:** derivation (`VERIFIED-DERIVATION`). The constants A, B, C, D are Jorion's "efficient set statistics" (Table 1, p. 287).
- **Canonical:**
  - w(m) = [(C − Bm)Σ⁻¹1 + (Am − B)Σ⁻¹μ_raw] / D;
  - σ²(m) = (Am² − 2Bm + C)/D, a parabola in (m, σ²), i.e. a hyperbola in (σ, m);
  - any two distinct frontier portfolios span the frontier: w(m₃) = αw(m₁) + (1 − α)w(m₂), with α = (m₃ − m₂)/(m₁ − m₂).
- **Assumptions:** Σ positive definite; short sales allowed; no riskless asset.
- **Numerical tests:** 40 random problems × 5 targets agree with SLSQP to 1e-6; the variance identity is exact; two-fund spanning.

## EQ-MVO-2a Long-only frontier: critical lines

- **Source:** Markowitz 1952 p. 87: "The efficient set in the 4 security case is, as in the 3 security and also the N security case, a series of connected line segments", and "if we plotted V against E for efficient portfolios we would again get a series of connected parabola segments"; fn. 10 (p. 87) sketches tracing the set along critical lines.
- **Canonical:** w(m) is piecewise linear in m between corner portfolios, where the set of non-zero weights changes; σ²(m) is piecewise quadratic.
- **Numerical tests:** 121 QP solutions along the long-only frontier of a 6-asset problem. Within each active set the weights are exactly linear in m (second differences ≤ 1e-5); 3 corners here.

## EQ-MVO-3 Riskless asset: tangency, capital market line, separation

- **Source equations and pages:**
  - Tobin 1958 §3.6: dominant sets solve [v_ij][x_i] = [λr_i] (eq. 3.22, p. 83). "All dominant sets lie on a ray from the origin" (p. 83). "The proportionate composition of the non-cash assets is independent of their aggregate share of the investment balance" (p. 84). The opportunity locus is a line, eqs. (3.23)–(3.25), p. 84.
  - The analysis is "applicable only so long as cash is assumed to be a riskless asset"; without one, the locus is "a hyperbola rather than a line" (pp. 84–85).
  - Tobin's cash yields zero, so his r_i are returns in excess of cash.
  - Sharpe 1964 Part III: the capital market line with borrowing and lending at the pure rate.
- **Canonical:**
  - w_tan = Σ⁻¹μ / 1′Σ⁻¹μ;
  - SR_max = √(μ′Σ⁻¹μ);
  - with risk aversion γ: risky holdings x = Σ⁻¹μ/γ, cash 1 − 1′x; x/1′x = w_tan for every γ (separation).
- **r_f (owner decision S46-D1, 2026-10-08):** the after-tax per-period rate on uninvested cash at the best liquid deposit available to the user, otherwise the broker's cash rate; same tax and currency basis as μ. Borrowing uses a separate rate (kinked frontier).
- **Conditions:** 1′Σ⁻¹μ > 0, equivalently r_f < m_g = B/A. Otherwise the formula returns a portfolio with negative expected excess return (the lower branch), and a maximum-Sharpe method must emit a failure record (`TANGENCY_UNDEFINED`, provisional), not a weight vector.
- **Source note:** Tobin assumes x_i ≥ 0 (p. 82) but solves the equality system (3.22), which can give negative holdings; Sharpe (1964, fn. 15) points this out. The long-only case is EQ-MVO-3a.
- **Numerical tests:**
  - 40 random problems: w_tan equals numerical maximum-Sharpe (3 starts) and attains √(μ′Σ⁻¹μ);
  - the tangency lies on the EQ-MVO-2 hyperbola;
  - separation holds for γ ∈ {2, 5, 20};
  - the r_f > m_g case yields negative expected excess return.

## EQ-MVO-3a Long-only maximum Sharpe ratio

- **Source:** derivation (`VERIFIED-DERIVATION`): homogeneity of the Sharpe ratio allows the substitution y = w/κ.
- **Canonical:** min_y y′Σy s.t. μ′y = 1, y ≥ 0 (plus homogenised linear constraints); w = y/1′y.
- **Conditions:** feasible only if some μ_i > 0; otherwise a failure record (`NO_POSITIVE_EXCESS_RETURN`, provisional).
- **Numerical tests:** 30 problems with mixed-sign μ; the convex solution's Sharpe ratio ≥ the best of 5 direct SLSQP maximisations, with weights agreeing to 2e-3.

## EQ-MVO-4 Global minimum variance

- **Source:**
  - Jorion 1986 eq. (14) and fn. 5 (p. 285): Y₀ is "the average return for the minimum variance portfolio"; the weights "minimize the variance … subject to the condition that they sum to one".
  - DGNU 2009 eqs. (1)–(2), p. 801.
- **Canonical:** w_g = Σ⁻¹1 / 1′Σ⁻¹1; σ²_g = 1/A; m_g = B/A. Independent of μ.
- **Numerical tests:** closed form = SLSQP to 1e-6; σ²_g = 1/A exactly.

## EQ-MVO-4a Long-only GMV as covariance shrinkage

- **Source:** DGNU 2009 p. 802, restating Jagannathan & Ma (2003): the short-sale-constrained GMV "coincides with the solution to the unconstrained problem … if the sample covariance matrix … is replaced by Σ_JM = Σ − λ1′ − 1λ′" (eq. 3), with λ ≥ 0 the short-sale multipliers. Proposition 1 (p. 802): the 1-norm-constrained GMV with δ = 1 equals the short-sale-constrained GMV. J&M 2003 itself is not in hand (`S4_0_SOURCE_INVENTORY.md`).
- **Canonical (multiplier scale for the objective w′Σw):** λ = Σw* − σ*²·1 ≥ 0, with λ_i w*_i = 0; then Σ_JM w* = σ*²·1, so w* ∝ Σ_JM⁻¹1 when Σ_JM is invertible.
- **Use:** explains why long-only constraints regularise (`S4_RISK_MODEL_CHOICE.md` M-1 finding 3). Relevant to S4.11's GMV record.
- **Numerical tests:** 40 problems: KKT dual feasibility and complementary slackness; Σ_JM w* = σ*²·1; GMV(Σ_JM) = w* to 1e-5; the 1-norm (δ = 1) solution = the long-only solution to 1e-4.

## EQ-MVO-E1 Error amplification by the condition number

- **Source:** linear algebra (`VERIFIED-DERIVATION`). It quantifies Michaud's (1989) "error maximisation" (p. 31) for the unconstrained solution x = Σ⁻¹μ.
- **Canonical:** ‖δx‖/‖x‖ ≤ κ(Σ)·‖δμ‖/‖μ‖, with κ = λ_max/λ_min. The bound is attained with μ along the top eigenvector and δμ along the bottom one.
- **Use:** a CRO diagnostic (S4.16): report κ of the Σ used by μ-dependent methods. This connects to EPO's "problem portfolios" (PBL 2021 p. 125; EQ-MVO-5 at S4.7).
- **Numerical tests:** κ ∈ {10, 10³, 10⁵}: the bound holds in 200 random perturbations each and is attained to 1e-6.

## EQ-MVO-E2 Bayes–Stein expected returns (Jorion 1986)

- **Source equations and pages:**
  - eq. (14), p. 285: E[r] = (1 − w)Ȳ + w·1Y₀, with w = λ/(T + λ) and Y₀ = 1′Σ⁻¹Ȳ / 1′Σ⁻¹1 (the GMV mean);
  - eq. (15): V[r] = Σ(1 + 1/(T + λ)) + λ/(T(T + 1 + λ))·11′/(1′Σ⁻¹1);
  - eq. (16), p. 285: diffuse prior, E[r] = Ȳ, V[r] = Σ(1 + 1/T);
  - eq. (17), p. 286: ŵ = (N + 2) / ((N + 2) + T(Ȳ − 1Y₀)′Σ⁻¹(Ȳ − 1Y₀));
  - eq. (18): Σ̂ = (T − 1)/(T − N − 2)·S.
- **Assumptions:** i.i.d. normal returns; Σ estimated (eq. 18); T > N + 2.
- **Conventions that reproduce Table 2 (INFERENCE from the reproduction):** eq. (18) is applied in both the diffuse and Bayes–Stein rules; λ̂ = Tŵ/(1 − ŵ); negative exponential utility with risk tolerance 52.2%/12 per month (A = 12/52.2 per %), weights summing to one.
- **Use:** documents how estimation error in μ costs utility and how shrinkage toward the GMV mean recovers it. It is a candidate **expected-return estimator** (type M.CMA), so it belongs to S4.15/S9, not to the PC library.
- **Numerical tests (`s46_estimation_error_jorion.py`):**
  - Table 1 statistics: c 0.11836 (0.11838), b 0.0953, Y₀ 0.805, a 0.15849, d 0.08176 (0.08171);
  - F_MAX 0.99728 vs 0.99734;
  - Table 2 at T = 25 / 50 / 100 / 200: all 15 testable risk cells within 1.7 of the paper's Monte Carlo standard errors (K = 1,000); the shrinkage mean within 2.5 SE (largest deviation at T = 200: 0.309 vs 0.316);
  - the orderings stated on p. 288 hold (Bayes–Stein < diffuse < certainty equivalence; minimum variance best at small T and worst at T = 200).

---

## S4.7 entries — mean–variance family

## EQ-MVO-3b Maximum Sharpe under Policy Statement constraints

- **Source:** derivation (`VERIFIED-DERIVATION`); the same homogenisation is used by G&I 2003 eq. (39), p. 13, and recommended in `S4_GITHUB_IMPL_REVIEW.md` §7.
- **Canonical:** max μ′x/√(x′Σx) s.t. 1′x = 1, l ≤ x ≤ u, Gx ≤ h, √((x − b)′Σ(x − b)) ≤ TE ⟺ min y′Σy s.t. μ′y = 1, 1′y = κ, lκ ≤ y ≤ uκ, Gy ≤ hκ, √((y − κb)′Σ(y − κb)) ≤ κ·TE, κ ≥ 0; x = y/κ. Every constraint is linear or a second-order cone, so the problem is convex.
- **Failure:** infeasible when no feasible portfolio has positive excess return (`NO_POSITIVE_EXCESS_RETURN`).
- **Numerical tests (`s47_max_sharpe.py`):** 25 problems with caps, a group limit and a tracking-error budget (tracking error binding in 16, caps in 8, group in 3): the convex solution equals multi-start direct maximisation (Sharpe ratios equal to 8 decimals).

## EQ-MVO-5 Problem portfolios

- **Source:** PBL 2021 eqs. (5)–(8), p. 129. Ω = PDP′ (correlation matrix); PC portfolios of unit-volatility assets; z_MVO = D⁻¹s^P/γ, so the risk in PC i is its Sharpe ratio times the leverage 1/√D_i.
- **Use:** explains error amplification in MVO (links EQ-MVO-E1): the least important PCs have underestimated risk and noisy Sharpe ratios, and get the largest leveraged bets. Diagnostic for S4.16.
- **Numerical tests:** the PC-space solution maps back to Σ⁻¹s/γ exactly (`s47_epo_pbl.py`).

## EQ-EPO-1 Shrunk risk matrices

- **Source:** PBL eqs. (9)–(10), p. 130: D̃ = (1 − θ)D + θI ⟺ Ω̃ = (1 − θ)Ω + θI, Σ̃ = σΩ̃σ. eq. (19), p. 132: Σ_w = (1 − w)Σ̃ + wV = σ[(1 − w)Ω̃ + wI]σ, V = diag of variances.
- **Canonical property (verified):** applying θ and then w multiplies every correlation by (1 − θ)(1 − w).
- **PBL's choices:** θ = 5% in most samples (Table 1, p. 135; Global 2: Ω̃ = 0.95Ω + 0.05I), or a random-matrix-theory estimate (Global 3).

## EQ-EPO-2 General and simple EPO

- **Source:** eq. (17) EPO = (1/γ)(τΣ̃ + Λ)⁻¹(τs + γΛa); with Λ = λV and w = λ/(τ + λ): eq. (18) EPO(w) = Σ_w⁻¹[(1 − w)s/γ + wVa]; with a = V⁻¹s/γ: eq. (20) EPO^s(w) = Σ_w⁻¹s/γ (all p. 132).
- **Limits:** w = 0 → MVO on Σ̃; w = 1 → V⁻¹s/γ (diagonal MVO; with a TSMOM-type signal this is equal-volatility weighting, eq. 27).
- **Units:** s must be in expected-excess-return units for a meaningful γ; the simple EPO's Sharpe ratio does not depend on γ (p. 132).
- **w selection in PBL:** "for each time period, we estimated what choice of w (within a finite grid of possible values) would have produced the highest EPO portfolio Sharpe ratio in the time period up until that date. Then, we used this estimate in the next time period" (Figure 2 notes, p. 138); at least 15 years of data before the first choice (Table 1 notes). The grid is not stated (PBL-2).

## EQ-EPO-3 Anchored EPO

- **Source:** eqs. (21)–(22), p. 133: γ = √(s′Σ_w⁻¹Σ̃Σ_w⁻¹s)/√(a′Σ̃a), which equalises the Σ̃-variance of Σ_w⁻¹s/γ and of the anchor a; EPO^a(w) = Σ_w⁻¹[(1 − w)·(√(a′Σ̃a)/√(s′Σ_w⁻¹Σ̃Σ_w⁻¹s))·s + wVa].
- **Limits (verified):** w = 1 → the anchor a; w = 0 → the MVO portfolio scaled to the anchor's risk.
- **PBL's anchors:** 1/N (Equity 6) and 1/σ (Equity 7), Table 1.

## EQ-EPO-4 Limits and equivalences

- **Source:** Prop. 1, eq. (13)–(14), p. 131 (Bayesian posterior with prior μ ~ N(γΣa, τΣ), s|μ ~ N(μ, Λ)); Prop. 2, eqs. (15)–(16) (robust optimisation with an ellipsoidal set for μ); Prop. 3, p. 133 (MVO; reverse MVO; Black–Litterman with Π = γΣa, Q = s, P = I, Ω = Λ; robust; generalised ridge), proofs pp. 147–148 (Tikhonov, Lavrentiev).
- **PBL-1 (boundary qualification, verified):** Prop. 2 states that the solutions for c ∈ (0, ∞) equal those for τ ∈ (0, ∞). The robust objective has a kink at x = a; for c ≥ c* = √((s − γΣa)′Λ⁻¹(s − γΣa)) the robust solution is exactly the anchor, which corresponds to τ = 0 (Prop. 3 part 2), outside (0, ∞). For c < c* the correspondence holds.
- **Numerical tests (`s47_epo_pbl.py`):** all equivalences to 1e-8; Prop. 2 in 30 cases below c* and 18 at or above it.

## EQ-EPO-5 Signal scaling

- **Source:** eq. (23) TSMOM s_i = 0.1σ_i·sign(r_{12}); eqs. (24)–(26) XSMOM and its volatility-scaled variants; eq. (27) the fully shrunk EPO weight s_i/(γσ_i²) (pp. 136–137); γ_t = n_t/40% for TSMOM so that w = 1 reproduces the TSMOM factor.
- **Use:** links to S4.8 (signals) and S4.9 (signal × PC compatibility).

## EQ-BL-1 Equilibrium returns

- **Source:** BL 1992 Appendix item 6, p. 42: Π = δΣW, with W = market-capitalisation weights (items 2–3; currencies via the universal-hedging constant λ).
- **Canonical:** Π = δΣw_mkt; reverse optimisation (δΣ)⁻¹Π = w_mkt (EQ-H-2a).
- **Inputs:** w_mkt from PC-A2 data (S45-D3); δ system-estimated (S4.15/S9).

## EQ-BL-2 Posterior

- **Source:** item 7: prior centred on Π with covariance τΣ; views PE[R] = Q + ε, ε ~ N(0, Ω), **Ω diagonal**. Item 8: E[R]‾ = [(τΣ)⁻¹ + P′Ω⁻¹P]⁻¹[(τΣ)⁻¹Π + P′Ω⁻¹Q]. Text p. 35: with 100% confidence, Π + τΣP′(PτΣP′)⁻¹(Q − PΠ).
- **BL-2 (misprint):** item 8 is printed "[(τΣ⁻¹Π + P′Ω⁻¹Q]" with an unbalanced parenthesis. Read literally (τ·Σ⁻¹·Π) it gives τ²Π with no views instead of Π; the intended term is (τΣ)⁻¹Π.
- **Properties (verified, `s47_black_litterman.py`):** no-view and consistent-view limits; the full-confidence limit satisfies the views exactly; **when Ω is proportional to τ** (He & Litterman's τ·diag(PΣP′); Idzorek's (1 − C)/C·τ·pΣp′), τ cancels from the posterior mean.

## EQ-BL-3 Optimisation on the posterior

- **Source:** BL 1992 treats covariances as known (fn. 4, p. 43) and optimises with Σ; portfolios are scaled to the equilibrium portfolio's risk, 10.7% (fn. 6, p. 43). He & Litterman use Σ + M̄⁻¹ (BL-1, S4.4); Idzorek uses Σ.
- **Use:** decision S47-D1.

## EQ-ROB-1 Uncertainty sets

- **Source:** G&I 2003 model (1), p. 3: r = μ + V′f + ε. (2) S_d: d_i ∈ [d̲_i, d̄_i]; (3) S_v: V = V₀ + W, ‖W_i‖_G ≤ ρ_i; (4) S_m: |μ_i − μ₀,i| ≤ γ_i (p. 4).
- **Calibration (§5, pp. 17–18):** from a factor regression over p periods with design A = [1 B′]: γ_i = √((AᵀA)⁻¹₁₁·c₁(ω)·s_i²), ρ_i = √(m·c_m(ω)·s_i²), G = (Q(AᵀA)⁻¹Qᵀ)⁻¹, with c_J(ω) the ω-quantile of F(J, p − m − 1); d̄_i from a bootstrap or any worst-case residual-variance estimate. "The typical choices of ω lie in the range 0.95–0.99" (p. 18).
- **Numerical tests:** simulated coverage 0.950 / 0.949 for ω = 0.95.

## EQ-ROB-2 Robust counterparts

- **Worst cases:** mean μ₀′φ − γ′|φ| (eq. 15); residual variance φ′D̄φ; factor variance max over ‖y‖_G ≤ ρ′|φ| of ‖V₀φ + y‖²_F = min over 0 < σ < 1/λ_max(H) of r²/σ + Σw_i²/(1 − σλ_i) (Lemma 1, eq. 26, pp. 8–9); if F = κG, the worst-case factor st. dev. is ‖F^½V₀φ‖ + √κ·ρ′|φ| (eqs. 64–67, pp. 19–20).
- **Problems:** robust minimum variance (6), (31)–(32), p. 11; robust maximum return (7), (33)–(34); robust maximum Sharpe (8), (35)–(37), p. 12, with general linear constraints (38)–(39), p. 13 (homogenised as in EQ-MVO-3b). The paper assumes long-only after p. 11.
- **Numerical tests (`s47_robust_mv.py`):** vertex enumeration for (15); Lemma 1 = brute force over the ellipsoid; F = κG closed form; robust minimum variance = Markowitz at zero uncertainty; its worst case is a valid bound and beats the classical portfolio's worst case (8 cases, 0.4–4.2%); robust maximum Sharpe homogenisation = direct maximisation (6 cases).

## EQ-REF-1 Resampled efficient frontier

- **Source:** Michaud & Michaud 2008.
  - Procedure (pp. 37–38): simulate T periods from the inputs; re-estimate means and covariances; compute 51 efficient portfolios equally spaced in return from minimum variance to maximum return under the same constraints; repeat (500 replications in the text).
  - RE portfolio (pp. 42–44, fn. 4): average of rank-associated portfolios; App. A (p. 56): λ-association by quadratic utility, "slightly less statistically stable than rank-association".
  - fn. 7 (p. 44): RE maximum-return weights = probability that each asset is the maximum-return asset.
  - The number of simulated observations is "a free parameter" modelling forecast confidence (pp. 51–52; the Forecast Confidence level is patent pending, fn. 30). RE optimisation is patented with an exclusive licensee (p. 42, fn. 1) → D-2.
- **Numerical tests (`s47_resampled_frontier.py`, specification check under D-2):**
  - classical Table 5.1 maximum Sharpe within 0.6 pp, and minimum variance;
  - unbounded maximum Sharpe 0.2538 vs 0.253, which input rounding alone moves between 0.245 and 0.264;
  - Table 6.1 RE minimum-variance / middle / maximum-return portfolios within 0.7 / 1.6 / 3.0 pp (500 replications, T = 216);
  - the fn. 7 identity; all 51 RE portfolios below the classical frontier; long simulated samples approach MV.
- **MCH-1 (under-specification):** Table 6.1's "middle" portfolio is not defined. The printed MV middle is efficient on our frontier at rank 24 of 51, not at the return midpoint (rank 26). The printed inputs also tie France and Japan at 0.88, so the classical maximum-return portfolio is not unique in the rounded data (the book shows 100% France).

