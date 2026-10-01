# ADR-0010 — Investor risk preference is distinct from model risk-aversion parameters

- **Status:** ACCEPTED (separation) · calibration design `OPEN` (RQ-02)
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (explicit instruction, design session 2026-10-01) · **Gate:** G0 · **Stage:** S0
- **Supersedes:** legacy single global γ · **Resolves:** none

## Context
Many optimisers require a risk-aversion parameter (e.g. γ in
max w′μ − (γ/2) w′Σw). The owner proposed qualitative categories
(Aggressive / Moderate / Conservative) mapping to γ ranges, as an example.

## Decision
1. The Policy Statement stores the investor's **risk preference**; each
   model's risk parameter (γ_MVO, volatility target, risk budget, EPO sizing,
   …) is a **derived model parameter**, produced by a calibration layer.
   They are never the same object.
2. The example mapping γ∈[1,3]/[4,6]/[7,10] is **not adopted**.
3. The calibration layer's design, the elicitation inputs, any category
   mapping, and whether an advanced mode exists are research (RQ-02),
   assigned to S1 (elicitation), S2 (representation and theory), S11
   (model-specific parameterisation).

## Evidence
`VERIFIED-DERIVATION` (07 §5): γ's numerical value depends on return units
(percent vs. decimal changes the required γ by 100×); it is invariant to
consistent annualisation but not to inconsistent scaling; it has no
preference meaning in simple EPO (scale only) or endogenous-γ EPO
(normalisation), and does not exist in risk parity / minimum variance / HRP;
the risk implied by a fixed γ changes whenever estimates change (Merton-share
illustration under assumed inputs).

## Consequences
The UI must not present one coefficient as meaning the same across models.
Risk preference propagates to constraints, parameters, CRO thresholds,
sizing, and monitoring — never to beliefs (ADR-0009).

## Revisit trigger
Resolution of RQ-02.
