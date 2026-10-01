# ADR-0002 — Living, version-controlled documents with a gate-based Git workflow

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (G0 approval, 2026-10-01) · **Gate:** G0 · **Stage:** S0
- **Supersedes:** none · **Resolves:** none

## Context
The owner prefers living, version-controlled documents over committing only
when the framework is complete. The developer needs the current
authoritative state and the history of why it changed.

## Decision
Documents are committed at every decision gate following
`Research → Decision gate (PR) → ADR → Documentation update (same PR) → Commit → Merge → Tag gate-GNN → Next stage`,
with the authority, immutability, status-label, and commit conventions in
01_SOURCE_OF_TRUTH_AND_WORKFLOW.md. Only the owner merges gate PRs.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Commit when complete | Developer never sees churn | No pre-registration evidence; no decision history; developer blocked for months |
| Commit continuously to `main` without gates | Fast | Drafts and decisions indistinguishable on `main` |
| **Gate-based PRs, status labels, tags** | Pre-registration via commit hashes; clear authority; pinnable versions | Some process overhead |

## Evidence
Methodological: committing protocols and thresholds before results is the
mechanism for pre-registration (P13). `ASSUMED`: the PR/tag workflow is
adequate for a three-person project.

## Consequences
The developer builds only against `ACCEPTED` ADRs and `STABLE` sections.

## Revisit trigger
If process overhead materially slows research, or the team grows.
