# ADR-0014 — Reusable engine with a private local user layer; declared vs. effective Policy Statement

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (G1 approval, 2026-10-01) · **Gate:** G1 · **Stage:** S1
- **Supersedes:** none · **Extends:** ADR-0006 (local-workspace root, data classes, field metadata), ADR-0010 (derivation records), ADR-0012 typed contracts (`required_profile_fields`, parameter authority); amends the 00_CHARTER scope/roles text — no accepted ADR body is modified
- **Resolves:** D-S1-1 (where personal answers are stored); opens RQ-39 … RQ-47

## Context
The engine is a reusable application that several people (the owner,
friends) run locally, each with a private profile. User inputs change over
time and differ between users, so they are runtime configuration, not
project decisions. The repository is public.

## Decision
1. **Two layers.**
   - **System/public layer** (version-controlled, public): schemas and
     validation rules; available configuration options; methodological
     definitions; public facts registries (provenance, effective dates,
     staleness per 03); research and evidence; deterministic methods;
     synthetic fixtures.
   - **Local user layer** (private, git-ignored, never pushed): Investor
     Profile; Declared Policy Statements; Portfolio State; user run history.
2. **Hierarchy root (extends ADR-0006).** Engine installation (system layer)
   → Local workspace → one or more User Profiles → each with an Investor
   Profile and Policy Statement(s) → Goal/Portfolio → Account. Profiles are
   isolated from each other and from the public repository.
3. **Data classes.**
   - **A** runtime user configuration.
   - **A′** Portfolio State (holdings, cash, tax lots, account values) — separate from the Investor Profile and Policy Statement, with separate versioning.
   - **B** public facts (registries).
   - **C** methodological configuration (options only from admissible methods).
   - **D** derived values.
   - **E** synthetic test fixtures.

   User inputs (A) are runtime configuration: editable at any time, every save is a new immutable version, and no ADR is needed to change them. Any value crossing a class boundary carries provenance (D values name their A/A′ field versions, B fact IDs and snapshot, C method ID and version).
4. **Field metadata.** Every field declares the attributes of
   S1_INPUT_SPECIFICATION §2, including: nature (factual / preference /
   research-dependent); class; status; activation rule; purpose; exhaustive
   consumers; privacy class (P0–P3); necessity; control; options and option
   source (static / registry / eligibility / pending); custom permission;
   validation; dependencies; propagation tags; allowed value origins; pending
   research.

   4a. **Schema capability ≠ UI activation.** The schema may represent a
   field that the UI does not ask for. Activation comes only from a satisfied
   field condition or from an accepted production method whose eligibility
   contract lists the field in `required_profile_fields`. Fields are never
   collected because they might be useful someday.

   4b. **Value origins.** These are distinct and recorded:
   - `user_entered`;
   - `remembered` — the user's own saved value shown for editing; **not** a default;
   - `accepted_proposal` — a clearly labelled derived proposal the user confirmed, with provenance;
   - `technical_default` — allowed only for technical/methodological settings, never for personal facts or preferences;
   - `imported` (A′), `registry` (B), `derived` (D).

   No personal field is silently preselected. Every personal field offers
   "don't know" and "prefer not to say". Real profiles never become system
   defaults, fixtures, or research evidence.
5. **Declared vs. effective Policy Statement.**
   - **Declared** = the user's A inputs, versioned and immutable per version.
   - **Effective** = the result of the resolution rules (S1_INPUT_SPECIFICATION §7.1). Precedence: B facts and hard feasibility > C admissibility > A preferences.
   - **The precedence governs implementability only, not authority over preferences.** The Declared Policy Statement is preserved exactly. Facts, constraints, feasibility, and methodology may block, narrow, or make a preference pending in Effective; they never rewrite or substitute the declared value. Alternatives are used only if the user declared them.
   - Every difference produces a conflict record. Neither side is silently overridden, Effective is never edited directly, and only Effective drives the investment process.
   - Downstream invalidation follows the **Effective** diff.
   - Portfolio State changes never alter A values or preference-derived calibration.
6. **Preferences cannot redefine facts or rules.** Tax rates, broker fees,
   regulatory rules, formulas, and verified market facts come only from
   registries or accepted methodology. Methodological options (C) come only
   from admissible methods. A user-set method parameter is allowed only
   where the admitting method's contract marks it user-settable, within the
   stated bounds (parameter authority).
7. **Raw preference preserved (extends ADR-0010).** Preferences requiring
   calibration are stored as given. Derived parameters carry derivation
   records reproducible from the record.
8. **Purpose limitation for personal data.**
   - Every personal-data field declares its decision purpose, exhaustive permitted consumers, and necessity.
   - A field with no decision purpose is not collected.
   - Information collected for one purpose must not silently affect unrelated decisions. A new consumer or purpose requires an ADR.
   - Example: year of birth may inform horizon and goal validation, human capital, or risk capacity, but never becomes an investment signal or alters market beliefs (extends ADR-0009 to factual personal inputs).
   - The Feasibility Engine and agents receive only the fields their declared purpose permits.
9. **Privacy boundary.** Personal data stays on the user's machine. Shared or
   committed run manifests reference profile *hashes*, never contents.
   Flows to external services (e.g. hosted LLM providers) are limited to
   fields whose declared purpose requires that service, and require an
   explicit, minimised, user-approved policy (RQ-40). Until that is decided,
   none is assumed.
10. **Jurisdiction scope.** Users resident in a jurisdiction the Tax Registry
   does not cover are reported as unsupported (a conflict record), never
   given another jurisdiction's rules by default (RQ-42).
11. **Portability.** Profiles must not be assumed to exist only inside one
   installation. A versioned export/import artefact is a required future
   capability, subject to S8 privacy/security decisions (RQ-43).

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Single-owner design (implicit before) | Simpler | Hard-codes one person's answers; not reusable; privacy risk in a public repo |
| Personal data in a private repository | Versioned | Excludes friends' local use; centralises personal data |
| **Public system layer + private local workspaces** | Reusable; private by construction; facts shared and verifiable | Requires local storage, profile management, conflict reporting |

## Consequences
- S1 delivers a reusable input specification, interaction model, resolution and propagation rules, and **synthetic** fixtures. No real profile is required for G1.
- Any real profile is optional private development data and is never a fixture.
- S2 formalises the schema, validation engine, ordering, and dependency graph.
- Method contracts (06 §5) gain `required_profile_fields` and parameter-authority fields.
- S8 specifies local storage, multi-profile handling, portability, and the conflict UI.
- `.gitignore` excludes `/local/`.

## Revisit trigger
A hosted or multi-tenant deployment is ever considered.
