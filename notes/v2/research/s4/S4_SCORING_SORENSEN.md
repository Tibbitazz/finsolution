# S4 record — Sørensen/Storebrand cross-sectional scoring (owner-designated reference specification)

**Document status:** DRAFT (S4 record, 2026-10-07). The method work belongs to S9c → G9. · **Basis:**
- owner instruction, 2026-10-07;
- ADR-0012 (§2–§5);
- ADR-0024 §4 (allocation domains);
- ADR-0025 (admission ≠ evaluation).

## 0. What this record does and does not do

**Owner instruction (2026-10-07):** "implement the z-scoring for the stock analysis screening, specifically the Sørensen/Storebrand method."

**Effect:**
- The method is the **reference specification** for cross-sectional value and momentum scores in the individual-security allocation domain (S9c).
- The variant grids of RQ-29, RQ-30 and RQ-31 are built around it. Alternatives are pre-registered **variants**; they do not replace it.

**Not done by this record:**
- **No mapping to μ/α.** A score is not an expected return without an accepted mapping (ADR-0012 §3; RQ-33). See §3, P-3, for why this matters in the source's own production step.
- **No master composite.** Value and momentum stay separate descriptors (ADR-0012 §4).
- **No performance claim.** Admission is methodological (ADR-0025); evaluation follows the S7 protocol (RQ-37).
- **No new roster entry.** Roster v0 is unchanged (§6).

**Open choices (§4) do not block the work.** Each one is a declared parameter whose reference value is the source's own choice.

## 1. Sources (identity verified 2026-10-07; read in full)

| Source | Identity | Authority class | Location |
|---|---|---|---|
| L. Q. Sørensen, *Constructing value and momentum scores*, 2026-01-26, 13 slides, R code | md5 `14bc695e6270` | SECONDARY: teaching material by a practitioner, not peer-reviewed. Primary for **this specification** by owner designation | `COURSE/Constructing value and momentum scores.pdf` (HANDOFF §9) |
| L. Q. Sørensen, Storebrand Asset Management, *Factor Investing*, 2025-01-24, 47 slides | md5 `c25dd13a5d76` | SECONDARY (practitioner) | `COURSE/Factor investing Storebrand.pdf` |
| Asness, Moskowitz & Pedersen (2013), *JF* 68(3) | AVAILABLE (S4.0 §4) | Academic primary for value/momentum signals and rank weights (ADR-0012 Evidence) | RPT |
| Pedersen, Babu & Levine (2021), *FAJ* 77(2) | AVAILABLE (S4.0 §1) | Primary for EPO with rank-type signals (§5, O-9c) | RPT |
| Lead, not read: the score demo cited on Storebrand p. 38 (`lars-qvigstad-sorensen.github.io/files/value_score.html`) | — | — | Not fetched (D-4) |

## 2. The method as specified in the sources

Notation:
- $U_t$ = benchmark constituents at $t$ (MSCI World in the source; 2026 p. 2);
- $x^{PE}_{i}$ = Bloomberg field `best_pe_ratio`, the consensus-estimate P/E going by the field name; the vendor definition must be verified in S6;
- $x^{PB}_{i}$ = `px_to_book_ratio`;
- $R^{12m}_i, R^{1m}_i$ = `last_close_trr_1yr`, `last_close_trr_1mo` (total returns, in %).

| # | Step | Specification | Source |
|---|---|---|---|
| S-1 | Orientation | Higher = better: use $-x^{PE}$ and $-x^{PB}$ | 2026 pp. 6, 8 |
| S-2 | Standardise | $z_k(i) = (y_{k,i} - \bar y_k)/s_k$ over the **whole** $U_t$ (R `scale()`: sample sd). No sector or region neutralisation | 2026 p. 8 |
| S-3 | Value composite | $V_i = z\big(w\,z_{PE}(i) + (1-w)\,z_{PB}(i)\big)$. The code uses equal weights | Storebrand p. 37; 2026 pp. 6, 8 |
| S-4 | Momentum 12–1 | $M_i = (1+R^{12m}_i)/(1+R^{1m}_i) - 1 = P_{t-1}/P_{t-12} - 1$ on a total-return index | 2026 p. 7; Storebrand pp. 10, 40 |
| S-5 | Score | value$_i = 100\cdot\text{percent\_rank}(V_i)$ and momentum$_i = 100\cdot\text{percent\_rank}(z(M_i))$, with percent_rank $= (\text{rank}_i - 1)/(n-1)$ (dplyr; ties take the minimum rank). Range 0–100 | 2026 p. 8; Storebrand p. 28 ("internal factor scores (0–100)") |
| S-6 | Missing data | `drop_na()` over all fields: a stock missing any field leaves **both** scores | 2026 p. 8 |
| S-7 | Portfolio step (teaching) | $\max_w \sum_i \text{score}_i w_i$ with constraints; "higher score indicates higher expected returns"; "maximizing score is not sufficient … need constraints" (UCITS, maximum weights) | Storebrand pp. 40, 45 |
| S-8 | Portfolio step (production) | "Minimize tracking error subject to constraints", using the covariance matrix and stock attributes. **The exact formulation is not given** | Storebrand p. 46 |
| — | Other factors named, not specified computationally | Size (market cap); low volatility (volatility, beta); quality (ROE, earnings growth, gross profitability, leverage) | Storebrand p. 10 → RQ-28 candidates only |

The source notes that "rank distribution is uniform" while the "z-score distribution preserves distance" (2026 p. 13). The choice between them is RQ-29.

## 3. Verified properties (synthetic data only; script in the Appendix, seed 20261007)

| # | Property | Status | Consequence |
|---|---|---|---|
| P-1 | percent_rank$(z_{PE}+z_{PB})$ = percent_rank$(z(z_{PE}+z_{PB}))$. The source's code ranks the unstandardised sum; this is identical, because $z(\cdot)$ is strictly increasing | `VERIFIED-DERIVATION` (and numerically identical) | The code and slide p. 6 agree |
| P-2 | $\max s'w$ subject to $\mathbf 1'w = 1$, $0 \le w \le c$ is solved by holding the top $\lceil 1/c\rceil$ names at the cap, by an exchange argument (fractional knapsack with unit sizes). The solution is **invariant to any strictly increasing transform of $s$** | `VERIFIED-DERIVATION`; LP check: 15 names at $c$ = 7%, unchanged under $e^{3s}$ | Under S-7 with box constraints only, z-score versus percentile is irrelevant. Score magnitudes are discarded, which is why the source says constraints are needed |
| P-3 | $\min_a a'\Sigma a$ subject to $s'a = k$, $\mathbf 1'a = 0$ gives $a = \lambda\,\Sigma^{-1}(s - \bar s\mathbf 1)$, with $\bar s = \mathbf 1'\Sigma^{-1}s/\mathbf 1'\Sigma^{-1}\mathbf 1$. This is the active mean–variance portfolio with $\alpha \propto s$ | `VERIFIED-DERIVATION` (Lagrangian); numerical max error 2.2 × 10⁻¹⁶ | S-8, if read as "minimise TE subject to a score-exposure target" (our reading; not stated in the source), **implicitly maps the score linearly to α**. So it needs an accepted RQ-33 mapping (ADR-0012 §3), and the transformation then matters because magnitudes enter |
| P-4 | One outlier changes the effective metric weights for **every other** name. Example: N = 500 lognormal P/E and P/B, one P/B set to 208; Spearman correlations among the other 499 names | Synthetic illustration (not a general result) | The nominal equal weight is not the effective weight; the final percentile rank does not undo this (RQ-31 note) |
| | — no outlier: composite vs P/E 0.77, vs P/B 0.53 | | |
| | — one P/B outlier: 0.94, 0.23 | | |
| | — winsorised at 1%/99%: 0.68, 0.63 | | |
| P-5 | With $-x^{PE}$, a loss-maker (P/E < 0) ranks **cheapest**. With E/P it ranks most expensive | `VERIFIED-DERIVATION` (sign) | Material only if the vendor field returns negative values for negative forward earnings. Whether it does is `OPEN` (S6) |

## 4. Open specification choices: declared parameters, reference value = source

| ID | Choice | Reference (source) | Variants to pre-register | RQ / stage |
|---|---|---|---|---|
| O-1 | Orientation | $-P/E$, $-P/B$ | E/P, B/P (P-5) | RQ-31 |
| O-2 | Outliers | None | Winsorise at q; rank-then-combine | RQ-29, RQ-31 |
| O-3 | Share classes | Each line scored separately (GOOGL and GOOG both in the sample, 2026 p. 2) | Issuer-level de-duplication with a primary line | RQ-28; S6 |
| O-4 | Comparison universe | Global | Region-, sector- or industry-neutral (Storebrand p. 30: value "can also be applied within industries"); a policy-independent reference universe, then filter (ADR-0013) | RQ-30, RQ-38 |
| O-5 | Point-in-time data | Snapshot download | Historical consensus P/E; constituents without survivorship; data timestamps | RQ-08; S6 |
| O-6 | Missing data | Listwise across both factors | Per-factor availability; the universe declared per descriptor | RQ-31 |
| O-7 | Order of operations | Combine z, then rank | Rank each metric, then combine | RQ-31 |
| O-8 | Return currency for momentum | Vendor default (unstated) | Local currency vs NOK. In a global universe the choice changes ranks when currencies move | RQ-28; S6 |
| O-9 | Score → weights | S-7 (linear objective + constraints); S-8 (minimise TE) | (a) direct LP (P-2); (b) benchmark-relative minimum TE (P-3); (c) **Anchored EPO** with the benchmark as anchor. PBL 2021 p. 133 treat exactly "a relative ranking of securities based on their valuations", choosing γ so the signal portfolio's variance equals the anchor's (eq. 21); (d) AMP rank weights | RQ-33; S11 |
| O-10 | Refresh and staleness | Not stated | Monthly, matching the momentum formation; staleness state per descriptor (ADR-0012 §2) | S9c; S13 |

**Recommendation (owner decision at G9, or earlier if wanted):**
- Keep **V0 = the exact source method** as the reproduction oracle; reproducing it is an ADR-0025 admission criterion.
- Pre-register **V1 = the corrected variant** as the candidate production default: E/P and B/P, 1%/99% winsorisation, issuer de-duplication, per-factor missing-data rule.
- **Strongest objection:** V1 departs from the designated method. The reply is that every change is a declared parameter with a stated reason (P-4, P-5), and V0 stays reproducible.

## 5. Placement in the architecture

- **Domain and activation.**
  - Individual security (ADR-0024 §4).
  - Active only if the Policy Statement selects individual securities (S1 question 8.7: "Individual securities" or "Both"); S5 sets the universe.
- **Producer.**
  - The deterministic S9c scoring component (ADR-0012 §2).
  - Outputs two descriptors, SCORE-VAL and SCORE-MOM, with semantics "rank/score".
  - Provenance: inputs, version, comparison universe, timestamps, staleness.
- **Link to the signal library.** The momentum leg uses the same 12–1 formation as XSMOM (SIG-1, EQ-SIG-1). PBL's XSMOM signal is past 12-month return minus the cross-sectional average, scaled so that the positive signals sum to 1 (eqs. 24–25, p. 136). The source scores percentiles instead. Both are SIG-1 variants under RQ-29.
- **Agents (R8).** Agents cite the scores, may challenge where they apply (e.g. negative earnings, ADR-0012 §5), and never compute them.
- **Relationship to ANG.**
  - ANG allocates across asset classes; security scoring sits **below** an asset-class weight, inside a sleeve.
  - Whether this is a two-level process or integrated is open (S5/S11).
  - No PC agent is added.
- **Contamination.** The scores are deterministic and computed from point-in-time data. They carry no LLM look-ahead, so their historical evaluation is valid, subject to O-5. This contrasts with agent judgements (literature review of 2026-10-07).

## 6. Roster confirmation (owner, 2026-10-07)

- **ANG v2 Exhibit 3** has 21 methods; Boudt–Carl–Peterson as the tail-risk-parity reference identifies v2. Adding Simple and Anchored EPO (PC-B6, PC-B7) gives **roster v0 = 23** (S4_PLAN §C.3). The owner's request for "these portfolios + EPO extensions if applicable" is met.
- **EPO at the asset-class level:** PC-B6 and PC-B7.
- **EPO at the security level:** O-9(c). This needs the RQ-33 mapping and a stock-level covariance estimator (S10).
- No further roster entry.

## 7. Next steps (not started)

- S4.20: a typed SCORE contract stub (06 §5).
- S4.24: a synthetic V0 reproduction fixture as the test oracle.
- S7: pre-register the O-1 … O-10 variant grid with multiple-testing control (RQ-37).
- S6: point-in-time data (O-5, O-8).
- S9c → G9: specification and admission.
- *[2026-10-08]* Peer methods (Greenblatt, O'Shaughnessy, Investwiser quality, Seeking Alpha factor grades) are mapped onto the same parameterised contract, with fit verdicts, in `S4_SCORING_PEER_METHODS.md`. The order of operations (O-7) and the missing-data rule (O-6) are shown to be material (G-2, G-3).

## Appendix — verification script (synthetic; reproduces P-1 … P-5)

```python
import numpy as np; from scipy.optimize import linprog; from scipy.stats import rankdata, spearmanr
rng = np.random.default_rng(20261007)
z = lambda x: (x - x.mean()) / x.std(ddof=1)                      # R scale()
prank = lambda x: 100 * (rankdata(x, method='min') - 1) / (len(x) - 1)  # dplyr percent_rank
N = 500; pe = np.exp(rng.normal(np.log(18), .5, N)); pb = np.exp(rng.normal(np.log(3), .7, N))
assert np.array_equal(prank(z(-pe) + z(-pb)), prank(z(z(-pe) + z(-pb))))            # P-1
c, s = .07, rng.normal(size=60)
lp = lambda q: linprog(-q, A_eq=np.ones((1, 60)), b_eq=[1], bounds=[(0, c)] * 60, method='highs').x
assert np.allclose(lp(s), lp(np.exp(3 * s))) and (lp(s) > 1e-9).sum() == np.ceil(1 / c)  # P-2
n = 8; A = rng.normal(size=(n, n)); S = A @ A.T / n + .05 * np.eye(n); s = rng.normal(size=n)
K = np.block([[2 * S, s[:, None], np.ones((n, 1))], [s[None], np.zeros((1, 2))], [np.ones((1, n)), np.zeros((1, 2))]])
a = np.linalg.solve(K, np.r_[np.zeros(n), .5, 0])[:n]; Si = np.linalg.inv(S); o = np.ones(n)
d = Si @ (s - (o @ Si @ s) / (o @ Si @ o)); assert np.allclose(a, .5 / (s @ d) * d)       # P-3
pb2 = pb.copy(); pb2[0] = 208.; m = np.arange(N) > 0                                    # P-4
eff = lambda p, b: [spearmanr((z(-p) + z(-b))[m], -v[m])[0] for v in (p, b)]
print(eff(pe, pb), eff(pe, pb2))   # ≈ [0.77, 0.53]  [0.94, 0.23]
```
