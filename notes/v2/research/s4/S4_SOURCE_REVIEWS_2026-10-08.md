# S4 record — reviews of six owner-supplied sources (2026-10-08)

**Document status:** DRAFT (S4.4 follow-up; feeds S4.7, S4.11, S4.12, S4.13, S4.16, S4.19–S4.24) · **Basis:** owner request 2026-10-08 ("review them thoroughly to gather all necessary and essential information"); `S4_PC_SOURCE_MAP.md` §6 (the six SSRN items); ADR-0024 §8 (verification area); ADR-0025 (admission requires verified reproduction).

**Status effect** (S4_PLAN §C.1 ladder): PC-C3, PC-D2 and PC-D3 move to **SOURCE REVIEWED**, as do PC-B2 and PC-C2 for their supporting sources. The mathematics is extracted into the Equation Register at each method's own step. Nothing here selects or ranks a method.

**Verification:** every reproduction below is our own code in `verification/s44_*.py`. Each script asserts its tolerances and prints `PASS`; all six pass. No third-party code was executed.

## 0. Identity

| Source | Version in hand | md5 · pages | Governing version | Maps to |
|---|---|---|---|---|
| He & Litterman, *The Intuition Behind Black-Litterman Model Portfolios* | GSAM working paper (1999), PDF of 2002 | `a03589438332` · 27 | Same (working paper only) | PC-B2 |
| Idzorek, *A Step-by-Step Guide to the Black-Litterman Model: Incorporating User-Specified Confidence Levels* | Draft of 26 Apr 2005 (SSRN 3479867) | `cf1ee81ea46d` · 34 | Satchell (ed.) 2007 chapter, pp. 17–38 | PC-B2 |
| Spinu, *An Algorithm for Computing Risk Parity Weights* | SSRN 2297383 working paper | `7152aad7f6f6` · 6 | Same | PC-C2 (algorithm) |
| López de Prado, *Building Diversified Portfolios that Outperform Out-of-Sample* | Version of 23 May 2016 (SSRN 2708678) | `575345cad8d5` · 31 | *JPM* 42(4):59–69 | PC-C3 |
| Chekhlov, Uryasev & Zabarankin, *Drawdown Measure in Portfolio Optimization* | UF research report 2003-15, 25 Jun 2003 | `597c81fcff3f` · 41 | *IJTAF* 8(1):13–58 (2005) | PC-D2 |
| Boudt, Carl & Peterson, *Asset Allocation with Conditional Value-at-Risk Budgets* | Version of 24 May 2012 (SSRN 1885293) | `a6b28ba66935` · 36 | *J. Risk* 15(3):39–68 (2013) | PC-D3 |

Where a working version is read, the published version governs (D-3). Page numbers below are the documents' printed pages.

## 1. He & Litterman — Black–Litterman portfolios (PC-B2)

**What it specifies:**
- Equilibrium Π = δΣw_eq (eq. 2, p. 3).
- Prior μ ~ N(Π, τΣ); views Pμ = Q + ε, ε ~ N(0, Ω) (eqs. 3–7).
- Posterior mean μ̄ = [(τΣ)⁻¹ + P′Ω⁻¹P]⁻¹[(τΣ)⁻¹Π + P′Ω⁻¹Q] (eq. 8) and posterior covariance M̄⁻¹ (eq. 9, p. 4).
- Optimal unconstrained weights w* = (δΣ̄)⁻¹μ̄ with **Σ̄ = Σ + M̄⁻¹** (eqs. 10–13, p. 6).
- Main result: w* = (w_eq + P′Λ)/(1+τ), with Λ given in closed form (eqs. 17–18, p. 7). The portfolio is the scaled market portfolio plus view portfolios.
- Properties 3.1–3.2 (pp. 8–9): a view's weight has the sign of q − p′μ̃; it rises with q, and its magnitude rises with confidence.
- With constraints, use μ̄ and Σ̄ in an optimiser (p. 13).

**Verified:** Π (Table 2) exactly; Tables 4–8 to within 0.1 pp in returns and 0.3 pp in weights (the published inputs are rounded); Λ within 0.02; eq. 17 ≡ eq. 13 exactly; Property 3.1 (third view gets λ₃ = 0, Table 8).

**Findings:**
- **Ω convention recovered.** The paper never states how Ω was set. The published ω/τ values (0.021, 0.017, 0.059) equal the view-portfolio variances p′Σp, so ω_k = τ·p_kΣp_k′. Idzorek states the same convention (p. 15).
- **HL-1** (label slip): the text's "λ = 0.302" (p. 11) is λ/(1+τ); Tables 5–8 report λ itself.

## 2. Idzorek — user-specified confidence (PC-B2)

**What it specifies:**
- Reverse optimisation Π = λΣw_mkt with an implied λ (eq. 1, p. 3; note 5).
- The BL posterior (eq. 3), with the He–Litterman Ω, under which τ becomes irrelevant (pp. 14–15).
- Market-cap-weighted relative views (eq. 7, p. 13), preferred over equal weighting.
- **Weights from Σ, not Σ̄:** w = (λΣ)⁻¹E[R] (eq. 2, p. 5). With no views this returns w_mkt exactly.
- The new method (sec. 3.2, pp. 23–26) maps a 0–100% confidence C_k per view to ω_k so that the tilt ≈ C_k × the 100%-confidence tilt. It finds ω_k by a numerical least-squares search (step 6).

**Verified:** λ = 3.065 (paper ≈ 3.07); Tables 4, 6, 7 within 0.02 pp; implied confidences 43.06 / 33.02 / 32.94%.

**Finding IDZ-1 (closed form, `VERIFIED-DERIVATION`):** for one view, w − w_mkt = (τ/λ)·p′(Q − pΠ)/(τ·pΣp′ + ω). The ratio to the 100%-confidence tilt is therefore τ·pΣp′/(τ·pΣp′ + ω) for every asset, and setting it to C gives

  **ω_k = τ·p_kΣp_k′·(1 − C_k)/C_k**.

This matches Idzorek's numerical search to 1.6 × 10⁻⁸. It makes the confidence method exact and deterministic: no optimiser and no tolerance in the method contract.

**Finding BL-1 (convention conflict between the two sources):** He & Litterman compute weights with Σ̄ = Σ + M̄⁻¹, which scales the market portfolio by 1/(1+τ). Idzorek uses Σ. ANG names neither. The PC-B2 contract must declare one (S4.7).

## 3. Spinu — computing risk-parity / risk-budget weights (PC-C2)

**What it specifies:**
- Risk budgeting x_i(Cx)_i = b_i·x′Cx is equivalent to Cx = b/x (eq. 3), which has a **unique positive solution** (Thm 1.1); there are 2ᴺ sign-orthant solutions without long-only (Prop. 1.3).
- The solution minimises F(x) = ½x′Cx − Σb_i log x_i (eq. 4), which is convex and self-concordant (Prop. 3.2).
- Algorithm (Thm 3.4):
  - reduce to the correlation matrix and rescale so that min b = 1;
  - x₀ = √(Σb)/√(1′C1)·1;
  - damped Newton steps x ← x − Δx/(1+δ), with δ = ‖Δx/x‖∞, while λ > 0.95·(3−√5)/2;
  - then pure Newton steps to the tolerance.
- He calls (Cx)_i·x_i/x′Cx the "marginal risk contribution"; it is the *percentage* risk contribution in most other texts (naming only).

**Verified:**
- Budgets met to about 10⁻⁷ relative error.
- At N = 50 with random budgets, at most 12 iterations (paper: < 16).
- At N = 1400 risk parity, 5 / 7 / 8 Newton updates at correlation condition numbers of about 4 / 33 / 5,700. The paper's "< 6" holds for well-conditioned matrices; it does not state its Wishart parameters (SPN-1).
- The Maillard–Roncalli–Teïletche ordering σ(long-only MV) ≤ σ(ERC) ≤ σ(1/N) held in 500 of 500 random cases.

**Implications:** deterministic and unique, so PC-C2 can use this solver with a declared tolerance. General budgets b cover the §D.1 "general risk budgeting" candidate, if it is ever admitted.

## 4. López de Prado — Hierarchical Risk Parity (PC-C3)

**What it specifies:**
- Stage 1 (pp. 5–6): d = √(½(1−ρ)); a "distance of distances" d̃ (Euclidean distance between columns of D); single linkage.
- Stage 2 (p. 7): quasi-diagonalisation, ordering the leaves.
- Stage 3 (p. 8): recursive bisection of the ordered list. In each half the cluster variance uses inverse-variance weights; the split factor is α = 1 − V₁/(V₁+V₂).
- The code (Appendix A.3–A.4) is Python 2.

**Verified:** Exhibit 7 reproduced **exactly**: all 30 weights (CLA, HRP, IVP) to two decimals, condition number 150.9324, σ_HRP 0.4640, σ_CLA 0.4486, and top-5 concentrations 92.66% / 62.57%. Python 2's `random.randint` was emulated exactly.

**Findings:**
- **HRP-1 (order dependence).** The published algorithm is **not invariant to the order of the assets**. Bisection halves the ordered leaf list, and a dendrogram's left/right orientation is arbitrary. Reordering inputs changed weights in 127 of 200 random 12-asset cases (mean change 4.6% of the portfolio, maximum 52%). The tree-split variant the paper itself suggests (p. 11) is order-invariant (differences around 10⁻¹⁶). It differs materially from the published one (mean 17%, maximum 48%).
  - Consequence: as for Sørensen, **V0 = the published algorithm** (the reproduction oracle; it needs a declared canonical ordering to be deterministic) and **V1 = tree-split** (candidate). Decision at S4.11.
  - **Correction:** `S4_GITHUB_IMPL_REVIEW.md` §7 said a correct HRP moves 0.00 under reordering. That holds only in particular cases. The third-party implementation's REJECT stands on its other defect (cluster variance computed with integer asset indices).
- **HRP-2 (numerical robustness).** A sample correlation can exceed 1 by rounding (e.g. 1.0000000000000002), which makes √(½(1−ρ)) NaN; clip to [−1, 1]. Python 2's `len(i)/2` must become `//`.
- The paper's out-of-sample results (variance 0.0671 for HRP vs 0.0928 for IVP vs 0.1157 for CLA) come from one simulation design. They are evidence about that design, not admission evidence (ADR-0025).

## 5. Chekhlov, Uryasev & Zabarankin — drawdown measures (PC-D2)

**What it specifies:**
- Drawdown on the **uncompounded** cumulative return w_k = Σr (eq. 6), in **absolute** terms: ξ_k = max_{j≤k} w_j − w_k (eq. 7, p. 6). The relative drawdown on compounded wealth is set aside (p. 7).
- Conditional Drawdown (CDD): CV@R_α of the drawdown series (eqs. 14, 16). α = 1 gives maximum drawdown and α = 0 average drawdown (Prop. 4, eq. 17).
- Linear-programming forms (eqs. 25, 30, 31).
- Portfolio problem: maximise expected uncompounded return subject to the (mixed) CDD ≤ γ, with static weights over scenario paths, as an LP (eqs. 47, 49; MaxDD and AvDD cases eqs. 55–56, p. 21).
- Example: 32 futures trend-following systems, 1995–1999, block bootstrap (blocks of 100 days), box constraints 0.2 ≤ x ≤ 0.8 (pp. 24–26). The data are not published, so the tables cannot be reproduced.

**Verified:**
- Definition (14) = LP (25) = knapsack (30) = path LP (31) for α ∈ {0, 0.5, 0.8, 0.95}.
- The α → 1 and α = 0 limits equal maximum and average drawdown.
- LP (55) encodes MaxDD ≤ γ exactly: with a binding limit the realised MaxDD equals γ.

**Findings:**
- **CDD-1 (definition vs ANG's Policy Statement).** CUZ's drawdown is absolute and uncompounded. ANG's drawdown limit ("−25% peak-to-trough", p. 15) is relative and compounded. They are different quantities, so the PC-D2 contract must declare which it uses and how γ maps to the Policy Statement.
- **CDD-2 (infeasibility).** Long-only and fully invested, a tight γ can be infeasible (it was at γ = 2% in our test). The contract needs an explicit infeasible outcome with a reason code.
- **Input class:** return paths or scenarios (historical or block bootstrap), not μ and Σ (ANG-17).

## 6. Boudt, Carl & Peterson — CVaR budgets (PC-D3)

**What it specifies:**
- CVaR in returns (eq. 2).
- Euler contributions C_i = w_i·∂CVaR/∂w_i (eq. 3), the percentage contributions (eq. 4), and the conditional-expectation form (eq. 5, Scaillet).
- CVaR concentration = max_i C_i (eq. 6).
- **Main proposal: minimum CVaR concentration (MCC), argmin max_i C_i** (eq. 10). It equals CVaR × the maximum percentage contribution (eq. 14), so it balances total CVaR against concentration.
- Equal CVaR contributions (ERC-CVaR) as an alternative (eq. 11).
- The minimum-CVaR portfolio's percentage contributions equal its weights (eq. 15; Appendix).
- MCC is non-convex, so they use a derivative-free global optimiser (differential evolution, p. 11).
- **Modified CVaR** (Appendix, pp. 32–33): Cornish–Fisher quantile g (eq. 21) and an Edgeworth-type expectation (eq. 22), using coskewness (N×N²) and cokurtosis (N×N³) at α = 5%. They state it is unreliable for smaller α (p. 7).
- Empirical design: DCC-GARCH(1,1) covariance, expanding-window mean, winsorised de-volatilised returns, equicorrelation co-moments, 8-year minimum sample, quarterly rebalancing, 1984–2010.

**Verified:**
- The printed Iq terms satisfy **Iq = −∫_{−∞}^{g} u^{q+1}φ(u)du** exactly; this is the identity behind eq. 22.
- With zero skew and excess kurtosis, eq. 22 reduces exactly to the Gaussian CVaR (eq. 7).
- Euler additivity holds.
- Proposition (15) holds.
- In our synthetic example MCC and ERC-CVaR coincide to 3–4 decimals, consistent with the paper's own examples (Table 1 p. 15; p. 16). They are not equal in general (eq. 14).

**Findings:**
- **BCP-1:** ANG's "tail-risk parity" could mean ERC-CVaR (eq. 11) or MCC (eq. 10), the paper's own proposal. To be declared.
- **BCP-2:** PC-D3 needs **coskewness and cokurtosis** as additional risk objects (ADR-0027 D3: one authoritative model per problem *and risk object*; registered in S4.13). DCC-GARCH is the paper's empirical design, not part of the method's definition. Under D3 the covariance part uses the problem's authoritative model.
- **BCP-3:** a stochastic global optimiser needs a recorded seed, or a deterministic multi-start, to meet the determinism requirement.
- **Typo:** in eq. 22, "s_p²" should read s_t².

## 7. Findings summary

| ID | Method | Finding | Handling | Stage |
|---|---|---|---|---|
| HL-1 | PC-B2 | "λ = 0.302" in the text is λ/(1+τ) | Recorded | — |
| BL-1 | PC-B2 | Weights from Σ (Idzorek) vs Σ + M̄⁻¹ (He & Litterman); Ω convention and τ unspecified in ANG | ANG-41; declare in the contract | S4.7 |
| IDZ-1 | PC-B2 | Closed form ω = (1−C)/C·τ·pΣp′ replaces the numerical search | Adopt into the specification (deterministic) | S4.7 |
| SPN-1 | PC-C2 | Iteration counts depend on conditioning | Declare tolerance and iteration cap | S4.11 |
| HRP-1 | PC-C3 | Published HRP is order-dependent; tree-split variant is invariant | ANG-42; V0 (published, canonical order) / V1 (tree-split) | S4.11 |
| HRP-2 | PC-C3 | Correlation clipping; Python 2 integer division | Implementation requirement | S4.20, S4.24 |
| CDD-1 | PC-D2 | Absolute uncompounded drawdown vs ANG's relative compounded limit | ANG-40 | S4.12 |
| CDD-2 | PC-D2 | Infeasible at tight γ | Reason code | S4.12, S4.20 |
| BCP-1 | PC-D3 | MCC vs ERC-CVaR | ANG-39 | S4.12 |
| BCP-2 | PC-D3 | Coskewness and cokurtosis risk objects | S4.13 registration | S4.13 |
| BCP-3 | PC-D3 | Stochastic optimiser | Seed or deterministic multi-start | S4.12, S4.20 |
