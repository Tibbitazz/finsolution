# ADR-0024 — S4 method governance: research lane, revisions, parameter authority, allocation domains, dual contracts

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-02 · **Date decided:** 2026-10-02
- **Decided by:** Owner (S4 plan approval: OD-2, OD-3, OD-5, OD-7 and corrections 3, 6–10, 2026-10-02) · **Gate:** — (owner decision; reviewed at G4) · **Stage:** S4
- **Supersedes:** none · **Extends:** ADR-0005, ADR-0012, ADR-0015, ADR-0023
- **Resolves:** C-2, C-3 (S4 plan §B.1); ANG-20, ANG-21

## Decision
1. **Research-candidate lane (OD-2).** Researcher-discovered methods move through:

   `DISCOVERED → RESEARCH CANDIDATE → SPECIFIED → VERIFIED → ADMISSIBILITY REVIEW → ADMITTED`

   - A research candidate may run experimentally and take part in research-oriented peer review.
   - It receives **no production CIO allocation** until ADMITTED through the gate process.
   - ANG's same-run participation of a discovered method (maximum entropy, March 2026) is deliberately not adopted for production. This is a governance adaptation of ANG.
2. **Revisions (OD-3).** A PC-agent revision may only:
   1. correct a genuine implementation error identified in review;
   2. revise its qualitative rationale;
   3. acknowledge or respond to CRO/peer criticism;
   4. re-run deterministic computation where an input was erroneous;
   5. re-run under an alternative or sensitivity explicitly authorised by the method contract;
   6. change a methodological parameter only where the parameter authority explicitly allows the PC agent to.

   **Constraints on every revision:**
   - An LLM never edits portfolio weights.
   - Parameters are never tuned opportunistically to win peer approval.
   - Every revised deterministic run records its reason, its trigger (review ID), and the before/after inputs.
3. **Parameter-authority classes.** Every Method Contract classifies each parameter as one of:
   - **fixed**;
   - **system-estimated** (by an accepted upstream method);
   - **user-authorized** (from the Policy Statement, within declared bounds);
   - **agent-selectable** (within contract bounds);
   - **sensitivity-only** (may be varied for diagnostics, never for the proposal).
4. **Allocation domain (OD-7).**
   - Every Method Contract declares the allocation domains it supports: asset class · fund/ETF · individual security · strategy/sleeve · portfolio of portfolios.
   - A method is not valid at a level merely because its mathematics can be evaluated there.
   - Contracts never assume ANG's 18-asset-class universe. S5 sets the feasible universe and allocation unit.
5. **Dual contract (correction 10).** Every Method Contract has:
   - **(a) a machine/computational contract**: inputs, outputs, units, parameters, constraints, data requirements, determinism;
   - **(b) an agent-readable methodological contract**: objective; economic intuition; assumptions; inputs used; inputs deliberately not used; expected-return dependence; risk-model dependence; constraints; known sensitivities; known failure modes; interpretation of the weights; valid comparison dimensions; invalid comparisons; source provenance.
6. **Heterogeneous inputs.** Contracts must not force methods through a common expected-return interface (heuristic, μ+Σ, Σ-only, distribution/path/factor, agentic).
7. **EPO hierarchy (correction 3), current scope.**
   - `MVO → EPO framework → Simple EPO → Anchored EPO`, with the exact mathematical relationships established from Pedersen, Babu & Levine (2021) in S4.7.
   - EPO belongs to the return-optimised / MVO lineage, not to a separate philosophical family.
   - UEPO, SEPO and DEPO are excluded and are not recreated through aliases.
8. **Verification area (OD-5).**
   - `notes/v2/research/s4/verification/` holds Python reference implementations for equation verification, source reproduction, limiting cases, synthetic examples, invariants, reference outputs and numerical comparison.
   - It is separate from production application code.
   - Current package availability (e.g. cvxpy absent) is never an architectural reason to avoid a method. The developer chooses the production implementation after receiving the contracts.

## Consequences
- S4.20 contracts carry parameter classes, allocation domains and both contract parts.
- S12 implements the revision rules.
- The Researcher lane needs a candidate registry (S8).

## Revisit trigger
S12 deliberation design shows the revision categories are insufficient or too permissive.
