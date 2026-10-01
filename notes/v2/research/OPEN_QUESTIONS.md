# Open Research Questions

**Document status:** STABLE (S0) as a register; every question `OPEN` · Status vocabulary: [02 §C](../02_EVIDENCE_AND_STATUS.md)

No question below was resolved to complete S0. Each is assigned to the stage
and gate where it must be decided. "Owner input" marks questions that depend
on the owner's own circumstances rather than on literature.

| ID | Question | Stage → Gate | Status | Notes |
|---|---|---|---|---|
| RQ-01 | Investor Profile content: goals, priorities, horizons, cash flows, outside wealth, experience | S1 → G1 | IN-RESEARCH | Schema public (S1_QUESTIONNAIRE); answers are local per user (ADR-0014); the owner's profile is the first test case |
| RQ-02 | Representation and calibration of risk preference (see below) | S1, S2, S11 → G1, G2, G11 | OPEN | ADR-0010 fixes only the separation |
| RQ-03 | Norwegian account wrappers in scope (excl. individuell pensjonssparing) and their rules; taxation of shares, funds (incl. fund equity-share rules), interest; shielding deduction; wealth-tax treatment | S3a → G3 | OPEN | Primary sources only; legacy ASK claims are leads only |
| RQ-04 | Kildeskatt: withholding on foreign dividends, treaty rates, credit against Norwegian tax, treatment inside wrappers, fund-level withholding in non-domestic funds/ETFs | S3a → G3 | OPEN | |
| RQ-05 | Instrument regulation for Norwegian retail investors: retail-availability rules (e.g. key information documents), CFDs, leveraged products | S3c → G3 | OPEN | |
| RQ-06 | Broker profiles for Nordnet and eToro: costs, instruments, ownership/custody model (real security vs. derivative), wrappers offered, FX, execution/API, data, tax reporting, availability to Norwegian residents | S3b → G3 | OPEN | Neither preferred (ADR-0007) |
| RQ-07 | Universe, geography, allocation unit, currency policy | S5 → G5 | OPEN | Joint with S3, S4, S6a |
| RQ-08 | Data vendors, survivorship, FX/risk-free sources, text data and leakage controls, registry storage | S6 → G6 | OPEN | |
| RQ-09 | Evaluation protocol: walk-forward design, holdout, metrics, benchmark, multiple-testing controls, materiality margins | S7 → G7 | OPEN | Pre-registered before results |
| RQ-10 | Technology stack, agent anatomy, LLM provider/pinning, reuse of legacy R code | S8 → G8 | OPEN | With developer |
| RQ-11 | Whether and how to identify regimes | S9a → G9 | OPEN | |
| RQ-12 | CMA methods and combination; whether a bounded LLM judge is permitted | S9b → G9 | OPEN | |
| RQ-13 | Return signals (cross-sectional, time-series, valuation, etc.) | S9c → G9 | OPEN | Refined into RQ-27 … RQ-33 (ADR-0012, proposed) |
| RQ-14 | Risk-model estimators; RMT/high-dimensional eligibility region in (N, T_eff) | S10 → G10 | OPEN | Framework in 06 §4; no threshold set |
| RQ-15 | Portfolio-construction method set and constraint handling | S11 → G11 | OPEN | |
| RQ-16 | Whether multi-agent deliberation adds value; aggregation rules | S12 → G12 | OPEN | Deterministic control required |
| RQ-17 | Role of tactical signals (timing-only / bounded tilt / overlay / risk scaling / integrated) and tactical methods | S13c–d → G13c–d | OPEN | Stage preserved; detail later |
| RQ-18 | Rebalancing policy; cost, tax, FX model; asset-location rules | S13a–b → G13a–b | OPEN | |
| RQ-19 | Execution mode per broker (manual vs. API) | S13f → G13 | OPEN | Depends on RQ-06 |
| RQ-20 | Investment-case report contents and approval workflow | S14 → G14 | OPEN | |
| RQ-21 | Monitoring thresholds; eligibility hysteresis | S4, S16 → G4, G16 | OPEN | |
| RQ-22 | Meta-agent permissions and materiality threshold | S17 → G17 | OPEN | |
| RQ-23 | Conflict-priority ordering in the Policy Statement | S2 → G2 | OPEN | |
| RQ-24 | Re-verification cadence per fact domain | S3 → G3 | OPEN | |
| RQ-25 | Definition of the permanent simple control baseline | S7 → G7 | OPEN | |
| RQ-26 | Statistical power for evaluating the agent layer at strategic horizons | S7, S15 → G7, G15 | OPEN | May be low; must be stated honestly |
| RQ-27 | Descriptor taxonomy: exact classification rules for cross-sectional scores, time-series states, implementation/risk attributes (asset × account, asset × portfolio), and position-dependent tactical rules; output-semantics vocabulary | S4, S9c → G4, G9 | OPEN | ADR-0012 proposes the distinction; details open |
| RQ-28 | Candidate cross-sectional signal families (value, momentum, quality/profitability, low volatility, size; others to be identified): rationale, evidence, definitions, data, eligible universe — per family | S9c → G9 | OPEN | Candidates only; sources' claims to be verified per family |
| RQ-29 | Transformation: raw, cross-sectional z-score (incl. winsorised variants), percentile rank, quantile class, rank-weights — judged on outlier robustness, information preservation, interpretability, cross-sectional stability, universe-size dependence, turnover, concentration, suitability as optimiser input | S9c → G9 | OPEN | Criteria and variant grid pre-registered under RQ-37; z-scores not presumed superior |
| RQ-30 | Normalisation/comparison universe: whole eligible universe, country, region, sector, industry, asset class, hierarchical/neutralised; minimum group size and fallback | S9c → G9 | OPEN | Linked to RQ-38 |
| RQ-31 | Within-factor composites: metric selection and orientation (e.g. P/E vs. E/P for loss-makers), weights (equal, fixed ex ante, estimated), missing-data rule, order of operations (combine-then-rank vs. rank-then-combine) | S9c → G9 | OPEN | Final ranking does not remove outlier dominance inside a z-sum |
| RQ-32 | Across-signal aggregation architecture: (A) master composite, (B) separate signal vector, (C) specialist consumers of different signals, (D) hybrid; whether aggregation happens at score, belief, or portfolio-return level | S9d, S11, S12 → G9, G11, G12 | OPEN | No master score adopted. AMP combines strategy *returns* (eq. 3), not scores |
| RQ-33 | Mapping scores to use: score → α → μ (incl. as an EPO signal); direct score/rank weights; benchmark tilts w = w_b + Δw(score); per-method consumption; transfer of long-short factor evidence to a long-only investor | S9d, S11 → G9, G11 | OPEN | Scores must not be substituted for μ without an accepted mapping |
| RQ-34 | Evidence-packet schema for agents: raw metrics, method and version, comparison universe, observation and data timestamps, provenance, staleness; agent-use rules | S8, S12 → G8, G12 | OPEN | Rule R8 proposed |
| RQ-35 | Time-series tactical signal candidates (mean reversion incl. 5-day z-score scale-in rule, trend, moving-average state, breakout, volatility state, RSI, …); asset state vs. position-dependent policy; signal-time vs. execution-time assumptions | S13d → G13d | OPEN | Registered only; nothing approved; the screenshot rule has no evidence attached |
| RQ-36 | Asset-state abstraction (structured descriptor vector consumed selectively) vs. simpler alternatives; correct indexing (asset, asset × account, asset × portfolio) | S8, S9d → G8, G9 | OPEN | Candidate only |
| RQ-37 | Signal-evaluation design: factor-portfolio tests (rank-weighted and quantile), predictive tests, net-of-cost evaluation under account configuration, pre-registered variant grid, multiple-testing control | S7 → G7 | OPEN | Must be fixed before any signal result is produced |
| RQ-39 | Local workspace design: storage format and location, multiple profiles, encryption at rest, backup/export, separation of user run history | S8 → G8 | OPEN | ADR-0014 |
| RQ-40 | Personal-data flow to external services (hosted LLM providers, data vendors): which fields, if any, may leave the machine; minimisation; local vs. hosted models; user consent | S8, S12 → G8, G12 | OPEN | None assumed until decided |
| RQ-41 | Field metadata and predefined option sets (e.g. risk categories, leverage levels, exclusion lists): research basis, advanced/custom ranges, validation | S2 → G2 | OPEN | Options must not be defaults |
| RQ-42 | Handling of users outside registry-covered jurisdictions; process for adding a jurisdiction | S3 → G3 | OPEN | Unsupported is reported, never defaulted to Norway |
| RQ-38 | Comparison-universe invariance: compute relative scores over the policy-permitted universe or over a preference-independent reference universe, then filter | S5, S9c → G5, G9 | OPEN | ADR-0013 (proposed) makes the comparison universe an explicit input |

## RQ-02 — Risk preference: representation and calibration

Assigned: **S1** (what to elicit), **S2** (representation; theory across
formulations), **S11** (model-specific parameterisation and calibration).

Already established by derivation (07 §5, `VERIFIED-DERIVATION`): γ's value
depends on return units; it is invariant to *consistent* annualisation under
i.i.d. scaling; it carries different (or no) meaning across MVO, EPO, risk
parity, minimum variance, HRP; the risk implied by a fixed γ moves with
estimates.

To determine:
1. What γ represents economically (e.g. relative vs. absolute risk aversion; link to expected-utility and the mean-variance approximation) and under which assumptions.
2. How its interpretation depends on the exact objective function (budget constraint, risk-free asset, leverage, benchmark-relative objectives).
3. Its dependence on return units, annualisation, horizon, and serial dependence beyond the i.i.d. case.
4. Ranges used in the academic literature and the evidence behind them (sources to be verified before citation).
5. Whether any academically defensible mapping exists from qualitative categories (Aggressive / Moderate / Conservative) to γ; if not, state so and design a calibration mechanism.
6. Whether one γ can be used across MVO, EPO, and other methods (derivation says not in general; specify per-method parameterisation).
7. Whether preference should instead be anchored on economically interpretable quantities — volatility target, maximum acceptable loss at a stated probability and horizon, certainty equivalent, drawdown tolerance — and the trade-off between a fixed γ (risk varies with opportunities) and a fixed risk target (ignores opportunity changes).
8. Whether the Policy Statement offers both a qualitative mode and an advanced mode (direct γ or calibration inputs), and how the UI explains the derived model parameters.

The owner's illustrative mapping (γ∈[1,3]/[4,6]/[7,10]) is recorded and not adopted.
