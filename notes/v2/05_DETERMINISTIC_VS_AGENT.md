# 05 — Deterministic Code vs. Agent Responsibility

**Document status:** STABLE (S0) for rules R1–R7; layer assignments are the accepted architecture, agent anatomy `PROPOSED` (S8) · **Decision basis:** ADR-0004

## 1. Binding rules

| # | Rule |
|---|---|
| R1 | **No LLM-produced number enters a calculation** unless it is a bounded choice among candidates computed in code (e.g. a blend weight constrained to lie within the range of code-computed estimates), logged with its rationale. |
| R2 | **Every agent decision point has a deterministic fallback rule.** The full pipeline must run in **deterministic-only mode**. This mode is backtestable and is the control against which the value added by agent judgement is measured. |
| R3 | **Hard constraints are deterministic predicates** on proposed weights or trade lists, checked in code after every agent step. Agents cannot waive them. |
| R4 | **Read-only to agents:** the Policy Statement, compliance logic, approval matrix, eligibility results, and the facts registries. |
| R5 | **Agents see only the deliberable method set** ([06](06_MODEL_ELIGIBILITY_GOVERNANCE.md)); they may read exclusion reports but cannot reinstate excluded methods. |
| R6 | **Beliefs ⊥ preferences** (ADR-0009): no agent may adjust a market estimate to fit investor preferences. |
| R7 | **Every agent output is archived** with its inputs and model identifiers (replay mode, [04](04_REPRODUCIBILITY.md)). |

## 2. Layer assignment (accepted architecture)

| Layer | Deterministic code | Agent | Human |
|---|---|---|---|
| 0 Governance (Policy Statement, approvals) | Validation, feasibility checks | May help draft/explain; never sets values | Writes and approves |
| 0b Registries (facts) | Storage, versioning, staleness | May assist research; cannot mark `VERIFIED` without source | Approves fact verification policy |
| 1 Data | All ingestion and validation | Text extraction only, flagged, with leakage controls | — |
| 2 Universe & instruments | All eligibility predicates | — | Sets preferences |
| 2b Method Library & Feasibility Engine | All | — | Approves thresholds (ADR) |
| 3 Research / beliefs | All estimates | Optional bounded combination/judgement (RQ-12) | — |
| 4 Risk | All | Narrative only | — |
| 5 Portfolio construction | All optimisers | Optional parameter choice within bounds | — |
| 6 Deliberation (protocol) | Metrics, vote tallies | Critique, voting, adversarial proposals — **if retained** (RQ-16) | — |
| 7 Decision & investment case | Ensemble rules, compliance | Optional bounded selection; report narrative | Approves |
| 8 Tactical & implementation | Costs, taxes, FX, sizing, trade lists | Explanation; tactical judgement only if RQ-17 allows | Executes trades unless an ADR decides otherwise (RQ-19) |
| 9 Monitoring | All checks and alerts | Summaries | Responds to flags |
| 10 Learning | Forecast evaluation, shadow tests | Proposes changes | Approves above materiality |

## 3. Proposed agent anatomy (`PROPOSED`, decided at S8)

Following the reference paper's Appendix A.1: each agent = a natural-language
description (role, inputs, workflow, outputs), deterministic scripts it calls,
shared skills (methodology documents + scripts), and a structured output
contract (schema-validated JSON for machines + markdown for humans).

## 4. Signals and scores — `PROPOSED` (ADR-0012), not to be implemented before G0

- **Placement.** Within layer 3 (Research), a distinct deterministic **signal & scoring component** produces descriptors (cross-sectional scores, time-series states) from point-in-time data. Belief formation (expected returns, regime) is a separate, downstream step. Implementation/risk attributes are computed in layers 4 and 8, indexed asset × account or asset × portfolio.
- **Score ≠ belief.** No score is used as μ, α, or an EPO signal without an `ACCEPTED` mapping (RQ-33).

| # | Rule (proposed) |
|---|---|
| R8 | **Evidence binding.** Agents' quantitative characterisations of assets must cite deterministic descriptors from their evidence packet (value, method and version, comparison universe, timestamps, provenance, staleness — schema RQ-34). Agents cannot compute, alter, or re-normalise descriptors. They may interpret them, compare them with other evidence, and challenge their applicability, in writing and logged. |
