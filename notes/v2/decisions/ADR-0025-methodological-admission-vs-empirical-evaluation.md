# ADR-0025 — Methodological admission is distinct from empirical evaluation

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-02 · **Date decided:** 2026-10-07
- **Decided by:** Owner (decision D-1, HANDOFF §6, confirmed 2026-10-07; principle set by OD-4, 2026-10-02) · **Gate:** — (owner confirmation before S4.1; reviewed at G4) · **Stage:** S4
- **Supersedes (in part):** ADR-0005 (meaning of ADMISSIBLE); 06 §1 step (3) and §2 rule 4 wording; 02 §D definitions of `ADMISSIBLE` and `PRODUCTION`
- **Resolves:** C-4 (S4 plan §B.1)
- **Spec commit / tag:** acceptance commit on `stage/s04-method-library` (see CHANGELOG 2026-10-07); gate tag at G4
- **Acceptance note:** accepted as proposed. The heading "Proposed decision" is retained so that the text is unchanged from the version the owner reviewed; it is the decision.

## Context — the conflict
The owner decided (OD-4, 2026-10-02):
- S4 determines whether a methodology is sufficiently specified and justified to enter the Method Library for its stated role.
- Favourable historical performance is **not** a prerequisite for methodological admission.
- S7 defines the empirical evaluation protocol; S15 validates the integrated system.
- The ANG PC architecture is **not** disabled merely because S7 has not yet happened.

The accepted texts say otherwise:
- **06 §1 (3) ADMISSIBLE:** "passed the pre-registered evaluation protocol vs. the simple control, net of the selected accounts' costs, FX and taxes".
- **06 §2 rule 4:** PROVISIONAL methods "may enter empirical evaluation (step 3) but not deliberation or production".
- **02 §D:** `ADMISSIBLE` = "Passed empirical evaluation against the control under the protocol"; `PRODUCTION` = "Admissible and enabled by an accepted ADR".

Under those definitions no method could be DELIBERABLE before S7 evidence exists. That directly contradicts OD-4. The accepted texts cannot be edited silently, so this ADR proposes the change.

## Proposed decision
1. **Funnel names preserved:** FEASIBLE → ELIGIBLE → ADMISSIBLE → DELIBERABLE.
2. **ADMISSIBLE redefined** as *methodologically admitted for its declared role*. That requires all of the following:
   - identifiable primary source;
   - sufficiently clear mathematical definition;
   - deterministic implementability;
   - verified reproduction of the implementation;
   - explicit inputs and assumptions;
   - defined role in the PC (or other) architecture;
   - an accepted Method Contract (ADR-0024);
   - plus FEASIBLE and ELIGIBLE in the point-in-time problem context.

   Admission is granted at G4 (or a later gate) by ADR or library manifest.
3. **Empirical evaluation status** becomes a **separate axis**: `UNEVALUATED → EVALUATED (protocol vN)`, produced under the S7 pre-registered protocol (including the simple-control comparison).
   - It informs CIO weighting/selection evidence, monitoring, and S15 validation.
   - It is **not** a precondition for admission or deliberation.
   - An attractive backtest never makes a method admissible.
4. **Two kinds of evidence kept apart:** methodological admission is distinct from CIO weighting/selection evidence.
5. **PROVISIONAL retained:** a method whose eligibility thresholds are not yet established (e.g. RMT before the S10 study) remains not deliberable (06 §2 rule 4 stays, minus its reference to step (3) as empirical).
6. **"Production validated"** is reserved for the integrated system after S15. Before that, outputs carry a "not production-validated" label. The architecture is not disabled.
7. **PRODUCTION** (02 §D) redefined as: admitted, deliberable in context, and enabled by an accepted ADR. Its empirical-evaluation status is displayed alongside.

## Alternatives
| Option | For | Against |
|---|---|---|
| Keep accepted definitions | No change | Contradicts OD-4; disables the ANG pipeline until S7 |
| **Split admission and evaluation (this ADR)** | Matches OD-4; keeps S7's role intact | Requires care that evaluation evidence still governs CIO weighting |
| Rename statuses entirely | Clean slate | Churn across S0–S3 documents |

## Consequences on acceptance
- 06 §1 and 02 §D are annotated (not rewritten) to point to this ADR.
- S4.21 implements the admission criteria.
- S7 defines the evaluation axis.
