# S1 — Investor Profile & Policy Statement Input Specification

**Document status:** STABLE (accepted at G1, 2026-10-01) · **Basis:** ADR-0014, ADR-0006, ADR-0009, ADR-0010, ADR-0012, ADR-0013
**Audience:** developer (UI/input contract) and reviewers. **Companion:** [S1_SYNTHETIC_FIXTURES.md](S1_SYNTHETIC_FIXTURES.md).

This specification defines **what any local user can enter or change**, what
each field means and may be used for, how the interface collects it, and how
a user's Declared Policy Statement becomes the Effective Policy Statement.
It contains **no user's personal values**. All user inputs are runtime
configuration, editable at any time and versioned. They are never
architectural decisions, defaults, or research evidence.

**Layer boundary.** S1 specifies the user-facing contract. S2 specifies the
machinery: formal schema language, validation engine, conflict-priority
ordering (RQ-23), dependency graph, approval matrix, calibration (RQ-02b/c).
Where an option list depends on research, this document fixes only the
**option source** and the **UI structure**, never the options.

---

## 1. Data classes (ADR-0014 §3)

| Class | Name | Contents | Origin | Editable by user? |
|---|---|---|---|---|
| **A** | Runtime user configuration | Investor Profile and Declared Policy Statement fields | User | Yes, any time; every save is a new version |
| **A′** | Portfolio State | Account values, holdings, cash, tax lots, transactions | Import (preferred) or user entry | Corrected, not "preferred"; separate versioning |
| **B** | Public/system facts | Supported jurisdictions, wrappers, broker offerings and fees, test requirements, instrument availability, tax rules | Versioned registries (03) | No |
| **C** | Methodological configuration | Options that exist only through admissible methods (e.g. benchmark set, hedging approach, rebalancing approach) | Research → eligibility funnel (06) | The user chooses only among admissible options |
| **D** | Derived values | Computed from A/A′/B/C by accepted methods | Engine | No; a derived *proposal* may be accepted into A (§4) |
| **E** | Synthetic test fixtures | Hypothetical profiles with expected behaviour | Specification authors | n/a (test assets; never real data) |

**Provenance across boundaries.** Any value crossing a class boundary carries
a provenance record:
- **D values:** the A/A′ field versions, B fact IDs and snapshot, C method ID and version, timestamp.
- **Accepted proposals (D→A):** the proposal's provenance plus the acceptance event.
- **C options:** the method-registry version that made them admissible.

## 2. Field-specification schema (attributes every field must declare)

| # | Attribute | Values / content |
|---|---|---|
| 1 | `id` | Stable namespaced ID (e.g. `INV.tax_residence`). Never reused; retired, not deleted |
| 2 | `level` | investor · goal/portfolio · account · governance · metadata |
| 3 | `class` | A · A′ · B · C · D (§1) |
| 4 | `nature` | F factual · P preference · R preliminary/research-dependent |
| 5 | `status` | core · optional · conditional · methodological · derived · state · retired |
| 6 | `capability` | `schema` = representable (always true for listed fields) |
| 7 | `activation` | When the UI asks for it: `always` · `if <field condition>` · `if method-requires` (some production method's contract lists the field, 06 §5) · `never-yet` |
| 8 | `purpose` | Decision purpose (ADR-0014 §8); no purpose → not collected |
| 9 | `consumers` | **Exhaustive** list of permitted components; anything else requires an ADR |
| 10 | `privacy` | P0 non-personal · P1 personal, low sensitivity · P2 personal financial · P3 sensitive |
| 11 | `necessity` | required (for an Effective Policy Statement while active) · optional |
| 12 | `control` | dropdown · multi-select · toggle · slider · numeric · range · repeating table · free text · system-derived display · file import |
| 13 | `options` + `option_source` | Static list · registry-driven (B) · eligibility-driven (C) · `pending: <stage/RQ>` |
| 14 | `custom` | Not allowed · allowed (validated) · allowed only if the admitting method marks it user-settable |
| 15 | `validation` | Type, range, unit, cross-field rules |
| 16 | `depends_on` | Fields or facts that gate activation or options |
| 17 | `recomputes` | Propagation tags (§7) |
| 18 | `value_origin_rules` | Which origins are allowed (§4) |
| 19 | `pending_research` | Stage/RQ that must finish before options or semantics are final |

Every personal field also offers **"don't know"** and **"prefer not to say"**.
These are stored as such and never imputed.

## 3. Schema capability vs. UI activation (ADR-0014 §4a)

- **Capability:** the engine can represent the field, so adding its use later needs no redesign.
- **Activation:** the UI asks for the field only when its `activation` rule holds.

Purpose-limited fields stay inactive and uncollected until an **accepted
production method's eligibility contract declares the field as a required
profile input** (06 §5, `required_profile_fields`). Activation is therefore
computed: active = `always` ∪ satisfied field conditions ∪ fields required
by production methods.

## 4. Value origins (ADR-0014 §4b)

| Origin | Meaning | Allowed for personal (P1–P3) fields? | UI treatment |
|---|---|---|---|
| `user_entered` | The user typed or selected it | yes | normal |
| `remembered` | The user's own previously saved value, shown for editing | yes — this is **not** a default | shown as "your saved value", with its version date |
| `accepted_proposal` | A labelled derived proposal the user confirmed | yes, with provenance | badge "from proposal"; the original proposal is kept |
| `technical_default` | System default for technical or methodological settings | **no** | badge "system default"; overridable only if `custom` permits |
| `imported` | Portfolio State from a broker export or file | A′ only | source and import time shown |
| `registry` | Class B fact | n/a (read-only) | source, effective date, staleness |
| `derived` | Class D value | n/a (read-only) | "derived — how?" opens the provenance record |

**Rules:**
- No personal field ever has a preselected value on first entry.
- A rejected proposal stores the user's value and keeps the proposal record.
- Real profiles never seed defaults, fixtures, or research evidence.

## 5. Field inventory and specification

The S1 questionnaire was treated as a candidate inventory (Q-numbers =
legacy mapping). Fields are merged, removed, made conditional, or added on
purpose grounds. Abbreviations:
- **Prv** privacy · **Nec** necessity (R = required while active, O = optional).
- **Recomp** propagation tags (§7).
- "B-opts", "C-opts" = registry-driven / eligibility-driven options.

### 5.1 Investor level

| ID (Q) | Class / nature / status | Activation | Purpose → consumers | Prv | Nec | Control · options | Custom | Validation | Depends on | Recomp | Pending |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `INV.tax_residence` (1.1) | A/F/core | always | Select tax and wrapper rules → Tax & Wrapper registry lookup, Feasibility Engine | P2 | R | dropdown · B-opts (jurisdictions in registry) + "Other (unsupported)" | no | one value | registry coverage | EFF FEAS UNIV TAX | RQ-42 |
| `INV.residence_change_expected` (1.2) | A/F/conditional | if method-requires (multi-period / cross-jurisdiction tax planning admitted) | Plan across tax regimes → tax-aware methods only | P2 | O | toggle + year + country (B-opts) | no | year ≥ current | `INV.tax_residence` | TAX PC | RQ-46 |
| `INV.birth_year` (1.3) | A/F/conditional | if method-requires (lifecycle / human-capital / risk-capacity method) | Horizon and goal validation; human capital; risk capacity → those methods only. **Never** a signal or belief input | P2 | O | numeric (year) or age band | no | plausible range | — | CAL PC | S5, RQ-02 |
| `INV.consumption_currencies` (1.4) | A/F/core | always | Define currency risk relative to consumption and liabilities → currency-risk definition, hedging methods | P1 | R | multi-select (ISO list) + share % | no | shares sum to 100% | — | UNIV CAL PC REP | RQ-07 |
| `INV.reporting_currency` (1.5) | A/P/core | always | Reporting and benchmark currency → reporting, performance measurement | P1 | R | dropdown (ISO list) · **derived proposal** = primary consumption currency, confirm required | no | one value | `INV.consumption_currencies` | REP MON | — |
| `INV.trading_restrictions` (1.6) | A/F/core | always | Hard constraints on universe and timing → universe filter, Feasibility Engine | P3 | R | toggle + free text + optional issuer list | yes (text) | issuer IDs resolvable | — | EFF UNIV FEAS | — |
| `INV.investment_experience` (1.7) | A/F/conditional | if method-requires (S3c establishes a legitimate role) | Possible suitability / complex-product access / UI behaviour → TBD by S3c; not collected until then | P1 | O | multi-select | no | — | — | FEAS | RQ-45 (remove if broker tests are the mechanism) |
| `INV.complex_product_tests` (1.8) | A/F (user-attested)/core-dependent | if `POL.instrument_permissions` allows any instrument whose registry entry requires a test | Determine complex-instrument feasibility → Feasibility Engine | P2 | R (when active) | table: broker × product × {passed, not taken, don't know} · rows from B | no | broker/product must exist in B | `ACC.accounts`, `POL.instrument_permissions`, B test requirements | EFF FEAS ELIG | S3c |
| `INV.risk_category` (7.1) | A/P/core | always | Raw risk preference → calibration layer (D), CRO thresholds, report | P1 | R | dropdown: Conservative · Moderate · Aggressive · Custom (described) — **stored raw; no γ** | yes (text) | — | — | CAL PC MON | RQ-02 |
| `INV.max_one_year_decline` (7.2) | A/P/core | always | Loss tolerance → soft drawdown target, monitoring trigger, calibration | P1 | R | numeric % + derived NOK display (from A′) | yes | 0 < x ≤ 100 | — | CAL PC MON | RQ-02 |
| `INV.drawdown_reactions` (7.3) | A/P/optional | always | Pre-committed responses to triggers; calibration cross-check → monitoring, calibration | P1 | O | dropdown per level (levels set in S2) | no | — | — | MON CAL | RQ-02 |
| `INV.past_drawdown_behaviour` (7.4) | A/F/conditional | if method-requires (calibration uses revealed preference) | Stated-vs-revealed cross-check → calibration only | P1 | O | dropdown + text | yes | — | — | CAL | RQ-02 |
| `INV.volatility_range` (7.5) | A/P/optional | always | Soft volatility band → calibration, CRO | P1 | O | range % or "no view" | yes | low < high | — | CAL MON | RQ-02 |
| `INV.choice_battery` (7.6) | A/P/conditional | if method-requires (RQ-02c instrument accepted) | Model-consistent calibration → calibration only | P1 | O | system-presented battery | no | per instrument | — | CAL | RQ-02c |
| `INV.income_stability` (4.3) | A/F/conditional | if method-requires (risk-capacity method) | Risk capacity → that method only | P2 | O | dropdown | no | — | — | CAL | RQ-02 |
| `INV.employment_sector` (4.4) | A/F/conditional | if method-requires (human-capital concentration method) | Concentration underweight/exclusion → that method, universe filter | P3 | O | dropdown + toggle (listed employer) + optional issuer | yes | — | — | UNIV PC | S5 |
| `INV.outside_assets` (5.1) | A/F/conditional | if `POL.wealth_scope` = total wealth (admissible) | Total-wealth optimisation → that method only | P2 | O | repeating table: type · amount or band. **Pension types are excluded and rejected by validation (ADR-0020)** | yes | amounts ≥ 0; type ∉ pension | `POL.wealth_scope` | PC CAL | S5/S7 |
| `INV.debts` (5.2) | A/F/conditional | if method-requires (risk-capacity / leverage method) | Risk capacity; debt as opportunity cost → those methods | P3 | O | repeating table: type · balance/band · rate · fixed/floating | yes | rate ≥ 0 | — | CAL PC | RQ-02 |
| `INV.external_flow_consent` (new) | A/P/conditional | if S8 admits any external service | Consent per external service and field set → privacy gateway | P1 | R (when active) | toggle per service | no | — | RQ-40 decision | EFF | RQ-40 |

### 5.2 Goal / portfolio level

| ID (Q) | Class / nature / status | Activation | Purpose → consumers | Prv | Nec | Control · options | Custom | Validation | Depends on | Recomp | Pending |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `GOL.goals` (2.1 + 2.2) | A/P/core | always | Portfolio units, horizon per portfolio, soft return targets, goal priority → portfolio set-up, horizon (BEL-H), feasibility check on save, report | P2 | R (≥1 goal) | repeating table: name · purpose (static list + other) · target amount (today's money) or "none" · horizon (year or years) · priority rank · flexibility (essential/important/aspirational) · use pattern (lump sum / gradual over N years / none) | yes (name, purpose) | horizon > 0; unique priority ranks; amount ≥ 0 | — | EFF BEL-H CAL PC MON REP | — |
| `GOL.portfolio_mapping` (2.3) | A/R/conditional | if ≥2 goals **and** S2/S5 admit both representations | Separate vs. combined portfolios → portfolio set-up | P1 | O | dropdown | no | — | `GOL.goals` | PC IMPL | S2/S5 |
| `LIQ.planned_withdrawals` (3.1) | A/F/core | always | Cash-buffer constraint; cash-flow schedule → Feasibility, implementation | P2 | O (empty allowed) | repeating table: amount · date · certainty | no | date ≥ today | `GOL.goals` (consistency) | EFF FEAS IMPL PC | — |
| `LIQ.external_buffer` (3.2) | A/F/core | always | Whether the engine must hold the emergency reserve → liquidity constraint | P2 | R | toggle + months of expenses | no | ≥ 0 | — | EFF FEAS | — |
| `LIQ.engine_cash_reserve` (3.3 + 3.4) | A/P/core | always | Minimum cash and access speed → liquidity constraint, instrument eligibility | P2 | R | toggle + amount (% or NOK) + access speed (days/weeks/months/>1 year) | yes | 0–100% | `LIQ.external_buffer` | EFF FEAS PC IMPL | — |
| `CF.contributions` (4.2) | A/F/core | always | Planned inflows → rebalancing via cash flows, trade sizing, projections | P2 | O (none allowed) | amount + frequency + reliability | no | ≥ 0 | — | IMPL PC REP | — |
| `POL.markets` (8.1 + 8.2) | A/R/core | always | Feasible universe → universe construction, comparison universe | P1 | R | multi-select include/exclude · options **pending S3/S5** (C/B-opts) | no | include ∩ exclude = ∅ | `ACC.accounts` (availability) | EFF UNIV ELIG PC | S5, RQ-07, RQ-38 |
| `POL.home_bias_view` (8.3) | A/P/conditional | if method-requires (S5 home-bias method) | Home-bias tilt → that method | P1 | O | dropdown | no | — | `POL.markets` | PC | S5 |
| `POL.instrument_permissions` (8.4) | A/R/core | always | Hard instrument constraints → universe, eligibility, feasibility | P1 | R | matrix allow/deny/undecided × instrument types · rows **B-opts** | no | — | `ACC.accounts`, B availability, `INV.complex_product_tests` | EFF UNIV ELIG FEAS PC | S3c, S4 |
| `POL.leverage` (8.5) | A/R/core | always | Leverage constraint → construction, feasibility, financing costs | P1 | R | dropdown: none / limited (max) / permitted · options **pending S3/S4** | yes (max, if admitted) | max ≥ 1 | `ACC.accounts` (margin availability) | EFF ELIG FEAS PC IMPL | S3, S4 |
| `POL.exclusions` (8.6) | A/P/optional | always | Ethical/sector/issuer filters → universe filter | P1 | O | multi-select (list **pending RQ-41**) + issuer search + text | yes | resolvable | — | EFF UNIV PC | RQ-41, RQ-38 |
| `POL.allocation_unit` (8.7) | A/R/core | always | Securities vs. asset classes/funds → universe type, scoring scope | P1 | R | dropdown: securities / asset classes & funds / both / no view · availability **C-opts** | no | — | `POL.markets` | UNIV ELIG PC | S5, RQ-07 |
| `POL.currency_hedging` (8.8) | C/R/methodological | if any admissible hedging approach exists | Currency policy → construction, implementation | P1 | O | dropdown **C-opts** | per method | — | `INV.consumption_currencies` | PC IMPL | S5, RQ-07 |
| `POL.wealth_scope` (5.3) | C/R/methodological | if a total-wealth method is admissible | Managed-only vs. total-wealth optimisation → construction | P1 | O | dropdown **C-opts** | no | — | — | ACT PC | S5/S7 |
| `POL.benchmark` (10.3) | C/R/methodological | always (shows "pending" until S7) | Comparison/evaluation → reporting, monitoring | P1 | O | dropdown **C-opts** + free-text wish (recorded, not used) | no | — | `INV.reporting_currency` | REP MON | S7, RQ-09 |
| `POL.keep_holdings` (6.2) | A/P/core | always (if A′ has holdings) | Holdings exempt from selling → hard constraint, transition plan | P2 | O | table referencing A′ positions | no | must exist in A′ | `STATE.holdings` | EFF FEAS PC IMPL | — |

### 5.3 Rebalancing policy (new group; configuration capability only)

**Placement decision.** Rebalancing is included in the S1 inventory as a
**configuration structure**. Users must eventually be able to express a
rebalancing preference, and the developer's UI contract needs the
conditional structure now. Admissible methods, parameters, and values are
**not** decided here; they are S13b research (RQ-44).

**Scope boundary.** *Target unchanged + weight drift → rebalancing* (S13b).
*New signal or information → new target or tactical allocation →
implementation* is **not** rebalancing and belongs to S13c/S13d. A trade
caused by a target change is never labelled a rebalancing trade.

**Five distinct layers:**

| Layer | Class | Example | Owner |
|---|---|---|---|
| 1 User preference | A | Prefers band-based over calendar | User (`REB.approach`) |
| 2 Methodological admissibility | C | Which approaches S13b admits | Research / eligibility funnel |
| 3 User-set parameter | A | A chosen band width, **only** where the admitting method marks it user-settable | User, within method bounds |
| 4 System-derived parameter | D | Band derived from transaction costs or an accepted optimisation | Engine, with provenance |
| 5 Portfolio State trigger | A′ → event | Current weights cross the *effective* threshold | Monitoring / implementation |

| ID | Class / nature / status | Activation | Purpose → consumers | Prv | Nec | Control · options | Custom | Validation | Depends on | Recomp | Pending |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `REB.approach` | A/R/core (capability) | always; shows "pending" until S13b admits ≥1 approach | Rebalancing preference → implementation (S13b) | P1 | R once ≥1 admissible | dropdown **C-opts**; candidate structure: calendar · threshold/band · hybrid · method-determined · custom (only if a method permits) | per method | must be admissible | — | IMPL MON | RQ-44 |
| `REB.calendar_params` | A or D | if approach ∈ {calendar, hybrid} | Frequency → implementation | P1 | per method | control set by the admitting method's contract | per method (parameter authority) | per method | `REB.approach` | IMPL | RQ-44 |
| `REB.band_params` | A or D | if approach ∈ {band, hybrid} | Band definition → implementation | P1 | per method | control set by the method contract (e.g. band type, width) | per method | per method | `REB.approach` | IMPL MON | RQ-44 |
| `REB.custom_spec` | A | if approach = custom **and** a method permits custom | Custom rule → implementation | P1 | R (when active) | structured editor (S13b) | yes | validated by method | `REB.approach` | IMPL MON | RQ-44 |
| `REB.use_cash_flows` | A/P/conditional | if `CF.contributions` or `LIQ.planned_withdrawals` non-empty **and** an admissible method supports it | Rebalance via inflows/outflows → implementation | P1 | O | toggle | no | — | `CF.contributions` | IMPL | RQ-44 |

`ENG.max_trades_per_month` constrains both rebalancing and signal-driven
implementation. Its interaction with each is resolved in S13b/S13c.

### 5.4 Account level

| ID (Q) | Class / nature / status | Activation | Purpose → consumers | Prv | Nec | Control · options | Custom | Validation | Depends on | Recomp | Pending |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `ACC.accounts` (6.1 configuration) | A/F/core | always | Broker × wrapper × currency → registries lookup, feasibility, asset location, costs | P2 | R (≥1) | repeating table: broker (**B-opts**: Nordnet, eToro, Other-unsupported) · wrapper (**B-opts per broker × jurisdiction**) · currency · existing/planned | no | broker offers wrapper; jurisdiction supports wrapper | `INV.tax_residence` | EFF FEAS UNIV ELIG TAX IMPL | S3a/b |
| `ACC.open_new_accounts` (6.3) | A/P/optional | always | Permission for what-if comparisons → what-if engine only | P1 | O | dropdown + text | yes | — | — | REP | — |
| `ACC.currency_accounts` (6.4) | A/P/optional | if any configured broker offers currency accounts (B) | FX-cost option → costs, implementation | P1 | O | toggle | no | — | `ACC.accounts`, B | IMPL TAX | S3b |
| `TAX.wealth_tax_position` (10.1) | A/F/conditional | if method-requires (tax-aware methods admitted) | Value of tax-aware decisions → tax methods only | P3 | O | dropdown band | no | — | `INV.tax_residence` | TAX PC | S13a |

### 5.5 Engagement and governance

| ID (Q) | Class / nature / status | Activation | Purpose → consumers | Prv | Nec | Control · options | Custom | Validation | Depends on | Recomp | Pending |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `ENG.max_trades_per_month` (9.2) | A/P/core | always | Execution burden limit → implementation, rebalancing, tactical | P1 | R | numeric | — | integer ≥ 0 | — | IMPL | S13 |
| `ENG.review_frequency` (9.3) | A/P/core | always | Run and report cadence → scheduler, report | P1 | R | dropdown | no | — | — | REP MON | — |
| `ENG.report_depth` (9.5) | A/P/optional | always | Report verbosity (UI preference; distinct from experience) → report | P0 | O | dropdown | no | — | — | REP | S14 |
| `GOV.autonomy` (9.4) | A/R/core | always; shows "pending" until S2 | What runs without approval → approval matrix | P1 | R once S2 defines it | dropdown · options **pending S2** | no | — | — | EFF | S2 |
| `META.profile` (new) | A/P0 | always | Profile name, schema version, declared version → workspace management | P0 | R | text + system fields | yes | — | — | — | RQ-39, RQ-43 |

### 5.6 Portfolio State (A′), derived values (D), retired

| ID (Q) | Class | Notes |
|---|---|---|
| `STATE.account_values` (6.1 value part) | A′ | Imported or entered; P2. Changes never alter preferences (§7) |
| `STATE.holdings` (6.5) | A′ | Instrument, quantity, cost basis, acquisition date; P2; import preferred |
| `STATE.cash` | A′ | Per account and currency; P2 |
| `DER.total_capital` (4.1) | D | Σ account values; no longer asked |
| `DER.realised_gains` (10.2) | D | From transaction history; no longer asked |
| `DER.horizon_per_portfolio` | D | From `GOL.goals` (+ mapping) |
| `DER.reporting_currency_proposal` | D | From `INV.consumption_currencies`; offered as a proposal |
| `DER.effective_permitted_instruments` | D | law ∩ wrapper ∩ broker ∩ `POL.instrument_permissions` |
| `DER.feasibility_thresholds` | D | From A′ + B (minimum commissions, minimum orders, fractional availability) |
| `DER.risk_capacity`, `DER.model_risk_parameters` | D | Calibration (RQ-02); raw `INV.risk_category` preserved |
| `DER.rebalancing_effective_params` | D | From `REB.*` + admitting method + A′/B |
| ~~hours per month~~ (9.1) | retired | No consumer; may be re-added under §8 if a purpose appears |

## 6. Interaction model

1. **Profiles.** A local workspace holds ≥1 profile (`META.profile`). Profiles are isolated. Export/import is a future capability (RQ-43).
2. **Sections.** Investor → Goals & liquidity → Accounts → Universe & instruments → Rebalancing → Engagement & governance. Only active fields are shown.
3. **"Why we ask".** Each field shows its purpose, consumers, necessity, and privacy class (from §5).
4. **Option states.**
   - Admissible options are selectable.
   - Options pending research are shown disabled, with "available after <stage>".
   - Options ruled out by facts or feasibility for *this* profile are shown disabled, with the reason.
5. **Missing values.** "Don't know" / "Prefer not to say" are allowed on every personal field. Partial saves are allowed. Missing *required* fields make the Effective Policy Statement incomplete, which blocks runs that need those fields.
6. **Editing.**
   - Each save creates a new Declared version (immutable) and triggers resolution (§7).
   - The user sees a diff of Declared changes and of the resulting Effective changes.
   - Remembered values are shown as "your saved value (date)", never as defaults.
7. **Derived proposals.** Shown with a "proposal" badge and a "how derived" link. Accept → stored as `accepted_proposal`. Reject → the user's value is stored and the proposal record kept.
8. **Conflict panel.** Lists every conflict record (§7.2) with actions: change my input · declare the narrowed value as my new input (creates a new Declared version; never automatic) · keep my input (it stays declared, shown as not effective) · open the explanation.
9. **Newly active fields.** When a method enters production and requires an inactive field, the user is notified: which method, why, necessity, privacy class. The field is optional to answer unless the method's contract makes it required for that method. If declined, the method is reported as ineligible for this profile; it is never run on imputed data.
10. **Effective view.** A read-only view of the Effective Policy Statement with provenance for each value. It is never edited directly.

## 7. Declared → Effective resolution and change propagation

### 7.1 Resolution rules

Inputs: Declared version *v* (A), Portfolio State snapshot (A′), facts
snapshot (B), method-registry snapshot (C).

| Step | Check | Outcome on failure |
|---|---|---|
| 1 | Schema validation (types, ranges, required-while-active) | **error** — the field is invalid; the Effective Policy Statement is incomplete |
| 2 | Activation and dependency | Inactive fields are `not_applicable`; dependent fields are re-evaluated |
| 3 | Facts (B): jurisdiction supported; wrapper offered and eligible; instrument availability; test requirements | **narrowed** (law ∩ wrapper ∩ broker ∩ preference) or **blocked** |
| 4 | Methodology (C): option admissible; parameter authority respected | **blocked** or **pending** (no admissible option yet) |
| 5 | Feasibility (Feasibility Engine with A′ + B) | **narrowed** / **blocked** with reasons |
| 6 | Internal consistency (e.g. goal horizons vs. withdrawals; targets vs. limits) | **conflict** — reported to the user; resolved per S2 ordering (RQ-23) or by the user, never silently |
| 7 | Derive D values with provenance | — |

**Per-field outcome:** `accepted` · `narrowed` · `blocked` · `pending` · `not_applicable` · `incomplete`.

**Declared is never rewritten (G1 clarification).** The precedence below
decides only **what can be implemented** in the Effective Policy Statement.
It is not a hierarchy of authority over the user's preferences.
- The Declared Policy Statement is preserved exactly as declared.
- Facts, legal or account constraints, feasibility, and methodology may give a preference the status blocked, narrowed, or pending in the Effective Policy Statement. They never replace the declared value.
- The engine never substitutes another option. Example: `declared = band rebalancing` → `effective status = pending/blocked`, `reason = no admissible band-rebalancing method`. It does not switch to calendar.
- An alternative is used only if the user has explicitly declared it. Whether fields support declared ordered alternatives is an S2 schema question (RQ-48).
- If a required effective value is blocked or pending, processes that need it are reported as unavailable, not run on a substitute.
- When the binding fact or method changes, the preserved declared value is re-resolved automatically without user re-entry.

**Class precedence fixed in S1 (implementability only):**
- B facts and hard feasibility > C admissibility > A preferences.
- Conflicts *between* A fields are presented to the user. Automatic ordering among A fields is S2's job (RQ-23).

**Never:**
- silent override, or rewriting or substituting a declared value;
- editing Effective directly;
- using a blocked value;
- imputing missing values;
- treating a remembered value as a default.

The Effective version is stored with a hash of (A *v*, A′ snapshot, B snapshot, C snapshot).

### 7.2 Conflict record

`field` · `declared_value` · `effective_value` (or none) · `outcome` ·
`binding_source` (fact ID@version | method ID@version | feasibility rule |
field) · `explanation` · `consequence` · `user_actions` ·
`first_seen` / `resolved_at`.

### 7.3 Change propagation

**Rule: invalidation is driven by the Effective diff, not the Declared diff.**
A declared change that leaves the Effective Policy Statement unchanged (for
example, a still-blocked preference) refreshes only the conflict panel and
report.

| Tag | Artefacts recomputed |
|---|---|
| EFF | Effective Policy Statement, conflict records |
| FEAS | Feasibility results, exclusion reports |
| UNIV | Feasible universe; declared comparison universe (ADR-0013) |
| ELIG | Eligible/admissible method sets; activation set (ACT) |
| ACT | Set of active conditional fields |
| BEL-H | Horizon-specific beliefs only (ADR-0009 exception) |
| CAL | Derived risk parameters / calibration (D) |
| PC | Candidate portfolios, aggregation, target portfolio |
| IMPL | Drift evaluation, rebalancing evaluation, trade lists, sizing |
| TAX | Tax computations, asset location |
| MON | Monitoring thresholds and alerts |
| REP | Report content |

**By event type:**

| Event | Recomputes | Must **not** recompute |
|---|---|---|
| A change (Declared *v*+1) | EFF + the field's tags, gated by the Effective diff | Market beliefs (except BEL-H for horizon fields; UNIV for universe fields) |
| A′ change (state) | FEAS (size-dependent rules), IMPL, TAX, MON, REP; derived thresholds | A values, CAL inputs from preferences, beliefs, ELIG unless a size-dependent eligibility rule flips |
| B change (fact version) | EFF → affected tags; staleness flags | — |
| C change (method admitted/retired) | ELIG, ACT, EFF → affected tags; newly active fields notified | — |
| D change | Downstream of that D only | Its own inputs |

## 8. Extensibility rules (adding or changing fields without redesign)

1. A new field requires a complete §2 specification, including purpose, consumers, privacy, and necessity (ADR-0014 §8).
2. **Adding a field ≠ activating it.** Activation comes only from a satisfied field condition or a production method's `required_profile_fields`.
3. A new consumer or purpose for an existing personal field requires an ADR.
4. IDs are never reused. Retired fields keep their spec entry. Their stored values are handled by the privacy/retention policy (S8).
5. Option lists sourced from B or C update without schema change. Static lists change only by spec revision.
6. Schema versioning and migration of saved profiles are S2/S8 machinery (RQ-47).

## 9. Deferred questions (not resolved in S1)

| Topic | Where |
|---|---|
| Market, instrument, leverage, exclusion, wrapper option lists | S3, S4, S5; RQ-41, RQ-42 |
| Allocation-unit and hedging availability; total-wealth scope | S5, S7; RQ-07 |
| Risk-preference calibration, elicitation instrument, drawdown-reaction levels | S2, S11; RQ-02 |
| Conflict-priority ordering among A fields | S2; RQ-23 |
| Autonomy / approval-matrix options | S2 |
| Benchmark set | S7; RQ-09 |
| Rebalancing taxonomy, admissible methods, parameter authority | S13b; RQ-44 |
| Role of self-reported experience vs. broker tests | S3c; RQ-45 |
| Anticipated residence change / multi-period tax planning | S3a, S13a; RQ-46 |
| Local storage, profiles, export/import, schema migration | S8; RQ-39, RQ-43, RQ-47 |
| External data flows and consent | S8, S12; RQ-40 |
