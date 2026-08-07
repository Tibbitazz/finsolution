# ENGINE_V1 — Master Technical Specification

**Status:** Authoritative design document. Supersedes all prior working notes on
scope (this file previously existed as an incrementally-edited note; it is now
rewritten as the single source of truth). It does not supersede the empirical/
numerical findings already recorded in `STATUS.md` or the literature notes in
`notes/covariance/`, `notes/shrinkage/`, `notes/momentum/` — those are cited
here, not duplicated in full.

**Convention.** Every claim carries one tag:
`[CONFIRMED]` — an agreed design decision, to be implemented as stated.
`[VERIFIED]` — a factual claim checked against a primary source this design
process.
`[ASSUMED]` — a working assumption, plausible but not independently checked.
`[OPEN]` — unresolved; implementation must not proceed past it silently.
`[EXPERIMENTAL]` — reviewed in depth but deliberately not built yet, gated on
a stated condition (data availability, universe size, etc.).
`[PARKED]` — considered and consciously deferred; not on the near-term path.

**Companion document.** `notes/MATHEMATICAL_APPENDIX.md` is the authoritative
source for every EPO, TSMOM, XSMOM, GARCH, DCC, and transaction-cost formula
— each verified directly against the published source paper (Pedersen, Babu
& Levine 2021; Gârleanu & Pedersen 2013), with LaTeX, full variable
definitions, and explicit sourcing status per equation. **Where Part IV below
and the appendix overlap, the appendix is authoritative** — it was produced
later, against the primary sources directly, and corrects specific details
Part IV states more loosely (e.g., Part IV does not capture PBL's confirmed
$[t-12,t]$ momentum-window convention, or the exact endogenous-$\gamma$
anchored-EPO formula). Part IV remains useful as the compact, single-document
overview; the appendix is the implementation-grade reference for anything it
covers.

**Reading order for a new developer.** Part I gives the mental model. Part II
and Part III establish what data exists and what universe it defines. Part IV
is the complete mathematics — read once, then use as reference (see the
companion-document note above for where the appendix takes precedence). Part V and
Part VI describe what the system actually computes, in the order it computes
it. Parts VII–IX describe constraints, testing, and output. Part X is the
build order. Parts XI–XII are the living backlog.

---

# Part I — System Overview

## I.1 Objective

ENGINE_V1 is a **medium-to-long-horizon security-selection and strategic
asset-allocation (SAA) engine**, built for a Norway-based investor trading
through Nordnet, spanning two markets: the Oslo Stock Exchange (OSE) and U.S.
equities (S&P 500 / Nasdaq). All portfolio-level results are expressed in
Norwegian kroner (NOK).

It is explicitly **not** a short-term or algorithmic trading system. It does
not predict daily price direction, and it does not attempt to time markets at
a technical/tactical level as its primary function. Its job is to decide,
periodically, **what securities to hold and in what proportion**, using
estimated expected returns, an estimated risk model, and a portfolio
optimizer, subject to real-world costs and constraints. A separate,
architecturally subordinate **tactical layer** — pre-existing outside this
engine, using technical indicators (ATR, EMA, RSI) and triple-barrier labeling
— is responsible only for *timing the entry and exit* of positions this engine
has already decided to hold. That tactical layer is out of scope for this
document except where it interfaces with this engine's outputs.

## I.2 Investment philosophy

1. **Simplicity beats complexity.** Every added model, factor, or data source
   must earn its place with a demonstrated out-of-sample benefit; complexity
   is not evidence of rigor.
2. **Regime awareness is mandatory**, but is implemented as a *risk overlay*
   (position sizing, correlation-breakdown monitoring), not as a hard
   directional filter, unless a specific filter has been separately justified
   and tested.
3. **Every feature must have economic or behavioral intuition.** No purely
   statistical, data-mined inputs.
4. **The system should fail small and predictably.** Estimation failures
   (e.g., a volatility model that fails to converge) fall back to a simpler,
   well-understood alternative rather than propagating a degenerate result.
5. **"Better" is not assumed — it is measured out of sample.** A more
   sophisticated model (more shrinkage, a richer covariance estimator, an
   added constraint) is adopted only when it demonstrably improves realized,
   not in-sample, performance at the actual scale the system runs at. This
   project has already produced its own internal evidence for this principle
   (§VI.9).

## I.3 Portfolio construction philosophy

The organizing method is **Enhanced Portfolio Optimization** (EPO; Pedersen,
Babu & Levine, 2021, *Financial Analysts Journal* 77(2)). EPO's central
insight is that standard mean-variance optimization is dominated by
estimation error, not by a wrong economic model — the fix is not a better
point estimate of the covariance matrix, but a **principled shrinkage of
correlations toward zero**, controlled by a single intensity parameter that
interpolates between raw mean-variance optimization and a maximally
diversified, low-estimation-error portfolio. This shrinkage-first framing
governs the whole risk-model design in Part VI, not just the one solver
literally named `epo`.

Two design separations follow from this and are enforced everywhere in the
codebase:

- **Signal (`μ`) is independent of risk (`Σ`).** Every expected-return
  estimator (historical mean, cross-sectional momentum, time-series momentum,
  value) is a swappable input; every risk estimator (sample covariance, GARCH,
  DCC, shrunk, RMT-cleaned) is a separately swappable input. Any signal can be
  paired with any risk estimator and fed to any solver. This is what makes it
  possible to later say "the improvement came from the risk model, not the
  signal" or vice versa — a claim that is meaningless if the two are entangled.
- **Construction is separate from selection.** A shrinkage intensity, a
  leverage ratio, or a stacking size is a *parameter to be selected*
  out-of-sample, not a value fitted in-sample. The system's parameter-
  selection layer (L5) is a first-class part of the architecture, not an
  afterthought.

## I.4 System architecture

The system is organized into seven layers, each with a narrow, well-defined
job. This layering is already implemented in the codebase (`core/`,
`signals/`, `operators/`, `solvers/`) and is retained as the organizing
principle for everything new in this specification.

```
L0  Data          — acquisition, validation, currency conversion, universe
L1  Signal (μ)     — expected-return estimation and security ranking
L2  Risk (Σ)       — volatility, correlation, covariance, shrinkage
L3  Optimizer      — portfolio construction (the "solver")
L4  Overlay        — constraints, position sizing, leverage, regime, stacking
L5  Selection      — out-of-sample selection of tunable parameters
L6  Output         — costs, turnover, rebalancing, reporting, backtest
```

A **strategy** is a named row combining one solver (L3), one signal (L1), a
set of risk operators (L2), and a parameter set (constraints, leverage,
rebalancing rule) — this is the existing `REGISTRY` design and is retained
unchanged as the unit of comparison throughout the system. Many strategies
share the same solver with different parameters; adding a new strategy is
adding a registry row, not writing new code.

## I.5 High-level data flow

```
Raw market data (OHLCV, FX, macro, factor benchmarks)
        │
   L0: clean, validate, convert to NOK, construct point-in-time universe
        │
   L1: compute raw factor metrics → sector-relative standardize → rank → μ
        │
   L2: estimate D_t (volatility) and R_t (correlation) → Σ_t = D_t R_t D_t
        │      (shrunk/cleaned per-solver as appropriate)
        │
   L3: solver(μ, Σ, params) → raw portfolio weights
        │
   L4: apply constraints → position sizing → leverage/regime overlay →
        (optionally) stack additional sleeves on top
        │
   L6: apply transaction costs → realize the period's return → repeat
        │
   Output: gross/net performance, risk reports, holdings, diagnostics
```

## I.6 Major system modules (as they exist or are planned in the codebase)

| Module | Role | Status |
|---|---|---|
| `core/config.R` | Single source of truth for all tunable parameters | Built; needs daily-frequency recalibration (Part X, Phase 0) |
| `core/registry.R` | Strategy catalogue — one row per (solver, signal, ops, params) combination | Built |
| `core/solver_api.R`, `solvers/*.R` | Self-registering portfolio-construction methods | Built (mean-variance and risk-budget families) |
| `core/signal_api.R`, `signals/*.R` | Self-registering expected-return estimators | Built (sample mean, cross-sectional momentum); time-series momentum planned |
| `core/moment_api.R`, `operators/*.R` | Self-registering `(μ,Σ) → (μ',Σ')` transforms — shrinkage, anchoring | Built (correlation shrinkage); RMT and DCC planned |
| `core/engine.R` | Data import, moment estimation, rolling backtest loop, checkpointing | Built; monthly-calibrated, needs Part X Phase 0 rework for daily data |
| `modules/*.R` | Research questions and analysis built on top of engine output | Partially built; several planned modules specified in Part V–IX |

## I.7 End-to-end workflow, data acquisition to live management

1. Acquire and validate daily market data for the OSE+US equity universe, FX
   rates, macro series, and benchmark/factor data (Part II).
2. Convert every non-NOK return series to NOK (Part IV, §IV.17).
3. Construct the point-in-time investable universe for each period, applying
   survivorship, liquidity, and Nordnet-investability screens (Part III).
4. Compute raw factor metrics, standardize them sector-relatively, and form
   the ranking signal that becomes `μ` (Part V, §V.1–V.3).
5. Estimate the volatility and correlation model for the same period's
   universe, producing `Σ` (Part VI).
6. Run the selected solver(s) to produce raw portfolio weights (Part V, §V.4).
7. Apply constraints, position sizing, leverage, regime overlay, and any
   stacked sleeves (Part V, §V.5–V.12; Part VII).
8. Apply transaction costs and realize the period's portfolio return; advance
   to the next period (Part VIII).
9. Report performance, risk, and diagnostics (Part IX).
10. **Live portfolio implementation** is downstream of all of the above and is
    explicitly **not yet scoped in detail** — it depends on Part X Phase 0
    closing (universe/survivorship, currency, daily-frequency rework) and the
    backtest engine being internally consistent first. This is stated plainly
    rather than assumed: there is currently no live-trading component, only a
    backtest/research engine that this specification brings to a
    daily-data-consistent, decision-ready state.

---

# Part II — Data Architecture

Every entry below states purpose, frequency, preferred/fallback source,
required fields, historical coverage, cleaning/validation needs, storage
location, and update cadence. Only datasets independently verified this
design process, or already present in the repository, are given a specific
provider; where no provider could be verified, that is stated as `[OPEN]`
rather than invented.

## II.1 Equities — OSE and U.S.

- **Purpose:** primary security universe; source of prices, returns, and
  corporate-action data for the core SAA sleeve.
- **Frequency:** daily.
- **Preferred provider:** Yahoo Finance. `[VERIFIED]` OSE tickers resolve
  under the `.OL` suffix (e.g., `EQNR.OL`); U.S. tickers resolve directly.
- **Fallback/supplementary provider:** EODHD. `[VERIFIED]` generically
  supports 60+ exchanges, 150K+ tickers, and a `delisted=1` parameter on its
  exchange-symbol-list endpoint. `[OPEN]` whether this delisted-coverage
  mechanism is populated for Oslo Børs specifically — not confirmed.
- **Required fields:** date, open, high, low, close, adjusted close, volume.
- **Historical coverage:** as available per ticker; ragged/incomplete history
  is expected for smaller OSE names and must be handled by the universe
  construction logic (§III.6), not assumed away.
- **Data cleaning:** adjust for splits/dividends before any return is
  computed (adjusted close, or an explicit adjustment factor). Missing/
  delayed observations handled by the `.active_set` mechanism (§III.6), not
  by silent forward-fill.
- **Validation:** schema check against `CONFIG$asset_cols`; spot-check a
  sample of known corporate actions (splits, large dividends) against a
  second source when a new ticker is onboarded.
- **Storage:** `data/` (current: `test_data.csv`, `data/OSE Data/`); new
  per-ticker OHLCV to follow the same directory convention, one file or
  partition per exchange.
- **Update frequency:** daily, end-of-day.

## II.2 ETFs (mainstream, broad-market)

- Same pipeline as II.1 (Yahoo primary, EODHD fallback) — ETFs are ordinary
  listed securities for data purposes. No separate data architecture needed.
- **Nordnet investability:** `[CONFIRMED]` mainstream broad-market ETFs on
  the primary listed exchanges are treated as default-tradable via Nordnet
  without per-instrument verification (§III.12).

## II.3 Leveraged ETFs

- **U.S. leg:** `[VERIFIED]` standard, liquid, daily-reset products exist
  (e.g., SPXL, TQQQ) and are covered by the same Yahoo/EODHD pipeline as any
  other U.S.-listed security. Usable for the leverage-vehicle comparison in
  §V.9.
- **OSE leg:** `[VERIFIED, important correction]` Nordnet does **not** offer
  U.S.-style leveraged ETFs on the Norway leg. The relevant Nordnet product is
  a **mini future or certificate** ("Nordnet Markets" ETPs) — a structurally
  different instrument built around a financing level and a knock-out
  barrier, not daily NAV-reset compounding. Data source for these products is
  `[OPEN]` — not researched this session, and its mathematics (§XI) has not
  been derived. Do not substitute the U.S. LETF data pipeline for this
  instrument class.

## II.4 Mutual funds

- **Availability:** `[VERIFIED]` Nordnet offers mutual funds, including its
  own index and interest-rate funds (money-market, bond, high-yield, green
  bond categories).
- **Data source for systematic backtesting (NAV history, fees):** `[OPEN]` —
  not verified this session. Do not assume a specific provider.

## II.5 Fixed income

- **Norwegian risk-free proxy:** `[VERIFIED, already in repository]`
  `data/GOVT_GENERIC_RATES copy.csv` — Norwegian 3-month T-bill
  (Statskasseveksler) yield, daily, 2020-01-02 onward, 1,552 rows, currently
  unused by the engine. Sovereign, not interbank, credit risk — a candidate
  robustness check against NIBOR (§II.8).
- **NIBOR:** `[VERIFIED, already in repository]` via `data/OSE Data/Risk Free
  Rates/` (Ødegaard), monthly 1979-12→2025-04, daily 1979-12-31→2025-04-29.
  NIBOR from 1986; overnight NIBOR 1982–86; two-year treasury yield 1980–82
  (Ødegaard's own construction, documented as "messy" pre-1986 by the author).
- **Broader Nordnet-investable bond universe** (individual bond issues, bond
  funds beyond the risk-free proxy): `[OPEN]` — no specific data source
  verified this session.

## II.6 Managed futures

- **External index data (PivotalPath Managed Futures Index):** `[VERIFIED,
  negative finding]` PivotalPath tracks 2,500+ institutional hedge funds; a
  free "Index App" gives basic performance insight, but comprehensive
  historical index data requires an institutional subscription (sales-gated,
  not self-serve). Not usable as a systematic backtest data source as
  currently accessible.
- **External benchmark (SG Trend Index):** `[VERIFIED, negative finding]`
  real, credible, widely referenced (top-10 trend CTAs, equal-weighted,
  annually reconstituted, daily-calculated) — but full historical daily data
  requires a commercial relationship with Société Générale. Usable only for
  periodic validation via third-party summary figures, not as a build source.
- **Recommended approach: in-house construction.** No external data
  subscription required beyond the futures price data itself. See §V.10 for
  the full construction specification. **Data requirement:** continuous,
  roll-adjusted futures price series across equity index, government bond,
  currency, and commodity futures. `[OPEN]` Yahoo Finance has some futures
  tickers (`ES=F`, `GC=F`, `CL=F`) but roll-adjustment/back-adjustment
  quality on the free tier is unverified — naive front-month splicing would
  corrupt a trend signal and must be checked before this sleeve is built.

## II.7 Alternative investments (merger arbitrage, gold, commodities)

- **Merger arbitrage:** `[VERIFIED]` NYLI/IQ Merger Arbitrage ETF (ticker
  `MNA`) — real, liquid, retail-accessible, launched 2009, trades on major
  U.S. exchanges. Used as a practical proxy rather than an in-house
  deal-spread replication (data-intensive, out of scope for now). Standard
  equity/ETF data pipeline (II.1) applies.
- **Gold:** no data-access barrier — standard futures (`GC=F`) or ETF proxy
  via the existing equity pipeline.
- **Broader commodities:** a liquid commodity-basket ETF proxy — `[OPEN]`
  specific instrument not selected this session.

## II.8 FX data

- **Preferred provider:** Norges Bank API. `[VERIFIED]` REST interface, ~40
  currency pairs including USD/NOK, official mid-rate (midpoint of interbank
  bid/ask), published daily ~16:00 CET, free. `[OPEN]` exact historical start
  date for USD/NOK not confirmed this session.
- **Fallback/supplementary provider:** Yahoo Finance. `[VERIFIED]` FX tickers
  exist for the needed pairs (`NOK=X`, `USDNOK=X`, `NOKUSD=X`, `NOKEUR=X`),
  daily OHLC (not just a single point — usable for range-based FX volatility
  estimation, §IV.4). `[OPEN]` whether the quoted rate is mid, bid, or a
  blended composite; `[ASSUMED, not independently verified]` generally less
  authoritative than a central-bank source.
- **Required fields:** date, rate (Norges Bank); date, OHLC (Yahoo).
- **Data cleaning:** neither source provides bid/ask spread — a separate
  spread assumption is required for realistic transaction cost modeling
  (§II.12).
- **Storage:** new addition to `data/`, parallel structure to existing OSE
  factor data.
- **Update frequency:** daily.

## II.9 Risk-free rates (see also §IV.2 for the multi-purpose split)

| Purpose | Rate | Source | Status |
|---|---|---|---|
| OSE-leg excess returns / evaluation | NIBOR (1M) | Ødegaard, `data/OSE Data/` | `[VERIFIED, in repository]` |
| US-leg excess returns / evaluation | Fed Funds Effective Rate | FRED | `[CONFIRMED as the target rate]`; not yet pulled into `data/` |
| Leverage financing cost | Nordnet margin rate | Nordnet's own pricing page | `[VERIFIED]` 7.32% effective NOK, flat to 2,000,000 NOK |
| Investor-facing diagnostic (not systematic) | Nordnet broker cash rate | secondary source only | `[OPEN]` ~3.6%, not confirmed from Nordnet directly |
| Robustness-check alternative | Norwegian 3M T-bill | `data/GOVT_GENERIC_RATES copy.csv` | `[VERIFIED, in repository, unused]` |

## II.10 Corporate actions, dividends, delistings

- **Dividends/splits:** handled via adjusted close (II.1); `[VERIFIED]`
  EODHD's dividends/splits endpoints apply identically to delisted tickers
  once identified, meaning solving the delisting-identification problem
  (II.11 below) largely also solves this one.
- **Delistings:** `[VERIFIED]` EODHD's `delisted=1` mechanism exists
  generically; `[OPEN]` OSE-specific coverage unconfirmed. This is the single
  highest-stakes open data item in the project (§XI.1) — required for
  survivorship-bias control (§III.5).

## II.11 Historical index constituents

- `[VERIFIED, promising, unconfirmed for OSE]` EODHD's Index API supports a
  `historical=1` parameter for point-in-time index-membership snapshots —
  documented for major indices; not confirmed to cover OSEBX/OSEAX.
- `[VERIFIED, authoritative fallback]` Euronext/Oslo Børs publish semi-annual
  index-review documents (reconstitution June 1 and December 1) — a primary
  source, labor-intensive to assemble into a clean dataset but authoritative,
  and worth cross-checking against even if a commercial API claims coverage.
- `[OPEN, unverified]` Norgate Data was surfaced as a possible survivorship-
  bias-free constituent source; its core coverage is understood to be US/
  Australia-focused and Nordic coverage was not confirmed.
- **If no clean multi-decade source is found:** `[CONFIRMED fallback,
  already decided]` explicitly disclose and bound the survivorship exposure
  rather than proceeding silently.

## II.12 Option data / volatility data

- **VIX:** `[CONFIRMED]` pull from FRED (`VIXCLS`) or CBOE directly, not a
  Yahoo-derived `^VIX` quote — it is both a regime input (Part VII) and the
  US-leg implied-vol proxy.
- **EPU / TPU:** `[VERIFIED]` real, free, downloadable —
  policyuncertainty.com and FRED, covering the U.S. and (for EPU) Norway
  among 22 countries.
- **OSE options / implied volatility:** `[VERIFIED, real product, access
  unconfirmed]` Euronext sells commercial EOD/reference derivatives data for
  Oslo Børs; Millistream is rolling out a new Oslo Børs derivatives feed.
  `[OPEN, likely negative]` single-name OSE options liquidity outside a
  handful of large caps (Equinor, DNB) was not independently confirmed and is
  presumed thin. **Recommendation:** do not build OSE single-name implied
  volatility in the near term; use the GARCH/range-based conditional
  volatility estimators (§IV.5–IV.6) as the OSE risk-model input instead.

## II.13 Benchmark indices

- **OSE:** `[VERIFIED, in repository]` Ødegaard's EW/VW/OSEAX/OBX series,
  `data/OSE Data/Market Returns/`. Note the OBX series in this file starts
  2000-02 despite the underlying index existing since 1987 — the distributed
  series is shorter than the full index history.
- **U.S.:** standard S&P 500 / Nasdaq benchmark data via the existing
  Yahoo/EODHD equity pipeline — not separately verified this session but
  standard, low-risk data.

## II.14 Factor data

- **OSE:** `[VERIFIED, in repository]` Ødegaard's SMB/HML/UMD,
  `data/OSE Data/Pricing Factors/`, monthly 1981-07→2025-02, daily
  1981-07-01→2025-02-28. Note: no market-factor column is supplied; the
  market leg must be constructed as `VW − Rf` (or `EW − Rf`).
- **U.S.:** Ken French Data Library (`mba.tuck.dartmouth.edu`) — a
  well-established, freely available, canonical source, directly referenced
  as the standard in the Storebrand/Sørensen factor-investing materials
  reviewed during this design process. `data/F-F_Research_Data_Factors.csv`
  and `data/49_Industry_Portfolios.csv` are already present but are tied to
  the legacy predecessor project's monthly/US-only design and are on the
  scrub list (§III, Part X Phase 0) — retained only as a regression fixture
  for validating engine mechanics, not as production data.

## II.15 Macroeconomic variables

- VIX, EPU, TPU — as above (II.12), already sourced.
- Interest-rate regime, inflation series: `[OPEN]` specific provider not
  independently researched this session. FRED is the natural extension for
  US series (already established as a source in this project via VIX/EFFR);
  Norges Bank/SSB (Statistics Norway) are the natural extensions for
  Norwegian series, consistent with already-verified Norges Bank usage, but
  neither has been specifically checked for the required interest-rate/
  inflation series.
- **Bounded list, by design** (§VII.2): VIX, EPU, TPU, an interest-rate
  regime indicator, and an inflation indicator — explicitly not an
  open-ended "other macro factors" bucket, to avoid multiple-testing risk in
  a regime-conditioned strategy.

## II.16 Sector / industry classification

- **Status:** `[OPEN]` — no source verified. GICS or an equivalent taxonomy
  is required to support the sector-relative security-ranking pipeline
  (§V.2). U.S. large-cap coverage under any standard provider is not in
  doubt; OSE small/mid-cap coverage depth is the specific open question and
  blocks §V.2's pipeline as specified until resolved.

## II.17 Nordnet product/universe reference data

- **API:** `[VERIFIED, decisive]` a technical API exists (`nExt`: REST + SSL
  socket feed, instrument search) but **is not currently onboarding new
  customers.** Not usable as a data source for universe maintenance at this
  time (§III.12).
- **Practical alternative:** Nordnet's own public web pages (fund lists,
  bond lists, ETP/mini-futures lists) — confirmed to exist, usable for
  periodic manual verification, not automated ingestion.

---

# Part III — Investment Universe

## III.1 Eligible asset classes

Core: individual equities (OSE, US primary listings) and mainstream
broad-market ETFs. Secondary/planned: fixed income (via Nordnet-available
bond funds), managed futures and alternative sleeves (via return stacking,
Part V §V.9–V.12), cash/T-bill instruments for the risk-free/financing legs.
Leveraged products (US LETFs, OSE mini-futures/certificates) are eligible
**only** as an explicit leverage-implementation vehicle (§V.8), not as
general portfolio holdings.

## III.2 Geographic scope

Oslo Børs (OSE) and U.S. equities (S&P 500 / Nasdaq). No other markets are in
scope. `[OPEN]` whether the framework should ever extend beyond these two —
not raised or decided in this design process; treat any extension as a new
scope decision, not an implicit one.

## III.3 Listing requirements

Primary listing on Oslo Børs or a major U.S. exchange (NYSE, Nasdaq).
Multiple share classes (e.g., dual-class structures) are treated per standard
data-provider identification; no special handling has been designed for them.

## III.4 Liquidity requirements

`[OPEN, blocked]` an average-daily-volume (ADV) based screen is planned but
not implemented; `data/OSE Data/Liquidity/` exists as a placeholder directory
and is currently empty. Until populated, liquidity screening is not enforced
and this should be treated as a known gap, not a silent pass.

## III.5 Survivorship bias controls

This is the single highest-stakes open item in the project. A backtest run
against today's index constituents, applied to the past, systematically
overstates performance by construction (it measures only the survivors). The
mitigation path (§II.11) is: (1) attempt EODHD's `historical=1` index-
membership mechanism for OSEBX/OSEAX; (2) cross-check against the Euronext
semi-annual index-review archive regardless of (1)'s outcome; (3) if neither
yields a clean multi-decade record, **explicitly disclose and bound the
survivorship exposure** in any reported results rather than proceeding as if
it were solved. This fallback is itself a confirmed decision, not an
avoidance of one.

## III.6 Universe construction, and the active-set mechanism

At each period `t`, the investable universe is the set of assets that are
(a) not yet delisted as of `t` (survivorship-consistent), (b) have a
sufficiently complete return history over the estimation window `[t−est, t−1]`
to support signal and risk estimation, and (c) pass the liquidity/Nordnet-
investability screens below. Because OSE listings have genuinely ragged,
incomplete history (many names have short or gap-ridden series), a naive
"drop any asset with any missing observation" rule would shrink the universe
severely. The recommended mechanism — **`.active_set(M, t)`**, identified in
prior review of a predecessor implementation but not yet ported into
`ENGINE_V1` — marks an asset "active" at `t` if and only if its
`[t−roll, t]` window is fully clean; the optimizer's effective dimension `N_t`
is therefore time-varying, and inactive columns are carried as `NA` rather
than dropped from the panel entirely. This is what makes a ragged,
incomplete-history universe tractable, and Oslo Børs is exactly the kind of
universe this is needed for.

## III.7 Security screening

Liquidity/ADV filter (§III.4, currently unenforced pending data). UCITS-style
basic eligibility screens, if the fund vehicle ultimately requires them — not
independently specified in this design process beyond the general principle
already noted in the Storebrand methodology review (constrained optimization
subject to maximum-weight and other practitioner constraints, §V.5).

## III.8 Sector classification / III.9 Industry classification

Required as an input tag per security (§II.16, `[OPEN]` on source) to support
the sector-relative security-ranking pipeline (§V.2). Until resolved, the
ranking pipeline degrades to its pre-existing global (non-sector-relative)
behavior — a known, acceptable interim state, not a blocking failure.

## III.10 Asset tagging

Each security requires, at minimum: exchange/listing market, sector/industry
classification, currency of denomination, and asset class (equity, ETF, fixed
income, etc.) as persistent metadata — used by the L1 ranking pipeline
(sector grouping), the L0 currency conversion step (§IV.17), and L6 reporting
(exposure breakdowns, §IX).

## III.11 Currency handling

`[CONFIRMED]` Base currency is NOK. All non-NOK securities are translated to
NOK at the point of data ingestion (§IV.17), using unhedged spot-rate
translation — not currency hedging. FX risk is therefore a real, retained
component of every non-NOK asset's risk profile and must enter the covariance
model (§VI) on the NOK-translated return series, not the local-currency one.

## III.12 Nordnet investability requirements

Because Nordnet's API is closed to new customers (§II.17), universe
maintenance cannot be automated against Nordnet directly. **Two-tier
approach:**
1. **Default-tradable, no per-instrument check:** standard OSE-listed and
   major U.S.-exchange common stocks, and mainstream broad-market ETFs —
   standard retail-broker exchange coverage, and the primary universe this
   entire system is built around.
2. **Requires explicit, periodic (recommended: quarterly) manual
   verification** against Nordnet's own public product-list pages: mini
   futures/certificates/warrants (used only for the leverage-vehicle
   question, §V.8), specific bond issues, specific fund share classes.

## III.13 How securities enter and leave the universe

A security **enters** the universe at the first period where it (a) has a
primary listing on OSE or a covered U.S. exchange, (b) has sufficient return
history to satisfy the active-set criterion (§III.6), and (c) passes the
Tier-1 Nordnet-investability default (§III.12). A security **leaves** the
universe at delisting (its full return history up to that date is retained in
the backtest for survivorship correctness, per §III.5) or if it fails the
liquidity screen once that screen is implemented (§III.4). There is currently
no mechanism for provisional/temporary exclusion (e.g., a trading halt) —
this is not designed and should be treated as an open gap if it becomes
relevant.

---

# Part IV — Mathematical Framework

**See `notes/MATHEMATICAL_APPENDIX.md` for the paper-verified, implementation-
grade version of every EPO/TSMOM/XSMOM/GARCH/DCC/transaction-cost formula
below — that document takes precedence on any point of overlap.**

Notation used throughout: `P_t` price at time `t`; `R_t` simple return; `r_t`
log return; `w` portfolio weight vector; `μ` expected-return vector; `Σ`
covariance matrix; `Ω` correlation matrix; `D` diagonal matrix of volatilities
(`Σ = DΩD`); vector quantities are column vectors unless stated otherwise.

### IV.1 Arithmetic (simple) returns
**Expression:** `R_t = P_t/P_{t-1} − 1`.
**Interpretation:** the proportional price change over one period.
**Use:** wherever returns must be additive *across assets* within a period —
portfolio-return aggregation, `w'R`.
**Inputs:** price series. **Outputs:** per-asset return series.
**Dependencies:** none (base calculation).

### IV.2 Log returns
**Expression:** `r_t = ln(P_t/P_{t-1}) = ln(1+R_t)`.
**Interpretation:** the continuously-compounded return; additive *across
time* (`Σr_t` = cumulative log return), unlike simple returns.
**Use:** GARCH/DCC estimation (§IV.5–IV.6), the academic momentum
definition (§IV.16).
**Dependencies:** IV.1.

### IV.3 Excess returns
**Expression:** `Re_t = R_t − Rf_t`.
**Interpretation:** return in excess of the risk-free alternative — the
quantity signal and risk models are actually estimated on, not raw return.
**Use:** feeds `make_moments()` (L2) and all L1 signal construction.
**Critical implementation note:** `Rf_t` here is the **moment-estimation**
risk-free rate (NIBOR for OSE-leg assets, EFFR for US-leg assets, both
**NOK-denominated after §IV.17's conversion**) — not the leverage financing
rate (§IV.11), which is a separate quantity for a separate purpose.
**Dependencies:** IV.1, IV.17 (currency conversion must happen first), the
risk-free-rate purpose-split (§II.9).

### IV.4 FX-adjusted (currency-converted) returns
**Expression:** `R_NOK,t = (1+R_local,t)·(1+R_FX,t) − 1`, where `R_FX,t` is
the percentage change in NOK-per-foreign-currency-unit.
**Interpretation:** decomposes a foreign asset's NOK return into a
local-asset-return component and an FX-return component; the FX component
carries its own volatility and correlation structure.
**Use:** the mandatory first transformation applied to every non-NOK return
series (see §IV.17 for the full statement, including pipeline placement).
**Dependencies:** IV.1 (both legs), an FX rate series (§II.8).

### IV.5 Unconditional (simple) volatility
**Expression:** `σ̂ = sqrt[(1/(T−1))·Σ_t(r_t − r̄)²]`; annualized
`σ_annual = σ_daily·√252` (daily data).
**Use:** baseline/simple volatility feature; fallback when GARCH is
unavailable or has failed to converge.
**Dependencies:** IV.2.

### IV.6 Range-based volatility estimators
Using daily Open (`O`), High (`H`), Low (`L`), Close (`C`), over a window of
`N` periods:
- **Parkinson (1980):** `σ²_P = (1/(4N·ln2))·Σ[ln(H_t/L_t)]²`. Ignores
  overnight jumps; ~5× more efficient than close-to-close.
- **Garman-Klass (1980):** `σ²_GK = (1/N)·Σ[0.5·(ln(H_t/L_t))² −
  (2ln2−1)·(ln(C_t/O_t))²]`. ~7.4× efficiency; still assumes continuous
  trading from the prior close.
- **Rogers-Satchell (1991):** `σ²_RS = (1/N)·Σ[ln(H_t/C_t)·ln(H_t/O_t) +
  ln(L_t/C_t)·ln(L_t/O_t)]`. Drift-independent (fixes the zero-drift
  assumption in Parkinson/GK).
- **Yang-Zhang (2000) — primary estimator:** `σ²_YZ = σ²_overnight +
  k·σ²_oc + (1−k)·σ²_RS`, where `σ²_overnight` is the sample variance of
  `ln(O_t/C_{t-1})`, `σ²_oc` is the sample variance of `ln(C_t/O_t)`, and
  `k = 0.34/(1.34 + (N+1)/(N−1))`. Handles overnight jumps and drift — the
  most complete of the four, and directly relevant given the tactical
  layer's earnings-gap event flag.
**Use:** L2 volatility feature set; a lower-noise substitute for
close-to-close vol, and the closest available proxy to a realized-measure
input given no intraday data source.
**Dependencies:** requires OHLC, not close-only, from L0.

### IV.7 Conditional volatility — GARCH family
Let `ε_t = r_t − μ` (demeaned log return).
- **GARCH(1,1):** `σ²_t = ω + α·ε²_{t-1} + β·σ²_{t-1}`.
- **GJR-GARCH(1,1) — primary estimator:** `σ²_t = ω + α·ε²_{t-1} +
  γ·ε²_{t-1}·1(ε_{t-1}<0) + β·σ²_{t-1}`.
**Interpretation:** `γ` captures the equity leverage/asymmetry effect — a
negative return raises subsequent conditional volatility more than an
equally-sized positive return (Black 1976; Christie 1982), one of the most
robust stylized facts in equity volatility. GJR-GARCH captures this with one
added parameter over plain GARCH.
**Use:** produces `D_t` (the diagonal volatility matrix) feeding
`Σ_t = D_t R_t D_t`.
**Fallback rule:** revert to plain GARCH(1,1) when the asymmetry parameter is
unidentifiable (short/ragged history, common on OSE) or when GJR estimation
fails to converge — an automatic fallback, not a manual override, consistent
with the "fail small and predictably" philosophy (§I.2).
**Dependencies:** per-asset MLE, independent across assets — no scalability
issue at this stage (the scalability constraint is entirely in the
correlation layer, §IV.8).

### IV.8 Conditional correlation — corrected DCC (cDCC)
Standardized residuals: `z_t = ε_t/σ_t` (using §IV.7's `σ_t`).
**Expression:** `Q_t = (1−a−b)·Q̄ + a·z_{t-1}z'_{t-1} + b·Q_{t-1}` (Aielli
2013's corrected recursion — the original Engle 2002 two-step estimator has a
known consistency defect; do not implement the uncorrected version).
Correlation matrix: `R_t = diag(Q_t)^{-1/2}·Q_t·diag(Q_t)^{-1/2}`.
**Interpretation:** captures time-varying co-movement — most informative at
short horizons (spikes toward 1 in crises, i.e., diversification breakdown).
**Critical design note:** `Q̄`, the long-run correlation target, is itself a
sample correlation matrix and inherits the same Marchenko-Pastur estimation
noise that motivates shrinkage/RMT (§IV.9–IV.10) — DCC does not solve
estimation-error noise, it adds time-variation on top of whatever target is
supplied. `Q̄` must be cleaned via §IV.9 before the recursion is applied.
**Routing rule:** feed the SAA optimizer a **slow-moving** correlation
estimate (the cleaned `Q̄`, refreshed low-frequency, or a long rolling
window); feed the **fast**, daily `R_t` to the regime layer (§VI.9, §VII) as
a correlation-breakdown diagnostic/trigger, not directly into rebalancing
weights. This resolves the tension between wanting correlation to be
"dynamic" and wanting the portfolio to be "stable" — each need is routed to
the layer that actually requires it.
**Large-N fallback:** DECO (Engle & Kelly 2012) — a single equicorrelation
`ρ_t` across all pairs, `O(N)` rather than `O(N²)` computation — gated by
universe size the same way RMT is (§IV.10).
**Dependencies:** §IV.7's `D_t`, §IV.9's cleaning operator.

### IV.9 Correlation shrinkage (implemented)
**Expression:** `Ω_w = (1−w)·Ω + w·I`; reconstruction `Σ = D·Ω_w·D`
(variances preserved — only correlations are shrunk).
**Interpretation:** this is EPO's core mechanism (Pedersen, Babu & Levine
2021, Eq. 7/15) and is identical to "basic linear shrinkage" in the Random
Matrix Theory cleaning literature (Bun, Bouchaud & Potters 2016/2017,
"Cleaning correlation matrices") — pulling every eigenvalue of the sample
correlation matrix linearly toward 1 (i.e., toward the identity), which
counteracts Markowitz's tendency to over-allocate to the smallest,
noise-dominated eigenmodes.
**Implementation:** `operators/shrinkage.R::shrink_corr`, default
`w = CONFIG$epo_w = 0.75` (Pedersen, Babu & Levine's own empirical finding of
~0.75 as a reasonable starting intensity).
**Use:** L2 operator, applied to any base correlation estimate (static
sample, or DCC's `Q̄`) before it reaches a solver.

### IV.10 Random Matrix Theory (RMT) cleaning — experimental, gated by N
**Background:** the sample correlation matrix `E = (1/T)XX'` has eigenvalues
that are a *broadened* version of the true matrix's spectrum (Marchenko-
Pastur, 1967): small eigenvalues are biased downward, large eigenvalues
biased upward. Since Markowitz-style inversion (`Σ⁻¹`) over-weights the
smallest, most noise-dominated eigenmodes, this is a first-order source of
out-of-sample portfolio blow-ups.
**The Rotationally Invariant Estimator (RIE)** — the theoretically optimal
cleaning recipe among those reviewed (Ledoit-Péché 2011; Bun & Knowles 2016;
detailed algorithm and full verification already recorded in
`notes/covariance/rmt_background.md`, not reproduced in full here) — keeps
the sample eigenvectors and replaces each eigenvalue `λ_k` with a nonlinear,
debiased estimate `ξ̂_k`, converging to the oracle `⟨u_k, C u_k⟩` as `N,T→∞`
jointly. Pedersen, Babu & Levine's own appendix implementation is this
RIE algorithm plus a sort-by-size step and a trace-preserving rescale.
**Status:** `[EXPERIMENTAL]`, gated by universe size — the RIE is a
large-`N` asymptotic tool; on a small panel (e.g., `N=6`, `q=N/T≈0.05`) it is
essentially a no-op and the underlying asymptotics do not hold. **Do not
build until a large-N universe (order tens to ~50+ names or more) is loaded**
— this is a direct extension of the project's own empirically-derived
threshold (see §IV.9/§V.7's FF49 finding on `q`). Linear shrinkage (§IV.9)
is the correct tool below that threshold.
**Related, also reviewed but not implemented, `[EXPERIMENTAL/PARKED]`:**
Ledoit & Wolf (2003) shrinkage toward a single-index target (needs a market
index as an extra input); Ledoit & Wolf (2004) shrinkage toward a scaled
identity (shrinks variances, not just correlations — a materially different
object from EPO's correlation-only shrinkage, kept conceptually distinct);
Wang (2005) — an *expected-return*, not covariance, shrinkage method,
belonging to the anchored-EPO/Black-Litterman branch rather than the
Ledoit-Wolf covariance branch. Full literature notes for all three are
recorded in `notes/shrinkage/`.

### IV.11 Portfolio expected return, variance, volatility
- **Expected return:** `μ_p = w'μ`.
- **Variance:** `σ²_p = w'Σw`.
- **Volatility:** `σ_p = sqrt(w'Σw)`.
**Use:** every solver call; L6 performance reporting.
**Dependencies:** L1 output (`μ`), L2 output (`Σ`), L3 output (`w`).

### IV.12 Portfolio construction — solver menu

| Solver | Expression | Notes |
|---|---|---|
| Equal weight | `w_i = 1/N` | Baseline; ignores `μ` and `Σ` entirely |
| Tangency (unconstrained) | `w ∝ Σ⁻¹μ`, normalized `w=Σ⁻¹μ/(1'Σ⁻¹μ)` | Highest combined sensitivity to `μ` and `Σ` estimation error |
| Minimum variance | `w=Σ⁻¹1/(1'Σ⁻¹1)` (unconstrained closed form) | Ignores `μ`; high sensitivity to `Σ` only |
| Naive risk parity (vol) | `w_i ∝ 1/σ_i` | Uses only `diag(Σ)` — **never reads the correlation matrix** |
| Naive risk parity (var) | `w_i ∝ 1/σ_i²` | Same property as above |
| True risk parity | solve `Σw = λ·b/w` (Newton's method) for equal risk contribution | Uses full `Σ`, moderate sensitivity |
| Maximum diversification | `w ∝ Σ⁻¹σ` | Uses full `Σ`, high sensitivity |
| Mean-variance, risk aversion `γ` | `λ=(1'Σ⁻¹μ−γ)/(1'Σ⁻¹1)`; `w=Σ⁻¹(μ−λ·1)/γ`, normalized to sum 1 | `γ` is a genuine preference parameter here — see the γ note below, not a fixed constant |
| EPO (simple) | `w = Σ_w⁻¹s` (unnormalized — correct for a zero-sum long/short signal `s`) | `Σ_w` is `Σ` after §IV.9's shrinkage; `γ=1` fixed by construction — see γ note below |
| **EPO (anchored)** | see below | `Σ_w⁻¹` applied to a *blended* signal, not the raw one |

**Anchored EPO** (Pedersen, Babu & Levine 2021, Eq. 14/17) — `[VERIFIED
against `operators/anchor.R`, this omission corrected]`. This is a distinct,
already-implemented solver-plus-operator combination, not a variant of
simple EPO, and belongs in this table. It blends the raw signal toward an
**anchor portfolio** `a` (e.g., equal-weight, `a_i=1/N`, or inverse-vol,
`a_i=(1/σ_i)/Σ(1/σ_j)`) before the `epo` solver runs — using the **same**
shrinkage intensity `w` that already governs correlation shrinkage (§IV.9),
so one parameter controls both the covariance treatment and how far the
portfolio is pulled toward the anchor. Two modes, both implemented:
- **Eq. 14 (fixed `γ`):** `μ' = (1−w)·(1/γ)·s + w·V·a`.
- **Eq. 17 (endogenous `γ` — the default mode, `gamma_mode="endogenous"`):**
  `μ' = (1−w)·k·s + w·V·a`, where
  `k = sqrt[(a'Σ̃a) / (s'Σ_w⁻¹Σ̃Σ_w⁻¹s)]` — chosen so the raw-signal book's
  variance is matched to the anchor book's variance before blending, rather
  than requiring the user to specify a `γ`.
Here `V = diag(variances)` (preserved through shrinkage, §IV.9), `Σ̃` is the
pre-shrinkage ("tilde") covariance, `Σ_w` is the shrunk covariance, `s` is
the raw L1 signal. The blended `μ'` then feeds the same `epo` solver:
`x = Σ_w⁻¹μ'`. **Boundary conditions** (already numerically verified in
`STATUS.md` against an independent monolithic reimplementation, to residual
levels attributable only to a `1e-10` ridge term): `w=0` recovers the pure
(scaled) signal MVO direction; `w=1` gives `x = a` exactly.
**Use:** the recommended production form of EPO when a specific, defensible
default portfolio (equal-weight, inverse-vol, or a supplied benchmark/TAA
vector) is preferred as the shrinkage target, rather than shrinking purely
toward the uninformative identity-correlation direction that simple EPO
implies. **Dependencies:** §IV.9's `shrink_corr` (must run first in the
`params$ops` pipeline so `Σ_pre`/`Σ̃` is available), the anchor choice `a`.

**A note on `γ` — do not treat it as a single, arbitrary constant across
the table.** `γ` means different things in different rows, and conflating
them is a real error to guard against:
- **In the `epo` solver, `γ=1` is fixed by construction, and is a
  mathematical convenience, not a risk-preference statement.** The
  zero-sum long/short EPO book's Sharpe ratio is invariant to `γ` (scaling
  `γ` just rescales the book's gross exposure, not its risk-adjusted
  return), so the codebase fixes it at 1 and lets `apply_overlay()` (§IV.14)
  handle actual sizing separately. Do not read this `γ=1` as advice for any
  other solver.
- **In classical mean-variance (`meanvar_ra`), anchored EPO's Eq. 14 mode,
  and the leverage overlay (§IV.14, `l=clip(μ_w/(γ·σ²_w),…)`), `γ` is a
  genuine CRRA-style risk-aversion coefficient and directly determines
  portfolio sizing and leverage** — it should reflect the actual investor's
  risk tolerance, not an unexamined default. `[VERIFIED against
  `core/config.R`]` the current system-wide default is `CONFIG$gamma = 5`,
  documented in the code itself as "CRRA / mean-variance risk aversion
  (drives leverage)" — not 1, and not arbitrary; `core/registry.R` already
  anticipates this being overridden per strategy (its own example:
  `list(lower=0, upper=0.5, gamma=9)`, i.e., a more risk-averse setting than
  the default). **Recommendation:** treat `γ` as a deliberately chosen,
  per-strategy `REGISTRY` parameter reflecting the specific investor's or
  strategy's risk tolerance — typical CRRA calibrations in the academic and
  institutional literature range roughly from `γ≈2` (aggressive) to `γ≈10`
  (conservative); `γ=1` sits below that range (near risk-neutral) and is
  not a reasonable default for sizing a real portfolio or its leverage.
  Because the same `γ` also drives `apply_overlay()`'s leverage ratio,
  changing it has consequences beyond the `meanvar_ra` weights alone —
  calibrate once, deliberately, and be aware it is not a locally-scoped
  choice.

**Design rule (solver-specific risk treatment):** because sensitivity to
correlation-matrix quality varies sharply by solver (the naive risk-parity
family never even reads `Ω`), each `REGISTRY` row should specify its own
`Σ`-cleaning operator pipeline rather than assuming one global treatment —
already supported by the existing per-strategy `params$ops` mechanism, no
new architecture required.
**Dependencies:** L1 `μ`/`s`, L2 `Σ`.

### IV.13 Efficient frontier
For a target return `μ_p`, minimize `w'Σw` subject to `w'μ=μ_p`, `w'1=1`.
Closed form via the two-constraint Lagrangian: let `A=1'Σ⁻¹1`, `B=1'Σ⁻¹μ`,
`C=μ'Σ⁻¹μ`, `D=AC−B²`. Then:
`σ²_p(μ_p) = (A·μ_p² − 2B·μ_p + C) / D`.
**Use:** research/reporting visualization of the achievable risk-return set
(§IX.6); not required by any currently-implemented solver, each of which
targets a single point on or near this frontier rather than tracing it.

### IV.14 Capital Allocation Line (CAL) and leverage
**CAL:** `E[R_p] = Rf + [(E[R_tan]−Rf)/σ_tan]·σ_p` — a straight line from
`(0,Rf)` through the tangency portfolio; slope = tangency Sharpe ratio.
Under unequal borrowing/lending rates the line **kinks** at the tangency
point and is flatter above it (the borrowing segment).
**Leverage overlay (as implemented):** `l = clip(μ_w/(γ·σ²_w), l_min, l_max)`,
final weights `= l·w`.
**Financing-cost-corrected levered return (required fix, not yet
implemented):** `R_levered,t = l·R_p,t − (l−1)·financing_rate_t` — replaces
the current implicit assumption that borrowing is frictionless at `Rf`.
`financing_rate_t` is the *leverage-financing* rate (§II.9), not the
moment-estimation risk-free rate — these are two distinct quantities that
the current single-`Rf` design conflates.
**Leveraged-ETF compounding (US leg only — see §IV.15 for why this does not
extend to the OSE leg):**
`V_T/V_0 = Π_t(1+k·r_t)`; in log form, `ln(V_T/V_0) ≈ k·Σr_t −
½k(k−1)·Σr_t² ≈ k·Σr_t − ½k(k−1)·σ²T`.
The second term is a volatility-drag cost relative to a naive
`k×`-cumulative-return benchmark. **This term applies to any frequently-
rebalanced constant-leverage-ratio strategy**, not only ETF-wrapped ones — a
margin position rebalanced daily to a constant target `l` (exactly what
`apply_overlay()` does if re-applied every period) incurs the same
`−½l(l−1)σ²T` drag by the identical derivation. What margin borrowing avoids
by *not* rebalancing to a fixed ratio is the drag; what it reintroduces
instead is leverage-ratio drift (toward a margin call in drawdowns, toward
under-exposure in rallies).
**Magnitude, for context:** at 16% annualized equity volatility, `k=2` costs
≈2.6%/year against the naive expectation; `k=3` costs ≈7.7%/year; these
figures roughly triple to quadruple at 30%+ annualized (stressed) volatility.

### IV.15 Mini-future / structured-leverage instrument mathematics — OPEN
**[OPEN, not derived]** the Nordnet-accessible OSE-leg leverage vehicle
(mini futures/certificates, §II.3) is built around a financing level and a
knock-out/barrier mechanism, not daily-reset NAV compounding. §IV.14's
`k(k−1)σ²T` derivation does **not** apply to this instrument class — it
carries additional barrier/gap risk with its own payoff structure. This
mathematics has not yet been derived in this design process and must be
completed before this instrument is used as a leverage-implementation
vehicle on the OSE leg (see §XI for the corresponding outstanding item).

### IV.16 Security ranking / factor-score normalization
- **Z-score:** `Z = (x−μ)/σ`. Preserves magnitude; used to combine
  heterogeneous raw metrics into one composite meaningfully.
- **Demeaned rank:** `R = rank(x) − mean(rank(x))`. Identical to
  Asness, Moskowitz & Pedersen (2013), Eq. 1. Bounds any single name's
  influence to `1/N` regardless of outlier magnitude — outlier-robust by
  construction.
- **Percentile rank:** `100·rank(x)/N`.
- **Sector-relative application:** apply any of the above **within** each
  sector group rather than globally. This is mathematically safe: all three
  transforms are exactly zero-sum within any group they are applied to
  (subtracting a group mean cannot change the group's own sum), so
  group-wise application is a strictly stronger version of the same
  zero-sum property, not a different one.
- **Composite score:** `Score = Σ_k w_k·Z_k` — weighted sum of standardized
  metrics, computed within-group.
- **Full four-stage production pipeline** (see §V.2 for the complete
  specification and rationale): group → within-group z-score composite →
  demeaned-rank output → feeds `μ`.
**Academic momentum lookback** (for the momentum metric specifically):
`M = P_{t-1}/P_{t-12}` (12-month lookback, skipping the most recent month) —
the standard "12-1" convention.

### IV.17 Currency conversion — restated formally (see §III.11, §IV.4)
`R_NOK,t = (1+R_local,t)(1+R_FX,t) − 1`. **Location: L0, immediately after
computing local-currency returns, before any other calculation** — so every
downstream quantity (`μ`, `Σ`, `w`, reported performance) is NOK-denominated
throughout, and no downstream layer has to separately track currency.
**Excess-return convention:** subtract the **NOK** risk-free rate from the
NOK-converted total return of every asset, regardless of listing market —
never subtract a local risk-free rate from a local return and convert
afterward, which would produce a currency-inconsistent excess return.

### IV.18 Turnover and transaction costs
**Turnover (drift-adjusted, one-way):**
`τ_t = ½·Σ_i|w_{i,t} − w^{drift}_{i,t}|`, where
`w^{drift}_{i,t} = w_{i,t-1}(1+R_{i,t}) / (1+Σ_j w_{j,t-1}R_{j,t})` — the
pre-trade weight after price drift. **Not** a naive weight difference, which
would conflate drift with actual trading and overstate cost.
**Transaction cost:** `TC_t = Σ_i c_i·|Δw_{i,t}|·V_t`, where `c_i` is a
blended per-asset rate (Nordnet Mini commission tier + FX spread where
applicable + slippage estimate, §VII.5).
**Net return:** `R_net,t = R_gross,t − TC_t/V_t`.

### IV.19 Risk-adjusted performance measures
- **Sharpe ratio:** `SR = (R̄_p−R̄f)/σ_p`, annualized `SR·√252`.
- **Sortino ratio:** `(R̄_p−MAR)/σ_downside`,
  `σ_downside = sqrt[(1/T)Σ_t min(R_t−MAR,0)²]`.
- **Information ratio:** `IR = (R̄_p−R̄_bench)/TE`, `TE = std(R_p−R_bench)`.
- **Appraisal ratio:** `α_Jensen/σ_ε` from `R_{p,t}−Rf_t = α + β'F_t + ε_t`
  (Newey-West standard errors; `F` = the OSE/US factor set, §II.14).
- **Maximum drawdown:** `MDD = min_t(V_t/max_{s≤t}V_s − 1)`.

### IV.20 Position sizing and volatility targeting
`w_scaled = w·(σ_target/σ_p)` — scales a solver's raw weights to a target
portfolio volatility, using §IV.11's `σ_p`. Necessary to compare strategies
on a common risk footing (an arbitrary-scale output like `Σ⁻¹μ` is not
directly comparable to a sum-to-one output like equal weight on any basis
except Sharpe).

### IV.21 Rebalancing mathematics
**Threshold trigger:** rebalance asset `i` if `|w_{i,t}−target_i| > band_i`.
**Hybrid (default):** evaluate the threshold check only at scheduled
calendar points rather than continuously — combines calendar predictability
with threshold turnover discipline.

### IV.22 Constraint mathematics
- **Box constraints (long-only, position limits):** `lb_i ≤ w_i ≤ ub_i` for
  each asset — already implemented via `.bound()` in the constrained solvers.
- **Linear group constraints (sector/factor caps):** `Σ_{i∈group} w_i ≤ cap`
  — expressible as additional rows in a linear-inequality constraint matrix;
  the current `constrOptim`-based implementation can technically accept
  these but is already documented as slow at `N≈49`, so **migrate to a
  proper QP solver (`quadprog`/`osqp`) before adding these constraints**,
  rather than compounding a known performance problem.
- **Turnover constraint, preferred form (soft penalty):** add
  `λ·Σ_i|Δw_i|` to the optimization objective rather than imposing a hard
  cap `Σ|Δw_i| ≤ τ_max`, which can render the problem infeasible when the
  true optimum requires large repositioning.
- **Theoretical grounding for constraints generally:** Jagannathan & Ma
  (2003) show that no-short-sale constraints are approximately equivalent to
  a specific form of covariance shrinkage — constraints and shrinkage (§IV.9)
  are substitutes for correcting the same estimation-error problem, not
  unrelated design axes. This motivates treating "which constraints are
  on by default" as a shrinkage-intensity-like decision, not an arbitrary
  practitioner preference.

### IV.23 Leverage mathematics — see §IV.14 (CAL/margin/LETF) and §IV.15
(mini-futures, open)

### IV.24 Return stacking (generalized)
`R_stacked,t = R_base,t + StackSize·Σ_i Weight_i·(R_sleeve,i,t − Fee_i/12 −
(Rf_t + Financing_i/12))`.
**Variable definitions:** `R_base,t` — the core SAA sleeve's realized return
(the existing solver-output `PANEL`); `i` — index over one or more
diversifying sleeves (market-neutral, managed futures, merger arbitrage,
commodities, etc.); `Weight_i` — fixed blend weights within the alternative
sleeve; `StackSize` — notional scale of alternative exposure per dollar of
base capital; `Fee_i` — annualized cost of accessing sleeve `i`;
`Financing_i` — annualized spread over the risk-free rate required to carry
sleeve `i`'s notional exposure; `Rf_t` — the NOK risk-free rate (§II.9,
consistent with §IV.3/§IV.17).
**Economic interpretation:** at `StackSize=0`, identical to the base
portfolio. This generalizes §IV.14's single-position leverage overlay to
*adding a separate, independently-selected return stream* on top of an
unchanged base — a genuinely different operation from re-scaling exposure to
the same tangency-style portfolio (moving along a fixed CAL vs. shifting to a
different, hopefully better, frontier via genuine diversification).
**Use:** a new L4 module, architecturally distinct from `apply_overlay()` —
operates on realized/backtested return panels, not inside the per-period
solver dispatch.
**Dependencies:** each sleeve's own return series; the NOK risk-free rate.

---

# Part V — Portfolio Construction

This part describes the sequential steps the system executes, per rebalance
period, to go from raw data to a set of implementable portfolio weights.

## V.1 Factor calculations

Raw metrics computed per security per period: value (price/earnings,
price/book — planned, not built), momentum (12-1 month, implemented as
`mom12_1`), quality/profitability (planned, not built). Each metric is a
simple, well-established, economically-motivated quantity — no composite
or opaque scoring at this stage (§IV.16, §V.2 handle combination).

## V.2 Security scoring — the four-stage ranking pipeline

This is the confirmed, retained methodology, synthesized from two competing
reference approaches examined during design (the Storebrand/Sørensen
practitioner method and the Asness/Moskowitz/Pedersen 2013 academic
method) rather than adopting either wholesale:

1. **Group** each security by sector/peer classification.
2. **Within-group z-score** each raw metric (`Z=(x−μ)/σ` computed inside the
   sector group, not globally) — necessary to combine metrics of different
   scale (e.g., P/E and P/B) meaningfully; this is the Storebrand mechanism.
3. **Weighted composite** across metrics: `Score = Σ_k w_k·Z_k`.
4. **Final demeaned-rank transform** applied to the composite
   (`rank(Score) − mean(rank(Score))`, computed within-group) before it
   feeds `μ` — this is the Asness/Moskowitz/Pedersen (2013) mechanism,
   chosen for outlier robustness (bounds any single name's influence to
   `1/N`) and turnover stability.

**Why this specific combination, not one method alone:** the two reference
methods solve different problems. The academic method (simple signal,
rank-weighted, no downstream optimizer) is designed to measure a factor's
return premium as cleanly as possible with minimal data-mining risk — a
research/validation tool. The practitioner method (multi-metric z-score
composite feeding a constrained optimizer) is designed for actual
implementation subject to real-world constraints. This system needs both
roles: the academic method's simple rank-weight formula is reserved as a
**validation tool** for any new candidate metric (confirm genuine predictive
power before promoting it into production); the composite-then-rank pipeline
above is the **production** methodology feeding `μ`.

**Sector-neutrality rationale:** isolates stock-selection alpha from
industry-momentum contamination (Moskowitz & Grinblatt, 1999, "Do Industries
Explain Momentum?", *Journal of Finance* 54(4)) — a large share of
naively-measured individual-stock momentum profit is actually industry
momentum. Sector-neutral construction prevents the selection signal from
smuggling in an unacknowledged sector bet, and makes any deliberate,
explicit sector allocation decision (§VII.6) meaningful rather than
accidental.

**Implementation:** extends the existing `cs_signal`/`.cs_transforms`
machinery (`signals/cross_sectional.R`) with a `group` argument — no new
architecture required, since all three existing transforms (demean, z-score,
rank) are already exactly zero-sum and remain so when applied within a group.

## V.3 Ranking methodology — see §V.2 (single unified specification)

## V.4 Universe selection

Applied before the optimizer runs, per §III.6–III.7: point-in-time active
set (ragged-history-aware), liquidity screen (pending data), Nordnet
investability tier (§III.12).

## V.5 Portfolio optimization

The solver menu (§IV.12) is dispatched via the `REGISTRY` — each strategy
row names a solver, a signal, a risk-operator pipeline, and a parameter set.
Signal and risk are independently swappable (§I.3); the same solver can be
run against different `μ`/`Σ` combinations to isolate where performance
comes from.

## V.6 Constraint handling

Default-on: long-only box bounds, per-asset position limits (minor extension
of the existing `.bound()` mechanism). Optional, gated on a QP-solver
migration (§IV.22): sector caps, factor caps, hard turnover caps. Preferred
turnover form: soft penalty, not hard cap. Optional, gated on liquidity data:
ADV-based position caps.

## V.7 Long-only implementation

The default mode: box constraints `0 ≤ w_i ≤ ub_i`, `Σw_i=1`. Already
implemented in `min_var` and `tangency_con` via `.bound()` and
`constrOptim`.

## V.8 Long/short implementation

**Confirmed design rule:** long/short is a **signal property**, not a solver
property — a demeaned (zero-sum) signal fed to the `epo` solver naturally
produces an unnormalized long/short weight vector (the sum of weights need
not be 1, correctly, for a zero-sum signal). Long-only is imposed
separately, at the constraint (L4) layer. This is already implemented and
locked, not a new decision.

## V.9 Sector handling

Two distinct uses, not to be conflated: (1) **sector-relative scoring**
within the security-ranking pipeline (§V.2) — always applied when sector
data is available; (2) **sector exposure caps** as a portfolio constraint
(§V.6) — optional, gated on the QP-solver migration, and conceptually
separate from (1). Sector-neutral scoring does not by itself guarantee
sector-neutral portfolio weights; if that guarantee is required, an explicit
cap (2) is needed as well.

## V.10 Position sizing

`scale_to_vol` (§IV.20) — applied after the raw solver output, to place
every strategy on a common risk footing before comparison or before applying
leverage (§V.11).

## V.11 Leverage

**US leg:** `apply_overlay()` (§IV.14), financing-cost-corrected — subtract
the actual Nordnet margin rate (7.32%, confirmed) from levered excess
return, not the moment-estimation risk-free rate. Leveraged ETFs are a
supported, empirically-comparable alternative implementation vehicle for the
same target leverage ratio, to be resolved by a direct backtest comparison
against margin (not by theory alone) — see Part X for sequencing.
**OSE leg:** the Nordnet-accessible vehicle is a mini-future/certificate, a
structurally different instrument (§IV.15) whose mathematics remains open;
do not apply the US-leg LETF analysis to this leg.

## V.12 Return stacking / portable alpha

Generalized architectural pattern (§IV.24), not limited to any specific
sleeve. **Build-cost-ordered sleeve priority:**
1. **Market-neutral (cheapest — reuses existing machinery entirely).**
   Running an existing signal (e.g., `xsmom`) through the `epo` solver
   *without* the long-only constraint is already a market-neutral strategy
   in the return-stacking sense — no new signal, no new data.
2. **Managed futures / trend-following** — in-house construction, §V.13.
3. **Merger arbitrage** — external proxy (`MNA` ETF, §II.7), not an in-house
   deal-spread build.
4. **Commodities (direct)** — liquid ETF/futures proxy, low build cost.
5. **Parked:** global macro (lacks the clean academic foundation TSMOM/XSMOM
   have; relies on discretionary or complex multi-factor judgment, a poor
   fit for a rules-based engine); broad alternative risk premia (diffuse,
   heavier data needs); fixed-income strategies distinct from the core bond
   holding (could reuse existing signal machinery later, not prioritized
   now).
**Architectural requirement:** extends `REGISTRY` to support a stacked-
strategy type (base row + one or more sleeve rows + stack parameters) — a
genuinely new L4 capability, operating on realized return panels rather than
inside the per-period solver dispatch `apply_overlay()` runs in.

## V.13 Managed futures integration — in-house construction

- **Signal:** time-series momentum (`ts_signal`, planned) — sign of trailing
  return over one or more lookback windows.
- **Asset classes (start minimal, not a full CTA-scale universe):** equity
  index futures, a small number of government bond futures, major currency
  pairs, a small commodity basket. Consistent with the "start small, add
  complexity only when justified" philosophy (§I.2); Moskowitz, Ooi &
  Pedersen (2012) use ~58 instruments in the original TSMOM paper, which is
  not the recommended starting scope here.
- **Position sizing:** volatility-scaled per instrument,
  `w_i ∝ sign(trend_i)/σ_i` — mathematically identical to the
  already-implemented `naive_vol_rp` solver mechanism, just applied to a
  time-series signal over a futures universe rather than a cross-sectional
  signal over equities. Likely requires only the new `ts_signal` and a new
  data universe, not new solver code.
- **Sleeve-level risk management:** scale the combined sleeve to a target
  annualized volatility (§IV.20's `scale_to_vol`, e.g. 10%, a standard CTA
  convention).
- **Rebalancing:** likely a higher-frequency, sleeve-specific cadence than
  the core SAA sleeve — already supported by the per-strategy
  `rebalance_rule` parameter, no new architecture.
- **Data requirement, open:** continuous, roll-adjusted futures price
  series — verify roll-adjustment quality before building (§II.6, §XI).
- **Validation, not construction, role for SG Trend Index:** a periodic
  sanity check that the in-house sleeve's risk-adjusted performance and
  equity-correlation profile are broadly consistent with a professional
  index — not a data source to build against, and not investable directly
  even with full data access.

## V.14 Alternative investments

Merger arbitrage (MNA proxy), gold (no barrier), commodities (liquid ETF
proxy) — see §II.7, §V.12.

## V.15 Risk budgeting

The naive and true risk-parity solver families (§IV.12) already implement
risk budgeting for the core equity sleeve; the managed-futures sleeve
applies the same per-instrument vol-scaling logic within its own universe
(§V.13).

## V.16 Volatility targeting

See §IV.20 — applied at both the core-sleeve level (before comparing
strategies) and the managed-futures-sleeve level (§V.13), as two separate
applications of the same mechanism.

## V.17 Transaction costs

See §IV.18, §VII.5 for the full cost-model specification. Applied uniformly
across every strategy, always reported gross and net (§IX.1).

## V.18 Rebalancing

Hybrid (calendar-check, threshold-trigger) as the default policy; calendar-
only and threshold-only also selectable. Exposed as a per-strategy
`REGISTRY` parameter (`rebalance_rule`) — no new architecture, consistent
with the existing "solver + params + tier = strategy" design.

---

# Part VI — Risk Model

Status legend used throughout this part: `[CONFIRMED]` in the near-term build
path; `[EXPERIMENTAL]` reviewed and specified but gated on a stated
condition; `[PARKED]` considered, consciously deferred; `[OPEN]` genuinely
undesigned as of this document.

## VI.1 Volatility estimation — `[CONFIRMED]`

GJR-GARCH(1,1) primary, GARCH(1,1) automatic fallback (§IV.7). Range-based
estimators (Yang-Zhang primary, Garman-Klass cross-check, §IV.6) as a
lower-noise alternative and as the closest available proxy to a realized
measure given no intraday data.

## VI.2 Correlation estimation — `[CONFIRMED]`

cDCC (Aielli-corrected, §IV.8) for dynamic correlation, feeding the SAA
optimizer a slow-refreshed, shrunk estimate and the regime layer a fast
daily one. DECO `[CONFIRMED as the large-N fallback]`, gated by universe
size.

## VI.3 Covariance estimation — `[CONFIRMED]`

`Σ_t = D_t R_t D_t` (§IV.8, §IV.11). Solver-specific treatment via the
`params$ops` pipeline (§IV.12's design rule).

## VI.4 Shrinkage — `[CONFIRMED, partially built]`

`shrink_corr` (§IV.9) is implemented and is EPO's core mechanism. Ledoit &
Wolf (2003, 2004) and Wang (2005) variants are reviewed in full in
`notes/shrinkage/` and summarized in §IV.10 — `[EXPERIMENTAL/PARKED]`, kept
as benchmark comparisons rather than adopted as the production mechanism.

## VI.5 Random Matrix Theory — `[EXPERIMENTAL]`

RIE cleaning (§IV.10), gated on a large-N universe existing. A no-op and
untestable at the current small-panel scale. Full algorithm in
`notes/covariance/rmt_background.md`.

## VI.6 DCC — `[CONFIRMED]`

See VI.2/§IV.8.

## VI.7 HEAVY models — `[EXPERIMENTAL, blocked on data]`

DCC-HEAVY / DECO-HEAVY (Bauwens & Xu, 2023, *International Journal of
Forecasting* 39(2), 938–955, reviewed directly) replace the GARCH/DCC
recursion's driving input (lagged squared/cross daily returns) with a
realized measure built from intraday data — structurally a minimal-surgery
upgrade to the same recursion, not a different model family, so building
cDCC now does not foreclose this upgrade later. **Blocked entirely on
acquiring an intraday data source**, which does not currently exist in this
project's data architecture (Part II). Revisit jointly with the
Realized-GARCH question (§IV.7) if intraday data is ever acquired — they
would share the same realized-measure construction step.

## VI.8 DECO — `[CONFIRMED as large-N fallback]`

See VI.2.

## VI.9 Regime detection — `[CONFIRMED]`

Adopted as a **risk-overlay input**, not a hard security-selection filter:
(a) regime-conditioned `γ` in `apply_overlay()` (Moreira & Muir, 2017,
"Volatility-Managed Portfolios," *Journal of Finance* 72(4)); (b) the fast
DCC `R_t` correlation-breakdown signal as a de-risking/rebalancing trigger.
Macro inputs: VIX, EPU, TPU, an interest-rate regime, an inflation
indicator — a **bounded, pre-specified list**, deliberately not an
open-ended "other macro factors" bucket, to avoid multiple-testing/data-
snooping risk in a regime-conditioned strategy. `[OPEN]` whether a
Norway-specific regime factor (Brent oil price, given OSEBX's energy
weighting) should be added — flagged, not decided. Hard security-selection
filtering based on regime is `[PARKED]`, pending its own whipsaw-cost
backtest.

## VI.10 Stress testing — `[OPEN, not yet designed]`

No stress-testing framework has been specified in this design process. This
is recorded honestly as a gap, not filled in with an invented framework —
see Part XI for the corresponding outstanding item and Part X for where it
belongs in the build sequence (after the core risk model and regime layer
are operational).

## VI.11 Scenario analysis — `[OPEN, not yet designed]`

Same status as VI.10 — not discussed in this design process; recorded as an
outstanding item rather than fabricated here.

## VI.12 Risk monitoring — `[CONFIRMED at a basic level]`

Realized-vs-modeled volatility/correlation checks, a regime-state dashboard,
and drawdown tracking against `max_lev`/constraint limits are specified as
required L6 outputs (§IX.7) at a basic diagnostic level. A fuller risk-
monitoring framework (limit breaches, automated alerts) is `[OPEN]`,
downstream of live implementation (§I.7), which is itself not yet scoped.

---

# Part VII — System Constraints

## VII.1 Portfolio constraints

Long-only box bounds and per-asset position limits: default on. Sector caps,
factor caps, hard turnover caps: optional, gated on the QP-solver migration
(§IV.22). Preferred turnover form: soft penalty in the objective, not a hard
cap.

## VII.2 Position limits

Per-asset upper bound `ub_i` (already supported via `.bound()`); default
value not yet fixed — a `[user-configurable]` `CONFIG` parameter.

## VII.3 Leverage constraints

`l_min`, `l_max` bound the overlay's leverage ratio (`CONFIG$min_lev`,
`CONFIG$max_lev`, currently `0.1`/`1.5`). **`[OPEN]`** `max_lev=1.5` is not
documented as derived from Nordnet's actual margin maintenance/LTV terms —
treat as a placeholder pending verification, not a calibrated risk limit.

## VII.4 Liquidity constraints

ADV-based position cap: designed but not implemented, blocked on populating
`data/OSE Data/Liquidity/` (currently empty).

## VII.5 Trading constraints

Nordnet tradability tiers (§III.12); mandatory investor knowledge test
before first purchase of complex ETPs (mini futures, certificates,
warrants) — a compliance gate external to this system's own logic, but
relevant to which instruments the leverage-implementation layer (§V.11) can
actually use. Transaction cost model: Nordnet Mini commission (0.15%/29 NOK
minimum, Nordic; 0.2%/49 NOK minimum, foreign; ~52,667 NOK per-trade
breakeven where the minimum fee dominates the percentage rate) + FX spread
(`[OPEN]` exact Nordnet spread not confirmed; Norges Bank mid-rate is a
valuation reference, not a cost figure) + bid-ask/market-impact slippage for
thin OSE names, modeled separately (half-spread × ADV-participation).

## VII.6 Rebalancing constraints

Hybrid calendar+threshold default, per-strategy `rebalance_rule`. `[OPEN]`
tax treatment: Aksjesparekonto (ASK) wrapper likely defers capital-gains tax
on intra-account EU/EEA rebalancing `[ASSUMED, needs confirmation of actual
account type]`; U.S.-listed shares likely fall outside ASK eligibility
`[OPEN, moderate confidence, not fully verified]` — if so, every US-leg
rebalancing trade is a realization event, an asymmetric cost between the
two markets that the framework should model explicitly once resolved.

## VII.7 Sector rules

Sector-relative scoring (§V.2): always applied when sector data is
available (`[OPEN]` on data source, §II.16). Sector exposure caps as a hard
constraint: optional, separate decision (§V.9).

## VII.8 Currency rules

NOK base, unhedged translation (§III.11, §IV.17). No hedging instrument is
currently in the design.

## VII.9 Investment eligibility

Two-tier Nordnet-investability rule (§III.12): default-tradable for standard
listed equities/mainstream ETFs; explicit periodic manual verification
required for mini futures/certificates/warrants, specific bonds, specific
fund share classes.

## VII.10 User-configurable settings (existing `CONFIG` surface)

`project_name`, `data_dir`/`cache_dir`/`solver_dir`/`signal_dir`/
`operator_dir`, `data_file`/`data_format`, `asset_cols`/`rf_col`,
`window_mode`/`est_window`/`start` (all require Part X Phase 0 recalibration
for daily data), `gamma` (risk aversion), `epo_w` (shrinkage intensity,
default 0.75), `lower`/`upper` (default weight bounds), `apply_leverage`,
`min_lev`/`max_lev`, `engine_version`/`registry_version` (bump discipline —
the rolling-loop cache is keyed by a hash that covers `CONFIG` loop-fields
and the `REGISTRY`, but **not** solver source code; changing solver math
without bumping `engine_version` silently reloads a stale cached result —
this is a standing operational hazard, not a one-time note).

---

# Part VIII — Backtesting Framework

## VIII.1 Daily workflow

Per period `t`: define the estimation window `[t−est_window, t−1]`; compute
base moments (`Σ` via §VI, with the estimation window's return panel);
for each `REGISTRY` row, compute the signal (`μ`, §V.2) over the same
window, apply that row's `params$ops` risk-operator pipeline, run the
solver (§V.5), apply the overlay (constraints, leverage, regime, §V.6–V.11),
and realize the period-`t` return using period-`t`'s actual return vector.
This loop structure (`build_outputs()` in `core/engine.R`) is already
implemented; Part X Phase 0 requires recalibrating its window-length
parameters for daily rather than monthly data before results are
trustworthy.

## VIII.2 Data alignment

Dates must be `Date` objects, not character strings (a currently-open gap —
`core/engine.R` treats dates as `character`, which breaks calendar joins and
is explicitly called out as needing fixing before daily data can be handled
correctly). The `.active_set` mechanism (§III.6) handles ragged/incomplete
history within the window.

## VIII.3 Signal generation

§V.1–V.3 — executed per period, over the trailing estimation window only
(no look-ahead).

## VIII.4 Portfolio formation

§V.4–V.11 — executed per period, producing the period's target weights.

## VIII.5 Execution assumptions

**`[OPEN, design gap]`** the core engine loop currently computes weights and
realizes returns without an explicit per-period transaction-cost deduction
inside the loop itself — cost is applied as a post-hoc L6 adjustment
(§IV.18) rather than inside `build_outputs()`. This is a design choice
worth stating explicitly rather than leaving implicit: it keeps the gross
return computation clean and simple, at the cost of requiring turnover to be
tracked separately and cost applied afterward, consistently, for every
strategy.

## VIII.6 Transaction cost model

§IV.18, §VII.5 — Nordnet Mini tiers, FX spread, slippage.

## VIII.7 FX handling

§IV.17 — applied once, at L0, before the backtest loop begins; the loop
itself never handles multi-currency returns.

## VIII.8 Performance reporting

§IX.1 — gross and net, always, for every strategy.

## VIII.9 Benchmark comparison

Ødegaard's OSE aggregates (EW/VW/OSEAX/OBX, §II.13) for the OSE leg;
standard S&P 500/Nasdaq benchmark data for the US leg.

## VIII.10 Risk reporting

§IX.7 — realized-vs-modeled vol/correlation, regime-state, drawdown vs.
leverage/constraint limits.

## VIII.11 Validation procedures

The project already has one directly relevant, completed validation:
`STATUS.md` records a numerical-identity check between the plugin-operator
pipeline (`shrink_corr` → `anchor_blend` → `epo` solver) and a predecessor
monolithic anchored-EPO implementation, run on a seeded 30-asset/60-month
panel, matching to residual levels attributable only to a `1e-10` numerical
ridge term (max relative difference ≤ ~2.75e-8 across shrinkage intensities
`w∈{0,0.1,0.5,0.75,0.99,1}`). This standard — reimplement independently,
compare on a seeded synthetic panel, quantify the residual — is the
project's own precedent for validating any new component (a new solver, a
new risk operator) before it is trusted in the main backtest loop, and
should be applied to each new module specified in this document as it is
built.

---

# Part IX — Reporting Framework

## IX.1 Performance tables

Gross and net (mandatory, every strategy): CAGR, Sharpe, Sortino, Information
Ratio, Appraisal Ratio (once the factor-alpha regression module exists,
§IV.19), maximum drawdown, turnover.

## IX.2 Holdings

Current period weights per strategy, per security, with sector/currency/
asset-class tags (§III.10) for breakdown views.

## IX.3 Attribution

Factor-alpha regressions (Newey-West standard errors) against the OSE/US
factor set (§II.14), producing the Appraisal Ratio and factor-exposure
breakdown (§IX.11).

## IX.4 Risk reports

Realized-vs-modeled volatility and correlation; regime-state summary;
leverage/constraint-limit proximity.

## IX.5 Charts

Equity curves (gross vs. net, small multiples across the solver menu — a
direct test for "backtest vanity metrics," per the system's founding
philosophy, §I.2); a cost-rate sensitivity sweep (0–50bps assumed cost,
per strategy) showing whether a strategy's apparent edge survives realistic
costs.

## IX.6 Efficient Frontier

Visualization of §IV.13's closed-form frontier for the current period's
`μ`/`Σ`, with the currently-selected strategies' realized points marked
against it.

## IX.7 Capital Allocation Line

Visualization of §IV.14's CAL (including the kink under unequal borrowing/
lending rates), with the actual leverage ratio `l_t` and financing cost
marked.

## IX.8 Correlation heatmaps

Visualization of `Ω_t` (or `R_t` from the fast DCC output, §VI.2) —
mechanically simple given `Σ_t`/`Ω_t` are already computed each period; not
yet built but a low-effort addition once the risk model (Part VI) is in
place.

## IX.9 Drawdowns

Maximum drawdown (§IV.19) and a drawdown time series (underwater curve) per
strategy.

## IX.10 Rolling performance

Rolling Sharpe/volatility over a fixed trailing window, to visualize
regime-sensitivity of realized performance.

## IX.11 Factor exposures

`β` vector from the §IX.3 factor regression, reported per strategy.

## IX.12 Transaction-cost analysis

The §IX.5 cost-sensitivity sweep, plus a breakdown of cost sources
(commission vs. FX spread vs. slippage) once the full cost model (§VII.5)
is implemented.

## IX.13 Turnover

Per-strategy turnover time series (§IV.18), to diagnose which regimes or
solvers drive cost.

## IX.14 Portfolio diagnostics

Leverage ratio over time, regime-state flags over time, active-set size
(`N_t`) over time (diagnosing how much of the ragged-history universe is
actually usable at any given point).

---

# Part X — Implementation Roadmap

Phases are ordered to minimize rework: each phase either unblocks the next
or is independently valuable and safely deferrable. Where two items within
a phase have no dependency on each other, they are noted as parallelizable.

## Phase 0 — Foundation (blocking; nothing downstream is trustworthy until this closes)

**Objectives:** resolve the universe/survivorship question; implement
currency conversion; make the engine internally consistent for daily data;
split the risk-free rate; execute the data scrub.
**Deliverables:**
- Universe/survivorship resolution (§III.5, §XI.1) — run the EODHD
  `historical=1` test against OSEBX/OSEAX; cross-check the Euronext
  semi-annual archive; if unresolved, implement the disclose-and-bound
  fallback.
- NOK currency conversion implemented at L0 (§IV.17) — Norges Bank primary,
  Yahoo Finance fallback.
- Date-type conversion (`character` → `Date`) throughout `core/engine.R`.
- Daily-data recalibration of `CONFIG$est_window`/`start`/`window_mode` —
  these are currently documented as *months* and must be re-derived, not
  reinterpreted, for daily granularity; bump `CONFIG$engine_version`.
- Risk-free-rate split implemented: separate `rf_moments` (NIBOR/EFFR) and
  `financing_rate` (Nordnet margin rate) series, threaded through a
  corrected `apply_overlay()` (§IV.14).
- Scrub list executed per `STATUS.md` §5 (remove predecessor-provenance
  files, replace the regression fixture with a seeded synthetic panel per
  the already-recorded decision).
**Dependencies:** none upstream — this is the entry point.
**Testing:** re-run the `STATUS.md` numerical-identity validation
(§VIII.11) after the daily-data recalibration to confirm the engine still
computes what it computed before, modulo the intended parameter changes.
**Completion criteria:** universe/survivorship status is either resolved or
explicitly bounded and disclosed; all return series entering the engine are
NOK-denominated; `est_window`/`start` are daily-data-appropriate values with
a documented derivation; `apply_overlay()` uses the correct financing rate.

## Phase 1 — Engine completion (no new research required)

**Objectives:** port mechanisms already identified as necessary but not yet
built.
**Deliverables:** `.active_set(M,t)` (§III.6); `scale_to_vol` (§IV.20); an
L5 out-of-sample parameter-selection mechanism (starting with the EPO
shrinkage intensity `w`, per the project's existing plan, generalizing later
to a small model-selection problem across `{base-Σ estimator × shrinkage}`
choices per §VI.4's own finding that "better" model quality does not
monotonically imply better OOS performance); an L6 performance-stats module
(§IX.1's metrics).
**Dependencies:** Phase 0.
**Parallelizable:** `.active_set`, `scale_to_vol`, and the performance-stats
module have no dependency on each other and can be built concurrently.
**Testing/validation:** each ported mechanism validated against its
predecessor-project behavior where one exists (per the §VIII.11 standard).
**Completion criteria:** all four deliverables built and unit-verified.

## Phase 2 — Signal layer

**Objectives:** implement sector-relative security scoring; add
time-series momentum.
**Deliverables:** `cs_signal` extended with a `group` argument (§V.2);
`ts_signal` builder (§IV.16, needed for both a potential value signal later
and for §V.13's managed-futures sleeve).
**Dependencies:** Phase 0 (data must be daily and NOK-denominated first);
sector classification data (§II.16, `[OPEN]`) blocks the `group` extension
specifically — if unresolved, the pipeline degrades gracefully to its
pre-existing global behavior rather than blocking the whole phase.
**Testing:** verify the zero-sum property holds within groups (§IV.16);
verify skip-month invariance for any new momentum-family signal, per the
project's existing verification standard for `xsmom`.
**Completion criteria:** sector-relative ranking pipeline operational (or
explicitly degraded-and-documented if sector data remains unresolved).

## Phase 3 — Risk layer

**Objectives:** build the confirmed volatility and correlation models.
**Deliverables:** GJR-GARCH(1,1) with automatic GARCH(1,1) fallback
(§IV.7); range-based estimators (§IV.6); cDCC (§IV.8), composed with the
existing `shrink_corr` operator on the long-run target `Q̄`; DECO large-N
fallback (§IV.8).
**Dependencies:** Phase 0.
**Parallelizable:** volatility and range-based-estimator work can proceed
independently of the correlation work, though cDCC depends on the
volatility layer's output (`D_t`).
**Testing:** OOS Sharpe/IR comparison against the existing static-shrinkage
baseline, at the actual universe size the system runs at — per §VI.4's
explicit finding that model sophistication must be justified empirically,
not assumed.
**Completion criteria:** `Σ_t = D_t R_t D_t` computed per period, routed
correctly (slow/shrunk to the optimizer, fast to the regime layer).

## Phase 4 — Portfolio and backtest completion

**Objectives:** turnover/cost model; factor-alpha attribution; rebalancing
policy selection; constraint-solver migration.
**Deliverables:** full transaction-cost model (§VII.5); Newey-West
factor-alpha regression module (§IX.3), unlocking the Appraisal Ratio;
`rebalance_rule` as a per-strategy `REGISTRY` parameter (§V.18); migration
of `constrOptim`-based solvers to a QP solver (`quadprog`/`osqp`), ahead of
adding sector/factor/turnover constraints (§IV.22).
**Dependencies:** Phase 1 (performance-stats module), Phase 2/3 (a working
signal and risk model to report on).
**Testing:** the cost-sensitivity sweep (§IX.5) run across the full solver
menu, checking specifically for strategies whose apparent edge does not
survive realistic costs.
**Completion criteria:** gross/net reporting, turnover, and factor
attribution operational for every registered strategy; constrained solvers
migrated and re-validated for speed at realistic `N`.

## Phase 5 — Leverage and alternative sleeves

**Objectives:** resolve the leverage-vehicle question per market; build the
first (cheapest) alternative sleeves.
**Deliverables:** US-leg margin-vs-LETF empirical comparison (§V.11);
OSE-leg mini-future mathematics derivation (§IV.15, currently `[OPEN]`) and
subsequent comparison; market-neutral sleeve (near-zero incremental cost,
§V.12); in-house managed-futures/TSMOM sleeve (§V.13), blocked on verifying
futures roll-adjustment data quality; merger-arbitrage (MNA proxy) and
commodity sleeves; `REGISTRY` extension to support the generalized
stacked-strategy type (§V.12).
**Dependencies:** Phase 3 (risk model, for the managed-futures sleeve's
own vol targeting), Phase 4 (cost model, needed to evaluate any leverage/
stacking approach net of realistic costs).
**Parallelizable:** the market-neutral sleeve can be built immediately and
independently of the managed-futures/merger-arb work, since it requires no
new data.
**Testing:** the leverage-vehicle comparison is itself the test (§V.11) —
run head-to-head against a naive benchmark in calm- and stressed-volatility
sub-samples, per the theoretical framework in §IV.14. Each new alternative
sleeve validated for genuine diversification (correlation to the core
sleeve, especially in drawdowns) before being combined via stacking, not
assumed diversifying by label.
**Completion criteria:** at least one leverage vehicle and one alternative
sleeve (market-neutral, the cheapest) fully operational and validated;
managed-futures and merger-arb sleeves either operational or explicitly
blocked-and-documented on their respective open data items.

## Phase 6 — Reporting, risk monitoring, and live-implementation scoping

**Objectives:** complete the reporting suite; formalize risk monitoring;
scope live implementation.
**Deliverables:** the full Part IX reporting suite (efficient frontier and
CAL visualizations, correlation heatmaps, rolling performance, factor
exposure and portfolio diagnostics); a formal risk-monitoring/limit-breach
framework (currently only basic diagnostics are specified, §VI.12); a
stress-testing and scenario-analysis framework (currently entirely
undesigned, §VI.10–VI.11 — this phase is where that design work should
happen, informed by a working risk model rather than speculatively); a
scoped plan for live portfolio implementation (§I.7), which this document
deliberately does not attempt to specify in detail before the backtest
engine itself is daily-consistent and validated.
**Dependencies:** all prior phases.
**Completion criteria:** the system produces every report specified in
Part IX from a single, internally-consistent daily backtest run; a written
plan exists for live implementation, even if live implementation itself is
scheduled beyond this phase.

---

# Part XI — Outstanding Items Register

Every item below follows the same template: description, why unresolved,
required research/testing, external dependencies, priority, recommended
next action. Priority reflects how much downstream work is blocked, not the
order items were raised.

## XI.1 — Point-in-time OSE constituent and delisting data
**Description:** no dataset in this repository currently provides
point-in-time OSEBX/OSEAX index membership or a reliable delisted-name
list.
**Why unresolved:** the two most promising leads (EODHD's `historical=1`
index-membership parameter, and Norgate Data's general survivorship-bias-
free constituent tooling) have not been tested against Oslo Børs
specifically; both are generic capabilities whose OSE-specific coverage is
unconfirmed.
**Required research:** query EODHD's index-membership endpoint for
OSEBX/OSEAX with a trial key; cross-check results against the Euronext
semi-annual (June 1/December 1) index-review archive.
**Required testing:** spot-check the resulting constituent history against
several known historical OSE delistings/mergers by name.
**External dependencies:** EODHD trial/paid access; Euronext's public
document archive (free but labor-intensive to parse).
**Priority:** High (blocking Phase 0).
**Recommended next action:** run the EODHD test this week; do not defer
further design work on the assumption this will resolve itself.

## XI.2 — EODHD Oslo Børs delisted-ticker and point-in-time fundamentals coverage
**Description:** whether EODHD's generic delisted-ticker mechanism and
point-in-time fundamentals (confirmed for US 8-K filings) extend to
Norwegian filers.
**Why unresolved:** not tested against OSE specifically.
**Required research:** direct API query against a known-delisted OSE
ticker.
**External dependencies:** EODHD access.
**Priority:** High (tied to XI.1).
**Recommended next action:** combine with XI.1's test pass.

## XI.3 — OSE options liquidity / implied volatility
**Description:** whether single-name OSE options have sufficient quoted
depth to support a trustworthy implied-volatility surface.
**Why unresolved:** not independently confirmed; presumed thin outside a
handful of large caps based on general market knowledge, not verified data.
**Required research:** direct liquidity/quote-depth check against Euronext
or Millistream's OSE derivatives feed.
**External dependencies:** Euronext Data Shop or Millistream commercial
access.
**Priority:** Low (already deprioritized — GARCH/range-based estimators are
the designed substitute).
**Recommended next action:** none required near-term; revisit only if a
specific need for OSE implied vol arises.

## XI.4 — Nordnet FX conversion spread (valutaspread)
**Description:** Nordnet's actual bid-ask FX spread for NOK/USD conversion
is not published with a specific figure on the pages reviewed.
**Why unresolved:** the relevant page references a "Valutaspread" section
without a numeric rate.
**Required research:** direct inquiry to Nordnet, or account-statement
inspection.
**External dependencies:** Nordnet.
**Priority:** Medium (needed for realistic cross-border cost modeling,
§VII.5).
**Recommended next action:** request the figure directly from Nordnet;
absent that, use a conservative assumed spread and flag it as an assumption
in any cost-sensitivity output.

## XI.5 — Nordnet broker cash-account interest rate
**Description:** only a secondary-source figure (~3.6%) has been obtained,
not Nordnet's own published rate.
**Why unresolved:** not found on Nordnet's own pages this design process.
**Required research:** check Nordnet's own site directly.
**External dependencies:** Nordnet.
**Priority:** Low (diagnostic use only, §II.9).
**Recommended next action:** confirm before using the figure beyond a
footnote.

## XI.6 — Nordnet margin maintenance/LTV terms
**Description:** `CONFIG$max_lev = 1.5` is not documented as derived from
Nordnet's actual maintenance-margin or loan-to-value terms.
**Why unresolved:** not researched this design process.
**Required research:** review Nordnet's margin-lending terms directly.
**External dependencies:** Nordnet.
**Priority:** Medium (affects whether the leverage cap is a real risk limit
or a placeholder).
**Recommended next action:** verify before treating `max_lev` as calibrated
in any live-adjacent use.

## XI.7 — Sector/GICS classification coverage for OSE names
**Description:** no confirmed data source for sector classification with
adequate depth for OSE small/mid-cap names.
**Why unresolved:** not researched this design process; U.S. large-cap
coverage is not in doubt, OSE coverage depth is the open question.
**Required research:** check standard providers' (or a free alternative's)
Nordic small/mid-cap sector-classification coverage.
**External dependencies:** whichever provider is evaluated.
**Priority:** High (blocks the sector-relative security-ranking pipeline,
§V.2, a core deliverable).
**Recommended next action:** prioritize this research ahead of or alongside
Phase 2.

## XI.8 — Mini-future / structured-leverage instrument mathematics
**Description:** the Nordnet-accessible OSE-leg leverage vehicle (mini
futures/certificates) has a financing-level/knock-out-barrier structure
whose payoff and decay mathematics have not been derived (§IV.15).
**Why unresolved:** identified late in this design process, after the
US-leg leveraged-ETF analysis was already built; not yet analyzed.
**Required research:** derive the mini-future payoff and cost structure
from Nordnet's own product documentation.
**Required testing:** validate the derived math against actual quoted
mini-future prices for a known underlying.
**External dependencies:** Nordnet product specifications.
**Priority:** Medium (blocks the OSE leg of the leverage-vehicle comparison
specifically, not the core SAA engine).
**Recommended next action:** complete before Phase 5's OSE-leg leverage
work.

## XI.9 — OBX/Oslo Børs equity-index-futures liquidity
**Description:** liquidity of Oslo Børs index futures, relevant to a
portable-alpha implementation on the Norway leg.
**Why unresolved:** not researched this design process.
**Required research:** direct liquidity check via Euronext/Millistream.
**External dependencies:** Euronext/Millistream.
**Priority:** Low (portable alpha is already a lower-priority, Phase-5
track).
**Recommended next action:** defer until Phase 5's portable-alpha work
begins.

## XI.10 — Norway-specific regime factor (Brent oil)
**Description:** whether a Brent oil price regime should be added to the
bounded macro-factor list (§VI.9), given OSEBX's energy-sector weighting.
**Why unresolved:** flagged as a design option, not decided by the project
owner.
**Required research:** none required to decide — this is a design
preference, not a factual question.
**External dependencies:** none.
**Priority:** Low/Medium (an enhancement, not a blocker).
**Recommended next action:** a decision is needed from the project owner
before Phase 3's regime-layer work incorporates or excludes it.

## XI.11 — ASK-wrapper eligibility and account type confirmation
**Description:** whether US-listed shares are ASK-eligible, and
confirmation of the actual account type in use, affecting the tax-cost
asymmetry between the OSE and US legs (§VII.6).
**Why unresolved:** moderate-confidence general knowledge only; not
verified against current Norwegian tax rules or the specific account.
**Required research:** confirm current ASK eligibility rules; confirm
account type.
**External dependencies:** Norwegian tax authority guidance / Nordnet
account documentation.
**Priority:** Medium (affects rebalancing cost realism, not core mechanics).
**Recommended next action:** confirm before finalizing the rebalancing cost
model in Phase 4.

## XI.12 — Millistream / Infront paid-tier evaluation
**Description:** whether a paid Nordic-specific data subscription
(Millistream, Infront) is worth adopting.
**Why unresolved:** deliberately deprioritized until concrete gaps in the
free-tier (Yahoo/EODHD) data are identified.
**Required research:** identify specific, concrete data gaps first.
**External dependencies:** Millistream/Infront sales process.
**Priority:** Low.
**Recommended next action:** revisit only after Phase 0–3 expose specific,
named data gaps the free tier cannot fill.

## XI.13 — Norges Bank historical USD/NOK coverage depth
**Description:** the exact start date of Norges Bank's USD/NOK series is
not confirmed.
**Why unresolved:** not checked directly against the API this design
process.
**Required research:** direct API query.
**External dependencies:** Norges Bank API (already accessible, free).
**Priority:** Medium (needed before fixing any backtest start date that
depends on FX history).
**Recommended next action:** check as part of Phase 0's currency-conversion
implementation.

## XI.14 — Yahoo Finance FX quote type (mid/bid/blended)
**Description:** whether Yahoo's FX tickers quote a mid, bid, or blended
composite rate is not confirmed.
**Why unresolved:** not checked this design process.
**Required research:** direct comparison against Norges Bank's published
mid-rate on overlapping dates.
**External dependencies:** none beyond both data sources.
**Priority:** Low (Yahoo is a fallback/supplement source only, §II.8).
**Recommended next action:** check as part of Phase 0.

## XI.15 — Futures roll-adjustment data quality
**Description:** whether free-tier futures data (Yahoo/EODHD) is properly
roll-adjusted, or whether naive front-month splicing would introduce
spurious returns at roll dates.
**Why unresolved:** not checked this design process.
**Required research:** compare a continuous futures series against a known
roll-adjustment methodology on a sample contract.
**External dependencies:** Yahoo/EODHD futures data access.
**Priority:** High (directly blocks the in-house managed-futures sleeve,
§V.13, Phase 5).
**Recommended next action:** verify before beginning Phase 5's
managed-futures build.

## XI.16 — Nordnet ETN / investment-trust product availability
**Description:** whether Nordnet offers ETNs or investment-trust structures
as distinct, separately-labeled products.
**Why unresolved:** not confirmed this design process; European retail
platforms often don't use these exact US-style wrapper terms.
**Required research:** direct check of Nordnet's product pages.
**External dependencies:** none.
**Priority:** Low.
**Recommended next action:** confirm only if a specific need for either
wrapper type arises.

## XI.17 — Nordnet API onboarding status
**Description:** Nordnet's `nExt` API exists technically but is not
currently onboarding new customers.
**Why unresolved:** this is a platform policy, confirmed as of this design
process but not necessarily permanent.
**Required research:** none — periodic re-checking is the appropriate
action, not research.
**External dependencies:** Nordnet's own onboarding policy.
**Priority:** Low (a design workaround, §III.12, already exists and does
not depend on this changing).
**Recommended next action:** re-check before any production/live-
implementation build (Phase 6 or later).

## XI.18 — Mutual fund and broader fixed-income data sourcing
**Description:** no specific data provider has been verified for mutual
fund NAV histories or a broader Nordnet-investable bond universe beyond the
risk-free proxies already in `data/`.
**Why unresolved:** not researched this design process.
**Required research:** identify a provider once a specific need for fund/
bond-level (not just risk-free-rate-level) fixed-income data arises.
**External dependencies:** TBD.
**Priority:** Low (not currently a blocking dependency for the core equity
SAA engine).
**Recommended next action:** defer until fixed-income is prioritized beyond
its current risk-free-rate role.

## XI.19 — Stress testing and scenario analysis framework
**Description:** no stress-testing or scenario-analysis methodology has
been designed.
**Why unresolved:** not discussed in this design process at all — recorded
honestly as an absence, not filled in speculatively.
**Required research/design:** a full framework design, informed by a
working risk model (§VI.10–VI.11).
**External dependencies:** none beyond internal design work.
**Priority:** Medium (important for a production investment system, but
correctly sequenced after the core risk model exists, per Phase 6).
**Recommended next action:** scope as part of Phase 6.

## XI.20 — Live portfolio implementation
**Description:** no live-trading component exists or has been scoped in
detail.
**Why unresolved:** deliberately deferred — depends on Phase 0 closing and
the backtest engine reaching a validated, daily-consistent state first.
**Required research/design:** a full live-implementation plan (order
routing, position reconciliation, monitoring) once the backtest engine is
ready.
**External dependencies:** Nordnet's trading interface (manual, given the
API's closed status, §XI.17).
**Priority:** Medium (the eventual goal, but correctly not on the critical
path yet).
**Recommended next action:** scope as part of Phase 6.

---

# Part XII — Developer Task Register

Grouped by subsystem, in implementation order within each group. `∥` marks
tasks that can be developed in parallel with the task(s) immediately
preceding them, given no dependency between them.

## XII.1 Data / L0

1. [ ] Implement NOK currency conversion (Norges Bank primary, Yahoo
   fallback) — §IV.17.
2. [ ] Convert all date handling in `core/engine.R` from `character` to
   `Date`.
3. [ ] Run the Phase 0 universe/survivorship research (EODHD `historical=1`
   test, Euronext archive cross-check) and implement whichever path it
   resolves to, or the disclose-and-bound fallback.
4. [ ] Build the OSE data loader for the six verified Ødegaard files.
5. [ ] ∥ Execute the repository scrub list (`STATUS.md` §5): remove
   predecessor-provenance files, replace the FF49 regression fixture with a
   seeded synthetic panel.
6. [ ] Re-derive `CONFIG$est_window`/`start`/`window_mode` for daily data;
   bump `engine_version`.
7. [ ] Implement `.active_set(M, t)`.
8. [ ] Populate `data/OSE Data/Liquidity/` once a source is identified
   (blocked on XI research).

## XII.2 Risk-free rate / financing

9. [ ] Split `Rf` into `rf_moments` (NIBOR/EFFR) and `financing_rate`
   (Nordnet margin rate) as distinct series.
10. [ ] Correct `apply_overlay()` to subtract `financing_rate`, not
    `rf_moments`, from levered excess return.
11. [ ] ∥ Pull EFFR from FRED into `data/`.
12. [ ] ∥ Add the Norwegian 3M T-bill series as an `Rf` robustness-check
    option (already in `data/`, currently unused).

## XII.3 Signal layer / L1

13. [ ] Extend `cs_signal` with a `group` argument (sector-relative
    scoring).
14. [ ] Source and integrate sector/GICS classification data (blocked on
    XI.7 research).
15. [ ] Build the `ts_signal` builder (time-series momentum).
16. [ ] ∥ Build the value signal (P/E, P/B metrics) — lower priority,
    parked relative to the above.

## XII.4 Risk layer / L2

17. [ ] Implement GJR-GARCH(1,1) with automatic GARCH(1,1) fallback.
18. [ ] ∥ Implement range-based volatility estimators (Yang-Zhang,
    Garman-Klass) from daily OHLC.
19. [ ] Implement cDCC (Aielli-corrected), consuming GARCH output.
20. [ ] Compose cDCC's `Q̄` with the existing `shrink_corr` operator.
21. [ ] Implement the DECO large-N fallback.
22. [ ] Wire per-`REGISTRY`-row `Σ`-treatment selection via `params$ops`
    (no new engine code — a registry-design task).
23. [ ] `[EXPERIMENTAL, gated]` implement the RIE/RMT operator, only once a
    large-N universe is loaded.

## XII.5 Portfolio construction / L3–L4

24. [ ] Port `scale_to_vol`.
25. [ ] Migrate `constrOptim`-based solvers (`crra`, `tangency_con`,
    bounded `min_var`, `true_vol_rp`) to a QP solver (`quadprog`/`osqp`).
26. [ ] ∥ Add sector/factor exposure caps and hard/soft turnover
    constraints, once the QP migration lands.
27. [ ] Implement the regime-conditioned `γ` modulation in
    `apply_overlay()`.
28. [ ] Wire the fast DCC `R_t` correlation-breakdown trigger into the
    regime/rebalancing logic.
29. [ ] Source and integrate the bounded macro-factor set (VIX from
    FRED/CBOE, EPU/TPU from policyuncertainty.com).

## XII.6 Leverage and alternative sleeves / L4

30. [ ] Build the US-leg margin-vs-LETF empirical comparison.
31. [ ] Derive the OSE-leg mini-future/certificate mathematics (blocked on
    XI.8 research).
32. [ ] ∥ Build the market-neutral sleeve (existing `epo` + existing
    signal, long-only constraint removed) — no new data required.
33. [ ] Verify futures roll-adjustment data quality (XI.15) before
    proceeding.
34. [ ] Build the in-house managed-futures/TSMOM sleeve (depends on 15, 24,
    33).
35. [ ] ∥ Build the merger-arbitrage sleeve (MNA ETF proxy).
36. [ ] ∥ Build the commodity sleeve (liquid ETF/futures proxy).
37. [ ] Extend `REGISTRY` to support the generalized stacked-strategy type
    (base + sleeve(s) + `StackSize`/fee/financing parameters).

## XII.7 Costs, turnover, rebalancing / L6

38. [ ] Implement the full transaction-cost model (Nordnet Mini tiers + FX
    spread + slippage).
39. [ ] Implement drift-adjusted turnover calculation.
40. [ ] Expose `rebalance_rule` as a per-strategy `REGISTRY` parameter
    (calendar / threshold / hybrid).
41. [ ] Confirm ASK eligibility and account type (XI.11) before finalizing
    the rebalancing tax-cost model.

## XII.8 Performance, reporting, and validation / L6

42. [ ] Build the L6 performance-stats module (gross/net, Sharpe, Sortino,
    IR, turnover).
43. [ ] Build the Newey-West factor-alpha regression module (unlocks
    Appraisal Ratio).
44. [ ] ∥ Build the cost-sensitivity sweep chart (0–50bps).
45. [ ] ∥ Build efficient-frontier and CAL visualizations.
46. [ ] ∥ Build correlation heatmap visualization.
47. [ ] ∥ Build rolling-performance and drawdown charts.
48. [ ] Re-run the `STATUS.md`-style numerical-identity validation against
    every new component before it is trusted in the main loop.

## XII.9 Future / lower-priority

49. [ ] Design the stress-testing and scenario-analysis framework.
50. [ ] Scope live portfolio implementation.
51. [ ] Re-evaluate Nordnet API onboarding status.
52. [ ] `[PARKED]` global macro, broad alternative risk premia, and
    fixed-income sleeves — no near-term action.
53. [ ] `[PARKED]` APARCH, FIGARCH volatility models — no near-term action.
54. [ ] `[EXPERIMENTAL, blocked]` DCC-/DECO-HEAVY — revisit only if an
    intraday data source is acquired.

---

*End of specification. This document should be updated in place as design
decisions are made, resolved, or revised — following the same tagging
convention used throughout — rather than superseded by a new file, to
preserve a single source of truth.*
