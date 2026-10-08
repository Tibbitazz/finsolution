# S4 record — peer scoring methods: Investwiser (Greenblatt, O'Shaughnessy, quality), Seeking Alpha factor grades

**Document status:** DRAFT (S4 record, 2026-10-08). The method work belongs to S9c → G9. · **Companion to:** `S4_SCORING_SORENSEN.md` (the reference specification) · **Basis:**
- owner request 2026-10-08: "identify the true source of the O'Shaughnessy and Magic Formula used in InvestWiser; how they compute profitability and quality; go through Seeking Alpha's factor methods; can we use them alongside the Sørensen metrics?";
- ADR-0012 (§1–§4);
- ADR-0025 (admission criteria);
- RQ-28 … RQ-32 and RQ-37.

**What this is not:**
- **Not an adoption.** Nothing changes the Sørensen reference specification.
- **Vendor back-tests are not evidence** (P13; RQ-37). This includes Seeking Alpha's "beat the S&P 12 of 13 years", Investwiser's "tested back to 1996" and Greenblatt's reported 1988–2004 results.

**Evidence labels:**
- `VERIFIED-SOURCE`: the platform's own published text or code, or a primary paper, with date.
- `VERIFIED-SECONDARY`: a third-party description.
- `CANDIDATE SOURCE`: bibliographic data not yet checked (02, citation rule).
- `INFERENCE`; `VERIFIED-DERIVATION`.

---

## 1. Investwiser: what each score is (from its public front-end definitions, accessed 2026-10-08)

**Common construction:**
- Every component is a **percentile rank 0–100 against all Nordic stocks** in its universe. The translation keys say "sammenlignet med andre nordiske aksjer, fra 0 til 100".
- So the comparison universe is global-Nordic, not sector-relative.
- Fundamentals come from EODHD (`S6_LEAD_DATA_SOURCES_2026-10-08.md` §4.2), as TTM and annual series.

| Score (field) | Investwiser's own definition | Components exposed in the code | Attributed original |
|---|---|---|---|
| **Magic Formula** (`magic_formula_pct`) | "Magic Formula score (Greenblatt). Ranks by return on capital and earnings yield" | `rank_roc_greenblatt`: "Return on capital — Greenblatt (EBIT / (net fixed assets + working capital))". `rank_earnings_yield_greenblatt`: "inntjeningsavkastning slik Greenblatt regner den". The formula is not printed; the app also carries `ev_ebit_ttm` and `ebit_yield_ttm`, so EBIT/EV is likely (`INFERENCE`) | Greenblatt, *The Little Book That Beats the Market* (§2.1) |
| **O'Shaughnessy** (`oshaughnessy_pct`) | "O'Shaughnessy Value Composite. Combines multiple value measures per James O'Shaughnessy" | Ranks labelled "(O'Shaughnessy)": `rank_ev_ebitda_yield` (EBITDA / EV, EV = market cap + net debt), `rank_ocf_yield` (operating cash flow / market cap), `rank_shareholder_yield` ("utbytte, tilbakekjøp og gjeldsnedbygging"). Other value ranks present: `rank_earnings_yield`, `rank_book_yield`, `rank_sales_yield`. Together these are the six VC2 inputs (`INFERENCE` that all six enter) | O'Shaughnessy, *What Works on Wall Street*, 4th ed. (§2.2) |
| **Quality** (`quality_pct`) | "Quality score based on equity ratio, ROA, and earnings stability". A variant text says "lønnsomhet, finansiell helse, resultatstabilitet" | `rank_roa`, `rank_equity_ratio` (equity / total assets), `rank_ni_growth_volatility` ("jevn resultatvekst"). The stability statistic (window, estimator) is **not stated** | No attribution. A practitioner blend of profitability, leverage and stability |
| **Value** (`value_pct`) | "Value score based on P/E, P/B, dividend yield, and cash flow". A second text says "K/E, K/B, EV/EBITDA relativt til universet" (**inconsistent** descriptions) | — | No attribution |
| **Trend** (`momentum_pct`) | "Momentum score based on price performance over 3-12 months" | `rank_ret_3m`, `rank_ret_6m`, `rank_ret_12m_skip1m` | 12-1 is the academic convention (as in Sørensen); 3 m and 6 m are not skip-month |
| **Total / Fundamental / Conviction** (`qvm_pct`, `qv_pct`, `qm_pct`) | Combinations of quality, value and trend ("Graham & Dodd-inspirert" for QV) | Combination rule not stated | — |
| Other diagnostics (not in the scores, as far as visible) | — | Piotroski F-score (nine criteria listed), Altman Z, Beneish M, Sloan ratio, "Operating Profitability (Novy-Marx)" | See §2.3 |

**Deviations from the originals** (`VERIFIED-SOURCE` for Investwiser's text, `VERIFIED-SECONDARY` for the originals):

| # | Deviation |
|---|---|
| IW-1 | **Shareholder yield includes debt paydown.** O'Shaughnessy's shareholder yield is dividend yield plus buyback yield (VC3 uses buyback yield only). Adding net debt paydown is the definition used by other authors (secondary sources). So Investwiser's VC is a variant, not O'Shaughnessy's VC2 |
| IW-2 | **"Operating Profitability (Novy-Marx)" is defined as gross profit / total assets.** Novy-Marx's measure is *gross* profitability. "Operating profitability" is the Fama–French (2015) RMW construct with a different numerator and book equity in the denominator. The label conflates two different measures |
| IW-3 | **The Value score has two inconsistent descriptions** (P/E, P/B, dividend yield, cash flow vs P/E, P/B, EV/EBITDA) |
| IW-4 | **The quality stability statistic is undisclosed**, as is the combination rule of the composites. They cannot be reproduced |

## 2. The original sources

### 2.1 Greenblatt's "Magic Formula" · `VERIFIED-SECONDARY` (book not in hand)
- **Source:** Joel Greenblatt, *The Little Book That Beats the Market* (Wiley; 2005/2006 and later editions) (`CANDIDATE SOURCE` for exact edition and pages).
- **Definitions:**
  - Return on capital (ROC) = **EBIT / (net working capital + net fixed assets)**.
  - Earnings yield (EY) = **EBIT / enterprise value**.
- **Procedure:**
  - rank every eligible stock on ROC and on EY (rank 1 = best);
  - add the two ranks; the lowest sum is best.
- **Eligibility:** minimum market capitalisation; **exclude utilities and financials**; some versions also exclude foreign listings.
- **Portfolio rule:** buy 20–30 top names, staggered over the year; hold about a year; rebalance annually.
- **Why EBIT and EV:** EBIT neutralises tax and leverage differences; EV includes debt.
- **Category:** a **cross-family composite**. EY is a value metric and ROC a profitability/quality metric, so in our terms it is an across-signal aggregation (RQ-32), not a within-factor composite.

### 2.2 O'Shaughnessy's Value Composites · `VERIFIED-SECONDARY` (book not in hand)
- **Source:** James P. O'Shaughnessy, *What Works on Wall Street*, 4th ed. (McGraw-Hill, 2011) (`CANDIDATE SOURCE` for pages).
- **Composites:**
  - **VC1** = P/B, P/E, P/S, EBITDA/EV, P/CF;
  - **VC2** = VC1 + shareholder yield (dividend + buyback);
  - **VC3** = VC1 + buyback yield.
- **Scoring:** each factor gets a percentile **1–100** across the universe, cheapest = 1 in the book's orientation. The ranks are **averaged and re-ranked** into percentiles.
- **Missing data:** a missing factor is **ignored**, provided at least **three** factors are present.
- **Related strategy:** "Trending Value": top decile of VC2, then the top 25 by 6-month price momentum.
- **Later change:** the author's firm later moved away from P/B (secondary report).

### 2.3 Primary literature for quality and profitability (what a well-founded quality family should rest on) · `CANDIDATE SOURCE`
All entries are to be obtained and verified at S9c; bibliographic data is from memory and not yet checked.

| Measure | Primary | Note |
|---|---|---|
| Gross profitability GP/A | Novy-Marx (2013), "The Other Side of Value: The Gross Profitability Premium", *JFE* | The measure Investwiser labels "Novy-Marx" |
| Operating profitability OP | Fama & French (2015), "A Five-Factor Asset Pricing Model", *JFE* | RMW factor; book-equity denominator |
| Quality minus junk (profitability, growth, safety, payout) | Asness, Frazzini & Pedersen (2019), "Quality Minus Junk", *RAST* | A multi-dimensional quality definition with z-scored components; AQR publishes QMJ factor data (S6 lead §3) |
| F-score | Piotroski (2000), *JAR* | Nine binary signals |
| Accruals (Sloan ratio) | Sloan (1996), *Accounting Review* | Earnings quality |
| Distress (Z) and manipulation (M) | Altman (1968), *JF*; Beneish (1999), *FAJ* | Diagnostics rather than return signals |

## 3. Seeking Alpha factor grades · `VERIFIED-SOURCE` (help centre and symbol pages, accessed 2026-10-08)

**Construction** (from the "Quant Ratings and Factor Grades FAQ"):
- "Over 100 metrics for each stock are compared to the same metrics for the other stocks in its **sector**".
- Five factor grades, **A+ to F**: Value, Growth, Profitability, Momentum, EPS Revisions.
- The overall rating is Strong Sell … Strong Buy (score 1.0–5.0) and is "**not a simple average** … some factors are weighted higher than others", "to maximize the predictive value".
- **Caps:** a stock is "disqualified as anything higher than a Neutral" if Growth, Momentum or EPS Revisions is D+ or worse, or Value or Profitability is D− or worse.
- The overall rating "also takes account of a stock's size and risk".
- Updated daily before the open. About 5,600 stocks, **only with sell-side coverage**; US listings and ADRs; no foreign exchanges.
- Designed by Steven Cress.
- **Why sector-relative:** sectors have different profitability and growth and therefore different average valuations. Seeking Alpha rejects DCF and own-history valuation for the value grade.

**Metrics shown per factor** (KO symbol pages; grades are behind the paywall):

| Factor | Metrics (each shown vs sector median and vs the stock's own 5-year average) |
|---|---|
| Value | P/E non-GAAP and GAAP (TTM, FWD); PEG (TTM, FWD); EV/Sales, EV/EBITDA, EV/EBIT, P/S, P/B, P/CF (each TTM and FWD); dividend yield |
| Growth | Revenue, EBITDA, EBIT, EPS diluted and GAAP growth (YoY and FWD); EPS long-term growth (3–5 y); levered FCF, FCF per share and OCF growth; ROE growth; working-capital and capex growth; dividend growth |
| Profitability | Gross, EBIT, EBITDA, net-income and levered-FCF margins; return on common equity, total capital and total assets; capex/sales; asset turnover; cash from operations (level); cash per share; net income per employee |
| Momentum | 3-, 6-, 9- and 12-month price performance (sector-relative) |
| EPS Revisions | "quantity of revisions": up vs down revisions relative to the sector (window not stated on this page; a third-party summary says 90 days) |

**Properties relevant to us:**
- About half the Value and Growth metrics and all EPS Revisions **require consensus estimates** (FWD).
- Some profitability metrics are **size-dependent levels** (cash from operations, net income per employee), mixed with ratios.
- Weights are undisclosed and selected for predictive value, which is in-sample selection unless shown otherwise.

## 4. One generic structure behind all of these methods (`VERIFIED-DERIVATION` / synthetic check)

Every method above is an instance of one cross-sectional composite-score contract with declared parameters:

| Parameter | Sørensen (reference) | Greenblatt MF | O'Shaughnessy VC2 | Investwiser Q/V/M | Seeking Alpha grades |
|---|---|---|---|---|---|
| Metrics and orientation | −P/E, −P/B; 12-1 return | EY = EBIT/EV, ROC = EBIT/(NWC + NFA) | P/B, P/E, P/S, EBITDA/EV, P/CF, shareholder yield | See §1 | >100, see §3 |
| Eligibility exclusions | listwise missing | utilities, financials, size floor | ≥ 3 factors present | finance sector for some metrics | sell-side coverage required |
| Comparison universe | global (MSCI World) | eligible universe | universe | all Nordic | **sector** (plus own 5-year history displayed) |
| Transform | z-score | ordinal rank | percentile 1–100 | percentile 0–100 | letter grade (quantile class) |
| Combine | **z-sum, then rank** | **rank-sum** | **mean percentile, then re-rank** | not stated | **weighted (undisclosed) + caps** |
| Reproducible from public text? | Yes (code) | Yes | Mostly (book) | No (IW-4) | **No** |

**Results:**
- **G-1** (`VERIFIED-DERIVATION`):
  - With no missing data, Greenblatt's rank-sum ordering is **identical** to the ordering of the mean percentile. With $p = (r-1)/(N-1)$, the mean percentile is an affine function of the rank sum.
  - Numerically identical once floating-point noise among equal rank sums is removed.
  - So Greenblatt and O'Shaughnessy are both **rank-then-combine**, which is variant O-7(b) of the Sørensen record.
- **G-2** (synthetic; seed 20261008; N = 500; two lognormal metrics):
  - z-then-combine (Sørensen reference) and rank-then-combine have Spearman correlation 0.94, but share only **27 of the top 50** names.
  - **O-7 materially changes the selected portfolio.** It must be a pre-registered variant, never a silent implementation detail (RQ-29, RQ-31, RQ-37).
- **G-3** (synthetic; six metrics; 15% missing at random):
  - O'Shaughnessy's "average over available, ≥ 3 required" versus "fill with the median" shares 39 of the top 50.
  - The missing-data rule is also material (O-6).

## 5. Can we use these methods alongside the Sørensen metrics? Fit verdicts

**General answer: yes, as *candidate variants of our own specification*, not as imported vendor scores.** Five conditions apply:
1. **Own specification from primary sources:** definitions written from the books and papers, not from vendor tooltips.
2. **Neutral naming:** e.g. "EY–ROC rank composite (Greenblatt-type)". Whether "Magic Formula" is a protected mark is `UNVERIFIED`.
3. **Pre-registration:** every variant enters the pre-registered grid (RQ-37). Nothing is chosen because a vendor or author reports good returns.
4. **Data:** primary as-filed data (EDGAR; ESEF via filings.xbrl.org), point-in-time by filing date, or per-user licensed data (DR-7).
5. **Composition:** ADR-0012 §4 holds. Across-family composites (Magic Formula = value × quality; QVM) are RQ-32 aggregation methods, not master scores.

| Method | Verdict | Reason | Data feasibility |
|---|---|---|---|
| **EY = EBIT/EV** (value descriptor) | **FITS**, as an RQ-28 value metric | Clear mathematics; uses EV (leverage-neutral); avoids P/E's loss-maker problem only if EBIT > 0 is handled (cf. P-5) | Statements + price; IFRS 16 lease liabilities in EV must be declared |
| **ROC (Greenblatt)** (quality/profitability descriptor) | **FITS**, as an RQ-28 quality metric | Clear mathematics. Denominator ≤ 0 needs a rule | Statements; annual ESEF suffices |
| **Greenblatt EY + ROC rank composite** | **PARTIAL**, as an RQ-32 cross-family variant | Reproducible, but it fixes the across-family weights (1:1) and the transform (rank-sum). Registered as a variant, not a default | As above; financials and utilities excluded by eligibility predicate (06) |
| **O'Shaughnessy VC2-type value composite** | **FITS**, as an RQ-31 within-value composite variant | Superset of Sørensen's value metrics (P/E, P/B) plus P/S, EBITDA/EV, P/CF, shareholder yield. Exact rules: percentile, average, re-rank, ≥ 3 present | Statements + price; buyback data needs cash-flow-statement detail |
| **Investwiser Quality** (ROA, equity ratio, earnings stability) | **PARTIAL** (concept only) | Mixes profitability, leverage and stability; the stability statistic is undisclosed (IW-4). Re-specify from primaries (§2.3) | Feasible; stability needs ≥ 5 years of history |
| **Primary quality measures** (GP/A, OP, QMJ components, F-score) | **FITS**, as RQ-28 quality candidates | Published definitions | Statements; QMJ safety needs price-based beta and volatility |
| **Investwiser QVM / QV / QM totals** | **DOES NOT FIT** as defined | Combination rule undisclosed; it would also be a master composite (ADR-0012 §4) | — |
| **Seeking Alpha Quant Rating** (overall) | **DOES NOT FIT** | Undisclosed weights selected "to maximize the predictive value" (fails ADR-0025 reproduction; in-sample selection risk); US only; requires sell-side estimates | — |
| **Seeking Alpha concept: sector-relative grading** | **PARTIAL**, as an RQ-30 / O-4 variant | Sector-relative comparison is exactly variant O-4. Letter grades are a quantile-class transform (RQ-29). Their argument (sectors differ in profitability and growth) is a hypothesis to test, not a finding | Needs a sector classification. GICS is licensed; an open alternative must be chosen at S6 |
| **Seeking Alpha concept: own-history comparison** ("% diff. to 5Y avg") | **PARTIAL**, as a time-series state descriptor (ADR-0012 §1, S^TS), not a cross-sectional score | Different descriptor type | Feasible |
| **Seeking Alpha concept: disqualification caps** | **PARTIAL**, as an explicit non-linear aggregation rule (RQ-32) | Could be specified transparently if a composite is ever admitted | — |
| **EPS Revisions; forward growth and FWD multiples** | **DEFERRED** | Need point-in-time consensus estimates (S6 lead F-4: paid or academic only) | Not feasible with free data |
| **Momentum variants** (3 m, 6 m, 9 m, 12 m; 12-1; sector-relative) | **FITS**, as SIG-1 variants | 3 m and 6 m without skip-month overlap the short-term reversal window. 12-1 remains the reference | Prices only |

## 6. Proposed registration (candidates for the S9c grid; nothing adopted)

| ID (candidate) | Type (ADR-0012) | Definition | Status |
|---|---|---|---|
| SCORE-VAL | S^CS value | Sørensen reference (V0) / corrected (V1) | Reference (`S4_SCORING_SORENSEN.md`) |
| SCORE-VAL-VC | S^CS value composite | VC1 / VC2 / VC3-type (§2.2) | Variant (RQ-31) |
| DESC-V-EYEV | S^CS value metric | EBIT / EV | Candidate (RQ-28) |
| DESC-Q-ROCG, DESC-Q-GPA, DESC-Q-OP, DESC-Q-ROA, DESC-Q-FSCORE, DESC-Q-ACCR | S^CS quality metrics | §2.1, §2.3 | Candidates (RQ-28) |
| AGG-EYROC | Across-family aggregation | Greenblatt-type rank composite | Variant (RQ-32) |
| SCORE-MOM (12-1) + variants (3/6/9/12 m; sector-relative) | S^CS momentum | §1, §3 | Reference + variants (SIG-1) |
| DESC-REV, DESC-GROWTH-FWD | S^CS estimates-based | §3 | DEFERRED (PIT consensus) |

**Parameters every candidate declares** (one typed contract, §4):
- metric set and orientation;
- eligibility exclusions;
- comparison universe (global / region / **sector**);
- transform (z / percentile / rank / quantile class);
- combine order (**z-then-rank vs rank-then-combine**, G-2);
- missing-data rule (G-3);
- outlier rule (P-4);
- re-rank.

## 7. Open items
1. Obtain Greenblatt (book) and O'Shaughnessy (4th ed.) for `VERIFIED-SOURCE` definitions. Obtain the §2.3 primaries.
2. Decide an open sector classification for sector-relative variants; GICS is licensed (S6).
3. Accounting conventions for Nordic IFRS data: EBIT definition; IFRS 16 leases in EV and NFA; negative or zero denominators; financials and utilities handling; TTM vs annual (ESEF is annual only).
4. Naming and trademark check for "Magic Formula".

## 8. Sørensen vs Greenblatt: how to decide (owner question, 2026-10-08)

**First, a clarification of G-2.** The 27/50 overlap compared two *orders of operation* on the **same** metrics. It is not a Sørensen-vs-Greenblatt comparison. On real data the two will disagree more, because they use different metrics:
- **Sørensen:** pure cheapness (−P/E, −P/B), with momentum as a separate score;
- **Greenblatt:** cheapness on an enterprise basis (EBIT/EV) **plus** profitability (ROC).

**Is one "more accurate"? Neither, a priori.** They answer different questions:
- Sørensen: how cheap is the stock?
- Greenblatt: how cheap *and* how profitable is it?

Their usefulness is **predictive power for future, risk-adjusted, net-of-cost returns in our universe**. That is an **empirical belief question**, not a preference (ADR-0009: beliefs ⊥ preferences). Preference enters only if the investor has a non-pecuniary taste (e.g. "I want to own profitable companies"). That would be a Policy Statement field, never a reason to prefer a signal.

**What the literature suggests** (priors and leads only; not our evidence; `VERIFIED-SECONDARY` unless stated):
- **For adding profitability:** Novy-Marx (2013, *JFE* 108(1)): gross profitability predicts returns "roughly as well as book-to-market", and "controlling for profitability also dramatically increases the performance of value strategies, especially among the largest, most liquid stocks" (abstract wording via secondary records).
- **Against Greenblatt's ROC leg:** Gray & Carlisle (*Quantitative Value*, 2012), per a CFA Institute review: the Magic Formula's edge comes from EBIT/EV, with none from ROC. EBIT/EV alone beat the two-factor formula by more than 2% per year (1974–2011, US).
- **Nordic evidence is mixed:**
  - Finland 1991–2013 (peer-reviewed): EBIT/EV gave the best risk-adjusted returns among value variants;
  - Oslo 2003–2022 (NHH thesis): Magic Formula alpha of about 0.5% per month, significant before costs and weak after;
  - Nordic 2008–2021 (NHH thesis): significant alpha before costs.

  Theses are leads only.

**Taken together:** the *metric* (EBIT/EV vs P/E, P/B), the *profitability* dimension and the *combination rule* are three separable questions. The literature does not settle them for our universe and costs.

**Decision protocol** (pre-registered in S7 under RQ-37, before any result is seen):

| Step | Rule |
|---|---|
| D-1 | **Define both exactly:** Sørensen V0/V1; Greenblatt-type AGG-EYROC; plus the separable components DESC-V-EYEV and DESC-Q-ROCG. Same universe, rebalance frequency, point-in-time data (filing-date lag), cost model and eligibility |
| D-2 | **Primary metric:** a long-only top-quantile portfolio per signal vs the universe benchmark, giving **net-of-cost active return and information ratio**. **Secondary:** rank IC (Spearman of score vs next-period return; mean and HAC t-statistic); decile monotonicity; turnover |
| D-3 | **Head-to-head:** a test of the IR or Sharpe difference with HAC standard errors. **Spanning regressions** (regress A's returns on B's and the market's; is A's alpha given B non-zero, and B's alpha given A?) separate "different" from "better" |
| D-4 | **Multiple testing:** the variant count is fixed in advance, with deflated-Sharpe / higher t-hurdle logic (D7) |
| D-5 | **Power, stated up front** (D9; T ≈ 2(1−ρ)(2/ΔSR)² years to reach t = 2). See the table below |
| D-6 | **Decision rule if the test cannot discriminate (the likely case):** prefer by (i) robustness across sub-periods and markets, (ii) turnover and cost, (iii) economic rationale, (iv) simplicity. Or **do not choose**: keep both as separate descriptors (ADR-0012 §4) and let the portfolio/CIO layer diversify across them (AMP combine strategy returns, not scores) |
| D-7 | **Confirm forward:** an untouched holdout plus a prospective record before any production default changes |

Power table for D-5:

| Correlation ρ of the two strategies' returns | ΔSR = 0.1 | ΔSR = 0.2 | ΔSR = 0.3 |
|---|---|---|---|
| 0.5 | 400 years | 100 | 44 |
| 0.7 | 240 | 60 | 27 |
| 0.9 | 80 | 20 | 9 |

(Leading-term approximation; i.i.d. returns.) **With realistic history (10–30 years) only large differences are detectable**, which is why D-6 matters more than a "winner" test.

**Recommendation:**
- Sørensen stays the **reference** (owner designation; reproduction oracle).
- The Greenblatt-type composite and its separable components are pre-registered **variants**.
- The decision is taken at G9 by D-1 … D-7.
- Expected outcome under low power: decomposition plus combination (cheapness on an enterprise basis plus a separate profitability descriptor), not a winner-takes-all choice.

## 9. Score table: separate scores for the dashboard and for agent review (owner request, 2026-10-08)

**Owner request:** "perhaps the Sørensen and Greenblatt may show two different scores instead of combining them, since they show two different things. We want to construct a similar scoring table as Investwiser has shown. This will be useful for the dashboard for our visual analysis, and the agents when they are doing their review."

**Answer: agreed, with one refinement.**
- **Separate display is already what our rules require:**
  - ADR-0012 §4 (no master composite);
  - Sørensen's own value and momentum are already two scores (`S4_SCORING_SORENSEN.md` S-5);
  - §8 D-6 ("do not choose; keep both as separate descriptors").
- **Refinement: they are only partly "two different things".**
  - Sørensen Value (−P/E, −P/B) and Greenblatt's earnings yield (EBIT/EV) both measure **cheapness** and should usually be positively rank-correlated.
  - The genuinely different content is Greenblatt's **return on capital** (profitability) and Sørensen's **momentum**.
  - Greenblatt's score is itself a combination (EY + ROC).

  So the table shows the **legs** as columns, and the Greenblatt-type combined rank only as a labelled aggregation variant. A reader can then see *why* the two methods disagree on a stock, e.g. "cheap but unprofitable" or "profitable but expensive".
- **Display does not decide inputs.** Which scores feed beliefs or portfolio construction is still decided by the §8 protocol at G9. A column's presence is not an admission (ADR-0025).

### 9.1 Layout (v0 proposal; nothing adopted)
One row per security in the declared universe at an as-of date, and one column per descriptor. This follows the Investwiser format (percentiles 0–100 against a stated universe, §1), with our own specifications and without undisclosed totals.

| Group | Column | Descriptor ID (§6) | Definition (summary) | Cell | Status badge |
|---|---|---|---|---|---|
| Value | Value (Sørensen) | SCORE-VAL (V0; V1 variant) | z(−P/E) + z(−P/B), re-standardised, then percentile | 0–100 | REFERENCE |
| Value | Earnings yield, EV basis (Greenblatt-type) | DESC-V-EYEV | EBIT / EV | 0–100, raw % on drill-down | CANDIDATE |
| Value | Value composite (O'Shaughnessy-type) | SCORE-VAL-VC | VC2-type: mean percentile of six metrics, re-ranked | 0–100 | VARIANT |
| Quality | Return on capital (Greenblatt-type) | DESC-Q-ROCG | EBIT / (NWC + NFA) | 0–100, raw % on drill-down | CANDIDATE |
| Quality | Gross profitability | DESC-Q-GPA | Gross profit / total assets (Novy-Marx) | 0–100 | CANDIDATE |
| Quality | Operating profitability | DESC-Q-OP | Fama–French (2015) RMW-type | 0–100 | CANDIDATE |
| Quality | Return on assets | DESC-Q-ROA | Net income / total assets | 0–100 | CANDIDATE |
| Quality | F-score | DESC-Q-FSCORE | Nine binary criteria (Piotroski) | **raw 0–9**, not a percentile | CANDIDATE |
| Quality | Accruals | DESC-Q-ACCR | Sloan-type accruals | 0–100 | CANDIDATE |
| Momentum | Momentum 12–1 (Sørensen) | SCORE-MOM | P(t−1)/P(t−12) − 1 on a total-return index | 0–100 | REFERENCE |
| Momentum | 3 m and 6 m returns | SCORE-MOM variants | No skip month; they overlap the short-term reversal window (§5) | 0–100 | VARIANT |
| Aggregation (labelled) | EY–ROC rank composite (Greenblatt-type) | AGG-EYROC | Rank-sum of EY and ROC, shown as a percentile | 0–100 | AGGREGATION VARIANT (RQ-32) |
| Context (not scores) | Sector, country, currency, market cap, liquidity, data as-of | — | Raw values | — | CONTEXT |
| Deferred | EPS revisions; forward growth | DESC-REV, DESC-GROWTH-FWD | — | — | DEFERRED (point-in-time consensus) |

### 9.2 Cell contract (every non-context cell)

| Field | Content |
|---|---|
| Value | Percentile 0–100 by percent_rank = (rank − 1)/(n − 1), as in `S4_SCORING_SORENSEN.md` S-5; or a raw value for count scores |
| Raw inputs (drill-down) | Each metric with units, fiscal period (TTM or annual; period end), price date and currency |
| Comparison universe | ID, definition and N on the as-of date. The column header states it (e.g. "pct vs Nordic eligible, N = 412") |
| Method | Transform and combine order (z-then-rank vs rank-then-combine, G-2), missing-data rule (G-3) and method version (e.g. V0/V1) |
| Provenance | Data source, filing or publication date, as-of timestamp (point-in-time; DR-1) |
| Staleness | ADR-0012 §2 staleness state |
| Null reason | A code from §9.3. A blank cell always says why |
| History | Stored point-in-time values over time (sparkline). **Never recomputed with later-restated data** |
| Admission and use | Status badge (§9.1) plus the consumer roles that currently use the descriptor (admitted uses per consumer, ADR-0026 §8) |

### 9.3 Null-reason codes (requirements; the S9c contract defines them)

| Code | Meaning | Example |
|---|---|---|
| NR-1 | Input missing | No EBIT reported. In V0, listwise deletion (S-6) blanks both Sørensen scores |
| NR-2 | Ineligible by predicate | Financials and utilities for EV-based metrics |
| NR-3 | Sign or denominator rule | ROC with NWC + NFA ≤ 0; P/E for loss-makers in V0 (P-5) |
| NR-4 | Insufficient history | Fewer than 12 months of prices; under 5 years for stability measures |
| NR-5 | Stale beyond limit | Last filing older than the staleness limit |
| NR-6 | Comparison group too small | Sector-relative variant below the minimum group size (RQ-30) |

### 9.4 Rules

| Rule | Content | Reason |
|---|---|---|
| T-1 | **No master total by default.** AGG-EYROC, and any QVM-type total, appear only as labelled aggregation variants registered under RQ-32 | ADR-0012 §4; a total hides which leg drives it (§5: Investwiser totals DOES NOT FIT) |
| T-2 | **Display ≠ signal.** A column is shown with its status badge. Showing it neither admits it nor makes it a belief or PC input | ADR-0025; §8 |
| T-3 | **The universe is explicit.** Changing the comparison universe (global, region, sector) creates a different descriptor ID, not a toggle on the same one | O-4; RQ-30 |
| T-4 | **Agents cite, challenge and never compute.** They cite cell IDs (descriptor, as-of, version). A challenge (e.g. P/E is meaningless for a loss-maker; EV distorted by IFRS 16 leases) is a structured note against the cell, never a changed number | R8; ADR-0012 §5 |
| T-5 | **Overlap panel.** For the current universe and date, show the cross-sectional Spearman correlation matrix among the displayed columns, with its history | Answers "do Sørensen and Greenblatt measure different things?" with data each period. Highly correlated columns are fewer independent bets (cf. N_eff, `S4_ANG_BASELINE.md` §13.1) |
| T-6 | **Disagreement view.** List securities where two columns diverge by more than a declared percentile gap (e.g. top quintile on SCORE-VAL, bottom half on DESC-Q-ROCG). The gap is a display parameter, not a signal | Directs review to the cases where the methods differ |
| T-7 | **Neutral encoding.** Percentiles on a neutral sequential scale; no buy/sell colours or labels | ADR-0017 (analysis-only default) |
| T-8 | **One artefact, two consumers.** One deterministic Score Table artefact per (universe, as-of, method versions). The dashboard renders it (S8 view registry, PM-9; S14 report). Agents receive it, or row subsets, inside evidence packets (RQ-34) | Dashboard and agents never see different numbers |

### 9.5 How agents use it in review
- **Security-sleeve reviewers and the CRO:**
  - cite which descriptors drive a proposal's holdings;
  - flag concentration in one leg (e.g. all cheapness, no profitability);
  - flag holdings with null or stale cells.
- **Learning (ADR-0027 D1, proposed):** the stored table at each as-of date is the record against which later outcomes are measured (Forecast and Outcome Records). Scores are deterministic and point-in-time, so their historical evaluation is valid. There is no LLM look-ahead (`S4_SCORING_SORENSEN.md` §5).

### 9.6 Asset-class analogue (not specified here)
ANG works at the asset-class level. The analogous object there is an **asset-class evidence panel**: one row per asset class, with columns for:
- the CMA by method and the judge's final estimate and range;
- confidence;
- the TSMOM state;
- volatility under the authoritative risk model for that problem, with horizon (ADR-0027 D3 r3).

Its type belongs in the S4.3 taxonomy; its content belongs in S4.15.

### 9.7 Open items
- Column set and display order: S9c and S14. Display order is a presentation preference, not a belief.
- Universe (Nordic, global, other): S5. Open sector classification: §7 item 2.
- Data: S6. ESEF is annual only, so TTM fields need another source.
- Visual mock-up: S8/S14. The UI concept prototype stays outside GitHub.

## Appendix — verification script (synthetic; reproduces G-1 … G-3)

```python
import numpy as np; from scipy.stats import rankdata, spearmanr
rng = np.random.default_rng(20261008); N = 500
z = lambda x: (x - x.mean()) / x.std(ddof=1); pct = lambda x: (rankdata(x) - 1) / (len(x) - 1)
ey = np.exp(rng.normal(np.log(.08), .6, N)); roc = np.exp(rng.normal(np.log(.15), .9, N))
R = rankdata(-ey) + rankdata(-roc); avgp = (pct(ey) + pct(roc)) / 2
assert np.array_equal(rankdata(-R, method='min'), rankdata(np.round(avgp, 12), method='min'))   # G-1
zc = z(ey) + z(roc); top = lambda s, k=50: set(np.argsort(-s)[:k])
print(round(spearmanr(zc, avgp)[0], 4), len(top(zc) & top(avgp)))                             # G-2: 0.9415, 27
```
