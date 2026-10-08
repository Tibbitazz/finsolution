# ADR-0027 — ANG adaptation decisions: governed learning, registry evolution, one authoritative risk model per problem, runtime diagnostics, declared units

- **Status:** PROPOSED
- **Date proposed:** 2026-10-08 · **Date decided:** —
- **Decided by:** — (owner; at G4 or earlier) · **Gate:** G4 · **Stage:** S4 (S4.2)
- **Supersedes:** none · **Extends:** ADR-0023 §8 ("a learning loop with human approval above materiality"), ADR-0024 §1, ADR-0025, ADR-0026 §4.4 and §8 · No body edits
- **Resolves:** C-5, C-6, C-11, C-12, C-13 (`research/s4/S4_ANG_ADAPTATION.md` §2); ANG-31, ANG-33, ANG-37 (in principle)
- **Spec commit / tag:** —
- **Revision history (pre-acceptance; PROPOSED text may change until decided):**
  - r1, 2026-10-08 (`37f81df`): D3 = one authoritative risk model per declared horizon per run, used by every PC method and the CRO.
  - r2, 2026-10-08 (owner review question: "should the risk estimation depend on the PC method, not one universal estimate applied to all?"): D3 split into **method-specific construction risk models** and **one common reference risk model per horizon for evaluation**. Evidence added: RMT cleaning by universe size (`S4_ANG_BASELINE.md` §13.3, Appendix C). **Withdrawn:** the owner had asked for an opinion, not a change.
  - r3, 2026-10-08 (**owner decision: Option A**): one authoritative risk model per problem (universe × horizon × risk object); estimator chosen by the risk role on a pre-registered risk-accuracy test; method-internal regularisation stays in the methods; CRO sensitivity report.

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

### D3 — One authoritative risk model per problem per run [AD] (r3, Option A)
1. The risk role produces **one authoritative risk model per declared problem**: universe (e.g. the asset-class SAA set; a security sleeve) × horizon (e.g. SAA; short horizon) × risk object (Σ; scenarios; factor model). Universe, horizon and the D5 units are mandatory fields. Every PC method addressing that problem consumes it by ID; the CRO, Policy Statement limit checks, candidate cards, Portfolio Map and learning records use the same model. **[SRC]** ANG p. 6 and p. 9: one covariance matrix feeds all PC agents.
2. **Estimator selection** is made by the risk role, once per problem, under a protocol fixed in advance (S7), on **out-of-sample risk accuracy** (realised variance of minimum-variance and tracking-error portfolios; robust volatility losses; model confidence set), and re-evaluated on a fixed cadence (S17). Never per run, never per PC method, never on portfolio return outcomes. If candidates are statistically indistinguishable, the simplest is chosen. Record: `research/s4/S4_RISK_MODEL_CHOICE.md`.
3. **Method-internal regularisation** stays inside each method as its source defines it (EPO correlation shrinkage, Black–Litterman prior, resampling, robust uncertainty sets), with parameters declared and tuned per constraint regime under S7/S11. No PC method receives a tailored risk model. **[SRC]** PBL 2021 pp. 125–127.
4. **PC agents never choose, test or switch estimators** (specification search; gameable limits; ADR-0026 §4.1).
5. **CRO sensitivity report:** each candidate's risk and weights under at least one alternative admissible estimator; a material change of the CIO recommendation is flagged in the board memo. Reported, never used to select. **[SRC]** ANG pp. 12, 19, 29.
6. AC-level volatility estimates and correlation rows are evidence only; assembled matrices are symmetrised and projected to the nearest PSD correlation matrix, with the distance reported.
7. **[DER]** Estimator choice matters greatly in unconstrained and high-dimensional problems and little under long-only bounds, and the ranking depends on the problem (`S4_ANG_BASELINE.md` Appendices B and C; `S4_RISK_MODEL_CHOICE.md` M-1, M-2). Hence per problem, not per method.
8. **[DEF]** Estimators, windows, eligibility regions and the sensitivity set → S10 (RQ-14); protocol → S7; method parameters → S11.

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
| Method-specific construction risk models + one common reference model (r2, withdrawn) | Estimator tailored to each method; one yardstick for evaluation | Two risk systems; per-method estimator choice is a specification search; the methods' real need (dampening return-error amplification) is met better inside the method (`S4_RISK_MODEL_CHOICE.md` M-2) |
| Each PC method picks its own Σ **and is evaluated on it** | Flexible | Candidates are incomparable; a method can pass limits by choosing a low-risk estimate; non-PSD inputs |
| PC agent tries several risk models and keeps the best | Appears adaptive | Backtest overfitting (Bailey et al. 2014); gameable limits; non-deterministic if an LLM chooses |
| **One authoritative risk model per problem, selected on pre-registered risk accuracy; regularisation inside methods; CRO sensitivity (this ADR, r3 = Option A)** | ANG-consistent (pp. 6, 9); comparable candidates; one yardstick for limits and learning; testable choice | Cannot tailor the estimator to one method within a problem; mitigated by method-internal regularisation and the sensitivity report |
| Leave units implicit | Less paperwork | D6 shows the numéraire changes weights; silent unit mixing |

## Evidence
- `VERIFIED-SOURCE`: ANG v2 pp. 0, 2, 9 (fn. 4), 10, 12, 20, 24–25, 27–29; lecture s12, s16, s36.
- `VERIFIED-DERIVATION`: N_eff formula; GARCH horizon share; D6.
- Synthetic simulations (illustrative, one data-generating process each): `S4_ANG_BASELINE.md` Appendix B (estimator target × constraints) and Appendix C (RMT cleaning × universe size × constraints); `S4_RISK_MODEL_CHOICE.md` M-1, M-2 (covariance vs return errors in mean–variance optimisation; method-level regularisation vs swapping the risk model).
- `VERIFIED-SOURCE` / `VERIFIED-ABSTRACT` literature for D3: listed in `S4_RISK_MODEL_CHOICE.md` §1–§2.
- `ASSUMED` (architecture decisions, not empirical claims): L-1 … L-7; the family floor; one authoritative risk model per problem (universe × horizon × risk object).

## Consequences
- S4.3 adds learning objects for PC methods, review/vote, CIO and CRO, plus a risk-model artefact type with universe, horizon, risk-object, estimator, version and unit fields.
- S4.13 makes a per-method risk-representation dependency mandatory and registers estimator candidates per problem, with eligibility over (N, q_eff, constraint regime, horizon).
- S4.16/S4.17: candidate cards and diagnostics carry in-sample labels and uncertainty, and a risk-model sensitivity line (risk and weights under at least one alternative admissible estimator).
- S4.20 contract fields: currency, hedging, horizon and return-convention fields.
- S8: promotion pipeline (replay, shadow, promote, rollback); error-correlation measurement; no global auto-deploy path.
- S17: thresholds and margins.

## Revisit trigger
- S7/S17 evidence that the guardrails block measurably beneficial learning.
- S10 evidence that, within one problem, the best estimator differs materially by method in a way that method-internal regularisation cannot address.
- S10/S17 evidence that the authoritative model's choice changes the CIO recommendation materially and often (then report a set of models, not one).
