# ADR-0012 — Deterministic signal & scoring architecture: descriptor taxonomy, score ≠ belief, typed eligibility

- **Status:** PROPOSED (to be decided at G0)
- **Date proposed:** 2026-10-01 · **Date decided:** —
- **Decided by:** — · **Gate:** G0 (architecture); methods at G7/G9/G11/G12/G13d · **Stage:** S0
- **Supersedes:** none · **Extends:** ADR-0004 (adds rule R8), ADR-0005 (typed contracts), ADR-0011 (S9 restructure) — none of their bodies is modified
- **Resolves:** none (opens RQ-27 … RQ-37)

## Context
The owner supplied three sources — Asness, Moskowitz & Pedersen (2013),
*Value and Momentum Everywhere*, JF 68(3) (AMP); L. Q. Sørensen,
*Constructing value and momentum scores* (2026); L. Q. Sørensen / Storebrand,
*Factor Investing* (2025) — and a social-media description of a 5-day
z-score mean-reversion rule. The word "score" covers different objects in
these materials, and v2 had no explicit place for deterministic scoring.

## Decision
1. **Descriptor taxonomy.** Every deterministic descriptor declares what it is
   relative to and how it is indexed:
   - **Cross-sectional characteristic/score** S^CS_{i,t}: relative to a
     *declared comparison universe* at t.
   - **Time-series state** S^TS_{i,t}: relative to the asset's own history.
   - **Implementation/risk attributes:** indexed asset × account (cost, tax,
     FX, broker feasibility, liquidity at the account's size) or
     asset × current portfolio (marginal risk contribution, concentration).
     They are not expected-return signals.
   - **Position-dependent tactical rules** (e.g. scale-in by tranche,
     exit-all conditions) are *policies* over asset state and holding state,
     not scores.

   Each descriptor declares an **output semantics** from: characteristic ·
   rank/score · expected-return estimate · constraint/attribute · tactical state.
2. **Deterministic production.** Within the Research layer, a distinct
   deterministic signal & scoring component produces descriptors from
   point-in-time data: raw data → raw characteristics → transformation →
   scores. Belief formation (expected returns, regime) is a separate,
   downstream step. Every descriptor carries provenance: raw inputs, method
   and version, comparison universe, observation and data timestamps,
   staleness state.
3. **Score ≠ expected return.** No score, rank, or z-score is used as μ, α,
   or an EPO signal s unless an `ACCEPTED` mapping specification exists
   (RQ-33). Each consumer (portfolio-construction method, agent, tactical
   rule) declares which representation it consumes.
4. **No master composite adopted.** The data model must represent signal
   dimensions separately. Any across-signal aggregation is an explicit,
   versioned method in the Method Library (RQ-32). Within-factor composites
   are likewise explicit methods (RQ-31).
5. **Agent boundary — new rule R8 (evidence binding), extending ADR-0004.**
   Any quantitative characterisation of an asset by an agent ("cheap",
   "strong momentum") must cite a deterministic descriptor from its evidence
   packet. Agents cannot compute, alter, or re-normalise descriptors. They
   may interpret them, compare them with other evidence, and challenge their
   applicability (e.g. a value metric for a firm with negative earnings), in
   writing and logged.
6. **Eligibility, extending ADR-0005.** Signals, transformations,
   aggregations, and score→belief mappings are Method Library entries.
   They pass the same funnel through **typed contracts**: a common core
   plus type-specific fields (06 §5). There is no parallel framework.
7. **Roadmap, extending ADR-0011.** S9 is restructured (9a regime, 9b CMAs,
   9c cross-sectional scores, 9d score→belief mapping & aggregation). S7
   pre-registers the signal-evaluation design and variant grid. Time-series
   tactical signals are governed in S13d.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Scores embedded inside CMA/optimiser methods | Fewer components | Couples signals to return-requiring optimisers (EPO/MVO); hides a reusable input; scores silently become μ |
| Separate, parallel signal-eligibility framework | Clean conceptual split | Duplicated governance that drifts (the legacy failure mode) |
| **Distinct scoring component + one funnel with typed contracts** | Reuse across consumers; one governance regime; separation kept by type/semantics fields | Contract schema is more complex |

## Evidence
`VERIFIED-SOURCE` (read in full 2026-10-01):
- AMP p. 932 distinguishes time-series momentum ("a timing strategy using each asset's own past returns") from the cross-sectional momentum studied.
- AMP eq. (1): rank weights w = c_t(rank(S) − mean rank).
- AMP p. 938: ranks mitigate outliers; raw-signal portfolios "similar and … slightly better".
- AMP p. 939: signal-weighted factors beat tercile spreads.
- AMP eq. (3): combination is of strategy *returns*.
- AMP Table I: value–momentum correlation ≈ −0.53 to −0.65 within stock markets.
- AMP Table VI: separate value and momentum factors needed for pricing.
- Sørensen 2026: global z-scores → equal-weighted sum → percentile rank; 12–1 momentum.
- Storebrand 2025: max Σ score·w requires constraints; "higher score indicates higher expected returns".

`ASSUMED` (our inference, untested): aggregating signals into one score
before portfolio construction may discard diversification information that
return-level combination preserves.

## Consequences
- More research questions (RQ-27 … RQ-37).
- The scoring design space is combinatorial, so S7 must pre-register the variant grid with multiple-testing control.
- The comparison-universe issue exposes an ambiguity in ADR-0009's enforcement test (addressed by ADR-0013).

## Revisit trigger
Evidence at G9/G11/G12 that a different decomposition serves consumers better.
