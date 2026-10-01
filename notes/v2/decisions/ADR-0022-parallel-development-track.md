# ADR-0022 — Parallel software-development track after G3

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (explicit instruction at G3 closure, 2026-10-01) · **Gate:** G3 · **Stage:** S3 → S4/S8
- **Supersedes:** none · **Amends:** ADR-0011 (roadmap ordering of S8 and the meaning of S18)
- **Resolves:** none (RQ-10 remains with S8)

## Context
The roadmap implied a largely sequential path with developer handoff at
S18. S0–S3 already specify the method-agnostic framework: local user layer
and profiles, Policy Statement and resolution, finding records, dependency
graph, authority model, and fact registries. Waiting for S4–S13 would
leave the developer idle and delay detection of implementability problems.

## Decision
1. After G3 the project runs two coordinated tracks:
   - **Track A**, research and methodology: S4 → S5/S6a → S6b → S7 → S9 ∥ S10 → S11 → S12 → S13 → S14 → S15 → S16 ∥ S17;
   - **Track B**, software and platform: S8 begins immediately after G3. After G8, the developer builds the production-oriented local application foundation and progressively integrates each accepted Track-A contract.
2. **S18** is the final developer handoff and completion specification (final documentation, accepted contracts, installation and release material, remaining integration). It is not the first developer involvement.
3. **Separation of authority:**
   - Track B (S8) decides how contracts are represented, registered, invoked, stored, isolated, and tested. It never decides which investment methods are scientifically accepted.
   - Track A (S4 onward) decides methods and their contracts. It does not dictate frontend or backend technology unless a method requirement makes it necessary.
4. **No hard-coded methodology.** Unresolved methodology is represented by typed interfaces or stubs, never by fake investment logic or candidate methods treated as decided. Synthetic data only for development; no personal data is required for testing.
5. **Change control:**
   - Developer findings return through a controlled process defined at G8.
   - Material changes go through ADR, schema, or gate.
   - Implementation details that do not alter accepted semantics remain developer decisions.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Sequential (handoff at S18) | Fewer moving parts | Developer idle for many stages; late discovery of implementability issues |
| **Parallel tracks from G3** | Early, production-oriented foundation; early feedback on specifications | Risk of premature methodology in code, mitigated by rules 3–5 and the readiness matrix |
| Parallel from G2 | Earlier start | Registry contract (ADR-0019) not yet accepted |

## Consequences
- 08_ROADMAP §1 shows both tracks; S8 and S18 entries amended.
- The S8 plan must include a developer-readiness matrix (READY / INTERFACE ONLY / NOT READY), a core-framework vs. method-module boundary, and a progressive implementation contract for G4–G14.

## Revisit trigger
Track B repeatedly blocked by Track-A ambiguity, or methodology leaking into
framework code.
