# 10 — Scope-exclusion register

**Document status:** STABLE (established at G3 closure, 2026-10-01) · **Basis:** the ADRs cited per row

This register prevents excluded functionality from re-entering later
stages unnoticed. It distinguishes three kinds of entry:

| Kind | Meaning | How it could change |
|---|---|---|
| **E — Excluded from current scope** | Deliberately not built, researched, or maintained now. The architecture could be extended to include it | New ADR (and schema change where relevant) |
| **I — Prohibited by an architectural invariant** | Contradicts a foundational design rule; the architecture is built to prevent it | Superseding the foundational ADR. This is a redesign, not an extension |
| **D — Deferred, not excluded** | Recorded here only to show it is not an exclusion | Arrives at its owner stage |

"Excluded" does not mean "architecturally impossible". Only kind I entries
are designed to be impossible.

| # | Item | Kind | Basis | Notes |
|---|---|---|---|---|
| X-01 | Pension saving and pension products (IPS, EPK, any pension wrapper), pension taxation | E | ADR-0008, ADR-0020 | Rejected by validation (FX3-16) |
| X-02 | Pension wealth (in total-wealth state, risk capacity, outside assets) | E | ADR-0020 | `INV.outside_assets` excludes pension types |
| X-03 | Wealth tax: facts, research, calculations, effects in comparison or construction; fields collected solely for it | E | ADR-0021 | `TAX.wealth_tax_position` retired; rejected by validation (FX3-23) |
| X-04 | Broker-routing optimisation | E | Charter §2; ADR-0006 | The architecture must keep it possible later |
| X-05 | Broker or account ranking, "best" or preferred broker, default sort by cost | E | ADR-0007 (neither preferred); ADR-0019 §12 | Descriptive comparison only |
| X-06 | Personal financial data in the public repository; committed run manifests containing profile contents | I | ADR-0014 | Local user layer is git-ignored; manifests reference hashes |
| X-07 | Real profiles or legacy questionnaire values as system defaults or fixtures; technical defaults for personal fields | I | ADR-0014, ADR-0001 | Synthetic fixtures only |
| X-08 | Legacy (ENGINE_V1) values or claims as inputs | I | ADR-0001; 03 §4.5 | Leads only, as `legacy_unverified` |
| X-09 | Implicit substitution of undeclared alternatives; rewriting Declared values | I | ADR-0014 §5, ADR-0016 | Resolution invariants |
| X-10 | Universal risk-category → γ mapping; γ as a portable investor attribute; a single global γ across formulations | I | ADR-0010, ADR-0018 | Parameters scoped to formulation |
| X-11 | Preferences altering beliefs (except the declared horizon exception) | I | ADR-0009, ADR-0013 | — |
| X-12 | Cross-purpose use of personal fields (e.g. age as an investment signal) | I | ADR-0014 §8 | Undeclared consumers rejected (FX2-16) |
| X-13 | Portfolio-size categories or buckets as registry or method concepts | I | ADR-0007; 03 §4.6 | Capital is continuous |
| X-14 | Self-reported experience as an eligibility grant; engine-run substitutes for broker-required tests | I | ADR-0019 (D3-07); S1 spec 1.7 | Field 1.7 inactive |
| X-15 | Treating unknown as false or not offered; a single attribute (e.g. domicile) implying ineligibility; unqualified jurisdiction support | I | ADR-0019 | Carried invariants (OPEN_QUESTIONS) |
| X-16 | Methods that do not declare their reads and dependencies participating in production | I | ADR-0015 (D2-08) | Ineligible by construction |
| X-17 | Execution-related authority before S13 safeguards | D | ADR-0017 | Architecturally supported; disabled until safeguards |
| X-18 | Individual-security master | D | D3-d | S6 |
| X-20 | UEPO, SEPO, DEPO (and aliases) | E | ADR-0024 §7 | Excluded unless the owner explicitly reopens them |
| X-21 | ANG's illustrative rankings (Exhibit 7), ensemble weights (Exhibit 8) and parameters as priors, quality scores or defaults | I | ADR-0023 §8–9 | Research objects only |
| X-22 | LLM-edited portfolio weights; opportunistic parameter tuning in revisions | I | ADR-0024 §2; 05 R1 | — |
| X-19 | Hard-coded investment methodology (any specific model, γ, volatility target, benchmark, band, rebalancing approach, factor weights, score mapping, tactical rule, routing logic) before its gate | D | ADR-0022, ADR-0001 (P1) | Typed interfaces until accepted |

**Rule:** a later stage that touches an E or I item must cite this register.
Changing an E item requires a new ADR. Changing an I item requires
superseding the basis ADR.
