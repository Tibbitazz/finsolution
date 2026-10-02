# ANG interpretation / issues register

**Document status:** LIVING REGISTER (opened at S4.0, 2026-10-02) · **Source:** Ang, Azimbayev & Kim, version 21 Sep 2026 (40 pp). Page numbers are printed page numbers (PDF page − 1).

**Rules:**
- The source is never silently repaired.
- Each issue records both locations, the conflict, its materiality, possible interpretations, whether a decision is required, and the responsible stage.
- Resolutions are recorded here and in the stage document that makes them.

**Materiality:**
- **H** — affects a method's mathematics or an architectural contract.
- **M** — affects a protocol detail or an input specification.
- **L** — naming or citation only.

**Issue types:** internal inconsistency (II) · ANG versus cited source (AS) · under-specification (US).

| ID | Type | Location A | Location B | Conflict | Mat. | Possible interpretations | Decision? | Stage |
|---|---|---|---|---|---|---|---|---|
| ANG-01 | II | Exhibit 4 ("PC agents vote for two proposals") | §3.4 p.12 (modified Borda: top-5 ranking 5..1 plus bottom flag −2, no self-vote) | Voting mechanics differ | M | (a) Exhibit simplified, text authoritative; (b) "two" conflated with the two peer reviews | Yes, at S12 (mechanics are a research object anyway) | S12 |
| ANG-02 | II | Exhibit 3 ("CVaR optimization") | Exhibits 7–8 ("CVaR Minimization") | Objective unclear | H | (a) min-CVaR portfolio; (b) mean–CVaR trade-off/frontier; (c) max return s.t. CVaR limit | Yes | S4.12 |
| ANG-03 | II | §4.3 p.16 ("six expected-return methods") | Exhibit 6 (five method columns + auto-blend; survey absent) and Exhibit A.2 (6 + auto-blend = 7 candidates) | Method count and list | M | (a) survey omitted from Exhibit 6 for lack of data; (b) Exhibit 6 incomplete | No (inventory lists all seven) | S4.15 → S9 |
| ANG-04 | II | Exhibit 1 ("Covariance Agents", plural) | §3.1 p.6 ("A covariance agent") | One vs. several covariance agents | M | (a) single agent; (b) several estimators (cf. §6.3 CRO sub-agents with different estimators) | At S10 | S10 |
| ANG-05 | II | Exhibit 1 ("Risk Agent") | §3.4 ("Chief Risk Officer (CRO) agent") | Naming | L | Same role | No | S4.1 |
| ANG-06 | II | Exhibit 4 ("Total Portfolio Allocation (TPA)") | Exhibit 3, §3.3 ("Total Portfolio Approach") | Naming | L | Same method | No | S4.12 |
| ANG-07 | II | Exhibit 4 ("Global min vol") | Exhibit 3 ("Global minimum variance") | Naming | L | Same portfolio (argmin σ ≡ argmin σ² under the same constraints) | No; record the equivalence | S4.11 |
| ANG-08 | II | §3.5 p.13 (CIO receives "the 21 candidate portfolios") | Exhibit 5 (inputs drawn as revised PC agents) | CIO input set | M | Exhibit 8 weights all 21 methods, so the CIO combines revised and unrevised candidates | Record; S12 | S12 |
| ANG-09 | II | §3.4 p.12 (metric score: backtest Sharpe, IPS compliance, diversification, regime fit, estimation risk, CMA utilization, **regime-dependent** weights) | §4.5 p.19 (CIO scores six dimensions with **fixed** 25/15/15/20/15/10) | Two scoring layers with different weighting | M | Distinct layers (strategy-review metric vs. CIO judgement) | Neither weight set adopted (ADR-0023) | S12 |
| ANG-10 | AS | §3.3 p.10 (Researcher's max-entropy method "maximizes the Shannon entropy of portfolio weights subject to a minimum Sharpe ratio floor") | Bera & Park (2008), as summarised by the publisher record: cross-entropy objective with side conditions from the mean and covariance of *resampled* returns | ANG's description may differ from the cited method | H (for the Researcher example) | (a) ANG implements a simplified variant; (b) the summary is incomplete | Verify against Bera & Park when retrieved | S4.14 |
| ANG-11 | AS | §4.5 p.19 ("effective number of assets of 11.2 (Meucci 2009)"); fn 8 (equal-weighted 18-asset universe has 18 "by construction") | Meucci (2009): "effective number of bets" from the entropy of the distribution of *uncorrelated bets* | The footnote implies a weight-based measure (e.g. exp-entropy or inverse HHI of weights). Meucci's ENB of an equal-weighted correlated universe is generally not N | M (CRO/CIO diagnostic definition) | (a) ANG uses a weight-entropy measure and cites Meucci loosely; (b) a different Meucci variant | Yes, at S4.16 | S4.16 |
| ANG-12 | AS | p.3 ("Du et al. (2023) show multi-agent debate …"; next sentence "Du et al. (2023) demonstrate that ensembles of LLM agents can match or exceed human crowd accuracy in prediction tasks") | Du et al. (2023) is the debate paper (arXiv 2305.14325) | The second claim may cite the wrong source | L (no method depends on it) | (a) citation error; (b) a finding within Du et al. | No; verify when relevant | S12 |
| ANG-13 | AS | Exhibit 3 (Kirby & Ostdiek 2012 for **both** inverse volatility and inverse variance) | Kirby & Ostdiek's volatility-timing rule (to be read) uses inverse variance with a tuning exponent | How 1/σ maps to the source | M | (a) 1/σ is the exponent-½ special case; (b) 1/σ comes from another source | Yes | S4.5 |
| ANG-14 | AS / US | Exhibit 3 (volatility targeting, Moreira & Muir 2017) | Moreira & Muir scale the time-series exposure of a single factor portfolio by c/σ²_t | ANG does not say which base portfolio is vol-targeted, the target level, or where the residual goes (cash) | H | (a) scale 1/N or another base portfolio to a target volatility with a cash residual; (b) per-asset volatility scaling | Yes | S4.5 |
| ANG-15 | US | §3.3 p.10; Exhibit 3 (TPA two-factor, equity and bonds; ABD 2014; text also cites Gilmore & Simonian 2025) | — | No formulation given: factor definitions, exposure estimation, optimisation objective | H | Specify from ABD 2014 (reference-portfolio / factor framework) and Gilmore & Simonian | Yes | S4.12 |
| ANG-16 | US | §3.3 p.10 (adversarial diversifier: maximise tracking variance vs. the centroid of the other PC weights, s.t. Sharpe ≥ 75% of the maximum-Sharpe portfolio) | — | Unspecified: budget/long-only/bounds; which Sharpe (ex-ante with CMAs?); risk-free rate; maximising a convex function (non-convex problem, multiple optima); tie-breaking | H | Specification required for deterministic reproducibility | Yes | S4.14 |
| ANG-17 | US | p.6 (PC agents "take the CMAs … and the covariance matrix") | Exhibit 3 (market-cap weight needs capitalisations; CVaR, drawdown and tail-risk parity need return scenarios or paths; TPA needs factor exposures) | Inputs beyond CMAs + Σ are not listed | H (contract heterogeneity) | PC input sets are heterogeneous (owner item 12) | Resolved by heterogeneous contracts (S4.20) | S4.20 |
| ANG-18 | US | Exhibit 3 ("Mean–downside risk", Sortino & van der Meer); Exhibit 7 ("Mean-Downside Risk (Sortino)") | — | Objective unclear | H | (a) maximise the Sortino ratio; (b) mean–semivariance efficient portfolio at a target; (c) minimise downside deviation s.t. a return floor | Yes | S4.5 / S4.12 |
| ANG-19 | II (interpretive) | §3.4 p.12 and §4.5 (backtest Sharpe used in scoring and ensemble weighting) | pp. 2, 13, 22 (the agentic pipeline "cannot be cleanly backtested") | Apparent tension | M | Deterministic method components can be backtested; the agentic layer cannot (§5.1) | Recorded; S7 defines runtime diagnostics | S7 |
| ANG-20 | US | §3.4 p.13 (top five "revise their proposals"; may "revise their structured output to incorporate comments") | R1 (05) | What may change in a revision | H | Settled by OD-3 (ADR-0024 §2) | Resolved (ADR-0024) | S12 |
| ANG-21 | US | §3.3 p.10 (Researcher's method enters the same run and receives CIO weight; Exhibit 8: 5.6%) | ADR-0005 / 06 funnel | Production governance | H | Settled by OD-2 (ADR-0024 §1) | Resolved (ADR-0024) | S4.14 |
| ANG-22 | AS | Exhibit 3 (TPA cited to ABD 2014) | §3.3 p.10 (TPA also cited to Gilmore & Simonian 2025) | Two sources for one method | L/M | ABD for the concept; Gilmore & Simonian for practice | Read both | S4.12 |
