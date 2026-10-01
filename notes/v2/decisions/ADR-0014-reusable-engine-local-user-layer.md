# ADR-0014 — Reusable engine with a private local user layer; declared vs. effective Policy Statement

- **Status:** PROPOSED (principles instructed by the owner on 2026-10-01; to be accepted at G1)
- **Date proposed:** 2026-10-01 · **Date decided:** —
- **Decided by:** — · **Gate:** G1 · **Stage:** S1
- **Supersedes:** none · **Extends:** ADR-0006 (adds the local-workspace root and field metadata), ADR-0010 (derivation records); amends the 00_CHARTER scope/roles text — no accepted ADR body is modified
- **Resolves:** D-S1-1 (where personal answers are stored); opens RQ-39 … RQ-42

## Context
The engine is a reusable application that several people (the owner,
friends) run locally, each with a private profile. The owner's S1 answers
are one local test configuration, not engine defaults. The repository is
public.

## Decision
1. **Two layers.**
   - **System/public layer** (version-controlled, public): schemas and
     validation rules; available configuration options; methodological
     definitions; public facts registries (provenance, effective dates,
     staleness per 03); research and evidence; deterministic methods.
   - **Local user layer** (private, git-ignored, never pushed): Investor
     Profile; goals and horizons; risk preferences; liquidity needs; accounts
     and capital; universe preferences; instrument permissions; constraints
     and exclusions; engagement preferences; all other user-specific Policy
     Statement settings; user run history.
2. **Hierarchy root (extends ADR-0006).**
   Engine installation (system layer) → Local workspace → one or more User
   Profiles → each with an Investor Profile and Policy Statement(s) →
   Goal/Portfolio → Account. Nothing in one profile is visible to another
   profile or to the public repository.
3. **Declared vs. effective Policy Statement.**
   - **Declared** = the user's inputs as entered, versioned and immutable
     per version.
   - **Effective** = Declared ∩ public facts (registries) ∩ accepted
     methodology ∩ feasibility (Feasibility Engine, eligibility funnel).
   - Every difference between them is reported as a **conflict record**:
     field, user value, binding rule or fact and its source, consequence,
     and the user's available actions. Neither side is silently overridden.
   - Only the Effective Policy Statement drives the investment process.
4. **Field metadata (schema requirement for S2).** Every field declares:
   - **input nature**: factual investor input · user preference ·
     preliminary/research-dependent preference;
   - **editability**: user-editable · registry-sourced (read-only fact) ·
     methodology-defined (read-only rule) · system-derived (read-only,
     with derivation record);
   - **input type**: dropdown · multi-select · numeric · range · toggle ·
     repeating table · free text · system-derived display;
   - **option source**: static · registry-driven · eligibility-driven;
   - whether an advanced/custom value is permitted, and its validation;
   - Policy Statement decision category (07 §3).

   Every personal field offers "don't know" and "prefer not to say". No
   personal field is pre-filled. User answers never populate system defaults.
5. **Preferences cannot redefine facts or rules.** Tax rates, broker fees,
   regulatory rules, formulas, and verified market facts are not editable as
   preferences. They come only from registries or accepted methodology.
6. **Raw preference preserved (extends ADR-0010).** A preference requiring
   calibration is stored as given. Each derived model parameter carries a
   derivation record: method id and version, inputs (including the raw
   preference and the facts/estimates snapshot), output, timestamp. The
   derivation is reproducible from the record.
7. **Privacy boundary.** Personal data stays on the user's machine. Run
   manifests shared or committed reference profile *hashes*, never contents.
   Any flow of personal data to external services (e.g. hosted LLM
   providers) requires an explicit, minimised, user-approved policy (RQ-40);
   until that is decided, none is assumed.
8. **Jurisdiction scope.** Tax residence is a user input. Users resident in a
   jurisdiction the Tax Registry does not cover are reported as unsupported
   (a conflict record), not given Norwegian rules by default. Initial
   coverage target: Norway (RQ-42).

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Single-owner design (implicit before) | Simpler | Hard-codes one person's answers; not reusable; privacy risk in a public repo |
| Personal data in a private repository | Versioned | Excludes friends' local use; still centralises personal data |
| **Public system layer + private local workspaces** | Reusable; private by construction; facts shared and verifiable | Requires local storage, profile management, conflict reporting |

## Consequences
- S1 outputs an Investor Profile *schema* plus one local test profile.
- S2 must specify field metadata.
- S8 must specify local storage, multi-profile handling, and the
  conflict-explanation UI.
- `.gitignore` excludes `/local/`.

## Revisit trigger
A hosted or multi-tenant deployment is ever considered.
