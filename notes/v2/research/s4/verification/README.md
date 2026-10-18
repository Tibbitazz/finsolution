# S4 verification area

**Document status:** STABLE (established at S4.0, 2026-10-02) · **Basis:** ADR-0024 §8 (OD-5)

**Contents:** mathematical verification and reference implementations for S4 only:
- equation verification;
- source reproduction;
- limiting-case tests;
- synthetic examples;
- invariants;
- reference outputs;
- numerical comparison.

**Rules:**
- **Not production code.** The developer chooses the production implementation after receiving the Method Contracts (S4.20). Reference outputs here serve as test oracles.
- **Language:** Python (numpy/scipy). The packages available today do not determine the production architecture. A method that needs convex optimisation is not avoided because a solver is not installed here.
- **Synthetic data only.** No personal data, ever.
- **No performance-driven selection.** Results here verify that a method matches its mathematical specification. They never rank methods (performance evaluation belongs to S7).
- **Empty at S4.0.** Code is added from S4.5 onward.
- *[2026-10-08, S4.4]* **Source-reproduction scripts added ahead of S4.5** (owner request to review the six supplied papers in depth). Each script is self-asserting and prints `PASS`. Run with `python3 <script>` (numpy, scipy, pandas):

  | Script | Reproduces | Method |
  |---|---|---|
  | `s44_black_litterman_he_litterman.py` | He & Litterman: Π (Table 2), Tables 4–8, eq. (17) = eq. (13), Ω = τ·diag(PΣP′) | PC-B2 |
  | `s44_black_litterman_idzorek.py` | Idzorek: λ, Tables 4/6/7; closed-form ω = (1−C)/C·τ·pΣp′ equals the paper's numerical step 6 | PC-B2 |
  | `s44_risk_parity_spinu.py` | Spinu: Newton algorithm (Thm 3.4), iteration bound at N = 50; Maillard–Roncalli–Teïletche volatility ordering | PC-C2 |
  | `s44_hrp_lopez_de_prado.py` | López de Prado: Exhibit 7 exactly (seed 12345); order-dependence of published HRP; order-invariant tree-split variant | PC-C3 |
  | `s44_drawdown_cdd.py` | Chekhlov–Uryasev–Zabarankin: CV@R definition = LP (25) = knapsack (30) = path LP (31); MaxDD/AvDD limits; LP (55) exact and infeasible case | PC-D2 |
  | `s44_cvar_budgets_bcp.py` | Boudt–Carl–Peterson: Iq identity, Gaussian limit, Euler allocation, Prop. (15), MCC % contributions | PC-D3 |
- *[2026-10-08, S4.5]* **Heuristic-method scripts** (`S4_HEURISTICS.md`; equations in `S4_EQUATION_REGISTER.md`):

  | Script | Reproduces / proves | Method |
  |---|---|---|
  | `s45_equal_weight_dgu.py` | DGU: 1/N invariants; μ ∝ Σ1 optimality; Proposition 1, all 15 stated critical windows; Monte Carlo of the expected-utility terms | PC-A1 |
  | `s45_market_cap.py` | Cap-weight invariants; zero turnover between issuance events; reverse optimisation; Sharpe (1964) linear relation | PC-A2 |
  | `s45_volatility_timing_ko.py` | Kirby–Ostdiek VT(η): limits, invariants, eq. (12) by QP, eq. (13) example, A3 = ERC iff equal correlations, turnover eq. (6) vs DGU eq. (15), cash degeneracy | PC-A3, PC-A4 |
  | `s45_volatility_managed_mm.py` | Moreira–Muir: eq. (1) with ex-post c, fn. 6, no look-ahead (MM-1), appraisal identity, Table IV variants, 1/σ vs 1/σ², the V1 engine form | PC-A5 |
- *[2026-10-08, S4.6]* **Mean–variance foundation scripts** (`S4_MVO_FOUNDATION.md`):

  | Script | Reproduces / proves | Method |
  |---|---|---|
  | `s46_mvo_closed_forms.py` | GMV, frontier, two-fund separation, utility form, tangency and Tobin separation, long-only maximum Sharpe (convex form), Markowitz critical lines, Jagannathan–Ma via KKT, DGNU Prop. 1, condition-number bound, cash in Σ | PC-B1, PC-C1 (foundation) |
  | `s46_estimation_error_jorion.py` | Jorion (1986) Table 1 statistics and Table 2 risk functions and shrinkage factors within the paper's Monte Carlo error | Estimation error; Bayes–Stein |
- *[2026-10-08, S4.7]* **Mean–variance family scripts** (`S4_MVO_FAMILY.md`):

  | Script | Reproduces / proves | Method |
  |---|---|---|
  | `s47_max_sharpe.py` | Constrained maximum Sharpe via homogenisation (caps, group limit, tracking-error cone) = direct maximisation | PC-B1 |
  | `s47_epo_pbl.py` | PBL eqs. (5)–(22), Props. 1–3 (BL, MVO, reverse MVO, Tikhonov, Lavrentiev), Prop. 2 both regimes (PBL-1), eq. (27), constrained V1 | PC-B6, PC-B7 |
  | `s47_black_litterman.py` | BL 1992 reverse optimisation, limits, p. 35 formula, BL-2 misprint, τ cancellation | PC-B2 |
  | `s47_robust_mv.py` | Goldfarb–Iyengar worst cases (eq. 15, Lemma 1, F = κG), robust min variance and max Sharpe, regression-set coverage | PC-B3 |
  | `s47_resampled_frontier.py` | Michaud & Michaud Tables 5.1 and 6.1 (MV and RE), fn. 7, limits. Specification check (D-2 closed 2026-10-08: core patent expired) | PC-B4 |
  | `s47_epo_grid_design_study.py` | **Design study, not a ranking:** grid size and 5% pre-shrink for PBL's past-only w rule (synthetic) | PC-B6 (S47-D2) |
- *[2026-10-15, before S4.8]* **Source verification for trend and volatility filters** (`ANG_ISSUES_REGISTER.md`, Paleologo section):

  | Script | Reproduces / proves | Used by |
  |---|---|---|
  | `s48_kalman_ewma_paleologo.py` | Paleologo (2025) ch. 2: Muth closed form and gain; steady-state Kalman = EWMA; AR(1) Riccati root; PAL-1 (omitted time update; correct filter = GARCH(1,1) recursion), PAL-2 … PAL-5, PAL-8. Ch. 5: PAL-6 (printed MSE minimised at √3·h). Ch. 6: PAL-7 (half-life convention) | S4.8 (EWMA/trend filters), S7, S10 |
- *[2026-10-15, S4.8]* **Momentum signal scripts** (`S4_MOMENTUM.md`; equations EQ-SIG-1 … EQ-SIG-5):

  | Script | Reproduces / proves | Signal |
  |---|---|---|
  | `s48_momentum_constructions.py` | JT overlapping cohorts; AMP eq. (1) invariants; PBL eqs. (24)–(27), PBL-3; MOP eq. (1) (centre of mass 60 d = half-life 41.9 d; no look-ahead); MOP eqs. (6)–(7) exact; JT eq. (3); BHM residual momentum (factor neutrality; BHM-1); G&K eq. (1), GK-1; E&L legs, EL-2; B&SC eqs. (5)–(6); DM eq. (6) vs the exact maximiser (DM-1); HOP combination | SIG-1, SIG-2, variants, EQ-SIG-4 |
  | `s48_trend_filters.py` | Bruder et al.: uniform MA = TSMOM sign; crossover = triangular return weights (BRU-1); Kalman gain = Muth gain = EWMA; HP and L1 two-sided; Mann statistic (BRU-2); Paleologo drift-precision limit | SIG-2T |
- *[2026-10-15, S4.9]* **Signal × PC compatibility** (`S4_SIGNAL_PC_COMPATIBILITY.md`):

  | Script | Proves | Use |
  |---|---|---|
  | `s49_signal_pc_compatibility.py` | Unscaled ranks into MVO are ill-defined (R-1); α = IC·ω·z with Grinold's volatility step invariant, benchmark neutrality, unit consistency (R-2); PBL EPO at w = 0 and 1; conditioned-universe constructions; direction rule after the engine-level scaling (R-4: 0.19 vs 0.69). Revised 2026-10-18 | S4.9, S9d, S4.20 |
  | `s49_double_counting_dcells.py` | EPO = MVO on shrunk mean and covariance (PBL eq. 22 removes scale, not location); double counting R-7 (unit-counting inflation, singular redundancy, tilt inside the host class, long-only active-sleeve bound, history vs holdings beta); D-cell tests (V1 identities; O2 re-solves; O3 zeroing/flipping breaks GMV/ERC; signed GMV and signed ERC); transfer coefficient of momentum compositions | S4.9, S4.13, S4.16, S4.20 |
  | `s49_alpha_sources.py` | Grinold 1994 (Exhibits 3–5, Exhibit 7 claims, eqs. 1–4, fns. 6, 8, 9; GRI-1, GRI-2); Grinold & Kahn *Advances* ch. 3 (eqs. 35–37, sign-only TC, Exhibit 11, four examples); CdST 2002 (Table 1, long-only reproduction, ex post R² ≈ TC²); Gallego lecture secs. 1.4–1.7 | EQ-MAP-3, EQ-TC-1 |
- *[2026-10-18, S4.10]* **Anchors and benchmarks** (`S4_ANCHOR_BENCHMARK.md`):

  | Script | Proves | Use |
  |---|---|---|
  | `s410_anchor_benchmark.py` | Anchored EPO with four anchors (w = 1, anchor-consistent signals, eq. 21, w = 0, level for centred signals); ASK infeasibility of 60/40 and projections; household feasibility LP = cut condition; Roll 1992 eqs. (1)–(5), A.4–A.6 (ROLL-1); Jorion 2003 (B3)–(B6), (C6), (C17), Tables 1–3, Theorems 2a–2d; GRS identity and Exhibit 6 (GKA-1), null-size simulation | EQ-ANC-1, EQ-FEAS-1, EQ-TEV-1/2, EQ-GRS-1 |
- *[2026-10-18, S4.11]* **Risk-structured methods** (`S4_RISK_STRUCTURED.md`):

  | Script | Proves | Use |
  |---|---|---|
  | `s411_risk_structured.py` | GMV closed form and CdST 2011 single-index long-only formula = QP; MRT §4.1 tables and eqs. (3)–(8), A.1, A.3, §3.5; ERC uniqueness; HRP V1 invariance, V0 order dependence and canonical determinism, limits; C&C Examples 1–2 and eqs. (4), (6)–(8), (11)–(12), long-only KKT; MinCorr/MinCorr2 worked example, invariances, MCA-4 domain; C5 × O2 | EQ-RS-1 … EQ-RS-5 |
- *[2026-10-18, S4.12a]* **Scenario and downside methods** (`S4_NON_TRADITIONAL.md`):

  | Script | Proves | Use |
  |---|---|---|
  | `s412_cvar_ru.py` | Rockafellar & Uryasev Table 3 (exact), eqs. (18)–(19) and Table 4 (10⁻⁶; RU-1), Tables 5–6 within sampling error (Monte Carlo and Sobol LPs), RU-3; RU-2 (LP = quantile-integral CVaR on discrete scenarios with ties); NT-1 (min-CVaR vs GMV by horizon; demeaned → GMV; recentring moves weights); EQ-SCN-1 moments. Runs about 2 minutes | PC-D1; EQ-NT-1, EQ-SCN-1 |
  | `s412_drawdown_tail.py` | Relative drawdown = 1 − e^{−log drawdown}; CDD-1 both directions; γ_min LP (CDD-2); CDD-3 convexity and exact binding of a relative limit; drift moves γ_min; demeaned Gaussian ERC-CVaR = ERC; BCP-4 existence; BCP-1 coincidence and divergence; BCP-3 determinism; BCP-5 modified-CVaR accuracy; historical ERC-CVaR by convex log-barrier; D3 × O2 | PC-D2, PC-D3; EQ-NT-2, EQ-NT-3 |
  | `s412_downside_b5.py` | S&vdM fn. 3 = K&S A7; A9 = A10; KS-1; SVDM-1; MTXY QP = direct convex; convexity; Estrada heuristic exact only under concordant shortfalls; max Sortino by homogenisation = global and on the frontier; EQ-SPLIT-1 invariance at MAR = cash rate; normal reductions (max Sortino = tangency; mean–TSV frontier = MV frontier) | PC-B5; EQ-DS-1, EQ-DS-2 |
- *[2026-10-18, S4.12b]* **Total Portfolio Approach** (`S4_NON_TRADITIONAL.md` Part B):

  | Script | Proves | Use |
  |---|---|---|
  | `s412b_tpa.py` | Treynor & Black eqs. (10)–(17) = Markowitz, (19) squared ratios add (TB-1), (20), (25), (28)–(32), p. 78 halving; AQR fns. 11–12; ABD eq. (4) and constrained OLS (A.3); TPA-1, TPA-2; TPA-R unconstrained closed form; TPA-R = Roll + exposure neutrality (TPA-3); distinctness against B1, B1 + TE, Roll and Anchored EPO; tangency coincidence (TPA-4) | PC-D4; EQ-NT-4 |

