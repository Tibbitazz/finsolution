# ENGINE_V1 — Mathematical Appendix and Developer Specification

**Purpose.** Every formula required to implement the portfolio-construction
framework: signals, risk models, optimization, transaction costs, rebalancing,
leverage, constraints, factor scoring, and performance evaluation. Written to
be mathematically self-contained — a developer should not need any other
document to find a missing equation, variable definition, or sequencing rule.

**Companion document.** `notes/SPECIFICATION.md` is the master technical
specification — system architecture, data sources, investment universe,
constraints, roadmap, and the full developer task register. This document is
the mathematical reference that master specification's own Part IV points
to; where the two overlap, **this document is authoritative** (it was
verified directly against the primary source papers; `SPECIFICATION.md`'s
Part IV predates that verification pass and is looser on several points this
document corrects — e.g., the confirmed momentum-window convention in §3,
and the exact anchored-EPO formula in §8.3). Read `SPECIFICATION.md` first
for system context; use this document for implementation-grade formulas.

**Primary sources, read directly for this document (not from memory):**
- **PBL** — Pedersen, L.H., Babu, A., & Levine, A. (2021). "Enhanced Portfolio
  Optimization." *Financial Analysts Journal*, 77(2), 124–151. Published
  version (not the SSRN preprint) — equation numbers below are the **published
  FAJ numbering** and were read directly from the PDF, including page-image
  verification of Equations 17–22, 23–28, and A1–A2. This resolves an
  ambiguity this project's own `notes/covariance/rmt_background.md` had
  flagged as open (in-code comments cited SSRN preprint numbering; that note
  guessed at a FAJ reconciliation but had not verified it against the actual
  PDF). **That reconciliation is now done and confirmed** — see §8.
- **GP** — Gârleanu, N., & Pedersen, L.H. (2013). "Dynamic Trading with
  Predictable Returns and Transaction Costs." *Journal of Finance*, 68(6),
  2309–2352. Read directly; equation numbers below match the published paper.
- **AMP** — Asness, C.S., Moskowitz, T.J., & Pedersen, L.H. (2013). "Value and
  Momentum Everywhere." *Journal of Finance*, 68(3), 929–985. Read directly in
  an earlier design session (this session re-confirms only what is used here).
- **Sørensen** — L.Q. Sørensen (Storebrand Asset Management), "Factor
  Investing" and "Constructing Value and Momentum Scores" (internal decks,
  read directly in an earlier design session).
- Other sources (Ledoit-Wolf, Engle, Bollerslev, Glosten-Jagannathan-Runkle,
  Aielli, etc.) are cited where used; where a formula's exact notation could
  not be verified against a primary text this session, that is stated
  explicitly rather than presented as confirmed.

**Notation collision — read this before anything else.** PBL uses **`x`** for
the portfolio weight vector and reserves **`w`** for the EPO shrinkage
parameter. Every other section of this document (returns, MVO, GMV,
constraints, performance) follows standard portfolio-math convention and uses
**`w`** for portfolio weights, consistent with how you have been writing it.
**Section 8 (EPO) uses PBL's own notation exactly as published** — `x` for
weights, `w` for shrinkage — because the user requirement is to preserve the
paper's notation there. Do not carry EPO's `w` (shrinkage) into any other
section's `w` (weights); they are unrelated symbols that happen to collide
only inside Section 8's source material. This is flagged again at the start
of Section 8.

**Status tags**, used on every formula: **[SOURCED: X]** — taken directly from
source X, notation preserved. **[ADAPTED: X]** — based on source X but the
notation or a minor element (e.g., discrete-time indexing) has been changed
for consistency with the rest of this document, with the change stated.
**[PROPOSED]** — not from a specific academic source; an implementation
choice, stated as such, not presented as literature-backed.

**Document structure**, per the four required categories, applied throughout
rather than as one final section: each formula's box states whether it is
**Confirmed methodology** (in the near-term build path), an **Optional
extension** (reviewed, gated), or feeds an **Unresolved design decision**
(consolidated in Table C). **Developer implementation notes** appear inline
under each formula and are consolidated in Table D.

---

## 1. General requirements — the per-formula template

Every formula below is presented as: **Equation** (LaTeX) → **Variables** →
**Required inputs** → **Interpretation** → **Used in** (system location) →
**Estimation window/frequency** → **Source status** → **Assumptions** →
**Numerical issues** → **Implementation notes/pseudocode**. Simple,
low-risk formulas (e.g., simple return) compress this template; formulas with
real ambiguity or estimation risk (EPO, GARCH, DCC, GP dynamic trading) use it
in full.

---

## 2. Return calculations

### 2.1 Simple (arithmetic) return

$$R_{i,t} = \frac{P_{i,t}+D_{i,t}}{P_{i,t-1}}-1$$

**Variables:** $P_{i,t}$ price of asset $i$ at $t$; $D_{i,t}$ cash dividend
(or other cash distribution) paid between $t-1$ and $t$.
**Inputs:** raw price series, dividend/distribution series (or a
provider-adjusted close that already embeds them).
**Interpretation:** proportional wealth change over one period, inclusive of
income — the quantity that is additive **across assets** within a period
(portfolio return aggregation, §4.3, requires simple returns, not log
returns).
**Used in:** every return series entering the system; source data for §2.2.
**Estimation window:** none — a point calculation per period.
**Source status:** [PROPOSED] — standard definition, not attributed to a
specific paper.
**Treatment of specific cases:**
- **Adjusted prices.** Use provider-adjusted close (Yahoo/EODHD) where
  available so that $D_{i,t}$ is implicitly embedded and does not need to be
  added separately — do not add $D_{i,t}$ on top of an already-adjusted
  price, which double-counts the dividend.
- **Stock splits.** Must be reflected in the adjustment factor applied to the
  entire pre-split price history, not just the split date, or $R_{i,t}$ on
  the split date will show a spurious jump.
- **Delistings.** The final observed price (or a recovery-value proxy if the
  provider furnishes one) becomes the last $P_{i,t}$; the asset then exits
  the universe (§III of the master specification, `notes/SPECIFICATION.md`)
  — its historical returns up to that date remain in the panel for
  survivorship correctness.
- **Missing observations.** Do not forward-fill price (which fabricates a
  zero return); instead exclude the asset from that period's active set
  (the `.active_set(M,t)` mechanism already specified in
  `notes/SPECIFICATION.md` §III.6).
- **Non-trading days.** No return is computed for a date the exchange did
  not trade; the panel is indexed on the trading calendar of each asset's
  home exchange, reconciled to a common calendar only after currency
  conversion (§2.5) and before cross-sectional signal construction (§3.4),
  since a cross-sectional signal requires all assets observed on the same
  date.
**Numerical issues:** none at this stage; issues from bad ticks/outliers are
handled at the validation layer (`notes/SPECIFICATION.md` §II.1), not in the
return formula itself.

### 2.2 Log return

$$r_{i,t} = \ln\left(\frac{P_{i,t}}{P_{i,t-1}}\right)$$

**Interpretation:** continuously-compounded return; additive **across time**
($\sum_t r_{i,t}$ is the cumulative log return), unlike simple returns.
**When to use which:**
- **Log returns** for GARCH/DCC estimation (§9, §10) — required, since the
  GARCH literature's asymptotic theory and stationarity conditions are
  stated in terms of log-return innovations; and for constructing
  multi-period trailing-return signals where compounding needs to be exact
  over long windows without arithmetic drift (§3).
- **Arithmetic returns** for **any portfolio wealth or aggregation
  calculation** — $\sum_i w_i R_{i,t}$ is a portfolio's simple return; the
  same sum of log returns is **not** the portfolio's log return except as a
  second-order approximation. Do not use log returns inside §4.3's portfolio
  return formula.
**Source status:** [PROPOSED] — standard definition.
**Numerical issues:** for $R_{i,t}$ close to $-100\%$ (near-total loss),
$r_{i,t}\to-\infty$; guard against this in delisting-adjacent observations.

### 2.3 Excess return

$$r_{i,t}^{e} = R_{i,t}-r_{f,t}$$

**Variables:** $r_{f,t}$ the risk-free rate over the same period, **already
NOK-denominated and time-aligned** (see §2.5's dependency).
**Alignment rule (this is where implementation errors are most likely):**
$r_{f,t}$ must be sourced and compounded at the **same frequency as
$R_{i,t}$**. If the system is estimating at daily frequency (the confirmed
target frequency, `notes/SPECIFICATION.md` §A.0) but the risk-free source is
a monthly or annualized quote (e.g., an annualized NIBOR fixing), convert via
$r_{f,t}^{daily} = (1+r_{f}^{annual})^{1/252}-1$, not by dividing the annual
rate by 252 (which understates compounding, immaterially at low rates but
should not be built as a silent approximation).
**Which risk-free rate:** NIBOR (1M) for OSE-leg assets, Fed Funds Effective
Rate for US-leg assets, **both converted to NOK-consistent excess-return
terms after §2.5's currency conversion has already happened** —
`notes/SPECIFICATION.md` §IV.3 states this purpose-split; it is not repeated
in full here, only cross-referenced.
**Used in:** all signal construction (§3), all risk-model estimation (§7,
§9, §10), all performance measures (§15).
**Source status:** [PROPOSED] — standard definition; the purpose-specific
choice of *which* risk-free rate is a confirmed project decision
(`notes/SPECIFICATION.md` §A.4), not a PBL specification.

### 2.4 Cumulative portfolio wealth

$$W_T = W_0\prod_{t=1}^{T}(1+R_{p,t})$$

**Variables:** $W_0$ initial capital; $R_{p,t}$ portfolio simple return in
period $t$ (§4.3).
**Used in:** all performance reporting (§15), the leveraged-compounding
analysis already derived in `notes/SPECIFICATION.md` §IV.14.
**Source status:** [PROPOSED] — standard definition. **Must** use simple, not
log, returns (§2.2's rule).

### 2.5 NOK-denominated return for foreign assets

$$1+R_{i,t}^{NOK} = (1+R_{i,t}^{LC})(1+R_{c/NOK,t})$$

equivalently

$$R_{i,t}^{NOK} = R_{i,t}^{LC} + R_{c/NOK,t} + R_{i,t}^{LC}R_{c/NOK,t}$$

**Variables:** $R_{i,t}^{LC}$ asset $i$'s return in its local listing
currency $c$; $R_{c/NOK,t}$ the return of currency $c$ **expressed as NOK
per unit of $c$** — i.e., the percentage change in how many NOK one unit of
$c$ buys.
**Quotation-convention warning (explicit, since a reversed convention
silently produces the wrong sign of FX P&L):** if the sourced FX series is
quoted as *foreign-currency-per-NOK* (e.g., Norges Bank and most quote
conventions for USD/NOK give **NOK per USD**, which is the convention this
formula wants directly) versus *NOK-per-foreign-currency inverted* (some
providers quote NOK/USD as USD-per-NOK), **verify the quotation direction
before computing $R_{c/NOK,t}$**, and if the sourced series is inverted, use
$R_{c/NOK,t} = \frac{1}{S_t/S_{t-1}}-1$ where $S_t$ is the as-quoted rate,
not $R_{i,t}^{LC}$ minus the raw quoted change. A sign error here silently
flips whether a strengthening NOK helps or hurts a foreign holding's
NOK-denominated return, and will not throw an error — it will just produce a
plausible-looking wrong number. **Recommended check before production use:**
compute a known case by hand (e.g., a period where USD/NOK is known to have
risen X%) and confirm the sign of $R_{c/NOK,t}$ matches intuition before
trusting the pipeline.
**Used in:** L0 currency conversion, applied immediately after computing
local-currency simple returns, before any other calculation —
`notes/SPECIFICATION.md` §IV.17 states the pipeline placement; this section
supplies the formula itself with the full derivation.
**Source status:** [PROPOSED] — standard FX-return decomposition, not
attributed to a specific paper.
**Numerical issues:** none beyond the quotation-direction risk above.
**Dependency:** FX rate source (Norges Bank primary, Yahoo Finance fallback,
per `notes/SPECIFICATION.md` §II.8/§A.1a).

---

## 3. Expected-return signals

### 3.1 Time-series momentum (TSMOM) — [SOURCED: PBL Eq. 23]

**Trailing excess return** [ADAPTED: PBL notation]:

$$R_{i,t-L:t}^{e} = \prod_{k=t-L+1}^{t}(1+R_{i,k}^{e})-1$$

**PBL's exact TSMOM signal** (verified directly against the published PDF,
page-image-confirmed):

$$s_{i,t}^{TSMOM} = 0.1\times\sigma_{i,t}\times\operatorname{sign}\!\left(r_{i,t-12,t}^{e}\right) \qquad \text{(PBL Eq. 23)}$$

**Variables:** $\sigma_{i,t}$ the estimated volatility of asset $i$ at $t$
(PBL's Global-1 sample uses an EWMA daily-volatility estimate with a 60-day
center of mass — see §3.1's "risk model used by PBL" note below);
$r^e_{i,t-12,t}$ the trailing 12-month excess log return.

**Critical, explicitly verified finding on window convention — do not
substitute a different one.** PBL's own notation is $r^i_{t-12,t}$: the
trailing window runs from month $t-12$ to month $t$ **inclusive of the
signal-formation date itself**. This is confirmed by direct visual
inspection of the published equation (Eq. 23) and independently reconfirmed
in Appendix A's benchmark formulas (Eq. A1, A2, same subscript). **PBL's
TSMOM does not use the "12-1" skip-most-recent-month convention** common
elsewhere in the momentum literature (e.g., Jegadeesh & Titman 1993,
Asness/Moskowitz/Pedersen 2013's own 2-12 formulation cited in an earlier
design session, and this project's own existing `signals/cross_sectional.R`
`mom12_1` implementation, which explicitly skips the most recent month).
**[DECIDED]** The project has confirmed adoption of PBL's no-skip
$[t-12,t]$ convention — for **both** TSMOM and XSMOM (§3.4 carries the
XSMOM-specific consequence; this paragraph covers TSMOM only). Consequence
for TSMOM: the existing `mom12_1` metric (`signals/cross_sectional.R`),
which skips the most recent month, **must not be reused as-is for
`ts_signal`** — a new, no-skip trailing-return calculation is required
(Table D, item 3). `mom12_1` itself is not deprecated by this decision — see
§3.4 for what happens to its current consumer, the `xsmom` signal.

**Sharpe-ratio scaling constant, 0.1:** PBL state this constant is
calibrated to match Moskowitz, Ooi & Pedersen (2012)'s realized Sharpe
ratios, and — importantly — **"this choice is inconsequential for the
Sharpe ratio of the final EPO portfolio"** (PBL's own text, verified). It
matters for the *interpretation* of $s_{i,t}$ as a signed conditional
expected excess return, but not for any Sharpe-ratio-based backtest result,
since simple EPO (§8.1) is linear/scale-invariant in the signal up to
$\gamma$.

**Used in:** L1 signal layer, feeding $\mathbf{s}$ in the EPO family (§8) or
$\boldsymbol{\mu}$ in classical MVO (§5); the in-house managed-futures sleeve
already specified in `notes/SPECIFICATION.md` §V.13.
**Estimation window/frequency:** PBL's own backtest used monthly signal
formation over a 12-month trailing window, applied to daily-estimated
$\sigma_{i,t}$ (EWMA, 60-day center of mass) — a mixed-frequency design
(monthly signal, daily risk estimate) that should be preserved if
reproducing PBL exactly, rather than assumed to be all-daily.
**Numerical issues:** requires at least 12 months of return history per
asset before a first signal can be formed; ragged-history assets (common on
OSE) need the `.active_set` gating already specified.
**Pseudocode:**
```
for each instrument i, each formation date t:
    r_trail = cumulative_return(i, from=t-12m, to=t)     # inclusive, no skip
    sigma_i_t = ewma_vol(i, center_of_mass=60d)           # or GJR-GARCH, see §9
    s[i,t] = 0.1 * sigma_i_t * sign(r_trail)
```

### 3.2 Equal-notional TSMOM benchmark portfolio — [SOURCED: PBL Eq. A1]

$$x_{t}^{TSMOM,\,equal\text{-}notional} = \frac{1}{n_t}\operatorname{sign}\!\left(r_{i,t-12,t}^{i}\right)$$

**Variables:** $n_t$ number of instruments available at $t$.
**Interpretation:** long or short each instrument with equal notional
exposure, sized only by $1/n_t$ — no volatility scaling at all. PBL note
explicitly (verified) that notional-weighted portfolios are uncommon in
practice across heterogeneous-volatility asset classes, because portfolio
risk ends up dominated by whichever instruments happen to have the highest
volatility — this is presented **as a benchmark to beat**, not a
recommended production construction.
**Long/short exposure:** by construction, gross notional exposure is exactly
$\sum_i |x_i| = 1$ (fully invested, one-dollar gross); the split between long
and short notional depends entirely on how many instruments currently have
positive vs. negative trailing sign — **it is not constrained to be 50/50**,
and net exposure $\sum_i x_i$ varies over time with the prevailing trend
breadth.
**Used in:** benchmark/validation only (§8.5's out-of-sample comparison
requires a benchmark to beat) — not a production portfolio-construction
method in this system.
**Source status:** [SOURCED: PBL Eq. A1], confirmed by direct page-image
inspection of Appendix A.

### 3.3 Equal-volatility TSMOM benchmark portfolio — [SOURCED: PBL Eq. A2]

$$x_{t}^{TSMOM,\,equal\text{-}volatility} = \frac{1}{n_t}\cdot\frac{40\%}{\sigma_{i,t}}\operatorname{sign}\!\left(r_{i,t-12,t}^{i}\right)$$

**Explicit correction to a plausible-but-wrong alternative.** This is
**not** $\operatorname{sign}(\cdot)/\sigma_{i,t}$ normalized by the sum of
absolute weights across assets (a natural-looking alternative that was
proposed as a starting point before the source was verified) — PBL's actual
construction divides by $n_t$ **and** scales by a **fixed 40% annualized
volatility-target constant** per instrument, not by a data-dependent
normalizer. The two constructions are not equivalent, and give different
time-series behavior (the sum-of-absolute-weights version is always exactly
gross-1; PBL's version is not — its gross exposure varies with the average
level of $1/\sigma_{i,t}$ across the current universe). **Use PBL's Eq. A2
exactly if the goal is to reproduce their published benchmark or their
$\gamma_t = n_t/40\%$ calibration (§8, Eq. 23's note) — the two are
linked and must not be decoupled.**
**Interpretation:** each instrument targets 40% annualized standalone
volatility, divided equally across $n_t$ instruments — this is the standard
Moskowitz, Ooi & Pedersen (2012) TSMOM implementation, which PBL reproduce
exactly for benchmarking purposes (confirmed: PBL state they chose
$\gamma_t = n_t/40\%$ specifically **so that** the fully-shrunk ($w=100\%$)
EPO portfolio exactly matches this benchmark — see §8.1).
**Source status:** [SOURCED: PBL Eq. A2], page-image-confirmed.
**Developer note:** if this benchmark is built for validation purposes
(§16's role for benchmark comparisons generally), the 40% constant and the
$1/n_t$ scaling must both be reproduced exactly, or the fully-shrunk EPO
identity check (a useful internal consistency test — at $w=100\%$, simple
EPO should degenerate to a scalar multiple of this benchmark) will not hold
and will falsely look like an implementation bug when it is actually a
benchmark-construction mismatch.

### 3.4 Cross-sectional momentum (XSMOM) — [SOURCED: PBL Eq. 24–26, 28]

$$XSMOM_{i,t} := r_{i,t-12,t} - \frac{1}{n}\sum_{j=1}^{n} r_{j,t-12,t}$$

$$s_{i,t}^{XSMOM} = c_t\left(r_{i,t-12,t} - \frac{1}{n}\sum_{j=1}^{n} r_{j,t-12,t}\right) \qquad \text{(PBL Eq. 24)}$$

**Normalization** (PBL Eq. 25, verified exactly):

$$\sum_{i}s_{i,t}\,\mathbb{1}_{\{s_{i,t}>0\}} = \sum_{i}\left|s_{i,t}\right|\mathbb{1}_{\{s_{i,t}<0\}} = 1$$

**Derivation of $c_t$:** $c_t$ is the unique positive scalar such that
scaling the raw demeaned cross-sectional return by $c_t$ makes the positive
signals sum to exactly $+1$ (equivalently, by construction of the
demeaning, the negative signals' absolute values also sum to exactly $1$,
since the demeaned values already sum to zero overall — the normalization
condition is one equation with one unknown, solved as
$c_t = 1\big/\sum_{i:\,\tilde s_{i,t}>0}\tilde s_{i,t}$ where $\tilde
s_{i,t}=r_{i,t-12,t}-\bar r_{t-12,t}$ is the pre-scaling demeaned value).
**Window convention: identical to §3.1's finding — $[t-12,t]$, no skip-month
adjustment**, independently confirmed by direct inspection of Eq. 24's
published notation (`r^i_{t-12,t}`, same subscript pattern as TSMOM's Eq.
23). **[DECIDED]** confirmed alongside TSMOM — the no-skip convention applies
to XSMOM as well, not TSMOM alone. Consequence: the project's existing
`xsmom` signal (`signals/cross_sectional.R::register_signal("xsmom",
cs_signal("mom12_1", "demean"), ...)`) is built on the skip-month `mom12_1`
metric and is therefore **not** PBL's XSMOM as specified — it is a
legitimate, distinct signal in its own right (the AMP-2013-style skip-month
convention, per an earlier design session), but must not be presented as
"the PBL XSMOM implementation." A new signal — e.g. `xsmom_pbl`, built on
the same no-skip trailing-return metric as §3.1's `ts_signal` — is required
to reproduce PBL's specification exactly (Table D, item 3). Both signals
are retained side by side; neither replaces the other.
**Signal timing:** formed at $t$ using only information available through
$t$ (no look-ahead) — consistent with the general estimation-window
discipline already specified for the L1 layer.
**Minimum eligible assets / missing histories:** PBL's own equity samples
require the full 12-month trailing window per instrument before inclusion;
an asset without 12 full months of history is excluded from $n$ (the
active-count) for that period, consistent with the `.active_set` mechanism.
**Ties:** not addressed explicitly in PBL's text; [PROPOSED] treat tied raw
values as retaining their natural (non-strict) ordering — since the signal
used is the continuous demeaned value, not a discrete rank, exact ties are
measure-zero in practice and do not require a special rule.
**Raw or excess returns:** PBL's equity samples subtract the one-month US
T-bill rate before computing the 12-month trailing return (confirmed in the
paper's data section) — i.e., **excess returns**, consistent with §2.3.
**Sector-neutralization:** **not part of PBL's XSMOM specification** — their
XSMOM is demeaned across the *entire* cross-section of test assets (49 US
equity industries), which is itself a form of neutralization relative to
the broad universe, but is not sector/industry-relative in the sense this
project's own security-scoring pipeline uses (§16). Do not conflate the
two: PBL's cross-sectional demeaning and this project's within-sector
z-score/rank pipeline (§16) are related but distinct mechanisms, and §16's
sector-relative construction is a **[PROPOSED]**, project-specific
extension, not part of PBL's XSMOM.

**Variants — explicitly marked as variants, not the baseline:**

$$s_{i,t} = XSMOM_{i,t}\times\sigma_{i,t} \qquad \text{(PBL Eq. 26, "Equity 4")}$$
$$s_{i,t} = XSMOM_{i,t}\times\sigma_{i,t}^{2} \qquad \text{(PBL "Equity 5", verified: } s_{i,t}=(\sigma_{i,t})^2\times XSMOM_{i,t}\text{)}$$

PBL's own rationale (verified): multiplying by $\sigma_{i,t}$ makes the
fully-shrunk EPO portfolio's notional weight proportional to the Sharpe
ratio of each instrument's outperformance (PBL Eq. 27:
$EPO^s(w{=}100\%)^i = XSMOM^i_t/(\gamma\sigma^i_t)$) — an intuitive scaling
under the belief that the investment opportunity set is roughly stable over
time. The $\sigma^2$ variant makes the fully-shrunk portfolio directly
proportional to outperformance itself, with no volatility adjustment at all.
**Used in:** L1 signal layer; the $\times\sigma$ and $\times\sigma^2$
variants are selectable, not defaults.
**Source status:** [SOURCED: PBL Eq. 24–26, 28] — all four (baseline,
normalization, $\times\sigma$, $\times\sigma^2$) verified directly.

---

## 4. Basic portfolio constructions

### 4.1 Equal-weight portfolio

$$w_{i,t}^{1/N} = \frac{1}{N_t}$$

**Eligibility/entry-exit:** $N_t$ is the count of assets in the active,
Nordnet-investable universe at $t$ (`notes/SPECIFICATION.md` §III.13) — an
asset newly meeting eligibility enters at the next rebalance with weight
$1/N_t$ (diluting existing holdings); a delisted or screened-out asset exits
and the remaining $N_t-1$ assets are rescaled to $1/(N_t-1)$ at the next
rebalance, not intraperiod.
**Source status:** [PROPOSED] — standard baseline, already implemented as
`equal_weight` in `solvers/mean_variance.R`.

### 4.2 Inverse-volatility portfolio

$$\tilde a_{i,t} = \frac{1}{\sigma_{i,t}}, \qquad a_{i,t}^{1/\sigma} = \frac{\tilde a_{i,t}}{\sum_{j=1}^{N_t}\tilde a_{j,t}}$$

**Role:** this is the anchor portfolio for **Equity 7** in PBL's anchored-EPO
implementation (confirmed, §8.3) and is already implemented as the
`vol_inverse` anchor in `operators/anchor.R`.
**Volatility estimate — which one, and why this matters:** PBL's own
empirical $\sigma_{i,t}$ (Global samples) is an **EWMA estimate with a
60-day center of mass**, not GARCH — this is a confirmed, direct finding
from the paper's data section, and is worth stating plainly: **PBL's own
published methodology does not use GARCH or GJR-GARCH at all.** This
project's decision to use GJR-GARCH/GARCH(1,1) as the volatility estimator
(`notes/SPECIFICATION.md` §A.3, §IV.7) is therefore an **[ADAPTED]**
extension beyond PBL's own specification, not something PBL itself
recommends or tests — worth being explicit about in any developer-facing
description, since a reader might otherwise assume GARCH is "the PBL risk
model." The options, ordered by fidelity to PBL's own choice:
1. **Rolling historical (realized) volatility** — simplest, not what PBL
   used for their headline Global samples but is what they used for the
   Equity 1–8 samples (60-month/40-day/120-day equal-weighted estimates).
2. **EWMA volatility (60-day center of mass)** — [SOURCED: PBL, Global 1–3
   samples] — exactly PBL's own choice for their strongest empirical
   results.
3. **GARCH(1,1) / GJR-GARCH(1,1)** — [ADAPTED, this project's own extension,
   not in PBL] — see §9 for the full specification and rationale
   (leverage-effect capture).
**Recommendation for this project:** since this project has already
confirmed GJR-GARCH/GARCH as its volatility estimator
(`notes/SPECIFICATION.md`), that decision stands, but it should be
documented — including in any results write-up — as a deliberate departure
from PBL's own empirical implementation, not an implementation detail PBL
specifies. **[UNRESOLVED, developer-facing]** if exact replication of PBL's
published Sharpe ratios is ever desired as a validation step, EWMA
(60-day center of mass) must be used instead, since GARCH will not
numerically reproduce their reported figures.
**Source status of the anchor formula itself:** [SOURCED: PBL, "Equity 7"
description, page-image-verified].

### 4.3 Portfolio return

$$R_{p,t+1} = \sum_{i=1}^{N_t} w_{i,t}R_{i,t+1}$$

**Self-financing long/short formulation:** for a zero-net-investment
long/short book (e.g., simple EPO with a demeaned signal, §3.4/§8.1), gross
exposure $G_t=\sum_i|w_{i,t}|$ and net exposure $E_t=\sum_i w_{i,t}$ are
tracked separately; the portfolio return is still $\sum_i w_i R_{i,t+1}$,
but the **financing** of the short leg (short-sale proceeds, borrow cost)
must be modeled explicitly if the book is not literally zero-net — see
§13's leverage/financing treatment and §11's borrow-fee line item.
**Source status:** [PROPOSED] — standard definition. **Must use simple
returns** (§2.2's rule); this is the point in the pipeline where using log
returns instead would silently produce a wrong portfolio return whenever
weights are not all equal (the log-sum-of-parts ≠ log-of-the-sum error).

---

## 5. Mean–variance optimization

**Objective** [SOURCED: PBL Eq. 2, ADAPTED notation from $x$ to $w$ for
consistency with the rest of this document outside §8]:

$$\max_{\mathbf{w}}\left[\mathbf{w}'\boldsymbol{\mu}-\frac{\gamma}{2}\mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}\right]$$

**Unconstrained solution** [SOURCED: PBL Eq. 3]:

$$\mathbf{w}^{MVO} = \frac{1}{\gamma}\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}$$

**Variables:** $\boldsymbol{\mu}$ expected excess return vector (a signal,
§3, or a historical-mean estimate); $\boldsymbol{\Sigma}$ covariance matrix
(§7); $\gamma$ absolute risk aversion.
**Interpretation:** this portfolio has the highest attainable Sharpe ratio
**if** $\boldsymbol{\mu}$ and $\boldsymbol{\Sigma}$ are measured without
error — PBL's entire paper (§8 below) is about why this assumption fails in
practice and what to do about it. Do not present $\mathbf{w}^{MVO}$ as a
production solver without also implementing the EPO shrinkage in §8; it is
included here as the theoretical baseline every other formula in §6–§8 is
defined relative to.
**Already implemented:** `solvers/mean_variance.R::meanvar_ra` (the
constrained-$\gamma$ variant) and `::tangency_unc`.

**Constrained formulations** (all [PROPOSED] standard QP constraint forms,
not PBL-specific):

| Constraint | Formula |
|---|---|
| Fully invested | $\mathbf{1}'\mathbf{w}=1$ |
| Long-only | $w_i\geq0\ \forall i$ |
| Long/short | no sign restriction; typically paired with a net-exposure or gross-leverage bound below |
| Maximum individual weight | $w_i\leq w_i^{max}$ |
| Gross leverage | $\sum_i|w_i|\leq L_{max}$ |
| Net exposure | $\sum_i w_i = E_{net}$ |
| Turnover | see §14 |
| Liquidity | see §14 |
| Minimum trade size | a post-solve filter: do not execute a rebalancing trade with $|Trade_{i,t}|$ below an exchange- or broker-specific minimum ticket; either round to zero or round up to the minimum, a [PROPOSED] operational choice not fixed by any of the papers here |
| Sector limits | see §14 |

**Numerical issues:** the unconstrained closed form requires $\boldsymbol{\Sigma}$
invertible; when it is not (or is ill-conditioned — the entire motivation
for §7.3/§8), the constrained QP form must be used regardless of whether
box/leverage constraints are otherwise desired, since the closed form is
undefined. **This is precisely the "problem portfolio" phenomenon PBL
identify (§8) — do not treat MVO's numerical fragility as a solver-engineering
problem to patch around; it is the substantive problem §8 exists to solve.**

---

## 6. Global minimum-variance portfolio

$$\min_{\mathbf{w}}\mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}\quad\text{s.t.}\quad\mathbf{1}'\mathbf{w}=1$$

**Unconstrained closed form:**

$$\mathbf{w}^{GMV} = \frac{\boldsymbol{\Sigma}^{-1}\mathbf{1}}{\mathbf{1}'\boldsymbol{\Sigma}^{-1}\mathbf{1}}$$

**Constrained (QP) form:** minimize $\mathbf{w}'\boldsymbol{\Sigma}\mathbf{w}$
subject to $\mathbf{1}'\mathbf{w}=1$ and any of §5's box/leverage/sector
constraints — solved numerically (`quadprog`/`osqp`, per
`notes/SPECIFICATION.md` §IV.22's already-flagged migration off
`constrOptim`), not in closed form once inequality constraints bind.
**Interpretation:** ignores $\boldsymbol{\mu}$ entirely — depends only on
the risk model, and is therefore the portfolio in this document least
sensitive to expected-return estimation error, but still fully exposed to
$\boldsymbol{\Sigma}$ estimation error (§7's shrinkage discussion applies
here as much as to MVO).
**Already implemented:** `solvers/mean_variance.R::min_var`.
**Source status:** [PROPOSED] — classical Markowitz result, not
paper-specific.

---

## 7. Risk model

### 7.1 Sample covariance

$$\hat{\Sigma}_{ij} = \frac{1}{T-1}\sum_{t=1}^{T}(r_{i,t}-\bar r_i)(r_{j,t}-\bar r_j)$$

**Estimation window:** rolling or expanding, per `CONFIG$window_mode` — see
`notes/SPECIFICATION.md` §A.0's flag that the existing `est_window`/`start`
parameters are calibrated for monthly data and require re-derivation for
daily frequency (Task C.1 in that document).
**Source status:** [PROPOSED] — standard estimator.

### 7.2 Volatility–correlation decomposition

$$\boldsymbol{\Sigma}_t = \mathbf{D}_t\mathbf{R}_t\mathbf{D}_t, \qquad \mathbf{D}_t=\operatorname{diag}(\sigma_{1,t},\ldots,\sigma_{N,t})$$

[SOURCED: PBL Eq. 4, which uses lowercase $\sigma$ for the same diagonal
matrix and $\Omega$ for the correlation matrix — this document uses $\mathbf{R}_t$
for correlation to avoid collision with the return symbol $R_{i,t}$ used
throughout §2–§6; PBL's own $\Omega$ notation is preserved inside §8, where
their formulas are reproduced verbatim.]
**Used in:** every risk-model output (§9's $\mathbf{D}_t$ from GARCH, §10's
$\mathbf{R}_t$ from DCC) is assembled into $\boldsymbol{\Sigma}_t$ via this
identity before reaching any solver.

### 7.3 Correlation shrinkage — the EPO formula

$$\mathbf{R}_{w,t} = (1-w)\mathbf{R}_t + w\mathbf{I}, \qquad \boldsymbol{\Sigma}_{w,t}=\mathbf{D}_t\mathbf{R}_{w,t}\mathbf{D}_t$$

[SOURCED: PBL Eq. 19, verified exactly — see §8 for the full derivation and
the exact published notation, $\boldsymbol{\Sigma}_w=(1-w)\tilde{\boldsymbol{\Sigma}}+w\mathbf{V}$,
$\tilde{\boldsymbol{\Sigma}}=\sigma[(1-w)\tilde{\boldsymbol{\Omega}}+w\mathbf{I}]\sigma$.]
**Already implemented:** `operators/shrinkage.R::shrink_corr`.

**Four distinct shrinkage concepts — do not combine their parameters unless
the methodology explicitly requires it, per your instruction:**

1. **Initial risk-model shrinkage** ("pre-shrink," PBL's Global 2:
   $\tilde{\boldsymbol{\Omega}}^{Global\,2}=0.95\tilde{\boldsymbol{\Omega}}^{Global\,1}+0.05\mathbf{I}$,
   verified exactly) — a small, fixed shrinkage applied to condition the raw
   sample correlation matrix before any signal-driven shrinkage. Purpose:
   fix the risk model alone (PBL state 5%–10% is typically sufficient for
   this purpose).
2. **EPO shrinkage** (the $w$ in Eq. 19/§7.3 above) — a much larger
   shrinkage (PBL find $w\approx75\%$ works well in several applications),
   whose purpose is **not** primarily to fix the risk model but to correct
   for **expected-return** estimation error, which PBL show (§8's Eq. 14
   derivation) manifests mathematically as a need for additional correlation
   shrinkage beyond what the risk model alone would justify.
3. **Shrinkage selected to improve covariance estimation on its own terms**
   — e.g., Ledoit-Wolf-style Frobenius-loss-optimal shrinkage (reviewed in
   this project's `notes/shrinkage/`, not implemented) — an analytic,
   in-sample-optimal intensity, conceptually distinct from (2).
4. **Shrinkage selected to maximize realized, out-of-sample portfolio
   performance** — PBL's own $w$-selection procedure (§8.5) is this: an
   *empirical*, Sharpe-ratio-maximizing choice, not derived from any
   estimation-loss formula at all.
**These can be composed** (e.g., apply (1) as a fixed 5% pre-shrink, then
apply (2)/(4) on top, exactly as PBL's Global 2 sample does) **but must not
be conflated into a single parameter** — this project's existing
architecture already keeps them separate (`shrink_corr` can be composed
twice in a `params$ops` pipeline, per `notes/SPECIFICATION.md` §A.3), which
is the correct structure for this distinction.

---

## 8. Enhanced Portfolio Optimization

**Notation for this section only, exactly as published — see the header's
collision warning:** $\mathbf{x}$ = portfolio weights (not $\mathbf{w}$),
$w$ = the EPO shrinkage parameter (not portfolio weights), $\mathbf{s}$ =
signal, $\mathbf{a}$ = anchor portfolio, $\mathbf{V}=\operatorname{diag}(\sigma^2)$
= diagonal variance matrix, $\boldsymbol{\Sigma}_w$ = EPO-shrunk covariance,
$\tilde{\boldsymbol{\Sigma}}$ = the base ("enhanced," pre-$w$-shrinkage) risk
estimate — i.e., the output of §7.3's item (1)/(3) treatments, before item
(2)'s $w$-shrinkage is applied. All equation numbers below are the
**published FAJ numbering**, verified directly against the PDF (text
extraction plus page-image confirmation for Eq. 17–22).

### 8.1 Simple EPO — [SOURCED: PBL Eq. 20]

$$\mathbf{x}^{EPO_s}(w) = \frac{1}{\gamma}\boldsymbol{\Sigma}_{w}^{-1}\mathbf{s}$$

**Derivation context:** this is the special case of the general $EPO(w)$
formula (Eq. 18, below) that arises when the anchor is chosen as
$\mathbf{a}=(1/\gamma)\mathbf{V}^{-1}\mathbf{s}$ — i.e., a
self-referential anchor proportional to the inverse-variance-weighted
signal itself, **not** the absence of an anchor. This is worth stating
explicitly because "simple EPO has no anchor" is a natural but incorrect
simplification; the anchor is present but chosen so it cancels out of the
final expression.
**Interpretation:**
- $w=0$: standard MVO (§5).
- $w\to100\%$: correlations fully shrunk to zero — the covariance matrix
  becomes diagonal, $\boldsymbol{\Sigma}_{100\%}=\mathbf{V}$, and
  $\mathbf{x}^{EPO_s}(100\%) = (1/\gamma)\mathbf{V}^{-1}\mathbf{s}$, i.e., a
  pure inverse-variance-weighted signal portfolio with no correlation
  information used at all.
- Intermediate $w$: a smooth interpolation, **not** a mixture of two
  separately-computed portfolios — the shrinkage acts inside the matrix
  inversion, not as a post-hoc blend (contrast with anchored EPO, §8.3,
  where a literal blend does appear).
**Role of $\gamma$:** [SOURCED: PBL, verified] Eq. 20 is **linear in risk
tolerance**, so the Sharpe ratio of $\mathbf{x}^{EPO_s}(w)$ does not depend
on $\gamma$ at all — PBL explicitly recommend setting $\gamma=1$ "or any
other number that corresponds to a desirable level of risk" purely for
sizing, since it has no effect on risk-adjusted performance. **This $\gamma=1$
recommendation is specific to simple EPO's scale-invariance property and
must not be read as general risk-aversion guidance** — see the explicit
warning already recorded in `notes/SPECIFICATION.md` §IV.12 distinguishing
this from classical MVO's genuine, preference-reflecting $\gamma$.
**Normalization/vol-scaling:** Eq. 20 as stated is not normalized to sum to
1 or to any fixed gross exposure; production use should apply §13's
volatility targeting on top.
**Used in:** L3 solver, already implemented as `solvers/mean_variance.R::epo`
combined with `operators/shrinkage.R::shrink_corr`.

### 8.2 General EPO — [SOURCED: PBL Eq. 17]

Presented before the practical simplified versions, per your instruction,
as PBL themselves derive it:

$$EPO = \frac{1}{\gamma}(\tau\tilde{\boldsymbol{\Sigma}}+\boldsymbol{\Lambda})^{-1}(\tau\mathbf{s}+\gamma\boldsymbol{\Lambda}\mathbf{a})$$

**Variables:** $\tau$ the magnitude of shocks to true expected returns
(from PBL's Bayesian prior, Eq. 12: $\boldsymbol{\mu}=\gamma\tilde{\boldsymbol{\Sigma}}\mathbf{a}+\boldsymbol{\eta}$,
$\boldsymbol{\eta}\sim N(0,\tau\tilde{\boldsymbol{\Sigma}})$); $\boldsymbol{\Lambda}$
the covariance of measurement error in the signal $\mathbf{s}$ (from
$\mathbf{s}=\boldsymbol{\mu}+\mathbf{e}$, $\mathbf{e}\sim N(0,\boldsymbol{\Lambda})$).
**Derivation lineage** [SOURCED: PBL Propositions 1–3, verified]: Eq. 17
unifies two independently-derived results that PBL prove are
identical solutions — a **Bayesian** estimator (PBL Eq. 14, following a
Black-Litterman-style prior but with different notation and, critically, a
*general* anchor rather than always the market portfolio) and a **robust
optimization** solution (PBL Eq. 16, a max-min formulation over an ellipsoidal
uncertainty set for $\boldsymbol{\mu}$). PBL's Proposition 3 (verified)
further shows Eq. 17 nests standard MVO ($\tilde{\boldsymbol{\Sigma}}=\boldsymbol{\Sigma}$,
$\boldsymbol{\Lambda}=0$), the anchor alone ($\tau=0$, "reverse MVO"), the
Black-Litterman estimator (when $\mathbf{a}$ is the market portfolio and
$\boldsymbol{\Sigma}$ has no estimated error), and a generalized ridge
regression.
**Practical parameters:** $\tilde{\boldsymbol{\Sigma}}$ and $\mathbf{s}$ are
directly estimable (§7, §3); $\mathbf{a}$, $\gamma$, $\tau$, and
$\boldsymbol{\Lambda}$ are, in PBL's own words, "tricky" — resolved in
practice via the assumption below (§8.3).
**Used in:** the theoretical basis for §8.1 and §8.3; not implemented
directly (its "tricky" parameters are exactly what §8.3's $w$-reparametrization
eliminates).

### 8.3 Anchored EPO — [SOURCED: PBL Eq. 18, 19, 21, 22]

**Practical reparametrization** (assuming $\boldsymbol{\Lambda}=\lambda\mathbf{V}$
— measurement-error noise independent across assets, proportional to each
asset's own variance):

$$EPO(w) = \boldsymbol{\Sigma}_{w}^{-1}\left[(1-w)\frac{1}{\gamma}\mathbf{s}+w\mathbf{V}\mathbf{a}\right] \qquad \text{(PBL Eq. 18)}$$

$$\boldsymbol{\Sigma}_w = (1-w)\tilde{\boldsymbol{\Sigma}}+w\mathbf{V} = \sigma\left[(1-w)\tilde{\boldsymbol{\Omega}}+w\mathbf{I}\right]\sigma \qquad \text{(PBL Eq. 19)}$$

where $w:=\lambda/(\tau+\lambda)\in[0,1]$ is the **EPO shrinkage parameter**
— the reparametrization's entire benefit (PBL, verified) is that the two
"tricky" parameters $\lambda$ and $\tau$ collapse into tracking only their
*relative* magnitude via this single $w$.

**Endogenous risk aversion** — used when the signal's scale is unknown
(e.g., a momentum sign or a valuation rank, not literally "2% expected
return"), verified by direct page-image inspection [SOURCED: PBL Eq. 21]:

$$\gamma = \frac{\sqrt{\mathbf{s}'\boldsymbol{\Sigma}_{w}^{-1}\tilde{\boldsymbol{\Sigma}}\boldsymbol{\Sigma}_{w}^{-1}\mathbf{s}}}{\sqrt{\mathbf{a}'\tilde{\boldsymbol{\Sigma}}\mathbf{a}}}$$

**Derivation logic (verified from PBL's own text):** Eq. 18 is "essentially
a mixture of the anchor portfolio and the portfolio
$\boldsymbol{\Sigma}_w^{-1}(1/\gamma)\mathbf{s}$" — $\gamma$ is chosen to
**equalize the variance** of these two component portfolios (i.e., set
$\operatorname{Var}(\mathbf{a})=\operatorname{Var}(\boldsymbol{\Sigma}_w^{-1}(1/\gamma)\mathbf{s})$
under the base risk estimate $\tilde{\boldsymbol{\Sigma}}$), which yields
Eq. 21 directly.

**Complete anchored EPO solution** — substituting Eq. 21 into Eq. 18
[SOURCED: PBL Eq. 22, verified exactly by page image]:

$$\mathbf{x}^{EPO_a}(w) = \boldsymbol{\Sigma}_{w}^{-1}\left[(1-w)\frac{\sqrt{\mathbf{a}'\tilde{\boldsymbol{\Sigma}}\mathbf{a}}}{\sqrt{\mathbf{s}'\boldsymbol{\Sigma}_{w}^{-1}\tilde{\boldsymbol{\Sigma}}\boldsymbol{\Sigma}_{w}^{-1}\mathbf{s}}}\mathbf{s}+w\mathbf{V}\mathbf{a}\right]$$

**This is the exact PBL form. The approximate expression
$(1-w)\mathbf{a}+w\boldsymbol{\Sigma}_w^{-1}\mathbf{s}$ is explicitly
rejected as a substitute** — it is not what PBL derive; it omits the
endogenous-$\gamma$ scaling term entirely and would materially misstate the
blend between signal and anchor.
**Independent verification against this project's own code:** this formula
matches `operators/anchor.R::anchor_blend`'s `"endogenous"` mode exactly —
`k <- sqrt(num/den)` where `num = a'Σ̃a`, `den = y'Σ̃y`, `y = Σ_w⁻¹s` (and
$y'\tilde{\boldsymbol{\Sigma}}y \equiv \mathbf{s}'\boldsymbol{\Sigma}_w^{-1}\tilde{\boldsymbol{\Sigma}}\boldsymbol{\Sigma}_w^{-1}\mathbf{s}$
since $\boldsymbol{\Sigma}_w^{-1}$ is symmetric). This closes the citation-
verification item `notes/covariance/rmt_background.md` had left open
(SSRN-vs-FAJ equation numbering) — **the codebase's implementation is
confirmed correct against the published paper, with the correct FAJ
equation numbers being 18/19/21/22, not the SSRN preprint's 7/14/16/17 the
in-code comments currently cite.** [DEVELOPER TASK] update the comments in
`operators/anchor.R` and `operators/shrinkage.R` to cite the verified FAJ
numbers.
**Fixed-$\gamma$ alternative** [SOURCED: PBL Eq. 14/18's fixed-$\gamma$
mode]: $EPO(w) = \boldsymbol{\Sigma}_w^{-1}[(1-w)(1/\gamma)\mathbf{s}+w\mathbf{V}\mathbf{a}]$
with $\gamma$ chosen directly rather than solved endogenously — PBL note a
typical range of **$\gamma\in[1,10]$ based on investor preference** when
using this mode, verified directly from the text. This is the general
risk-aversion range already recorded in `notes/SPECIFICATION.md` §IV.12
(refined there to "roughly 2–10" from general CRRA literature before this
paper was available — **PBL's own stated range is 1–10; update the earlier
note to cite PBL directly rather than a generic literature estimate**).
**Already implemented:** `operators/anchor.R::anchor_blend`, both
`"endogenous"` (Eq. 21/22) and fixed-$\gamma$ (Eq. 14/18) modes.

### 8.4 Inverse-volatility anchor

$$a_{i,t} = \frac{\sigma_{i,t}^{-1}}{\sum_{j=1}^{N_t}\sigma_{j,t}^{-1}}$$

Identical to §4.2 — repeated here in EPO's own notation for completeness.
**Relation to risk allocation:** this anchor assigns **equal standalone
(marginal, uncorrelated) volatility** to each asset — it is **not**
equivalent to equal *portfolio* risk contribution once correlations are
nonzero, since two assets with equal standalone volatility but different
average correlation to the rest of the book contribute unequally to total
portfolio variance. True equal-risk-contribution is a different, nonlinear
construction (PBL's own text references this distinction, citing Baltas
2015 and Yang et al. 2019's equal-risk-contribution TSMOM portfolios as a
related but separate concept from their own anchor choice — verified).

### 8.5 Selection of the EPO shrinkage parameter — [SOURCED: PBL, in-text procedure + Table 2/Figure 2 notes]

**PBL's own procedure, verified against both the main text and the Figure 2
table note:**

1. Define a grid $w\in\mathcal{W}\subseteq[0,1]$ — PBL state "a finite grid
   of possible values" without publishing the exact grid points in the text
   available; Table 2 reports results at $\{0\%,10\%,25\%,50\%,75\%,90\%,99\%,100\%\}$,
   which is a reasonable **[ADAPTED]** default grid to use if PBL's own
   internal grid is not otherwise recoverable, but is not confirmed to be
   the literal grid used for their live $w$-selection (Table 2's grid
   appears to be a reporting choice, for the fixed-$w$ comparison rows
   specifically, not necessarily identical to the OOS-selection grid).
2. At each decision date $t$, for each candidate $w$, backtest using **only
   information available before $t$** — an **expanding window** (PBL's own
   description: "the time period up until today"; not a fixed-length
   rolling window).
3. Compute each candidate's realized Sharpe ratio over that expanding
   history.
4. Select $w_t^* = \arg\max_{w\in\mathcal{W}}\widehat{SR}_t^{OOS}(w)$.
5. Apply $w_t^*$ to the **next** period only (not retroactively) — this is
   the look-ahead-bias control: $w_t^*$ is chosen using data through $t$ and
   used to trade at $t+1$.
**Initial training period:** PBL began each backtest 15 years after the
earliest available data for that sample specifically to ensure a reasonable
amount of history exists for the *first* OOS $w$-selection (verified,
stated explicitly for both the Global and Equity samples).
**Rolling vs. expanding — confirmed expanding**, not rolling: PBL's own
wording ("the time period up until today," not "the trailing $N$ years")
supports expanding, and this project's own prior design note
(`notes/ROADMAP.md`, "OOS w-selection... adaptive per-period Sharpe-max")
should be updated to state expanding explicitly if not already.
**Ties:** [UNRESOLVED] — not addressed in the verified text; a
[PROPOSED] tie-break (e.g., prefer the larger $w$, on the grounds that more
shrinkage is the more conservative/lower-variance choice when performance is
statistically indistinguishable) should be adopted explicitly and
documented, not left to whatever an argmax implementation happens to do on
ties.
**Look-ahead prevention:** enforced structurally by using only
$t' \le t$ data for the $w_t^*$ selection and applying it only to $t+1$'s
trade — the same discipline as any walk-forward parameter selection
elsewhere in this system (`notes/SPECIFICATION.md`'s L5 layer).
**Empirical finding, for context (PBL, verified):** $w\approx75\%$ worked
well "in several applications" — this is descriptive of PBL's results, not
a rule to hardcode in place of running the actual OOS procedure.

---

## 9. GARCH volatility models

### 9.1 Standard GARCH(1,1) — [PROPOSED synthesis of Bollerslev (1986); not from PBL, who use EWMA instead — see §4.2's explicit note]

$$r_{i,t} = \mu_{i,t}+\varepsilon_{i,t}, \qquad \varepsilon_{i,t}=\sigma_{i,t}z_{i,t}, \qquad \sigma_{i,t}^2 = \omega_i+\alpha_i\varepsilon_{i,t-1}^2+\beta_i\sigma_{i,t-1}^2$$

**Restrictions:** $\omega_i>0$, $\alpha_i\ge0$, $\beta_i\ge0$; covariance
stationarity requires $\alpha_i+\beta_i<1$.
**Initialization:** $\sigma_{i,0}^2$ typically set to the unconditional
sample variance $\hat\omega_i/(1-\hat\alpha_i-\hat\beta_i)$ once parameters
are estimated, or to a burn-in-period sample variance before the first few
observations stabilize the recursion.
**Distributional assumption:** $z_{i,t}$ is typically assumed Gaussian for
QMLE estimation (consistent even if the true distribution is fat-tailed,
under standard regularity conditions) or Student-$t$ for a better fit to
equity return kurtosis — **[UNRESOLVED]** which is used in production is
not yet decided; Student-$t$ is the more defensible choice for daily equity
data but adds one estimated degrees-of-freedom parameter per asset.
**Rolling vs. expanding estimation:** [UNRESOLVED] — not fixed by this
document; re-estimating GARCH parameters on every rolling window is
standard but computationally heavier than periodic re-estimation with
daily-updated conditional variance in between. **[PROPOSED]** re-estimate
parameters on a lower-frequency cadence (e.g., monthly) while updating
$\sigma_{i,t}^2$ via the recursion daily using the latest parameters — a
common practitioner compromise, not fixed by any source here.
**Convergence failures / fallback hierarchy:** if MLE fails to converge, or
returns a boundary solution, fall back to §2.3-consistent rolling historical
volatility (§4.2, option 1) for that asset in that period — automatic, not
manual, per the "fail small and predictably" system philosophy already
established (`notes/SPECIFICATION.md` §I.2).

### 9.2 GJR-GARCH(1,1) — preferred model, GARCH(1,1) fallback

$$\sigma_{i,t}^2 = \omega_i+\alpha_i\varepsilon_{i,t-1}^2+\gamma_i\,\mathbb{1}(\varepsilon_{i,t-1}<0)\,\varepsilon_{i,t-1}^2+\beta_i\sigma_{i,t-1}^2$$

[SOURCED: Glosten, Jagannathan & Runkle (1993), *Journal of Finance* 48(5).]
**Leverage effect:** $\gamma_i>0$ captures the well-documented asymmetry in
equity volatility — a negative return raises subsequent conditional
volatility more than an equally-sized positive return (Black 1976; Christie
1982) — already discussed at length in `notes/SPECIFICATION.md` §IV.7; not
repeated here beyond the formula and restriction.
**Restrictions:** $\omega_i>0$, $\alpha_i\ge0$, $\beta_i\ge0$,
$\alpha_i+\gamma_i\ge0$ (so conditional variance stays non-negative even on
the largest admissible negative shock), and
$\alpha_i+\beta_i+\tfrac{1}{2}\gamma_i<1$ for covariance stationarity
(the $\tfrac12$ reflects $\varepsilon_{t-1}<0$ roughly half the time under
symmetric innovations).
**Fallback hierarchy** (already confirmed project decision, restated here
with the numerical trigger conditions): fall back to plain GARCH(1,1) (§9.1)
when (a) history is too short/ragged to identify $\gamma_i$ reliably, or (b)
GJR MLE fails to converge or returns $\gamma_i$ at a constraint boundary.
Fall back further to §4.2's rolling historical volatility if GARCH(1,1)
itself fails.
**PBL relationship — restated for emphasis:** neither GARCH(1,1) nor
GJR-GARCH is used anywhere in PBL's own published implementation; both are
this project's own, independently-motivated extension to the risk-model
layer, layered underneath the (PBL-sourced) EPO shrinkage machinery in §7–§8.

---

## 10. DCC correlation model

**Standardized residuals:**

$$\mathbf{z}_t = \mathbf{D}_t^{-1}\boldsymbol{\varepsilon}_t$$

**Dynamic covariance process** [SOURCED: Engle (2002), *Journal of Business
& Economic Statistics* 20(3)]:

$$\mathbf{Q}_t = (1-a-b)\bar{\mathbf{Q}}+a\,\mathbf{z}_{t-1}\mathbf{z}_{t-1}'+b\,\mathbf{Q}_{t-1}$$

**Conditional correlation matrix:**

$$\mathbf{R}_t = \operatorname{diag}(\mathbf{Q}_t)^{-1/2}\,\mathbf{Q}_t\,\operatorname{diag}(\mathbf{Q}_t)^{-1/2}$$

**Restrictions:** $a\ge0$, $b\ge0$, $a+b<1$.
**Full conditional covariance:** $\mathbf{H}_t=\mathbf{D}_t\mathbf{R}_t\mathbf{D}_t$
(identical structural role to §7.2's $\boldsymbol{\Sigma}_t$).

**cDCC** [SOURCED: Aielli (2013), *Journal of Business & Economic
Statistics* 31(3)] — the corrected updating equation replaces the plain
$\mathbf{z}_{t-1}\mathbf{z}_{t-1}'$ term with a version rescaled by the
lagged correlation-implied standard deviations,
$\mathbf{Q}_t = (1-a-b)\bar{\mathbf{Q}}+a\left(\mathbf{q}_{t-1}^{1/2}\odot\mathbf{z}_{t-1}\right)\left(\mathbf{q}_{t-1}^{1/2}\odot\mathbf{z}_{t-1}\right)'+b\,\mathbf{Q}_{t-1}$,
where $\mathbf{q}_{t-1}=\operatorname{diag}(\mathbf{Q}_{t-1})$ and $\odot$ is
elementwise multiplication. **Why it matters:** the original Engle (2002)
two-step estimator has a known finite-sample inconsistency — $E[\mathbf{Q}_t]\ne\bar{\mathbf{Q}}$
in general under the plain recursion, because $\mathbf{z}_t$'s covariance is
$\mathbf{R}_t$, not $\mathbf{Q}_t$, and the original recursion conflates the
two. Aielli's correction restores consistency of the targeted
$\bar{\mathbf{Q}}$.
**This project's status:** cDCC, not vanilla DCC, is the confirmed choice
(`notes/SPECIFICATION.md` §A.3/§VI.2) — a genuine correction to adopt, not
an optional refinement.
**Relative to the original PBL implementation:** **PBL's paper uses neither
DCC nor cDCC anywhere.** Their dynamic risk model is EWMA-based (§4.2). DCC/
cDCC is this project's own, separately-motivated extension for capturing
time-varying correlation beyond what a static or EWMA estimate provides —
**[EXPERIMENTAL/CONFIRMED-in-build-path, but explicitly not part of PBL's
methodology]**, and should be documented as such rather than implied to be
part of "the PBL risk model."
**DECO** (Engle & Kelly, 2012) — a single equicorrelation across all pairs,
the confirmed large-N fallback, unchanged from `notes/SPECIFICATION.md`
§A.3 — not repeated in full here.
**Routing rule** (already confirmed, restated for completeness): feed the
SAA optimizer a slow-refreshed, shrunk correlation estimate (§7.3's
machinery applied to DCC's $\bar{\mathbf{Q}}$ before the recursion runs);
feed the regime layer the fast, daily $\mathbf{R}_t$ as a
correlation-breakdown diagnostic.

---

## 11. Transaction costs

### 11.1 Static proportional cost (ex-post deduction)

$$TC_t = \sum_{i=1}^{N}c_{i,t}\left|w_{i,t}^{target}-w_{i,t}^{pre}\right|$$

**Pre-trade weight, after asset returns have drifted the portfolio away
from yesterday's target:**

$$w_{i,t}^{pre} = \frac{w_{i,t-1}(1+R_{i,t})}{1+R_{p,t}}$$

**Turnover** (one-way, half-sum convention):

$$TO_t = \frac{1}{2}\sum_{i=1}^{N}\left|w_{i,t}^{target}-w_{i,t}^{pre}\right|$$

Also report gross (non-halved) one-way turnover,
$\sum_i|w_{i,t}^{target}-w_{i,t}^{pre}|$, alongside the halved figure if the
convention used by a comparison source (e.g., an external benchmark report)
differs — state which convention is used wherever a turnover number is
reported, since the two differ by exactly 2× and silently mixing them
produces incomparable figures.
**Net portfolio return:** $R_{p,t}^{net}=R_{p,t}^{gross}-TC_t$.
**Source status:** [PROPOSED] — standard construction, not attributed to a
specific paper (distinct from the GP quadratic-cost framework in §11.2,
which is a genuinely different optimization paradigm, not just a different
formula for the same cost).

### 11.2 Ex-ante turnover-penalized optimization (single-period)

$$\max_{\mathbf{w}_t}\left[\mathbf{w}_t'\boldsymbol{\mu}_t-\frac{\gamma}{2}\mathbf{w}_t'\boldsymbol{\Sigma}_t\mathbf{w}_t-\frac{\lambda}{2}(\mathbf{w}_t-\mathbf{w}_t^{pre})'\boldsymbol{\Lambda}_t(\mathbf{w}_t-\mathbf{w}_t^{pre})\right]$$

**Source status — now resolved, per your instruction not to attribute
until verified:** **[SOURCED: Gârleanu & Pedersen (2013), Eq. 3's cost
function $TC(\Delta x_t)=\tfrac12\Delta x_t'\Lambda\Delta x_t$ combined with
Eq. 2's single-period objective term.]** This single-period expression is
the per-period building block of GP's full multi-period objective (§11.3);
it is a correct and properly-sourced special case, not an unverified
invented formula — the earlier draft of this document (before GP was
available) correctly declined to attribute it; that caveat is now resolved.
**Variables:** $\boldsymbol{\Lambda}_t$ GP's trading-cost matrix (symmetric
positive-definite; $TC(\Delta\mathbf{w}_t)=\tfrac12\Delta\mathbf{w}_t'\boldsymbol{\Lambda}_t\Delta\mathbf{w}_t$,
GP Eq. 3, verified) — a multidimensional Kyle's-lambda, interpretable as the
price impact of trading $\Delta\mathbf{w}_t$ (GP's own explanation,
verified: trading $\Delta x_t$ shares moves the average price by
$\tfrac12\Lambda\Delta x_t$, so total cost is $\Delta x_t$ times the price
move). Under GP's **Assumption 1** (verified): $\boldsymbol{\Lambda}_t=\lambda\boldsymbol{\Sigma}_t$
— transaction costs proportional to the amount of risk traded, which both
simplifies the solution (§11.3) and is "implied by the model of Gârleanu,
Pedersen, and Poteshman (2009)" (GP's own citation, verified).

### 11.3 Full Gârleanu-Pedersen dynamic trading model — [SOURCED: GP Eq. 1–13] — **[DECIDED: NOT BUILT — reference only]**

**Decision: the project stops at §11.2's single-period turnover penalty.**
The full multi-period model below is **not being implemented** — retained
in this document as the sourced, verified reference derivation (so the
scope decision is documented against the actual model being declined, not
against a vague description of it), and in case the decision is revisited
once a multi-factor signal decomposition exists (see the blocking
dependency noted below). Do not build against this subsection without a new
decision superseding this one.

**This is the complete multi-period model, not only the single-period
building block above.** Included per your original instruction to provide
the dynamic trading objective and optimal partial-adjustment rule rather
than only a static deduction, and retained for reference under the decision
above.

**Return-predicting factor model** (GP Eq. 1–2):

$$\mathbf{r}_{t+1} = \mathbf{B}\mathbf{f}_t+\mathbf{u}_{t+1}, \qquad \Delta\mathbf{f}_{t+1}=-\boldsymbol{\Phi}\mathbf{f}_t+\boldsymbol{\varepsilon}_{t+1}$$

**Variables:** $\mathbf{f}_t$ a $K\times1$ vector of return-predicting
factors (e.g., distinct signals with different mean-reversion speeds —
GP's own motivating example is a fast-decaying momentum signal alongside a
slow-decaying value signal); $\mathbf{B}$ an $S\times K$ factor-loading
matrix; $\mathbf{u}_{t+1}$ unpredictable noise, $\operatorname{var}_t(\mathbf{u}_{t+1})=\boldsymbol{\Sigma}$;
$\boldsymbol{\Phi}$ a $K\times K$ matrix of mean-reversion (alpha decay)
coefficients; $\boldsymbol{\varepsilon}_{t+1}$ factor shocks,
$\operatorname{var}_t(\boldsymbol{\varepsilon}_{t+1})=\boldsymbol{\Omega}$.

**Quadratic transaction cost** (GP Eq. 3): $TC(\Delta\mathbf{x}_t)=\tfrac12\Delta\mathbf{x}_t'\boldsymbol{\Lambda}\Delta\mathbf{x}_t$.

**Dynamic objective** (GP Eq. 4):

$$\max_{x_0,x_1,\ldots}\ E_0\left[\sum_t(1-\rho)^{t+1}\left(\mathbf{x}_t'\mathbf{r}_{t+1}-\frac{\gamma}{2}\mathbf{x}_t'\boldsymbol{\Sigma}\mathbf{x}_t\right)-\frac{(1-\rho)^t}{2}\Delta\mathbf{x}_t'\boldsymbol{\Lambda}\Delta\mathbf{x}_t\right]$$

**Variables:** $\rho\in(0,1)$ discount rate; $\gamma$ risk aversion
(equivalent role to §5/§8's $\gamma$, but here in a multi-period setting).
**The optimal policy — "trade partially toward the aim"** (GP Proposition 2,
Eq. 10, under Assumption 1's $\boldsymbol{\Lambda}=\lambda\boldsymbol{\Sigma}$):

$$\mathbf{x}_t = \left(1-\frac{a}{\lambda}\right)\mathbf{x}_{t-1}+\frac{a}{\lambda}\,\mathbf{aim}_t$$

where the scalar trading rate $a/\lambda<1$ solves (GP Eq. 9):

$$a = \frac{-(\gamma(1-\rho)+\lambda\rho)+\sqrt{(\gamma(1-\rho)+\lambda\rho)^2+4\gamma\lambda(1-\rho)^2}}{2(1-\rho)}$$

**The aim portfolio — "aim in front of the target"** (GP Proposition 3, Eq.
11–13): letting $\mathbf{Markowitz}_t=(\gamma\boldsymbol{\Sigma})^{-1}\mathbf{B}\mathbf{f}_t$
(the static, no-transaction-cost optimum — "the Markowitz portfolio," GP
Eq. 11) and $z=\gamma/(\gamma+a)$:

$$\mathbf{aim}_t = z\,\mathbf{Markowitz}_t+(1-z)E_t(\mathbf{aim}_{t+1}) = \sum_{\tau=t}^{\infty}z(1-z)^{\tau-t}E_t(\mathbf{Markowitz}_\tau)$$

**Interpretation:** the investor does not trade toward today's Markowitz
portfolio; the aim portfolio is a forward-looking, exponentially-weighted
average of the **current and all expected future** Markowitz portfolios,
with faster-decaying signals (higher $\boldsymbol{\Phi}$ eigenvalues)
receiving less weight in the aim than slower-decaying ones, since their
predictive content will have faded by the time a slowly-traded position can
be built. The trading rate $a/\lambda$ is independent of the current
portfolio $\mathbf{x}_{t-1}$ — every period, the investor closes a fixed
*fraction* of the gap to the aim, not a fixed *amount*.
**Comparative statics** (GP, verified): the trading rate is decreasing in
transaction costs $\lambda$ and increasing in risk aversion $\gamma$ (higher
$\gamma$ makes deviating from the aim more painful relative to the cost of
trading toward it).
**Relative to this project's existing rebalancing framework:** this is a
**materially more sophisticated model** than the calendar/threshold/hybrid
rebalancing rules already specified (`notes/SPECIFICATION.md` §IV.15,
§V.18). Implementing GP's full model requires (a) an explicit multi-factor
signal decomposition with estimated mean-reversion speeds
$\boldsymbol{\Phi}$ per factor — not currently part of this project's L1
signal layer, which treats each strategy's signal as a single combined
score, not a vector of separately-decaying factors — and (b) solving the
Riccati-equation-based coefficient matrices $A_{xx}$, $A_{xf}$, $A_{ff}$ (GP
Eq. 6, Appendix), a nontrivial numerical component beyond anything currently
in `core/engine.R`. **[DECIDED]** the project uses the simpler single-period
turnover penalty (§11.2) rather than building this engine — resolved, not
deferred; §11.2 is the confirmed transaction-cost-in-the-objective
treatment. Revisit only if a genuine multi-factor, differentially-decaying
signal architecture is later adopted at L1, since that is the actual
prerequisite this model needs and does not currently exist.

**Distinguishing the three transaction-cost treatments, explicitly, per
your instruction:**
1. **Ex-post deduction** (§11.1) — compute target weights ignoring costs
   entirely, then subtract realized $TC_t$ from realized return. Simplest;
   does not change the portfolio that is traded, only how its net
   performance is reported.
2. **Turnover-penalized optimization** (§11.2) — costs enter the objective
   the optimizer solves, so the *chosen* weights themselves are
   cost-aware, but only one period ahead.
3. **Optimal dynamic trading with quadratic costs** (§11.3, full GP) —
   costs enter a genuinely multi-period objective; the optimal policy
   explicitly trades toward where predictors are *expected to be*, not just
   where they are today, and the partial-adjustment trading rate is itself
   derived from the cost/risk-aversion trade-off rather than chosen
   heuristically (e.g., as a fixed rebalancing band, §12.2). **Not
   implemented, per the decision above — listed for completeness of the
   conceptual distinction, not as a build target.**

### 11.4 Additional cost components — [PROPOSED, project-specific, already itemized in `notes/SPECIFICATION.md` §VII.5]

Commissions (Nordnet Mini tiers, confirmed rates); bid-ask spreads and
market impact (modeled separately from commission, half-spread ×
ADV-participation for thin OSE names); FX conversion costs (§2.5's currency
conversion, cost side per §II.8/§A.1a); fixed ticket costs and minimum
commissions (Nordnet Mini's ~52,667 NOK breakeven, already derived); financing
costs (the leverage-overlay financing rate, distinct from the risk-free rate
— `notes/SPECIFICATION.md` §IV.14's corrected formula); borrow fees for
short positions (**[OPEN]** no specific Nordnet short-borrow rate has been
researched or confirmed in this project to date — do not assume a figure).

---

## 12. Rebalancing

### 12.1 Calendar-based rebalancing

Target weights computed and (subject to §11's cost model) traded to on
predetermined dates — daily, weekly, monthly, or quarterly. [PROPOSED]
simplest, most predictable turnover profile; does not respond to
intraperiod drift magnitude.

### 12.2 Band (threshold) rebalancing

$$\left|w_{i,t}^{pre}-w_{i,t}^{target}\right| > b_i$$

triggers a rebalancing trade in asset $i$.
**Interpretation of "4%" — resolved per your instruction, treated as
percentage points unless otherwise confirmed:** for $b_i=0.04$, this
document treats the band as **four percentage points of portfolio weight**
(e.g., a target of 10% triggers at drift to 6% or 14%), **not** 4% relative
to the target (which would trigger at 9.6%/10.4% for the same 10% target —
a much tighter, more turnover-inducing band) and not 4% of total portfolio
value in some other aggregated sense. **[UNRESOLVED]** this is stated as
the working assumption per your explicit instruction, not as a confirmed
design decision from a prior conversation — flagged in Table C for
final confirmation before implementation, since the three interpretations
produce materially different turnover and are easy to conflate silently in
code (e.g., comparing a weight *difference* against a *relative* threshold
by mistake).
**Trade execution on breach — [UNRESOLVED, Table C]:** four distinct
policies are possible and this document does not assume one:
(a) rebalance the *entire* portfolio to target once any single asset
breaches its band; (b) trade *only* the breached position(s) back to
target, leaving others to drift; (c) return breached positions fully to
target; (d) move breached positions only back to the nearest band boundary
(a smaller trade than full reversion to target, reducing turnover further).
**[PROPOSED default, pending confirmation]** policy (b) combined with (c) —
trade only the assets that actually breached, and return each fully to its
target weight — is the most common practitioner convention and the
[PROPOSED] default, but this has not been confirmed as this project's
choice and must not be assumed correct without sign-off.

---

## 13. Volatility targeting and leverage

$$L_t = \frac{\sigma^{target}}{\hat\sigma_{p,t}}, \qquad 0\le L_t\le L_{max}$$

$$\mathbf{w}_t^{scaled} = L_t\,\mathbf{w}_t, \qquad w_{f,t} = 1-\mathbf{1}'\mathbf{w}_t^{scaled}$$

$$R_{p,t}^{lev} = L_t R_{risky,t}+(1-L_t)r_{f,t}-FC_t$$

**Variables:** $w_{f,t}$ the residual cash/financing weight (negative when
$L_t>1$, i.e., the position is leveraged and the "cash weight" represents
borrowing); $FC_t$ any financing spread beyond the risk-free rate.
**Consistency with `notes/SPECIFICATION.md`'s already-corrected leverage
overlay:** this is the same construction as that document's §IV.14
`apply_overlay()` formula, restated with $L_t$ in place of that document's
$l$ for consistency with this section's own notation — **the financing-cost
correction already specified there applies identically here**: $FC_t$ must
be the actual financing rate paid (confirmed Nordnet margin rate, 7.32%
effective NOK), not the risk-free rate $r_{f,t}$ used elsewhere in the same
formula for the *unlevered* cash return — conflating the two was the
originally-identified bug, already fixed in the master specification and
not reintroduced here.
**Leveraged ETF implementation** — daily reset and compounding: **[SOURCED:
derivation in `notes/SPECIFICATION.md` §IV.14]**, restated:
$V_T/V_0=\prod_t(1+k\cdot r_t)$; $\ln(V_T/V_0)\approx k\sum_t r_t-\tfrac12k(k-1)\sum_t r_t^2\approx k\sum_t r_t-\tfrac12k(k-1)\sigma^2T$.
This applies to any frequently-rebalanced constant-leverage-ratio strategy,
not only ETF-wrapped ones (already established at length in the master
specification's leverage discussion; not re-derived here). **Distinct
Nordnet OSE-leg vehicle:** mini futures/certificates use a financing-level/
knock-out-barrier structure, not this compounding formula — that
instrument's own mathematics remains **[OPEN]**, per
`notes/SPECIFICATION.md` §IV.15/§XI.8, unresolved by this document.

---

## 14. Portfolio constraints

| Constraint | Formula | Source status |
|---|---|---|
| Fully invested | $\mathbf{1}'\mathbf{w}=1$ | [PROPOSED], standard |
| Long only | $w_i\ge0$ | [PROPOSED], standard |
| Position limit | $w_i^{min}\le w_i\le w_i^{max}$ | [PROPOSED], standard |
| Gross leverage | $\lVert\mathbf{w}\rVert_1=\sum_i|w_i|\le L_{max}$ | [PROPOSED], standard |
| Turnover | $\sum_i|w_{i,t}-w_{i,t}^{pre}|\le TO_{max}$ | [PROPOSED]; the soft-penalty form (§11.2's $\lambda$ term) is the confirmed preference over this hard cap, per `notes/SPECIFICATION.md` §IV.22, since a hard cap can render the problem infeasible |
| Liquidity | $|Trade_{i,t}|\le\kappa\cdot ADV_{i,t}$ | [PROPOSED]; blocked on populating `data/OSE Data/Liquidity/` (currently empty, per master spec) |
| Minimum holdings | $\sum_i\mathbb{I}(w_i\ne0)\ge K_{min}$ | [PROPOSED]; **cardinality constraints are non-convex** — see note below |
| Maximum holdings | $\sum_i\mathbb{I}(w_i\ne0)\le K_{max}$ | [PROPOSED]; same non-convexity note |

**Cardinality constraints — algorithmic treatment required.** $\sum_i\mathbb{I}(w_i\ne0)$
is a non-convex, combinatorial function of $\mathbf{w}$; it cannot be added
directly to the QP solvers already used elsewhere in this system
(`quadprog`/`osqp`, per the confirmed migration off `constrOptim`). Two
standard approaches, neither yet adopted as a project decision:
1. **Mixed-integer QP (MIQP)** — introduce a binary indicator per asset and
   solve exactly; correct but materially heavier computationally, and would
   require a different solver library than the continuous QP tools already
   planned.
2. **Heuristic post-processing** — solve the continuous problem, then
   truncate the smallest positions to zero and re-solve/re-normalize among
   the remainder; simpler, no new solver dependency, but not
   provably optimal.
**[UNRESOLVED DESIGN DECISION, Table C]** — whether MIQP is ever justified
given this system's scale, or whether the heuristic approach is adopted as
the permanent policy; not decided by this document.

---

## 15. Performance and risk measures

$$\hat\mu_{ann} = F\bar R, \qquad \hat\sigma_{ann} = \sqrt{F}\,\hat\sigma$$

**Variables:** $F$ observations per year (252 for daily — supersedes the
project's earlier monthly-era $F=12$ convention, per
`notes/SPECIFICATION.md` §A.0's daily-frequency mandate; must be applied
consistently everywhere $F$ appears below).

$$SR = \frac{\bar R_p-\bar r_f}{\sigma(R_p-r_f)}\sqrt{F}, \qquad Sortino = \frac{\bar R_p-\bar r_f}{\sigma_{down}}\sqrt{F}$$

$$DD_t = \frac{W_t}{\max_{u\le t}W_u}-1, \qquad MDD=\min_t DD_t$$

$$CAGR = \left(\frac{W_T}{W_0}\right)^{1/Y}-1, \qquad Calmar = \frac{CAGR}{|MDD|}$$

**Additional required measures** (all [PROPOSED] standard definitions,
already specified in full in `notes/SPECIFICATION.md` §IV.19 and not
re-derived here beyond this pointer, to avoid duplicate, potentially
drifting definitions across two documents):
**Information ratio** $IR=(\bar R_p-\bar R_{bench})/TE$, $TE=\operatorname{std}(R_p-R_{bench})$;
**beta/alpha** from $R_{p,t}-r_{f,t}=\alpha+\beta'F_t+\varepsilon_t$
(Newey-West standard errors, against the OSE/US factor set already
specified); **tracking error** as above; **VaR/CVaR** — [OPEN, not yet
specified in this project] if required, standard historical or parametric
VaR at a stated confidence level, and CVaR as the expected shortfall beyond
that VaR threshold — no methodology has been chosen yet, flagged in Table C
rather than invented here; **portfolio concentration** — e.g.
Herfindahl-Hirschman index $\sum_i w_i^2$; **effective number of holdings**
$1/\sum_i w_i^2$; **gross and net exposure** $\sum_i|w_i|$ and $\sum_i w_i$
respectively (already defined in §5's constraint table, repeated here as
reporting outputs, not just constraints).

---

## 16. Factor / security scoring

This section was not part of the original 16-item outline and is added per
your request. It formalizes, in this document's LaTeX/sourcing standard,
the security-scoring methodology already established and confirmed across
this project's design process (`notes/SPECIFICATION.md` §A.2, §V.2).

### 16.1 Within-group standardization — [SOURCED: Sørensen (Storebrand), z-score composite mechanism]

$$Z_{i,k,t} = \frac{x_{i,k,t}-\mu_{k,g(i),t}}{\sigma_{k,g(i),t}}$$

**Variables:** $x_{i,k,t}$ raw metric $k$ (e.g., a value or quality ratio,
sign-oriented so higher is always better) for asset $i$ at $t$; $g(i)$ the
sector/peer-group of asset $i$; $\mu_{k,g(i),t}$, $\sigma_{k,g(i),t}$ the
cross-sectional mean and standard deviation of metric $k$ **within** group
$g(i)$ at $t$ (not the global cross-section).
**Interpretation:** standardizes heterogeneous raw metrics (e.g., P/E and
P/B, different units and scales) onto a common footing so they can be
linearly combined; computing $\mu$, $\sigma$ **within sector** rather than
globally isolates stock-selection information from industry-level effects
— specifically, industry momentum contaminating naively-measured
individual-stock momentum (Moskowitz & Grinblatt, 1999, "Do Industries
Explain Momentum?", *Journal of Finance* 54(4) — already cited in this
project's design record and anticipated in the codebase's own comment,
`signals/cross_sectional.R`: "MG1999").
**Source status:** [SOURCED: Sørensen/Storebrand deck, "Constructing Value
and Momentum Scores," read directly in an earlier design session — the deck
demonstrates $z(w\times z(\text{metric}_1)+(1-w)\times z(\text{metric}_2))$];
[ADAPTED] the within-group (rather than global) computation is this
project's own extension, motivated by MG1999 and by Sørensen's own slide 30
explicitly naming "within industries" as a valid application of the same
method, not a departure from it.

### 16.2 Composite score

$$Score_{i,t} = \sum_k \omega_k\,Z_{i,k,t}$$

**Variables:** $\omega_k$ metric weights (fixed, chosen ex ante — not
optimized in-sample, to avoid data-mining the weighting itself).
**Zero-sum property, exact:** since each $Z_{i,k,t}$ is already exactly
zero-sum within its group ($\sum_{i\in g}(x_{i,k,t}-\mu_{k,g,t})=0$ by
construction of the mean), any linear combination $Score_{i,t}$ is also
exactly zero-sum within each group — a property carried through to §16.3's
final transform.

### 16.3 Final outlier-robust transform — [SOURCED: AMP (2013), Eq. 1]

$$R_{i,t} = \operatorname{rank}(Score_{i,t}) - \operatorname{mean}\big(\operatorname{rank}(Score_{\cdot,t})\big) \qquad \text{computed within group } g(i)$$

**Directly identical to** Asness, Moskowitz & Pedersen (2013)'s cross-sectional
rank-weight construction (their Eq. 1, verified by direct reading in an
earlier design session:
$w^S_{it}=c_t(\operatorname{rank}(S_{it})-\sum_i\operatorname{rank}(S_{it})/N)$),
and identical to this project's own already-implemented
`signals/cross_sectional.R::.cs_transforms$rank`.
**Why rank as the final stage, z-score as the combination stage:** AMP's
own stated rationale (verified, quoted in an earlier design session):
"using ranks of the signals as portfolio weights helps mitigate the
influence of outliers, but portfolios constructed using the raw signals are
similar and generate slightly better performance" — i.e., AMP themselves
report this is a **deliberate robustness-for-performance trade-off**, not a
free improvement. Bounding any single name's influence to $1/N$ within its
group is particularly relevant on this project's OSE micro/small-cap
universe, where extreme raw-metric outliers (illustrated concretely in the
Sørensen deck's own sample data, where Tesla's P/E ratio reaches roughly
225x) are more likely than in AMP's own large/liquid test universe.
**This is the value handed to $\mathbf{s}$ (§3) or $\boldsymbol{\mu}$ (§5),
feeding the EPO family (§8) or classical MVO (§5) identically to any other
signal in this document** — no special-casing is required downstream of
$R_{i,t}$.
**Percentile-rank variant** (Sørensen's own final reporting form, used for
screening/display, not necessarily as the value fed to the optimizer):
$100\cdot\operatorname{rank}(Score_{i,t})/n_{g(i),t}$.
**Used in:** L1 signal layer, `notes/SPECIFICATION.md` §A.2's four-stage
pipeline (group → within-group z-score composite → demeaned-rank output →
feeds $\mathbf{s}$/$\boldsymbol{\mu}$) — this section supplies the formal
mathematics for that already-confirmed pipeline.
**Estimation window/frequency:** matches whatever the underlying raw
metrics' own frequency/window is (e.g., trailing 12-month for a momentum
metric per §3, point-in-time for a valuation ratio) — the standardization
and ranking themselves are contemporaneous, cross-sectional operations with
no separate window of their own.
**Numerical issues:** requires a minimum group size for $\sigma_{k,g(i),t}$
to be meaningfully estimated — a sector with very few names produces a
noisy or degenerate z-score; **[OPEN]** no minimum-group-size threshold has
been set, and this is compounded by the still-unresolved sector-data-
coverage question for OSE names (`notes/SPECIFICATION.md` §XI.7) — small
Nordic sectors may need either a minimum-$n$ fallback to global (non-sector)
standardization, or a coarser sector taxonomy, neither of which has been
decided.
**Source status of AMP's simple (non-composite) rank-weight formula
specifically:** [SOURCED: AMP Eq. 1] reserved as a **validation tool** for
any new candidate raw metric before it is promoted into the §16.2 composite
— confirming a metric has genuine predictive power in AMP's minimal,
hard-to-overfit form before it earns a place in the production pipeline,
consistent with the already-confirmed project decision on this point.

---

## Table A. Formula register

| Formula | Equation | Source | Module | Inputs | Output | Status |
|---|---|---|---|---|---|---|
| Simple return | §2.1 | [PROPOSED] | L0 | price, dividends | $R_{i,t}$ | Confirmed |
| Log return | §2.2 | [PROPOSED] | L0/L2 | price | $r_{i,t}$ | Confirmed |
| Excess return | §2.3 | [PROPOSED] | L1/L2 | $R_{i,t}$, $r_{f,t}$ | $r^e_{i,t}$ | Confirmed |
| NOK conversion | §2.5 | [PROPOSED] | L0 | $R^{LC}_{i,t}$, FX rate | $R^{NOK}_{i,t}$ | Confirmed |
| TSMOM signal | §3.1 Eq. 23 | [SOURCED: PBL] | L1 | trailing return, $\sigma_{i,t}$ | $s_{i,t}^{TSMOM}$ | Confirmed, no-skip $[t-12,t]$ decided |
| TSMOM benchmarks | §3.2–3.3 Eq. A1–A2 | [SOURCED: PBL] | Validation only | trailing return, $\sigma_{i,t}$, $n_t$ | $x^{TSMOM}_t$ | Confirmed (benchmark role only) |
| XSMOM signal + variants | §3.4 Eq. 24–26,28 | [SOURCED: PBL] | L1 | trailing return | $s^{XSMOM}_{i,t}$ | Confirmed, no-skip $[t-12,t]$ decided (new `xsmom_pbl` signal needed, distinct from existing `xsmom`) |
| Equal weight | §4.1 | [PROPOSED] | L3 | universe | $w^{1/N}$ | Confirmed, built |
| Inverse-vol anchor | §4.2 | [SOURCED: PBL "Equity 7"] | L2/L3 | $\sigma_{i,t}$ | $a^{1/\sigma}_{i,t}$ | Confirmed, built |
| Portfolio return | §4.3 | [PROPOSED] | L6 | $w$, $R$ | $R_{p,t}$ | Confirmed |
| MVO | §5 Eq. 2–3 | [SOURCED: PBL] | L3 | $\mu,\Sigma,\gamma$ | $w^{MVO}$ | Confirmed, built |
| GMV | §6 | [PROPOSED] | L3 | $\Sigma$ | $w^{GMV}$ | Confirmed, built |
| Sample covariance | §7.1 | [PROPOSED] | L2 | returns | $\hat\Sigma$ | Confirmed |
| $\Sigma=D R D$ | §7.2 | [SOURCED: PBL Eq. 4, adapted symbol] | L2 | $D,R$ | $\Sigma_t$ | Confirmed |
| Correlation shrinkage | §7.3 Eq. 19 | [SOURCED: PBL] | L2 | $\Omega,w$ | $\Sigma_w$ | Confirmed, built |
| General EPO | §8.2 Eq. 17 | [SOURCED: PBL] | Theory only | $\tilde\Sigma,s,a,\tau,\Lambda,\gamma$ | — | Confirmed (derivation basis) |
| Simple EPO | §8.1 Eq. 20 | [SOURCED: PBL] | L3 | $s,\Sigma_w,\gamma$ | $x^{EPO_s}$ | Confirmed, built |
| Anchored EPO | §8.3 Eq. 18,19,21,22 | [SOURCED: PBL] | L2/L3 | $s,a,\Sigma_w,\tilde\Sigma,w$ | $x^{EPO_a}$ | Confirmed, built |
| EPO $w$-selection | §8.5 | [SOURCED: PBL, grid unconfirmed] | L5 | past Sharpe by $w$ | $w_t^*$ | Confirmed procedure, grid open |
| GARCH(1,1) | §9.1 | [PROPOSED: Bollerslev 1986] | L2 | $r_{i,t}$ | $\sigma^2_{i,t}$ | Confirmed fallback |
| GJR-GARCH(1,1) | §9.2 | [SOURCED: GJR 1993] | L2 | $r_{i,t}$ | $\sigma^2_{i,t}$ | Confirmed primary |
| DCC / cDCC | §10 | [SOURCED: Engle 2002 / Aielli 2013] | L2 | $z_t$ | $R_t$ | Confirmed (cDCC), not in PBL |
| Static TC | §11.1 | [PROPOSED] | L6 | $w^{target},w^{pre},c$ | $TC_t$ | Confirmed |
| Turnover-penalized opt. | §11.2 | [SOURCED: GP 2013] | L3/L4 | $\mu,\Sigma,\lambda,\Lambda$ | $w_t$ | **Confirmed** — decided scope (see §11.3's row) |
| Full GP dynamic trading | §11.3 Eq. 4,9,10,13 | [SOURCED: GP 2013] | L3/L4 | $B,\Phi,\Omega,\Sigma,\lambda,\gamma,\rho$ | $x_t$ | **Decided: not built** — reference only |
| Rebalancing bands | §12.2 | [PROPOSED] | L6 | $w^{pre},w^{target},b_i$ | trigger | Confirmed mechanism, band definition open |
| Vol targeting / leverage | §13 | [SOURCED: derivation in master spec] | L4 | $\sigma^{target},\hat\sigma_p$ | $L_t$ | Confirmed |
| Constraints | §14 | [PROPOSED] | L3/L4 | — | feasible $w$ | Mixed — see per-row status |
| Performance measures | §15 | [PROPOSED] | L6 | returns | ratios | Confirmed |
| Factor scoring pipeline | §16 | [SOURCED: Sørensen + AMP 2013] | L1 | raw metrics, sector tags | $\mathbf{s}$ | Confirmed, sector-data-blocked |

## Table B. Confirmed specifications

- Return definitions (§2.1–2.4), NOK conversion (§2.5).
- TSMOM (PBL Eq. 23) and XSMOM (PBL Eq. 24–26, 28) as the L1 signal
  specification, **with the $[t-12,t]$ no-skip window explicitly confirmed
  against the published paper and formally adopted by project decision for
  both signals** — this project's separate, pre-existing skip-month
  `mom12_1` (and the existing `xsmom` signal built on it) is a different,
  non-PBL construction, retained alongside the new no-skip metrics rather
  than replaced by them.
- **Transaction-cost scope, decided:** the single-period turnover-penalized
  objective (§11.2, sourced to GP 2013) is the confirmed treatment. The full
  multi-period Gârleanu-Pedersen dynamic trading model (§11.3) is sourced
  and documented but **will not be built** — its prerequisite (a
  multi-factor, differentially-decaying L1 signal architecture) does not
  exist in this project and is not planned.
- Equal-weight, inverse-volatility-anchor, and portfolio-return mechanics
  (§4).
- Classical MVO and GMV, both closed-form and QP-constrained (§5–§6).
- The full correlation-shrinkage / EPO family — general, simple, and
  anchored, including the endogenous-$\gamma$ formula — verified exactly
  against the published FAJ text and cross-checked against this project's
  own `operators/anchor.R` and `operators/shrinkage.R` (§7.3, §8). **The
  SSRN-vs-FAJ equation-numbering discrepancy this project's own notes had
  flagged as open is now resolved: FAJ Eq. 18/19/21/22, not SSRN's
  7/14/16/17.**
- The PBL out-of-sample $w$-selection procedure (expanding window, argmax
  realized Sharpe, apply next period) — §8.5.
- GJR-GARCH(1,1) primary / GARCH(1,1) fallback volatility, with the
  explicit acknowledgment that **this is not part of PBL's own published
  methodology** (§4.2, §9).
- cDCC (not vanilla DCC) as the confirmed correlation-dynamics model,
  likewise not part of PBL's own methodology (§10).
- Static ex-post transaction cost deduction (§11.1) as the confirmed
  minimum cost treatment.
- Volatility targeting and the leverage-overlay formula, financing-cost
  corrected (§13).
- The four-stage factor-scoring pipeline: sector grouping → within-group
  z-score composite → demeaned-rank transform → feeds the signal layer
  (§16).

## Table C. Open methodological questions

| # | Question | Status |
|---|---|---|
| 1 | ~~Exact TSMOM/XSMOM lookback convention~~ | **[RESOLVED]** PBL's no-skip $[t-12,t]$ convention adopted for **both** TSMOM (§3.1) and XSMOM (§3.4). `mom12_1` (skip-month) is retained as a separate, distinct signal, not reused for either — new no-skip metrics are required for `ts_signal` and a new `xsmom_pbl`-style signal (Table D, item 3) |
| 2 | Exact rebalancing frequency (daily/weekly/monthly/quarterly, §12.1) | Open — not fixed by any source in this document |
| 3 | Interpretation of the rebalancing band (percentage points vs. relative vs. portfolio-value share, §12.2) | Open — this document uses percentage points as a stated working assumption only |
| 4 | Trade-execution policy on band breach (full portfolio vs. breached-only; full reversion vs. nearest-boundary, §12.2) | Open |
| 5 | GARCH vs. GJR-GARCH estimation details: innovation distribution (Gaussian vs. Student-$t$), rolling vs. expanding parameter re-estimation cadence (§9.1) | Open |
| 6 | DCC vs. cDCC — resolved in favor of cDCC; remaining open item is estimation software/library choice, not the model itself | Narrowed, not fully closed |
| 7 | Fixed vs. dynamically (OOS) selected EPO shrinkage parameter — PBL's procedure is confirmed (§8.5); the exact candidate grid $\mathcal{W}$ used in production is not | Open |
| 8 | Long-only vs. long/short by default — already addressed at the architecture level (`notes/SPECIFICATION.md` §V.8: long/short is a signal property via demeaning, long-only is an L4 constraint) but the **default** posture for new strategies is not restated here as settled | Open |
| 9 | Target volatility $\sigma^{target}$ and leverage limits $L_{max}$ — no specific numbers confirmed anywhere in this project's record | Open |
| 10 | Transaction-cost source/specification beyond Nordnet Mini's published commission tiers: FX spread exact rate, short-borrow fees | Open, per `notes/SPECIFICATION.md` §XI.4/§XI.18 |
| 11 | ~~Whether to build the full Gârleanu-Pedersen multi-period dynamic trading model (§11.3) or rely on the single-period turnover penalty (§11.2)~~ | **[RESOLVED]** single-period turnover penalty (§11.2) only. §11.3 retained as sourced reference, not a build target; revisit only if a multi-factor, differentially-decaying L1 signal architecture is later adopted |
| 12 | Cardinality constraints (min/max number of holdings): MIQP vs. heuristic post-processing (§14) | Open |
| 13 | VaR/CVaR methodology, if required (§15) | Open — not yet specified at all |
| 14 | Minimum sector-group size for §16.1's within-group standardization, and the fallback behavior below that threshold | Open, compounded by unresolved OSE sector-data coverage |
| 15 | Tie-breaking rule for §8.5's $w$-selection when multiple grid points tie on realized Sharpe | Open — a [PROPOSED] default (prefer larger $w$) is suggested but not confirmed |

## Table D. Developer implementation sequence

1. **Data and returns** — §2 in full, including the currency-conversion
   quotation-direction check (§2.5) before any cross-market figure is
   trusted.
2. **Universe eligibility** — per `notes/SPECIFICATION.md` Part III;
   sector/peer-group tagging specifically required before §16 can run.
3. **Signals** — §3: build the new no-skip $[t-12,t]$ trailing-return metric
   and the `ts_signal`/`xsmom_pbl` signals per the now-resolved Table C item
   1 decision (do not reuse `mom12_1`/`xsmom` for these); and §16 (factor
   scoring pipeline).
4. **Volatility models** — §9, with the fallback hierarchy implemented as
   automatic, not manual.
5. **Correlation and covariance models** — §7, §10; compose §7.3's
   shrinkage with DCC's $\bar{\mathbf{Q}}$ as already specified in the
   master spec, not as two independent, uncoordinated steps.
6. **Benchmark portfolios** — §4.1–4.2, §3.2–3.3 (the latter for
   out-of-sample comparison only, per their confirmed validation-only role).
7. **MVO and minimum variance** — §5–§6.
8. **Simple EPO** — §8.1.
9. **Anchored EPO** — §8.3–§8.4, including the endogenous-$\gamma$
   verification against `operators/anchor.R` already completed in this
   document (§8.3) — the developer task is updating the in-code equation
   citations, not re-deriving the math.
10. **Constraints** — §14, with the cardinality-constraint scope decision
    (Table C item 12) resolved before, not during, implementation.
11. **Transaction costs** — §11.1 first (minimum viable), then §11.2
    (confirmed scope, per the now-resolved Table C item 11 decision); §11.3
    is not a build step.
12. **Rebalancing** — §12, with Table C items 2–4 resolved first; do not
    build a specific band-execution policy against an unstated assumption.
13. **Backtesting** — integrate 1–12 into `core/engine.R`'s rolling loop,
    per the daily-frequency recalibration already required
    (`notes/SPECIFICATION.md` Task C.1) — this is a precondition, not a
    parallel, independent task.
14. **Performance reporting** — §15.
15. **Validation against PBL results** — reproduce PBL's Table 2 (Global
    1–3 Sharpe ratios by fixed $w$) as an end-to-end regression test,
    **using EWMA volatility (§4.2), not GJR-GARCH**, since GJR-GARCH will
    not reproduce PBL's published figures — this is the correct use of
    "validate against the paper": confirm the EPO machinery is implemented
    correctly using PBL's own risk model, before layering this project's
    own GARCH/DCC extensions on top and evaluating those on their own,
    separate empirical merits.
