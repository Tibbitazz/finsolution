# S4.9 Signal × PC compatibility: what a momentum signal may become, method by method

**Document status:** REVIEWED · **S4.9 DONE (2026-10-18).** *Annotated 2026-10-18 under S412-D6 (μ-free scenario methods; D3 × O2 tested). Annotated 2026-10-25: R-1 refined (owner decision REN-D3, §4).* Drafted 2026-10-15; revised 2026-10-18 after the owner's review. Owner decisions **S49-D1 … S49-D5 all recorded 2026-10-18** (§7). · **Basis:**
- S4_PLAN §G (step S4.9), amendment 4 (momentum roles open until S4.8/S4.9), §D.1 (candidate "signal-conditioned heuristics"), SYNC-3 (with S4.10);
- `S4_MOMENTUM.md` (S4.8; decisions S48-D1 … D6; S48-D3 carried here);
- ADR-0012 (signals are descriptors; μ only through an accepted mapping, §3); ADR-0024 §1, §4, §7 (research lane; allocation domains; EPO in the MVO lineage); ADR-0025 (admission ≠ evaluation; admission requires an identifiable primary source); ADR-0026 §8 (evidence by use); ADR-0027 D3; EQ-SPLIT-1 (S47-D6).

**Revision of 2026-10-18 (owner review):**
- EPO consumes expected returns (it is MVO with a shrunk mean and a shrunk covariance); the draft's "signal-native" wording was wrong and contradicted ADR-0024 §7 (§0, §3).
- Double counting checked and ruled: new §3a and rule R-7.
- The D cells were tested before any decision (§3b); outcomes V1, R (research lane, owner decision) or reclassified.
- The alpha mapping corrected against Grinold 1994 and Grinold & Kahn's *Advances* (EQ-MAP-3: volatility of the forecast return; volatility step for vol-proportional raw forecasts; additive signals).
- Transfer coefficient added as a diagnostic (§4a, EQ-TC-1).

**Related files:** `verification/s49_signal_pc_compatibility.py`, `verification/s49_double_counting_dcells.py`, `verification/s49_alpha_sources.py` (all PASS); register entries EQ-MAP-1 … EQ-MAP-4, EQ-TC-1 and the S49-D3 note on EQ-SPLIT-1 (`S4_EQUATION_REGISTER.md`); RQ-33 (score → μ), RQ-17 (tactical role), RQ-32 (aggregation).

**Scope:** for every pairing of a momentum signal with a roster method, is the construction *defined* and *source-supported*? **Nothing here says a pairing is good** (S7). The exit criterion: no combination without semantics.

---

## 0. Summary

1. **Six objects** (amendment 4), each with its own semantics: O1 evidence descriptor · O2 signal-conditioned universe · O3 direction/exposure rule · O4 expected-return mapping · O5 standalone sleeve · O6 tactical overlay (§2).
2. **The roster splits by input.**
   - **μ-free methods** (A1–A5, C1–C5, D3, min-CVaR) can use a signal only through *selection* (O2), *direction* (O3) or as a *sleeve* (O5), never through μ.
     - *[2026-10-18, owner decision S412-D6]* D3 and min-CVaR are μ-free **only on demeaned scenarios**. CVaR contains the scenario mean, so on raw or μ-centred scenarios they consume μ (finding NT-1, `S4_NON_TRADITIONAL.md` §2.1). S412-D1 and D6 fix the demeaned form for both.
   - **μ-consuming methods** (B1–B7, D2, D4, mean–CVaR, E2) can use it only through a *mapping* to returns (O4). **EPO (B6/B7) is one of them:** PBL take the signal as already scaled to the conditional expected excess return (p. 127), and eq. (18) is MVO with the mean shrunk toward the anchor-implied returns and the correlations shrunk toward zero (verified). PBL supply tested mappings (eqs. 23–27 = EQ-MAP-1/2) and a scale calibration for proportional signals (eq. 21), which removes scale but not location. Every μ-consumer, EPO included, needs a mapping accepted at S9d.
3. **Source-supported compositions** (§3):
   - 1/N or cap weights within a momentum-selected set (JT deciles; AMP terciles);
   - sign × 1/σ (MOP; HOP), i.e. TSMOM is PC-A3 with a direction rule;
   - EPO with momentum signals mapped to expected returns (PBL eqs. 23–27; EPO w = 0 is MVO on the mapped signal, w = 1 is TSMOM's sign × 1/σ);
   - 1/N across factor portfolios including momentum (DGU Table 2, dataset 7).
4. **The §D.1 candidate "signal-conditioned heuristics" is literature-supported but not a distinct method:** it is a composition (O2 or O3 × A1/A2/A3). No roster change (§5).
5. **Rules the engine needs** (verified):
   - **unscaled scores never enter an optimizer, EPO included** (R-1; *refined 2026-10-25 by owner decision REN-D3: a score enters an optimiser only through a declared, accepted mapping; see §4*). The alpha form is α = IC·ω·z with ω the volatility of the return being forecast (Grinold; EQ-MAP-3);
   - **a direction rule acts after the engine-level risk scaling** (R-4; owner decision S49-D3). With 2 of 10 assets in an uptrend, exposure is 0.19 if the rule follows the scaling and 0.69 if it precedes it;
   - **no double counting** (R-7, §3a): a sleeve overlapping a class is never a separate unit beside it; sleeve risk by look-through of current holdings; one channel per signal unless the combined weight is explicit.
6. **D cells tested** (§3b): three become V1 (derived from PBL); seven are defined and tested but unsourced and go to the **research lane** (owner decision S49-D1); two remain untested (S4.11, S4.12).
7. **S48-D3 decided as S49-D2:** sleeves follow R-7. Long-only sleeves are tilts inside their host class; long–short (zero-investment) sleeves only where shorting is permitted, and then they may be units of their own. No sleeve-level scaling in the base case; constant volatility as a registered variant; DM's dynamic rule is a timing model (S13c).
8. **Signal-conditioned heuristics (S49-D5):** composition rules for V/V1 cells, fixed per run and never agent-selectable; no roster change.

---

## 1. Sources (stage 1)

Used:
- S4.8 sources (`S4_MOMENTUM.md` §1);
- PBL 2021 eqs. (8), (18)–(27), Props. 1–3 (pp. 127–137);
- **Grinold (1994)**, "Alpha is Volatility Times IC Times Score", *JPM* 20(4):9–16 (in hand 2026-10-18): eq. (1); Examples 1–5; eqs. (2)–(4); fns. 6, 7, 9, 11;
- **Grinold & Kahn, *Advances in Active Portfolio Management*** (McGraw-Hill; in hand 2026-10-18; governing, newest version): ch. 3 eqs. (19)–(20) (forecasting rule), (35)–(37) and Exhibit 11 (transfer coefficient); ch. 9 "Signal Weighting" (read at S9d);
- **Clarke, de Silva & Thorley (2002)**, *FAJ* 58(5):48–66 (in hand 2026-10-18): transfer coefficient, generalised fundamental law, Table 1, ex post decomposition;
- Michaud & Michaud 2008 ch. 12, pp. 109–111 (secondary statement of the scaling rule; consistent units; index-weighted active returns sum to zero);
- Daniel & Moskowitz 2016 §3, Fig. 3 (time-varying betas of winner and loser portfolios);
- DeMiguel, Garlappi & Uppal 2009 Table 2, p. 1918 (datasets include MKT/SMB/HML/UMD portfolios as assets);
- Treynor & Black 1973 (appraisal-ratio sizing for PC-D4); Black & Litterman 1992 (views).

Secondary only: Gallego, IEOR4706 Lecture 7 (Columbia, Autumn 2000), a teaching note on Grinold & Kahn (benchmark alpha-neutrality; information-ratio portfolio). Grinold & Kahn's *Active Portfolio Management* (2nd ed.) is not in hand; low priority now (alpha refinement procedures only).

---

## 2. The six objects

| ID | Object | Semantics | Source support | Owner of the use |
|---|---|---|---|---|
| O1 | **Evidence descriptor** | The signal as a fact agents may cite (R8); no weight effect by itself | ADR-0012; ADR-0026 §8 | All roles; S8/S12 |
| O2 | **Signal-conditioned universe** | The signal selects the set (e.g. top tercile or decile by XSMOM; positive TSMOM); a μ-free method weights within it, re-solved on the selected sub-matrix | JT 1993 (equal-weighted deciles); AMP 2013 (terciles: value-weighted for stocks, equal-weighted otherwise); DM 2016 (value-weighted deciles) | S4.9 → S11 |
| O3 | **Direction / exposure rule** | Per asset, the signal sets the sign (long/short) or, long-only, hold vs cash, applied to a base weight. Defined only for separable base weights (A1, A3, A4; §3b) | MOP 2012 eq. (5); HOP 2017 (sign × equal volatility); long-only cash version derived (shorts → 0) | S4.9 → S11; timing use → S13c |
| O4 | **Expected-return mapping** | The signal becomes μ (or α) in return units, consumed by a μ-based method, EPO included | PBL eqs. (21), (23)–(27); Grinold 1994 / G&K ch. 3 (α = IC·ω·z); Michaud & Michaud ch. 12; BL views (PBL Prop. 3) | S9d (RQ-33) |
| O5 | **Standalone sleeve** | A momentum portfolio (WML, TSMOM factor, long-only winners, factor-momentum rotation) held under R-7: long-only, a tilt inside its host class (never a separate unit beside it); zero-investment long–short, a unit of its own where shorting is permitted (S49-D2) | DGU Table 2 (factor portfolios incl. UMD as assets); MOP/AMP factor portfolios; B&SC/DM scaling; CdST fn. 7 (long–short plus market exposure) | S4.9 → S11; account permissions |
| O6 | **Tactical overlay / timing evidence** | The signal informs *when and how* to implement an approved target, inside the Trader's mandate; never changes w* | ADR-0026 §5, §8.9; HANDOFF §4.6 (TSMOM as logged timing evidence) | S13c–d (RQ-17, RQ-35) |

The **blend-weight layer** (factor momentum varying the composite's factor weights, S48-D6) sits *before* any PC method, in score aggregation (RQ-32). It is not a pairing with a method.

---

## 3. Compatibility matrix

Codes: **V** = defined and source-supported · **V1** = defined, derived from a sourced rule (variant) · **M** = requires a mapping accepted at S9d (O4) or a CMA for the sleeve (O5) · **R** = defined and tested on synthetic data (§3b), no source for the pairing: **research lane** (ADR-0024 §1; owner decision S49-D1, 2026-10-18) · **D** = defined, not yet tested (tested at the step named; research lane unless a source is found) · **—** = no semantics (invalid). O1 is valid for every method; O6 is not a PC pairing (S13). O5 cells are subject to R-7 (§3a).

| Method | Input class | O2 conditioned universe | O3 direction rule | O4 μ mapping | O5 sleeve as asset |
|---|---|---|---|---|---|
| PC-A1 1/N | μ-free | **V** (JT EW deciles; AMP EW terciles) | **V1** (sign × 1/N = EPO w = 1 with s ∝ σ²·sign; long-only cash version) | — | **V** (DGU dataset 7: factor portfolios incl. UMD) |
| PC-A2 cap weight | μ-free, capitalisations | **V** (DM VW deciles; AMP VW stock terciles) | — (cap weights have no sign) | — | — (a strategy has no capitalisation) |
| PC-A3 1/σ | μ-free | **V1** (long-only TSMOM: positive-trend set at 1/σ) | **V** (MOP eq. 5; HOP: TSMOM = A3 with signs) | — | V |
| PC-A4 1/σ² | μ-free | **V1** (separable: equals re-solving on the set) | **V1** (sign × 1/σ² = EPO w = 1 with s ∝ sign) | — | V |
| PC-A5 volatility targeting | μ-free, time-varying | — | — | — | **V** (B&SC = A5-type scaling of a momentum sleeve; S48-D3) |
| PC-B1 max Sharpe | μ + Σ | **R** (MVO with an exclusion constraint; μ from a different signal only, R-7c) | — | **M** (EQ-MAP-1/2 tested by PBL in EPO; w = 0 is MVO) | M (CMA for the sleeve) |
| PC-B2 Black–Litterman | μ + Σ + views | — | — | **M** (Q = mapped signal; PBL Prop. 3: EPO ≡ BL with Π = γΣa, Q = s, P = I, Ω = Λ) | M |
| PC-B3 robust MV | μ + Σ + uncertainty | — | — | **M** (PBL Prop. 2: ellipsoidal robust ≡ EPO) | M |
| PC-B4 resampled frontier | μ + Σ | — | — | **M** (scaling per EQ-MAP-3) | M |
| PC-B5 mean–downside | μ + scenarios | — | — | M | M |
| PC-B6 simple EPO | μ (s in return units) + shrunk Σ | — | — | **M** (PBL-tested mappings EQ-MAP-1/2; scale absorbed by the risk target, location not) | M |
| PC-B7 anchored EPO | μ + shrunk Σ + anchor | — | — | **M** (PBL-tested mappings; eq. 21 scale calibration; anchor at S4.10) | M |
| PC-C1 GMV | Σ only | **R** | reclassified: long-only → O2 (**R**); long–short → B1 with μ ∝ sign (**M**) | — | V |
| PC-C2 ERC | Σ only | **R** | reclassified: long-only → O2 (**R**); long–short → signed ERC (**R**) | — | V |
| PC-C3 HRP | Σ only | **R** | — | — | V |
| PC-C4 max diversification | Σ only | **R** | — | — | V |
| PC-C5 min correlation | Σ only | **R** (tested at S4.11, 2026-10-18; research lane under S49-D1) | — | — | V |
| PC-D1 CVaR | scenarios (± μ) | **R** (min-CVaR) | — | M (mean–CVaR; ANG-02 open) *[2026-10-18: ANG-02 decided by S412-D1: V0 min-CVaR on demeaned scenarios (μ-free); mean–CVaR is variant V1, scenarios centred on S9's μ]* | V / M |
| PC-D2 drawdown-constrained | μ + paths | — | — | M | M |
| PC-D3 tail-risk parity | scenarios | **R** (tested at S4.12a, 2026-10-18; research lane under S49-D1) | — | — | V |
| PC-D4 TPA | α + residual risk | — | — | **M** (Treynor–Black α/σ²_ε with α = IC·ω·z, residual ω) | — |
| PC-E2 adversarial diversifier | Σ + Sharpe floor (μ) | — | — | M (ANG-16 open) | M |
| PC-E1 Researcher | role | Runs the research-lane compositions (R) and proposes new ones | | | |

**Reading a μ-free method with O5:** see §3a. The sleeve never enters beside the class it overlaps; its risk comes from looking through to its current holdings.

---

## 3a. Double counting (R-7; owner request 2026-10-18)

Set-up (`s49_double_counting_dcells.py`): three classes (equity, bonds, commodities) plus a long-only momentum sleeve drawn from the same 30 stocks as the equity sleeve; correlation of sleeve and equity 0.91.

| Method | Equity weight (look-through), without → with the sleeve as a unit | Equity share of risk, without → with |
|---|---|---|
| 1/N | 0.33 → 0.50 | 0.53 → 0.76 |
| 1/σ | 0.17 → 0.30 | 0.35 → 0.68 |
| ERC | 0.16 → 0.22 | 0.33 → 0.50 |
| HRP | 0.049 → 0.055 | ≈ 0 (bond diversification) |
| GMV | 0.10 → 0.12 | 0.10 → 0.12 |

Four distinct problems:
1. **Exposure double counting.** Large for methods that count each asset as one unit (1/N, 1/σ, ERC). HRP clusters the two together; GMV sees the covariance.
2. **Exact redundancy.** Single stocks plus a sleeve of the same stocks give a singular joint covariance; every split between the sleeve and its stocks is the same portfolio.
3. **Risk measurement.** A sleeve's own return history misstates the risk of its current holdings when the holdings rotate (synthetic: beta 1.09 from history against 1.50 from holdings; mechanism documented by Daniel & Moskowitz 2016 §3, Fig. 3). The draft's statement that "the sleeve's return history enters the authoritative risk model" was wrong as a rule.
4. **Signal double counting.** One signal entering through two channels: O2 + O4 with the same signal; an agent adjusting a μ that already contains it (O1 + O4); a composite score containing momentum plus a momentum sleeve. A direction rule applied to an output that already carries the sign turns every position long (excluded by the "—" cells).

**Rule R-7 (no double counting):**
- **R-7a (exposure).** A long-only sleeve that overlaps a class in the same problem is never a separate unit beside it. It is either a tilt inside the host class (hierarchical: allocation domain "strategy/sleeve" inside the class, ADR-0024 §4) or a zero-investment active sleeve h − w_host held at size x within the host's weight e; long-only, 0 ≤ x ≤ e (verified). With the tilt inside the host, the class weight under 1/N and the class risk share under ERC do not move with the tilt (verified). This is the long-only bound Clarke, de Silva & Thorley measure (active weight ≥ −benchmark weight); their fn. 7 structure (long–short plus market exposure) needs shorting (R-5).
  - *[2026-10-18, owner decision S49-D2]* **Exception: zero-investment long–short sleeves** (winners minus losers; TSMOM factor) carry no net class exposure and may be units of their own where shorting is permitted, as in DGU dataset 7 (1/N across MKT, SMB, HML, UMD). Held as a unit, such a sleeve adds no net equity weight beyond the host's (verified); its gross positions and its beta are counted by look-through (R-7b, R-7d).
- **R-7b (risk).** Sleeve risk always comes from looking through to its current holdings in the authoritative risk model (ADR-0027 D3), at every problem level. The sleeve's return history is for evaluation (S7) only.
- **R-7c (signals).** Each signal declares its channels per problem. One signal through two channels requires an explicit, recorded weight for each; for correlated signals the combination follows the regression weights (Grinold 1994 eqs. (3)–(4); after costs: G&K ch. 9 at S9d).
- **R-7d (reporting).** Every candidate reports its look-through exposure by asset class, by signal and by size (long-only constraints create an unintended small-cap tilt; CdST Fig. 4). Contract predicate at S4.20; report at S4.16.

**Data dependency:** for the owner's ETF universe (e.g. a world-momentum ETF beside a world-index ETF), R-7 needs ETF constituent holdings (S6). Gap class B: gates ETF sleeves at S6/S11, not S4.

---

## 3b. D cells: tests and outcomes (owner request 2026-10-18: no decision without testing)

Specification tests only (`s49_double_counting_dcells.py`): is the construction well defined, does it depend on the score only through the selection or the signs, does the method's defining property survive, does R-4 hold. No returns were tested (S7; RQ-16).

| Former D cell | Finding | Outcome |
|---|---|---|
| A1 × O3 (sign × 1/N); A4 × O3 (sign × 1/σ²) | Identity: sign × σ^(k−2) weights = EPO(w = 1) with s ∝ σ^k·sign; k = 2 → 1/N, k = 1 → 1/σ (PBL), k = 0 → 1/σ². PBL use the σ^k exponent for XSMOM (eqs. 24–27) and k = 1 for TSMOM. Each k is a belief: k = 1 equal Sharpe, k = 2 return ∝ variance, k = 0 equal expected return. The long-only 1/N version resembles Faber's trend timing (not in hand; a 10-month moving-average rule) | **V1** |
| A4 × O2 | Separable weights: dropping assets equals re-solving on the set | **V1** |
| C1, C2, C3, C4 × O2; D1 (min-CVaR) × O2 | Re-solved on the selected sub-matrix (from the authoritative model, never re-estimated): well defined, non-negative, sums to 1; identical under three monotone transforms of the score; ERC keeps equal risk contributions within the set | **R** (research lane) |
| B1 × O2 | MVO with an exclusion constraint; not the same as truncating μ (excluded assets would otherwise serve as hedges). With momentum μ it double counts (R-7c) | **R** (research lane) |
| C1 × O3, C2 × O3 | "Sign × base weight" breaks correlation-aware methods: zeroing GMV differs from GMV on the up-trend set (up to 0.06 in weight); zeroing ERC leaves contributions of 7.8–9.0% instead of an equal 8.3%; flipping ERC signs gives negative contributions (−5.7% to 10.7%); flipped GMV differs from signed GMV by up to 0.11. Correct constructions: long-only → re-solve on the up-trend set (= O2); long–short GMV → min variance with signed budget d′w = 1, which is MVO with μ ∝ sign (O4); long–short ERC → signed ERC = D·ERC(DΣD), equal contributions with the prescribed signs, unique because long-only ERC of DΣD is unique | **Reclassified**: C1 → O2 (R) / B1-M; C2 → O2 (R) / signed ERC (**R**) |
| C5 × O2; D3 × O2 | Not yet tested (need their own implementations). *[2026-10-18]* C5 × O2 tested at S4.11: defined for ≥ 3 selected assets with non-degenerate correlations, rank-only (`s411_risk_structured.py`). *[2026-10-18]* D3 × O2 tested at S4.12a: ERC-CVaR re-solved on the selected subset is defined, positive, sums to 1 and is identical under three monotone transforms of the score (`s412_drawdown_tail.py`) | C5 × O2 → **R** (research lane); D3 × O2 → **R** (research lane) |

**Research lane (ADR-0024 §1):** the seven R constructions (C1, C2, C3, C4, D1 and B1 on a selected set; signed ERC) may run experimentally and in research peer review; no production CIO allocation until an admissibility review admits them (ADR-0025 requires an identifiable primary source). Leads for that review, from memory and not in hand: Baltas (2015) on trend following with correlation-aware risk parity; Bai, Scheinberg & Tütüncü (2016) on risk parity by orthant.

---

## 4. Rules derived (verified)

| ID | Rule | Basis | Check |
|---|---|---|---|
| R-1 | **No unscaled score enters a μ-consuming method, EPO included.** Ranks or raw scores fed as μ give weights that depend on arbitrary choices (rank origin, centring). Alphas not proportional to volatility tilt the optimizer toward low-volatility assets ("alpha eating") | Michaud & Michaud p. 109; Grinold 1994 Example 5; G&K ch. 3 Insight 4; PBL p. 127 and eq. (21) (scale calibration removes scale, not location) | MVO weights on ranks 1…N, 0…N−1 and centred ranks differ by > 0.1; PBL eq. (22) weights differ for ranks and centred ranks |
| R-2 | **Mappings are in return units, per period consistent with Σ, scaled by the volatility of the return being forecast, and benchmark-neutral when used as active α** | Grinold 1994 eq. (1), Example 3; G&K ch. 3 eqs. (19)–(20); Michaud & Michaud pp. 110–111 | α = IC·ω·z invariant to relabelling; volatility step for vol-proportional forecasts; units factor 12; w_b′α = 0 |
| R-3 | **μ-free methods use a signal only through O2, O3 or O5;** O3 only on separable base weights (A1, A3, A4). *[2026-10-18, S412-D6]* Scenario methods count as μ-free only on demeaned scenarios | Input classes (§3); §3b; NT-1 | Zeroing or flipping breaks GMV and ERC |
| R-4 | **A direction rule acts after the engine-level scaling (EQ-SPLIT-1): it may lower risk below σ*, never raise it** (owner decision S49-D3) | EQ-SPLIT-1 rescales the risky mix to σ*; applied after a trend rule it re-levers the remaining positions | 2 of 10 assets up: exposure 0.19 (rule after scaling) vs 0.69 (rule before) |
| R-5 | **A sleeve (O5) exists only where the account permits its positions** (shorting for long–short), and needs a CMA when allocated by a μ-based method | Nordnet shorting only in the ordinary share account, with tests (`research/S3_FINDINGS.md`); S9b | — |
| R-6 | **Tactical overlays (O6) never change w*;** they are logged timing evidence within the Trader's mandate | ADR-0026 §5, §8.9 | — |
| R-7 | **No double counting:** (a) an overlapping long-only sleeve is a tilt inside its host class or a zero-investment active sleeve (long-only 0 ≤ x ≤ e), never a unit beside it; a zero-investment long–short sleeve may be a unit where shorting is permitted (S49-D2); (b) sleeve risk by look-through of current holdings; (c) one channel per signal unless the combined weight is explicit; (d) look-through exposure reported by class, signal and size | §3a; DM 2016 §3; Grinold 1994 eqs. (3)–(4); CdST 2002 | 1/N equity 0.33 → 0.50 as a separate unit, unchanged as a tilt; beta 1.09 vs 1.50; singular joint covariance |

*[2026-10-25, owner decision REN-D3]* **R-1 refined, not removed.** R-1's three concerns are the origin (centring), the scale and "alpha eating". In budget-neutral, tracking-error-constrained exposure maximisation (maximise (w − b)′z subject to a TE budget and full investment) the first two vanish: shifting or rescaling z leaves the solution unchanged, and the TE budget, not the score, sets the risk (`s4ren_multifactor_reference.py` P-R2, P-R4). The third becomes an explicit modelling choice: the implied mapping α = λ·z (**EQ-MAP-5**, the characteristic-premium model, a common premium per unit of score) sizes positions as z/ω², while EQ-MAP-3 (α = IC·ω·z, Grinold) sizes them as z/ω (P-R5). Rule as refined: **a score enters an optimiser only through a declared mapping accepted at S9d (ADR-0012 §3); EQ-MAP-5 is admissible only in budget-neutral, TE-constrained exposure maximisation; where the level or scale of μ matters (asset-class MVO with cash or leverage, BL, EPO) the mapping must fix both (EQ-MAP-1 … 4).** For the reference multifactor composite (`S4_SCORING_RENSHAW_ANG.md`) EQ-MAP-5 is V0 and EQ-MAP-3 the tested V1; S7 compares them (cross-sectional test of whether the premium per unit of score rises with volatility).

PBL links verified: EPO eq. (18) = MVO on μ̃ = (1 − w)s + wγVa with Σ_w; EPO w = 0 equals MVO on the signal; EPO w = 1 with s = 0.1·σ·sign(r) is proportional to MOP's sign × 1/σ (PBL-3).

---

## 4a. Transfer coefficient (diagnostic; EQ-TC-1)

The transfer coefficient measures how much of a signal reaches the weights: IR_P = IR_Q·ρ_PQ for any portfolio P (G&K ch. 3 eq. 37; CdST eq. 6: IR ≈ TC·IC·√N). Reference values (verified, `s49_alpha_sources.py`): sign-only positions 0.80; long-only at 5% tracking error 0.58 (CdST Table 1; own reproduction 0.53); long-only with cap neutrality 0.47; 25% turnover limit 0.49; multiple constraints 0.31.

Momentum compositions in a long-only security universe (synthetic: 300 stocks, cap-weighted benchmark, top-third screen, Grinold alphas; `s49_double_counting_dcells.py`):

| Construction on the selected set | TC | Tracking error |
|---|---|---|
| 1/N (V) | 0.49 | 3.7% |
| cap weights (V) | 0.43 | 4.3% |
| 1/σ (V1) | 0.49 | 3.6% |
| ERC (R) | 0.48 | 3.9% |
| GMV (R) | 0.25 | 8.5% |
| HRP (R) | 0.18 | 12.2% |
| max diversification (R) | 0.26 | 8.9% |
| min-CVaR (R) | 0.23 | 8.9% |

In GMV, HRP, max diversification and min-CVaR on a selected set most of the active risk comes from the method's own tilt, not from the signal. A diagnostic, not a performance result and not an admission criterion.

**Consequences:**
- Long-only momentum (XSMOM included) is possible but transfers roughly half the signal; expect about half the unconstrained IR.
- Asset-class trend rules have low breadth: G&K's tactical example (IC 0.1, 12 bets a year, TC 0.5) gives IR ≈ 0.17. A realistic prior for S7.
- Turnover limits (and need-to-trade regions, RQ-44) lower TC: a cost to set against the trading savings at S13.
- The ex post decomposition (CdST eqs. 11–12) separates signal success from constraint noise: a learning-loop input (S17).

---

## 5. The §D.1 candidate "signal-conditioned heuristics"

S4_PLAN §D.1 admits it "only if S4.9 shows it is a distinct, literature-supported construction".
- **Literature-supported:** yes.
  - 1/N within the winner decile is JT's construction;
  - cap weights within terciles is AMP's (stocks);
  - sign × 1/σ is MOP's TSMOM.
- **Distinct:** no. Each is a composition of an existing signal (SIG-1/SIG-2) with an existing heuristic (A1/A2/A3/A4) through O2 or O3.

**Decision (S49-D5, 2026-10-18): no new roster item.** The V/V1 compositions are registered as **composition rules**, with four conditions:
1. **Typed at S4.20** as composition rules: base method, signal variant (SIG-1/SIG-2 and variant), selection fraction or sign rule, and order of operations (a direction rule acts after the engine-level scaling, R-4).
2. **Fixed per run, never agent-selectable.** Each admitted composition is a separately declared candidate, fixed before the run at S11. A PC agent may not switch momentum conditioning on or off for its method (no specification search; ADR-0026 §4.1, ADR-0027 D3.4 by analogy).
3. **Duplicate detection.** Compositions sit close to their base method; the S4.16 distance check flags near-duplicate proposals before review and voting.
4. **Research-lane constructions are excluded.** The seven R constructions stay in the research lane (S49-D1).

Admitted compositions: A1 × O2 and A2 × O2 (V); A3 × O3 (V); A3 × O2, A1 × O3, A4 × O2, A4 × O3 (V1). Their transfer coefficients in the synthetic test (0.43–0.49) are close to long-only max Sharpe (0.51; §4a).

---

## 6. Mappings registered for S9d (RQ-33; register EQ-MAP-1 … 4; owner decision S49-D4)

| ID | Mapping | Source | Notes |
|---|---|---|---|
| EQ-MAP-1 | TSMOM → s_i = SR₀·σ_i·sign(R_i) (constant Sharpe per asset; PBL SR₀ = 0.1 monthly); magnitude variant s_i = SR₀·σ_i·clip(z_i) | PBL eq. (23); S48-D1; same form as Grinold's direction-only forecast (1994 fn. 11) | Units: σ per period of Σ; total σ (absolute forecast) |
| EQ-MAP-2 | XSMOM → s_i = c_t(R_i − R̄)·σ_i^k, k ∈ {0, 1, 2}; positives sum to 1 | PBL eqs. (24)–(27) | k = 0 is the constant-IC member (Grinold); k = 1, 2 imply skill rising with volatility, testable at S7 |
| EQ-MAP-3 | Score → α_i = IC·ω_i·z_i; ω = volatility of the return being forecast; volatility step for vol-proportional raw forecasts (momentum); several signals add with regression-adjusted ICs; benchmark-neutralised for active use | G&K ch. 3 eqs. (19)–(20) (governing); Grinold 1994; Michaud & Michaud ch. 12 | IC assumed, never fitted in-sample (S7); fixed-weight composites re-standardised (RQ-32); after-cost combination: G&K ch. 9 at S9d |
| EQ-MAP-4 | Views: Q = EQ-MAP-1/2/3 output; P = I (absolute) or relative (long–short) views; Ω from confidence (He–Litterman; Idzorek, IDZ-1) | BL 1992; PBL Prop. 3 | EPO ≡ BL under Π = γΣa, Q = s, P = I, Ω = Λ |

All four are **registered, not accepted**. S9d chooses, under the S7 protocol. Relative signals (XSMOM) carry no level of their own; they need one from an anchor, a prior or a CMA (S4.10). Absolute signals (TSMOM) carry their own level.

---

## 7. Owner decisions (stage 6)

| ID | Decision | Options | Recommendation | Owner decision |
|---|---|---|---|---|
| **S49-D1** | The matrix (§3) as the admissible-compositions list | (a) V and V1 admissible; M once an S9d mapping or sleeve CMA is accepted; tested-but-unsourced cells to the research lane; untested cells tested first; — excluded · (b) admit tested-but-unsourced cells under a composition ruling on ADR-0025 · (c) admit all D cells untested | (a) after testing (the draft's untested (a) was rejected by the owner) | **2026-10-18: (a).** "Put all seven in research lane." V/V1 admissible; M once mapped; the seven R constructions → research lane; C5 × O2 and D3 × O2 tested at S4.11/S4.12, research lane unless a source is found; — excluded |
| **S49-D2** (= S48-D3) | Momentum sleeves and their scaling | (a) sleeves under R-7 · (b) no sleeves: momentum only as O2–O4 · (c) sleeves as free-standing units beside their class (excluded by R-7) | **(a)** | **2026-10-18: (a).** Long-only sleeves (winners, positive-trend set, factor-ETF rotation) are tilts inside the host class (0 ≤ x ≤ e; class weight set by the class-level method). Zero-investment long–short sleeves only where `POL.instrument_permissions` permit shorting; they may be units of their own (DGU dataset 7; R-7a exception). Risk always by look-through of current holdings (R-7b). Base case: no sleeve-level scaling; tilt size x set at S11 within the Policy Statement's active-risk bounds; EQ-SPLIT-1 scales the whole portfolio. Constant-volatility variant: long–short as published (B&SC: 126-day variance, 12% target, leverage cap); long-only applied to the tilt size x, not to the whole sleeve (derived, V1). DM's dynamic weight is a timing model (S13c; RQ-17), point-in-time only. ETF sleeves need constituent holdings (S6/S11; gap class B). Evaluation at S7 |
| **S49-D3** | Order of operations for direction rules (R-4) | (a) base method → engine-level scaling → direction rule (risk may fall below σ*, never rise) · (b) direction rule → scaling (re-levers remaining positions) · (c) direction rules exempt from EQ-SPLIT-1 like PC-A5 | **(a)** | **2026-10-18: (a).** Noted on EQ-SPLIT-1; binds at G4 with B-46 |
| **S49-D4** | Mapping candidates for S9d | (a) register EQ-MAP-1 … 4 with R-1/R-2 as admissibility conditions; choose at S9d · (b) choose one now | **(a)** | **2026-10-18: (a)** |
| **S49-D5** | Signal-conditioned heuristics (§D.1) | (a) composition rules for V/V1, no roster change · (b) new roster items | **(a)** | **2026-10-18: (a)**, with the four conditions of §5 (typed at S4.20; fixed per run, never agent-selectable; duplicate detection at S4.16; research-lane constructions excluded) |

---

## 8. Verification (stage 7)

| Script | Proves | Result |
|---|---|---|
| `s49_signal_pc_compatibility.py` (revised 2026-10-18) | R-1 (ranks into MVO ill-defined); R-2 (α = IC·ω·z with the volatility step, invariant to relabelling; benchmark neutrality; units factor 12); PBL EPO at w = 0 and w = 1; O2 constructions (1/N, cap, 1/σ within a selected set) well defined and rank-only; R-4 ordering (0.19 vs 0.69); the S48-D1 identity | PASS |
| `s49_double_counting_dcells.py` | EPO = MVO on shrunk mean and covariance; PBL eq. (22) removes scale, not location; R-7 (exposure, redundancy, look-through risk, signal; zero-investment long–short sleeve as a unit adds no net class exposure); the D-cell tests of §3b; the TC table of §4a | PASS |
| `s49_alpha_sources.py` | Grinold 1994 Exhibits 3–5, Exhibit 7 claims, eqs. (1)–(4) as regressions, fns. 6, 8, 9 (GRI-1, GRI-2: rounding only); momentum needs the volatility step; PBL k = 0 is the constant-IC member; G&K ch. 3 eqs. (35)–(37), sign-only TC √(2/π), Exhibit 11, four examples; CdST Table 1 = eq. (6), long-only TC reproduction, ex post R² ≈ TC²; Gallego secs. 1.4–1.7 | PASS |

---

## 9. Handed forward

| To | Item |
|---|---|
| S4.10 | Anchored EPO with a signal (B7): anchor choice S47-D3 (reminder first); the 60/40 question (RQ-09 note); the level for relative signals; the anchor as TC reference for SAA problems; G&K *Advances* ch. 20 ("Are Benchmark Portfolios Efficient?") |
| S4.11 | C5 × O2 test; research-lane C1–C4 × O2 implementations reuse the S4.11 records |
| S4.12 | D3 × O2 test; PC-D4 TPA with EQ-MAP-3 (residual ω); mean–CVaR (D1) and drawdown (D2) as μ-consuming |
| S4.13 | R-7b: look-through risk for sleeves at every problem level |
| S4.14 | PC-E1 Researcher: the seven research-lane constructions |
| S4.16 | EQ-TC-1 as a reported construction diagnostic; R-7d exposure reports; duplicate detection for compositions near their base method (S49-D5) |
| S4.20 | Composition rules typed (method + conditioning / direction rule; fixed per run, never agent-selectable; S49-D5); R-1 … R-7 as contract predicates; sleeve forms of S49-D2 |
| S6 | ETF constituent holdings for R-7 look-through (gap class B) |
| S9d | EQ-MAP-1 … 4; G&K ch. 9 signal weighting; RQ-32 re-standardisation; blend-weight timing (S48-D6) |
| S11 | Which compositions enter the candidate set (declared before the run); sleeves under R-7; tilt size x within the Policy Statement's active-risk bounds |
| S13c–d | O6 overlays; DM dynamic weight as a timing model (S49-D2, point-in-time); JT cohorts for turnover; TC cost of turnover limits and need-to-trade regions |
| S17 | CdST ex post decomposition (signal vs constraint noise) for the learning loop |
| G4 | EQ-SPLIT-1 amendment for direction rules (S49-D3) with B-46 |

---

## 10. Ladder status after S4.9 (signal ladder)

| Signal | Status |
|---|---|
| SIG-1, SIG-2 and variants | CONSTRUCTION EXTRACTED · **PLACEMENT DETERMINED** · **PC-COMPATIBILITY DETERMINED** (S49-D1 … D5 decided 2026-10-18) |
| Strategy-level scaling (cvol, dyn) | **PLACEMENT DETERMINED** (S49-D2): cvol as a sleeve variant; dyn as a timing model (S13c) |
