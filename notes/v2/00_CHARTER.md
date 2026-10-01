# 00 — Project Charter

**Document status:** STABLE (S0) · **Decision basis:** ADR-0001, ADR-0004 … ADR-0011

## 1. Objective

Design — to a specification precise enough that a developer can build it
without making undocumented financial or methodological assumptions — a
**personal agentic investment engine** that:

- runs locally on a server and is used through a browser interface;
- is governed by an interactive **Policy Statement** (the investor's governing
  investment-policy configuration, [07](07_POLICY_STATEMENT_GOVERNANCE.md));
- takes the investor from preferences and research evidence to a formal
  Policy Statement, data and signals, risk estimation, portfolio
  construction, multi-agent deliberation, a target portfolio, entry/exit and
  implementation decisions, a pre-trade investment-case report, monitoring and
  rebalancing, performance/model feedback, and controlled system improvement.

The architectural starting point is Ang, Azimbayev & Kim (2026), *The
Self-Driving Portfolio: Agentic Architecture for Institutional Asset
Management*. It is a reference architecture, **not** a source of
methodological defaults: every method choice is a research question.

## 2. Scope

| In scope | Out of scope (current system) | Not yet decided (research) |
|---|---|---|
| Local users (the owner and others) each running the engine with a private profile, tax-resident in a jurisdiction covered by the Tax Registry — initially Norway (ADR-0014) | All pension saving and pension products (IPS, EPK, any pension wrapper; pension wealth) — excluded by ADR-0008 and ADR-0020. Wealth tax (facts, fields, calculations, effects in comparison or construction) — excluded by ADR-0021 | Investment universe, geography, allocation unit |
| Brokers **Nordnet** and **eToro**, via an extensible Broker Registry, neither preferred (ADR-0007) | Broker-routing optimisation (architecture must permit it later; ADR-0006) | Account wrappers in scope beyond the exclusion above (S3a) |
| One or more accounts per investor; account capital as a **continuous** input (ADR-0007) | — | Execution mode (manual vs. API) per broker (S13f) |
| Strategic allocation, tactical entry/exit, implementation, monitoring, learning | — | Every model: returns, signals, risk, construction, tactical, aggregation |

## 3. Roles

| Role | Responsibility | Authority |
|---|---|---|
| **Owner** (Oliver) | Sets objectives and preferences; decides every gate; approves ADRs, Policy Statement changes, and anything requiring human approval | Final |
| **Research & architecture assistant** (Claude) | Literature and fact research, derivations, verification, option analysis with an honest recommendation, drafting documents and ADRs | Proposes; never accepts its own proposals |
| **Local user** | Owns a private Investor Profile and Policy Statement; sets preferences within facts, methodology, and feasibility (ADR-0014) | Final over own preferences; none over facts, methodology, or gates |
| **Developer** | Implements `ACCEPTED`/`STABLE` specifications; raises implementability and ambiguity issues | Decides software engineering details not covered by an ADR, provided no financial/methodological assumption is introduced |

## 4. Standard

Every specification must be defensible before an expert examiner attacking the
weakest assumption: methodological choices are justified against credible
alternatives with the trade-off named; claims carry an evidence tag
([02](02_EVIDENCE_AND_STATUS.md)); statistical, economic, and causal
significance are reported separately; robustness and fragility are reported
unprompted; uncertainty is flagged, never smoothed over.

## 5. Design principles

Each principle is binding and traceable to an ADR. Principles marked † were
present in the legacy material; they are retained **only because they are
independently justified here**, not because they were previously documented.

| # | Principle | Basis |
|---|---|---|
| P1 | **Research-first.** No method is adopted by inheritance, by availability in a library, or because the reference paper uses it. | ADR-0001 |
| P2 | **Foundation first.** Upstream questions (investor, jurisdiction, accounts, universe, data, evaluation protocol) are settled before anything that depends on them. | ADR-0011 |
| P3 | **Beliefs ⊥ preferences.** Investor preferences never alter estimates of returns, risk, correlations, regimes, or signals. Sole exception: the investment horizon sets the *forecast horizon*. | ADR-0009 |
| P4 | **Deterministic computation; bounded agent judgement.** Numbers are computed in code; agents interpret, critique, and choose only among code-computed candidates, with a deterministic fallback for every agent decision. | ADR-0004 |
| P5 | **Eligibility before evaluation before deliberation.** Methods reach agents only after passing feasibility, eligibility, and empirical admissibility for the *current* problem. | ADR-0005 |
| P6 | **Evidence net of the real implementation environment.** Performance is evaluated out of sample, net of the selected accounts' costs, FX, and taxes. | ADR-0006, ADR-0007 |
| P7 | **A simple control is permanent.** Every layer, method, and agent must beat a simple baseline out of sample, net of costs, to remain enabled. | ADR-0011 (RQ-25 defines the baseline) |
| P8 | **Facts are versioned data, not code.** Broker fees, tax rules, wrapper rules, and instrument attributes carry source, date, jurisdiction, and re-verification requirements. | ADR-0006 |
| P9 | **Reproducibility.** Every run is identified by a manifest covering data, facts, Policy Statement, code, models, prompts, and seeds. † (generalised) | ADR-0001, [04](04_REPRODUCIBILITY.md) |
| P10 | **Human approval at consequential points.** Policy Statement changes, soft-target breaches, registry changes, and trades require owner approval as set in the approval matrix. | ADR-0004 |
| P11 | **Fail small and predictably.** Estimation failures fall back to simpler, documented alternatives rather than propagating degenerate output. † | ADR-0004 |
| P12 | **Separations.** Signal ⊥ risk estimation; construction ⊥ parameter selection (tuning parameters chosen out of sample, past-only). † | ADR-0004 |
| P13 | **Pre-registration.** Evaluation protocols, eligibility thresholds, and materiality margins are committed to Git *before* the results they govern are produced. | ADR-0002 |

## 6. Definition of done (framework)

The framework is complete when, for every component in the roadmap, an
accepted specification states its inputs, outputs, mathematics, eligibility
contract, data requirements, fallback behaviour, evidence status, and
whether it is deterministic code, agent judgement, or human control — so that
no financial or methodological assumption is left to implementation.
