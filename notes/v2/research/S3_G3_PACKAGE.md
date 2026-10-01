# S3 — Gate G3 package

**Document status:** DRAFT (for G3 review; revision 2, 2026-10-01, incorporating the owner's G3-review corrections) · **Branch:** `stage/s03-external-facts`

**Approval semantics:**
- **Part A** contains external facts, accepted into registry v1 on stated evidence. They are not preferences.
- **Part B** contains proposed architectural decisions.
- **Part C** contains gaps, classified A/B/C by consequence.

**Companion documents:**
- [S3_REGISTRY_ARCHITECTURE.md](S3_REGISTRY_ARCHITECTURE.md)
- [S3_FINDINGS.md](S3_FINDINGS.md)
- [../facts/](../facts/)
- [S3_SYNTHETIC_FIXTURES.md](S3_SYNTHETIC_FIXTURES.md)
- [ADR-0019](../decisions/ADR-0019-external-fact-registry.md) (PROPOSED)
- [ADR-0020](../decisions/ADR-0020-pension-saving-excluded.md) and [ADR-0021](../decisions/ADR-0021-wealth-tax-excluded.md) (ACCEPTED, owner instructions)

**Meaning of accepting registry v1:**
- Each fact is accepted at its stated source, scope, verification level, valid-time coordinates, and knowledge-time coordinates, based on the evidence available on its verification date (2026-10-01).
- Acceptance does not certify any fact forever.
- Later authoritative changes create new effective-dated facts and never rewrite historical ones.

---

## Part A — Research findings

| Area | Where | Highlights |
|---|---|---|
| Norway income tax and wrappers | S3_FINDINGS §2; no_tax.yaml, no_wrappers.yaml | 22%; factor 1.72; shielding 2025 3.6%; 2026 shielding and 2027 parameters unavailable; fund rule; ASK rules from Skatte-ABC 2025/2026 incl. withdrawals, FX, transfers; exit tax. **Wealth tax removed (ADR-0021)** |
| ASK withholding credit | S3_FINDINGS §2.1 | **Corrected:** credit rules may apply on a taxable withdrawal (verified); calculation, tracking, input-value interaction, carry-forward application, and broker information not established |
| Withholding W1–W9 | §3; withholding_us_no.yaml | W8 now references the seven-part ASK decomposition |
| Regulation, PRIIPs chain | §4, §4.1; regulation_eea_no.yaml | Conditional rule verified; "US ETFs unavailable" remains interpretation; ESMA paragraph citations re-verified (one correction: ¶64–65) |
| RQ-45 | §5 | Firm obligation; no engine consumer established, none ruled out |
| RQ-49 | §6 | A1–A13 authoritative statements; A vs. B unresolved; capability register |
| Nordnet / eToro | §7–§8 | Unknown ≠ unsupported audit (§9); eToro inactivity conflict unresolved after second attempt |

Registry v1 contains **83 records** (62 verified, 3 interpretation, 2
unresolved_conflicting, 16 unavailable). All pass the contract check.

## Part B — Decisions

**Owner instructions recorded (not for re-approval):**

| ID | Decision | Recorded in |
|---|---|---|
| D3-a | G3 approves registries, not account configuration | 08; CHANGELOG |
| D3-b | All pension saving and products excluded | ADR-0020 |
| D3-c | Logical record contract; YAML provisional | Architecture §1 |
| D3-d | Instrument-type level only | Architecture §6 |
| D3-e | **Wealth tax excluded entirely**; `TAX.wealth_tax_position` retired; S3 wealth-tax records removed; jurisdiction domain removed | ADR-0021 |

**For approval (final table):**

| ID | Proposed decision | ADR / location |
|---|---|---|
| D3-01 | Logical fact-record contract; `legal_status` + `verification_status` + `verification_level`; mapping from vocabulary E; conflicts as linked records, not versions | ADR-0019 §1–2 |
| D3-02 | Bitemporal `Fact(t \| k)`: proposals never returned; future-effective facts never leak; "current" derived at query time; runs pin k. Unknowns propagate as unknown → `pending` + finding; never false/0 or a prior period's value | ADR-0019 §3–4 |
| D3-03 | Admissibility layers legal ∩ wrapper ∩ broker ∩ methodological ∩ user with binding sources. **Unknown ≠ unsupported:** `not_offered`/`prohibited` require a source statement; absence of evidence is `unknown` | ADR-0019 §5 |
| D3-04 | Withholding layers W1–W9; treaty ≠ actually withheld. W8 decomposed for ASK into applicability, timing, calculation, tracking, input-value interaction, carry-forward, and broker information; "may apply" kept conditional | ADR-0019 §6; S3_FINDINGS §2.1 |
| D3-05 | Instrument-type attribute schema (S6); RegRule ≠ BrokerImplementation | ADR-0019 §7–8 |
| D3-06 | Re-check cadences and event triggers (incl. each new Skatte-ABC edition); `stale` flag with owner approval when stale facts feed hard constraints, costs, or tax. Jurisdiction support needs **eight** covered domains (wealth tax removed); domain-level vs. fact-level coverage; no fallback | ADR-0019 §9–10 |
| D3-07 *(revised per owner)* | **Field 1.7 `INV.investment_experience` is not retired.** It stays an inactive, conditional schema capability, **not collected by default**, pending RQ-45. Self-reported experience **never independently grants product eligibility**. Actual regulatory and broker eligibility is determined by applicable rules and the broker's process. The engine **never substitutes its own assessment** for a broker-required appropriateness test. The field activates only if later research establishes a legitimate consumer | S1 spec row 1.7; FX3-25 |
| D3-08 *(revised per owner)* | **No universal legal-review prerequisite.** RQ-49 stays open. The full S2 authority model and the capability spectrum from analytics to unattended execution are preserved. Capabilities are recorded in the register `capability → evidence/regulatory status → unresolved issue → required dependency/safeguard → enablement status` (S3_FINDINGS §6.3). A capability is gated only where a genuine unresolved dependency prevents responsible implementation, and is never removed from the architecture because of a gate. Professional legal review is **not** adopted as a project rule; the owner may adopt it later as a governance safeguard | S3_FINDINGS §6.3; FX3-26 |
| D3-09 | Registry-driven option sources; descriptive comparison (no score, rank, weights, default cost sort; no wealth-tax dimension) | ADR-0019 §11–12 |
| D3-10 | RQ-46: `INV.residence_change_expected` stays conditional/inactive; activates only if S13a admits a method needing it; exit-tax facts recorded | — |
| D3-11 | Accept registry v1 (83 records) at recorded statuses, with the meaning of acceptance stated above. V-abs facts must be read in full before reliance in a hard constraint | ADR-0019 §13 |
| D3-12 | Fixtures FX3-01 … FX3-16 (required) and FX3-17 … FX3-26 (extras, incl. wealth-tax exclusion, unknown vs. not offered, experience never grants eligibility, gated capability retained) | Fixtures |
| D3-13 | RQ dispositions on acceptance: RQ-03, 04, 05, 06, 24, 42, 46 → RESOLVED (facts as registry v1; structure by ADR-0019). **RQ-45 and RQ-49 remain open** with bounded findings. RQ-51 added | OPEN_QUESTIONS |

### Final statuses

**RQ-49:** OPEN, with bounded findings. It gates:
- application-originated personalised recommendations, before enablement;
- the presentation of personalised target portfolios, trade lists, and model portfolios, by S11/S14;
- user-confirmed, rule-based, and unattended execution in distributed builds, by S13f, together with S13 safeguards (ADR-0017) and S16 monitoring.

**Not gated by RQ-49:** generic analytics, personalised descriptive analytics, and deterministic implementation of user-selected rules for the user's own use.

**US ETFs / PRIIPs:**
- Verified: a PRIIP without a Norwegian KID cannot lawfully be sold to Norwegian retail investors. This is a one-step application of Art. 13(1), PRIIPs-loven § 4, and Finanstilsynet's "also on the customer's own initiative".
- Interpretation: "US-domiciled ETFs are unavailable". Step 3 (no Norwegian KID exists) is per-instrument and supported only by secondary sources; it moves to S6 as `kid_available_no`.

**eToro inactivity fee:** unresolved. Both records are kept and linked. The leads point to stale documentation or a 2026 change, but these are secondary sources.

## Part C — Unresolved items by consequence

Full table: S3_FINDINGS §10.

| Class | Items |
|---|---|
| **A — non-blocking** | U6 US reclaim; U7, U7b, U7c verbatim re-reads and application dates; U8 ESMA/Norwegian appropriateness texts; U12 fund-rule start date; U14 CFD national-measure status |
| **B — capability-gating** | U1 shielding 2026 → 2026 tax calcs → S13a · U2 2027 parameters → S13a · U4a–e ASK credit mechanics → ASK after-tax modelling, tax-reporting aids, comparison illustrations → S13a · U5 / RQ-51 fund-level withholding → after-tax fund inputs → S6/S13a · U9, U9b KID availability and AIF-marketing barrier → legal layer for third-country funds → S5/S6 · U10 eToro gaps → eToro feasibility, costs, execution → S5/S13a/S13f · U11 Nordnet gaps → sizing and execution → S13e/S13f · U13 RQ-49 → capabilities listed above → S11/S14, S13f |
| **C — G3-blocking** | **None.** U4 (ASK credit) was the only candidate; applicability is now verified at the level G3 needs |
| Withdrawn | U3 NOU 2026:9 (wealth tax, ADR-0021) |

## Files changed

**Revision 1 (commit 2542ecd):**
- 00_CHARTER.md, 02_EVIDENCE_AND_STATUS.md, 03_FACTS_REGISTRY_POLICY.md, 08_ROADMAP.md
- research/S1_INPUT_SPECIFICATION.md, research/OPEN_QUESTIONS.md
- new S3 research documents; facts/ (6 YAML files and README)
- ADR-0019, ADR-0020
- register, CHANGELOG, README

**Revision 2 (owner corrections):**

| File | Change |
|---|---|
| decisions/ADR-0021-wealth-tax-excluded.md | New, ACCEPTED |
| decisions/ADR-0019-external-fact-registry.md | Unknown ≠ unsupported; eight domains; acceptance meaning; fixtures to FX3-26 (still PROPOSED) |
| decisions/README.md | ADR-0021 row |
| 00_CHARTER.md | Wealth tax added to out-of-scope |
| 03_FACTS_REGISTRY_POLICY.md | Wealth removed from Tax Registry contents; scope line |
| 08_ROADMAP.md | S3 B: wealth tax removed |
| research/S1_INPUT_SPECIFICATION.md | `TAX.wealth_tax_position` retired; field 1.7 row per D3-07 |
| research/OPEN_QUESTIONS.md | RQ-03 text; RQ-04/05 notes; RQ-45, RQ-49 remain open with stages extended |
| research/S3_FINDINGS.md | Rewritten (ASK credit §2.1; PRIIPs chain §4.1; RQ-45; RQ-49 §6; eToro §8; audit §9; A/B/C §10) |
| research/S3_REGISTRY_ARCHITECTURE.md | Scope line; broker layer `offered · not_offered · unknown`; unknown ≠ unsupported; re-check table; eight domains; acceptance meaning |
| research/S3_SYNTHETIC_FIXTURES.md | FX3-02/05/06/13/18 revised; FX3-23 … 26 added |
| research/S3_G3_PACKAGE.md | This revision |
| research/PROJECT_STATUS_2026-10-01.md | New: S0–S18 status review |
| facts/no_tax.yaml | 4 wealth-tax records removed |
| facts/no_wrappers.yaml | ASK credit decomposed into 7 records; withdrawal rule enriched; FX rule added |
| facts/withholding_us_no.yaml | W8 updated |
| facts/regulation_eea_no.yaml | PRIIPs chain (5 new records); US-ETF record re-based; ESMA paragraphs corrected; unverified EU application dates nulled |
| facts/broker_nordnet.yaml | API reopening as verified absence; wealth reporting removed; capability semantics header |
| facts/broker_etoro.yaml | 3 hidden unknowns split out; inactivity re-check notes; capability semantics header |
| facts/README.md, CHANGELOG.md, README.md | Updated |

No accepted ADR body was changed. Nothing under `local/` is tracked.

## Owner decisions still required before G3 can close

1. Approve D3-01 … D3-13 as revised, or amend them.
2. Confirm the **PRIIPs promotion**: should the conditional rule be `verified` as a one-step application of mandatory provisions, or kept as `interpretation` because no source states "prohibited" in those words?
3. Confirm the **A/B/C classification**, especially U4 (ASK credit mechanics) as B → S13a rather than C.
4. Confirm the **RQ-49 gating assignments** in S3_FINDINGS §6.3 (which capabilities are enablable vs. gated, and the stages).
5. Confirm **Norway as "supported"** with treaty coverage limited to US-source income. Other source countries' withholding stays unknown until recorded.
