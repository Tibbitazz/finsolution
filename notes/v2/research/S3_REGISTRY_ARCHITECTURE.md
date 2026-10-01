# S3 — External-fact registry architecture

**Document status:** STABLE (accepted at G3, 2026-10-01) · **Proposed decision:** ADR-0019 · **Companions:** [S3_FINDINGS.md](S3_FINDINGS.md), [S3_SYNTHETIC_FIXTURES.md](S3_SYNTHETIC_FIXTURES.md), [S3_G3_PACKAGE.md](S3_G3_PACKAGE.md), provisional records in [../facts/](../facts/)

**Scope.**
- S3 establishes external facts and their provenance.
- It chooses no user's account setup, makes no recommendation, and makes no later-stage methodological decision.
- All pension saving (ADR-0020) and wealth tax (ADR-0021) are out of scope: no registry domain, fact, field, calculation, or comparison dimension exists for them.
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

**Meaning of accepting a registry version (e.g. v1 at G3):**
- Each fact is accepted at its stated source, scope, verification level, valid-time coordinates, and knowledge-time coordinates, based on the evidence available on its verification date.
- Acceptance does not certify a fact forever.
- Later authoritative changes create new effective-dated facts. They never rewrite historical ones.

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
| Broker | S3 (B) | offered · not_offered · unknown | "Not offered at the selected broker (source: …)" vs. "Unknown whether offered" |
| Methodological | S4/S9–S13 (C) | admissible · ineligible · pending | "No admissible method uses this instrument type" |
| User | S1 (A) | permitted · denied · undecided | "Excluded by your Policy Statement" |

Each layer returns its value **with its binding source**. The engine keeps
all layer results, so "Legal = permitted, Wrapper = permitted, Broker =
not_offered" yields a different explanation from "Legal = restricted" or
"Method = ineligible". S3 populates only the first three layers. Legal
availability never implies that an instrument should be held.

**Unknown is not unsupported.** `not_offered` (and `prohibited` in the
legal and wrapper layers) requires a source statement establishing it.
Absence of evidence yields `unknown`, which resolves to `pending` with a
finding (§3), never to exclusion presented as a fact. The two produce
different explanations (FX3-24).

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
point-in-time facts per §2. Verified findings: S3_FINDINGS §3 (W8 decomposition §2.1).

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
| `product_classification` | Rule selection (e.g. PRIIP or not) | Product documentation |
| `fund_regime` (UCITS · AIF · other), `fund_legal_form` | Regulation; marketing rules; KID | Fund documentation |
| `priips_applicable` | Whether the PRIIPs KID regime applies | Derived from classification + rules |
| `kid_available` (point-in-time) | Any KID published | Manufacturer |
| `kid_norwegian_compliant_available` (point-in-time) | Norwegian retail access condition | Manufacturer/distributor |
| `marketing_access_status[jurisdiction]` (point-in-time) | Marketing/access rules beyond PRIIPs (e.g. AIF marketing) | Regulator / distributor |
| `mifid_complexity` | Appropriateness requirement | Regulation (pending Art. 25(4) re-read) |
| `derivative`, `leverage_factor` | Regulation; risk | Product documentation |
| `distribution_policy` | Tax timing | Fund documentation |
| `trading_currency` | FX | Venue data |
| `withholding_source_country` | W-layers | Derived from domicile/source of income |
| `broker_availability[broker]` (point-in-time) | Broker layer | Broker facts |

**Eligibility is derived, never inferred from one attribute.**
- Retail eligibility in a jurisdiction is computed from the attributes above and the applicable rules, for example the verified conditional PRIIPs rule `reg.no.priips.no_kid_no_retail_sale`.
- No single attribute such as `domicile_country = US` implies `ineligible`. A US-domiciled ETF with a compliant Norwegian KID and broker availability is not excluded by domicile.
- Per-instrument values are populated in S6 (FX3-27).
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
| Annual income-tax parameters (rates, upward factor) | After budget proposal (October), after Storting adoption (December), at Skatteetaten advance-assessment publication (December); `reverify_by` = 31 Jan of the income year | Budget/proposition publication; Skatteetaten rate pages |
| Shielding rate | When published (January after the income year) | Skatteetaten rate page |
| Statutory rules (ASK, fund taxation, exit tax, credit incl. ASK credit mechanics) | Annually; Skatte-ABC new edition (each income year) | Law amendments (Lovdata), propositions |
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

**Support is represented per domain, not as one label.** A jurisdiction
has a **support profile**: for each fact domain, a coverage status at date t
(`covered` · `partially covered (scope stated)` · `not covered`). An
**operation** is supported at t only if every domain it requires is covered
for the scope the operation needs. Each consuming component declares its
required domains. There is no unqualified "jurisdiction supported" flag.

Fact domains for a residence jurisdiction:
- (1) income/gains/dividend/interest taxation for individuals;
- (2) account/wrapper rules;
- (3) withholding layers W7–W8 as residence country;
- (4) treaty and withholding entries per source country;
- (5) regulation/product-access rules for retail investors;
- (6) broker entities serving residents;
- (7) tax-reporting mechanics;
- (8) exit-tax rules where they exist.

Wealth taxation is not a domain (ADR-0021).

**Process for adding a jurisdiction or domain:**
1. Scope the domains.
2. Collect primary sources.
3. Record the facts.
4. Review the gaps.
5. Approve at a gate (ADR).

Operations whose required domains are not covered are **unsupported**, with
an I2 record naming the missing domains. There is no fallback to Norwegian
or generic rules.

**Fact-level gaps inside a covered domain:**
- Individual facts may still be `unavailable` (e.g. a rate not yet published). They propagate as unknown under §3 and make only the dependent artefacts `pending`.
- Gaps whose resolution is required before a capability is enabled are recorded as Class B items in the carried gating register (OPEN_QUESTIONS).

**Norway — support profile at 2026-10-01 (registry v1):**

| Domain / operation scope | Coverage |
|---|---|
| Core individual investment-income taxation (rates, upward factor, shielding, fund rule, credit, exit tax) | Covered for the verified v1 facts; 2026 shielding and 2027 parameters unavailable (Class B → S13a) |
| Non-pension account/wrapper rules (ASK, ordinary account) | Covered for registry-v1 scope; ASK credit mechanics capability-gated (Class B → S13a) |
| US → Norway direct-dividend withholding | Covered to the verified extent (W1–W3, W5 Nordnet, W7, W8 partial); W5 eToro, W6 unavailable |
| Other source-country treaty/withholding regimes | **Not covered** |
| Fund-level withholding | Not covered (RQ-51, Class B → S6/S13a) |
| Retail product-access rules (PRIIPs, CFD measures, MiFID definitions) | Covered at rule level; per-instrument eligibility is S6 |
| Broker entities (Nordnet, eToro) | Covered for recorded facts; unknowns recorded (Class B → S5/S13a/S13f) |
| Tax-reporting mechanics | Covered for Nordnet; partial for eToro |
| Pension, wealth tax | Out of scope (ADR-0020, ADR-0021) |

## 10. Registry-driven option sources (contents per S3_FINDINGS)

| Field | Option source | v1 contents |
|---|---|---|
| `INV.tax_residence` | Jurisdiction support profiles (§9) | Norway (domain-specific support profile, §9); Other → no covered domains, so every tax-dependent operation is unsupported |
| `ACC.accounts.broker` | Broker registry | Nordnet · eToro · Other (unsupported) |
| `ACC.accounts.wrapper` (per broker × jurisdiction) | Wrapper registry ∩ broker offering | Nordnet: ASK, Aksje- og fondskonto (verified). eToro: ordinary taxable trading account (interpretation: no Norwegian wrapper verified); ASK at eToro = **unknown**. Pension wrappers: none (ADR-0020) |
| `POL.instrument_permissions` rows | Instrument types (§6) ∩ broker availability | Per broker; unknowns shown as unknown |
| `INV.complex_product_tests` rows | Broker implementation records (§7) | Nordnet: tests for complex products, leverage, short selling (V-abs). eToro: unknown |

## 11. Descriptive account-comparison specification

**Purpose:** let a user compare broker × wrapper × account configurations
on factual dimensions at a stated date t. **No ranking, score, "best", or
recommendation.**

- **Dimensions:** fee schedule (commissions, minimums, platform fees); FX mechanics and charges; currency accounts; markets; instrument types; wrappers; fractional trading; margin/leverage/shorting; API capability; tax-reporting support; execution functionality; regulatory/product-access requirements; investor protection.
- **Output:** a matrix of `Fact(t | k)` values with status, verification level, and source per cell. An `unresolved_conflicting` fact (e.g. the eToro inactivity fee) makes the affected cost component `unknown` wherever the conflict matters.
  - Unknown shows as unknown.
  - Order is neutral (alphabetical), with no highlighting of any configuration. This follows the ESMA briefing ¶62 caution on emphasis that tends to influence selection.
- **Optional deterministic cost illustration:** for a user-specified hypothetical trade (size, market, currency), the matrix shows the computed commission and FX charge per configuration from registry facts, labelled as a calculation of published fees, not advice.
- **Never:** aggregate scores, weights across dimensions, or default sort by cost.
