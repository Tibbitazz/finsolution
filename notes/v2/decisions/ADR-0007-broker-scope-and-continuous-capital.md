# ADR-0007 — Initial broker scope (Nordnet, eToro) and continuous account capital

- **Status:** ACCEPTED
- **Date proposed:** 2026-10-01 · **Date decided:** 2026-10-01
- **Decided by:** Owner (explicit instruction, design session 2026-10-01) · **Gate:** G0 · **Stage:** S0
- **Supersedes:** legacy Nordnet-only assumption · **Resolves:** none

## Decision
1. The initial Broker Registry covers **Nordnet** and **eToro**. Neither is
   preferred. All their characteristics are `OPEN` until researched from
   current authoritative sources in S3b (RQ-06).
2. The registry is extensible: adding a broker requires new records only.
3. Account capital is a **continuous** input. No portfolio-size category
   (including NOK 50,000) is structural unless later research establishes
   an economic reason. The Feasibility Engine derives thresholds (minimum
   commission effects, minimum order sizes, fractional availability,
   diversification feasibility) from actual account value and registry
   facts, per broker and instrument.

## Alternatives considered
| Option | For | Against |
|---|---|---|
| Size buckets (e.g. < / > NOK 50k) | Simple UI | Arbitrary; true thresholds differ by broker and instrument |
| **Continuous capital + derived thresholds** | Economically correct; broker-specific | Requires registry completeness |

## Consequences
The UI may still *display* derived thresholds (e.g. "below X NOK, instrument
Y costs more than Z% per trade at this broker"); these are outputs, not inputs.

## Revisit trigger
Owner adds a broker; research identifies a structural size threshold.
