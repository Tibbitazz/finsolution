# 02 — Evidence and Status Taxonomy

**Document status:** STABLE (S0) · **Decision basis:** ADR-0003

## Why separate vocabularies

The legacy material used one tag set for different things — `[CONFIRMED]`
meant "decided", not "verified", so methods were tagged confirmed without the
out-of-sample evidence its own principles required. v2 uses **five separate
vocabularies**, one per object type. A tag from one vocabulary is never used
for another.

## A. Evidence tags — for claims

| Tag | Meaning | Must accompany it |
|---|---|---|
| `VERIFIED-SOURCE` | Checked against a primary/authoritative source in this project | Citation (with page/section/equation or URL), date checked |
| `VERIFIED-DERIVATION` | Proven or computed mathematically, reproducibly | The derivation or the script, inline or linked |
| `VERIFIED-EMPIRICAL` | Shown on data under the pre-registered evaluation protocol | Run manifest ID, protocol version |
| `ESTABLISHED` | Standard textbook result, not re-derived here | A citation that has itself been checked (`VERIFIED-SOURCE` on the reference) before the claim is used in a decision |
| `CONTESTED` | Credible sources disagree | Both sides, cited |
| `ASSUMED` | Working assumption, not tested | Why it is plausible; what would falsify it |
| `OPEN` | Unknown | Assigned research question (RQ-id) |
| `LEGACY-UNVERIFIED` | Appeared in legacy material; not re-verified in v2 | Treated as `OPEN`; never used as an input |

**Citation rule.** A reference may be cited as support only if its existence
and the cited content have been checked. Unchecked references may be listed as
*candidate sources* and must be labelled so.

**Significance rule.** Statistical significance, economic significance, and
causal interpretation are reported separately and never inferred from one
another.

## B. Decision status — for ADRs

`PROPOSED` → `ACCEPTED` → (`SUPERSEDED` | `DEPRECATED`); or `PROPOSED` → `REJECTED`.
Only the owner moves a decision to `ACCEPTED` or `REJECTED`.

## C. Research-question status — for RQs

`OPEN` → `IN-RESEARCH` → `AT-GATE` → `RESOLVED` (links the ADR) | `DEFERRED` (with reason and revisit trigger).

## D. Method lifecycle — for methods in the Method Library

| Status | Meaning |
|---|---|
| `REGISTERED` | In the library with an eligibility contract |
| `PROVISIONAL` | One or more contract thresholds not yet established; may enter empirical evaluation only |
| `INFEASIBLE` / `INELIGIBLE` | Excluded **for a given problem context** (context-specific, recomputed point-in-time) |
| `ELIGIBLE` | Passes feasibility and eligibility for the context |
| `ADMISSIBLE` | Passed empirical evaluation against the control under the protocol |
| `PRODUCTION` | Admissible and enabled by an accepted ADR |
| `RETIRED` | Removed by ADR; history retained |

## E. Fact status — for registry facts

`VERIFIED` · `LEGACY-UNVERIFIED` · `ASSUMED` · `OPEN` · `EXPIRED` (past `reverify_by`).
See [03](03_FACTS_REGISTRY_POLICY.md).
