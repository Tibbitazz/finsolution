# ADR-0006 — Configuration hierarchy and versioned external-facts registries

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (design session 2026-10-01) · **Gate:** G0 (structure); field contents at G2 · **Stage:** S0
- **Supersedes:** legacy implicit single-broker assumption · **Resolves:** none

## Context
Costs, available instruments, tax treatment, FX, and execution differ by
jurisdiction, wrapper, instrument, and broker; the same theoretical portfolio
may be suboptimal or unimplementable under a different account setup.

## Decision
1. Configuration hierarchy: Investor → Goal/Portfolio(s) → Account(s);
   plus Methodological (eligible menu only) and System-governance levels
   (07_POLICY_STATEMENT_GOVERNANCE.md §2).
2. Facts live in four versioned registries — Jurisdiction & Tax, Wrapper,
   Instrument Master, Broker — referenced by configuration, never entered as
   parameters (03_FACTS_REGISTRY_POLICY.md).
3. Tax outcome = f(residence law, instrument, wrapper); brokers implement
   wrappers but do not determine tax.
4. Precedence: permitted instruments = law ∩ wrapper ∩ broker ∩ preference;
   account-level infeasibility overrides portfolio-level wishes, visibly.
5. Multiple accounts and brokers are supported in the data model (holdings
   and tax lots at account level; targets at portfolio level; an
   asset-location mapping between). Broker-routing optimisation is out of
   scope now but must remain possible without redesign.
6. Broker and account nodes are part of the artifact dependency graph; all
   performance is evaluated net of the selected configuration.
7. Hard constraints are deterministic predicates on weights/trades; realised
   outcomes are soft targets or monitoring triggers.

## Consequences
Registry research (S3) precedes universe (S5) and evaluation (S7); what-if
runs across account configurations become possible.

## Revisit trigger
If a jurisdiction/wrapper/broker case cannot be represented.
