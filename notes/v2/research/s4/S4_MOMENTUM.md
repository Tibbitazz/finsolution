# S4.8 Momentum signals — SIG-1 XSMOM, SIG-2 TSMOM, and their variants: construction records

**Document status:** REVIEWED (2026-10-15). Owner decisions S48-D1, D2, D4, D5 and D6 decided 2026-10-15; S48-D3 deferred to S4.9 (§5.1) and decided there as S49-D2 (2026-10-18). · **Basis:**
- S4_PLAN §G (step S4.8; amendment 19, owner decision 2026-10-15) and §F (EQ-SIG-1 … 3);
- `S4_METHODS_OUTLINE.md` §1 (nine-stage workflow) and §2 (S4.8);
- `S4_TAXONOMY.md` (M.SIGNAL → A.DESCRIPTOR); ADR-0012 (signals are deterministic descriptors; μ only through an accepted mapping); ADR-0024 §3–§4 (parameter authority, allocation domains); ADR-0025 (admission ≠ evaluation); ADR-0026 §8 (evidence by use); ADR-0027 D3 (one authoritative risk model per problem).

**Related files:**
- Equations: `S4_EQUATION_REGISTER.md`, S4.8 entries EQ-SIG-1 … EQ-SIG-5.
- Verification: `verification/s48_momentum_constructions.py`, `s48_trend_filters.py`, `s48_kalman_ewma_paleologo.py` (all PASS; synthetic data).
- Issues: `ANG_ISSUES_REGISTER.md` (ANG-23 annotated; source issues HOP-1, DM-1, DM-2, BHM-1, GK-1, EL-1, EL-2, BRU-1, BRU-2, PBL-3).
- Sources: `S4_0_SOURCE_INVENTORY.md` §4 (governing set) and §16 (variants).

**Scope:** how each momentum signal is *constructed*, exactly and point-in-time. **Nothing here says that any signal adds value** (that is S7/S9), nor how a signal becomes portfolio weights or expected returns (S4.9, S9d).

---

## 0. Summary

1. **Two signal objects, one family.** Cross-sectional momentum (SIG-1) ranks assets on their own past return relative to others. Time-series momentum (SIG-2) takes each asset's own past return sign or trend. MOP's decomposition (eqs. 6–7) shows both rest on the same auto-covariance term. They differ by a lead–lag term and by cross-sectional versus squared mean returns. The identities are verified exactly.
2. **Conventions differ by source and domain.**
   - Securities: 12–1 (skip the latest month), as in JT (who skip one week), AMP, DM and BHM, and in our Sørensen score.
   - Futures and asset classes: MOP's TSMOM uses 12–0 (no skip). AMP skip a month in every asset class for uniformity, noting that not skipping is stronger outside equities.
   - **Decided (S48-D1, 2026-10-15):** both signals are run in every domain, and the skip follows the asset type, not the signal type: single stocks 12–1 for XSMOM *and* TSMOM; index ETFs, futures and asset classes 12–0 for both, with 12–1 as a sensitivity test. Sign and magnitude forms are registered variants (§5.1).
3. **Volatility enters three times, and they must not be confused:**
   - (i) **position sizing** inside TSMOM, 40%/σ per asset (MOP eq. 5). This belongs to the short-horizon risk problem (ADR-0027 D3; S48-D2);
   - (ii) **scaling of a whole momentum strategy** (B&SC constant volatility; DM dynamic μ/σ²). This is the same family as PC-A5 (S4.5) and is governed by EQ-SPLIT-1 (S48-D3);
   - (iii) **z-scoring of signals** (G&K's capped z). Here GK-1 applies: the cap's effect depends on the lookback.
4. **The trend-filter family is one linear family** (S4_PLAN amendment 19):
   - a uniform moving average of returns is TSMOM's cumulative return;
   - a moving-average crossover is a triangular weighting of returns;
   - the steady-state Kalman local-level filter is an EWMA of returns, with the same gain as Muth/Paleologo.
   - HP, L1 and Kalman *smoothers* are two-sided. Only the end point of an expanding-window fit is point-in-time.
5. **Variants specified:**
   - residual momentum (BHM; it removes factor exposure: correlation with beta 0.65 for total momentum, −0.02 for residual momentum, on synthetic data);
   - factor momentum, time-series and cross-sectional (G&K; E&L);
   - multi-horizon TSMOM (HOP).
6. **Ten source issues recorded.** The material ones:
   - BHM-1: the paper's words and its own example disagree on whether the regression alpha is removed;
   - DM-1: DM's optimal weight is an approximation; the exact maximiser differs by 0.13% of Sharpe at monthly scale;
   - GK-1: the cap;
   - HOP-1: the per-market volatility estimator is not stated.
7. **Owner decisions S48-D1 … D6** with recommendations (§5).

---

## 1. Sources read (stage 1)

Governing sources are read in full for construction and data sections, and skimmed for empirical sections (stated per row). Versions per the newest-version rule.

| Signal | Source | Version | Read | Notes |
|---|---|---|---|---|
| SIG-1 | Jegadeesh & Titman (1993), *JF* 48(1):65–91 | Published | §I–III in full (pp. 65–74); §IV–IX skimmed | J/K strategies with overlapping cohorts, p. 68; WRSS and eq. (3), pp. 71–72 |
| SIG-1, SIG-2 | Asness, Moskowitz & Pedersen (2013), *JF* 68(3):929–985 | Published | §I in full (pp. 933–939); rest skimmed | MOM2–12, p. 936; non-stock momentum, p. 937; rank weights eq. (1), p. 938; eqs. (2)–(3), p. 939 |
| SIG-2 | Moskowitz, Ooi & Pedersen (2012), *JFE* 104:228–250 | Published | §2–5.2 in full (pp. 230–241); §6 skimmed | Ex-ante volatility eq. (1), p. 233; (k, h) strategies, pp. 233–234; TSMOM eq. (5), p. 236; decomposition eqs. (6)–(7), p. 241 |
| SIG-2 | Hurst, Ooi & Pedersen (2017), "A Century of Evidence on Trend-Following Investing" | SSRN copy (abstract 2993026); the *JPM* published version governs | Construction (pp. 3–5) and App. B (costs) in full | HOP-1 |
| Strategy scaling | Daniel & Moskowitz (2016), *JFE* 122:221–247 | Published | §2.1 (p. 223), §3.4–3.5, §4 (pp. 232–236), App. C–D (p. 245) in full | DM-1, DM-2 |
| Strategy scaling | Barroso & Santa-Clara (2015), *JFE* 116:111–120 | Published | §3–4 in full (pp. 113–116) | Eqs. (5)–(6), p. 115 |
| SIG-1 variant | Blitz, Huij & Martens (2011), *JEF* 18(3):506–521 | Accepted manuscript (published governs) | Methodology (ms pp. 10–12) in full | BHM-1 |
| SIG-2 variant (factors) | Gupta & Kelly (2019), *JPM* Quantitative Special Issue | Published | Factor construction and TSFM (pp. 3–6) in full | GK-1 |
| SIG-1/2 variant (factors) | Ehsani & Linnainmaa, NBER WP 25551 (Feb 2019) | Working version; *JF* 77(3) (2022) governs, requested | §3.2 (p. 7) in full | EL-1, EL-2 |
| Trend filters | Bruder, Dao, Richard & Roncalli (2011), Lyxor | Working paper (SSRN 2289097) | §2.1–2.3.2, §3 in full (pp. 2–16, 22–31); App. A not read | BRU-1, BRU-2 |
| Trend filters | Paleologo (2025) ch. 2 | 1st ed. | Already verified (`s48_kalman_ewma_paleologo.py`) | PAL-1 … PAL-8 |
| Link to EPO | Pedersen, Babu & Levine (2021), *FAJ* 77(2) | Published | Signals and risk models (pp. 135–137) | PBL-3 |
| Supporting, missing | Levine & Pedersen (2016), *FAJ* 72(3) | — | — | Not needed for the equivalences; BRU covers them |

---

## 2. The family (lineage)

```
                       past returns of assets (point-in-time, excess or total)
                 ┌──────────────────────────┴──────────────────────────┐
     SIG-1 cross-sectional (relative)                       SIG-2 time-series (own trend)
     JT 1993 deciles · AMP 2013 ranks ·                     MOP 2012 sign × 40%/σ · HOP 2017 1/3/12-month mix
     PBL linear (r − r̄) · Sørensen percentile               trend filters: uniform MA (= TSMOM), EWMA = Kalman
       ├─ residual (BHM 2011)                                 local level, MA crossover (triangular), Lanczos;
       └─ factors as assets: CSFM (G&K), XS (E&L)             two-sided HP / L1 / smoother = research only
                                                              └─ factors as assets: TSFM (G&K), TS (E&L)
                 └──────────────── common core: own auto-covariance (MOP eqs. 6–7; JT eq. 3) ─┘

     Strategy-level risk management (applies to either): constant volatility (B&SC) · dynamic μ/σ² (DM)
     → same family as PC-A5 / Moreira–Muir (S4.5); governed by EQ-SPLIT-1 (S47-D6)
```

---

## 3. ANG and sources (stage 3)

| Issue | ANG | Sources | Resolution |
|---|---|---|---|
| ANG-23 | Exh. A.1 step 4 lists "technical signals (momentum, trend, mean reversion, relative momentum)" without construction, horizon, lookback or use rule | Momentum and relative momentum = SIG-1; trend = SIG-2 and the trend-filter family; mean reversion = RQ-35 family T3 (not S4.8) | Constructions specified here. Admitted uses remain with S4.9 (objects), S9 (beliefs) and S13d (timing), under ADR-0026 §8 |
| ANG roster | No momentum PC method; signals feed AC agents | XSMOM/TSMOM are our extensions (ADR-0024; HANDOFF §4.6) | Unchanged |

---

## 4. Signal records (stages 2, 4, 5, 7)

Common to every record:
- **Point-in-time:** every input is dated at or before the formation date. Volatilities use data through t−1. Parameters estimated from data (betas, regression coefficients) use expanding or rolling windows ending at t−1 (verified: no look-ahead in each estimator).
- **Returns:** total returns (dividends reinvested) for securities. For TSMOM, *excess* returns over the short rate **in the instrument's currency** (MOP's futures returns are excess by construction). This is a market rate from S6 data, not the user's after-tax deposit rate of S46-D1, which governs portfolio cash, not signals.
- **Output:** a descriptor (A.DESCRIPTOR, ADR-0012) with semantics, version, comparison universe, timestamps. Weights only through S4.9/S9d.

### SIG-1 Cross-sectional momentum (XSMOM)
- **Sources:** JT 1993 (governing for the construction class); AMP 2013 (governing for the rank form and multi-asset use); PBL eqs. (24)–(25) (linear form, EPO link); Sørensen/Storebrand (percentile, `S4_SCORING_SORENSEN.md` S-4).
- **Definition (EQ-SIG-1):**
  - formation return R_i = P_{i,t−1−s}/P_{i,t−J−s} − 1 over J months, skipping s;
  - JT: J ∈ {3, 6, 9, 12}, holding K ∈ {3, 6, 9, 12}, skip 0 or 1 week;
  - AMP/DM/BHM/Sørensen: J = 12, s = 1 month (MOM2–12).
  - **Decided V0 (S48-D1):** single stocks 12–1; index ETFs, futures and asset classes 12–0 (12–1 as sensitivity).
- **Forms of the cross-sectional object:**
  - decile portfolios (JT: equal-weighted; DM: value-weighted);
  - rank weights w_i = c_t(rank(S_i) − mean rank), $1 long and $1 short (AMP eq. 1);
  - linear w_i ∝ r_i − r̄ (WRSS; PBL eq. 24, scaled so the positive signals sum to 1);
  - percentile score (Sørensen).
- **JT holding rule:** overlapping cohorts; each month 1/K of the book is replaced (verified: the cohort average equals the aggregated weights).
- **Universe filters (sources):**
  - AMP: largest stocks covering 90% of market capitalisation; price ≥ $1; at least 12 months of history;
  - DM: at least 8 monthly returns in the 11-month formation window.
  - These are S5 choices.
- **Inputs:** monthly total-return series per asset; universe snapshot at t.
- **Parameters:** J, s, holding K, form (S48-D1, S48-D4). Authority: fixed per source (V0); alternatives sensitivity-only (S7 grid).
- **Invariants (verified):**
  - AMP weights sum to zero, with +1 and −1 legs;
  - invariant to strictly increasing transforms of S;
  - the median asset gets zero weight when N is odd.
- **Allocation domains:** individual security; asset class (AMP); fund/ETF; strategy/sleeve (factors, below).
- **Agent-readable summary:**
  - *Intuition:* assets that beat their peers over the past year tend to keep doing so for a few months.
  - *Sensitivities:* skip month; universe; crash risk after market rebounds (DM).
  - *Valid comparison:* the same universe and date.

#### SIG-1 variant R: residual momentum (BHM 2011)
- **Definition (EQ-SIG-1R):**
  - regress each stock's excess return on the Fama–French three factors over months t−36 … t−1 (complete history required);
  - residual momentum = Σ u over t−12 … t−2, divided by the standard deviation of u over the same 11 months;
  - deciles, equal-weighted, with JT overlapping holding.
- **BHM-1:** whether u = r − β̂′f (alpha not subtracted, V0) or r − α̂ − β̂′f (V1); the text and its example disagree.
- **Property (verified):** removes the factor component of momentum. With the market trending in the formation window, the correlation of the score with market beta is 0.65 for total momentum and −0.02 for residual momentum.
- **Inputs:** factor returns for the stock's region (S6: Fama–French regional factors or our own). **Parameters:** window 36, formation 12–1, model FF3 (fixed, V0).

#### SIG-1 variant F: cross-sectional factor momentum
- **Definition (EQ-SIG-1F):**
  - factors (long–short portfolios) treated as assets;
  - E&L: long factors with above-median prior-year return, short those below;
  - G&K CSFM: the analogous construction on their 65 factors.
- **Note:** E&L find that the time-series version dominates (variant 2F).

### SIG-2 Time-series momentum (TSMOM)
- **Sources:** MOP 2012 (governing); HOP 2017 (multi-horizon); PBL eq. (23) (EPO link).
- **Definition (EQ-SIG-2):**
  - per instrument s, r^{TSMOM}_{t,t+1} = sign(r^s_{t−12,t})·(40%/σ^s_t)·r^s_{t,t+1} (MOP eq. 5);
  - portfolio = equal-weighted average over available instruments;
  - (k, h) versions with JT-style overlapping holding (MOP §3.2).
- **Ex-ante volatility (MOP eq. 1):**
  - σ²_t = 261·Σ_i (1−δ)δ^i (r_{t−1−i} − r̄_t)², with r̄_t the EWMA mean;
  - δ/(1−δ) = 60 days (centre of mass), so δ = 60/61;
  - **half-life 41.9 days; e-folding 61 days** (verified; conventions registered per PAL-7);
  - σ at t−1 is applied to the return at t.
- **HOP 2017:**
  - equal-weighted combination of the 1-, 3- and 12-month signals;
  - per-market positions at equal volatility;
  - the portfolio scaled to a 10% ex-ante target with a rolling 3-year equal-weighted covariance of monthly returns (fn. 7);
  - costs (App. B, Exh. B1) and 2/20 fees simulated.
  - **HOP-1:** the per-market volatility estimator is not stated.
- **PBL eq. (23):** signal s_i = 0.1·σ_i·sign(r_{12}); with γ = n/40% the fully shrunk EPO weights are **proportional** to MOP's (factor 0.1; PBL-3: the paper says "exactly matched"; the Sharpe ratio is unaffected).
- **Inputs:** daily excess returns (for σ); monthly excess returns (signal); the instrument-currency short rate. σ belongs to the **short-horizon risk problem** (ADR-0027 D3; S48-D2).
- **Parameters:**
  - lookback k (12, or the HOP mix) and holding h (1): fixed V0; **skip by asset type (S48-D1): single stocks 12–1, index ETFs, futures and asset classes 12–0**; sign (V0) vs magnitude (variant);
  - 40% per instrument and 10% portfolio: scale constants, superseded by the engine-level target EQ-SPLIT-1;
  - σ estimator: system-estimated (S48-D2).
- **Invariants (verified):**
  - σ uses only data through t−1;
  - centre-of-mass identity;
  - the HOP combined position lies in {−1, −⅓, ⅓, 1} per unit of market volatility.
- **Allocation domains:** asset class; fund/ETF; individual security (with care: TSMOM on single stocks is not zero-net, as E&L note citing Goyal & Jegadeesh (2018, *RFS*; MISSING — LOCATED)); strategy/sleeve (factors).
- **Agent-readable summary:**
  - *Intuition:* an asset that has risen over the past year tends to keep rising for a few months.
  - *Sensitivities:* lookback; turning points (whipsaw); the volatility estimator.
  - *Valid comparison:* the same instrument and horizon; never across currencies without the basis.

#### SIG-2 variant F: time-series factor momentum
- **Definition (EQ-SIG-2F):**
  - **E&L:** long factors with positive prior one-year return, short those with negative; equal-weighted legs.
  - **G&K eq. (1):** s_{i,j,t} = clip(Σ_{τ=1..j} f_{i,t−τ+1}/σ_{i,j,t}, −2, 2), where σ is the annualised factor volatility over 3 years (j < 12) or 10 years (j ≥ 12); legs rescaled to $1 long and $1 short.
- **GK-1:** dividing a j-month sum by an annual σ is a z-score only at j = 12. The ±2 cap binds 0.0% at j = 1, 4.5% at j = 12 and 37% at j = 60 (verified).
- **EL-2:** the long–short is undefined when all factors share the sign (rule needed; S48-D6).
- **Use for long-only users:** factor momentum is tradable only where the account permits shorting factor legs. For long-only Policy Statements it is a timing input for factor tilts (RQ-11, RQ-17), not a sleeve. S4.9 decides the objects.

#### SIG-2 variant T: the trend-filter family (amendment 19)
- **Sources:** Bruder et al. 2011 §2.2–2.3, §3; Paleologo 2025 ch. 2 (Muth; PAL-1 … PAL-8).
- **Definition (EQ-SIG-2T):** a causal linear filter of log returns, μ̂_t = Σ_{i≥0} a_i R_{t−i}. Members (all verified):
  - **uniform:** a_i = 1/n for i < n. The sign equals TSMOM's sign exactly.
  - **EWMA / Kalman local level:** a_i = (1 − e^{−λ})e^{−λi}, with λ = −ln(1 − κ). The gain κ = 2σ_η/(σ_η + √(σ_η² + 4σ_ζ²)) equals Muth's (−q + √(q² + 4q))/2. Half-life is ln 2/λ.
  - **moving-average crossover** 2/(n₁ − n₂)·(ȳ_{n₂} − ȳ_{n₁}): triangular weights peaking at the short horizon; expectation (n₁ − n₂)/2·m under drift m;
  - Lanczos / asymmetric kernels (Bruder p. 8).
- **Two-sided smoothers** (HP/L2 x̂ = (I + 2λD′D)⁻¹y, L1 trend filter, Kalman smoother) revise past estimates when new data arrive (verified). They are **research tools only**; a live signal uses the end point of an expanding-window fit.
- **Trend detection** (Bruder §3.2.2): the Mann statistic with variance n(n−1)(2n+5)/18. BRU-2: bounds ±n(n−1)/2.
- **Precision limit:** the drift estimator's variance depends on calendar span, not sampling frequency (Paleologo pp. 38–39; verified). Filters trade noise against lag; none escapes this.
- **Parameters:** kernel and horizon or half-life, from a pre-registered grid (S48-D5). The half-life convention is declared as 2^{−s/h}.

### Strategy-level risk management of momentum (EQ-SIG-4)
- **Constant volatility (B&SC eqs. 5–6):**
  - σ̂²_t = 21·Σ_{j=0..125} r²_{d_{t−1}−j}/126, uncentred daily returns, the 126 sessions before the month;
  - scaled return (σ_target/σ̂_t)·r_t, σ_target = 12% a year (monthly 12%/√12);
  - weights ranged 0.13–2.00 in the paper (uncapped);
  - robustness: 1- and 3-month windows and EWMA half-lives of 1, 3 and 6 months give "nearly identical" results (fn. 14).
- **Dynamic (DM eq. 6):**
  - w*_t = (1/2λ)·μ_t/σ²_t;
  - μ_t from a regression of WML on I_B·σ̂²_m, where I_B = 1 if the market's past 24-month return is negative and σ̂²_m is the 126-day market variance;
  - σ_t from GJR-GARCH plus the 126-day realised volatility (App. D, in-sample);
  - the **out-of-sample** version (§4.3, eq. 9) uses an expanding-window regression and the 126-day WML variance only.
  - **DM-1:** eq. (6) rests on App. C's approximation; the exact maximiser is w ∝ μ/(σ² + μ²). The gap is 0.13% of Sharpe at monthly scale and 18% if μ is six times larger (verified).
  - **DM-2:** the main text's σ² definition contains a typo, (R² − μ)², against App. C's (R − μ)².
- **Relation:** cvol = dyn when μ/σ is constant (verified). Both are PC-A5-type scalers (Moreira–Muir; S4.5) and fall under EQ-SPLIT-1 and the leverage cap (S47-D6; S48-D3).

---

## 5. Owner decisions (stage 6)

### 5.1 Decisions recorded (owner, 2026-10-15, after discussion)

The draft options are kept in §5.2. The discussion revised D1 and D6 and moved D3 to S4.9.

- **S48-D1 (decided, revised): both signals in every domain; skip by asset type; sign and magnitude.**
  - The skip month exists to avoid the one-month reversal of single stocks (bid–ask bounce and microstructure; Jegadeesh 1990; AMP p. 936). It applies to TSMOM on a stock as much as to XSMOM. Liquid index products show little of it: AMP (p. 937) report stronger momentum outside equities without the skip, and MOP (fn. 10) say their XSMOM results do not depend on it.
  - V0:
    - single stocks (Oslo, US, global): XSMOM and TSMOM 12–1;
    - index ETFs, futures and asset classes: XSMOM and TSMOM 12–0, with 12–1 as a sensitivity test;
    - HOP's 1/3/12-month TSMOM mix as a variant;
    - holding 1 month; JT overlapping cohorts as a turnover variant (S13).
  - **Sign vs magnitude.** MOP's TSMOM uses only the sign, so among assets with positive trends the weights differ only by volatility (1/σ). Magnitude forms (G&K's capped z; the trend estimate μ̂; expected returns proportional to trend strength) are registered variants; whether magnitude adds to sign is an S7 question (MOP Fig. 1 shows both predict).
  - **Identity (linear forms):** (1/N)·rᵢ = (1/N)·(rᵢ − r̄) + r̄/N. Magnitude-weighted TSMOM is XSMOM's relative tilt plus a common position sized by the average trend, so "all long, the stronger ones more" comes from the cross-sectional part.
  - **Cautions recorded:**
    - single-stock TSMOM partly re-labels average equity returns (the 12μ′μ/N term of MOP eq. 7), so it is evaluated against an always-long control, as MOP do (S7). Goyal & Jegadeesh (2018) on net exposure: MISSING — LOCATED. Huang, Li, Wang & Zhou (2020, *JFE*) on time-series predictability: cited from memory, not verified;
    - for long-only users, XSMOM *selects* and TSMOM *times* (hold or cash);
    - XSMOM needs a meaningful cross-section, so a minimum number of assets is declared per universe (S5/S7).
- **S48-D2 (decided): TSMOM sizing volatility.**
  - MOP's EWMA (centre of mass 60 days, half-life 41.9 days, demeaned, ×261) is the reference and the reproduction oracle. In production σ comes from the authoritative short-horizon risk model chosen at S10 (ADR-0027 D3).
  - **Frequency:** daily returns where prices are synchronous and liquid; 2–5-day returns where they are not (different closing times, e.g. Oslo vs New York; stale fund NAVs; thin ETFs; PBL used 3-day returns for correlations). Units must match (annualised σ against an annual target), not frequencies: volatility precision improves with sampling frequency, drift precision does not (Paleologo pp. 38–39; `s48_trend_filters.py`). Daily data understate monthly risk when returns are positively autocorrelated (B&SC fn. 15).
- **S48-D3 (deferred to S4.9): strategy-level scaling.** Constant-volatility (B&SC) and dynamic (DM) scaling apply only if momentum is held as its own sleeve. When momentum is a return signal, every portfolio is scaled once by the engine-level target (EQ-SPLIT-1, S47-D6). S4.9 decides whether momentum may exist as a sleeve. For long-only accounts a long–short sleeve is not tradable. *[2026-10-18, decided as S49-D2]* Sleeves follow R-7 (`S4_SIGNAL_PC_COMPATIBILITY.md` §3a, §7): long-only sleeves are tilts inside their host class; zero-investment long–short sleeves only where shorting is permitted. Base case without sleeve-level scaling; constant volatility (B&SC) a registered variant (long–short as published; long-only on the tilt size); DM's dynamic weight a timing model (S13c), point-in-time only.
- **S48-D4 (decided): SIG-1 outputs a rank-based score descriptor** (transformation per RQ-29 at S9c).
  - AMP eq. (1) rank weights are the reference factor-return construction; JT deciles are the reproduction oracle. Weights only through S4.9/S9d mappings.
  - XSMOM is long–short only as an academic *factor*. As a *signal* it serves long-only portfolios: top-ranked holdings, benchmark-relative tilts, or a long-only optimizer.
- **S48-D5 (decided in principle): trend filters.** Causal members only. Horizons and half-lives come from a pre-registered grid whose values are set at S7. No likelihood- or cross-validation-calibrated parameters in V0. Two-sided smoothers are for research only.
- **S48-D6 (decided, revised): variants.**
  - **Residual momentum:** V0 = BHM's example reading (alpha not subtracted), V1 = alpha subtracted, as a sensitivity test; FF3; 36 months.
  - **Factor momentum:** stock-level momentum stays an ingredient of the composite score. Factor momentum is admitted for long-only users as:
    - **time-varying weights on the composite's factor blend** (e.g. the ⅓, ⅓, ⅙, ⅙ weights, RQ-32), bounded and evaluated at S7; or
    - cross-sectional rotation among factor ETFs.
  - Time-series factor signals are computed on long–short or active factor returns (ETF minus market), never on a long-only ETF's raw return, which mostly tracks the market.
  - V0 = Ehsani & Linnainmaa's sign rule; V1 = Gupta & Kelly's capped z; empty-leg rule (EL-2): hold the non-empty leg.
  - Confirmed against the *JF* 2022 version when it arrives (EL-1).
  - **The difference from long-only stock XSMOM:** XSMOM decides which stocks; factor momentum decides how much weight each factor gets. The two can disagree (for example, a cheap stock that rose less than an expensive one).

### 5.2 Draft options (as proposed 2026-10-15, before the discussion)

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **S48-D1** | Formation, skip and holding conventions | (a) each signal keeps its governing source's convention as V0: securities 12–1 (SIG-1, BHM, Sørensen); asset-class XSMOM 12–1 (AMP); TSMOM 12–0 (MOP); HOP 1/3/12 mix as a variant; holding 1 month, JT cohorts as a turnover variant (S13) · (b) one uniform 12–1 everywhere · (c) chosen by the S7 grid | **(a)**, with the alternatives pre-registered as sensitivity variants at S7. Choosing by backtest (c) is the overfitting route the S7 protocol exists to prevent |
| **S48-D2** | TSMOM position-sizing volatility | (a) MOP's EWMA (centre of mass 60 days, demeaned, ×261) as V0 and reproduction oracle; in production σ comes from the authoritative short-horizon risk model chosen at S10 (ADR-0027 D3) · (b) MOP's estimator permanently · (c) a per-signal estimator | **(a)**. (c) contradicts ADR-0027 D3; (b) would freeze a choice S10 must make on risk accuracy |
| **S48-D3** | Strategy-level risk management of momentum | (a) specify constant volatility (B&SC) as a construction variant under EQ-SPLIT-1 with the leverage cap; register DM's dynamic rule as a timing model, specified only in its point-in-time (expanding-window) form · (b) constant volatility only · (c) neither (the engine-level target alone) | **(a)**. Whether either improves anything is an S7 question; DM's in-sample parameters are not admissible |
| **S48-D4** | What SIG-1 outputs | (a) a rank-based score descriptor (transformation per RQ-29 at S9c); AMP eq. (1) rank weights as the reference factor-return construction for evaluation and as inputs to factor momentum; JT deciles as the reproduction oracle · (b) portfolio weights directly | **(a)**, consistent with ADR-0012 §3 and the Sørensen record; weights only through S4.9/S9d |
| **S48-D5** | Trend-filter family | (a) causal members only (uniform, EWMA/Kalman, crossover, Lanczos); horizons and half-lives from a pre-registered grid (e.g. matched to 1, 3 and 12 months); no maximum-likelihood or cross-validated calibration in V0; two-sided smoothers for research · (b) also data-calibrated parameters (Bruder §3.1) | **(a)**. Bruder note that likelihood calibration yields very short-term trends; calibration adds estimation error and a degree of freedom S7 would have to police |
| **S48-D6** | Variant specifications | Residual momentum: V0 = BHM's example reading (alpha not subtracted) with V1 = alpha subtracted as sensitivity; FF3, 36 months. Factor momentum: V0 = E&L sign rule (12 months, equal-weighted legs), V1 = G&K capped z (GK-1 noted); empty-leg rule (EL-2): hold the non-empty leg at $1. Both pending the *JF* 2022 check (EL-1) | **As stated.** The E&L construction is confirmed against the *JF* version when it arrives |

---

## 6. Verification (stage 7)

| Script | Reproduces / proves | Result |
|---|---|---|
| `s48_momentum_constructions.py` | JT overlapping cohorts (cohort average = aggregated weights; 1/K replaced monthly); AMP eq. (1) invariants; PBL eqs. (24)–(27) and PBL-3; MOP eq. (1) centre of mass = 60 days = half-life 41.9 days, no look-ahead; **MOP eqs. (6)–(7) exact** (sample-moment identities to 1e-12); JT eq. (3) (ratio 0.9998); BHM factor neutrality and BHM-1; G&K eq. (1) and GK-1; E&L legs; B&SC eqs. (5)–(6), no look-ahead; DM eq. (6) vs the exact maximiser (DM-1); HOP combination | PASS |
| `s48_trend_filters.py` | Uniform MA of returns = TSMOM sign; crossover = triangular weights, expectation (n₁ − n₂)/2·m (BRU-1); Kalman gain = Muth gain = EWMA (λ = −ln(1 − κ); 14-day half-life at 5%); HP and L1 two-sided, end point point-in-time; L1 piecewise linear; Mann variance and bound (BRU-2); drift precision independent of sampling frequency | PASS |
| `s48_kalman_ewma_paleologo.py` | Paleologo ch. 2/5/6 (PAL-1 … PAL-8) | PASS (2026-10-15) |

No published example is reproduced numerically: the governing papers' results need CRSP/futures data. The checks are construction identities, invariants and point-in-time properties on synthetic data, as the S4.8 plan row specifies.

---

## 7. Handed forward

| To | Item |
|---|---|
| S4.9 | Which objects each signal may become (signal, conditioned universe, exposure rule, μ mapping, standalone strategy, overlay); PBL eqs. (23)–(27) as the EPO link; **S48-D3** (strategy-level scaling, only if a momentum sleeve is admitted); factor momentum as time-varying blend weights (S48-D6) |
| S4.13 | SIG-2's σ (short-horizon risk problem); B&SC/DM σ; BHM's factor model |
| S5 | Universe filters (AMP 90% capitalisation, price floor, history minimums) |
| S6 | Daily total and excess returns; the instrument-currency short rate; regional factor returns; factor portfolios (French/AQR libraries or S9c-built) |
| S7 | Pre-registered grids (lookback, skip, filter horizons, variants); look-ahead tests; costs (HOP Exh. B1 as reference only); multiple-testing control |
| S9 | Factor-momentum timing (RQ-11); earnings momentum (Novy-Marx; S6-gated); momentum gap (Huang); trends and cycles (Ang 2023) |
| S10 | The authoritative short-horizon σ (S48-D2) |
| S13 | JT overlapping cohorts as a turnover device; DM crash conditioning as a timing candidate (RQ-17) |

---

## 8. Ladder status after S4.8 (signal ladder, S4_PLAN §C.1)

| Signal | Status |
|---|---|
| SIG-1 XSMOM (+ variants R, F) | SOURCE REVIEWED · CONSTRUCTION EXTRACTED · construction checks PASS; specification decided (S48-D1, D4, D6) |
| SIG-2 TSMOM (+ variants F, T) | SOURCE REVIEWED · CONSTRUCTION EXTRACTED · construction checks PASS; specification decided (S48-D1, D2, D5 in principle, D6) |
| Strategy-level scaling (cvol, dyn) | CONSTRUCTION EXTRACTED · **PLACEMENT DETERMINED** (S49-D2, 2026-10-18): cvol as a sleeve variant; dyn as a timing model (S13c) |
