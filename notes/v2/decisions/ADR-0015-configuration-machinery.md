# ADR-0015 — Configuration machinery: logical schema, constraint representation, resolution, dependency graph, schema evolution, option governance

- **Status:** ACCEPTED (with owner amendments at G2)
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (G2 approval, 2026-10-01) · **Gate:** G2 · **Stage:** S2
- **Supersedes:** none · **Extends:** ADR-0014 (implements the S1 contract); ADR-0004 R3; ADR-0012 typed contracts
- **Resolves:** RQ-41 (governance only), RQ-47

## Context
S1 fixed the user-facing contract. S2 must specify methodology-neutral
machinery that can represent later decisions without making them
(owner instruction, S2 approval).

## Decision
Adopt, as specified in research/S2_CONFIGURATION_MACHINERY.md:
1. **O1:** immutable, content-addressed objects with `id@version` references; typed values with explicit unit, basis, and period, preserved through every derivation (D2-01).
2. **O2:** a generic constraint object with hardness ∈ {hard, soft, trigger}, source, applicability, and convexity class; the formal hard-constraint rule. **No investment constraint is adopted** (D2-02).
3. **O3:** the resolution algorithm with invariants — Declared never modified; nothing undeclared enters Effective; determinism; implementability-only precedence (D2-03).
4. **O5:** a declared-read dependency graph with input-version cache keys, Effective-gated edges, static validators for purpose limitation, beliefs ⊥ preferences, and acyclicity. A component that cannot declare its inputs does not participate in the production graph. There is no rerun-everything default (D2-08).
5. **O10:** schema evolution by appending versions. Semantic changes require a new field ID with no automatic migration. Effective versions record schema, facts, methods, and resolver versions (D2-12).
6. **Option-set governance:** status lifecycle and provenance by source type; no contents populated (D2-13).

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Mutable records + audit log | Simpler storage | Weaker reproducibility; history can drift |
| Coarse (section-level) invalidation | Simpler graph | Unnecessary recomputation; hides dependency errors |
| **Fine-grained declared-read graph** | Incremental recomputation; enforceable privacy and belief boundaries | Requires complete method contracts |

## Consequences
- Method contracts must declare all reads.
- Physical formats and the graph engine are S8 decisions.
- Substantive constraints and option contents remain with their stages.

## Revisit trigger
An implementation shows that a declared-read graph is infeasible at the
required granularity.
