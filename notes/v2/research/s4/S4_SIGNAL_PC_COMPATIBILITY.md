# S4.9 Signal × PC compatibility: what a momentum signal may become, method by method

**Document status:** DRAFT (2026-10-15), awaiting owner decisions S49-D1 … S49-D5 (§7). · **Basis:**
- S4_PLAN §G (step S4.9), amendment 4 (momentum roles open until S4.8/S4.9), §D.1 (candidate "signal-conditioned heuristics"), SYNC-3 (with S4.10);
- `S4_MOMENTUM.md` (S4.8; decisions S48-D1 … D6; S48-D3 carried here);
- ADR-0012 (signals are descriptors; μ only through an accepted mapping, §3); ADR-0024 §1, §4 (research lane; allocation domains); ADR-0025 (admission ≠ evaluation); ADR-0026 §8 (evidence by use); ADR-0027 D3; EQ-SPLIT-1 (S47-D6).

**Related files:** `verification/s49_signal_pc_compatibility.py` (PASS); register entries EQ-MAP-1 … EQ-MAP-4 (`S4_EQUATION_REGISTER.md`); RQ-33 (score → μ), RQ-17 (tactical role), RQ-32 (aggregation).

**Scope:** for every pairing of a momentum signal with a roster method, is the construction *defined* and *source-supported*? **Nothing here says a pairing is good** (S7). The exit criterion: no combination without semantics.

---

## 0. Summary

1. **Six objects** (amendment 4), each with its own semantics: O1 evidence descriptor · O2 signal-conditioned universe · O3 direction/exposure rule · O4 expected-return mapping · O5 standalone sleeve · O6 tactical overlay (§2).
2. **The roster splits by input.**
   - **μ-free methods** (A1–A5, C1–C5, D3, min-CVaR) can use a signal only through *selection* (O2), *direction* (O3) or as a *sleeve* (O5), never through μ.
   - **μ-consuming methods** (B1–B7, D2, D4, mean–CVaR, E2) can use it only through a *mapping* to returns (O4). B6/B7 (EPO) are the source-native route; for the others the mapping must be accepted at S9d.
3. **Source-supported compositions** (§3):
   - 1/N or cap weights within a momentum-selected set (JT deciles; AMP terciles);
   - sign × 1/σ (MOP; HOP), i.e. TSMOM is PC-A3 with a direction rule;
   - EPO with momentum signals (PBL eqs. 23–27; EPO w = 0 is MVO on the signal, w = 1 is TSMOM's sign × 1/σ);
   - 1/N across factor portfolios including momentum (DGU Table 2, dataset 7).
4. **The §D.1 candidate "signal-conditioned heuristics" is literature-supported but not a distinct method:** it is a composition (O2 or O3 × A1/A2/A3). No roster change (§5).
5. **Two rules the engine needs** (verified):
   - **unscaled scores never enter an optimizer.** Ranks fed to MVO give weights that depend on an arbitrary rank origin. The mapping α = IC·σ·z is invariant to relabelling, and units must match (a factor 12 otherwise; Michaud & Michaud pp. 109–111);
   - **a direction rule acts after the engine-level risk scaling.** Otherwise a risk-off state is levered back up: with 2 of 10 assets in an uptrend, exposure is 0.19 if the rule follows the scaling and 0.69 if it precedes it.
6. **S48-D3 resolved here as a proposal:** strategy-level scaling (B&SC, DM) applies only to O5 sleeves. A long–short sleeve exists only where the account permits shorting (§7, S49-D2).

---

## 1. Sources (stage 1)

No new governing source. Used:
- S4.8 sources (`S4_MOMENTUM.md` §1);
- PBL 2021 eqs. (8), (23)–(27), Props. 2–3 (pp. 129–137);
- Michaud & Michaud 2008 ch. 12, pp. 109–111 (scaling forecasts: "relative valuations need scaling"; IC × expected volatility, after Ambachtsheer 1977; consistent units; the index-weighted sum of active returns is zero);
- DeMiguel, Garlappi & Uppal 2009 Table 2, p. 1918 (datasets include MKT/SMB/HML and MKT/SMB/HML/UMD portfolios as assets);
- Treynor & Black 1973 (appraisal-ratio sizing for PC-D4);
- Black & Litterman 1992 (views).

Grinold (1989) and Grinold & Kahn (1999) are not in hand. The α-scaling rule rests on Michaud & Michaud's statement of it.

---

## 2. The six objects

| ID | Object | Semantics | Source support | Owner of the use |
|---|---|---|---|---|
| O1 | **Evidence descriptor** | The signal as a fact agents may cite (R8); no weight effect by itself | ADR-0012; ADR-0026 §8 | All roles; S8/S12 |
| O2 | **Signal-conditioned universe** | The signal selects the set (e.g. top tercile or decile by XSMOM; positive TSMOM); a μ-free method weights within it | JT 1993 (equal-weighted deciles); AMP 2013 (terciles: value-weighted for stocks, equal-weighted otherwise); DM 2016 (value-weighted deciles) | S4.9 → S11 |
| O3 | **Direction / exposure rule** | Per asset, the signal sets the sign (long/short) or, long-only, hold vs cash, applied to a base weight | MOP 2012 eq. (5); HOP 2017 (sign × equal volatility); long-only cash version derived (shorts → 0) | S4.9 → S11; timing use → S13c |
| O4 | **Expected-return mapping** | The signal becomes μ (or α) in return units, consumed by a μ-based method | PBL eqs. (23)–(27); Michaud & Michaud ch. 12 (α = IC·σ·score); BL views (Q from signals; PBL Prop. 3) | S9d (RQ-33) |
| O5 | **Standalone sleeve** | A momentum portfolio (WML, TSMOM factor, long-only winners, factor-momentum rotation) held as an asset of the allocation | DGU Table 2 (factor portfolios incl. UMD as assets); MOP/AMP factor portfolios; B&SC/DM scaling | S4.9 → S11; account permissions |
| O6 | **Tactical overlay / timing evidence** | The signal informs *when and how* to implement an approved target, inside the Trader's mandate; never changes w* | ADR-0026 §5, §8.9; HANDOFF §4.6 (TSMOM as logged timing evidence) | S13c–d (RQ-17, RQ-35) |

The **blend-weight layer** (factor momentum varying the composite's factor weights, S48-D6) sits *before* any PC method, in score aggregation (RQ-32). It is not a pairing with a method.

---

## 3. Compatibility matrix

Codes: **V** = defined and source-supported · **V1** = defined, derived from a sourced rule (variant) · **M** = requires a mapping accepted at S9d (O4) or a CMA for the sleeve (O5) · **D** = defined but no source in hand (research lane only, ADR-0024 §1) · **—** = no semantics (invalid). O1 is valid for every method; O6 is not a PC pairing (S13).

| Method | Input class | O2 conditioned universe | O3 direction rule | O4 μ mapping | O5 sleeve as asset |
|---|---|---|---|---|---|
| PC-A1 1/N | μ-free | **V** (JT EW deciles; AMP EW terciles) | D (sign × equal notional) | — | **V** (DGU dataset 7: factor portfolios incl. UMD) |
| PC-A2 cap weight | μ-free, capitalisations | **V** (DM VW deciles; AMP VW stock terciles) | — (cap weights have no sign) | — | — (a strategy has no capitalisation) |
| PC-A3 1/σ | μ-free | **V1** (long-only TSMOM: positive-trend set at 1/σ) | **V** (MOP eq. 5; HOP: TSMOM = A3 with signs) | — | V (sleeve as asset) |
| PC-A4 1/σ² | μ-free | D | D | — | V |
| PC-A5 volatility targeting | μ-free, time-varying | — | — | — | **V** (B&SC = A5-type scaling of a momentum sleeve; S48-D3) |
| PC-B1 max Sharpe | μ + Σ | D (mixes a selection with other beliefs; not recommended) | — | **M** (PBL Prop. 3: EPO w = 0 = MVO on s) | M (CMA for the sleeve) |
| PC-B2 Black–Litterman | μ + Σ + views | — | — | **M** (Q = mapped signal; PBL Prop. 3: EPO ≡ BL with Π = γΣa, Q = s, P = I, Ω = Λ) | M |
| PC-B3 robust MV | μ + Σ + uncertainty | — | — | **M** (PBL Prop. 2: ellipsoidal robust ≡ EPO) | M |
| PC-B4 resampled frontier | μ + Σ | — | — | **M** (Michaud ch. 12 scaling) | M |
| PC-B5 mean–downside | μ + scenarios | — | — | M | M |
| PC-B6 simple EPO | signal s + Σ | — | — | **V** (PBL eqs. 23–27: signal-native) | M |
| PC-B7 anchored EPO | signal s + Σ + anchor | — | — | **V** (PBL; anchor at S4.10) | M |
| PC-C1 GMV | Σ only | D | D | — | V |
| PC-C2 ERC | Σ only | D | D | — | V |
| PC-C3 HRP | Σ only | D | — | — | V |
| PC-C4 max diversification | Σ only | D | — | — | V |
| PC-C5 min correlation | Σ only | D | — | — | V |
| PC-D1 CVaR | scenarios (± μ) | D (min-CVaR) | — | M (mean–CVaR; ANG-02 open) | V / M |
| PC-D2 drawdown-constrained | μ + paths | — | — | M | M |
| PC-D3 tail-risk parity | scenarios | D | — | — | V |
| PC-D4 TPA | α + residual risk | — | — | **M** (Treynor–Black α/σ²_ε with α = IC·σ_ε·z) | — |
| PC-E2 adversarial diversifier | Σ + Sharpe floor (μ) | — | — | M (ANG-16 open) | M |
| PC-E1 Researcher | role | Proposes new compositions through the research lane | | | |

**How to read a μ-free method with O5:** the sleeve's return history enters the authoritative risk model as one more asset (ADR-0027 D3). A long-only momentum sleeve overlaps the equity sleeves it is drawn from, so the allocation double-counts equity exposure unless the sleeve is defined as an active (relative) return (S11).

---

## 4. Rules derived (verified in `s49_signal_pc_compatibility.py`)

| ID | Rule | Basis | Check |
|---|---|---|---|
| R-1 | **No unscaled score enters a μ-consuming method.** Ranks or raw scores fed as μ give weights that depend on arbitrary choices (rank origin, centring) | Michaud & Michaud p. 109 ("relative valuations need scaling") | MVO weights on ranks 1…N, 0…N−1 and centred ranks differ by > 0.1 |
| R-2 | **Mappings are in return units, per period consistent with Σ, and benchmark-neutral when used as active α** (index-weighted α sums to zero) | Michaud & Michaud pp. 110–111 | α = IC·σ·z is invariant to affine relabelling and to monotone transforms of ranks; mixed monthly/annual units misstate weights by a factor 12; neutralisation w_b′α = 0 |
| R-3 | **μ-free methods use a signal only through O2, O3 or O5** | Input classes (§3) | — |
| R-4 | **A direction rule acts after the engine-level scaling (EQ-SPLIT-1): it may lower risk below σ*, never raise it** | EQ-SPLIT-1 rescales the risky mix to σ*; applied after a trend rule it re-levers the remaining positions | 2 of 10 assets up: exposure 0.19 (rule after scaling) vs 0.69 (rule before) |
| R-5 | **A sleeve (O5) exists only where the account permits its positions** (shorting for long–short), enters the risk model as an asset, and needs a CMA when allocated by a μ-based method | Nordnet shorting only in the ordinary share account, with tests (`research/S3_FINDINGS.md`); ADR-0027 D3; S9b | — |
| R-6 | **Tactical overlays (O6) never change w*;** they are logged timing evidence within the Trader's mandate | ADR-0026 §5, §8.9 | — |

PBL links verified: EPO w = 0 equals MVO on the signal; EPO w = 1 with s = 0.1·σ·sign(r) is proportional to MOP's sign × 1/σ (PBL-3).

---

## 5. The §D.1 candidate "signal-conditioned heuristics"

S4_PLAN §D.1 admits it "only if S4.9 shows it is a distinct, literature-supported construction".
- **Literature-supported:** yes.
  - 1/N within the winner decile is JT's construction;
  - cap weights within terciles is AMP's (stocks);
  - sign × 1/σ is MOP's TSMOM.
- **Distinct:** no. Each is a composition of an existing signal (SIG-1/SIG-2) with an existing heuristic (A1/A2/A3) through O2 or O3.

**Outcome:** no new roster item. The compositions are registered as **composition rules** with V/V1 status, to be typed at S4.20 (a method plus a conditioning or direction rule).

---

## 6. Mappings registered for S9d (RQ-33; register EQ-MAP-1 … 4)

| ID | Mapping | Source | Notes |
|---|---|---|---|
| EQ-MAP-1 | TSMOM → s_i = SR₀·σ_i·sign(R_i) (constant Sharpe per asset; PBL SR₀ = 0.1 monthly); magnitude variant s_i = SR₀·σ_i·clip(z_i) | PBL eq. (23); S48-D1 | Units: σ per period of Σ |
| EQ-MAP-2 | XSMOM → s_i = c_t(R_i − R̄)·σ_i^k, k ∈ {0, 1, 2}; positives sum to 1 | PBL eqs. (24)–(27) | k = 1: risk weights with constant total; k = 2: EPO w = 1 weight ∝ outperformance |
| EQ-MAP-3 | Score → α_i = IC·σ_i·z_i, benchmark-neutralised (w_b′α = 0) | Michaud & Michaud ch. 12 (Ambachtsheer 1977) | IC assumed, never fitted in-sample (S7); σ total or residual, matching the method |
| EQ-MAP-4 | Views: Q = EQ-MAP-1/2/3 output; P = I (absolute) or relative (long–short) views; Ω from confidence (He–Litterman; Idzorek, IDZ-1) | BL 1992; PBL Prop. 3 | EPO ≡ BL under Π = γΣa, Q = s, P = I, Ω = Λ |

All four are **registered, not accepted**. S9d chooses, under the S7 protocol.

---

## 7. Owner decisions (stage 6)

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **S49-D1** | Accept the matrix (§3) as the admissible-compositions list | (a) V and V1 cells admissible; M cells admissible once an S9d mapping or sleeve CMA is accepted; D cells to the research lane only; — cells excluded · (b) also admit D cells now | **(a).** D cells have semantics but no source; admitting them would add untested constructions to the library (amendment 12, selectivity) |
| **S49-D2** (= S48-D3) | Momentum sleeves and their scaling | (a) O5 sleeves: long-only (winners, positive-trend or factor-ETF rotation) for every account; long–short only where `POL.instrument_permissions` permit shorting. Sleeve scaling: constant volatility (B&SC) as a variant under EQ-SPLIT-1 and the leverage cap; DM's dynamic rule as a timing model in point-in-time form (RQ-17) · (b) no sleeves: momentum only as O2–O4 | **(a)**, with the evaluation at S7. Sleeves defined on active (relative) returns where they overlap the equity allocation |
| **S49-D3** | Order of operations for direction rules (R-4) | (a) base method → engine-level scaling → direction rule (risk may fall below σ*, never rise) · (b) direction rule → scaling (re-levers remaining positions) · (c) direction rules exempt from EQ-SPLIT-1 like PC-A5 | **(a)**, recorded as an amendment to the EQ-SPLIT-1 entry (an exception list item) at G4 with B-46 |
| **S49-D4** | Mapping candidates for S9d | (a) register EQ-MAP-1 … 4 with R-1/R-2 as admissibility conditions; choose at S9d · (b) choose one now | **(a).** Choosing now would pre-empt the S7 protocol |
| **S49-D5** | Signal-conditioned heuristics (§D.1) | (a) composition rules, no roster change · (b) new roster items | **(a)** |

---

## 8. Verification (stage 7)

| Script | Proves | Result |
|---|---|---|
| `s49_signal_pc_compatibility.py` | R-1 (ranks into MVO ill-defined); R-2 (α = IC·σ·z invariant; benchmark neutrality; units factor 12); PBL EPO at w = 0 and w = 1; O2 constructions (1/N, cap, 1/σ within a selected set) well defined and invariant to monotone score transforms; R-4 ordering (0.19 vs 0.69); the S48-D1 identity | PASS |

---

## 9. Handed forward

| To | Item |
|---|---|
| S4.10 | Anchored EPO with a signal (B7): anchor choice S47-D3 (reminder first); the 60/40 question (RQ-09 note) |
| S4.12 | PC-D4 TPA with EQ-MAP-3 α; mean–CVaR (D1) and drawdown (D2) as μ-consuming |
| S4.13 | Sleeves as assets in the authoritative risk model |
| S4.20 | Composition rules typed (method + conditioning / direction rule); R-1 … R-6 as contract predicates |
| S9d | EQ-MAP-1 … 4; blend-weight timing (S48-D6) |
| S11 | Which compositions enter the candidate set; sleeve overlap with the equity allocation |
| S13c–d | O6 overlays; DM timing; JT cohorts for turnover |
| G4 | EQ-SPLIT-1 amendment for direction rules (S49-D3) with B-46 |

---

## 10. Ladder status after S4.9 (signal ladder)

| Signal | Status |
|---|---|
| SIG-1, SIG-2 and variants | CONSTRUCTION EXTRACTED · **PLACEMENT DETERMINED** · **PC-COMPATIBILITY DETERMINED** (pending S49-D1 … D5) |
