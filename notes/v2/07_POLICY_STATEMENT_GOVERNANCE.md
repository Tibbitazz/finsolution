# 07 — Policy Statement Governance

**Document status:** STABLE (S0) for structure and principles; field lists and all calibrations `OPEN` (S1/S2/S11) · **Decision basis:** ADR-0006, ADR-0008, ADR-0009, ADR-0010

## 1. Definition and name

**Policy Statement** — the governing investor-policy configuration of the
engine: the investor's objectives, preferences, constraints, account
structure, permitted strategies, and autonomy/approval rules. It is the name
used in architecture, schemas, documentation, UI, and code (ADR-0008). The
abbreviation "IPS" is not used for it. The Norwegian pension product
*individuell pensjonssparing* is out of scope and is not modelled.

## 2. Hierarchy

```
Investor            tax residence, base currency, goals, horizons, risk preference (§5),
 │                  risk capacity, liquidity needs / cash-flow plan, outside wealth, experience
 ├─ Goal → Portfolio(s)    benchmark, allocation POLICY (ranges/bounds — weights are outputs),
 │                         risk limits, universe preferences, permitted strategies,
 │                         rebalancing and tactical policy
 │    └─ Account(s)        broker, wrapper, account currency(ies), capital (continuous),
 │                         permitted instruments, execution mode
 ├─ Methodological         preferences/overrides restricted to the ELIGIBLE menu (06)
 └─ System governance      autonomy, approval matrix, eligibility policy, agent permissions,
                           facts-staleness policy, reproducibility settings
Registries (facts; referenced, never entered as parameters): Tax · Wrapper · Instrument · Broker
```

Version 1 may run one portfolio; the schema permits several (goal-based).

**Precedence.** Effective permitted instruments for an account =
law ∩ wrapper ∩ broker ∩ investor preference. An account-level infeasibility
overrides a portfolio-level wish; the position is assigned to another account
or reported infeasible — never silently dropped.

## 3. Decision categories for Policy Statement items

| Category | Meaning |
|---|---|
| 1 User-defined parameter | Set by the owner |
| 2 Hard constraint | A deterministic predicate on weights or trades, checkable at decision time; never waived by an agent |
| 3 Soft target | Sought, may be missed; every miss is flagged in the investment-case report and requires a recorded owner response |
| 4 Model choice | Selected from the eligible, admissible menu |
| 5 Agent-determined | Chosen by an agent within bounds set by categories 1–4 |
| 6 System default | Technical defaults (windows, tolerances) until research replaces them |
| 7 Human approval | Actions requiring explicit owner approval |

**Hard-constraint rule.** Only quantities that are deterministic functions of
the proposed portfolio or trade list at decision time can be hard
constraints. Realised outcomes (realised drawdown, realised volatility)
cannot be: they are expressed either as ex-ante targets on a model-estimated
measure (soft) or as monitoring triggers with a pre-committed response.

**Conflict priority.** The Policy Statement must declare an ordering for
conflicts (e.g. hard constraints > risk limits > return target). The
ordering's content is `OPEN` (RQ-23, S2).

**Feasibility check on save.** Internally inconsistent or infeasible Policy
Statements (e.g. a return target unreachable within risk limits under current
estimates) are flagged when saved, not at trade time.

## 4. Beliefs ⊥ preferences (ADR-0009)

Preferences over outcomes never change beliefs about markets. Changing any
preference field must leave unchanged every artefact representing expected
returns, covariances/correlations, volatilities, regime states, and signals.

- **Single exception:** the investment horizon sets the *forecast horizon*
  of expected-return and risk estimates (a horizon-specific estimate is a
  different belief, not a distorted one).
- **Enforcement:** a propagation test — perturb each preference field and
  assert that the hashes of all belief artefacts are unchanged (horizon
  excepted). This test is part of the deterministic test suite.
- **Clarification (ADR-0013, accepted 2026-10-01):** as originally worded, this test cannot hold when a
  universe preference changes (Σ dimension, equilibrium returns, and
  cross-sectional scores all depend on the asset set). It is enforced as
  conditional invariance given a declared comparison universe (ADR-0013).
  The choice of comparison universe is RQ-38.

## 5. Risk preference vs. model parameters (ADR-0010)

**Accepted:** the investor's risk preference (a Policy Statement object) and
any optimiser's risk-aversion parameter (a model parameter) are **separate
objects**. Model parameters are *derived* from the preference by a
calibration layer:

```
Risk preference (qualitative selection and/or advanced input)
  + horizon + risk capacity + loss/drawdown tolerance + volatility preference
        │
 Risk-preference calibration layer        [design OPEN — RQ-02]
        │
 Model-specific parameterisation          γ_MVO · volatility target · risk budget · EPO sizing · …
```

**Why the separation is required — `VERIFIED-DERIVATION`** (numerical check
committed with S0 work; reproduce with any μ, Σ):

For the mean-variance objective max_w [w′μ − (γ/2) w′Σw], unconstrained
solution w* = (1/γ) Σ⁻¹μ:

1. **Units.** Expressing returns in percent (μ×100, Σ×10⁴) with the same γ
   scales w* by 1/100; the same portfolio requires γ/100. γ has no
   unit-free meaning without a stated return convention.
2. **Annualisation.** Scaling μ and Σ consistently by horizon h (μ×h, Σ×h)
   leaves w* unchanged; scaling μ but not Σ (a common error) multiplies w*
   by h. Invariance holds only under consistent scaling and the i.i.d.
   approximation; serial dependence breaks it (`ASSUMED` boundary, RQ-02).
3. **Not comparable across methods.** In simple EPO the solution is linear in
   1/γ, so γ only scales positions and leaves the Sharpe ratio unchanged;
   in anchored EPO with endogenous γ it is a normalisation, not a
   preference; risk parity, minimum variance, and hierarchical risk parity
   have no γ at all. One number cannot carry the same meaning across all
   construction methods.
4. **Category-to-γ mappings move with beliefs.** In the one-risky-asset
   Merton share w = (μ − r)/(γσ²), with an assumed 5% premium and 16%
   volatility, γ = 1, 2, 3, 5, 7, 10 give risky shares 1.95, 0.98, 0.65,
   0.39, 0.28, 0.20. A fixed γ band therefore implies a *different* risk
   level whenever estimates change — which is either correct
   expected-utility behaviour or an unwanted drift, depending on what the
   investor's preference actually is. That trade-off is unresolved (RQ-02).

**Not adopted:** the illustrative mapping Aggressive γ∈[1,3], Moderate
γ∈[4,6], Conservative γ∈[7,10]. It is recorded as an owner-proposed example
only. Note also that the ranges are non-contiguous (γ ∈ (3,4) and (6,7) map
to no category). Whether any qualitative-to-γ mapping is defensible is RQ-02.

**Interface requirement (accepted in principle; design `OPEN`):** the
Policy Statement must allow a simple qualitative selection for ordinary use,
and must not present a single coefficient as having identical meaning across
models. Whether an advanced mode (direct γ or calibration inputs) is offered,
and how, is RQ-02.

## 6. Propagation of risk preference

```
Risk preference → calibration → constraints / model parameters → candidate portfolios
  → CRO evaluation → aggregation / target portfolio → sizing and implementation → monitoring thresholds
```
Risk preference does **not** propagate into expected returns, covariances,
correlations, volatilities, regimes, or signals (§4).

## 7. Change control

Every Policy Statement change is versioned, requires owner approval, and
triggers recomputation of exactly the dependent artefacts (artifact
dependency graph, S8). Agents cannot modify the Policy Statement.
