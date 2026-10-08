# S4.7 Mean–variance family — PC-B1, B2, B3, B4, B6, B7: method records

**Document status:** DRAFT (2026-10-08). Awaiting owner decisions S47-D1 … S47-D6 (§5). · **Basis:**
- S4_PLAN §G (step S4.7) and §F (EQ-MVO-5, EQ-EPO-1 … 5, EQ-BL-1 … 3, EQ-ROB-1 … 2, EQ-REF-1);
- `S4_METHODS_OUTLINE.md` §1–§2;
- `S4_MVO_FOUNDATION.md` (S4.6; S46-D1);
- ADR-0024 §3–§5, §7 (EPO lineage); ADR-0025 (admission); ADR-0027 D3–D4 (risk model; runtime diagnostics); decision D-2 (Michaud IP check).

**Related files:**
- Equations: `S4_EQUATION_REGISTER.md`, S4.7 entries.
- Verification: `verification/s47_max_sharpe.py`, `s47_epo_pbl.py`, `s47_black_litterman.py`, `s47_robust_mv.py`, `s47_resampled_frontier.py` (all PASS; synthetic data and published inputs). Earlier: `s44_black_litterman_*.py`, `s46_*.py`.
- Issues: `ANG_ISSUES_REGISTER.md` (ANG-41, ANG-47 annotated; ANG-48, ANG-49 new; BL-2, MCH-1, PBL-1, PBL-2).

**Scope:** the mathematics of the six return-optimised methods, verified against their sources. **Nothing here selects or ranks methods** (admission ADR-0025, evaluation S7).

---

## 0. Summary

**Findings:**
1. **Maximum Sharpe (B1)** under Policy Statement constraints (caps, group limits, tracking error) is a convex problem after the substitution y = κx. It matched multi-start direct maximisation in all 25 test problems, with constraints binding.
2. **EPO (B6/B7) unifies the family.** PBL's general EPO contains:
   - standard MVO (w = 0);
   - the anchor (w = 1, or τ = 0);
   - Black–Litterman with absolute views (P = I);
   - robust optimisation with an ellipsoidal set for expected returns;
   - ridge-type regularisation.

   Every one of these identities was verified numerically. The fully shrunk EPO with a TSMOM-type signal is equal-volatility weighting, the same weighting as inverse volatility (PC-A3).
3. **A boundary case in PBL's robust result (PBL-1).** When the uncertainty set is large (c ≥ c*), the robust portfolio is exactly the anchor, which corresponds to τ = 0. Proposition 2's statement covers only τ > 0. This is minor.
4. **Black–Litterman (B2).**
   - BL 1992 optimises with Σ, treating covariances as known (fn. 4), and uses a diagonal Ω.
   - The appendix formula has a misprint (BL-2). Read literally it gives τ²Π instead of Π when there are no views.
   - When Ω is proportional to τ, as in both He–Litterman's and Idzorek's rules, τ cancels from the posterior mean.
5. **Robust mean–variance (B3, Goldfarb & Iyengar).** The verified elements are:
   - the worst-case formulas (vertex enumeration and brute force over the ellipsoid);
   - the factor-model shortcut for the worst case;
   - the robust minimum-variance and maximum-Sharpe problems;
   - the regression-calibrated uncertainty sets, which give 95% coverage at ω = 0.95.

   Two caveats:
   - G&I need a **factor model and its regression statistics**, which ANG's PC inputs do not provide (ANG-48).
   - The simpler robust variant with ellipsoidal uncertainty in expected returns **is EPO** (PBL Prop. 2), so it would not be a distinct method.
6. **Resampled frontier (B4).** Michaud & Michaud's published example reproduces:
   - classical maximum Sharpe within 0.6 percentage points, and minimum variance;
   - resampled minimum-variance, middle and maximum-return portfolios within 0.7, 1.6 and 3.0 percentage points (500 replications).

   The procedure and the "forecast confidence" parameter are patented or patent-pending (D-2). ANG specifies none of its parameters (ANG-49). Table 6.1's "middle" portfolio is not defined (MCH-1).
7. **Estimation error, the common thread.** On the printed inputs, the unconstrained maximum-Sharpe ratio moves between 0.245 and 0.264 from input rounding alone, while the long-only result is stable. This is Michaud's error maximisation, and it is why every method here regularises (shrinkage, constraints, robustness or resampling).

**Decisions for the owner (§5):**
- S47-D1: Black–Litterman convention.
- S47-D2: how the EPO shrinkage w is set.
- S47-D3: the anchor for anchored EPO.
- S47-D4: robust mean–variance specification.
- S47-D5: resampled-frontier specification and the IP check.
- S47-D6: the cash/risky split carried from S46-D1, which affects every method here.

---

## 1. Sources read (stage 1)

| Method | Governing source | Version | Read | Notes |
|---|---|---|---|---|
| PC-B1 | Tobin 1958; Sharpe 1964 (tangency), Markowitz 1952 (problem) | Read at S4.5/S4.6 | — | ANG-47 |
| PC-B2 | Black & Litterman 1992, *FAJ* 48(5):28–43 | Published (JSTOR), md5 `6a8e2bbebdb4` | Views section, appendix (p. 42), footnotes (p. 43); tables located, not transcribed | He & Litterman, Idzorek reproduced at S4.4. Printed page = PDF page + 26 |
| PC-B3 | Goldfarb & Iyengar 2003, *MOR* 28(1):1–38 | Published (JSTOR), md5 `09a33510a521` | §§2–3, §5 and the special case (pp. 1–20); equations from page images | Printed page = PDF page − 1 |
| PC-B4 | Michaud & Michaud 2008, *Efficient Asset Management*, 2nd ed. | Book (owner upload) | Ch. 2 data (p. 16), ch. 5 (pp. 36–39), ch. 6 (pp. 42–56) | Patented procedure (D-2) |
| PC-B6, PC-B7 | Pedersen, Babu & Levine 2021, *FAJ* 77(2):124–151 | Published, open access, md5 `82ce461a4258`; author version md5 `75c0752ae184` (same structure; equation numbers differ) | §§II–III, Tables 1–2, Fig. 2, App. B; equations from page images | Not in ANG (roster extension) |

**Not reproduced:**
- PBL's and BL's empirical tables (they need data).
- BL 1992's tables. Its currency-hedged equilibrium across about 20 assets would need a long transcription from scanned tables; its posterior arithmetic is covered by the He & Litterman and Idzorek reproductions (S4.4).

---

## 2. Lineage (MVO → estimation error → regularisation)

```
                  Markowitz (1952) problem ─── Tobin (1958) / Sharpe (1964): riskless asset, tangency
                                   │
                   PC-B1 maximum Sharpe (EQ-MVO-3, 3a, 3b)
                                   │   estimation error: κ(Σ) amplification (EQ-MVO-E1),
                                   │   problem portfolios (EQ-MVO-5), DGU / Jorion (S4.5, S4.6)
       ┌───────────────┬───────────┴─────────────┬──────────────────────┐
  shrink the inputs   Bayesian prior          robust worst case      resample and average
  (risk and signal)   (equilibrium anchor)    (uncertainty sets)     (estimation noise)
       │               │                         │                      │
  PC-B6 simple EPO    PC-B2 Black–Litterman   PC-B3 robust MV        PC-B4 resampled frontier
  PC-B7 anchored EPO  (P = I case = EPO,      (G&I factor-model      (Michaud & Michaud)
  (PBL 2021)           PBL Prop. 3)            sets; the ellipsoidal-mean
                                                case = EPO, PBL Prop. 2)
```

EPO's Proposition 3 shows that B6/B7 nest MVO, the anchor, BL with absolute views and ellipsoidal-mean robust optimisation. What keeps B2, B3 and B4 distinct from EPO:
- **B2:** relative views (P ≠ I) and the market-equilibrium anchor.
- **B3:** factor-model uncertainty in the covariance, not only in the mean.
- **B4:** a non-parametric averaging of re-optimised portfolios.

---

## 3. ANG and sources (stage 3)

| ID | Finding | Status |
|---|---|---|
| ANG-47 | Maximum Sharpe cites Markowitz 1952; the tangency comes from Tobin and Sharpe | Recorded at S4.6; PC-B1 record below |
| ANG-41 | BL conventions unspecified (Σ vs Σ + M̄⁻¹; Ω; τ) | → S47-D1 |
| ANG-48 (new) | Robust MV: which of G&I's problems (min variance / max return / max Sharpe) and which uncertainty sets is not specified; G&I need a factor model and regression statistics, which are not among ANG's PC inputs (CMAs + Σ); the ellipsoidal-mean alternative coincides with EPO | → S47-D4 |
| ANG-49 (new) | Resampled frontier: replications, simulated sample length (forecast confidence), association rule and frontier point are unspecified; the procedure is patented | → S47-D5 |
| BL-2 | BL 1992 appendix item 8 misprint | Source issue (L) |
| PBL-1 | Prop. 2 boundary at c ≥ c* | Source issue (L) |
| PBL-2 | The grid for the out-of-sample w choice is not stated | Source issue (L) |
| MCH-1 | Table 6.1 "middle" undefined; France/Japan tie in the printed inputs | Source issue (L) |

---

## 4. Method records (stages 2, 4, 5, 7)

Common to all six:
- **Inputs:** μ = CMA excess returns over the cash rate (S46-D1; A.CMA, S9) and Σ (authoritative risk model of the strategic problem, ADR-0027 D3).
- **Domains:** asset class, fund/ETF, security, sleeve, provided μ and Σ are defined there.
- **Constraints:** Policy Statement linear and tracking-error constraints enter natively. Non-linear limits (drawdown, CVaR) do not (S4.12).
- **Output:** risky-asset weights. The cash share is set per S47-D6.
- **Failures:** typed records (I-2), never a silent fallback.

### PC-B1 Maximum Sharpe ratio
- **Sources:**
  - Tobin 1958 §3.6 and Sharpe 1964 Part III: tangency and separation.
  - Markowitz 1952: the problem.
  - ANG cites Markowitz only (ANG-47).
- **Definition:** w_tan = argmax μ′x/√(x′Σx) over the constraint set (EQ-MVO-3/3a/3b). Closed form when only the budget applies.
- **Parameters:** none beyond the constraint set (user-authorised) and r_f (S46-D1).
- **Failures:**
  - `TANGENCY_UNDEFINED`: budget-only problem with r_f ≥ m_g;
  - `NO_POSITIVE_EXCESS_RETURN`.
- **Invariants:**
  - independent of risk aversion (Tobin);
  - invariant to scaling μ by a positive constant;
  - convex solution = direct maximum.
- **Verification:** `s46_mvo_closed_forms.py`, `s47_max_sharpe.py`.
- **Agent-readable summary:**
  - *Objective:* highest expected excess return per unit of risk.
  - *Sensitivities:* the most sensitive method to errors in μ (EQ-MVO-E1; the unconstrained Sharpe moves 0.245–0.264 under input rounding alone).
  - *Valid comparison:* the efficient benchmark when CMAs are trusted.
  - *Invalid comparison:* in-sample Sharpe as evidence of quality (I-9).
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level).

### PC-B2 Black–Litterman
- **Sources:** BL 1992 (governs); He & Litterman 1999 and Idzorek 2005 (S4.4).
- **Definition:**
  - prior Π = δΣw_mkt (EQ-BL-1);
  - posterior E[R]‾ with views (P, Q, Ω) (EQ-BL-2);
  - optimisation on the posterior (EQ-BL-3).
- **Inputs:**
  - w_mkt from PC-A2 data (S45-D3);
  - δ;
  - views from the AC agents' CMAs (S4.15/S9);
  - Ω from the CMAs' confidence.
- **Parameters (recommended, S47-D1):**
  - δ: system-estimated (market risk premium and variance);
  - P = I (absolute views, one per asset class);
  - Q = the CMA vector;
  - Ω diagonal (BL 1992 item 7) with ω_i from each CMA confidence via Idzorek's closed form (IDZ-1);
  - τ fixed (it cancels when Ω ∝ τ);
  - optimisation with Σ (BL 1992).
- **Role boundary:** BL equilibrium returns are also an ANG CMA method (CMA-3, S4.15). As a CMA they are a belief input; as PC-B2 they are a construction method. The two roles stay distinct.
- **Invariants:**
  - no views → Π, hence the market portfolio;
  - full confidence → the views hold exactly;
  - P = I equals Bayesian EPO with the market anchor.
- **Verification:** `s44_black_litterman_*.py`, `s47_black_litterman.py`, `s47_epo_pbl.py`.
- **Agent-readable summary:**
  - *Intuition:* start from the market and tilt toward views in proportion to confidence.
  - *Sensitivities:* the views' confidence; δ; the market weights (data contract).
  - *Failure modes:* market weights undefined for some classes (cash, commodities: S45-D3).
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); convention pending S47-D1.

### PC-B3 Robust mean–variance
- **Source:** Goldfarb & Iyengar 2003.
- **Definition (recommended, S47-D4):** robust maximum Sharpe (eqs. 35–39) with factor-model uncertainty sets:
  - box for the means;
  - ellipsoids for the loadings;
  - intervals for the residual variances;
  - calibrated by the §5 regression confidence regions at ω.
- **Inputs:**
  - a factor model (V₀, F, D) and its regression statistics (s_i², AᵀA) over p periods;
  - μ (the regression intercepts in G&I, or CMA-based means: S47-D4).
- **Parameters:**
  - ω: fixed at 0.95 (G&I's typical range 0.95–0.99); 0.99 as sensitivity-only;
  - factors: declared in the contract;
  - d̄: a worst-case residual-variance rule.
- **Failures:**
  - `NO_POSITIVE_WORST_CASE_EXCESS_RETURN`: G&I's constraint qualification, i.e. at least one asset's worst-case return above r_f;
  - `NO_FACTOR_MODEL`.
- **Invariants:**
  - zero uncertainty reduces to the classical problem;
  - the worst case is a valid bound;
  - the robust optimum beats the classical portfolio's worst case.
- **Verification:** `s47_robust_mv.py`.
- **Agent-readable summary:**
  - *Intuition:* optimise against the worst parameters inside a confidence region, so noisy estimates are penalised.
  - *Sensitivities:* ω and the factor choice.
  - *Failure modes:* too large an ω gives a very conservative portfolio (G&I p. 18).
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); specification pending S47-D4.

### PC-B4 Resampled efficient frontier
- **Source:** Michaud & Michaud 2008 (governs; ANG cites Michaud 1998). **IP check first (D-2).**
- **Definition:**
  - simulate T periods from (μ, Σ) and re-estimate;
  - compute the constrained efficient frontier (51 portfolios);
  - repeat K times and average the rank-associated portfolios (EQ-REF-1).
- **Parameters (recommended, S47-D5):**
  - T = the length of the estimation sample. That is the book's base case; tuning T as a "forecast confidence" level is patent-pending and is not adopted;
  - K ≥ 1,000: at 500, our reproduction differed from the book by up to 3 percentage points;
  - rank association (the book's default);
  - seed recorded;
  - proposal = the RE portfolio with the highest Sharpe ratio on the original inputs (parameter-free and consistent with B1); λ-association is the alternative.
- **Invariants:**
  - weights sum to 1 and are non-negative;
  - the fn. 7 identity;
  - large T approaches the classical frontier.
- **Verification:** `s47_resampled_frontier.py` (specification check only).
- **Agent-readable summary:**
  - *Intuition:* average many equally plausible optimal portfolios.
  - *Sensitivities:* T (confidence); K (Monte Carlo noise).
  - *Valid comparison:* against the classical frontier on the same inputs.
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (specification check); implementation blocked until the D-2 check.

### PC-B6 Simple EPO
- **Source:** PBL 2021. Roster extension (ADR-0024 §7). UEPO, SEPO and DEPO are excluded (X-20).
- **Definition:** EPO^s(w) = Σ_w⁻¹s/γ, with Σ_w = (1 − w)Σ̃ + wV (EQ-EPO-1/2). For our long-only use (V1): maximise x′m_w − ½x′Σ_w x under Policy Statement constraints. The unconstrained optimum is eq. (18); the KKT conditions are verified.
- **Inputs:**
  - s = the CMA excess-return vector. EPO is signal-agnostic (PBL p. 136), and signal combinations are S4.9's question;
  - Σ̃ = the authoritative risk model.
- **Parameters (recommended, S47-D2):**
  - θ = 0: the authoritative Σ is the input, and θ and w compound anyway;
  - w: system-estimated by PBL's past-only rule (expanding window, maximum trailing Sharpe on a pre-registered grid, at least 15 years of history), pre-registered at S7;
  - γ: scale only (S47-D6).
- **Invariants:**
  - w = 0 → MVO on Σ̃;
  - w = 1 → V⁻¹s/γ;
  - the Sharpe ratio is independent of γ;
  - θ and w compound as (1 − θ)(1 − w).
- **Caution:**
  - PBL's evidence is long–short futures and industry portfolios.
  - Our M-2 test found that EPO with w = 0.75 over-corrects under long-only caps (`S4_RISK_MODEL_CHOICE.md`). The past-only rule may well pick w ≈ 0 in our setting, and that is a legitimate outcome.
- **Verification:** `s47_epo_pbl.py`.
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); w protocol pending S47-D2.

### PC-B7 Anchored EPO
- **Source:** PBL eqs. (21)–(22).
- **Definition:** EPO^a(w), with γ set so that the signal component's risk equals the anchor's (EQ-EPO-3).
- **Inputs:** as B6, plus the anchor a (S47-D3 → S4.10).
- **Parameters:** w as B6; the anchor per S4.10.
- **Invariants:**
  - w = 1 → the anchor;
  - w = 0 → MVO scaled to the anchor's risk.
- **Verification:** `s47_epo_pbl.py`.
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); anchor pending S4.10.

---

## 5. Owner decisions (stage 6)

### S47-D1 — Black–Litterman convention
- **Options:**
  - (a) BL 1992: optimise with Σ; Ω diagonal.
  - (b) He & Litterman: Σ + M̄⁻¹ in the weight step; Ω = τ·diag(PΣP′).
- **Further elements:**
  - Ω rule: Idzorek's confidence closed form (IDZ-1) vs He–Litterman's proportional rule;
  - views: absolute (P = I) from the CMAs vs relative views.
- **Recommendation:**
  - (a) BL 1992;
  - absolute views P = I with Q = the CMAs;
  - Ω from each CMA's confidence via IDZ-1;
  - τ fixed.
- **Why:**
  - BL 1992 governs.
  - ANG's AC agents already output a confidence with each CMA (ANG p. 6), which IDZ-1 maps directly to Ω.
  - With Ω ∝ τ, τ cancels from the posterior mean (verified), so its value does not matter under (a).
  - Relative views have no source in our pipeline yet (S9).

### S47-D2 — EPO shrinkage w
- **Options:**
  - (a) system-estimated by PBL's past-only rule (expanding window; maximum trailing Sharpe on a pre-registered grid, e.g. {0, 0.1, 0.25, 0.5, 0.75, 0.9, 1}; at least 15 years of history);
  - (b) a fixed w;
  - (c) sensitivity-only.
- **Recommendation:** (a), pre-registered at S7, with θ = 0.
- **Why:**
  - It is PBL's own procedure and is past-only, consistent with P12 and ADR-0027 D4.
  - A fixed w has no transferable value: PBL's best in-sample w varies by sample (Table 2), and our long-only test argues against a large w.

### S47-D3 — Anchor for PC-B7
- **Recommendation:** defer to S4.10 (anchor and benchmark architecture), as planned.
- **Candidates:** 1/N (A1; PBL Equity 6), 1/σ (A3; PBL Equity 7), market cap (A2), `POL.benchmark`.

### S47-D4 — Robust mean–variance
- **Options:**
  - (a) G&I robust maximum Sharpe with factor-model uncertainty sets, calibrated by §5 at ω = 0.95;
  - (b) G&I robust minimum variance with a target return α;
  - (c) robust MV with an ellipsoidal set for expected returns only.
- **Recommendation:** (a).
- **Why:**
  - It parallels B1 and needs no target parameter.
  - It keeps B3 distinct from EPO; option (c) is EPO (PBL Prop. 2), so it would duplicate B7.
- **Dependency:** B3 needs a factor model and its regression statistics. Either the authoritative risk model for the problem is a factor model that exposes them (S10), or the factors are declared in B3's contract. Otherwise B3 is ineligible for that problem.

### S47-D5 — Resampled frontier
- **IP check (D-2):** before any implementation.
  - The book says RE optimisation is patented with an exclusive licensee, and the forecast-confidence level is patent pending.
  - Lead to check (UNVERIFIED): a US patent filed around 1998 would normally have expired by about 2018–2019.
- **Recommendation for the specification:**
  - T = the estimation-sample length;
  - K ≥ 1,000;
  - rank association;
  - seed recorded;
  - proposal = the maximum-Sharpe RE portfolio on the original inputs.

### S47-D6 — Cash/risky split (carried from S46-D1)
- **Options:**
  - (a) one engine-level rule: each method proposes its risky portfolio, and one transparent rule sets the cash/risky split from the Policy Statement risk target, the leverage permission and the borrowing rate;
  - (b) each method sets its own split (through γ, δ or its own definition).
- **Recommendation:** (a).
- **Why:**
  - Tobin's separation (verified at S4.6).
  - Candidates are compared at equal risk.
  - The scale parameters γ and δ are calibration-dependent (RQ-02), so per-method cash shares would be artefacts.
  - ANG's own final portfolio missed its volatility band.
- **Consequences to accept with it:**
  1. Volatility targeting (PC-A5, S45-D1) is itself a split rule. Under (a) it either duplicates the engine rule (static target) or is a time-varying variant of it. Its distinctness is tested at admission (ADR-0025), and portfolio-level timing stays at S13c/T4.
  2. It is an adaptation of ANG, where cash is one of the asset classes. If accepted, it is recorded as an ANG adaptation (B-46) and in the S4.20 contracts.
  3. With borrowing permitted at a higher rate, the levered risky mix should switch to the borrowing tangency (S4.6 discussion).

---

## 6. Verification (stage 7)

| Script | Reproduces / proves | Result |
|---|---|---|
| `s47_max_sharpe.py` | Constrained maximum Sharpe via homogenisation = direct maximisation (25 problems); unconstrained = closed form; infeasibility | PASS |
| `s47_epo_pbl.py` | PBL eqs. (5)–(22), Props. 1–3 (BL, MVO, reverse MVO, Tikhonov, Lavrentiev), Prop. 2 in both regimes (PBL-1), eq. (27) link to inverse volatility, constrained V1 KKT | PASS |
| `s47_black_litterman.py` | BL 1992 item 6 reverse optimisation; limits; the p. 35 full-confidence formula; BL-2; τ cancellation | PASS |
| `s47_robust_mv.py` | G&I eq. (15), Lemma 1, the F = κG closed form, robust minimum variance and maximum Sharpe, regression-set coverage | PASS |
| `s47_resampled_frontier.py` | Michaud Tables 5.1 and 6.1 (MV and RE), unbounded Sharpe, fn. 7, REF below MV, T limits | PASS (specification check, D-2) |

---

## 7. Handed forward

| To | Item |
|---|---|
| S4.8 / S4.9 | EPO with TSMOM/XSMOM signals (EQ-EPO-5); signal units |
| S4.10 | B7 anchor (S47-D3); BL's market anchor |
| S4.11 | EQ-MVO-4a and CdST 2006 for GMV; EPO's fully shrunk portfolio = inverse volatility (A3) |
| S4.13 | B3 needs a factor model with regression statistics; B4 re-estimates μ and Σ inside the method (a method-internal resampling, not a new risk model) |
| S4.15 / S9 | δ; CMA confidence → Ω (IDZ-1); BL equilibrium as CMA-3 kept distinct from PC-B2 |
| S4.16 | κ(Σ) and problem-portfolio diagnostics (EQ-MVO-5) |
| S4.20 | Failure codes; the split rule (S47-D6); the D-2 gate for B4 |
| S7 | The EPO w protocol (S47-D2); REF Monte Carlo error at the chosen K |
| S10 | Factor-model availability for B3 |

---

## 8. Ladder status after S4.7

| Method | Status |
|---|---|
| PC-B1 | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level) |
| PC-B2 | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); convention pending S47-D1 |
| PC-B3 | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); specification pending S47-D4 |
| PC-B4 | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (specification check); implementation blocked by D-2 |
| PC-B6 | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); w protocol pending S47-D2 |
| PC-B7 | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); anchor pending S4.10 |
