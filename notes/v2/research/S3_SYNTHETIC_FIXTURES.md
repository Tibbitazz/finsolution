# S3 — Synthetic registry and resolution fixtures (class E)

**Document status:** DRAFT (S3, for G3) · **Basis:** [S3_REGISTRY_ARCHITECTURE.md](S3_REGISTRY_ARCHITECTURE.md) · stubs as in [S1_SYNTHETIC_FIXTURES.md](S1_SYNTHETIC_FIXTURES.md) and [S2_SYNTHETIC_FIXTURES.md](S2_SYNTHETIC_FIXTURES.md)

These fixtures test **registry and resolution behaviour**. They prescribe no
investment, broker, or account choice. Mechanics use stub facts (`STUB.*`),
stub brokers (`STUB-BRK-A`, `STUB-BRK-B`), stub wrappers (`STUB-WRP-1`),
and stub methods (`STUB-M*`), so a test never depends on a real fact staying
true. Where a real registry record motivated a fixture, it is named as the
*analogue*. The fixture still uses the stub.

**Notation:** `Fact(t | k)`: valid time t, knowledge time k (§2).

## Required at S3 approval (1–16)

| ID | Setup | Event / query | Expected behaviour | Must not happen |
|---|---|---|---|---|
| FX3-01 Announced 2026, effective 2027 | `STUB.rate` v1 = 22% effective 2026-01-01; v2 = 23%, `enacted_not_yet_effective`, `announced_on` 2026-10-07, `effective_from` 2027-01-01 | `Fact(2026-12-15 | 2026-12-15)`; `Fact(2027-03-01 | 2027-03-01)` | 22% for 2026; 23% for 2027. v2 visible in a "future-effective" listing with its status | 23% applied to any 2026 calculation |
| FX3-02 Proposal never effective | `STUB.discount_removal`, `legal_status = proposed` (analogue: NOU 2026:9) | Any `Fact(t | k)`; then the proposal is withdrawn | Never returned by `Fact`; visible only via explicit proposal queries; withdrawal recorded as a new version (`withdrawn`) | Any calculation using the proposed value; deleting the proposal record |
| FX3-03 Historical rule | `STUB.factor` with hypothetical values a (2021), b (2022), c (2023 onward) as successive intervals | Historical analysis for 2022 with k = now | b returned for t = 2022-06-30 | Applying today's value to a past date |
| FX3-04 Broker fee changes | `STUB-BRK-A.commission` 0.10% until 2026-06-30; 0.08% from 2026-07-01 (v2 supersedes v1 for later t) | Cost illustration for trades dated 2026-05 and 2026-08 | 0.10% and 0.08% respectively; both versions retained with lineage | Overwriting v1; applying 0.08% to the May trade |
| FX3-05 Broker capability changes | `STUB-BRK-A.api.new_subscriptions` = open until 2026-03-31, closed after (analogue: Nordnet API) | Re-resolve a config that depends on API onboarding, at t = 2026-10-01 | Broker layer `unavailable` for new API onboarding, with the source and date; dependent authority grants stay non-operational; finding raised | Treating the capability as available because it was available earlier |
| FX3-06 Legal but not at broker | Instrument type X: legal = permitted; wrapper = permitted; `STUB-BRK-B` does not offer X | Build external admissibility for (BRK-B, WRP-1) | Excluded with explanation "Broker = unavailable"; legal and wrapper layer results retained | Explaining the exclusion as a legal restriction; dropping layer results |
| FX3-07 At broker, prohibited by wrapper | X offered by `STUB-BRK-A`; `STUB-WRP-1` permits only EEA-domiciled shares; X is non-EEA (analogue: ASK) | Admissibility for (BRK-A, WRP-1) and (BRK-A, ordinary account) | WRP-1: excluded, "Wrapper = prohibited", citing the wrapper rule. Ordinary account: externally admissible | Excluding X from the ordinary account; citing the broker |
| FX3-08 Externally feasible, later methodologically inadmissible | X externally admissible (legal, wrapper, broker all permit); `STUB-M7` (the only method using X) later retired | Re-resolution | Method layer → `ineligible`; external layers unchanged; explanation distinguishes "Method = ineligible" from the external layers; Declared unchanged | Rewriting external facts; deleting X from the registry |
| FX3-09 Appropriateness test | Product type P (complex); BrokerImplementation at `STUB-BRK-A`: test required (implements RegRule `STUB.reg.appropriateness`); user's `INV.complex_product_tests` row for P = not passed | Resolve | P `pending` with the reason "broker test required", citing the RegRule and the BrokerImplementation separately | Using self-reported experience (field 1.7) to admit P; marking P legally prohibited |
| FX3-10 Unknown stays unknown | `STUB-BRK-B.fractional` = null, `unavailable` (analogue: eToro ASK, fractional shares) | Feasibility check of a config needing that capability | Check returns `unknown`; outcome `pending` with an F-type finding; comparison cell shows "unknown" | Coercion to `false` (silent prohibition) or `true` (silent permission) |
| FX3-11 Conflicting authoritative facts | Two official broker sources disagree on a fee: records `.fee_page` and `.help_article`, both `unresolved_conflicting`, linked (analogue: eToro inactivity fee) | Cost query; registry review | Neither returned as current; cost component `unknown`; both shown side by side for review; owner prompted | Picking one by recency or plausibility; averaging |
| FX3-12 Layered withholding | `STUB.W1` 30%; `STUB.W2` treaty 15%; `STUB.W5` at BRK-A: treaty rate with condition "local-market listing"; instrument listed on a non-local market | Withholding projection | W1, W2 reported separately; W5 condition unmet, so the actually withheld rate is `unknown` (or W1 if a source states it), never assumed equal to W2; W7 credit capped per rule | Assuming actually withheld = treaty rate |
| FX3-13 Future-effective fact does not leak | `STUB.threshold` v2 recorded 2026-10-01 with `effective_from` 2027-01-01 | Current run (t = k = 2026-10-01) | v1 used; v2 listed as future-effective only | v2 in any current-year computation, cache, or report figure |
| FX3-14 Unsupported jurisdiction | User declares `INV.tax_residence` = `STUB-JUR-X` (no verified domains) | Resolve | Jurisdiction `unsupported`; I2 conflict listing the missing domains (§9); tax-dependent artefacts `pending`; Declared preserved | Falling back to Norwegian or generic rules |
| FX3-15 Descriptive comparison | Two configurations (BRK-A × WRP-1; BRK-B × ordinary account) with mixed known/unknown cells | Comparison request, with and without a hypothetical trade | Matrix of facts with status, level, and source per cell; neutral order; optional cost illustration labelled as arithmetic on published fees | Score, rank, "best" label, default sort by cost, highlighting |
| FX3-16 Excluded pension product | User enters an outside-asset row of type pension, or attempts a pension wrapper | Validation | Rejected as out of scope (ADR-0020); not in the investable universe, total-wealth state, risk capacity, or comparison | Storing it as outside wealth; creating a conditional pension field |

## Additional fixtures (proposed)

| ID | Setup | Event / query | Expected behaviour | Must not happen |
|---|---|---|---|---|
| FX3-17 Unavailable period not substituted | `STUB.shield` 2025 = 3.6% verified; 2026 = null, `unavailable` (analogue: shielding rate) | Tax projection for income year 2026 | Projection component `unknown`, or computed only under an explicit, labelled user scenario. Finding raised | Silently carrying the 2025 value forward |
| FX3-18 Unknown tax treatment propagates | `STUB.wrapper.credit` = null (analogue: credit inside ASK) | Projection of after-tax dividend in WRP-1 | Component `unknown`; any figure that depends on it is flagged | Assuming no credit, or full credit |
| FX3-19 Stale fact | `STUB-BRK-A.commission` past `reverify_by` | Run producing a trade-cost estimate | Fact returned with the `stale` flag; run requires owner approval (03 §4); re-check task raised | Treating it as fresh; silently dropping the cost |
| FX3-20 Event-driven re-check | Broker announces a fee change effective in 30 days | Registry update | New version recorded as future-effective once verified; prior version superseded only from the new `effective_from`; until verified, the announcement is recorded `announced` | Applying the announced fee early; overwriting the old version |
| FX3-21 Interpretation labelled | Legal layer for X = restricted, `verification_status = interpretation` (analogue: US ETF retail access under PRIIPs) | Admissibility explanation | Explanation states the restriction **and** that it is an interpretation, citing the underlying rule | Presenting the inference as an explicit source statement |
| FX3-22 Knowledge-time reproduction | A run on 2026-11-01 used `STUB.rate` v1; on 2026-12-01 a corrected v1′ (same valid time) is recorded | Reproduce the 2026-11-01 run | With k from the run manifest, v1 is returned and the output reproduces exactly; with k = now, v1′ is returned and the difference is reported | Rewriting history; failing to reproduce the original run |
