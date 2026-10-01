# S2 — Configuration machinery (logical specification)

**Document status:** STABLE (accepted at G2, 2026-10-01, with owner amendments to O4, O6, O7) · **Basis:** ADR-0004, ADR-0005, ADR-0006, ADR-0009, ADR-0012, ADR-0013, ADR-0014; S1_INPUT_SPECIFICATION
**Decisions:** ADR-0015 … ADR-0018 (accepted) · **Decision list:** [S2_G2_DECISIONS.md](S2_G2_DECISIONS.md)
**Companions:** [S2_RISK_PREFERENCE_RESEARCH.md](S2_RISK_PREFERENCE_RESEARCH.md), [S2_SYNTHETIC_FIXTURES.md](S2_SYNTHETIC_FIXTURES.md)

**Scope rule.** This document specifies machinery capable of representing
later decisions. It makes none of them. Examples of investment constraints
show how they would be *represented*; no constraint is adopted here. The
specification is language-neutral: physical formats, storage, and
technology are S8 decisions.

---

## O1 — Logical schema model

### Entities

| Entity | Key contents | Mutability |
|---|---|---|
| `FieldSpec` | The 19 attributes of S1 §2, plus `spec_version`, `supports_ordered_alternatives` (O4), `semantic_hash` (O10) | Immutable per version |
| `OptionSet` / `OptionEntry` | See RQ-41 governance below | Entries change status only through governed events |
| `Profile` | `profile_id`, schema line, created | Metadata only |
| `DeclaredVersion` | `profile_id`, `version`, `parent`, `schema_version`, `field_values[]`, `created_at`, `content_hash` | **Immutable** |
| `FieldValue` | `field_id@spec_version`, `value` (typed), `origin` (S1 §4), `origin_provenance`, flags `dont_know` / `prefer_not_to_say` | Part of an immutable version |
| `StateSnapshot` (A′) | Per account: values, positions, lots, cash; import source; `content_hash` | Immutable per snapshot |
| `FactsSnapshot` / `MethodRegistrySnapshot` | References to B and C versions | Immutable |
| `EffectiveVersion` | Input hashes (Declared, State, Facts, Methods, resolver version); `resolution_records[]`; `content_hash` | Immutable |
| `ResolutionRecord` | `field_id`, `declared_ref`, `effective_value`, `outcome`, `alternative_used` (rank or none), `finding_refs[]` (O4) | Immutable |
| `FindingRecord` | Typed record (O4 record architecture): `finding_id`, `type`, `fields[]`, `goals[]`, `binding_sources[]`, `inputs` (`id@version`, incl. belief snapshot where relevant), `explanation`, `consequence`, `user_actions`, `status` (open / acknowledged / resolved / superseded), `first_seen_in` / `last_seen_in` (Effective versions) | Immutable per Effective version; lineage tracked across versions |
| `DerivationRecord` | `output_id`, `method_id@version`, typed `inputs[]` (each `id@version` with class), `parameters`, `output` (with units), `timestamp`, `content_hash` | Immutable |
| `AuthorityGrant` | See O6 | Versioned |
| `ChangeEvent` | Class (A / A′ / B / C / D / schema / authority), refs, timestamp | Append-only log |

**Identity.** Every immutable object is content-addressed (hash of
canonical content). References are always `id@version`. Nothing is updated
in place; change creates a new version linked to its parent.

### Typed values with explicit units

Every numeric value carries **unit**, **basis**, and where relevant
**period**, as data. This metadata is preserved through every derivation: a `DerivationRecord` records input and output units, and every conversion step.
- unit: e.g. NOK, %, count, years;
- basis: decimal (0.05) vs. percent (5);
- period: per year, per month, per trade.

This is required because model parameters such as γ change meaning under
unit and frequency changes (07 §5, VERIFIED-DERIVATION). Conversions are
explicit deterministic functions. Mixing incompatible units is a validation
error, never a silent coercion.

Value types: scalar · enum reference (`OptionEntry id@version`) · set ·
range · money (amount + currency) · rate (value + basis + period) · date ·
duration · repeating table (row schema) · free text · structured custom
specification (validated by the admitting method's schema).

## O2 — Validation and constraint representation (methodology-neutral)

Two layers share one representation:

1. **Field validation rules** on A values: type, range, unit, required-while-active, cross-field predicates.
2. **Constraint objects** on portfolios, positions, groups, accounts, or trade lists, used by the Feasibility Engine and construction methods.

### Constraint object

| Element | Content |
|---|---|
| `id`, `version` | Stable identity |
| `scope` | portfolio · account · position · group · trade list · time window |
| `subject` | Expression over declared variables (below) |
| `relation` | ≤ · ≥ · = · ∈ · ∉ · implies |
| `bound` | Constant (typed, with unit) · reference to an A field · reference to a D value |
| `hardness` | `hard` (must hold) · `soft` (penalty reference supplied by a method) · `trigger` (monitoring condition with pre-committed response) |
| `source` | Law/fact ID (B) · account/broker fact (B) · user field (A) · method contract (C) · system invariant |
| `applicability` | Conditions under which it applies (e.g. account type) |
| `convexity_class` | linear · convex · non-convex (e.g. cardinality) — read by eligibility (06 §3) |
| `provenance`, `status` | Who introduced it, when; active/retired |

### Expression vocabulary

| Family | Represents | Examples (illustrative only — none adopted) |
|---|---|---|
| Linear | Bounds, group sums, net exposure | `w_i ≥ 0` would express long-only; `Σ_{i∈G} w_i ≤ b` a group cap |
| Piecewise-linear | Gross exposure, turnover | `Σ|w_i| ≤ L` would express a gross-leverage limit; `Σ|w_i − w_i^pre| ≤ τ` a turnover limit |
| Cardinality | Number of non-zero positions | `#{i: w_i ≠ 0} ≤ K` (non-convex) |
| Membership | Eligibility sets | `i ∈ EligibleSet(account)` from registries |
| Logical | Implications, conjunctions | `w_i > 0 ⇒ account(i) ∈ {...}` |
| Named measure | Risk/cost measures defined elsewhere | `Measure(id@version)(w) ≤ x`, where the measure (e.g. an ex-ante volatility estimator) is a C method |

**Hard-constraint rule (07 §3, formalised).** `hardness = hard` is valid only
if the subject is a deterministic function of the proposed weights or trade
list and of versioned inputs at decision time. A constraint on a realised
future outcome is rejected as `hard` by validation. It may be `soft` (on an
ex-ante measure) or `trigger`.

**Neutrality.** The machinery adopts no investment constraint. Which
constraints apply comes from law and account facts (B), user fields (A), and
accepted methods (C) through their own stages.

## O3 — Declared → Effective resolution algorithm

**Inputs:** `DeclaredVersion` *v*, `StateSnapshot` *s*, `FactsSnapshot` *f*,
`MethodRegistrySnapshot` *m*, resolver version *r*.
**Output:** `EffectiveVersion` = hash(*v*, *s*, *f*, *m*, *r*) with a `ResolutionRecord` per field.

1. **Validate** each active field (O1/O2 rules) → `incomplete` or invalid → finding type I0 (validation).
2. **Activation**: compute the active set from field conditions and `required_profile_fields` of production methods; inactive → `not_applicable`.
3. **For each active field, in dependency order** (O5 graph):
   - a. Take the declared candidate list: the single value, or the ordered alternatives `[a₀, a₁, …]` if the FieldSpec has `supports_ordered_alternatives = true` (O4).
   - b. For candidate `a_k`, evaluate facts (*f*), methodology (*m*), and feasibility (*s*, *f*) → `accepted` · `narrowed` · `blocked` · `pending`.
   - c. If `a₀` is `accepted` or `narrowed`, use it. If `blocked`/`pending` and a later declared alternative is `accepted`/`narrowed`, use the first such; record `alternative_used = k`. Otherwise the field is `blocked`/`pending`.
   - d. Emit findings (O4 taxonomy) with binding sources.
4. **Cross-field analysis**: classify interactions per O4 (inconsistency / trade-off / multi-goal separation). Every classified interaction produces a typed `FindingRecord` (O4 record architecture). Only I1–I3 records are conflicts.
5. **Derive** D values with `DerivationRecord`s.
6. **Assemble** the `EffectiveVersion`.

**Invariants** (testable):
- (i) Resolution never modifies the Declared version (its hash is unchanged).
- (ii) No value enters Effective unless it was declared by the user (as the value or a declared alternative), comes from a registry, or is derived by an accepted method.
- (iii) Determinism: identical inputs give an identical Effective hash.
- (iv) The precedence (facts and feasibility → methodology → preferences) governs implementability only.

**Re-resolution triggers:** any change to *v*, *s*, *f*, *m*, or *r*. A
preserved declared value re-resolves without user re-entry.

## O4 — Interaction taxonomy, ordering policy, ordered alternatives

### Taxonomy (refines RQ-23)

| Type | Definition | Engine response | Ordering? |
|---|---|---|---|
| **I1 Logical inconsistency** | Two declarations cannot simultaneously be true or implemented (e.g. "keep holding X" and "exclude X's issuer") | `ConflictRecord`; both values preserved; user resolves | **No automatic ordering** |
| **I2 Hard-constraint conflict** | A preference conflicts with law, account, broker capability, or feasibility | `ConflictRecord`; `narrowed`/`blocked`; Declared preserved | Precedence of facts and feasibility (implementability only) |
| **I3 Methodological conflict** | No admissible method for a requested option | `ConflictRecord`; `pending`/`blocked`; Declared preserved; declared alternatives may apply | Precedence of admissibility (implementability only) |
| **T1 Competing objectives / trade-off** | Both declarations valid, implying different objectives (e.g. higher return target and lower volatility preference) | **Not a conflict.** A `TradeOffRecord` is kept in structured state and the audit trail, passed to construction and the report. **S2 does not resolve trade-offs**; the construction methodology does (S11) | **None** |
| **T2 Multi-goal separation** | Apparently conflicting requirements belong to different goals | No conflict. A `GoalRoutingRecord` (where routing is relevant) attaches requirements to their goals; separate portfolio units if `GOL.portfolio_mapping` permits | **None needed** |
| **F1 Objective infeasibility** | A declared objective cannot be attained within declared limits under current estimates (feasibility check on save) | `FeasibilityFinding`, versioned and attributable (goal, limits, belief snapshot, method version); the goal is **never modified**; reported, not auto-resolved | None; user informed |

### Record architecture

| Interaction | Record type | Conflict? | Persistence |
|---|---|---|---|
| I1, I2, I3 | `ConflictRecord` | Yes | Versioned; lineage across Effective versions |
| T1 | `TradeOffRecord` | No | Versioned; visible in state, report, audit trail |
| T2 | `GoalRoutingRecord` (where relevant) | No | Versioned |
| F1 | `FeasibilityFinding` | No | Versioned; attributable to its inputs; re-evaluated when inputs change; remains visible while it holds |

All are `FindingRecord` subtypes (O1). None of them modifies the Declared
Policy Statement.

**Classifier rule.** Classification is deterministic from field semantics.
When a pair cannot be classified with certainty (I1 vs. T1), it is
presented as a *possible inconsistency* for the user to confirm. It is
never silently ranked.

**Ordering policy (ADR-0016; research basis in S2_RISK_PREFERENCE_RESEARCH §4).**
1. Separate by goal first (T2).
2. Use explicit user priority where the user declared one (goal priority rank already exists; optional field-level priority).
3. Otherwise ask the user to resolve.

No system default ordering of valid objectives. A future default would
require its own ADR with evidence.

### Ordered alternatives (RQ-48) — mechanism only

- FieldSpec metadata `supports_ordered_alternatives` (true/false; default false for every field until set by that field's specification). When true, the value is an
  ordered list `[preferred, fallback₁, fallback₂, …]`. Each element must be
  independently valid.
- **An empty fallback list means there is no user-authorised substitute.**
  Undeclared alternatives are never inferred.
- Fallback applies only when the preferred option is `blocked` or `pending`,
  not when it is `narrowed`.
- The resolution record shows `alternative_used`. Declared stays unchanged.
- **Semantic requirements** for setting `supports_ordered_alternatives = true` (all must hold, and are checked when the field's option set and methodology are specified):
  - single-choice field;
  - options sourced from B or C, so availability can change outside the user's control;
  - the substitutes are economically distinct choices the user can meaningfully rank.
- **Which fields expose the mechanism is decided by the stage that researches each field's options and methodology**, not by G2. Candidate/example uses: `REB.approach` (S13b), `POL.currency_hedging` (S5), `POL.benchmark` (S7), `POL.allocation_unit` (S5). This is not a whitelist.
- A field with `supports_ordered_alternatives = false` resolves only its single declared value; it can never use another option.
- **Normally failing the requirements:** set-valued permissions (instruments, markets), numeric
  limits, personal facts.

## O5 — Dependency graph and incremental recomputation

**Nodes** are artefacts at the finest stable granularity, each with a
typed ID and version:
- A fields (per field, per goal/account where applicable);
- A′ items (per account, per position);
- B facts (per fact);
- C methods (per method version);
- Effective fields;
- D values;
- downstream artefacts: universe; comparison universe; estimates keyed by their declared inputs (e.g. covariance keyed by universe, window, estimator); horizon-specific beliefs keyed by (asset set, horizon); eligible sets; candidate portfolios per portfolio unit; target; trade lists per account; report sections; monitoring thresholds.

**Edges** are *declared reads*:
- field consumers (S1 §5);
- `required_profile_fields` and input declarations in method contracts (06 §5);
- report-section inputs.

**Cache key** of an artefact = hash(its method `id@version`, the versions of
all its declared inputs). An artefact is invalidated **iff** its key
changes. Recomputation proceeds over the dirty subgraph in topological
order; clean artefacts are reused.

**Gating:**
- Edges from A fields read **Effective** values, so a Declared change that leaves Effective unchanged dirties nothing downstream except the conflict panel and report.
- **Presentation-only fields** (e.g. `ENG.report_depth`) have edges only to report nodes and cannot reach estimates or portfolios.
- **Horizon fields** dirty only the horizon-specific belief nodes keyed by that horizon and their descendants. They do not touch registries, horizon-independent estimates, or other portfolio units.

**Static checks (graph validator):**
- An edge from a personal field to a node not listed in its `consumers` is rejected (purpose limitation, ADR-0014 §8).
- An edge from any preference field to a belief node is rejected (ADR-0009/0013), except horizon → horizon-keyed belief nodes and declared comparison-universe edges.
- Cycles are rejected.

**No "rerun everything" default.** An artefact whose method contract does
not declare its reads is **non-cacheable and flagged**. Its method is
treated as having an incomplete contract, which fails eligibility (06).
The engine does not fall back to recomputing the whole graph.

## O6 — Authority model (analysis vs. execution)

**Central invariant:** analytical authority ≠ decision authority ≠ execution authority. No execution-related authority becomes operational before the appropriate S13 safeguards and eligibility conditions exist.

The eight dimensions below are the **S2 logical representation** (and the basis for the fixtures). S8 and S13 may refine, split, or consolidate them where implementation, broker capabilities, security, or regulatory research require, provided the central invariant is preserved.

Authority is **grant-based**: no grant means no authority. Absence of a
grant is not a default value. Dimensions follow the information-processing
stages of Parasuraman, Sheridan & Wickens (2000) and are defined separately
so analytical discretion never implies permission to move money.

| # | Dimension | Stage (P/S/W 2000) | Notes |
|---|---|---|---|
| 1 | Analyse | Information acquisition and analysis | |
| 2 | Propose / recommend | Decision selection (advisory) | |
| 3 | Construct candidate portfolios | Decision selection | |
| 4 | Select among candidates | Decision selection | Only if eventually permitted (S12) |
| 5 | Generate trade list | Action selection | |
| 6 | Stage orders | Action implementation | Schema capability; inactive until S13 |
| 7 | Submit orders to a broker | Action implementation | Schema capability; inactive until S13; requires broker API capability (B) |
| 8 | Execute without per-trade confirmation | Action implementation | Schema capability; inactive until S13 safeguards |

**`AuthorityGrant`:** `dimension` · `scope` (profile/portfolio/account) ·
`limits` (typed constraint objects, O2, e.g. maximum trade value) ·
`confirmation_requirement` · `valid_from` / `valid_to` · `revocable`
(always true) · `granted_by` · `version`.

**Invariants:**
- A higher action-stage grant requires the lower ones it depends on (dimension 7 requires 5 and 6).
- Dimensions 6–8 cannot be granted until an accepted S13 safeguard specification exists.
- Agent permissions inside the engine (05 R4) are a separate, narrower layer and never exceed user grants.

**Not decided here:** the UI levels presented to users.
`GOV.autonomy` becomes a grouped view over these grants (S1 field revised in
G2 decision D2-07).

## O7 — Calibration interface (mechanism only)

A **calibration method** is a C method whose contract additionally declares:
- input ontology classes (S2_RISK_PREFERENCE_RESEARCH §1);
- target model and objective formulation;
- output parameters with unit, basis, period, and return frequency;
- validity conditions;
- dependence on belief snapshots, if any;
- recalibration triggers.

Every output is a D value with a `DerivationRecord`. **No calibration
mapping is adopted in S2.** Model-specific mappings are S11 (RQ-02d).

**Scope of model parameters.** A parameter such as γ has meaning only within
its specified formulation, units, and calibration context. It is stored as a
D value scoped to (model, formulation, calibration method `id@version`,
input snapshot). It is never stored as a portable attribute of the investor
or reused by another model.

**Two distinct uses (for S11, RQ-02d/RQ-50):**
- (a) *calibrating a model to the user*, which produces a parameter;
- (b) *selecting a portfolio from an efficient opportunity set by an interpretable user choice*, e.g. choosing among projected outcome profiles. This may avoid pretending that an economically precise γ has been measured.

The calibration interface supports both, and a selection-based method
records the chosen option, the opportunity set, and its belief snapshot.

## O10 — Schema evolution and historical interpretability (RQ-47)

| Change class | Example | Mechanism |
|---|---|---|
| Cosmetic | Label or help text | Spec revision; `semantic_hash` unchanged; no data change |
| Semantics-preserving rename/restructure | Field ID renamed, same meaning | New spec version with an explicit mapping flagged `semantics_preserving`. Migration **creates a new Declared version** with migration provenance. Old versions untouched |
| Option-set change | Option retired | Through option governance (below). Historical values stay valid as history and re-resolve now (`blocked`/`pending` with reason) |
| **Semantic change** | Meaning of a field changes materially | **New field ID** (or major version marked incompatible). No automatic migration; user prompted; old field retired, old values retained as history and never reinterpreted |

**Historical reconstruction.** Every `EffectiveVersion` records the schema
version, facts snapshot, method-registry snapshot, and resolver version, so
past decisions can be interpreted under the rules in force at the time. No
migration ever rewrites a past version.

## RQ-41 — Option-set governance (contents remain with S3–S5 and later)

`OptionEntry` = `id` (stable, never reused) · `label` · `status`
(`proposed` · `active` · `disabled` with reason · `retired`) ·
`provenance` (spec ADR | registry fact `id@version` | method `id@version`) ·
`effective_from` / `effective_to` · `applicability` conditions.

| Source type | Entry enters by | Leaves or disabled by |
|---|---|---|
| Static | Spec revision via ADR | Spec revision via ADR |
| Registry-driven (B) | Fact verified and recorded | Fact superseded, expired, or not applicable |
| Eligibility-driven (C) | Method becomes admissible | Method retired or ineligible for the context |

Per-profile disabling (facts or feasibility for that profile) is a
resolution outcome, not an option-set change. S2 populates **no** option
contents.
