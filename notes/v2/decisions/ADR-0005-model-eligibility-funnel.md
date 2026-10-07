# ADR-0005 — Model-eligibility funnel before evaluation and deliberation

- **Status:** ACCEPTED · **Superseded in part by:** [ADR-0025](ADR-0025-methodological-admission-vs-empirical-evaluation.md), 2026-10-07 (the meaning of ADMISSIBLE: methodological admission, with empirical evaluation as a separate axis)
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (design session 2026-10-01) · **Gate:** G0 (framework); thresholds at G4 and stage gates · **Stage:** S0
- **Supersedes:** none · **Resolves:** none (thresholds remain RQ-14, RQ-21 and per-method RQs)

## Context
Some methods are statistically or computationally appropriate only under
conditions (e.g. RMT covariance cleaning depends on N, T, and their ratio).
Letting every implemented method reach agents invites inappropriate choices.

## Decision
Adopt the funnel Feasible → Eligible → Admissible → Deliberable
(06_MODEL_ELIGIBILITY_GOVERNANCE.md): mandatory eligibility contracts;
point-in-time evaluation; threshold provenance classes; `PROVISIONAL` status
for methods with unestablished thresholds (evaluation only, never
deliberation/production); pre-registered thresholds; sandbox-only overrides;
user-visible exclusion reports; implementation-driven eligibility derived
from continuous account value and current registry facts.

## Evidence
`VERIFIED-DERIVATION`: Marchenko–Pastur band computations (06 §4) show q and
N carry distinct information, so contracts carry both.

## Consequences
Method sets become context-dependent and may vary over time; monitoring and
evaluation must handle eligibility changes.

## Revisit trigger
If eligibility churn materially harms stability (RQ-21).
