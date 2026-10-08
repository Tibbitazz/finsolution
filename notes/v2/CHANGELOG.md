# Changelog — notes/v2

## 2026-10-08 — S4.4 updated after the owner's uploads and permitted downloads (branch `stage/s04-method-library`)

- **Kirby & Ostdiek** (owner upload; working version of 9 May 2010): ANG-13 resolved. Inverse volatility = VT(½), inverse variance = VT(1) in KO's volatility-timing family; KO test η ∈ {1, 2, 4} only, so ANG's 1/σ is in the family but outside KO's evidence.
- **Michaud 1989** (owner upload; published text copy) read in full: diagnoses error maximisation and non-uniqueness; **does not specify the resampled efficient frontier**. PC-B4's procedure source becomes Michaud & Michaud 2008 (*JOIM* 6(1)). `S4_RISK_MODEL_CHOICE.md` updated (Michaud now `VERIFIED-SOURCE`; p. 38 attributes error maximisation mainly to return errors). RQ-33 lead: the IC adjustment.
- **Maillard, Roncalli & Teïletche** working version (May 2009) downloaded from the author's site with owner permission. The six other permitted items are SSRN-only. SSRN refused scripted access and showed a security check that was not bypassed, so they are listed for manual download.
- **PC-C5:** the authors' release channels were found (release post, Scribd upload, spreadsheet, co-author R code with two variants). New issue ANG-38 (variant unspecified). Options for closing the identity gap are recorded.
- **Updated:** `S4_PC_SOURCE_MAP.md` (§1, §2, new §6), `ANG_ISSUES_REGISTER.md`, `S4_0_SOURCE_INVENTORY.md` §13, `OPEN_QUESTIONS.md` RQ-33, HANDOFF. Not pushed.

## 2026-10-08 — S4.4 PC source map drafted (branch `stage/s04-method-library`)

- **New** `research/s4/S4_PC_SOURCE_MAP.md` (DRAFT for owner review): governing primary, supporting sources and access route for every roster method.
  - 21 of 22 methods SOURCE LOCATED (10 with the governing primary in hand; 4 open working versions; 7 paywalled or book); PC-C5 minimum correlation is a documented gap (identity: third-party mirror only).
  - ANG-vs-source differences known before reading (ANG-02, -07, -10, -13, -14, -15, -16, -17, -18, -22, ABD-5); ANG-35 disposition recorded.
  - Acquisition plan ordered by step; nothing downloaded (D-4). A local BI course note on Treynor–Black-type sizing found and recorded as SECONDARY for PC-D4.
- **Updated:** S4_PLAN C.2; ANG issues register (ANG-35); HANDOFF. Not pushed.

## 2026-10-08 — S4.3 reviewed: owner confirms O-1 … O-4 (branch `stage/s04-method-library`)

- `S4_TAXONOMY.md` status REVIEWED: six kinds (Input added); Researcher typed as a role with roster numbering unchanged; new method-type ID prefixes assigned at their owning stages; specification objects stay in the repository without a separate registry.
- S4_PLAN C.2 and HANDOFF updated. Pushed together with the S4.3 draft commit.

## 2026-10-08 — S4.3 taxonomy drafted (branch `stage/s04-method-library`)

- **New** `research/s4/S4_TAXONOMY.md` (DRAFT for owner review; SYNC-2):
  - six kinds: Method, Artefact, Role, Control, Record, Input (Input added to the five-kind outline; owner confirmation O-1);
  - 18 method types (plugin categories; refining 06 §5 `method_type`), 17 artefact types, role types with mandate/skill/memory/instance specifications, 11 control types, 10 record types, 6 input types;
  - relations for the S4.22 dependency graph; method vs configuration vs parameter vs variant; identity and versioning rules; status ladders by kind;
  - inventory pass: every item has exactly one type. Findings F-1 … F-10, e.g. PC-E1 Researcher is a role (roster unchanged), "anchor" is a relation, decision states are Decision Record fields, two learning objects are role specifications.
- **Updated:** S4_PLAN C.2 (S4.3 DRAFTED); HANDOFF. Not pushed.

## 2026-10-08 — ADR-0027 D3 r3 (Option A); r2 and P-V1/P-V2 withdrawn; risk-model choice record (branch `stage/s04-method-library`)

- **Correction of the previous commit.** The owner had asked for an opinion on per-method risk estimation, not a change. D3 r2 (method-specific construction models plus a reference model) is withdrawn and recorded as such in ADR-0027's revision history.
- **ADR-0027 D3 r3 = Option A (owner decision, 2026-10-08; ADR still PROPOSED as a whole):**
  - one authoritative risk model per problem (universe × horizon × risk object) per run, used by every PC method on that problem, the CRO, limit checks, candidate cards, Portfolio Map and learning records;
  - estimator chosen by the risk role per problem on a pre-registered out-of-sample risk-accuracy test (S7 → S10), never per PC method and never on portfolio returns;
  - method-internal regularisation (EPO, Black–Litterman, resampling, robust sets) stays inside the methods;
  - PC agents never choose or test estimators; the CRO reports sensitivity to alternative estimators.
- **New** `research/s4/S4_RISK_MODEL_CHOICE.md` (owner question: how much the risk model matters; whether one is better; which; when):
  - literature (Michaud 1989; DeMiguel, Garlappi & Uppal 2009; Chopra & Ziemba 1993; Jagannathan & Ma 2003; Chan, Karceski & Lakonishok 1999; Ledoit & Wolf 2004, 2017; Ardia et al. 2017; PBL 2021; Patton 2011; Hansen, Lunde & Nason 2011), each with its verification status;
  - M-1 (synthetic): return-forecast errors dominate mean–variance losses; estimator choice matters greatly unconstrained (1,655 vs 674 bp/yr) and little long-only (≤ 2 bp/yr);
  - M-2: EPO-style regularisation inside the method beats swapping risk models unconstrained, and over-corrects under long-only caps;
  - candidates per problem; selection rule; stage map (original plan; no change).
- **Withdrawn:** P-V1, P-V2 and S4_PLAN §G.1 (the original plan already covers them).
- **Reconciled:** `S4_ANG_ADAPTATION.md` B-7, B-33, B-34, C-12, §4, §5; S4_PLAN C-12 and the S4.3, S4.13, S4.16 rows; decision register; RQ-14; `S4_ANG_BASELINE.md` §13.3; `S4_SCORING_PEER_METHODS.md` §9.6; HANDOFF.

## 2026-10-08 — S4.2 owner-review round: method-specific risk models, RMT by universe size, score table, verification timing (branch `stage/s04-method-library`)

- **ADR-0027 D3 revised (r2; still PROPOSED)** after the owner's question "should the risk estimation depend on the PC method?":
  - construction risk models are **method-specific** (declared per PC method in its contract; produced by the risk role as versioned artefacts);
  - **one common reference risk model per declared horizon per run** serves evaluation: CRO diagnostics, IPS/limit checks (binding), candidate cards, Portfolio Map (PM-1) and learning records. It is a reference-estimator control (ADR-0026 §4.1);
  - dual reporting on candidate cards (risk-model disagreement; sensitivity line);
  - AC-level risk outputs remain evidence; PSD projection kept;
  - title, alternatives, evidence, consequences and revisit triggers updated; revision history added.
- **RMT cleaning by universe size** (`S4_ANG_BASELINE.md` §13.3, Appendix C; synthetic, reproducible, seed 20261008):
  - harmful for 17 asset classes (genuine sub-edge eigenvalues destroyed);
  - best for 100–300 stocks;
  - neutral under long-only 10% caps.
  - Eligibility needs N, q_eff, constraint set and a spectrum diagnostic. No threshold set (S10, RQ-14).
- **Score table spec** (`S4_SCORING_PEER_METHODS.md` §9): separate columns for Sørensen value and momentum and the Greenblatt-type EY and ROC legs; AGG-EYROC only as a labelled aggregation variant; cell contract; null-reason codes NR-1 … NR-6; rules T-1 … T-8; one artefact for dashboard and agents.
- **Verification timing** (S4_PLAN §G.1): mathematical verification per method in S4.5–S4.24 on synthetic data; empirical selection of signals, moments and estimators in S7 → S9/S10/S11. Refinements P-V1 and P-V2 proposed, not applied.
- **Reconciled:** `S4_ANG_ADAPTATION.md` B-7, B-33, B-34, C-12, §4, §5; S4_PLAN C-12 and the S4.3, S4.13 and S4.16 rows; decision register; RQ-14, RQ-32; Sørensen record pointer; HANDOFF. Not pushed.

## 2026-10-08 — S4.2 adaptation map drafted; ADR-0027 proposed (branch `stage/s04-method-library`)

- **New** `research/s4/S4_ANG_ADAPTATION.md` (DRAFT for owner review):
  - every element of the S4.1 baseline classified U/G/A/D/N with reason, binding source and owning stage;
  - B-1 … B-23 retained from S4_PLAN §B; **B-24 … B-45 new**: autonomy via ADR-0017; anatomy and skills; non-equity CMAs; CMA units; one risk model; horizon field; heterogeneous PC inputs; candidate cards; dissent; runtime backtest diagnostics; registry evolution; extended learning objects; per-role promotion; data; determinism; security.
- **Conflicts:** C-7, C-8 resolved (superseded proposals). Proposed resolutions for C-5, C-6 and new C-11 … C-13 via ADR-0027. C-14 resolved by planning.
- **Issues:** ANG-01 … ANG-37 dispositioned. Developer-facing summary for SYNC-1.
- **New ADR-0027 (PROPOSED):**
  - D1: learning adopted as a core component under L-1 … L-7;
  - D2: no automatic culling; retirement by ADR; family-coverage floor;
  - D3: one authoritative risk model per declared horizon; AC-level risk outputs are evidence; PSD projection;
  - D4: runtime backtest diagnostics deterministic, protocol-defined, labelled in-sample, never admission evidence;
  - D5: declared currency, hedging, horizon and return convention; numéraire per RQ-07.
- **Updated:** decision register; S4_PLAN (§B superseded; C.2 status; C-5 … C-14); HANDOFF; CHANGELOG. Not pushed.

## 2026-10-08 — S4.1 settled: owner questions on scoring choice, learning, covariance, FMP/Finviz, external references (branch `stage/s04-method-library`)

- **Sørensen vs Greenblatt** (`S4_SCORING_PEER_METHODS.md` §8):
  - an empirical belief question, not a preference;
  - literature priors: Novy-Marx 2013; Gray & Carlisle; Nordic theses;
  - decision protocol D-1 … D-7 (spanning regressions, HAC IR difference, multiple testing);
  - power table: e.g. 60 years for ΔSR = 0.2 at ρ = 0.7;
  - recommendation: decompose and combine if indistinguishable.
- **Learning** (`S4_ANG_BASELINE.md` §13.1):
  - verified as an ANG pillar;
  - two loops (forecast learning; registry evolution);
  - PC-method evaluation intended but unspecified;
  - tension with correlated errors recorded as **ANG-37 (H)**, quantified by N_eff = N/(1+(N−1)ρ);
  - design rules L-1 … L-7.
- **Volatility and covariance** (§13.2):
  - three ANG risk inputs (ANG-33 extended);
  - estimator inventory extended (CCC-GARCH, EWMA, Higham nearest-correlation, constant correlation; candidates);
  - synthetic simulation (Appendix B, reproducible): the scaled-identity Ledoit–Wolf target is harmful for heterogeneous-volatility classes; long-only constraints regularise; estimator choice is method-dependent;
  - GARCH horizon derivation (3-year deviation share ≈ 0.07).
- **FMP and Finviz** (S6 lead §4.5b): FMP PARTIAL (per-user key; global only at Ultimate; Oslo unconfirmed; not PIT); Finviz DOES NOT FIT (US-only screener).
- **External references** (`S4_EXTERNAL_REVIEWS_2026-10-08.md`):
  - MongoDB agentic-portfolio demo: DOES NOT FIT (no optimiser, risk model or evaluation; LLM recommendations; S8 infrastructure patterns only);
  - Medium article: about a personal website, DOES NOT FIT.
- **Annotated:** RQ-08, RQ-14, RQ-22, RQ-37, RQ-56; S4.0 §6 inventory; ANG register (ANG-37; ANG-33); HANDOFF.

## 2026-10-08 — S4.1 ANG v2 baseline drafted (owner instruction; branch `stage/s04-method-library`)

- **New** `research/s4/S4_ANG_BASELINE.md` (DRAFT for owner review; canonical map, superseding S4_PLAN §A, which is kept as history). It is based on:
  - a full read of all 40 pages;
  - Exhibits 1, 2, 4 and 5 read from rendered images;
  - a lecture cross-check.
- **Contents:** scope; pipeline and stage table (inputs, code vs LLM, outputs, citations, unspecified items); order and information barriers; roster reconciliation (44, itemisation marked as inference); agent anatomy and skill inventory; CMA-judge rules; data and provenance; determinism and model governance; IPS governance and memo contents; stated limitations; illustrative-run facts.
- **Verified exhibit arithmetic:**
  - V-1: Borda total 273;
  - V-3: 40/60 min–max composite reproduced to ≤ 0.0011;
  - V-4: weight sums;
  - V-6: effective N = inverse HHI = 11.2 (resolves the ANG-11 definition);
  - V-7: judge within [min, max].
- **New issues** ANG-28 … ANG-36:
  - non-equity CMA methods;
  - "12 other asset classes";
  - Exhibit 1 vs text;
  - meta-agent PC metrics missing;
  - dissent reports;
  - **two volatility sources (H)**;
  - data provenance and PIT;
  - category counts;
  - review assignment.
- **Correction:** ANG Exh. A.1 names the data skill `apex-data-financial (fmp, finviz)`. The S6 lead (§1, F-1) and RQ-08 are corrected; the earlier "no vendor named" was wrong.
- S4_PLAN §C.2 status and header updated; HANDOFF updated. Nothing pushed.

## 2026-10-08 — Peer scoring methods reviewed (owner request; branch `stage/s04-method-library`)

- **New** `research/s4/S4_SCORING_PEER_METHODS.md` (DRAFT).
- **Investwiser scores** traced from its public front-end definitions:
  - Magic Formula = Greenblatt ROC + EY ranks;
  - O'Shaughnessy = VC2-type composite, but shareholder yield includes debt paydown (IW-1);
  - Quality = ROA, equity ratio, earnings stability;
  - Trend = 3 m, 6 m, 12-1;
  - all percentile ranks against all Nordic stocks.
  - Mislabel found: "Operating Profitability (Novy-Marx)" is actually GP/A (IW-2). Undisclosed rules: IW-3, IW-4.
- **Originals recorded:** Greenblatt and O'Shaughnessy (secondary until the books are obtained); quality primaries listed as candidate sources.
- **Seeking Alpha factor grades** (help-centre FAQ and symbol pages):
  - sector-relative A+–F grades on five factors;
  - overall rating with undisclosed weights optimised for prediction, plus disqualification caps;
  - estimates-dependent; US only.
- **One generic score contract** maps all methods.
  - G-1: rank-sum ≡ mean percentile.
  - G-2: z-then-combine vs rank-then-combine share only 27/50 top names (synthetic).
  - G-3: the missing-data rule is material.
- **Fit verdicts:** EY, ROC, VC-type and primary quality measures FIT as candidates. The Greenblatt composite and the sector-relative concept are PARTIAL. Seeking Alpha's overall rating and Investwiser's totals DO NOT FIT. Estimate-based metrics are DEFERRED.
- RQ-28 … RQ-32, the Sørensen record (§7) and HANDOFF annotated. Nothing adopted.

## 2026-10-08 — S6 data-source lead extended; step 1 complete (owner instruction; branch `stage/s04-method-library`)

- **Seeking Alpha** (§4.4), stated in its help centre:
  - fundamentals, estimates and analyst ratings from S&P Global Market Intelligence;
  - backtests from ClariFI (S&P);
  - prices from Quodd (formerly Xignite): Cboe BZX real-time, Nasdaq UTP delayed;
  - "You may not copy or redistribute".
- **Alpha Picks** is a rules-based, unaudited model portfolio. Its sector-relative quant grades and explicit buy/sell rules are recorded as peer references, not adopted.
- **S&P Global Market Intelligence** (§4.5):
  - Capital IQ Pro: enterprise; no public price; third-party estimates ≈$12–30k per user per year.
  - Capital IQ Financials: point-in-time; from 1985; 180,000+ companies.
  - Capital IQ Estimates **Snapshot**: point-in-time every 2 h since Aug 2016.
  - Kensho MCP connector for Claude.
  - Academic access via university and WRDS.
  - Not free; not suitable for a distributed engine.
- **Data lineage** (§4.6): primary sources for statements, estimates, prices, announcements, classification and FX, with free-access status. **ESEF filings via filings.xbrl.org** were verified: 958 Norwegian filings, public JSON-API, as-filed annual data.
- **Findings:** F-4 updated (PIT consensus exists only at vendor level); new F-8 (consumer platforms are resellers) and F-9 (a free primary route for Nordic fundamentals). Candidate stack and open checks extended.
- RQ-08 and HANDOFF updated. Step 1 of the 2026-10-08 plan is complete; the branch was pushed with owner authorisation.

## 2026-10-08 — S6 data-source lead recorded (owner instruction: step 1; branch `stage/s04-method-library`)

- **New** `research/s6/S6_LEAD_DATA_SOURCES_2026-10-08.md` (DRAFT; lead for S6, not a vendor decision). Contents:
  - what ANG, the lecture and the third-party code say about data: no vendor; FactSet only as a future extension in the third-party README;
  - data requirement map D-A … D-H;
  - a dated source and licence table;
  - findings F-1 … F-7, open S6 checks and a candidate stack (not adopted).
- **Vendor identification:**
  - **Simply Wall St = S&P Global Market Intelligence / Capital IQ** (stated in the help centre, data-sources page and terms; licence personal and non-commercial, no retransmission).
  - **Investwiser = EODHD** (inferred, high confidence), from fingerprints:
    - the translation key `unavailableEohd`;
    - `.INDX`, `.FOREX` and `EUFUND` symbology;
    - logo paths that resolve only on eodhd.com, including a stale ticker.
  - Investwiser also states Quartr (transcripts) and Oslo Børs/Nasdaq (announcements).
- **Norges Bank Datatorg verified:** a keyless test query succeeded; 24 dataflows; reuse with attribution.
- **EODHD disclaimer recorded:** non-exchange VWAP pricing, so research-grade.
- **DR-7 refined:** ISIN/FIGI identity; per-user credentials only in the local layer; licence class per source; provenance stamp; no cross-user sharing.
- **Annotated:** RQ-08, CB-19, S4_PLAN §I DR line and HANDOFF.

## 2026-10-08 — ADR-0026 accepted after the owner's check; branch pushed (owner option (a); branch `stage/s04-method-library`)

- **ADR-0026 ACCEPTED.** All quotations, pages and M-1 … M-4 were re-verified against the sources.
  - **Corrections:**
    - C-1: ANG p. 29;
    - C-2: ADR-0025 status;
    - C-3: Sharpe's alpha case, p. 231;
    - C-4: BCD's Tinbergen paraphrase;
    - C-5: ABD's term "adverse selection";
    - C-6: van Binsbergen–Brandt–Koijen cited in §4.1.
  - **Additions:**
    - S-1: ABD p. 66, rule-based automatic rebalancing;
    - S-2: ANG pp. 27–28 self-modification limits; skills, memory and prompts are not mandate fields;
    - S-3: post-cutoff evidence requirement for the value of discretion, plus the D8 detectability point;
    - S-4: BCD p. 20 on self-selected internal benchmarks.
  - An owner check record is appended to the ADR.
- **Annotations** (dated pointer notes; no rewriting):
  - 05 §2 layer 8: tactical judgement means deviation from w*;
  - 08 S13d: a function inventory, and evidence governed by use.
  - Conflicts C-9 and C-10 resolved in S4_PLAN §B.1.
- **Status lines updated:** decision register, S4_PLAN, S4_ACCOUNTABILITY (F20/F21 stay **candidates** for S4.20), S4_DOWNSTREAM_INVENTORY, S4.0 §10, README, HANDOFF (§3, §4.2, §6).
- **Branch pushed** to origin (owner authorisation; no PR). Developer visibility of SYNC-1 material follows; the binding rule is unchanged (only `ACCEPTED` ADRs and `STABLE` sections are built against).

## 2026-10-07 — Look-ahead contamination and agent-homogeneity literature; handoff refresh (owner approval of plan C; branch `stage/s04-method-library`)

- **New** `research/s4/S4_LIT_LOOKAHEAD_2026-10-07.md` (DRAFT), with paper-by-paper verdicts:
  - Henning et al. **v3** (PARTIAL; newest version, read online);
  - Liang 2026 (PARTIAL);
  - Gao, Jiang & Yan 2026 **v2** plus the authors' procedure file (FITS; read as data, never executed);
  - Didisheim, Fraschini & Somoza 2025 (FITS);
  - the 'Sentiment Analysis 2' upload is a duplicate of Glasserman & Lin.
- **Correction:** the bias-direction statement. Cutoff-based evidence shows inflated in-sample accuracy; 'unknown sign' is limited to named-vs-anonymised designs. Also corrected: S4_INPUTS §3.6 (index-level agents are the worst case for outcome recall). All numbers were re-checked against the texts; P3's 2023 mean LAP is 0.016.
- **New candidates:**
  - a clean-window learning rule (a model upgrade resets it);
  - diagnostics X-1 … X-5;
  - developer requirements DR-9 (model provenance) and DR-10 (log-probabilities or repeated sampling). Interface only; not accepted.
- **Pointers:**
  - RQ-10/22/26/55/56 annotated;
  - S4.0 §12 added and the G&L scope noted;
  - S4_PLAN amendment 18 and §I DR line.
- **HANDOFF refreshed:**
  - commits and decisions;
  - §4.6 scoring and new §4.7 contamination;
  - §6 open decisions, including the ADR-0026 check and its pending corrections C-1 … C-6;
  - sources; key results; tooling note.
- Nothing pushed.

## 2026-10-07 — Sørensen/Storebrand scoring recorded as the reference specification (owner instruction; branch `stage/s04-method-library`)

- **New** `research/s4/S4_SCORING_SORENSEN.md` (DRAFT).
  - Method from both source decks, with page references (re-read in full).
  - Verified properties P-1 … P-5 on synthetic data, with an inline script:
    - P-2: under a capped linear objective only the ordering of scores matters;
    - P-3: TE minimisation with a score-exposure target implies α ∝ score, so it needs an RQ-33 mapping;
    - P-4: one outlier moves the effective metric weights for every other name;
    - P-5: the loss-maker sign issue.
  - Open choices O-1 … O-10; V0 (exact) and V1 (corrected) proposed.
  - Placement: individual-security domain, S9c, R8.
  - Anchored EPO with a rank signal: PBL 2021 p. 133, eq. 21.
- Roster v0 = 23 (ANG v2 Exhibit 3 + PC-B6/B7) confirmed by the owner. No roster change.
- RQ-28/29/30/31/33 annotated. S4_PLAN amendment 17 and tracker entry added. HANDOFF §9 gains the `COURSE` path.
- No μ mapping, no master composite, no evaluation claim.

## 2026-10-07 — Owner decisions D-1 … D-4 applied; ADR-0025 accepted (branch `stage/s04-method-library`)

- **ADR-0025 ACCEPTED** (owner decision D-1). Admission is methodological; empirical evaluation (S7) is a separate axis; "production validated" waits for S15.
  - 06 §1 step (3), 06 §2 rule 4 and 02 §D are **annotated, not rewritten**.
  - ADR-0005's status line records the partial supersession, as 01 §3 allows.
  - Decision register updated; conflict C-4 marked resolved in S4_PLAN §B.1.
- **D-2:** the Michaud resampling IP check happens before PC-B4 is implemented; it does not block the specification.
- **D-3:** open SSRN or author working versions are accepted; the journal version governs.
- **D-4:** unchanged (per-item download permission). Two items were permitted on 2026-10-07.
- **CB-17 … CB-19:** the owner confirmed adoption at G4.
- **`.gitignore`:** `.Rhistory` added. The owner's untracked R history file is untouched.
- **ADR-0026 stays PROPOSED**, pending the owner's verification.

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
