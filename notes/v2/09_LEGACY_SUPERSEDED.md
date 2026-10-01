# 09 — Legacy Material: Superseded

**Document status:** STABLE (S0) · **Decision basis:** ADR-0001

## 1. Designation

The following material is **legacy**. It has **no authority** over the v2
framework, is not developed further, and is retained unmodified for
historical reference only.

| Material | Location | Version control |
|---|---|---|
| `SPECIFICATION.md` (ENGINE_V1 master specification) | repository root | Git (`4c9e82a`) |
| `MATHEMATICAL_APPENDIX.md` | repository root | Git (`4c9e82a`) |
| `notes/SPECIFICATION.md`, `notes/MATHEMATICAL_APPENDIX.md` (newer local edits not on GitHub) | local `ENGINE_V1/notes/` | none |
| `notes/ROADMAP.md`, `notes/STATUS.md` | local `ENGINE_V1/notes/` | none |
| `notes/covariance/`, `notes/shrinkage/`, `notes/momentum/` | local `ENGINE_V1/notes/` | none |
| ENGINE_V1 R code (`core/`, `signals/`, `operators/`, `solvers/`, `modules/`) | local `ENGINE_V1/` | none |

Every legacy `[CONFIRMED]`, `[DECIDED]`, `[VERIFIED]`, roadmap item, broker
assumption, model choice, and implementation decision is void in v2. Legacy
numerical values (commissions, rates, spreads, tax rates) may be used only
as `LEGACY-UNVERIFIED` research leads in S3.

## 2. What carries forward — and on what basis

Only method-neutral concepts that are **independently justified** in v2:

| Concept | Where in v2 | Independent justification |
|---|---|---|
| Separate evidence tags; explicit `OPEN` items | [02](02_EVIDENCE_AND_STATUS.md) (redesigned) | Auditability; legacy conflation corrected |
| Validation by independent reimplementation on seeded synthetic panels with quantified residuals | [04](04_REPRODUCIBILITY.md) §3 | Standard numerical verification practice |
| Reproducibility invariant (loop hash) | [04](04_REPRODUCIBILITY.md) §1 (generalised; code-hash defect corrected) | Required for any auditable decision system |
| Signal ⊥ risk estimation; construction ⊥ parameter selection; fail-small fallbacks | [00](00_CHARTER.md) P11–P12 | Attribution of performance; overfitting control; robustness |
| Plugin-registry pattern (method = registered, swappable unit) | Method Library, [06](06_MODEL_ELIGIBILITY_GOVERNANCE.md) | Composability; now extended with eligibility contracts |
| Formula mechanics: simple/log/excess returns, FX translation incl. quotation-direction check, drift-adjusted turnover, ex-post costs, standard performance measures | To be re-specified, with citations, in the stages that use them (S6, S7, S13) | Standard definitions; re-stated rather than imported so no legacy convention enters unexamined |

Candidate *methods* named in legacy material (e.g. EPO, GARCH-family,
DCC, RMT/RIE, Ledoit-Wolf shrinkage, momentum constructions, Gârleanu–Pedersen
dynamic trading) have no special standing: they may be registered in the
Method Library like any other candidate and must pass the same funnel.

## 3. Why superseded (recorded evidence)

Internal contradictions found in the legacy record, unresolved by any decision log:

| Topic | Earlier | Later |
|---|---|---|
| Data frequency | monthly ("locked") | daily |
| Momentum window | 12-1 skip-month ("locked") | no-skip [t−12, t] ("decided") |
| Geography | OSE-only primary | OSE + US merged |
| Currency | local primary | NOK unhedged ("confirmed") |
| Rebalancing band | percentage points (GitHub) | relative (local only) |
| Status tags | adopt only with out-of-sample evidence | GARCH/DCC "confirmed" without it |
| Tactical layer | — | asserted timing-only; not in repository |

Additionally: the repository specification cited sections (`§A.0–§A.4`) and
files that are not in the repository; GitHub and local copies diverged.

## 4. Not carried into the repository

`ENGINE_V1/notes/agentic-saa/self-driving-portfolio-review.md` (local; the
stage-1 knowledge base of the reference paper) is not part of v2 until the
owner has reviewed it; see CHANGELOG pending items.
