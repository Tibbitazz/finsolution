# S4.11 Risk-structured methods: PC-C1 … PC-C5

**Document status:** REVIEWED · **S4.11 DONE (2026-10-18).** Owner decisions S411-D1 … S411-D5 accepted as recommended, 2026-10-18 (§4). · **Basis:** S4_PLAN §G (step S4.11); `S4_METHODS_OUTLINE.md` §1 (workflow, method-record template); `S4_PC_SOURCE_MAP.md` (all five sources in hand); ADR-0024 §3–§6; ADR-0025; ADR-0027 D3; invariants I-1 … I-9 (`S4_GITHUB_IMPL_REVIEW.md` §10); S4.9 (C5 × O2 pending cell; S49-D1 research-lane rule); S4.6 (EQ-MVO-4, 4a).

**Related files:** `verification/s411_risk_structured.py` (PASS); existing `s44_risk_parity_spinu.py`, `s44_hrp_lopez_de_prado.py`; register EQ-RS-1 … EQ-RS-5 (`S4_EQUATION_REGISTER.md`); issue MCA-4 (`ANG_ISSUES_REGISTER.md`).

**Scope:** the mathematics of five μ-free methods that use only the risk model. **Nothing here ranks them** (S7; ADR-0025).

---

## 0. Summary

1. **All five sources read and verified.** Published examples reproduced: MRT's four-asset example in full (1/n, minimum variance and ERC tables, including the constant-correlation cases); Choueifaty & Coignard's Examples 1–2; Varadi et al.'s worked example; López de Prado's Exhibit 7 (S4.4). Clarke, de Silva & Thorley's 2011 single-index closed form for long-only GMV equals the numerical optimum.
2. **Each method in one line:**
   - **C1 GMV:** minimise variance; long-only with bounds in the source (CdST 2006: 3% cap for 1,000 stocks).
   - **C2 ERC:** equal risk contributions; unique long-only solution (Spinu), between GMV and 1/N in risk.
   - **C3 HRP:** cluster by correlation, then split risk down the tree by inverse variance.
   - **C4 MDP:** maximise the diversification ratio; equals GMV on the correlation matrix, rescaled by 1/σ.
   - **C5 MinCorr:** a heuristic that over-weights assets with low average correlation, then divides by volatility.
3. **Verified equivalences** (§2): with uncorrelated assets GMV = HRP = 1/σ² and ERC = MDP = 1/σ; with a constant correlation ERC = MDP = 1/σ; with equal volatilities MDP = GMV; σ_GMV ≤ σ_ERC ≤ σ_1/N always. **S4_PLAN's example "maximum diversification = GMV when correlations are equal" is wrong:** it holds when volatilities are equal; with equal correlations MDP equals ERC and 1/σ.
4. **What each method is optimal for** (§2): GMV if all expected returns are equal; MDP if expected returns are proportional to volatility; ERC if correlations are constant and Sharpe ratios equal; market capitalisation if expected returns are proportional to ρ_iB σ_i.
5. **Open choices** (§4): the GMV constraint set; HRP published (with a canonical ordering) vs tree split; the minimum-correlation variant; constraint handling for the three methods without native constraints; failure behaviour.
6. **New source issue MCA-4:** MinCorr and MinCorr2 are undefined for two assets or a constant correlation matrix; MinCorr2 also whenever all average correlations are equal (e.g. two identical blocks).
7. **C5 × O2** (the pending S4.9 cell): defined and rank-only on a selected set of at least three assets → research lane under S49-D1.

---

## 1. Sources read (stage 1)

| Method | Governing source | Read | Supporting |
|---|---|---|---|
| C1 | Clarke, de Silva & Thorley (2006), "Minimum-Variance Portfolios in the U.S. Equity Market", *JPM* 33(1):10–24 (scan) | In full 2026-10-18 | CdST (2011), "Minimum-Variance Portfolio Composition", *JPM* 37(2):31–45 (single-index closed forms, eqs. 1–2, A-2 … A-7); EQ-MVO-4, 4a (S4.6) |
| C2 | Maillard, Roncalli & Teïletche (*JPM* 36(4), 2010; working version May 2009 read) | In full | Spinu 2013 (solver; S4.4) |
| C3 | López de Prado (*JPM* 42(4), 2016; working version 23 May 2016) | S4.4 (reviewed; Exhibit 7 exact) | — |
| C4 | Choueifaty & Coignard (2008), "Toward Maximum Diversification", *JPM* 35(1):40–51 | In full 2026-10-18 | Choueifaty, Froidure & Reynier 2013 (not located; optional) |
| C5 | Varadi, Kapler, Bee & Rittenhouse (2012), *The Minimum Correlation Algorithm*, CSS Analytics (authors' release) | S4.4 (identity; algorithm transcribed); comparison section 2026-10-18 | Kapler's `min.corr`, `min.corr2` (read, never executed) |

Source details that matter:
- **CdST 2006:** 1,000 largest US stocks; 60-month (or 250-day) covariance structured by five principal components or Ledoit–Wolf shrinkage; long-only with a 3% upper bound and full investment; a long/short variant (budget only) ran about 170/70. Covariances are uncentred (mean not subtracted). These are estimation choices; ours come from S10 (ADR-0027 D3).
- **MRT:** ERC is defined long-only (0 ≤ x ≤ 1); eq. (8) shows ERC is the minimum-volatility portfolio subject to Σ ln x_i ≥ c, between GMV (c = −∞) and 1/N (c = −n ln n).
- **C&C:** their tests used long-only weights, a 4% risk-contribution cap and UCITS limits. These are their implementation constraints, not part of the method.
- **Varadi et al.:** introduce two variants (MinCorr, MinCorr2) without a formal recommendation. MinCorr2 ranked best on their own diversification-efficiency score; it is "less biased towards anti-correlated assets". Their "Risk Parity" comparator is inverse volatility (correlations ignored), i.e. PC-A3, not PC-C2.

---

## 2. Verified relations across the five methods

| Condition | GMV | ERC | HRP | MDP | Source / check |
|---|---|---|---|---|---|
| Uncorrelated assets | 1/σ² | 1/σ | 1/σ² | 1/σ | `s411`; MRT eq. (3) with ρ = 0; C&C eq. (4) |
| Constant correlation ρ | depends on ρ (= 1/σ only at ρ = −1/(n−1)) | 1/σ | not unique (tied distances) | 1/σ | MRT eq. (3), App. A.1; C&C eq. (4) |
| Equal volatilities | GMV | MRT eq. (4) fixed point | — | **= GMV** | C&C p. 43; `s411` |
| Two assets | MRT p. 8 formula | 1/σ (independent of ρ) | 1/σ² | 1/σ | MRT §3.1; LdP; C&C Ex. 1 |
| Risk ordering | σ_GMV ≤ σ_ERC ≤ σ_1/N | | | | MRT App. A.3; 200 random cases |

**Implied expected returns that make each portfolio the tangency portfolio** (C&C eqs. 11–12; MRT §3.5; verified): GMV ⇔ equal expected returns; MDP ⇔ μ ∝ σ; ERC ⇔ constant correlation and equal Sharpe ratios; market capitalisation ⇔ μ_i ∝ ρ_iB σ_i. These belong on each method's agent-readable card: a μ-free method still carries an implicit belief.

---

## 3. Method records (stages 2, 4, 5, 7)

### PC-C1 Global minimum variance

- **Identity:** PC-C1 · Global minimum variance (ANG Exh. 3; "Global min vol" in Exh. 4, the same portfolio: ANG-07, verified) · family C · `M.PC` · roster v0.
- **Sources:** governing CdST 2006 (pp. 12–14: long-only, 3% upper bound, budget; pp. 19–20: long/short); supporting CdST 2011 (eqs. 1–2, A-5, A-6, A-7); EQ-MVO-4 (unconstrained closed form), EQ-MVO-4a (long-only = unconstrained GMV of a shrunk matrix, Jagannathan–Ma).
- **Definition:** w = argmin w′Σw s.t. 1′w = 1 and the constraint set (S411-D1). Unconstrained: w = Σ⁻¹1/1′Σ⁻¹1.
- **Single-index insight (CdST 2011, verified):** with Σ = σ²_M ββ′ + diag(σ²_ε), w_i = (σ²_LMV/σ²_εi)(1 − β_i/β_L) for β_i < β_L, else 0; β_L from the running sums over the lowest betas (A-6). Systematic risk, not idiosyncratic risk, decides membership; long-only GMV holds the low-beta minority (synthetic test: 33 of 150 stocks, threshold β_L = 0.79 against β_LS = 1.16).
- **Inputs:** Σ from the problem's authoritative risk model. Not used: μ.
- **Parameters:** bounds and long/short permission: user-authorized (Policy Statement; account permissions). No method parameter.
- **Constraints:** native (quadratic programme): long-only, per-asset bounds, group bounds.
- **Allocation domains:** asset class, fund/ETF, security, sleeve.
- **Output and failures:** weights; `INFEASIBLE_CONSTRAINTS` (e.g. N·u < 1); `SINGULAR_RISK_MODEL` for the unconstrained form.
- **ANG vs source:** ANG-07 (naming; resolved).
- **Invariants:** sums to 1; permutation-equivariant; scale-invariant in Σ; σ minimal among feasible portfolios.
- **Verification:** `s411_risk_structured.py` — closed form; long-only; single-index closed form = QP; 3% cap. PASS.
- **Agent-readable summary:** *Objective:* lowest ex-ante variance. *Intuition:* holds low-beta, low-correlation assets. *Implicit belief:* equal expected returns. *Sensitivities:* the risk model, especially low estimated variances ("error maximisation", CdST p. 14). *Failure modes:* concentration in a few low-volatility assets (MRT example: 74.5% in one asset). *Valid comparisons:* ERC, MDP, HRP on risk and concentration. *Invalid:* treating its return as a forecast.

### PC-C2 Equal risk contribution (ERC)

- **Identity:** PC-C2 · Risk parity (ERC) · family C · `M.PC` · roster v0.
- **Sources:** governing MRT (eqs. 1–8; §3.5; §4.1; App. A.1, A.3); Spinu 2013 (solver, Thm 3.4; S4.4).
- **Definition:** x ∈ [0, 1]ⁿ, 1′x = 1, x_i(Σx)_i = x_j(Σx)_j for all i, j (EQ-RS-1). Equivalently x_i = 1/(nβ_i) with β_i the beta of asset i on the portfolio (eq. 5), or the minimum-volatility portfolio subject to Σ ln x_i ≥ c (eq. 8).
- **Inputs:** Σ (authoritative risk model). Not used: μ.
- **Parameters:** budgets b = 1/n (fixed; general budgets are the §D.1 research-lane candidate); solver tolerance (fixed, declared).
- **Constraints:** long-only by definition. **Bounds are not native:** the long-only ERC is unique, so a bound below an ERC weight makes exact ERC infeasible (MRT example: 38.4% in asset 1 against, say, a 30% cap). S411-D4.
- **Allocation domains:** asset class, fund/ETF, sleeve; security (Spinu: N = 1,400 tested).
- **Output and failures:** weights; `NOT_POSITIVE_DEFINITE`; `CONSTRAINT_CONFLICT` (bound below the unique ERC weight).
- **ANG vs source:** consistent.
- **Invariants:** equal risk contributions; unique; permutation-equivariant; σ_GMV ≤ σ_ERC ≤ σ_1/N.
- **Verification:** MRT §4.1 tables (1/n: σ 11.5%, contributions 12.3/26.4/14.1/47.2%; MV: σ 8.6%, 74.5/0/15.2/10.3%; ERC: σ 10.3%, 38.4/19.2/24.3/18.2% with marginal risks 0.067/0.134/0.106/0.141); constant-correlation cases; eqs. (3)–(8); A.1; A.3; §3.5. PASS.
- **Agent-readable summary:** *Objective:* every asset contributes the same share of risk. *Intuition:* a risk-balanced middle ground between GMV and 1/N. *Implicit belief:* equal Sharpe ratios with constant correlations. *Sensitivities:* the risk model; high-volatility assets get small weights. *Failure modes:* conflicts with bounds; leverage needed to reach high risk targets (EQ-SPLIT-1 handles). *Valid comparisons:* 1/σ (equal under constant correlation), MDP. *Invalid:* calling 1/σ "risk parity" when correlations differ (Varadi et al.'s usage).

### PC-C3 Hierarchical risk parity (HRP)

- **Identity:** PC-C3 · HRP · family C · `M.PC` · roster v0.
- **Sources:** governing López de Prado 2016 (stages 1–3, pp. 5–8; Appendix A.3–A.4 code; tree-split suggestion, p. 11); S4.4 review (HRP-1, HRP-2).
- **Definition (EQ-RS-2):** distance d_ij = √(½(1 − ρ_ij)); single-linkage clustering on the distance-of-distances; then **V0** (published): quasi-diagonal leaf order and recursive bisection of the ordered list, or **V1** (tree split): bisection along the dendrogram's own children. At each split, cluster variances use inverse-variance weights and the split factor is α = 1 − V₁/(V₁ + V₂).
- **Inputs:** Σ (correlations for clustering, variances for splitting). Not used: μ.
- **Parameters:** linkage = single (fixed V0; alternatives sensitivity-only); distance formula (fixed); variant V0/V1 (S411-D2); for V0, the canonical ordering convention (fixed, declared).
- **Constraints:** long-only and fully invested by construction; bounds not native (S411-D4).
- **Allocation domains:** asset class, fund/ETF, security (designed for large N).
- **Output and failures:** weights; `INVALID_CORRELATION` (non-finite entries); correlations clipped to [−1, 1] (HRP-2).
- **ANG vs source:** ANG-42 (order dependence; linkage unstated) → S411-D2.
- **Invariants:** sums to 1, positive; uncorrelated assets → 1/σ² (verified); two assets → inverse variance; **I-7 permutation invariance:** V1 satisfies it; V0 changed weights in 32 of 60 random reorderings and satisfies it only after a declared canonical ordering (which is itself an arbitrary convention that moves weights).
- **Verification:** `s44_hrp_lopez_de_prado.py` (Exhibit 7 exact; order dependence) and `s411_risk_structured.py` (V1 invariance; V0 canonical determinism; diagonal and two-asset limits; clipping). PASS.
- **Agent-readable summary:** *Objective:* allocate risk top-down through a correlation hierarchy without inverting Σ. *Intuition:* similar assets share a budget. *Sensitivities:* the linkage and, for V0, the input order. *Failure modes:* tied distances (constant correlation) make the tree arbitrary. *Valid comparisons:* ERC, inverse variance. *Invalid:* treating V0 weights as order-independent.

### PC-C4 Maximum diversification (MDP)

- **Identity:** PC-C4 · Most-Diversified Portfolio · family C · `M.PC` · roster v0.
- **Sources:** governing Choueifaty & Coignard 2008 (eqs. 1–9, 11–12; Examples 1–2; long-only section, p. 43).
- **Definition (EQ-RS-3):** maximise DR(w) = w′σ/√(w′Σw) under the constraint set. Unconstrained: w ∝ σ⁻¹C⁻¹1 (eq. 4). Long-only: minimise y′Cy with y = σ∘w, 1′y = 1, y ≥ 0, then w ∝ y/σ (eq. 2).
- **Properties (verified):** every held asset has the same correlation with the MDP, 1/DR(M) (eqs. 6–7); ρ(P, M) = DR(P)/DR(M) for any P (eq. 8); long-only: excluded assets have higher correlation; DR ≥ 1, equal to 1 only for a single asset; equals GMV when volatilities are equal; equals 1/σ (and ERC) under constant correlation.
- **Inputs:** Σ. Not used: μ.
- **Parameters:** none beyond constraints.
- **Constraints:** native (quadratic programme after the transformation).
- **Allocation domains:** asset class, fund/ETF, security.
- **Output and failures:** weights; `INFEASIBLE_CONSTRAINTS`; non-unique when C is singular (C&C p. 44: any solution has the same DR).
- **ANG vs source:** consistent. ANG's illustration ranks the MDP first in the vote (S4.1).
- **Verification:** Examples 1 (66.7/33.3) and 2 (25.7/25.7/48.6); eqs. (4), (6)–(8), (11)–(12); long-only KKT; limits. PASS.
- **Agent-readable summary:** *Objective:* the highest ratio of average stand-alone risk to portfolio risk. *Implicit belief:* expected returns proportional to volatility. *Sensitivities:* correlations and volatilities. *Failure modes:* concentration in low-correlation assets. *Valid comparisons:* GMV (equal vols), ERC and 1/σ (constant correlation). *Invalid:* confusing DR with the Sharpe ratio unless μ ∝ σ.

### PC-C5 Minimum correlation

- **Identity:** PC-C5 · Minimum Correlation Algorithm · family C · `M.PC` · roster v0.
- **Sources:** governing Varadi et al. 2012 (algorithm steps pp. 13–14; worked examples pp. 15–16; comparison §; issues MCA-1 … MCA-4); Kapler's code (cross-check).
- **Definition (EQ-RS-4):**
  - *MinCorr:* standardise the off-diagonal correlations by their mean and sample SD; A = 1 − Φ(ρ_ij); average each row of A; rank the averages descending (rank power 1) into rank weights; w = rank weights × A, normalised; divide by σ_i; normalise.
  - *MinCorr2:* the same, but standardise the row averages of the correlation matrix (diagonal set to 0) and multiply the rank weights by 1 − C.
- **Inputs:** correlations and volatilities from Σ. Not used: μ.
- **Parameters:** variant (S411-D3); rank power = 1 (fixed V0; the code's default); SD convention: sample SD of off-diagonal elements (MCA-2).
- **Constraints:** long-only and fully invested by construction; bounds not native (S411-D4).
- **Allocation domains:** asset class, fund/ETF (the authors' ETF tests); security possible.
- **Output and failures:** weights; `DEGENERATE_CORRELATION` when the dispersion used for standardising is zero (MCA-4): N = 2, a constant correlation matrix, and for MinCorr2 any matrix with equal average correlations (e.g. two identical blocks; verified).
- **ANG vs source:** ANG-38 (variant and tuning unspecified) → S411-D3.
- **Invariants:** sums to 1, positive; permutation-equivariant; invariant to a common volatility scale (verified).
- **Verification:** paper example (mean 0.817, SD 0.104; MinCorr [0.21, 0.31, 0.48], MinCorr2 [0.50, 0.30, 0.20], labels swapped in the paper, MCA-1); invariances; degeneracy cases. PASS.
- **Agent-readable summary:** *Objective:* tilt toward assets with low average correlation, scaled by inverse volatility. *Intuition:* a fast proportional heuristic for MDP-like diversification. *Sensitivities:* the correlation dispersion (standardisation). *Failure modes:* degenerate correlation structures (MCA-4); ranks make weights jump when averages cross. *Valid comparisons:* MDP, 1/σ. *Invalid:* reading weights as optimal for any objective.

**C5 × O2 (S4.9 pending cell):** MinCorr on a momentum-selected set is defined when the set has at least three assets and non-degenerate correlations, and depends on the score only through the selection (identical under three monotone transforms; verified). Under S49-D1 (tested, no source for the pairing) it joins the **research lane**.

---

## 4. Owner decisions (stage 6)

*[2026-10-18]* **Owner decision: S411-D1 … D5 accepted as recommended.** GMV long-only with Policy Statement bounds (unconstrained only where shorting is permitted); HRP V1 (tree split) in production with V0 as the reproduction oracle; MinCorr in production with MinCorr2 as a sensitivity variant; Policy Statement bounds for ERC, HRP and MinCorr by declared post-processing (S4.20), constrained variants as research-lane leads; typed failure records, no silent fallback.

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| **S411-D1** | GMV constraint set | (a) long-only with Policy Statement bounds, native; the unconstrained (long/short, budget-only) form only where the account permits shorting · (b) long-only without bounds · (c) unconstrained everywhere | **(a).** CdST's base case is long-only with an upper bound; their 3% is a 1,000-stock example, so the bound comes from the Policy Statement |
| **S411-D2** | HRP variant (ANG-42; I-7) | (a) V1 tree split in production; V0 kept as the reproduction oracle (Exhibit 7) · (b) V0 with a declared canonical ordering · (c) both as candidates | **(a).** V1 is the paper's own suggestion (p. 11) and satisfies I-7 without an arbitrary ordering convention; V0's canonical ordering would be a hidden parameter that moves weights. Linkage stays single (V0), others sensitivity-only |
| **S411-D3** | Minimum-correlation variant (ANG-38) | (a) MinCorr (the paper's title algorithm) in production; MinCorr2 registered as a sensitivity variant; rank power 1 · (b) MinCorr2 in production · (c) both | **(a).** MinCorr is defined on a strictly larger set of inputs (MCA-4); the authors' preference for MinCorr2 rests on their own in-sample comparison, which is evaluation evidence (S7), not admission evidence (ADR-0025) |
| **S411-D4** | Constraints for methods without native constraint handling (C2 ERC, C3 HRP, C5 MinCorr) | (a) as for the heuristics (S4.5): the method produces its weights; Policy Statement bounds are applied by a declared post-processing step at S4.20; the candidate card reports the distance moved and which defining property is lost (e.g. equal risk contributions) · (b) native constrained variants (e.g. constrained risk budgeting; lead from memory: Richard & Roncalli 2019) in the research lane · (c) mark the method infeasible when a bound binds | **(a)**, with (b) registered as a research-lane lead |
| **S411-D5** | Failure behaviour (I-2) | (a) a typed failure record with a reason code (`DEGENERATE_CORRELATION`, `NOT_POSITIVE_DEFINITE`, `INFEASIBLE_CONSTRAINTS`, `CONSTRAINT_CONFLICT`, `INVALID_CORRELATION`); no silent fallback · (b) a declared fallback (e.g. MinCorr → 1/σ), labelled as the fallback | **(a).** The CIO then sees one candidate fewer, not a substitute under the method's name |

---

## 5. Verification (stage 7)

| Script | Proves | Result |
|---|---|---|
| `s411_risk_structured.py` | C1: closed form; argmin σ = argmin σ²; CdST 2011 single-index formulas (1), (2), (A-5)–(A-7) = numerical QP; 3% cap. C2: MRT §4.1 tables, eqs. (3)–(8), App. A.1, A.3, §3.5; uniqueness (Spinu = SLSQP). C3: V1 invariance; V0 order dependence (32/60) and canonical determinism; limits; clipping. C4: Examples 1–2; eqs. (4), (6)–(8), (11)–(12); long-only KKT; limits. C5: worked example; invariances; MCA-4 cases; C5 × O2 | PASS |
| `s44_risk_parity_spinu.py`, `s44_hrp_lopez_de_prado.py` | Spinu solver; HRP Exhibit 7 exact | PASS (S4.4) |

---

## 6. Handed forward

| To | Item |
|---|---|
| S4.13 | Risk inputs: all five consume Σ only; HRP and MinCorr use correlations and variances separately |
| S4.14 | Research lane: C5 × O2; constrained risk budgeting (lead) |
| S4.16 | Candidate card: implicit expected-return belief per method (§2); distance moved by post-processing; risk-contribution report |
| S4.20 | Constraint post-processing rule (S411-D4); failure codes (S411-D5); HRP variant and canonical ordering for the oracle |
| S10 | CdST's covariance choices (PC, shrinkage, uncentred, daily vs monthly) as estimator candidates, selected per problem |
| S4_PLAN | Annotation: the S4.11 example equivalence should read "MD = GMV when volatilities are equal" |

---

## 7. Ladder status after S4.11

| Method | Status |
|---|---|
| PC-C1 … PC-C5 | SOURCE REVIEWED · MATHEMATICS EXTRACTED · COMPUTATION VERIFIED (source level); specification decided (S411-D1 … D5) |
