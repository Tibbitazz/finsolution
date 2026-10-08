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

**New issues from this reconstruction** (added to the register):

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
