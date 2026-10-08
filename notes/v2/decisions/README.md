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
| [ADR-0005](ADR-0005-model-eligibility-funnel.md) | Model-eligibility funnel | ACCEPTED (meaning of ADMISSIBLE superseded in part by ADR-0025, 2026-10-07) | G0 | S0 | 2026-10-01 | — | all thresholds; hysteresis (RQ-21) |
| [ADR-0006](ADR-0006-configuration-hierarchy-and-registries.md) | Configuration hierarchy; facts registries | ACCEPTED | G0 | S0 | 2026-10-01 | single-broker assumption | field contents (G2) |
| [ADR-0007](ADR-0007-broker-scope-and-continuous-capital.md) | Brokers Nordnet + eToro; continuous capital | ACCEPTED | G0 | S0 | 2026-10-01 | Nordnet-only assumption | all broker facts (RQ-06) |
| [ADR-0008](ADR-0008-policy-statement-naming-and-scope.md) | "Policy Statement"; pension product out of scope | ACCEPTED | G0 | S0 | 2026-10-01 | "IPS" naming | — |
| [ADR-0009](ADR-0009-beliefs-vs-preferences.md) | Beliefs ⊥ preferences (horizon exception) | ACCEPTED | G0 | S0 | 2026-10-01 | — | — |
| [ADR-0010](ADR-0010-risk-preference-vs-model-parameters.md) | Risk preference ≠ model parameters | ACCEPTED (separation) | G0 | S0 | 2026-10-01 | single global γ | calibration (RQ-02) |
| [ADR-0011](ADR-0011-roadmap-v2.md) | Roadmap v2, S0–S18 | ACCEPTED | G0 | S0 | 2026-10-01 | legacy roadmaps | — |
| [ADR-0012](ADR-0012-signal-and-scoring-architecture.md) | Signal & scoring architecture; score ≠ belief; rule R8; typed contracts | ACCEPTED | G0 | S0 | 2026-10-01 | — (extends 0004, 0005, 0011) | RQ-27 … RQ-37 |
| [ADR-0014](ADR-0014-reusable-engine-local-user-layer.md) | Reusable engine; private local user layer; declared vs. effective Policy Statement; data classes; activation; value origins; purpose limitation; portability | ACCEPTED | G1 | S1 | 2026-10-01 | — (extends 0006, 0010, 0012) | RQ-39 … RQ-47 |
| [ADR-0015](ADR-0015-configuration-machinery.md) | Configuration machinery: schema, constraints, resolution, dependency graph, evolution, option governance | ACCEPTED | G2 | S2 | 2026-10-01 | — (extends 0014, 0004, 0012) | — |
| [ADR-0016](ADR-0016-interaction-taxonomy-and-alternatives.md) | Interaction taxonomy, ordering policy, ordered alternatives | ACCEPTED | G2 | S2 | 2026-10-01 | — (extends 0014) | — |
| [ADR-0017](ADR-0017-authority-model.md) | Authority model: analysis separated from execution | ACCEPTED | G2 | S2 | 2026-10-01 | — (extends 0004) | UI levels; S13 safeguards |
| [ADR-0018](ADR-0018-risk-preference-ontology.md) | Risk-preference ontology, calibration interface, elicitation deferral | ACCEPTED | G2 | S2 | 2026-10-01 | — (extends 0010, 0014) | RQ-02d, RQ-50 |
| [ADR-0019](ADR-0019-external-fact-registry.md) | External-fact registry: record contract, point-in-time semantics, layered admissibility, withholding layers, re-check, jurisdiction support, comparison | ACCEPTED | G3 | S3 | 2026-10-01 | — (extends 0003, 0006, 0015, 0016) | CB-01 … CB-16 carried; RQ-45, RQ-49, RQ-51 open |
| [ADR-0020](ADR-0020-pension-saving-excluded.md) | All pension saving and pension products out of scope | ACCEPTED | — (owner instruction) | S3 | 2026-10-01 | — (extends 0008) | — |
| [ADR-0021](ADR-0021-wealth-tax-excluded.md) | Wealth tax entirely out of scope; `TAX.wealth_tax_position` retired | ACCEPTED | — (owner instruction) | S3 | 2026-10-01 | — (extends 0006; analogous to 0020) | — |
| [ADR-0022](ADR-0022-parallel-development-track.md) | Parallel software-development track after G3; S18 = final handoff/completion | ACCEPTED | G3 (owner instruction) | S3 → S4/S8 | 2026-10-01 | — (amends 0011) | S8 plan |
| [ADR-0023](ADR-0023-ang-architectural-baseline.md) | ANG as architectural baseline; role ≠ runtime; Method ≠ Agent; extensible roster; adopted vs. illustrative | ACCEPTED | — (owner, S4 plan) | S4 | 2026-10-02 | — (clarifies 05 §2, ADR-0004) | — |
| [ADR-0024](ADR-0024-s4-method-governance.md) | Research lane; revision rules; parameter-authority classes; allocation domains; dual contracts; EPO hierarchy; verification area | ACCEPTED | — (owner, S4 plan) | S4 | 2026-10-02 | — (extends 0005, 0012, 0015, 0023) | — |
| [ADR-0025](ADR-0025-methodological-admission-vs-empirical-evaluation.md) | Methodological admission ≠ empirical evaluation (redefines ADMISSIBLE) | ACCEPTED | — (owner decision D-1; reviewed at G4) | S4 | 2026-10-07 | in part ADR-0005; 06 §1(3), §2 rule 4 wording; 02 §D (annotated, not rewritten) | admission criteria implemented in S4.21; evaluation axis defined in S7 |
| [ADR-0026](ADR-0026-agent-mandates-and-implementation-authority.md) | Agent Mandate and Decision Record objects; investment decision ≠ rebalancing determination ≠ implementation discretion ≠ execution; escalation; evidence rights; no containers | ACCEPTED | — (owner check, option (a); reviewed at G4) | S4 | 2026-10-08 | — (extends 0023; annotates 0012 §7, 05 §2 layer 8, 08 S13d) | discretion breadth and window values (RQ-53, S13); field types (S4.20/S8); attribution (RQ-54) |
| [ADR-0027](ADR-0027-ang-adaptation-learning-risk-units.md) | ANG adaptation: governed learning (L-1 … L-7), registry evolution without auto-culling, method-specific construction risk models with one common reference model per declared horizon, runtime backtest diagnostics, declared CMA/risk units | PROPOSED | owner, at G4 or earlier | S4 | — | — (extends 0023 §8, 0024 §1, 0025, 0026 §4.4/§8) | thresholds S7/S17; estimators S10; numéraire S5 |
| [ADR-0013](ADR-0013-clarify-beliefs-preferences-test.md) | Clarify ADR-0009 test: declared comparison universe | ACCEPTED | G0 | S0 | 2026-10-01 | — (clarifies 0009) | RQ-38 |

**Basis of `ACCEPTED` entries dated 2026-10-01:** explicit owner instructions or
approvals given in the design session of that date; ADR-0002, ADR-0003,
ADR-0012, and ADR-0013 were accepted at the G0 review of the same date; ADR-0014 at the G1 review; ADR-0015 … ADR-0018 at the G2 review (with owner amendments); ADR-0020 by explicit owner instruction in the S3 approval (D3-b); ADR-0021 by explicit owner instruction during the G3 review; ADR-0019 at the G3 review (with owner amendments); ADR-0022 by explicit owner instruction at G3 closure; ADR-0023 and ADR-0024 by owner decision on the S4 plan (2026-10-02); ADR-0025 by owner decision D-1 (2026-10-07); ADR-0026 by the owner's mathematical/authority check, with corrections C-1 … C-6 and additions S-1 … S-4 (2026-10-08). Extending or
clarifying ADRs never edit the body of the ADR they extend.
