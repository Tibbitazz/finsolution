# ADR-0017 — Authority model: analysis separated from execution

- **Status:** ACCEPTED (with owner amendments at G2)
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (G2 approval, 2026-10-01) · **Gate:** G2 · **Stage:** S2
- **Supersedes:** none · **Extends:** ADR-0004 (R4, human approval), S1 field `GOV.autonomy`
- **Resolves:** structure of the approval matrix (S2 output O6)

## Context
A single "autonomy" field would conflate analytical discretion with
permission to move money (owner instruction).

## Decision
0. **Central invariant:** analytical authority ≠ decision authority ≠ execution authority. No execution-related authority becomes operational before the appropriate S13 safeguards and eligibility conditions exist.
1. A stage-separated model distinguishing information acquisition/analysis, proposal, decision/portfolio construction, trade generation/staging, order submission, and unattended execution. Its **S2 logical representation** is eight grant dimensions; S8/S13 may refine, split, or consolidate them where implementation, broker capabilities, security, or regulatory research require, provided the invariant holds:
   1. analyse;
   2. propose/recommend;
   3. construct candidate portfolios;
   4. select among candidates (if eventually permitted);
   5. generate trade list;
   6. stage orders;
   7. submit orders to a broker;
   8. execute without per-trade confirmation.

   They are aligned with the four information-processing stages of Parasuraman, Sheridan & Wickens (2000).
2. No grant means no authority. Grants carry scope, limits (O2 constraint objects), confirmation requirement, validity window, and are revocable.
3. Dependency: higher action-stage grants require the lower ones they depend on.
4. Dimensions 6–8 are schema capabilities only and cannot be granted until accepted S13 safeguards exist (and broker API capability for 7).
5. Agent permissions remain a separate, narrower layer that never exceeds user grants.
6. `GOV.autonomy` becomes a grouped view over grants. UI levels are not fixed here.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Single autonomy scale | Simple UI | Conflates analysis with money movement |
| **Per-stage grants** | Precise, auditable, safe by construction | More configuration surface (mitigated by grouped UI views) |

## Revisit trigger
S13 safeguard design.
