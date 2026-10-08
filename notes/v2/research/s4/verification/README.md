# S4 verification area

**Document status:** STABLE (established at S4.0, 2026-10-02) · **Basis:** ADR-0024 §8 (OD-5)

**Contents:** mathematical verification and reference implementations for S4 only:
- equation verification;
- source reproduction;
- limiting-case tests;
- synthetic examples;
- invariants;
- reference outputs;
- numerical comparison.

**Rules:**
- **Not production code.** The developer chooses the production implementation after receiving the Method Contracts (S4.20). Reference outputs here serve as test oracles.
- **Language:** Python (numpy/scipy). The packages available today do not determine the production architecture. A method that needs convex optimisation is not avoided because a solver is not installed here.
- **Synthetic data only.** No personal data, ever.
- **No performance-driven selection.** Results here verify that a method matches its mathematical specification. They never rank methods (performance evaluation belongs to S7).
- **Empty at S4.0.** Code is added from S4.5 onward.
- *[2026-10-08, S4.4]* **Source-reproduction scripts added ahead of S4.5** (owner request to review the six supplied papers in depth). Each script is self-asserting and prints `PASS`. Run with `python3 <script>` (numpy, scipy, pandas):

  | Script | Reproduces | Method |
  |---|---|---|
  | `s44_black_litterman_he_litterman.py` | He & Litterman: Π (Table 2), Tables 4–8, eq. (17) = eq. (13), Ω = τ·diag(PΣP′) | PC-B2 |
  | `s44_black_litterman_idzorek.py` | Idzorek: λ, Tables 4/6/7; closed-form ω = (1−C)/C·τ·pΣp′ equals the paper's numerical step 6 | PC-B2 |
  | `s44_risk_parity_spinu.py` | Spinu: Newton algorithm (Thm 3.4), iteration bound at N = 50; Maillard–Roncalli–Teïletche volatility ordering | PC-C2 |
  | `s44_hrp_lopez_de_prado.py` | López de Prado: Exhibit 7 exactly (seed 12345); order-dependence of published HRP; order-invariant tree-split variant | PC-C3 |
  | `s44_drawdown_cdd.py` | Chekhlov–Uryasev–Zabarankin: CV@R definition = LP (25) = knapsack (30) = path LP (31); MaxDD/AvDD limits; LP (55) exact and infeasible case | PC-D2 |
  | `s44_cvar_budgets_bcp.py` | Boudt–Carl–Peterson: Iq identity, Gaussian limit, Euler allocation, Prop. (15), MCC % contributions | PC-D3 |
- *[2026-10-08, S4.5]* **Heuristic-method scripts** (`S4_HEURISTICS.md`; equations in `S4_EQUATION_REGISTER.md`):

  | Script | Reproduces / proves | Method |
  |---|---|---|
  | `s45_equal_weight_dgu.py` | DGU: 1/N invariants; μ ∝ Σ1 optimality; Proposition 1, all 15 stated critical windows; Monte Carlo of the expected-utility terms | PC-A1 |
  | `s45_market_cap.py` | Cap-weight invariants; zero turnover between issuance events; reverse optimisation; Sharpe (1964) linear relation | PC-A2 |
  | `s45_volatility_timing_ko.py` | Kirby–Ostdiek VT(η): limits, invariants, eq. (12) by QP, eq. (13) example, A3 = ERC iff equal correlations, turnover eq. (6) vs DGU eq. (15), cash degeneracy | PC-A3, PC-A4 |
  | `s45_volatility_managed_mm.py` | Moreira–Muir: eq. (1) with ex-post c, fn. 6, no look-ahead (MM-1), appraisal identity, Table IV variants, 1/σ vs 1/σ², the V1 engine form | PC-A5 |
