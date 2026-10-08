# S4.1 — ANG v2 architectural baseline: canonical, page-cited reconstruction

**Document status:** DRAFT for owner review (S4.1; exit = owner review; SYNC-1 together with S4.2) · **Prepared:** 2026-10-08 · **Basis:**
- ADR-0023 (ANG as the architectural baseline);
- ADR-0024 (S4 method governance);
- S4_PLAN §G row S4.1.

**Supersedes as the canonical map:** S4_PLAN §A, which stays as draft history. Corrections to it are listed in §0.3.

**What this document is.** A faithful reconstruction of what the paper *specifies*: roles, order, data flows, decision rules, contracts, governance and stated limitations. It also lists everything the paper leaves *unspecified* and every internal inconsistency.

**What it is not:**
- **Not the adaptation.** What we adopt, generalise, adapt or defer is S4.2 (`S4_ANG_ADAPTATION.md`).
- **Not a source of defaults.** ANG's numbers and design choices are recorded, never adopted (ADR-0001; S4_PLAN §A.6).

## 0. Sources, conventions, verification

### 0.1 Sources

| Source | Identity | Authority |
|---|---|---|
| **ANG v2:** Ang, Azimbayev & Kim, *The Self-Driving Portfolio: Agentic Architecture for Institutional Asset Management*, 21 Sep 2026 (arXiv 2604.02279 v2) | `DOC/Self-Driving Portfolio.pdf`, 40 PDF pages, md5 `617df77ace2f` | **Primary** (ADR-0023). Newest version (checked 2026-10-07) |
| Q Group lecture, Oct 2026 (41 slides; speaker notes on s13, s22, s27, s31, s38) | PDF md5 `24ae5f9d2479`; PPTX md5 `1f2f5aa17f91` | **Secondary** (same author). Interprets, never overrides. Product content (ApexOS, BARREL) is a lead only |
| Prior records | `ANG_ISSUES_REGISTER.md` (ANG-01 … ANG-27); `S4_INPUTS_2026-10-07.md` §1, §3; `S4_GITHUB_IMPL_REVIEW.md`; REF-01 | Cross-reference |

### 0.2 Conventions
- **Pages are printed page numbers** (PDF page − 1). "p. 0" is the unnumbered title page with the abstract. "sNN" is a lecture slide.
- **Statement labels:**
  - **[P]** stated in the paper text;
  - **[X]** shown in an exhibit (diagrams were read from rendered page images);
  - **[L]** lecture (secondary);
  - **[I]** our inference;
  - **[U]** unspecified by the source, an open item with an owning stage.
- **Verification** (2026-10-08):
  - all 40 pages read in full;
  - Exhibits 1, 2, 4 and 5 read from rendered images;
  - published numbers re-computed (§9, V-1 … V-8).

### 0.3 Corrections found while verifying S4_PLAN §A (the draft)

| Item in §A | Correct reading |
|---|---|
| "illustrative run … not evidence … (pp. 2, 13, 21)" | **pp. 2, 14, 22** |
| Footnote 6 cited as "p. 15" | Footnote 6 starts on **p. 14** and continues on **p. 15** |
| Data vendors not recorded | Exh. A.1 (p. 38) lists the skill **`apex-data-financial (fmp, finviz)`**, a Bloomberg identifier (`BBG: SPTR Index`) and "History: Jan 1990–present" (§5). This also corrects `research/s6/S6_LEAD_DATA_SOURCES_2026-10-08.md` §1, which said ANG names no vendor |
| Exhibit 1 depiction differences not recorded | Exhibit 1 shows CMAs as an *input*, plural "Covariance Agents", a "Risk Agent", and **no CIO or strategy-review box** (ANG-30) |

---

## 1. Scope and boundary of ANG

| Element | ANG | Ref |
|---|---|---|
| Decision scope | Strategic asset allocation (SAA): one "Recommended policy portfolio weights" output per run. For contrast, the conventional process reviews "one recommended portfolio" in a cycle that "typically runs quarterly or semi-annually" | [X] Exh. 1 p. 7; [P] p. 5 |
| Starts from | The IPS: objectives, risk tolerance, horizon, permissible asset classes | [P] p. 5; §4.1 p. 15 |
| Ends at | Target weights plus a board memo. "The weights are then implemented through trading" — no trading role | [P] p. 5; p. 14 |
| Universe (illustration) | 18 ETF-investable asset classes:<br>- 6 equity;<br>- 8 fixed income;<br>- REITs, Gold, Commodities, Cash | [P] p. 15 |
| CMA horizon and units (illustration) | "%, nominal, 3-year horizon" | [X] Exh. 6 p. 17 |
| Benchmark | 60/40 equity–bond (performance comparison and the TE constraint) | [P] pp. 14–15 |
| Agent count | 44 specialised agents (not itemised by the paper; §3) | [P] p. 0; p. 29 |
| Organisational principle | Human moves up the "abstraction ladder" to writing the IPS and supervising (Johnson et al. 2017) | [P] p. 4; §6.1 pp. 26–27 |

## 2. Canonical pipeline: stages, actors, inputs, processing, outputs

```
H0  Human: writes IPS (3 layers) ............................................ p.15, p.26
 │
W   Workflow manager orchestrates every stage (not counted in the 44) ........ p.5; Exh.1
 │
S1  Macro agent ──► macro-view.json (regime, growth/inflation/policy scores) + narrative ... p.7; Exh.A.1
 │        (fetch macro & market data + web search; weighted 4-dimension scoring → 1 of 4 regimes + confidence)
 ├───────────────────────────────┐
S2  18 AC agents (parallel)      S3  Covariance agent ─► Σ (historical data + macro forecasts)   p.6
 │   per AC: hist / valuation /       │
 │   technical / sentiment+web /      │
 │   6 methods + auto-blend (code)    │
 │   → CMA judge (LLM, [min,max])     │
 │   → cma.json … analysis.md         │
 └───────────────┬───────────────────┘
S4  PC agents: 19 fixed + Researcher (parallel, 20) → Adversarial Diversifier (after the 20) ... p.9
 │        (inputs: CMAs + Σ; optimisers run in code; proposal + written justification)
S5  Strategy review ............................................................... pp.10–13
 │   5a CRO: standardised risk report per candidate (neutral; no vote; enforces hard IPS constraints)
 │   5b Peer review: each agent reviews 2 peers (1 intra-, 1 inter-category); seeded random
 │      assignment; 42 reviews; all released simultaneously
 │   5c Vote: modified Borda (top-5: 5,4,3,2,1; bottom flag −2; no self-vote)
 │   5d Blend vote with metric score (regime-dependent weight); diversity: top-5 spans ≥3 of 5 families
 │   5e Top-5 revise (use the two reviews + CRO report; may use any comment)
S6  CIO agent (LLM-as-judge): all 21 candidates + reviews + CRO reports + votes + metric scores
 │   (+ macro, Exh.5) → single method OR one of 7 ensembles (code) → weights + rationale +
 │   invalidation conditions → board memo ......................................... pp.13–14, 19
H1  Human: board / investment committee reads, challenges, approves; flagged deviations ... p.14, p.25
 │
R   Rebalancing: quarterly plan + off-cycle drift triggers (in memo); trading out of scope ..... p.14, p.5
M   Meta agent: after each rebalancing period, feedback vs realised (rolling 3 y) → edits skills,
    prompts, code; human approval above a materiality threshold; IPS/compliance files excluded .. pp.27–28
```

### 2.1 Stage table (detail; every row cited)

| Stage | Actor | Inputs | Processing — **code** vs **LLM** | Outputs | Ref | Unspecified [U] |
|---|---|---|---|---|---|---|
| H0 IPS | Human | — | Three layers: universe; objective; active-risk budget. Hard/soft classification | IPS document; every agent reads it | [P] p. 15; p. 26 | Format/schema of the IPS as an agent input |
| W Orchestration | Workflow manager | All stage outputs | Sequencing, parallel dispatch, barriers | — | [P] p. 5; [X] Exh. 1 | Orchestration framework; fn. 2 (p. 3) lists frameworks as examples only |
| S1 Macro | Macro agent | Macro and market data; web search ("real-time readings of both numeric and textual information") | **Code:** data fetch; scoring of four dimensions (growth, inflation, monetary policy, financial conditions) "using a weighted scoring framework". **LLM:** classification "with a confidence level" and narrative | Regime ∈ {expansion, late-cycle, recession, recovery} + confidence; `macro-view.json` (regime, growth/inflation/policy scores); narrative report. Consumed by all AC agents | [P] p. 6; p. 7; [X] Exh. A.1 p. 38; skill `macro-regime` p. 36 | Indicator list, weights, thresholds, confidence definition; split of code vs LLM within the classification (**[I]** scoring in code by p. 36's division) |
| S2 Asset-class CMAs | 18 AC agents, parallel | Macro view; historical returns; valuation; technical signals; sentiment and flows via web search; IPS | **Code** (`cma_methods.py`): historical stats; signals; **6 methods + auto-blend**, each returning point estimate, confidence score, component breakdown, rationale. **LLM** (CMA judge, equity ACs): 5-step rules; final ∈ [min, max] of the candidates | Expected return, volatility, confidence; investment-case memo ("13-section" `analysis.md`). Files: `cma_methods.json`, `cma.json`, `signals.json`, `historical_stats.json`, `scenarios.json`, `correlation_row.json`, `analysis.md` | [P] pp. 6, 8–9; [X] Exh. 2 p. 8; Exh. A.1 p. 38; Exh. A.2 p. 39 | Volatility estimator; confidence-score definition; auto-blend weights ("confidence-weighted", p. 39); arithmetic vs geometric; currency/hedging; **non-equity AC method sets and judge (ANG-28)** |
| S3 Covariance | Covariance agent ("Agents" in Exh. 1) | Historical data; macro forecasts | **Code** (by p. 36 / fn. 6) | Asset-class covariance matrix Σ | [P] p. 6; [X] Exh. 1 | Estimator, window, frequency, shrinkage, horizon/units vs CMAs; relation to AC volatility estimates (**ANG-33**); singular vs plural (ANG-04) |
| S4 Proposals | 21 PC agents | CMAs + Σ (p. 6). Some methods need more: capitalisations, scenarios, factor exposures (ANG-17) | **Code:** each fixed method's optimiser. **LLM:** written justification. Researcher: literature search + new method proposal. Adversarial Diversifier: optimisation vs centroid | Proposed weights + written justification per agent | [P] pp. 6–7, 9–10; [X] Exh. 3 p. 11 | Per-method constraints and parameters (S4.5–S4.14) |
| S5a Risk reports | CRO agent | Each candidate portfolio | Standard risk metrics: ex-ante and backtest volatility, VaR, maximum drawdown, concentration, factor tilts, IPS compliance. Neutral: "scores risk and produces commentary, but does not vote". Enforces hard constraints | One standardised risk report per candidate; "Each PC agent receives a CRO agent's report" | [P] pp. 10–11, 15; [X] Exh. 4 p. 12 | Metric definitions (ANG-11 resolved for "effective N", §9 V-6); VaR level and method; backtest window; factor model |
| S5b Peer review | 21 PC agents | Peer proposals; CRO reports | **LLM:** each agent reviews two peers, one intra- and one inter-category. Assignment "randomized with a recorded seed"; 42 reviews; "All reviews are released simultaneously" | 42 reviews | [P] p. 11; fn. 5 | Assignment algorithm and balance (**ANG-36**) |
| S5c Vote | 21 PC agents | All reviews | **LLM:** modified Borda. Top-5 ranking (5, 4, 3, 2, 1) plus a bottom flag (−2), excluding itself. Lecture vote schema: `{top_5[], bottom_1, top_1_justification, bottom_1_justification}` [L s31 notes] | Vote ballots and totals; "dissent reports" for bottom-ranked methods (p. 18; **ANG-32**) | [P] p. 12; [X] Exh. 4 ("vote for two proposals": ANG-01) | Tie-breaking; ballot validation |
| S5d Blend and shortlist | (code [I]) | Vote totals; metric score (weighted composite of backtest Sharpe, IPS compliance, diversification, regime fit, estimation risk, CMA utilization) | Blend with a **regime-dependent weight**. March 2026: 40% normalised vote + 60% normalised metric (reproduced: §9 V-3). Diversity: top-5 must span ≥ 3 of 5 families | Composite ranking; top-5 shortlist | [P] p. 12; p. 17; [L] s31 notes | Metric-score weights; normalisation (min–max, [I] from V-3); regime → weight table (only late-cycle given; ANG-09) |
| S5e Revision | Top-5 PC agents | Two specific reviews; CRO report; all other reviews | **LLM + code:** "revise their proposals … can revise their structured output" | Revised proposals | [P] p. 13 | What may change (resolved for us by ADR-0024 §2; ANG-20) |
| S6 Combination | CIO agent | 21 candidates (Exh. 8 weights all 21; ANG-08), peer reviews, CRO reports, vote tallies, metric scores; macro (Exh. 5) | **LLM-as-judge** over **code** ensembles (`script.py`): choose one method or one of **7 ensembles**:<br>1. simple average;<br>2. inverse tracking-error weighting;<br>3. backtest-Sharpe weighting;<br>4. meta-optimisation (PCs as "assets");<br>5. regime-conditional weighting;<br>6. composite-score weighting;<br>7. trimmed mean.<br>Each is evaluated "on the same diagnostic suite"; IPS compliance "non-negotiable". Scores the 21 methods on six dimensions: backtest Sharpe 25, IPS 15, diversification 15, regime fit 20, estimation robustness 15, CMA utilization 10 | Final weights; written rationale; assumptions; "what would cause the portfolio to no longer be valid"; board memo | [P] pp. 6, 13–14, 19; [X] Exh. 5 p. 13 | Ensemble formulas (centroid membership; trimming fraction; meta-optimiser objective); how the six-dimension scores enter the choice (ANG-09) |
| H1 Approval | Board / investment committee | Board memo | Human: read, challenge, approve. Recommended practice: record a response to each flagged deviation | Approval / rejection | [P] p. 14; p. 25 | — |
| R Rebalancing | (not an agent role) | Memo | "quarterly rebalancing plan with off-cycle drift triggers" | — | [P] p. 14; p. 27 | Drift-trigger rule; implementation (out of scope; ADR-0026 adds it) |
| M Learning | Meta agent | Past macro and AC estimates, signal directions, regime calls; realised returns | After each rebalancing period; rolling 3-year window. **Code:** regime accuracy, cross-sectional rank correlation of expected returns, signal hit rates, per-method prediction error by AC and regime. **LLM:** diagnose weaknesses; research improvements "through backtesting and statistical analysis"; edit skills, prompts and Python code | Structured change log (evidence, reasoning, exact modifications). Above a materiality threshold → human approval; below → automatic. Declared file set excludes the IPS and IPS-compliance files | [P] pp. 27–28; [L] s16, s36 (ANG-25) | Materiality threshold; test protocol before deployment; PC-method and CIO evaluation metrics (**ANG-31**) |

### 2.2 Order, parallelism and information barriers
1. **Macro first.** Its output conditions all downstream analysis ([P] pp. 6–7).
2. **AC agents in parallel** ([P] p. 6). **[I]** The covariance agent can run in parallel with them, since it uses historical data and macro forecasts (p. 6), not CMAs.
3. **PC agents:** 19 fixed + Researcher in parallel; then the Adversarial Diversifier, because it needs the other 20 ([P] p. 9).
4. **Strategy review:**
   - CRO reports **before** peer review ("First", p. 10);
   - reviews **released simultaneously** ([P] p. 11), an information barrier;
   - vote after all reviews are read ([P] p. 11);
   - blend and shortlist; then revision ([P] pp. 12–13).
5. **CIO last** among agents; the human approves the memo ([P] pp. 13–14).
6. **Meta agent:** asynchronous, after each rebalancing period ([P] p. 27).

## 3. Agent roster and count reconciliation

| Role | Count | Ref |
|---|---|---|
| Macro | 1 | [P] p. 6 |
| Asset-class | 18 (one per asset class) | [P] p. 6, p. 15 |
| Covariance | 1 (Exh. 1 says "Agents") | [P] p. 6; ANG-04 |
| PC: fixed methods | 19 | [P] p. 9; Exh. 3 |
| PC: Researcher | 1 | [P] p. 10 |
| PC: Adversarial Diversifier | 1 | [P] p. 10 |
| CRO ("Risk Agent" in Exh. 1) | 1 | [P] p. 10; ANG-05 |
| CIO | 1 | [P] p. 13 |
| Meta | 1 | [P] p. 27 |
| **Total** | **44** | **[I]**: the paper states 44 (p. 0, p. 29) but never itemises it. This is the only itemisation consistent with 44 and a single covariance agent. The workflow manager is not counted |

**PC categories** ([X] Exh. 3 p. 11):

| Category | Methods |
|---|---|
| A, Heuristic (5) | EW, market-cap, inverse volatility, inverse variance, volatility targeting |
| B, Return-optimised (5) | max Sharpe, Black–Litterman, robust MV, resampled frontier, mean–downside |
| C, Risk-structured (5) | GMV, ERC, HRP, maximum diversification, minimum correlation |
| D, Non-traditional (4) | CVaR, max-drawdown-constrained, tail-risk parity, TPA two-factor |
| E, Agentic (2) | Adversarial Diversifier, Researcher |

The text says "four to six methods per category" (p. 9); no category has six (**ANG-35**, L). The registry is meant to become endogenous as methods are added or culled ([P] fn. 4 p. 9; p. 10).

**Agentic PC roles:**
- **Researcher** ([P] p. 10): "explores the literature … identifies objectives not yet represented … proposes a novel method not spanned by the current registry". March 2026: maximum entropy subject to a minimum Sharpe floor (Bera & Park 2008; ANG-10). It finished 11th; "a production pipeline would likely add this method" ([P] pp. 18–19).
- **Adversarial Diversifier** ([P] p. 10):
  - maximise tracking variance relative to the centroid (mean of the other 20 PC weights), subject to Sharpe ≥ 75% of the maximum-Sharpe portfolio;
  - "not intended as a standalone recommendation";
  - voted to the bottom by 18 agents but given 2.7% CIO weight ([P] pp. 19–20; ANG-16).

## 4. Agent anatomy, skills and contracts (App. A; lecture s27)
- **Four components** ([P] p. 36):
  1. a **description** (markdown "job description": role, pipeline position, step-by-step workflow, inputs, analyses, outputs; read by the LLM at runtime);
  2. **scripts** (Python: fetch data from APIs, compute statistics, build expected-return models, run optimisers);
  3. **skills** (shared folders of methodology documentation plus scripts);
  4. an **output contract** (JSON per schema for machines plus markdown for humans; [P] p. 37).
- **Division of labour** ([P] p. 36): "the LLM handles judgment, interpretation, and narrative; the scripts handle computation." The lecture repeats this as "Code for calculation, agents for judgement and reasoning" ([L] s13).
- **Files per agent** ([X] Exh. 2 p. 8; Exh. 5 p. 13; [L] s27, s30):
  - `<agent>.md` (e.g. `us-large-cap.md`, `ig-corp.md`, `cio.md`, `adversarial-diversifier.md`);
  - `SKILL.md`;
  - `script.py`;
  - output reports (`analysis.md`).
- **Description-file fields** ([X] Exh. A.1 p. 38): Role, Slug, BBG ticker, Category, History, Macro sensitivity, Required skills, Workflow (8 steps), Key considerations (asset-specific guidance "read at runtime"), Output.
- **Skill inventory** (union; ANG-26):
  - paper: `macro-regime`, `historical-analysis`, `asset-class-report`, `signal-generation`, `equity-analysis`, `cma-judge`, `apex-data-financial (fmp, finviz)` ([P] pp. 36–39);
  - lecture: `AC-input-loader`, `asset-class-report`, `cash-analysis`, `credit-analysis`, `ensemble-methods`, `equity-analysis`, `historical-analysis`, `macro-regime`, `pc-report`, `portfolio-diagnostics`, `real-assets-analysis`, `signal-generation` ([L] s27 notes).
- **CMA judge skill** ([X] Exh. A.2 p. 39; used "by every equity asset-class agent", [P] p. 37):
  - inputs: `cma_methods.json`, `signals.json`, `macro-view.json`, `historical_stats.json`;
  - **7 candidates:**
    1. historical ERP + Rf;
    2. regime-adjusted;
    3. BL equilibrium;
    4. inverse Gordon;
    5. implied ERP (CAPE);
    6. survey/analyst;
    7. auto-blend (confidence-weighted 1–6);
  - **rules:**
    1. dispersion class: tight < 3 pp, moderate 3–6, wide > 6;
    2. regime logic: late-cycle → valuation + regime-adjusted; expansion → auto-blend; recession → regime-adjusted + BL;
    3. valuation context: P/E > 30× → valuation methods; < 12× → historical + BL;
    4. signal alignment;
    5. select one / custom weights / blend;
  - **constraint:** final ∈ [min_method, max_method].
- **Macro sensitivity** is declared per AC agent (e.g. US Large Cap: Growth +, Rates −, Inflation −, Dollar +; [X] Exh. A.1).

## 5. Data and provenance (what the paper says)

| Item | Statement | Ref |
|---|---|---|
| Data skill | `apex-data-financial (fmp, finviz)`: Financial Modeling Prep and Finviz, as a required skill of the US Large Cap agent | [X] Exh. A.1 p. 38 |
| Identifiers | Bloomberg ticker per AC agent (e.g. `BBG: SPTR Index`) | [X] Exh. A.1 p. 38 |
| History | "History: Jan 1990–present" (US Large Cap); illustrative simulation of the final weights "over 1996-2026 as a static allocation" | [X] p. 38; [P] p. 2 |
| Web search | Macro agent (real-time numeric and textual); AC agents (sentiment, fund flows, positioning) | [P] p. 7; [X] Exh. A.1 |
| Look-ahead mitigation | "proprietary techniques"; retrieval, homogenisation, obfuscation; "we do not claim that these procedures eliminate look-ahead bias" | [P] p. 2; fn. 6 pp. 14–15; pp. 23–24 |
| Point-in-time handling of data | Not specified (**ANG-34**) | [U] |

## 6. Determinism, reproducibility and model governance
- **Code:** "All numerical computation, statistics, and optimizer runs are executed in code, not in the LLM, and are fully replicable" ([P] fn. 6 p. 15; p. 36).
- **Pinned and documented** within a review cycle ([P] fn. 6 pp. 14–15):
  - model version and type per agent;
  - temperature, top-k, top-p and other sampling parameters;
  - peer-review pairing seeds;
  - description files, skills, output contracts, prompts;
  - natural-language reasoning and audit trails.
- **Non-determinism remains** even at temperature 0 (batching, hardware, floating point; Atil et al. 2025; He et al. 2025). "A run for the same historical date … produced at a different time … may produce different numbers" ([P] p. 14; p. 24; [L] s20–21).
- **Evaluation stance:**
  - agentic pipelines "cannot be completely backtested"; prospective evaluation is the remedy (Koijen & Levy 2026);
  - the leakage critique "does not apply … in live production" ([P] p. 2; p. 24).
- **Model risk:** version drift. Mitigations: pin versions; periodically revalidate against "a fixed test battery"; archive prompts, outputs and model identifiers; keep deterministic optimisers as a stable anchor ([P] p. 25).

## 7. Governance (IPS-centred)
- **The IPS is "the most important part"** and the "load-bearing institutional artifact" ([P] p. 15; p. 26). Its three layers in the illustration ([P] p. 15):

  | Layer | Content | Type |
  |---|---|---|
  | (1) Universe | 18 asset classes | **Hard** |
  | (2) Objective | CPI + 3.0–4.0% real return; 8–12% volatility band; −25% maximum drawdown | **Soft** targets |
  | (3) Active risk | Ex-ante TE ≤ 6% vs 60/40 | **Hard** |

- **Enforcement:**
  - the CRO enforces hard constraints and checks IPS compliance for every candidate;
  - the CIO "may not breach" hard constraints and is "instructed to comply";
  - soft-target deviations are "flagged in the board memo … rather than silently overridden" ([P] p. 15; p. 26).
- **Example:** ex-ante volatility of 7.54% sits below the 8% band, a deliberate late-cycle choice that the CRO flags and the CIO accepts. Realised simulated drawdown −25.6% is "just beyond" the −25% soft target ([P] pp. 15–16, 19, 22).
- **Autonomy is a policy choice.** Tightening the TE bound or adding hard floors → supervisory control; relaxing → goal-oriented autonomy ([P] p. 27).
- **Board memo contents** ([P] p. 14):
  - recommended allocation and expected performance vs 60/40;
  - macro rationale;
  - largest positions;
  - changes since the last review;
  - key risks;
  - quarterly rebalancing plan with off-cycle drift triggers;
  - IPS compliance statement;
  - plus, from the CIO, the rationale, assumptions and invalidation conditions.
- **Oversight risks:**
  - **Automation surprise:** committees must genuinely engage, e.g. record a response to each flagged deviation ([P] p. 25).
  - **Security:** self-modifying agents need sandboxing, privilege separation and auditor agents ([P] p. 26).
- **Decomposition principle:** "decompose when the task requires genuinely distinct expertise that benefits from independent reasoning before aggregation". Examples: a Chief Economist team; CRO sub-agents with different covariance estimators ([P] pp. 28–29).

## 8. Limitations stated by ANG (§5)

| Risk | Statement | Mitigation stated | Ref |
|---|---|---|---|
| Data leakage | LLMs encode outcomes unavailable at the decision date; the risk sits in the agentic layer (judge, interpretation, interaction) even when quantitative components are properly backtested | Point-in-time LLMs (smaller); retrieval of point-in-time evidence; homogenisation; obfuscation ("entity neutering"); evidence-only prompting. Do not eliminate leakage | [P] pp. 23–24; [L] s17–18 |
| Non-reproducibility | Identical calls differ | Prospective evaluation | [P] p. 24 |
| Correlated LLM errors | "LLM monoculture"; it "can convert apparent diversification across 21 methods into a single hidden bet"; the risk sits in the LLM-as-judge layer | Multiple foundation models; deterministic optimisers; robustness test with one model family per PC category | [P] pp. 24–25 |
| Model risk | Version drift breaks audit replay | Pinning; test battery; archives; deterministic anchor | [P] p. 25 |
| Automation surprise | Rubber-stamping | Readable memo; flagged deviations; recorded committee responses | [P] p. 25 |
| Governance | — | Hard vs soft; human at every consequential deviation | [P] p. 26 |
| Security | Tool-using, file-modifying agents | Sandboxing; privilege separation; auditor agents | [P] p. 26 |
| Evidence status of the run | "one realization of a stochastic system … not a backtest"; "not as evidence of outperformance"; the drawdown advantage is "largely mechanical" | — | [P] pp. 2, 14, 22 |

## 9. Illustrative run: facts recorded and arithmetic verified (not adopted)

**Run facts:**
- **Regime:** late-cycle, stagflation-tinged, medium-high confidence; recession probability 25–35% ([P] pp. 2, 16).
- **CMA judge (Exh. 6, p. 17):** custom blends. US Growth −2.0 pp vs auto-blend; US Large Cap −1.1; US Small Cap 0.0; EM and REITs −0.2.
- **Vote (Exh. 7, p. 18):** maximum diversification 1st, Black–Litterman 2nd; CVaR and Adversarial Diversifier at the bottom with "dissent reports".
- **CIO** ([P] p. 19): inverse-tracking-error ensemble.

  | Statistic | Value |
  |---|---|
  | Expected return | 6.87% |
  | Volatility | 7.54% |
  | Backtest Sharpe | 0.43 |
  | Effective N | 11.2 |
  | TE vs 60/40 | 2.41% |

  The ensemble rewards "centrality"; the Borda rank "measures peer respect", so the two "diverge" by design ([P] p. 21).
- **Final weights (Exh. 9, p. 22):** equity 44.9 / fixed income 41.7 / cash 8.1 / real assets 5.1.

**Verification** (`VERIFIED-DERIVATION` on published numbers; script in the Appendix):

| # | Check | Result |
|---|---|---|
| V-1 | Borda total = 21 voters × (5+4+3+2+1) − 21 × 2 | **273 = 273**. All 21 bottom flags fall on AdvDiv (18, matching p. 19) and CVaR (3) |
| V-3 | Composite = 0.4 · minmax(vote) + 0.6 · minmax(metric) | Reproduces Exh. 7 to ≤ 0.0011 (3-decimal rounding); rank order identical. **Confirms min–max normalisation** (ANG-09) |
| V-4 | Weight sums | Exh. 8 = 100.0%. Exh. 9 = 99.8% (rounding); categories 44.9 / 41.7 / 8.1 / 5.1; credit sleeve 6.5; intermediate + long Treasuries 23.1, all as in the text (p. 21); risk contributions sum to 99.8% |
| V-6 | "Effective number of assets 11.2 (Meucci 2009)" | **1/Σw² of Exh. 9 = 11.2 exactly.** exp(entropy) = 13.57. 60/40 → 1.92 ("≈ 2", fn. 8); EW-18 → 18. **ANG's measure is the inverse Herfindahl of weights**, not Meucci's effective number of bets. Resolves ANG-11 (definition); the citation is loose |
| V-7 | CMA judge constraint and Δ (Exh. 6) | All seven judge values lie within [min, max] of the methods shown; Judge − Auto = Δ in every row. The auto-blend ≠ equal-weighted mean of the five methods shown, consistent with confidence weighting plus the unshown survey method (ANG-03) |
| V-8 | CIO dimension weights | 25 + 15 + 15 + 20 + 15 + 10 = 100 |

## 10. Lecture cross-check (secondary; Oct 2026)

| Paper element | Lecture | Relation |
|---|---|---|
| Code computes, LLM judges (p. 36) | "Code for calculation, agents for judgement and reasoning"; "Context + skills > tools > AI model"; "Most of the effort is … the harness" (s13, s15) | **Agrees**; adds an emphasis on context and harness |
| AC agents + files (Exh. 2) | Same picture with `ig-corp.md`, `SKILL.md`, `script.py`, `analysis.md`; a 12-skill list (s27) | **Adds** skill names and `analysis.md` (ANG-26, ANG-27) |
| PC roster (Exh. 3) | Same; AdvDiv "Maximizes active risk relative to other PC agents subject to a SR constraint"; Researcher "Researches new portfolio construction methods that are not currently done" (s28–30) | **Agrees** (Sharpe definition still open, ANG-16) |
| Strategy review (pp. 10–13) | Candidate cards with 8 metrics; CRO report; 2 reviews *received* per candidate; vote JSON schema; regime-dependent blend "e.g., 40% … / 60% … in a late-cycle regime"; top-5 revise; "CIO Package" (s31 notes, s32) | **Adds** candidate cards (ANG-24), the vote output contract and the received-review framing (ANG-36). "Vote for two proposals" repeats Exh. 4 (ANG-01) |
| CIO (Exh. 5) | Macro + PC + CRO → CIO → SAA + board memo (s33) | **Agrees** |
| Meta agent (pp. 27–28) | "Every agent is updated from realized outcomes, and every change is tested before it ships" (s36); BARREL skill evolver deploys across all agents (s16) | **Adds** test-before-ship and global deployment (ANG-25; product lead only) |
| Limitations (§5) | Risks list identical (s38); masking example (s18); non-determinism demo (s20–21); autonomy vs verifiability table (s19) | **Agrees**; adds verifiability grading (RQ-55) |
| Scale | One agent per company; roles analyst/PM/risk/CIO (s34–35) | Direction of extension (security domain; ADR-0024 §4) |
| Data | "In-house: no new data or models to buy" (s40) | No vendor named in the lecture; the paper names FMP and Finviz (§5) |

## 11. Open items: unspecified and inconsistent elements

**Issues already registered:**
- ANG-01 … ANG-27 (`ANG_ISSUES_REGISTER.md`);
- ANG-11 is resolved by V-6 (definition = inverse HHI);
- ANG-09 is supported by V-3 (min–max normalisation, 40/60).

**New issues from this reconstruction** (added to the register; ANG-37 added at the S4.1 settlement, §13):

| ID | Type | Issue | Mat. | Stage |
|---|---|---|---|---|
| ANG-28 | US | The CMA judge skill is used "by every **equity** asset-class agent" (p. 37). Exh. 6 covers equities and REITs only. The method set and judgement rules for **fixed income, cash, gold and commodities** CMAs are not given (beyond "credit-spread duration and sector concentration", p. 9) | M | S4.15 → S9b |
| ANG-29 | II | Exh. A.1 step 2: "correlations vs **12** other asset classes", while the universe has 18 classes (17 others) | L | S4.15 |
| ANG-30 | II | Exh. 1 shows "Capital market assumptions" as an **input** box (with objectives and constraints) and no CIO or strategy-review box. §3.1 has AC agents produce CMAs and a CIO step. Reading: diagram simplification; CMAs may also be externally sourced (p. 5) | M | S4.2 |
| ANG-31 | US | The meta agent is said to evaluate "the portfolio methodologies of the PC agents" (p. 27), but the listed feedback metrics cover macro and AC outputs only. There are **no PC-method, review/vote or CIO-ensemble learning metrics** | M | S4.3 (objects) → S17 |
| ANG-32 | US | "dissent reports" are triggered for bottom-voted methods (p. 18). Trigger rule, content and consumer (CIO? memo?) are unspecified | L/M | S4.17 → S12 |
| ANG-33 | US | **Two volatility sources:** the AC agents' volatility estimate (CMA, p. 6) and the covariance agent's Σ (p. 6). Which one PC agents and the CRO use, whether diag(Σ) must equal the CMA volatilities, and the horizon/units consistency with "3-year nominal" CMAs (Exh. 6) are unspecified | **H** | S4.13 → S10 |
| ANG-34 | US | Data provenance: FMP and Finviz via `apex-data-financial` and web search (pp. 7, 38). Point-in-time handling and the "proprietary" look-ahead techniques are undisclosed (pp. 2, 14–15, 24) | M | S6 |
| ANG-35 | II | "four to six methods per category" (p. 9) vs Exh. 3 counts 5/5/5/4 (+2 agentic) | L | S4.4 |
| ANG-36 | US | Paper: each agent *reviews* two peers (p. 11). Lecture: each candidate *receives* two reviews (s31 notes). Both ⇒ a balanced 2-in/2-out design. With category E of size 2, the intra-category review is forced (Researcher ↔ AdvDiv) [I]. The assignment algorithm is unspecified (cf. the third-party self-assignment defect, `S4_GITHUB_IMPL_REVIEW.md`) | M | S4.17 → S12 |
| ANG-37 | US | **Learning × correlated errors.** ANG never addresses whether self-learning (global skill deployment, common lessons, performance culling, an LLM editing LLM agents) homogenises agents and erodes the diversity its own CIO logic relies on (p. 20; pp. 24–25 vs pp. 27–28; s16). See §13.1 | **H** | S4.2, S4.3 → S8, S17 |

## 12. S4.1 exit checklist (S4_PLAN §G row S4.1)

| Required element | Where |
|---|---|
| Roles; order; data flows | §2, §2.1, §2.2, §3 |
| CMA | §2.1 S2; §4 (judge skill) |
| Covariance | §2.1 S3; ANG-33 |
| PC (incl. Researcher, AdvDiv) | §2.1 S4; §3 |
| CRO; review; voting; revision | §2.1 S5a–S5e |
| CIO | §2.1 S6; §7 (memo) |
| Meta | §2.1 M |
| IPS governance | §7 |
| Determinism boundaries | §4, §6 |
| Limitations | §8 |
| Inconsistencies | §0.3, §11; register |
| Lecture cross-check (ANG-24 … ANG-27) | §10 |

**Handoff (SYNC-1, with S4.2):** the stage table §2.1 and the open items §11 are the developer-facing input. S4.2 classifies every element (adopted / generalised / adapted / deferred / N/A) and resolves or escalates C-1 … C-10.

## 13. S4.1 settlement: owner questions of 2026-10-08

### 13.1 Learning in ANG: verified, and its tension with correlated errors

**Learning is a core pillar of ANG** (`VERIFIED-SOURCE`).
- **In the paper:**
  - Abstract (p. 0): a meta agent "compares past forecasts against realized returns and rewrites agent code and prompts to improve future performance".
  - p. 2: "Our agentic architecture also allows agents to learn and acquire new skills".
  - Conclusion (p. 29): the meta agent "closes the feedback loop between prediction and realized outcomes so that agents can learn".
- **In the lecture:** SELF-LEARNING is one of the three things "really new", alongside SCALE and PRODUCTIVE DISSENT (s12, s26; also s16, s36).

**ANG has two learning loops:**
1. **Forecast learning (meta agent, pp. 27–28).**
   - Macro and AC estimates are scored against outcomes over a rolling 3-year window.
   - Skills, prompts and code are edited, with human approval above a materiality threshold.
2. **Method-registry evolution.**
   - "as the agents discover and evaluate new PC methods, and decommission other PC approaches, the size and type of the PC registry will become endogenous" (fn. 4 p. 9).
   - "successful new PC methods will be added … a portfolio review process can also cull unsuccessful PC methods" (p. 10).
   - The forecasts to be evaluated include "the portfolio methodologies of the PC agents" (p. 27).
   - **But no PC-method evaluation metric is given** (ANG-31). The paper also concedes that "because of the long horizons required for SAA evaluations, it will take some time before we can evaluate whether the meta agent's modifications genuinely improve out-of-sample performance" (p. 28).

**Does learning conflict with agent correlation?** **Yes, potentially. ANG does not address the interaction (new ANG-37).** Four mechanisms can homogenise the agents:

| # | Mechanism | Effect |
|---|---|---|
| (a) | **Global deployment:** the lecture's skill evolver "deploys the improved skill across all agents" (s16) | All agents share the same updated instructions, raising error correlation |
| (b) | **Common lessons:** every agent learns from the same outcome history | Agents converge on the same lessons |
| (c) | **Performance culling:** "cull unsuccessful PC methods" | Shrinks the method set toward recent winners. This contradicts ANG's own CIO logic, which values centrality and the orthogonal Adversarial Diversifier and appeals to boosting, where the ensemble gains "precisely from learners that make forecasting errors in uncorrelated dimensions" (p. 20) |
| (d) | **An LLM meta agent editing other LLM agents** | Judge = author risk (self-preference; RQ-56) |

**Quantified** (L-1, `VERIFIED-DERIVATION`, the standard equicorrelation result): N agents whose errors have pairwise correlation ρ behave like N_eff = N / (1 + (N−1)ρ) independent agents. For 21 agents:

| ρ | 0.0 | 0.1 | 0.3 | 0.6 | 0.9 |
|---|---|---|---|---|---|
| N_eff | 21.0 | 7.0 | 3.0 | 1.62 | 1.11 |

Learning that raises ρ from 0.1 to 0.3 cuts the effective ensemble from 7 to 3. The statistical power to learn is also low (D9, D10: hit-rate SE 0.144 with 12 quarterly observations), so performance-driven culling largely selects on noise (D7: the best of 50 null strategies over 5 years has Sharpe ≈ 1.0).

**Determination (`INFERENCE`; proposed as S4.2 classification "ADOPTED with guardrails"):** learning and diversity are complementary *if* diversity is a learning constraint, not an afterthought. Candidate design rules for S4.3/S8/S17:

| Rule | Content |
|---|---|
| L-1 | **Separate learning targets.** Forecast-model parameters, CMA-method weights and method eligibility are learned in **code** under pre-registered statistics. Prompts and skills change only through the gated path |
| L-2 | **PC methods are evaluated deterministically** (S7 protocol: net-of-cost, IR vs control, drawdown, turnover, CRO diagnostics) over **minimum horizons fixed in advance**. Evaluation informs CIO weighting (ADR-0025 axis); **it never auto-culls**. Retirement requires failing admission criteria or pre-registered evidence thresholds with multiple-testing control (D7) |
| L-3 | **Diversity floor.** Learning may never reduce coverage below a family floor. This generalises ANG's own "≥ 3 of 5 families" rule (p. 12) from the shortlist to the registry |
| L-4 | **Correlation as a promotion guardrail.** A change is promoted only if measured cross-agent error correlation (M6) and proposal dispersion do not deteriorate beyond a pre-set margin |
| L-5 | **Per-role, not global, deployment** of learned skills. Champion/challenger shadow runs before promotion (S4_INPUTS §4.5) |
| L-6 | **Judge ≠ author.** The meta agent proposes; a deterministic test battery plus a human decides (ADR-0026 §4.4; ANG pp. 27–28) |
| L-7 | **Clean-window rule.** Only post-cutoff outcomes count as learning signals (`S4_LIT_LOOKAHEAD_2026-10-07.md` §2.4) |

### 13.2 Volatility and covariance: what ANG specifies, and what it does not

**What ANG specifies** (`VERIFIED-SOURCE`):

| Element | Statement | Ref |
|---|---|---|
| Covariance agent | "estimates the asset class covariance matrix using historical data and macro forecasts". **No estimator, window, frequency, shrinkage or horizon is given** | p. 6; Exh. 1 says "Covariance Agents" |
| AC agents | Output "a volatility estimate" with the CMA; `historical_stats.json` carries trailing volatility; **each AC agent also writes `correlation_row.json`** ("correlations vs 12 other asset classes", ANG-29) | p. 6; p. 39; Exh. A.1 p. 38 |
| CRO | Reports "ex-ante and backtest volatility, value-at-risk, maximum drawdown" | p. 10 |
| Decomposition hint | CRO sub-agents for "short-horizon versus long-horizon volatility (each using different covariance estimators produced by yet further agents)" | p. 29 |

So ANG has **three** potential risk inputs: AC volatilities, AC correlation rows and the covariance agent's Σ. How they are reconciled is unspecified (ANG-33, raised to cover the correlation rows).

**A matrix assembled from separately estimated rows** (different windows or samples) need not be symmetric or positive semi-definite. It would need projection to the nearest correlation matrix (Higham 2002, `CANDIDATE SOURCE`) before any optimiser uses it.

**Our position:**
- The correlation or covariance estimator is a **Method Library entry** (COV-x) with its own eligibility contract (06 §4 RMT example: q = N/T plus a minimum N). PC methods declare their Σ dependency (S4.13 → S10; RQ-14).
- **Candidates** (inventory S4.0 §6, extended):

  | Family | Estimators |
  |---|---|
  | Static | Sample over a fixed or rolling window |
  | Exponentially weighted | EWMA (RiskMetrics 1996) |
  | Linear shrinkage | Ledoit–Wolf 2003/2004, **including correlation-only and constant-correlation targets** (Elton & Gruber 1973) |
  | Nonlinear shrinkage | Ledoit–Wolf 2017 |
  | RMT cleaning | Laloux et al.; Bun–Bouchaud–Potters 2017 |
  | Factor models | — |
  | Dynamic GARCH-type | CCC-GARCH (Bollerslev 1990), DCC (Engle 2002), cDCC (Aielli 2013) |

**Evidence computed now** (synthetic; one stylised DGP: 17 asset classes, block correlations, volatilities 2–21%, Gaussian i.i.d., 200 simulations; Appendix B, seed 20261008; **illustrative, not adopted**):

Each cell is out-of-sample GMV variance divided by the true minimum.

| Months T | Long-only: sample | LW-identity | LW-correlation | CC-0.5 | Unconstrained: sample | LW-identity | LW-correlation | CC-0.5 |
|---|---|---|---|---|---|---|---|---|
| 36 | 1.059 | **3.286** | 1.054 | 1.043 | 1.82 | **10.74** | 1.64 | 1.92 |
| 60 | 1.049 | 2.445 | 1.044 | 1.041 | 1.40 | 7.05 | 1.42 | 1.83 |
| 120 | 1.023 | 1.578 | 1.021 | 1.043 | 1.15 | 3.83 | 1.23 | 1.75 |

**Findings (C-1b):**
1. **Target choice matters more than whether to shrink.** Shrinking toward a scaled identity equalises variances across asset classes with heterogeneous volatility and is harmful throughout. Correlation-only shrinkage preserves the volatilities.
2. **The long-only constraint already regularises** (consistent with Jagannathan & Ma 2003). For long-only GMV, all reasonable estimators are within 2–6% of the oracle; for unconstrained GMV, estimation error costs 15–82% and correlation shrinkage helps at short T.
3. **Fixed shrinkage intensity misfires as T grows** (CC-0.5 at T = 120). Intensity must be data-driven.

So estimator choice is **method- and constraint-dependent**, which supports the per-method Σ-dependency contract in S4.13.

**Dynamic models (C-2, `VERIFIED-DERIVATION`):**
- For a GARCH(1,1)-type variance with persistence φ, the share of today's variance deviation that survives in the average forecast over H periods is (1 − φ^H) / ((1 − φ)H).
- At daily φ = 0.98: 0.82 over 1 month, 0.20 over 1 year, **0.066 over 3 years**.
- So conditional-volatility dynamics barely move a **3-year SAA** covariance. They matter for **short-horizon** uses: CRO risk reports, volatility targeting (PC-A5), monitoring and Trader timing evidence.
- This matches ANG's own short- vs long-horizon split (p. 29). Horizon must be a declared field of every Σ (ADR-0026 §8 descriptor horizon).

### 13.3 RMT cleaning and universe size (owner question, 2026-10-08, second round)

**Question:** "What about the RMT-cleaned risk model based on the number of assets included?"

**Mechanism** (`VERIFIED-DERIVATION`; closed form plus the spectra below):
- Eigenvalue clipping (Laloux et al. 1999, `CANDIDATE SOURCE`) keeps the eigenvalues of the sample correlation matrix above the Marchenko–Pastur edge λ+ = (1 + √q)², q = N/T. It replaces all others by their average (trace preserving).
- This is close to ideal when the true spectrum is **a few large factors plus a flat bulk**: the clipped bulk is then pure noise.
- It is **harmful when genuine eigenvalues lie below the edge**. Clipping lifts real low-variance directions (e.g. near-collinear bond maturities), which minimum-variance-type methods exploit.
- The edge is a pure-noise null. It cannot tell a small genuine eigenvalue from noise, and at small N there are too few eigenvalues for the bulk to be estimated (06 §4).

**True spectra of the two synthetic designs** (Appendix C):

| Design | True correlation eigenvalues | Above λ+ at T = 60 / 120 / 250 |
|---|---|---|
| 17 asset classes (Appendix B design) | 6.92, 4.22, 1.11, 0.99, 0.82, 0.60, 0.40, 0.40, 0.20 (×6), 0.15, 0.15, **0.02** | 2 / 2 / 2 (λ+ = 2.35 / 1.89 / 1.59) |
| 100 stocks (market + 8 sectors; one draw) | 38.06; 3.07 … 0.78 (eight sector eigenvalues); bulk of 91 in [0.20, 0.77] | spiked-bulk shape, which RMT is designed for |

In population terms, clipping in the asset-class design replaces 15 eigenvalues (1.11 down to 0.02) by their mean of about 0.39. The 0.02 and 0.15 directions are real hedges, and they are lost.

**Simulation R-1** (synthetic; Gaussian i.i.d.; monthly; 100 simulations per cell; seed 20261008; Appendix C; **illustrative, not adopted**). Unconstrained GMV; each cell is out-of-sample variance divided by the true-GMV variance:

| Universe | T (months) | q = N/T | Sample | LW-correlation | RMT clipping | Eigenvalues kept (mean) |
|---|---|---|---|---|---|---|
| 17 asset classes | 60 | 0.28 | **1.39** | 1.42 | 1.89 | 2.0 |
| 17 asset classes | 120 | 0.14 | **1.16** | 1.23 | 1.83 | 2.0 |
| 17 asset classes | 250 | 0.07 | **1.07** | 1.12 | 1.77 | 2.0 |
| 50 stocks | 60 | 0.83 | 6.44 | 1.70 | **1.44** | 1.0 |
| 50 stocks | 120 | 0.42 | 1.67 | 1.42 | **1.30** | 1.0 |
| 50 stocks | 250 | 0.20 | 1.25 | **1.21** | 1.24 | 1.1 |
| 100 stocks | 60 | 1.67 | singular | 1.96 | **1.65** | 1.1 |
| 100 stocks | 120 | 0.83 | 5.95 | 1.93 | **1.43** | 1.8 |
| 100 stocks | 250 | 0.40 | 1.67 | 1.51 | **1.33** | 3.4 |
| 300 stocks | 60 | 5.00 | singular | 2.39 | **2.20** | 2.1 |
| 300 stocks | 120 | 2.50 | singular | 1.93 | **1.51** | 3.9 |
| 300 stocks | 250 | 1.20 | singular | 2.63 | **1.26** | 7.1 |

**Simulation R-2** (same stock design; 100 stocks; long-only, maximum weight 10%; 40 simulations):

| T | q | Sample | LW-correlation | RMT clipping |
|---|---|---|---|---|
| 120 | 0.83 | 1.125 | 1.120 | 1.120 |
| 250 | 0.40 | 1.060 | 1.058 | 1.069 |

**Findings (R-1, R-2):**
1. **The same estimator is the worst choice in one problem and the best in another.** At the asset-class level (N = 17) RMT clipping was the worst estimator at every T (1.77–1.89× vs 1.07–1.39× for the sample matrix). For 100–300 stocks it was the best in every cell. At N = 50, T = 250 the three are within 0.04.
2. **Dimension alone is not the criterion; spectrum shape matters too.** The asset-class failure is not only "N is small". The design has genuine eigenvalues far below the edge. This refines 06 §4: the eligibility contract needs N, q_eff **and** a spectrum or structure diagnostic. The exact form is an S10 question.
3. **Some cleaning is mandatory once T ≤ N.** The sample matrix is then singular, and unconstrained methods cannot run on it (300 stocks at T = 250 months is already q > 1).
4. **Constraints again neutralise most differences** (R-2: all within 1.06–1.13×; differences ≤ 0.011, standard errors not computed). This matches §13.2 finding 2 and Jagannathan & Ma (2003).
5. **Unexplained result, recorded rather than smoothed over:** LW-correlation at N = 300 is worse at T = 250 (2.63) than at T = 120 (1.93). A plausible cause is the intensity estimate near q ≈ 1 with an identity target that ignores the market factor. This has not been investigated.

**Implications:**
- **Asset-class level** (ANG's level; roster v0): RMT clipping is **not supported** by this evidence. Sample or correlation-shrinkage estimators (§13.2) remain the candidates.
- **Security level** (Sørensen scoring → security-level EPO, `S4_SCORING_SORENSEN.md` O-9c; any unconstrained or weakly constrained stock-level method): RMT cleaning or nonlinear shrinkage (LW 2017) are leading candidates. Some cleaning is required when T ≤ N.
- This is direct evidence that the risk model must be chosen **per problem** (universe, dimension, horizon), not once for everything: the same estimator is best for one universe and worst for another (ADR-0027 D3 r3, Option A; `S4_RISK_MODEL_CHOICE.md`).

**Caveats:**
- one design per level;
- Gaussian, i.i.d. and stationary returns (no heavy tails, volatility clustering or regime change);
- GMV only (no μ);
- the stock design is exactly the spiked model RMT is built for, which favours RMT;
- linear shrinkage is represented by one target only (identity on correlations). LW 2003 single-factor and constant-correlation targets, LW 2017 nonlinear shrinkage, Bun–Bouchaud–Potters rotationally invariant estimators, EWMA and effective-T effects are **not** in this run.

All of these belong to the S10 design (RQ-14). **No threshold is set.**

## Appendix — verification script (published numbers; reproduces V-1, V-3, V-4, V-6)

```python
import numpy as np
vote = np.array([96,76,42,41,22,22,5,3,1,4,3,0,0,0,0,0,0,0,0,-6,-36], float)
metric = np.array([.553,.551,.503,.497,.510,.479,.468,.468,.459,.438,.406,.407,.406,.365,.362,.359,.355,.304,.253,.239,.205])
comp = np.array([1,.936,.750,.737,.702,.648,.578,.572,.549,.522,.464,.457,.456,.386,.380,.375,.368,.280,.191,.150,0])
mm = lambda x: (x - x.min()) / (x.max() - x.min())
assert vote.sum() == 21*15 - 21*2                                   # V-1
assert np.abs(.4*mm(vote) + .6*mm(metric) - comp).max() < 0.0015    # V-3
w9 = np.array([15.9,14.7,8.9,8.4,8.1,7.3,7.2,4.9,4.8,4.4,3.6,2.4,2.1,1.6,1.6,1.4,1.3,1.2]); p = w9 / w9.sum()
print(round(1/np.sum(p**2), 1), round(np.exp(-np.sum(p*np.log(p))), 2))  # V-6: 11.2 (inverse HHI) vs 13.57
```

## Appendix B — covariance-estimator simulation (synthetic; reproduces the §13.2 table)

```python
import numpy as np, warnings; from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
vol=np.array([.16,.20,.16,.19,.17,.21,.02,.05,.12,.07,.10,.08,.07,.11,.19,.15,.20])   # 6 EQ, 8 FI, REIT, gold, commodities
g=['E']*6+['T','T','T','C','H','S','C','M','R','G','K']
def rho(a,b):
    if a==b: return {'E':.80,'T':.85,'C':.80}.get(a,.6)
    s={a,b}
    if s<={'E','R','H','M'}: return .60
    if 'E' in s and s&{'T','S'}: return -.10
    if 'E' in s and 'C' in s: return .30
    if s<={'T','S','C'}: return .55
    return .05 if 'G' in s else (.25 if 'K' in s else .20)
N=17; R=np.array([[1 if i==j else rho(g[i],g[j]) for j in range(N)] for i in range(N)])
e,V=np.linalg.eigh(R); R=V@np.diag(np.clip(e,1e-3,None))@V.T; d=np.sqrt(np.diag(R)); R/=np.outer(d,d); Sig=np.outer(vol,vol)*R/12
def lw(X):                                   # Ledoit-Wolf (2004), scaled-identity target
    T,n=X.shape; Xc=X-X.mean(0); S=Xc.T@Xc/T; m=np.trace(S)/n; d2=np.sum((S-m*np.eye(n))**2)/n
    b2=min(sum(np.sum((np.outer(x,x)-S)**2) for x in Xc)/n/T**2,d2); return (b2/d2)*m*np.eye(n)+((d2-b2)/d2)*S
def lw_corr(X):                              # LW on standardised data -> shrunk correlation, sample vols kept
    s=X.std(0); C=lw((X-X.mean(0))/s); d=np.sqrt(np.diag(C)); return np.outer(s,s)*C/np.outer(d,d)
def cc(X,k=.5):                              # fixed 50% shrink of correlation toward constant correlation
    S=np.cov(X,rowvar=False,bias=True); s=np.sqrt(np.diag(S)); Rs=S/np.outer(s,s); rb=(Rs.sum()-N)/(N*(N-1))
    Rc=np.full((N,N),rb); np.fill_diagonal(Rc,1); return np.outer(s,s)*((1-k)*Rs+k*Rc)
def lo(S): return minimize(lambda w:w@S@w,np.ones(N)/N,jac=lambda w:2*S@w,bounds=[(0,1)]*N,
           constraints=[{'type':'eq','fun':lambda w:w.sum()-1}],method='SLSQP',options={'maxiter':500,'ftol':1e-14}).x
def un(S): x=np.linalg.solve(S,np.ones(N)); return x/x.sum()
rng=np.random.default_rng(20261008); a=lo(Sig); va=a@Sig@a; b=un(Sig); vb=b@Sig@b
E={'sample':lambda X:np.cov(X,rowvar=False,bias=True),'LW-identity':lw,'LW-corr':lw_corr,'CC-0.5':cc}
for T in (36,60,120):
    L={k:[] for k in E}; U={k:[] for k in E}
    for _ in range(200):
        X=rng.multivariate_normal(np.zeros(N),Sig,T)
        for k,f in E.items(): S=f(X); w=lo(S); v=un(S); L[k].append(w@Sig@w/va); U[k].append(v@Sig@v/vb)
    print(T,{k:round(np.mean(x),3) for k,x in L.items()},{k:round(np.mean(x),2) for k,x in U.items()})
```

## Appendix C — RMT cleaning by universe size (synthetic; reproduces the §13.3 tables and spectra)

Run time is about 40 s. Output order: R-1 rows, R-2 rows, then the two spectra.

```python
import numpy as np, warnings; from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
rng=np.random.default_rng(20261008)
def lw_target_identity(Z):                      # LW(2004) on standardised data (correlation shrinkage toward I)
    T,n=Z.shape; Zc=Z-Z.mean(0); S=Zc.T@Zc/T; m=np.trace(S)/n; d2=np.sum((S-m*np.eye(n))**2)/n
    b2=min(sum(np.sum((np.outer(x,x)-S)**2) for x in Zc)/n/T**2,d2); return (b2/d2)*m*np.eye(n)+((d2-b2)/d2)*S
def to_cov(C,s): d=np.sqrt(np.diag(C)); return np.outer(s,s)*C/np.outer(d,d)
def est_sample(X): return np.cov(X,rowvar=False,bias=True)
def est_lwcorr(X): s=X.std(0); return to_cov(lw_target_identity((X-X.mean(0))/s),s)
def est_rmt(X):                                 # Laloux et al. eigenvalue clipping, trace preserving
    T,n=X.shape; s=X.std(0); C=np.corrcoef(X,rowvar=False); q=n/T; lp=(1+np.sqrt(q))**2
    w,V=np.linalg.eigh(C); noise=w<lp
    if noise.sum()>0: w=w.copy(); w[noise]=w[noise].mean()
    Cc=V@np.diag(w)@V.T; return to_cov(Cc,s)
def gmv_u(S):
    try: x=np.linalg.solve(S,np.ones(len(S)))
    except np.linalg.LinAlgError: return None
    return x/x.sum()
def factor_corr(n,k=8):                         # stock universe: market + k sectors, heterogeneous loadings
    bm=rng.uniform(.4,.8,n); sec=rng.integers(0,k,n); bs=rng.uniform(.2,.5,n)
    F=np.zeros((n,k)); F[np.arange(n),sec]=bs; L=np.column_stack([bm,F]); C=L@L.T; np.fill_diagonal(C,1)
    return C
def asset_class_corr():                         # 17 asset classes (as in Appendix B)
    g=['E']*6+['T','T','T','C','H','S','C','M','R','G','K']
    def rho(a,b):
        if a==b: return {'E':.80,'T':.85,'C':.80}.get(a,.6)
        s={a,b}
        if s<={'E','R','H','M'}: return .60
        if 'E' in s and s&{'T','S'}: return -.10
        if 'E' in s and 'C' in s: return .30
        if s<={'T','S','C'}: return .55
        return .05 if 'G' in s else (.25 if 'K' in s else .20)
    R=np.array([[1 if i==j else rho(g[i],g[j]) for j in range(17)] for i in range(17)])
    e,V=np.linalg.eigh(R); R=V@np.diag(np.clip(e,1e-3,None))@V.T; d=np.sqrt(np.diag(R)); return R/np.outer(d,d)
# R-1: unconstrained GMV
cases=[("17 asset classes",asset_class_corr(),np.array([.16,.20,.16,.19,.17,.21,.02,.05,.12,.07,.10,.08,.07,.11,.19,.15,.20]))]
for n in (50,100,300): cases.append((f"{n} stocks",factor_corr(n),rng.uniform(.18,.45,n)))
est={'sample':est_sample,'LW-corr':est_lwcorr,'RMT-clip':est_rmt}
for name,C,vol in cases:
    n=len(vol); Sig=np.outer(vol,vol)*C/12; w0=gmv_u(Sig); v0=w0@Sig@w0
    for T in (60,120,250):
        out={k:[] for k in est}; nclip=[]
        for _ in range(100):
            X=rng.multivariate_normal(np.zeros(n),Sig,T)
            for k,f in est.items():
                if k=='sample' and T<=n: continue
                w=gmv_u(f(X))
                if w is not None: out[k].append(w@Sig@w/v0)
            nclip.append((np.linalg.eigvalsh(np.corrcoef(X,rowvar=False))>=(1+np.sqrt(n/T))**2).sum())
        print(name,T,round(n/T,2),{k:(round(np.mean(v),2) if v else 'singular') for k,v in out.items()},'kept',np.mean(nclip))
# R-2: long-only GMV, max weight 10%, 100 stocks (re-seeded)
def lo(S):
    n=len(S); return minimize(lambda w:w@S@w,np.ones(n)/n,jac=lambda w:2*S@w,bounds=[(0,.10)]*n,
        constraints=[{'type':'eq','fun':lambda w:w.sum()-1}],method='SLSQP',options={'maxiter':300,'ftol':1e-12}).x
rng=np.random.default_rng(20261008)
n=100; C=factor_corr(n); vol=rng.uniform(.18,.45,n); Sig=np.outer(vol,vol)*C/12; w0=lo(Sig); v0=w0@Sig@w0
for T in (120,250):
    out={k:[] for k in est}
    for _ in range(40):
        X=rng.multivariate_normal(np.zeros(n),Sig,T)
        for k,f in est.items(): w=lo(f(X)); out[k].append(w@Sig@w/v0)
    print('R-2',T,round(n/T,2),{k:round(np.mean(v),3) for k,v in out.items()})
# Mechanism: true correlation spectra (re-seeded draw of the stock DGP)
print('17-class spectrum',np.round(np.sort(np.linalg.eigvalsh(asset_class_corr()))[::-1],2))
rng=np.random.default_rng(20261008); f=np.sort(np.linalg.eigvalsh(factor_corr(100)))[::-1]
print('100-stock spectrum: top 9',np.round(f[:9],2),'bulk range',np.round((f[9:].min(),f[9:].max()),2))
```
