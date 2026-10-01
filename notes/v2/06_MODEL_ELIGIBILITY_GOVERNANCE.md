# 06 — Model-Eligibility Governance

**Document status:** STABLE (S0) for the framework; every threshold `OPEN` · **Decision basis:** ADR-0005

## 1. The funnel

```
Policy Statement + Accounts/Brokers + Universe + Data availability   (= Problem Context, point-in-time)
        │
 (1) FEASIBLE     hard logical preconditions            [code]
        │
 (2) ELIGIBLE     theoretical / empirical preconditions  [code]
        │
 (3) ADMISSIBLE   passed the pre-registered evaluation protocol vs. the simple control,
        │         net of the selected accounts' costs, FX and taxes   [code]
        │
 (4) DELIBERABLE  the only set agents may see and choose among        [agents, within bounds]
```

Replaces the pattern "all available models → agent chooses".

## 2. Rules

1. **Contract required.** A method cannot be registered without an
   eligibility contract (§3). This applies equally to methods proposed by a
   researcher agent.
2. **Point-in-time.** Eligibility is evaluated with information available at
   each decision date. Using full-sample N or T to decide eligibility at date
   t is look-ahead bias. The eligible set may therefore change over time;
   monitoring reports changes.
3. **Threshold provenance.** Every threshold is classed as *logical*
   (mathematical necessity), *theoretical* (literature-derived), or
   *empirical* (calibrated under the protocol), with an evidence tag.
4. **Provisional status.** Until all its thresholds are established, a method
   is `PROVISIONAL`: it may enter empirical evaluation (step 3) but not
   deliberation or production.
5. **Pre-registration.** Thresholds and materiality margins are committed
   before the comparative results they govern are seen (P13).
6. **Overrides.** The owner may override an exclusion only in a research
   sandbox, logged; never in production.
7. **Transparency.** Every exclusion produces a user-visible record: the
   failing condition, measured value vs. threshold, threshold source and
   evidence tag, and what would make the method eligible.
8. **Continuous inputs.** Implementation-driven eligibility (minimum
   commission vs. position size, minimum order size, fractional-share
   availability, diversification feasibility) is derived from the **actual
   account value** and current Broker Registry facts — never from a size
   category (ADR-0007).

## 3. Eligibility contract — fields

| Group | Fields |
|---|---|
| Dimensional | min N; min effective sample T_eff; admissible range of q = N/T_eff; min N for asymptotic validity (separate from q); min cross-section per date |
| Data | frequency; min history per asset; OHLC vs. close; point-in-time fundamentals; market capitalisations; factor data; max missingness; ragged-history tolerance |
| Statistical | stationarity; moment/tail conditions; parameters vs. observations (identifiability); estimation-window type (affects T_eff) |
| Universe | asset-class mix; instrument types; need for a benchmark/market portfolio |
| Constraints | long-only / short / leverage / gross-net / cardinality compatibility; convexity |
| Implementation | liquidity; rebalancing cadence vs. signal half-life; minimum position vs. broker minimum order and fractional availability; instruments permitted in the selected accounts |
| Computation | solver class; runtime budget at actual N; conditioning |
| Dependencies | upstream methods/data required |
| Provenance | per threshold: source, evidence tag, date, owner |

Open framework question: hysteresis rules to prevent methods flickering in and
out of eligibility (RQ-21, decided at G4).

## 4. Worked example — RMT covariance cleaning (status: `OPEN`, RQ-14, S10)

What is established (`ESTABLISHED`, references to be checked before use in a decision):
- Under i.i.d. returns with finite moments and N, T → ∞ at fixed q = N/T, the
  eigenvalues of a pure-noise sample correlation matrix fill the
  Marchenko–Pastur band λ± = (1 ± √q)² (Marchenko & Pastur 1967; applied to
  financial correlations by Laloux et al. 1999).
- Cleaning estimators (eigenvalue clipping, rotationally invariant estimators,
  nonlinear shrinkage) are optimal in that large-dimensional limit.

Computed illustration (`VERIFIED-DERIVATION`, closed form, σ² = 1):

| N | T | q | Noise band [λ−, λ+] |
|---|---|---|---|
| 8 | 60 | 0.133 | [0.40, 1.86] |
| 8 | 1,260 | 0.006 | [0.85, 1.17] |
| 18 | 60 | 0.300 | [0.21, 2.40] |
| 50 | 60 | 0.833 | [0.01, 3.66] |
| 300 | 1,260 | 0.238 | [0.26, 2.21] |
| 300 | 252 | 1.19 | T < N: sample matrix singular |

Implication for the contract: **q alone is the wrong criterion.** q
(more precisely q_eff = N/T_eff) measures *how much noise* there is; N
measures whether the asymptotic machinery can *estimate* it (the estimators
work from the empirical distribution of N eigenvalues). At N = 8, T = 60
the noise band is wide, yet only 8 eigenvalues exist. The contract therefore
carries both a q range and a separate minimum N.

Not yet known (`OPEN`): finite-N performance relative to linear shrinkage;
effects of heavy tails, volatility clustering, and non-stationarity; the
effective T under EWMA/rolling windows; the economically meaningful margin.
Research design and threshold calibration: S10 (RQ-14). **No threshold is set.**
