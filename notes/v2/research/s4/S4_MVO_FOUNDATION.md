# S4.6 Mean–variance foundation (supports PC-B1, PC-C1)

**Document status:** DRAFT (2026-10-08). Awaiting owner decision S46-D1 (§5). · **Basis:**
- S4_PLAN §G (step S4.6) and §F (EQ-MVO-1 … EQ-MVO-4);
- `S4_METHODS_OUTLINE.md` §1 (nine-stage workflow) and §2 (S4.6 plan);
- ADR-0024 §3 (parameter authority), ADR-0027 D3 and D5 (risk model per problem; declared units);
- `S4_RISK_MODEL_CHOICE.md` (M-1, M-2), `S4_HEURISTICS.md` (S45-D4, EQ-H-1b).

**Related files:**
- Equations: `S4_EQUATION_REGISTER.md`, S4.6 entries (EQ-MVO-1 … EQ-MVO-4 with sub-equations; EQ-MVO-E1, E2).
- Verification: `verification/s46_mvo_closed_forms.py`, `verification/s46_estimation_error_jorion.py` (both PASS; synthetic data, plus Jorion's published parameters).
- Issues: `ANG_ISSUES_REGISTER.md` (ANG-47 new; ANG-44 extended).

**What this step is:** the shared mathematics under every mean–variance method: the problem, its closed forms, the riskless asset, the minimum-variance portfolio, constraints, and the estimation-error problem. **Method records are written where the methods are specified:** maximum Sharpe (PC-B1) at S4.7, global minimum variance (PC-C1) at S4.11. Nothing here selects or ranks methods.

**Exit criterion (S4_PLAN §G):** "closed form = solver within tolerance". Met (§6).

---

## 0. Summary

**Findings:**
1. **Markowitz (1952) is long-only and has no riskless asset.** Efficient means "minimum V for given E or more and maximum E for given V or less", with short sales excluded (pp. 81–82). Long-only efficient weights are piecewise linear between corner portfolios (p. 87); our solver traces this exactly.
2. **The tangency portfolio and separation come from Tobin (1958) and Sharpe (1964), not Markowitz.** Tobin proves that the composition of the risky assets is independent of how much is held in cash, "only so long as cash is assumed to be a riskless asset" (pp. 84–85). ANG cites Markowitz (1952) for maximum Sharpe ratio (ANG-47, L).
3. **Closed forms verified against numerical solvers:** GMV, the budget-only frontier and its variance, two-fund separation, the utility form's position on the frontier, tangency = numerical maximum Sharpe, and Tobin separation.
4. **The tangency formula fails when the cash rate is at or above the GMV mean.** It then returns a portfolio with negative expected excess return. A maximum-Sharpe method must report failure in that case.
5. **Long-only maximum Sharpe** is solved exactly by a convex reformulation (verified against direct maximisation).
6. **Long-only minimum variance is covariance shrinkage.** The long-only GMV equals the unconstrained GMV of Σ − λ1′ − 1λ′, with λ the short-sale multipliers (Jagannathan & Ma, as restated by DeMiguel et al. 2009). We verified it through the optimality conditions, which explains our earlier finding that long-only constraints regularise (M-1).
7. **Estimation error.**
   - The unconstrained weights' relative error can reach κ(Σ) times the relative error in expected returns. The bound is attained, which quantifies Michaud's "error maximisation".
   - Jorion's (1986) published simulation reproduces from his Table 1: all 15 testable risk cells of Table 2 are within the paper's own Monte Carlo error.
   - Minimum variance, which ignores expected returns, beats every μ-based rule in short samples (T ≤ 40 months) and loses in long ones. Shrinking means toward the GMV mean (Bayes–Stein) beats sample means at every sample size.
8. **Cash cannot be a row of Σ** at the asset-class level. With a 0.5%-volatility cash row, the minimum-variance portfolio is 99.1% cash and the condition number rises from 16 to 1,811 (decision S46-D1).

**Decision for the owner:** S46-D1, cash as the riskless asset (§5).

---

## 1. Sources read (stage 1)

| Source | Version in hand | Read | Role |
|---|---|---|---|
| Markowitz (1952), *JF* 7(1):77–91 | Published (JSTOR), 16 pp., md5 `6d3a4f0d62ae` | Full | Problem definition; long-only efficient set; critical lines |
| Tobin (1958), *RES* 25(2):65–86 | Published (JSTOR), 23 pp., md5 `665232264639` | §3.6 in full (pp. 82–85) and the setting (§§2–3) | Riskless asset; separation; linear opportunity locus |
| Sharpe (1964), *JF* 19(3):425–442 | Read at S4.5 | Full | Capital market line |
| Michaud (1989), *FAJ* 45(1):31–42 | Read at S4.4 | Full | Error maximisation (`S4_RISK_MODEL_CHOICE.md` §1.1) |
| Jorion (1986), *JFQA* 21(3):279–292 | Published (JSTOR), 15 pp., md5 `06ef6474672c` | Full; Tables 1–2 read from page images | Estimation risk; Bayes–Stein; reproduced |
| DeMiguel, Garlappi, Nogales & Uppal (2009), *Mgmt Sci* 55(5):798–812 | Published, md5 `32133579bf40` (in the thesis folder) | §2 and §3.1 | Supporting: the Jagannathan–Ma restatement and Proposition 1 |
| DeMiguel, Garlappi & Uppal (2009) | Read at S4.5 | Full | Utility form; critical window (EQ-H-1b) |
| Jagannathan & Ma (2003); Kan & Zhou (2007) | **Not in hand** (supporting, not blocking per the plan) | — | J&M's result is covered by DGNU's restatement plus our own derivation; Kan & Zhou's loss framework is reflected in DGU's Proposition 1 (reproduced at S4.5) |

---

## 2. The foundation (stage 2)

Full register entries: `S4_EQUATION_REGISTER.md`. In brief:

| ID | Content | Status |
|---|---|---|
| EQ-MVO-1 | The problem in risk form (minimum variance for a target mean) and utility form (max w′μ − (γ/2)w′Σw), with the Policy Statement constraint set 𝒲 applied natively | Verified: the utility form lies on the frontier at m = B/A + D/(Aγ) |
| EQ-MVO-2 | Budget-only frontier in closed form; σ²(m) = (Am² − 2Bm + C)/D; two-fund separation | Verified against SLSQP to 1e-6 |
| EQ-MVO-2a | Long-only frontier: piecewise-linear weights between corner portfolios (Markowitz p. 87) | Verified: exactly linear within each active set |
| EQ-MVO-3 | Riskless asset: w_tan = Σ⁻¹μ/1′Σ⁻¹μ, SR_max = √(μ′Σ⁻¹μ), separation (Tobin) | Verified; failure condition r_f ≥ m_g |
| EQ-MVO-3a | Long-only maximum Sharpe via min y′Σy s.t. μ′y = 1, y ≥ 0 | Verified against direct maximisation |
| EQ-MVO-4 | GMV: Σ⁻¹1/1′Σ⁻¹1, variance 1/A | Verified |
| EQ-MVO-4a | Long-only GMV = GMV of Σ − λ1′ − 1λ′; 1-norm (δ = 1) equivalence | Verified through KKT |
| EQ-MVO-E1 | Relative weight error ≤ κ(Σ) × relative input error; attained | Verified |
| EQ-MVO-E2 | Bayes–Stein means and predictive covariance (Jorion eqs. 14–18) | Tables 1–2 reproduced |

**How constraints enter.**
- For mean–variance methods, the Policy Statement's linear constraints (bounds, group limits, long-only, budget) enter **natively** as constraints of a convex quadratic programme, as ANG states: "various considerations in the IPS treated as constraints" (ANG p. 5).
- Closed forms exist only for the budget-only problem. Everything else is solved numerically, and the solution is checked through its optimality conditions (as done here for long-only GMV).
- Non-linear Policy Statement limits (drawdown, CVaR) belong to S4.12.

---

## 3. ANG versus the sources (stage 3)

| ID | ANG says | Sources say | Consequence | Status |
|---|---|---|---|---|
| ANG-47 | Exhibit 3 cites Markowitz (1952) for "Maximum Sharpe ratio" | Markowitz has no riskless asset and no Sharpe ratio; his efficient set is long-only. The tangency portfolio and separation are Tobin's (1958, §3.6) and Sharpe's (1964, Part III) | PC-B1's governing sources are Tobin and Sharpe for the tangency, and Markowitz for the problem | New (L) |
| ANG-44 (extended) | Cash is one of 18 classes (p. 15); a 3.7% risk-free rate appears in the CMAs (p. 16) | The riskless-asset results hold only if cash is riskless (Tobin pp. 84–85) | How cash enters the optimisers is unspecified for every family, not only the heuristics | Extended → S46-D1 |
| — | "various considerations in the IPS treated as constraints" (p. 5) | Markowitz's efficient set is defined under constraints (p. 81) | Consistent: native linear constraints for MV methods | Recorded |

---

## 4. Inputs, units and parameters (stages 4–5)

**Inputs** (the risk object is the authoritative Σ for the strategic asset-class problem, ADR-0027 D3):

| Input | Class | Basis |
|---|---|---|
| μ | A.CMA (S9) | Expected returns **in excess of the numéraire cash rate**, one declared basis (I-4; ADR-0027 D5: currency, nominal/real, horizon, arithmetic) |
| Σ | A.RISK, authoritative (S10) | Covariance of the same excess returns, same horizon and units |
| r_f | Data (S5/S6) | Numéraire cash rate for the horizon |
| 𝒲 | Policy Statement | Linear constraints: bounds, group limits, long-only, budget |

**Parameters:**

| Parameter | Authority | Note |
|---|---|---|
| Constraint set 𝒲 | User-authorised | From the Policy Statement, narrowed by account capability |
| γ (utility form only) | System-estimated by an accepted calibration method | Specific to the formulation and its units; never a portable investor attribute (`S2_RISK_PREFERENCE_RESEARCH.md`; RQ-02). PC-B1 (tangency) needs no γ |
| Target m or target volatility (risk form only) | User-authorised or derived by a declared rule | Fixed per method at S4.7 |
| Solver tolerances | Fixed | Recorded with each run (determinism) |

---

## 5. Owner decision (stage 6): S46-D1 — cash at the asset-class level

| Option | Description |
|---|---|
| **(a) Numéraire cash is the riskless asset** | Every μ and Σ is for returns in excess of the numéraire cash rate r_f, and cash is not a row of Σ. Methods return risky-asset weights (1′w = 1). The cash share is set outside the method by the Policy Statement (e.g. a liquidity floor), or by a method whose definition includes the riskless asset: A5's residual (S45-D1), or a declared position on the capital market line. Never beyond the leverage the Policy Statement allows. Foreign-currency cash is a risky asset (it carries FX risk) |
| (b) Cash as a risky asset | Cash is a row and column of Σ with its own small volatility and correlations, and every method allocates to it directly |
| (c) Both | Riskless for definitions, plus a cash row for some problems |

**Recommendation: (a).** Reasons:
1. **Sources.** Tobin's separation and the linear opportunity locus need a riskless asset (pp. 84–85). Sharpe's capital market line, and DGU, KO, Jorion and MM, all work in excess returns over the risk-free rate.
2. **Numerics (verified).**
   - With a 0.5%-volatility cash row, GMV puts 99.1% in cash, and κ(Σ) rises from 16 to 1,811, which multiplies error amplification (EQ-MVO-E1).
   - At S4.5 the same row put 80% / 98.5% of inverse volatility / inverse variance in cash.
   - Under (b), several methods would become cash allocations.
3. **Consistency.** It matches S45-D4, which puts the heuristics on risky assets only.
4. **The cost, stated openly.** Cash is riskless only in the numéraire's nominal terms. If CMAs are stated in real terms (ADR-0027 D5), numéraire cash carries inflation risk. The decision therefore depends on the units basis fixed at S5/S9; under a real basis, the cash rate is the real return on numéraire cash and its variance is ignored by assumption.

---

## 6. Verification (stage 7)

| Script | Reproduces / proves | Result |
|---|---|---|
| `s46_mvo_closed_forms.py` | The S4.6 checks listed below | PASS |
| `s46_estimation_error_jorion.py` | Jorion Table 1 statistics; F_MAX 0.99728 (0.99734); Table 2 at T = 25/50/100/200 (15 risk cells within 1.7 of the paper's Monte Carlo SE; shrinkage mean within 2.5 SE, SD within 10%); the p. 288 orderings | PASS |

`s46_mvo_closed_forms.py` checks:
- GMV, frontier and variance identity, two-fund separation, utility form (40 random problems; SLSQP to 1e-6);
- tangency = numerical maximum Sharpe; Tobin separation; the r_f ≥ m_g failure;
- long-only maximum Sharpe, convex form vs direct maximisation;
- Markowitz critical lines (121 QP solutions);
- Jagannathan–Ma through KKT; DGNU Proposition 1;
- the κ bound attained; GMV with cash in Σ.

**Exit met:** closed form = solver within tolerance (1e-6 for the budget-only problems).

**What the estimation-error evidence says for the engine** (to be reused, never as a selection rule):
- **Expected-return error dominates.** This is consistent across Michaud (p. 38), M-1 (`S4_RISK_MODEL_CHOICE.md`), DGU's critical windows (EQ-H-1b) and Jorion's Table 2.
- **Shrinkage helps, and so do constraints.** Jorion: Bayes–Stein beats sample means at every T. Jagannathan–Ma: long-only acts as covariance shrinkage. EPO (S4.7) shrinks the correlations.
- **μ-free methods are relatively robust in short samples.** Jorion's minimum-variance rule has the lowest loss for T ≤ 40 months and the highest at T = 200. This supports keeping both μ-dependent and μ-free families, with S7 deciding on evidence, not here.

---

## 7. Handed forward

| To | Item |
|---|---|
| S4.7 | PC-B1 record: tangency (EQ-MVO-3) with Tobin and Sharpe as governing sources (ANG-47); long-only form EQ-MVO-3a; failure codes `TANGENCY_UNDEFINED`, `NO_POSITIVE_EXCESS_RETURN`; the frontier-point rule (γ or target) per B method; EPO's problem portfolios (EQ-MVO-5) linked to EQ-MVO-E1 |
| S4.11 | PC-C1 record: EQ-MVO-4/4a; Clarke, de Silva & Thorley 2006 (in hand) for the long-only, 3% upper-bound design and their covariance structuring (p. 14) |
| S4.13 | μ-dependent methods need A.CMA and Σ on one basis; GMV needs Σ only |
| S4.15 / S9 | Bayes–Stein (EQ-MVO-E2) as a candidate expected-return estimator (M.CMA), with the conventions that reproduce Jorion |
| S4.16 | κ(Σ) as a CRO diagnostic for μ-dependent methods |
| S5 / S9 | The numéraire and units basis that S46-D1 depends on |
| S7 | Jorion's and DGU's loss framework as design input for the evaluation protocol |
| S2 / RQ-02 | γ calibration for utility-form methods |

---

## 8. Status after S4.6

| Item | Status |
|---|---|
| EQ-MVO-1 … EQ-MVO-4 (+ 2a, 3a, 4a), EQ-MVO-E1, E2 | EXTRACTED · VERIFIED |
| PC-B1, PC-C1 | Foundation mathematics extracted and verified; method records at S4.7 and S4.11 |
| S46-D1 | Awaiting owner decision |
