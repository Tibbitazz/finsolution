# S4.10 Anchors and benchmarks: what the engine anchors to, what it is judged against, and how they stay feasible

**Document status:** REVIEWED · **S4.10 DONE (2026-10-18).** Owner decisions S410-D1 … S410-D6 accepted as recommended, 2026-10-18 (§10). · **Basis:**
- S4_PLAN §G (step S4.10; SYNC-3 with S4.9); owner decision S47-D3 (anchor for PC-B7 deferred to this step; reminder given 2026-10-18);
- taxonomy findings F-2 ("anchor" is a use, not a method type) and F-3 (a benchmark is a definition plus its weights and returns) (`S4_TAXONOMY.md`);
- ADR-0024 §4 (allocation domains), §7 (EPO in the MVO lineage); ADR-0025 (admission ≠ evaluation); ADR-0027 D3, D5 (one risk model per problem; declared units); EQ-SPLIT-1 (S47-D6) and its S49-D3 note;
- S4.9 results: relative signals take their level from the anchor; the anchor is the reference portfolio of the transfer coefficient (EQ-TC-1);
- RQ-09 note of 2026-10-15 (60/40); Policy Statement field `POL.benchmark` (S1 field 10.3: comparison and evaluation, "pending until S7");
- registry fact `no.wrapper.ask.eligible_holdings` (Skatteetaten; V-full, verified 2026-10-01).

**Related files:** `verification/s410_anchor_benchmark.py` (PASS); register entries EQ-ANC-1, EQ-FEAS-1, EQ-TEV-1, EQ-TEV-2, EQ-GRS-1 (`S4_EQUATION_REGISTER.md`); issues ROLL-1, GKA-1 (`ANG_ISSUES_REGISTER.md`).

**Exit criterion (S4_PLAN):** contract stated; no index hard-coded. **Nothing here selects a benchmark for evaluation** (S7, G7) or says an anchor performs well (S7).

---

## 0. Summary

1. **Six objects, kept apart** (§2): the PC method's anchor slot · the anchor source · the benchmark definition · the benchmark's weights and returns · the comparison benchmark · the simple control.
2. **Where an anchor enters** (§3): anchored EPO (B7), Black–Litterman's equilibrium (B2), TPA's reference portfolio (D4), benchmark-relative candidates, and the transfer-coefficient reference. In B7 the anchor is what the method holds when the signal has nothing to say (verified: w = 1 returns the anchor; an anchor-consistent signal returns it at every w).
3. **An anchor contract** (§4, AC-1 … AC-7): declared rule, same universe and units as the problem, point-in-time, feasible, risk from the authoritative model, rebalancing stated, no hard-coded index.
4. **Feasibility** (§5). The 60/40 benchmark is not holdable inside an ASK: bond funds, high-yield funds and bond ETFs fall below the 80% share requirement (registry fact). A household-level anchor is feasible exactly when a transportation problem is feasible (verified against the supply–demand cut condition). Example: with 70% of wealth in an ASK, 60/40 is infeasible for the household; with 60% or less it is feasible.
5. **Benchmark-relative optimisation** (§6, Roll 1992; Jorion 2003, both verified): minimising tracking error ignores total risk. The optimal deviations do not depend on the benchmark; with an inefficient benchmark the result is inefficient by the same variance distance and has beta above 1. Adding a total-risk constraint costs little return (Jorion Table 2). The engine already has a total-risk target (EQ-SPLIT-1); benchmark-relative candidates must carry it inside.
6. **Benchmarks are rarely efficient** (§7; Grinold & Kahn ch. 20, GRS test): an anchor is a prior, not "the efficient portfolio".
7. **Anchor candidates** (§8, S47-D3): 1/N and 1/σ (PBL's tested anchors), market capitalisation (BL equilibrium), `POL.benchmark`. Recommended default: `POL.benchmark` where declared and feasible, otherwise 1/σ; market capitalisation for security sleeves.

---

## 1. Sources (stage 1)

| Source | Status | Used for |
|---|---|---|
| PBL 2021, eqs. (12)–(22), Props. 1–3; Table 1, p. 135, and p. 136 (Equity 6: anchor 1/N; Equity 7: anchor 1/σ) | In hand; S4.7 | Anchored EPO; anchor as benchmark, 1/N heuristic, strategic allocation or typical portfolio (pp. 127, 131) |
| Black & Litterman 1992 | In hand; S4.7 | Market portfolio as the equilibrium anchor (EQ-BL-1) |
| Sharpe 1964 | In hand; S4.5 | Reverse optimisation (EQ-H-2a) |
| **Roll (1992)**, "A Mean/Variance Analysis of Tracking Error", *JPM* 18(4):13–22 | **In hand 2026-10-18** (scan; read in full) | Tracking-error-variance (TEV) optimisation; beta; equidistance; beta constraint |
| **Jorion (2003)**, "Portfolio Optimization with Tracking-Error Constraints", *FAJ* 59(5):70–82 | **In hand 2026-10-18** (read in full) | Constant-TEV ellipse; total-risk constraint and its cost; Tables 1–3 |
| Grinold & Kahn, *Advances in Active Portfolio Management*, ch. 20 (Grinold 1992, revised October 2018) | In hand | Benchmark efficiency (GRS test); SR²_H = SR²_B + IR²_H |
| Michaud & Michaud 2008 ch. 9 | In hand (read 2026-10-15) | Benchmark-relative optimisation as total-return optimisation with slack benchmark constraints (RQ-09 note) |
| ANG v2 (S4.1) | In hand | 60/40 as performance benchmark and a hard ex-ante TE ≤ 6% constraint ([P] pp. 14–15) |
| Gibbons, Ross & Shanken (1989), *Econometrica* 57 | Not in hand (cited through G&K) | GRS test |

---

## 2. The objects

| Object | Definition | Type (taxonomy) | Authority | Consumers |
|---|---|---|---|---|
| **Anchor slot** | The input of a PC method that takes a reference portfolio (§3) | Part of the method's contract | Method contract (S4.20) | B7, B2, D4, benchmark-relative candidates; EQ-TC-1 |
| **Anchor source** | A rule that produces a weight artefact for the slot: 1/N, 1/σ, market capitalisation, `POL.benchmark` weights (§8) | Relation `anchors` (F-2); no anchor type | Per S410-D2/D3 | The slot |
| **Benchmark definition** | Constituents, weighting rule, rebalancing, currency and hedging basis, total-return convention | C.BENCHMARK (F-3) | User (`POL.benchmark`), within options set at S7 | S7, S14, S16 |
| **Benchmark weights and returns** | Point-in-time series produced from the definition | IN or A artefacts (F-3) | Data (S6) | Anchors that use the benchmark; evaluation |
| **Comparison benchmark** | The benchmark a candidate or the engine is judged against | Use of a benchmark definition | S7 protocol; `POL.benchmark` | S7, S14, S16 |
| **Simple control** | The simple method the engine must beat to justify its complexity (RQ-25) | Evaluation design | S7 | S7, S15 |

The same portfolio may fill several roles (e.g. the user's 60/40 as comparison benchmark and as anchor), but each role is declared separately and checked by its own rule.

---

## 3. Where an anchor enters

| Slot | How the anchor enters | Verified properties |
|---|---|---|
| **PC-B7 anchored EPO** (EQ-EPO-3) | μ̃ = (1 − w)s + wγVa with shrunk Σ_w; γ from eq. (21) equalises the risk of the signal portfolio and the anchor | w = 1 returns the anchor; an anchor-consistent signal s = γΣa returns the anchor at every w (reverse MVO); eq. (21) risk matching exact; at w = 0 the direction is anchor-free and the scale equals σ(a); different anchors give materially different portfolios at intermediate w |
| **PC-B2 Black–Litterman** (EQ-BL-1) | Π = δΣw_eq, w_eq = market capitalisation in BL 1992 | PBL Prop. 3: anchored EPO ≡ BL with Π = γΣa (verified at S4.7) |
| **PC-D4 TPA** | Reference portfolio w_ref (S4.12) | S4.12 |
| **Benchmark-relative candidates** | The benchmark q_B in tracking-error terms | §6 |
| **EQ-TC-1 transfer coefficient** | Reference portfolio for active weights | S4.9 §4a |
| PC-A5 base portfolio (S45-D1) | Not an anchor, but the same feasibility rule applies | — |

**Relative signals take their level from the anchor.** A cross-sectionally centred signal (XSMOM) has zero mean; with the 1/N anchor, the anchor-weighted expected return of μ̃ comes entirely from the anchor term (verified). Absolute signals (TSMOM) carry their own level (S4.9 §6).

---

## 4. Anchor contract (proposed; S410-D1)

| ID | Condition |
|---|---|
| AC-1 | **Declared rule and authority.** The anchor is a rule (1/N, 1/σ, market capitalisation, `POL.benchmark`) with a declared parameter authority (§10, S410-D3). |
| AC-2 | **Same problem.** Same universe, numéraire, horizon and units as the problem's authoritative risk model (ADR-0027 D3, D5). Weights over the problem's risky assets, cash explicit, summing to 1. |
| AC-3 | **Point-in-time.** Computable from data dated ≤ t (capitalisations, volatilities from the authoritative risk model at t). |
| AC-4 | **Feasible.** Holdable in the problem under account eligibility, long-only and Policy Statement bounds (§5). If not, either the problem is defined at household level and passes the feasibility check (EQ-FEAS-1), or the anchor is projected by a declared rule and the gap is reported. Never silent. |
| AC-5 | **Risk from the authoritative model.** σ(a) enters eq. (21); it is computed in the problem's risk model, never estimated separately. |
| AC-6 | **Rebalancing stated.** The anchor is a target-weight portfolio at the run date unless the source says otherwise (e.g. a buy-and-hold cap-weighted index drifts). |
| AC-7 | **No hard-coded index.** Named indices enter only through `POL.benchmark` or a data-defined rule (market capitalisation). |

---

## 5. Feasibility of anchors and benchmarks

### 5.1 The 60/40 benchmark and the ASK

**Fact (registry `no.wrapper.ask.eligible_holdings`, Skatteetaten, V-full):** an ASK may hold shares in companies domiciled in the EEA, units in securities funds domiciled in the EEA whose share component exceeds 80% at the start of the income year, and cash (no interest accrues). Money-market funds are excluded; bonds are outside the permitted set.

Consequences:
- Bond funds, high-yield bond funds and bond ETFs have a share component far below 80%, so they are **not ASK-eligible**.
- A portfolio of 60% shares and 40% equity funds is about 100% equities. It is not a 60/40 portfolio in the risk sense (verified: 15.8% volatility against 10.0% for the synthetic 60/40).

Projections of a 60/40 anchor onto the ASK-feasible set (synthetic universe, `s410_anchor_benchmark.py`):

| Projection | Composition | Volatility |
|---|---|---|
| The 60/40 anchor itself | 60% equities, 30% government bonds, 10% high yield | 10.0% |
| (i) Renormalise eligible weights | 100% equities | 15.8% |
| (ii) Ineligible weight to cash | 60% equities, 40% cash | 9.5% |
| (iii) Risk-matched equities + cash | 63.5% equities, 36.5% cash | 10.0% |

(i) changes the anchor's risk by more than half; (ii) and (iii) preserve the anchor's role as a risk reference. Cash in an ASK earns nothing, so (ii) and (iii) give up the bonds' yield.

### 5.2 Household-level feasibility (EQ-FEAS-1)

When the problem spans several accounts (S5 decides the allocation hierarchy; S13a decides asset location), an anchor with class weights a_j is feasible exactly when a transportation problem is feasible: each account's wealth W_k is fully allocated, each class weight is met, and no account holds an ineligible class. By the supply–demand theorem this holds if and only if, for every set J of classes, Σ_{j∈J} a_j ≤ the wealth of the accounts eligible for at least one class in J. Verified: LP feasibility equals the cut condition in 300 random cases.

Example (ASK plus an ordinary share account, both with cash): the 60/40 needs 40% of total wealth in bond-capable accounts. With 70% of wealth in the ASK it is infeasible; with 60% or less it is feasible.

---

## 6. Benchmark-relative optimisation (Roll 1992; Jorion 2003)

| Result | Source | Verified |
|---|---|---|
| The tracking-error-variance (TEV) optimal deviation x = D(q₁ − q₀), D = G/(R₁ − R₀), does not depend on the benchmark | Roll eq. (1), A.1; Jorion (B3) | Yes, three benchmarks |
| Tracking variance T = D²(σ₁² − σ₀²); total variance σ²_P = σ²_B + T + 2Dσ₀²(R_B/R₀ − 1); β = 1 + D(σ₀²/σ²_B)(R_B/R₀ − 1) | Roll eqs. (2)–(4) | Yes |
| If the benchmark's mean exceeds the global-minimum-variance mean, every TEV portfolio with positive target has β > 1; every portfolio that dominates the benchmark has β < 1 | Roll A.3, A.5 | Yes (2,000 random portfolios) |
| The TEV frontier is the efficient frontier shifted by a constant variance: σ²_B − σ²_B* = σ²_P − σ²_P* | Roll A.4 | Yes |
| A beta constraint makes the deviation depend on the benchmark (x = γ₁q₁ + γ₀q₀ + γ_Bq_B) and can dominate | Roll eq. (5), A.6 (ROLL-1: sign slip in A-10) | Yes, β ∈ {0.9, 1.0, 1.1} |
| Constant-TEV portfolios lie on an ellipse in (σ², μ) space; IR of the TEV frontier = √d | Jorion (B4), (C6) | Yes, by numerical optimisation |
| Constraining total risk to the benchmark's costs little return: at 4% TEV, Δ₁ = 2%, σ_MV = 8%, return falls 0.29 pp while risk falls 1.65 pp (ratio 0.18 against an IR of 0.5) | Jorion Table 2, (C17) | Yes, full Table 2 to rounding (σ_B = 13.76%) |
| Jorion's prescription: focus on total risk; if TEV limits stay, add a total-risk constraint | Jorion, Conclusions | — |

**Engine implications:**
- The engine already sets total risk through EQ-SPLIT-1. A benchmark-relative candidate that optimises excess return must carry the total-risk constraint **inside** its optimisation (EQ-SPLIT-1's exception for methods with absolute risk limits). Rescaling afterwards would change its tracking error.
- ANG imposes a hard ex-ante TE ≤ 6% against 60/40. Under Roll and Jorion a TE limit is acceptable as a constraint, not as the objective, and only together with total-risk control.
- Information ratios are reported together with total risk and beta (Roll), never alone (Jorion: part of the IR of a TEV portfolio can be obtained by leveraging the benchmark; Table 1: 60 of 200 bp).

---

## 7. Benchmark efficiency (Grinold & Kahn ch. 20; GRS)

- **Identity (verified ex ante and in the chapter's Exhibit 5):** SR²_H = SR²_B + IR²_H, where H is the maximum-Sharpe portfolio of the benchmark plus the test assets. A benchmark is efficient exactly when no test asset has alpha against it.
- **Evidence:** with four Barra tilt portfolios (volatility, momentum, size, value), the S&P 500, FTA, ALL ORDS and TOPIX were inefficient over 1973–1991; the DAX was not significantly so.
- **Consequence for anchors:** an anchor is a prior. Reverse-optimised returns from an inefficient benchmark pull the portfolio toward the benchmark's inefficiency; anchored EPO's w controls how hard.
- **GKA-1:** the 2018 edition counts the benchmark among the N assets (N = 5). Under GRS the benchmark is not a test asset (its alpha is zero by construction), so N = 4, as in the 1992 original. The printed F statistics match N = 4; the N and T − N − 1 columns do not. A null simulation confirms N = 4 has the right size (≈ 5%) and N = 5 under-rejects. Conclusions unchanged.
- **Candidate diagnostic** (registered, not adopted): the GRS test of `POL.benchmark` against the investable set, for S7 evaluation design and S16 monitoring.

---

## 8. Anchor candidates (S47-D3)

| Candidate | Source support | Data | Behaviour at asset-class level | Feasibility |
|---|---|---|---|---|
| **1/N** | PBL Equity 6 (tested); PBL p. 127 (1/N as an investor's heuristic anchor) | None | Risk concentrated in volatile classes | Any universe the problem holds |
| **1/σ** | PBL Equity 7 (tested); the fully shrunk simple EPO with TSMOM signals (PBL-3) | σ from the authoritative model | Equal standalone risk; bonds heavily weighted | Same |
| **Market capitalisation** | BL 1992 (equilibrium); PBL Prop. 3 | Security level: capitalisations (S6). Asset-class level: global market-portfolio weights (no source in hand; a lead from memory: Doeswijk, Lam & Swinkels 2014) | The equilibrium prior | Same |
| **`POL.benchmark`** | PBL pp. 127, 131 (the investor's benchmark) | Benchmark weights (S6) | The user's own reference | Must pass §5 |
| Previous approved target (strategic allocation) | PBL p. 131 (strategic asset allocation, typical portfolio) — exogenous in PBL | Engine output | Self-referential for the SAA problem | Only for a sub-problem whose upstream target is approved (e.g. a sleeve anchored to its approved class weight) |

---

## 9. The roles of 60/40 (RQ-09)

| Role | Assessment | Proposal |
|---|---|---|
| Comparison benchmark (evaluation, report, monitoring) | FITS (ANG) | Only through `POL.benchmark`; never a hard-coded default |
| Anchor | Possible where feasible | Through the anchor contract (AC-4); for an ASK-only problem, projected (§5.1) |
| Tracking-error objective | PARTIAL (Roll; Jorion) | Not an objective; a TE limit only as a constraint with total-risk control |
| Simple control | Not this object | S7 decides the control (RQ-25) |

---

## 10. Owner decisions (stage 6)

*[2026-10-18]* **Owner decision: S410-D1 … D6 accepted as recommended** ("I agree to the D points"). The owner's follow-up on 60/40 across an ASK and an ordinary account (AF) is the household case of §5.2: feasible while the AF holds at least 40% of the combined wealth.

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **S410-D1** | Object separation (§2) and anchor contract AC-1 … AC-7 (§4) | (a) accept · (b) amend | **(a)** |
| **S410-D2** | Admissible anchor sources for B7 (and the equilibrium source for B2, the reference for D4) | (a) 1/N, 1/σ, market capitalisation where data permit, `POL.benchmark` when feasible; previous approved target only for sub-problems with an approved upstream target · (b) (a) plus the previous target for the SAA problem · (c) a single fixed anchor | **(a).** (b) makes the SAA anchor itself; (c) contradicts F-2 and the "no hard-coded index" exit |
| **S410-D3** | Default anchor and authority | (a) SAA problem: `POL.benchmark` where declared and feasible, otherwise 1/σ; security sleeves: market capitalisation of the sleeve universe, otherwise 1/N. The user may choose any admissible source (user-authorized); the default is system-set · (b) 1/N everywhere · (c) 1/σ everywhere | **(a).** It ties the anchor to the user's stated reference where one exists, falls back to PBL's risk-balanced anchor, and keeps BL's equilibrium for securities |
| **S410-D4** | Infeasible anchors and benchmarks | (a) household-level problems check EQ-FEAS-1; an account-level problem projects an infeasible anchor by moving ineligible weight to cash (§5.1 (ii)), reporting the risk gap; a `POL.benchmark` infeasible for the household raises a Policy Statement conflict record (ADR-0014 declared → effective) · (b) projection (iii) risk-matched · (c) renormalise | **(a).** (ii) is transparent and keeps the risk role within half a point here; (c) changes risk by more than half |
| **S410-D5** | Roles of 60/40 (any benchmark) | (a) as §9 · (b) also a TE objective | **(a)** |
| **S410-D6** | Benchmark-relative candidates | (a) total-risk constraint inside every benchmark-relative optimisation (Jorion); TE only as a constraint; IR reported with total risk and beta (Roll) · (b) TE objective allowed | **(a)**, recorded as an EQ-SPLIT-1 exception-list clarification at G4 |

---

## 11. Verification (stage 7)

| Script | Proves | Result |
|---|---|---|
| `s410_anchor_benchmark.py` | Anchored EPO with four anchors (w = 1; anchor-consistent signals; eq. 21; w = 0; level for centred signals); ASK infeasibility of 60/40 and three projections; household feasibility LP = supply–demand cut condition (300 random cases); Roll eqs. (1)–(5), A.4–A.6, fn. 10 (ROLL-1); Jorion (B3)–(B6), ellipse (C6) and (C17) by numerical optimisation, Tables 1–3 and Theorems 2a–2d reproduced; GRS identity, Exhibit 5 identity, Exhibit 6 F with N = 4 (GKA-1), null-size simulation | PASS |

---

## 12. Handed forward

| To | Item |
|---|---|
| S4.12 | PC-D4 TPA reference portfolio under the anchor contract |
| S4.16 | Report IR with total risk and beta; anchor-feasibility and projection gaps on the candidate card |
| S4.20 | Anchor slot and AC-1 … AC-7 as contract fields; EQ-SPLIT-1 exception clarification (S410-D6) |
| S5 | Allocation hierarchy (account vs household problem); `POL.benchmark` option sets |
| S6 | Benchmark weights and returns; capitalisations; global market-portfolio weights for an asset-class cap anchor |
| S7 | Comparison benchmark and simple control (RQ-25); GRS as a candidate evaluation diagnostic (N = test assets excluding the benchmark) |
| S13a | Asset location consistent with EQ-FEAS-1 |
| S16 | GRS-type monitoring of benchmark efficiency (candidate) |
| G4 | S410-D6 clarification of EQ-SPLIT-1, with B-46 and S49-D3 |
