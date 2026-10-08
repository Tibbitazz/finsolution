# S4.2 — ANG → FinSol adaptation map

**Document status:** DRAFT for owner review (S4.2; exit = "every ANG element classified; conflicts resolved or escalated"; SYNC-1 with S4.1) · **Prepared:** 2026-10-08 · **Inputs:**
- `S4_ANG_BASELINE.md` (S4.1, canonical map);
- S4_PLAN §B (draft B-1 … B-23, kept as history);
- ADR-0023 … ADR-0026 (accepted);
- `ANG_ISSUES_REGISTER.md` (ANG-01 … ANG-37).

**Proposed companion ADR:** ADR-0027 (PROPOSED): adaptation decisions that no accepted ADR yet covers (§4).

## 0. Legend and rules
- **Class:**
  - **U**: adopted unchanged (structure);
  - **G**: generalised (same function, broader or formalised);
  - **A**: adapted for a reusable, individual-investor, multi-account, NOK-context engine;
  - **D**: deferred to an owning stage (role kept, method open);
  - **N**: not applicable or not adopted.
- **Binding:** where a row is already bound by an accepted ADR, the ADR is cited and this map adds nothing. Rows marked **(ADR-0027)** become binding only if the owner accepts ADR-0027. All other rows are classifications for planning (DRAFT).
- **Rules carried over:**
  - **ADR-0023 §8:** adopted architecture vs illustrative choices not adopted.
  - **ADR-0001:** no ANG numbers become defaults.
  - **R1–R8:** numbers are computed in code; agents interpret.

## 1. Classification map (every element of `S4_ANG_BASELINE.md`)

### 1.1 Governance and human authority

| ID | ANG element (baseline ref) | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-1 | IPS written by humans governs all agents (§2.1 H0; §7) | A | Declared → Effective **Policy Statement**; agents read the Effective PS, read-only (R4) | Individual investor; declared vs effective separation | ADR-0008, ADR-0014 (accepted) |
| B-2 | Hard vs soft constraints; soft breaches flagged, not overridden (§7) | G | Constraint hardness hard / soft / trigger; finding records; every deviation needs approval; constraint mathematical type (RQ-15) | Same principle, formalised; reverse-convex and path-dependent constraints handled explicitly | ADR-0015/0016 (accepted); RQ-15 |
| B-3 | Board / committee reads, challenges, approves (§2.1 H1) | A | The **user** approves the investment case; authority grants (ADR-0017); a recorded response to each flagged deviation (ANG p. 25) | The individual is the board | ADR-0017, ADR-0026 §10 |
| B-14 | Board memo vs 60/40 (§7) | A | Investment-case report (S14) vs the user's comparison benchmark (`POL.benchmark`, pending S7) | Individual context; comparison benchmark ≠ anchor | S14; S4.10 |
| B-24 | Autonomy set by tightening or relaxing the IPS (§7; p. 27) | A | Autonomy is set by **ADR-0017 authority dimensions** (dimensions 6–8 locked until S13 safeguards), not by IPS bounds alone | Separation of preferences (PS) from delegation (authority) | ADR-0017 (accepted) |
| B-23 | Governance through IPS, CRO, review, memo (§7) | G | **Accountability layer around ANG:** Agent Mandates, controls set in advance, trace keys, Decision Records, no container categories | BCD 2022 institutional evidence | ADR-0026 (accepted) |

### 1.2 Orchestration, anatomy, skills, contracts

| ID | ANG element | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-20 | Workflow manager (§2.1 W) | U | Orchestration component with explicit barriers (§2.2 of the baseline) | — | S8 |
| B-25 | Agent = description + scripts + skills + output contract (§4) | U | Same four components; **dual contract** (machine + agent-readable) per method | Matches R1/R8 | ADR-0023 §8, ADR-0024 §5 |
| B-26 | Skills library (paper + lecture union; §4) | G | Versioned skill registry, organised by allocation family and pipeline function; skills versioned independently of the model (DR-6) | Learning operates on skills; needs versioning | S4.3, S8 |
| B-27 | Output contract: JSON for machines + markdown for humans (§4) | U | Same; every narrative number cites a descriptor (R8 lint, DR-4); `analysis.md` skeleton v0 | — | S4_INPUTS §3.4; S8, S9b |
| B-28 | Decomposition principle (p. 29) | U | Used as the test for any new agent role | — | ADR-0026 §8.7 (accepted) |
| B-29 | Exact agent count 44 (§3) | N | Roster is versioned; count follows the universe and Method Library | ADR-0023 §6, §8 | ADR-0023 (accepted) |

### 1.3 Macro and asset-class (CMA) layer

| ID | ANG element | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-4 | Macro agent, 4 regimes, weighted scoring, web search (§2.1 S1) | G/D | Macro **role** kept. Regime method = RQ-11 (S9a). Deterministic fallback (R2). Web evidence is point-in-time, sourced and dated, with a mode stamp (DR-1, DR-5) | No methodological defaults; contamination (`S4_LIT_LOOKAHEAD`) | ADR-0023; S9a |
| B-5 | 18 AC agents, one per asset class (§2.1 S2) | G/D | AC-analysis role **per universe element**. Universe and allocation unit from S5 (UCITS implementation, research proxies) | Universe not yet chosen; may include the security domain | ADR-0024 §4; S5 |
| B-6 | 6 CMA methods + auto-blend in code; LLM judge bounded to [min, max] (§4) | U (structure) / D (enablement) | Same structure. Judge enablement = RQ-12. The judge's five rules are **not** adopted as defaults (ADR-0023 §8). The dispersion class becomes a code-computed descriptor | R1 derives from ANG | ADR-0023; S9b |
| B-30 | Non-equity CMA methods unspecified (ANG-28) | D | Per-family method sets (fixed income, cash, real assets) specified in S9b from primaries | Gap in ANG | S4.15 → S9b |
| B-31 | CMA units "%, nominal, 3-year" (USD implied) (§1) | A | **Every CMA declares** currency basis, hedging basis, horizon, arithmetic/geometric, nominal/real. Numéraire per RQ-07 (`INV.reporting_currency`, `INV.consumption_currencies`, `POL.currency_hedging`) **(ADR-0027 D5)** | D6: the numéraire changes portfolios | ADR-0027; S4.20; S5 |
| B-32 | AC agents' `signals.json` (momentum, trend, mean reversion, relative momentum) (§4) | G | Deterministic descriptors (ADR-0012), consumed by AC/CMA judgement within [min, max]; TSMOM/XSMOM as SIG-1/2 | ANG-23 | ADR-0026 §8.8–8.9 |

### 1.4 Risk layer

| ID | ANG element | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-7 | Covariance agent; estimator unspecified (§2.1 S3) | G/D | Risk **role**. Estimators are Method Library entries (COV-x) with eligibility contracts (06 §4). **Selection is per problem** (universe × horizon × risk object), not per PC method, on a pre-registered risk-accuracy test (ADR-0027 D3 r3, Option A; §13.2, §13.3; `S4_RISK_MODEL_CHOICE.md`) | ANG silent on the estimator; its ranking depends on dimension, constraints, horizon and use | S4.13 → S10; RQ-14 |
| B-33 | Three risk inputs: AC volatility, AC `correlation_row.json`, covariance agent Σ (ANG-33) | A | *(r3, Option A, 2026-10-08)* **One authoritative risk model per problem per run** (universe × horizon × risk object), produced by the risk role and consumed by every PC method on that problem, the CRO, limit checks, candidate cards, Portfolio Map and learning records. Estimator chosen per problem on a pre-registered risk-accuracy test (S7 → S10); method-internal regularisation stays in the methods; the CRO reports sensitivity to alternative estimators. AC-level volatilities and correlation rows are evidence, never PC inputs. Assembled matrices are symmetrised and projected to the nearest PSD correlation matrix **(ADR-0027 D3)** | ANG-consistent (pp. 6, 9); comparable candidates; one yardstick for limits; avoids per-method specification search | ADR-0027; S10 |
| B-34 | Short- vs long-horizon volatility via different estimators (p. 29) | G | The horizon is a **declared field** of every risk artefact, with one authoritative model per horizon. Short-horizon (CRO, volatility targeting, Trader evidence) and SAA-horizon Σ may differ (GARCH deviation share ≈ 0.07 over 3 y) | §13.2, C-2 | ADR-0026 §8 (descriptor horizon); S10 |

### 1.5 Portfolio construction

| ID | ANG element | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-8 | 19 fixed PC methods in 5 families (§3) | G | Same 19 as the reference registry **+ Simple and Anchored EPO** (B6/B7); heterogeneous typed contracts; allocation domains declared | Owner extension (roster v0 = 23) | ADR-0023 §6, ADR-0024 |
| B-9 | Researcher proposes a method; it enters the same run with CIO weight (§3) | A | Research lane DISCOVERED → … → ADMITTED; experimental runs allowed; **no production CIO weight before admission** | ADR-0005 funnel; ADR-0025 | ADR-0024 §1 (accepted) |
| B-10 | Adversarial Diversifier: max tracking variance vs centroid, s.t. Sharpe ≥ 75% of max (§3) | U (role) / G (formulation) | Role kept. Non-convex formulation completed in S4.14 (ANG-16); the 75% floor is not adopted | ANG under-specifies it | S4.14 |
| B-35 | PC inputs "CMAs + Σ" only (ANG-17) | G | Heterogeneous input contracts (caps, scenarios, paths, factors) | Methods need more than μ, Σ | S4.20 |
| B-17 | Single institutional pre-tax portfolio (§1) | A | PC at total-portfolio level on the admissible universe; accounts, asset location, tax and FX in S13a. Contracts allow PC-level or account-level constraints | Multi-account, tax-aware individual | S11/S13 |
| B-46 | Cash is one of the 18 asset classes; every PC method allocates to it; the final cash share emerges from the CIO ensemble (Exh. 9: 8.1%); the volatility band is soft and was missed (7.54% vs 8–12%) | A | Numéraire cash is the riskless asset (S46-D1). PC methods propose risky mixes; **one engine-level risk target and leverage rule** sets exposure: return-based methods along their frontier, others scaled, PC-A5 and methods with absolute risk limits internally; the CIO ensemble is rescaled to the target; cash placed at S13 | Tobin separation; candidates compared at equal risk; γ/δ not portable (X-10); cash rows in Σ degenerate (S4.5, S4.6 verified) | Owner decision S47-D6 (2026-10-08); binding by ADR at G4; S4.17, S4.18, S4.20, S7, S13 |

### 1.6 Strategy review and CIO

| ID | ANG element | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-11 | CRO: standard risk report; neutral; enforces hard constraints (§2.1 S5a) | U | Same. Diagnostics computed in code (R3), commentary by the agent. **Every diagnostic is defined by formula and named accurately**, e.g. ANG's "effective number of assets" = inverse HHI of weights, not Meucci's ENB (V-6) | R3; ANG-11 | S4.16 |
| B-36 | Candidate cards: 8 metrics cross-ranked (lecture; ANG-24) | G | **Candidate card = the R8 evidence object** for review and vote, computed deterministically | Separates evidence from the scoring composite | S4.16/S4.17 |
| B-12 | Peer review (1 intra + 1 inter), Borda + bottom flag, metric blend, diversity ≥ 3 of 5, top-5 revise (§2.1 S5b–e) | U (structure) / A (revision) | S12 baseline protocol. Revisions limited to ADR-0024 §2 categories. Assignment: balanced 2-in/2-out with forced pairs declared (ANG-36). Vote output contract (lecture schema). Weights (40/60), points and the diversity threshold are research objects. The protocol stays **replaceable** (DEL-1 … DEL-6; lecture s37 "moving beyond voting"; RQ-16) | R1; ADR-0023 §8 | S4.17 → S12 |
| B-37 | "Dissent reports" for bottom-voted methods (ANG-32) | G | Dissent is surfaced in the investment case (M8) with defined triggers | Visible dissent mitigates monoculture | S4.17 → S12, S14 |
| B-13 | CIO: single method or 7 ensembles; LLM-as-judge; six scoring dimensions (§2.1 S6) | U / A | Bounded choice among **code-computed** ensembles (R1); exact ensemble formulas in S4.18 (centroid membership, trimming, meta-optimiser). Six dimensions are candidate diagnostics; weights not adopted. **Final approval by the user** | R1, B-3 | S4.18 → S12 |
| B-38 | Runtime use of backtest Sharpe in metric score, CIO dimension and ensemble weighting (C-5) | A | Backtest diagnostics computed **deterministically under the S7-defined protocol** (window, costs, point-in-time universe), labelled in-sample, shown with their uncertainty; **never evidence for admission** and never a Method-Library selection criterion **(ADR-0027 D4)** | ANG-19; P13; D7 | ADR-0027; S7, S12 |

### 1.7 Downstream: rebalancing, implementation

| ID | ANG element | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-15 | Quarterly rebalancing plan + off-cycle drift triggers in the memo (§2.1 R) | D (methods) / A (ownership) | The rebalancing **rule** is part of the approved decision; its **determination** is a deterministic service; methods in S13b (RQ-44) | Rule ownership upstream | ADR-0026 §5.1–5.2 (accepted) |
| B-22 | "implemented through trading"; no trading role (§1) | G (extension) | Hybrid Trader + deterministic Execution; conditional tactical mandate; escalation edge | Individual needs accountable implementation | ADR-0026 §5–7 (accepted) |

### 1.8 Learning

| ID | ANG element | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-16 | Meta agent: forecast feedback (3-year rolling), edits skills, prompts, code; human approval above materiality (§2.1 M) | **A (adopted with guardrails)** | Learning **adopted as a core component** (owner priority). Learning objects captured from day one (DR-2). Rules **L-1 … L-7**: deterministic pre-registered evaluation; per-role deployment; diversity floor; correlation guardrail; judge ≠ author; clean window. Mandates never self-modified (ADR-0026 §4.4) **(ADR-0027 D1)** | ANG pillar; ANG-37 tension resolved by design | ADR-0027; S4.3, S8, S17 |
| B-39 | Registry evolution: add successful methods, **cull unsuccessful ones** (fn. 4 p. 9; p. 10) | A | Additions via the research lane (ADR-0024). **No automatic culling.** Evaluation informs CIO weighting (ADR-0025 axis). Retirement only by ADR (02 §D `RETIRED`) on admission failure or pre-registered evidence with multiple-testing control. A **family-coverage floor** is maintained **(ADR-0027 D2)** | Culling on noisy, short-horizon performance selects noise and erodes diversity (D7, D9, L-1) | ADR-0027; S7, S17 |
| B-40 | Learning metrics cover macro/AC only (ANG-31) | G | Learning objects extended to **PC methods** (deterministic evaluation records), **review/vote quality** (calibration of votes vs later outcomes), **CIO ensemble choices** and **CRO flags** | Owner: "agents must learn and evaluate PC methods" | S4.3 → S17 |
| B-41 | Lecture: improved skill deployed to every agent; test before ship (ANG-25) | A | Test-before-ship adopted (replay → shadow → promote/rollback). **Global deployment replaced by per-role promotion** with a diversity check | ANG-37; RQ-56 | S4_INPUTS §4.5; S17 |

### 1.9 Data, determinism, risks, evidence

| ID | ANG element | Class | Our form | Reason | Binding / stage |
|---|---|---|---|---|---|
| B-42 | Data skill FMP + Finviz; Bloomberg identifiers; US-listed universe (ANG-34) | A | Per-user credentials; licence class per source; ISIN/FIGI identity; point-in-time snapshots. FMP PARTIAL; Finviz N; EODHD, public and primary sources (S6 lead) | Licence and universe differ (UCITS, NOK) | DR-7; CB-19; S6 |
| B-43 | Computation in code; pinned model and sampling parameters; archived prompts, seeds, outputs (§6) | U | Same, plus model provenance incl. training cutoff (DR-9) and run manifest (04). ANG's model-risk mitigation — periodic revalidation against **a fixed test battery** (p. 25) — becomes the regression suite for model upgrades (DR-3) | Reproducibility; model drift | 04; DR-3; DR-9 |
| B-44 | Non-determinism; prospective evaluation; leakage mitigations (§6, §8) | U / G | Prospective evaluation (S7/S15); contamination diagnostics X-1 … X-5; mode stamp; R2 deterministic control | `S4_LIT_LOOKAHEAD` | S7, S8 |
| B-18 | Frontier LLMs + web search integral | A | Agent layer is the baseline. Deterministic-only is the R2 control and privacy fallback. Personal data reaches an LLM only with RQ-40 consent | Privacy (ADR-0014) | ADR-0023 §3 |
| B-21 | Heterogeneous foundation models vs correlated errors (§8) | D | Tested option (M5); error correlation measured (M6) | Kim et al. 2025: heterogeneity weaker than assumed | RQ-56; S7/S8 |
| B-45 | Security: sandboxing, privilege separation, auditor agents (§7) | G | Security requirements for S8, especially for any self-modification path | — | S8 |
| B-19 | Illustrative run (rankings, weights, regime call) (§9) | N | **Not evidence, not priors** | ANG's own caveat | ADR-0023 §9 (accepted) |

## 2. Conflicts: status after S4.2

| # | Status | Resolution |
|---|---|---|
| C-1 … C-4 | RESOLVED (ADR-0023/0024/0025) | — |
| C-5 Runtime backtest Sharpe | **Proposed resolution:** B-38 | ADR-0027 D4 |
| C-6 Meta-agent autonomous changes | **Proposed resolution:** B-16, B-39, B-41 (scope details remain S17) | ADR-0027 D1–D2; ADR-0026 §4.4 |
| C-7, C-8 | RESOLVED (superseded proposals) | Replaced by B-18 and by the S4 plan |
| C-9, C-10 | RESOLVED (ADR-0026) | — |
| **C-11 (new)** ANG culls methods on performance vs ADR-0025 (evaluation ≠ admission) and 02 §D (`RETIRED` by ADR only) | **Proposed resolution:** B-39 | ADR-0027 D2 |
| **C-12 (new)** ANG's three risk inputs vs one consistent risk model | **Proposed resolution:** B-33 (r3, Option A: one authoritative model per problem) | ADR-0027 D3 |
| **C-13 (new)** ANG's CMA unit and currency convention (USD implied) vs NOK context and D6 | **Proposed resolution:** B-31 | ADR-0027 D5; RQ-07 |
| **C-14 (new)** ANG's data stack (FMP, Finviz, US-listed ETFs) vs licence and universe findings | **Resolved by planning, no ADR needed:** B-42 | DR-7, CB-19, S6 |

No conflict with accepted S0–S3 content or ADR-0023 … ADR-0026 is introduced. ADR-0027 extends ADR-0023 §8 ("a learning loop with human approval above materiality") without contradicting it.

## 3. Disposition of the ANG issues (ANG-01 … ANG-37)

| Issues | Disposition |
|---|---|
| ANG-01, 09, 20, 32, 36 (review, vote, revision, dissent, assignment) | S4.17 → S12; B-12, B-37 |
| ANG-02, 14, 15, 16, 18, 22 (method objectives under-specified or ambiguous) | S4.5 – S4.14, per method, from primaries |
| ANG-03, 23, 28, 29 (CMA methods, signals) | S4.15 → S9b; B-6, B-30, B-32 |
| ANG-04, 33 (covariance plurality, three risk inputs) | B-7, B-33; ADR-0027 D3; S10 |
| ANG-05, 06, 07, 35 (naming, counts) | Recorded; no action |
| ANG-08 (CIO input set) | B-13: CIO combines all candidates (Exh. 8), revised and unrevised |
| ANG-10, 12, 13 (cited-source checks) | Verify when the primaries are read (S4.5, S4.14, S4.17) |
| ANG-11 (effective N) | Definition resolved (V-6); B-11 naming rule |
| ANG-17 (PC inputs) | B-35; S4.20 |
| ANG-19 (backtest vs "cannot be backtested") | B-38; ADR-0027 D4 |
| ANG-21 (Researcher in the same run) | ADR-0024 §1 (resolved) |
| ANG-24 … ANG-27 (lecture items) | B-36, B-41, B-26, B-27 |
| ANG-30 (Exhibit 1 vs text) | Text is authoritative; recorded |
| ANG-31, 37 (learning scope; learning × correlation) | B-16, B-39 … B-41; ADR-0027 D1–D2 |
| ANG-34 (data provenance) | B-42; S6 |

## 4. Proposed ADR-0027 (summary; full text in `decisions/`)

| # | Decision | Rows |
|---|---|---|
| D1 | Learning adopted as a core component under rules L-1 … L-7 | B-16, B-40, B-41 |
| D2 | Governed registry evolution: no automatic culling; retirement by ADR; family-coverage floor | B-39 |
| D3 | *(r3, Option A)* One authoritative risk model per problem (universe × horizon × risk object) per run; estimator selected on pre-registered risk accuracy; regularisation inside methods; CRO sensitivity report; AC-level risk outputs are evidence; PSD projection for assembled matrices | B-7, B-33, B-34 |
| D4 | Runtime backtest diagnostics are deterministic, protocol-defined, labelled in-sample, and never admission evidence | B-38 |
| D5 | Every CMA and risk artefact declares currency, hedging, horizon and return convention; numéraire per RQ-07 | B-31 |

## 5. Developer-facing summary (SYNC-1)

**Fixed now** (accepted ADRs; build as interfaces):
- **Roles and order:** macro → AC/CMA → risk → PC (parallel) → CRO → review/vote/revise → CIO → user approval.
- **Downstream extensions:** rebalancing determination → Trader → Execution.
- **Learning objects:** captured from the first slice.
- **Mandates and Decision Records** for every role.
- **Agent anatomy** (four components; dual contracts) and the R1/R8 boundary (numbers in code, cited by ID).

**Placeholders** (interfaces only until their stages decide):
- regime method;
- CMA methods and judge enablement;
- covariance estimators;
- every PC method's mathematics;
- review/vote mechanics and weights;
- ensemble formulas;
- rebalancing rules;
- learning thresholds.

**If ADR-0027 is accepted:** a risk-model artefact type with universe, horizon, risk-object, estimator and version fields (one authoritative model per problem per run); CMA unit fields; learning-promotion gates with a diversity floor and correlation guardrail; no auto-retirement path.

## 6. Exit check

| Criterion | Status |
|---|---|
| Every element of `S4_ANG_BASELINE.md` classified | §1: B-1 … B-45 (S4_PLAN §B rows retained; new B-24 … B-45) |
| Conflicts resolved or escalated | §2: C-1 … C-10 statuses; C-11 … C-14 new, with proposed resolutions |
| Issues dispositioned | §3: ANG-01 … ANG-37 |
| ADR drafted | ADR-0027 PROPOSED |
