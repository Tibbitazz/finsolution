# 08 — Roadmap (v2)

**Document status:** STABLE (S0; amended at G3 closure 2026-10-01 for parallel tracks) · **Decision basis:** ADR-0011, ADR-0022 · Supersedes every legacy roadmap.

## 1. Dependency chain — two coordinated tracks after G3 (ADR-0022)

```
S0 Charter & governance ── G0 ✓
 │
S1 Input specification ── G1 ✓
 │
S2 Configuration machinery ── G2 ✓
 │
S3 External-facts registries ── G3 ✓ (registries; no account choice)
 │
 ├──────────────── TRACK A — research / investment methodology ────────────────┐
 │                                                                             │
 │  S4 Method Library & Eligibility ── G4                                      │
 │   │                                                                         │
 │  S5 Universe & allocation unit ⇄ S6a data feasibility ── G5                 │
 │   │                                                                         │
 │  S6b Data architecture & registries ── G6                                   │
 │   │                                                                         │
 │  S7 Evaluation & backtest protocol ── G7 (pre-registered)                   │
 │   │                                                                         │
 │   ├── S9 Beliefs & signals (9a–9d) ── G9                                    │
 │   └── S10 Risk model (incl. RMT eligibility study) ── G10                   │
 │   │                                                                         │
 │  S11 Portfolio construction (incl. risk calibration) ── G11                 │
 │   │                                                                         │
 │  S12 Deliberation & aggregation ── G12                                      │
 │   │                                                                         │
 │  S13 Implementation & tactical (13a–13f) ── G13a–d                          │
 │   │                                                                         │
 │  S14 Investment-case report & approval ── G14                               │
 │   │                                                                         │
 │  S15 Full-system validation ── G15 (go / no-go)                             │
 │   │                                                                         │
 │  S16 Monitoring ∥ S17 Learning ── G17                                       │
 │                                                                             │
 └──────────────── TRACK B — software / platform development ─────────────────┤
    S8 Platform architecture & developer start ── G8 (begins after G3)        │
     │  then continuous build of the local application foundation             │
     │  consuming each accepted Track-A contract as its gate closes:          │
     │  G4 → method registry & eligibility engine · G5/G6 → universe,         │
     │  instrument & data contracts · G7 → evaluation harness · G9–G12 →      │
     │  belief/risk/construction/aggregation modules · G13 → cost/tax/FX/     │
     │  rebalancing/tactical/execution modules · G14 → report & approval UI   │
     │                                                                        │
    S18 Final developer handoff / completion ◄─────────────────────────────────┘
       (final documentation, accepted contracts, installation/release
        material, remaining integration) — not the first developer involvement
```

**Track coordination rules (ADR-0022):**
- **Track B never decides methodology.** It implements typed interfaces and stubs where Track A has not yet accepted a method. Track A never dictates frontend/backend technology unless a method requirement makes it necessary.
- **Progressive delivery.** Each Track-A gate delivers a software contract (S8 plan §"progressive implementation contract"). Track B integrates it without restructuring the core.
- **Feedback.** Developer findings (ambiguities, impossible contracts, missing data types, security or performance constraints, required schema changes) return through the change-control process defined at G8. Material changes go back through ADR, schema, or gate. They are never resolved silently in code.

**Why this order (Track A).** Preferences → feasible set → data → evaluation standard →
beliefs → choices → aggregation → implementation → oversight → learning.
Track B runs in parallel from G3 because S0–S3 already specify the
method-agnostic framework (profiles, Policy Statement, resolution,
registries, authority). Three deliberate placements: the evaluation protocol (S7) precedes every
model choice so it cannot be chosen to flatter results; the platform (S8) is
a parallel track because contracts and registries are method-agnostic; the
tactical layer (S13c–d) follows the target portfolio and the rebalancing
baseline because every tactical role is defined relative to them. S5 and S6a
iterate: universe choice needs data feasibility and vice versa.

## 2. Stages

Fields: **A** objective · **B** decisions · **C** research · **D** Policy Statement / configuration implications · **E** components affected · **F** blocks · **G** required output.

**S0 — Charter & governance.** A: how we decide; establish the source of truth. B: evidence standard, ADR process, facts policy, reproducibility, eligibility and Policy Statement governance, legacy status. C: none. D: system-governance level. E: all. F: everything. G: this directory.

**S1 — Investor Profile & Policy Statement input specification (user-facing layer).** A: specify what any local user can enter or change, field semantics, interaction model, conditional activation, privacy and purpose limitation, Declared → Effective behaviour, change propagation, and synthetic fixtures (ADR-0014). No real profile is required; user inputs are runtime configuration. B: tax residence (Norway); goals and priorities; horizons; cash flows; outside wealth; risk capacity vs. willingness; experience; *what to elicit about risk preference* (RQ-02a). C: lifecycle/strategic-allocation theory; risk-tolerance measurement and elicitation (RQ-02). D: Investor level. E: governance, report. F: S2, S3. G: research/S1_INPUT_SPECIFICATION.md and research/S1_SYNTHETIC_FIXTURES.md.

**S2 — Configuration machinery (underlying layer).** A: machine-readable governance implementing the S1 contract: formal schema language, validation engine, conflict-priority ordering, dependency graph, approval matrix, calibration machinery, schema versioning and migration (RQ-47). B: hierarchy (07 §2); category assignment; hard-constraint rule; precedence; conflict ordering (RQ-23); feasibility checks; approval matrix; artifact-dependency contract incl. broker/account nodes; **risk-preference object and its schema** (RQ-02b); **theory of risk-aversion parameters across formulations** (RQ-02c); *[ADR-0014]* field metadata for every Policy Statement field and the declared→effective resolution with conflict records; predefined option sets and their research basis (RQ-41). C: Policy Statement practice; portfolio-choice theory of risk aversion. D: defines all levels. E: all. F: S3–S8. G: research/S2_CONFIGURATION_MACHINERY.md, S2_RISK_PREFERENCE_RESEARCH.md, S2_SYNTHETIC_FIXTURES.md, S2_G2_DECISIONS.md; ADR-0015 … ADR-0018 (accepted at G2).

**S3 — External-facts research.** A: authoritative facts on the implementation environment. B: 3a Norwegian tax and in-scope wrappers (excluding individuell pensjonssparing), kildeskatt and treaty credits, fund-level withholding (RQ-03, RQ-04); wealth tax out of scope (ADR-0021); 3b Broker Registry for Nordnet and eToro — costs, instruments, ownership/custody model, wrappers offered, FX, execution/API, data, tax reporting (RQ-06); 3c instrument regulation, e.g. retail availability rules, CFDs (RQ-05); fact re-verification cadences (RQ-24). C: primary sources only. D: populates registries; enables account choices. E: universe, costs, tax, execution, eligibility. F: S5, S6b, S7, S13. G: registries v1 and their governance. **G3 approves the external-fact registries, not any user's account configuration** — broker, account, and wrapper choices are runtime user configuration (ADR-0014; consistency correction D3-a). Descriptive account-comparison specification (no ranking).

**S4 — Method Library & Eligibility framework (ANG baseline; ADR-0023/0024).** A: build and verify the mathematical repertoire operating inside the ANG agentic architecture (PC roster, upstream inventory, CRO/deliberation/CIO information contracts, typed dual contracts, eligibility framework), and remove infeasible methods before any comparison; plan in research/s4/S4_PLAN.md (S4.0–S4.27, SYNC-1…6 with S8). B: contract schema; funnel; reason codes; point-in-time evaluation; provisional policy; overrides; hysteresis (RQ-21). C: per method family as methods are registered. D: methodological level restricted to eligible menu. E: every method-consuming component. F: S5 (method requirements feed universe choice), S9–S13. G: eligibility-framework specification; candidate method inventory with contract status.

**S5 — Feasible universe & allocation unit.** A: what we allocate across. B: geography; asset-class vs. security vs. hierarchical; instrument types; currency policy — jointly determined by preferences, jurisdiction, accounts/brokers, data, and method requirements (RQ-07). C: diversification/home bias; 1/N vs. optimisation; selection net of costs; registry outputs. D: portfolio and account levels. E: all numerical layers. F: everything numerical. G: universe specification; allocation hierarchy; instrument-master scope; eligibility preview.

**S6 — Data.** A: point-in-time market data and versioned registries. B: 6a feasibility (parallel with S5); 6b vendors, survivorship, FX, risk-free rates, macro/text with leakage controls, snapshotting, registry storage, use of broker data (RQ-08). C: vendor coverage tests. D: system defaults. E: all. F: S7, S9, S10. G: data contracts, quality checks, registry storage design.

**S7 — Evaluation & backtest protocol (pre-registered).** A: fix how methods are judged before results. B: walk-forward design; holdout; costs/taxes from the account configuration; point-in-time eligibility; deterministic-only mode; prospective evaluation of the agent layer; benchmark; simple control baseline (RQ-25); multiple-testing controls; materiality margins; statistical power (RQ-26) (RQ-09); *[ADR-0012]* signal-evaluation design and the pre-registered variant grid (transformations × comparison universes × composite weights × windows) with multiple-testing control, and type-specific admissibility tests for signals, transformations, aggregations, and mappings (RQ-37). C: data-snooping and backtest-overfitting literature; prospective evaluation. D: benchmark, evaluation horizon. E: all gates. F: S9–S15. G: protocol and harness specification.

**S8 — Platform architecture & developer start (Track B, begins after G3; ADR-0022).** A: method-agnostic platform and the start of production-oriented construction of the local application foundation; developer-readiness matrix; core-framework vs. method-module boundary; progressive implementation contract for G4–G14; developer feedback and change control. Must not select investment methods. B: layers; boundary rules; artifact DAG; contracts; registries service; Feasibility Engine; agent anatomy; LLM provider and pinning; provenance; sandboxing; UI (Policy Statement editor incl. risk-preference interface, exclusion reports, what-if runs); technology stack and any reuse of legacy R code (RQ-10); *[ADR-0014]* local workspace and multi-profile storage, privacy boundary, personal-data flow to external services such as hosted LLMs (RQ-39, RQ-40), and a conflict-explanation UI; *[ADR-0012]* the deterministic signal & scoring component, the descriptor and evidence-packet schema (RQ-34), and whether an asset-state abstraction is adopted (RQ-36). C: agent frameworks; LLM non-determinism. D: approval implementation. E: all. F: infrastructure build. G: architecture specification; stack ADR.

**S9 — Beliefs & signals.** *[Restructured — ADR-0012]*
- **A:** expected returns, state, and deterministic cross-sectional descriptors.
- **B:**
  - 9a — whether and how to identify regimes (RQ-11).
  - 9b — CMA methods and combination, incl. whether a bounded LLM judge is allowed (RQ-12).
  - 9c — cross-sectional characteristics and scores: descriptor taxonomy (RQ-27); candidate families, e.g. value, momentum, quality/profitability, low volatility, size — candidates, not approved (RQ-28); transformation (RQ-29); comparison/normalisation universe (RQ-30, RQ-38); within-factor composites (RQ-31). Refines RQ-13.
  - 9d — mapping from scores to beliefs or weights (RQ-33) and across-signal aggregation architecture — master composite vs. separate signal vector vs. specialist consumers vs. hybrid (RQ-32).
  - Every candidate goes through the funnel with a typed contract (06 §5).
- **C:** return-predictability, CMA, forecast-combination, and factor literature (incl. Asness, Moskowitz & Pedersen 2013).
- **D:** method menus; horizon link; comparison universe (ADR-0013).
- **E:** macro, asset-class, judge agents; the signal & scoring component.
- **F:** S11–S13.
- **G:** method specifications with completed typed contracts; mapping specifications.
- **Dependencies added:** 9c ← S4 (typed contracts), S5 (cross-sections may be securities *or* asset-class instruments), S6 (point-in-time fundamentals, classifications, market caps), S7 (pre-registered signal evaluation); 9d ← 9b, 9c.

**S10 — Risk model.** A: Σ, downside, stress. B: covariance/volatility estimators; downside measure; factor model; stress/scenario design; **RMT and other high-dimensional methods only via the eligibility study, threshold pre-registered** (RQ-14). C: random-matrix and shrinkage literature; drawdown measures. D: risk-limit definitions. E: covariance agent, CRO. F: S11, S12. G: risk specification; RMT eligibility region or a "not eligible at our scale" record.

**S11 — Portfolio-construction method set.** A: competing methods from the admissible set only. B: method menu; constraint handling per method; common risk scaling; researcher-agent governance; **model-specific parameterisation of risk preference and the calibration mechanism** (RQ-02d) (RQ-15); *[ADR-0012]* which representation of signals each method consumes — expected returns via an accepted mapping, direct score/rank weights, or benchmark tilts (RQ-33). C: portfolio-construction literature. D: allowed menu; risk-preference mapping. E: PC agents. F: S12. G: method registry with contracts; calibration specification.

**S12 — Deliberation & aggregation.** A: one target portfolio. B: whether deliberation is retained; protocol; ensemble rules; decision-relevance test; deterministic control (RQ-16); *[ADR-0012]* agents receive deterministic evidence packets and are bound by rule R8 (RQ-34). C: multi-agent debate, voting, forecast/model combination, LLM-as-judge. D: ensemble menu. E: CRO, CIO. F: S13, S14. G: aggregation specification.

**S13 — Implementation & tactical.** A: target portfolio → per-account trades. B: 13a costs/tax/FX from the account configuration and asset-location rules; 13b rebalancing baseline (RQ-18, RQ-44): admissible approaches and parameter authority for the S1 `REB.*` configuration structure; drift-driven rebalancing (target unchanged) is kept distinct from signal-driven target changes (S13c/d); 13c tactical role — timing-only, bounded tilt, independent overlay, risk scaling, or integrated (RQ-17); 13d tactical specialist agents (trend/momentum, technical, entry, exit, stop/risk conditions, sizing, overlays, execution, costs/liquidity) — detailed later; *[ADR-0012]* time-series tactical signals are registered as candidates only (incl. a 5-day z-score mean-reversion rule), with the distinction between asset time-series state and position-dependent rules (RQ-35); horizon conflicts between cross-sectional and tactical signals are part of RQ-17; 13e sizing and rounding to broker minimum orders and fractional rules from continuous account value; 13f execution protocol per broker (RQ-19). C: dynamic trading with costs, time-series momentum, volatility management, technical-rule data snooping, stop-loss evidence, tax-aware rebalancing. D: tactical ranges, rebalancing policy, asset-location rules. E: tactical, sizing, execution components. F: S14, S15. G: ADRs; per-account trade-list contract.

**S14 — Investment-case report & approval.** A: explain the investment argument before execution. B: contents — Policy Statement compliance, macro view, estimates with dissent, method comparison and exclusion report, target vs. current, per-account trades, costs, FX, tax and kildeskatt impact, soft-target deviations with required responses, "what would make this wrong", fact snapshot and staleness, evidence status (RQ-20). D: approval matrix. E: CIO/report. F: S15. G: report template; approval workflow.

**S15 — Full-system validation.** A: go/no-go. B: deterministic walk-forward net of the actual accounts; prospective paper test of the agent layer; acceptance criteria. C: S7 protocol. F: live use. G: validation report.

**S16 — Monitoring.** A: stay within the Policy Statement. B: drift, risk, compliance, signal decay, data quality, eligibility-set changes, fact staleness, attribution, alert thresholds calibrated from S15 (RQ-21). G: monitoring specification.

**S17 — Learning & controlled improvement.** A: improve without silent drift. B: forecast evaluation; change proposals; shadow testing; materiality threshold; rollback; read-only files; threshold changes require evidence and approval (RQ-22). G: model-governance specification.

**S18 — Final developer handoff / completion.** A: completion of the build begun in Track B after G3/G8: final documentation, accepted contracts, installation/release material, remaining integration. Not the first developer involvement (ADR-0022). B: thin vertical slices; first slice = Policy Statement editor, registries, Feasibility Engine with exclusion report, one deterministic path to a report. G: build plan mapped to accepted specifications.

## 3. Decision gates

| Gate | Decision | Decided by |
|---|---|---|
| G0 | Charter, governance, roadmap | Owner |
| G1 | Investor profile | Owner |
| G2 | Policy Statement schema, precedence, risk-preference representation | Owner, on evidence |
| G3 ✓ | External-fact registries v1 and registry governance (not any user's account configuration) — closed 2026-10-01 | Owner, on S3 evidence |
| G4 | Eligibility framework, threshold policy, hysteresis | Owner, on evidence |
| G5 | Universe and allocation unit | Owner, on evidence |
| G6 | Data sources and registry design | Owner, on evidence |
| G7 | Evaluation protocol, benchmark, control, margins — fixed before results | Owner |
| G8 | Platform architecture, stack, developer-readiness matrix, core/module boundary, change control | Owner with developer |
| G9–G12 | Beliefs & signals (incl. score definitions, comparison universe, score→belief mapping, aggregation architecture); risk model incl. RMT region; PC set incl. risk calibration and signal consumption; aggregation | Owner, evidence-gated |
| G13a–d | Costs/tax/location; rebalancing; tactical role; tactical methods | Owner, evidence-gated |
| G14–G15 | Report specification; go/no-go | Owner |
| G17 | Learning permissions | Owner |

**Gate entry rule (from G3):** every gate package lists each item in the
carried gating register ([OPEN_QUESTIONS](research/OPEN_QUESTIONS.md))
whose owner stage is that gate's stage, with its disposition. A capability
gated by an open item stays disabled, but remains architecturally supported,
until the item is resolved at a gate.
