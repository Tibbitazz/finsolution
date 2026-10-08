# S4 Section 2 outline — method mathematics (S4.5–S4.14): orientation and tracker

**Document status:** LIVING (created 2026-10-08 on the owner's request; updated at the end of every step) · **Purpose:** keep the owner and the assistant oriented on where we are, what each step will do, what it needs and what it will ask of the owner. · **Basis:** S4_PLAN §C (ladders, checklist), §D (source map), §F (equation checklist), §G (approved step rows); `S4_PC_SOURCE_MAP.md`; `S4_SOURCE_REVIEWS_2026-10-08.md`; `S4_TAXONOMY.md`; ADR-0024, ADR-0025, ADR-0027 (D3 r3).

**This outline does not change the approved plan.** Each step's scope, sources and exit criterion come from S4_PLAN §G. What this document adds is the order of work inside each step, the issues already known, and the owner decision points we can see coming.

---

## 0. Where we are

| Stage / section | Content | Status |
|---|---|---|
| S0–S3 | Charter, inputs, Policy Statement governance, external facts | **Done** (G0–G3) |
| **S4 Section 1** — foundations (S4.0–S4.4) | Inventory, ANG reconstruction, adaptation and ADR-0027, accountability, taxonomy, source map | **Done** (S4.4 complete 2026-10-08; S4.2 and ADR-0027 await owner review at G4) |
| **S4 Section 2 — method mathematics (S4.5–S4.14)** | The mathematics of every roster method, verified with our own reference code | **In progress:** S4.5 done 2026-10-08 (owner accepted S45-D1 … D4); S4.6 done 2026-10-08 (owner decided S46-D1); S4.7 done 2026-10-08 (owner decided S47-D1 … D6); **next: S4.8** |
| S4 Section 3 — the process around the methods (S4.15–S4.18) | Upstream CMA inventory, CRO diagnostics and candidate card, deliberation, CIO ensembles | Not started |
| S4 Section 4 — consolidation (S4.19–S4.24) | Equation Register reconciliation, typed contracts, eligibility, dependency graph, full verification, fixtures | Not started |
| S4 Section 5 — gate (S4.25–S4.27) | Portfolio Map requirements, library freeze, G4 audit | Not started |
| After G4 | S5 universe and numéraire · S6 data · S7 evaluation protocol · S9 beliefs and signals · S10 risk model · S11 PC set · S12 deliberation · S13 implementation · S14 report · S15–S18 | Not started (S6 data lead exists; S8 platform track may start) |

**Section 2 in one sentence:** for every roster method we turn its governing source into exact mathematics, record where ANG differs, decide the open specification choices with the owner, and prove with our own code that our version reproduces the source. **Nothing is selected or ranked here**: admission (ADR-0025) and evaluation (S7) come later.

---

## 1. How every step runs (standard workflow)

Each step goes through the same nine stages. The PC-method ladder (S4_PLAN §C.1) moves from SOURCE LOCATED/REVIEWED to MATHEMATICS EXTRACTED and COMPUTATION VERIFIED within the step. NOTATION RECONCILED, CONTRACT DEFINED and FIXTURES DEFINED complete in Section 4.

| # | Stage | What happens | Output |
|---|---|---|---|
| 1 | Read | Governing source in full, plus supporting sources; versions and page references | Notes in the step record |
| 2 | Extract | Every equation the method needs, with the Equation-Register fields: source equation and page, notation, canonical notation, dimensions, units, assumptions, constraints, parameter authority, limiting cases, numerical tests (§F) | Entries in `S4_EQUATION_REGISTER.md` (created at S4.5, appended each step) |
| 3 | Compare | ANG's description vs the source; ANG issues confirmed, resolved or added | Rows in the step record; `ANG_ISSUES_REGISTER.md` |
| 4 | Inputs | Input class and risk objects per ADR-0027 D3 (problem = universe × horizon × risk object); units (D5) | Method record "inputs" section → feeds S4.13 |
| 5 | Parameters | Every parameter with its authority class (fixed / system-estimated / user-authorised / agent-selectable / sensitivity-only, ADR-0024 §3) | Method record |
| 6 | Choices | Open specification choices with options and a recommendation. Where a source is internally inconsistent or under-specified: V0 = exact source (reproduction oracle) and V1 = corrected or completed variant | **Owner decision points** |
| 7 | Verify | Own reference code in `verification/`: reproduce published examples; limiting cases; invariants (I-1 … I-9); synthetic data only; self-asserting scripts that print `PASS` | `verification/s4N_*.py` |
| 8 | Record | Method record per method (template in §1.1); status ladder updated; CHANGELOG, HANDOFF, this tracker | Step document |
| 9 | Stop | Owner review before the next step | — |

### 1.1 Method record template (one per method; S4.20 later turns it into the typed contract)
- **Identity:** ID, name, family, type M.PC (`S4_TAXONOMY.md`), roster version.
- **Sources:** governing (version, pages), supporting; where the published version governs a working copy.
- **Definition:** objective or algorithm in words, then the equations (EQ IDs).
- **Inputs and risk objects:** what it consumes, and what it deliberately does not use (e.g. μ-free).
- **Parameters:** values or ranges, authority class, reason.
- **Constraints:** how Policy Statement constraints enter (natively, by post-processing, or not at all).
- **Allocation domains:** asset class / fund / security (ADR-0024 §4).
- **Output:** weights; failure and infeasibility outcomes with reason codes (I-2).
- **ANG vs source:** differences and their resolution.
- **Specification choices:** V0/V1 where relevant, and the owner decision.
- **Invariants and limiting cases:** what any correct implementation must satisfy.
- **Verification:** script, what it reproduces, result.
- **Agent-readable summary** (ADR-0024 §5): objective, intuition, assumptions, known sensitivities and failure modes, valid and invalid comparisons.
- **Ladder status.**

---

## 2. The steps

### S4.5 Heuristic portfolios — PC-A1 … PC-A5
- **Methods:** A1 equal weight (1/N); A2 market-cap weight; A3 inverse volatility; A4 inverse variance; A5 volatility targeting.
- **Sources:** all in hand. DeMiguel, Garlappi & Uppal 2009; Sharpe 1964; Kirby & Ostdiek (working version 2010; JFQA 2012 governs); Moreira & Muir 2017 (JF).
- **Equations:** EQ-H-1 … EQ-H-4.
- **Known so far:**
  - A3/A4 are members of Kirby & Ostdiek's volatility-timing family VT(η), weights ∝ (1/σ²)^η: A3 = η ½ and A4 = η 1. KO test only η ∈ {1, 2, 4} on 120-month rolling variances of monthly excess returns (ANG-13, resolved).
  - A5 is under-specified in ANG (ANG-14, H): Moreira & Muir scale a single factor's exposure by c/σ²_t. ANG gives no base portfolio, target level, residual (cash) or leverage treatment.
  - A2 needs asset-class capitalisations (a data contract for S6).
- **Owner decisions expected:**
  - **A5 specification:** base portfolio, target, cash residual or leverage cap, volatility estimator and horizon. The estimator links to the short-horizon risk problem in ADR-0027 D3.
  - **A3/A4:** keep η fixed at the named values (recommended), or treat η as a parameter.
  - **A2:** the capitalisation source and its proxy.
- **Verification:**
  - invariants: weights sum to 1; positivity; scale invariance of A3/A4 to a common rescaling of Σ; permutation equivariance;
  - limits: VT(0) = 1/N, and VT(η → ∞) puts all weight on the minimum-volatility asset;
  - Moreira–Muir scaling identity on a synthetic series;
  - A4 equals minimum variance under a diagonal Σ (KO eq. 12).
- **Deliverables:** `S4_HEURISTICS.md` (five method records); `S4_EQUATION_REGISTER.md` (created); `verification/s45_*.py`.
- **Exit:** A1–A5 reach MATHEMATICS EXTRACTED → COMPUTATION VERIFIED.
- *[2026-10-08]* **Drafted:** `S4_HEURISTICS.md` (five method records; decisions S45-D1 … D4), `S4_EQUATION_REGISTER.md` (created; EQ-H-1 … EQ-H-4 with sub-equations and the shared turnover EQ-H-T), `verification/s45_*.py` (4 scripts, PASS). New issues: ANG-43 … ANG-46; source issues MM-1, MM-2. Exit reached at source level; A5's V1 parameters wait for S45-D1.

### S4.6 Mean–variance foundation (supports PC-B1, PC-C1)
- **Scope:** objective, efficient frontier, tangency portfolio, constraints, risk-free treatment, and the estimation-error problem.
- **Sources:** Markowitz 1952; Tobin 1958; Sharpe 1964; Michaud 1989 (read); Jorion 1986. Supporting but not blocking: Jagannathan & Ma 2003; Kan & Zhou 2007.
- **Equations:** EQ-MVO-1 … EQ-MVO-4.
- **Known so far:** the covariance and return-error evidence in `S4_RISK_MODEL_CHOICE.md` (M-1, M-2) and Michaud's p. 38 finding feed the estimation-error section.
- **Owner decision expected:** how the risk-free asset and cash are treated at the asset-class level (cash as an asset vs a risk-free rate).
- **Verification:** closed forms vs a numerical solver to tolerance; frontier tracing; two-fund separation; condition-number sensitivity on synthetic data.
- **Deliverable:** `S4_MVO_FOUNDATION.md`.
- **Exit:** closed form = solver within tolerance.
- *[2026-10-08]* **Drafted:** `S4_MVO_FOUNDATION.md`; register EQ-MVO-1 … EQ-MVO-4 (+ 2a, 3a, 4a), EQ-MVO-E1, E2; `verification/s46_*.py` (2 scripts, PASS; Jorion 1986 Tables 1–2 reproduced). ANG-47 new; ANG-44 extended. Exit met. Decision S46-D1 open.

### S4.7 Mean–variance family — PC-B1, B2, B3, B4, B6, B7
- **Methods:** B1 maximum Sharpe; B2 Black–Litterman; B3 robust MV; B4 resampled frontier; B6 Simple EPO; B7 Anchored EPO.
- **Sources:**
  - B1, B2, B6, B7: in hand (Black & Litterman 1992; He & Litterman; Idzorek; Pedersen, Babu & Levine 2021, both versions).
  - B4: in hand (Michaud & Michaud 2008 book).
  - **B3: Goldfarb & Iyengar 2003 (BI library)**; supporting Tütüncü & Koenig 2004 and Ceria & Stubbs 2006 (optional).
- **Equations:** EQ-MVO-3, EQ-MVO-5, EQ-EPO-1 … EQ-EPO-5, EQ-BL-1 … EQ-BL-3, EQ-ROB-1, EQ-ROB-2, EQ-REF-1.
- **Known so far:**
  - **BL:** weights from Σ (Idzorek) vs Σ + M̄⁻¹ (He & Litterman); Ω convention; τ (ANG-41, BL-1). Closed-form confidence Ω (IDZ-1). Both papers' examples already reproduce (`verification/s44_black_litterman_*.py`).
  - **REF:** patented and exclusively licensed (book p. 42); the D-2 IP check precedes implementation.
  - **EPO:** PBL tune the shrinkage w on trailing Sharpe (p. 127). That is an in-sample tuning rule, so its authority class and protocol need deciding (ADR-0027 D4).
- **Owner decisions expected:**
  - BL convention and Ω rule;
  - EPO shrinkage authority and tuning protocol;
  - robust-MV uncertainty set;
  - REF resampling count and seed, and the IP-check outcome.
- **Verification:** θ → 0 recovers MVO; PBL examples where feasible; robust MV as an SOCP; REF with seeded resampling; the BL reproductions.
- **Deliverable:** `S4_MVO_FAMILY.md` with a lineage diagram (MVO → estimation error → EPO).
- **Exit:** limits verified; ANG-vs-source differences recorded. If G&I has not arrived, B3 is completed last within the step.
- *[2026-10-08]* **Drafted:** `S4_MVO_FAMILY.md` (six method records, lineage, decisions S47-D1 … D6); register EQ-MVO-3b, EQ-MVO-5, EQ-EPO-1 … 5, EQ-BL-1 … 3, EQ-ROB-1 … 2, EQ-REF-1; `verification/s47_*.py` (5 scripts, PASS; Michaud Tables 5.1/6.1 and G&I calibration reproduced). New: ANG-48, ANG-49; source issues BL-2, MCH-1, PBL-1, PBL-2. Exit met.

### S4.8 Momentum signals — SIG-1 XSMOM, SIG-2 TSMOM
- **Sources:** in hand. Jegadeesh & Titman 1993; Moskowitz, Ooi & Pedersen 2012; Asness, Moskowitz & Pedersen 2013; Hurst, Ooi & Pedersen 2017; Daniel & Moskowitz 2016; Barroso & Santa-Clara 2015.
- **Equations:** EQ-SIG-1 … EQ-SIG-3.
- **Known so far:**
  - the Sørensen 12–1 momentum shares SIG-1's formation (`S4_SCORING_SORENSEN.md` §5);
  - PBL's XSMOM signal construction (eqs. 24–25);
  - ANG's AC-level "technical signals" are unspecified (ANG-23).
- **Owner decisions expected:** lookback and skip conventions; volatility-scaling estimator for TSMOM (short-horizon risk problem).
- **Verification:** constructions on synthetic series; sign and scale invariants.
- **Deliverable:** `S4_MOMENTUM.md`.
- **Exit:** construction contracts complete. Signals move on the signal ladder (`CONSTRUCTION EXTRACTED`).

### S4.9 Signal × PC compatibility
- **Scope:** which literature-supported objects a signal can become:
  - a signal;
  - a signal-conditioned universe;
  - an exposure rule;
  - an expected-return mapping;
  - a standalone strategy;
  - a tactical overlay.

  This is decided per pair with 1/N, 1/σ, MVO, Simple EPO, Anchored EPO and others. No combination is allowed without defined semantics; score → μ mappings are registered for S9d (RQ-33).
- **Deliverable:** `S4_SIGNAL_PC_COMPATIBILITY.md` (a matrix of valid / invalid / requires mapping).
- **Sync:** **SYNC-3** together with S4.10.

### S4.10 Anchor and benchmark architecture
- *[2026-10-08]* **Start by reminding the owner of S47-D3** (anchor for anchored EPO, PC-B7; candidates 1/N, 1/σ, market cap, `POL.benchmark`; `S4_MVO_FAMILY.md` §5).
- **Scope:** distinguish PC method · anchor source · benchmark definition · benchmark weights · comparison benchmark (taxonomy F-2, F-3). This includes a valid anchor contract (1/N, 1/σ, benchmark weights, other source-supported) and when the anchor equals the comparison benchmark.
- **Verification:** Anchored EPO with each anchor on synthetic data; anchor-invariance tests.
- **Deliverable:** `S4_ANCHOR_BENCHMARK.md`.
- **Exit:** contract stated; no index hard-coded.
- **Sync:** **SYNC-3**.

### S4.11 Risk-structured methods — PC-C1 … PC-C5
- **Methods:** C1 global minimum variance; C2 equal risk contribution; C3 HRP; C4 maximum diversification; C5 minimum correlation.
- **Sources:**
  - C2: in hand (Maillard–Roncalli–Teïletche working version; Spinu).
  - C3: in hand (López de Prado, reviewed).
  - C5: in hand (Varadi et al.; identity confirmed).
  - **C1: Clarke, de Silva & Thorley 2006 (BI).**
  - **C4: Choueifaty & Coignard 2008 (BI)**; supporting Choueifaty, Froidure & Reynier 2013 (optional).
- **Equations:** EQ-MVO-4, EQ-RS-1 … EQ-RS-5.
- **Known so far:**
  - **HRP:** the published algorithm is order-dependent; the tree-split variant is invariant (HRP-1, ANG-42); the numerical clipping requirement (HRP-2). Exhibit 7 already reproduces.
  - **ERC:** Spinu's solver is unique and deterministic.
  - **Minimum correlation:** two variants plus a rank power; the paper's example labels are swapped (ANG-38, MCA-1 … MCA-3).
  - **GMV:** long-only vs unconstrained.
- **Owner decisions expected:**
  - HRP V0 (published, with a canonical ordering) vs V1 (tree-split);
  - the minimum-correlation variant;
  - the GMV constraint set.
- **Verification:** ERC convergence; HRP determinism; equivalences (e.g. maximum diversification = GMV when correlations are equal); the existing `s44_*` scripts.
- **Deliverable:** `S4_RISK_STRUCTURED.md` (method records).
- **Exit:** verified.

### S4.12 Non-traditional methods — PC-D1 … PC-D4, and placement of PC-B5
- **Methods:** D1 CVaR; D2 maximum-drawdown-constrained; D3 tail-risk parity; D4 TPA two-factor; B5 mean–downside risk (placement and objective).
- **Sources:**
  - D2: in hand (Chekhlov–Uryasev–Zabarankin, reviewed).
  - D3: in hand (Boudt–Carl–Peterson, reviewed).
  - D4 concept and lead: in hand (Ang, Brandt & Denison 2014; AQR 2026; BI note).
  - B5: in hand (Sortino & van der Meer; scan).
  - **D1: Rockafellar & Uryasev 2000 (BI)**; supporting R&U 2002 (optional).
  - D4 primary sizing: **Treynor & Black 1973 (BI/JSTOR)**; Gilmore & Simonian 2025 (optional).
- **Equations:** EQ-NT-1 … EQ-NT-4, EQ-DS-1, EQ-DS-2.
- **Known so far:**
  - CVaR objective unclear (ANG-02);
  - absolute uncompounded drawdown vs ANG's relative limit, and infeasibility (ANG-40, CDD-2);
  - MCC vs ERC-CVaR, coskewness and cokurtosis objects, stochastic optimiser (ANG-39, BCP-2, BCP-3);
  - TPA: our own specification with a distinctness test against PC-B1, Anchored EPO and factor-MVO (amendment 14);
  - Sortino objective (ANG-18).
- **Owner decisions expected:** CVaR objective; drawdown definition and γ mapping; tail-risk object; TPA specification or merge; B5 objective.
- **Verification:** LP formulations on synthetic scenarios; CVaR → GMV under normality; the existing `s44_*` scripts; the TPA distinctness test.
- **Deliverables:** `S4_NON_TRADITIONAL.md`; TPA gap memo.
- **Exit:** verified, or an explicit gap.

### S4.13 Risk and covariance dependency inventory
- **Scope:** per PC method, the required risk representation (Σ, σ, semicovariance, scenarios, paths, factors, **coskewness and cokurtosis**), registered as risk objects per problem (ADR-0027 D3 r3). Estimator candidates are registered only; S10 selects.
- **Deliverable:** `S4_RISK_DEPENDENCIES.md`.
- **Exit:** every method's risk input typed.
- **Handoff:** → S10.

### S4.14 Agentic PC roles — PC-E1 Researcher (role), PC-E2 Adversarial Diversifier
- **Scope:**
  - Researcher: the research lane (ADR-0024 §1).
  - Adversarial Diversifier: complete formulation (budget, bounds, Sharpe definition, solver for maximising a convex function, determinism; ANG-16, I-5).
- **Sources:** ANG §3.3; Bera & Park 2008 (BI, optional; it is the Researcher's example).
- **Owner decisions expected:** the Adversarial Diversifier formulation choices.
- **Verification:** reference solver; orthogonality and Sharpe floor; a multiple-optima check.
- **Deliverable:** `S4_AGENTIC_PC.md`.
- **Exit:** contracts defined; open choices listed.

---

## 3. Owner decision points we can already see

| Step | Decision | Pre-identified options | Issue refs |
|---|---|---|---|
| S4.5 | Volatility targeting specification | Base portfolio; target; cash or leverage; estimator and horizon | ANG-14 |
| S4.5 | Inverse-vol / inverse-variance exponent | Fixed at ½ and 1 (recommended) vs parameter | ANG-13 |
| S4.5 | Asset-class capitalisation source | Data contract for S6 | ANG-46 (added at S4.5: S45-D3) |
| S4.5 | Heuristic universe and cash (added at S4.5) | Risky assets only vs cash as one of N | ANG-44 (S45-D4) |
| S4.6 | Risk-free and cash treatment | Cash as an asset vs a risk-free rate | ANG-44 (S46-D1) |
| S4.7 | Black–Litterman convention | Σ vs Σ + M̄⁻¹; Ω rule; closed-form confidence | ANG-41, BL-1, IDZ-1 |
| S4.7 | EPO shrinkage authority and tuning | Fixed vs system-estimated under the S7 protocol | ADR-0027 D4 |
| S4.7 | Resampled frontier | IP check (D-2); resampling count and seed | D-2 |
| S4.7 | Robust MV uncertainty set | Ellipsoidal / box; size authority | ANG-48 (S47-D4) |
| S4.7 | Cash/risky split (carried from S46-D1) | Engine-level rule vs per method | S47-D6 |
| S4.11 | HRP version | V0 published with canonical order vs V1 tree-split | ANG-42, HRP-1 |
| S4.11 | Minimum-correlation variant | MinCorr / MinCorr2; rank power | ANG-38, MCA-1 … 3 |
| S4.11 | GMV constraint set | Long-only vs unconstrained | — |
| S4.12 | CVaR objective | Min-CVaR / mean–CVaR / return subject to CVaR | ANG-02 |
| S4.12 | Drawdown definition and limit mapping | Absolute uncompounded (LP) vs relative compounded | ANG-40, CDD-2 |
| S4.12 | Tail-risk parity object | MCC vs ERC on modified CVaR | ANG-39 |
| S4.12 | TPA | Own specification after the distinctness test, or merge/relocate | Amendment 14 |
| S4.12 | Sortino objective | Max Sortino / mean–semivariance / downside deviation subject to a floor | ANG-18 |
| S4.14 | Adversarial Diversifier formulation | Budget, bounds, Sharpe definition, solver | ANG-16 |

---

## 4. Source acquisitions by step

| Needed by | Item | Route | Blocking? |
|---|---|---|---|
| S4.7 | Goldfarb & Iyengar (2003), *Robust Portfolio Selection Problems*, Math. Oper. Res. 28(1):1–38 | BI library (owner) | **In hand 2026-10-08** |
| S4.11 | Clarke, de Silva & Thorley (2006), *Minimum-Variance Portfolios in the U.S. Equity Market*, JPM 33(1):10–24 | BI library (owner) | **In hand 2026-10-08** (sixth upload; image scan, article complete). CdST 2011 kept as supporting |
| S4.11 | Choueifaty & Coignard (2008), *Toward Maximum Diversification*, JPM 35(1):40–51 | BI library (owner) | **In hand 2026-10-08** |
| S4.12 | Rockafellar & Uryasev (2000), *Optimization of Conditional Value-at-Risk*, J. Risk 2(3):21–41 | BI library (owner) | **In hand 2026-10-08** (author version; published governs) |
| S4.12 | Treynor & Black (1973), *How to Use Security Analysis to Improve Portfolio Selection*, J. Business 46(1) | BI / JSTOR | **In hand 2026-10-08** |
| Optional | Jagannathan & Ma 2003 (S4.6); Kan & Zhou 2007 (S4.6); Tütüncü & Koenig 2004, Ceria & Stubbs 2006, Scherer 2002 (S4.7); Choueifaty, Froidure & Reynier 2013 (S4.11); Rockafellar & Uryasev 2002, Boudt, Peterson & Croux 2008, Gilmore & Simonian 2025 (S4.12); Bera & Park 2008 (S4.14); Meucci 2009 (open SSRN; S4.16) | BI / SSRN | No |

---

## 5. Tracker (updated at the end of every step)

| Step | Methods | Status | Last update | Next action |
|---|---|---|---|---|
| S4.5 | A1–A5 | **Done** | 2026-10-08 | Owner accepted S45-D1 … D4 as recommended |
| S4.6 | MVO foundation | **Done** | 2026-10-08 | Owner decided S46-D1 (option (a), refined); BSU idea on hold (RQ-57) |
| S4.7 | B1, B2, B3, B4, B6, B7 | **Done** | 2026-10-08 | Owner decided S47-D1 … D6 (engine-level risk target, B-46) |
| S4.8 | SIG-1, SIG-2 | **Next** | 2026-10-08 | Start: read MOP 2012, AMP 2013, HOP 2017; extract SIG constructions |
| S4.9 | Signal × PC | Not started | — | — |
| S4.10 | Anchors, benchmarks | Not started | — | **Remind the owner first: S47-D3, the anchor for anchored EPO (PC-B7)** |
| S4.11 | C1–C5 | Not started (C2, C3, C5 sources reviewed or reproduced in S4.4) | — | — |
| S4.12 | D1–D4, B5 | Not started (D2, D3 sources reproduced in S4.4) | — | — |
| S4.13 | Risk dependencies | Not started | — | — |
| S4.14 | E1 role, E2 | Not started | — | — |

**After Section 2:** S4.15 upstream CMA and signal inventory (ANG's seven CMA candidates, judge, regime) · S4.16 CRO diagnostics and candidate card · S4.17 deliberation requirements · S4.18 CIO ensembles · S4.19–S4.24 consolidation · S4.25–S4.27 → **G4**.
