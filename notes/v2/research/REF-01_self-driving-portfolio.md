# REF-01 — Reference paper: *The Self-Driving Portfolio* (Ang, Azimbayev & Kim)

**Document status:** STABLE (research memo) · **Stage:** S0 · **Created:** 2026-10-01

**Source of record:** Ang, A., N. Azimbayev, and A. Kim, "The Self-Driving
Portfolio: Agentic Architecture for Institutional Asset Management,"
**version dated September 21, 2026**, 40 PDF pages (30 text pages +
bibliography + Appendix A.1–A.2). Read in full; diagram exhibits rendered and
inspected. Page numbers below are the printed page numbers. The paper contains
**no numbered equations**.

**Role in v2:** architectural reference only — not a source of methodological
defaults (00_CHARTER §1, ADR-0001). Tags follow 02_EVIDENCE_AND_STATUS.

---

## 1. Purpose and claims

- Problem: the binding constraint in institutional asset management is human
  bandwidth, not data or models (p. 1). Contribution "is conceptual": redesign
  strategic asset allocation (SAA) as an end-to-end agentic workflow governed by
  the investment policy statement (pp. 1–2).
- Explicitly not claimed: that the agentic process performs better — "a
  different question" (p. 2), answerable only by live performance (§7).

## 2. Architecture (§3, Exhibits 1–5, Appendix)

| Component | What the paper specifies | Unspecified |
|---|---|---|
| Investment policy statement (human) | Universe of 18 ETF-investable asset classes; CPI+3–4% real target; 8–12% vol band; −25% max drawdown; ≤6% ex-ante TE vs. 60/40. Hard: universe, TE. Soft: return, vol, drawdown — breaches flagged in board memo (§4.1, §5.5) | Full text, format |
| Macro agent | Data + web search; weighted scores on growth, inflation, policy, financial conditions → one of four regimes with confidence (p. 7) | Indicators, weights, thresholds |
| 18 asset-class agents | Six return methods + confidence-weighted auto-blend; LLM-as-judge selects/blends, final estimate constrained to [min, max] of methods (§3.2, Exh. A.2) | Non-equity method sets; confidence scoring |
| Covariance agent | "historical data and macro forecasts" (p. 6) | Estimator entirely |
| 21 portfolio-construction agents | 19 fixed methods (Exh. 3: heuristic, return-optimised, risk-structured, non-traditional) + researcher (proposes a method not in registry; max entropy in the run) + adversarial diversifier (maximise tracking variance vs. centroid of other 20, Sharpe ≥ 75% of max-Sharpe) (§3.3) | Constraints per method; solvers |
| Strategy review | CRO risk report (non-voting); each agent reviews 2 peers (1 same, 1 other category), seeded, 42 reviews; modified Borda (5,4,3,2,1; −2 bottom flag); blend with metric composite via regime-dependent weight; top-5 must span ≥3 of 5 families; top-5 revise (§3.4) | Blend schedule; metric weights |
| CIO agent | LLM-as-judge chooses a method or one of 7 ensembles (simple average, inverse-TE, backtest-Sharpe, meta-optimisation, regime-conditional, composite-score, trimmed mean); board memo (§3.5) | Ensemble definitions; selection rule |
| Meta agent (§6.2 only) | Compares past estimates with realised returns over rolling 3 years (regime accuracy, rank correlation, hit rates, per-method error); edits prompts, skills, Python; human approval above a materiality threshold; IPS files excluded | Threshold; decision rule; **no results reported** |
| Agent anatomy (App. A.1) | Description (markdown), scripts (all computation), skills (shared methodology + scripts), output contract (JSON + markdown) | — |

Agent count: stated 44 (abstract, §7), never enumerated; named roles give
1+18+1+21+1+1 = 43, plus the meta agent = 44 (`ASSUMED` reconciliation).

## 3. Illustrative run (§4) — what it does and does not show

One stochastic realisation "at March 2026", explicitly "not a backtest" and
"not evidence of outperformance" (pp. 2, 14, 22).

| Result | Value | Internal check |
|---|---|---|
| Regime | Late-cycle, stagflationary risk (label outside the 4-class scheme) | — |
| CMA judge (Exh. 6) | Custom blends; markdowns −2.0 (US Growth) … 0.0 (US Small Cap) | Deltas and [min,max] constraint consistent; survey column missing from table (`VERIFIED-DERIVATION`) |
| Votes (Exh. 7) | Max diversification 1st … adversarial last (−36) | Totals = 21 × (15 − 2); 18 + 3 bottom flags (`VERIFIED-DERIVATION`) |
| Composite (Exh. 7) | 0.4 · vote + 0.6 · metric | Reproduced to ±0.001 with **min–max normalisation** within the run (`VERIFIED-DERIVATION`) |
| Ensemble (Exh. 8) | Inverse-TE chosen; market-cap 11.1% largest, max-diversification (vote rank 1) 3.1% | Weights sum to 100%; the vote barely influences weights |
| Final portfolio (Exh. 9) | Equity 44.9 / FI 41.7 / cash 8.1 / real 5.1; E[r] 6.87%, vol 7.54% (below 8% soft floor), backtested Sharpe 0.43, TE 2.41% | Subtotals reproduce; equity carries 83.3% of risk |
| "Effective number of assets 11.2" (Meucci 2009) | — | Reproduces exactly as **1/HHI of weights**, not Meucci's risk-based measure (`VERIFIED-DERIVATION`) |
| Static simulation 1996–2026 | Max DD −25.6% vs. −34.3% (60/40); authors: "largely mechanical" | Data/proxies/rebalancing unspecified |

Asserted without evidence shown: valuation skepticism "emerges" rather than
being prompted (though Exh. A.2's judge rules prompt it); no permanent bearish
tilt in other runs (fn. 7); leakage mitigation effective ("proprietary
techniques"); runs complete "in minutes".

## 4. Limitations stated by the authors (§5)

Look-ahead bias at the LLM layer even when quantitative components are
properly backtested (§5.1); non-reproducibility at temperature zero; LLM
monoculture / correlated errors — "the risk most likely to concern a CIO"
(§5.2); model/version drift (§5.3); automation surprise (§5.4); security of
tool-using, file-modifying agents (§5.6).

## 5. Internal inconsistencies noted

Exh. 4 "vote for two proposals" vs. top-5 ballot in text; "surviving
proposals" vs. all 21 receiving ensemble weight; regime label outside scheme;
Exh. A.1 "correlations vs 12 other asset classes" in an 18-class universe;
Exh. A.2 has no rule for the recovery regime; Exh. 1 shows CMAs as an input;
1/HHI reported as Meucci's measure; p. 3 cites Du et al. (2023) for a
crowd-forecasting claim that does not match that paper as understood here
(`ASSUMED`, citation not re-checked).

## 6. Version differences: April 1, 2026 draft → September 21, 2026 (`VERIFIED-SOURCE`, both PDFs compared 2026-10-01)

An earlier local review (legacy, `ENGINE_V1/notes/agentic-saa/`) was written
against the **April 1, 2026 draft** (32 pp., no appendix; `~/Downloads`). It
represents that draft accurately but is not the source of record.

| Item | April 1 draft | September 21 version |
|---|---|---|
| Agents / methods | "approximately 50" / "over 20" | 44 / 21 |
| Shortlist diversity | ≥3 of **4** families | ≥3 of **5** families |
| Tail-risk parity source | Spinu (2013) | Boudt, Carl & Peterson (2013) |
| TPA name | Total Portfolio **Allocation** | Total Portfolio **Approach** |
| Backtest statistic | Sharpe 0.39 vs. 0.41 for 60/40 | Backtested Sharpe 0.43; ENA 11.2; drawdown comparison emphasised |
| Look-ahead remedy | "only correct solution" is point-in-time LLMs; "lookahead bias is unavoidable" | Mitigation by retrieval, homogenisation, obfuscation, "proprietary techniques"; no claim of elimination |
| Policy bounds | — | Explicit hard/soft distinction |
| Appendix (agent anatomy, skill files) | absent | present |

## 7. Research arguments carried forward from the legacy review

Version-independent arguments from the legacy review, re-tagged and assigned
to v2 research questions. Its ENGINE_V1-specific content (R implementation
status, legacy roadmap phases, references to unrecorded prior analyses) and
its verdict to omit the agentic layer are **not** carried forward; that
verdict conflicts with accepted ADR-0004 and survives here only as a contested
position under RQ-16.

| Argument | Tag | Assigned to |
|---|---|---|
| The paper's economic premise (human bandwidth) is weak for a single personal investor; deterministic code already runs many methods at zero marginal attention cost. Agent value must therefore come from judgement, not throughput | `CONTESTED` | RQ-16, P7 (permanent simple control), RQ-26 |
| LLM components contaminate historical evaluation; the authors themselves concede it | `VERIFIED-SOURCE` (both versions) | Already addressed by R2 deterministic-only mode; RQ-09, RQ-26 |
| A self-modifying meta agent conflicts with reproducibility unless changes are versioned, shadow-tested, and approved | `ASSUMED` (design argument) | RQ-22, 04_REPRODUCIBILITY |
| The adversarial diversifier and maximum-entropy methods require no LLM and can be implemented deterministically (the former is a non-convex maximisation) | `VERIFIED-DERIVATION` (formulation) | RQ-15 candidates via typed contracts |
| A rules-based (deterministic) CMA judge is implementable and is the natural R2 fallback for the paper's LLM judge | `ASSUMED` | RQ-12 |
| The meta agent's "cross-sectional rank correlation of expected returns" is a rank information coefficient — a standard forecast-evaluation quantity | `ESTABLISHED` (definition) | RQ-22, S17 |
| Volatility targeting is listed as a construction method but is a sizing overlay | `ASSUMED` | RQ-15 |
| A 1996–2026 history for 18 ETF-investable classes requires index proxies; several ETF categories post-date 1996 | `ASSUMED` (not checked per class) | RQ-08 |

## 8. What v2 takes from the paper (as reference, not default)

The IPS-as-governing-document idea (→ Policy Statement, ADR-0008); code for
computation / LLM for judgement (→ ADR-0004, strengthened with fallbacks);
agent anatomy (→ 05 §3, proposed); bounded LLM judgement (the [min, max]
constraint, generalised as R1); structured deliberation and adversarial
proposals (→ RQ-16, evaluated against a deterministic control); a forecast
feedback loop with human approval (→ S17). Everything methodological in the
paper is a candidate subject to the eligibility funnel (ADR-0005).
