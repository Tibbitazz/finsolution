# ADR-0011 — Adopt roadmap v2 (S0–S18) and its decision gates

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner ("Approved", design session 2026-10-01) · **Gate:** G0 · **Stage:** S0
- **Supersedes:** legacy SPECIFICATION Part X and Part XII; legacy ROADMAP.md · **Resolves:** none

## Decision
Adopt 08_ROADMAP.md: the dependency chain, stage definitions, parallel
branches (platform from G2; data engineering after G5/G6), and decision gates
G0–G17, including: external-facts research (S3) and the eligibility
framework (S4) upstream of universe selection (S5); a pre-registered
evaluation protocol (S7) before any model choice; RMT/high-dimensional
methods only via eligibility study (S10); portfolio construction on the
admissible set only (S11); implementation costs/taxes/FX from account
configuration (S13a); the tactical entry/exit stage preserved (S13c–d);
risk-aversion research placed at S1/S2/S11 (RQ-02).

## Consequences
Stage branches and gate PRs follow ADR-0002 once accepted.

## Revisit trigger
Any gate outcome that invalidates a downstream dependency.
