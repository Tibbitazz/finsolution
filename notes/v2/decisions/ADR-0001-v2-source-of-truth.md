# ADR-0001 — v2 framework is the source of truth; ENGINE_V1 material is superseded

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (explicit instruction, design session 2026-10-01) · **Gate:** G0 · **Stage:** S0
- **Supersedes:** all legacy ENGINE_V1 specifications, roadmaps, and decisions
- **Resolves:** none

## Context
The legacy ENGINE_V1 material (repository-root specification and appendix,
local notes, R code) was designed as a security-selection backtest engine
organised around one optimisation method, with no Policy Statement, agents,
UI, or implementation layer. Its record contains unlogged decision reversals
and GitHub/local divergence (09_LEGACY_SUPERSEDED.md §3).

## Decision
`notes/v2/` on `main` is the single source of truth. Legacy material is
retained unmodified for reference, has no authority, and is not developed
further. Legacy `[CONFIRMED]`/`[DECIDED]` tags, roadmap items, broker
assumptions, model choices, and values are void; values may serve only as
`LEGACY-UNVERIFIED` research leads. Method-neutral concepts carry forward
only where independently justified (09 §2).

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Continue developing legacy specification | Reuses effort | Scope mismatch; would anchor research on inherited choices |
| Edit legacy files in place | One location | Destroys the historical record; mixes authorities |
| **New versioned area, legacy frozen** | Clean authority; history preserved | Some re-specification of standard formulas |

## Consequences
All future work references v2 documents and ADRs only. Standard formulas are
re-stated with citations in the stages that use them.

## Revisit trigger
None anticipated.
