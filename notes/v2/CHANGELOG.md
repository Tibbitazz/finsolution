# Changelog — notes/v2

## 2026-10-01 — S1 started (branch `stage/s01-investor-context`)

- ADR-0014 (PROPOSED, for G1): reusable engine with a private local user layer; declared vs. effective Policy Statement with conflict records; field metadata; raw preferences preserved with derivation records; privacy boundary; unsupported-jurisdiction rule.
- D-S1-1 resolved by the owner: personal data stays local and git-ignored. `.gitignore` excludes `/local/`.
- research/S1_QUESTIONNAIRE.md (renamed from S1_INVESTOR_INPUTS.md): public template with nature (F/P/R), interface type, need, and later use per question.
- Amended: 00 scope and roles; 07 §8 (proposed); 08 S1, S2, S8; RQ-01 updated; RQ-39 … RQ-42 added.

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
