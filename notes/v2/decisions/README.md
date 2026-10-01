# Decision Register

**Document status:** STABLE (S0) · Format: [ADR_TEMPLATE.md](ADR_TEMPLATE.md) · Process: [01 §3](../01_SOURCE_OF_TRUTH_AND_WORKFLOW.md)

Only `ACCEPTED` decisions are binding for implementation. ADR bodies are
append-only after acceptance; changes are new ADRs that supersede old ones.

| ID | Title | Status | Gate | Stage | Decided | Supersedes | Open parts |
|---|---|---|---|---|---|---|---|
| [ADR-0001](ADR-0001-v2-source-of-truth.md) | v2 is source of truth; ENGINE_V1 superseded | ACCEPTED | G0 | S0 | 2026-10-01 | legacy material | — |
| [ADR-0002](ADR-0002-living-docs-git-workflow.md) | Living docs, gate-based Git workflow | ACCEPTED | G0 | S0 | 2026-10-01 | — | — |
| [ADR-0003](ADR-0003-evidence-status-taxonomy.md) | Separate evidence/status vocabularies | ACCEPTED | G0 | S0 | 2026-10-01 | legacy tags | — |
| [ADR-0004](ADR-0004-layers-and-agent-boundary.md) | Layer model; deterministic/agent boundary | ACCEPTED | G0 | S0 | 2026-10-01 | legacy L0–L6 | agent anatomy (S8) |
| [ADR-0005](ADR-0005-model-eligibility-funnel.md) | Model-eligibility funnel | ACCEPTED | G0 | S0 | 2026-10-01 | — | all thresholds; hysteresis (RQ-21) |
| [ADR-0006](ADR-0006-configuration-hierarchy-and-registries.md) | Configuration hierarchy; facts registries | ACCEPTED | G0 | S0 | 2026-10-01 | single-broker assumption | field contents (G2) |
| [ADR-0007](ADR-0007-broker-scope-and-continuous-capital.md) | Brokers Nordnet + eToro; continuous capital | ACCEPTED | G0 | S0 | 2026-10-01 | Nordnet-only assumption | all broker facts (RQ-06) |
| [ADR-0008](ADR-0008-policy-statement-naming-and-scope.md) | "Policy Statement"; pension product out of scope | ACCEPTED | G0 | S0 | 2026-10-01 | "IPS" naming | — |
| [ADR-0009](ADR-0009-beliefs-vs-preferences.md) | Beliefs ⊥ preferences (horizon exception) | ACCEPTED | G0 | S0 | 2026-10-01 | — | — |
| [ADR-0010](ADR-0010-risk-preference-vs-model-parameters.md) | Risk preference ≠ model parameters | ACCEPTED (separation) | G0 | S0 | 2026-10-01 | single global γ | calibration (RQ-02) |
| [ADR-0011](ADR-0011-roadmap-v2.md) | Roadmap v2, S0–S18 | ACCEPTED | G0 | S0 | 2026-10-01 | legacy roadmaps | — |
| [ADR-0012](ADR-0012-signal-and-scoring-architecture.md) | Signal & scoring architecture; score ≠ belief; rule R8; typed contracts | ACCEPTED | G0 | S0 | 2026-10-01 | — (extends 0004, 0005, 0011) | RQ-27 … RQ-37 |
| [ADR-0014](ADR-0014-reusable-engine-local-user-layer.md) | Reusable engine; private local user layer; declared vs. effective Policy Statement; data classes; activation; value origins; purpose limitation; portability | ACCEPTED | G1 | S1 | 2026-10-01 | — (extends 0006, 0010, 0012) | RQ-39 … RQ-47 |
| [ADR-0015](ADR-0015-configuration-machinery.md) | Configuration machinery: schema, constraints, resolution, dependency graph, evolution, option governance | PROPOSED | G2 | S2 | — | — (extends 0014, 0004, 0012) | — |
| [ADR-0016](ADR-0016-interaction-taxonomy-and-alternatives.md) | Interaction taxonomy, ordering policy, ordered alternatives | PROPOSED | G2 | S2 | — | — (extends 0014) | — |
| [ADR-0017](ADR-0017-authority-model.md) | Authority model: analysis separated from execution | PROPOSED | G2 | S2 | — | — (extends 0004) | UI levels; S13 safeguards |
| [ADR-0018](ADR-0018-risk-preference-ontology.md) | Risk-preference ontology, calibration interface, elicitation deferral | PROPOSED | G2 | S2 | — | — (extends 0010, 0014) | RQ-02d, RQ-50 |
| [ADR-0013](ADR-0013-clarify-beliefs-preferences-test.md) | Clarify ADR-0009 test: declared comparison universe | ACCEPTED | G0 | S0 | 2026-10-01 | — (clarifies 0009) | RQ-38 |

**Basis of `ACCEPTED` entries dated 2026-10-01:** explicit owner instructions or
approvals given in the design session of that date; ADR-0002, ADR-0003,
ADR-0012, and ADR-0013 were accepted at the G0 review of the same date; ADR-0014 at the G1 review. Extending or
clarifying ADRs never edit the body of the ADR they extend.
