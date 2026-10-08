# FinSol — working handoff (single entry point)

**Document status:** DRAFT (living; owner-approved location, 2026-10-07) · **State as of:** 2026-10-08 · **Branch:** `stage/s04-method-library` (pushed to origin 2026-10-08, owner-authorised; no PR) · **Supersedes:** the local files `ENGINE_V1/HANDOFF_2026-10-07.md` and `ENGINE_V1/FINSOL_HANDOFF_2026-10-02.md`.

**What this file is.** The one document to read first, by the owner, a new assistant session, or the developer. It **indexes and summarises** the authoritative documents; it never overrides them. If this file and a document it points to disagree, the pointed-to document wins:
- `ACCEPTED` ADRs win over `STABLE` documents, which win over `DRAFT` documents (01 §2);
- `main` wins over open branches.

**Developer binding rule (README):** build only against `ACCEPTED` ADRs and `STABLE` sections. Everything on this branch since G3 is `DRAFT` or `PROPOSED` until the owner accepts it at a gate, and is invisible to the developer until pushed.

---

## 1. Mandate (00_CHARTER, STABLE)

**Objective.** Specify, precisely enough that a developer can build it **without undocumented financial or methodological assumptions**, a local, browser-based, **personal agentic investment engine**:
- governed by each user's Policy Statement;
- reusable for many local users (initially Norway tax residents);
- using Nordnet and eToro, neither preferred;
- with capital as a continuous input.

**It is** a specification framework. It is done when every component has an accepted spec: inputs, outputs, mathematics, eligibility, data, fallback, evidence status, and whether it is code, agent or human. **It is not** a trading system or a "profitable prediction system".

**Roles:**
- the owner decides every gate;
- the assistant proposes and never accepts its own proposals;
- the developer implements accepted specs.

Principles P1–P13 and rules R1–R8 are in 00 §5 and 05 §1. Exclusions X-01 … X-22 are in 10.

---

## 2. Rules for any assistant working on this project

### 2.1 Owner's standing protocol (binding)
1. Foundation first: data, sample and definitions before anything dependent.
2. No code or document changes without a confirmed plan (scope options plus an honest recommendation), then explicit go-ahead.
3. Small, independently verifiable steps; verify with a source or mathematics.
4. Verify, don't assert; show evidence; say "unknown" when unknown; never fabricate citations, data or attributions.
5. Protect verified results (legacy loop-hash invariant; ask the owner to verify bit-equality when relevant).
6. Push back with reasoning; never rubber-stamp, including the owner's suggestions.
7. For earlier work, search past conversations; current owner instructions win.
8. The owner controls scope and pace.

**Standard:** PhD-grade. Justify choices against alternatives; give epistemic status; engage the literature honestly; pre-empt the strongest objection; keep statistical, economic and causal significance separate; report robustness and fragility unprompted; be concise.

### 2.2 Standing rules (owner decisions)
- **Uncertainty is not a constraint.** Unknown ≠ unsupported ≠ not offered. Gap classes: **A** (we resolve), **B** (external fact), **C** (owner input).
- **Sources are review inputs.** Every upload gets FITS / PARTIAL / DOES NOT FIT and the eight-question fit test (S4 plan §E; formerly handoff §7.5): mandate, layer, authority, setting transfer, computable/governable, in scope, testable against a simple control, not duplicative.
- **Newest version (2026-10-07).** Always work from the newest version of research (paper, code, presentation), and record the version. Newer never raises the source class.
- **Code reuse (2026-10-07).** The paper (newest version) is the baseline. Code, including third-party code, is used where it fits, after verification against the primary source and our invariants, with licence attribution.
- **Agentic learning is a priority (2026-10-07).** Design it in from S4/S8; keep gated promotion (§4.3).
- **Claim labels:** `VERIFIED-SOURCE` (page cited; scope never wider than the source) · `VERIFIED-SECONDARY` · `VERIFIED-DERIVATION` · `VERIFIED-REPO` · `INFERENCE` · `HYPOTHESIS` · `UNVERIFIED`.
- **ADR statement labels:** [SRC] / [AD] / [GR] / [DEF].

### 2.3 Security and isolation (never violate)
- **No personal financial data in the repository.** The local profile lives in git-ignored `local/`. Use synthetic data for tests. Do not resume the owner's questionnaire unless asked. Illustrations use synthetic capital values.
- **No downloads** without explicit per-item permission (filename, source, size). The owner supplies papers.
- **No push, PR or merge** without explicit owner authorisation. Gate workflow: stage branch → gate PR → owner review → merge commit → tag `gate-GNN`.
- **ADRs are append-only after acceptance.** Accepted documents are annotated, never rewritten.
- **Third-party code is never executed** without explicit isolation; API keys are never printed.
- **The ANG sandbox** (`ENGINE_V1/ang_sandbox/`) is **closed** (decision D7, 2026-10-07). It has no authority. Its EODHD/Tiingo keys should be regenerated by the owner.
- **The UI concept prototype** stays outside GitHub (private artifact "Ledger Concept Study").
- **The owner's email** is for identification only.

### 2.4 Tooling (this Mac)
- No `gh` CLI; PRs are made via a compare URL in the browser.
- No `pdftoppm`; for PDFs use `pypdf` plus single-page split plus `sips`; NFKC-normalise text before searching.
- System Python 3.9.6. numpy, scipy and pypdf are in the user site-packages, which `python3 -I` hides: append `~/Library/Python/3.9/lib/python/site-packages` to `sys.path` explicitly.
- Direct downloads (curl) may be blocked by the permission system. The two retrievals permitted on 2026-10-07 used a web-fetch tool, which returns summaries and archives nothing.
- Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Session scratchpads do not persist; durable reviews go into `research/` on approval.

---

## 3. Repository state

### 3.1 Gates and commits
- G0 … G3 closed (PRs #1–#4; tags `gate-G0` … `gate-G3`). `main` = `dcce874`.
- Branch `stage/s04-method-library`, **pushed 2026-10-08** (owner authorisation; no PR):

| Commit | Content |
|---|---|
| `5dfd160` | S4 plan; S4.0 inventory; ANG issues register; ADR-0023/0024 ACCEPTED; ADR-0025 PROPOSED |
| `d113f67` | S4.0 acquisition checklist |
| `7c87442` | S4 closure prep: ADR-0026 PROPOSED; S4_ACCOUNTABILITY; S4_DOWNSTREAM_INVENTORY; RQ-52 … RQ-54 |
| `7118821` | ABD 2014 recorded; TPA task restated; owner decision D-5 (AQR as TPA weight-specification source); ADR-0026 ABD citations |
| `8601950` | Lecture and sandbox inputs; learning first; correlated agent errors; RQ-55, RQ-56; CB-17 … CB-19 proposed |
| `63b2378` | Third-party implementation review (technicalities, mathematics, IPS constraints) |
| `f441bcb` | Combined working handoff (this file) |
| `231c71d` | ADR-0025 ACCEPTED (D-1); 06/02 annotated; D-2, D-3, D-4 recorded; CB-17 … CB-19 adoption at G4 confirmed; `.Rhistory` ignored |
| `ebc8529` | Sørensen/Storebrand scoring recorded as the owner-designated reference specification (`S4_SCORING_SORENSEN.md`); roster v0 = 23 confirmed |
| `a46c613` | Look-ahead and agent-homogeneity literature (`S4_LIT_LOOKAHEAD_2026-10-07.md`); DR-9, DR-10; correction of the bias-direction statement; handoff refresh |
| `d153b4d` | **ADR-0026 ACCEPTED** (owner check, option (a): C-1 … C-6, S-1 … S-4); 05 and 08 annotated; conflicts C-9, C-10 resolved; branch pushed |
| `e9a5aeb` | S6 data-source lead (step 1 of the plan of 2026-10-08); RQ-08, CB-19, DR-7 annotated |
| `96c163c` | S6 lead extended: Seeking Alpha, S&P Capital IQ (Pro, Financials, Estimates), data lineage, ESEF via filings.xbrl.org; step 1 complete; pushed |
| `3aa8f34` | Peer scoring methods (Investwiser Greenblatt/O'Shaughnessy/quality; Seeking Alpha factor grades); G-1 … G-3 |
| `18d738d` | **S4.1** ANG v2 baseline (`S4_ANG_BASELINE.md`); ANG-28 … ANG-36; §A superseded; FMP/Finviz correction |
| `d29fad3` | S4.1 settlement: scoring decision protocol; learning × correlation (ANG-37); covariance evidence; FMP/Finviz; external reviews; **pushed** |
| `37f81df` | **S4.2** adaptation map (`S4_ANG_ADAPTATION.md`) + ADR-0027 PROPOSED; S4_PLAN §B superseded; C-5 … C-14 statuses; **not pushed** |
| `f5470f2` | S4.2 owner-review round: ADR-0027 D3 r2 (later withdrawn); RMT by universe size (`S4_ANG_BASELINE.md` §13.3, Appendix C); score-table spec (`S4_SCORING_PEER_METHODS.md` §9); RQ-14, RQ-32 annotated |
| `afcff9d` | **ADR-0027 D3 r3 = Option A** (owner decision): one authoritative risk model per problem; r2 and P-V1/P-V2 withdrawn (original plan kept); risk-model choice record `S4_RISK_MODEL_CHOICE.md` (M-1, M-2); pushed |
| `4446151` | **S4.3** taxonomy (`S4_TAXONOMY.md`): six kinds, type catalogue, relations, method/configuration/parameter, identity and versioning, inventory pass (F-1 … F-10); pushed |
| `6d9f972` | S4.3 reviewed: owner confirms O-1 … O-4; status REVIEWED; pushed |
| `bb3d983` | **S4.4** PC source map (`S4_PC_SOURCE_MAP.md`): 21/22 SOURCE LOCATED, PC-C5 identity gap; ANG-35 recorded; not pushed |
| `5898b60` | S4.4 update after the owner upload and permitted download: Kirby & Ostdiek (ANG-13 resolved), Michaud 1989 read in full (no resampling procedure; PC-B4 → Michaud & Michaud 2008), MRT working version obtained; ANG-38; PC-C5 identity route; SSRN items for manual download |
| `7e96e56` | S4.4 second round: all 22 methods SOURCE LOCATED; PC-B4 governed by Michaud & Michaud 2008 (book); PC-C5 identity confirmed (byte-identical file, metadata, code reproduction); source issues MCA-1 … MCA-3 |
| `5db675e` | Six SSRN sources reviewed and reproduced (`S4_SOURCE_REVIEWS_2026-10-08.md`; `verification/s44_*.py` all PASS); ANG-39 … ANG-42; GitHub-review HRP correction; pushed |
| `5aa0e36` | S4.4 marked DONE (owner); **Section 2 outline and tracker** `S4_METHODS_OUTLINE.md`; I-7 annotated (HRP); not pushed (owner: push together with S4.5) |
| `e3e0acc` | **S4.5** heuristic portfolios: `S4_HEURISTICS.md` (A1–A5 method records; owner decisions S45-D1 … D4), `S4_EQUATION_REGISTER.md` (created), `verification/s45_*.py` (4 scripts, PASS); ANG-14 sharpened; ANG-43 … ANG-46; MM-1, MM-2; fifth-round uploads recorded (21/22 governing sources in hand; CdST 2006 still open) |
| `1ac0833` | S4.5 owner decisions S45-D1 … D4 recorded (accepted as recommended); S4.5 DONE; CdST 2006 verified (22/22 governing sources in hand); S4.6 NEXT. `5aa0e36`, `e3e0acc` and this commit pushed (owner authorisation 2026-10-08) |
| (latest) | **S4.6** mean–variance foundation: `S4_MVO_FOUNDATION.md`; register EQ-MVO-1 … 4 (+ 2a, 3a, 4a), EQ-MVO-E1, E2; `verification/s46_*.py` (PASS; Jorion 1986 Tables 1–2 reproduced); ANG-47; ANG-44 extended; owner decision S46-D1 open; not pushed |

### 3.2 Decisions (ADRs; `decisions/README.md`)
- 0001–0022 accepted at G0–G3. 0023 (ANG baseline) and 0024 (S4 method governance) ACCEPTED.
- **0025** (admission ≠ evaluation): **ACCEPTED 2026-10-07** (owner decision D-1). 06 §1/§2 and 02 §D are annotated; ADR-0005 is superseded in part.
- **0027** (ANG adaptation: governed learning L-1 … L-7, registry evolution without auto-culling, one authoritative risk model per problem (universe × horizon × risk object; D3 r3, Option A, owner decision 2026-10-08), runtime diagnostics, declared units): **PROPOSED 2026-10-08** (S4.2).
- **0026** (Agent Mandate and Decision Record; investment decision ≠ rebalancing determination ≠ implementation discretion ≠ execution): **ACCEPTED 2026-10-08** after the owner's mathematical/authority check, with corrections C-1 … C-6 and additions S-1 … S-4 (owner check record in the ADR). 05 §2 layer 8 and 08 S13d are annotated.

### 3.3 Where things are (`notes/v2/`)
- **Governance:** 00–10; `decisions/`; `facts/` (registry v1, 82 records).
- **Open questions and the carried gating register:** `research/OPEN_QUESTIONS.md` (RQ-01 … RQ-56; CB-01 … CB-16 in force; CB-17 … CB-19 to be adopted at G4, owner-confirmed).
- **S4 (`research/s4/`):**

| File | Content |
|---|---|
| `S4_PLAN.md` | Plan, amendments 1–18, G4 criteria 1–24 |
| `S4_ANG_BASELINE.md` | **S4.1 (DRAFT, awaiting owner review):** canonical page-cited reconstruction of ANG v2. Stage table; roster reconciliation (44); agent anatomy and skills; data (FMP, Finviz); determinism; IPS governance; limitations; verified exhibit arithmetic (V-1 … V-8; effective N = inverse HHI); lecture cross-check; new issues ANG-28 … ANG-36 |
| `S4_ANG_ADAPTATION.md` | **S4.2 (DRAFT, awaiting owner review):** every baseline element classified U/G/A/D/N (B-1 … B-45); conflicts C-1 … C-14; ANG-01 … ANG-37 dispositioned; developer summary (SYNC-1); companion ADR-0027 PROPOSED |
| `S4_TAXONOMY.md` | **S4.3 (REVIEWED 2026-10-08; O-1 … O-4 confirmed; SYNC-2):** six kinds (Method, Artefact, Role, Control, Record, Input); method types as plugin categories; artefact, role, control, record and input types; relations; method vs configuration vs parameter; identity and versioning; inventory pass with findings F-1 … F-10 |
| `S4_PC_SOURCE_MAP.md` | **S4.4 (DRAFT, owner decisions recorded):** governing primary, supporting sources and access route per roster method; **all 22 SOURCE LOCATED** (PC-C5 identity confirmed; PC-B4 governed by Michaud & Michaud 2008); ANG-vs-source differences; acquisition list (six SSRN items for the owner, four BI items) |
| `S4_SOURCE_REVIEWS_2026-10-08.md` | **Reviews of the six SSRN sources** (He & Litterman, Idzorek, Spinu, López de Prado, Chekhlov–Uryasev–Zabarankin, Boudt–Carl–Peterson): what each specifies, exact reproductions, findings (BL-1 Σ vs Σ̄; IDZ-1 closed-form Ω; HRP-1 order dependence; CDD-1 drawdown definition; BCP-1 MCC vs ERC) |
| `S4_METHODS_OUTLINE.md` | **Orientation for Section 2 (S4.5–S4.14), LIVING:** where we are across the engine; the nine-stage workflow every method step follows; method record template; per-step plan (methods, sources, equations, known issues, owner decisions, verification, deliverable, exit); decision points; acquisitions; tracker |
| `S4_HEURISTICS.md` | **S4.5 (REVIEWED; owner decisions accepted 2026-10-08):** method records for PC-A1 … A5 (sources, equations, inputs, parameter authority, invariants, agent-readable summary); ANG vs source; decisions S45-D1 (volatility-targeting specification), D2 (fixed exponents), D3 (capitalisation data requirements), D4 (cash and universe) |
| `S4_MVO_FOUNDATION.md` | **S4.6 (DRAFT, owner decision open):** the shared mean–variance mathematics (problem, closed forms, riskless asset and separation, GMV, long-only variants, estimation error with Jorion reproduced); ANG-47; decision S46-D1 (numéraire cash as the riskless asset) |
| `S4_EQUATION_REGISTER.md` | **LIVING (created at S4.5):** canonical notation; EQ-H-1 … EQ-H-4 with sub-equations and shared turnover EQ-H-T, each with source page, assumptions, authority, limits and tests; appended at every Section 2 step |
| `S4_0_SOURCE_INVENTORY.md`, `S4_0_ACQUISITION_CHECKLIST.md` | Sources |
| `ANG_ISSUES_REGISTER.md` | ANG-01 … ANG-46; source issues ABD-1 … ABD-5, MCA-1 … MCA-3, MM-1, MM-2 |
| `S4_ACCOUNTABILITY.md` | Mandate schema F1–F19 + candidates F20–F21; stubs |
| `S4_DOWNSTREAM_INVENTORY.md` | T1–T12; FVG lead; simulation conventions |
| `S4_INPUTS_2026-10-07.md` | Lecture, sandbox lessons, learning, correlated errors, derivations D1–D10, developer requirements DR-1 … DR-8 |
| `S4_GITHUB_IMPL_REVIEW.md` | Third-party code: verdicts, mathematics, IPS constraints, invariants I-1 … I-9 |
| `S4_SCORING_SORENSEN.md` | Owner-designated Sørensen/Storebrand value and momentum scores: specification, verified properties P-1 … P-5, open choices O-1 … O-10 |
| `S4_SCORING_PEER_METHODS.md` | Investwiser scoring (Greenblatt, O'Shaughnessy, quality) traced to originals; Seeking Alpha factor grades; one generic score contract; fit verdicts (FITS / PARTIAL / DOES NOT FIT); results G-1 … G-3 |
| `S4_EXTERNAL_REVIEWS_2026-10-08.md` | MongoDB Atlas agentic-portfolio demo (DOES NOT FIT as methodology; S8 infrastructure patterns only); Medium "vibe-coded portfolio" (a personal website, DOES NOT FIT) |
| `S4_LIT_LOOKAHEAD_2026-10-07.md` | Look-ahead contamination and agent homogeneity: four papers (one duplicate removed), bias-direction correction, clean-window rule, diagnostics X-1 … X-5, DR-9, DR-10 |
| `../s6/S6_LEAD_DATA_SOURCES_2026-10-08.md` | **S6 lead (early):** data needs D-A … D-H; source and licence table; Simply Wall St and Seeking Alpha = S&P Global Market Intelligence (stated; Seeking Alpha prices from Quodd); Investwiser = EODHD (inferred from fingerprints); S&P Capital IQ Pro/Financials/Estimates (enterprise; PIT Estimates Snapshot since Aug 2016); data lineage to primary sources (filings, ESEF via filings.xbrl.org, exchanges, brokers); Norges Bank Datatorg verified; DR-7 refined; candidate stack (not adopted) |

---

## 4. Architecture (what we are building)

### 4.1 Baseline and adaptations (ADR-0023; S4 plan §A–§B)
**Baseline.** ANG v2 (arXiv 2604.02279 v2, 21 Sep 2026) is the **architectural baseline**, not a source of method defaults (X-21):
- Policy Statement → Macro → asset-class/CMA agents (bounded LLM judge) → covariance/risk;
- **parallel heterogeneous PC proposals** (roster v0 = 23: 19 ANG methods + Researcher + Adversarial Diversifier + our Simple and Anchored EPO);
- CRO → peer review, vote, revision → CIO (bounded choice among code-computed ensembles);
- investment-case report → investor approval;
- monitoring, rebalancing, learning.

**Our extensions:**
- Simple/Anchored EPO;
- XSMOM/TSMOM signal objects;
- deterministic-only mode (R2);
- facts registry and tax/broker admissibility;
- the accountability layer and the implementation chain (ADR-0026);
- the learning design (§4.3).

### 4.2 Decision-to-execution chain (ADR-0026, ACCEPTED 2026-10-08)
Investor/Policy Statement → accountability layer (mandates, controls set in advance by another party, trace IDs, Decision Records) → deterministic evidence services → ANG organisation → **approved decision** → [conditional tactical mandate] → **deterministic rebalancing determination** → **hybrid Trader** → **deterministic execution** → submission (investor or ADR-0017 grant; dimensions 6–8 locked until S13) → post-trade → monitoring, attribution, learning.

The approved decision carries:
- w*;
- the rebalancing rule;
- the window;
- the maximum interim deviation;
- urgency;
- escalation triggers;
- admitted timing evidence;
- the default action.

The hybrid Trader decides *when and how* within its mandate. It never changes the target, rule, window or limits.

### 4.3 Agentic learning (owner priority; `S4_INPUTS_2026-10-07.md` §4)
- **Reference:** paper §6.2 meta agent plus the lecture's two layers (agent memory; skill evolution; test → promote/rollback).
- **Learning objects** go into the S4.3 taxonomy; **capture from day one** (DR-2).
- **Signals:** outcome-based signals have low power at strategic frequency (D10). Process-based signals (RQ-55) carry the learnable signal.
- **Promotion** is per role, with a diversity check (RQ-56). Material changes are human-approved.
- **RQ-22 is split:** design now, permissions at S17.

### 4.4 Correlated agent errors (RQ-56)
Frontier models make highly correlated errors even across providers (Kim et al., ICML 2025), so model heterogeneity is a tested option, not a guarantee. The robust mitigations are:
- numbers in code (R1/R8);
- a deterministic ballast path;
- independence before exposure;
- judge ≠ author;
- measured error correlation on verifiable tasks;
- diversity-protected learning;
- visible dissent.

### 4.5 Structural lessons from the third-party code (`S4_GITHUB_IMPL_REVIEW.md`)
**Adopt as patterns (S8/S12):**
- a declarative agent registry;
- a mandatory tool sequence;
- tools bound with fixed arguments, with outputs passed **by reference**;
- fail-closed schema gates;
- review/vote barriers;
- a forced vote tool;
- pre-flight gates;
- effort budgets;
- provenance tags;
- variability tests with repeat runs.

**Port and verify:**
- exact projection;
- CVaR LP;
- review assignment (fixed);
- the AdvDiv SCP loop (fixed);
- ensembles.

**Reject:** its BL, robust MV, resampled frontier, tail-risk parity, HRP, the "LW" estimator, its IPS logic and its in-sample backtest. Invariants I-1 … I-9 are binding candidates for S4.23/S8.

### 4.6 Where our own decisions plug in
- **XSMOM/TSMOM:** deterministic signal scripts (AC evidence; μ only through an accepted S9d mapping; TSMOM also usable as Trader timing evidence, logged).
- **Simple/Anchored EPO:** family-B PC agents with the standard anatomy.
- **TPA family:** our own funded, reference-relative, constrained specification plus a distinctness test (S4.12).
- **Sørensen/Storebrand scores** (owner-designated, 2026-10-07):
  - deterministic S9c descriptors SCORE-VAL and SCORE-MOM in the individual-security domain;
  - V0 = the exact source method (reproduction oracle); V1 = a corrected variant, proposed;
  - weights only through an accepted RQ-33 mapping, e.g. Anchored EPO with a rank signal (PBL p. 133).

### 4.7 Look-ahead contamination (`S4_LIT_LOOKAHEAD_2026-10-07.md`)
- **Direction:** cutoff-based evidence shows **inflated** in-sample accuracy. The earlier "unknown sign" applies only to named-vs-anonymised designs.
- **Size:** index-level recall is near-total (S&P 500 monthly correlation 1.00). Historical evidence on asset-class agent judgements therefore carries essentially no weight. R2, the mode stamp and forward testing carry evaluation; deterministic layers are unaffected.
- **Learning:** outcomes count only after the producing model's training cutoff, and a model upgrade resets the window (candidate rule; DR-9).
- **Diagnostics:** X-1 … X-5 (LAP test, q-trimming, rewording dispersion, cross-version comparison, forecast-rationality battery). Platform requirement DR-10 (log-probabilities or repeated sampling).

---

## 5. Stage status and next work

| Stage | Status |
|---|---|
| S0–S3 | Done (G0–G3) |
| S4 | S4.0 done. **S4.1 drafted and settled 2026-10-08** (`S4_ANG_BASELINE.md`, pushed). **S4.2 drafted 2026-10-08** (`S4_ANG_ADAPTATION.md`; ADR-0027 PROPOSED, D3 = r3, Option A, decided by the owner 2026-10-08; awaiting review). S4.2b and S4.15b drafted. **S4.3 reviewed 2026-10-08** (`S4_TAXONOMY.md`; owner confirmed O-1 … O-4; SYNC-2). **S4.4 DONE 2026-10-08** (`S4_PC_SOURCE_MAP.md`; all 22 sources located, 18 in hand; six SSRN sources reviewed and reproduced). **Section 2 (S4.5–S4.14) under way; orientation in `S4_METHODS_OUTLINE.md`.** **S4.5 DONE 2026-10-08** (`S4_HEURISTICS.md`; owner accepted S45-D1 … D4). **S4.6 drafted 2026-10-08** (`S4_MVO_FOUNDATION.md`; decision S46-D1 open) |
| S8 (Track B) | May start after G3. Developer Architecture Brief (S4 plan §I) plus DR-1 … DR-10 registered as interface items; G8a not held |
| S6 | Not started as a stage; **data-source lead recorded early** (2026-10-08) |
| S5, S7, S9–S18 | Not started (08_ROADMAP) |

**Recommended order:**
1. **Owner decisions (§6).**
2. **Push decision** for this branch, so the developer can see SYNC-1 material.
3. **S4.1 → S4.4 sequentially**, stopping for review after each:
   - S4.1: page-cited ANG v2 reconstruction including skill anatomy, cross-checked against the lecture (ANG-24 … ANG-27);
   - S4.2: adaptation map and conflicts;
   - S4.3: taxonomy, including the ADR-0026 objects and the learning objects;
   - S4.4: PC source map.
4. **Paper acquisition** (owner-supplied):
   - Priority A before S4.5–S4.7 (Kirby–Ostdiek, Kan–Zhou, Jagannathan–Ma, He–Litterman, Idzorek, Goldfarb–Iyengar, Tütüncü–Koenig, Ceria–Stubbs, Michaud 1998, Scherer 2002, EPO author code);
   - Priority B before S4.8–S4.14, including Maillard–Roncalli–Teïletche (ERC, PC-C2), López de Prado (HRP), Treynor & Black 1973 and Gilmore & Simonian 2025 (S4.12).
5. **From S4.5:** mathematics and the agent-readable contract are reviewed **together** per method. Reference implementations go in `research/s4/verification/` with invariants I-1 … I-9.
6. **Discipline:**
   - no architecture expansion without a genuine contradiction;
   - every upload gets a fit verdict;
   - nothing is adopted because ANG, a paper, code or a suggestion contains it;
   - S4 gets more selective, not larger.

---

## 6. Open owner decisions (consolidated)

| # | Decision | Recommendation | Where |
|---|---|---|---|
| 0 | **S4.2 review:** accept `S4_ANG_ADAPTATION.md`; accept, amend or defer **ADR-0027** (governed learning; no auto-culling; one authoritative risk model per problem (r3, Option A, decided by the owner 2026-10-08); runtime diagnostics; declared units) | Accept ADR-0027 at G4 or earlier | S4.2 |
| 1 | **S8 start:** circulate the Developer Architecture Brief (S4 plan §I) with DR-1 … DR-10 as interface-only items | After the push | S4 plan §H–§I |
| 2 | **Sandbox keys:** regenerate/revoke the EODHD and Tiingo keys | Do (owner action) | sandbox D7 |
| 2b | **Data access (owner, when S6 starts):** free FRED, OpenFIGI and Tiingo keys; whether to take EODHD All World (+ fundamentals); whether the university licence (Bloomberg / FactSet / I/B/E/S) allows personal research use for validation | Decide at S6; nothing needed now | S6 lead §7–§8 |
| 3 | **Papers to supply** (§5 step 4) | — | S4.0 checklist |
| 4 | **Sørensen production default:** V0 (exact) vs V1 (corrected) | V1 as a pre-registered candidate; V0 kept as the oracle; decide at G9 or earlier | S4_SCORING_SORENSEN §4 |
| 5 | **S4.6 decision S46-D1:** cash at the asset-class level: (a) numéraire cash is the riskless asset (excess returns; cash not a row of Σ; cash share set by the Policy Statement or by a method that includes the riskless asset) vs (b) cash as a risky asset vs (c) both | (a) | `S4_MVO_FOUNDATION.md` §5 |

**Resolved on 2026-10-08 (later):** S4.5 decisions S45-D1 … D4 accepted as recommended (`S4_HEURISTICS.md` §4); CdST 2006 received and verified, so all 22 governing PC sources are in hand; `5aa0e36` and the S4.5 commits pushed with owner authorisation.

**Resolved on 2026-10-08:** ADR-0026 accepted with C-1 … C-6 and S-1 … S-4, and F20/F21 kept as candidate fields; branch pushed (no PR).

**Resolved on 2026-10-07:**
- D-1 (ADR-0025 accepted), D-2 (Michaud IP check before PC-B4), D-3 (SSRN working versions), D-4 (unchanged; two retrievals permitted);
- CB-17 … CB-19 adoption at G4;
- roster v0 = 23 (ANG v2 Exhibit 3 + EPO) confirmed;
- Sørensen/Storebrand designated as the reference scoring specification;
- ABD edits (all five) and D-5;
- CB option (a);
- RQ-55 and RQ-56 as new questions;
- fair value gaps as a research lead;
- agentic learning as a priority;
- the newest-version and code-reuse rules;
- sandbox closure;
- plan A;
- this file's location.

The session reviews of 2026-10-02 (previous handoff §10) are now reflected in the repository:
- architecture → ADR-0026 and S4_ACCOUNTABILITY;
- closure prep → `7c87442`;
- ABD review → ANG-22, ABD-1 … ABD-5 and S4.0;
- self-assessment → the discipline rule in §5 step 6.

---

## 7. Sources at a glance (detail: `research/s4/S4_0_SOURCE_INVENTORY.md`)

| Verdict | Sources |
|---|---|
| **FITS** | ANG v2 (architecture only); Sharpe 1981 (narrow: diversification of judgement); Sensoy 2009 (narrow: controls set in advance); Perold 1988 (shortfall identity); Perold & Sharpe 1988 (rebalancing rule reflects risk tolerance); Nordnet price list 2026-10-07 (facts); **Norges Bank Datatorg** (NOK FX and rates; keyless; attribution); public macro and factor sources (FRED, SSB, ECB, French, AQR, Shiller, Damodaran; S6 lead); **Gao, Jiang & Yan 2026 v2** + procedure file (contamination test); **Didisheim, Fraschini & Somoza 2025** (memorisation; q-trimming; rewording dispersion); **Sørensen 2026 / Storebrand 2025** (secondary; owner-designated reference scoring specification) |
| **PARTIAL** | Q Group lecture Oct 2026 (secondary; learning design, candidate cards, skills, verifiability); BCD 2022 (accountability); **ABD 2014** (funding/benchmarking TPA; rebalancing rule upstream; implementation leeway; verification horizons); **AQR 2026** (TPA weight mechanics per D-5; assumes leverage/shorting); van Binsbergen–Brandt–Koijen 2008; Jegadeesh 1990 and Lehmann 1990 (individual-stock reversal only); Glasserman & Lin 2023 (named vs anonymised only; see §4.7); **Henning et al. 2025 v3** (same-model homogeneity; forecast-rationality battery); **Liang 2026** (pre/post-cutoff magnitudes; weak identification); correlated-error literature (Kim et al. 2025; Kleinberg & Raghavan 2021; Panickssery et al. 2024; Liang et al. 2024); **third-party GitHub code** (patterns and verified pieces only); ML specification (candidates only); z-score screenshot (lead) |
| **DOES NOT FIT** | **Simply Wall St** (S&P Capital IQ data; personal use, no retransmission), **Seeking Alpha** (S&P + Quodd data; no redistribution) and **Investwiser** (EODHD data; personal use) as data sources (peer references only); **S&P Capital IQ** for a distributed engine (enterprise; owner-only validation via university at most); Yahoo/yfinance; Nordnet External API (closed to new subscribers); Tinbergen, Grinold (not needed); misidentified uploads (Jones & Wermers 2011; NBIM news page); Altbridge benchmark; podcast; news items (illustration only) |

---

## 8. Key quantitative results to remember (each with conditions in its source memo)

| Result | Value | Source |
|---|---|---|
| Unconstrained AQR/Treynor–Black sizing = tangency under a factor-model Σ | Numerical difference 1.6 × 10⁻¹⁴; SR² additivity | Checklist A.3 |
| Nordnet Mini→Normal crossover | 49,500 NOK (US/other), 52,667 NOK (Nordic; matches Nordnet's stated guidance) | Inputs memo D4 |
| GMV weights are invariant to the NOK/USD numéraire only if covariance with FX is equal across assets | — | D6 |
| Best Sharpe from 50 null strategies over 5 years | ≈ 1.0 | D7 |
| Detecting ΔSR = 0.04 | 250 / 50 / 5 years at ρ = 0.95 / 0.99 / 0.999 | D9 |
| Trader value | ≈ 1,000 independent legs to detect 10 bp | D8 |
| Outcome-based learning with 12 quarterly observations | Hit-rate SE 0.144 | D10 |
| Third-party HRP | Not permutation-invariant (0.22 vs 0) | Review §7 |
| Volatility floor (σ ≥ c) | Reverse-convex: never a silent hard optimiser constraint | Review §3 |
| Capped linear score objective | Holds the top ⌈1/c⌉ names; invariant to monotone score transforms | Scoring P-2 |
| Minimise TE subject to a score-exposure target | Active weights ∝ Σ⁻¹(s − s̄1), i.e. α ∝ score (max error 2.2 × 10⁻¹⁶) | Scoring P-3 |
| One P/B outlier among 500 synthetic names | Composite rank correlation with P/E 0.77 → 0.94, with P/B 0.53 → 0.23 | Scoring P-4 |
| LLM recall of index returns (GPT-4.1) | S&P 500 monthly correlation 1.00 (sign 98%); stocks 0.20 | Literature §1 P4 |
| Lookahead Propensity after the cutoff | Mean 0.000 (2024) vs 0.18–0.88 (2012–2022) | Literature §1 P3 |
| RMT eigenvalue clipping vs universe size (unconstrained GMV, synthetic) | 17 asset classes: worst (1.77–1.89× oracle vs sample 1.07–1.39×); 100–300 stocks: best (300 stocks, T = 250: 1.26 vs LW-corr 2.63); long-only 10% cap: all 1.06–1.13× | S4.1 §13.3 |
| Mean–variance loss from covariance vs return-forecast errors (17 classes, synthetic) | Unconstrained: return error ≈ 1,000 bp/yr, covariance error ≈ 60–70; sample vs shrinkage 1,655 vs 674 bp/yr. Long-only: estimator choice ≤ 2 bp/yr, 2–5% of weights | `S4_RISK_MODEL_CHOICE.md` M-1 |
| HRP (López de Prado 2016) | Exhibit 7 reproduced exactly; the published algorithm is order-dependent (weights changed in 127/200 random reorderings; up to 52% of the portfolio); the tree-split variant is invariant | Source reviews §4 |
| Idzorek confidence method | Closed form ω = (1−C)/C·τ·pΣp′ equals the paper's numerical search (1.6 × 10⁻⁸) | Source reviews §2 |

---

## 9. Local paths (not in the repository; never copied, for copyright)

| Item | Path |
|---|---|
| Papers | `DOC` = `~/Documents/Documents - Oliver’s MacBook Pro/Portfolio Optimization/Portfolio Optimization/` (incl. `Finsol Research Papers/`: ABD 2014, AQR TPA, Glasserman & Lin, S4 papers zip, the 2026-10-07 look-ahead paper zips); `RPT` = `~/Desktop/Research Papers Thesis/` |
| Course slides (Sørensen/Storebrand) | `COURSE` = `~/Documents/Documents - Oliver’s MacBook Pro/MSc Finance/Semester 2/Res. Meths. Finance/` (`Constructing value and momentum scores.pdf`; `Factor investing Storebrand.pdf`) |
| Lecture | `~/Downloads/Self driving portfolioPP.pdf`; `~/Downloads/Q Group Oct 2026.pptx` |
| BCD 2022 | `~/Downloads/Evaluation_GPFG.pdf` |
| ANG April draft | `~/Downloads/The Self-Driving Portfolio_ …pdf` (superseded) |
| Closed sandbox | `~/Desktop/ENGINE_V1/ang_sandbox/` |
| Legacy | `~/Desktop/ENGINE_V1/` (non-authoritative, ADR-0001) |
