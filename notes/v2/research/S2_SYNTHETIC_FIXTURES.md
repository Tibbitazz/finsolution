# S2 — Synthetic boundary fixtures (class E)

**Document status:** STABLE (accepted at G2, 2026-10-01; FX2-03 amended and FX2-17 … FX2-20 added at G2) · **Basis:** [S2_CONFIGURATION_MACHINERY.md](S2_CONFIGURATION_MACHINERY.md); stubs as in [S1_SYNTHETIC_FIXTURES.md](S1_SYNTHETIC_FIXTURES.md)

Hypothetical values, stub facts (`STUB.*`), and stub methods (`STUB-M*`)
only. Each fixture specifies expected machinery behaviour, never a
recommendation.

Additional stubs:
- `STUB-M5` — band rebalancing (admitted, then later retired).
- `STUB-M6` — calendar rebalancing (admitted).
- `STUB-CAL1` — calibration method consuming `INV.income_stability` and producing a model parameter with units.
- `STUB-CAP1` — risk-capacity method producing a capacity estimate (D) from horizon and liquidity inputs.
- `STUB-REQ1` — feasibility method evaluating whether a goal target is attainable within declared limits under a belief snapshot.

| ID | Setup | Event | Expected machinery behaviour | Must not happen |
|---|---|---|---|---|
| FX2-01 Genuine inconsistency (I1) | `POL.keep_holdings` includes X; `POL.exclusions` excludes X's issuer | Save | I1 conflict record naming both fields; both declared values preserved; X's effective treatment `pending` user resolution | Automatic ranking of one field over the other |
| FX2-02 Separate goals (T2) | G1: 2-year essential lump sum; G2: 30-year aspirational growth; different loss tolerances declared per goal | Save | Classified T2; requirements attached to their goals; no conflict record | Treating the goals as conflicting; averaging horizons or tolerances |
| FX2-03 Competing objectives (T1) | One goal with a high return target and a low volatility preference | Save | Classified T1: a `TradeOffRecord` (versioned; fields, goal, explanation) is stored in structured state, appears in the report and audit trail, and is passed to construction. No conflict record; the trade-off is **not resolved** by the configuration layer | Forcing the user to rank; auto-adjusting either value; dropping the trade-off from state |
| FX2-04 Declared fallback | `REB.approach` = [band, calendar]; band inadmissible, `STUB-M6` admitted | Save | Effective uses calendar with `alternative_used = 1`; Declared unchanged | Recording calendar as the user's preference |
| FX2-05 No declared fallback | `REB.approach` = [band] (empty fallback list); band inadmissible | Save | Effective `pending`; reason cites the method registry; no substitution | Inferring calendar as a reasonable substitute |
| FX2-06 Method retired after creation | Effective v4 uses `STUB-M5` (band) | `STUB-M5` retired (C change) | Re-resolution: `pending` (or the declared fallback if present); downstream nodes reading the rebalancing parameters dirtied; user notified; Declared unchanged | Silent continuation with the retired method; deleting the declared value |
| FX2-07 Limited recomputation | Two portfolio units G1, G2 | Change G2 horizon | Dirty: G2 horizon-keyed belief nodes, G2 candidates/target, G2 trade lists, G2 monitoring, report sections for G2. Clean: registries, horizon-independent estimates, all G1 artefacts | Recomputing G1 or any registry |
| FX2-08 Presentation-only change | Any profile | Change `ENG.report_depth` | Only report nodes dirty | Recomputing covariance, beliefs, portfolios, or trade lists |
| FX2-09 Semantics-preserving rename | Field `A.x` renamed `A.y` in spec v2, mapping flagged `semantics_preserving` | Migration | New Declared version with migration provenance; v1 versions and their Effective versions remain reproducible under the v1 schema | Rewriting v1 in place |
| FX2-10 Semantic change | Field meaning changes materially (e.g. a loss measure redefined) | Schema evolution | New field ID; no automatic migration; user prompted to answer the new field; old value retained as history and not reinterpreted | Copying the old value into the new field |
| FX2-11 Analysis without execution authority | Grants: analyse, propose, construct, generate trade list; none for stage/submit/execute | Run, then attempt to stage orders | Trade list produced. Staging rejected: authority missing; dimension 6 not grantable before S13 | Staging or submitting orders; inferring authority from other grants |
| FX2-12 Missing conditional risk input | `STUB-CAL1` in production requires `INV.income_stability`; user declines ("prefer not to say") | Resolve | Only `STUB-CAL1` (and the artefacts that read it) become ineligible or unavailable; the rest of the Effective Policy Statement is complete | Invalidating the whole profile; imputing income stability |
| FX2-13 Unit mismatch | A calibration method expects decimal annual returns; an input is declared as percent monthly | Run | Explicit unit conversion recorded in the derivation record, or a validation error if no conversion is defined | Silent coercion; parameter computed on mismatched units |
| FX2-14 Hard constraint on a realised outcome | A constraint declared `hard` on realised one-year drawdown | Validate | Rejected as `hard` (subject is not a decision-time deterministic function); allowed as `soft` on an ex-ante measure or as `trigger` | Accepting it as hard |
| FX2-15 Undeclared dependency | A method contract omits one of its reads | Eligibility | Artefact flagged non-cacheable; method fails eligibility for an incomplete contract | Falling back to recomputing the whole graph |
| FX2-16 Undeclared consumer of personal data | A method reads `INV.birth_year` without being in its `consumers` list | Graph validation | Edge rejected (purpose limitation); method not deployable until spec and ADR updated | Silent use of the field |
| FX2-17 Unattainable goal (F1) | Goal G with target T and a declared loss limit; `STUB-REQ1` finds T unattainable under belief snapshot B₁ | Save; later beliefs move to B₂ | A versioned `FeasibilityFinding` citing G, the limit, B₁, and the method version; goal G and its target unchanged. Under B₂ the finding is re-evaluated: superseded if T becomes attainable, retained (new version) if not; lineage kept | Modifying T or the limit; hiding the finding; treating it as a contradiction in the Policy Statement |
| FX2-18 Field without ordered alternatives | `POL.leverage` (`supports_ordered_alternatives = false`) declared "permitted, max 2"; account allows no leverage; "none" is available | Save | `POL.leverage` `narrowed`/`blocked` per facts; no other option is selected on the user's behalf; `ConflictRecord` I2 | Selecting another option as a substitute; enabling an alternatives list for this field implicitly |
| FX2-19 Alternatives strictly as declared | `REB.approach` (supports alternatives) declared [band, hybrid]; both inadmissible; calendar admissible but **not declared** | Save | Effective `pending`; `alternative_used = none`; reason lists both declared options | Using calendar because it is available and "reasonable" |
| FX2-20 Preference–capacity disagreement | Stated `INV.risk_category` = Aggressive, `INV.max_one_year_decline` = 40%; `STUB-CAP1` estimates low capacity | Resolve | A finding record exposing the disagreement, referencing both objects and the capacity method version. Stated values and the capacity estimate unchanged. No capacity-based hard constraint applied (pending S11) | Overwriting the stated preference; converting capacity into a preference; silently limiting the portfolio |
