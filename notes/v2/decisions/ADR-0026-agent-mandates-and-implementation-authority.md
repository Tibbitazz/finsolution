# ADR-0026 — Agent Mandates, institutional accountability, and implementation authority

- **Status:** PROPOSED
- **Date proposed:** 2026-10-02 · **Date decided:** —
- **Decided by:** — (route approved by the owner, D-C, 2026-10-02; final acceptance after the owner's mathematical/authority check, at G4 or earlier) · **Gate:** G4 · **Stage:** S4
- **Supersedes:** none
- **Extends:** ADR-0023 (§1 roles, §5 object model). **Annotates the reading of** ADR-0012 §7, 05 §2 layer 8, and 08 S13d. No body edits.
- **Resolves:** S4 closure gaps G-4, G-6, G-7, G-8, G-12 (`research/s4/S4_PLAN.md` §0, amendment 11)
- **Spec commit / tag:** —
- **Pre-acceptance amendment (2026-10-07, owner-approved ABD edit 4):** ABD 2014 [SRC] citations added in §4.1, §5.1, §5.3 and the Evidence list. No decision content changed.

## Basis labels used in this ADR
Every statement carries one of four labels, so that design choices are never presented as findings.

| Label | Meaning |
|---|---|
| **[SRC]** | Supported by a cited source. The scope of support is stated, and is never wider than the source |
| **[AD]** | **Architecture decision.** A system-design choice by this project. Sources may motivate it; none proves it |
| **[GR]** | **Governance rule.** A normative project rule. Not an empirical claim |
| **[DEF]** | Deferred: implementation detail or empirical question, owned by the named stage |

## Context
- ANG (Ang, Azimbayev & Kim, version of 21 Sep 2026) is the baseline investment-process architecture (ADR-0023).
- ANG ends at the strategic allocation: weights "are then implemented through trading" (p. 5). Its board memo carries "a quarterly rebalancing plan with off-cycle drift triggers" (p. 14). It defines no trading role.
- The owner's architecture review of 2026-10-02 (decisions D-A … D-E) used the Bauer–Christiansen–Døskeland (2022) review of NBIM ("BCD") as a complementary **accountability** framework *around* ANG, not a replacement.
- This ADR records the resulting objects and authority boundaries.

## Decision

### §1 Purpose and scope
1. **[AD]** Add an accountability layer around ANG's decision architecture without changing ANG's roles, order or authority boundaries.
2. **[AD]** Scope:
   - all ANG roles;
   - downstream extensions: Trader/Implementation, with an Execution service;
   - a conditional Tactical mandate.
3. **[AD]** Out of scope:
   - the methodology of any role (S7, S9–S13);
   - schema encoding (S8).

### §2 Relationship to ADR-0023
1. **[AD]** ADR-0023 §1–§9 remain in force.
2. **[AD]** This ADR:
   - adds two objects to ADR-0023 §5;
   - adds the downstream roles as **extensions** (ANG lists "rebalancing" among its roles but specifies no trading function);
   - adds an escalation edge.
3. **[AD]** No ANG role is removed, merged or reordered.

### §3 Object model (extends ADR-0023 §5)
1. **[AD]** `Method ≠ Method Contract ≠ Agent Role ≠ Agent Mandate ≠ Agent Instance ≠ Proposal ≠ Decision Record`.

| Object | Definition |
|---|---|
| Agent Role | Organisational position and its authority boundary (ADR-0023 §2) |
| **Agent Mandate** | Versioned contract governing one role. Fields: purpose; owned decisions; prohibited decisions; information/evidence rights and admitted interpretations; permitted methods (by Method Contract reference); hard constraints and risk limits (by reference); trade-off resolution declared in advance; control *type*; ADR-0017 authority grants required; runtime realisation; reporting obligations; escalation rules; provenance/trace keys; cost responsibility; evaluation (structure only); change control |
| Agent Instance | Runtime realisation: deterministic code, pinned model, human, or hybrid |
| Proposal | Output of a deliberative role (e.g. Portfolio Proposal) |
| **Decision Record** | Immutable record of a decision **or non-decision** by a role or authority. Carries trace keys, inputs consumed with their declared use, authority exercised, rationale and state |

2. **[AD]** A mandate references Method Contracts and never restates their mathematics.
3. **[AD]** A role has one active mandate version at a time.
4. **[DEF]** Field types, storage and versioning mechanics → S4.20 / S8.

### §4 Mandate controls, trade-offs, change control
1. **[GR]** A mandate declares its control *type* (portfolio control, forecasting reference, reference estimator, implementation control, validation criterion, admission criteria …). The *content* is fixed in advance by the S7 protocol. It is designated by a party other than the evaluated role.
   - **[SRC]** BCD p. 20 and App. C (p. 98) list "specified in advance" among valid benchmark properties, citing Wermers (2011).
   - **[SRC]** Sensoy (2009) finds self-designated prospectus benchmarks mismatched to actual style for almost one-third of funds, consistent with strategic behaviour. Scope: this supports "specification in advance is necessary but not sufficient". It does not address benchmarks chosen after observing performance; that prohibition is **[GR]**.
   - **[SRC]** ABD (2014, p. 92) recommends starting measurement from "a publicly-stated index from an independent index provider", which "provides transparency, accountability, and verifiability". p. 101: the rebalanced weighted benchmark "is entirely owned by the Ministry of Finance and the Storting", i.e. not by the manager evaluated against it. Scope: this supports controls being set independently of, and before, the evaluated role. It does not prescribe our control types.
2. **[GR]** Where one role weighs several criteria, the resolution rule or the resolving authority is declared in advance.
   - **[SRC]** BCD (pp. 6, 80) says two potentially conflicting objectives on one instrument "could lead to organizational challenges". Scope: this motivates explicit resolution. It does **not** establish a rule of one objective per role, and none is adopted.
3. **[AD]** Mathematical objectives and penalties belong in Method Contracts, not in mandates.
4. **[GR]** Any change to a mandate's owned decisions, prohibited decisions, information rights, limits, escalation rules or control type is **material** and requires human approval (consistent with ADR-0023 §8). Learning-loop outputs (S17) may propose mandate changes; they may not apply them.

### §5 Authority boundaries: investment decision → rebalancing determination → implementation → execution

**Principle [AD]:** investment decision ≠ rebalancing determination ≠ implementation discretion ≠ execution.

1. **Approved portfolio decision.** Produced by ANG → CIO; approved by the investor (ADR-0017).
   - **[AD]** It fixes:
     - target w* (version);
     - rebalancing rule (version);
     - permitted implementation window;
     - maximum interim deviation;
     - urgency class;
     - escalation triggers;
     - admitted timing-evidence method(s), if any;
     - default action while escalated.
   - **[SRC]** Upstream ownership of the rebalancing rule:
     - ANG p. 14: the rebalancing plan is part of the CIO's board memo;
     - BCD p. 14 fn. 5 and p. 20 fn. 13: the rebalancing decision and bands are set by the Ministry, not the implementing manager;
     - Perold & Sharpe (1988, p. 26): the choice of rule should fit "the investor's risk tolerance", and analysts "cannot and should not choose a strategy without substantial knowledge of the investor's circumstances and desires".
     - ABD (2014): the diversified benchmark and "a rebalancing rule" are the first stages of the investment process; they "involve active choices" (p. 16). "Rebalancing rules can add value, on average, compared to non-rebalanced, passive holdings" (p. 19). The rebalanced weighted benchmark is "the final stage under the responsibility of the Ministry of Finance" (p. 94). Returns should be reported at each stage (p. 92; Fig. 14, p. 159).
   - **Scope of that support:** it covers who **owns the rule**. It does not cover how the rule is evaluated.
2. **Rebalancing determination.**
   - **[AD]** Given the approved rule, the determination is **deterministic**: it evaluates the rule on current state and produces either an authorised transition or a no-rebalance Decision Record. It is a service, not an agent role.
   - **Rationale:** reproducibility (04), R2, and the absence of residual judgement once the rule is approved.
   - **Not a source finding.** No cited source shows that every rebalancing determination must be deterministic.
   - **Corollary [AD]:** a rule that requires judgement to evaluate (e.g. "rebalance when warranted") is not a valid approved rule. Such judgement is a portfolio decision and belongs upstream (ANG → CIO → investor).
3. **Trader / Implementation** is a **hybrid** role **[AD]**.
   - Code computes candidate implementation plans, limits, quantities, cost estimates and implementation statistics.
   - The Trader decides **when and how** within the mandate:
     - selects among permitted alternatives;
     - defers or stages when permitted;
     - uses admitted implementation/timing evidence;
     - escalates.
   - Agent choices are bounded per R1. Hard constraints are deterministic predicates per R3.
   - **[SRC]** Perold (1988, pp. 5–7) motivates judgement over pace: execution cost and opportunity cost are "at opposite ends of a seesaw", and pace of trading is "the chief factor". Scope: the trade-off exists. **Whether discretion adds value is [DEF] (S7/S13) and is never assumed.**
   - **[SRC]** ABD (2014): because traders can front-run an investor known to be forced to trade, "a fund manager should therefore have some leeway to optimally implement rebalancing" (p. 21). NBIM's framework is praised as one that "allows NBIM leeway to implement the required transactions" with "no ad-hoc decisions to rebalance" (p. 66). Scope: this supports implementation leeway under a rule owned upstream, for a very large fund facing adverse selection. Transfer of that motive to a small investor is **not** established. The leeway rationale here rests on cost/spread/FX/timing, and its value remains [DEF] (RQ-53).
4. **[AD]** The Trader may not:
   - change w*, the investment thesis, the rebalancing rule, the window or the deviation limit;
   - create exposure absent from the authorised transition;
   - convert implementation discretion into an unauthorised tactical strategy.
5. **Execution.**
   - **[AD]** Execution is a **deterministic service under the Trader's mandate**: order construction, rounding, broker rules.
   - Separate Decision Records; same accountability unit as the Trader.
   - **This is a system-design choice, not a literature finding.**
6. **Submission.**
   - **[GR]** Requires the investor or an ADR-0017 grant.
   - Dimensions 6–8 stay locked until accepted S13 safeguards exist (ADR-0017 §4).
7. **Post-trade evaluation.** **[AD]** Independent of the evaluated role.
8. **Default posture.**
   - **[AD]** A relatively narrow implementation window, with explicit evaluation status displayed.
   - Consistent with OD-4 / ADR-0025 (PROPOSED): no new gate before S7, and no assumption that discretion creates alpha.
9. **Deferred to S13 (RQ-53) [DEF]:**
   - discretion breadth;
   - default window values;
   - the quantitative boundary between implementation timing and tactical deviation;
   - whether controlled discretion reduces implementation shortfall net of delay cost at this investor's scale.

### §6 Tactical authority (conditional)
1. **[AD]** A tactical mandate (w^TAC = w* + Δ^TAC within explicit bounds) exists **only** if RQ-17 admits it at G13c.
2. **[AD]** If it exists, it is a separate mandate with:
   - its own control (w*);
   - its own limits;
   - its own costs;
   - its own attribution.
3. **[AD]** Implementation discretion never substitutes for it.

### §7 Escalation
1. **[AD]** Information relevant to the **investment case** returns to the appropriate investment authority (CRO / CIO / ANG re-run / investor). Examples:
   - a regime change;
   - an admissibility fact change (ADR-0019);
   - a stated invalidation condition;
   - a price move beyond a mandate threshold.
2. **[AD]** Information relevant only to **implementation** is handled within the mandate.
3. **[GR]** The escalating role never reverses the target unilaterally.
4. **[AD]** "Suspended pending investment review" is distinct from execution deferral and from awaiting authorisation (owner D-E).
5. **[DEF]** Whether it is encoded as a state or as a reason code → S8/S13 state-machine design.

### §8 Evidence rights
1. **[AD]** Evidence is produced once, by deterministic, versioned services (ADR-0012 §2).
2. **[AD]** Each descriptor declares:
   - its **horizon**;
   - its **admitted interpretations per consumer role**.
3. **[GR]** Each consumer records which evidence it used and for what purpose.
4. **[AD]** The same evidence may be consumed by several layers (e.g. AC/CMA judgement, CIO, Trader timing). That is legitimate when logged and is not automatically duplication.
5. **[GR]** No decision authority follows from an indicator's existence or predictiveness. Authority comes only from a mandate.
6. **[GR]** Agents interpret evidence; they never compute or alter it (R8).
7. **[AD]** No standalone Technical Agent in roster v0 (owner D-B).
   - Reconsideration requires the decomposition test: a distinct decision or responsibility, plus incremental decision value from independent synthesis.
   - **[SRC]** ANG p. 28 says to "decompose when the task requires genuinely distinct expertise that benefits from independent reasoning before aggregation".
8. **[SRC]** ANG computes technical signals inside the AC agents ("momentum, trend, mean reversion, relative momentum"; p. 38, Exh. A.1 step 4). The CMA judge "check[s] signal alignment" within [min_method, max_method] (p. 39, Exh. A.2). Scope: this establishes the AC/CMA placement only. ANG states no technical inputs for PC agents, the CIO, or trading.
9. **Annotation [AD]:** ADR-0012 §7, "time-series tactical signals are governed in S13d", is read **by use**, not by signal type:
   - time-series evidence used for beliefs or regime → S9;
   - used for timing or tactics → S13d.

### §9 Reporting and traceability
1. **[AD]** Every decision and non-decision produces a Decision Record.
2. **[AD]** Trace keys form the chain: `fill → order → implementation decision → authorised transition → approved target (incl. implementation parameters) → CIO decision → proposals → methods/evidence (with consumer use) → data/fact snapshot → Effective PS → Declared PS`.
3. **[GR]** Decision traceability ≠ causal performance attribution.
4. **[GR]** No container categories: every active decision type maps to mandate, role, method/evidence, authority, target acted on, constraints, timing, data, rationale, cost and outcome.
   - **[SRC]** BCD pp. 77–78 recommends mapping investments to teams. BCD describes the fund-allocation substrategy as "very difficult to assess as it is an amalgam of many diverse" strategies (pp. 4, 74), and "allocations" as "a container category" (p. 77).
5. **[DEF]** Attribution kinds and conventions → S7/S14 (RQ-54).

### §10 Human approval
**[GR]** Human approval is required for:
- the approved portfolio decision, including its implementation parameters;
- material mandate changes;
- any widening of Trader discretion;
- admission of any tactical mandate;
- ADR-0017 grants.

### §11 Annotations (no body edits)
1. **[AD]** 05 §2 layer 8: "tactical judgement only if RQ-17 allows" refers to deviation from w*. Implementation judgement inside the mandate is governed by RQ-53 / S13.
2. **[AD]** 08 S13d: the list of "tactical specialist agents (trend/momentum, technical, entry, exit, …)" is a **function inventory**. A function becomes an agent role only where the decomposition test (§8.7) passes.

## Mathematical claims embedded in this ADR and its companions

| # | Claim | Status | Conditions / scope |
|---|---|---|---|
| M-1 | For a linear CIO ensemble w = Σ_k λ_k w_k with Σ_k λ_k = 1 held over a period, the period return is r = Σ_k λ_k r_k. So λ-weighted attribution to proposals is an identity | `VERIFIED-DERIVATION` (linearity of portfolio return in weights) | Single period, on the weights held at the period start; no trading inside the period. Not applicable to non-linear ensembles (meta-optimisation, trimmed mean), which allow only counterfactual attribution |
| M-2 | Under "diversification of judgement" with linear expected-return estimates whose weights sum to 1, the first-best portfolio is the weighted combination of each manager's whole-portfolio optimum, and each manager uses the client's risk tolerance | `VERIFIED-SOURCE` (Sharpe 1981, eq. (20)–(22a), p. 230) | Mean–variance; common risk model; weights sum to 1. Sharpe shows the result fails when weights need not sum to 1 (alpha case, eq. (23)). For heterogeneous ANG methods it is an **analogy**, not a proof |
| M-3 | Implementation shortfall = Σ_i Σ_j (p_ij − p_i^b) t_ij + Σ_i (p_i^e − p_i^b)(n_i − m_i^e) = execution cost + opportunity cost | `VERIFIED-SOURCE` (Perold 1988, App. B, p. 9) | Measurement period between paper-portfolio trades; no net cash flows; transaction prices include commissions and transfer taxes; paper prices are decision-time midpoints (p. 5); management fees excluded (p. 5) |
| M-4 | For the paper-portfolio ladder P0 … P5, P5 − P0 equals the sum of adjacent differences | `VERIFIED-DERIVATION` (telescoping identity) | Each adjacent difference depends on the ladder's ordering and contains interaction effects. **Conditional decomposition, not causal effects** (RQ-54) |

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Deterministic Trader | Simplest; fully reproducible | Removes the judgement the role exists for; simplicity is not evidence (owner) |
| Trader with authority to deviate from w* | Flexible | An unaccountable tactical layer, i.e. a container category (BCD) |
| Rebalancing agent | Symmetry with other roles | Owns no residual judgement once the rule is approved |
| Standalone Technical Agent | Specialisation | Fails the decomposition test now; adds an unattributable opinion |
| One-objective-per-role rule | Simple accountability | Not supported by BCD; collides with methods that contain several terms |
| Edit ADR-0023 / ADR-0012 / 05 / 08 bodies | Single source of text | Violates change control; annotate instead |

## Evidence
- `VERIFIED-SOURCE` (read 2026-10-02):
  - ANG pp. 5, 14, 28, 38–39;
  - BCD pp. 4, 6, 14, 20, 49, 74, 77–80, 98;
  - Sharpe (1981) pp. 220, 230, 232–233;
  - van Binsbergen, Brandt & Koijen (2008), abstract and conclusions;
  - Sensoy (2009), abstract;
  - Perold (1988) pp. 4–9;
  - Perold & Sharpe (1988) pp. 16, 26;
  - Ang, Brandt & Denison (2014) pp. 16, 19, 21, 66, 92, 94, 101; Fig. 14 p. 159 (added 2026-10-07; identity verified).
- `VERIFIED-DERIVATION`: M-1, M-4.
- `ASSUMED`, i.e. architecture decisions that are not empirical claims:
  - deterministic rebalancing determination;
  - deterministic execution service;
  - the hybrid Trader;
  - the narrow default window;
  - evidence consumer logging;
  - no Technical Agent in v0.

Statistical and economic significance of implementation discretion: none claimed. That question is empirical (S7/S13).

## Consequences
- S4 plan:
  - S4.2b: accountability layer (role taxonomy, mandate stubs, responsibility matrix, escalation model);
  - S4.3: object types;
  - S4.15b: downstream inventory;
  - S4.16–S4.22: trace-key and evidence-use fields;
  - G4 criteria K-19 … K-23.
- `research/s4/S4_ACCOUNTABILITY.md` holds the mandate schema and stubs.
- `OPEN_QUESTIONS.md`: RQ-52 … RQ-54; RQ-17 and RQ-35 annotations.
- S8 receives mandates, Decision Records and trace keys as **interface-only** items (SYNC-1, SYNC-5).
- Harder: adding a role without a mandate, or an active decision without a responsible role.

## Revisit trigger
- S13 evidence on the value of implementation discretion.
- The RQ-17 outcome.
- S8 schema design reveals a missing authority boundary.
- The owner's mathematical/authority check finds a claim mislabelled.
