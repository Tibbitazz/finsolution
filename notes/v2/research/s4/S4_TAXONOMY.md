# S4.3 — Canonical object taxonomy: kinds, types, identity, versioning

**Document status:** DRAFT for owner review (S4.3; exit = "every inventory item has one type"; **SYNC-2**) · **Prepared:** 2026-10-08 · **Entry:** S4.2 drafted (`S4_ANG_ADAPTATION.md`; ADR-0027 PROPOSED, D3 r3 decided by the owner) · **Basis:**
- ADR-0023 §5 (Method, Method Contract, Agent Role, Agent Instance, Portfolio Proposal);
- ADR-0026 §3 (adds Agent Mandate and Decision Record);
- ADR-0012 §1–§6 (descriptor classes, typed contracts);
- ADR-0024 §1–§5 (research lane, revision categories, parameter-authority classes, allocation domains, dual contracts);
- ADR-0025 (admission ≠ evaluation);
- ADR-0027 (PROPOSED): D1 learning objects; D3 risk-model artefact;
- 06 §1, §3, §5 (funnel, contract fields, `method_type`); 04 §1 (run manifest); ADR-0006, ADR-0019 and 03 (configuration, facts registries);
- S4_PLAN §G row S4.3 and §C.1 (status ladders).

**What this document is.** One vocabulary for every object the engine and its specification use. It feeds the Method Library and registry design (SYNC-2), the typed contracts (S4.20), the dependency graph (S4.22) and the Portfolio Map requirements (S4.25).

**What it is not:**
- not field schemas (S4.20) or storage design (S8);
- not mathematics (S4.5 onward) or method selection (S7–S12);
- not a change to any accepted ADR. Where it refines a term in an accepted document, it says so and the refinement takes effect only by annotation through an ADR.

---

## 1. Meta-model: six kinds

Every object has exactly **one kind** and **one type** within it. How an object is *used* (as an anchor, a benchmark, evidence) is a **relation** (§8), never a kind or a type.

| Kind | What it is | Test question | Mutability | Identity |
|---|---|---|---|---|
| **Method** (M) | A deterministic procedure that computes outputs from declared inputs, specified by a dual Method Contract (ADR-0024 §5). A method is never an LLM (ADR-0023 §5) | Does it compute an output by a fixed procedure? | ID immutable; contract versioned | Method ID (e.g. PC-B7) |
| **Artefact** (A) | An output produced inside a run by a method or a role, consumed downstream | Is it produced by the process and consumed later in the process? | Immutable; a revision is a new artefact | Content hash + run ID |
| **Role** (R) | An organisational position with an authority boundary, governed by an Agent Mandate and realised by Agent Instances (role ≠ runtime, ADR-0023 §2) | Does it decide, interpret or act under authority? | Mandate versioned; one active version | Role ID |
| **Control** (C) | A constraint, limit, benchmark, reference or criterion fixed in advance by a party other than the role it governs (ADR-0026 §4.1) | Is it a yardstick or boundary others are held to? | Versioned, effective-dated; changed only by owner or gate | Control ID + version |
| **Record** (REC) | An append-only account of something that happened: a decision, a claim, an outcome, a change | Does it log an event for accountability or learning? | Append-only; corrections are new records | Record ID |
| **Input** (IN) | Point-in-time data from outside the engine | Did it enter from outside, rather than being computed? | Snapshot | Snapshot content hash |

**Deviation from the outline given to the owner (five kinds).** Input is added as a sixth kind. Market-data, fact-registry and holdings snapshots are neither computed (Artefact) nor yardsticks (Control). Without the sixth kind the exit test fails (§13, F-10). **Owner confirmation requested (§15, O-1).**

**Governing specifications attach to the kind they govern:**
- the **Method Contract** belongs to Method;
- **Agent Mandate**, **Skill Version**, **Agent Memory State** and **Agent Instance** belong to Role;
- the **Policy Statement** is the container of user-authorised Controls.

---

## 2. Method types (the Method Library; plugin categories)

Method types partition by **output semantics and decision function**. They refine 06 §5's `method_type` values ({model, signal, transformation, aggregation, score→belief mapping, tactical rule}): "model" is split by function, the others map one to one. This is a refinement for the registry; 06 is not edited.

| Type | Definition | Members now (inventory) | Output | Owning stage | ANG counterpart |
|---|---|---|---|---|---|
| M.CMA | Produces a capital-market assumption per universe element (expected return; possibly volatility and confidence). Includes deterministic combinations of CMA methods | CMA-1 historical ERP + Rf; CMA-2 regime-adjusted; CMA-3 BL equilibrium; CMA-4 inverse Gordon; CMA-5 implied ERP (CAPE); CMA-6 survey/analyst; CMA-7 auto-blend | A.CMA | S4.15 → S9b | `cma_methods.py` (Exh. A.2, p. 39) |
| M.REGIME | Classifies or scores the macro state | ANG four-dimension scoring and four-regime classification (candidate, RQ-11) | A.REGIME | S4.15 → S9a | Macro agent code (p. 6) |
| M.SIGNAL | Return signal over time (S^TS) or across assets (S^CS) | SIG-1 XSMOM; SIG-2 TSMOM | A.DESCRIPTOR | S4.8 → S9 | `signals.json` |
| M.SCORE | Cross-sectional characteristic or score of securities (ADR-0012 §1) | SCORE-VAL (V0, V1); SCORE-MOM; SCORE-VAL-VC; DESC-V-EYEV; DESC-Q-ROCG, -GPA, -OP, -ROA, -FSCORE, -ACCR; DESC-REV and DESC-GROWTH-FWD (deferred) | A.DESCRIPTOR | S9c | — |
| M.TRANSFORM | Transformation of descriptor values (z-score, percentile, rank, quantile class, winsorisation) | RQ-29 grid | A.DESCRIPTOR | S9c | — |
| M.AGGREGATE | Explicit combination across signals or scores (RQ-32) | AGG-EYROC | A.DESCRIPTOR | S9d | — |
| M.MAPPING | Score → belief mapping (RQ-33) | None yet | A.CMA | S9d | — |
| M.RISK | Risk-model estimator for a declared problem (ADR-0027 D3) | COV-x: sample; Ledoit–Wolf (identity, constant-correlation, correlation-only targets); nonlinear shrinkage; RMT clipping and rotationally invariant estimators; EWMA; CCC/DCC/cDCC; factor models; nearest-PSD projection (repair) | A.RISK | S4.13 → S10 | Covariance agent (p. 6) |
| M.PC | Portfolio-construction method: maps declared inputs to a weight vector. Attribute `family` ∈ {A heuristic, B return-optimised, C risk-structured, D non-traditional, E agentic-context} | PC-A1 … A5, B1 … B7, C1 … C5, D1 … D4, E2; S4_PLAN §D.1 candidates at research-lane status | A.PROPOSAL | S4.5–S4.14 → S11 | Exh. 3 (p. 11) |
| M.DIAGNOSTIC | Computes a risk or quality diagnostic for a weight vector or a candidate | CRO metrics (ex-ante and backtest volatility, VaR, ES, maximum drawdown, concentration, effective N, tracking error, factor tilts); proposal distance; metric score; computable CIO dimensions | A.CRO_REPORT, A.CARD | S4.16 | CRO (p. 10); metric score (p. 12) |
| M.DELIBERATION | Deterministic parts of deliberation: reviewer assignment, ballot validation, tally, vote–metric blend, shortlist diversity rule | ANG modified Borda and blend (mechanics registered; values not adopted, ADR-0023 §8) | A.TALLY | S4.17 → S12 | pp. 11–12 |
| M.ENSEMBLE | Combines candidate portfolios into one, or selects one | ENS-0 single-method selection; ENS-1 simple average; ENS-2 inverse tracking error; ENS-3 backtest-Sharpe; ENS-4 meta-optimisation; ENS-5 regime-conditional; ENS-6 composite-score; ENS-7 trimmed mean | A.ENSEMBLE_CANDIDATE | S4.18 → S12 | CIO `script.py` (pp. 13–14) |
| M.REBALANCE | Deterministic rebalancing rule (T10) | RQ-44 candidates | REC.DECISION (determination) | S13b | "Quarterly with drift triggers" (p. 14) |
| M.IMPLEMENT | Implementation method (T5, T9) | Cost-aware; staged execution | A.PLAN | S13e | — (extension) |
| M.TIMING | Timing-evidence method (T3, T6, T8) | Registered families only | A.DESCRIPTOR | S13d | — |
| M.TACTICAL | Tactical policy over asset and holding state; conditional on RQ-17 (T11) | Registered families only | A.PLAN | S13c–d | — |
| M.EVALUATION | Evaluation, testing and attribution procedures | S7 protocols; scoring decision protocol D-1 … D-7; deflated Sharpe; model confidence set; spanning regressions; risk-model losses (`S4_RISK_MODEL_CHOICE.md`); attribution | REC.EVALUATION | S7, S14, S16 | Meta-agent metrics (p. 27) |
| M.ELIGIBILITY | Funnel predicates (FEASIBLE, ELIGIBLE) and admission checks | 06 §3 contract predicates | A.ELIGIBILITY_RESULT | S4.21 | — |

**Every method plugin declares** (06 §3; ADR-0024 §3–§5):
- type and, for M.PC, family;
- allocation domains;
- input artefact types and output artefact type;
- parameters with their authority class (fixed, system-estimated, user-authorised, agent-selectable, sensitivity-only);
- determinism (including seeds);
- Method Contract version.

---

## 3. Artefact types

| Type | Content | Producer | Main consumers |
|---|---|---|---|
| A.REGIME | Regime, confidence, dimension scores | Macro role via M.REGIME | AC/CMA role; CIO |
| A.CMA | Per universe element: per-method estimates, final estimate within [min, max], confidence, judge rationale, units (ADR-0027 D5) | AC/CMA role via M.CMA | PC methods; CRO; Forecast Records |
| A.DESCRIPTOR | Signal, score or timing-evidence values with provenance and staleness (ADR-0012 §2). Identity includes the comparison universe (`S4_SCORING_PEER_METHODS.md` §9, T-3) | M.SIGNAL, M.SCORE, M.TRANSFORM, M.AGGREGATE, M.TIMING | Methods via their contracts; evidence panels and packets |
| A.EVIDENCE_PANEL | Score table (security level) or asset-class evidence panel (`S4_SCORING_PEER_METHODS.md` §9) | Deterministic assembly from A.DESCRIPTOR, A.CMA, A.RISK | Dashboard; agents (via packets) |
| A.EVIDENCE_PACKET | Evidence given to one agent for one task: items, horizon, admitted uses (RQ-34; ADR-0026 §8) | Deterministic assembly | One role invocation |
| A.RISK | Risk model for one problem: universe, horizon, risk object, estimator (M.RISK ID and version), window, data snapshot, units, PSD distance; `authority` ∈ {authoritative, evidence} | Risk role via M.RISK | PC methods; CRO; limit checks; candidate cards |
| A.PROPOSAL | Weight vector plus justification. A revision is a new artefact that `supersedes` the old one and carries an ADR-0024 §2 revision category | PC role via M.PC | CRO; reviewers; CIO |
| A.RESEARCH_CANDIDATE | A method proposed in the research lane (ADR-0024 §1) | Researcher role | Research review; S4 lane |
| A.CRO_REPORT | Standardised risk report per candidate | CRO via M.DIAGNOSTIC | Reviewers; CIO; memo |
| A.CARD | Candidate card: metrics labelled in-sample with uncertainty, risk-model sensitivity line (ADR-0027 D3, D4) | M.DIAGNOSTIC | Reviewers; CIO; Portfolio Map |
| A.REVIEW | Peer review (structured fields plus text) | Reviewer role | Revision; vote; CIO |
| A.BALLOT | Vote ballot (top five, bottom flag, justifications) | Reviewer role | M.DELIBERATION |
| A.TALLY | Vote totals, composite ranking, shortlist, dissent reports | M.DELIBERATION | Revision; CIO; memo |
| A.ENSEMBLE_CANDIDATE | One ensemble's (or the single selection's) portfolio with diagnostics | M.ENSEMBLE | CIO |
| A.MEMO | Narrative artefact: AC investment-case memo (`analysis.md`), investment-case report / board memo (S14) | AC role; CIO | Investor; reviewers |
| A.PLAN | Implementation plan (Trader) or order set (Execution service) | M.IMPLEMENT, M.TACTICAL; Trader | Execution; post-trade |
| A.ELIGIBILITY_RESULT | Eligible and excluded sets with exclusion reasons (04 §1) | M.ELIGIBILITY | Run manifest; deliberation |

**All text artefacts written by agents** (memos, reviews, rationales) carry the run ID, model provenance (DR-9) and the list of descriptors cited (R8).

---

## 4. Role types and their specification objects

| Type | Definition | Members (S4_ACCOUNTABILITY §2) |
|---|---|---|
| R.HUMAN_AUTHORITY | Human authority with final approval | Investor |
| R.AGENT_ROLE | Deliberative or interpretive role; runtime may be agent, deterministic, human or hybrid | Macro/Regime; AC/CMA; Covariance/Risk; PC agent *k*; Researcher; Adversarial Diversifier; CRO; Peer reviewer; CIO; Tactical mandate (conditional); Trader; Monitoring/Attribution; Meta/Learning |
| R.SERVICE | Deterministic role with no discretion (ADR-0026 §5) | Rebalancing determination; Execution service |
| R.MANDATE | Agent Mandate: versioned contract governing one role (ADR-0026 §3) | One active version per role |
| R.SKILL | Skill Version: description, scripts, skills and output contract (ADR-0023 §8) | E.g. the CMA judge skill (Exh. A.2) |
| R.MEMORY | Agent Memory State: versioned store a role may read; part of the run manifest (`S4_INPUTS_2026-10-07.md` §4) | One per role instance lineage |
| R.INSTANCE | Agent Instance: deterministic code, pinned model, human or hybrid (ADR-0023 §5) | Runtime-specific |

---

## 5. Control types

| Type | Definition | Examples |
|---|---|---|
| C.POLICY_STATEMENT | Versioned container of the investor's declared constraints, targets and preferences (07; ADR-0008) | The local Policy Statement |
| C.CONFIGURATION | Configuration nodes: investor, goal/portfolio, account (ADR-0006 §1) | Account set; allocation-unit choice (S5) |
| C.CONSTRAINT | Hard deterministic predicate on weights, trades or agent outputs (ADR-0006 §7) | Long-only; caps; permitted instruments; the CMA judge's [min, max] bound |
| C.SOFT_TARGET | Target or band whose breach is flagged, not blocked | Volatility band; drawdown target (ANG p. 15) |
| C.LIMIT | Risk limit | Tracking-error limit; interim-risk limits set by the CRO (ADR-0026 §5) |
| C.BENCHMARK | Benchmark definition (policy or comparison benchmark; S4.10) | A 60/40 definition (ANG's; values not adopted) |
| C.REFERENCE | Reference-estimator, forecasting-reference or validation control (ADR-0026 §4.1) | The per-problem risk-model selection (ADR-0027 D3); forecasting references for CMAs |
| C.PROTOCOL | Pre-registered evaluation protocol and variant grid (S7; RQ-37) | Scoring protocol D-1 … D-7; risk-model selection rule |
| C.ADMISSION | Methodological admission criteria (ADR-0025) | The eight criteria in 06 §1 (annotation) |
| C.THRESHOLD | Materiality thresholds, promotion margins, hysteresis (S17; ADR-0027 L-4; RQ-21) | Learning promotion margin |
| C.GRANT | Authority grant (ADR-0017) | Permission to submit orders |

**Rule:** a control's value is never changed after the results it governs have been seen (ADR-0026 §4.1).

---

## 6. Record types

| Type | Content | Basis |
|---|---|---|
| REC.DECISION | Decision Record for a decision **or non-decision**. Subtypes: approved decision; rebalancing determination; implementation; order; authorisation; post-trade; escalation; promotion/rollback. Carries trace keys, inputs consumed with declared use, authority exercised, rationale and **decision state per transaction leg** (the seven no-trade concepts, one primary reason, owner, resolving condition) | ADR-0026 §9; S4_ACCOUNTABILITY §3, §5 |
| REC.RUN_MANIFEST | Run manifest; its hash is the run ID | 04 §1 |
| REC.FORECAST | Every quantitative claim (CMA, regime, signal direction, risk forecast) with horizon, timestamp, evidence IDs and run ID | `S4_INPUTS_2026-10-07.md` §4.3; ADR-0027 D1 |
| REC.OUTCOME | Realised value for a Forecast Record at its horizon (point-in-time) | Same |
| REC.EVALUATION | Result of an M.EVALUATION run: PC-method evaluation (ADR-0027 L-2), review and vote quality, CIO choice quality, CRO flag accuracy, risk-model losses, attribution | ADR-0027 D1; ANG-31 |
| REC.REFLECTION | Agent-written diagnosis of a trace and its outcome (text only) | `S4_INPUTS_2026-10-07.md` §4.3 |
| REC.CHANGE_PROPOSAL | Proposed modification: target, rationale, evidence, materiality class | Same; ADR-0027 L-6 |
| REC.TEST | Replay or shadow test of a change | Same; ADR-0027 L-5 |
| REC.EVIDENCE_USE | Per-consumer log of evidence used and its declared use | ADR-0026 §8 |
| REC.CHALLENGE | Agent challenge to a descriptor's applicability, attached to the cell or descriptor | ADR-0012 §5; `S4_SCORING_PEER_METHODS.md` §9 T-4 |

---

## 7. Input types

| Type | Content | Stage |
|---|---|---|
| IN.MARKET_DATA | Prices, returns, index levels, FX, rates (point-in-time snapshot) | S6 |
| IN.FUNDAMENTALS | As-filed company data (e.g. ESEF), with filing dates | S6 |
| IN.ESTIMATES | Point-in-time consensus estimates (deferred; S6 lead F-4) | S6 |
| IN.TEXT | Macro and news text, with leakage controls | S6 |
| IN.FACTS | Snapshot of the four facts registries (ADR-0019; 03) | S3 / S6 |
| IN.HOLDINGS | Positions, tax lots and cash per account | S6 / S13 |

---

## 8. Relations (edges for the S4.22 dependency graph)

| Relation | From → to | Example |
|---|---|---|
| produces | Method or role → artefact | M.RISK → A.RISK |
| consumes (declared use) | Method or role → artefact or input | PC-B1 consumes A.CMA as μ |
| configures | Configuration → method | Anchored EPO with a 1/N anchor |
| parameterises | Parameter value → method run | EPO shrinkage w |
| governs | Mandate → role; control → method or role | Tracking-error limit → CIO |
| realises | Instance → role | Pinned model → CRO role |
| evaluates | Evaluation record → method or role | PC-method evaluation |
| supersedes | Artefact or record → earlier version | Revised proposal → original |
| cites | Text artefact → descriptor | R8 citation |
| anchors | Anchored-EPO configuration → weight artefact or benchmark | PC-B7 → PC-A1 output |
| benchmarked_against | Portfolio or evaluation → benchmark control | Candidate → policy benchmark |
| records | Record → artefact or decision | Forecast Record → A.CMA |

---

## 9. Method vs configuration vs parameter (and variant)

| Concept | Definition | Test | Examples |
|---|---|---|---|
| **Method** | A procedure whose objective, constraint *form* and algorithm are fixed by its primary source | Changing it changes the mathematics as the source defines it → **a different method** (new ID) | Simple EPO (PC-B6) vs Anchored EPO (PC-B7); GMV vs ERC |
| **Configuration** | The declared bindings that instantiate a method for a use: allocation domain and universe, which A.CMA / A.RISK / descriptors it consumes, anchor source, benchmark, the Policy Statement constraint set | Changing what the method is applied to or bound to → **same method, new configuration** | PC-B7 anchored to 1/N vs to benchmark weights; SCORE-VAL over a global vs a Nordic universe |
| **Parameter** | A value inside the method's declared parameter space, with an authority class (ADR-0024 §3) | Changing a value inside the declared space → **same method and configuration, new parameter value** | EPO shrinkage w; Black–Litterman τ; HRP linkage; resampling count and seed; shrinkage intensity (system-estimated) |
| **Variant** | A named, pre-registered configuration plus parameter set | Counts as a separate trial for multiple-testing control (S7; RQ-37) | SCORE-VAL V0 and V1; the O-1 … O-10 grid |

**Edge rules:**
1. A correction of an implementation error that restores the source's mathematics is not a new method. It is a logged correction with fixture evidence (S4.24).
2. Combining two methods (e.g. an ensemble, an auto-blend) is a method of its own type. It is not a configuration of its parts.
3. Artefact identity includes configuration (e.g. a descriptor over another comparison universe is a different descriptor ID), while the method ID stays the same.

---

## 10. Identity and versioning

| Kind | ID form | Versioning | Who may change | Retirement |
|---|---|---|---|---|
| Method | Existing schemes kept: PC-, SIG-, SCORE-, DESC-, AGG-, COV-, EQ-. New, assigned at the owning stage: CMA-1 … 7, ENS-0 … 7, DIAG-, DELIB-, REB-, IMPL-, TIME-, TAC-, EVAL-, ELIG-, MAP- | ID immutable. Method Contract vMAJOR.MINOR: MAJOR when a machine-contract field changes (inputs, outputs, parameters, domains); MINOR for agent-readable text. Implementation tracked by code commit in the run manifest | Research lane (ADR-0024 §1); gate process | By ADR only (02 §D; ADR-0027 D2); IDs never reused |
| Configuration | Hash of method ID + contract version + bindings + parameter values; variants get names | New hash on any change | Per parameter-authority class | Archived with runs |
| Artefact | Content hash + run ID | Immutable; revision = new artefact with `supersedes` and a reason | Producing role, within its mandate | Never deleted while a record references it |
| Role | Role ID | Mandate versions (one active, ADR-0026 §3); skill versions and memory states referenced in the run manifest | Owner (mandates never self-modified, ADR-0026 §4.4) | By ADR |
| Control | Control ID + version + effective date | New version per change | Owner or gate (07; ADR-0026 §4) | Superseded, never deleted |
| Record | Record ID | Append-only; corrections are new records referencing the original | Creating role or service | Never |
| Input | Snapshot content hash | New snapshot per as-of | Data pipeline (S6) | Retained per S6 policy |

**Type IDs** (M.PC, A.RISK, …) are distinct from object IDs (PC-B1, COV-3, …) and use dotted notation to avoid collisions with existing hyphenated IDs (conflicts C-x, rules R1 … R8, checks R-1/R-2).

---

## 11. Status ladders by kind

| Kind | Ladder |
|---|---|
| Method | S4_PLAN §C.1 ladders (PC method, signal, upstream method, ensemble); research lane `DISCOVERED → … → ADMITTED` (ADR-0024 §1); runtime funnel `FEASIBLE → ELIGIBLE → ADMISSIBLE → DELIBERABLE` (06 §1 with the ADR-0025 annotation); `RETIRED` by ADR |
| Role | §C.1 agent-role ladder (ending in mandate stub) |
| Control | `DRAFT → ACCEPTED → EFFECTIVE → SUPERSEDED` |
| Artefact | `VALID → STALE` (ADR-0012 §2) `→ SUPERSEDED` |
| Record | None (immutable) |
| Input | Snapshot validity per S6 |

---

## 12. Inventory pass (exit test: every item has exactly one type)

### 12.1 Method Library and upstream inventory

| Items | Type | Note |
|---|---|---|
| PC-A1 … A5, B1 … B7, C1 … C5, D1 … D4 (21) | M.PC | Families A–D |
| PC-E2 Adversarial Diversifier (its optimisation) | M.PC | Family E; the agent role is a separate item (§12.2) |
| PC-E1 Researcher | R.AGENT_ROLE | **Not a method** (F-1) |
| §D.1 candidate additions (7) | M.PC | At research-lane status, not admitted |
| SIG-1, SIG-2 | M.SIGNAL | |
| SCORE-VAL, SCORE-MOM, SCORE-VAL-VC; DESC-* (9) | M.SCORE | DESC-REV and DESC-GROWTH-FWD deferred |
| AGG-EYROC | M.AGGREGATE | |
| RQ-29 transformations | M.TRANSFORM | |
| CMA-1 … CMA-6 | M.CMA | |
| CMA-7 auto-blend | M.CMA | Combination of CMA methods (F-4) |
| CMA judge | R.SKILL | A skill of the AC/CMA role, bounded by a C.CONSTRAINT (F-7) |
| ANG regime classification | M.REGIME | Candidate (RQ-11) |
| Covariance estimators (S4.0 §6; baseline §13.2; `S4_RISK_MODEL_CHOICE.md` §3) | M.RISK | |
| CRO metrics; metric score; computable CIO dimensions | M.DIAGNOSTIC | ANG's CIO weights not adopted |
| Reviewer assignment; Borda tally; vote–metric blend; shortlist diversity rule | M.DELIBERATION | |
| Seven ensembles + single-method selection | M.ENSEMBLE | ENS-0 … 7 |
| Rebalancing rule (ADR-0026) | M.REBALANCE | |
| Implementation method (ADR-0026) | M.IMPLEMENT | |
| Timing-evidence method (ADR-0026) | M.TIMING | |
| Tactical policy (ADR-0026, conditional) | M.TACTICAL | |
| Meta-agent metrics; S7 evaluation designs; D-1 … D-7 | M.EVALUATION | |
| Funnel predicates | M.ELIGIBILITY | |

### 12.2 Process artefacts, roles, controls, records, inputs

| Items | Type | Note |
|---|---|---|
| `macro-view.json` | A.REGIME | |
| `cma_methods.json`, `cma.json` | A.CMA | |
| `scenarios.json` | A.CMA | Content unspecified in ANG; provisional |
| `signals.json`, `historical_stats.json` | A.DESCRIPTOR | |
| AC volatility estimate; `correlation_row.json` | A.RISK (`authority = evidence`) | ADR-0027 D3.6 (F-8) |
| Covariance matrix Σ | A.RISK (`authority = authoritative`) | |
| `analysis.md` (AC memo); board memo / investment-case report | A.MEMO | |
| Score table; asset-class evidence panel | A.EVIDENCE_PANEL | |
| Evidence packet (ADR-0026) | A.EVIDENCE_PACKET | |
| Proposals; revised proposals | A.PROPOSAL | |
| Researcher's proposed method | A.RESEARCH_CANDIDATE | |
| CRO report | A.CRO_REPORT | |
| Candidate card | A.CARD | |
| Reviews (42 in ANG) | A.REVIEW | |
| Ballots | A.BALLOT | |
| Vote totals; composite ranking; shortlist; dissent reports | A.TALLY | |
| Ensemble portfolios | A.ENSEMBLE_CANDIDATE | |
| Implementation plan; order set | A.PLAN | |
| Eligibility result | A.ELIGIBILITY_RESULT | |
| Investor | R.HUMAN_AUTHORITY | |
| Macro/Regime; AC/CMA; Covariance/Risk; PC agent *k*; Researcher; Adversarial Diversifier; CRO; Peer reviewer; CIO; Tactical mandate; Trader; Monitoring/Attribution; Meta/Learning | R.AGENT_ROLE | |
| Rebalancing determination; Execution service | R.SERVICE | |
| Agent Mandate | R.MANDATE | |
| Skill Version | R.SKILL | Learning object, but a specification, not a record (F-5) |
| Agent Memory State | R.MEMORY | Same (F-5) |
| Agent Instance | R.INSTANCE | |
| Policy Statement | C.POLICY_STATEMENT | |
| Investor, goal/portfolio and account nodes | C.CONFIGURATION | |
| Hard bounds; permitted instruments; judge bound [min, max] | C.CONSTRAINT | |
| Volatility band; drawdown target | C.SOFT_TARGET | |
| Tracking-error limit; interim-risk limits | C.LIMIT | |
| Policy and comparison benchmarks | C.BENCHMARK | Benchmark weights and returns are IN or A (F-3) |
| Per-problem risk-model selection; forecasting references | C.REFERENCE | ADR-0027 D3; ADR-0026 §4.1 |
| Evaluation protocols; variant grids | C.PROTOCOL | |
| Admission criteria | C.ADMISSION | |
| Materiality thresholds; promotion margins; hysteresis | C.THRESHOLD | |
| ADR-0017 grants | C.GRANT | |
| Decision Record; approved-decision, determination, implementation, order, authorisation, post-trade records; Promotion/Rollback Decision | REC.DECISION | Promotion/rollback is a subtype (F-5) |
| Decision state; the seven no-trade concepts | Field of REC.DECISION | Not objects (F-6) |
| Run manifest | REC.RUN_MANIFEST | |
| Forecast Record | REC.FORECAST | |
| Outcome Record | REC.OUTCOME | |
| Learning records for PC methods, review/vote, CIO and CRO (ADR-0027 D1) | REC.EVALUATION | |
| Reflection | REC.REFLECTION | |
| Change Proposal; meta-agent change log | REC.CHANGE_PROPOSAL | |
| Replay / Shadow Test | REC.TEST | |
| Consumer log | REC.EVIDENCE_USE | |
| Agent challenge note | REC.CHALLENGE | |
| Market data; fundamentals; consensus estimates; text; facts snapshot; holdings | IN.MARKET_DATA; IN.FUNDAMENTALS; IN.ESTIMATES; IN.TEXT; IN.FACTS; IN.HOLDINGS | |

### 12.3 Families and specification objects (not engine objects)

| Items | Treatment |
|---|---|
| Downstream families T1–T12 (`S4_DOWNSTREAM_INVENTORY.md`) | A family is **not an object**. Each registered member is typed by its placement (F-9): T1 → M.SIGNAL, M.TIMING or M.TACTICAL; T2 → M.SIGNAL; T3 → M.TIMING or M.TACTICAL; T4 → M.PC (PC-A5) or M.TACTICAL; T5 → M.IMPLEMENT; T6 → M.TIMING or M.REGIME; T7 → C.CONSTRAINT; T8 → M.TIMING; T9 → M.IMPLEMENT; T10 → M.REBALANCE; T11 → M.TACTICAL; T12 → M.EVALUATION |
| ADRs, RQs, ANG issues, carried gating items (CB), conflicts (C-x), developer requirements (DR), sources, Equation Register entries (EQ) | **Specification objects**, outside the engine object model: they live in the specification repository, not in a runtime registry. Types SPEC.ADR, SPEC.RQ, SPEC.ISSUE, SPEC.CB, SPEC.CONFLICT, SPEC.REQUIREMENT, SPEC.SOURCE, SPEC.EQUATION. An EQ entry is a component referenced by a Method Contract (O-4) |

**Result:** every item in the S4 inventory, the roster, the upstream and downstream inventories, the ADR-0026/0027 objects and the ANG pipeline has exactly one type. Ten findings arose in the pass (§13).

---

## 13. Findings from the inventory pass

| # | Finding | Resolution in this taxonomy | Effect elsewhere |
|---|---|---|---|
| F-1 | **PC-E1 Researcher is a role, not a method.** Roster v0's 23 entries are 22 methods and 1 role | Typed R.AGENT_ROLE; its outputs are A.RESEARCH_CANDIDATE | No roster change. ADR-0023 §6's invariant is parallel heterogeneous proposals; ANG also lists the Researcher among PC agents. G4 conformance counts are unaffected |
| F-2 | **"Anchor" is a use, not a method type.** An anchor is a weight artefact (from any M.PC) or a benchmark control bound to PC-B7 by configuration | Relation `anchors` (§8); no anchor type | S4.10 should speak of "anchor source" rather than "anchor method" |
| F-3 | **"Benchmark" has two objects:** the definition (C.BENCHMARK) and its weights and returns (IN or A) | Split | S4.10 |
| F-4 | **ANG's auto-blend is a CMA method**, a combination of CMA methods, not an across-signal aggregation | M.CMA (combination subtype) | S4.15 |
| F-5 | **Learning objects span three kinds:** six are records; Skill Version and Agent Memory State are role specifications; Promotion/Rollback Decision is a Decision Record subtype | As typed in §4 and §6 | S8 storage design (DR-2) |
| F-6 | **Decision states (no-trade concepts) are fields, not objects** | Enumerated per-leg field of REC.DECISION | S8/S13 encoding |
| F-7 | **The CMA judge is a skill of the AC/CMA role**, bounded by a control | R.SKILL + C.CONSTRAINT | S9b |
| F-8 | **AC volatility estimates and correlation rows are risk artefacts with evidence authority** | A.RISK, `authority = evidence` | ADR-0027 D3.6 |
| F-9 | **Downstream families are not objects** | Members typed by placement | S4.15b; S13 |
| F-10 | **Data and fact snapshots fit no kind of the five-kind outline** | Sixth kind Input | Owner confirmation (O-1) |

---

## 14. SYNC-2: what the developer can design now

**Registries follow the kinds:**

| Registry | Holds | Properties |
|---|---|---|
| Method Library | Method types (§2) as plugin categories; Method Contracts | Versioned contracts; research lane; funnel status |
| Artefact store | Artefact types (§3) | Content-addressed, immutable, typed, linked by `supersedes` |
| Role registry | Roles, mandates, skill versions, memory states, instances (§4) | One active mandate per role; runtime adapters (deterministic, LLM, human, hybrid) |
| Control registry | Control types (§5) | Versioned, effective-dated; owner/gate changes only |
| Record log | Record types (§6) | Append-only |
| Input snapshots | Input types (§7) | Content-hashed, point-in-time |

**Fixed now for design:** the six kinds, the type lists, the relations (§8) and the identity rules (§10).

**Deferred:**
- field schemas → S4.20;
- storage and technology → S8;
- the membership of each type → owning stages (S4.5 onward, S9–S13).

---

## 15. Exit check and open items

| Criterion (S4_PLAN §G row S4.3) | Status |
|---|---|
| Canonical object types for CMA/belief, signals, risk/covariance, PC families A–E, anchors, benchmarks, constraints, CRO diagnostics, deliberation, CIO ensembles, rebalancing, implementation | §2–§5 (anchors as a relation, F-2) |
| ADR-0026 objects: evidence packet, Agent Mandate, Decision Record, decision state, rebalancing rule, implementation method, timing-evidence method, tactical policy | §3–§6, §12 |
| Learning objects (amendment 15) and candidate card | §4, §6 (F-5); A.CARD |
| ADR-0027 additions: risk-model artefact; learning objects for PC methods, review/vote, CIO and CRO; score table | A.RISK; REC.EVALUATION; A.EVIDENCE_PANEL |
| Method vs configuration vs parameter; identity and versioning | §9, §10 |
| Every inventory item has one type | §12; findings F-1 … F-10 |

**Open items for the owner:**
- **O-1:** confirm six kinds (Input added; F-10).
- **O-2:** confirm F-1 (the Researcher typed as a role; roster numbering unchanged).
- **O-3:** ID prefixes for new method types are assigned at their owning stages (§10). Confirm that no IDs need assigning now.
- **O-4:** whether specification objects (§12.3) need a registry beyond the repository. Recommendation: no; the repository is their registry.
