# S4 verification area

**Document status:** STABLE (established at S4.0, 2026-10-02) · **Basis:** ADR-0024 §8 (OD-5)

**Contents:** mathematical verification and reference implementations for S4 only:
- equation verification;
- source reproduction;
- limiting-case tests;
- synthetic examples;
- invariants;
- reference outputs;
- numerical comparison.

**Rules:**
- **Not production code.** The developer chooses the production implementation after receiving the Method Contracts (S4.20). Reference outputs here serve as test oracles.
- **Language:** Python (numpy/scipy). The packages available today do not determine the production architecture. A method that needs convex optimisation is not avoided because a solver is not installed here.
- **Synthetic data only.** No personal data, ever.
- **No performance-driven selection.** Results here verify that a method matches its mathematical specification. They never rank methods (performance evaluation belongs to S7).
- **Empty at S4.0.** Code is added from S4.5 onward.
