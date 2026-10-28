# S4 record — Renshaw, Gu, Candar & Ang: multifactor composite (owner-designated reference specification)

**Document status:** DRAFT (S4 record, 2026-10-25; annotated 2026-10-26: risk dependencies cross-referenced to S4.13, §4). The method work belongs to S9c/S9d (signals, scores, aggregation), S9a/S13c (timing), S10 (security risk model) and S11 (construction) → G9/G11. · **Basis:**
- owner decisions REN-D1 … REN-D7, 2026-10-25 (§0);
- ADR-0012 (§2–§5); ADR-0024 §1, §3, §4, §8; ADR-0025 (admission ≠ evaluation); ADR-0026 (agents interpret, never compute);
- `S4_SCORING_SORENSEN.md` (precedent and predecessor); `S4_SIGNAL_PC_COMPATIBILITY.md` (R-1, R-7); `S4_MOMENTUM.md` (S48-D6); RQ-11, RQ-17, RQ-28 … RQ-33, RQ-37.

**Verification:** `verification/s4ren_multifactor_reference.py` (synthetic; P-R1 … P-R8).

## 0. What this record does and does not do

**Owner decisions (2026-10-25):**

| ID | Decision |
|---|---|
| REN-D1 | The paper is the **reference specification** for the multifactor composite: signals, factor scores, the 1/3–1/3–1/6–1/6 score, the construction and the three timing models. **Only the construction is adopted.** FinSol applies it to its own universe (RQ-07 owner instruction) and its own datasets; the paper's results are not replicated |
| REN-D2 | **The Renshaw definitions replace the Sørensen/Storebrand definitions** for value and momentum factor scores, in screening and in construction. Sørensen is kept for three uses: (i) its 0–100 percentile rank as the **display transform** of the Renshaw scores; (ii) the exact Sørensen method as a **reproduction oracle** of the 2026-10-07 instruction; (iii) SIG-1 12–1 stays the **standalone** cross-sectional momentum signal (S48-D1), with its channel declared under R-7c when used beside the composite |
| REN-D3 | **Rule R-1 refined, not removed.** A score enters an optimiser only through a declared mapping accepted at S9d (ADR-0012 §3). In budget-neutral, tracking-error-constrained exposure maximisation the mapping α = λ·z (**EQ-MAP-5**; λ irrelevant) is admissible and is the reference (V0). The volatility-scaled EQ-MAP-3 is the tested variant (V1). Where the level or scale of μ matters, the mapping must fix both (EQ-MAP-1 … 4) |
| REN-D4 | **Factor-momentum timing follows the source** (S48-D6 annotated; RQ-11) |
| REN-D5 | **The three timing models run in the research lane (ADR-0024 §1) in shadow mode:** computed and logged monthly, no effect on production weights until pre-registered S7 criteria are met. A label embargo is mandatory |
| REN-D6 | **Analyst revisions stay missing** (the source's missing-data rule) until S6 finds a licensable, dated source; FMP's rating-change endpoint is to be checked (§9) |
| REN-D7 | **EBIT/EV is registered as a V1 test variant**: a third cyclical-value signal (§2), not part of V0 |

**Not done by this record:**
- no admission (ADR-0025: S4.20 contract, S4.24 fixture, then G9/G11);
- no performance claim: the sources are index-provider backtests, gross of costs, with no live period;
- no roster change: the construction is a composition (signals → score → EQ-MAP-5 → tracking-error-constrained optimisation), as with the Sørensen O-9 options;
- no production timing (REN-D5);
- nothing about the paper's data vendors is required.

## 1. Sources

| Source | Identity | Authority and use |
|---|---|---|
| iSTOXX *Equity Indices Methodology Guide* §118 "iSTOXX Ang Research Enhanced Index Family" | Version of 13 Oct 2026; 833 pp.; md5 `5132886537fc` | **Newest, rule-level.** Governs signal, score, timing and constraint definitions |
| Renshaw, Gu, Candar & Ang, "Real-world diversification in multifactor indices", STOXX whitepaper | August 2026; 15 pp.; md5 `aa7059c760c3` | Condensed; identical results; omits App. C |
| Renshaw, Gu, Candar & Ang, "Diversification all the way down" | July 2026; 40 pp.; md5 `8828567fbd66` (zip `66921059025e`) | **Only source for the market-similarity configuration (App. C)** and the signal-level evidence |
| Eisfeldt, Kim & Papanikolaou, "Intangible Value", NBER WP 28056 (Nov 2021 version) | md5 `5c861121091e`; *CFR* 11(2) 2022 governs | Public convention for capitalising intangibles (§2, O-R5) |

All are SECONDARY (source inventory §23). Stewart (2009), Lev & Sougiannis (1996) and Sloan (1996) are cited by the source; no legitimate open copy was found, so the owner supplies them.

## 2. Signals (V0 = guide; V1 = FinSol's declared conventions)

Every signal is z-scored with parent-universe weights, truncated at ±3, missing values omitted (P-R1). ISS-EVA-type inputs (signals 3–5, 9) are winsorised at the 1st/99th percentiles before z-scoring.

| # | Factor | Signal | V0 definition (guide §118.1.2) | V1 / declared convention | Status |
|---|---|---|---|---|---|
| 1 | Cyclical value | Book to price | Common equity (latest reported within 2 years) / average 30-day total issuer market cap | Filing-date lag; issuer-level market cap (all share classes) | Implementable |
| 2 | Cyclical value | Earnings yield | ¾ (trailing four-quarter net income / 30-day average total issuer market cap) + ¼ (12-month forward estimate / same) | Forward leg missing without point-in-time consensus → trailing only | Implementable (trailing) |
| 2b | Cyclical value | EBIT/EV (V1 only, REN-D7) | — | EBIT / enterprise value (registered DESC-V-EYEV); tested for overlap with enhanced value and quality | Test variant |
| 3 | Enhanced value | Economic-profit yield | EVA (NOPAT − capital charge) / EV; EV net of surplus cash and non-operating assets | NOPAT and capital adjustments and the cost-of-capital method declared (O-R4) | Implementable (approximated) |
| 4 | Enhanced value | Intangible asset ratio | (Reported intangibles + cumulative capitalised R&D and advertising, after tax) / Capital (operating + intangible + goodwill + other capital, excluding funding capital) | Perpetual inventory (O-R5); no price variable, an intangible-intensity measure | Implementable (approximated) |
| 5 | Enhanced value | Free-cash-flow yield | (NOPAT − ΔCapital + non-cash adjustments) / EV | EVA-consistent; CFO − capex as variant | Implementable |
| 6 | Momentum | Price momentum | Cumulative return over 260 trading days, last 21 progressively down-weighted | Taper shape declared (O-R1) | Implementable |
| 7 | Momentum | Idiosyncratic momentum | Cumulative specific return (risk model) over 250 days excluding the last 20; non-live days = 0 | FinSol's security factor model (RO-8, S10); FF3 residuals as interim variant | After S10 |
| 8 | Momentum | Analyst revisions | (Upgrades − downgrades) / all analyst sentiments, latest 30-day window (I/B/E/S) | Missing (REN-D6); a rating-change version is a declared variant (§9) | Missing |
| 9 | Momentum | Economic-profit momentum | Annual change in EVA / prior-period sales | From signal 3's EVA series | Implementable (needs history) |
| 10 | Momentum | Low short interest | Mean of standardised on-loan/market cap, on-loan/ADV, on-loan/lendable; sign reversed | Components without data omitted; Norway: public net short positions ≥ 0.5% as the on-loan/market-cap proxy (§9) | Partial |
| 11 | Momentum | Hedge-fund holdings | Mean of standardised % held by hedge funds, holdings value/volume, number of funds/√market cap | SEC 13F data sets (US only, quarterly, 45-day lag) plus a hedge-fund filer classification | US research-grade |
| 12 | Quality | Return on equity | Four-quarter earnings / average of four common-equity values | Negative equity rule | Implementable |
| 13 | Quality | Return on assets | Four-quarter earnings / average of four total-asset values | — | Implementable |
| 14 | Quality | Cash flow to assets | Latest annual operating cash flow / average of beginning and end total assets | — | Implementable |
| 15 | Quality | Sales to EV | Four-quarter sales / EV | A valuation ratio inside quality (interaction declared) | Implementable |
| 16 | Quality | Gross profit to assets | Four-quarter (sales − COGS) / average of four total-asset values | Financials excluded by predicate | Implementable |
| 17 | Quality | Sales to assets | Four-quarter sales / average of four total-asset values | — | Implementable |
| 18 | Quality | Operating accruals to assets | Four-quarter (income − operating cash flow) / average of four total-asset values | Orientation declared: lower accruals score higher (O-R6) | Implementable |

Quality in the guide is "based on Axioma's Profit Quality Factor", a vendor composite of signals 12–18. FinSol builds its own composite of the seven signals by the guide's general rule (equal weights, P-R1).

## 3. Factor scores and the multifactor score

- **Factor score:** the equal-weighted mean of the available signals, z-scored again with parent weights and truncated at ±3 (P-R1). The paper's own rule handles missing signals (8, 10, 11) without changing the specification.
- **Dynamic multi-factor score:** Score_i = Σ_k w_k·F_ik over the four factors (missing factor scores omitted), z-scored and truncated at ±3. The weights w_k come from §5, with base weights 1/3 momentum, 1/3 quality, 1/6 enhanced value and 1/6 cyclical value.
- **Display (REN-D2):** the Renshaw scores are shown as 0–100 percentile ranks (Sørensen S-5 transform). Computation uses the truncated z.
- **Corrections registered as V1 variants (RQ-31):**
  - clip, then z (or iterate to a fixed point), so outliers do not set the scale;
  - a missing-count rule (normalise by √((1 + (k − 1)ρ̄)/k) or require k ≥ 2). Without it a name with one signal has 1.55× the dispersion at ρ = 0.3 (P-R3).

## 4. Construction

**Objective:** maximise the active exposure (w − b)′Score subject to the constraints below (guide §118.1.3). Under REN-D3 this is EQ-MAP-5: active mean–variance with α ∝ Score (P-R4).

| Constraint (guide, Ang01) | FinSol |
|---|---|
| Tracking error ≤ 100 bp (ex ante) | **Adopted as a parameter.** With few holdings 1% is infeasible, so the budget is set per sleeve (S5/S11) |
| Beta 0.98–1.02 | Adopted |
| ICB Level 1 active exposure within ±2% | Adopted with FinSol's sector classification (S6) |
| Stock weight ∈ [max(0, b − 2%), min(b + 2%, 20b)] | Adopted where the number of holdings permits; otherwise replaced by the cardinality rule |
| Minimum active factor exposures: momentum, quality, enhanced value 20%; cyclical value 0% | V0; a no-floor sensitivity at S7 (the floors were chosen with knowledge of the sample) |
| One-way turnover ≤ 5% per quarter; quarterly review | Adopted (method-determined rebalancing, RQ-44) |
| Infeasibility: relax tracking error first, then turnover | Adopted (fail small, P11) |
| Minimum holding 10 bp new / 2 bp existing; issuer ≤ 22.5%; sum of issuers > 4.5% ≤ 47.5%; liquidity S = 20, p = 10th percentile; do-not-trade at zero 60-day volume | **Index-product rules, replaced** by Policy Statement concentration limits and account-size feasibility (06 rule 8) |
| Axioma optimizer and risk model | Replaced: S10 security risk model (RO-2/RO-8, `S4_RISK_DEPENDENCIES.md`); solver is the developer's choice. *[2026-10-26]* In S4.13 terms: RO-2 (Σ) for the tracking error, the beta band and the total-risk constraint (§4 row EQ-MAP-5); RO-8 for signal 7's specific returns (§3 row SIG-1/R); the timing models' statistics are internal (§4); findings F-12 and F-13 |

**FinSol adaptations:**
- **Number of holdings:** about 270 names is not realistic. A capital-dependent cardinality limit K, from per-trade minimum commissions (RQ-07 D1–D3; 06 rule 8), turns the problem into a mixed-integer variant.
- **Total-risk constraint inside the optimisation** (S410-D6; normally non-binding at small tracking error).
- **Placement:** a long-only tilt inside its host equity class (R-7a). Risk is measured by look-through (R-7b), and the total is scaled by EQ-SPLIT-1.
- **Anchor:** the cap-weighted parent universe of the sleeve (S410: market capitalisation for security sleeves).
- **Mixed portfolios:** F-11 (`S4_RISK_DEPENDENCIES.md`).

## 5. Timing models (research lane, shadow mode: REN-D5)

**Market similarity** (guide §118.1.2; July paper §4.1 and App. C):
- **Inputs:** returns of each factor portfolio, the parent index and the industry indices (ICB Level 1).
- **Features:** dispersion of returns, volatility and beta across factor and sector series; mean and s.d. of pairwise correlations; rolling betas and residual variance; 6- and 36-month behaviour. Every feature is z-scored over a rolling 36 months.
- **Target:** the sign of the 3-month forward active return.
- **State space:** five expanding-window principal components.
- **Similarity and fit:** a Gaussian kernel with bandwidth = 25th percentile of historical distances; a local logistic regression per factor, minimum 36 labelled months.
- **Rule:** double a factor whose probability is ≥ 10 points above each other factor; halve one ≥ 10 points below each.

**Factor momentum** (REN-D4): the 18-month information ratio of each factor portfolio against the parent (monthly returns on the review calendar). Double the top factor if it leads each of the others by ≥ 0.15; halve the bottom one if it trails each by ≥ 0.15.

**Factor-of-factors:** EWMA_T = 10%·ActExp_T + 90%·EWMA_{T−1} of the multi-factor portfolio's momentum and cyclical-value exposures. Double momentum after a rise ≥ 0.3%; halve cyclical value after a fall ≥ 0.3%.

**Combination:** each model's weights are renormalised, then averaged 50/25/25. No factor is eliminated. One model moves a weight within [0.4×, 2.0×] of nominal; the effective number of factors stays ≥ 2.58 (P-R6).

**V0 = the source + embargo**: training only on months whose 3-month label has been realised by the forecast date (m + 3 ≤ t; P-R8). A version without the embargo is look-ahead and never admissible.

**V1 candidates** (pre-registered variants, RQ-37):
- PCA re-scored with each date's fit (consistent geometry; first forecast after 108 rather than 143 months);
- fixed ridge in the logistic regression;
- an effective-sample floor (below it, no tilt);
- a base-rate-neutral rule comparing each probability with that factor's own expanding base rate;
- a null-calibrated threshold in place of 10 points;
- factor-of-factors computed on the static-weight portfolio's exposures (removes the feedback loop).

**Shadow mode:**
- **Logged each month:** inputs hash, probabilities, information ratios, EWMAs, the would-be weights and later the realised outcomes. Production uses the static base weights.
- **Exit:** the pre-registered S7 criteria (net of the turnover the tilts consume; power stated).
- **Data needed:** the paper-literal market-similarity model needs about 12 years of daily factor-portfolio history before its first forecast (P-R8: 143 months; 24 Jun 2002 + 143 months = May 2014, the source's June 2014). FinSol's own factor portfolios therefore run prospectively; public long–short factor series (Ken French data library) can serve a research variant.

## 6. Verified properties (`verification/s4ren_multifactor_reference.py`, synthetic)

| # | Property |
|---|---|
| P-R1 | Parent-weighted z has parent-weighted mean 0 and s.d. 1; truncation ±3; missing signals omitted; re-z |
| P-R2 | Active exposure (w − b)′s does not depend on the centring of s |
| P-R3 | Composite dispersion with k available signals ∝ √(1/((1 + (k − 1)ρ)/k)): 1.55× for k = 1 vs 6 at ρ = 0.3 |
| P-R4 | Maximum exposure under a tracking-error budget with full investment = a ∝ Σ⁻¹(s − s̄1) (EQ-MAP-5); invariant to positive scaling and shifts, not to monotone non-linear transforms |
| P-R5 | Alpha eating: with diagonal residual risk, positions ∝ z/ω² (EQ-MAP-5) vs z/ω (EQ-MAP-3); same score at 20% and 40% residual volatility → 4:1 vs 2:1 |
| P-R6 | Rules "against each of the other three"; per-model bounds [0.4×, 2.0×]; effective number 3.6 static, 3.32 when the 50% model doubles momentum, 2.58 at the extreme |
| P-R7 | Factor-momentum and factor-of-factors worked examples; the 50/25/25 ensemble sums to 1 and keeps every factor |
| P-R8 | Embargo enforced; paper-literal first forecast at month 143 (108 with re-scoring); bandwidth = 25th percentile of pairwise distances |

## 7. Simulation findings (synthetic; scratch study 2026-10-25; mechanics, not the source's performance)

**Market-similarity model, paper-literal reading:**

| Setting | Months with a tilt | Out-of-sample AUC | Note |
|---|---|---|---|
| No predictability, Exhibit 5 means | 0.86 | 0.47–0.50 | Cyclical value halved in 54% of months: the rule compares probabilities that embed long-run hit rates |
| No predictability, equal means | 0.74 | 0.46–0.51 | Accuracy below the majority-class rate |
| No predictability, **no embargo** | 0.73 | **0.57–0.61** | Spurious +0.17%/yr (t ≈ 3.2); an AUC ≥ 0.70 for some sleeve in 12% of replications (0% with the embargo) |

- **Kernel localisation is mild:** the effective sample is about 76% of the training rows.
- **Extreme probabilities (beyond 0.05/0.95) appear in about a quarter of forecasts** under no predictability.
- **Own-date PCA scores** share only 66% of the ten nearest months with re-scored history.

**Factor momentum** (18-month IR, 0.15 margin): about 97% of months tilt under no predictability. The IR standard error over 18 months is about 0.82, so the margin barely filters.

## 8. Open specification choices (declared parameters; V0 value first)

| ID | Choice | V0 | Variants |
|---|---|---|---|
| O-R1 | Price-momentum taper over the last 21 days | Linear taper (declared; the guide gives no shape) | Hard skip (12–1) |
| O-R2 | z weighting | Parent (capitalisation) weights | Equal weights |
| O-R3 | Order of z and truncation | z, then truncate (source) | Truncate, then z; iterate (§3) |
| O-R4 | EVA conventions and cost of capital | Declared open convention: NOPAT = EBIT(1 − t) with R&D and advertising adjustments; capital including capitalised intangibles; WACC method fixed in advance | Stewart's conventions once supplied |
| O-R5 | Capitalising intangibles | Perpetual inventory, δ = 0.2, initial stock = flow/(g + δ) with g = 0.1 (Eisfeldt, Kim & Papanikolaou), applied to R&D and advertising, after tax | 100% of SG&A (EKP) where advertising is not reported; industry-specific R&D rates (Lev & Sougiannis, once supplied) |
| O-R6 | Accrual orientation | Lower accruals score higher | — (Sloan, once supplied) |
| O-R7 | Analyst revisions | Missing (REN-D6) | Rating-change version from a licensed dated source |
| O-R8 | Hedge-fund identification for 13F | — | Declared classification method |
| O-R9 | Sector classification | Open classification chosen at S6 | — |
| O-R10 | Universe per sleeve | RQ-07 universe; one parent universe per sleeve (US, Oslo, global) | — |
| O-R11 | Cardinality K and tracking-error budget | From account capital and the Policy Statement | — |
| O-R12 | Timing thresholds | 10 points / 0.15 / 0.3% (source) | Null-calibrated (§5) |

## 9. Data map (S6; per-user licences, CB-19)

| Data | Route found 2026-10-25 | Status |
|---|---|---|
| Prices, constituents, market caps | EODHD / Tiingo (S6 lead) | Supported, point-in-time to be tested |
| Statements (US) | SEC EDGAR XBRL, point-in-time by filing date | Supported |
| Statements (Oslo) | ESEF via filings.xbrl.org (annual only); quarterly items need a vendor | Partial |
| Consensus forward earnings | Vendor-only (S6 F-4) | Not available → signal 2 trailing only |
| Analyst rating changes | FMP `grades` endpoint documents dated events (grading firm, previous and new grade, action); coverage, history depth and licence unverified. No free dated Nordic source found (MiFID II research is a paid service) | To check (REN-D6) |
| Hedge-fund holdings | SEC Form 13F data sets (structured, from 2013) | US research-grade |
| Short positions (Norway) | Finanstilsynet public register of net short positions ≥ 0.5% (daily) | Partial proxy |
| Short interest (US) | FINRA free data covers OTC only; listed stocks via the exchanges | Licence unverified |
| Securities-lending (on-loan, lendable) | Vendor-only | Not available |
| Proxies for timing research | Ken French data library (S6 public stack) | Research only |

## 10. Relationship to other records

- **Sørensen** (`S4_SCORING_SORENSEN.md`): definitions replaced (REN-D2); its V1 (E/P, B/P, winsorising) converges on cyclical value.
- **SIG-1, SIG-1/R, S48-D6:** price and idiosyncratic momentum are SIG-1 and SIG-1/R variants. Factor-momentum timing follows the source (REN-D4). One channel per signal (R-7c).
- **R-1 and EQ-MAP-5:** REN-D3 (`S4_SIGNAL_PC_COMPATIBILITY.md` §4; `S4_EQUATION_REGISTER.md`).
- **ADR-0012:** descriptors stay separate in the data model (§1); the composite is an explicit versioned aggregation (§4); the score enters construction only through EQ-MAP-5 (§3).
- **Hand-forward to S4.16:** diversification diagnostics for the composite (factor-portfolio correlations, nominal versus effective exposures, effective number of factors, leave-one-out) and timing monitoring (tilt frequency against the null band), as part of the Option D total-portfolio packet.

## 11. Issues in the sources

Recorded in the source inventory §23 and the owner assessments. Condensed:
- "Sharpe ratio" is return/volatility (no risk-free rate).
- Start-date labels: March vs May 2004 for identical numbers. The guide's base date, 22 Mar 2004, supports March.
- August's beta bound 1.20 is a misprint (guide: 0.98–1.02).
- The intangible ratio has no price variable.
- "Double or halve" holds before renormalisation (actual 0.4×–2.0×).
- Factor-of-factors feedback loop.
- The guide's floor table omits momentum for Ang01 (its text includes it).
- The guide's issuer-limit text repeats "0.5bps" for the single-factor indices (a typo).

## 12. Next steps

- S4.15 (upstream inventory): fold this record in.
- S4.20: typed contracts (06 §5 fields) for the 18 signals, four factor scores, the aggregation, EQ-MAP-5 and the timing models.
- S4.24: synthetic fixtures (P-R1 … P-R8 are the starting point).
- S6: the data map (§9).
- S7: pre-register the variants with multiple-testing control, the embargo, null calibration and shadow-mode criteria (RQ-37).
- S9c/S9d → G9; S10 security risk model; S11 construction with cardinality.
