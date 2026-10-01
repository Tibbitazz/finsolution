# 04 — Reproducibility and Versioning Standard

**Document status:** STABLE (S0) · **Decision basis:** ADR-0001, ADR-0002

## 1. Run manifest

Every run (backtest, live recommendation, what-if, evaluation) writes a
manifest. Its hash is the **run ID**.

| Component | Identifier |
|---|---|
| Market data | Data snapshot ID (content hash) |
| External facts | Facts snapshot ID ([03](03_FACTS_REGISTRY_POLICY.md)) |
| Policy Statement | Policy Statement version |
| Specification | Git commit of `notes/v2` / gate tag |
| Code | Git commit hash of **all** code, including every method's source |
| Method Library | Library version + eligibility-contract versions |
| Eligibility result | Hash of the eligible/excluded set and exclusion report |
| LLM layer | Provider, model identifier and version, sampling parameters, seeds where supported, prompt/skill/description file hashes |
| Randomness | All random seeds (e.g. peer-review pairing, simulation) |
| Environment | Dependency lockfile hash, runtime version |

**Correction of a known legacy defect.** The legacy cache key covered
configuration but not solver source, so changing a formula silently reloaded
stale results. In v2, every cache key includes the code commit hash; a cache
hit with a different code hash is impossible by construction.

## 2. Two reproducibility classes

| Layer | Requirement |
|---|---|
| **Deterministic** (data processing, estimation, optimisation, eligibility, costs, metrics) | Bit-identical on the same environment. Across environments, results must agree within a tolerance stated per computation; the tolerance is part of the specification. |
| **Agentic** (LLM outputs) | Not bit-reproducible in general, even at temperature zero (non-determinism of hosted inference is documented; source to be cited at S8). Requirement: every agent output is archived, and a **replay mode** re-runs everything downstream deterministically from archived agent outputs. |

## 3. Validation standard for new components

Retained from legacy practice because independently sound:
1. Reimplement the component independently (or derive a closed-form special case).
2. Compare on a seeded synthetic panel and, where available, a real-data fixture.
3. Report the residual quantitatively and attribute it (e.g. to a stated
   numerical ridge term). "Looks right" is not validation.
4. Boundary/identity checks wherever theory provides them.

## 4. Document versioning

Specification versions are Git commits; gate versions are tags `gate-GNN`.
Results reference the specification commit they were produced under.
