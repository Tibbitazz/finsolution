# FinSol — working handoff (single entry point)

**Document status:** DRAFT (living; owner-approved location, 2026-10-07) · **State as of:** 2026-10-28 · **Branch:** `stage/s04-method-library` (this handoff pushed to origin 2026-10-28, owner-authorised; no PR) · **Supersedes:** the local files `ENGINE_V1/HANDOFF_2026-10-07.md` and `ENGINE_V1/FINSOL_HANDOFF_2026-10-02.md`.

**Committed versus uncommitted work.** This handoff is committed. §11 records work done after `76068d8`: the methodological review, the Hecht check, the F-1 analysis, the S4.13 inventory (*[2026-10-24]* corrected and committed as a DRAFT; *[2026-10-28]* accepted by the owner), analyses delivered to the owner, and owner decisions, some still pending. Nothing in §11 is binding; the documents it points to still govern (01 §2). Updates inside §1–§10 are dated *[2026-10-21]* or later.

**What this file is.** The one document to read first, by the owner, a new assistant session, or the developer. It **indexes and summarises** the authoritative documents; it never overrides them. If this file and a document it points to disagree, the pointed-to document wins:
- `ACCEPTED` ADRs win over `STABLE` documents, which win over `DRAFT` documents (01 §2);
- `main` wins over open branches.

**Developer: start with §10** (building the engine from scratch: what is binding, reading path, architecture, build order, method-library status, rules and invariants, what not to build, open items).

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
- *[2026-10-21]* **Questions are for opinion (2026-10-08).** An owner question gets a sourced opinion, not a document change; change documents only when the owner asks or approves an option, and say explicitly when the existing plan already covers something.
- *[2026-10-21]* **Check coverage before proposing (2026-10-19).** Before labelling any research-derived enhancement "Adopt", check the actual governance text (ADRs, 06 §5 contract fields, RQ notes, S4_PLAN rows, the S4.15b inventory, equation lists), not titles. On 2026-10-19 nearly all of eight proposals (E-1 … E-8) duplicated existing rules, and some were bans on things nobody had proposed.
- *[2026-10-21]* **Structural checks are not methodological validity (2026-10-20).** A passing registry checker or a complete table does not show that the methodological choices are right; verify definitions and mathematics first, and say what a checker cannot check.
- *[2026-10-21]* **Read-only reviews stay read-only.** When the owner asks for a review or a plan, change nothing until the owner authorises the plan.

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
- Branch `stage/s04-method-library`, first pushed 2026-10-08, **last pushed 2026-10-19** (owner authorisation each time; no PR):

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
| `389eff4` | **S4.6** mean–variance foundation: `S4_MVO_FOUNDATION.md`; register EQ-MVO-1 … 4 (+ 2a, 3a, 4a), EQ-MVO-E1, E2; `verification/s46_*.py` (PASS; Jorion 1986 Tables 1–2 reproduced); ANG-47; ANG-44 extended; owner decision S46-D1 open |
| `b38f1d4` | S4.6 decision S46-D1 recorded (numéraire cash as the riskless asset; risk-free rate = after-tax rate on uninvested cash at the best liquid deposit, otherwise the broker cash rate); S4.6 DONE; RQ-57 (household-level advice incl. BSU) ON HOLD; S4.7 NEXT; pushed with `389eff4` (owner authorisation) |
| `f28d116` | **S4.7** mean–variance family: `S4_MVO_FAMILY.md` (B1, B2, B3, B4, B6, B7 records; lineage; decisions S47-D1 … D6 incl. the cash/risky split); register S4.7 entries; `verification/s47_*.py` (5 scripts, PASS; Michaud Tables 5.1/6.1 and Goldfarb–Iyengar calibration reproduced; PBL Props. 1–3 verified); ANG-48, ANG-49; BL-2, MCH-1, PBL-1, PBL-2 |
| `f063e5a` | S4.7 decisions part 1 (D1, D2 rule, D3, D4, D5; D-2 closed); EPO grid design study |
| `ce32bb1` | S4.7 DONE: S47-D2 parameters (θ = 0; 11-point logit grid) and S47-D6 (engine-level risk target per method type; EQ-SPLIT-1; adaptation B-46) recorded; S4.8 NEXT; pushed with `f28d116`, `f063e5a` (owner authorisation) |
| `2135803` | **S47-D7** (Michaud patent family closed; components enter as candidates); Paleologo 2025 registered with PAL-1 … PAL-8 and `verification/s48_kalman_ewma_paleologo.py` (PASS); S4.8 supporting sources received (7 of 8); **OpenBB decisions OB-1** (ODP as data-access layer) **and OB-2** (Workspace as interface reference; DR-11); RQ-08, RQ-10, RQ-44 annotated; **pushed 2026-10-15** (owner authorisation) |
| `e32458a` | S4.8 scope accepted (S4_PLAN amendment 19); discussion records on RQ-09/11/14/15/16/28/31/32/33/35; handoff refreshed |
| `31d18c3` | **S4.8 drafted:** `S4_MOMENTUM.md` (SIG-1 XSMOM, SIG-2 TSMOM; variants residual, factor, trend-filter; strategy-level scaling); register EQ-SIG-1 … EQ-SIG-5; `verification/s48_momentum_constructions.py`, `s48_trend_filters.py` (PASS); ANG-23 annotated; HOP-1, DM-1/2, BHM-1, GK-1, EL-1/2, BRU-1/2, PBL-3; decisions S48-D1 … D6 open |
| `0f94d14` | **S4.8 DONE:** decisions S48-D1, D2, D4, D5, D6 recorded (`S4_MOMENTUM.md` §5.1; register aligned); D3 → S4.9; RQ-32 corrected; RQ-07 universe instruction; RQ-11/RQ-32 factor-momentum notes; S4.9 NEXT |
| `86c1ace` | **S4.9 drafted:** `S4_SIGNAL_PC_COMPATIBILITY.md`; register EQ-MAP-1 … 4; `verification/s49_signal_pc_compatibility.py` (PASS); RQ-33 annotated; decisions S49-D1 … D5 open |
| `34b7b06` | **S4.9 reviewed** (owner review 2026-10-18): EPO consumes expected returns (draft wording corrected); rule **R-7** (no double counting: sleeves inside the host class, look-through risk, one channel per signal, exposure reports); D cells tested (three V1; **seven to the research lane**, S49-D1; two untested); **EQ-MAP-3 corrected** per Grinold 1994 and Grinold & Kahn *Advances* ch. 3; **EQ-TC-1** transfer coefficient; S49-D1, D3, D4 decided, D2 and D5 open; `verification/s49_double_counting_dcells.py`, `s49_alpha_sources.py` (PASS); GRI-1, GRI-2, LEC-1; sources §17; RQ-28 (EP = economic profit), RQ-32, RQ-33 annotated; **pushed 2026-10-18 together with `e32458a`, `31d18c3`, `0f94d14`, `86c1ace`** (owner authorisation) |
| `2972c46` | **S4.9 DONE:** S49-D2 (sleeves under R-7: long-only tilts inside the host class; zero-investment long–short sleeves only where shorting is permitted and then units of their own; no sleeve-level scaling in the base case; constant volatility a variant; DM dynamic weight a timing model, S13c) and S49-D5 (composition rules for V/V1, fixed per run, never agent-selectable; duplicate detection at S4.16); R-7a exception verified (`s49_double_counting_dcells.py`); S48-D3 closed; RQ-17 annotated; S4.10 NEXT |
| `562e10d` | **S4.10 drafted:** `S4_ANCHOR_BENCHMARK.md` (owner reminded of S47-D3 first; six objects; anchor contract AC-1 … AC-7; 60/40 not ASK-eligible (bond and high-yield funds below the 80% share rule) and household feasibility EQ-FEAS-1; Roll 1992 and Jorion 2003 verified: tracking-error optimisation ignores total risk, a total-risk constraint costs little; GRS benchmark efficiency); register EQ-ANC-1, EQ-FEAS-1, EQ-TEV-1, EQ-TEV-2, EQ-GRS-1; `verification/s410_anchor_benchmark.py` (PASS); ROLL-1, GKA-1; sources §18; RQ-09 annotated; decisions S410-D1 … D6 open |
| `3c27e0a` | **S4.10 DONE:** owner accepted S410-D1 … D6 (anchor contract; admissible anchor sources; default `POL.benchmark` if feasible, else 1/σ, securities by market capitalisation; infeasible anchors: household check EQ-FEAS-1, account-level projection to cash; 60/40 only via `POL.benchmark`; total-risk constraint inside benchmark-relative candidates, noted on EQ-SPLIT-1 for G4); S47-D3 closed; S4.11 NEXT |
| `d16f9bd` | RQ-18 discussion record (accounts and asset location); **pushed 2026-10-18 with `2972c46`, `562e10d`, `3c27e0a`** (owner authorisation) |
| `9d4eddb` | **S4.11 drafted:** `S4_RISK_STRUCTURED.md` (GMV, ERC, HRP, MDP, MinCorr records; verified relations and implied expected-return beliefs; S4_PLAN equivalence example corrected: MD = GMV when volatilities are equal); register EQ-RS-1 … EQ-RS-5; `verification/s411_risk_structured.py` (PASS); MCA-4; C5 × O2 → research lane; decisions S411-D1 … D5 open |
| `e81598c` | **S4.11 DONE:** owner accepted S411-D1 … D5 (GMV long-only with Policy Statement bounds; HRP V1 tree split, V0 oracle; MinCorr, MinCorr2 sensitivity; post-processing bounds for ERC/HRP/MinCorr; typed failure records); S4.12 NEXT; pushed with `9d4eddb` (owner authorisation) |
| `02ecd79` | HANDOFF §10 developer guide (building the engine from scratch); file table refreshed; **pushed 2026-10-18 with `e81598c`** (owner authorisation, with the S4.12a/b split agreed) |
| `e50fed5` | **S4.12a drafted** (S4_PLAN amendment 20): `S4_NON_TRADITIONAL.md` (CVaR, drawdown, tail-risk parity, mean–downside records; NT-1 scenario location; normal-limit relations; CDD-3 convex relative drawdown); register EQ-NT-1 … 3, EQ-DS-1, 2, EQ-SCN-1; `verification/s412_*.py` (3 scripts, PASS); RU-1 … 3, SVDM-1, KS-1, BCP-4, BCP-5, CDD-3; ANG-02/18/39/40 annotated; D3 × O2 → research lane; inventory §19; decisions S412-D1, D2, D3, D5, D6 open. **pushed 2026-10-19** with the S4.12b decision commit |
| `11c6fd0` | **S4.12a DONE:** owner accepted S412-D1, D2, D3, D5, D6, option (a) in each (min-CVaR on demeaned scenarios, β = 0.95; relative compounded MaxDD in convex form; ERC-CVaR by the convex form, MCC a variant; max Sortino with MAR = cash rate; scenario location rule: demeaned for μ-free uses, centred on S9's μ otherwise, never raw historical); S4.9 annotated; ANG-02/18/39/40 resolved; S4.12b NEXT. **pushed 2026-10-19** with the S4.12b decision commit |
| `5e671fe` | **S4.12b drafted:** `S4_NON_TRADITIONAL.md` Part B (PC-D4 TPA-R record; distinctness test passed against B1, B1 + TE, Roll and Anchored EPO; TPA gap memo); register EQ-NT-4; `verification/s412b_tpa.py` (PASS); TB-1, TPA-1, TPA-2; ANG-06/15/22 annotated; inventory §20; decision S412-D4 open. **pushed 2026-10-19** with the S4.12b decision commit |
| `a9a2689` | **S4.12b DONE:** owner decision S412-D4 = option (a) (chosen as "B" in the discussion): TPA-R (V1) plus the funding report on every candidate card; Gilmore & Simonian 2025, Elkamhi & Lee 2025 and Cavaglia, Han & Seshadri 2026 read (`S4_NON_TRADITIONAL.md` §9.8; inventory §21; Cavaglia's single-candidate weight verified in `s412b_tpa.py`); ANG-15/22 resolved. Discussion records from the owner's methodological review (2026-10-19): RQ-08 (no text-to-signal capability, three revisit triggers), RQ-28/RQ-30 (two S9c candidates), S4.15b T6/T12 sources located (inventory §22). S4.13 NEXT. **Pushed 2026-10-19 with `e50fed5`, `11c6fd0`, `5e671fe`** (owner authorisation) |
| `76068d8` | HANDOFF refreshed for hand-over: last push date; `2135803` hash; RQ-57; amendments 1–20; S4.12 issues, equations and scripts; TPA in §4.6, §7 (fit verdicts for the three TPA uploads), §8, §10.7 and §10.8 (funding report rule); DR-11 in §6. **Pushed 2026-10-19** (owner authorisation) |
| `61792e4` | **HANDOFF published 2026-10-24** (owner request): §11 adds the work since `76068d8` (methodological review E-1 … E-8, Hecht 2014 check, F-1 analysis, S4.13 draft, review and correction plan, checker limitations, the two 2026-10-24 analyses). Only `notes/v2/HANDOFF.md` changed; the S4.13 drafts remain uncommitted |
| `0ae42a9` | *[2026-10-24]* **S4.13 corrected and committed** (owner authorised corrections 1–21, the candidate kind MEASURE, this commit and the push): `research/s4/S4_RISK_DEPENDENCIES.md` (DRAFT; 24 candidates COV-1 … COV-24, with modified CVaR as COV-24 of kind MEASURE; exact F-1 condition in §6.1; F-11 mixed portfolios; RO-3 narrowed; EQ-SIG-4 internal; changes listed in its §10) and `research/s4/verification/s413_risk_dependencies.py` (PASS); S4_PLAN C.2 row; verification README (31 scripts); this handoff (§3, §5, §6 items 10, 13, 15, 16; §10.7, §10.10; §11). S4.13 awaits owner acceptance; F-1 awaits an owner decision. **Pushed 2026-10-24** (owner authorisation) |
| `e1cd68f` | *[2026-10-25]* **Corrections against Renshaw et al. (2026)** (owner decisions D1 and D4, 2026-10-25): RQ-28 (cyclical value = book-to-price + earnings yield; Shiller-type definition removed; signals per the source), RQ-31 (reference transform), RQ-32 (source; value sleeves weakly related), RQ-11 (reference timing specification), S48-D6 annotation, source inventory §23, CHANGELOG, this handoff (§6 items 17–20, §11.9). **Pushed 2026-10-25** (owner authorisation) |
| `54ffad9` | *[2026-10-25]* **Renshaw et al. reference specification recorded** (owner decisions REN-D1 … REN-D7): new record `research/s4/S4_SCORING_RENSHAW_ANG.md` (18 signals, four factor scores, construction with FinSol adaptations, three timing models in shadow mode, data map); `verification/s4ren_multifactor_reference.py` (PASS); R-1 refined and EQ-MAP-5 registered; Sørensen definitions superseded (kept as display transform, oracle and standalone SIG-1); S4_PLAN amendment 21; RQ-08/11/17/28/29/33/37 notes; source inventory §23 (+ Eisfeldt, Kim & Papanikolaou; three papers for the owner to supply); verification README (32 scripts). Committed 2026-10-25; **pushed 2026-10-25 with `af04d93`** (owner authorisation) |
| `af04d93` | *[2026-10-25]* **Momentum and interface review decisions** (owner approvals P1, P2, P3, P5, P6, P7; P4 not needed; OB-2 amended): score-table rows replaced by the Renshaw factors with a trend-state column and the multifactor score as a labelled aggregation (P1); rule T-9 vocabulary (P2); T-1 clarified and T-7 revised so that red/green is presentation only (P3); `no.wrapper.ask.eligible_holdings@2` (claim wording: shares of EEA-domiciled companies; source re-read) and the RQ-07 note corrected (P5); security-sleeve review in the AC/CMA mandate (P6, `S4_ACCOUNTABILITY.md` §2); RQ-20 candidate S14 template, the 13-section CIO report (P7); OB-2 amended to a combined Investwiser / OpenBB Workspace reference (S6 lead §4.7, DR-11, RQ-10); S6 lead §4.2 EODHD attribution owner-confirmed; new developer lead `research/s8/S8_LEAD_UX_MARKET_FIND_ANALYSIS_2026-10-25.md`. **Pushed 2026-10-25** (owner authorisation) |
| `828e0e7` | *[2026-10-26]* **S4.13 aligned with the Renshaw record** (owner authorisation): SIG-1/R row for idiosyncratic momentum (signal 7) on RO-8; cross-cutting rows for the construction (EQ-MAP-5 on RO-2) and the timing models (internal, shadow mode); findings F-12 and F-13; evidence sweep (119 established markers, 114 matched, five misattributions corrected); the checker accepts REN-Dx; Renshaw record §4 cross-reference; S4_PLAN amendment 21 note. Pushed 2026-10-28 (owner authorisation) |
| `22b384c` | *[2026-10-28]* **F-1 decided, option (a)** (owner decision): "demeaned" = each asset's excess return minus its own mean, centred on zero, cash rate not added back (D1 V0, D3); μ-consuming methods declare their basis at S4.20 (defaults: D2 total; B5 total with MAR = the cash rate; D1 V1 the target's basis); dated notes on S412-D6, EQ-SCN-1 and R-3; seven S4.13 cells updated; return basis proposed for ADR-0027 D5. Pushed 2026-10-28 (owner authorisation) |
| (latest) | *[2026-10-28]* **S4.13 accepted; bookkeeping** (owner authorisation): S4.13 DONE (ADR-0027 stays PROPOSED); S4_PLAN C.2 (S4.13 DONE; Option D notes on S4.16 and S4.18); outline tracker (S4.12b, S4.13); RQ-14 note; source inventory §24 (Wang, Chen & Wu 2025; Hecht 2014); verification README; CHANGELOG; this handoff. Pushed 2026-10-28 with `828e0e7` and `22b384c` (owner authorisation) |

### 3.2 Decisions (ADRs; `decisions/README.md`)
- 0001–0022 accepted at G0–G3. 0023 (ANG baseline) and 0024 (S4 method governance) ACCEPTED.
- **0025** (admission ≠ evaluation): **ACCEPTED 2026-10-07** (owner decision D-1). 06 §1/§2 and 02 §D are annotated; ADR-0005 is superseded in part.
- **0027** (ANG adaptation: governed learning L-1 … L-7, registry evolution without auto-culling, one authoritative risk model per problem (universe × horizon × risk object; D3 r3, Option A, owner decision 2026-10-08), runtime diagnostics, declared units): **PROPOSED 2026-10-08** (S4.2).
- **0026** (Agent Mandate and Decision Record; investment decision ≠ rebalancing determination ≠ implementation discretion ≠ execution): **ACCEPTED 2026-10-08** after the owner's mathematical/authority check, with corrections C-1 … C-6 and additions S-1 … S-4 (owner check record in the ADR). 05 §2 layer 8 and 08 S13d are annotated.

### 3.3 Where things are (`notes/v2/`)
- **Governance:** 00–10; `decisions/`; `facts/` (registry v1, 82 records; *[2026-10-25]* plus one later version, `no.wrapper.ask.eligible_holdings@2`, P5).
- **Open questions and the carried gating register:** `research/OPEN_QUESTIONS.md` (RQ-01 … RQ-57, RQ-57 ON HOLD; CB-01 … CB-16 in force; CB-17 … CB-19 to be adopted at G4, owner-confirmed).
- **S4 (`research/s4/`):**

| File | Content |
|---|---|
| `S4_PLAN.md` | Plan, amendments 1–21, G4 criteria 1–24 |
| `S4_ANG_BASELINE.md` | **S4.1 (DRAFT, awaiting owner review):** canonical page-cited reconstruction of ANG v2. Stage table; roster reconciliation (44); agent anatomy and skills; data (FMP, Finviz); determinism; IPS governance; limitations; verified exhibit arithmetic (V-1 … V-8; effective N = inverse HHI); lecture cross-check; new issues ANG-28 … ANG-36 |
| `S4_ANG_ADAPTATION.md` | **S4.2 (DRAFT, awaiting owner review):** every baseline element classified U/G/A/D/N (B-1 … B-45); conflicts C-1 … C-14; ANG-01 … ANG-37 dispositioned; developer summary (SYNC-1); companion ADR-0027 PROPOSED |
| `S4_TAXONOMY.md` | **S4.3 (REVIEWED 2026-10-08; O-1 … O-4 confirmed; SYNC-2):** six kinds (Method, Artefact, Role, Control, Record, Input); method types as plugin categories; artefact, role, control, record and input types; relations; method vs configuration vs parameter; identity and versioning; inventory pass with findings F-1 … F-10 |
| `S4_PC_SOURCE_MAP.md` | **S4.4 (DRAFT, owner decisions recorded):** governing primary, supporting sources and access route per roster method; **all 22 SOURCE LOCATED** (PC-C5 identity confirmed; PC-B4 governed by Michaud & Michaud 2008); ANG-vs-source differences; acquisition list (six SSRN items for the owner, four BI items) |
| `S4_SOURCE_REVIEWS_2026-10-08.md` | **Reviews of the six SSRN sources** (He & Litterman, Idzorek, Spinu, López de Prado, Chekhlov–Uryasev–Zabarankin, Boudt–Carl–Peterson): what each specifies, exact reproductions, findings (BL-1 Σ vs Σ̄; IDZ-1 closed-form Ω; HRP-1 order dependence; CDD-1 drawdown definition; BCP-1 MCC vs ERC) |
| `S4_METHODS_OUTLINE.md` | **Orientation for Section 2 (S4.5–S4.14), LIVING:** where we are across the engine; the nine-stage workflow every method step follows; method record template; per-step plan (methods, sources, equations, known issues, owner decisions, verification, deliverable, exit); decision points; acquisitions; tracker |
| `S4_HEURISTICS.md` | **S4.5 (REVIEWED; owner decisions accepted 2026-10-08):** method records for PC-A1 … A5 (sources, equations, inputs, parameter authority, invariants, agent-readable summary); ANG vs source; decisions S45-D1 (volatility-targeting specification), D2 (fixed exponents), D3 (capitalisation data requirements), D4 (cash and universe) |
| `S4_MVO_FOUNDATION.md` | **S4.6 (REVIEWED; S46-D1 decided 2026-10-08):** the shared mean–variance mathematics (problem, closed forms, riskless asset and separation, GMV, long-only variants, estimation error with Jorion reproduced); ANG-47; decision S46-D1 (numéraire cash as the riskless asset) |
| `S4_MVO_FAMILY.md` | **S4.7 (REVIEWED; S47-D1 … D6 decided 2026-10-08; S47-D7, Michaud patent family closed, 2026-10-15):** maximum Sharpe (constrained convex form), Black–Litterman (BL 1992 conventions; BL-2), robust MV (Goldfarb–Iyengar; ANG-48), resampled frontier (Michaud; D-2; ANG-49), simple and anchored EPO (PBL; Props. 1–3); lineage; decisions S47-D1 … D6 |
| `S4_MOMENTUM.md` | **S4.8 (REVIEWED 2026-10-15; scope = S4_PLAN amendment 19; decisions S48-D1, D2, D4, D5, D6; D3 → S4.9):** SIG-1 XSMOM and SIG-2 TSMOM construction records with variants (residual momentum, factor momentum, trend-filter family incl. Kalman = EWMA) and strategy-level scaling (constant volatility; DM dynamic); both signals in every domain with the skip by asset type; factor momentum for long-only users as time-varying blend weights |
| `S4_SIGNAL_PC_COMPATIBILITY.md` | **S4.9 (DONE 2026-10-18; S49-D1 … D5):** objects O1–O6; compatibility matrix for the 23 methods (V / V1 / M / R / D / —); rules R-1 … R-7 (no unscaled scores into optimizers, EPO included; units; direction rules after the engine-level scaling; no double counting); transfer coefficient EQ-TC-1; research-lane constructions; composition rules fixed per run |
| `S4_ANCHOR_BENCHMARK.md` | **S4.10 (DONE 2026-10-18; S410-D1 … D6):** six objects (anchor slot, anchor source, benchmark definition, benchmark weights/returns, comparison benchmark, simple control); anchor contract AC-1 … AC-7; account and household feasibility (EQ-FEAS-1); tracking error (Roll 1992, Jorion 2003); GRS benchmark efficiency |
| `S4_RISK_STRUCTURED.md` | **S4.11 (DONE 2026-10-18; S411-D1 … D5):** GMV, ERC, HRP (V1 tree split), MDP, MinCorr records; verified relations and implied beliefs; failure records |
| `S4_NON_TRADITIONAL.md` | **S4.12a (DONE 2026-10-18; S412-D1, D2, D3, D5, D6, option (a)); S4.12b Part B (DONE 2026-10-19; S412-D4 option (a): TPA-R, distinctness test, gap memo, the three TPA papers §9.8):** CVaR, drawdown, tail-risk parity and mean–downside records; scenario location (NT-1) and the location rule (S412-D6, EQ-SCN-1); relations under normality (GMV, ERC, max Sharpe, MV frontier); convex relative drawdown (CDD-3); failure codes |
| `S4_RISK_DEPENDENCIES.md` | *[2026-10-24]* **S4.13 (*[2026-10-28]* DONE, accepted by the owner; corrected 2026-10-24; aligned with the Renshaw record 2026-10-26):** method → risk-input map (28 method records in 33 rows, plus 8 cross-cutting consumers); 3 provisional problems; 8 shared risk objects RO-1 … RO-8; 24 candidates COV-1 … COV-24 in seven kinds (including MEASURE, for modified CVaR), none selected, no thresholds; findings F-1 … F-13 (F-1: exact ERC-CVaR existence condition in §6.1, *[2026-10-28]* decided, option (a); F-11: joint risk for mixed asset-class and security portfolios, unresolved; F-12: one S10 security model for PC-B3, Renshaw signal 7 and EQ-MAP-5; F-13: the reference level of a sleeve's total-risk constraint); status markers established / provisional / unresolved; ADR-0027 treated as PROPOSED |
| `S4_EQUATION_REGISTER.md` | **LIVING (created at S4.5):** canonical notation; EQ-H (heuristics), EQ-MVO, EQ-EPO, EQ-BL, EQ-ROB, EQ-REF, EQ-SPLIT-1, EQ-SIG (momentum), EQ-MAP (signal → μ), EQ-TC-1, EQ-ANC/FEAS/TEV/GRS (anchors and benchmarks), EQ-RS (risk-structured), EQ-NT-1 … 3, EQ-DS, EQ-SCN-1 (scenario and downside methods, S4.12a), EQ-NT-4 (TPA-R, S4.12b); each with source page, assumptions, authority, limits and tests |
| `verification/` | **Reference implementations (oracles, not production code; ADR-0024 §8):** 32 committed self-asserting scripts that print PASS, including the S4.13 registry checker `s413_risk_dependencies.py` (*[2026-10-24]*) and `s4ren_multifactor_reference.py` (*[2026-10-25]*); index in `verification/README.md` |
| `S4_0_SOURCE_INVENTORY.md`, `S4_0_ACQUISITION_CHECKLIST.md` | Sources |
| `ANG_ISSUES_REGISTER.md` | ANG-01 … ANG-49; source issues ABD-1 … ABD-5, MCA-1 … MCA-4, MM-1, MM-2, BL-2, MCH-1, PBL-1 … PBL-3, PAL-1 … PAL-8, the S4.8 momentum set (HOP-1, DM-1/2, BHM-1, GK-1, EL-1/2, BRU-1/2), GRI-1, GRI-2, LEC-1, ROLL-1, GKA-1, and the S4.12 set (RU-1 … RU-3, SVDM-1, KS-1, BCP-4, BCP-5, CDD-3, CES-1, TB-1, TPA-1, TPA-2) |
| `S4_ACCOUNTABILITY.md` | Mandate schema F1–F19 + candidates F20–F21; stubs; *[2026-10-25]* security-sleeve review in the AC/CMA mandate (P6) |
| `S4_DOWNSTREAM_INVENTORY.md` | T1–T12; FVG lead; simulation conventions; T6/T12 source leads (2026-10-19) |
| `S4_INPUTS_2026-10-07.md` | Lecture, sandbox lessons, learning, correlated errors, derivations D1–D10, developer requirements DR-1 … DR-8 |
| `S4_GITHUB_IMPL_REVIEW.md` | Third-party code: verdicts, mathematics, IPS constraints, invariants I-1 … I-9 |
| `S4_SCORING_SORENSEN.md` | Owner-designated Sørensen/Storebrand value and momentum scores: specification, verified properties P-1 … P-5, open choices O-1 … O-10 |
| `S4_SCORING_RENSHAW_ANG.md` | *[2026-10-25]* **Reference specification for the multifactor composite** (owner decisions REN-D1 … REN-D7): Renshaw, Gu, Candar & Ang (2026) and the iSTOXX methodology guide §118; 18 signals, four factor scores, base weights 1/3–1/3–1/6–1/6, maximum exposure under a tracking-error budget (EQ-MAP-5), three timing models in the research lane in shadow mode; construction only, FinSol's own universe and data; supersedes the Sørensen definitions |
| `S4_SCORING_PEER_METHODS.md` | Investwiser scoring (Greenblatt, O'Shaughnessy, quality) traced to originals; Seeking Alpha factor grades; one generic score contract; fit verdicts (FITS / PARTIAL / DOES NOT FIT); results G-1 … G-3 *[2026-10-25]* §9: Renshaw factor rows and trend-state column (P1); T-9 vocabulary (P2); T-1 clarified, T-7 revised to colour-as-presentation (P3) |
| `S4_EXTERNAL_REVIEWS_2026-10-08.md` | MongoDB Atlas agentic-portfolio demo (DOES NOT FIT as methodology; S8 infrastructure patterns only); Medium "vibe-coded portfolio" (a personal website, DOES NOT FIT) |
| `S4_LIT_LOOKAHEAD_2026-10-07.md` | Look-ahead contamination and agent homogeneity: four papers (one duplicate removed), bias-direction correction, clean-window rule, diagnostics X-1 … X-5, DR-9, DR-10 |
| `../s6/S6_LEAD_DATA_SOURCES_2026-10-08.md` | **S6 lead (early):** data needs D-A … D-H; source and licence table; Simply Wall St and Seeking Alpha = S&P Global Market Intelligence (stated; Seeking Alpha prices from Quodd); Investwiser = EODHD (inferred from fingerprints; *[2026-10-25]* owner-confirmed from Investwiser's FAQ); S&P Capital IQ Pro/Financials/Estimates (enterprise; PIT Estimates Snapshot since Aug 2016); data lineage to primary sources (filings, ESEF via filings.xbrl.org, exchanges, brokers); Norges Bank Datatorg verified; DR-7 refined; candidate stack (not adopted). *[2026-10-15]* §4.7 OpenBB: ODP v5 admitted as a data-access layer (OB-1); Workspace as the interface reference (OB-2) |
| `../s8/S8_LEAD_UX_MARKET_FIND_ANALYSIS_2026-10-25.md` | *[2026-10-25]* **S8 lead (DRAFT): page layout and interaction design for Market, Find Investments and Analysis** (developer brief under OB-2 as amended): design principles UX-1 … UX-13; process-numbered navigation; shared components C-1 … C-16; the three areas page by page; agent assessment cards with citations instead of a chat; template-generated sentences; data contract per widget; what not to build; traceability to T-1 … T-9, R8, ADR-0017/0019/0025/0026. Names no product |

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
- **TPA family (S412-D4, option (a), 2026-10-19):** TPA-R, our own funded, reference-relative, constrained specification (distinctness test passed), plus the funding report (β, α, appraisal ratio against `POL.benchmark`) on every candidate card (S4.16).
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
| S4 | S4.0 done. **S4.1 drafted and settled 2026-10-08** (`S4_ANG_BASELINE.md`, pushed). **S4.2 drafted 2026-10-08** (`S4_ANG_ADAPTATION.md`; ADR-0027 PROPOSED, D3 = r3, Option A, decided by the owner 2026-10-08; awaiting review). S4.2b and S4.15b drafted. **S4.3 reviewed 2026-10-08** (`S4_TAXONOMY.md`; owner confirmed O-1 … O-4; SYNC-2). **S4.4 DONE 2026-10-08** (`S4_PC_SOURCE_MAP.md`; all 22 sources located, 18 in hand; six SSRN sources reviewed and reproduced). **Section 2 (S4.5–S4.14) under way; orientation in `S4_METHODS_OUTLINE.md`.** **S4.5 DONE 2026-10-08** (`S4_HEURISTICS.md`; owner accepted S45-D1 … D4). **S4.6 DONE 2026-10-08** (`S4_MVO_FOUNDATION.md`; owner decided S46-D1). **S4.7 DONE 2026-10-08** (`S4_MVO_FAMILY.md`; owner decided S47-D1 … D6; engine-level risk target B-46; S47-D7 on 2026-10-15). **S4.8 DONE 2026-10-15** (`S4_MOMENTUM.md`; owner decided S48-D1, D2, D4, D5 in principle, D6; D3 → S4.9). **S4.9 DONE 2026-10-18** (`S4_SIGNAL_PC_COMPATIBILITY.md`; owner decided S49-D1 … D5). **S4.10 DONE 2026-10-18** (`S4_ANCHOR_BENCHMARK.md`; owner accepted S410-D1 … D6). **S4.11 DONE 2026-10-18** (`S4_RISK_STRUCTURED.md`; owner accepted S411-D1 … D5). **S4.12 split (amendment 20): S4.12a DONE 2026-10-18** (`S4_NON_TRADITIONAL.md`; owner accepted S412-D1, D2, D3, D5, D6). **S4.12b DONE 2026-10-19** (TPA-R; owner decided S412-D4, option (a)). *[2026-10-24]* **S4.13 drafted 2026-10-19, reviewed 2026-10-20, corrected and committed 2026-10-24 (owner-authorised corrections 1–21)**; *[2026-10-28]* **S4.13 DONE** (aligned with the Renshaw record 2026-10-26; F-1 decided, option (a); accepted by the owner; §11.11) |
| S8 (Track B) | May start after G3. Developer Architecture Brief (S4 plan §I) plus DR-1 … DR-11 registered as interface items (DR-11: OpenBB Workspace as the interface reference, OB-2; *[2026-10-25]* OB-2 amended to a combined Investwiser / OpenBB Workspace reference, page-level lead `research/s8/S8_LEAD_UX_MARKET_FIND_ANALYSIS_2026-10-25.md`); G8a not held |
| S6 | Not started as a stage; **data-source lead recorded early** (2026-10-08); OpenBB ODP v5 admitted as a data-access layer (OB-1, 2026-10-15) |
| S5, S7, S9–S18 | Not started (08_ROADMAP) |

**Recommended order** *(refreshed 2026-10-24)*:
1. **SYNC-3 reached** (S4.9 and S4.10 done): circulate the developer brief when the owner is ready.
2. *[2026-10-24]* **S4.13 owner acceptance → owner decisions F-1, Hecht fixes and the remaining bookkeeping (§6 items 10–13) → S4.14** (agentic roles; read-only reconciliation first), then Sections 3–5 (S4.15–S4.27) → **G4**. *[2026-10-25]* The Renshaw reference composite (`S4_SCORING_RENSHAW_ANG.md`) is folded into S4.15; its contracts, fixtures, data and pre-registration follow at S4.20, S4.24, S6 and S7. *[2026-10-28]* Done: S4.13 accepted, F-1 decided, bookkeeping item 13. Before S4.14: the two remaining Hecht edits (§6 item 12).
3. **Owner items in parallel** (review S4.0, S4.1, S4.2/ADR-0027 before S4.16; developer brief after S4.10): G4 review of S4.2/ADR-0027 and the binding of B-46; S8 start with the developer brief (DR-1 … DR-11, incl. the OpenBB interface reference); sandbox key rotation; papers (§6 item 7).
4. **Per step:** mathematics and the agent-readable contract are reviewed together per method; reference implementations go in `research/s4/verification/` with invariants I-1 … I-9.
5. **Discipline:**
   - no architecture expansion without a genuine contradiction;
   - every upload gets a fit verdict;
   - nothing is adopted because ANG, a paper, code or a suggestion contains it;
   - S4 gets more selective, not larger.

---

## 6. Open owner decisions (consolidated)

| # | Decision | Recommendation | Where |
|---|---|---|---|
| 0 | **S4.2 review:** accept `S4_ANG_ADAPTATION.md`; accept, amend or defer **ADR-0027** (governed learning; no auto-culling; one authoritative risk model per problem (r3, Option A, decided by the owner 2026-10-08); runtime diagnostics; declared units). *[2026-10-28]* At the review also: add the return basis (excess or total) to D5's declared units (F-1); confirm that PC-A5's long-horizon problem is P-STRAT (S4.13 F-8). Review before S4.16, the first step that consumes the risk-object IDs | Accept ADR-0027 at G4 or earlier | S4.2 |
| 1 | **S8 start:** circulate the Developer Architecture Brief (S4 plan §I) with DR-1 … DR-11 as interface-only items | After the push | S4 plan §H–§I |
| 2 | **Sandbox keys:** regenerate/revoke the EODHD and Tiingo keys | Do (owner action) | sandbox D7 |
| 2b | **Data access (owner, when S6 starts):** free FRED, OpenFIGI and Tiingo keys; whether to take EODHD All World (+ fundamentals); whether the university licence (Bloomberg / FactSet / I/B/E/S) allows personal research use for validation | Decide at S6; nothing needed now | S6 lead §7–§8 |
| 3 | **Papers to supply** (§5 step 4) | — | S4.0 checklist |
| 4 | *[superseded 2026-10-25 by REN-D2: Renshaw definitions; Sørensen V0 kept as oracle]* **Sørensen production default:** V0 (exact) vs V1 (corrected) | V1 as a pre-registered candidate; V0 kept as the oracle; decide at G9 or earlier | S4_SCORING_SORENSEN §4 |
| 5 | **G4 binding of B-46** (engine-level risk target, S47-D6): record by ADR at G4 together with the S4.2 adaptation review | Bind at G4 | `S4_ANG_ADAPTATION.md` B-46 |
| 7 | **Papers:** Levine & Pedersen 2016 (open); Ehsani & Linnainmaa *JF* 2022 (newer than the NBER version in hand; EL-1) | Supply when convenient; not blocking | `S4_0_SOURCE_INVENTORY.md` §16 |
| 9 | **Optional papers (S4.12a):** R&U 2002 (discrete distributions; RU-2 verified numerically); Sortino & Price 1994 (the Sortino ratio); Boudt, Peterson & Croux 2008 (modified ES) | Not blocking | `S4_0_SOURCE_INVENTORY.md` §19 |
| 10 | *[2026-10-24; **accepted 2026-10-28**, scope: the inventory; ADR-0027 stays PROPOSED]* **S4.13 acceptance.** Corrections 1–21 and the MEASURE kind were authorised and applied on 2026-10-24 and committed (§11.4) | Accept the corrected inventory; F-1 stays open (item 11) | `S4_RISK_DEPENDENCIES.md` §10 |
| 11 | *[2026-10-21; **decided 2026-10-28: option (a)**; dated notes on S412-D6, EQ-SCN-1 and R-3]* **F-1 scenario return basis** (clarify S412-D6 / EQ-SCN-1) | Option (a): zero-location excess-return scenarios for μ-free methods (D1 V0, D3); every μ-consuming method declares its basis. Evidence supports (a); not yet decided | §11.3 |
| 12 | *[2026-10-21]* **Hecht (2014) record fixes:** S4.12b §9.8 wording; source-inventory entry; Cavaglia citation issue. *[2026-10-28]* The source-inventory entry is done (§24, with the bookkeeping); the §9.8 wording and CHS-1 remain | Approve the two remaining edits | §11.2 |
| 13 | *[2026-10-24; **done 2026-10-28**]* **Remaining bookkeeping after S4.13:** outline tracker; source inventory (Wang, Chen & Wu 2025; Hecht 2014); RQ-14 note; CHANGELOG; Option D as dated notes on S4_PLAN S4.16 and S4.18. Done on 2026-10-24: S4_PLAN C.2 row, verification README (31 scripts), this handoff | Approve; can follow in a later commit | §11.4 |
| 14 | *[2026-10-21]* **Admission route for internally discovered signals** (E-3; ADR-0025's "primary source" criterion is undefined for them) | Owner decision at S4.21/G4; not recorded here until then | §11.1 |
| 15 | *[2026-10-24]* **Chief Total Portfolio Agent alongside the CIO? Decided 2026-10-24: Option D.** No new agent; the CIO's total-portfolio responsibility goes into its Agent Mandate (S4.18/S4.20); S4.16 adds a deterministic total-portfolio evidence packet (the CRO diagnostic contract and the funding report applied to the CIO's final ensemble and current holdings) | Recorded as dated notes on S4_PLAN S4.16/S4.18 (2026-10-28); already handed forward in `S4_RISK_DEPENDENCIES.md` §8 | §11.8 |
| 16 | *[2026-10-24]* **Historical means combined with momentum as expected returns? Closed 2026-10-24:** the owner kept the current design; nothing is recorded | — | §11.8 |
| 17 | *[2026-10-25; **decided**: REN-D3: R-1 refined; EQ-MAP-5 (V0) and EQ-MAP-3 (V1)]* **Scores in the optimiser.** The reference construction maximises exposure to the composite score under a tracking-error budget, which is active mean–variance with alpha proportional to the score; rule R-1 (S4.9) bars unscaled scores from μ-consuming methods | Owner discussion | §11.9 |
| 18 | *[2026-10-25; **decided**: REN-D2: Renshaw replaces Sørensen definitions; Sørensen kept as display transform, oracle and standalone SIG-1]* **Renshaw versus Sørensen:** separate reference specifications for single-factor scores and the multifactor composite, or Renshaw replaces Sørensen | Owner discussion | §11.9 |
| 19 | *[2026-10-25; **decided**: REN-D5: research lane, shadow mode, embargo mandatory]* **Enabling the timing models** (research lane; shadow mode until S7 evidence) | Owner discussion | §11.9 |
| 20 | *[2026-10-25; **decided**: REN-D6: analyst revisions missing until a licensable dated source; FMP to check; data map in the record §9]* **Data sources** for analyst revisions, short interest and hedge-fund holdings; public proxy series for the timing models | S6 (owner: internet sources may be used) | §11.9 |
| 21 | *[2026-10-25; **decided**: P6]* **Security-sleeve review:** the host class's AC/CMA reviews its security sleeve; no new agent | Set the mandate fields (F4–F7) at S4.18/S4.20 | `S4_ACCOUNTABILITY.md` §2 |
| 22 | *[2026-10-25]* **`S3_FINDINGS.md` line 48** (STABLE, accepted at G3) still summarises ASK holdings as "EEA-listed shares". The registry record is corrected (`@2`), but an accepted document is annotated only by ADR | Leave it unchanged, or annotate it at the next registry ADR. The registry record governs | §11.10 |
| 23 | *[2026-10-25]* **Review of the S8 UX lead** (`research/s8/S8_LEAD_UX_MARKET_FIND_ANALYSIS_2026-10-25.md`) before it goes to the developer with the brief (item 1) | Owner review; then circulate with DR-1 … DR-11 | §11.10 |

**Resolved on 2026-10-28:** S4.13 accepted (scope: the inventory; ADR-0027 stays PROPOSED; items handed forward stay open); the Renshaw alignment and five source corrections (2026-10-26); F-1 = option (a) ("demeaned" = each asset's excess return minus its own mean, centred on zero, cash rate not added back; μ-consuming methods declare their basis at S4.20); return basis and F-8 added to the ADR-0027 review; bookkeeping item 13; push of `828e0e7`, `22b384c` and the bookkeeping commit.

**Resolved on 2026-10-25 (momentum and interface review):** momentum and interface review: P1 (Renshaw factor rows, trend-state column, Sørensen 12–1 in the drill-down), P2 (T-9 vocabulary), P3 (T-1 clarified; T-7 revised: red/green allowed as presentation only, never an agent or analysis input), P4 not needed (owner: Investwiser's FAQ previously confirmed EODHD), P5 (ASK claim wording, new fact version), P6 (security-sleeve review in the AC/CMA mandate), P7 (RQ-20 candidate S14 template); OB-2 amended to a combined Investwiser / OpenBB Workspace reference; Investwiser's AI assistant disregarded.

**Resolved on 2026-10-25 (later):** REN-D1 … REN-D7 (reference specification recorded; Renshaw replaces Sørensen definitions; R-1 refined with EQ-MAP-5; factor momentum follows the source; timing models in shadow mode; analyst revisions missing until a licensable dated source; EBIT/EV a cyclical-value test variant); download of Eisfeldt, Kim & Papanikolaou (NBER) with owner permission.

**Resolved on 2026-10-25:** Renshaw et al. (2026) designated the reference specification for the multifactor composite (construction only; FinSol's own universe and datasets); factor-momentum timing follows the source; RQ-28, RQ-31 and RQ-32 corrected; the August whitepaper and the iSTOXX methodology guide downloaded with owner permission.

**Resolved on 2026-10-24:** the S4.13 correction plan (corrections 1–21; candidate kind MEASURE; one commit with the minimum bookkeeping, pushed); Option D for the total-portfolio question (item 15); historical means with momentum closed, current design kept (item 16); the handoff publication (`61792e4`).

**Resolved on 2026-10-19 (methodological review, E-1 … E-8):** E-1, E-2, E-6 and E-7 withdrawn as covered by existing governance; E-4, E-5 and E-8 recorded as discussion notes or source leads (`a9a2689`); E-3 held for an owner decision at S4.21/G4 (§11.1).

**Resolved on 2026-10-19 (S4.12b done):** S412-D4 option (a): TPA-R (V1) as the family-D candidate, plus the funding report (β, α, AR against `POL.benchmark`) on every candidate card. The three TPA papers were supplied and read (`S4_NON_TRADITIONAL.md` §9.8).

**Resolved on 2026-10-18 (S4.12a done):** S412-D1, D2, D3, D5, D6 accepted, option (a) in each (D1 after the owner asked how (a) differs from (b); D6 with the owner's question on historical means answered: S9 is the only source of μ).

**Resolved on 2026-10-18 (S4.11 done):** S411-D1 … D5 accepted as recommended; push of `9d4eddb` and the decision commit (owner authorisation).

**Resolved on 2026-10-18 (later):** RQ-18 discussion record (one target across accounts, asset location, cross-account rebalancing); push of `2972c46`, `562e10d`, `3c27e0a` and the RQ-18 commit (owner authorisation).

**Resolved on 2026-10-18 (S4.10 done):** S410-D1 … D6 accepted as recommended; S47-D3 closed (admissible anchors 1/N, 1/σ, market capitalisation, `POL.benchmark`; default `POL.benchmark` where feasible, else 1/σ; securities by market capitalisation). Owner pushback on 60/40: with an ASK and an ordinary account (AF), 60/40 is feasible for the combined holdings while the AF holds ≥ 40% of the wealth (EQ-FEAS-1; 07 §2 places benchmark and allocation policy at portfolio level).

**Resolved on 2026-10-18 (S4.9 done):** S49-D2 (= S48-D3; momentum sleeves under R-7, with the exception that zero-investment long–short sleeves may be units of their own where shorting is permitted; base case without sleeve-level scaling; constant volatility a variant; DM dynamic weight a timing model at S13c) and S49-D5 (composition rules for V/V1, typed at S4.20, fixed per run and never agent-selectable, duplicate detection at S4.16, research-lane constructions excluded).

**Resolved on 2026-10-18 (S4.9 review):** S49-D1 (V/V1 admissible; M once an S9d mapping is accepted; the seven tested-but-unsourced constructions to the research lane, ADR-0024 §1; C5 × O2 and D3 × O2 tested at S4.11/S4.12; owner: "Put all seven in research lane"), S49-D3 (direction rules after the engine-level scaling; binds at G4 with B-46), S49-D4 (register EQ-MAP-1 … 4; choose at S9d); the S4.9 revision (EPO consumes expected returns; R-7; Grinold-based EQ-MAP-3; EQ-TC-1); RQ-28: "EP" means economic profit, E/P is the earnings–price ratio; push of `e32458a` … `86c1ace` and the revision commit.

**Resolved on 2026-10-15 (S4.8):** S48-D1 (both signals in every domain; skip by asset type: single stocks 12–1, index ETFs/futures/asset classes 12–0; sign and magnitude variants), S48-D2 (MOP EWMA as oracle; production σ from S10; daily or 2–5-day returns by microstructure), S48-D4 (rank-based score), S48-D5 (causal filters; grid at S7), S48-D6 (residual momentum readings; factor momentum for long-only users as time-varying blend weights or factor-ETF rotation, signals on long–short or active returns); S48-D3 deferred to S4.9. RQ-32 corrected (composite-score weights, not portfolio weights). **Universe (owner instruction, RQ-07):** Norwegian equities, US and global equities, ETFs; allocation unit both.

**Resolved on 2026-10-15 (later):** S4.8 scope accepted (S4_PLAN amendment 19); `2135803` pushed; discussion findings recorded as dated notes on RQ-09, RQ-11, RQ-14, RQ-15, RQ-16, RQ-28, RQ-31, RQ-32, RQ-33, RQ-35.

**Resolved on 2026-10-15:** S47-D7 (Michaud patent family closed; generic names; implementation from the mathematics; components as candidates); Paleologo registration with PAL-1 … PAL-8 and a verification script; start S4.8 once the papers are in; OB-1 (OpenBB ODP v5 as a data-access layer, provider licences governing) and OB-2 (OpenBB Workspace layout and design as the interface reference for S8).

**Resolved on 2026-10-08 (S4.7, part 2):** S47-D2 parameters (EPO on the authoritative risk model, θ = 0; 11-point logit-spaced grid with a switching margin at S7) and S47-D6 (one engine-level risk target and leverage rule, applied per method type: return-based methods along their frontier, others scaled, PC-A5 and absolute-risk-limited methods internally, ensemble rescaled; EQ-SPLIT-1; adaptation B-46).

**Resolved on 2026-10-08 (S4.7):** S47-D1 (follow BL 1992), S47-D2 rule (endogenous w, past-only best trailing Sharpe), S47-D3 (anchor deferred to S4.10; remind the owner first), S47-D4 (G&I robust maximum Sharpe), S47-D5 (resampled frontier as recommended; **D-2 closed for PC-B4**: core patent US 6,003,018 expired 2018-09-09 per Google Patents). Owner note: the engine allows both long-only and long/short portfolios according to user preferences and abilities.

**Resolved on 2026-10-08 (S4.6):** S46-D1 decided: numéraire cash is the riskless asset; the risk-free rate is the after-tax rate on uninvested cash at the best liquid deposit available to the user, otherwise the broker's cash rate; cash location is an implementation decision (S13); borrowing at a separate rate only if permitted. The BSU / household-advice idea is ON HOLD (RQ-57). Open for S4.7: engine-level vs per-method cash/risky split.

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
| **FITS** | *[2026-10-21]* **Hecht (2014)**, "Evaluating Hedge Funds – Alphas, Sharpe Ratios & the Underappreciated Appraisal Ratio" (Evanston Capital Management; hedgefundinsight.org, 18 Dec 2014; read in full): secondary practitioner source, no new mathematics (§11.2). **Ledoit & Wolf 2003** (*JEF* 10:603–621) and **2004** (*JMVA* 88:365–411): abstracts and the shrinkage-intensity lemmas checked (S4.13 review). **Grinold, *Advances* ch. 32 p. 671:** eq. (10) is a total-return scenario (§11.3). *[2026-10-19]* **Cavaglia, Han & Seshadri 2026** (appraisal ratio against a reference portfolio: supports the funding-report lens; their single-candidate weight is Treynor & Black's one-asset case, verified). *[2026-10-18]* S4.12 governing sources, reproduced: **Rockafellar & Uryasev 2000**; **Chekhlov, Uryasev & Zabarankin 2005**; **Boudt, Carl & Peterson 2013**; **Sortino & van der Meer 1991** with Markowitz, Todd, Xu & Yamane 1993; **Cesarone et al. 2026**; Grinold & Kahn *Advances* ch. 27 (Kahn & Stefek) and ch. 32 (Grinold); **Treynor & Black 1973**. **Roll 1992** (tracking-error optimisation; ROLL-1 sign slip only); **Jorion 2003** (total-risk constraint; Tables 1–3 reproduced). **Grinold 1994** (alpha = volatility × IC × score; GRI-1, GRI-2 rounding only); **Grinold & Kahn, *Advances in Active Portfolio Management*** (governing version of the forecasting rule and the fundamental law with the transfer coefficient; ch. 9 for S9d); **Clarke, de Silva & Thorley 2002** (transfer coefficient; long-only TC ≈ 0.58). *[2026-10-15]* **Paleologo 2025** (ch. 2, 5, 6; textbook, secondary for the original papers; PAL-1 … PAL-8); **Michaud & Michaud 2008** (read in full; resampling family free of patents, S47-D7); **OpenBB ODP v5** (data-access layer, OB-1) and **OpenBB Workspace** (interface reference, OB-2). ANG v2 (architecture only); Sharpe 1981 (narrow: diversification of judgement); Sensoy 2009 (narrow: controls set in advance); Perold 1988 (shortfall identity); Perold & Sharpe 1988 (rebalancing rule reflects risk tolerance); Nordnet price list 2026-10-07 (facts); **Norges Bank Datatorg** (NOK FX and rates; keyless; attribution); public macro and factor sources (FRED, SSB, ECB, French, AQR, Shiller, Damodaran; S6 lead); **Gao, Jiang & Yan 2026 v2** + procedure file (contamination test); **Didisheim, Fraschini & Somoza 2025** (memorisation; q-trimming; rewording dispersion); **Sørensen 2026 / Storebrand 2025** (secondary; owner-designated reference scoring specification) |
| **PARTIAL** | *[2026-10-19]* **Gilmore & Simonian 2025** (TPA as a framework; their multi-objective candidate would duplicate the CIO and lacks stated objectives and weights); **Elkamhi & Lee 2025** (TPA as a mindset; guardrails map to Policy Statement bounds; no method). *[2026-10-18]* Gallego, Columbia IEOR4706 Lecture 7 (2000; secondary teaching note on Grinold & Kahn; LEC-1). Q Group lecture Oct 2026 (secondary; learning design, candidate cards, skills, verifiability); BCD 2022 (accountability); **ABD 2014** (funding/benchmarking TPA; rebalancing rule upstream; implementation leeway; verification horizons); **AQR 2026** (TPA weight mechanics per D-5; assumes leverage/shorting); van Binsbergen–Brandt–Koijen 2008; Jegadeesh 1990 and Lehmann 1990 (individual-stock reversal only); Glasserman & Lin 2023 (named vs anonymised only; see §4.7); **Henning et al. 2025 v3** (same-model homogeneity; forecast-rationality battery); **Liang 2026** (pre/post-cutoff magnitudes; weak identification); correlated-error literature (Kim et al. 2025; Kleinberg & Raghavan 2021; Panickssery et al. 2024; Liang et al. 2024); **third-party GitHub code** (patterns and verified pieces only); ML specification (candidates only); z-score screenshot (lead) |
| **DOES NOT FIT** | **Simply Wall St** (S&P Capital IQ data; personal use, no retransmission), **Seeking Alpha** (S&P + Quodd data; no redistribution) and **Investwiser** (EODHD data; personal use) as data sources (peer references only); **S&P Capital IQ** for a distributed engine (enterprise; owner-only validation via university at most); Yahoo/yfinance; Nordnet External API (closed to new subscribers); Tinbergen; Grinold (not needed at the time; superseded 2026-10-18, see FITS); misidentified uploads (Jones & Wermers 2011; NBIM news page); Altbridge benchmark; podcast; news items (illustration only) |

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
| Mean-reverting variance state (Paleologo ch. 2, corrected) | The optimal linear filter is the GARCH(1,1) recursion (α = aK, β = a(1−K), α + β = a), not plain EWMA; the printed recursion has 4–16% higher prediction error (PAL-1) | `s48_kalman_ewma_paleologo.py` |
| Momentum sleeve as a separate unit beside its host class (S4.9, R-7) | 1/N: equity weight 0.33 → 0.50; ERC: equity risk share 0.33 → 0.50; unchanged when the sleeve is a tilt inside the class; sleeve beta 1.09 from its history vs 1.50 from its holdings | `s49_double_counting_dcells.py` |
| Transfer coefficient (S4.9, EQ-TC-1) | Sign-only 0.80; long-only at 5% tracking error 0.53–0.58; momentum screen + 1/N, 1/σ or ERC ≈ 0.48, + GMV, HRP, MDP or min-CVaR 0.18–0.26 | `s49_alpha_sources.py`, `s49_double_counting_dcells.py` |
| Momentum alphas without Grinold's volatility step (EQ-MAP-3) | Implied per-asset skill dispersion 2.3× higher in the most volatile third; \|past return\| correlates with volatility at the proportional benchmark (0.40 vs 0.40) | `s49_alpha_sources.py` |
| Risk-structured methods under special structures (S4.11) | Uncorrelated: GMV = HRP = 1/σ², ERC = MDP = 1/σ; constant correlation: ERC = MDP = 1/σ; equal vols: MDP = GMV; σ_GMV ≤ σ_ERC ≤ σ_1/N | `s411_risk_structured.py` |
| Scenario location in min-CVaR (S4.12a, NT-1; R&U data, β = 0.95) | Weight gap to GMV 1.9 / 3.2 / 6.2 / 10.6 / 14.0 pp at 1 / 3 / 12 / 36 / 60 months; demeaned scenarios → GMV | `s412_cvar_ru.py` |
| Drawdown definitions (S4.12a, CDD-1, CDD-3) | Choppy path: CUZ absolute 20% vs relative compounded 63%; trend decline the reverse; the relative MaxDD limit is convex and binds exactly; CUZ at γ = 15% gives 14.52% relative | `s412_drawdown_tail.py` |
| Tail-risk parity (S4.12a, BCP-4, BCP-5) | No long-only ERC-CVaR if an asset has μ ≥ c₂σ (cash in total-return CVaR); modified CVaR errs +6% to +12% at 5% and up to +86% at 2.5% under fat tails, not monotone in the tail level | `s412_drawdown_tail.py` |
| Normal limits of the scenario and downside methods (S4.12a) | Min-CVaR (demeaned) = GMV; ERC-CVaR (demeaned Gaussian) = ERC; max Sortino (MAR = cash rate) = max Sharpe; mean–target-semivariance frontier = MV frontier | `s412_*` |
| Total-risk constraint on a tracking-error portfolio (Jorion 2003 Table 2; S4.10) | At 4% TEV, Δ₁ = 2%, σ_MV = 8%: −0.29 pp return for −1.65 pp risk (ratio 0.18 vs IR 0.5) | `s410_anchor_benchmark.py` |
| 60/40 anchor in an ASK (S4.10) | Not holdable (bond and high-yield funds < 80% shares); projections: renormalised 15.8% vol vs 10.0%; bonds → cash 9.5%; household feasible only if bond-capable accounts hold ≥ 40% of wealth | `s410_anchor_benchmark.py` |
| Direction rule vs engine-level scaling (S4.9, R-4) | 2 of 10 assets in uptrend: exposure 0.19 if the trend rule follows the scaling, 0.69 if it precedes it (re-levering) | `s49_signal_pc_compatibility.py` |
| Residual momentum (BHM 2011) on synthetic data with a trending market | Correlation of the score with market beta: total momentum 0.65, residual momentum −0.02 | `s48_momentum_constructions.py` |
| DM optimal momentum weight μ/σ² vs the exact unconditional-Sharpe maximiser μ/(σ² + μ²) | Relative Sharpe gap 0.13% at monthly scale; 18% when μ is six times larger (DM-1) | `s48_momentum_constructions.py` |
| MOP ex-ante volatility | Centre of mass 60 days = half-life 41.9 days = e-folding 61 days | `s48_momentum_constructions.py` |
| Printed MSE volatility loss (Paleologo ch. 5) | Minimised at σ̂² = √3·h under normality, so not robust; use Σ(r² − σ̂²)² and QLIKE (PAL-6) | `s48_kalman_ewma_paleologo.py` |
| HRP (López de Prado 2016) | Exhibit 7 reproduced exactly; the published algorithm is order-dependent (weights changed in 127/200 random reorderings; up to 52% of the portfolio); the tree-split variant is invariant | Source reviews §4 |
| TPA (S4.12b; TB-1, TPA-2) | Squared ratios add: SR²(reference + active) = SR²(reference) + AR², and long-only halves the squared ratio (T&B p. 78). The funding set changes the alpha: an absolute-return asset's alpha is 2.0% with cash in the funding set and 0.05% with stocks and bonds only. TPA-R is distinct at TE 3% (max \|Δw\| 0.21–0.44 against B1, B1 + TE, Roll and Anchored EPO) and equals the tangency portfolio only unconstrained, cash-funded, with a factor-efficient reference | `s412b_tpa.py` |
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
| Paleologo (2025) EPUB | `~/Desktop/The Elements of Quantitative Investing.epub.zip` |

---

## 10. Developer guide: building the engine from scratch

*Written 2026-10-18 at the owner's request. It summarises; the documents it points to govern (01 §2). Everything below that is not an `ACCEPTED` ADR or a `STABLE` document is design input, not a build instruction.*

### 10.1 What is binding today

| Status | What | Build against it? |
|---|---|---|
| **ACCEPTED ADRs** | ADR-0001 … ADR-0026 (`decisions/README.md`) | **Yes** |
| **PROPOSED ADR** | ADR-0027 (governed learning L-1 … L-7; no auto-culling; one authoritative risk model per problem; runtime diagnostics; declared units). Owner review at G4 or earlier | Interfaces only |
| **STABLE documents** | 00–10 (open parts marked inside); `research/S1_INPUT_SPECIFICATION.md`, `S2_CONFIGURATION_MACHINERY.md`, `S2_G2_DECISIONS.md`, `S3_REGISTRY_ARCHITECTURE.md`, `S3_FINDINGS.md`, `S3_G3_PACKAGE.md`; the S1–S3 synthetic fixtures; `facts/` (registry v1, accepted at G3) | **Yes** |
| **S4 documents** (`research/s4/`) | DRAFT or REVIEWED; owner decisions recorded per step; nothing is a Method Library baseline until G4 (library manifest v1) | Interfaces and stubs only (ADR-0022 §4); reference implementations are oracles |
| **S6 lead** | `research/s6/S6_LEAD_DATA_SOURCES_2026-10-08.md` (DRAFT); OB-1, OB-2 owner decisions | Design input for data adapters and the UI reference |
| **Legacy** | Repository-root `SPECIFICATION.md`, `MATHEMATICAL_APPENDIX.md`, everything in `ENGINE_V1/` | **Never** (ADR-0001; 09) |

If a build step needs a choice no accepted decision covers, raise a spec question; never decide methodology in code (README; ADR-0022 §3–§5).

### 10.2 Repository, branches and what stays outside

- **Repository:** `Tibbitazz/finsolution`. `main` = `dcce874` (G3). S4 work is on `stage/s04-method-library` (pushed; no PR until G4). Gate workflow: stage branch → gate PR → owner merges → tag `gate-GNN` (ADR-0002).
- **Never in the repository:**
  - personal data: the local user layer lives in git-ignored `finsolution/local/` (ADR-0014; `.gitignore` excludes `/local/`, `*.local.*`);
  - credentials and vendor keys: user-supplied, stored only in the local layer, never in logs or run manifests (DR-7);
  - the owner's UI concept prototype and the ANG sandbox (`ENGINE_V1/ang_sandbox`), which never touch the repository.
- **Development and tests use synthetic data only** (ADR-0022 §4; S1–S3 fixtures).
- **Third-party code** is never executed without isolation; reusable pieces are ported and verified (`S4_GITHUB_IMPL_REVIEW.md` §10–§11).

### 10.3 Reading path for a developer (minimum)

1. `README.md` → `00_CHARTER.md` → `01_SOURCE_OF_TRUTH_AND_WORKFLOW.md` → `02_EVIDENCE_AND_STATUS.md`.
2. `04_REPRODUCIBILITY.md` (run manifest, two reproducibility classes, validation standard) and `05_DETERMINISTIC_VS_AGENT.md` (layer assignment; rules R1–R8).
3. `06_MODEL_ELIGIBILITY_GOVERNANCE.md` (Feasible → Eligible → Admissible → Deliberable; ADR-0025 redefines Admissible) and `07_POLICY_STATEMENT_GOVERNANCE.md` (hierarchy Investor → Goal/Portfolio → Account; precedence).
4. `08_ROADMAP.md` (two tracks; what each gate delivers to Track B) and `10_SCOPE_EXCLUSIONS.md`.
5. The platform ADRs: 0004 (layers), 0006 (configuration hierarchy and registries), 0014 (reusable engine, local user layer, data classes, value origins), 0015 (configuration machinery), 0016 (interaction taxonomy), 0017 (authority model), 0019 (external-fact registry), 0022 (parallel track), 0023 (ANG baseline), 0024 (method governance), 0025 (admission ≠ evaluation), 0026 (mandates and decision chain).
6. The STABLE S1–S3 specifications and `facts/`.
7. For the investment process: `S4_ANG_BASELINE.md` (the pipeline), `S4_ANG_ADAPTATION.md` §5 (**SYNC-1 developer summary**), `S4_TAXONOMY.md` §1 and §14 (**SYNC-2**: six kinds and registries), `S4_SIGNAL_PC_COMPATIBILITY.md` and `S4_ANCHOR_BENCHMARK.md` (**SYNC-3**), `S4_ACCOUNTABILITY.md`, `S4_GITHUB_IMPL_REVIEW.md` §10 (invariants I-1 … I-9), `S4_EQUATION_REGISTER.md` and `verification/README.md`.

### 10.4 What the engine is (accepted architecture)

**Purpose (00 §1–§2):** a personal agentic investment engine that runs locally on a server with a browser interface, is governed by an interactive Policy Statement, and takes the investor from preferences and research evidence through data and signals, risk, portfolio construction, multi-agent deliberation and a target portfolio to implementation decisions, a pre-trade investment-case report, monitoring, rebalancing and controlled improvement. Reusable by several local users with private profiles (ADR-0014), tax-resident initially in Norway; brokers Nordnet and eToro, neither preferred (ADR-0007); one or more accounts with continuous capital; pension products and wealth tax out of scope (ADR-0020, ADR-0021). The specification must be precise enough that the developer makes no undocumented financial or methodological assumption.

**Layers (05 §2; ADR-0004).** Deterministic code computes; agents interpret within bounds; humans approve:

| Layer | Code | Agent | Human |
|---|---|---|---|
| 0 Governance (Policy Statement) / 0b Registries | Validation, feasibility, storage, staleness | Draft/explain; never sets values | Writes, approves |
| 1 Data · 2 Universe · 2b Method Library and Feasibility Engine | All | — (text extraction only, flagged) | Preferences, thresholds |
| 3 Beliefs · 4 Risk · 5 Portfolio construction | All estimates and optimisers | Bounded judgement where admitted (RQ-12); narrative | — |
| 6 Deliberation · 7 Decision and investment case | Metrics, tallies, ensembles, compliance | Critique, vote, bounded selection, report narrative | Approves |
| 8 Implementation · 9 Monitoring · 10 Learning | Costs, taxes, FX, sizing, trade lists, checks, forecast evaluation | Explanation; implementation discretion within an Agent Mandate (ADR-0026) | Executes (until S13 safeguards); approves changes |

**Rules every component obeys (05):** R1 no LLM-produced number enters a calculation (except a logged bounded choice among code-computed candidates); R2 every agent decision point has a deterministic fallback, and the whole pipeline runs in **deterministic-only mode**; R3 hard constraints are deterministic predicates checked after every agent step; R4 Policy Statement, compliance, approvals, eligibility and registries are read-only to agents; R5 agents see only the deliberable method set; R6 beliefs ⊥ preferences; R7 every agent output archived with inputs and model identifiers; R8 every number in agent narrative cites a deterministic descriptor.

**Investment process (ADR-0023, the ANG baseline):** Policy Statement → macro → asset-class/CMA agents → risk (one authoritative model per problem, ADR-0027 D3, proposed) → **parallel PC proposals** (roster v0 = 23 methods) → CRO (neutral risk reports; enforces hard constraints) → peer review, vote, revision → CIO (bounded choice among code-computed ensembles) → investment-case report → investor approval → rebalancing determination → hybrid Trader (when and how, within mandate) → execution (ADR-0026). Never collapse PC → CRO → deliberation → CIO into one optimiser (ADR-0023). Role ≠ runtime; Method ≠ Agent.

**Objects (S4_TAXONOMY, SYNC-2):** six kinds, each with its own registry: Method (Method Library; dual contracts), Artefact (content-addressed store), Role (mandates, skill versions, memory states), Control (Policy Statement items, limits, benchmarks; effective-dated), Record (append-only: Decision, Forecast, Outcome, Change Proposal), Input (point-in-time snapshots).

**Configuration (S1, S2; ADR-0014/0015/0016/0017):** immutable content-addressed objects with `id@version`; typed values with unit, basis and period; Declared Policy Statement never modified, Effective derived by the resolution algorithm with conflict records; dependency graph with input-version cache keys; schema evolution by appending versions; authority grants in eight dimensions (dimensions 6–8, staging, submitting and unattended execution, are schema capabilities only until S13 safeguards exist).

**Facts (ADR-0019; S3):** bitemporal point-in-time facts (`Fact(t | k)`), two status axes, admissibility layers legal ∩ wrapper ∩ broker ∩ methodological ∩ user, unknown ≠ unsupported, staleness re-check policy.

**Reproducibility (04):** every run writes a manifest (data snapshot, facts snapshot, Policy Statement version, spec commit, code commit, Method Library version, eligibility hash, LLM provider/model/version/parameters/prompt hashes, seeds, environment lockfile); its hash is the run ID; cache keys include the code commit. Deterministic layer bit-identical on one environment; agentic layer archived and replayable.

### 10.5 Build order (Track B, ADR-0022; S4_PLAN §H–§I; 08 S18)

1. **S8a, now:** circulate the Developer Architecture Brief (S4_PLAN §I) with interface items DR-1 … DR-11 → developer feedback → architecture alternatives → owner decisions → **G8a** (architecture, stack, data boundaries, change control). Not yet done.
2. **Foundation slice (after G8a; 08 S18 "first slice"):** Policy Statement editor (S1 fields, S2 validation and Declared → Effective resolution, conflict records); registries (facts v1, point-in-time queries, staleness); Feasibility Engine with exclusion report (06; ADR-0019 admissibility layers); one deterministic path to a report (deterministic-only mode); run manifest and replay (04); local user layer and privacy boundary (ADR-0014); authority grants (ADR-0017). From the first slice also: learning capture (Forecast/Outcome Records, DR-2), mode stamp (DR-5), as-of gate with a look-ahead test (DR-1), model provenance on agent outputs (DR-9).
3. **Progressive contracts by sync point:**

| Sync | Track A delivers | Track B builds | State |
|---|---|---|---|
| SYNC-1 | Pipeline, roles, authority boundaries, mandates, Decision Records (interfaces) | Module boundaries and orchestration; roles separable | Delivered (S4.1–S4.2b; S4.2/ADR-0027 await owner review) |
| SYNC-2 | Six kinds, type catalogue, relations, identity rules | Registries and plugin categories | Delivered (S4.3 reviewed) |
| SYNC-3 | Signal → belief → PC relationships; anchor and benchmark objects | Data flows; anchor/benchmark entities; account and household feasibility | **Delivered 2026-10-18** (S4.9, S4.10 done) |
| SYNC-4 | PC → CRO → deliberation → CIO information flow (S4.16–S4.18) | Evidence-packet storage, review records, run structure | Pending |
| SYNC-5 | Typed Method Contracts, schema, reference oracles, mandate schema (S4.20) | The real Method Registry and method host | Pending |
| SYNC-6 | Accepted Method Library baseline v1 (G4) | Methods behind contracts | Pending |

4. **After G4, gate by gate:** G5/G6 → universe, instrument and data contracts (S5, S6); G7 → evaluation harness (pre-registered protocol); G9–G12 → belief, risk, construction and aggregation modules; G13 → cost, tax, FX, rebalancing, tactical and execution modules; G14 → report and approval UI; S15 validation; S16 monitoring; S17 learning; S18 final handoff.

### 10.6 Interface and data

- **UI reference (OB-2, DR-11):** the OpenBB Workspace layout and design: dashboards of widgets, apps, an AI copilot and agents on the same data, a connect-your-own-backend model (local API, MCP). Reference only; no OpenBB branding. *[2026-10-25, OB-2 amended]* Combined reference: OpenBB Workspace for the shell; Investwiser as UX inspiration for the page layout of Market, Find Investments and Analysis, adapted and never copied. Read `research/s8/S8_LEAD_UX_MARKET_FIND_ANALYSIS_2026-10-25.md`; it overrides nothing in the score-table rules (T-1 … T-9).
- **Data access (OB-1):** OpenBB ODP v5 (Apache-2.0; pinned; never the AGPL v4 or earlier) may be wrapped behind our own data-access adapters; each provider's licence governs (DR-7, CB-19). Installing or running it needs owner permission per item.
- **Identity and credentials (DR-7):** ISIN/FIGI identity with vendor symbology mapped; user-supplied keys only in the local layer; licence class and provenance stamp per datum; no cross-user sharing.
- **Cost model (DR-8; CB-17, CB-18):** account price class and currency-account flags; FX conversion flows.
- **Accounts:** one target portfolio at portfolio level, placed across accounts by asset location (07 §2; S13a). Feasibility of a target, anchor or benchmark across accounts is a transportation check (EQ-FEAS-1). ASK eligibility comes from the registry (`no.wrapper.ask.eligible_holdings`).

### 10.7 Method Library status (S4; specification decided by the owner, not yet admitted)

| Group | Methods | Record | Equations | Oracle scripts | Decisions |
|---|---|---|---|---|---|
| A heuristics | 1/N, market cap, 1/σ, 1/σ², volatility targeting | `S4_HEURISTICS.md` | EQ-H-1 … 4, EQ-H-T | `s45_*` | S45-D1 … D4 |
| MVO foundation | problem, closed forms, riskless asset, GMV, estimation error | `S4_MVO_FOUNDATION.md` | EQ-MVO-1 … 5, E1, E2 | `s46_*` | S46-D1 |
| B MVO family | max Sharpe, Black–Litterman, robust MV, resampled frontier, simple and anchored EPO | `S4_MVO_FAMILY.md` | EQ-MVO-3b, EQ-BL, EQ-ROB, EQ-REF, EQ-EPO, **EQ-SPLIT-1** | `s47_*` | S47-D1 … D7 |
| Signals | XSMOM, TSMOM (+ residual, factor, trend-filter variants) | `S4_MOMENTUM.md` | EQ-SIG-1 … 5 | `s48_*` | S48-D1 … D6 |
| Signal × PC | objects O1–O6; rules R-1 … R-7; EQ-MAP-1 … 4 (registered for S9d); EQ-TC-1 | `S4_SIGNAL_PC_COMPATIBILITY.md` | EQ-MAP, EQ-TC-1 | `s49_*` | S49-D1 … D5 |
| Anchors, benchmarks | anchor contract; feasibility; tracking error | `S4_ANCHOR_BENCHMARK.md` | EQ-ANC-1, EQ-FEAS-1, EQ-TEV-1/2, EQ-GRS-1 | `s410_*` | S410-D1 … D6 |
| C risk-structured | GMV, ERC, HRP (tree split), MDP, MinCorr | `S4_RISK_STRUCTURED.md` | EQ-RS-1 … 5 | `s411_*`, `s44_*` | S411-D1 … D5 |
| D non-traditional | CVaR, drawdown, tail-risk parity (S4.12a done); TPA-R (S4.12b done) | `S4_NON_TRADITIONAL.md` | EQ-NT-1 … 4, EQ-SCN-1 | `s412_cvar_ru.py`, `s412_drawdown_tail.py`, `s412b_tpa.py`, `s44_cvar_budgets_bcp.py`, `s44_drawdown_cdd.py` | S412-D1, D2, D3, D6; S412-D4 (a) |
| B5 mean–downside | max Sortino / mean–target-semivariance | `S4_NON_TRADITIONAL.md` | EQ-DS-1, EQ-DS-2 | `s412_downside_b5.py` | S412-D5, D6 |
| Risk dependencies (S4.13) | Method → risk-object map; 24 candidates registered (estimators, transformations, compositions, generators, data preparation, one risk measure), none selected | `S4_RISK_DEPENDENCIES.md` (DONE, accepted 2026-10-28) | — | `s413_risk_dependencies.py` | F-1 decided 2026-10-28, option (a); return bases declared at S4.20 |
| Multifactor composite (reference) | 18 signals → cyclical value, enhanced value, momentum, quality → 1/3–1/3–1/6–1/6 score (timing in shadow mode) → maximum exposure under a tracking-error budget | `S4_SCORING_RENSHAW_ANG.md` | EQ-MAP-5 | `s4ren_multifactor_reference.py` | REN-D1 … REN-D7 |
| E agentic | Researcher (research lane), Adversarial Diversifier | S4.14 | — | — | — |

**Using the oracles:** the scripts in `research/s4/verification/` reproduce each source's published examples and assert invariants on synthetic data. They are reference implementations for testing production code (04 §3), not production code (ADR-0024 §8). Environment used: Python 3.9.6, numpy 2.0.2, scipy 1.13.1, pandas 2.3.3; run each script with `python3 <script>`; every script prints a line starting with `PASS`. The production stack is the developer's choice after G8a.

### 10.8 Cross-cutting rules the implementation must enforce

| Rule | Content | Source |
|---|---|---|
| I-1 … I-9 | numbers pass by reference; typed failure records, no silent fallback; duplicate detection by portfolio distance; one declared CMA basis; one Sharpe definition per use; missing returns never filled; invariance fixtures (e.g. permutation); revisions only within contract authority; in-sample labels | `S4_GITHUB_IMPL_REVIEW.md` §10 |
| EQ-SPLIT-1 | One engine-level risk target σ* and leverage cap; μ-free methods scaled, return-based methods along their frontier, ensemble rescaled. Notes binding at G4: direction rules act after the scaling (S49-D3); benchmark-relative candidates carry the total-risk constraint inside (S410-D6) | `S4_EQUATION_REGISTER.md`; S47-D6 |
| R-1 … R-7 | No unscaled score into any μ-consuming method (EPO included); units; μ-free methods use signals only by selection, direction (separable bases) or sleeve; direction after scaling; sleeves only where permitted; overlays never change w*; no double counting (sleeves inside the host class; look-through risk; one channel per signal) | `S4_SIGNAL_PC_COMPATIBILITY.md` §4 |
| Composition rules | V/V1 compositions are separate candidates declared before the run; never toggled by an agent | S49-D5 |
| Anchor contract | AC-1 … AC-7; no hard-coded index; benchmark only from `POL.benchmark` | S410-D1 … D5 |
| Scenario location | Scenario sets combine S10's dependence and scale with a location: zero (demeaned) for μ-free methods, S9's μ for μ-consuming ones (EQ-SCN-1); raw historical means are never the location; CVaR by the LP or quantile integral, never the naive tail mean | S412-D6; RU-2 |
| Funding report | Every candidate card carries the funding report against `POL.benchmark`: per-asset β (ABD sum-to-one funding over the reference's assets), α and appraisal ratio, with the funding set stated, since it changes the alpha (TPA-2) | S412-D4; S4.16 |
| Constraints | Methods without native constraints get Policy Statement bounds by a declared post-processing step (S4.20) with the distance moved reported | S45-D4; S411-D4 |
| Failure records | Typed reason codes (e.g. `DEGENERATE_CORRELATION`, `NOT_POSITIVE_DEFINITE`, `INFEASIBLE_CONSTRAINTS`, `CONSTRAINT_CONFLICT`) | S411-D5; I-2 |
| Admission vs evaluation | Admission needs a primary source, clear mathematics, deterministic implementability, verified reproduction, explicit inputs, a role and an accepted contract; backtests are never admission evidence | ADR-0025 |
| Research lane | Discovered or unsourced constructions run experimentally with no production CIO allocation until admitted | ADR-0024 §1; S49-D1 |
| Look-ahead | As-of gate on all agent tool and data access; clean-window rule | DR-1; `S4_LIT_LOOKAHEAD_2026-10-07.md` |

### 10.9 What not to build or decide in code

- No investment method, parameter, threshold, benchmark, anchor or index chosen in code; unresolved methodology stays behind typed interfaces (ADR-0022 §4).
- No LLM edits weights or produces numbers that enter calculations (R1; ADR-0024 §2).
- No auto-retirement of methods or agents (ADR-0027 D2, proposed).
- No execution authority beyond grants; dimensions 6–8 not grantable before S13 safeguards (ADR-0017).
- No personal data, credentials or real profiles in the repository or fixtures (ADR-0014).
- No backtest result used to admit a method (ADR-0025); runtime backtest diagnostics are labelled in-sample (ADR-0027 D4, proposed).
- No silent fallback to another method under a method's name (I-2).
- No Yahoo/yfinance or other sources whose licence does not fit (S6 lead).

### 10.10 Open items that affect the developer

| Item | Owner of the next step | Where |
|---|---|---|
| Circulate the Developer Architecture Brief; hold G8a | Owner, with the developer | S4_PLAN §I; §6 item 1 |
| ADR-0027 and the S4.2 adaptation map: review | Owner (G4 or earlier) | §6 item 0 |
| B-46 binding of EQ-SPLIT-1 with the S49-D3 and S410-D6 notes | Owner at G4 | §6 item 5 |
| *[2026-10-28: S4.13 accepted]* S4.14 – S4.27 (inventories, CRO/deliberation/CIO requirements, typed contracts, eligibility framework, verification, freeze, G4 audit) | Track A | S4_PLAN C.2 |
| S5 universe and allocation hierarchy (account vs household problems); S6 data contracts; S7 evaluation protocol | Track A after G4 | 08 |
| Regulatory status of the application (RQ-49) | Open | OPEN_QUESTIONS |

**Change control (ADR-0022 §5):** developer findings (ambiguities, impossible contracts, missing data types, security or performance constraints, schema changes) return through the process fixed at G8; material changes go through an ADR, schema change or gate, never silently in code.

---

## 11. Work since `76068d8` (2026-10-19 → 2026-10-25)

Nothing in this section is binding. *[2026-10-24]* The two S4.13 files described in §11.4 are now committed as DRAFT (awaiting owner acceptance; *[2026-10-28]* accepted, §11.11); every other item is a proposal, an analysis or an owner decision, recorded in a governing document only where this section says so.

### 11.1 Owner's methodological review of eight proposals (2026-10-19)

**Context.** After S4.12b the owner asked for research on eight areas: portfolio-context evaluation of new investments; alpha and risk-adjusted metrics; peer-relative valuation; turning text into signals; thesis-driven signal discovery; nonlinearity and machine learning; volatility drag; and technical analysis. Many of the ideas came from Pete Hecht (AQR) on the *How I Invest* podcast. The research produced proposals E-1 … E-8. The owner then asked for a critical re-check against the existing governance, which found that nearly all of them duplicated existing rules.

| Proposal | Owner outcome | Where recorded |
|---|---|---|
| E-1 portfolio-context report | Withdrawn; covered by the S412-D4 funding report, EQ-DIAG-6 (risk contributions), Portfolio Map PM-1, RQ-44's certainty-equivalent cost test, S14 | Not recorded |
| E-2 metric panel | Withdrawn; covered by invariants I-5 and I-9, ADR-0027 D4, EQ-DIAG-1 … 8, RQ-37 D-4 (deflated Sharpe) | Not recorded |
| E-3 signal evidence protocol | Withdrawn as a separate protocol. The gap it exposed remains open: ADR-0025's "primary source" criterion is undefined for internally discovered signals. The owner will decide the admission route at S4.21/G4 | Not recorded until the owner decides |
| E-4 peer-relative valuation | Two optional S9c candidates: cash-based operating profitability (Ball et al. 2016); within- and across-industry components (Asness, Porter & Stevens 2000) | RQ-28 and RQ-30 notes (`a9a2689`) |
| E-5 text-to-signal | No capability built; none prohibited. Revisit only if S9c finds a material gap text could fill, credible evidence appears for a deterministic text descriptor in the engine's markets, or a long, point-in-time, licensable Oslo document source becomes available | RQ-08 note (`a9a2689`) |
| E-6 nonlinear / ML policy | Withdrawn. Owner decision D-D (2026-10-02, `S4_DOWNSTREAM_INVENTORY.md` §2) already sets the ML admission bar. No separate ML policy and no restriction by asset class or model type. A nested-model comparison may be considered within S7/RQ-09/RQ-37, subject to verification | Not recorded |
| E-7 return basis and volatility drag | Withdrawn; covered by ADR-0027 D5, I-4, RQ-12, EQ-SPLIT-1, 07 §5 and the Kelly family row; its two bans had nothing to ban | Not recorded |
| E-8 technical evidence cards | Withdrawn; the useful part filled two registered source gaps (families T6 and T12, located only) | S4.15b T6/T12 rows; source inventory §22 (`a9a2689`) |

### 11.2 The Hecht (2014) reference (review 2026-10-20)

- **What it is.** Cavaglia, Han & Seshadri (2026) cite "Hecht (2014)" for extending the appraisal ratio to any reference portfolio. The owner identified the source: Peter Hecht, "Evaluating Hedge Funds – Alphas, Sharpe Ratios & the Underappreciated Appraisal Ratio", hedgefundinsight.org, 18 December 2014. It was read in full over plain HTTP because the site's HTTPS certificate had expired.
- **Author.** Written while Hecht was at Evanston Capital Management. He is the same person as AQR's Pete Hecht in the podcast: the article's bio and the podcast both give a Chicago PhD under Fama, a Harvard Business School assistant professorship and allocator roles. Cavaglia et al. list the piece as an AQR working paper. That is a citation discrepancy; no AQR version was found, though the search was not exhaustive.
- **Content.**
  - The appraisal ratio comes from regressing a new investment's excess return on the investor's existing total portfolio.
  - (max Sharpe)² = AR² + (existing Sharpe)², stated without proof, crediting Treynor & Black 1973.
  - No weight formula: Cavaglia's single-candidate weight is their own, Treynor & Black's one-asset case, verified in `s412b_tpa.py`.
  - Worked example on a 60/40: emerging-market equities have the highest return but the lowest AR; catastrophe bonds have the highest AR.
- **Verdict.** FITS as a secondary practitioner source; it adds no new mathematics. Note that Hecht measures against the current portfolio with cash funding, whereas the S412-D4 funding report uses `POL.benchmark` with stock/bond funding. TPA-2 shows that the funding set changes the alpha.
- **Pending owner approval (three small edits):**
  1. `S4_NON_TRADITIONAL.md` §9.8: Cavaglia et al. credit Hecht and Kepos with extending the *candidate* to any mix of assets, factors or return drivers and the base to a reference portfolio. The current text says "base portfolio to any mix".
  2. Add Hecht (2014) to the source inventory as read (secondary).
  3. Record the affiliation discrepancy as a Cavaglia citation issue (proposed ID CHS-1).

### 11.3 F-1 — the scenario return basis (analysis 2026-10-20; *[2026-10-28]* decided: option (a), §11.11)

**Definitions (verified):**
- Grinold, *Advances* ch. 32, eq. (10), p. 671: with probability π_s the **total** return on asset n is r_F + μ_nΔt + σ_n z_{n,s}√Δt. Here r_F is the total return on a risk-free investment over [0, Δt], μ_n the annual expected **excess** return, σ_n the annual volatility, and z is built from asset n's excess-return history, demeaned and standardised. Grinold's setting is expected-utility maximisation over fully invested portfolios.
- EQ-SCN-1 (S4.12a register) reproduces this, with μ = 0 for μ-free uses ("demeaned") and S9's μ for μ-consuming uses. Its μ-free scenarios therefore have mean r_F, not zero.
- S4.6 §4: μ and Σ are both in excess of the numéraire cash rate.
- S412-D6 (a): μ-free D1 V0 and D3 use demeaned scenarios; μ-consuming D1 V1, D2 and B5 use scenarios centred on S9's μ. Its rationale: keep S9 as the only source of μ, remove a horizon-dependent hidden risk aversion, and make the normal limits (GMV, ERC) hold.
- **The S4.12a verification used zero location throughout:** `s412_cvar_ru.py` recentres with `target_mu + zs*sd` and no r_F; the Gaussian D3 tests in `s412_drawdown_tail.py` use μ = 0; the scenario test demeans with `Y -= Y.mean(0)`.
- So the register's canonical form and the verified implementation disagree.

**D3 exactly** (record and S412-D3):
- the risk measure is scenario CVaR at β = 0.95 (EQ-NT-1) of the loss −y′w;
- Euler contributions C_i = w_i·E[−r_i | tail];
- ERC-CVaR means equal shares, solved by the convex log-barrier y* = argmin CVaR(y) − (1/N)Σ ln y_i, with w = y*/1′y*;
- the result is long-only and fully invested by construction; bounds are applied by post-processing (S411-D4).

S412-D3's own rationale: "The convex form removes the stochastic optimiser and the existence failure". BCP-4 names "cash in a total-return CVaR" as the failure case.

**Exact existence condition (derivation):**
1. CVaR(y; Y + c·1) = CVaR(y; Y) − c·1′y, by translation equivariance and positive homogeneity.
2. The barrier objective is convex. If CVaR(y₀) < 0 for some y₀ ≥ 0, the objective tends to −∞ along t·y₀. It then has no minimiser, and because a stationary point of a convex function is its global minimiser, no portfolio with equal positive contributions exists.
3. If CVaR(y) > 0 for every nonzero y ≥ 0, the objective is coercive and its minimiser is unique.

With a common per-period cash return in the location, then, **ERC-CVaR exists if and only if the long-only minimum CVaR on zero-location scenarios (D1 V0's optimum) exceeds the period cash return.**

- **Normal special case.** CVaR⁰(w) = c₂·σ(w)·√Δt, with c₂ = φ(z)/(1 − β) = 2.0627 at β = 0.95. ERC-CVaR then exists if and only if the long-only minimum-variance volatility exceeds r_F√Δt / c₂. That bound is 1.94% annual at r_F = 4% and 0.56% monthly, and it grows with √Δt (3.36% at three years).
- **Sufficient single-asset bounds.** Gaussian (BCP-4): any asset with σ_i ≤ r_F√Δt / c₂. Distribution-free, by Cauchy–Schwarz: any asset with σ_i ≤ r_F·√Δt·√(1 − β), i.e. 0.89% annual.
- **The S4.13 draft states only the single-asset Gaussian form.** That form is sufficient but not necessary. *[2026-10-24]* Corrected in the committed inventory (§6.1).

**Numerical reproduction** (S4.12a's Gaussian functions copied verbatim, plus the decided barrier form; scratch, 2026-10-20):

| Case | Result |
|---|---|
| Volatilities 16%, 6%, 1.5%; correlations 0.1, 0, 0.2; annual; cash rate in the location | No solution: S4.12a least-squares residual 0.52; the barrier objective diverges. The long-only GMV volatility is 1.49%, below 1.94% |
| Same, zero location | (0.0733, 0.1777, 0.7490), equal to volatility-ERC |
| Same, monthly | Zero location (0.0733, 0.1777, 0.7490); with the cash rate (0.0560, 0.1382, 0.8058); shares equal in both |
| 16%, 2.5%, 2.5%, uncorrelated, annual | No solution, although no asset is below 1.94%: the long-only GMV volatility is 1.76% |
| 16%, 3%, 3%, annual | Solution exists: the long-only GMV volatility is 2.10% |
| Fat-tailed scenarios (t4 with a crash jump), scenario CVaR | Annual: min CVaR⁰ 3.37% < 4%, no solution. Monthly: 0.97% > 0.33%, solution exists, weights (0.0724, 0.1717, 0.7559) → (0.0562, 0.1331, 0.8108) |
| D1 V0 (min-CVaR LP), with and without the shift | Identical weights; CVaR shifts by exactly −r_FΔt |

**Mechanism.** The cash return enters each Euler contribution as −r·w_i, in proportion to weight rather than risk. Parity therefore shifts toward low-risk assets, and once the cash return exceeds the smallest achievable tail loss no parity point exists. D1 V0 is unaffected because, over 1′w = 1, the objective only shifts by a constant. Two things guarantee this: the D1 record's invariant ("a uniform shift of the scenarios by c changes CVaR by −c for a fully invested x") and S47-D6 (μ-free methods produce a fully invested risky mix), given one common r_F. The S4.13 draft wrongly cites S45-D4 for this (*[2026-10-24]* corrected).

**Return basis needed by each consumer:**

| Method | Basis | Status of the claim |
|---|---|---|
| D1 V0 | Either basis | Derivation, verified |
| D3 | Zero-location excess returns, for existence and the ERC limit as verified and decided | Source-supported (S412-D3 rationale; BCP-4) |
| D1 V1 | Target R and the scenario mean on one basis | Derivation; no source preference |
| D2 | Total returns (a compounded wealth drawdown) | Inference from CDD-3 and `INV.max_one_year_decline` (S1); not pinned by a source |
| B5 | Total returns with MAR = the cash rate (as verified in `s412_downside_b5.py`), or excess returns with MAR = 0 | Source-supported |

**Options:**
- **(a)** Zero-location excess-return scenarios for μ-free methods, with each μ-consuming method declaring its basis. Consistent with all S4.12a results, S412-D3's rationale, S412-D6's rationale and S4.6. EQ-SCN-1's total-return form stays valid for μ-consuming uses.
- **(b)** Keep r_F everywhere. D3's existence and weights would then depend on the cash rate and the horizon, which S412-D6 set out to remove; the S4.12a D3 evidence would no longer apply.
- **(c)** Defer to S10. This leaves D3 without "a clear mathematical definition" (an ADR-0025 admission criterion) and blocks its S4.20 contract.

**Recommendation: (a).** Note that D3 is *not* invariant to a common cash return under EQ-SCN-1 as written; that is the defect. Option (a) makes it invariant by construction.

**Owner instruction (2026-10-21):** the recommendation is not an approved decision. Do not edit S412-D6 or EQ-SCN-1, and do not alter any method record to make the convention look settled. The decision stays outside the S4.13 corrections until the owner authorises it.

### 11.4 S4.13 — risk and covariance dependency inventory

*[2026-10-28]* **Accepted by the owner** (§11.11). **Status 2026-10-24: corrected and committed.** The owner authorised corrections 1–21 (the plan below, extended by a re-check on 2026-10-24 with six more items: COV-5's unsupported mechanism text, the §5 eligibility-field attribution, COV-6's inference label, COV-2's source, the Option D hand-forward to S4.16, and the checker's selection-wording rule), chose the candidate kind MEASURE for modified CVaR, and authorised one commit with the minimum bookkeeping and a push. Results, all run on 2026-10-24:
- the S4.13 checker passes;
- all 31 verification scripts pass;
- a scratch mutation suite of 26 cases behaved as expected: 20 caught (including the fabricated decision ID and the S412-D6 rewording, now a clean failure), 5 limitation probes still pass as documented in the inventory's §9 (a consistent wrong mapping, a cutoff beside "No threshold set", a wrong tag from the vocabulary, wrong content, an edited §6.1 number), and the allowed wording "no default" passes;
- only the five intended files changed; ADR-0027 is still PROPOSED; S4_NON_TRADITIONAL, the equation register and decisions/ are unchanged.

The changes are listed in the inventory's §10. S4.13 awaits owner acceptance; F-1 awaits the owner's decision (§11.3). The text below records the draft, the review and the plan as they stood before the corrections.

**Drafted 2026-10-19** (owner authorised S4.13 with safeguards: read-only reconciliation first, no estimator selection, no invented thresholds, ADR-0027 kept PROPOSED, no commit). Two untracked files:
- `notes/v2/research/s4/S4_RISK_DEPENDENCIES.md`:
  - 28 method records (21 PC methods: A1–A5, B1–B7, C1–C5, D1–D4; SIG-1, SIG-2 and four variants; EQ-SIG-4), in 32 rows, plus 6 cross-cutting consumers (EQ-SPLIT-1, EQ-MAP-3, EQ-TC-1, R-7, AC-5, S412-D4);
  - 3 provisional problems (P-STRAT, P-SEC, P-SHORT);
  - 8 objects: RO-1 Σ strategic, RO-2 Σ security sleeve, RO-3 short horizon, RO-4 demeaned scenarios, RO-5 μ-centred scenarios, RO-6 paths, RO-7 co-moments, RO-8 factor model;
  - 23 candidates COV-1 … COV-23, all "candidate", "No threshold set";
  - findings F-1 … F-10; Binding: 6 established, 32 unresolved.
- `notes/v2/research/s4/verification/s413_risk_dependencies.py`: a registry checker that prints PASS (re-verified 2026-10-20). The ten reported mutations all reproduced as failures.

**Read-only review 2026-10-20 (owner-requested). Verdict: defensible with limited corrections, not acceptable as drafted.** Findings:
- **Objects:**
  - RO-1, RO-2, RO-4, RO-5 and RO-6 are justified.
  - RO-3 groups instrument volatility (SIG-2), base-portfolio volatility (A5) and strategy-return volatility (EQ-SIG-4); S48-D2's frequency rule is over-attributed to all of them.
  - RO-7 frames co-moments correctly, but the *modified-CVaR estimator* that S412-D3 requires is not registered.
  - RO-8 is justified for B3 only; the EQ-MAP-3 → RO-8 link is unsupported (EQ-MAP-3's residual ω is benchmark-relative, from Σ).
  - Omission: portfolios mixing asset-class units and single securities (RQ-07 allocation unit "both") need joint or hierarchical risk across RO-1 and RO-2. R-7 covers only sleeves inside a host class.
- **Estimators:**
  - COV-8 and COV-9 are misclassified as transformations. Ledoit–Wolf shrinkage is an estimator: LW 2003's abstract ("an optimally weighted average of two existing estimators") and Lemma 1, p. 10, and LW 2004 Lemma 3.3 estimate the intensity from the raw observations.
  - COV-10 and COV-11 are conditional on how the intensity is set.
  - COV-9's RO-1 link contradicts the exclusion in S4_RISK_MODEL_CHOICE §3.
  - COV-7's RO-1 link has no evidence; it mixes factor-model forms.
  - COV-22: ABD App. C.1 names Geltner (1991) unsmoothing; the draft wrongly says "method not specified".
  - COV-23's evidence is overstated (only a note cites Paleologo p. 135).
  - COV-12's abstract evidence comes from S4_RISK_MODEL_CHOICE, not this review.
  - COV-16 and COV-21 each mix two things.
- **Status:**
  - The 6/32 split is justified under the weakest-link rule, but it hides that the requirement itself (type and object) comes straight from a record in about 28 of the 32 rows.
  - Four rows rest on inference or an option; only PC-A5 σ* is labelled as such.
  - Misattributions: S48-D2, S45-D1, S412-D4 (D4 security level) and S45-D4 (D1 V0).
- **Checker:** see §11.5.

**Correction plan (2026-10-21) — awaiting owner authorisation.** Scope: the two S4.13 files only. No exception is needed; no decision, accepted ADR, method record or S4.12 result changes.
- **A. F-1:**
  - a new §6.1 in the inventory giving the exact condition, the normal special case and the two sufficient bounds;
  - the corrected D1 V0 reasoning (D1 invariant plus S47-D6, not S45-D4);
  - the downstream basis table, each claim labelled source-supported or inference;
  - options (a)–(c), with (a) recorded as evidence-supported and pending;
  - updates to §0, §7, and the PC-D1 V0, PC-D3 and RO-4/RO-5 cells;
  - the checker's F-1 reproduction rewritten to verify the corrected claims (exact condition, the 16/2.5/2.5 counterexample, the 3% case, fat-tailed scenarios, the D1 V0 LP invariance, the Cauchy–Schwarz bound).
- **B. Registry:**
  - add COV-24, modified (Cornish–Fisher) CVaR: input RO-7 (co-moments from COV-20 or COV-21), output CVaR_β and Euler contributions for PC-D3's modified-CVaR variant, formula BCP App. eqs. 21–22, with the BCP-5 caution, not the default (S412-D3);
  - **taxonomy question:** add a sixth kind, MEASURE (computes a method's risk measure from a risk object and constructs no object), excluded from the constructed-by lists (recommended), or fall back to TRANSFORMATION with an explicit "consumes RO-7, constructs nothing" rule;
  - reclassify COV-8 and COV-9 as ESTIMATOR;
  - set COV-10 and COV-11 to "ESTIMATOR / TRANSFORMATION (conditional on how the intensity is set)";
  - drop RO-1 from COV-9, noting the S4_RISK_MODEL_CHOICE §3 evidence-based exclusion, which is not a decision;
  - drop RO-8 from EQ-MAP-3 and restate it from the register.
- **C. Evidence and attribution:**
  - COV-22: Geltner (1991) via ABD App. C.1;
  - COV-12: abstract per S4_RISK_MODEL_CHOICE §2;
  - COV-23: OPEN (page not re-checked);
  - D4 security-level row: basis is the S4.12b record (allocation domains), stated as an option;
  - S48-D2 limited to SIG-2; S45-D1 for A5 (MM V0 oracle: the previous month's 22 daily returns); A5's production frequency unresolved;
  - P-STRAT universe attribution;
  - the R-7 coupling relabelled as derived;
  - RO-1's singularity minimum cites 06 §4;
  - a traceability sweep of every `[established: …]` marker, reporting any further mismatches.
- **D. Grouping:**
  - narrow RO-3 to "the short-horizon risk model" (Σ_t, with instrument σ_i and a portfolio's σ̂ as views), since both remaining consumers' records map to "the short-horizon risk problem"; per-universe instances unresolved (S5, S10);
  - EQ-SIG-4 becomes INTERNAL: its record defines σ by the sources' own estimators (B&SC: 126 uncentred daily returns; DM: GJR-GARCH in-sample, 126-day variance out of sample) and S49-D2 makes it variant-only; production treatment unresolved (S10, S13c);
  - new finding F-11 plus dependency entries in the EQ-SPLIT-1, AC-5 and S412-D4 rows for mixed asset-class and security portfolios, traced to RQ-07, the allocation domains, EQ-SPLIT-1 and R-7; unresolved (S5, S10). No new object ID and no architecture.
- **E. Checker:**
  - required: fail cleanly when S412-D6 cannot be interpreted; verify that cited decision IDs (S4x-Dy, OB-x, ADR numbers) exist in other repository documents;
  - consequential rule changes for B: the MEASURE kind if approved, and the conditional-kind syntax;
  - rewrite §9 to list what is and is not checked, including the demonstrated false negatives;
  - optional, not implemented: input types grounded in each record's Inputs field; comparison signs in eligibility cells.
- **Verification plan:**
  1. the S4.13 checker (expect PASS);
  2. all 30 committed verification scripts plus the S4.13 checker, each PASS or FAIL;
  3. a scratch mutation suite: the 10 originals expected to fail; the fabricated-ID probe now expected to fail; the S412-D6 rewording expected to fail cleanly; the consistent-remapping, cutoff-with-phrase, evidence-upgrade and wrong-content probes still passing as documented limitations; COV-24 marked as constructing RO-7 expected to fail;
  4. a git diff check that only the two files differ and ADR-0027 is still PROPOSED.
- **Cannot be completed without more evidence or a decision:**
  - the MEASURE kind (owner);
  - F-1 (owner);
  - the final kind of COV-10 and COV-11 (needs Elton & Gruber 1973 / LW 2004 *JPM* or an intensity specification);
  - D2's total basis (pending the Policy Statement drawdown quantity: S1 field 7.2 is a one-year decline, and the MaxDD mapping belongs to S11/S13);
  - Geltner 1991 (not in hand).
- **Outside scope; needs separate approval:**
  - the F-1 annotation of S412-D6 / EQ-SCN-1;
  - the Hecht fixes (§11.2);
  - bookkeeping (§6 item 13);
  - commit and push.

**Acceptance criteria (owner, 2026-10-21).** The corrected deliverable must:
- trace each material requirement to its source;
- distinguish risk objects from estimators and other candidate types;
- avoid unsupported mappings and misattributed evidence;
- record the mixed-portfolio dependency without resolving it;
- state F-1's condition correctly, separating the general condition from special cases;
- keep ADR-0027 PROPOSED;
- pass the checker and the relevant regression tests, with actual results reported;
- make no claim that structural validation proves methodological validity.

### 11.5 Checker limitations demonstrated (scratch probes, 2026-10-20; re-run on the corrected checker 2026-10-24)

**Grounded in authoritative text:**
- coverage, read from the record headings;
- the S412-D6 location classes, parsed from the decision row;
- ADR-0027's status, read from its file;
- *[2026-10-24]* cited decision IDs, checked against the other notes/v2 documents.

Everything else checks the inventory against itself.

| Probe | Result |
|---|---|
| GMV remapped to the short-horizon RO-3, all references consistent | Passes (not detected) |
| GMV retyped as a factor model on RO-8, consistently | Passes |
| A cutoff ("eligible only when q_eff ≤ 0.5") added while keeping "No threshold set" | Passes |
| A fabricated basis `[established: S499-D9]` | Passed; caught since 2026-10-24 |
| An evidence tag upgraded from OPEN to VERIFIED-SOURCE | Passes |
| B1's minimum data replaced by a false "none required" | Passes |
| S412-D6 reworded ("do not use μ") | Crashed (AttributeError); clean failure since 2026-10-24 |
| C5's heading loses its ID | Caught |
| *[2026-10-24]* A number in §6.1 edited | Passes: the F-1 values are the checker's own constants, not parsed from the text |

### 11.6 Next steps, in order

1. *[2026-10-24]* Done: the owner authorised the corrections and the MEASURE kind; they were applied, checked (§11.4), committed and pushed.
2. Owner: accept S4.13; decide F-1 (recommendation (a)); the Hecht fixes; the remaining bookkeeping (§6 items 10–13). *[2026-10-28]* Done, except the two remaining Hecht edits (§6 item 12).
3. S4.14 (agentic PC roles: Researcher research lane; Adversarial Diversifier formulation, ANG-16), starting with a read-only reconciliation, then S4.15–S4.27 → G4.
4. Unchanged owner items in parallel (§6 items 0–9), including the S4.2/ADR-0027 review and sandbox key rotation.

### 11.7 Notes for the next assistant

- **Scratch work is not persistent.** The F-1 reproduction and the mutation harnesses lived in the earlier session's scratchpad, `/private/tmp/claude-501/-Users-oliver-Desktop-ENGINE-V1/4750b449-c158-429d-a18a-0899ca2a7b6d/scratchpad/` (folders `s413` and `s413review`), and may be gone. *[2026-10-24]* The F-1 reproduction now lives in the committed checker `s413_risk_dependencies.py`; the 2026-10-24 mutation harness ran in a session scratchpad and is not kept.
- **numpy 2.0.2 on this Mac:** `@` (matmul) can raise spurious floating-point warnings through Accelerate even though the results are finite. Use `einsum`, or check `isfinite`.
- **Web reading:** the web-fetch tool fails on expired TLS certificates; reading the page over plain HTTP into the scratchpad worked for the Hecht article. Podcast transcripts that render with JavaScript were read in the built-in browser by extracting `window.__tx`.
- **Repository state:** *[2026-10-25]* branch `stage/s04-method-library`, with the 2026-10-25 corrections commit as the latest, in sync with origin; no untracked files; no PR (gate PR at G4).
- **Assistant memory files** (outside the repository) hold the protocol and feedback rules summarised in §2.1–§2.2. Current owner instructions always win over them.
- **Security reminders (§2.3):**
  - no personal financial data in the repository;
  - no downloads without per-item permission;
  - no push, PR or merge without explicit authorisation;
  - ADRs are append-only;
  - API keys are never printed;
  - the UI concept prototype stays outside GitHub;
  - the owner's E-3 decision is recorded only when the owner authorises it (S4.21/G4).

### 11.8 Analyses delivered 2026-10-24 (owner request) and the owner's decisions on them

1. **A Chief Total Portfolio Agent (CTPA) alongside the CIO?**
   - **Current architecture:** ADR-0023 makes "CIO combination/selection with explanation" a baseline role. ADR-0026 makes the approved portfolio decision the CIO's, approved by the investor, and makes rebalancing determination deterministic. In S4_ACCOUNTABILITY, the CIO owns the ensemble choice, rationale, invalidation conditions and proposed rebalancing rule; the CRO owns independent risk assessment and whole-portfolio interim limits.
   - **Where the candidate CTPA functions already sit:** holistic view, imbalance detection, consistency with the Policy Statement, and cross-position interactions are covered by deterministic services (Portfolio Map PM-1, CRO diagnostics, the S412-D4 funding report, R-7 look-through, S16 monitoring, the R3/R4 predicates) plus the CIO. Top-down views are covered by the macro and asset-class/CMA roles and by S9.
   - **Owner decision (2026-10-24): Option D accepted**, as recommended. Not yet noted in S4_PLAN S4.16/S4.18 (bookkeeping, §6 item 13); `S4_RISK_DEPENDENCIES.md` §8 already hands the evidence packet forward to S4.16.
   - **Recommendation (accepted):** no new agent. Make the CIO's total-portfolio responsibility explicit in its Agent Mandate (S4.18/S4.20). At S4.16, require a deterministic total-portfolio evidence packet: the CRO diagnostic contract and the funding report applied to the CIO's final ensemble and to current holdings. F-11 joint risk stays unresolved (S5/S10).
   - **Revisit if:** several goal portfolios run at once, household scope enters, or process evidence (RQ-55, S15) shows total-portfolio errors the packet misses.
2. **Historical means combined with momentum as expected returns? (Michaud & Michaud 2008.)**
   - **Owner decision (2026-10-24):** disregard the analysis and keep the current design. Nothing from it, including the Michaud source observations below, is recorded in the governing documents; the text below is kept only as the record of what was delivered.
   - **Source findings (read 2026-10-24):**
     - ch. 11 (pp. 101–108) presents a Theil–Goldberger mixed estimate that assumes views independent of the historical data (p. 105) and normal distributions (p. 102 fn. 3);
     - Table 11.1 reproduces to within 0.1 pp with the standard precision-weighted posterior, using the return covariance (not the variance of the mean) as the historic uncertainty; the matrix order of B as printed in (11.1) does not reproduce the table;
     - ch. 8 gives James–Stein shrinkage toward the global mean;
     - ch. 12 (pp. 109–111) says rankings must be scaled by IC × volatility.
   - **Repository position:** ADR-0012 (no score as μ without an accepted mapping); S4.9 R-1, R-2 and R-7c; EQ-MAP-1 … 4 registered, not accepted; Bayes–Stein (EQ-MVO-E2) handed to S9 as a CMA candidate.
   - **Derivation:** a momentum window inside the historical sample correlates √(k/T) with the mean (0.22 for 12 of 240 months). Under no predictability its optimal weight is zero. A naive "independent view" combination raises the variance by 4.3% while claiming a 4.8% reduction; under the Table 11.1 convention the variance is about 17 times worse.
   - **Recommendation (not pursued; the current design stands):** no blend of historical means with momentum as μ. Bayesian shrinkage remains a CMA candidate. Momentum reaches μ-consuming methods only through a registered mapping under an explicit predictive model, with an out-of-sample IC and a matched horizon (MOP 2012: persistence for 1–12 months, partial reversal later); μ-free methods use it only through O2/O3/O5/O6. A validation plan was proposed for S7/S9.

### 11.9 Renshaw et al. (2026): reference specification for the multifactor composite (2026-10-25)

- **Sources** (source inventory §23): the July 2026 paper (40 pp.); the August 2026 STOXX whitepaper (15 pp.; identical results; omits the market-similarity configuration, App. C); the iSTOXX Equity Indices Methodology Guide §118 (version of 13 Oct 2026; rule-level and newest).
- **Owner decisions 2026-10-25:** the paper is the reference specification for the multifactor composite: signals, factor scores, the 1/3–1/3–1/6–1/6 score, the construction and the three timing models. Only the construction is adopted; FinSol applies it to its own universe and datasets and does not aim to replicate the paper's results. Factor-momentum timing follows the source (S48-D6 annotated; RQ-11).
- **Corrected in place:** RQ-28 (cyclical value = book-to-price + earnings yield; the Shiller-type definition removed; signals per the source), RQ-31 (reference transform), RQ-32 (source; the two value sleeves are weakly related).
- **Decided later on 2026-10-25 (REN-D1 … REN-D7):** reference record `research/s4/S4_SCORING_RENSHAW_ANG.md`; Renshaw replaces the Sørensen definitions (Sørensen kept as display transform, reproduction oracle and standalone SIG-1); R-1 refined and EQ-MAP-5 registered (V0), EQ-MAP-3 the tested V1; factor momentum follows the source; timing models in the research lane in shadow mode with a mandatory embargo; analyst revisions missing until a licensable dated source (FMP to check); EBIT/EV a cyclical-value test variant. Verification: `s4ren_multifactor_reference.py`.
- **Owner to supply:** Stewart (2009) *JACF*; Lev & Sougiannis (1996) *JAE*; Sloan (1996) *Accounting Review* (no legitimate open copy found).
- **Outside the repository:** the owner-facing assessments (`ENGINE_V1/RENSHAW_2026_DIVERSIFICATION_ASSESSMENT.md`, `ENGINE_V1/RENSHAW_2026_IMPLEMENTATION_ASSESSMENT_v2.md`) and a scratch reimplementation of the market-similarity model.

### 11.10 Momentum taxonomy and interface review: owner decisions (2026-10-25)

- **Review:** owner-facing, read-only, outside the repository (`ENGINE_V1/MOMENTUM_AND_INTERFACE_REVIEW_2026-10-25.md`). The owner's screenshots were of Investwiser's English interface.
- **Momentum taxonomy (no change needed):** one family, two objects: SIG-1 XSMOM (cross-sectional; "conventional price momentum" is SIG-1) and SIG-2 TSMOM (time-series state). The headline Momentum score is the Renshaw factor; TSMOM is shown as a trend state; the Sørensen 12–1 is the standalone SIG-1 signal in the drill-down.
- **Decided:**
  - **P1:** §9.1 score-table rows (Renshaw factors; trend-state context column; labelled multifactor aggregation).
  - **P2:** T-9 vocabulary.
  - **P3:** T-1 clarified; T-7 revised by the owner: "the colours can be red/green as long as it does not directly affect the agents decisions. It is only for visual representation, but not as a factor in the analysis."
  - **P4:** not needed: the owner states Investwiser's FAQ previously confirmed EODHD (S6 lead §4.2 annotated).
  - **P5:** new fact version; the source passage was re-read on 2026-10-25 ("listed shares domiciled in the EEA"; several Oslo-listed companies do not qualify).
  - **P6:** security-sleeve review in the AC/CMA mandate.
  - **P7:** RQ-20 candidate template.
- **OB-2 amended:** combined Investwiser / OpenBB Workspace reference. Investwiser is UX inspiration for Market, Find Investments and Analysis, analysed and rebuilt for the engine; its AI assistant is disregarded.
- **Developer document:** `research/s8/S8_LEAD_UX_MARKET_FIND_ANALYSIS_2026-10-25.md` (DRAFT; names no product, as the owner asked). It is based on a page-by-page review of the three areas on 2026-10-25, covering every view and tab.
- **Left unchanged deliberately:**
  - `S3_FINDINGS.md` line 48 and `facts/README.md` ("82 records"), both accepted at G3. The README count remains true for registry v1; see §6 item 22.
  - `S4_SCORING_PEER_METHODS.md` §1 ("Fundamentals come from EODHD"), per P4.

### 11.11 S4.13 close-out and F-1 (2026-10-26 to 2026-10-28)

- **Evidence sweep (read-only):** all 119 `[established: …]` markers in the inventory were checked against their sources; 114 matched. Five cited the wrong source and were corrected:
  - PC-A5 (three markers) → EQ-H-4;
  - EQ-SPLIT-1's units → a derivation, with ADR-0027 D5 provisional;
  - EQ-MAP-3's ω → R-2.
  - No requirement and no Binding value changed.
- **Renshaw alignment** (`828e0e7`): the Renshaw record (2026-10-25) cited RO-2/RO-8, but S4.13 did not list it. Now aligned:
  - a SIG-1/R row for signal 7 on RO-8;
  - the EQ-MAP-5 construction on RO-2;
  - the timing models as internal statistics (shadow mode);
  - F-12: one S10 security model may serve PC-B3, signal 7 and EQ-MAP-5;
  - F-13: the reference level of a sleeve's total-risk constraint (S5/S11).
  - Seven mutation probes fail as intended.
- **F-1 decided, option (a)** (`22b384c`): "demeaned" means each asset's excess return minus its own mean, centred on zero, with the cash rate not added back (D1 V0, D3).
  - **Why Grinold adds the cash rate:** his objective is expected utility of total return (*Advances* ch. 32, PDF pp. 669–671). The total form stays for objectives that concern wealth (D2; total-return limits and reports).
  - **What (a) means for portfolios:**
    - 17 of the 21 methods use no scenarios and are unaffected; D1 V0 is unchanged;
    - D3 always has a solution on non-degenerate scenarios and no longer depends on the cash rate;
    - D1 V1, D2 and B5 declare their basis at S4.20;
    - complete portfolios add the cash return back: a constant when lending at one rate, a financing term under leverage. Account-dependent cash returns (cash in an ASK earns none) stay in implementation.
- **S4.13 accepted** (2026-10-28), as the inventory only. ADR-0027 stays PROPOSED: review it before S4.16, add the return basis to D5, and confirm F-8. The items handed forward (§8) stay open.
- **Next:** the two remaining Hecht edits (§6 item 12), then S4.14 (read-only reconciliation first).
