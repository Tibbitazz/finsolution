# ADR-0016 — Interaction taxonomy, ordering policy, and declared ordered alternatives

- **Status:** PROPOSED (for G2)
- **Date proposed:** 2026-10-01 · **Date decided:** —
- **Decided by:** — · **Gate:** G2 · **Stage:** S2
- **Supersedes:** none · **Extends:** ADR-0014 §5
- **Resolves (proposed):** RQ-23, RQ-48

## Context
Not every pair of user inputs pulling in different directions is a
conflict (owner instruction). Fallbacks must be user-authorised, never
inferred (G1 clarification).

## Decision
1. **Taxonomy** (D2-04):
   - I1 logical inconsistency;
   - I2 hard-constraint conflict;
   - I3 methodological conflict;
   - T1 competing objectives (not a conflict; a trade-off note passed to construction);
   - T2 multi-goal separation (not a conflict);
   - F1 objective infeasibility under current estimates (a finding).

   Only I1–I3 create conflict records. Uncertain classifications are shown as possible inconsistencies.
2. **Ordering** (D2-05): goal separation → explicit user priority → user resolution. No system default ordering of valid objectives without a future ADR and evidence.
3. **Ordered alternatives** (D2-06):
   - Enabled per field only where the field is single-choice, its options come from a registry or the eligibility funnel, and its substitutes are meaningfully rankable.
   - An empty list means there is no substitute.
   - Fallback applies only when the preferred option is blocked or pending.
   - `alternative_used` is recorded.
   - Enabled now for `REB.approach`, `POL.currency_hedging`, `POL.benchmark`, `POL.allocation_unit`.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Fixed default hierarchy | Always resolvable | Ranks valid preferences without basis; no source supports a universal order |
| Alternatives on all fields | Uniform | Invites inferred substitutes; meaningless for set/numeric fields |
| **Taxonomy + user-sovereign ordering + selective alternatives** | Preserves user authority; minimal inference | More user prompts |

## Evidence
- Das et al. (2010): goals as separate accounts with their own risk attitudes [V-abs].
- ESMA35-43-3172 GL4: flag inconsistent responses for reconsideration [V-full].
- Both are cited in S2_RISK_PREFERENCE_RESEARCH §4.

## Revisit trigger
Evidence that a default ordering is needed and justified for a specific field pair.
