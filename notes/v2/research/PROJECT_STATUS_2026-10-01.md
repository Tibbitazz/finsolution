# Project status review — S0 to S18 (snapshot 2026-10-01)

**Document status:** SNAPSHOT dated 2026-10-01 (informational; not a specification; not rewritten later). *Post-snapshot note: G3 closed the same day and ADR-0022 introduced parallel Track A/Track B; see 08_ROADMAP for the current plan.* · **Sources:**
- [08_ROADMAP](../08_ROADMAP.md)
- [decision register](../decisions/README.md)
- [OPEN_QUESTIONS](OPEN_QUESTIONS.md)
- gate artefacts S1–S3
- git tags `gate-G0`, `gate-G1`, `gate-G2`
- branch `stage/s03-external-facts`

## A. Completed stages

| | **S0 / G0** | **S1 / G1** | **S2 / G2** |
|---|---|---|---|
| Objective | Charter and decision governance; source of truth | Reusable Investor Profile & Policy Statement **input specification** (not a personal profile) | Configuration machinery implementing the S1 contract |
| Principal outputs | 00–09 governing documents; decision register; RQ register; REF-01 paper memo; facts README | S1_INPUT_SPECIFICATION (data classes A–E, field schema, activation, value origins, field inventory, interaction model, Declared → Effective, propagation, extensibility); fixtures FX-01 … 18 | S2_CONFIGURATION_MACHINERY; S2_RISK_PREFERENCE_RESEARCH; fixtures FX2-01 … 20; S2_G2_DECISIONS |
| Major architectural decisions | v2 is source of truth, legacy superseded; gate workflow; separate evidence/status vocabularies; layer model and deterministic/agent boundary (R1–R8); eligibility funnel Feasible → Eligible → Admissible → Deliberable; configuration hierarchy and versioned registries; brokers Nordnet + eToro, continuous capital; "Policy Statement"; beliefs ⊥ preferences; risk preference ≠ model parameters; roadmap S0–S18; signal & scoring architecture (score ≠ belief); declared comparison universe | Reusable engine with private, git-ignored local user layer; Declared never rewritten; precedence decides implementability only; purpose limitation; capability vs. activation; value origins; portability | Immutable typed versions with units; constraint hardness; resolution invariants; finding records (I1–I3, T1, T2, F1); ordered alternatives as metadata; stage-separated authority model (8 logical grants; analytical ≠ decision ≠ execution); declared-read dependency graph; risk ontology (γ never portable); schema evolution |
| Accepted ADRs | 0001–0013 | 0014 | 0015–0018 |
| RQs | None resolved (S0 registered RQ-01 … RQ-38) | Resolved: RQ-01, RQ-02a. Added RQ-39 … RQ-47; RQ-48 added at G1 | Resolved: RQ-02b/c, RQ-23, RQ-41 (governance), RQ-47 (policy), RQ-48 (mechanism). Deferred: RQ-02d → S11; RQ-41 contents → S3–S5; RQ-47 tooling → S8. Added RQ-49, RQ-50 |
| Gate / merge / tag | PR #1 merged `cfa68fd`; tag `gate-G0` | PR #2 merged `92b2af2`; tag `gate-G1` | PR #3 merged `2ab6c11`; tag `gate-G2` |

## B. Current stage — S3 External-facts research

| Item | Status |
|---|---|
| Completed | Registry architecture (record contract; bitemporal semantics; uncertainty; admissibility layers; W1–W9; instrument-type schema; RegRule/BrokerImplementation; re-check policy; jurisdiction process; option sources; comparison specification); research findings; registry v1; fixtures; G3 package (revision 2); ADR-0019 PROPOSED; ADR-0020 and ADR-0021 ACCEPTED |
| Research performed | Norwegian income taxation 2026, ASK (Skatteetaten, Skatte-ABC 2025/2026 A-10 and U-20), fund taxation, credit deduction, exit tax; US withholding (IRS, treaty, W-8BEN); PRIIPs (Regulation, PRIIPs-loven, forskrift, Finanstilsynet); MiFID II / vphl definitions; CFD measures; ESMA advice briefing; Nordnet and eToro official pages |
| Registries | 6 provisional files, 83 records: Norway tax (9), wrappers (15), US→NO withholding (10), regulation (14), Nordnet (16), eToro (19) |
| Fixtures | FX3-01 … FX3-26 |
| Unresolved | Class A: 7 items. Class B: 13 items in 8 groups gated to S5/S6/S13a/S13e/S13f/S11/S14. **Class C: none** (S3_FINDINGS §10) |
| Corrections from the G3 review | All applied in revision 2 (wealth-tax removal; ASK credit; D3-07; D3-08; RQ-49 register; PRIIPs chain; eToro re-check; unknown ≠ unsupported audit; A/B/C; acceptance meaning) |
| Required before G3 closes | Owner approval of D3-01 … D3-13 and the five confirmations in S3_G3_PACKAGE ("Owner decisions still required"); then PR → merge → tag `gate-G3` |

## C. Remaining roadmap

| Stage | Purpose | Major dependencies | Principal unresolved questions | Expected gate / output |
|---|---|---|---|---|
| **S4** Method Library & Eligibility | Remove infeasible methods before comparison | G2 (contracts, graph), G3 (facts as feasibility inputs) | Contract schema completion; reason codes; provisional policy; hysteresis (RQ-21); descriptor taxonomy (RQ-27) | G4: eligibility framework spec; candidate method inventory with contract status |
| **S5** Feasible universe & allocation unit | What we allocate across | G3 (legal, wrapper, broker layers), S4, S6a | Universe, geography, allocation unit, currency policy (RQ-07); comparison universe (RQ-38); third-country fund access (U9) | G5: universe spec; allocation hierarchy; instrument-master scope |
| **S6a** Data feasibility | Can the data support the universe and methods? | S5 (iterates with it) | Vendor coverage (RQ-08) | Input to G5 |
| **S6b** Data architecture & registries | Point-in-time data and registry storage | S5, S6a, ADR-0019 | Vendors, survivorship, FX/risk-free sources, leakage controls, registry storage (RQ-08); instrument attributes incl. `kid_norwegian_compliant_available` and fund-level withholding (RQ-51) | G6: data contracts, quality checks, registry storage design |
| **S7** Evaluation & backtest protocol | Fix how methods are judged before results | S6b | Walk-forward design, holdout, benchmark, multiple testing (RQ-09); control baseline (RQ-25); statistical power (RQ-26); signal-evaluation design (RQ-37) | G7: pre-registered protocol and harness spec |
| **S8** Platform architecture (branch B) | Method-agnostic platform | G2 (can run in parallel) | Stack, agent anatomy, LLM pinning (RQ-10); local workspace and encryption (RQ-39); personal-data flow to external services (RQ-40); portability (RQ-43); evidence packets (RQ-34); asset-state abstraction (RQ-36); implementing `Fact(t \| k)` | G8: architecture and stack ADR |
| **S9** Beliefs & signals | Expected returns, regime, cross-sectional descriptors, score → belief mapping | S4, S5, S6, S7 | Regimes (RQ-11); CMAs and LLM judge (RQ-12); signals (RQ-13, RQ-27 … 31); aggregation architecture (RQ-32); score → use mapping (RQ-33) | G9: method specs with typed contracts; mapping specs |
| **S10** Risk model | Σ, downside, stress | S6, S7 | Estimators; RMT/high-dimensional eligibility region in (N, T_eff), pre-registered threshold (RQ-14) | G10: risk spec; RMT region or "not eligible at our scale" |
| **S11** Portfolio construction & risk calibration | Competing methods from the admissible set | S9, S10, S4 | Method set and constraints (RQ-15); model-specific risk calibration vs. selection from an opportunity set (RQ-02d); elicitation validation (RQ-50); signal consumption (RQ-33); capacity-based hard constraints (D2-10); RQ-49 presentation of target portfolios | G11: method registry; calibration spec |
| **S12** Deliberation & aggregation | One target portfolio | S11 | Whether deliberation adds value; ensemble rules; deterministic control (RQ-16); evidence packets and rule R8 (RQ-34) | G12: aggregation spec |
| **S13** Implementation & tactical | Target → per-account trades | S12; registries (G3) | 13a costs/tax/FX/asset location (RQ-18; ASK credit mechanics U4; RQ-51; RQ-46); 13b rebalancing taxonomy and parameter authority (RQ-44); 13c tactical role (RQ-17); 13d tactical agents and time-series candidates (RQ-35); 13e sizing; 13f execution per broker (RQ-19), authority safeguards for grants 6–8 (ADR-0017), RQ-49 for execution | G13a–d: ADRs; per-account trade-list contract; execution protocol |
| **S14** Investment-case report & approval | Explain before execution | S13 | Report contents and approval workflow (RQ-20); RQ-49 presentation constraints; possible consumers of field 1.7 (RQ-45) | G14: report template; approval workflow |
| **S15** Full-system validation | Go/no-go | S7 protocol, S14 | Acceptance criteria; power (RQ-26); elicitation validation (RQ-50) | G15: validation report, go/no-go |
| **S16** Monitoring | Stay within the Policy Statement | S15 | Alert thresholds; hysteresis (RQ-21); fact staleness operations | Monitoring spec |
| **S17** Learning & controlled improvement | Improve without silent drift | S16 | Meta-agent permissions; materiality (RQ-22) | G17: model-governance spec |
| **S18** Developer handoff | Buildable sequence | Accepted specs | Slice order (first slice: Policy Statement editor, registries, Feasibility Engine with exclusion report, one deterministic path to a report) | Build plan |

## D. Cross-stage open issues

| Issue | RQ | Responsible stage(s) |
|---|---|---|
| Risk calibration (model-specific; calibration vs. selection from opportunity set) | RQ-02d | S11 (with S15 validation) |
| Rebalancing taxonomy and parameter authority | RQ-44 (with RQ-18) | S13b |
| Investment experience vs. appropriateness | RQ-45 | Open beyond G3; consumers researched by S14 at the latest |
| Anticipated residence change | RQ-46 | S13a (field stays conditional) |
| Regulatory implications of the application | RQ-49 | Open beyond G3; S11/S14 (recommendation framing), S13f (execution) |
| Risk-elicitation validation | RQ-50 | S11, S15 |
| Fund-level withholding | RQ-51 | S6 (instrument attributes), S13a |
| Tactical-layer role | RQ-17 (RQ-35) | S13c–d |
| Scoring → beliefs / expected returns | RQ-32, RQ-33 (RQ-27 … 31, RQ-38) | S9d, S11, S12 |
| RMT eligibility and calibration | RQ-14 | S10 |
| External-data and privacy architecture | RQ-39, RQ-40, RQ-43 (RQ-08 for vendors) | S8 (S6b for data) |
| Eligibility hysteresis and monitoring thresholds | RQ-21 | S4, S16 |
| ASK credit mechanics | U4a–e | S13a |

## E. Scope exclusions (current project)

| Exclusion | Basis |
|---|---|
| All pension saving and pension products (IPS, EPK, any pension wrapper), pension wealth, pension taxation, pension total-wealth treatment | ADR-0008, ADR-0020 |
| Wealth tax: facts, fields, calculations, effects in comparison or construction; `TAX.wealth_tax_position` retired | ADR-0021 |
| Broker-routing optimisation (architecture must permit it later) | Charter §2; ADR-0006 |
| Portfolio-size categories / buckets (capital is continuous) | ADR-0007; 03 §4.6 |
| Legacy (ENGINE_V1) values or claims as inputs | ADR-0001; 03 §4.5 |
| A universal risk-category → γ mapping; γ as a portable investor attribute; a single global γ | ADR-0010, ADR-0018 |
| Preferences altering beliefs (except the declared horizon exception) | ADR-0009, ADR-0013 |
| Personal data in the public repository; real profiles as defaults or fixtures; technical defaults for personal fields | ADR-0014 |
| Cross-purpose use of personal fields (e.g. age as an investment signal) | ADR-0014 §8 |
| Implicit substitution of undeclared alternatives | ADR-0016 |
| Execution-related authority before S13 safeguards (gated, not excluded) | ADR-0017 |
| Self-reported experience as an eligibility grant; engine-run substitutes for broker tests | D3-07 (proposed at G3) |
| Broker or account ranking, "best" labels, cost-sorted defaults | D3-09 (proposed at G3) |
| Individual-security master in S3 (deferred to S6, not excluded) | D3-d |

## F. Progress snapshot

| Stage | Status | Gate | Main result | Next dependency |
|---|---|---|---|---|
| S0 | Closed | G0 ✓ (`gate-G0`) | Governance, ADR-0001 … 0013, roadmap | — |
| S1 | Closed | G1 ✓ (`gate-G1`) | Reusable input specification, FX-01 … 18, ADR-0014 | — |
| S2 | Closed | G2 ✓ (`gate-G2`) | Configuration machinery, FX2-01 … 20, ADR-0015 … 0018 | — |
| S3 | At gate (revision 2) | G3 pending | Registry architecture, registry v1 (83 records), FX3-01 … 26, ADR-0019 (proposed), ADR-0020/0021 | Owner approval → PR → tag |
| S4 | Not started | G4 | — | G3 |
| S5 | Not started | G5 | — | G3, S4, S6a |
| S6a | Not started | (G5) | — | S5 |
| S6b | Not started | G6 | — | S5, S6a |
| S7 | Not started | G7 | — | S6b |
| S8 | Not started (may run in parallel from G2) | G8 | — | G2 (G3 for registry service) |
| S9 | Not started | G9 | — | S4–S7 |
| S10 | Not started | G10 | — | S6, S7 |
| S11 | Not started | G11 | — | S9, S10 |
| S12 | Not started | G12 | — | S11 |
| S13 | Not started | G13a–d | — | S12, G3 |
| S14 | Not started | G14 | — | S13 |
| S15 | Not started | G15 | — | S14, S7 |
| S16 | Not started | — | — | S15 |
| S17 | Not started | G17 | — | S16 |
| S18 | Not started | — | — | Accepted specs (first slice can begin once G3 and G8 exist) |

**Where we are:**
- The governing, input, configuration, and external-fact layers are specified. S0–S2 are accepted; S3 is at its gate.
- No methodological question has been decided yet: no universe, data, evaluation protocol, beliefs, risk model, construction, or implementation methods.
- Before the application can be implemented and validated, the remaining work is S4–S7 (eligibility, universe, data, pre-registered evaluation), S8 (platform, can start in parallel), the methodological stages S9–S13, then S14–S15 (report and go/no-go validation).
