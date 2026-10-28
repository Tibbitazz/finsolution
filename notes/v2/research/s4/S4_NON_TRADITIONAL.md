# S4.12 Non-traditional methods: PC-D1 … PC-D4 and PC-B5

*Part A (§0–§8): S4.12a, scenario and downside methods (DONE). Part B (§9–§10): S4.12b, PC-D4 Total Portfolio Approach (DONE; S412-D4 decided).*

**Document status:** S4.12a REVIEWED · S4.12b REVIEWED · **S4.12a DONE (2026-10-18)**, the first of two stops agreed by the owner on 2026-10-18 (S4.12b = PC-D4 TPA). Owner decisions S412-D1, D2, D3, D5 and the cross-cutting S412-D6 **accepted as recommended, option (a) in each, 2026-10-18** (§4). *S412-D6 clarified by the owner 2026-10-28 (F-1; note under the §4 decision table).* **S4.12b drafted 2026-10-18 and DONE 2026-10-19:** owner decision S412-D4 = option (a) (§9.6); the three TPA papers read after drafting (§9.8). · **Basis:** S4_PLAN §G (step S4.12); `S4_METHODS_OUTLINE.md` §1 (workflow, method-record template) and §2 (S4.12); `S4_SOURCE_REVIEWS_2026-10-08.md` §5–§6 (CUZ, BCP; S4.4); ADR-0024 §1, §3–§6; ADR-0025; ADR-0027 D3; S4.9 (R-3, S49-D1); S4.11 (S411-D4, S411-D5); EQ-SPLIT-1.

**Related files:** `verification/s412_cvar_ru.py`, `s412_drawdown_tail.py`, `s412_downside_b5.py`, `s412b_tpa.py` (all PASS); existing `s44_drawdown_cdd.py`, `s44_cvar_budgets_bcp.py`; register EQ-NT-1 … EQ-NT-4, EQ-DS-1, EQ-DS-2, EQ-SCN-1 (`S4_EQUATION_REGISTER.md`); issues RU-1 … RU-3, SVDM-1, KS-1, BCP-4, BCP-5, CDD-3, CES-1, TB-1, TPA-1, TPA-2 (`ANG_ISSUES_REGISTER.md`).

**Scope:** the mathematics of three scenario-based methods (CVaR, drawdown, tail-risk parity) and of mean–downside risk. **Nothing here ranks them** (S7; ADR-0025). Forecastability evidence read at this step is recorded as evaluation evidence, not admission evidence.

---

## 0. Summary

1. **Sources read and verified.**
   - **D1:** Rockafellar & Uryasev's tables 3–6 reproduce. Table 3 and the Table 4 normal-theory values match to 10⁻⁶. The scenario LP matches Tables 5–6 within sampling error.
   - **D2 and D3:** Chekhlov–Uryasev–Zabarankin and Boudt–Carl–Peterson were re-checked against S4.4 and extended.
   - **B5:** Sortino & van der Meer 1991 was read in full (scan). Its computation comes from Markowitz–Todd–Xu–Yamane 1993 (exact QP) and Cesarone et al. 2026 (convexity), and both reproduce.
   - **Advances chapters:** ch. 27 (Kahn & Stefek, downside risk) and ch. 32 (Grinold, scenario-based portfolio selection) were read in full.
2. **Each method in one line:**
   - **D1 CVaR:** minimise the expected loss in the worst (1 − β) of scenarios, as a linear programme.
   - **D2 drawdown:** maximise expected return subject to a limit on peak-to-trough loss along scenario paths.
   - **D3 tail-risk parity:** equalise (or cap the largest) contributions to CVaR.
   - **B5 mean–downside:** trade expected return against the shortfall below a minimum acceptable return (MAR).
3. **New cross-cutting finding NT-1 (§2.1): scenario methods are not location-free.**
   - CVaR includes the scenario mean. So min-CVaR equals GMV only when the scenarios have zero mean.
   - With raw scenarios, min-CVaR silently uses the historical mean as an expected return. The weight gap from GMV grows with the horizon: 1.9 pp at one month, 6.2 pp at one year, 14 pp at five years (R&U data).
   - The same holds for D3, where BCP's eqs. (2) and (7) contain −w′μ.
   - S4.9 listed min-CVaR and D3 as μ-free. That is true only under a demeaning convention that was never declared. Rule S412-D6 (accepted 2026-10-18) fixes this: demeaned scenarios for μ-free uses, and scenarios centred on S9's μ for μ-consuming uses (Grinold's eq. 10 construction).
4. **Every method reduces to a mean–variance or risk-parity method under normality** (§2.2, verified):
   - **D1:** min-CVaR on demeaned scenarios = GMV.
   - **D1 with an active return constraint:** mean–CVaR = the MV frontier (R&U Proposition).
   - **D3:** ERC-CVaR on demeaned Gaussian scenarios = ERC (C2).
   - **B5:** max Sortino with MAR = the cash rate = max Sharpe (tangency), and the mean–target-semivariance frontier = the MV frontier.

   Their only distinct content is the non-normality of the scenario set. This is the implied belief each candidate card must state.
5. **Specification findings:**
   - **CDD-3 (convex relative drawdown):** the Policy Statement's relative, compounded maximum-drawdown limit is a convex constraint in the weights (window form on log wealth). It can be enforced exactly, without CUZ's absolute uncompounded proxy. The proxy can be off in either direction: 20% vs 63% on a choppy path, the reverse on a trend decline (CDD-1 quantified).
   - **BCP-4 (ERC-CVaR existence):** long-only ERC-CVaR does not exist when an asset's expected return is at least c₂(β)·σ. Cash in a total-return CVaR is such an asset. On demeaned scenarios a unique solution exists through a convex log-barrier.
   - **BCP-5 (modified CVaR accuracy):** errors of 6–12% at β = 95% under fat tails, up to 86% at 97.5%, and not monotone in the tail level.
   - **B5 citation gap:** the Sortino *ratio* is not in Sortino & van der Meer 1991. It is in Sortino & Price 1994 (not in hand).
6. **Decisions (§4), all option (a), accepted by the owner 2026-10-18:**
   - **S412-D1:** min-CVaR on demeaned scenarios, β = 0.95; R&U's mean–CVaR (P1) a registered variant.
   - **S412-D2:** relative compounded maximum drawdown in its convex form, γ = the Policy Statement limit, maximise expected return, α = 1; CUZ's LP the reproduction oracle.
   - **S412-D3:** ERC-CVaR on demeaned scenario CVaR by the convex form; MCC a variant with a recorded seed or start set; modified CVaR not the default.
   - **S412-D5:** maximum Sortino ratio, MAR = the cash rate per period, exact target semivariance; family B, a separate candidate.
   - **S412-D6:** demeaned scenarios for μ-free uses, scenarios centred on S9's μ for μ-consuming uses; raw historical location never.
7. **D3 × O2 (the last pending S4.9 cell):** defined and rank-only. It goes to the **research lane** under S49-D1.

---

## 1. Sources read (stage 1)

| Method | Governing source | Version in hand · md5 | Read | Supporting |
|---|---|---|---|---|
| D1 | Rockafellar & Uryasev, "Optimization of Conditional Value-at-Risk", *J. Risk* 2(3), 2000 | Preprint dated 5 Sep 1999 (26 pp; figure and table cross-references print as "??") · `ee8f86ef5b31` | In full 2026-10-18 | R&U 2002 (general distributions; not in hand, optional) |
| D2 | Chekhlov, Uryasev & Zabarankin, *IJTAF* 8(1):13–58, 2005 | UF report 2003-15 · `597c81fcff3f` | S4.4 (reviewed); re-checked | — |
| D3 | Boudt, Carl & Peterson, *J. Risk* 15(3):39–68, 2013 | Version of 24 May 2012 · `a6b28ba66935` | S4.4 (reviewed); re-checked | Boudt, Peterson & Croux 2008 (modified ES; not in hand) |
| B5 | Sortino & van der Meer, "Downside Risk", *JPM* 17(4):27–31, Summer 1991 | Scan, no text layer · `b1756aecbd53` | In full 2026-10-18 (page images) | See below |
| B5 (computation) | Markowitz, Todd, Xu & Yamane, "Computation of mean-semivariance efficient sets by the Critical Line Algorithm", *Ann. Oper. Res.* 45:307–317, 1993 | Published · `edc9c17c056a` | In full | Cesarone, Corradini, Giunta & Lampariello, "Semivariance, semicovariance matrix and lower partial moments for portfolio selection", *Finance Research Letters* 91:109424, 2026 (online 23 Dec 2025; CC BY) · `1807243dfd4b`, read §1–§5 |
| B5 (heuristic) | Estrada, "Mean-Semivariance Optimization: A Heuristic Approach", *J. Appl. Finance* 18(1), 2008 | Published · `5e1e193381c9` | Method sections | Not adopted (§3, B5) |
| All | Grinold & Kahn, *Advances in Active Portfolio Management* (2019), ch. 26 intro, ch. 27 (Kahn & Stefek, "Heat, Light, and Downside Risk", BARRA white paper Dec 1996), ch. 28 intro, ch. 32 (Grinold, "Mean-Variance and Scenario-Based Approaches to Portfolio Selection", revision of *JPM* Winter 1999:10–22) | `096bdb504af3` (S4.9) | In full (PDF pp. 559–591, 595, 664–686) | — |

Identified in the library, not needed for S4.12a and not read in full:
- Hogan & Warren, *JFQA* 9(1):1–11, 1974 (semivariance CAPM).
- Cumova & Nawrocki, *J. Econ. Bus.* 71:68–89, 2014 (upside potential and downside risk).
- Sortino, van der Meer & Plantinga, "The Dutch Triangle", *JPM* Fall 1999 (scan; identity from the page image).
- Landsman, Makov, Yao & Zhou, *Eur. J. Finance*, 2022 (random targets).
- Nassar & Ephrem, "Optimal allocation using the Sortino ratio" (2020 note; a single-bet Kelly setting, not multi-asset).
- Martin, Ulcer Index (web page).

Source details that matter:
- **R&U:**
  - Theorems 1–2 assume the loss distribution is continuous: eq. (27), Ψ(x, ·) continuous. The engine's scenario sets are discrete. The LP still returns CVaR as the quantile integral (1/(1−β))∫_β^1 VaR_u du, including ties and non-integer βq (verified; RU-2). A naive "mean of losses beyond VaR" differs from it in that case.
  - The governing result for discrete distributions is R&U 2002 (not in hand).
  - The Proposition requires the return constraint (15) to be active and β ≥ 0.5.
  - The hedging example (§4; Tables 7–9, Nikkei options) uses nonsmooth optimisation and is outside our domain.
- **S&vdM 1991:**
  - Risk is defined against a MAR. Downside variance (Fishburn 1977) is DR = ∫_{−∞}^{M}(M − r)² f(r) dr (fn. 3), computed on the combined (portfolio) distribution, i.e. endogenously.
  - Their test assumed "near perfect forecasts" of quarterly scenarios. It is in-sample evidence about a measure, not about a method's out-of-sample value.
  - The ratio that carries Sortino's name is not defined here. Kahn & Stefek cite Sortino & Price 1994 for it.
- **Kahn & Stefek (ch. 27):**
  - Five-year-to-five-year persistence across 578 asset classes, 475 funds and 1,160 stocks.
  - Average R² falls when variance's prediction is removed: 0.70 for SD, 0.64 for variance, 0.60 for semivariance but 0.10 for abnormal semivariance; target semivariance 0.42 → 0.12; shortfall probability 0.40 → 0.01.
  - Conclusion: downside risk of fundamental assets adds little beyond variance. A preference overlay (options or dynamic strategies) belongs in a second stage.
  - Their 2019 introduction adds a counterpoint. Kahn's group runs one minimum-CVaR fund on historical simulation and "found some evidence" that historical simulation predicted CVaR better than SD under symmetry (ch. 26 intro, fn. 5).
- **Grinold (ch. 32):**
  - Scenario returns are built as r_{n,s} = r_F + μ_nΔt + σ_n z_{n,s}√Δt, with Σπ_s z = 0 and Σπ_s z² = 1 (eq. 10). The engine controls the first two moments; history supplies dependence and higher moments. A recency tilt is π_{S−j} = φ^j π_S.
  - Using raw history is called "unwise".
  - The 2019 view is that the scenario approach is "attractive" for few assets, a stable universe and total-return objectives. That is our SAA case.

---

## 2. Cross-cutting findings

### 2.1 NT-1: scenario location

| Method | Where the scenario mean enters | Consequence with raw historical scenarios |
|---|---|---|
| D1 min-CVaR | CVaR_β(x) = −μ′x + c₂(β)σ(x) under normality; in general CVaR shifts by −x′Δμ when scenarios shift by Δμ | Weights depend on the historical mean, with an implicit risk aversion that changes with horizon (μ ∝ h, σ ∝ √h). R&U data, β = 0.95: gap to GMV 1.9 / 3.2 / 6.2 / 10.6 / 14.0 pp at 1 / 3 / 12 / 36 / 60 months |
| D3 ERC-CVaR, MCC | Contributions contain −w_iμ_i (BCP eqs. 2, 7) | Parity depends on means; a long-only solution may not exist (BCP-4) |
| D2 | Drawdowns depend on drift; the objective is the mean | Feasibility boundary γ_min moves with the drift (verified) |
| B5 | Objective μ′x and the shortfall location | The objective's μ (S9) and the scenarios' implicit μ disagree unless harmonised |

**Harmonisation (EQ-SCN-1; Grinold eq. 10):**
- Standardise the history to z, with zero mean and unit variance per asset under the scenario probabilities.
- Scale by the authoritative σ (S10).
- Add the location:
  - zero for methods declared μ-free;
  - S9's μ for methods that consume μ.

Correlations and higher moments come from history. Verified: the recentred set has exactly the target means and SDs and the historical correlation matrix. Raw historical location would be an undeclared capital-market assumption, which conflicts with S9 owning μ. → S412-D6.

### 2.2 Relations under normality (verified)

| Method | Normal limit | Script |
|---|---|---|
| D1, demeaned, no return constraint | GMV | `s412_cvar_ru.py` (Sobol 32,768, within 2 pp) |
| D1, return constraint active (R&U P1) | MV frontier portfolio; VaR = −R + c₁σ, CVaR = −R + c₂σ (eqs. 18–19) | Table 3 exact; Table 4 to 10⁻⁶ |
| D3, demeaned Gaussian CVaR | ERC (C2) | `s412_drawdown_tail.py` (10⁻⁵) |
| B5, max Sortino, MAR = cash rate | Max Sharpe (tangency) at that rate: Sortino = k/√g(k) with k the Sharpe ratio and g(k) = (1 + k²)N(−k) − kφ(k) decreasing | `s412_downside_b5.py` (10⁻⁵, long-only) |
| B5, min target semivariance at a return | MV frontier portfolio (for a fixed mean, target semivariance increases with σ) | Same (10⁻⁵) |

**Reading:**
- The four methods differ from B1, C1 and C2 only through the shape of the scenario distribution (fat tails, asymmetry, serial dependence for D2).
- Kahn & Stefek's evidence says that shape is weakly persistent for fundamental assets. That is a hypothesis for S7 evaluation, not a reason to exclude the methods (ADR-0025; owner rule "unknown ≠ unsupported").
- Grinold's revised view supports the scenario approach for our setting.

### 2.3 Tail sample size

- With q scenarios, CVaR_β rests on q(1 − β) observations.
- Normal-theory CVaR at β = 0.99 needed a 65,536-point Sobol set to come within 1.5%. At β = 0.95, 16,384 points gave 1%.
- Historical monthly sets have q of 240–600, so 2–6 observations at 99% and 12–30 at 95%.
- The contract must report q(1 − β) and fail below a minimum. The minimum is set at S10 / S4.20.

---

## 3. Method records (stages 2, 4, 5, 7)

### PC-D1 CVaR minimisation

- **Identity:** PC-D1 · CVaR optimisation (ANG Exh. 3) / "CVaR Minimization" (Exh. 7–8); ANG-02 · family D · `M.PC` · roster v0.
- **Sources:** governing R&U 2000: Theorems 1–2 (eqs. 4–10), scenario form (17), Proposition with (18)–(19), Tables 1–6. Supporting: R&U 2002 (not in hand); Grinold eq. 10 (scenario construction).
- **Definition (EQ-NT-1):**
  - F_β(x, α) = α + (1/(q(1−β)))Σ_k[−y_k′x − α]⁺.
  - CVaR_β(x) = min_α F_β(x, α).
  - The joint minimisation over (x, α, u) is the LP: min α + (1/(q(1−β)))Σu_k s.t. u_k ≥ −y_k′x − α, u ≥ 0, x ∈ X.
  - **V0 (recommended, S412-D1):** min CVaR_β(x) over the Policy Statement set X (Theorem 2 with general X), on demeaned scenarios.
  - **V1:** R&U's P1, min CVaR_β s.t. μ′x ≥ R, on scenarios centred on S9's μ.
- **Inputs:** scenario set Y (q × N), a risk object owned by S10 (ADR-0027 D3), with location per S412-D6. V0 does not use μ.
- **Parameters:**
  - β: fixed V0, recommended 0.95.
  - Scenario horizon and q: system, from S10.
  - R (V1): user-authorised.
- **Constraints:** native (LP): long-only, bounds, groups, linear turnover.
- **Allocation domains:** asset class, fund/ETF, security.
- **Output and failures:**
  - Weights, plus VaR as a by-product (the minimising α; RU Theorem 1).
  - `INFEASIBLE_CONSTRAINTS`.
  - `INSUFFICIENT_TAIL_SCENARIOS`: q(1 − β) below the S10 minimum.
  - V1: `INFEASIBLE_RETURN_TARGET`.
- **ANG vs source:** ANG-02 (objective unclear) → S412-D1; ANG-17 (scenario input) → S4.20.
- **Invariants:**
  - The LP value equals the quantile-integral CVaR on discrete scenarios (RU-2).
  - CVaR ≥ VaR.
  - Convex and positively homogeneous in x.
  - A uniform shift of the scenarios by c changes CVaR by −c for a fully invested x.
  - Demeaned and normal → GMV.
- **Verification:** `s412_cvar_ru.py`. PASS.
  - Table 3 exact; Table 4 to 10⁻⁶.
  - Tables 5–6 within sampling error: at β = 90% and 95%, the mean of 6 Monte Carlo runs at q = 10,000 is within 1% and Sobol 16,384 is within 1%; at 99%, Sobol 65,536 is within 1.5%.
  - RU-1, RU-2, RU-3; NT-1.
- **Agent-readable summary:**
  - *Objective:* the smallest average loss in the worst 5% of scenarios.
  - *Intuition:* GMV for the tails.
  - *Implicit belief:* identical to GMV if scenarios were normal; any difference comes from fat tails or asymmetry in the scenario set.
  - *Sensitivities:* the 12–30 tail observations of a historical set decide the solution; the scenario window.
  - *Failure modes:* the tail set is dominated by one crisis; too few tail scenarios.
  - *Valid comparisons:* GMV, D3.
  - *Invalid:* comparing a demeaned CVaR with one computed on raw scenarios.

### PC-D2 Maximum-drawdown-constrained

- **Identity:** PC-D2 · Max drawdown-constrained (ANG Exh. 3; Policy Statement limit "−25% peak-to-trough", ANG p. 15) · family D · `M.PC` · roster v0.
- **Sources:**
  - Governing: CUZ 2005, eqs. 6–7, 14, 16–17, 25, 30–31, 47, 49, 55–56 (S4.4: CDD-1, CDD-2).
  - The relative compounded form is our derivation (CDD-3, verified). No source in hand states it.
- **Definition (EQ-NT-2):**
  - **CUZ (absolute, uncompounded):** w_k(x) = Σ_{t≤k} r_t′x; ξ_k = max_{j≤k} w_j − w_k; CDD_α = CVaR_α(ξ); MaxDD at α → 1.
  - **Relative compounded (the Policy Statement quantity):** L_k(x) = Σ_{t≤k} ln(1 + r_t′x); D_k = max_{j≤k} L_j − L_k; relative drawdown 1 − e^{−D_k}.
  - MaxDD_rel ≤ γ ⇔ −Σ_{t=j+1}^{k} ln(1 + r_t′x) ≤ −ln(1 − γ) for every window j < k. This is convex: each term is minus the log of an affine function.
  - CDD_α on log drawdowns is convex as well (verified). The relative-percentage CDD for α < 1 is a concave transform of convex functions, so convexity is not guaranteed.
  - **Problem (CUZ eqs. 47/55):** maximise mean return over the paths s.t. the drawdown limit, x ∈ X.
- **Inputs:**
  - Return paths (T × N; historical or block bootstrap) from S10.
  - Location: S9's μ (S412-D6).
  - γ from the Policy Statement.
- **Parameters:**
  - γ: user-authorised. ANG's example is 25%, so the log-wealth cap is −ln 0.75 = 0.2877.
  - α: recommended 1 (MaxDD, the Policy Statement quantity); 0.8 and 0.95 as sensitivity variants.
  - Path length and block length: system (S10).
- **Constraints:** native (LP for CUZ; convex NLP for the relative form).
- **Allocation domains:** asset class, fund/ETF.
- **Output and failures:**
  - Weights.
  - `INFEASIBLE_DRAWDOWN_LIMIT`, reported with γ_min = min_x MaxDD(x). γ_min is one LP (CUZ form) or one convex programme (relative form). Verified: feasible at γ_min + 10⁻⁷, infeasible at γ_min − 10⁻⁴.
  - `INFEASIBLE_CONSTRAINTS`.
- **EQ-SPLIT-1:** exception class ("absolute risk limit"). σ* enters inside the optimisation; there is no post-scaling, because scaling would breach the drawdown limit.
- **ANG vs source:** ANG-40, CDD-1 → S412-D2.
- **Invariants:**
  - Relative = 1 − exp(−log drawdown), exactly.
  - Log drawdown ≥ CUZ drawdown on every path.
  - A binding solution realises γ exactly.
  - Feasible ⇔ γ ≥ γ_min.
- **Verification:** `s44_drawdown_cdd.py` (CUZ equivalences; LP 55) and `s412_drawdown_tail.py`:
  - CDD-1 in both directions: a choppy path has CUZ 20% vs relative 63%; a trend decline is the reverse.
  - The γ_min boundary.
  - Midpoint convexity: 2,000 pairs (MaxDD) and 900 (CDD).
  - A relative 15% limit binds exactly. The CUZ LP at γ = 15% realises a 14.52% relative drawdown with weights 2.5 pp apart.

  PASS.
- **Agent-readable summary:**
  - *Objective:* the highest expected return whose worst peak-to-trough loss along the scenario paths stays within the limit.
  - *Intuition:* path-aware risk control.
  - *Implicit belief:* the paths' ordering (serial dependence, crash sequences) is informative.
  - *Sensitivities:* the path set; the drift (location); one extreme path at α = 1.
  - *Failure modes:* infeasible at tight γ.
  - *Valid comparisons:* B1 at the same σ*; D1.
  - *Invalid:* comparing CUZ absolute drawdowns with the relative Policy Statement limit.

### PC-D3 Tail-risk parity

- **Identity:** PC-D3 · Tail-risk parity (ANG Exh. 3, BCP 2013) · family D · `M.PC` · roster v0.
- **Sources:** governing BCP: eqs. 2–7, 10, 11, 14, 15; Appendix eqs. 21–22 (S4.4: BCP-1 … BCP-3). Supporting: R&U (scenario CVaR, EQ-NT-1).
- **Definition (EQ-NT-3):**
  - Euler contributions C_i = w_i ∂CVaR/∂w_i (eq. 3). For scenario CVaR, C_i = w_i E[−r_i | portfolio loss in the tail] (eq. 5). Shares %C_i = C_i/CVaR.
  - **ERC-CVaR:** %C_i = 1/N (eq. 11).
  - **MCC:** argmin max_i C_i (eq. 10) = argmin CVaR · max %C_i (eq. 14).
  - **Deterministic ERC-CVaR on scenario CVaR (our derivation):** y* = argmin CVaR(y) − (1/N)Σ ln y_i over y > 0, then w = y*/1′y*.
    - The problem is strictly convex, so y* is unique.
    - It exists when CVaR(y) > 0 for every y ≥ 0, y ≠ 0, which holds on demeaned, non-degenerate scenarios.
    - Contributions are equal in the subgradient sense. On discrete scenarios they matched to within 0.004 of 1/N (CVaR is piecewise linear), and six starts of a derivative-free solver agreed to 10⁻³. A production solver should solve the convex programme exactly (S4.20, S4.23).
- **Inputs:**
  - Demeaned scenarios (S412-D6), or for modified CVaR the co-moments Σ, M3 (N × N²) and M4 (N × N³) (BCP-2; S4.13).
  - Not used: μ.
- **Parameters:**
  - β: recommended 0.95 (BCP's α = 5%).
  - Object: ERC or MCC (S412-D3).
  - CVaR estimator: an S10/S4.13 choice (ADR-0027 D3).
- **Constraints:**
  - ERC-CVaR is long-only by construction; bounds by post-processing (S411-D4 rule).
  - MCC accepts native constraints.
- **Allocation domains:** asset class, fund/ETF. Security level is impractical with M4, but feasible with scenario CVaR.
- **Output and failures:**
  - Weights.
  - `NO_ERC_SOLUTION` (BCP-4).
  - `DEGENERATE_SCENARIOS`.
  - For MCC, a search record (seed or start set) is required (BCP-3).
- **EQ-SPLIT-1:** μ-free (demeaned), so exposure is k = min(σ*/σ(p), L).
- **ANG vs source:** ANG-39 (BCP-1) → S412-D3.
- **Invariants:**
  - The Euler sum equals CVaR.
  - Demeaned Gaussian → ERC (C2).
  - Min-CVaR shares = weights (Prop. 15).
  - The MCC objective is ≤ CVaR_ERC/N, with equality iff the ERC portfolio is itself an MCC solution.
- **Verification:** `s44_cvar_budgets_bcp.py` and `s412_drawdown_tail.py`. PASS.
  - **BCP-1 divergence case:** μ = (2, 6, 7)%, σ = (20, 10, 4)%, ρ₁₃ = 0.8, ρ₂₃ = 0.5. ERC (3.3, 12.8, 83.8)% vs MCC (0, 11.2, 88.8)%. MCC drops asset 1.
  - **BCP-4:** cash-like asset μ 1.2%, σ 0.5%: no solution; demeaned: solution exists.
  - **BCP-5.**
  - **Determinism:** seeded differential evolution is bit-identical; two deterministic start sets agree to 10⁻⁹.
- **Agent-readable summary:**
  - *Objective:* equal shares of tail loss.
  - *Intuition:* risk parity for crashes.
  - *Implicit belief:* identical to ERC if scenarios were normal.
  - *Sensitivities:* the tail sample; co-moment estimates. Modified CVaR is unstable and not monotone in the tail level under high kurtosis (BCP-5).
  - *Failure modes:* BCP-4 on raw scenarios; MCC drops assets.
  - *Valid comparisons:* C2 ERC, D1.
  - *Invalid:* modified CVaR below 5%.

**D3 × O2 (S4.9 pending cell):**
- ERC-CVaR re-solved on a signal-selected subset of the authoritative risk object is well defined.
- It sums to 1, is positive, and is identical under three monotone transforms of the score (verified).
- Under S49-D1 (tested, no source for the pairing) it joins the **research lane**. With C5 × O2 (S4.11) this closes the S4.9 D cells.

### PC-B5 Mean–downside risk

- **Identity:** PC-B5 · Mean–downside risk (ANG Exh. 3, Sortino & van der Meer; Exh. 7 "Mean-Downside Risk (Sortino)") · family B · `M.PC` · roster v0.
- **Sources:**
  - Governing (concept, measure): S&vdM 1991, fn. 3, Figure 4, pp. 27–31.
  - Computation: MTXY 1993, eqs. 3.1–3.8 (exact QP); Cesarone et al. 2026 (eqs. 1, 14–16; Remark 4: convex; their projected-gradient optimum matches MTXY to at most 1.44 × 10⁻⁴ relative, Table 3; CES-1).
  - Definitions and normal closed form: Kahn & Stefek, eqs. A5–A10.
  - The Sortino ratio: Sortino & Price 1994 (not in hand).
- **Definition:**
  - **EQ-DS-1 (measure):**
    - Target semivariance TSV_c(x) = (1/T)Σ_t[(c − r_t′x)⁺]². This is MTXY (3.1b) with bm_t = c, the sample form of fn. 3, and K&S (A7).
    - The divisor is T, all periods, as in the integral.
    - Downside deviation DD_c = √TSV_c. Sortino ratio SoR_c = (μ′x − c)/DD_c.
  - **EQ-DS-2 (objectives):**
    - **(a)** Max SoR_c. Homogenise: min (1/T)Σ[((c − r_t)′y)⁺]² s.t. (μ − c1)′y = 1, y ≥ 0, then x = y/1′y. This is a convex QP; verified equal to the global maximum and on the MTXY frontier.
    - **(b)** Min TSV_c s.t. μ′x ≥ η (Cesarone eq. 15; MTXY 3.3). ANG-18's options (b) and (c) are this one problem.
    - **(c′)** Min λ·TSV_c − μ′x (Cesarone eq. 16; the form of S&vdM's "3 risk to 1 return" test).
- **Inputs:** μ (S9); scenarios centred on μ (S412-D6); MAR c (Policy Statement). Not used: Σ.
- **Parameters:**
  - c: user-authorised; recommended default = the cash rate per period.
  - η or λ for the variants.
- **Constraints:** native (QP).
- **Allocation domains:** asset class, fund/ETF, security (MTXY: 1,008 securities).
- **Output and failures:**
  - Weights.
  - `NO_POSITIVE_EXCESS`: no feasible x with μ′x > c.
  - `NO_SHORTFALL_SCENARIOS`: DD_c = 0, so the ratio is undefined.
  - `INFEASIBLE_RETURN_TARGET` (b).
  - `INFEASIBLE_CONSTRAINTS`.
- **Semivariance computation:**
  - Exact (MTXY QP or the direct convex form; verified equal).
  - Estrada's exogenous semicovariance matrix is **not adopted**. It is exact only when all assets fall short together; the relative error reached 74% in our test, and its optimum differs from the exact one.
- **EQ-SPLIT-1:** with c = the cash rate, SoR of k·p + (1 − k)·cash does not depend on k (verified), so the exposure rule applies as for B1. With c ≠ the cash rate it does depend on k.
- **ANG vs source:** ANG-18 → S412-D5. ANG's "Sortino" label cites a paper that does not define the ratio (citation gap, class B).
- **Invariants:**
  - TSV at target = mean equals half the variance under symmetry.
  - Under normality, max SoR (c = cash rate) = tangency, and the frontier = the MV frontier.
  - TSV_c is convex.
- **Verification:** `s412_downside_b5.py`: fn. 3 = A7; A9 = A10; KS-1; SVDM-1; MTXY QP = direct convex at three targets; Estrada; homogenised max SoR; the normal reductions; EQ-SPLIT-1 invariance. PASS.
- **Agent-readable summary:**
  - *Objective:* the highest return per unit of shortfall below the MAR.
  - *Intuition:* penalise only bad outcomes.
  - *Implicit belief:* the asymmetry in the scenario set is real and persistent (Kahn & Stefek found little persistence for fundamental assets). Identical to max Sharpe if scenarios were normal.
  - *Sensitivities:* the MAR; the number of shortfall observations; μ.
  - *Failure modes:* few or no shortfalls; the ratio is not invariant to cash scaling if MAR ≠ the cash rate.
  - *Valid comparisons:* B1 with the same μ and scenarios.
  - *Invalid:* comparing Sortino ratios with different MARs or denominators (1/T vs 1/#shortfalls).

---

## 4. Owner decisions (stage 6)

*[2026-10-18]* **Owner decision: S412-D2, D3, D5 and D6 accepted as recommended (option (a)); S412-D1 option (a) accepted after the owner asked how (a) differs from (b).** The owner also asked why historical means are never the scenario location (D6). The answer given: S9 is the only source of μ (one declared CMA basis, I-4); an implicit sample mean would differ by method and window, carry a risk aversion set by the scenario horizon, and add estimation error; a historical-average CMA, if S9 adopts one, enters through S9 like any other. History still supplies dependence, tails and paths.

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **S412-D1** | CVaR objective (ANG-02) and β | (a) **V0** min-CVaR over the Policy Statement set on demeaned scenarios (μ-free, normal limit GMV); R&U's P1 (min CVaR s.t. μ′x ≥ R, centred on S9's μ) registered as V1 · (b) P1 as V0 · (c) maximise μ′x s.t. a CVaR limit | **(a), β = 0.95.** It matches ANG's "CVaR Minimization", keeps D1 in the μ-free class beside GMV, and has R&U's Proposition as its oracle. Return-seeking forms already exist in family B. β = 0.99 rests on 2–6 historical tail observations (§2.3) |
| **S412-D2** | Drawdown definition, γ mapping, objective, α (ANG-40; CDD-1, CDD-2) | (a) relative compounded MaxDD via the convex window form (CDD-3), γ = the Policy Statement limit with no mapping; CUZ's objective (max mean); α = 1; CUZ LP kept as the reproduction oracle (V0) and CDD on log drawdowns for α < 1 as variants · (b) CUZ absolute LP with a declared mapping of γ · (c) both as candidates | **(a).** It enforces exactly the quantity the Policy Statement limits. No exact mapping between the two definitions exists (CDD-1, both directions). The cost is a convex programme instead of an LP. Infeasibility reports γ_min |
| **S412-D3** | Tail-risk object (ANG-39, BCP-1), CVaR estimator, determinism (BCP-3) | (a) ERC-CVaR ("parity") on demeaned scenario CVaR through the convex log-barrier (unique, deterministic); MCC registered as a variant with a recorded seed or start set; modified CVaR kept as BCP's reproduction oracle and registered as an S4.13 estimator candidate with the BCP-5 caution · (b) MCC as V0 (BCP's own proposal) · (c) BCP as published (modified CVaR; ERC or MCC) | **(a).** "Parity" names equal contributions. The convex form removes the stochastic optimiser and the existence failure. Modified CVaR's accuracy problem (BCP-5) and its N³ co-moment object argue against it as the default estimator |
| **S412-D5** | B5 objective (ANG-18), MAR, placement | (a) max Sortino ratio (homogenised QP), MAR = the cash rate per period (scale-invariant under EQ-SPLIT-1), exact target semivariance with divisor T; variants (b) and (c′) registered; Estrada excluded; placement family B, a separate candidate · (b) min target semivariance at a Policy Statement return η · (c) the λ form | **(a).** It is the single-point analogue of B1 (max Sharpe) and nests it under normality, so the difference is attributable to scenario shape. A different MAR (0, inflation) is a sensitivity variant |
| **S412-D6** | Scenario location rule (NT-1), new | (a) methods declared μ-free (D1 V0, D3) use demeaned scenarios; methods that consume μ (D1 V1, D2, B5) use scenarios centred on S9's μ (EQ-SCN-1); raw historical location is never used; S4.9 §2 item 3 and R-3 get a dated annotation ("μ-free only on demeaned scenarios") · (b) centre all scenario methods on S9's μ; D1 and D3 move to the μ-consuming class and their S4.9 rows are reclassified · (c) raw historical scenarios | **(a).** It keeps S9 as the only source of μ. It removes a horizon-dependent hidden risk aversion. It makes the normal limits (GMV, ERC) hold. (c) would be an undeclared CMA |

*[2026-10-28, owner decision F-1, clarifying S412-D6]* **"Demeaned" means each asset's excess return minus its own mean (deviations from the mean), so the scenarios are centred on zero; the cash rate is not added back.** This applies to the μ-free methods (D1 V0, D3). It is the convention under which the S4.12a results were verified and under which S412-D6's rationale holds (the normal limits GMV and ERC).
- Methods that consume μ (D1 V1, D2, B5) centre their scenarios or paths on S9's μ and declare their return basis, excess or total, in their S4.20 contracts. Defaults: D2 total returns (a drawdown concerns wealth); B5 total returns with MAR = the cash rate, equivalent to excess returns with MAR = 0; D1 V1 the basis of its target R.
- Quantities stated in total returns (Policy Statement loss limits, investor reports) add the cash return back explicitly, including any borrowing cost under leverage.
- Grinold adds the cash rate because his objective is expected utility of total return (*Advances* ch. 32, PDF pp. 669–671); the total form is kept for objectives that concern wealth.
- No S4.12a result changes. Analysis: `S4_RISK_DEPENDENCIES.md` §6.1 (finding F-1).

---

## 5. Verification (stage 7)

| Script | Proves | Result |
|---|---|---|
| `s412_cvar_ru.py` | R&U Table 3 (exact); eqs. (18)–(19) and Table 4 (10⁻⁶; RU-1 reading); Tables 5–6 within sampling error (pseudo-random and Sobol); RU-3; RU-2 (LP = quantile integral on discrete scenarios with ties; naive tail mean differs); NT-1 (horizon profile; demeaned → GMV; centred → mean-CVaR point; recentring moves weights); EQ-SCN-1 moments | PASS (≈ 2 min) |
| `s412_drawdown_tail.py` | Relative = 1 − e^{−log DD}; log ≥ CUZ; CDD-1 both directions; γ_min LP boundary (CDD-2); CDD-3 convexity (MaxDD and CDD on log drawdowns) and exact binding; drift moves γ_min; Gaussian ERC-CVaR = ERC at μ = 0; BCP-4 (Cauchy–Schwarz bound over 20,000 portfolios; no solution; demeaned exists); BCP-1 coincidence and divergence; BCP-3 determinism; BCP-5 (4 M-sample historical vs modified CVaR at 5/2.5/1%); historical ERC-CVaR uniqueness; D3 × O2 | PASS |
| `s412_downside_b5.py` | fn. 3 = A7; A9 = A10; KS-1; SVDM-1; MTXY QP = direct convex; convexity; Estrada inexact except under concordant shortfalls, its optimum not exact; max Sortino homogenised = global and on the frontier; EQ-SPLIT-1 invariance at MAR = cash rate; normal reductions | PASS |
| `s44_drawdown_cdd.py`, `s44_cvar_budgets_bcp.py` | S4.4 reproductions | PASS |

---

## 6. New issues (detail in `ANG_ISSUES_REGISTER.md`)

| ID | Location | Issue | Materiality |
|---|---|---|---|
| RU-1 | R&U eq. (19) | Printed "exp(erf⁻¹(2β−1))²". Only exp([erf⁻¹(2β−1)]²) = φ(Φ⁻¹(β))·√(2π) reproduces Table 4 | L |
| RU-2 | R&U eq. (27), Theorems 1–2 | Continuity assumed; discrete scenarios are covered by the LP (verified), formally by R&U 2002 (not in hand) | M (contract: LP definition, never the naive tail mean) |
| RU-3 | R&U Table 5 | Three "VaR Dif (%)" signs flipped (β = 0.9; q = 3,000, 5,000, 10,000); magnitudes correct | L |
| SVDM-1 | S&vdM Figure 4 | Printed downside variances equal SP × (average shortfall)², not fn. 3 (1.5 × larger for the drawn tails; ratio 4 unchanged); the drawn triangles do not have the stated mean 10% and SD 12% | L (illustration) |
| KS-1 | *Advances* ch. 27, fn. 12 | Monthly target −10%/√12 = −2.89% uses volatility scaling for a return level (−0.83% arithmetic, −0.87% geometric) | L (their test used a deeper target) |
| BCP-4 | BCP eq. (11) | Long-only ERC-CVaR does not exist if any μ_i ≥ c₂(β)σ_i (e.g. cash in total-return CVaR) | M |
| BCP-5 | BCP Appendix eqs. (21)–(22) | Modified CVaR errs 6–12% at 5% and up to 86% at 2.5% under fat tails; not monotone in the tail level | M |
| CDD-3 | CUZ §2 vs ANG p. 15 | The relative compounded drawdown limit is convex in the weights (resolution aid for ANG-40) | — (finding) |
| CES-1 | Cesarone et al. 2026, §4.2 text vs Table 3 | The text says the relative differences to MTXY "remain below 10⁻⁴"; Table 3 has 1.44 × 10⁻⁴ (N = 50, T = 4,000) | L |

---

## 7. Handed forward

| To | Item |
|---|---|
| S4.12b | PC-D4 TPA: distinctness test, gap memo, S412-D4 |
| S4.9 (annotated 2026-10-18 under S412-D6) | Min-CVaR and D3 are μ-free only on demeaned scenarios |
| S4.13 | Risk objects: scenario set (q × N, horizon, probabilities, location rule), paths (T × N, bootstrap block), co-moments M3/M4 (BCP-2); minimum tail count q(1 − β) |
| S9 | μ injected into scenarios by EQ-SCN-1 for μ-consuming scenario methods |
| S10 | Scenario generation: standardised history z, recency weights π_{S−j} = φ^j π_S (Grinold), block bootstrap (CUZ); estimator caution BCP-5 |
| S4.16 | Candidate card: tail count; VaR and CVaR; γ_min; deviation of %C_i from 1/N; MAR; normal-limit twin (GMV, ERC, max Sharpe) |
| S4.20 | Failure codes; EQ-SPLIT-1 classes (D2 exception); ERC-CVaR bounds by post-processing (S411-D4) |
| S7 | Kahn & Stefek's persistence result as an evaluation hypothesis; Cesarone et al.'s DJIA comparison is evaluation evidence only |
| S13 / G4 | The Policy Statement drawdown limit can be checked exactly for every candidate with the CDD-3 form |

---

## 8. Ladder status after S4.12a

| Method | Status |
|---|---|
| PC-D1, PC-D2, PC-D3 | SOURCE REVIEWED · MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); specification decided (S412-D1 … D3, D6) |
| PC-B5 | SOURCE REVIEWED · MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); specification decided (S412-D5, D6) |
| PC-D4 | S4.12b |

---

# Part B — S4.12b: PC-D4 Total Portfolio Approach

## 9. PC-D4 (stages 1–7)

### 9.1 Sources read

| Source | Version · md5 | Read | Role |
|---|---|---|---|
| Treynor & Black, "How to Use Security Analysis to Improve Portfolio Selection", *J. Business* 46(1):66–86, 1973 | Published (JSTOR) · `4a0b5496a175` | In full 2026-10-18 | Primary for appraisal-ratio sizing and the forecast-to-alpha regression |
| Ang, Brandt & Denison, *Review of the Active Management of the Norwegian Government Pension Fund Global*, 20 Jan 2014 | Report · `da26aa3090d0` | §III.C and App. B–C re-read 2026-10-18 (in full 2026-10-02) | ANG's cited source: the TPA concept (Reference Portfolio, funding mix, active-risk appetite) |
| AQR Portfolio Solutions Group, "Total Portfolio Approach: A Quant Lens", *Alternative Thinking* 2026 Issue 2 | `16bf8f961f21` | pp. 3–16 re-read 2026-10-18 | Weight mechanics (owner decision D-5): appraisal ratio, fns. 11–12 |
| Gerard, BI course note GRA 6531 (13 Jan 2026) | `7295450f59a2` | Read; secondary | Teaching derivation of the single-fund case; nothing beyond T&B and AQR |
| Gilmore & Simonian 2025 (*JPM* 51(10)); Cavaglia, Han & Seshadri 2026 (*JPM* 52(6), cited by AQR); Elkamhi & Lee 2025 (*JPM* 51(8)) | — | Not in hand | Possible sources for a constrained TPA formulation (§10) *[2026-10-19]* Obtained (owner upload) and read after drafting: §9.8 |

### 9.2 What each source specifies

- **ANG:** "TPA two-factor (equity, bonds)" and nothing more. There are no factor definitions, exposure estimates, objective or constraints (ANG-15). ANG cites ABD in Exhibit 3 and also Gilmore & Simonian in the text (ANG-22). The name varies between "Approach" and "Allocation" (ANG-06).
- **ABD (§III.C, App. C):**
  - The owner sets a Reference Portfolio, "the minimum level of systematic risk" (CPPIB and GIC use 65/35), and an active-risk appetite, e.g. a tracking-error limit (§III.C.1).
  - Every investment is funded from the Reference Portfolio's assets. Its opportunity cost is a stock/bond mix (eq. 4: β = 1.3 ≡ $1.30 stocks − $0.30 bonds).
  - The mix is estimated by OLS with the coefficients constrained to sum to one (eq. A.3), which ABD call "a very crude way" (p. 122). The unspanned part (intercept plus residual) is what active management is for.
  - **No weight-producing rule** (ABD-5).
- **Treynor & Black:**
  - Single-index model. Active positions h_i ∝ μ_i/σ_i² on appraisal premiums (eq. 13). A market position completes the desired market exposure (eq. 16). Together these equal the unconstrained Markowitz solution (eq. 17).
  - The three stages are: maximise the appraisal ratio, blend with the market to maximise Sharpe, then lever or lend. Squared Sharpe = market ratio + appraisal ratio (eq. 19).
  - Appraisal premiums come from a forecast regression μ = ρ(s_z/s_e)(e + g) with residual variance (1 − ρ²)s_z² (eqs. 28–29). This is EQ-MAP-3 with IC = ρ and ω the residual volatility.
  - Without short selling, about half the terms of the appraisal ratio vanish (p. 78).
  - Assumes unlimited borrowing and short sales and no taxes (p. 67).
- **AQR:**
  - AR = α/σ_ε from a regression on stock and bond excess returns. SR²_max = SR²_current + AR² (fn. 11).
  - The allocation is ∝ AR/σ_ε, and existing weights fall by β times the allocation (fn. 12).
  - AQR says explicitly that it "assumes the investor is unconstrained" (p. 7).

### 9.3 Findings (verified, `s412b_tpa.py`)

| ID | Finding |
|---|---|
| — | T&B eqs. (10)–(17) equal the Markowitz tangency exactly; eqs. (19), (20), (25) hold; eqs. (28)–(32) by simulation; the p. 78 halving holds on average (squared ratio × ½, AR × 1/√2). AQR fns. 11–12 exact. ABD eq. (4) and the constrained OLS (A.3) reproduced (closed form = sample regression) |
| **TB-1** | T&B's "Sharpe ratio" and "appraisal ratio" are **squared** quantities (eq. 19; the paper says so for Sharpe). Modern usage (AQR) is α/σ_ε. Squared ratios add; unsquared ratios do not |
| **TPA-1** | With ABD's sum-to-one funding, the residuals are correlated with the reference. So total variance ≠ reference variance + tracking-error variance (cross-term nonzero in the solution). Total risk must be constrained explicitly (S410-D6) |
| **TPA-2** | **The funding set decides the alpha.** With cash as a funding leg (AQR's excess-return regression) an absolute-return asset keeps its 2.0% alpha. With stocks and bonds only (ABD, fully invested), its funding is forced into bonds and the alpha falls to 0.05%. Commodities go from +2.0% to −0.6%. AQR's appraisal ratios assume cash or leverage funding. A household that cannot borrow faces ABD's opportunity cost |
| **TPA-3** | The reference-relative TPA below **is Roll's benchmark-relative problem plus one linear constraint**: its active set is exactly {x : the funding exposures of x are zero}, and the objectives coincide (μ′Ma = α′a). Verified: same optimum. Solver note: the budget constraint is implied by the neutrality constraints (betas sum to one); stating both stalled SLSQP |
| **TPA-4** | **Coincidence with PC-B1:** with cash-funded betas, a reference that is the factor tangency (μ_f = λΣ_f w_ref) and no constraints, the tangency equals λ·reference + the funded active portfolio exactly. TPA then equals B1 at the T&B scale. Outside these conditions they differ |

### 9.4 Method record — PC-D4 reference-relative TPA (TPA-R, V1)

- **Identity:** PC-D4 · Total Portfolio Approach, two-factor (equity, bonds) (ANG Exh. 3 and 4; ANG-06) · family D · `M.PC` · roster v0 · **V1 (our specification; ABD has no weight rule)**.
- **Sources:**
  - The concept (Reference Portfolio, funding mix, active-risk appetite) is ABD §III.C.1–C.2, eq. (4), App. C (A.3).
  - Sizing: Treynor & Black eqs. (13)–(19) and AQR fns. 11–12.
  - The machinery is Roll 1992 and Jorion 2003 (EQ-TEV-1/2, S4.10).
- **Definition (EQ-NT-4):**
  - **Reference:** w_ref = `POL.benchmark`, with assets R (two: equity, bonds; three if the benchmark holds cash).
  - **Funding betas (ABD A.3):** β_i = argmin Var(r_i − β′r_R) s.t. 1′β = 1, computed from the authoritative Σ.
  - **Alphas:** α_i = μ_i − β_i′μ_R (S9's μ; zero for the reference assets).
  - **Active vector a ≥ 0 on the non-reference assets:** w = w_ref + Ma, where M subtracts β′a from the reference assets. The weights sum to one automatically, and the funding exposures stay at the reference's.
  - **Problem:** max α′a s.t. (Ma)′Σ(Ma) ≤ TE², w′Σw ≤ σ*², w ≥ 0, Policy Statement bounds. This is a convex SOCP.
  - **Unconstrained oracle (V0):** a = TE·Σ_ε⁻¹α/√(α′Σ_ε⁻¹α) (T&B/AQR, multivariate).
- **Inputs:**
  - μ (S9) and Σ (authoritative risk model) for betas, alphas and risk.
  - `POL.benchmark` (S410-D1) and the active-risk budget TE (Policy Statement; ANG's IPS has an active-risk-budget layer).
  - The signal route stays the S4.9 M cell: α = IC·ω·z with residual ω (EQ-MAP-3; T&B eq. 28 is its primary form).
- **Parameters:**
  - TE: user-authorised, required.
  - Funding set: the reference's assets (S412-D4).
  - No method parameter beyond these.
- **Constraints:** native (convex). Long-only applies through a ≥ 0 and w ≥ 0. The p. 78 effect applies: only positive-alpha assets are held, so the squared appraisal ratio is about halved.
- **Allocation domains:** asset class, fund/ETF. Security level is possible with a factor risk model.
- **Output and failures:**
  - Weights, plus a funding report (β, α, AR = α/σ_ε per asset, used TE).
  - `MISSING_REFERENCE` (no `POL.benchmark`).
  - `MISSING_ACTIVE_RISK_BUDGET`.
  - `REFERENCE_INFEASIBLE` (EQ-FEAS-1; S410-D4 handling).
  - `NO_POSITIVE_ALPHA`: returns the reference, with a record.
  - `INFEASIBLE_CONSTRAINTS`.
- **EQ-SPLIT-1:** exception class. The reference sets systematic risk, and σ* enters as a constraint inside (S410-D6). There is no post-scaling: scaling would move the funding exposures.
- **Invariants:**
  - Funding exposures equal the reference's.
  - The weights sum to one.
  - TE is binding unless no positive alpha remains.
  - The unconstrained form matches the closed form.
  - It equals Roll with neutrality (TPA-3), and equals B1 only under TPA-4.
- **Agent-readable summary:**
  - *Objective:* keep the owner's equity/bond risk mix and add other asset classes only where they beat the stocks-and-bonds mix that funds them, within the active-risk budget.
  - *Intuition:* ABD's opportunity-cost model turned into weights.
  - *Implicit belief:* the reference is the right systematic risk, and value comes only from unspanned returns.
  - *Sensitivities:*
    - Alphas are differences of capital-market assumptions (e.g. EM: μ_EM − 1.15μ_E + 0.15μ_F), so errors in μ_E and μ_F propagate through β.
    - The funding set (TPA-2).
    - Beta estimates for smoothed or illiquid assets (ABD App. C).
  - *Failure modes:* concentration in the few positive-alpha assets; nothing to do when no asset beats its funding mix.
  - *Valid comparisons:* Roll and Anchored EPO at the same TE.
  - *Invalid:* AQR-style appraisal ratios (cash-funded) for a fully invested portfolio without leverage.

### 9.5 Distinctness test (amendment 14)

Universe: equity and bonds (reference 60/40) plus HY, real estate, commodities, EM, small caps and absolute return. The factor-structured Σ has correlated residuals. TE budget 3%. Maximum absolute weight difference from TPA-R:

| Comparator | Max \|Δw\| | Note |
|---|---|---|
| PC-B1 long-only max Sharpe (= factor-MVO here: Σ is factor-structured) | 0.40 | Equity beta 0.14 vs the reference's 0.60 |
| PC-B1 with TE ≤ 3% vs the reference (EQ-MVO-3b) | 0.21 | Equity exposure drifts to 0.44 |
| Roll: max expected return s.t. TE ≤ 3% (no neutrality) | 0.44 | Equity exposure 0.77: TE spent on a factor tilt |
| Anchored EPO, anchor = reference, w set so TE = 3% | 0.40 | Shorts; factor exposures move |

**Result:**
- TPA-R is **distinct** from every comparator at the same active risk.
- Its defining content is that the factor exposure is pinned to the owner's reference and the whole active budget goes to unspanned returns.
- It coincides with B1 only in the unconstrained, cash-funded, factor-efficient-reference case (TPA-4).

### 9.6 Owner decision (stage 6)

*[2026-10-19]* **Owner decision: S412-D4 option (a).** TPA-R (V1) is the family-D candidate as specified in §9.4 (formal admission at G4 under ADR-0025, like every roster method), and the funding report (β, α, AR against `POL.benchmark`, funding set stated) becomes a lens on every candidate card (S4.16). In the discussion the owner first proposed following Gilmore & Simonian. After the three uploaded papers and ANG's own use of TPA were reviewed (§9.8), the choice was restated as A (framework and funding lens only), B (A plus the TPA-R candidate) and C (a Gilmore & Simonian multi-objective candidate; not recommended, because it duplicates the CIO's multi-criteria role and its objectives and weights are unspecified). The owner chose **B**, which is option (a) below; the letters differ only because of that restatement.

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **S412-D4** | PC-D4 specification or merge (amendment 14) | (a) **admit TPA-R (V1)** as the family-D candidate as specified in §9.4: reference = `POL.benchmark`, ABD sum-to-one funding over the reference's assets, betas from the authoritative Σ, alphas from S9's μ, max α′a s.t. the Policy Statement active-risk budget and the total-risk constraint, long-only; the unconstrained T&B/AQR form as the oracle; plus the funding report (β, α, AR) as a candidate-card lens for every candidate (S4.16) · (b) **merge**: no D4 candidate; "exposure-neutral TE optimisation" registered as a constraint option for benchmark-relative B-family candidates · (c) **relocate**: no TPA weights; funding decomposition and appraisal ratios only as an S4.16/S14 lens | **(a).** Distinct at matched TE. Every component is sourced: reference, active-risk appetite and funding are ABD; sizing is T&B/AQR; constraints are Roll/Jorion. It gives the ensemble the one candidate that keeps the owner's systematic mix by construction. The funding set follows ABD (no cash leg unless the reference holds cash) because the household cannot borrow (TPA-2) |

### 9.7 Handed forward

| To | Item |
|---|---|
| S4.16 | Funding report per candidate: ABD betas, alphas and appraisal ratios against `POL.benchmark`, with the funding set stated (TPA-2) |
| S4.20 | Failure codes; EQ-SPLIT-1 exception class; total-risk constraint inside (TPA-1); no redundant budget constraint with neutrality (TPA-3) |
| S9 / S9d | Alphas α = μ − β′μ_R from the CMA vector; the signal route via EQ-MAP-3 with residual ω (T&B eq. 28) |
| S10 | Betas from the authoritative Σ; unsmoothing for appraisal-based assets (ABD App. C.1) |
| S7 | Concentration and alpha sensitivity as evaluation hypotheses (no ranking here) |

| Method | Status |
|---|---|
| PC-D4 | SOURCE REVIEWED · MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level and V1); specification decided (S412-D4 (a), 2026-10-19) |

### 9.8 Sources read after drafting: the three TPA papers and ANG's own use (2026-10-18/19)

The owner uploaded the three papers the gap memo listed as optional (§10 item 4). They were read in full, with ANG's own treatment of TPA re-checked against both paper versions, before S412-D4 was decided.

| Source | Version · md5 (zip / pdf) | What it says about TPA | Effect on §9.4 |
|---|---|---|---|
| Gilmore & Simonian, "Some Practical Considerations for the Total Portfolio Approach to Pension Fund Management", *JPM* 51(10):40–48, 2025 (*Future of Asset Management 2025*) | Owner upload · `9f42284f7dd0` / `a2598d982802` | A holistic framework: one team, total-portfolio objectives, risk factors throughout. Its tools are multi-objective optimisation (a Pareto frontier over plan goals), dimension reduction and factor investing. It gives no TPA weight rule, and it cautions that anchoring to a reference portfolio, and trying to beat it, can pull attention from the plan's own goals | None. A multi-objective candidate would duplicate the CIO's multi-criteria role and needs objectives and importance weights the paper does not give (option C, not chosen) |
| Elkamhi & Lee, "Total Portfolio Approach", *JPM* 51(8), 2025 (*Portfolio Manager Perspectives 2025*, pp. 110 ff.) | Owner upload · `9a04b3d83470` / `8f7d10133090` | TPA as a mindset of preparedness rather than a strategy: governance through guardrails and ranges, dynamic positioning, factor-based tools. No weight rule | None. Guardrails and ranges are Policy Statement bounds; dynamic, regime-aware positioning stays in S9 and S13 |
| Cavaglia, Han & Seshadri, "Applying the Appraisal Ratio and Style Analysis to Total Portfolio Management", *JPM* 52(6), April 2026 (pp. 74 ff.) | Owner upload · `debdd580831d` / `017eb7e9302a` | A reference portfolio set by the board; the appraisal ratio of a candidate regressed on the reference as the key TPA metric, with SR² additivity; the single-candidate weight w\* = w₀/(1 + (1 − β)w₀), w₀ = (AR/SR_P)(σ_P/σ_ε); style analysis as a complement. The reference need not be efficient. The AR section (pp. 75–76) cites Hecht (2014) and Kepos (2018) for extending the base portfolio to any mix of return drivers | Supports the funding-report lens directly: per-asset AR against the reference. The weight is T&B's one-asset case, funded from the reference; verified against the mix's Sharpe ratio (`s412b_tpa.py`, 453 cases). No new variant |

**ANG's own use of TPA (re-checked in both versions):**
- **v2 (21 Sep 2026):** one Exhibit 3 row, "Total Portfolio Approach (TPA) two-factor (equity and bonds)", cited to ABD 2014. One sentence in §3.3 (p. 10) says TPA is gaining popularity with institutions and is not bound by traditional asset classes, citing ABD and Gilmore & Simonian. No formulation and no code.
- **April 2026 draft:** the same roster row (Exhibit 4 there), named "Total Portfolio Allocation" (ANG-06); the text cites ABD only. Vote and weight results identical.
- **Results:** 6th of 21 in the agents' vote; 2.7% of the final ensemble (Exhibit 8), the lowest weight, tied with the Adversarial Diversifier. No TPA weights are shown.
- **IPS:** ex-ante tracking error against the 60/40 benchmark must not exceed 6%, a hard constraint on the final portfolio. The engine's counterpart is `POL.benchmark` with the Policy Statement active-risk budget, which TPA-R uses.
- **Third-party implementation:** TPA is missing (`S4_GITHUB_IMPL_REVIEW.md`, PC roster row).

**Conclusion.** All three papers treat TPA as a framework, not a construction method; none gives a constrained TPA weight rule. ANG's label is reproducible only through ABD. Nothing read here changes TPA-R (V1); Cavaglia et al. strengthen the case for the funding-report lens.

---

## 10. TPA gap memo (amendment 14 deliverable)

1. **ANG gives no formulation** (ANG-15). Its cited source (ABD) is a funding and benchmarking framework without a weight rule (ABD-5).
2. **What we used, by class:**
   - **Primary:** Treynor & Black for sizing and the forecast mapping.
   - **ANG's cited source:** ABD for the concept, the funding regression and the active-risk appetite.
   - **Practitioner, owner decision D-5:** AQR for the multivariate appraisal-ratio sizing.
   - **Already verified (S4.10):** Roll and Jorion for the constrained machinery.
3. **What we had to specify ourselves (V1):**
   - the combination into one optimisation (TPA-R);
   - the funding set for an unlevered household (ABD's sum-to-one, TPA-2);
   - betas from the authoritative Σ rather than separate regressions;
   - alphas from S9's μ;
   - the explicit total-risk constraint (TPA-1).
4. **Gaps that remain (class B: not in hand, not a constraint on proceeding):**
   - Gilmore & Simonian 2025 (cited in ANG's text) may describe the practice ANG intended.
   - Cavaglia, Han & Seshadri 2026 and Elkamhi & Lee 2025 may contain a constrained or univariate appraisal-ratio formulation.
   - None is needed for the mathematics above. If obtained, they are read against §9.4 and may add a variant.
   - *[2026-10-19]* **Closed.** All three obtained (owner upload) and read (§9.8). None gives a constrained TPA weight rule; Cavaglia et al.'s single-candidate weight is T&B's one-asset case (verified). No variant added.
5. **Distinctness:** passed (§9.5). TPA-R is not a relabelled B1, B7 or factor-MVO. It is Roll's problem with the owner's systematic exposure held fixed (TPA-3).

