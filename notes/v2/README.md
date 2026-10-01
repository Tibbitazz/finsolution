# Framework v2 — Personal Agentic Investment Engine

**Document status:** STABLE (S0) · **Owner:** Oliver Eliassen · **Created:** 2026-10-01

This directory is the **single source of truth** for the investment engine's
research process, architecture, decisions, and specifications
([ADR-0001](decisions/ADR-0001-v2-source-of-truth.md)). Everything outside it —
including the repository-root `SPECIFICATION.md` and `MATHEMATICAL_APPENDIX.md`
and all local `ENGINE_V1/notes/` files — is **legacy and non-authoritative**
([09_LEGACY_SUPERSEDED.md](09_LEGACY_SUPERSEDED.md)).

## Binding rule for implementation

The developer may build **only** against:
1. decisions with status `ACCEPTED` in the [decision register](decisions/README.md), and
2. documents (or sections) whose header status is `STABLE`.

Anything `DRAFT`, `PROPOSED`, `OPEN`, or `PROVISIONAL` is not an instruction to
build. If an implementation needs a choice that no accepted decision covers,
raise it as a spec question — do not decide it in code.

## Reading order

| # | Document | Purpose |
|---|---|---|
| 00 | [Charter](00_CHARTER.md) | Objective, scope, roles, design principles |
| 01 | [Source of truth & Git workflow](01_SOURCE_OF_TRUTH_AND_WORKFLOW.md) | How documents change and how decisions are made |
| 02 | [Evidence & status taxonomy](02_EVIDENCE_AND_STATUS.md) | The vocabulary used for every claim, decision, method, and fact |
| 03 | [Facts-registry policy](03_FACTS_REGISTRY_POLICY.md) | Broker, tax, wrapper, and instrument facts as versioned data |
| 04 | [Reproducibility standard](04_REPRODUCIBILITY.md) | Run manifests, hashing, replay, validation |
| 05 | [Deterministic code vs. agents](05_DETERMINISTIC_VS_AGENT.md) | Who computes, who judges, who approves |
| 06 | [Model-eligibility governance](06_MODEL_ELIGIBILITY_GOVERNANCE.md) | Feasible → Eligible → Admissible → Deliberable |
| 07 | [Policy Statement governance](07_POLICY_STATEMENT_GOVERNANCE.md) | The governing investor-policy object; beliefs vs. preferences |
| 08 | [Roadmap](08_ROADMAP.md) | Stages S0–S18, dependency chain, decision gates |
| 09 | [Legacy superseded](09_LEGACY_SUPERSEDED.md) | What the old material is, and what (if anything) carries forward |
| — | [Decision register](decisions/README.md) | All ADRs and their status |
| — | [Open research questions](research/OPEN_QUESTIONS.md) | Every unresolved question, assigned to a stage |
| — | [REF-01 reference paper](research/REF-01_self-driving-portfolio.md) | Knowledge base of the architectural reference paper |
| — | [Changelog](CHANGELOG.md) | Document-level change history |

## Layout

```
notes/v2/
├── README.md                     ← this index
├── 00_CHARTER.md … 09_LEGACY_SUPERSEDED.md
├── CHANGELOG.md
├── decisions/                    ← ADRs (append-only) + register
├── research/                     ← open questions, research memos per stage
└── facts/                        ← versioned external facts (empty until S3)
```

## Current position

Stage **S0 (Charter & decision governance)** — closed at gate G0 (2026-10-01);
all S0 ADRs (0001–0013) accepted. **S1 — Investor & jurisdiction context** in progress (ADR-0014 proposed).
No methodological question has been resolved; all are recorded in
[research/OPEN_QUESTIONS.md](research/OPEN_QUESTIONS.md).
