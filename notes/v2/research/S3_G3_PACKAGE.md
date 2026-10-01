# S3 — Gate G3 package

**Document status:** DRAFT (for G3 review) · **Branch:** `stage/s03-external-facts` · **Prepared:** 2026-10-01

**Approval semantics (per the S3 instruction):**
- **Part A** contains external facts. Accepting them means accepting them into registry v1 on the stated evidence, as of 2026-10-01. They are not preferences or project decisions; a later change in the world creates a new effective-dated version, not an ADR.
- **Part B** contains proposed architectural decisions. These need approval.
- **Part C** lists gaps. They are not decided.

**Companion documents:**
- [S3_REGISTRY_ARCHITECTURE.md](S3_REGISTRY_ARCHITECTURE.md) (architecture)
- [S3_FINDINGS.md](S3_FINDINGS.md) (evidence)
- [../facts/](../facts/) (records)
- [S3_SYNTHETIC_FIXTURES.md](S3_SYNTHETIC_FIXTURES.md)
- [ADR-0019](../decisions/ADR-0019-external-fact-registry.md) (PROPOSED)

---

## Part A — Research findings (external facts)

| Area | Where | Highlights |
|---|---|---|
| Norway tax and wrappers | S3_FINDINGS §2; no_tax.yaml, no_wrappers.yaml | 22%; factor 1.72; wealth tax NOK 1.9 m, 1.00%/1.10%; 80% valuation; ASK rules incl. withholding-reduces-input-value; exit tax; shielding 2025 = 3.6%; 2026 rate and 2027 parameters `unavailable`; NOU 2026:9 `proposed` |
| Withholding | S3_FINDINGS §3; withholding_us_no.yaml | W1 30% → W2 15% → W3 W-8BEN → W5 Nordnet treaty rate (conditional) → W7 credit capped; W5 eToro, W6, W9 unavailable |
| Regulation | S3_FINDINGS §4; regulation_eea_no.yaml | PRIIPs KID in Norwegian from 2024-10-01; CFD measures from 2018-08-01; MiFID II / vphl definitions; ESMA advice briefing (non-binding) |
| RQ-45 | S3_FINDINGS §5 | Appropriateness is a firm obligation, implemented by the broker |
| RQ-46 | S3_FINDINGS §2 (exit tax) | Exit tax covers shares, funds, ASK; NOK 3 m deduction; 12-year rule |
| RQ-49 | S3_FINDINGS §6 | Authoritative statements A1–A9 kept separate from inference; capability → rule table; no legal conclusion |
| Nordnet | S3_FINDINGS §7; broker_nordnet.yaml | 16 records: 14 verified, 2 unavailable |
| eToro | S3_FINDINGS §8; broker_etoro.yaml | 16 records: 10 verified, 3 unavailable, 1 interpretation, 1 conflict pair; further unknown sub-values (Norway commission amount, API regional eligibility, direct reporting to Skatteetaten) |

Registry v1 contains 72 records. All records pass the contract check: required fields present; vocabularies valid; unavailable ⇒ null; conflict ⇒ linked; proposal ⇒ no `effective_from`.

## Part B — Proposed decisions

**Already decided by owner instruction (recorded, not for re-approval):**

| ID | Decision | Recorded in |
|---|---|---|
| D3-a | G3 approves registries, not any user's account configuration (consistency correction) | 08_ROADMAP; CHANGELOG |
| D3-b | All pension saving and products excluded | ADR-0020 (ACCEPTED) |
| D3-c | YAML provisional; logical record contract, not file-per-fact | S3_REGISTRY_ARCHITECTURE §1 |
| D3-d | Instrument-type level only; no security master | S3_REGISTRY_ARCHITECTURE §6 |

**For approval:**

| ID | Proposed decision | Basis | ADR |
|---|---|---|---|
| D3-01 | Logical fact-record contract; two status axes (`legal_status`, `verification_status`) plus `verification_level`; mapping from vocabulary E; conflicts as linked records, not versions | Architecture §1 | 0019 §1–2 |
| D3-02 | Bitemporal `Fact(t \| k)`: proposals never returned; future-effective facts never leak; "current" derived; runs pin k. Unknowns propagate as unknown → `pending` + finding; never false/0 or a prior period's value | §2–§3 | 0019 §3–4 |
| D3-03 | Admissibility layers legal ∩ wrapper ∩ broker ∩ methodological ∩ user, each with value and binding source; S3 fills only the first three | §4 | 0019 §5 |
| D3-04 | Withholding layers W1–W9; treaty ≠ actually withheld | §5 | 0019 §6 |
| D3-05 | Instrument-type attribute schema (for S6); RegRule ≠ BrokerImplementation (`implements` link) | §6–§7 | 0019 §7–8 |
| D3-06 | Re-check cadences and event triggers; `stale` flag; owner approval when stale facts feed hard constraints, costs, or tax. Jurisdiction support needs nine verified domains; domain-level vs. fact-level coverage; no fallback; Norway supported at domain level with listed fact gaps and US-only treaty coverage | §8–§9 | 0019 §9–10 |
| D3-07 | **Field 1.7 `INV.investment_experience`.** **Option 1 (recommended): retire the field.** No eligibility consumer exists, since access is governed by the broker's assessment (RQ-45), and purpose limitation (ADR-0014 §8) bars collecting a field without a consumer. **Option 2:** keep it in the candidate inventory, inactive, until a consumer (e.g. explanation depth, S15) is researched. `INV.complex_product_tests` (1.8) remains the access-related field | S3_FINDINGS §5 | Spec change (S1 spec row); no ADR body edited |
| D3-08 | **RQ-49 bounded finding.** No regulatory status is concluded. Architectural consequences adopted now: (1) keep the S2 authority model unchanged (ADR-0017); (2) local, self-hosted execution with user-held broker credentials is the reference pattern, and there is no developer-hosted order relay; (3) **professional legal review is a gating condition** before personalised-output, trade-list, order-submission, or unattended-execution capabilities are enabled in publicly distributed builds; (4) neutral presentation (no emphasis or ranking, ESMA ¶62); disclaimers are not relied on (¶64). RQ-49 stays open for that review | S3_FINDINGS §6 | Recorded in 08 (S13 gate condition) at acceptance |
| D3-09 | Registry-driven option sources (§10) and the descriptive comparison specification (§11): no scores, ranks, weights, or default cost sort | §10–§11 | 0019 §11–12 |
| D3-10 | RQ-46: `INV.residence_change_expected` stays conditional/inactive; it activates only if S13a admits a method requiring it; exit-tax facts are available | S3_FINDINGS §2 | — |
| D3-11 | Accept registry v1 contents (Part A) as facts as of 2026-10-01 at their recorded verification statuses; V-abs entries flagged for full reading before any reliance in a hard constraint | Part A | — |
| D3-12 | Fixtures FX3-01 … FX3-16 (required) and FX3-17 … FX3-22 (proposed extras) | Fixtures | — |
| D3-13 | RQ-51 added (fund-level withholding). RQ-03/04/05/06/24/42/45/46 → RESOLVED on acceptance (factual parts as registry v1; structural parts by ADR-0019). RQ-49 remains open (D3-08) | OPEN_QUESTIONS | — |

## Part C — Unresolved facts and gaps

S3_FINDINGS §9, items U1–U13. Most consequential:
- U4: credit inside ASK.
- U5/RQ-51: fund-level withholding.
- U7: verbatim MiFID II Art. 25(3)/(4) and Del. Reg. 2017/565 Art. 9 text, including the exact "third parties" wording of Art. 4(1)(1).
- U9: direct authority on US-ETF retail access.
- U10: several eToro attributes, including the inactivity-fee conflict.
- U13: legal review for RQ-49.

None blocks G3. Each is recorded as unknown and resolves to `pending` where it is consumed.

## Files changed on this branch

| File | Change |
|---|---|
| 00_CHARTER.md | Out-of-scope row: all pension saving (ADR-0008, ADR-0020) |
| 02_EVIDENCE_AND_STATUS.md | Note on the proposed fact-status extension (ADR-0019) |
| 03_FACTS_REGISTRY_POLICY.md | Pension scope line; current contents → registry v1 (provisional); re-check pointer |
| 08_ROADMAP.md | D3-a correction (G3 ≠ account choice) |
| research/S1_INPUT_SPECIFICATION.md | `INV.outside_assets` excludes pension types |
| research/OPEN_QUESTIONS.md | RQ-03/04/05/06/24/42/45/46/49 → AT-GATE; RQ-49 reframed; RQ-51 added |
| research/S3_REGISTRY_ARCHITECTURE.md | New |
| research/S3_FINDINGS.md | New |
| research/S3_SYNTHETIC_FIXTURES.md | New |
| research/S3_G3_PACKAGE.md | New (this file) |
| facts/README.md + 6 YAML files | Registry v1 (provisional) |
| decisions/ADR-0019 | New, PROPOSED |
| decisions/ADR-0020 | New, ACCEPTED (owner instruction) |
| decisions/README.md, CHANGELOG.md, README.md | Register, change history, index |

No accepted ADR body was changed. Nothing under `local/` is tracked.
