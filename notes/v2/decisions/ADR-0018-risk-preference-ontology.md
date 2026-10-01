# ADR-0018 — Risk-preference ontology, calibration interface, and elicitation deferral

- **Status:** ACCEPTED (with owner amendments at G2)
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (G2 approval, 2026-10-01) · **Gate:** G2 · **Stage:** S2
- **Supersedes:** none · **Extends:** ADR-0010 (separation of preference and parameters), ADR-0014 §7 (derivation records)
- **Resolves:** RQ-02b, RQ-02c · **Defers:** RQ-02d (S11), RQ-50

## Context
Risk concepts must not be collapsed, and no category → γ mapping may be
assumed (owner instruction). Research memo:
research/S2_RISK_PREFERENCE_RESEARCH.md.

## Decision
1. **Ontology** (D2-09): stated preference · elicited preference/tolerance · risk capacity · risk requirement · model risk-aversion parameter · portfolio risk controls. They are distinct objects with provenance; none is interchangeable with another.
2. **Calibration** only through calibration-method contracts (O7). These declare formulation, units, basis, period, return frequency, validity, belief dependence, and recalibration triggers, and every output carries a derivation record. No mapping is adopted in S2.
3. **No universal category → γ mapping.** Qualitative categories are ordinal stated preferences. Calibration happens within the consuming model. **Model parameters such as γ have meaning only within a specified formulation, units, and calibration context, and are never stored as portable attributes of the investor.**
4. **Disagreements** among inputs (e.g. requirement > capacity; stated vs. elicited): the distinct objects are preserved, the disagreement is exposed, no object overwrites another, and capacity is never converted into preference. Whether particular objectively measurable capacity measures become hard portfolio constraints is deferred to S11; G2 does not restrict disagreements to being informational only (D2-10, amended).
5. **No elicitation instrument adopted** (D2-11). The `Instrument` contract is adopted; `INV.choice_battery` stays conditional; drawdown-reaction levels stay pending; candidate approaches go to S11 validation.
6. **Calibration vs. selection (for S11, RQ-02d/RQ-50):** calibrating a model to the user is distinct from selecting a portfolio from an efficient opportunity set through an interpretable user choice. Both remain available as distinct calibration-method types.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Category → γ table | Simple | Unsupported: γ is formulation-, unit-, frequency-specific; elicitation is method-dependent and better ordinal than cardinal |
| Single composite risk score | Simple | Collapses distinct concepts; loses provenance |
| Adopt an existing questionnaire now | Ready-made | Questionnaires explain little variation in holdings (Klement 2015); cross-method inconsistency (Pedroni et al. 2017) |
| **Ontology + model-internal calibration + deferred instrument** | Defensible; transparent | Calibration work moves to S11 |

## Evidence
See the research memo §2–§5. Key sources:
- Pratt (1964);
- Sharpe (2007);
- Merton (1969);
- Barsky et al. (1997);
- Dohmen et al. (2011);
- Holt & Laury (2002);
- Charness, Gneezy & Imas (2013);
- Pedroni et al. (2017);
- Klement (2015);
- ESMA35-43-3172;
- Das et al. (2010).

Each source carries its verification level in the memo.

## Revisit trigger
S11 calibration research or S15 validation results.
