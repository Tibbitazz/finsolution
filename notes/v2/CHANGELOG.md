# Changelog — notes/v2

## 2026-10-07 — Combined working handoff (owner-approved; branch `stage/s04-method-library`)

- **New** `HANDOFF.md` (DRAFT, living): the single entry point. Contents: mandate, assistant rules (protocol; standing rules incl. newest-version, code-reuse and learning priority; security; tooling), repository state, architecture summary, stage status and recommended order, consolidated open owner decisions, sources at a glance, key quantitative results, local paths.
- It indexes the authoritative documents and never overrides them. It supersedes the two local handoff files in ENGINE_V1.
- README reading order updated.

## 2026-10-07 — Third-party implementation review (owner request; branch `stage/s04-method-library`)

- **New** `research/s4/S4_GITHUB_IMPL_REVIEW.md` (DRAFT). The chirindaopensource repository is not the authors' code: it implements arXiv v1 (Apr 2026), is MIT-licensed and was never executed.
- **Fidelity:** roster matches neither paper version; ≈ 8 distinct portfolios of 20; late-cycle vote weight contradicts the paper; CIO uses the top 5 only; no learning loop.
- **Verified defects:** HRP not permutation-invariant; clip-and-renormalise breaks the cap; "LW" is not Ledoit–Wolf; returns forward-filled; mixed-unit CMA candidates; inconsistent AdvDiv Sharpe floor; BL without views; review assignment self-assigns a single-member family; LLM-passed weights (R1); IPS soft targets treated as hard; broken tool bindings.
- **Kept:** per-component verdicts; IPS-constraint mathematics (the reverse-convex volatility floor; path-dependent drawdown); ERC explained (PC-C2); invariants I-1 … I-9; port-and-verify candidates (exact projection, CVaR LP, assignment, SCP, Borda/composite, ensembles, drift metrics, provenance).
- **Pointers:** RQ-15 and ANG-08 annotated; S4_PLAN amendment 16 and S4.23 row.
- No method adopted; nothing pushed.

## 2026-10-07 — Lecture and sandbox inputs; agentic learning first; correlated agent errors (owner approval of plan A; branch `stage/s04-method-library`)

- **New memo** `research/s4/S4_INPUTS_2026-10-07.md` (DRAFT):
  - authority and versions (paper v2 governs; lecture secondary; sandbox none);
  - lecture→FinSol conformance map, with a correction to the earlier review;
  - the analysis.md review and candidate skeleton v0;
  - learning as a first-class component (reference design, learning objects, capture from day one, signals and their power, promotion protocol, RQ-22 split);
  - correlated-agent-error research and mitigations M1–M8;
  - generalisable sandbox lessons with derivations D1–D10;
  - what is not transferred;
  - developer requirements DR-1 … DR-8 (interface only).
- **OPEN_QUESTIONS:**
  - RQ-55 (agent output stability and verifiability) and RQ-56 (correlated agent errors) added;
  - RQ-07/08/09/12/16/18/22/26/34/35/44/52/53 annotated;
  - CB-17 … CB-19 proposed for the next gate, with evidence from Nordnet's price list retrieved 2026-10-07.
- **ANG_ISSUES_REGISTER:** type LP; ANG-24 … ANG-27 added; ANG-01/06/09/12/16 annotated.
- **S4_PLAN:** amendment 15; S4.1/S4.3/S4.16/S4.17/S4.20 rows; §I developer list; G4 criterion 24 (learning readiness).
- **S4_ACCOUNTABILITY:** candidate fields F20 (verifiability) and F21 (learning signals).
- **S4_DOWNSTREAM_INVENTORY:** T5/T7/T9 notes; §4 fair-value-gap research lead; §5 candidate simulation conventions.
- **S4_0_SOURCE_INVENTORY:** §11 new sources.
- **README:** current position.
- No accepted document changed; no methodology adopted; nothing pushed.

## 2026-10-07 — ABD 2014 recorded; TPA task restated (owner approval of the five ABD edits and decision D-5; branch `stage/s04-method-library`)

- **Source:** Ang, Brandt & Denison (2014) recorded as AVAILABLE. The owner-supplied file was verified (163 pp., md5 da26aa3090d0; title, date and authors match ANG's reference list). The S4.0 inventory and acquisition checklist are updated: totals 33 confirmed / 38 located / 8 missing; download items 41.
- **Owner decision D-5:** AQR (2026) may substitute for ABD as the specification source for how TPA becomes weights, where more informative. ABD remains ANG's cited source for the concept.
- **`VERIFIED-DERIVATION`:** unconstrained AQR/Treynor–Black sizing equals the tangency portfolio under a factor-structured Σ (numerical check 1.6 × 10⁻¹⁴; SR² additivity). Hence a distinctness test is required for PC-D4.
- **ANG_ISSUES_REGISTER:** ANG-22 updated (ABD's TPA is a funding/benchmarking framework without a weight rule). New section with ABD-1 … ABD-5 (verified against the PDF).
- **S4_PLAN:** amendment 14; §D PC-D4 row; S4.12 restated (own TPA-family specification plus distinctness test; else MERGE/RELOCATE).
- **ADR-0026 (PROPOSED; pre-acceptance amendment):** ABD [SRC] citations added in §4.1 (independent, pre-set controls), §5.1 (rebalancing rule owned upstream) and §5.3 (implementation leeway; transfer to a small investor not established). No decision content changed.
- **OPEN_QUESTIONS:** RQ-52 candidate field "verification horizon". RQ-54 candidates: a not-rebalanced ladder rung, cost-of-constraints reporting, a replicable control in preference to an absolute target.
- No methodology adopted; nothing pushed.

## 2026-10-02 — S4 closure preparation: accountability layer and source closure (owner approval of T-0 … T-8; branch `stage/s04-method-library`)

- **ADR-0026 PROPOSED:** Agent Mandate and Decision Record objects (extends ADR-0023 §5); investment decision ≠ rebalancing determination ≠ implementation discretion ≠ execution; escalation; evidence rights; no container categories. Every statement is labelled [SRC] / [AD] / [GR] / [DEF]; embedded mathematical claims M-1 … M-4 are listed with their conditions. Annotates the reading of ADR-0012 §7, 05 §2 layer 8 and 08 S13d (no body edits). Final acceptance after the owner's mathematical/authority check.
- research/s4/S4_ACCOUNTABILITY.md (S4.2b draft): mandate schema; role taxonomy incl. extensions and services; mandate stubs; responsibility matrix v0; escalation; no-trade concepts (provisional); traceability chain and P0–P5 ladder (definitions only).
- research/s4/S4_DOWNSTREAM_INVENTORY.md (S4.15b draft, inventory only): families T1–T12. The ML trading specification is rejected as a system (owner D-D), with retained components relocated. The z-score rule is a research lead within T3, with family removal criteria declared in advance.
- S4.0 corrections:
  - the ABD 2014 URL was wrong (it served BCD 2022) in the inventory and checklist; corrected candidates listed, none fetched;
  - BCD 2022 and the owner-supplied papers registered with verified identities (§10; checklist Addendum A);
  - two supplied files misidentified (Jones & Wermers 2011; NBIM news page 2014);
  - AQR (2026) TPA paper read in full: it cannot replace ABD 2014 as ANG's cited source, but can serve as a conditional specification lead for a separately labelled TPA-family candidate (Addendum A.3).
- S4_PLAN.md:
  - amendments 11–13;
  - §E.1 source authority and §E.2 selectivity exit states;
  - B-15 updated; B-22/B-23 added; C-9/C-10 added;
  - role ladder with MANDATE STUB DEFINED;
  - S4.2b and S4.15b steps;
  - field additions in S4.3, S4.12, S4.16–S4.18, S4.20, S4.22;
  - SYNC-1/5 additions;
  - G4 criteria 19–23.
- OPEN_QUESTIONS: RQ-52, RQ-53, RQ-54 added; RQ-17 annotated (cross-layer evidence reuse must be traceable); RQ-35 reworded family-first.
- ANG_ISSUES_REGISTER: ANG-22 updated (TPA under-specified; ABD not obtained); ANG-23 added (technical signals under-specified).
- No methodology review, equation extraction or method ranking has begun. Nothing pushed.

## 2026-10-02 — S4 plan approved in principle; S4.0 completed (branch `stage/s04-method-library`)

- research/s4/S4_PLAN.md: S4 plan (ANG baseline) with owner decisions OD-1 … OD-7 and corrections 1–10.
- ADR-0023 ACCEPTED (ANG architectural baseline; role ≠ runtime; R2 preserved; Method ≠ Agent; extensible roster; adopted vs. illustrative; no ANG priors).
- ADR-0024 ACCEPTED (research lane; revision rules; parameter-authority classes; allocation domains; dual contracts; EPO hierarchy; verification area).
- ADR-0025 PROPOSED: OD-4 conflicts with accepted 06 §1(3) / 02 §D definitions of ADMISSIBLE; proposes separate admission and evaluation axes.
- S4.0 outputs: research/s4/S4_0_SOURCE_INVENTORY.md; research/s4/ANG_ISSUES_REGISTER.md (ANG-01 … ANG-22); research/s4/verification/README.md.
- 10_SCOPE_EXCLUSIONS: X-20 (UEPO/SEPO/DEPO), X-21 (ANG rankings/weights as priors), X-22 (LLM weight edits / opportunistic tuning).
- RQ-16 note; 08 S4 entry updated. No mathematical review or method ranking has begun.

## 2026-10-01 — Gate G3 closed

- Owner approved G3 with final amendments: ADR-0019 ACCEPTED; ADR-0020 and ADR-0021 retained; ADR-0022 ACCEPTED (parallel development track after G3; S18 = final handoff/completion).
- Registry v1 accepted: 82 records. The US-ETF interpretation record was removed; the PRIIPs conditional rule was reformulated narrowly; per-instrument attributes deferred to S6.
- Domain-specific jurisdiction support and operation-level support checks (ADR-0019 §10; architecture §9).
- RQ-49 capability gating approved in principle; deterministic user-selected rules not automatically recommendations.
- RQ-03/04/05/06/24/42 resolved; RQ-46 resolved for S3; RQ-45, RQ-49, RQ-51 open.
- Carried gating register CB-01 … CB-16 with gate entry rule (08 §3); carried invariants (unknown ≠ not_offered; domain-specific support; derived eligibility).
- 10_SCOPE_EXCLUSIONS.md established (E / I / D kinds).
- 08_ROADMAP: Track A / Track B diagram; S8 and S18 redefined.
- Fixtures FX3-27, FX3-28 added. S3 documents STABLE.

## 2026-10-01 — S3 G3 package revision 2 (owner corrections at G3 review; G3 not closed)

- **Wealth tax out of scope (ADR-0021, ACCEPTED, owner instruction):** 4 provisional wealth-tax records removed (never accepted, so no registry history affected); `TAX.wealth_tax_position` (S1 10.1) retired; jurisdiction-support domain removed (nine → eight); 00, 03, 08, RQ-03 amended. Total-wealth optimisation scope and outside wealth in risk capacity are unaffected.
- **ASK withholding credit corrected:** Skatte-ABC 2025/2026 A-10-5.4.1 states the credit rules may apply on a taxable withdrawal. The draft's "credit availability unknown" was wrong. Decomposed into seven records (applicability, timing, calculation, tracking, input-value interaction, carry-forward, broker information); unestablished mechanics remain unknown. ASK withdrawal and FX rules added from Skatte-ABC.
- **D3-07 revised:** field 1.7 not retired; inactive, not collected by default; never grants eligibility; never substitutes a broker test.
- **D3-08 revised:** no universal legal-review prerequisite; capability register (capability → evidence → unresolved issue → dependency/safeguard → enablement status); RQ-49 remains open beyond G3; A vs. B analysis recorded.
- **PRIIPs chain:** conditional rule (PRIIP without Norwegian KID → no retail sale) verified; "US ETFs unavailable" kept as interpretation; 5 regulation records added.
- **ESMA citations re-verified** against the PDF; disclaimer point corrected to ¶64–65; ¶16, ¶25, ¶38, ¶40–41, ¶81 added.
- **Unverified EU application dates** (MiFID II, PRIIPs) set to null (U7c).
- **eToro inactivity fee:** second attempt; unresolved; both records kept.
- **Unknown ≠ unsupported:** broker layer `offered · not_offered · unknown`; 3 hidden unknowns split into own records; Nordnet API reopening expressed as verified absence.
- Unresolved items classified A/B/C (no class C). Meaning of registry acceptance stated in ADR-0019, architecture, facts README, and package.
- Fixtures FX3-23 … FX3-26 added; FX3-02/05/06/13/18 revised.
- research/PROJECT_STATUS_2026-10-01.md: S0–S18 status review.

## 2026-10-01 — S3 package prepared for G3 (branch `stage/s03-external-facts`)

- **Consistency correction (D3-a):** 08_ROADMAP previously described G3 as approving the user's account choice. G3 approves the external-fact registries only; no user's account configuration is a gate decision.
- **D3-b:** ADR-0020 ACCEPTED (owner instruction). All pension saving and products are out of scope. 00, 03, and the S1 spec (`INV.outside_assets`) updated.
- **D3-c, D3-d** recorded: logical record contract (YAML provisional); instrument-type level only.
- research/S3_REGISTRY_ARCHITECTURE.md: record contract, point-in-time semantics, uncertainty, admissibility layers, W1–W9, instrument-type schema, RegRule/BrokerImplementation, re-check policy, jurisdiction process, option sources, comparison specification.
- research/S3_FINDINGS.md and facts/*.yaml: registry v1 (72 records, verified 2026-10-01) for Norway tax and wrappers, US→NO withholding, EEA/NO regulation, Nordnet, eToro.
- research/S3_SYNTHETIC_FIXTURES.md: FX3-01 … FX3-22.
- research/S3_G3_PACKAGE.md: findings (A), proposed decisions D3-01 … D3-13 (B), gaps (C).
- ADR-0019 PROPOSED. 02 and 03 annotated (not rewritten). RQ-03/04/05/06/24/42/45/46/49 at gate; RQ-49 reframed; RQ-51 added.

## 2026-10-01 — Gate G2 closed

- Owner approved G2 with amendments; ADR-0015 … ADR-0018 ACCEPTED; S2 documents STABLE.
- D2-01: units/basis/period preserved through derivations.
- D2-04: structured finding-record architecture (ConflictRecord, TradeOffRecord, GoalRoutingRecord, FeasibilityFinding); T1 not resolved in S2; unattainable goals stay visible without modifying the goal.
- D2-06: `supports_ordered_alternatives` metadata with semantic requirements; no closed whitelist; per-field enablement by later stages.
- D2-07: eight grants are the S2 logical representation, refinable by S8/S13; invariant analytical ≠ decision ≠ execution authority.
- D2-09: model parameters scoped to formulation/units/calibration context; never portable investor attributes.
- D2-10: disagreements preserved and exposed; capacity-based hard constraints deferred to S11 (not restricted to informational).
- Fixtures: FX2-03 amended; FX2-17 … FX2-20 added.
- RQ-02 (02b/c), RQ-23, RQ-41 (governance), RQ-47 (policy), RQ-48 (mechanism) resolved. RQ-49 clarified as research only. RQ-02d/RQ-50 note the calibration-vs-selection distinction.
- Research memo accepted with its verification limitations preserved (Pedroni et al., Levy & Markowitz caveats retained).

## 2026-10-01 — S2 package prepared for G2 (branch `stage/s02-configuration-machinery`)

- research/S2_CONFIGURATION_MACHINERY.md: O1 logical schema (immutable versions; typed values with unit/basis/period), O2 methodology-neutral constraint representation, O3 resolution algorithm with invariants, O4 interaction taxonomy and ordered alternatives, O5 dependency graph with incremental recomputation, O6 authority model, O7 calibration interface, O10 schema evolution, option-set governance.
- research/S2_RISK_PREFERENCE_RESEARCH.md: risk ontology; theory of risk-aversion parameters; elicitation evidence and practice; claims tagged TH/EM/IP/AI with source-verification levels.
- research/S2_SYNTHETIC_FIXTURES.md: FX2-01 … FX2-16.
- research/S2_G2_DECISIONS.md: proposed decisions D2-01 … D2-14, separated from findings.
- ADR-0015 … ADR-0018 PROPOSED. RQ-02 (02b/c), RQ-23, RQ-41, RQ-47, RQ-48 at gate; RQ-49 (regulatory status of distribution) and RQ-50 (elicitation validation) added.

## 2026-10-01 — Gate G1 closed

- Owner approved G1: ADR-0014 ACCEPTED; S1_INPUT_SPECIFICATION and S1_SYNTHETIC_FIXTURES STABLE; interaction model, resolution, propagation, fixtures, S1/S2 separation, RQ-43 … RQ-47.
- G1 clarification made explicit: the precedence facts/feasibility → methodology → preferences decides implementability only. Declared values are never rewritten or substituted (ADR-0014 §5, spec §7.1, 07 §8). RQ-48 added (declared ordered alternatives, S2).
- FX-18 added: valid declared preference preserved while methodologically inadmissible (no existing fixture tested this exactly; FX-17 has no user selection, FX-05 is data/universe ineligibility). FX-03 states declared retention explicitly.
- RQ-01 RESOLVED. PROPOSED markers removed from 00, 06, 07.

## 2026-10-01 — S1 refocused on the reusable input specification

- S1 deliverable changed from collecting a personal profile to the reusable Investor Profile & Policy Statement input specification: research/S1_INPUT_SPECIFICATION.md (data classes A–E, field-specification schema, capability vs. activation, value origins, field inventory incl. new rebalancing configuration group, interaction model, Declared → Effective resolution, change propagation, extensibility) and research/S1_SYNTHETIC_FIXTURES.md (17 edge-case fixtures with stub facts and methods).
- ADR-0014 amended (still PROPOSED for G1): data classes, Portfolio State separation, runtime-configuration status of user inputs, capability vs. activation, value origins, parameter authority, portability.
- 06 §5: method contracts gain `required_profile_fields` and parameter authority (proposed, ADR-0014).
- Roadmap: S1/S2 split by layer; S13b note on rebalancing configuration and the drift vs. signal distinction.
- RQ-01 at gate; RQ-18 note; RQ-43 … RQ-47 added.
- S1_QUESTIONNAIRE marked SUPERSEDED (kept as candidate-inventory history).
- No personal data is committed. The owner's Section 1 answers remain local development data only.

## 2026-10-01 — S1 started (branch `stage/s01-investor-context`)

- ADR-0014 (PROPOSED, for G1): reusable engine with a private local user layer; declared vs. effective Policy Statement with conflict records; field metadata; raw preferences preserved with derivation records; privacy boundary; unsupported-jurisdiction rule.
- D-S1-1 resolved by the owner: personal data stays local and git-ignored. `.gitignore` excludes `/local/`.
- research/S1_QUESTIONNAIRE.md (renamed from S1_INVESTOR_INPUTS.md): public template with nature (F/P/R), interface type, need, and later use per question.
- Amended: 00 scope and roles; 07 §8 (proposed); 08 S1, S2, S8; RQ-01 updated; RQ-39 … RQ-42 added.
- Purpose limitation added to ADR-0014 (§8): every personal field declares its decision purpose, exhaustive permitted consumers, and necessity; fields without a purpose are not collected; no silent cross-purpose use. Reflected in RQ-40, RQ-41, 07 §8, and the questionnaire (Necessity and Purpose → permitted consumers columns). Question 1.4 reworded to consumption and liability currencies.

## 2026-10-01 — Gate G0 closed

- Owner accepted ADR-0002, ADR-0003, ADR-0012, ADR-0013 (status lines updated;
  bodies unchanged). All S0 ADRs 0001–0013 now ACCEPTED.
- PROPOSED markers removed from 05 §4, 06 §5, 07 §4, 08 (sections now binding).
- Added research/REF-01_self-driving-portfolio.md: knowledge base of the
  source-of-record version (21 Sep 2026), verified exhibit arithmetic, an
  April-vs-September version-difference table, and version-independent
  arguments from the legacy April-draft review, re-tagged and assigned to RQs.
  The legacy review itself was not moved (it describes the April 1 draft and
  assesses it against superseded ENGINE_V1); it remains untouched locally.

## 2026-10-01 — S0 amendment: signal & scoring research pre-registration (branch `stage/s0-governance`)

Basis: owner-supplied Asness, Moskowitz & Pedersen (2013); Sørensen,
*Constructing value and momentum scores* (2026); Sørensen/Storebrand,
*Factor Investing* (2025); a 5-day z-score mean-reversion description.
No scoring model implemented; no methodological question resolved.

Added:
- ADR-0012 (PROPOSED): descriptor taxonomy, deterministic scoring component, score ≠ belief, rule R8, typed eligibility contracts, S9 restructure.
- ADR-0013 (PROPOSED): clarification of ADR-0009's enforcement test (declared comparison universe).
- RQ-27 … RQ-38; RQ-13 marked refined.

Amended (additions only, marked PROPOSED):
- 05 §4 (scoring placement, R8).
- 06 §5 (typed contracts and signal/tactical fields).
- 07 §4 (known-gap note).
- 08 (S7, S8, S9 restructure, S11, S12, S13d, gates G9–G12).
- Decision register.
- v2 README current position.

No accepted ADR body changed.

## 2026-10-01 — S0: Charter & decision governance (branch `stage/s0-governance`)

Created:
- Index, charter, source-of-truth & Git workflow, evidence & status taxonomy,
  facts-registry policy, reproducibility standard, deterministic-vs-agent
  principles, model-eligibility governance, Policy Statement governance,
  roadmap v2, legacy-superseded record.
- Decision register; ADR template; ADR-0001 … ADR-0011
  (9 ACCEPTED on explicit owner instruction/approval; ADR-0002 and ADR-0003 PROPOSED).
- Open research questions RQ-01 … RQ-26, including RQ-02 (risk preference).
- Empty facts directory.

Changed outside `notes/v2/`:
- Repository-root `README.md`: pointer to v2 and legacy notice.
  Legacy specification files left untouched.

Pending (owner action):
- Gate G0 review: accept/reject ADR-0002, ADR-0003; approve merge to `main`; tag `gate-G0`.
- Decide whether the stage-1 reference-paper knowledge base
  (`ENGINE_V1/notes/agentic-saa/self-driving-portfolio-review.md`, local)
  is added under `research/` after review.
