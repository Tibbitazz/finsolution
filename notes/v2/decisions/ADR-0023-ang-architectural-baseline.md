# ADR-0023 — ANG as the architectural baseline for the agentic investment process

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-02 · **Date decided:** 2026-10-02
- **Decided by:** Owner (S4 plan approval, OD-1 and OD-6, with amendments, 2026-10-02) · **Gate:** — (owner decision; reviewed again at G4) · **Stage:** S4
- **Supersedes:** none · **Clarifies:** 05_DETERMINISTIC_VS_AGENT §2 (layers 3, 5, 6, 7), ADR-0004, REF-01 "architectural reference only" · **Amends:** none
- **Resolves:** C-1 (S4 plan §B.1)

## Context
REF-01 and ADR-0004 treated Ang, Azimbayev & Kim (21 Sep 2026; "ANG") as an
architectural reference. 05 §2 marks ANG-derived layers as "optional" (layer
3 judge) or "if retained (RQ-16)" (layer 6 deliberation). Read in isolation,
that wording could permit collapsing `PC agents → CRO → peer review /
deliberation → CIO` into a conventional optimizer-selection pipeline. The
owner has decided that ANG is the baseline architecture.

## Decision
1. **Baseline roles.** ANG's principal functional roles are the architectural baseline:
   - IPS-governed process (our Policy Statement);
   - macro/regime analysis;
   - asset/asset-class analysis with CMA methods and judgement;
   - covariance/risk estimation;
   - parallel heterogeneous portfolio-construction (PC) proposals;
   - CRO risk assessment;
   - peer review and deliberation with revision;
   - CIO combination/selection with explanation;
   - Researcher;
   - Adversarial Diversifier;
   - monitoring, rebalancing and learning.
2. **Role ≠ runtime.**
   - Preserving a role means preserving its **functional separation and authority boundary**.
   - A role may be implemented by one agent, several agents, deterministic code, human review, or a hybrid.
   - No installation is required to invoke a separate LLM per role.
3. **R2 preserved.**
   - Deterministic-only / privacy mode remains available (05 R2).
   - ANG being the baseline does not require personal data to be sent to external LLMs (ADR-0014, RQ-40).
4. **Clarification of 05 §2.**
   - "Optional" and "if retained (RQ-16)" refer to runtime enablement and to the evidential weight of agent judgement in decisions.
   - They never permit removing a role from the architecture or merging roles so that authority boundaries disappear.
   - The 05 text is not edited; this ADR governs its reading.
5. **Object model.** Five objects are kept distinct:
   - **Method** — a deterministic methodology, e.g. PC-B1 Maximum Sharpe;
   - **Method Contract** — its machine-readable and agent-readable specification;
   - **Agent Role** — e.g. "Maximum-Sharpe PC agent", which invokes a method, interprets its output and participates in review;
   - **Agent Instance** — a runtime realisation of a role;
   - **Portfolio Proposal** — the output object.

   A method is never an LLM. Deterministic mode can run methods without invoking their deliberative roles.
6. **Extensible roster.**
   - ANG's roster (19 fixed + Researcher + Adversarial Diversifier = 21) is the **reference baseline**.
   - The PC roster is versioned and extensible under the governed Method Library; the initial S4 baseline adds Simple and Anchored EPO.
   - The invariant is **parallel heterogeneous PC proposals under a governed Method Library**, not the number 21.
7. **Separation of evaluation stages.** These stay distinct objects and contract boundaries:
   - method output → portfolio proposal → CRO diagnostics → peer assessment → revision → CIO combination/selection;
   - PC method evaluation, peer ranking, and CIO combination are three separate things.

   **The peer vote is not a portfolio-weighting algorithm.**
8. **Adopted vs. not adopted.**

   **Adopted as baseline (architecture):**
   - roles and their order;
   - IPS-centred governance with hard/soft constraints and flagged deviations;
   - deterministic computation in code with agents interpreting structured outputs;
   - agent anatomy as description + scripts + skills + output contract;
   - parallel PC proposals in five families plus the agentic category;
   - a neutral CRO;
   - intra- and inter-category review;
   - dissent surfacing and diversity of the shortlist;
   - CIO choice among single methods and ensembles with written rationale and invalidation conditions;
   - a governance memo (our investment-case report, S14);
   - a learning loop with human approval above materiality.

   **Illustrative implementation choices, NOT adopted (research objects for their owning stages):**
   - 40/60 vote/metric weighting;
   - CIO criterion weights 25/15/15/20/15/10;
   - the 75% Sharpe floor;
   - exact voting mechanics (Borda points, bottom flag);
   - random reviewer assignment and the two-reviewer design;
   - the exact number of agents;
   - exact CMA blending and judgement rules;
   - the four-regime classification scheme;
   - the IPS numbers and the 18-asset universe;
   - quarterly rebalancing;
   - the March-2026 rankings (Exhibit 7) and ensemble weights (Exhibit 8).
9. **No priors from ANG's example.** Exhibit 7 rankings and Exhibit 8 ensemble weights are never imported as priors, quality scores or defaults.
10. **Issues register.** Inconsistencies and ANG-versus-source differences are recorded in `research/s4/ANG_ISSUES_REGISTER.md`. They are never silently repaired.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Keep ANG as "reference only" | Maximum freedom | Permits silent collapse into optimizer selection |
| **ANG roles as baseline; runtime flexible; R2 kept** | Preserves the architecture and privacy mode | Requires role contracts for every layer |
| Adopt ANG wholesale incl. parameters | Simple | Imports untested illustrative choices; conflicts with ADR-0001 P1 |

## Consequences
- S4 builds contracts for every role and keeps methods separate from agents.
- S8 must represent roles composably (no monolithic "investment AI").
- S12 owns the deliberation and CIO protocols.
- The ANG-conformance audit is a G4 criterion.

## Revisit trigger
Evidence under the S7/S15 protocols that a role's runtime implementation adds
no value. Even then, this changes enablement only; removing a role needs a
superseding ADR.
