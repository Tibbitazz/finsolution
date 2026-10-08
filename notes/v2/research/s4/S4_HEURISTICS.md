# S4.5 Heuristic portfolios — PC-A1 … PC-A5: method records

**Document status:** REVIEWED (2026-10-08). Owner decisions S45-D1 … S45-D4 accepted as recommended (§4). · **Basis:**
- S4_PLAN §G (step S4.5) and §F (EQ-H-1 … EQ-H-4);
- `S4_METHODS_OUTLINE.md` §1 (nine-stage workflow, method record template) and §2 (S4.5 plan);
- ADR-0024 §3–§5 (parameter authority, allocation domains, dual contract);
- ADR-0027 D3 (one authoritative risk model per problem).

**Related files:**
- Equations: `S4_EQUATION_REGISTER.md` (EQ-H-1 … EQ-H-4, EQ-H-T).
- Verification: `verification/s45_equal_weight_dgu.py`, `s45_market_cap.py`, `s45_volatility_timing_ko.py`, `s45_volatility_managed_mm.py` (all print PASS; synthetic data only).
- Issues: `ANG_ISSUES_REGISTER.md` (ANG-14 annotated; ANG-43 … ANG-46; MM-1, MM-2).

**Scope:** the mathematics of the five heuristic methods, verified against their sources. **Nothing here selects or ranks methods** (ADR-0025 admission and S7 evaluation come later).

---

## 0. Summary

**Findings:**
1. **Equal weight (A1).** DGU's 1/N is defined over the N *risky* assets (p. 1922). Their analytic critical-window result reproduces exactly in our code (Proposition 1; e.g. 270 / 534 / 1061 months vs the paper's 270 / 530 / 1060).
2. **The cited claim is weaker than ANG's wording.** DGU find that no optimiser is "consistently better than the 1/N rule" (abstract), which is not dominance. Kirby & Ostdiek, ANG's own source for A3/A4, attribute DGU's result "largely" to research design (ANG-45).
3. **Market cap (A2).** Sharpe (1964) contains no capitalisation-weighting rule and never mentions a market portfolio (ANG-43). The link runs through equilibrium. We verified the identity that makes cap weights the mean–variance portfolio when expected returns are equilibrium returns (EQ-H-2a, the same identity as Black–Litterman's Π).
4. **A2 data cannot double-count.** ANG's universe overlaps (US Value / US Growth vs US Large / Small Cap), so summing their capitalisations double-counts US equity (ANG-46).
5. **Inverse volatility and inverse variance (A3/A4)** are Kirby & Ostdiek's VT(η) at η = ½ and η = 1 (ANG-13, resolved at S4.4).
   - All stated limits and the paper's worked example reproduce.
   - A4 is minimum variance with correlations set to zero.
   - A3 equals equal-risk-contribution only when all correlations are equal.
6. **Cash cannot sit inside the A1–A4 universe** (ANG-44). With a 0.5%-volatility cash-like asset, A3 puts 80% and A4 98.5% of the portfolio in cash (verified). A2 is undefined for cash, and A1 would hold 1/N in cash.
7. **Volatility targeting (A5).** Moreira & Muir's method is inverse-*variance* scaling, which is not volatility targeting. Only 1/σ scaling keeps ex-ante risk constant (verified: risk ratio between high- and low-volatility periods 1.00 vs 0.43).
   - Their c is set ex post over the full sample.
   - The baseline uses leverage up to 6.4× (Table V).
   - ANG gives no base portfolio, target, cap or cash rule (ANG-14).
8. **Two inconsistencies inside Moreira & Muir:**
   - **MM-1:** eq. (2) as printed computes the variance from the month being scaled, which is look-ahead. The text says "previous month"; we implement the text.
   - **MM-2:** two α values are swapped between Tables IV and V.

**Decisions for the owner (§4):**
- S45-D1: A5 specification.
- S45-D2: fixed exponents for A3/A4.
- S45-D3: capitalisation data requirements for A2.
- S45-D4: cash and universe rule for heuristics.

*[2026-10-08]* All four accepted by the owner as recommended (§4).

---

## 1. Sources read (stage 1)

| Method | Governing source | Version in hand | Read | Notes |
|---|---|---|---|---|
| PC-A1 | DeMiguel, Garlappi & Uppal (2009), *RFS* 22(5):1915–1953 | Published (OUP), 39 pp., md5 `1e7d229fda18` | Full. Key places: §1 (pp. 1921–1922), eq. (15) p. 1929, §4 Proposition 1 and Figure 1 (pp. 1936–1941) | Printed page = PDF page + 1914 |
| PC-A2 | Sharpe (1964), *JF* 19(3):425–442 | Published (Wiley), 18 pp., md5 `75ba440f7d6d` | Full | No weighting rule (ANG-43) |
| PC-A3, PC-A4 | Kirby & Ostdiek (2012), *JFQA* 47(2):437–467 | Working version 9 May 2010, 43 pp., md5 `8da209076a0e`; **the JFQA version governs** (D-3; differences unchecked) | §2.1 (eqs. 5–6, p. 6), §2.4 (eqs. 12–15, pp. 13–15), §3.1 (p. 16), §5.1 (p. 23) | Printed page = PDF page − 1 |
| PC-A5 | Moreira & Muir (2017), *JF* 72(4):1611–1644 | Published (Wiley), 34 pp., md5 `4e9dbe517e91` | §I.B–E (pp. 1616–1621), Tables IV–V (pp. 1625–1626) | Internet Appendix (alternative variance forecasts) not in hand; not needed for the specification |

---

## 2. ANG versus the sources (stage 3)

| ID | ANG says | Source says | Consequence | Status |
|---|---|---|---|---|
| ANG-13 | Exhibit 3 (p. 11): Kirby & Ostdiek for both inverse volatility and inverse variance | VT(η) family; η = ½ and η = 1 are members; KO test η ∈ {1, 2, 4} | A3 = VT(½), A4 = VT(1) | Resolved at S4.4; confirmed |
| ANG-14 | "Volatility targeting" (Exhibit 3), citing Moreira & Muir | Inverse-variance scaling of one excess return; c ex post; leverage up to 6.4× | Specification gap: base, target, exponent, cap, cash | **Sharpened** → S45-D1 |
| ANG-43 | Market-cap weight cites Sharpe (1964) | No capitalisation rule; p. 435: the theory "does not imply that all investors will hold the same combination" (fn. 19) | A2 rests on the equilibrium identity EQ-H-2a, not on a rule in the cited paper | New (L) |
| ANG-44 | Universe includes Cash as one of 18 classes (p. 15); heuristics' treatment of cash not stated | DGU and KO define weights over risky assets, using excess returns | A1–A4 must exclude cash, or A3/A4 degenerate | New (H) → S45-D4 |
| ANG-45 | Heuristics "dominate when expected returns are poorly measured (DeMiguel, Garlappi, and Uppal 2009)" (p. 9) | DGU: none of 14 models "is consistently better than the 1/N rule". KO: DGU's result is "largely due to their research design" | Framing only; agent-readable summaries must not overstate | New (L) |
| ANG-46 | Universe of 18 classes with US Value and US Growth alongside US Large and US Small Cap (p. 15) | — (universe design) | A2 double-counts capitalisation; A1 and A3/A4 overweight US equity relative to a partition | New (M) → S5, S45-D3 |
| MM-1 | — | eq. (2) as printed sums days of the scaled month; the text says previous month | Implement the strictly-past reading | Source issue (M) |
| MM-2 | — | Table IV vs Table V: α swapped between the 1/RV and expected-variance rows | No effect on our specification | Source issue (L) |

---

## 3. Method records (stages 2, 4, 5, 7)

### PC-A1 Equal weight (1/N)

- **Identity:** PC-A1 · Equal weight · family A heuristic · type `M.PC` · roster v0.
- **Sources:**
  - Governing: DGU 2009 — §1.1, p. 1922; eq. (1), p. 1921; eq. (15), p. 1929; Proposition 1, p. 1938.
  - Supporting: KO eq. (14) at η = 0.
- **Definition:** hold 1/N in each risky asset and rebalance back to 1/N at each rebalancing date. EQ-H-1.
- **Inputs and risk objects:** the universe list only.
  - Deliberately not used: μ, Σ, and any return data.
  - No risk object.
- **Parameters:** none. N comes from the universe (S5).
- **Constraints:** none native. Policy Statement bounds are applied by post-processing (S4.20). A bound-adjusted output is labelled as the constrained variant (I-2).
- **Allocation domains:** asset class, fund/ETF, security, sleeve. The result depends on how the universe is partitioned (ANG-46).
- **Output:** N weights. Failure: empty universe → `NO_UNIVERSE` (provisional code; S4.20 types it).
- **ANG vs source:** ANG-44 (cash in N), ANG-45 (framing), ANG-46 (overlap).
- **Specification choices:** S45-D4.
- **Invariants and limiting cases:**
  - sums to 1; strictly positive; permutation-equivariant; independent of the data;
  - VT(0) = 1/N;
  - mean–variance optimal iff μ ∝ Σ1 (EQ-H-1a).
- **Verification:** `s45_equal_weight_dgu.py` — PASS.
  - invariants and the μ ∝ Σ1 condition;
  - all 15 critical windows stated in DGU reproduced;
  - Monte Carlo confirmation of the expected-utility terms (EQ-H-1b).
- **Agent-readable summary:**
  - *Objective:* diversify without estimating anything.
  - *Intuition:* estimation error in expected returns (and covariances) can cost more than optimisation gains. In DGU's US-equity calibration (S* = 0.15, S_ew = 0.12 monthly), sample mean–variance needs about 3,200 months with 25 assets to beat 1/N on average.
  - *Assumptions:* none about returns. Every universe element is treated as equally important.
  - *Sensitivities:* universe granularity and overlap; rebalancing frequency (drift creates turnover).
  - *Failure modes:* overlapping classes; a near-riskless asset counted as one of N.
  - *Valid comparisons:* the estimation-error benchmark for any optimiser on the same universe.
  - *Invalid comparisons:* across different universes; reading DGU as "1/N dominates".
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level).

### PC-A2 Market-cap weight

- **Identity:** PC-A2 · Market-cap weight · family A heuristic · `M.PC` · roster v0.
- **Sources:**
  - Cited by ANG: Sharpe 1964, read in full. It provides the capital market line and the expected-return–B_ig relation (fns. 22, 25, 26), but no weighting rule (ANG-43).
  - Supporting: He & Litterman reproduction at S4.4 (Π = δΣw_mkt).
- **Definition:** w_i = m_i / Σ_j m_j (EQ-H-2). Between issuance events no trading is needed: the drifted weights are the next cap weights.
- **Inputs and risk objects:** capitalisations m_i, a data input under the S6 contract.
  - Deliberately not used: μ and Σ.
  - No risk object.
- **Parameters:**
  - capitalisation source and proxy per asset class: user-authorised data-contract choice (S45-D3);
  - capitalisation values: system data;
  - update frequency: S6;
  - nothing agent-selectable.
- **Constraints:** none native; post-processing as for A1.
- **Allocation domains:**
  - security: the natural domain;
  - asset class: valid only with capitalisation proxies that partition the universe;
  - fund/ETF: fund AUM is not the asset class's capitalisation, so invalid unless each fund is mapped to its class's capitalisation.
- **Output:** N weights. Failures (provisional codes):
  - `MISSING_CAP` (never filled, I-6);
  - `UNIVERSE_NOT_PARTITION` (ANG-46);
  - `CAP_UNDEFINED` for classes without a defined capitalisation (cash; possibly gold and commodities, S45-D3).
- **ANG vs source:** ANG-43, ANG-46, ANG-17 (resolved by heterogeneous contracts).
- **Specification choices:** S45-D3, S45-D4.
- **Invariants and limiting cases:**
  - sums to 1; positive; invariant to the currency unit;
  - zero turnover between issuance events;
  - tangency = w_m iff μ = λΣw_m; E(R_i) − P = B_im[E(R_m) − P] (EQ-H-2a).
- **Verification:** `s45_market_cap.py` — PASS.
- **Agent-readable summary:**
  - *Objective:* hold the market in proportion to its value.
  - *Intuition:* under homogeneous expectations and market clearing, the market portfolio is the efficient risky portfolio (equilibrium logic). It is also the portfolio that needs no trading.
  - *Assumptions:* equilibrium; measurable, non-overlapping capitalisations.
  - *Sensitivities:* proxy definitions; which classes are included.
  - *Failure modes:* overlapping or missing classes; classes without a capitalisation.
  - *Valid comparisons:* the equilibrium reference for Black–Litterman (PC-B2) and a no-view anchor (S4.10).
  - *Invalid comparisons:* treating it as "optimal" when the universe is only a subset of the market.
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level).

### PC-A3 Inverse volatility

- **Identity:** PC-A3 · Inverse volatility · family A heuristic · `M.PC` · roster v0.
- **Sources:**
  - Governing: Kirby & Ostdiek (JFQA 2012 governs; working version read): eq. (14), p. 14; limits, pp. 14–15.
  - η = ½ belongs to the family but is not tested by KO.
- **Definition:** VT(½): w_i = σ_i^{−1} / Σ_j σ_j^{−1} (EQ-H-3). Each asset's stand-alone risk w_iσ_i is equal.
- **Inputs and risk objects:** σ_i, the diagonal of the authoritative risk model for the method's problem (ADR-0027 D3).
  - Deliberately not used: μ and correlations.
- **Parameters:**
  - η = ½: fixed (S45-D2);
  - σ_i: system-estimated;
  - other η values: sensitivity-only.
- **Constraints:** long-only and fully invested by construction; Policy Statement bounds by post-processing.
- **Allocation domains:** asset class, fund/ETF, security, sleeve, provided all σ_i share one horizon and currency basis.
- **Output:** N weights. Failures (provisional codes):
  - `INVALID_RISK_INPUT` (σ_i missing or ≤ 0);
  - `CASH_IN_UNIVERSE` (S45-D4).
- **ANG vs source:** ANG-13 (resolved), ANG-44.
- **Invariants and limiting cases:**
  - sums to 1; positive; permutation-equivariant; invariant to the variance unit;
  - monotone (lower σ → higher weight);
  - equals ERC (PC-C2) when all correlations are equal, and not otherwise.
- **Verification:** `s45_volatility_timing_ko.py` — PASS.
- **Agent-readable summary:**
  - *Objective:* equalise each asset's stand-alone risk.
  - *Intuition:* a correlation-free approximation to risk parity.
  - *Assumptions:* correlations are similar enough to ignore.
  - *Sensitivities:* the volatility estimator and window. The elasticity of a weight ratio to the volatility ratio is −1 for A3 (−2η in general).
  - *Failure modes:* near-riskless assets dominate; very unequal correlations make it differ from ERC.
  - *Valid comparisons:* ERC under similar correlations; A4 (same family).
  - *Invalid comparisons:* calling it risk parity when correlations differ.
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level).

### PC-A4 Inverse variance

- **Identity:** PC-A4 · Inverse variance · family A heuristic · `M.PC` · roster v0.
- **Sources:** Kirby & Ostdiek eq. (14) at η = 1 and eq. (12), p. 13. KO's baseline choice: "a natural choice … implied by mean-variance optimization with a diagonal covariance matrix" (p. 23).
- **Definition:** VT(1): w_i = σ_i^{−2} / Σ_j σ_j^{−2} (EQ-H-3). This equals the minimum-variance portfolio with the off-diagonals of Σ set to zero (EQ-H-3a).
- **Inputs, constraints, domains, failures:** as PC-A3.
- **Parameters:**
  - η = 1: fixed (S45-D2);
  - σ_i: system-estimated;
  - KO's η ∈ {2, 4}: sensitivity-only.
- **ANG vs source:** ANG-13 (resolved), ANG-44.
- **Invariants and limiting cases:**
  - as A3, with weight ratio (σ_j/σ_i)²;
  - equals the numerical solution of min w′Dw s.t. 1′w = 1 for diagonal D;
  - KO's eq. (13) worked example reproduced.
- **Verification:** `s45_volatility_timing_ko.py` — PASS.
- **Agent-readable summary:**
  - *Objective:* minimum variance without correlations.
  - *Intuition:* zeroing the correlations is "an aggressive form of shrinkage" (KO p. 14). It removes N(N−1)/2 estimated parameters and rules out short positions.
  - *Assumptions:* correlations carry less reliable information than variances.
  - *Sensitivities:* twice A3's elasticity to volatility estimates, so more concentrated.
  - *Failure modes:* as A3, stronger.
  - *Valid comparisons:* GMV (PC-C1, S4.11) on the same Σ, as the cost of ignoring correlations.
  - *Invalid comparisons:* treating it as the true GMV.
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level).

### PC-A5 Volatility targeting

- **Identity:** PC-A5 · Volatility targeting (MM's term: "volatility-managed") · family A heuristic · `M.PC` · roster v0.
- **Sources:**
  - Governing: Moreira & Muir 2017 — eqs. (1)–(2), p. 1616; fn. 6; eq. (3), p. 1617; p. 1620; eqs. (4)–(5), p. 1621; Tables IV–V, pp. 1625–1626.
  - Issues: MM-1, MM-2.
- **Definition:**
  - **V0 (the source, verification oracle):** f^σ_{t+1} = (c/RV²_t) f_{t+1}, with RV² from the previous month's 22 daily returns and c set ex post so that sd(f^σ) = sd(f).
  - **V1 (engine form, decided by S45-D1):** s_t = min(σ*/σ̂_t(b), L); w_t = s_t·b; w_{0,t} = 1 − s_t.
  - Both in EQ-H-4.
- **Inputs and risk objects:**
  - base portfolio b: the A2 output (A1 as the declared fallback; S45-D1);
  - σ̂_t(b): the short-horizon risk problem (ADR-0027 D3);
  - σ*: the long-run volatility of b, from the long-horizon risk problem (S45-D1);
  - L: from the effective `POL.leverage`;
  - deliberately not used: μ.
- **Parameters (V1; S45-D1 decided 2026-10-08):**
  - σ*: system-estimated, the long-run volatility of b (long-horizon risk problem);
  - L: user-authorised, min(1, effective `POL.leverage` maximum);
  - b: fixed, A2 (A1 as the declared fallback while S45-D3 is open);
  - estimator: system-estimated (S10);
  - exponent: fixed by decision;
  - rebalancing frequency: S13;
  - nothing agent-selectable.
- **Constraints:** with L ≤ 1, long-only plus cash. Asset bounds apply to s_t·b. Lower bounds can bind when s_t < 1, so post-processing is needed (S4.20).
- **Allocation domains:** asset class and sleeve (its natural use is as a portfolio-level exposure rule); fund/ETF and security valid if b is defined there.
- **Output:** N risky weights plus cash. Failures (provisional codes):
  - `BASE_FAILED` (propagates b's failure record, I-2);
  - `INVALID_RISK_INPUT`;
  - `TARGET_MISSING`.
- **ANG vs source:** ANG-14 (sharpened), MM-1, MM-2.
- *[2026-10-08, S47-D6]* **Exposure rule:** PC-A5 keeps its own exposure rule as an exception to the engine-level risk target; its distinctness from that rule is tested at admission (ADR-0025); portfolio-level timing stays at S13c.
- **Relation to other roster items:**
  - A1–A4 are cross-sectional rules; A5 is a time-series exposure rule.
  - It overlaps the tactical volatility overlay T4 (S13c). The S4.20 contract must keep A5 as a candidate portfolio and leave overlays on the final portfolio to S13c, so that the same timing is not applied twice.
- **Invariants and limiting cases:**
  - s_t ∈ [0, L]; cash ≥ 0 when L ≤ 1;
  - F_t-measurable (no look-ahead);
  - σ̂_t = σ* → A5 = b;
  - s_t is proportional to σ* until the cap binds.
  - V0: c leaves the Sharpe ratio unchanged; appraisal identity EQ-H-4a.
- **Verification:** `s45_volatility_managed_mm.py` — PASS.
- **Agent-readable summary:**
  - *Objective:* keep risk roughly constant over time by scaling exposure against recent volatility.
  - *Intuition:* volatility is persistent and, in MM's evidence, does not predict returns. Cutting exposure when volatility is high therefore improves risk-adjusted returns (MM: market α 4.86% p.a., appraisal ratio 0.34; the no-leverage variant keeps a Sharpe ratio of 0.52).
  - *Assumptions:* volatility persistence; no strong positive relation between volatility and subsequent returns.
  - *Sensitivities:* estimator horizon, cap, target, rebalancing frequency. MM report average absolute monthly weight changes of 0.16–0.73.
  - *Failure modes:* if high volatility is followed by high compensation, scaling reduces exposure exactly when it is rewarded (the premise fails); estimation noise in σ̂_t.
  - *Valid comparisons:* against its own base b (spanning regression, EQ-H-4a).
  - *Invalid comparisons:* α across different bases; V0's ex-post-c results treated as real-time performance.
- **Ladder:** MATHEMATICS EXTRACTED · COMPUTATION VERIFIED for V0 and V1. V1 parameters decided (S45-D1, 2026-10-08).

---

## 4. Owner decisions (stage 6)

### S45-D1 — PC-A5 specification

*[2026-10-08]* **Owner decision: accepted as recommended.** PC-A5 V1 = 1/σ scaling of the market-cap portfolio (A2; A1 as the declared fallback while S45-D3's data source is open) to its own long-run volatility, capped at min(1, effective `POL.leverage` maximum), cash residual, σ̂_t from the short-horizon risk problem.

| Sub-choice | Options | Recommendation | Why (verified) |
|---|---|---|---|
| (a) Exponent | 1/σ (volatility targeting) · 1/σ² (MM baseline) | **1/σ** | Only 1/σ keeps ex-ante risk constant (risk ratio 1.00 vs 0.43). MM Table IV/V: 1/RV halves turnover (0.38 vs 0.73), raises the break-even cost (84 vs 56 bp), matches the Sharpe ratio (0.53 vs 0.52) and halves the leverage tail (P99 3.36 vs 6.39). 1/σ² is Sharpe-optimal only with known variance and a constant mean (our oracle test); MM's own data show no advantage with estimated variance |
| (b) Target σ* | Long-run volatility of b (system-estimated; MM's normalisation done ex ante) · Policy Statement risk control (user-authorised) | **Long-run volatility of b** | Keeps A5 a pure timing of b's own risk, as in MM (c equalises unconditional risk). The Policy Statement band applies to the final portfolio and the CRO checks, not inside one candidate |
| (c) Cap L | Effective `POL.leverage` maximum · fixed 1 | **min(1, effective `POL.leverage` maximum)** | Cash stays ≥ 0. MM's no-leverage variant keeps Sharpe 0.52 (Table V). Leverage needs explicit Policy Statement and account permission (FX-06) |
| (d) Base b | A2 market cap · A1 1/N · `POL.benchmark` · MVE b′F (MM eq. 5) | **A2, with A1 as the declared fallback while S45-D3 is open** | MM's motivating case is the market portfolio (p. 1616). A2 keeps A5 μ-free and distinct from A1/A3/A4. MVE needs μ, which is not a heuristic. The benchmark is a reasonable alternative if the owner prefers A5 to time the policy portfolio |
| (e) Estimator and horizon | From the short-horizon risk problem (ADR-0027 D3), chosen at S10 by the pre-registered rule; MM's previous-month RV from daily returns is the V0 reference | **As stated** | Consistent with D3; avoids a method-private estimator |

### S45-D2 — A3/A4 exponents

*[2026-10-08]* **Owner decision: accepted as recommended.** η fixed: A3 = ½, A4 = 1; other values sensitivity-only.

- **Options:**
  - η fixed (A3 = ½, A4 = 1), other values sensitivity-only;
  - η as a parameter.
- **Recommendation:** fixed.
- **Why:**
  - KO state that the best η "will depend on the level of estimation risk, the level of transactions costs, and the number of assets" (p. 15), which makes tuning η an evaluation question (S7).
  - A free η would merge A3 and A4 into one tunable method and invite in-sample tuning, which ADR-0024 §2 prohibits.

### S45-D3 — A2 capitalisation data requirements (the source itself is chosen at S6)

*[2026-10-08]* **Owner decision: accepted as recommended.** Requirements 1–5 approved; the data source is chosen at S6.

- **Requirements proposed now:**
  1. Proxies partition the universe: no overlapping classes (ANG-46).
  2. One currency and one date.
  3. Float-adjusted market value where defined; amount outstanding at market value for bonds.
  4. A declared rule for classes without a capitalisation (cash; gold and commodities need a decision). Default: excluded from A2, with reason `CAP_UNDEFINED`.
  5. Update frequency stated.
- **Candidate sources:** index-provider market values (licensing to check at S6); published multi-asset market-portfolio estimates, e.g. Doeswijk, Lam & Swinkels (2014, FAJ) — not yet reviewed.
- **Recommendation:** approve the requirements; choose the source at S6.

### S45-D4 — Heuristic universe and cash

*[2026-10-08]* **Owner decision: accepted as recommended.** Option (a): A1–A4 on risky assets only.

- **Options:**
  - (a) A1–A4 operate on risky assets only. Cash enters only through A5's residual or a Policy Statement cash allocation applied in post-processing.
  - (b) Cash as one of the N.
- **Recommendation:** (a).
- **Why:**
  - DGU and KO define weights over risky assets with excess returns (DGU p. 1921; KO eq. 14).
  - Under (b), A3/A4 collapse into cash (80% / 98.5%, verified), A2 is undefined, and A1's cash share becomes an accident of N.
  - S4.6 decides the general treatment of cash and the risk-free rate; (a) is consistent with either outcome there.

---

## 5. Verification (stage 7)

| Script | Reproduces / proves | Result |
|---|---|---|
| `s45_equal_weight_dgu.py` | 1/N invariants; eq. (1); μ ∝ Σ1 optimality; Proposition 1: all 15 stated critical windows; Monte Carlo of the case 1–3 expected-utility terms (400,000 draws) | PASS |
| `s45_market_cap.py` | Cap-weight invariants; zero turnover without issuance, exact turnover with issuance; reverse optimisation; Sharpe's linear relation with B_im | PASS |
| `s45_volatility_timing_ko.py` | VT(η) limits (η = 0, ∞) and invariants; eq. (12) by numerical QP; eq. (13) example; A3 = ERC iff correlations equal; KO turnover eq. (6) = DGU eq. (15) plus the cash leg; the cash-degeneracy demonstration | PASS |
| `s45_volatility_managed_mm.py` | eq. (1) with ex-post c; fn. 6; no look-ahead (and the literal eq. (2) fails it); appraisal identity; Table IV variants and leverage tails; 1/σ vs 1/σ² risk behaviour and Sharpe ordering with oracle volatility; V1 bounds and realised volatility at target | PASS |

**Not reproduced:** MM's and KO's empirical tables (they need their data) and DGU's empirical Sections 3 and 5. The specifications here do not depend on those numbers.

---

## 6. Handed forward

| To | Item |
|---|---|
| S4.6 | General cash and risk-free treatment (S45-D4 is consistent with either outcome); EQ-H-1b as the estimation-error diagnostic for sample MV |
| S4.10 | A1 and A2 as anchor and benchmark candidates |
| S4.11 | EQ-H-3a (A4 = diagonal GMV); A3 = ERC under equal correlations |
| S4.13 | Risk dependencies: A1/A2 none; A3/A4 the variances only; A5 short-horizon volatility of b plus b's long-run volatility (S45-D1(b) accepted) |
| S4.16 | EQ-H-1a and EQ-H-4a as in-sample diagnostics (labelled, I-9) |
| S4.20 | Post-processing rule for Policy Statement bounds; provisional failure codes; the A5/T4 boundary |
| S5 | ANG-46: the universe must be a partition for A2 (and should be for A1, A3, A4) |
| S6 | S45-D3 capitalisation data contract |
| S7 | η sensitivity; DGU's critical-window logic for evaluation design |
| S10 | Estimators for the strategic (A3/A4) and short-horizon (A5) risk problems |
| S13c | A5 versus the T4 volatility overlay |

---

## 7. Ladder status after S4.5

| Method | Before | After |
|---|---|---|
| PC-A1 | SOURCE LOCATED (in hand) | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level) |
| PC-A2 | SOURCE LOCATED (in hand) | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); data contract open (S45-D3) |
| PC-A3 | SOURCE LOCATED (in hand) | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level) |
| PC-A4 | SOURCE LOCATED (in hand) | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level) |
| PC-A5 | SOURCE LOCATED (in hand) | MATHEMATICS EXTRACTED · COMPUTATION VERIFIED for V0 and V1; V1 parameters decided (S45-D1) |

NOTATION RECONCILED, CONTRACT DEFINED and FIXTURES DEFINED complete in Section 4 (S4.19–S4.24).
