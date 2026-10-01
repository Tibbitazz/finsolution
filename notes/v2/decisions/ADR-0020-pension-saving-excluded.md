# ADR-0020 — Pension saving and pension products are entirely out of scope

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (explicit instruction, S3 approval D3-b, 2026-10-01) · **Gate:** — (owner instruction) · **Stage:** S3
- **Supersedes:** none · **Extends:** ADR-0008 (which excluded only individuell pensjonssparing)
- **Resolves:** D3-b

## Context
Pension saving is irrelevant to this project. Unused pension functionality
risks pension wealth re-entering through total-wealth or risk-capacity
modelling.

## Decision
All pension saving and pension products are out of scope. This includes
individuell pensjonssparing (IPS), occupational/employee pension products
such as egen pensjonskonto (EPK), and any other pension wrapper. The engine
does not:
1. include pension accounts in the account/wrapper registry;
2. collect pension balances as outside wealth (`INV.outside_assets` excludes pension types);
3. use pension wealth in total-wealth allocation or risk-capacity calculations;
4. research pension taxation or pension investment rules;
5. create conditional pension fields for later activation;
6. include pension products in account comparisons.

## Consequences
- A pension type entered anywhere (e.g. as an outside-asset row, wrapper, or instrument) is rejected by validation as out of scope.
- It never enters the investable universe or total-wealth state (fixture FX3-16).
- Scope can only change through the normal schema and versioning process with a new ADR.

## Revisit trigger
The owner brings pension saving into scope.
