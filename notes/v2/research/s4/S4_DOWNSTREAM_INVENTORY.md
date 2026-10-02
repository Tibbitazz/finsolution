# S4.15b — Downstream method inventory (rebalancing, implementation, timing, tactical)

**Document status:** DRAFT (inventory only) · **Prepared:** 2026-10-02 · **Basis:** ADR-0026 (PROPOSED); ADR-0012; RQ-17, RQ-35, RQ-44, RQ-53

**Rules:**
- **Inventory only.** No method here is admitted, specified or reviewed mathematically in S4.
- Methodology belongs to S13 (with S7 evaluation).
- Inventory exit states: `REMOVED / RELOCATED / MERGED`, each with a reason (S4 plan §E.2).
- Source authority follows S4 plan §E.1. Social-media and owner-supplied examples are **research leads**, never evidence.

## 1. Candidate families

| ID | Family | Object type(s) | Located primary sources (status) | Layer / stage | Status |
|---|---|---|---|---|---|
| T1 | Trend following / TSMOM | Signal · exposure rule · tactical overlay · timing evidence | MOP 2012, HOP 2017 (AVAILABLE; S4.8) | Belief S9 / tactical S13c / timing S13d (by use, ADR-0026 §8.9) | Registered |
| T2 | Cross-sectional momentum | Signal · signal-conditioned universe · μ mapping | JT 1993, AMP 2013 (AVAILABLE; S4.8) | S9c–d; not timing by default | Registered |
| T3 | Short-horizon reversal / mean reversion | Timing evidence · tactical rule | Jegadeesh 1990 and Lehmann 1990 (AVAILABLE, located; individual stocks only) | S13d | Registered — **family question first** (§3) |
| T4 | Volatility-conditioned scaling | Exposure rule | Moreira–Muir 2017 (AVAILABLE); Barroso–Santa-Clara 2015 (status per S4.0) | S11, S13c | Registered |
| T5 | Transaction-cost-aware implementation | Implementation method | Perold 1988 (AVAILABLE); Gârleanu–Pedersen 2013 (AVAILABLE, not re-read); others not obtained | S13b–e | Registered |
| T6 | Moving-average / trend filters | Timing evidence · regime evidence | Not obtained | S9a / S13d | Registered |
| T7 | Event-aware implementation | Implementation constraint | Not identified | S13e | Registered (source gap) |
| T8 | Statistical / ML timing evidence | Timing-evidence model | Not obtained | S13d, S7 | Registered; **only if a defined decision problem survives the family screen** |
| T9 | Staged execution | Implementation method | Not obtained | S13e | Registered |
| T10 | Deterministic rebalancing rules | Rebalancing rule | Perold & Sharpe 1988 (AVAILABLE); Gârleanu–Pedersen 2013 (local) | S13b (RQ-44) | Registered |
| T11 | Stop-loss / exit rules | Tactical rule (tactical mandate only) | Not obtained | S13d | Registered |
| T12 | Backtest-overfitting controls | Evaluation method | Harvey–Liu–Zhu (AVAILABLE); others not obtained | S7 | Registered |

## 2. ML trading specification (owner-supplied, 2026-10-02): disposition (owner D-D)

**Rejected as a system architecture.** Retained only as research candidates:

| Retained component | Relocated to |
|---|---|
| Data-quality / hygiene controls | Existing S6 / 04 requirements (MERGED) |
| Volatility, liquidity and spread statistics | Implementation evidence service (T5/T9 inputs) |
| Event calendars | T7 |
| Statistical timing methods | T8 (conditional) |
| Trend/momentum kernels | T1/T2/T6, **only where they add to the existing XSMOM/TSMOM framework** |

**REMOVED from the system level:**
- the stock-direction prediction objective;
- the claim that the feature set is "sufficient";
- Up/Down/No-Trade classification as a target;
- triple-barrier labelling in the strategic architecture;
- hard regime gates;
- stops and targets for strategic holdings;
- Long/Short output at the Trader layer.

**Hypotheses, not facts:**
- The price/EMA features are approximately exponentially weighted sums of past returns. This is an algebraic approximation.
- The feature set spans few independent dimensions. This needs empirical analysis and is pursued only if T8 is.

**Admission bar for any future ML model:** it must beat simple admissible controls after realistic costs, under appropriate out-of-sample validation (S7).

## 3. Short-horizon timing family: z-score example
- **Status:** research lead within T3. **Source class:** social media (hypothesis generation only). No privileged status; not a Trader or execution component.
- **Order of questions:**
  1. Does short-horizon reversal/technical information improve investment or implementation decisions after realistic costs, for the instruments this engine holds?
  2. Only if the family survives: test particular parameterisations, z-score last.
- **Located evidence:** Jegadeesh 1990 and Lehmann 1990 cover individual US stocks, cross-sectionally, long–short. They give **no** evidence for index ETFs, long-only use or implementation timing. Jegadeesh (p. 881) reports Lo & MacKinlay (1988) finding *positive* serial correlation in weekly returns, in the context of index and size-portfolio predictability.
- **Mathematical note:** with n = 5, |z| ≤ (n−1)/√n (sample SD) or √(n−1) (population SD). This bounds the range only. **Signal frequency is empirical.**
- **Execution-timing rule:** a signal that needs the final close cannot be treated as executable at that same close without look-ahead. A valid design is either:
  - pre-close signal → close execution; or
  - close signal → next tradable price.

  Lehmann (1990, fn. 16) notes that closing-price data cannot simulate open or limit-order execution.
- **Removal criteria for the whole family, declared in advance:**
  - no incremental performance after realistic costs;
  - redundancy with existing methods;
  - unstable results;
  - poor out-of-sample behaviour;
  - lack of economic rationale for the instrument class;
  - non-executable timing;
  - failure of robustness tests.
