# ADR-0003 — Separate evidence and status vocabularies

- **Status:** PROPOSED (to be accepted at G0)
- **Date proposed:** 2026-10-01 · **Date decided:** —
- **Decided by:** — · **Gate:** G0 · **Stage:** S0
- **Supersedes:** legacy tag convention · **Resolves:** none

## Context
Legacy tags conflated "decided" with "verified".

## Decision
Adopt the five vocabularies of 02_EVIDENCE_AND_STATUS.md: evidence tags
(claims), decision status (ADRs), research-question status (RQs), method
lifecycle (Method Library), fact status (registries) — never mixed. Adopt the
citation rule and the significance-separation rule.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Single tag set (legacy) | Simple | Proven to conflate decision with evidence |
| **Separate vocabularies** | Each object's status is unambiguous | More vocabulary to learn |

## Consequences
Every document and ADR uses these tags; reviews check them.

## Revisit trigger
If a status cannot be expressed in the vocabulary.
