# ADR-0013 — Clarify ADR-0009's enforcement test for relative (cross-sectional) quantities

- **Status:** PROPOSED (to be decided at G0)
- **Date proposed:** 2026-10-01 · **Date decided:** —
- **Decided by:** — · **Gate:** G0 · **Stage:** S0
- **Supersedes:** none · **Clarifies:** ADR-0009 (principle unchanged; body not modified)
- **Resolves:** none (opens RQ-38)

## Context
ADR-0009 (accepted) states that preferences never alter beliefs. Its
enforcement test, written in 07 §4, requires that perturbing any preference
field leave *every* belief-artefact hash unchanged. That cannot hold when a
universe preference changes:
- Σ changes dimension;
- equilibrium-implied returns (e.g. Black–Litterman) depend on the asset set;
- cross-sectional scores normalised over the policy-permitted universe change for every remaining asset when one asset is excluded.

The test as written is therefore unimplementable, not merely strict.

## Decision
1. The ADR-0009 principle stands unchanged.
2. Every relative or cross-sectional construct declares its **comparison
   universe** as an explicit, versioned input.
3. Enforcement is restated:
   - For asset-level beliefs of assets present both before and after a
     preference change, values must be unchanged, conditional on an
     unchanged declared comparison universe.
   - A change caused solely by a declared change in comparison universe is
     reported as such, never silently.
   - Horizon remains the sole exception that may change forecast targets.
4. Whether the comparison universe is the policy-permitted universe or a
   preference-independent reference universe is **OPEN** (RQ-38).

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Keep test as written | Simple | Fails on any universe change; would be ignored in practice |
| Add "universe" as a second blanket exception | Simple | Permits silent preference contamination of relative measures |
| **Conditional invariance with declared comparison universe** | Keeps principle enforceable and auditable | Every relative method must declare its universe |

## Evidence
`VERIFIED-DERIVATION` (logical): a z-score or rank of asset i depends on the
mean/dispersion/ordering of its comparison set; removing any member changes
it for every other member in general.

## Consequences
Signal and CMA contracts gain a mandatory comparison-universe field (06 §5).

## Revisit trigger
Resolution of RQ-38.
