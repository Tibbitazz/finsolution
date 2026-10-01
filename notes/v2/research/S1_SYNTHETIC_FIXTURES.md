# S1 — Synthetic test fixtures (class E)

**Document status:** DRAFT (S1, for G1) · **Basis:** [S1_INPUT_SPECIFICATION.md](S1_INPUT_SPECIFICATION.md), ADR-0014

Fixtures test **architectural behaviour**: validation, conflict records,
activation, and recomputation. They specify expected *system behaviour*,
never an expected investment recommendation.

**Rules:**
- All values are hypothetical. No fixture is derived from any real user's profile.
- Facts used by fixtures come from a **stub registry** (`STUB.*`), labelled as test data. Stub facts are never registry facts and assert nothing about real brokers, laws, or products.
- Methods named `STUB-M*` are placeholder method contracts. They do not imply that any real method is admissible.

## Stub registry and methods used

| Stub | Content |
|---|---|
| `STUB.jur.supported` | Jurisdiction J-A supported; J-Z not supported |
| `STUB.broker.X` | Offers wrappers W-1 (eligible to J-A residents; only instrument types E, F) and W-2 (all types except D); no product type D (CFD-like) |
| `STUB.broker.Y` | Offers W-2; product type C requires a knowledge test |
| `STUB.min_order` | Broker X minimum order 500 units of currency |
| `STUB-M1` | Covariance method requiring N ≥ 30 assets (eligibility contract) |
| `STUB-M2` | Risk-capacity method whose contract lists `INV.income_stability` in `required_profile_fields` |
| `STUB-M3` | Band-rebalancing approach; band width user-settable within [b_min, b_max] |
| `STUB-P1` | Derivation rule proposing reporting currency = primary consumption currency |

## Fixtures

| ID | Setup (hypothetical) | Event | Expected validation / conflicts | Expected recomputation | Must not happen |
|---|---|---|---|---|---|
| FX-01 Unsupported jurisdiction | `INV.tax_residence` = J-Z | Save | Conflict: outcome `blocked`; binding `STUB.jur.supported`; consequence: tax and wrapper rules unavailable, no runs that need TAX/FEAS; actions: change input / wait for coverage | EFF, FEAS | Applying J-A (or any) rules by default |
| FX-02 Conflicting goal horizons | Goals G1 (horizon 2y, essential, lump sum), G2 (horizon 30y, aspirational); `GOL.portfolio_mapping` inactive (not admitted) | Save | No error. Two horizons recorded. Consistency check flags that a single combined portfolio cannot serve both horizons; reported to the user (S2 ordering pending) | EFF, BEL-H (both horizons), PC | Silently averaging horizons; auto-choosing a priority |
| FX-03 Instrument unavailable at broker | `ACC.accounts` = broker X only; `POL.instrument_permissions` allows type D | Save | Type D `narrowed` out of `DER.effective_permitted_instruments`; binding `STUB.broker.X`; actions: add an account that offers D / remove the permission | EFF, UNIV, ELIG | Silently dropping D without a record; treating D as available |
| FX-04 Complex instrument without eligibility | Broker Y; type C allowed; `INV.complex_product_tests` (activates) = not taken | Save | `INV.complex_product_tests` becomes active and required. Type C `blocked` (test missing); action: take the test, then update | ACT, EFF, FEAS, ELIG | Inferring eligibility from experience or education |
| FX-05 Method ineligible for universe | Universe yields N = 12; user prefers a method using `STUB-M1` | Run | `STUB-M1` excluded with an exclusion record (N = 12 < 30); preference recorded but not effective | ELIG, FEAS | Running `STUB-M1` anyway; hiding the exclusion |
| FX-06 Preference vs. account/legal constraint | `POL.leverage` = permitted (max 2); only account is W-1 (no margin in stub) | Save | Leverage `narrowed` to none; binding `STUB.broker.X/W-1`; declared value retained | EFF, FEAS, PC | Overwriting the declared value |
| FX-07 Multiple accounts and wrappers | Accounts: X/W-1 and Y/W-2 | Save | Per-account permitted sets computed separately; union is available at portfolio level with account assignment | EFF, UNIV, TAX, IMPL | Merging accounts into one permitted set without account attribution |
| FX-08 Missing optional information | All optional fields "don't know" / empty; required fields present | Save | Effective complete; optional-dependent features marked unavailable (e.g. `INV.volatility_range` cross-check skipped) | EFF | Imputing values; blocking runs that don't need the optional fields |
| FX-09 Policy change invalidates downstream | Saved Effective v3 exists with target portfolio | User adds an exclusion that removes held assets | Effective diff non-empty | EFF, UNIV, PC, IMPL, REP recomputed; beliefs untouched except a declared comparison-universe change (UNIV) | Recomputing unrelated beliefs; keeping the stale target |
| FX-10 State change leaves preferences stable | Same profile | `STATE.account_values` rises 10% (import) | `DER.feasibility_thresholds` recomputed; no conflicts unless a size rule flips | FEAS (size rules), IMPL, TAX, MON, REP | New Declared version; recalibration from preferences; changes to A values |
| FX-11 Derived proposal rejected | `INV.consumption_currencies` = {K}; `STUB-P1` proposes reporting currency K | User selects L instead | Stored `INV.reporting_currency` = L (`user_entered`); proposal record kept with provenance | EFF, REP, MON | Storing K; re-proposing K on every save as if a default |
| FX-12 Editing a remembered value | Saved Declared v5 with `INV.max_one_year_decline` = x | User opens editor, changes to y | Editor shows x as "your saved value (date)". Save creates v6 with y; v5 immutable | EFF, CAL, PC, MON per Effective diff | Labelling x a system default; mutating v5 |
| FX-13 Conditional field activates | `STUB-M2` moves to production; profile has no `INV.income_stability` | Method admitted (C change) | User notified (method, purpose, privacy class). Until answered, `STUB-M2` is ineligible for this profile | ELIG, ACT, EFF | Running `STUB-M2` on an imputed value; collecting the field earlier |
| FX-14 Effective-unchanged declared change | `POL.instrument_permissions` already narrowed by broker (FX-03); user toggles another unavailable type | Save | Declared v+1 stored; Effective unchanged; conflict list updated | EFF (conflicts only), REP | Invalidating PC/IMPL |
| FX-15 Rebalancing: user parameter within method bounds | `REB.approach` = band via `STUB-M3`; user sets width outside [b_min, b_max] | Save | `REB.band_params` validation error (parameter authority); action: choose within bounds | EFF | Accepting the out-of-bounds value; silently clamping |
| FX-16 Rebalancing vs. signal change | Target unchanged; drift crosses effective band (A′ event) vs. separately a new tactical signal changes target | Monitoring tick | Drift event classified as rebalancing (S13b path); target change classified as a new target → implementation (S13c/d path); both obey `ENG.max_trades_per_month` | IMPL (rebalancing) vs. PC → IMPL (signal) | Labelling the signal-driven trade as rebalancing |
| FX-17 Rebalancing approach not yet admissible | No approach admitted (pre-S13b) | Open rebalancing section | `REB.approach` shown "pending S13b"; Effective field `pending`; runs needing rebalancing report the gap | EFF | Applying an unadmitted default approach |
