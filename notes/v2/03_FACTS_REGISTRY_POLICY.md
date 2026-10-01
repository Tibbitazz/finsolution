# 03 — Facts-Registry Policy

**Document status:** STABLE (S0) for policy; storage format `OPEN` (S6b/S8) · **Decision basis:** ADR-0006, ADR-0007

## 1. Principle

Facts about the world that the engine depends on — broker costs and
capabilities, tax law, account-wrapper rules, instrument attributes — are
**versioned external data**, never constants in code or configuration. They
change; the engine must know which version it used.

## 2. Registries

| Registry | Contains | Determined by |
|---|---|---|
| Jurisdiction & Tax Rules | Taxation of gains, dividends, interest, wealth; withholding tax (kildeskatt) and treaty credits; reporting obligations | Law of the investor's tax residence (Norway) and applicable treaties |
| Wrapper | Account-type rules: eligibility, tax deferral, contributions/withdrawals | Law |
| Instrument Master | Tax- and regulation-relevant instrument attributes: domicile, legal form, UCITS status, fund equity share, distribution policy, fund-level withholding, retail-availability requirements (e.g. key information documents) | Instrument documentation and law |
| Broker | Wrappers offered, instrument catalogue, costs, FX, execution, data, legal/custody model, tax reporting | Broker documentation |

**Tax is never a broker attribute.** Tax outcome = f(residence law, instrument,
wrapper). The broker determines only which wrappers and instruments are
offered and how withholding, reporting, and custody are implemented.

## 3. Fact record schema

Every fact is one record:

```yaml
fact_id:        broker.nordnet.commission.min.nordic_equity   # stable, hierarchical
registry:       broker                                        # broker | tax | wrapper | instrument
subject:        nordnet                                       # entity the fact is about
attribute:      commission_minimum
value:          <value>
unit:           NOK
applies_to:     {account_type: <...>, product: <...>, tier: <...>, market: <...>}
jurisdiction:   NO
effective_from: YYYY-MM-DD        # when it is true in the world
effective_to:   null
recorded_at:    YYYY-MM-DD        # when we recorded it (bitemporal)
source:         {type: primary|secondary, citation: <URL/document, section>, retrieved_on: YYYY-MM-DD}
status:         VERIFIED | LEGACY-UNVERIFIED | ASSUMED | OPEN | EXPIRED
confidence:     high | medium | low
reverify_by:    YYYY-MM-DD
verified_by:    <person/agent>
supersedes:     <fact_id@version> | null
notes:          <free text>
```

## 4. Rules

1. **Source hierarchy.** Law and tax authority (e.g. Skatteetaten, Lovdata) >
   regulator (Finanstilsynet) > broker's official documentation and price
   lists > secondary sources. Secondary sources are leads only and cannot
   produce a `VERIFIED` fact.
2. **Append-only versioning.** A changed fact is a new version that supersedes
   the old one; history is never overwritten. Facts are bitemporal
   (`effective_*` vs. `recorded_at`) so backtests can use the facts that were
   in force at each historical date.
3. **Snapshot pinning.** Every run pins a facts snapshot ID; it is part of the
   run manifest ([04](04_REPRODUCIBILITY.md)).
4. **Staleness.** A fact past `reverify_by` becomes `EXPIRED`. A run using an
   expired fact that affects a hard constraint, cost, or tax computation is
   flagged in the investment-case report and requires owner approval before
   any trade. Domain-specific re-verification cadences are set in S3 (RQ-24).
5. **No legacy values.** Values found in legacy material enter only as
   `LEGACY-UNVERIFIED` leads, never as inputs.
6. **No size categories.** Registries record the actual rules (minimum
   commissions, minimum order sizes, fractional availability, tiers). The
   Feasibility Engine derives the economically relevant thresholds from the
   **continuous** account value; no portfolio-size bucket (e.g. "below/above
   NOK 50,000") is a registry concept (ADR-0007).
7. **Scope.** Initial brokers: Nordnet and eToro, neither preferred; adding a
   broker requires only new records, never an architecture change. The
   All pension saving and pension products, including *individuell
   pensjonssparing*, are out of scope (ADR-0008, ADR-0020).

## 5. Current contents

Provisional registry v1 (verified 2026-10-01; for acceptance at G3): see
[facts/README.md](facts/README.md) and [S3_FINDINGS.md](research/S3_FINDINGS.md).
The record contract proposed in ADR-0019 (PROPOSED, G3) would replace the
§3 schema above; until acceptance §3 remains the policy text.

## 6. Open items

- Storage format and location (YAML files under `facts/` vs. a database) — S6b/S8.
- Re-verification cadence per domain — proposed in S3_REGISTRY_ARCHITECTURE §8 (RQ-24, at G3).
