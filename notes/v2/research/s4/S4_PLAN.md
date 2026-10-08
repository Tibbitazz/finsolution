# S4 plan — Method Library & Eligibility (ANG baseline)

**Status:** APPROVED IN PRINCIPLE by the owner, 2026-10-02, with amendments incorporated below. Execution: S4.0 done (awaiting review); S4.1 drafted and settled 2026-10-08 (`S4_ANG_BASELINE.md`); S4.2 drafted 2026-10-08 (`S4_ANG_ADAPTATION.md`, ADR-0027 PROPOSED; awaiting owner review). ADR basis: ADR-0023, ADR-0024, ADR-0025, ADR-0026 (accepted; ADR-0025 on 2026-10-07, ADR-0026 on 2026-10-08). **Amended 2026-10-02** (amendments 11–13: accountability layer, source authority, TPA source assessment; owner approval of T-0 … T-8). **Amended 2026-10-07** (amendment 14: ABD 2014 obtained; TPA task restated; owner decision D-5; amendment 15: lecture and sandbox inputs, agentic learning as priority, correlated agent errors; `S4_INPUTS_2026-10-07.md`; amendment 16: third-party implementation review; `S4_GITHUB_IMPL_REVIEW.md`; amendment 17: Sørensen/Storebrand scoring as the owner-designated reference specification; `S4_SCORING_SORENSEN.md`; amendment 18: look-ahead contamination and agent-homogeneity literature; `S4_LIT_LOOKAHEAD_2026-10-07.md`).
**Basis:** owner instruction of 2026-10-02; full re-read of ANG (version 21 Sep 2026, 40 pp, read in full by text extraction; Exhibits 1, 2, 4 and 5 extracted as images and inspected); accepted S0–S3 (G0–G3).
**Page numbers:** printed page numbers of the paper (PDF page − 1).

**Central principle:** ANG defines the baseline agentic investment-process architecture. S4 builds and verifies the mathematical repertoire that operates inside it. It extends ANG where justified (Simple/Anchored EPO, momentum) and must never collapse it into `user → optimizer → portfolio`.

---

## 0. Decision record (owner, 2026-10-02)

| # | Decision | Record |
|---|---|---|
| OD-1 | **Approved, strengthened.** ANG's principal functional roles are the baseline. The 05 "if retained" wording never permits collapsing PC → CRO → deliberation → CIO into optimizer selection. Architectural role ≠ runtime implementation (agent, agents, code, human or hybrid). Functional separation and authority boundaries are what must be preserved. R2 deterministic/privacy mode stays | ADR-0023 |
| OD-2 | **Approved.** Research lane `DISCOVERED → RESEARCH CANDIDATE → SPECIFIED → VERIFIED → ADMISSIBILITY REVIEW → ADMITTED`. Experimental runs and research peer review allowed; no production CIO allocation until admitted | ADR-0024 §1 |
| OD-3 | **Modified.** Revisions limited to six categories. No LLM edits of weights. No opportunistic tuning. Parameter classes: fixed / system-estimated / user-authorized / agent-selectable / sensitivity-only. Reason recorded for every revised run | ADR-0024 §2–3 |
| OD-4 | **Modified substantially.** Methodological admission (S4) ≠ empirical evaluation (S7) ≠ integrated validation (S15). No performance prerequisite for admission. The ANG pipeline is not disabled before S7. The app is not called "production validated" before S15. Methodological admission ≠ CIO weighting/selection evidence. **Conflicts with accepted 06 §1 / 02 §D definitions of ADMISSIBLE**, so carried by ADR-0025 (PROPOSED) | ADR-0025 |
| OD-5 | **Approved, qualified.** Python verification area separate from production code. Package availability does not shape the production architecture | ADR-0024 §8 |
| OD-6 | **Approved.** ANG-baseline ADR distinguishing adopted architecture from illustrative choices | ADR-0023 §8 |
| OD-7 | **Approved, generalized.** Contracts declare allocation domains (asset class · fund/ETF · security · strategy/sleeve · portfolio of portfolios). S5 decides | ADR-0024 §4 |

**Amendments incorporated:**
1. **ANG interpretation/issues register:** `ANG_ISSUES_REGISTER.md`.
2. **Source gaps in S4.0, kept in separate status classes:** `S4_0_SOURCE_INVENTORY.md`.
3. **EPO hierarchy:** MVO → EPO framework → Simple EPO → Anchored EPO, confirmed for current scope; no aliases of UEPO/SEPO/DEPO.
4. **Momentum roles open until S4.8/S4.9:** possible objects are signal · signal-conditioned universe · direction/exposure rule · expected-return mapping · standalone strategy · tactical overlay.
5. **Portfolio Map broadened** (§J).
6. **PC roster versioned and extensible.** Reference baseline is ANG's 21; the initial S4 baseline is 23 (+ Simple EPO, Anchored EPO).
7. **Method / Method Contract / Agent Role / Agent Instance / Portfolio Proposal** kept distinct; extended by ADR-0026 (ACCEPTED 2026-10-08) with **Agent Mandate** and **Decision Record**.
8. **Separation of stages:** method output → proposal → CRO → peer assessment → revision → CIO kept separate in contracts; the peer vote is not a weighting algorithm.
9. **No ANG rankings or ensemble weights** as priors or defaults.
10. **Dual (machine + agent-readable) Method Contracts.**
11. **Accountability layer (owner D-A … D-E, 2026-10-02; ADR-0026 ACCEPTED 2026-10-08).**
    - The NBIM review (Bauer, Christiansen & Døskeland 2022) is used as an accountability framework *around* ANG.
    - Investment decision ≠ deterministic rebalancing determination ≠ hybrid Trader discretion ≠ deterministic execution.
    - The approved decision carries the implementation parameters.
    - No standalone Technical Agent in v0.
    - Traceability ≠ attribution; no container categories.
    - Work items: S4.2b, S4.15b and the field additions in S4.3, S4.16–S4.22.
12. **Source authority and selectivity** (§E.1–E.2). S4 becomes more selective as research progresses, not merely larger.
13. **TPA source assessment.** ABD 2014 is not yet obtained. AQR (2026) cannot replace it as ANG's cited source, but can serve as a specification lead for a separately labelled TPA-family candidate, under conditions ([S4_0_ACQUISITION_CHECKLIST.md](S4_0_ACQUISITION_CHECKLIST.md), Addendum A.3).
14. **ABD obtained; TPA task restated (owner approval of the five ABD edits and decision D-5, 2026-10-07).**
    - ABD 2014 is AVAILABLE (identity verified). Its TPA is a funding/benchmarking framework with no weight rule (ANG-22; ABD-1 … ABD-5).
    - **D-5:** AQR (2026) may substitute for ABD as the specification source for how TPA becomes weights, where it is more informative.
    - S4.12 now specifies our own TPA-family candidate plus a distinctness test (below).
    - ABD [SRC] citations added to ADR-0026 §4.1, §5.1, §5.3 (pre-acceptance).
    - RQ-52 and RQ-54 carry the ABD-derived candidate refinements.
15. **Lecture and sandbox inputs; learning first; correlated errors (owner approval of plan A, 2026-10-07).** Substance in [S4_INPUTS_2026-10-07.md](S4_INPUTS_2026-10-07.md).
    - Paper v2 governs; the lecture is secondary; third-party code is reused only where verified.
    - **Agentic learning is a first-class component** (owner priority): learning objects in S4.3, capture from day one (S8), per-role promotion with a diversity check; RQ-22 split.
    - New RQ-55 (verifiability and stability) and RQ-56 (correlated agent errors). Proposed CB-17 … CB-19.
    - Field candidates for S4.20. Developer requirements DR-1 … DR-8 (§I). G4 criterion 24.
    - Sandbox-specific choices are explicitly not transferred (memo §7).
16. **Third-party implementation review (owner request, 2026-10-07).** [S4_GITHUB_IMPL_REVIEW.md](S4_GITHUB_IMPL_REVIEW.md) gives a per-component verdict (ADOPT / ADOPT-WITH-FIX / REJECT / OUT OF ROSTER), the IPS-constraint mathematics, invariants I-1 … I-9 for S4.23/S4.24/S8, and port-and-verify code candidates (MIT). No method is adopted by this review; S4.5–S4.14 specify each method from its primary source.
17. **Sørensen/Storebrand scoring (owner instruction, 2026-10-07).** [S4_SCORING_SORENSEN.md](S4_SCORING_SORENSEN.md) records the method as the **reference specification** for cross-sectional value and momentum scores in the individual-security domain.
    - Value: global z(−P/E), z(−P/B), equal-weight sum, then percentile 0–100. Momentum: 12–1 percentile.
    - Verified properties: P-1 … P-5.
    - Open choices O-1 … O-10 are declared parameters; V0 = exact source (reproduction oracle); V1 = corrected variant proposed.
    - Not a μ mapping (ADR-0012 §3); no master composite; no roster change (roster v0 = 23 confirmed by the owner).
    - Work: S4.20 contract stub, S4.24 fixture, S7 grid, S6 data, S9c → G9.
18. **Look-ahead contamination and agent homogeneity (owner upload, 2026-10-07).** [S4_LIT_LOOKAHEAD_2026-10-07.md](S4_LIT_LOOKAHEAD_2026-10-07.md) reviews four papers (one duplicate removed).
    - **Correction:** cutoff-based evidence shows inflated in-sample accuracy; the "unknown sign" statement is limited to named-vs-anonymised designs.
    - Index-level recall is near-total, so historical evidence on asset-class agent judgements carries essentially no weight. R2, DR-5 and forward testing are reinforced; deterministic layers are unaffected.
    - Candidate clean-window rule for learning (a model upgrade resets it).
    - Diagnostics X-1 … X-5 for S7; DR-9 and DR-10 for S8.
    - Pointers: RQ-10/22/26/55/56 and S4.0 §12.

---

## A. ANG architecture baseline map

> **Superseded as the canonical map (2026-10-08)** by [S4_ANG_BASELINE.md](S4_ANG_BASELINE.md) (S4.1). This section is kept as draft history. Corrections found while verifying it are listed in S4_ANG_BASELINE §0.3 (page references pp. 13/21 → 14/22; fn. 6 spans pp. 14–15; data skill `apex-data-financial (fmp, finviz)`; Exhibit 1 differences).

### A.1 Pipeline (§3.1, pp. 6–7; Exhibit 1, p. 7)

```
Human: IPS (3 layers: universe · objective · active-risk budget)            [§4.1 p.15]
   │  governs every stage; hard vs. soft constraints                         [§4.1, §5.5]
Workflow manager (orchestration)                                             [§3.1 p.5]
   │
1  Macro agent → regime ∈ {expansion, late-cycle, recession, recovery} + confidence + narrative
   │            (scores growth, inflation, monetary policy, financial conditions; data + web)   [p.7]
2  Asset-class (AC) agents, in parallel, one per asset class (18)
   │    → per AC: up to 6 expected-return methods + auto-blend → CMA judge (LLM-as-judge,
   │      final ∈ [min, max] of methods) → expected return, volatility, confidence, memo   [§3.2 pp.8–9; A.1, A.2]
3  Covariance agent → covariance matrix (historical data + macro forecasts)               [p.6]
   │
4  PC agents (21): 19 fixed methods + Researcher run in parallel; Adversarial Diversifier
   │    runs after the first 20 finish                                                       [§3.3 p.9]
5  Strategy review: CRO standardized risk report per candidate (neutral, no vote)
   │    → 2 peer reviews per agent (1 intra-category, 1 inter-category; random seed; 42 reviews,
   │      released simultaneously) → modified Borda vote (top-5: 5..1; bottom flag −2; no self)
   │    → blended with quantitative metric score (regime-dependent weight)
   │    → diversity constraint (top-5 spans ≥ 3 of 5 families) → top-5 revise            [§3.4 pp.10–13]
6  CIO agent (LLM-as-judge): all 21 candidates + reviews + CRO reports + votes + scores
   │    → may choose one method or one of 7 ensembles (each evaluated on the same diagnostic
   │      suite; IPS compliance non-negotiable) → final weights + rationale + invalidation conditions
   │    → board memo                                                                           [§3.5 pp.13–14]
Human: board / investment committee reads, challenges, approves                          [p.14; §5.4]
   │
Monitoring, rebalancing (quarterly plan + off-cycle drift triggers in memo), meta-agent learning  [p.14; §6.2]
```

### A.2 Agent roster (44 agents; abstract and §7)

| Role | Count | Function | Output | Determinism note |
|---|---|---|---|---|
| Macro agent | 1 | Regime classification with confidence | Regime file + narrative | Scoring framework in a skill; web search |
| AC agents | 18 | Per-asset-class CMAs | `cma_methods.json`, `cma.json`, `signals.json`, `historical_stats.json`, `scenarios.json`, `correlation_row.json`, `analysis.md` (A.1) | Methods run in code (`cma_methods.py`); judge is the LLM |
| Covariance agent | 1 | Covariance matrix | Σ | Estimator unspecified |
| PC agents | 19 + 2 | One method each | Proposed weights + justification | All optimiser runs in code (p.15 fn.6; A.1) |
| CRO agent | 1 | Standardized risk report; enforces hard constraints | Risk report | Neutral; does not vote |
| CIO agent | 1 | Score, combine or select; explain | Final weights, rationale, board memo | Ensemble methods in `script.py` (Exhibit 5) |
| Meta agent | 1 | Forecast-vs-realised feedback; modifies skills, prompts, code | Change log | Human approval above a materiality threshold; IPS and compliance files excluded (pp. 27–28) |
| Workflow manager | — | Orchestration | — | Not counted among the 44 |

Count check: 1 + 18 + 1 + 21 + 1 + 1 + 1 = 44. This matches the abstract.

### A.3 Inputs consumed by PC agents
PC agents "take the CMAs … and the covariance matrix" (p. 6). Categories differ in what they use (p. 9):
- A, heuristic: avoid optimisation-driven estimation error.
- B, return-optimised: use CMAs explicitly.
- C, risk-structured: risk metrics without return forecasts.
- D, non-traditional: expected shortfall, drawdown profiles, multi-factor risk budgets.
- E, agentic.

### A.4 Governance, determinism, learning, limitations
- **IPS** (§4.1, §5.5):
  - **Universe** (hard): 18 ETF-investable asset classes.
  - **Objective** (soft): CPI + 3–4%, volatility 8–12%, max drawdown −25%.
  - **Active risk** (hard): ex-ante TE ≤ 6% versus 60/40.
  - Soft breaches are flagged in the board memo, never silently overridden.
- **Autonomy is set by the IPS:** tightening bounds moves the system toward supervisory control (§6.1).
- **Deterministic computation** (p.15 fn.6; A.1): all numerical computation, statistics and optimiser runs execute in code. Model versions and sampling parameters are pinned within a review cycle; pairing seeds are recorded; prompts, skills and outputs are archived.
- **Agent anatomy** (A.1): description · scripts · skills · output contract (JSON + markdown).
- **Meta agent** (§6.2):
  - Feedback over a rolling 3-year window: regime accuracy, cross-sectional rank correlation of expected returns, signal hit rates, per-method prediction error by asset class and regime.
  - Modifies skills, prompts and Python code.
  - Materiality threshold with human approval above it; declared file set; full change log.
- **Decomposition** (§6.3): any node can become a team of sub-agents (e.g. CRO sub-agents using different covariance estimators).
- **Limitations** (§5):
  - LLM look-ahead leakage;
  - non-reproducibility;
  - correlated LLM errors, mitigated by heterogeneous models and deterministic optimisers;
  - model-version drift;
  - automation surprise;
  - security of self-modifying agents.
- **Evidence status:** the illustrative March-2026 run is "not a backtest" and "not evidence of outperformance" (pp. 2, 13, 21).

### A.5 Internal inconsistencies in ANG (record, do not resolve silently)

| # | Inconsistency | Locations | Handling |
|---|---|---|---|
| I-1 | "PC agents vote for two proposals" vs. top-five Borda + bottom flag | Exhibit 4 vs. §3.4 p.12 | Text is more specific; S12 records both |
| I-2 | "Covariance Agents" (plural) vs. "a covariance agent" | Exhibit 1 vs. §3.1 p.6 | S10: one or many estimators (cf. §6.3) |
| I-3 | Six methods per AC agent vs. five method columns in Exhibit 6 (survey absent) vs. 6 + auto-blend in A.2 | §4.3 p.16, Exhibit 6, A.2 | S9 inventory lists all seven candidates |
| I-4 | "CVaR optimization" vs. "CVaR Minimization" | Exhibit 3 vs. Exhibits 7–8 | Objective ambiguous (min-CVaR vs. mean–CVaR); resolve from Rockafellar–Uryasev |
| I-5 | "Total Portfolio Allocation" vs. "Total Portfolio Approach" | Exhibit 4 vs. Exhibit 3 | Naming only |
| I-6 | "Global min vol" vs. "Global minimum variance" | Exhibit 4 vs. Exhibit 3 | Same portfolio (argmin σ ≡ argmin σ²); record equivalence |
| I-7 | CIO input: "21 candidate portfolios" vs. Exhibit 5 showing revised PC agents | §3.5 p.13 vs. Exhibit 5; Exhibit 8 weights all 21 | CIO combines all 21 (revised and unrevised) |
| I-8 | Two scoring layers with different weights: strategy-review metric (regime-dependent weights) vs. CIO's six dimensions (25/15/15/20/15/10) | §3.4 p.12; §4.5 p.19 | Both registered for S12; neither weight set adopted |

### A.6 Illustrative ANG parameters — recorded, not adopted
Composite 40% vote / 60% metric; CIO weights 25/15/15/20/15/10; adversarial Sharpe floor 75% of max-Sharpe; Borda points 5..1 and −2; ≥ 3 of 5 families in the top five; IPS numbers; 18-asset universe; 3-year CMA horizon; quarterly rebalancing. These are ANG design choices. Each becomes a research question for its owning stage (S9/S12/S13). None becomes a default (ADR-0001).

---

## B. ANG → our application: adaptation map

> **Superseded as the canonical map (2026-10-08)** by [S4_ANG_ADAPTATION.md](S4_ANG_ADAPTATION.md) (S4.2). Rows B-1 … B-23 are retained there with the same IDs; B-24 … B-45 are added. This section is kept as draft history.

Format: `ANG baseline → proposed adaptation → reason → architectural consequence` · class: **U** adopted unchanged · **G** generalized · **A** adapted for individual investors · **D** deferred · **N** not applicable.

| # | ANG baseline | Proposed adaptation | Reason | Consequence | Class |
|---|---|---|---|---|---|
| B-1 | Human-written IPS governs all agents | Declared/Effective **Policy Statement** (S1–S2) | Individual investor; declared vs. effective separation | Agents read the Effective PS; read-only (R4) | A (accepted G0–G2) |
| B-2 | IPS hard vs. soft constraints; soft breaches flagged | Constraint hardness hard/soft/trigger; finding records; approval of deviations | Same principle, formalised | CRO checks call deterministic predicates (R3) | G |
| B-3 | Board / investment committee approves the memo | The user approves the investment case (S14); authority grants (ADR-0017) | The individual is the board | CIO output is a proposal; decision authority stays with the user | A |
| B-4 | Macro agent, 4 regimes, weighted scoring | Macro **role** preserved; regime method is a research question (RQ-11, S9a); deterministic fallback required (R2) | No methodological defaults | Role contract defined in S4; method in S9a | G/D |
| B-5 | 18 AC agents, one per asset class | AC-analysis role per universe element; universe and allocation unit from S5 | Universe not yet chosen; may be security-level | Contracts support asset-class and security level | G/D |
| B-6 | CMA methods + LLM judge bounded to [min, max] | Same structure; judge enablement is RQ-12; R1 already encodes ANG's bound | R1 was derived from ANG | Judge = bounded choice among code-computed estimates | U (structure) / D (enablement) |
| B-7 | One covariance agent | Risk role; estimator selection in S10 (shrinkage, GARCH/DCC, RMT under the eligibility study) | Methodology open | Each PC method declares the risk representation it needs | G/D |
| B-8 | 19 fixed PC methods, 5 families | Same 19 as the baseline registry, **plus Simple and Anchored EPO in family B** and governed additions | Owner extension | Method Library grows by ADR; heterogeneous typed contracts | G |
| B-9 | Researcher proposes a method; it joins the same run with CIO weight | Research lane DISCOVERED → … → ADMITTED; experimental runs and research review allowed; no production CIO allocation until admitted (ADR-0024 §1) | ADR-0005 funnel; R5 | Candidate state machine for discovered methods | A |
| B-10 | Adversarial Diversifier | Preserved as an agentic role over a deterministic optimisation; formulation needs completion (§D) | ANG under-specifies it | Runs after all others; its own contract | U/G |
| B-11 | CRO: standardized risk report; neutral | Preserved; diagnostics computed in code; commentary by agent | R3 | S4.16 defines the diagnostic contract | U |
| B-12 | Peer review (intra + inter), Borda, metric blend, diversity rule, top-5 revise | Preserved as the S12 baseline protocol; revisions limited to ADR-0024 §2 categories with parameter-authority classes; mechanics are S12 research questions | R1 | S4.17 metadata requirements | U (structure) / A (revision) |
| B-13 | CIO: 7 ensembles + single-method choice; LLM-as-judge | Preserved as the S12 baseline; ensemble choice = bounded choice among code-computed ensembles (R1); final approval by the user | R1, B-3 | S4.18 inventory | U/A |
| B-14 | Board memo vs. 60/40 | Investment-case report (S14) vs. the user's comparison benchmark (pending) | Individual context | Comparison benchmark ≠ anchor (§G S4.10) | A |
| B-15 | Rebalancing: quarterly + drift triggers in the CIO board memo | The rebalancing **rule** is part of the approved portfolio decision (proposed by the CIO, approved by the investor). Its **determination** is a deterministic service (ADR-0026 §5.1–5.2). Methods and parameters in S13b (RQ-44) | Rule ownership: ANG p. 14; BCD p. 14 fn. 5; Perold & Sharpe 1988 p. 26. Deterministic determination is an architecture decision | REB.* rule version carried by the approved decision | D (methods) / A (ownership) |
| B-16 | Meta agent self-modifies code and prompts below the materiality threshold | S17 (RQ-22). Method-Library or contract changes always go through the gate; sub-threshold scope defined at S17 | Reproducibility, ADR-0022 change control | Partial tension, flagged for S17 | A/D |
| B-17 | Single institutional portfolio, pre-tax, no accounts | PC layer works at total-portfolio level on the admissible universe; account eligibility, asset location and tax in S13a | Multi-account, tax-aware individual | Decision at S11/S13: PC-level vs. account-level constraints. S4 contracts must allow both | A |
| B-18 | Frontier LLMs plus web search are integral | Agent layer is the baseline architecture. Deterministic-only mode is the R2 control and privacy fallback. Personal data reaches an LLM only with RQ-40 consent | Privacy (ADR-0014) | S8 must support both modes. **Correction to my 2026-10-01 S8 proposal**, which called deterministic-only the default | A |
| B-19 | Agents favoured covariance-based methods in March 2026 | **Not adopted as evidence** | ANG's own caveat; S7 governs evidence | — | N |
| B-20 | Workflow manager | Orchestration component | — | S8 | U |
| B-21 | Heterogeneous LLMs to mitigate correlated errors | Registered for S8/S12 (RQ-10) | — | — | D |
| B-22 | Weights "are then implemented through trading" (p. 5); no trading role | **Extension:** hybrid Trader/Implementation role with a deterministic Execution service; conditional tactical mandate (RQ-17); escalation edge back to the investment process (ADR-0026 §5–7) | Individual investor needs an accountable implementation function | Mandates and Decision Records for downstream roles (S4.2b, S4.15b) | G (extension) |
| B-23 | Governance through IPS, CRO, review, board memo | **Accountability layer around ANG:** an Agent Mandate per role; controls set in advance by S7; trace keys; no container categories (ADR-0026) | BCD 2022 institutional evidence; ANG unchanged | `S4_ACCOUNTABILITY.md` | G |

### B.1 Conflicts identified (must be resolved explicitly)

| # | Conflict | Where | Proposed resolution |
|---|---|---|---|
| C-1 (RESOLVED by ADR-0023) | Accepted 05 §2 layer 6 says deliberation exists "**if retained** (RQ-16)", and layer 3's judge is "optional". This can read as permission to drop ANG's deliberation and CIO layers, which conflicts with the new baseline principle | 05_DETERMINISTIC_VS_AGENT §2 (accepted G0) | OD-1(a): roles are structurally mandatory; enablement and weight are evidence-gated. Amend by ADR (not by editing 05's accepted text) |
| C-2 (RESOLVED by ADR-0024 §2) | ANG revisions could mean LLM-edited weights; R1 forbids that | 05 R1 | Six revision categories; parameter classes |
| C-3 (RESOLVED by ADR-0024 §1) | Researcher methods enter the same run; our funnel requires admission | ADR-0005, 06, R5 | Research lane |
| C-4 (RESOLVED — ADR-0025 ACCEPTED 2026-10-07; 06 §1/§2 and 02 §D annotated) | Accepted 06/02 define ADMISSIBLE as empirically evaluated; OD-4 makes admission methodological | ADR-0005, 06 §1(3), §2.4, 02 §D | ADR-0025: admission (S4) and evaluation status (S7) as separate axes. The "demonstration mode" proposal is withdrawn |
| C-5 (PROPOSED RESOLUTION — ADR-0027 D4) | Runtime use of backtest Sharpe (vote metric, CIO dimension, ensemble weighting) | ANG §3.4, §4.5 | Runtime diagnostics computed deterministically under the S7-defined protocol. Never used for Method-Library selection in S4 |
| C-6 (PROPOSED RESOLUTION — ADR-0027 D1–D2; scope S17) | Meta-agent autonomous code changes below threshold | ADR-0022 change control; 05 layer 10 | S17 decides scope; Method-Library and contract changes always gated |
| C-7 (RESOLVED — superseded proposal) | My 2026-10-01 S8 proposal: "whether to use an LLM at all … default offline deterministic only" | Proposal only (not accepted) | Replaced by B-18 |
| C-8 (RESOLVED — superseded proposal) | My 2026-10-01 S4 proposal treated S4 as a flat method inventory | Proposal only | Replaced by this plan |

| C-9 (RESOLVED — ADR-0026 ACCEPTED 2026-10-08; 05 annotated) | 05 §2 layer 8, "tactical judgement only if RQ-17 allows", could be read to forbid any implementation judgement | 05 (accepted G0) | Annotation: refers to deviation from w*; implementation judgement inside the mandate is governed by RQ-53 / S13 |
| C-10 (RESOLVED — ADR-0026 ACCEPTED 2026-10-08; 08 annotated; ADR-0012 §7 read by use per ADR-0026 §8.9) | ADR-0012 §7 can be read as placing all time-series evidence in S13d, conflicting with ANG's AC-level technical signals; 08 S13d presumes several "specialist agents" | ADR-0012; 08 | Read by use (beliefs/regime → S9; timing/tactics → S13d); the S13d list is a function inventory |

| C-11 (PROPOSED RESOLUTION — ADR-0027 D2) | ANG culls PC methods on performance (fn. 4 p. 9; p. 10) vs ADR-0025 (evaluation ≠ admission) and 02 §D (`RETIRED` by ADR only) | ADR-0025; 02 §D | No auto-culling; retirement by ADR; family floor |
| C-12 (PROPOSED RESOLUTION — ADR-0027 D3, r3 Option A) | Three ANG risk inputs (AC vol, AC correlation rows, covariance agent; ANG-33) vs one consistent risk model | S4.13/S10 | One authoritative risk model per problem (universe × horizon × risk object), estimator chosen on pre-registered risk accuracy (`S4_RISK_MODEL_CHOICE.md`) |
| C-13 (PROPOSED RESOLUTION — ADR-0027 D5) | ANG CMA units implicit (USD, 3-year, nominal) vs NOK context and D6 | RQ-07 | Declared currency/hedging/horizon/return-convention fields |
| C-14 (RESOLVED by planning) | ANG data stack (FMP, Finviz, US-listed ETFs) vs licence and universe findings | S6 lead | DR-7, CB-19, S6 |

No conflict found with accepted S1–S3 content. The registries, Policy Statement and authority model are compatible with ANG's IPS-centred governance.

---

## C. S4 master checklist

### C.1 Status ladders by object type
- **PC method / EPO variant:** NOT STARTED → SOURCE LOCATED → SOURCE REVIEWED → MATHEMATICS EXTRACTED → NOTATION RECONCILED → DEPENDENCIES IDENTIFIED → CONTRACT DEFINED → COMPUTATION VERIFIED → FIXTURES DEFINED → S4 COMPLETE
- **Signal (XSMOM, TSMOM):** NOT STARTED → SOURCE LOCATED → SOURCE REVIEWED → CONSTRUCTION EXTRACTED → PLACEMENT DETERMINED → PC-COMPATIBILITY DETERMINED → CONTRACT DEFINED → COMPUTATION VERIFIED → FIXTURES DEFINED → INVENTORY COMPLETE (detail → S9)
- **Upstream method (CMA, regime, covariance):** NOT STARTED → SOURCE LOCATED → IDENTIFIED → DEPENDENCIES MAPPED → HANDED TO S9/S10
- **Agent role (Macro, AC, Cov, PC, CRO, Reviewer, CIO, Researcher, AdvDiv, Monitoring, Meta; extensions: Trader/Implementation, conditional Tactical; services: Rebalancing determination, Execution):** NOT STARTED → ANG EXTRACTED (or EXTENSION RECORDED) → ADAPTATION DECIDED → **MANDATE STUB DEFINED** → INFORMATION CONTRACT DEFINED → HANDED TO S8/S12/S13/S17
- **Ensemble / deliberation method:** NOT STARTED → ANG EXTRACTED → DEPENDENCIES MAPPED → REGISTERED FOR S12
- **Architectural item (taxonomy, anchors, benchmarks, diagnostics, Portfolio Map):** NOT STARTED → DRAFTED → REVIEWED → ACCEPTED AT G4

### C.2 Step checklist (sequential)
| Step | Title | Status |
|---|---|---|
| S4.0 | Source and artefact inventory | DONE — awaiting owner review |
| S4.1 | Full ANG architectural reconstruction | DRAFTED 2026-10-08: `S4_ANG_BASELINE.md` (page-cited; verified V-1 … V-8; ANG-28 … ANG-36); awaiting owner review |
| S4.2 | ANG adaptation map + ANG-baseline ADR | DRAFTED 2026-10-08: `S4_ANG_ADAPTATION.md` (B-1 … B-45; C-11 … C-14) + ADR-0027 PROPOSED; awaiting owner review |
| S4.2b | Accountability layer (ADR-0026) | DRAFTED 2026-10-02 — `S4_ACCOUNTABILITY.md`; completes with S4.2 |
| S4.3 | Method taxonomy | REVIEWED 2026-10-08: `S4_TAXONOMY.md` (six kinds; type catalogue; identity and versioning; inventory pass F-1 … F-10); owner confirmed O-1 … O-4; SYNC-2 material for the developer |
| S4.4 | ANG PC source map | DRAFTED 2026-10-08: `S4_PC_SOURCE_MAP.md` (21 of 22 methods SOURCE LOCATED; PC-C5 identity gap; ANG-vs-source differences; acquisition plan); awaiting owner review |
| S4.5 | Heuristic portfolios (5) | NOT STARTED |
| S4.6 | Classical MVO foundation | NOT STARTED |
| S4.7 | MVO-family extensions (Max Sharpe, Robust MV, REF, BL, Simple EPO, Anchored EPO) | NOT STARTED |
| S4.8 | Momentum signal review (XSMOM, TSMOM) | NOT STARTED |
| S4.9 | Signal × PC compatibility | NOT STARTED |
| S4.10 | Anchor and benchmark architecture | NOT STARTED |
| S4.11 | Risk-structured PC methods (5) | NOT STARTED |
| S4.12 | Non-traditional PC methods (4) + mean–downside placement | NOT STARTED |
| S4.13 | Risk/covariance dependency inventory | NOT STARTED |
| S4.14 | Agentic PC roles (Researcher, Adversarial Diversifier) | NOT STARTED |
| S4.15 | Upstream CMA/signal inventory | NOT STARTED |
| S4.15b | Downstream method inventory (inventory only) | DRAFTED 2026-10-02 — `S4_DOWNSTREAM_INVENTORY.md` |
| S4.16 | CRO diagnostic requirements | NOT STARTED |
| S4.17 | PC deliberation requirements | NOT STARTED |
| S4.18 | CIO ensemble inventory | NOT STARTED |
| S4.19 | Equation Register reconciliation | NOT STARTED |
| S4.20 | Typed Method Contracts | NOT STARTED |
| S4.21 | Eligibility framework | NOT STARTED |
| S4.22 | Dependency graph | NOT STARTED |
| S4.23 | Computational verification | NOT STARTED |
| S4.24 | Fixtures and invariants | NOT STARTED |
| S4.25 | Portfolio Map analytical requirements | NOT STARTED |
| S4.26 | Candidate baseline freeze | NOT STARTED |
| S4.27 | G4 audit incl. ANG conformance | NOT STARTED |

### C.3 Method tracker (all NOT STARTED)
Roster v0 (versioned; ANG reference 21 + 2): PC-A1 … PC-A5, PC-B1 … PC-B7 (incl. B6 Simple EPO, B7 Anchored EPO), PC-C1 … PC-C5, PC-D1 … PC-D4, PC-E1 Researcher, PC-E2 Adversarial Diversifier; SIG-1 XSMOM, SIG-2 TSMOM; SCORE-VAL and SCORE-MOM (Sørensen/Storebrand reference specification, individual-security domain, S9c; amendment 17); CMA-1 … CMA-7; COV inventory; ENS-1 … ENS-7 (+ single-method selection); DEL-1 … DEL-6.

---

## D. ANG PC method source map

Verified against Exhibit 3 (p. 11) in the 21 Sep 2026 version: the owner's list matches exactly, including "TPA two-factor (equity and bonds)" and E = Adversarial diversifier, Researcher (no references).

| ID | Family | Method (ANG name) | ANG sample reference | Primary sources needed for the mathematics | Input class (to be verified) | Notes / known ANG-vs-source issues |
|---|---|---|---|---|---|---|
| PC-A1 | A Heuristic | Equal weight (1/N) | DeMiguel, Garlappi & Uppal (2009) | Same | Universe only | — |
| PC-A2 | A | Market-cap weight | Sharpe (1964) | Sharpe 1964; an asset-class market-cap data source (S6) | Cap weights | Needs asset-class capitalisations; data question |
| PC-A3 | A | Inverse volatility | Kirby & Ostdiek (2012) | Kirby & Ostdiek 2012 | σ | KO's volatility timing has a tuning exponent; check how ANG's 1/σ relates |
| PC-A4 | A | Inverse variance | Kirby & Ostdiek (2012) | Same | σ² | As above |
| PC-A5 | A | Volatility targeting | Moreira & Muir (2017) | Moreira & Muir 2017 | σ_t of a base portfolio | MM scale a single factor's exposure over time; ANG's cross-asset implementation (base portfolio, cash) is unspecified. **Specification gap** |
| PC-B1 | B Return-optimized | Maximum Sharpe ratio | Markowitz (1952) | Markowitz 1952; Tobin 1958; Sharpe 1964 | μ, Σ, r_f | Tangency; constraints |
| PC-B2 | B | Black–Litterman | Black & Litterman (1992) | BL 1992; He & Litterman 1999; Idzorek 2005 | Σ, w_mkt, δ, views, τ | BL also appears as a CMA method (equilibrium return); keep the two roles distinct |
| PC-B3 | B | Robust mean-variance | Goldfarb & Iyengar (2003) | G&I 2003; Tütüncü & Koenig 2004; Ceria & Stubbs 2006 | μ, Σ, uncertainty sets | Uncertainty-set choice is a parameter-authority question |
| PC-B4 | B | Resampled efficient frontier | Michaud (1998) | Michaud 1998 book; Michaud 1989; Scherer 2002 (critique) | μ, Σ, resampling count, seed | Stochastic: seed must be recorded; check IP status of the procedure |
| PC-B5 | B | Mean–downside risk (Sortino) | Sortino & van der Meer (1991) | S&vdM 1991; Estrada 2008; Markowitz et al. (semivariance) | μ, downside deviation / semicovariance, MAR | Objective ambiguous (max Sortino vs. mean–semivariance frontier) |
| **PC-B6** | **B (MVO extension)** | **Simple EPO** | (not in ANG) | **Pedersen, Babu & Levine 2021 (FAJ) + author version** | μ (or signal), Σ, θ | Extension of MVO addressing estimation error; exact shrinkage form, θ role and limits to extract in S4.7 |
| **PC-B7** | **B (MVO extension)** | **Anchored EPO** | (not in ANG) | Same | μ/signal, Σ, θ, anchor portfolio | Anchor contract (1/N, 1/σ, benchmark weights, other) per S4.10 |
| PC-C1 | C Risk-structured | Global minimum variance | Clarke, de Silva & Thorley (2006) | CdST 2006; Markowitz 1952; Jagannathan & Ma 2003 | Σ | Long-only vs. unconstrained |
| PC-C2 | C | Risk parity (ERC) | Maillard, Roncalli & Teïletche (2010) | MRT 2010; Spinu 2013 (algorithm) | Σ | Existence and uniqueness (long-only) |
| PC-C3 | C | Hierarchical risk parity | López de Prado (2016) | Same | Σ (correlation distance, linkage) | Linkage choice is a parameter |
| PC-C4 | C | Maximum diversification | Choueifaty & Coignard (2008) | C&C 2008; Choueifaty, Froidure & Reynier 2013 | σ, Σ | — |
| PC-C5 | C | Minimum correlation | Varadi et al. (2012) | Varadi et al. 2012 (working paper) | Correlation matrix, σ | Source quality: working paper; algorithm specification must be verified |
| PC-D1 | D Non-traditional | CVaR optimization / minimization | Rockafellar & Uryasev (2000) | R&U 2000, 2002 | Scenario returns, α | I-4: objective ambiguity |
| PC-D2 | D | Max drawdown-constrained | Chekhlov, Uryasev & Zabarankin (2005) | Same | Return paths | MDD vs. CDaR formulation |
| PC-D3 | D | Tail-risk parity | Boudt, Carl & Peterson (2013) | Same; Boudt, Peterson & Croux 2008 (modified ES) | Return distribution, ES contributions | — |
| PC-D4 | D | Total Portfolio Approach, two-factor (equity, bonds) | Ang, Brandt & Denison (2014) | ABD 2014 (AVAILABLE; funding framework); AQR 2026 (specification source for weights, owner D-5); Treynor & Black 1973 (primary, to obtain); Gilmore & Simonian 2025 | Factor exposures of each asset; reference portfolio | **Largest specification gap:** ANG gives no formulation. Unconstrained AQR sizing ≡ tangency under factor-model Σ (`VERIFIED-DERIVATION`), so distinctness must come from the reference-relative, funded, constrained form (S4.12) |
| PC-E1 | E Agentic | Researcher | — | ANG §3.3; example Bera & Park 2008 (max entropy) | Any (proposed) | Governed candidate lane (OD-2) |
| PC-E2 | E Agentic | Adversarial diversifier | — | ANG §3.3 p.10 only | Other PC weights, μ, Σ | Max tracking variance vs. centroid s.t. Sharpe ≥ 0.75·SR_max. Unspecified: budget, long-only, which Sharpe, convexity (maximising a convex function) |

### D.1 Candidate additions — NOT YET APPROVED / REQUIRES RATIONALE
Each must answer the six questions in the owner's instruction (philosophy, overlap, distinct objective, inputs, primary literature, informational value for deliberation).

| Candidate | Philosophy | Overlap concern |
|---|---|---|
| Maximum entropy (Bera & Park 2008) | Information-theoretic diversification | ANG's own Researcher example; overlaps 1/N with a floor |
| Benchmark-relative MVO / minimum tracking error | Active-risk budgeting against the user's benchmark | Overlaps Anchored EPO with a benchmark anchor |
| Norm-constrained MVO (DeMiguel et al. 2009b) | Regularised MVO | Overlaps EPO / robust MV |
| Growth-optimal / Kelly | Log-utility, wealth maximisation | Distinct objective; leverage concerns |
| General risk budgeting (non-equal) | Risk allocation by budget | Generalises ERC; needs budget authority |
| Effective-bets diversification (Meucci 2009) | Factor-level diversification | Overlaps max diversification |
| Signal-conditioned heuristics (e.g. 1/N among a momentum-selected subset) | Momentum strategy expressed through a heuristic weighting | **Only if S4.9 shows it is a distinct, literature-supported construction** |

---

## E. Source/paper checklist

Superseded by the S4.0 output [S4_0_SOURCE_INVENTORY.md](S4_0_SOURCE_INVENTORY.md), which uses the status classes AVAILABLE / MISSING (LOCATED) / IDENTITY UNCONFIRMED / UNUSABLE/CORRUPT / SECONDARY.

### E.1 Source authority (amendment 12)
No source type automatically establishes an investment method.

| Source class | Authority |
|---|---|
| ANG | Baseline agent architecture (ADR-0023) |
| Accepted project ADRs | Governance |
| Peer-reviewed / primary methodological literature | Methodological evidence |
| BCD 2022 / NBIM material | Institutional and accountability evidence, where applicable |
| Legacy ENGINE_V1 / thesis material | Research lead only (ADR-0001) |
| Practitioner material | Candidate / research lead |
| Social-media material | Hypothesis generation only |
| Owner suggestions | Requirements or research questions **only when explicitly adopted as such**; never empirical evidence |

**Claim labels:**
- `VERIFIED-SOURCE`, with the scope stated and never wider than the source;
- `VERIFIED-SECONDARY`;
- `VERIFIED-DERIVATION`;
- `INFERENCE`, i.e. architectural reasoning;
- `HYPOTHESIS`, needing empirical analysis;
- `UNVERIFIED`.

ADRs additionally mark statements as [SRC] / [AD] / [GR] / [DEF] (ADR-0026).

### E.2 Selectivity (amendment 12)
- An inventory item leaves through `REMOVED` (evidence or reasoning does not justify it), `RELOCATED` (wrong layer or stage) or `MERGED` (duplicates an existing method), each with a recorded reason.
- A method is removed when the evidence does not justify it, regardless of who proposed it.

---

## F. Equation checklist (all NOT EXTRACTED / NOT VERIFIED)

| ID | Item | Method(s) |
|---|---|---|
| EQ-MVO-1 | Mean–variance objective (risk aversion λ or γ) and the frontier problem | MVO family |
| EQ-MVO-2 | Unconstrained solution and two-fund representation | MVO family |
| EQ-MVO-3 | Tangency / maximum-Sharpe portfolio with risk-free asset; constrained variant | PC-B1 |
| EQ-MVO-4 | GMV closed form; long-only variant | PC-C1 |
| EQ-MVO-5 | Estimation-error characterisation used by EPO (problem portfolios / eigen-structure) | PC-B6/B7 |
| EQ-EPO-1 | Shrunk risk matrix as a function of θ | PC-B6 |
| EQ-EPO-2 | Simple EPO weights | PC-B6 |
| EQ-EPO-3 | Anchored EPO weights; anchor entry | PC-B7 |
| EQ-EPO-4 | Limiting cases θ → 0 (MVO) and θ → 1; scaling/normalisation | PC-B6/B7 |
| EQ-EPO-5 | Any signal/variance scaling used in the source | PC-B6/B7 |
| EQ-BL-1 | Implied equilibrium returns Π = δΣw_mkt | PC-B2, CMA-3 |
| EQ-BL-2 | Posterior mean and covariance (τ, P, Q, Ω) | PC-B2 |
| EQ-BL-3 | Optimisation of the posterior | PC-B2 |
| EQ-ROB-1 | Uncertainty sets (ellipsoidal / box) | PC-B3 |
| EQ-ROB-2 | Robust counterpart (SOCP) | PC-B3 |
| EQ-REF-1 | Resampling procedure, frontier averaging, rank association | PC-B4 |
| EQ-DS-1 | Downside deviation / semivariance with MAR | PC-B5 |
| EQ-DS-2 | Optimisation objective (Sortino ratio or mean–semivariance) | PC-B5 |
| EQ-H-1 | 1/N weights | PC-A1 |
| EQ-H-2 | Cap weights | PC-A2 |
| EQ-H-3 | Inverse-vol and inverse-variance weights (KO exponent form) | PC-A3/A4 |
| EQ-H-4 | Volatility-managed scaling c/σ²_t, target-vol scaling, cash residual | PC-A5 |
| EQ-RS-1 | Risk contributions and the ERC system | PC-C2 |
| EQ-RS-2 | ERC solution conditions | PC-C2 |
| EQ-RS-3 | HRP: correlation distance, quasi-diagonalisation, recursive bisection | PC-C3 |
| EQ-RS-4 | Diversification ratio and its maximisation | PC-C4 |
| EQ-RS-5 | Minimum-correlation algorithm | PC-C5 |
| EQ-NT-1 | VaR/CVaR definitions; R&U auxiliary function and LP | PC-D1 |
| EQ-NT-2 | Drawdown / CDaR / MDD constraints (LP) | PC-D2 |
| EQ-NT-3 | ES contributions; equal-ES-contribution system; modified ES | PC-D3 |
| EQ-NT-4 | Two-factor exposure mapping and TPA optimisation (to be specified) | PC-D4 |
| EQ-AG-1 | Ensemble centroid | PC-E2 |
| EQ-AG-2 | Tracking variance (w − c)ᵀΣ(w − c) | PC-E2 |
| EQ-AG-3 | Sharpe-floor constraint SR(w) ≥ 0.75·SR_max | PC-E2 |
| EQ-AG-4 | Shannon-entropy objective (Researcher example) | PC-E1 example |
| EQ-SIG-1 | XSMOM: formation return (lookback, skip), ranking, rank-based weights (AMP-style) | SIG-1 |
| EQ-SIG-2 | TSMOM: sign of past excess return, volatility scaling (ex-ante σ estimator), position size | SIG-2 |
| EQ-SIG-3 | Score transformations (z-score, rank) — cross-reference RQ-29 | SIG-1/2 |
| EQ-CMA-1 | Historical ERP + r_f | CMA-1 |
| EQ-CMA-2 | Regime-conditional ERP | CMA-2 |
| EQ-CMA-3 | Grinold–Kroner building blocks | CMA-4 |
| EQ-CMA-4 | CAPE-implied ERP | CMA-5 |
| EQ-CMA-5 | Confidence-weighted auto-blend; judge bound [min, max] | CMA-7 |
| EQ-DIAG-1 | Ex-ante volatility | CRO |
| EQ-DIAG-2 | VaR and ES (historical/parametric) | CRO |
| EQ-DIAG-3 | Max drawdown | CRO |
| EQ-DIAG-4 | Concentration (HHI, effective N per Meucci 2009) | CRO |
| EQ-DIAG-5 | Tracking error | CRO |
| EQ-DIAG-6 | Risk contributions | CRO |
| EQ-DIAG-7 | Factor tilts | CRO |
| EQ-DIAG-8 | Diversification ratio | CRO |
| EQ-ENS-1 | Simple average | CIO |
| EQ-ENS-2 | Inverse-TE weighting | CIO |
| EQ-ENS-3 | Sharpe weighting | CIO |
| EQ-ENS-4 | Meta-optimisation over PC portfolios | CIO |
| EQ-ENS-5 | Regime-conditional weights | CIO |
| EQ-ENS-6 | Composite-score weights | CIO |
| EQ-ENS-7 | Trimmed mean | CIO |
| EQ-DEL-1 | Modified Borda | Deliberation |
| EQ-DEL-2 | Normalisation and vote/metric blend | Deliberation |
| EQ-DEL-3 | Diversity-constraint selection | Deliberation |

Each entry carries the Equation-Register fields from the owner's item 14 (source equation/page, notation, canonical notation, dimensions, units, assumptions, constraints, parameter authority, limiting cases, numerical tests).

---

## G. Revised S4.0–S4.27 execution plan

Columns: **Entry** · **Work** · **Sources** · **Computation** · **Output** · **Exit** · **Handoff**.

| Step | Entry | Work | Sources | Computation | Output | Exit | Handoff |
|---|---|---|---|---|---|---|---|
| S4.0 Inventory | Plan approved; OD-1 … OD-7 decided | Locate every paper, prior methodology document, code and object; extract zips; confirm identities; list missing primaries and how to obtain them | §E; local roots; ENGINE_V1 (legacy) | None | `S4_SOURCE_INVENTORY.md` (path, identity, version, status) | Every §E row has a status; missing list has an acquisition route | — |
| S4.1 ANG reconstruction | S4.0 | Canonical architecture map: roles, order, data flows, CMA, covariance, PC, CRO, review, voting, revision, CIO, Researcher, AdvDiv, meta, IPS governance, determinism boundaries, limitations, inconsistencies; **cross-checked against the Oct 2026 lecture (skill library ANG-26; candidate cards ANG-24; learning loop ANG-25; analysis.md ANG-27)** | ANG v2 (full); lecture (secondary) | None | `S4_ANG_BASELINE.md` (from §A, page-cited) | Owner review | **SYNC-1** (with S4.2) |
| S4.2 Adaptation map | S4.1 | Adopted / generalized / adapted / deferred / N/A per element; resolve C-1 … C-8; draft ANG-baseline ADR | ANG; S0–S3 | None | `S4_ANG_ADAPTATION.md`; ADR (PROPOSED, decided at G4 or earlier if owner prefers) | Every ANG element classified; conflicts resolved or escalated | **SYNC-1** |
| S4.3 Taxonomy | S4.2 | Canonical object types: CMA/belief, signals, risk/covariance, PC families A–E, anchors, benchmarks, constraints, CRO diagnostics, deliberation, CIO ensembles, rebalancing, implementation; **plus (ADR-0026): evidence packet/descriptor (horizon, admitted uses), Agent Mandate, Decision Record, decision state (no-trade concepts), rebalancing rule, implementation method, timing-evidence method, tactical policy (conditional)**; **plus (amendment 15, learning): Forecast Record, Outcome Record, Reflection, Agent Memory State, Skill Version, Change Proposal, Replay/Shadow Test, Promotion/Rollback Decision; candidate card**; **plus (ADR-0027, proposed, and owner request 2026-10-08): risk-model artefact (universe; horizon; risk object; estimator; version; units); learning objects for PC methods, review/vote, CIO and CRO; score table / descriptor panel (`S4_SCORING_PEER_METHODS.md` §9)**; method vs. configuration vs. parameter; identity/versioning | ANG; 06; ADR-0012 | None | `S4_TAXONOMY.md` | Every inventory item has one type | **SYNC-2** |
| S4.2b Accountability | S4.2 (draft exists) | Role taxonomy incl. extensions; Agent Mandate schema; mandate stub per role; responsibility matrix v0; escalation model; no-trade concepts; traceability chain (definitions only) | ANG; BCD 2022; Sharpe 1981; vBBK 2008; Sensoy 2009; Perold 1988; Perold & Sharpe 1988 | None | `S4_ACCOUNTABILITY.md` | Every role has a mandate stub; no container role; extensions marked | **SYNC-1** |
| S4.4 PC source map | S4.3 | Final §D with sources per method; ANG-vs-source differences listed | §D sources | None | `S4_PC_SOURCE_MAP.md` | Every PC method at SOURCE LOCATED or a documented acquisition gap | — |
| S4.5 Heuristics | S4.4 | A1–A5 mathematics; specify volatility targeting's base portfolio | DGU 2009; Sharpe 1964; KO 2012; MM 2017 | Reference implementations; invariants (weights sum to 1, positivity, scale invariance); synthetic Σ | Equation Register entries; method records | MATHEMATICS EXTRACTED → COMPUTATION VERIFIED | — |
| S4.6 MVO foundation | S4.4 | Objective, frontier, tangency, constraints, risk-free treatment, estimation-error problem | Markowitz 1952; Tobin 1958; Sharpe 1964; Michaud 1989; Jorion 1986 | Closed forms vs. numerical solver; frontier tracing; condition-number sensitivity on synthetic data | Register; `S4_MVO_FOUNDATION.md` | Closed form = solver within tolerance | — |
| S4.7 MVO extensions | S4.6 | Max Sharpe, Robust MV, REF, BL, **Simple EPO, Anchored EPO**: exact EPO mathematics, what is shrunk, θ, anchor entry, limits; MVO → estimation error → EPO lineage | PBL 2021 (both versions); BL 1992; G&I 2003; Michaud 1998 | Reproduce PBL published examples where feasible; verify θ → 0 recovers MVO; robust SOCP; REF with seeded resampling | Register; `S4_MVO_FAMILY.md` with lineage diagram | Limits verified; ANG-vs-source differences recorded | — |
| S4.8 Momentum | S4.4 | XSMOM and TSMOM exact constructions (lookback, skip, ranking, weights, volatility scaling, rebalance) | JT 1993; MOP 2012; AMP 2013; HOP 2017; DM 2016; B&SC 2015 | Reproduce construction on synthetic series; sign and scale invariants | Register; `S4_MOMENTUM.md` | Construction contracts complete | — |
| S4.9 Signal × PC | S4.5–S4.8 | Determine the methodological objects supported by the literature (signal · signal-conditioned universe · direction/exposure rule · expected-return mapping · standalone strategy · tactical overlay); ANG's AC-level technical signals (A.1 step 4) are one placement, not a conclusion; per pair: 1/N, 1/σ, MVO, Simple EPO, Anchored EPO, others; allowed constructions only where the literature supports them; momentum-score → μ mapping registered as an S9d methodology | As S4.8; PBL 2021 (signal use) | Toy examples showing each construction is well-defined; unit checks | `S4_SIGNAL_PC_COMPATIBILITY.md` (matrix: valid / invalid / requires mapping) | No combination without semantics | **SYNC-3** (with S4.10) |
| S4.10 Anchor & benchmark | S4.7 | Distinguish PC method · anchor method · benchmark · benchmark weights · comparison benchmark; valid anchor contract (1/N, 1/σ, benchmark weights, other source-supported); when anchor = comparison benchmark | PBL 2021; BL 1992 | Anchored EPO with each anchor on synthetic data; anchor-invariance tests | `S4_ANCHOR_BENCHMARK.md` | Contract stated; no index hard-coded | **SYNC-3** |
| S4.11 Risk-structured | S4.4 | C1–C5 | CdST 2006; MRT 2010; LdP 2016; C&C 2008; Varadi 2012 | ERC convergence; HRP determinism; equivalences (e.g. MD vs. GMV when correlations are equal) | Register; method records | Verified | — |
| S4.12 Non-traditional | S4.4 | D1–D4; placement of mean–downside risk. **TPA (restated 2026-10-07, amendment 14):** specify our own TPA-family candidate from: (i) ABD's funding decomposition (each position funded from a stock/bond reference portfolio by its betas, Eq. (4)); (ii) Treynor–Black/AQR appraisal-ratio sizing (active weight ∝ Σ_ε⁻¹α); (iii) a long-only, no-leverage constrained version (final weights w = w_ref + a − B′a within the Policy Statement bounds, optionally an active-risk budget relative to w_ref). **Distinctness test before admission:** compare with PC-B1 under a factor-model Σ (unconstrained equivalence is `VERIFIED-DERIVATION`), Anchored EPO with w_ref as anchor, and factor-MVO. If not distinct, MERGE or RELOCATE (e.g. to an attribution/funding lens in S14) | R&U 2000/02; CUZ 2005; BCP 2013; ABD 2014; AQR 2026 (secondary); Treynor & Black 1973 (to obtain); Gilmore & Simonian 2025 | LP formulations on synthetic scenarios; CVaR → GMV under normality checks | Register; method records; TPA gap memo | Verified or explicit gap | — |
| S4.13 Risk inventory | S4.5–S4.12 | Per PC method: required risk representation (Σ, σ, semicovariance, scenarios, paths, factors); estimator candidates (shrinkage, GARCH/GJR, DCC/cDCC, RMT) registered only; **(ADR-0027 D3 r3, Option A) estimator candidates registered per problem (universe × horizon × risk object) with eligibility over (N, q_eff, constraint regime, horizon); selection stays with S10** | LW 2003/04/17; Laloux; BBP 2017; Bollerslev; Engle; Aielli | None (S10 owns selection) | `S4_RISK_DEPENDENCIES.md` | Every method's risk input typed | → S10 |
| S4.14 Agentic PC | S4.7, S4.11 | Researcher: research lane DISCOVERED → RESEARCH CANDIDATE → SPECIFIED → VERIFIED → ADMISSIBILITY REVIEW → ADMITTED (ADR-0024 §1). AdvDiv: complete formulation (budget, bounds, Sharpe definition, solver for maximising a convex function, determinism) | ANG §3.3; Bera & Park 2008 | AdvDiv reference solver; verify orthogonality and Sharpe floor; multiple-optima check | `S4_AGENTIC_PC.md` | Contracts defined; open choices listed | — |
| S4.15 Upstream inventory | S4.3 | ANG CMA methods (7 candidates incl. auto-blend), confidence scores, judge, regime, covariance role, our momentum; split S4 inventory / S9 / S10 | ANG; GK 2002; Gordon 1959; CS 1998; Merton 1980 | None | `S4_UPSTREAM_INVENTORY.md` | Dependency structure fixed | → S9, S10 |
| S4.15b Downstream inventory | S4.3 | Families T1–T12; ML-specification disposition (owner D-D); z-score as a T3 lead with family removal criteria; **inventory only, no mathematical review** | Located sources only | None | `S4_DOWNSTREAM_INVENTORY.md` | Every family has a source status and a stage | → S13, S7 |
| S4.16 CRO diagnostics | S4.5–S4.14 | Diagnostic contract every candidate must expose (ANG list + IPS/PS compliance, estimation sensitivity, CMA use, distance to other proposals); **candidate card as the R8 evidence object (ANG-24); duplicate-proposal detection by portfolio distance (`S4_GITHUB_IMPL_REVIEW.md`)**; **trace keys; interim-risk-limit fields for implementation (ADR-0026 §5)**; **(ADR-0027 D3 r3, Option A) risk-model sensitivity line: risk and weights under at least one alternative admissible estimator; material change of the recommendation flagged** | ANG §3.4; diagnostics literature | Reference diagnostics on synthetic portfolios | `S4_CRO_CONTRACT.md` | Every PC output can populate it | **SYNC-4** |
| S4.17 Deliberation reqs | S4.16 | Metadata reviewers need (objective, assumptions, inputs, risks, sensitivity, CMA use, PS compliance, differences); **evidence cited with consumer use (ADR-0026 §8)**; ANG review/vote/revise protocol registered; **correlated-error mitigations M3–M4, M8 (RQ-56)** | ANG §3.4 | None | `S4_DELIBERATION_REQUIREMENTS.md` | Metadata schema complete | **SYNC-4** → S12 |
| S4.18 CIO inventory | S4.16 | 7 ensembles + single-method choice; inputs, dependencies, evaluation needs; explicit separation of PC method evaluation / peer ranking / CIO combination; **per ensemble: linear vs non-linear decomposability (ADR-0026 M-1); approved-decision fields incl. rebalancing rule and implementation parameters** | ANG §3.5, §4.5 | None | `S4_CIO_INVENTORY.md` | Registered, not approved | **SYNC-4** → S12, S7 |
| S4.19 Equation reconciliation | S4.5–S4.14 | Verify every equation against its primary source; canonical notation; dimensions and units | All | Dimension and unit checks | `S4_EQUATION_REGISTER.md` (complete) | All entries reconciled | — |
| S4.20 Typed contracts | S4.19 | Heterogeneous contracts by family (μ-free heuristic; μ+Σ; Σ-only; distribution/path/factor; agentic); **dual contract** (machine + agent-readable, ADR-0024 §5); **descriptor contract fields: horizon, admitted uses per consumer role, consumer log; trace keys emitted/consumed; machine-readable Agent Mandate schema (ADR-0026 §3)**; **parameter classes** (fixed / system-estimated / user-authorized / agent-selectable / sensitivity-only); **candidate fields (amendment 15): currency/hedging basis of return and risk inputs; common-basis declaration for CMA candidates; support for minimum-position/lot/cardinality constraints; verifiability class of agent-readable outputs (RQ-55); learning signals (RQ-22)**; **allocation domains**; Method ≠ Agent Role ≠ Proposal objects; reads, required PS fields, outputs, units, data needs, failure modes, deterministic class | 06 §5; ADR-0012/0015/0019 | Schema validation of every method record | `S4_METHOD_CONTRACTS.md` + machine-readable schema | Every method has a valid contract | **SYNC-5** |
| S4.21 Eligibility framework | S4.20 | Funnel predicates; **methodological admission criteria** (source, clear mathematics, deterministic implementability, verified reproduction, explicit inputs/assumptions, defined role; ADR-0025) kept separate from the empirical-evaluation axis (S7); point-in-time context; reason codes; exclusion report; threshold policy (no invented values); hysteresis framework; overrides; research-lane states | 06; ADR-0005 | Predicate tests on fixtures | `S4_ELIGIBILITY_FRAMEWORK.md` | No winner selected | — |
| S4.22 Dependency graph | S4.20 | Method / data / signal / risk / benchmark / constraint / fact-domain dependencies; deterministic / agent / human assignment per node; **role/mandate nodes and the Decision-Record lineage (ADR-0026 §9)** | All S4 outputs | Graph validation (acyclic, declared reads) | `S4_DEPENDENCY_GRAPH.md` | Complete | — |
| S4.23 Verification | S4.19–S4.22 | Implementation verification only: reproduce source examples, limits, equivalences, stability, constraints; **invariants I-1 … I-9 and port-and-verify of reusable third-party code (`S4_GITHUB_IMPL_REVIEW.md` §10–§11)** | Register | Full verification suite (synthetic Σ, μ, scenarios) | `S4_VERIFICATION_REPORT.md` + code (OD-5) | All methods at COMPUTATION VERIFIED or documented exception | — |
| S4.24 Fixtures | S4.23 | Fixtures and invariants able to detect wrong implementations | Register | Run against reference code | `S4_SYNTHETIC_FIXTURES.md` | Each method has ≥ 1 discriminating fixture | — |
| S4.25 Portfolio Map reqs | S4.20 | Metadata every method must expose (§J) | — | None | Requirements register | Complete | → S7, S11, S12, S8 |
| S4.26 Baseline freeze | S4.21–S4.25 | Versioned G4 Method Library baseline (open to governed additions) | — | — | Library manifest v1 | All items S4 COMPLETE or documented | — |
| S4.27 G4 audit | S4.26 | Full re-audit against ANG; answer the conformance question; A/B/C gap classification; CB items | ANG; all outputs | — | `S4_G4_PACKAGE.md` | Owner review | **SYNC-6** |

---

## H. S4/S8 synchronization map

| Sync | After | Developer receives | Developer can then |
|---|---|---|---|
| SYNC-1 | S4.1/S4.2/S4.2b | Canonical ANG pipeline, agent roles, authority boundaries, adaptation map; **Agent Mandate concept, downstream extensions and services, Decision Records (interface only)** | Shape module boundaries and orchestration so the roles stay separable (no monolithic "investment AI") |
| SYNC-2 | S4.3 | Taxonomy of module types (CMA, signal, risk, PC A–E, anchor, benchmark, diagnostics, deliberation, ensemble) | Design registry types and plugin categories |
| SYNC-3 | S4.9/S4.10 | Signal → belief → PC relationships; anchor/benchmark objects | Model data flows and the benchmark/anchor entities |
| SYNC-4 | S4.16–S4.18 | PC → CRO → deliberation → CIO information flow and metadata | Design evidence-packet storage, review records, run structure |
| SYNC-5 | S4.20 | Formal typed Method Contracts + schema + reference implementations as oracles; **machine-readable mandate schema; descriptor and trace-key fields (interface only)** | Implement the real Method Registry and method host |
| SYNC-6 | G4 | Accepted Method Library baseline v1 | Integrate the baseline methods behind contracts |

---

## I. S8a sequence alongside S4

```
S8a: Developer Architecture Brief ─► developer feedback ─► architecture alternatives ─► decisions ─► G8a ─► foundation implementation
            ▲                                ▲                                            ▲                       ▲
S4:  S4.0 ─ S4.1/4.2 (SYNC-1) ─ S4.3 (SYNC-2) ─ S4.4–4.10 (SYNC-3) ─ … ─ S4.16–18 (SYNC-4) ─ S4.19–20 (SYNC-5) ─ … ─ G4 (SYNC-6)
```

- **Developer Architecture Brief** (no stack prescribed):
  - ANG is the investment-process baseline;
  - deterministic calculations run in code;
  - specialist agents operate over structured deterministic outputs;
  - methods are modular and PC methods run in parallel;
  - the Method Library grows through governed additions;
  - CRO, deliberation and CIO are later layers and must never be collapsed into the optimiser;
  - S4 delivers contracts progressively; unresolved methodology stays behind interfaces;
  - both agent mode and deterministic-only mode must be supported (B-18);
  - role composability (Macro, CMA/AC, Covariance/Risk, PC, CRO, Review/Deliberation, CIO, Researcher, Meta);
  - the S0–S3 foundation and the readiness matrix (2026-10-01);
  - **registered for S8, interface only, not accepted (amendment 15):** DR-1 as-of gate with look-ahead test; DR-2 learning capture from the first slice (Forecast/Outcome Records, versioned agent memory in the run manifest); DR-3 repeat-run and seeded-fault harness; DR-4 R8 lint; DR-5 mode stamp; DR-6 multi-provider models with per-role assignment; DR-7 permanent instrument identifiers and user-supplied vendor credentials (refined 2026-10-08: licence class per source, provenance stamp, no cross-user sharing; `research/s6/S6_LEAD_DATA_SOURCES_2026-10-08.md` §6); DR-8 price class and currency-account flags in the cost model ([S4_INPUTS_2026-10-07.md](S4_INPUTS_2026-10-07.md) §8); **(amendment 18)** DR-9 model provenance (version, training cutoff, fine-tune date) on every agent output and Forecast Record; DR-10 contamination-diagnostic capability (log-probabilities or repeated sampling) ([S4_LIT_LOOKAHEAD_2026-10-07.md](S4_LIT_LOOKAHEAD_2026-10-07.md) §3).
- **G8a** fixes architecture, stack, data boundaries and change control, ideally around SYNC-2 so module types are known.
- **Foundation implementation** starts after G8a. The real Method Registry follows SYNC-5.

---

## J. Portfolio Map requirements register (placeholder)

**Purpose:** expose the portfolio opportunity/proposal space that the architecture generates. The classical efficient frontier is one view inside it.

**Candidate views (none adopted; S7 decides validity):**
- expected return ↔ risk;
- return ↔ drawdown;
- tracking error ↔ expected active return;
- diversification ↔ risk;
- portfolio similarity / distance;
- risk contributions;
- factor exposures;
- method clusters (do independent PC proposals cluster or disagree?);
- allocation differences.

| ID | Requirement | Analytical dependency | Responsible stage |
|---|---|---|---|
| PM-1 | Show competing PC proposals, current portfolio, benchmark, anchor, CIO portfolio | Common estimates for any weight vector | S11, S12, S8 |
| PM-2 | MVO frontier (and constrained frontier) as one view | Frontier under the same μ, Σ, constraints | S4 (math), S11 |
| PM-3 | Non-MVO methods shown as points, never implied to lie on the frontier | Metadata `generates_frontier` | S4.25 |
| PM-4 | Only valid comparison axes (ex-ante vs. realised; metric validity per method) | Comparison-metric definitions | S7 |
| PM-5 | Method-map view of clustering vs. disagreement | Portfolio-distance and similarity metrics | S11, S12 |
| PM-6 | CIO portfolio relative to the candidate set | Ensemble weights, centroid | S12 |
| PM-7 | Full provenance of every plotted quantity | Run manifests | S8 |
| PM-8 | Uncertainty display | Estimation-error measures | S10, S11 |
| PM-9 | Multiple coordinated views; no hard-coded visualization | View registry | S8 (after S7) |

---

## K. G4 acceptance criteria

1. Source inventory complete; every primary source located or its absence documented with the consequence.
2. ANG baseline map accepted; adaptation map with every element classified; conflicts C-1 … C-8 resolved; ANG-baseline ADR.
3. Taxonomy covering every object type.
4. All 19 fixed PC methods, Simple EPO and Anchored EPO: method records with every field in the owner's item 13.
5. Equation Register complete and reconciled to primary sources (page and equation cited); ANG-vs-source differences documented.
6. EPO lineage (MVO → estimation error → EPO → Simple / Anchored) explicit; limits verified.
7. Anchor/benchmark architecture with no hard-coded index.
8. Signal × PC compatibility matrix; momentum → μ mapping registered as an S9d methodology.
9. Researcher and Adversarial Diversifier contracts, with the governed candidate lane.
10. CRO diagnostic contract; deliberation metadata; CIO ensemble inventory, registered for S12, not approved.
11. Heterogeneous typed contracts and schema; eligibility framework without winners; dependency graph.
12. Computational verification report (implementation verification only) and discriminating fixtures.
13. Portfolio Map requirements register.
14. Hand-forward registers for S5/S6, S7, S9, S10, S11, S12, S13, S16/S17; CB items for S4 (currently none); gaps classified A/B/C.
15. Contracts implement: Method ≠ Method Contract ≠ Agent Role ≠ Agent Instance ≠ Portfolio Proposal; parameter-authority classes; allocation domains; dual (machine + agent-readable) contracts; a versioned PC roster; an explicit proposal → CRO → peer assessment → revision → CIO separation (the peer vote is not a weighting rule).
16. Methodological admission evidence per admitted method (ADR-0025 criteria), kept separate from empirical evaluation (S7).
17. ANG issues register reviewed; every H-materiality issue relevant to an admitted method resolved or recorded with its handling.
18. **ANG-conformance audit**, answering in writing:
    - Is every ANG role representable, with separable authority?
    - Can the system run `PC_i → Method_i → Portfolio_i` in parallel?
    - Can every candidate populate the CRO report and the deliberation metadata?
    - Can the CIO combine candidates by any of the registered ensembles without the library ranking methods?
    - Does any contract force all methods through a μ interface?
    - Does the user still approve as the "board"?
    - **Overall: does the Method Library still support ANG's agentic architecture, or has it become an optimizer-selection application?**
19. **Mandates:** every roster role, including downstream extensions and services, has a mandate stub with all ADR-0026 §3 fields present (values may be "deferred to Sxx").
20. **Evidence semantics:** every evidence/descriptor type declares horizon and admitted uses; the consumer-log requirement is in the contract.
21. **No-container audit passes:** every active decision type maps to mandate, role, method/evidence, authority, target, constraints, timing, data, rationale, cost and outcome.
22. **Implementation invariants** (ADR-0026 §5) are reflected in contracts: no field lets an implementation role change w*, the rebalancing rule, the window or the limits.
23. **Source-status table** complete, in groups: verified and available / identified but not available / unnecessary or overstated.
24. **Learning readiness (amendment 15; owner priority):** every role's mandate stub declares its learning signals (outcome- and process-based) and the records needed to compute them. The S4.3 taxonomy contains the learning objects. The S8 interface list includes capture from day one (DR-2).

---

## L. Explicit exclusions

- **UEPO, SEPO and DEPO are removed from the S4 plan.** They will not enter any later stage, under these or other names, unless the owner explicitly reopens them.
- No thesis experiment enters the Method Library without source and provenance review; thesis code is a lead only (ADR-0001).
- Pension saving and wealth tax remain out of scope (ADR-0020/0021).
- ANG's illustrative rankings, weights and parameters are not evidence and not defaults (§A.6; ADR-0023 §8–9).
- No ranking of methods is produced in S4.
