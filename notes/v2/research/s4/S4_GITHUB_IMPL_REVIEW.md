# Review of the third-party ANG implementation: technicalities and mathematics

**Document status:** DRAFT (S4 research input; amendment 15) · **Prepared:** 2026-10-07 · **Owner principles (2026-10-07):** paper v2 is the baseline; "use the code where it fits or is useful", after verification; never replicate the research, implement the *structure* with our own decisions (e.g. TSMOM/XSMOM/EPO). · **Labels:** `VERIFIED-SOURCE` (code read), `VERIFIED-DERIVATION` (proof or numerical check shown), `INFERENCE`, `UNVERIFIED`.

**Verdict vocabulary:**
- **ADOPT**: pattern or code may be ported, then verified in `research/s4/verification/` (S4.23).
- **ADOPT-WITH-FIX**: as ADOPT, after the stated fix.
- **REJECT**: do not port; our specification is given instead.
- **OUT OF ROSTER**: not an ANG method; not adopted. It may enter only through the research lane (ADR-0024 §1).

Adoption of any *method* still follows S4 governance. This document only says what the code can contribute.

---

## 0. Identity, version, executability

| Item | Finding | Label |
|---|---|---|
| Repository | github.com/chirindaopensource/agentic_architecture_for_institutional_asset_management; MIT licence (© 2026 Craig Chirinda); 15 commits, 14–18 Apr 2026 | `VERIFIED-SOURCE` |
| Author | Craig Chirinda ("AI aficionado"; 81 public repositories). README: "an **independent** … implementation". **Not** Ang, Azimbayev or Kim | `VERIFIED-SOURCE` |
| Paper version | "the April 2026 ArXiv preprint", i.e. arXiv 2604.02279 **v1**. Our baseline is **v2** (21 Sep 2026); arXiv lists only v1 and v2 (checked 2026-10-07) | `VERIFIED-SOURCE` |
| Files | `config.yaml` (2,892 lines; IPS, registries, prompts, parameters); `agent_tools.py` (20,468 lines; 104 top-level definitions, 80 unique names; six differing copies of `_cast_to_json_safe`); notebook "Draft 2" (Tasks 1–37; 22k code lines; newest code, 18 Apr); three AI-generated infographics | `VERIFIED-SOURCE` |
| Executability | Notebook never executed (0 outputs, 0 execution counts). The synthetic-data generator is in a **markdown** cell. The README example passes a mock OpenAI client that fails on the first model call. The agent-topology IPS tool is bound with keyword arguments its function does not accept: `inspect.signature` raises `ValueError` and a call raises `TypeError`. The robustness trial "sample estimator" always errors | `VERIFIED-DERIVATION` (tests run on extracted functions, 2026-10-07) |
| Not executed by us | Third-party code needing API keys. Static review of every file, plus our own re-implementations of the critical functions, gave stronger evidence than a demo | — |

Version lineage matters: the repo's prompt keys `…EXHIBIT3_VERBATIM` and `…EXHIBIT4_VERBATIM` are the v1 exhibit numbers (now App. A.1/A.2 in v2). The repo explicitly marks invented content `INFERRED` or "UNSPECIFIED IN MANUSCRIPT". **ADOPT** that provenance discipline (§9).

---

## 1. Fidelity to the paper (both versions)

| Element | Paper (v1 and v2) | Repo | Verdict |
|---|---|---|---|
| PC roster | 19 methods (Exh. 5 in v1 / Exh. 3 in v2) + Researcher + AdvDiv | 20 "canonical": 12 match; HERC, NCO, fractional Kelly, CVaR parity, max-decorrelation, factor risk parity, target-vol Sharpe, regime-conditional are **invented**; market-cap, inverse variance, vol targeting, mean–downside, min-correlation, max-DD, TPA **missing** | Fidelity failure |
| Effective distinct portfolios | 21 competing proposals | Notebook `run_optimizer` implements 11 slugs; the other 10 return an **ERC proxy**; all μ-using methods receive the **same μ**, so `bl_posterior` = `regime_conditional` = `max_sharpe`. **≈ 8 distinct portfolios of 20** | Fidelity failure |
| Families | v1: ≥ 3 of 4; v2: ≥ 3 of 5 | 4 (risk, return, naive, adversarial) | v1-consistent |
| Vote/metric blend | Regime-dependent; late-cycle run 40% vote / 60% metric (v2 p. 17; lecture notes s31) | Late-cycle α_vote = **0.6** | **Contradicts the paper.** v1 Exh. 9 reproduces only with 0.4 (BL row: 0.4·0.8485 + 0.6·0.9943 = 0.936) |
| CIO input | All 21 candidates (v2 p. 13; Exh. 8 weights all 21; ANG-08) | Top 5 only | Differs |
| Learning loop | §6.2 meta agent | Configuration stub only; **no code** | Missing |
| Skills | Substantive skill files (App. A.2) | Boilerplate placeholders (identical template; scripts referenced do not exist) | Missing |

---

## 2. Data conventions

| Item | Repo | Verdict / our specification |
|---|---|---|
| Returns | Simple periodic r_t = TR_t/TR_{t−1} − 1 on total-return indices; monthly; last business day | ADOPT as a convention candidate (S6) |
| Annualisation | μ × 12, σ × √12 | ADOPT (declared per computation; D2-01 units) |
| Missing data | `ffill(limit=5)` on the **returns** matrix | **REJECT.** Forward-filling a return fabricates observations. Missing stays missing (invariant I-6) |
| Unequal histories | Pairwise covariance over overlapping samples, then PSD clip | **REJECT** as a default. Unequal-history estimation is an S10 research item. Pairwise estimates can be indefinite and inconsistent |
| Point-in-time | Truncation at as-of date | ADOPT (with as-of gate DR-1) |
| Macro vintages | "latest available with approximation disclaimer" | **REJECT for historical evaluation** (revised data = look-ahead). Vintage-aware data required (S6) |
| Base currency | USD | Our basis is investor-declared (INV.reporting_currency). Numéraire changes portfolios (`S4_INPUTS_2026-10-07.md` D6) |

---

## 3. IPS constraints: mathematics, enforcement, and what to implement

### 3.1 Paper v2 (p. 15)
- **Hard:** the asset universe and ex-ante TE ≤ 6% vs 60/40. The CRO enforces them and the CIO may not breach them.
- **Soft:** CPI + 3–4% real return, an 8–12% volatility band, −25% max drawdown. Breaches are flagged in the board memo.
- The paper's own final portfolio has 7.54% volatility, a soft deviation it reports (p. 19).

### 3.2 Constraint mathematics and the repo's handling

| Constraint | Mathematics | Convexity (`VERIFIED-DERIVATION`) | Repo | Defect | Our treatment |
|---|---|---|---|---|---|
| Budget | 1′w = 1 | Linear | Enforced | — | Hard predicate (R3) |
| Long-only / box | l ≤ wᵢ ≤ u | Linear | Enforced in solvers; notebook projection exact; `agent_tools.py` clip-and-renormalise **breaks the cap** (input [0.5, 0.5, 0, …] stays 0.5 > 0.25) | Old copy only | Hard predicate; exact projection only as flagged repair (§6) |
| Tracking error | √((w−w_b)′Σ(w−w_b)) ≤ TE_max | Convex (second-order cone) | **Not in any optimiser**; post-hoc check only | Hard constraint left to luck; the 60/40 benchmark is mapped to two assets (US Large Cap, Intermediate Treasuries), a material modelling choice | Hard predicate (R3); inside construction where the method's contract allows (S11); benchmark representation per S4.10/S7 |
| Volatility band | σ_L ≤ √(w′Σw) ≤ σ_U | Upper bound convex; **lower bound reverse-convex**: {w : √(w′Σw) ≥ c} is the complement of a convex set, so the feasible set is non-convex | Treated as **hard** compliance (all three flags must pass) | Contradicts v2 (soft). Under the repo, ANG's own 7.54% portfolio would be **excluded** | Soft target with a finding record (S2), never a silent hard optimiser constraint |
| Real return target | μ′w − π_e ≥ 3% (π_e = expected inflation) | Linear given μ and π_e (needs a common real/nominal basis) | **Never checked** | Missing | Soft target; basis declared (I-4) |
| Max drawdown | min_t(V_t / max_{s≤t} V_s − 1) ≥ −25% | Path-dependent. Ex-ante only via scenario formulations (CDaR LP, Chekhlov–Uryasev–Zabarankin) or simulation | **In-sample historical** MDD used as hard compliance | Ex-post used as ex-ante; hard vs soft wrong | Soft; ex-ante via declared scenario method (S10/S11); in-sample labelled |
| Universe | Fixed 18-element vector | — | Implicit | — | Policy Statement universe (S5) |
| Compliance keys | — | — | CRO/CIO paths pass the right values. The agent-topology tool receives `IMPLEMENTATION_CONSTRAINTS` (no vol/TE keys) and falls back to hard-coded defaults; the binding also crashes | Silent defaults | Constraint values come only from the Effective Policy Statement (R4) |

### 3.3 What to implement (candidates for S4.20 / S11 / S2 interface)
Every Policy Statement constraint carries the following, routed to RQ-15 and S4.20:
1. a **mathematical type** (linear / SOC / reverse-convex / path-dependent);
2. its **evaluation basis** (ex-ante with stated estimates / ex-post with stated sample);
3. its **hardness** (hard / soft / trigger, per S1/S2);
4. its **enforcement point** (inside construction / R3 predicate after each step / report flag);
5. its **breach consequence** (block / finding record / escalation).

**Rule [AD]:** reverse-convex and path-dependent constraints are never silently turned into hard optimiser constraints.

**Feasibility pre-check:** joint feasibility of hard constraints, e.g. box with TE (S2 FeasibilityFinding).

---

## 4. Macro regime classification (deterministic core)

**Repo (cell 27; `VERIFIED-SOURCE`):**
- Expanding z-scores per indicator: z_t = (x_t − mean_{≤t}) / sd_{≤t}, point-in-time.
- Dimension scores s_d = Σ w_{d,k} z_{k,T}, with placeholder weights (growth: GDP 0.6, payrolls 0.4; inflation: CPI y/y 0.7, m/m 0.3; policy 0.5/0.5; financial conditions 0.6/0.4).
- Regimes by threshold boxes; confidence = softmax of regime "activations".

**Verdict: ADOPT-WITH-FIX** as the candidate **R2 deterministic fallback** for the Macro role (S9a, RQ-11):
- weights, thresholds and the softmax temperature are research parameters, not defaults;
- expanding windows from inception mix structural breaks; the window choice is a parameter;
- vintage-aware inputs are required;
- the four-regime scheme itself is illustrative (ADR-0023 §8).

---

## 5. Capital market assumptions

### 5.1 Equity candidates (cell 28; `VERIFIED-SOURCE`)

| # | Repo formula | Confidence (placeholder) | Verdict |
|---|---|---|---|
| 1 | r_f,now + 12·mean(r − r_f) over history | logistic(IR) | ADOPT-WITH-FIX (geometric/arithmetic and horizon declared) |
| 2 | r_f,now + 12·mean(r − r_f \| months in current regime), ≥ 12 obs, else full-history with penalty | regime confidence × sample factor | ADOPT-WITH-FIX (regime history must be point-in-time; low-n disclosed) |
| 3 | π = δ Σ w_mkt (δ = 2.5) | w_i / max w | **FIX:** π is an **excess** return; add r_f before comparison (I-4). w_mkt for non-equity classes is a data question (S6) |
| 4 | dividend yield + buyback yield + g + Δvaluation | fixed by proxy flag | ADOPT-WITH-FIX (Grinold–Kroner primary, checklist M-2; g proxy disclosed) |
| 5 | earnings yield (CAPE-based) | 1 − CAPE percentile | **FIX:** earnings yield ≈ a *real* return; convert to the common basis |
| 6 | survey value | exp(−λ · months stale) | ADOPT-WITH-FIX (survey source is Class B, M-4) |
| 7 | Σ cᵢ eᵢ / Σ cᵢ; confidence Σ cᵢ² / Σ cᵢ | — | ADOPT-WITH-FIX (R2 fallback = auto-blend) |

**Key defect: mixed units.** Excess (3), real (5) and nominal total (1, 2, 4, 6) candidates are bounded together by [min, max] (`VERIFIED-SOURCE`). This widens or shifts the judge's envelope arbitrarily. Invariant **I-4** applies.

### 5.2 CMA judge (cells 29; `agent_tools.py`)
- Deterministic tools: dispersion classes (spread < 3 / 3–6 / > 6 pp); regime tilt map; P/E thresholds 30×/12×; signal alignment (RSI, 12-month momentum, breadth thresholds); range constraint.
- The LLM chooses `final_estimate` and blend weights.
- **Two-layer gate:** an in-loop tool clips and instructs; a post-hoc check on the persisted file halts.

**Verdict: ADOPT** the pattern for S9b:
- a mandatory tool sequence;
- deterministic checks as tools;
- a two-layer range gate (R1 enforcement);
- the deterministic fallback.

The thresholds are paper-illustrative (v2 p. 39), not defaults.

### 5.3 Fixed income (cell 30)
- Estimate = y(T) + [y(T) − y(T−1)]·T + OAS − PD·LGD, with linear interpolation on 3m/2y/10y/30y.
- **FIX:** first-order roll-down return ≈ D_mod · [y(T) − y(T−Δ)], with **modified duration**, not maturity T; using T overstates roll-down for coupon bonds.
- The spread carry and default-loss treatment needs a source (practitioner decomposition; S9b).

**Verdict: ADOPT-WITH-FIX** as a candidate FI method.

### 5.4 Cash
Expected return = current cash yield proxy. ADOPT (trivial; horizon mismatch disclosed).

---

## 6. Covariance and weight repair

| Item | Repo | Verdict |
|---|---|---|
| "Ledoit–Wolf" | Target F = (tr S/N) I; intensity δ = ‖F‖²_F / ‖S‖²_F clipped to [0.1, 0.9] (cell 31) | **REJECT as LW.** The intensity ignores sample size and estimation noise, which is the essence of Ledoit–Wolf's optimal shrinkage. Implement LW (2004) from the primary (S10; checklist) |
| PSD repair | Eigenvalue clipping at 1e-8, symmetrise | ADOPT as a flagged repair (alternative: nearest-correlation methods; S10) |
| Window | 120 months; robustness 60/180 | Parameter (S10) |
| Exact projection onto {1′w = 1, l ≤ w ≤ u} | xᵢ = clip(wᵢ − λ, l, u), λ by bisection (notebook) | **ADOPT** (`VERIFIED-DERIVATION`: KKT solution of min ‖x − w‖²; numerical match to a QP solver ≤ 5.3 × 10⁻⁸ over 200 cases). Use only as a **flagged repair**: if a solver's output needs projection, the method failed its own constraints and the record must say so |
| Clip-and-renormalise (`agent_tools.py`) | max(·,0), clip, divide by sum | **REJECT** (breaks the cap; shown above) |

---

## 7. Portfolio-construction methods (notebook = newest; `agent_tools.py` where it differs)

| Method (our ID) | Repo implementation | Correct form / source | Verdict |
|---|---|---|---|
| Equal weight (A1) | 1/N | DGU 2009 | ADOPT |
| Inverse volatility (A3) | wᵢ ∝ 1/σᵢ | Kirby–Ostdiek 2012 (exponent; ANG-13) | ADOPT |
| GMV (C1) | SLSQP min w′Σw, box, budget | Convex QP | ADOPT-WITH-FIX (use a QP solver; convex) |
| Max Sharpe (B1) | SLSQP on −(μ′w − r_f)/σ_p from 1/N | Tangency; long-only box via the standard homogenisation y = κw: min y′Σy s.t. (μ − r_f)′y = 1, 1′y = κ, lκ ≤ y ≤ uκ, κ ≥ 0 (convex QP; cite at S4.6) | ADOPT-WITH-FIX (convex reformulation; no local optima) |
| Max diversification (C4) | SLSQP on −w′σ/σ_p | Same homogenisation with σ in place of μ − r_f | ADOPT-WITH-FIX |
| ERC / risk parity (C2) | min Σᵢ (wᵢ(Σw)ᵢ/w′Σw − 1/N)², SLSQP | Maillard–Roncalli–Teïletche 2010: long-only ERC exists and is unique; solved robustly via the log-barrier / Spinu (2013) formulation. With a 25% cap, exact ERC may be infeasible: report the deviation | ADOPT-WITH-FIX |
| HRP (C3) | Single linkage, bisection; cluster variance cᵀ Σ_cc c with **c = integer asset indices** | López de Prado 2016: cluster variance with inverse-variance weights inside the cluster | **REJECT** (`VERIFIED-DERIVATION`: not permutation-invariant; reordering assets moved weights by up to 0.22 vs 0.00 for a correct HRP) |
| Min CVaR (D1) | Rockafellar–Uryasev LP (HiGHS) on 5,000 **KDE-resampled** scenarios (notebook); SLSQP on a non-smooth objective (`agent_tools.py`) | R&U 2000 LP on declared scenarios | ADOPT the notebook LP with empirical scenarios; KDE only as sensitivity; **REJECT** the SLSQP version; resolve ANG-02 (min-CVaR vs mean–CVaR) |
| Black–Litterman (B2) | μ = π = δΣw_b (benchmark weights), **no views**, τ unused, then max-Sharpe with π − r_f | BL 1992; He–Litterman 1999: posterior with views (P, Q, Ω) from AC agents | **REJECT**; specify at S4.7 |
| Robust MV (B3) | Max-Sharpe on μ shrunk 50% toward its mean | Goldfarb–Iyengar 2003 uncertainty-set SOCP | **REJECT** |
| Resampled frontier (B4) | Perturb μ by 10%·\|μ\| noise, tiny Σ jitter | Michaud: simulate samples of length T, re-estimate, average rank-associated frontier portfolios (D-2 IP check) | **REJECT** |
| Tail-risk parity (D3) | ERC on a covariance of the EW portfolio's tail months | Boudt–Carl–Peterson 2013: equal ES contributions | **REJECT** |
| Adversarial diversifier (E2) | Sequential convex programming: maximise ∇f(w_k)′w over the feasible set with f(w) = (w − w̄)′Σ(w − w̄) and Sharpe floor; start at a tangency-like point; 20 iterations | ANG v2 p. 10 | **ADOPT-WITH-FIX.** `VERIFIED-DERIVATION`: f is convex, so f(w_{k+1}) ≥ f(w_k) + ∇f(w_k)′(w_{k+1} − w_k) ≥ f(w_k); monotone ascent to a KKT point. The floor set {μ′w − r_f − s·√(w′Σw) ≥ 0} (budget 1′w = 1) is convex, so each subproblem is a convex SOCP. **Fixes:** one consistent Sharpe definition (repo: floor from *backtest* Sharpe, constraint *ex-ante*; I-5); seeded multi-start; deterministic tie-break; centroid over **distinct** proposals (I-3) |
| Researcher (E1) | Literature tool + spec validator; outputs a method spec, no weights | ANG p. 10; research lane | ADOPT the "spec, no weights" behaviour (matches ADR-0024 §1) |
| HERC, NCO, Kelly, CVaR parity, max-decorrelation, factor RP, target-vol Sharpe, regime-conditional | Crude or duplicate (e.g. "HERC" = 50/50 halves with inverse vol; "factor RP" = ERC; "regime-conditional" = max Sharpe) | Not ANG methods | **OUT OF ROSTER** |
| Failure behaviour | Silent fallback to equal weight / ERC / GMV under the original name | — | **REJECT** (I-2) |

**ERC, explained (owner question 2026-10-07):**
- ERC means **equal risk contribution**, also called risk parity: choose weights so that each asset contributes the same share of portfolio variance, i.e. wᵢ(Σw)ᵢ = w′Σw / N for every i.
- It is **PC-C2 in our roster** (ANG Exh. 3; source Maillard, Roncalli & Teïletche 2010, located but not yet obtained).
- Status: NOT STARTED, because the method library begins at S4.5. It is scheduled in S4.11.
- We do not ignore it. We implement it ourselves from the primary source, with an existence/uniqueness check and a cap-feasibility report.
- In the repo, ERC also served as the silent fallback for ten other methods. That is a defect, not a design.

---

## 8. Deliberation and CIO

| Component | Repo mathematics | Verdict |
|---|---|---|
| Review assignment | Two linear-sum-assignment problems with seeded random costs: intra-family (self and cross-family cost 10⁶), then inter-family (excluding the intra peer). Each solution is a permutation, so **every candidate receives exactly two reviews** (`VERIFIED-DERIVATION`) | **ADOPT-WITH-FIX.** With a single-member family (the AdvDiv), the exact repo algorithm assigns the AdvDiv to **review itself** (seeds 12345, 1–5) and places some "inter" reviews within a family. Fix: one constrained assignment (each agent reviews 2 and is reviewed by 2; no self; ≥ 1 cross-family each), solved as a flow/integer programme, with a feasibility report |
| Barriers | Count gate (42 reviews; 21 votes), schema gate, atomic simultaneous release | ADOPT (S12; mitigation M3, RQ-56) |
| Vote | Forced `submit_vote` tool; top-5 scored 5…1, bottom flag −2; self-vote guard; Borda = Σ points | ADOPT mechanics (points are illustrative, ADR-0023 §8) |
| Composite | Min–max normalise votes and metrics; composite = α·vote + (1−α)·metric with invented α by regime | ADOPT the structure; α values not adopted (late-cycle contradicts the paper). Min–max over few candidates is unstable; rank normalisation is an alternative (S12) |
| Diversity rule | Greedy: swap the lowest-ranked duplicate-family member for the highest-ranked candidate of a missing family | ADOPT-WITH-FIX: families from Method Contracts; add distance-based duplicate detection (I-3) |
| Revision | LLM may pass an arbitrary `constraints_override` dict to the optimiser; prompt says "adjust method parameters and rerun" if non-compliant | **REJECT** (ADR-0024 §2–3; X-22; I-8) |
| CRO re-run after revision | Diagnostics recomputed on revised weights | ADOPT |
| CRO metrics | Ex-ante σ and TE; backtest Sharpe and MDD on the **estimation window**; Fama–French 3-factor regression | ADOPT σ/TE/MDD formulas; label in-sample (I-9). FF3 (US equity factors) is not a default for a multi-asset book (S10 factor model) |
| CIO scores | SR = backtest Sharpe; IPS = 0/1; diversification ratio; "regime fit" = ±(equity − bond weight) by regime; "estimation robustness" = −HHI; "CMA utilisation" = corr(w, μ); min–max over the top 5; weights 25/15/15/20/15/10 | Inventory for S4.18 only. Proxies are crude research objects; the weights are paper-illustrative (not adopted) |
| Ensembles | Simple average; inverse-TE; Sharpe-weighted (floored at 0); meta-optimisation (max Sharpe over PC portfolios as assets, per-asset cap via W′a); "regime-conditional" (**identical** to composite-score weighting); composite-score; trimmed mean (drop the max- and min-L1 outliers); each projected | ADOPT the formulas as S4.18 inventory candidates. Fix the duplicate. Linear ensembles keep M-1 attribution (ADR-0026) |
| Selection | Deterministic argmax of CIO score among compliant ensembles; the LLM narrates | Pattern consistent with B-13 (bounded choice among code-computed ensembles) and R2 |
| Input set | Top 5 only | Paper: all candidates (ANG-08); S12 decides |

---

## 9. Orchestration and engineering patterns (S8; interface only)

| Pattern | Verdict | Note |
|---|---|---|
| Declarative agent registry entry (description, skills, bound tools, input/output artifacts, schemas, loop limits, model/effort policy) | ADOPT | Runtime realisation of the mandate (F13) |
| Mandatory tool-call sequence + termination tools | ADOPT | Same sequence without the LLM = R2 path |
| Tools bound with fixed arguments (partial) | ADOPT-WITH-FIX | Agents cannot alter Σ, μ or constraints (R4). **But** outputs pass **by reference** (result ID/hash), never by value through an agent: the repo's `write_pc_weights_json(weights=…)` lets LLM-copied numbers become the official weights (I-1) |
| Fail-closed schema validation between phases | ADOPT | Typed contracts (S4.20) |
| Pre-flight artifact gate; terminal validation (sum, sign, N) | ADOPT | S12/S14 |
| Per-agent reasoning-effort/token budget | ADOPT | Run manifest (04) |
| VERBATIM / INFERRED / UNSPECIFIED tags on prompts and parameters | ADOPT | Maps to [SRC]/[AD] and parameter-authority classes |
| LLM-variability protocol: drift in final-weight L1, CMA estimates, top-5 overlap, rank Spearman, ensemble choice, compliance rate | ADOPT-WITH-FIX | **K repeats per configuration** to estimate the noise floor before attributing drift to a perturbation (RQ-55) |
| Data/model robustness (one-at-a-time: window, estimator) | ADOPT-WITH-FIX | Fix the estimator dispatch; S7 pre-registration |
| Provenance: SHA-256 of data frames and config; sealed archive | ADOPT | Subset of 04 (ours adds code commit, prompt/skill hashes, model IDs) |
| Backtest of static final weights over the estimation window | REJECT | In-sample (I-9); S7 walk-forward |
| Infographics claiming "21 unique allocations", a covariance "regime adjustment" | — | Not supported by the code |

---

## 10. Invariants for our engine (testable; derived from verified failures)

| ID | Invariant | Test (S4.23/S4.24/S8) |
|---|---|---|
| I-1 | Numbers pass between deterministic steps **by reference**, never re-typed by an agent | Tamper test: an agent-supplied value differing from the referenced result is rejected |
| I-2 | A failed method emits a typed failure/no-proposal record. A declared fallback is labelled as the fallback, never as the method | Force solver failure; check the record |
| I-3 | Duplicate proposals are detected by portfolio distance before review and voting; diversity is measured on distances, not only family labels | Two identical proposals → flagged |
| I-4 | CMA candidates share one declared basis (currency, nominal/real, total/excess, horizon, arithmetic/geometric) before any [min, max] bound | Mixed-basis inputs rejected |
| I-5 | One Sharpe definition per use, declared in the contract (ex-ante vs realised) | AdvDiv floor and constraint use the same definition |
| I-6 | Missing returns are never filled | Gap in input → explicit missing handling |
| I-7 | Methods pass invariance fixtures (e.g. HRP permutation invariance; estimator formulas vs reference) | Permutation test; LW reference values |
| I-8 | Revisions change only contract-authorised parameters within bounds | Override outside authority rejected |
| I-9 | In-sample diagnostics are labelled; runtime scoring metrics are defined by S7 | Label present in every CRO report |

---

## 11. What can be reused as code (MIT licence: keep the copyright notice in ported files)

Port-and-verify candidates. Each gets our reference implementation and fixtures in `research/s4/verification/` before any production use:
1. exact simplex-box projection (notebook `_apply_post_optimization_projection`);
2. Rockafellar–Uryasev CVaR LP (notebook `_cvar_lp_optimization`, without KDE by default);
3. review assignment via linear assignment (with the singleton-family fix);
4. AdvDiv SCP loop (with I-5 and multi-start);
5. Borda, normalisation and composite mechanics;
6. ensemble formulas (minus the duplicate);
7. drift metrics for variability tests;
8. provenance hashing;
9. the schema-gate and barrier patterns.

Not reusable: BL, robust MV, resampled frontier, tail-risk parity, HRP, the "LW" estimator, the invented methods, the IPS compliance logic, the in-sample backtest.

---

## 12. Where our own decisions plug in (structure, not replication)

**XSMOM / TSMOM.**
- Deterministic signal scripts in the AC role's signal step (`signals.json`, ANG step 4), used as bounded evidence for the CMA judge.
- As μ inputs only if S9d admits a mapping (RQ-33).
- TSMOM may also serve as timing evidence for the Trader by use (ADR-0026 §8.9), logged per consumer.

**Simple and Anchored EPO.**
- Two family-B PC agents with the standard anatomy: description, skill, verified script, dual contract.
- Anchor from S4.10.
- They enter review and voting like any method.

**Adding a method is a registry entry plus a contract plus a verified script**, through Method Library governance. This is ANG's "composable expertise" claim, realised under our gates.
