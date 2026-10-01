# S3 — External-fact registry architecture

**Document status:** DRAFT (S3, for G3) · **Proposed decision:** ADR-0019 · **Companions:** [S3_FINDINGS.md](S3_FINDINGS.md), [S3_SYNTHETIC_FIXTURES.md](S3_SYNTHETIC_FIXTURES.md), [S3_G3_PACKAGE.md](S3_G3_PACKAGE.md), provisional records in [../facts/](../facts/)

**Scope.**
- S3 establishes external facts and their provenance.
- It chooses no user's account setup, makes no recommendation, and makes no later-stage methodological decision.
- All pension saving is out of scope (ADR-0020).
- Instrument coverage is at instrument-type level only; individual instruments belong to S6.

---

## 1. Logical fact-record contract

The physical storage (database design, file granularity) is S6b/S8. The
provisional YAML under `notes/v2/facts/` follows this contract; several
logical records may share one file.

| Field | Content |
|---|---|
| `fact_id` | Stable hierarchical ID, never reused |
| `version` | Monotonic per `fact_id`; each version immutable |
| `domain` | tax · wrapper · withholding · regulation · broker · instrument_type · jurisdiction |
| `scope` | `jurisdiction`, `entity` (e.g. broker legal entity), `account_type`, `instrument_type`, `market`, `tier` — whichever apply |
| `attribute` | What the fact is about |
| `value` | Typed value, or `null` when unavailable — **never** coerced to `false`/`0` |
| `unit`, `basis`, `period` | Per ADR-0015 (e.g. `%`, `percent`, `income_year`) |
| `legal_status` | `effective` · `enacted_not_yet_effective` · `proposed` · `repealed` · `not_applicable` (for broker/commercial facts: `published` · `announced` · `withdrawn`) |
| `verification_status` | `verified` · `interpretation` (inference from sources, labelled) · `unresolved_conflicting` · `unavailable` · `legacy_unverified` |
| `verification_level` | `V-full` (passage read) · `V-abs` (official summary/abstract or search summary of an official page) · `V-bib` (existence only) |
| `announced_on` / `published_on` | Date of announcement or publication, if relevant |
| `enacted_on` | Date of adoption or enactment, if relevant |
| `effective_from` / `effective_to` | Valid-time interval (`effective_to` null = open) |
| `verified_on` | Date the fact was checked |
| `recorded_at` | Knowledge time: when the registry learned this version |
| `reverify_by` | Next re-check date (§8) |
| `supersedes` / `superseded_by` | `fact_id@version` links |
| `conditions` | Applicability conditions (structured) |
| `exceptions` | Known exceptions (structured or text) |
| `conflicts_with` | Other versions/sources in conflict (for `unresolved_conflicting`) |
| `source` | `citation`, `url`, `section`, `retrieved_on`, `authority_type` (statute · tax authority · regulator · EU legislation · EU authority guidance · treaty · broker official · secondary) |
| `claim` | The exact claim the source supports (short) |
| `notes`, `provenance` | Who/what recorded it; derivation if `interpretation` |

**Extension fields.** Domain-specific fields may be added where a domain
needs them, e.g. `layer` (W1–W9, §5) on withholding records, and
`implements` (the RegRule `fact_id`, §7) on broker-implementation records.
A conflict between sources is recorded as separate records linked by
`conflicts_with`. It is never recorded as successive versions of one
record, because versions represent changes in knowledge, not disagreement.

**Rule:** every material fact preserves
`claim → authoritative source → scope → effective date → verification date → verification status`.

## 2. Point-in-time semantics

**Two time axes:**
- **valid time** t — when the fact is true in the world;
- **knowledge time** k — when the registry knew it.

`Fact(t | k)` returns the version with:
1. `effective_from ≤ t < effective_to` (open end allowed);
2. `legal_status ∈ {effective, enacted_not_yet_effective}`, the latter only once `effective_from ≤ t`;
3. `recorded_at ≤ k`.

Defaults:
- Current calculations use t = k = now.
- Historical reproduction of a past engine decision uses the k recorded in that decision's manifest.
- Historical analysis uses t = the historical date, with k = now (the true historical rule) or k = t (what was known then), declared explicitly.

**Guarantees:**
- A `proposed` fact is **never** returned by `Fact(t | k)` for any t. It is visible only through explicit proposal queries.
- A future-effective fact (`effective_from > t`) is never returned for t, even if already recorded. A rate announced in the 2027 budget proposal in October 2026 cannot affect income year 2026.
- New information creates a **new version**; history is never overwritten.
- "Current" is **derived at query time** from t, k, and the intervals. It is never stored as a status, so it cannot go stale.

**Mapping to the status names requested at S3 approval:**

| Requested status | Representation |
|---|---|
| verified / current | `verification_status = verified`, `legal_status = effective`, t within interval |
| verified / future-effective | `verified` and (`enacted_not_yet_effective`, or `effective_from > t`) |
| superseded | Has `superseded_by`; still returned for t within its own interval |
| proposed / not effective | `legal_status = proposed` |
| unresolved / conflicting | `verification_status = unresolved_conflicting` with `conflicts_with` |
| unavailable / not verified | `verification_status = unavailable` (value null) |

## 3. Uncertainty is first-class

- `unavailable`, `unresolved_conflicting`, and unknown capabilities propagate as **unknown** through resolution. They never become `false`, `0`, or a current rule.
- A Feasibility Engine check over an unknown fact returns `unknown`. The default resolution outcome is `pending`, with a finding (ADR-0016 F-type or I2 with an unknown binding source), never silent permission or silent prohibition.
- Conflicting authoritative facts are recorded side by side for review. They are never resolved by inference.

## 4. Admissibility layers (provenance-preserving)

Effective investable universe ⊆
**legal/regulatory** ∩ **wrapper** ∩ **broker** ∩ **methodological** ∩ **user**.

| Layer | Owner stage | Values | Example explanation |
|---|---|---|---|
| Legal/regulatory | S3 (B) | permitted · restricted (conditions) · prohibited · unknown | "Not offered to retail investors without a Norwegian KID (PRIIPs)" |
| Wrapper | S3 (B) | permitted · prohibited · unknown | "ASK holds only EEA-domiciled listed shares and EEA equity funds" |
| Broker | S3 (B) | available · unavailable · unknown | "Not available at the selected broker" |
| Methodological | S4/S9–S13 (C) | admissible · ineligible · pending | "No admissible method uses this instrument type" |
| User | S1 (A) | permitted · denied · undecided | "Excluded by your Policy Statement" |

Each layer returns its value **with its binding source**. The engine keeps
all layer results, so "Legal = permitted, Wrapper = permitted, Broker =
unavailable" yields a different explanation from "Legal = restricted" or
"Method = ineligible". S3 populates only the first three layers. Legal
availability never implies that an instrument should be held.

## 5. Layered foreign-withholding representation

| # | Layer | Representation | Source domain |
|---|---|---|---|
| W1 | Source-country statutory withholding | Rate by income type and source country | Source-country law/authority |
| W2 | Treaty entitlement | Maximum rate by treaty, article, residence pair, income type | Treaty text |
| W3 | Eligibility requirements | Conditions (e.g. residence, beneficial ownership) and documentation (e.g. W-8BEN validity) | Treaty / source-country authority |
| W4 | Relief at source | Whether and how the payer applies the treaty rate at payment | Source-country authority; broker practice |
| W5 | Actually withheld | Rate applied by broker/custodian, by market/listing condition | Broker official documentation |
| W6 | Reclaim | Mechanism to recover excess withholding (authority, form, deadline) | Source-country authority |
| W7 | Domestic treatment | Credit (kreditfradrag): conditions, cap, treaty-rate limit, carry-forward | Residence-country authority |
| W8 | Wrapper-specific treatment | Treatment inside each wrapper (e.g. ASK) | Residence-country authority |
| W9 | Fund-level withholding | Withholding inside a fund (not suffered directly by the investor); investor-level relief, if any | Fund/residence-country sources |

W2 and W5 are separate facts and are never assumed equal. Values are
point-in-time facts per §2. Verified findings: S3_FINDINGS §3.

## 6. Instrument-type external-attribute schema (for S6 population)

Per instrument type (share, ETF, mutual fund, money-market fund, bond, bond
fund, CFD, option, future, warrant, leveraged/structured ETP, other), S6
records per instrument:

| Attribute | Purpose | Source domain |
|---|---|---|
| `instrument_type` | Rule selection | S6 data |
| `domicile_country` (point-in-time) | ASK eligibility; withholding source | Issuer/fund documentation |
| `listing_venue`, `eea_regulated_market` | ASK eligibility; regulation | Venue data |
| `fund_share_component_start_of_year` | Fund tax split; ASK eligibility (> 80%) | Fund manager / tax reporting |
| `ucits_status`, `fund_legal_form` | Regulation; KID | Fund documentation |
| `priips_kid_norwegian_available` (point-in-time) | Retail access (Norway) | Manufacturer/distributor |
| `mifid_complexity` | Appropriateness requirement | Regulation (pending Art. 25(4) re-read) |
| `derivative`, `leverage_factor` | Regulation; risk | Product documentation |
| `distribution_policy` | Tax timing | Fund documentation |
| `trading_currency` | FX | Venue data |
| `withholding_source_country` | W-layers | Derived from domicile/source of income |
| `broker_availability[broker]` (point-in-time) | Broker layer | Broker facts |
| `out_of_scope_pension` | Validation (ADR-0020) | Classification |

Derived, not stored: ASK eligibility = rule(domicile EEA ∧ (listed EEA share ∨ EEA fund with share component > 80%)), evaluated point-in-time.

## 7. Regulatory / product-access rule structure

`RegRule` = `rule_id@version` · `jurisdiction` · `legal_basis` (instrument,
article) · `applies_to` (instrument types / client category) ·
`requirement` (e.g. KID in Norwegian before retail access; appropriateness
assessment; leverage cap) · `actor` (manufacturer · distributor/broker ·
investor) · `effect_on_layer` (legal: restricted/prohibited/conditions) ·
`legal_status` / effective dates · source fields.

**Implementation records are separate from legal requirements:**
`BrokerImplementation` = broker · rule implemented (or own policy) · test or
questionnaire · scope · source. A broker's test is never recorded as the
law, and self-reported experience is never an eligibility rule (S3_FINDINGS §5).

## 8. Re-check and staleness policy (RQ-24)

| Domain | Scheduled review | Event triggers |
|---|---|---|
| Annual tax parameters (rates, factors, thresholds, valuation discounts) | After budget proposal (October), after Storting adoption (December), at Skatteetaten advance-assessment publication (December); `reverify_by` = 31 Jan of the income year | Budget/proposition publication; Skatteetaten rate pages |
| Shielding rate | When published (January after the income year) | Skatteetaten rate page |
| Statutory rules (ASK, fund taxation, exit tax, credit) | Annually | Law amendments (Lovdata), propositions |
| Treaty provisions | Every 2 years | Protocol signature or entry into force |
| Regulatory rules and guidance (PRIIPs, MiFID, ESMA, Finanstilsynet) | Every 6 months | ESMA/Finanstilsynet publications |
| Broker fee schedules | Quarterly | Broker price-list or terms change notices |
| Broker capabilities (account types, products, shorting, fractional) | Quarterly | Broker announcements |
| API availability | Quarterly; **monthly** while an enabled feature depends on it | Broker developer notices |
| Wrapper rules | Annually | Law change |

**Staleness:**
- A fact past `reverify_by` is flagged `stale`. It is still returned for its valid time, with the flag.
- Stale facts feeding a hard constraint, cost, or tax computation make the run require owner approval (03 §4).
- Event-driven re-verification creates a new version; the prior version is superseded only once the new one is verified.

## 9. Jurisdiction-addition process (RQ-42)

A jurisdiction is **supported** at date t only when the following domains
each have `verified` facts valid at t:
- (1) income/gains/dividend/interest taxation for individuals;
- (2) wealth taxation (or a verified "none");
- (3) account/wrapper rules;
- (4) withholding layers W7–W8 as residence country;
- (5) treaty table entries needed for supported markets;
- (6) regulation/product-access rules for retail investors;
- (7) at least one supported broker entity serving residents;
- (8) tax-reporting mechanics;
- (9) exit-tax rules where they exist.

Process:
1. Scope the domains.
2. Collect primary sources.
3. Record the facts.
4. Review the gaps.
5. Approve at a gate (ADR).

Partial coverage keeps the jurisdiction **unsupported**, with the missing
domains listed in the conflict record. There is no fallback to Norwegian or
generic rules.

**Domain-level vs. fact-level coverage:**
- Support is assessed per **domain**. A domain is covered when its core rules are verified.
- Individual facts inside a covered domain may still be `unavailable` (e.g. a rate not yet published). They propagate as unknown under §3 and make only the dependent artefacts `pending`, not the whole jurisdiction.
- Treaty coverage (5) is assessed per source country of the markets the user's configuration actually uses. A market whose treaty entry is missing has unknown withholding.

**Norway at 2026-10-01:**
- Domains (1)–(4) and (6)–(9) are covered.
- For (5), only US treaty entries are recorded, so withholding for other source countries is unknown until recorded.
- Fact-level gaps: S3_FINDINGS §9.

## 10. Registry-driven option sources (contents per S3_FINDINGS)

| Field | Option source | v1 contents |
|---|---|---|
| `INV.tax_residence` | Supported jurisdictions (§9) | Norway (supported, subject to the gaps listed in G3 part C); Other → unsupported |
| `ACC.accounts.broker` | Broker registry | Nordnet · eToro · Other (unsupported) |
| `ACC.accounts.wrapper` (per broker × jurisdiction) | Wrapper registry ∩ broker offering | Nordnet: ASK, Aksje- og fondskonto (verified). eToro: ordinary taxable trading account (interpretation: no Norwegian wrapper verified); ASK at eToro = **unknown**. Pension wrappers: none (ADR-0020) |
| `POL.instrument_permissions` rows | Instrument types (§6) ∩ broker availability | Per broker; unknowns shown as unknown |
| `INV.complex_product_tests` rows | Broker implementation records (§7) | Nordnet: tests for complex products, leverage, short selling (V-abs). eToro: unknown |

## 11. Descriptive account-comparison specification

**Purpose:** let a user compare broker × wrapper × account configurations
on factual dimensions at a stated date t. **No ranking, score, "best", or
recommendation.**

- **Dimensions:** fee schedule (commissions, minimums, platform fees); FX mechanics and charges; currency accounts; markets; instrument types; wrappers; fractional trading; margin/leverage/shorting; API capability; tax-reporting support; execution functionality; regulatory/product-access requirements; investor protection.
- **Output:** a matrix of `Fact(t | k)` values with status, verification level, and source per cell.
  - Unknown shows as unknown.
  - Order is neutral (alphabetical), with no highlighting of any configuration. This follows the ESMA briefing ¶62 caution on emphasis that tends to influence selection.
- **Optional deterministic cost illustration:** for a user-specified hypothetical trade (size, market, currency), the matrix shows the computed commission and FX charge per configuration from registry facts, labelled as a calculation of published fees, not advice.
- **Never:** aggregate scores, weights across dimensions, or default sort by cost.
