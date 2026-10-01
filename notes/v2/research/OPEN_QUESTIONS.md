# Open Research Questions

**Document status:** STABLE (S0) as a register; statuses as listed (updated at G3 closure, 2026-10-01) · Status vocabulary: [02 §C](../02_EVIDENCE_AND_STATUS.md)

No question below was resolved to complete S0. Each is assigned to the stage
and gate where it must be decided. "Owner input" marks questions that depend
on the owner's own circumstances rather than on literature.

| ID | Question | Stage → Gate | Status | Notes |
|---|---|---|---|---|
| RQ-01 | Investor Profile & Policy Statement input specification | S1 → G1 | RESOLVED (ADR-0014; S1_INPUT_SPECIFICATION) | S1_INPUT_SPECIFICATION + S1_SYNTHETIC_FIXTURES; no real profile required (ADR-0014) |
| RQ-02 | Representation and calibration of risk preference (see below) | S1, S2, S11 → G1, G2, G11 | IN-RESEARCH | 02a resolved in S1; 02b/02c RESOLVED (ADR-0018); 02d → S11, which must distinguish calibrating a model to the user from selecting a portfolio from an efficient opportunity set by interpretable choice (ADR-0018 §6) |
| RQ-03 | Norwegian account wrappers in scope (all pension wrappers excluded, ADR-0020) and their rules; taxation of shares, funds (incl. fund equity-share rules), interest; shielding deduction (wealth tax excluded, ADR-0021) | S3a → G3 | RESOLVED (ADR-0019; registry v1) | Primary sources only; legacy ASK claims are leads only; S3: S3_FINDINGS §2, facts/no_tax.yaml, facts/no_wrappers.yaml; all pension saving excluded (ADR-0020); Wealth-tax part withdrawn by owner scope decision (ADR-0021); ASK credit decomposition S3_FINDINGS §2.1; Closed at G3; remaining gaps carried as Class B (see carried gating register) |
| RQ-04 | Kildeskatt: withholding on foreign dividends, treaty rates, credit against Norwegian tax, treatment inside wrappers, fund-level withholding in non-domestic funds/ETFs | S3a → G3 | RESOLVED (ADR-0019; registry v1) | S3: W1–W9 model (ADR-0019 §6); US→NO verified for W1–W3, W5 (Nordnet), W7, W8 in part; W5 (eToro), W6, W9 unavailable (RQ-51); Corrected at G3 review: credit rules may apply on taxable ASK withdrawal (Skatte-ABC A-10-5.4.1); ASK mechanics partly unavailable (U4a–e, class B → S13a); Closed at G3; remaining gaps carried as Class B (see carried gating register) |
| RQ-05 | Instrument regulation for Norwegian retail investors: retail-availability rules (e.g. key information documents), CFDs, leveraged products | S3c → G3 | RESOLVED (ADR-0019; registry v1) | S3: PRIIPs KID requirement and CFD measures verified; US-ETF retail access recorded as interpretation (S3_FINDINGS §4); PRIIPs chain: conditional rule (PRIIP without Norwegian KID → no retail sale) verified; "US ETFs unavailable" stays interpretation (U9, class B → S5/S6); Closed at G3; remaining gaps carried as Class B (see carried gating register) |
| RQ-06 | Broker profiles for Nordnet and eToro: costs, instruments, ownership/custody model (real security vs. derivative), wrappers offered, FX, execution/API, data, tax reporting, availability to Norwegian residents | S3b → G3 | RESOLVED (ADR-0019; registry v1) | Neither preferred (ADR-0007); S3: facts/broker_nordnet.yaml, facts/broker_etoro.yaml; unknowns recorded as unknown; Closed at G3; remaining gaps carried as Class B (see carried gating register) |
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
| RQ-18 | Rebalancing policy; cost, tax, FX model; asset-location rules | S13a–b → G13a–b | OPEN | Rebalancing configuration structure fixed in S1 (`REB.*`); methods and parameters in RQ-44 |
| RQ-19 | Execution mode per broker (manual vs. API) | S13f → G13 | OPEN | Depends on RQ-06 |
| RQ-20 | Investment-case report contents and approval workflow | S14 → G14 | OPEN | |
| RQ-21 | Monitoring thresholds; eligibility hysteresis | S4, S16 → G4, G16 | OPEN | |
| RQ-22 | Meta-agent permissions and materiality threshold | S17 → G17 | OPEN | |
| RQ-23 | Conflict-priority ordering in the Policy Statement | S2 → G2 | RESOLVED (ADR-0016) | Interaction taxonomy and record architecture; no system default ordering |
| RQ-24 | Re-verification cadence per fact domain | S3 → G3 | RESOLVED (ADR-0019 §9) | Proposed cadences and event triggers: S3_REGISTRY_ARCHITECTURE §8 (ADR-0019 §9) |
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
| RQ-40 | Personal-data flow to external services (hosted LLM providers, data vendors): which fields, if any, may leave the machine; minimisation; local vs. hosted models; user consent | S8, S12 → G8, G12 | OPEN | None assumed until decided; only fields whose declared purpose requires an external component may be considered (ADR-0014 §8) |
| RQ-41 | Field metadata (incl. purpose, permitted consumers, necessity — ADR-0014 §8) and predefined option sets (e.g. risk categories, leverage levels, exclusion lists): research basis, advanced/custom ranges, validation | S2 → G2 | RESOLVED for governance (ADR-0015); contents → S3–S5 | Options must not be defaults |
| RQ-42 | Handling of users outside registry-covered jurisdictions; process for adding a jurisdiction | S3 → G3 | RESOLVED (ADR-0019 §10) | Unsupported is reported, never defaulted to Norway; Proposed nine-domain support test, no fallback: S3_REGISTRY_ARCHITECTURE §9 (ADR-0019 §10); Domain-specific support profiles; operation-level support checks (G3 amendment) |
| RQ-43 | Configuration portability: versioned export/import of a user profile across installations; schema-version compatibility; encryption and privacy of the artefact | S8 → G8 | OPEN | ADR-0014 §11 |
| RQ-44 | Rebalancing: taxonomy (drift-driven rebalancing vs. signal-driven target change), admissible approaches (calendar, band, hybrid, method-determined, custom), which parameters are user-settable vs. system-derived, trigger definitions, interaction with trade limits and cash flows | S13b → G13b | OPEN | Refines RQ-18; S1 fixes only the configuration structure |
| RQ-45 | Role, if any, of self-reported investment experience vs. verified broker knowledge tests in eligibility, suitability, or UI | S3c → G3; continues S14 (possible explanation/warning consumers) | OPEN (bounded finding at G3) | Field `INV.investment_experience` inactive (original note "remove if tests are the mechanism" superseded at G3 review); Finding: appropriateness is a firm obligation implemented by the broker; self-reported experience has no identified consumer → G3 D3-07 (retire vs. keep inactive); Owner at G3 review: field 1.7 NOT retired; kept inactive/conditional, not collected by default; never grants eligibility; never substitutes a broker test; activates only if a legitimate consumer is established (D3-07 revised); G3 approved D3-07 as revised |
| RQ-46 | Whether anticipated tax-residence change matters: multi-period or cross-jurisdiction tax-aware methods | S3a, S13a → G3, G13a | RESOLVED for S3 (ADR-0019; D3-10) | Field `INV.residence_change_expected` inactive; Exit-tax facts recorded (no.tax.exit_tax); field stays conditional; activation only if S13a admits a method needing it → G3 D3-10; Field stays conditional; method question carried to S13a |
| RQ-47 | Schema evolution: field versioning, retirement, migration of saved profiles | S2, S8 → G2, G8 | RESOLVED for policy (ADR-0015); tooling → S8 | |
| RQ-48 | Declared ordered alternatives: whether and how fields may carry user-declared fallbacks used only when the first choice is blocked or pending | S2 → G2 | RESOLVED as mechanism (ADR-0016); per-field enablement by each field\'s stage | Without declared alternatives, no substitution (S1 §7.1) |
| RQ-49 | Regulatory boundaries of a general-purpose, self-directed investment application used by individuals for their own portfolios, per capability (analytics → personalised outputs → trade lists → order submission → unattended execution), distribution model, hosting, and jurisdiction | S3c → G3; continues S11/S14, S13f | OPEN (bounded findings at G3; capability-specific) | A research question only — no regulatory status is implied. S3c investigates the boundary from intended functionality, distribution model, jurisdiction, and execution capabilities; regulatory status is not inferred from S2's use of ESMA guidance; Reframed at S3 approval (2026-10-01). S3_FINDINGS §6: authoritative statements A1–A9 separated from inference; capability → rule table; no legal conclusion → G3 D3-08; Owner at G3 review: no universal legal-review prerequisite; capability register (capability → evidence → unresolved issue → dependency/safeguard → enablement status) in S3_FINDINGS §6.3; A (application recommends) vs. B (user-declared rules computed) neither established as equivalent nor different; resolution needed by S11/S14 (recommendation framing) and S13f (execution) for gated capabilities; G3 approved gating in principle; no single application-wide conclusion |
| RQ-50 | Validation of risk-elicitation candidates for calibration use | S11, S15 → G11, G15 | OPEN | ADR-0018; candidate list in S2_RISK_PREFERENCE_RESEARCH §5; includes selection-from-opportunity-set approaches (ADR-0018 §6) |
| RQ-51 | Fund-level foreign withholding (W9): how withholding suffered inside funds/ETFs is determined and whether any investor-level relief exists, by fund domicile | S3 → S6, S13a | OPEN | Added at S3; no authoritative source located on 2026-10-01; Carried from G3 (Class B) |
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

## Carried gating register (Class B items)

Established at G3 (2026-10-01).
- Each item is **capability-gating**: it does not block the gate where it arose, but must be resolved before the named capability is enabled.
- **Gate entry rule** (08 §3): every gate package must list each item below whose owner stage is that gate's stage, with its disposition (resolved / still gating / re-assigned with reason).
- Items are closed only by a gate decision, never silently.

| ID | Unresolved question | Capability gated | Owner stage → gate | Resolution requirement |
|---|---|---|---|---|
| CB-01 | 2026 shielding rate (U1) | Tax calculations for income year 2026 | S13a → G13a | Record verified fact on publication; until then the component is unknown |
| CB-02 | 2027 tax parameters (U2) | Tax calculations for 2027 | S13a → G13a | Record on publication; proposals stay `proposed` |
| CB-03 | ASK credit: allocation/calculation inside ASK (U4a) | Detailed ASK after-tax modelling and tax functionality | S13a → G13a | Authoritative source on the mechanics; no inference meanwhile |
| CB-04 | ASK credit: tracking of withheld tax (U4b) | ASK tax-reporting aids | S13a → G13a | As above |
| CB-05 | ASK credit: interaction with input-value reduction (U4c) | ASK after-tax modelling | S13a → G13a | As above |
| CB-06 | ASK credit: carry-forward across dividend/withdrawal years (U4d) | Multi-year ASK tax projections | S13a → G13a | As above |
| CB-07 | ASK credit: broker-supplied information (U4e) | Broker tax-reporting support claims for ASK | S13a → G13a | Broker official documentation |
| CB-08 | Fund-level withholding (U5, RQ-51) | After-tax return inputs for funds/ETFs | S6 → G6 (attributes); S13a → G13a (treatment) | Authoritative source; instrument attribute design |
| CB-09 | Per-instrument PRIIPs/KID and fund-regime attributes; AIF-marketing barrier (U9, U9b) | Legal admissibility of individual instruments | S5/S6 → G5/G6 | S6 attribute population and sourcing; AIF-law research |
| CB-10 | eToro gaps (U10): Norway commission, entity applicability, ASK, withholding, appropriateness, API eligibility, direct reporting, inactivity-fee conflict | eToro feasibility, cost illustration, execution | S5 → G5 (availability); S13a → G13a (costs); S13f → G13 (API/execution) | Official eToro sources; conflict resolved only from authoritative current material |
| CB-11 | Nordnet gaps (U11): fractional shares, order types, exchange list; full reads of V-abs pages | Sizing/rounding; execution | S13e/S13f → G13 | Official Nordnet sources |
| CB-12 | RQ-49 — application-originated personalised recommendations | Recommendation/presentation functionality | S11/S14 → G11/G14 | Capability-specific characterisation |
| CB-13 | RQ-49 — target/model portfolios, trade lists | Enablement and presentation of these outputs | S11/S14 → G11/G14 | Revisit based on how output is generated and presented (A vs. B) |
| CB-14 | RQ-49 — distributed, rule-based, and unattended execution | Execution capabilities in distributed builds | S13f → G13 | Capability-specific characterisation with S13 safeguards (ADR-0017) |
| CB-15 | RQ-45 — legitimate consumer for field 1.7 | Any activation of `INV.investment_experience` | S14 → G14 (latest) | Research establishing a consumer; never an eligibility grant |
| CB-16 | Other source-country treaty/withholding regimes (S3_REGISTRY_ARCHITECTURE §9) | Withholding projections for non-US source countries | S5 → G5 (which markets); S13a → G13a (facts) | Facts recorded per source country used |

**Invariants carried from G3 into later stages (not gaps):**
- **Unknown ≠ verified not_offered.** This must survive into S5/S6 data structures and the Feasibility Engine (S8).
- **Domain-specific support.** Operations check their required fact domains.
- **Derived eligibility.** No single attribute, e.g. domicile, implies ineligibility.
