# S2 — Decisions at gate G2 (separated from research findings)

**Document status:** STABLE — owner approval 2026-10-01 with amendments to D2-01, D2-04, D2-06, D2-07, D2-09, D2-10, D2-14 (incorporated below). Findings live in [S2_CONFIGURATION_MACHINERY.md](S2_CONFIGURATION_MACHINERY.md) and [S2_RISK_PREFERENCE_RESEARCH.md](S2_RISK_PREFERENCE_RESEARCH.md).

| ID | Decision (as approved) | Deferred to later stages | ADR |
|---|---|---|---|
| D2-01 | Immutable, content-addressed versions; `id@version` references; typed values with explicit unit, basis, and period, **preserved through every derivation** | Physical format (S8) | 0015 |
| D2-02 | Generic constraint representation with hardness ∈ {hard, soft, trigger}; formal hard-constraint rule. **No investment constraint adopted** | Which constraints apply (S3–S13) | 0015 |
| D2-03 | Resolution algorithm and its four invariants | — | 0015 |
| D2-04 *(amended)* | Interaction taxonomy I1/I2/I3/T1/T2/F1 with a **structured finding-record architecture**: I1–I3 → `ConflictRecord`; T1 → `TradeOffRecord`; T2 → `GoalRoutingRecord` where relevant; F1 → `FeasibilityFinding`. All are versioned, attributable, and visible in state and the audit trail. Only I1–I3 are conflicts. An unattainable objective stays visible without modifying the goal. **T1 trade-offs are not resolved in S2** | Trade-off handling (S11) | 0016 |
| D2-05 | Ordering: goal separation → explicit user priority → user resolution. No implicit system ordering | — | 0016 |
| D2-06 *(amended)* | Ordered user-declared alternatives as a **schema mechanism**: field metadata `supports_ordered_alternatives` (default false) with semantic requirements for enabling it. An empty fallback list authorises no substitution; fallback only on blocked/pending. **No closed whitelist.** Which fields expose it is decided by the stage that researches each field's options and methodology. Current examples: `REB.approach`, `POL.currency_hedging`, `POL.benchmark`, `POL.allocation_unit` | Per-field enablement (S5, S7, S13b, …) | 0016 |
| D2-07 *(amended)* | Stage-separated authority model distinguishing information acquisition/analysis, proposal, decision/portfolio construction, trade generation/staging, order submission, and unattended execution. The eight grants are the **S2 logical representation**; S8/S13 may refine, split, or consolidate them. Central invariant: analytical ≠ decision ≠ execution authority. No execution-related authority is operational before S13 safeguards and eligibility conditions exist | Refinement (S8/S13); UI levels | 0017 |
| D2-08 | Declared-read dependency graph with incremental invalidation. A component that cannot declare its inputs does not participate in the production graph | Engine (S8) | 0015 |
| D2-09 *(amended)* | Six distinct risk concepts with provenance. No universal ordinal-category → γ conversion. **Model parameters such as γ have meaning only within a specified formulation, units, and calibration context, and are never stored as portable attributes of the investor** | Model calibration (S11) | 0018 |
| D2-10 *(amended)* | Disagreements between stated/elicited preference and estimated capacity: preserve the distinct objects; expose the disagreement; never overwrite one with another; never convert capacity into preference. **Whether particular objectively measurable capacity measures become hard portfolio constraints is deferred to S11**; G2 does not restrict such disagreements to being informational only | S11 | 0018 |
| D2-11 | No elicitation questionnaire adopted; 7.6 conditional; 7.3 pending; `Instrument` contract adopted | S11/S15 (RQ-50) | 0018 |
| D2-12 | Material semantic change requires a new field identity; history interpretable under the schema and methods of its time | Migration tooling (S8) | 0015 |
| D2-13 | Option-set lifecycle and provenance governance; no substantive contents | Contents (S3–S5 and later) | 0015 |
| D2-14 *(amended)* | Fixtures FX2-01 … FX2-20, including the five boundary tests added at G2 (FX2-03 amended; FX2-17 … FX2-20) | — | — |

**Also approved at G2:**
- The research memo as the S2 evidence base, with its verification limitations preserved.
- RQ-49 as a research question only; it implies no regulatory status.
- RQ-50.
- The calibration-vs-selection distinction registered under RQ-02d/RQ-50.
