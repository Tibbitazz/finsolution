# ADR-0008 — "Policy Statement" as the governing object; individuell pensjonssparing out of scope

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (explicit instruction, design session 2026-10-01) · **Gate:** G0 · **Stage:** S0
- **Supersedes:** use of "IPS" for the governing document · **Resolves:** naming collision

## Context
In Norway "IPS" also denotes *individuell pensjonssparing*, a pension
product, which would collide with "Investment Policy Statement".

## Decision
1. The governing investor-policy configuration is named **Policy Statement**
   throughout architecture, schemas, documentation, UI, and code.
2. *Individuell pensjonssparing* is not modelled as a wrapper or investment
   option in the current system.

## Consequences
Schemas and code use `PolicyStatement` (or equivalent); "IPS" is not used.

## Revisit trigger
Owner brings pension products into scope.
