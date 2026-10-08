# ADR-0027 — ANG adaptation decisions: governed learning, registry evolution, method-specific risk models with a common reference model, runtime diagnostics, declared units

- **Status:** PROPOSED
- **Date proposed:** 2026-10-08 · **Date decided:** —
- **Decided by:** — (owner; at G4 or earlier) · **Gate:** G4 · **Stage:** S4 (S4.2)
- **Supersedes:** none · **Extends:** ADR-0023 §8 ("a learning loop with human approval above materiality"), ADR-0024 §1, ADR-0025, ADR-0026 §4.4 and §8 · No body edits
- **Resolves:** C-5, C-6, C-11, C-12, C-13 (`research/s4/S4_ANG_ADAPTATION.md` §2); ANG-31, ANG-33, ANG-37 (in principle)
- **Spec commit / tag:** —
- **Revision history (pre-acceptance; PROPOSED text may change until decided):**
  - r1, 2026-10-08 (`37f81df`): D3 = one authoritative risk model per declared horizon per run, used by every PC method and the CRO.
  - r2, 2026-10-08 (owner review question: "should the risk estimation depend on the PC method, not one universal estimate applied to all?"): D3 split into **method-specific construction risk models** and **one common reference risk model per horizon for evaluation**. Evidence added: RMT cleaning by universe size (`S4_ANG_BASELINE.md` §13.3, Appendix C).

## Basis labels
**[SRC]** cited source (scope stated) · **[AD]** architecture decision · **[GR]** governance rule · **[DEF]** deferred to the named stage · **[DER]** derivation or simulation, with location.

## Context
- ANG v2 makes self-learning a core pillar: abstract; p. 2; pp. 27–29; lecture s12.
- ANG also says unsuccessful PC methods can be culled (fn. 4 p. 9; p. 10).
- ANG warns that correlated LLM errors can turn 21 methods into "a single hidden bet" (pp. 24–25). It never addresses how learning interacts with that risk (ANG-37).
- ANG has three unreconciled risk inputs (ANG-33). Its covariance agent produces **one** matrix that feeds all 21 PC agents (p. 6, step 4; p. 9 §3.3), while §6 suggests different covariance estimators for short- and long-horizon volatility (p. 29).
- ANG uses backtest Sharpe at runtime while stating that the pipeline "cannot be cleanly backtested" (ANG-19).
- ANG's CMA unit convention is implicit (USD, 3-year, nominal).

The owner requires that agents learn and evaluate portfolio-construction methods. Records: `S4_ANG_BASELINE.md` §13 and `S4_ANG_ADAPTATION.md`.

## Decision

### D1 — Learning is a core component, governed by rules L-1 … L-7 [AD/GR]
1. **[AD]** Learning covers:
   - forecasts (macro, CMA);
   - **PC methods** (deterministic evaluation records);
   - review and vote quality;
   - CIO ensemble choices;
   - CRO flags.

   Learning objects are captured from the first run (S4.3; DR-2).
2. **The rules:**

   | Rule | Content | Basis |
   |---|---|---|
   | L-1 | Learnable *parameters* (forecast-model parameters, CMA-method weights, eligibility thresholds) are estimated **in code** under pre-registered statistics. Prompts and skills change only through the gated path | [GR] |
   | L-2 | PC methods are evaluated **deterministically** under the S7 protocol, over minimum horizons fixed in advance. Evaluation informs CIO weighting (the ADR-0025 axis) | [GR] |
   | L-3 | A family-coverage floor applies (see D2) | [GR] |
   | L-4 | A change is promoted only if measured cross-agent error correlation and proposal dispersion do not deteriorate beyond a margin fixed in advance (RQ-56, M6) | [GR] |
   | L-5 | Promotion is **per role**, after replay and shadow testing, with rollback. No automatic deployment of a learned skill to all agents | [GR] |
   | L-6 | Judge ≠ author: a learning agent proposes; a deterministic test battery and a human decide above materiality. Mandates are never self-modified (ADR-0026 §4.4) | [GR] |
   | L-7 | Only outcomes after the producing model's training cutoff count as learning signals; a model upgrade resets the window | [GR] |

3. **[DER]** Why L-3 and L-4 exist:
   - N agents with pairwise error correlation ρ act as N_eff = N / (1 + (N−1)ρ) independent agents. For N = 21: 7.0 at ρ = 0.1; 3.0 at ρ = 0.3 (`S4_ANG_BASELINE.md` §13.1).
   - Outcome signals at strategic frequency have low power (D9, D10), so unguarded learning largely fits noise (D7).
4. **[DEF]** Materiality thresholds, horizons, margins and test batteries → S7 and S17 (RQ-22, RQ-55, RQ-56).

### D2 — Governed registry evolution [GR]
1. Methods are **added** only through the research lane (ADR-0024 §1).
2. **No automatic culling.** A method is `RETIRED` only by ADR (02 §D), on:
   - (a) failing its admission criteria (ADR-0025); or
   - (b) pre-registered evaluation evidence with multiple-testing control.
3. Weak recent performance alone changes the method's **weight** at the CIO stage, not its **existence**.
4. **Family-coverage floor:** the deliberable set keeps at least one admitted method in each family that the Policy Statement makes eligible. This generalises ANG's "≥ 3 of 5 families" shortlist rule (p. 12) to the registry.
   - **[SRC]** ANG p. 20: the ensemble benefits "precisely from learners that make forecasting errors in uncorrelated dimensions". Scope: motivates diversity preservation; not a proof.

### D3 — Risk estimation: method-specific construction models, one common reference model per horizon [AD]
Two different jobs need risk estimates, and they need different things:
- **constructing** a portfolio needs the estimator that works best *for that method, its constraint set and the universe dimension*;
- **evaluating and comparing** portfolios needs *one yardstick* that every candidate is measured on, fixed before the candidates exist.

1. **Construction risk models are method-specific.**
   - Every PC method (and EPO variant) declares a **risk-representation dependency** in its Method Contract (S4.13, S4.20): the object (Σ; volatilities + correlation; semicovariance; scenario set; factor model; none), the admissible estimator set, window and frequency, and horizon.
   - The **risk role** produces each declared construction model as a deterministic, versioned artefact referenced by ID. A PC agent never estimates its own risk model in a prompt (R1), and never switches estimator after seeing results.
   - Several construction models may therefore exist in one run for the same horizon. Each is labelled with the methods that consume it.
2. **Estimator eligibility is a function of the problem, not a global setting.** Each estimator is a Method Library entry (COV-x) with an eligibility contract over at least: dimension N, q_eff = N/T_eff, the consuming method's constraint set, and horizon (06 §4 already requires both a q range and a minimum N for RMT).
3. **One common reference risk model per declared horizon per run** is used for **evaluation, never as a hidden construction default**:
   - CRO ex-ante risk, VaR/ES and risk decomposition for every candidate;
   - IPS / Policy Statement limit and tracking-error checks (these **bind on the reference model**, so a method cannot pass a limit by choosing a more favourable estimator);
   - candidate cards, reviewer metric scores and CIO comparison;
   - the Portfolio Map's common estimates for any weight vector (S4_PLAN §J, PM-1);
   - learning records (ex-ante risk vs realised outcome, D1).

   The reference model is a **reference-estimator control** in the sense of ADR-0026 §4.1: its content is fixed in advance (S7 protocol, from the S10 estimator evidence), it is declared in the run configuration **before** candidates are produced, and it is designated by a party other than the evaluated roles. Neither a PC method nor the CIO chooses it; the risk role computes it.
4. **Dual reporting.** Each candidate card shows risk under (a) its own construction model and (b) the reference model. The gap is a CRO diagnostic ("risk-model disagreement"). A **sensitivity line** reports reference risk under at least one alternative admissible estimator.
   - **Strongest objection:** if the reference estimator coincides with some methods' construction estimator, those methods look better on the yardstick (home-field bias). Mitigations: dual reporting; the sensitivity line; and the reference estimator chosen for evaluation accuracy at the portfolio level (S10), not for any method.
5. **AC-level evidence.** AC-level volatility estimates and correlation rows (ANG-29) are **evidence**: consistency-checked against the reference model and reported. They are never direct PC inputs.
6. **Assembled matrices.** Any matrix assembled from separately estimated parts is symmetrised and projected to the nearest positive-semidefinite correlation matrix before use. The projection distance is reported as a diagnostic.
7. **Horizon** is a mandatory field of every risk artefact (construction and reference), together with the D5 units and a `role` field ∈ {construction, reference, evidence}.
8. **[DER] Why one estimator cannot serve all methods** (synthetic; one DGP each; illustrative):
   - **Target and constraints** (`S4_ANG_BASELINE.md` §13.2, Appendix B; 17 asset classes): scaled-identity shrinkage was harmful (up to 3.3× the minimum variance long-only, 10.7× unconstrained); correlation-only shrinkage and the long-only constraint were benign.
   - **Universe size** (§13.3, Appendix C; unconstrained GMV, out-of-sample variance / oracle):
     - for 17 asset classes, RMT eigenvalue clipping was **harmful** (1.77–1.89× vs sample 1.07–1.39×): the Marchenko–Pastur edge removes genuine low-variance directions;
     - for 100–300 stocks it was the **best** of the three in every cell tested (e.g. 300 stocks, T = 250: 1.26 vs 2.63 for correlation shrinkage; the sample matrix is singular);
     - with a long-only 10% cap (100 stocks) the three were within 1.06–1.13×.

   Hence eligibility is per method, constraint set and dimension (S4.13 → S10).
9. **[DEF]** Estimators, windows, eligibility regions, the reference-model choice and the sensitivity set → S10 (RQ-14). Whether IPS limits evaluated on the reference model are imposed *inside* each method's optimisation or checked afterwards → S4.16, S4.20, S11.

### D4 — Runtime backtest diagnostics [GR]
1. Backtest statistics used at runtime (candidate cards, metric score, CIO dimensions, ensemble weights) are:
   - computed **deterministically** under the S7-defined protocol (window, costs, point-in-time universe and data);
   - **labelled in-sample**;
   - shown with their sampling uncertainty.
2. They are **never** evidence for methodological admission (ADR-0025) and never a Method-Library selection criterion.
3. **[SRC]** ANG pp. 2, 14, 22: the agentic pipeline "cannot be cleanly backtested". Scope: applies to the agentic layer. Deterministic method backtests are possible but carry the overfitting risk quantified in D7.

### D5 — Declared units for beliefs and risk [AD]
1. Every CMA and risk artefact declares:
   - currency basis;
   - hedging basis;
   - horizon;
   - arithmetic vs geometric;
   - nominal vs real.
2. Artefacts on different bases are never combined without an explicit, versioned conversion.
3. **[DER]** The numéraire changes portfolios (D6: GMV weights are invariant to a NOK/USD change only if every asset's covariance with the exchange rate is equal).
4. **[DEF]** The engine's computation numéraire is decided at S5 (RQ-07), from `INV.reporting_currency`, `INV.consumption_currencies` and `POL.currency_hedging`.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Adopt ANG's learning as described (global skill deployment, performance culling) | Faithful; fast adaptation | Homogenises agents (ANG-37); culls on noise; conflicts with ADR-0025 and 02 §D |
| Disable learning until S17 | Simple | Contradicts the owner priority and ANG's pillar; loses data that must be captured from day one |
| **Governed learning (this ADR)** | Keeps the pillar; protects diversity; testable | More machinery (promotion gates, correlation measurement) |
| One authoritative risk model for construction **and** evaluation (r1 of this ADR; ANG's single covariance agent) | Consistent; simple | Forces one estimator on methods whose performance depends on it (§13.2, §13.3: the same estimator is best for one problem and 1.8× worse for another) |
| Each PC method picks its own Σ **and is evaluated on it** | Flexible | Candidates are incomparable; a method can pass limits by choosing a low-risk estimate; non-PSD inputs |
| **Method-specific construction models + one common reference model (this ADR, r2)** | Estimator fits the method; one yardstick for comparison, limits and learning | More artefacts; home-field bias of the reference estimator (mitigated by dual reporting and a sensitivity line) |
| Leave units implicit | Less paperwork | D6 shows the numéraire changes weights; silent unit mixing |

## Evidence
- `VERIFIED-SOURCE`: ANG v2 pp. 0, 2, 9 (fn. 4), 10, 12, 20, 24–25, 27–29; lecture s12, s16, s36.
- `VERIFIED-DERIVATION`: N_eff formula; GARCH horizon share; D6.
- Synthetic simulations (illustrative, one data-generating process each): `S4_ANG_BASELINE.md` Appendix B (estimator target × constraints) and Appendix C (RMT cleaning × universe size × constraints).
- `ASSUMED` (architecture decisions, not empirical claims): L-1 … L-7; the family floor; method-specific construction risk models with one common reference model per horizon.

## Consequences
- S4.3 adds learning objects for PC methods, review/vote, CIO and CRO, plus a risk-model artefact type with `role` (construction / reference / evidence), horizon and unit fields.
- S4.13 makes a per-method risk-representation dependency mandatory, with estimator eligibility over (N, q_eff, constraint set, horizon).
- S4.16/S4.17: candidate cards and diagnostics carry in-sample labels and uncertainty, and risk under both the construction and the reference model (risk-model disagreement; sensitivity line).
- S4.20 contract fields: currency, hedging, horizon and return-convention fields.
- S8: promotion pipeline (replay, shadow, promote, rollback); error-correlation measurement; no global auto-deploy path.
- S17: thresholds and margins.

## Revisit trigger
- S7/S17 evidence that the guardrails block measurably beneficial learning.
- S10 evidence that one estimator is eligible and best for every admitted method (construction and reference models may then coincide).
- S10 evidence that the choice of reference model changes the ranking of candidates materially (then report a reference set, not one model).
