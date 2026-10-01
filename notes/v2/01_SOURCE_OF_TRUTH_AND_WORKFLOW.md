# 01 — Source of Truth and Git Workflow

**Document status:** STABLE (S0) · **Decision basis:** ADR-0001, ADR-0002

## 1. Should the documents be living, or committed only when complete?

**Living, version-controlled documents — committed at every decision gate.**
There is no technical or methodological reason to wait, and two reasons not to:

1. **Pre-registration requires early commits.** The strongest defence against
   evaluation-shopping is to fix the evaluation protocol, eligibility
   thresholds, and materiality margins *before* results exist. A Git commit
   hash with a timestamp is the evidence that this happened (P13). Waiting
   until the framework is complete would destroy that evidence.
2. **The developer needs the current authoritative state**, and the history of
   *why* it changed — which the legacy material lacked (it reversed decisions
   without a record; see [09](09_LEGACY_SUPERSEDED.md) §3).

Living documents carry one real risk: a developer building against something
that later changes. It is controlled by the status rules below, not by
withholding documents.

## 2. Authority hierarchy

1. `main` branch, `notes/v2/` — authoritative.
2. Within it: `ACCEPTED` ADRs > `STABLE` documents > `DRAFT` documents.
3. Open branches and pull requests — proposals, not authority.
4. Legacy material (repository-root specs, local `ENGINE_V1/notes/`) — **no authority**.
5. Local, non-version-controlled files — never authoritative, whatever their content.

## 3. Workflow per stage

```
Research ──► Decision gate ──► ADR (PROPOSED → ACCEPTED) ──► Documentation update ──► Commit ──► Merge ──► Tag ──► Next stage
```

| Step | Mechanism |
|---|---|
| Research | Branch `stage/sNN-<slug>` from `main`. Research memos in `research/`; draft ADRs with status `PROPOSED`. |
| Decision gate | Pull request titled `[GNN] <decision>`. The PR description lists the decisions requested, options, recommendation, and evidence. The owner reviews. |
| ADR | On approval, ADR status → `ACCEPTED` with date and approver; superseded ADRs get `SUPERSEDED by ADR-XXXX` (their bodies are not edited). |
| Documentation update | Affected documents updated in the **same** PR as the ADR, so code-facing docs and decisions never diverge on `main`. |
| Commit | Convention below. |
| Merge | Owner merges to `main`. Only the owner merges gate PRs. |
| Tag | Annotated tag `gate-GNN` on the merge commit, so the developer can pin a specification version. |

Small corrections that change no decision (typos, broken links, clarifications
that do not alter meaning) may be committed without an ADR, but still via PR
and recorded in [CHANGELOG.md](CHANGELOG.md).

## 4. Immutability rules

- **ADRs are append-only.** After acceptance, only the status line and
  `Superseded by` link may change. A changed decision is a new ADR.
- **Facts are append-only versions** ([03](03_FACTS_REGISTRY_POLICY.md)).
- **Pre-registered artefacts** (evaluation protocols, thresholds, margins) are
  never edited after results are produced; a revision is a new, dated version
  with the reason recorded, and results produced under the old version remain
  attributed to it.

## 5. Document status labels

Every document starts with `Document status:` one of `DRAFT`, `UNDER REVIEW`,
`STABLE`, `SUPERSEDED`. A STABLE document may still contain sections marked
`OPEN`; the developer must not implement those sections.

## 6. Commit message convention

```
[S<stage>][<ADR-or-RQ ids>] <imperative summary>

<what changed and why, one paragraph>
```

Example: `[S0][ADR-0001..0011] Establish v2 governance framework`.

## 7. Developer interface

- Build only against `ACCEPTED` ADRs and `STABLE` sections (README binding rule).
- Raise ambiguities as GitHub issues labelled `spec-question`, referencing the
  document section; the answer becomes a documentation change or a new ADR.
- Implementation detail that introduces no financial/methodological
  assumption is the developer's call and needs no ADR.

## 8. Current state of version control

- Repository: `github.com/Tibbitazz/finsolution`, default branch `main`.
- `ENGINE_V1/` (local R code and notes) is **not** a Git repository and is
  therefore not part of the source of truth.
- S0 is prepared on branch `stage/s0-governance` and is pushed and merged only
  on owner approval at gate G0.
