# ADR-0009 — Beliefs about markets are independent of preferences over outcomes

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (explicit instruction, design session 2026-10-01) · **Gate:** G0 · **Stage:** S0
- **Supersedes:** none · **Resolves:** none

## Decision
Investor preferences (risk preference, return targets, constraints, autonomy)
never alter estimates of expected returns, covariances, correlations,
volatilities, regime states, or signals. **Single exception:** the
investment horizon sets the forecast horizon of estimates. Enforced by a
deterministic propagation test (07 §4): perturbing any preference field must
leave every belief-artefact hash unchanged, horizon excepted.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Allow preference-conditioned estimates | Outputs "feel" consistent | Wishful estimation; corrupts evaluation and attribution |
| **Strict separation (horizon exception)** | Normative decision theory (beliefs and utility are separate inputs) | Requires discipline in agent prompts and code review |

## Consequences
Agents must not be prompted with preferences when producing estimates; the
test suite enforces the separation.

## Revisit trigger
None anticipated.
