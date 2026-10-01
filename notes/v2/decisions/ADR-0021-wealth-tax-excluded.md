# ADR-0021 — Wealth tax is entirely out of scope

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (explicit scope instruction during G3 review, 2026-10-01) · **Gate:** — (owner instruction) · **Stage:** S3
- **Supersedes:** none · **Extends:** ADR-0006 (registry contents), ADR-0020 (analogous exclusion)
- **Resolves:** wealth-tax parts of RQ-03

## Context
Wealth tax is irrelevant to this project. Carrying wealth-tax facts, fields,
or calculations would add maintenance and re-verification burden, and a
risk of wealth-tax effects entering comparisons or construction, with no
project purpose.

## Decision
Wealth tax is out of scope. The engine does not:
1. hold wealth-tax facts in any registry (thresholds, rates, valuation discounts, proposals, or point-in-time history);
2. research future wealth-tax parameters;
3. compute wealth tax or wealth-tax effects;
4. include wealth-tax effects in account comparisons;
5. include wealth-tax effects in portfolio construction or implementation;
6. collect fields that exist solely for wealth-tax purposes.

**Consequences for existing material:**
- **S1 field `TAX.wealth_tax_position` (10.1)** is retired. It existed solely for wealth-tax purposes. Under the schema-evolution policy (ADR-0015, D2-12) it is retired, not deleted; its ID is never reused. It was never active, so no saved values exist.
- **S3 draft records** (wealth-tax threshold, rates, valuation discount, NOU 2026:9 wealth-tax proposal) are removed from the provisional registry. They were never accepted into a registry version, so there is no history to preserve; the removal is recorded in the CHANGELOG.
- **S3 jurisdiction-support domains:** wealth taxation is removed as a domain.
- **Not affected:** ordinary taxation of investment returns, transactions, dividends, interest, capital gains and losses, wrappers, foreign withholding, exit tax, and implementation. Total-wealth *optimisation scope* (`POL.wealth_scope`, `INV.outside_assets`) and outside wealth in *risk capacity* are not wealth tax and are unaffected.
- **Historical documents** (e.g. the SUPERSEDED S1_QUESTIONNAIRE item 10.1) are left unchanged as history. No accepted ADR body is edited; no accepted ADR depends on wealth tax.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Keep wealth-tax facts dormant | Cheap later extension | Re-verification burden; leakage risk into comparisons; contradicts owner scope |
| **Exclude entirely (as for pensions)** | Clean scope; nothing to maintain | Re-adding later needs a new ADR and research |

## Consequences
- Validation rejects wealth-tax facts, fields, and comparison dimensions (fixture FX3-23).
- Scope can change only through a new ADR and the normal schema/versioning process.

## Revisit trigger
The owner brings wealth tax into scope.
