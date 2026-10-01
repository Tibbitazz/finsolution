# ADR-0019 — External-fact registry: record contract, point-in-time semantics, layered admissibility

- **Status:** PROPOSED (for G3)
- **Date proposed:** 2026-10-01 · **Date decided:** —
- **Decided by:** — · **Gate:** G3 · **Stage:** S3
- **Supersedes:** none · **Related:** ADR-0020, ADR-0021 (scope exclusions) · **Extends:** ADR-0003 (fact-status vocabulary E), ADR-0006 (registries), ADR-0015 (versions, units), ADR-0016 (finding records), [03](../03_FACTS_REGISTRY_POLICY.md) §3–§4
- **Resolves:** RQ-24, RQ-42; structure for RQ-03 … RQ-06; bounded findings for RQ-45, RQ-46, RQ-49
- **Spec commit / tag:** —

## Context
S3 must make external facts usable by later stages without turning
uncertainty into false precision, proposals into law, or one jurisdiction's
rules into defaults. The single `status` field of 03 §3 conflates legal
standing with verification. It cannot express a verified proposal, a
verified future-effective rule, or two conflicting official sources.
Research basis: [S3_REGISTRY_ARCHITECTURE.md](../research/S3_REGISTRY_ARCHITECTURE.md), [S3_FINDINGS.md](../research/S3_FINDINGS.md).

## Decision
1. **Logical record contract** as in S3_REGISTRY_ARCHITECTURE §1.
   - Physical storage stays open (S6b/S8). Several records may share a file.
   - Conflicts between sources are separate records linked by `conflicts_with`, never successive versions.
2. **Two status axes replace the single `status` field:**
   - `legal_status` (effective · enacted_not_yet_effective · proposed · repealed · not_applicable; for commercial facts: published · announced · withdrawn);
   - `verification_status` (verified · interpretation · unresolved_conflicting · unavailable · legacy_unverified), with `verification_level` (V-full · V-abs · V-bib).

   Mapping from vocabulary E (02):

   | Vocabulary E | Contract |
   |---|---|
   | VERIFIED | `verified` |
   | LEGACY-UNVERIFIED | `legacy_unverified` |
   | OPEN | `unavailable` |
   | EXPIRED | Derived `stale` flag (not stored) |
   | ASSUMED | Not a registry status. An assumption is a labelled user scenario, never a fact |

   `confidence` is replaced by `verification_level` plus the `interpretation` status.
3. **Point-in-time semantics** (§2): bitemporal `Fact(t | k)`.
   - Proposals are never returned.
   - Future-effective facts never leak.
   - "Current" is derived at query time.
   - Runs pin k in their manifest.
4. **Uncertainty propagates as unknown** (§3), never as false/0 or as a prior period's value. Checks over unknown facts return `unknown` and resolve to `pending` with a finding.
5. **Admissibility layers** legal ∩ wrapper ∩ broker ∩ methodological ∩ user, each returning a value and its binding source (§4). S3 populates the first three only.
   - **Unknown ≠ unsupported:** `not_offered` and `prohibited` require a source statement; absence of evidence is `unknown` → `pending`.
6. **Withholding** is represented in nine layers W1–W9 (§5). Treaty rate and actually-withheld rate are distinct facts.
7. **Instrument-type attribute schema** (§6) for S6 population. No security master in S3.
8. **RegRule ≠ BrokerImplementation** (§7). A broker implementation references the rule it implements and never stands in for it.
9. **Re-check policy (RQ-24)**: domain cadences plus event triggers (§8).
   - Past `reverify_by` → `stale`.
   - A stale fact feeding a hard constraint, cost, or tax computation requires owner approval (03 §4).
10. **Jurisdiction support (RQ-42)**: a jurisdiction is supported at t only when all eight domains of §9 are covered (domain-level coverage; fact-level gaps propagate as unknown). Otherwise it is unsupported, with an I2 record naming the missing domains. There is no fallback.
11. **Registry-driven option sources** (§10) for `INV.tax_residence`, `ACC.accounts.broker`, `ACC.accounts.wrapper`, `POL.instrument_permissions`, and `INV.complex_product_tests`.
12. **Descriptive account comparison** (§11): matrix of facts with status and source; neutral order; optional cost illustration. No score, rank, weighting, or default cost sort.

13. **Meaning of acceptance:** accepting a registry version accepts each fact at its stated source, scope, verification level, valid-time and knowledge-time coordinates, on the evidence available at its verification date. It does not certify facts forever. Later authoritative changes create new effective-dated facts; history is never rewritten.

**Not decided here:** any user's broker or account; any instrument choice;
methodological admissibility; tax-engine calculations (S13a); the
regulatory status of the application (RQ-49 stays open, see G3 D3-08).

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Keep single `status` (03 §3) | Simple | Cannot represent verified proposals, future-effective rules, conflicts; invites "proposal = fact" errors |
| **Two status axes + bitemporal query** | Faithful to sources; reproducible; prevents leakage | More fields per record |
| Uni-temporal (valid time only) | Simpler | Past runs not reproducible after corrections (FX3-22) |
| Fallback to Norwegian/generic rules for unsupported jurisdictions | Broader apparent coverage | Silently wrong tax/regulatory outputs |
| Ranked broker comparison | Convenient | Recommendation by emphasis (ESMA35-43-3861 ¶62); no user-specific basis at S3 |

## Evidence
- Source-backed facts and their verification levels: S3_FINDINGS §2–§8. `VERIFIED-SOURCE` where V-full; V-abs entries need a full read before reliance.
- Bitemporal modelling: standard database practice (valid time vs. transaction time). `ASSUMED` as design rationale; no empirical claim.
- Emphasis caution: ESMA35-43-3861 ¶62. `VERIFIED-SOURCE` (V-full; non-binding guidance).

## Consequences
- 02 vocabulary E and 03 §3 are read through this mapping once ADR-0019 is accepted. Their bodies are annotated, not rewritten.
- S6 populates instrument records against §6.
- S8 implements `Fact(t | k)`, staleness flags, and the comparison view.
- S13a consumes tax facts without embedding them.
- Fixtures FX3-01 … FX3-26 become acceptance tests for the registry layer.

## Revisit trigger
S8 storage design shows the contract is unimplementable as specified, or a
new domain cannot be expressed with the two status axes.
