# ADR-0004 — Layer model and deterministic-code / agent boundary

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (roadmap approval, design session 2026-10-01) · **Gate:** G0 · **Stage:** S0
- **Supersedes:** legacy L0–L6 layering · **Resolves:** none

## Context
The reference paper keeps numerical computation in code and judgement in
LLM agents (its Appendix A.1), but its agentic layer cannot be cleanly
backtested (its §5.1) and its LLM steps have no deterministic fallback.

## Decision
1. Layers: Governance · Registries · Data · Universe & instruments · Method
   Library & Feasibility Engine · Research/beliefs · Risk · Portfolio
   construction · Deliberation (a protocol reusable at several layers) ·
   Decision & investment case · Tactical & implementation · Monitoring ·
   Learning; cross-cutting evaluation harness, provenance, orchestration, UI.
2. Rules R1–R7 of 05_DETERMINISTIC_VS_AGENT.md, including: no LLM number
   enters a calculation except as a bounded choice among code-computed
   candidates; a deterministic fallback for every agent decision and a
   deterministic-only mode; hard constraints are deterministic predicates
   checked after every agent step; Policy Statement, compliance, approval,
   eligibility, and facts are read-only to agents.
3. Fail-small fallbacks; signal ⊥ risk; construction ⊥ parameter selection.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Paper's architecture as-is | Proven to run | Unbacktestable agent layer; no fallback; no eligibility filter |
| Pure deterministic pipeline | Fully backtestable | Forgoes possible value of judgement — itself a research question (RQ-16) |
| **Hybrid with deterministic-only mode as control** | Backtestable baseline + measurable agent value | Two execution modes to maintain |

## Consequences
Agent value-added becomes a measurable quantity (S7, S15) rather than an assumption.

## Revisit trigger
Evidence from S12/S15 on agent value-added.
