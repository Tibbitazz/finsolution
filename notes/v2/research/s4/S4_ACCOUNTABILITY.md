# S4.2b — Accountability layer: role taxonomy, Agent Mandate schema, mandate stubs, responsibility matrix, escalation

**Document status:** DRAFT (S4.2b; candidate fields F20–F21 added 2026-10-07; companion to [ADR-0026](../../decisions/ADR-0026-agent-mandates-and-implementation-authority.md), ACCEPTED 2026-10-08; F20–F21 remain **candidate** fields for S4.20 by owner decision) · **Prepared:** 2026-10-02 · **Basis:** owner decisions D-A … D-E (2026-10-02); ADR-0023; ADR-0024; ADR-0017; 05 R1–R8

**Scope:**
- Structure only. No mandate *values* are decided here unless they follow from an accepted ADR.
- Every "deferred" entry names the owning stage.
- Basis labels follow ADR-0026: [SRC] / [AD] / [GR] / [DEF].

---

## 1. Agent Mandate schema (structure; types → S4.20 / S8)

| # | Field | Content | Basis |
|---|---|---|---|
| F1 | Identity & version | Mandate ID, role ID, version, approver, change history | [AD] ADR-0015 |
| F2 | Position | ANG role or extension; upstream and downstream roles | [AD] ADR-0023, ADR-0026 §2 |
| F3 | Purpose | What the role exists to do | [AD] |
| F4 | Owned decisions | Each typed as: bounded choice among code-computed candidates (R1), or an ADR-0024 §3 agent-selectable parameter | [GR] R1 |
| F5 | Prohibited decisions | Explicit list | [GR] |
| F6 | Information/evidence rights | Admitted evidence types and their **admitted interpretation** for this role; prohibited inputs; personal-data necessity (ADR-0014) | [AD] ADR-0026 §8; [GR] R5, R8 |
| F7 | Permitted methods | Method Contract references | [AD] ADR-0024 |
| F8 | Hard constraints | References (deterministic predicates) | [GR] R3 |
| F9 | Risk limits | References and owner | [AD] |
| F10 | Trade-off resolution | Declared in advance, where the role weighs several criteria | [GR] ADR-0026 §4.2 |
| F11 | Control type | Kind of control/reference/validation criterion. Content set in advance by S7, by a party other than the role | [GR] ADR-0026 §4.1 |
| F12 | Authority grants | ADR-0017 dimensions required | [GR] ADR-0017 |
| F13 | Runtime realisation | D / A / H / Hy; model pinning; R2 fallback | [AD] ADR-0023 §2–3 |
| F14 | Reporting | Output contract (machine + narrative), dissent, uncertainty with method | [AD] |
| F15 | Escalation | Triggers, destination, default action meanwhile | [AD] ADR-0026 §7 |
| F16 | Provenance | Trace keys emitted and consumed; evidence consumer log | [GR] ADR-0026 §8–9 |
| F17 | Cost responsibility | Costs this role causes | [AD] |
| F18 | Evaluation | Structure only; content S7 | [DEF] S7 |
| F19 | Change control | Material-change list; human approval | [GR] ADR-0026 §4.4 |
| F20 *(candidate, 2026-10-07)* | Verifiability | Per owned decision: autonomy class, verification method (known answer / seeded fault / repeat-run agreement / outcome), stability statistic | [DEF] RQ-55; for the owner's ADR-0026 check |
| F21 *(candidate, 2026-10-07)* | Learning signals | Outcome-based and process-based signals used to improve the role; records required; agent-memory scope; promotion rule (per role, diversity check) | [DEF] RQ-22 (design forward), RQ-56; G4 criterion 24 |

---

## 2. Role taxonomy and mandate stubs (v0)

**Key:**
- **Ext** = extension beyond ANG's specified roles.
- **Runtime** = default candidate only (D deterministic, A agent, H human, Hy hybrid).

| Role | ANG / Ext | Purpose (F3) | Owns (F4) | Must not (F5) | Evidence rights (F6) | Runtime (F13) | Control type (F11) | Stage owner |
|---|---|---|---|---|---|---|---|---|
| Investor | ANG ("board") | Owner; final authority | PS; approvals; grants | — | All | H | — | S1, S14 |
| Macro / Regime | ANG | Regime view | Regime classification (if a method is admitted) | Expected returns; weights | Macro data; trend/regime descriptors | Hy | Classification/forecast reference [DEF S7] | S9a |
| AC / CMA | ANG | Belief per universe element | CMA within [min, max] of code-computed methods | Weights; preference-driven adjustment (R6) | Valuation, history, technical descriptors ([SRC] ANG p. 38 step 4), macro | Hy | Forecasting reference [DEF S7] | S9b–d |
| Covariance / Risk | ANG | Risk representation | Choice among admitted estimators (where agent-selectable) | Weights | Returns; volatility state | D (Hy) | Reference estimator / statistical validation [DEF S7] | S10 |
| PC agent *k* (A1 … D4, B6, B7) | ANG (+ B6/B7 owner extension) | Proposal under method *k* | Interpretation; agent-selectable parameters only | Edit weights (R1); use evidence its contract does not consume | CMA, Σ; signals only via its Method Contract | Hy | Method-specific portfolio control [DEF S7] | S4, S11 |
| Researcher (E1) | ANG | Method discovery | Research-lane candidates | Production CIO allocation (ADR-0024 §1) | Literature | A | Admission criteria (ADR-0024/0025) | S4, S12 |
| Adversarial Diversifier (E2) | ANG | Orthogonal proposal | As its contract | Standalone recommendation | As PC | Hy | Diversity diagnostics [DEF S12] | S4, S12 |
| CRO | ANG | Independent risk assessment; sets interim-risk limits for implementation | Risk report; flags | Vote; weights | All proposals; risk and liquidity statistics | Hy | Risk-validation criteria [DEF S7] | S10, S12 |
| Peer reviewer | ANG | Critique and rank | Reviews; votes | Weights (vote ≠ weighting, ADR-0023 §7) | Proposals; CRO reports; cited evidence | A | Process criteria [DEF S12] | S12 |
| CIO | ANG | Combination/selection | Choice among code-computed ensembles; rationale; invalidation conditions; proposed rebalancing rule and implementation parameters | Hard constraints; final approval | All upstream evidence (logged use) | Hy | Simple-control comparison [DEF S7, RQ-25] | S12 |
| Rebalancing determination | ANG ("rebalancing") — **service** | Evaluate the approved rule | Nothing discretionary | Change rule or target | Holdings, prices, w*, rule | **D** ([AD] ADR-0026 §5.2) | Rule-defined | S13b |
| Tactical mandate | Ext — **conditional** (RQ-17) | Bounded temporary deviation | Δ^TAC within bounds | Change w* | Admitted tactical evidence | Hy | w* | S13c |
| Trader / Implementation | Ext | Implement w* well | When/how within window and limits; choice among permitted plans; deferral/staging when permitted; escalation | Change w*, thesis, rule, window, limits; create exposure; act tactically without a mandate | Cost, liquidity, spread, volatility, event calendars, admitted timing evidence, account/broker facts | **Hy** ([AD] ADR-0026 §5.3) | Implementation control, e.g. immediate-implementation paper portfolio [DEF S7] | S13c–e |
| Execution service | Ext — **service under the Trader** | Valid orders for the plan | Nothing discretionary | Change plan | Broker rules, lots, fractions | **D** ([AD] ADR-0026 §5.5) | Expected vs realised cost | S13e–f |
| Monitoring / Attribution | ANG ("monitoring") | Measure and report | Nothing | Decide | All records | D (+A summaries) | — | S14, S16 |
| Meta / Learning | ANG ("learning") | Propose improvements | Change proposals | Apply material changes (incl. mandates) without approval | Attribution records | Hy, H approval | — | S17 |

**Not in roster v0: a standalone Technical Agent** (owner D-B; ADR-0026 §8.7).

**Deferred for every row [DEF]:**
- F7: method lists (S4.20);
- F9: limit values;
- F14: output schemas (S8/S12/S13);
- F15: trigger thresholds (S12/S13);
- F18: evaluation content (S7).

---

## 3. Responsibility matrix v0: investment decision → execution

| Step | Decision content | Responsible | Approver | Record |
|---|---|---|---|---|
| 1 Portfolio decision | w*; rebalancing rule; window; interim-deviation limit; urgency; escalation triggers; admitted timing evidence; default action | ANG → CIO | Investor | Approved-decision record |
| 2 Rebalancing determination | Authorised transition, or no rebalance | Service (D) | — (rule pre-approved) | Determination record |
| 3 Implementation decision | When/how within the mandate | Trader (Hy) | — within mandate; escalation otherwise | Implementation record |
| 4 Execution | Orders | Service (D) under the Trader | — | Order records |
| 5 Submission | Send | Investor or ADR-0017 grant | Investor | Authorisation record |
| 6 Post-trade | TCA, shortfall, attribution inputs | Monitoring (independent) | — | Post-trade record |

**Risk ownership** [AD]:
- Strategic portfolio risk: PC / CRO / PS limits.
- Interim (transition) risk: the CRO sets limits on a **whole-portfolio** basis; the Trader plans within them.
- Liquidity: split by level (CRO portfolio, Trader order).
- Spread, commission, FX timing, delay cost and event exposure during implementation: Trader.
- Tax, wrapper and broker constraints: deterministic predicates.

---

## 4. Escalation model
- **Investment-case information** goes to CRO / CIO / ANG re-run / investor. Examples: regime change, admissibility fact change, invalidation condition, price move beyond a mandate threshold.
- **Implementation-only information** stays within the mandate.
- **During escalation** the mandate's default action applies (continue on schedule / hold within window / suspend). [DEF S13: which default]
- "Suspended pending investment review" stays distinct from deferral and from awaiting authorisation. [DEF S8/S13: state vs reason code]

---

## 5. "No trade" concepts (provisional; encoding deferred to S8/S13)

| # | Concept | Layer | Responsible |
|---|---|---|---|
| 1 | No portfolio change | Portfolio decision | ANG/CIO + investor |
| 2 | No rebalance: deterministic condition not met | Rebalancing determination | Rule |
| 3 | Execution deferred within the approved mandate | Implementation | Trader |
| 4 | Trade blocked by a binding constraint | Any | Binding source |
| 5 | Insufficient evidence/data | Any | Evidence owner |
| 6 | Awaiting required authorisation | Submission | Investor / grant |
| 7 | Suspended pending investment review | Implementation → investment process | Investment authority |

**Rules:**
- States are per transaction leg.
- A leg may carry several reasons, one of them primary.
- Every state has an owner and a resolving condition.

---

## 6. Traceability chain and attribution categories (definitions only; methods → S7/S14, RQ-54)

**Chain:**
`fill → order → implementation decision → authorised transition → approved target (incl. implementation parameters) → CIO decision → proposals → methods/evidence (consumer use) → data/fact snapshot → Effective PS → Declared PS`

**Paper-portfolio ladder (registered, not computed):**
- P0 user benchmark / policy baseline;
- P1 deterministic-only target (R2);
- P2 approved target;
- P2′ tactical target (only if admitted);
- P3 immediate-implementation paper portfolio, stamped at authorisation time ([SRC] Perold 1988, pp. 4–5: paper portfolio of decisions "just before you try to implement them", at decision-time mid);
- P4 actual gross;
- P5 actual net.

Adjacent differences are a **conditional, order-dependent decomposition with interaction effects. They are not causal effects** (ADR-0026 M-4).

**Attribution categories:** accounting · counterfactual · statistical · process/decision · transaction-cost. Residuals and interactions are not assumed identifiable.

**Governance delay** (CIO decision → authorisation) is measured separately and not charged to the Trader. [DEF RQ-54]
