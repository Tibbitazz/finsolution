# S8 lead — Page layout and interaction design for Market, Find Investments and Analysis (developer brief)

**Document status:** DRAFT (S8 lead; interface only; recorded early at the owner's request, 2026-10-25) · **Owner stage:** S8 → G8a/G8 (DR-11), S14 → G14 (report views) · **Basis:**
- owner direction 2026-10-25: implement the UX and the design and layout choices of three areas (Market, Find Investments, Analysis) to the extent they fit the engine. The layout is analysed and rebuilt for the engine, never copied;
- owner decision OB-2 as amended 2026-10-25: a combined interface reference. A workspace product is the reference for the shell (widgets, dashboards, connect-your-own-backend); a consumer research product is the page-level UX inspiration (`../s6/S6_LEAD_DATA_SOURCES_2026-10-08.md` §4.7; DR-11 in `../s4/S4_INPUTS_2026-10-07.md` §8);
- the score-table rules T-1 … T-9, cell contract and null-reason codes (`../s4/S4_SCORING_PEER_METHODS.md` §9);
- ADR-0012 (descriptors), ADR-0017 (analysis-only default), ADR-0019 (unknown ≠ unsupported), ADR-0025 (display ≠ admission), ADR-0026 (§8 evidence rights, §9 traceability, §10 approval); 05 R1–R8;
- RQ-07 (universe: Oslo-listed, US and global equities, ETFs and funds; allocation unit "both"; NOK numéraire), RQ-20 (report), RQ-30 (comparison universes), RQ-34 (evidence packets).

**What this document is not:**
- **Not a visual design or mock-up.** It describes structure, behaviour and content rules. Visual design is S8/S14 work. The UI concept prototype stays outside GitHub.
- **Not a technology choice.** Stack, framework and rendering are open (RQ-10, G8a).
- **Not an admission.** A column, card or filter on screen does not make a descriptor an input to beliefs or portfolio construction (T-2; ADR-0025).
- **Not a copy of any product.** No proprietary text, assets, branding, data, scores or style names are taken. Where a pattern conflicts with the engine's rules, the rule wins and this document says how the pattern changes.

**How to read it:**
- §0 states the idea and the design principles;
- §1–§2 cover the shell and the shared components;
- §3–§5 cover the three areas page by page;
- §6–§7 cover the agent assessment panel and the generated sentences;
- §8–§11 cover data contracts, exclusions, dependencies and the developer's open questions;
- §12 traces each pattern to its rule.

---

## 0. The idea

**Three areas, one purpose.** Market, Find Investments and Analysis are the "look before deciding" half of the engine. They answer three questions in order:

| Area | Question for the user | Process stage (12-stage interface) | Responsible role (S4.2b) |
|---|---|---|---|
| **Market** | What is happening across markets, sectors, factors and rates, and why might it matter? | 1 Market | Macro / Regime (hybrid) |
| **Find Investments** | Which instruments in my declared universe have the characteristics I am looking for? | 2 Research | AC/CMA (hybrid); the security sleeve is reviewed by the host class's AC/CMA (P6) |
| **Analysis** | What exactly is this one instrument, how does it compare, and what does the evidence say about it? | 2 Research | AC/CMA (hybrid) |

The pages show **deterministic evidence first**. Agent interpretations follow in a separate, clearly marked panel that cites that evidence (§6). The pages never recommend: they inform the later stages (beliefs, proposals, review, decision), where decisions are made under mandates.

**Design principles (binding for these three areas):**

| # | Principle | What it means on screen | Rule |
|---|---|---|---|
| UX-1 | **Time and source beside every number** | Every card and table carries an as-of date and a source line; every cell links to its provenance | R8; ADR-0012 §2; cell contract §9.2 |
| UX-2 | **Explain at the point of use** | Every metric has a "what it means" note and a "how it is calculated" link to the descriptor ID, method version and record | ADR-0012; §9.2 |
| UX-3 | **Context before detail** | Each page runs: summary strip → focal visual → lists and tables → drill-down | — |
| UX-4 | **The comparison universe is always stated** | Scores show which universe they rank against, with N, in the header or tooltip | T-3; RQ-30 |
| UX-5 | **No silent blanks** | A missing value shows a plain-language null reason (NR-1 … NR-6) | §9.3 |
| UX-6 | **Evidence and interpretation are separate** | Deterministic panels contain only computed values. Agent text sits in its own panel and cites cells | R8; T-4; ADR-0026 §8 |
| UX-7 | **No recommendation affordances** | No "best", "strongest" or "top pick" banners; no buy/sell labels; never sorted by a score by default | T-1; ADR-0017 |
| UX-8 | **Colour is presentation only** | Red/green may be used for direction. Colour is computed at render time, never stored, never passed to agents, never an analysis input; a non-colour equivalent always exists | T-7 |
| UX-9 | **One artefact, two consumers** | The page renders exactly the artefact versions the agents received; no page-side recomputation | T-8 |
| UX-10 | **Fixed vocabulary** | "Momentum" = the cross-sectional factor; "Trend" = the time-series state; technical indicators keep their own names | T-9 |
| UX-11 | **Honest fallbacks** | When a setting cannot be shown as asked, the view says what it shows instead (e.g. "one day has a single point per index, so the chart shows the last month") | — |
| UX-12 | **One value per metric** | For one instrument, as-of date and method version, a label has exactly one value everywhere on the page. Where two definitions exist (trailing 12 months vs last annual report), they carry different labels | §9.2; T-8 |
| UX-13 | **Reproducible state** | Page state (area, view, tab, instrument, universe, period, as-of, artefact versions) lives in the URL, so a view can be reopened exactly | 04 (reproducibility) |

**Why UX-12 is explicit.** A common failure in consumer research pages is the same label showing different numbers in different tabs, such as a dividend yield of 3% in one tab and 5% in another, or two different one-year returns on the same page. The causes are a different window, an annual-report value against a trailing value, or a price return against a total return. The engine avoids this by construction: every displayed value is a cell of one stored artefact with one definition.

---

## 1. Shell and navigation

**Workspace shell (from the workspace reference, DR-11):**
- **Widgets:** every card on a page is a widget bound to one artefact type (§8). Layouts can be rearranged and saved per user later without changing the data contract.
- **Backend:** the shell talks to the engine's own local backend (connect-your-own-backend; ADR-0014 local user layer). Personal data never go to a hosted service (RQ-40).

**Left navigation rail, grouped as a numbered process.** The page-level reference groups its pages as a short numbered workflow rather than a flat menu. The engine adopts the idea with its own stages:

| Band | Pages (process stage) |
|---|---|
| **1 Prepare** | Profile and Policy Statement (0) |
| **2 Look** | Market (1); Find Investments (2); Analysis (2); Charts (2) |
| **3 Decide** | Beliefs (3); Risk model (4); Proposals (5); Risk review (6); Deliberation (7); CIO decision and report (8); Approval (9) |
| **4 Act and learn** | Implementation (10); Monitoring and learning (11) |
| **Always available** | Evidence and provenance (data and fact snapshots, staleness); Method Library (admission and evaluation status); Decision log (trace keys, ADR-0026 §9) |

- Each band shows its number. A stage that has not run for the current cycle is shown as not started, not hidden.
- This document specifies band 2 only. The other bands follow the process stages and the CIO report layout (RQ-20, candidate S14 template).

**Page frame (identical in all three areas):**

| Zone | Content |
|---|---|
| **Header** | Page title and a one-line subtitle on the same line; page actions on the right (e.g. "Export", "Open in Charts") |
| **First-visit explainer** | A dismissible card: what the page is for and how to read it, in two or three plain sentences. Never shown again once dismissed |
| **Control bar** | Scope (universe or market), period, view switch (segmented control), and an **as-of chip** ("Data as of 23 Oct 2026 · snapshot S-…"). Selecting a past as-of opens the stored artefacts of that date (history mode, for reviewing past decisions) |
| **Main area** | The view's widgets, in a responsive grid: summary strip on top, then a wide focal widget with an optional right-hand side panel, then lists and tables |
| **Footer line per widget** | Coverage and source: e.g. "Closing prices 23 Oct 2026 · 2,310 instruments covered · source: [provider], licence class [x]" |

---

## 2. Shared components

Build these once and use them across all three areas. Each takes a cell or row of an artefact as input and never computes the value it shows.

| ID | Component | Behaviour and content |
|---|---|---|
| C-1 | **Metric card** | Label; value with unit; change with sign and period; as-of date; info icon (UX-2). An optional sparkline from stored point-in-time values |
| C-2 | **Score bar** | Horizontal 0–100 bar with a marker at the universe median (50) and the number printed beside it. Tooltip: descriptor ID, comparison universe and N, method version, as-of. Fill colour optional (T-7) |
| C-3 | **Diverging change bar** | Centred at zero, for returns and changes; the sign and number are always printed (non-colour equivalent) |
| C-4 | **Sparkline** | Stored history only. **Never recomputed from restated data** (§9.2 History) |
| C-5 | **Segmented control, tabs, chips** | View switches, sub-tabs and comparison chips. The selected state is part of the URL (UX-13) |
| C-6 | **Data table** | Pinned identity column; sortable columns; column chooser with a count badge (add, remove, reorder, resize); a pinned **"median of selection"** row; a per-cell info link; badges in the identity cell (§4.6); virtualised rows for large universes |
| C-7 | **Null-reason chip** | Replaces a missing value with a short plain-language reason (table below); the code is in the tooltip |
| C-8 | **Source line** | Coverage, as-of and source at the foot of every widget (UX-1) |
| C-9 | **Explainer popover** | "What it means" (one or two sentences), "how it is calculated" (link to the record), window label (e.g. "5 years · quarterly", "1 year · daily") |
| C-10 | **Event row** | Date; relative timing ("in 3 days"); session timing ("before the open", "after the close"); type; expected or actual value; after the event, the price reaction |
| C-11 | **Treemap** | Tile size = a stated size measure; tile colour = change (T-7). The legend states both. Clicking a tile drills down one level |
| C-12 | **Histogram** | Distribution of a measure across the universe in fixed bins (e.g. ≤ −5%, −5 to −3%, …, ≥ +5%), with counts per bin and a summary ("1,104 rose · 1,021 fell") |
| C-13 | **Scatter (bubble) chart** | Selectable X, Y and size measures; preset axis pairs; neutral descriptive quadrant labels; a truncation note when only the largest names are drawn |
| C-14 | **Agent assessment card** | §6 |
| C-15 | **Eligibility badge (three states)** | Eligible / Not eligible / **Unknown**. Unknown is never shown as not eligible (ADR-0019 item 5). Tooltip: the registry fact and version, and the instrument attribute it depends on |
| C-16 | **Status badge** | REFERENCE, CANDIDATE, VARIANT, AGGREGATION, DRILL-DOWN, CONTEXT, DEFERRED (§9.1), and for factor timing "static / shadow" |

**Null reasons in plain language (C-7; codes from §9.3):**

| Code | Short text on screen | Tooltip example |
|---|---|---|
| NR-1 | Not reported | "The company has not reported EBIT for the period" |
| NR-2 | Not meaningful for this type | "EV-based measures are not computed for banks and insurers" |
| NR-3 | Not meaningful (sign) | "P/E is not meaningful when earnings are negative" |
| NR-4 | Too little history | "Needs 12 months of prices; 7 available" |
| NR-5 | Data too old | "Last filing older than the staleness limit" |
| NR-6 | Comparison group too small | "Sector group has 6 members; minimum is 10" |

---

## 3. Market

**Purpose:** a fast, honest picture of markets over a chosen period, with what moved and what is scheduled. It is stage 1 of the process. The Macro / Regime role's assessment appears in its own panel (§6).

**Control bar:**
- **Market scope:** the markets in the declared universe (RQ-07): Oslo, United States, global developed, and "All". A secondary toggle switches between **"home market"** and **"home market in the world"** (the home market against the main world regions).
- **Period:** 1 day, 1 week, 1 month, 3 months, year to date, 1 year, 3 years, 5 years.
- **Currency:** **local or NOK** (the numéraire matters for comparisons; RQ-07). The selected basis appears on every return.
- **View switch:** Overview · Movements · Chart · Map · Funds and ETFs.

### 3.1 Summary strip (top of every Market view)

| Element | Content |
|---|---|
| **One-sentence summary** | A generated sentence from a fixed template catalogue (§7), e.g. "Markets moved in different directions; of the factor portfolios, quality did best." No language model |
| **Three compact cards side by side** | **Markets:** one row per exchange or region with a C-3 bar and %. **Sectors:** the two strongest and two weakest. **Factor portfolios:** the engine's own factor portfolios (cyclical value, enhanced value, momentum, quality and the multifactor portfolio, labelled "static weights") over the period |
| **Breadth** | Advancers and decliners as counts and a stacked bar; unchanged shown separately |
| **As-of** | "Figures as of [date, time, time zone]" |

**Why factor portfolios replace "styles".** Consumer products often group stocks into named style buckets with marketing names and report their average daily return. The engine shows **its own factor portfolios instead**: the Renshaw constructions (`../s4/S4_SCORING_RENSHAW_ANG.md`) on its own universe, with neutral names. Each one is a defined portfolio with a method version, so its return is well defined. Any region labels in factor space (e.g. "high quality and cheap") would be labelled aggregation variants with neutral names (T-1; RQ-32), never marketing labels.

### 3.2 Overview view

Layout: a two-column body under the summary strip.

**Left (wide): map widget**
- World or regions toggle. Countries coloured by the return of their main index over the period, in the selected currency basis.
- Clicking a country filters the movers panel. A note states how the colour is calculated ("main index total return, NOK basis").

**Right: "What moved" panel**
- **Tabs:** Instruments · Sectors · Countries · Factor portfolios · Indices · Funds and ETFs, plus an "All at once" summary mode.
- **Sub-tabs:** Gainers · Decliners · Most traded.
- **Each row:** name, identifier chip, change (C-3), value traded in NOK.
- **For groups:** the group's member count and its average or median change, with the statistic named ("Average change of the stocks in the group").

**Below: calendar widget**
- **Filters:** All · Reports · Dividends · Macro · Announcements; Week or Month.
- **Day strip:** dots on days with events.
- **Event list:** C-10 rows.
- **Footer:** "Open the full calendar"; a source line per event type.
- **In the engine:** the same event calendar is evidence for the Trader role's event checks (ADR-0026 §5 item 3) and for monitoring (stage 11). It is one artefact used in three places.

**Below: rates and inflation widget**
- **Per country:** the policy rate and the latest inflation figure.
- **Comparison sentence:** a generated plain-language sentence comparing the two (§7), e.g. "The policy rate is 0.6 points above inflation".
- **Long chart:** both series over a long history (e.g. since 2016), with markers at past rate decisions; the next decision date.
- **Source line:** official sources only (e.g. Norges Bank, Statistics Norway, the Federal Reserve, BLS, the ECB; S6 lead).

### 3.3 Movements view

| Widget | Content |
|---|---|
| **Index cards** | Level, change and a one-line generated meaning ("Oslo rose 0.7%"), one card per main index |
| **Coverage line** | "Closing prices 23 Oct 2026 · N instruments covered · source …" |
| **Breadth statistics** | Share of instruments that rose; share in a **positive long-term trend state** (SIG-2, 12–1); share in a positive short-term trend state; share trading more than usual (relative volume > 1). Labels follow T-9: these are trend states, not momentum scores |
| **Return distribution** | C-12 histogram of period returns across the universe |
| **Three tables** | Gainers · Decliners · Most active. Columns: instrument, price, change %, value traded (NOK), relative volume (× normal, with the normal window stated) |
| **Indices list** | Every index in scope with its change; a link to compare them in Charts |

### 3.4 Chart view

- Rebased multi-series line chart: all series start at 0% on the first date. Series are the main indices and, optionally, the engine's factor portfolios.
- Controls: series chips (with a count badge), a linear/log toggle, and the date range shown under the chart.
- **Honest fallback (UX-11):** for "1 day" the chart shows the last month and says why.

### 3.5 Map view

- C-11 treemap of the universe by sector. Size = market value; colour = period change. Clicking a sector shows its instruments.
- A legend sentence states the sizing and colouring.
- A right-hand side panel lists sectors with member count and average change.
- A selector switches the grouping (sector, country, factor quintile).

### 3.6 Funds and ETFs view

| Widget | Content |
|---|---|
| **Summary sentence** | Generated (§7), e.g. "Equity index funds rose most; bond funds were flat" |
| **Treemap by fund category** | Size = fund assets if available. **If fund size is missing, the tiles are equal and the view says so** (UX-11). A category with missing data is grey and labelled |
| **Category list** | Per category: number of funds, median ongoing charge, median period return |
| **Gainers and decliners** | Funds and ETFs, with category and cost |
| **Coverage note** | e.g. "N funds and ETFs; leveraged and inverse products excluded" |

**Consistency rule:** a count shown here (e.g. the number of funds) must equal the count in Find Investments for the same as-of date (UX-12). Both come from one universe artefact.

### 3.7 Engine-specific widgets on the Market page

- **Factor portfolio panel:**
  - period returns of the five factor portfolios with their method version;
  - weights labelled **"static base weights (1/3 momentum, 1/3 quality, 1/6 enhanced value, 1/6 cyclical value)"**;
  - the timing models' would-be weights, shown only with a **"shadow mode: not used in decisions"** badge (REN-D5).
- **Market-state panel:** deterministic market-state descriptors (dispersion, correlation, volatility). A market-similarity reading appears only in shadow mode, with the same badge.
- **Regime assessment:** the Macro / Regime role's assessment card (§6), below the deterministic panels and visually separate.

---

## 4. Find Investments

**Purpose:** screen the declared universe and compare instruments on the engine's own descriptors. The page is a view of the **Score Table artefact** (T-8): one deterministic artefact per (universe, as-of date, method versions). The page sorts, filters and renders it; it never computes a score.

### 4.1 Asset tabs

- **Shares**: single stocks in the universe (Oslo, US, global);
- **Funds and ETFs**: own columns and cost logic (§4.10);
- **All instruments**: the common columns only;
- **Holdings look-through**: choose a share and see which funds in the universe hold it, and how much.

### 4.2 Toolbar

- **Search:** a field selector (name, ticker, ISIN, sector).
- **Filters:** a button with a count badge (§4.7).
- **Columns:** a button with a count badge (C-6).
- **View switch:** Table · Cards · Scatter.
- **Saved setups:** a named combination of filters, columns and sort, stored per user in the local layer.

### 4.3 Preset screens

A row of chips, each with a **live count** of matching instruments. A preset is a **versioned filter definition**, not a recommendation, and has a neutral descriptive name. Hovering shows the exact rule. Examples:

| Preset (neutral name) | Rule (illustrative; definitions are versioned) |
|---|---|
| High quality, below-median price | Quality ≥ 70th percentile and cyclical value ≥ 50th |
| Profitable in each of the last 10 years | Years with positive net income = 10 (NR-4 if fewer years exist) |
| Dividend paid in each of the last 10 years | Years paying a dividend = 10 |
| Positive trend state | SIG-2 state = up (12–1 for stocks) |
| Low volatility | 1-year volatility in the lowest third of the universe |
| ASK-eligible | Registry eligibility = eligible (`no.wrapper.ask.eligible_holdings@2`: listed shares of EEA-domiciled companies; EEA-domiciled funds with > 80% shares). Unknown is shown as a separate count |

### 4.4 Result summary

- **Matches card:** "Matches 412 of [universe name] · as of [date]".
- **No "strongest overall" card (T-1).** Its place goes to a **selection profile**: the median percentile of the selection on each factor, against the universe median of 50. This tells the user what kind of selection they have built without singling out a winner.
- **Links:**
  - the **overlap panel** (T-5): Spearman correlations among the displayed factor columns for this universe and date;
  - the **disagreement view** (T-6): instruments where two factor columns diverge by more than a declared gap.

### 4.5 Medians strip

- A row of small cards with the **universe or selection median** of key measures: each factor percentile, P/E, dividend yield, 1-year return.
- Clicking a card sorts the table by that measure. The hint "tap a measure to sort by it" is shown once.
- Last card: **composition** by exchange or country (e.g. "NO 310 · US 1,650 · other 350") as a stacked bar.

### 4.6 Results table (default view)

**Identity cell:**
- ticker and name;
- an exchange chip;
- badges: ASK eligibility (C-15, three states), "no KID" for funds and ETFs without a Norwegian KID (PRIIPs, CB-09), and data flags (stale, partial).

**Default columns:**

| Group | Column | Cell |
|---|---|---|
| Factors | Cyclical value · Enhanced value · Quality · Momentum (Renshaw factors) | C-2 score bars, 0–100 against the stated universe |
| Trend | Trend state (SIG-2) | Up / down chip or a null reason; **not** a 0–100 score (T-9) |
| Aggregation (optional, off by default) | Multifactor (Renshaw) | C-2 bar. The header reads "Multifactor · weights 1/3 M, 1/3 Q, 1/6 EV, 1/6 CV · static". Never the first column, never the default sort (T-1) |
| Fundamentals | Return on equity; P/E (trailing 12 months) | Raw value with unit and a mini-bar against the universe |
| Size and liquidity | Market value (NOK) with sparkline; value traded | Raw values |
| Return | Total return 1 year (NOK or local, as selected) | % with sign |

**Table behaviour:**
- **Header:** each score column states its universe and N (e.g. "percentile vs declared equity universe, N = 2,310").
- **Pinned row:** "Median of selection" at the top.
- **Default sort:** market value, descending, or alphabetical. **Never a score** (UX-7).
- **Info link per cell:** descriptor ID, as-of, method version, raw inputs with fiscal period and currency, null reason, history sparkline (cell contract §9.2).
- **Drill-down:** expanding a factor cell shows its component signals (e.g. momentum: price, idiosyncratic, economic-profit momentum, short interest, hedge-fund holdings; analyst revisions shown as NR-1 until a source exists, REN-D6). The Sørensen 12–1 return and rank appear here as the standalone SIG-1 signal, never as a second headline momentum column.
- **Candidate descriptors** (e.g. Greenblatt-type return on capital, F-score) can be added through the column chooser and carry their status badge (C-16; T-2).

### 4.7 Filter panel

A side sheet with "Add filter", a list of active filters, "Reset" and "Close". Filters are grouped:

| Group | Examples |
|---|---|
| Descriptive | Exchange; country of listing; **country of domicile** (ASK); sector and industry; currency; size class; ASK eligibility; KID available |
| Fundamentals | Margins, returns on capital, growth over 1, 3, 5 and 10 years, balance-sheet ratios, cash conversion; years of profit, dividends and revenue growth |
| Valuation | P/E, P/B, P/S, EV/EBIT, FCF yield, shareholder yield; against own history and against the sector median |
| Price and risk | Returns over standard windows; volatility; drawdown; beta (benchmark named); trend state; relative volume |
| Factor scores | The four Renshaw factors and their component signals; candidate descriptors with status badges |
| Data quality | **Staleness state; last updated; null reasons present; coverage of components.** This lets the user exclude instruments whose evidence is thin |

- Each filter shows its definition, unit and window.
- A range filter shows the universe distribution (a small histogram) behind its slider.

### 4.8 Cards view

One card per instrument:
- identity and badges;
- the four factor bars and the trend state;
- three key facts (market value, P/E, 1-year return);
- a link to Analysis.

This view suits a short list.

### 4.9 Scatter view

- **Preset axis pairs:** quality against cyclical value; momentum against cyclical value; return on equity against P/E; dividend yield against 1-year return.
- **Free selection:** X, Y and bubble size from any numeric column.
- **Quadrants:** neutral labels such as "higher quality, lower price"; median lines at 50 for percentile axes.
- **Truncation note:** "Showing the 150 largest by market value of 2,310; adjust in settings."
- Clicking a bubble opens Analysis.

### 4.10 Funds and ETFs mode

- **Total-cost selector:** "Total cost at [broker]".
  - **Total cost = ongoing charge (from the KID) + platform fee** (from the facts registry's broker records, with the price-list date).
  - An explanation popover gives both sources and dates.
  - Brokers come from the registry (03 §4 rule 7); none is preferred or selected by default for the user.
- **Presets:** low cost; index funds; ETFs; equity share > 80% (the ASK fund condition).
- **Columns:**
  - type; equity share;
  - ongoing charge, platform fee and total cost;
  - volatility (1 year); total return (1, 3 and 5 years); maximum drawdown (5 years);
  - KID available; ASK eligibility (C-15);
  - **look-through exposures**: factor, sector, country and currency, where holdings data exist.
- **How funds are judged:** by look-through exposure and cost, not by a ranking on past return per unit of risk. A past-performance rank, if shown at all, is a descriptive column labelled as such and is not evidence (ADR-0025).
- **Fund equity share unknown:** ASK eligibility is **Unknown**, never "not eligible", and the tooltip says what is missing.

### 4.11 How agents use this page

- The Score Table rows the user sees are the rows the agents receive in their evidence packets (RQ-34).
- **Review panel:** a collapsible panel lists the security-sleeve review notes from the host class's AC/CMA role for instruments in the current selection (P6; §6). Each note links to the cells it cites.
- No agent ever writes into the table.

---

## 5. Analysis (one instrument)

**Purpose:** everything about one share, fund or ETF on one page, ranked against stated universes, with the evidence and the agents' cited assessments.

### 5.1 Header

- **Identity:** name; ticker; exchange chip; ISIN.
- **Descriptive tags:**
  - size class, sector and industry, currency;
  - **country of domicile** (ASK relevance), number of employees.
- **Badges:** ASK eligibility (C-15); KID available (funds and ETFs); data flags.
- **Description:** a short company or fund description with its source and date.

### 5.2 KPI row

Four C-1 cards:
1. **Closing price:** with change, date and currency.
2. **Factor summary:** the four factor percentiles as compact bars. Optionally the labelled Multifactor percentile, with "better than X% of [universe], N = …" and its weights and timing state.
3. **Total return over 1 year:** in NOK and local currency.
4. **Market value:** NOK.

Below the row: a link "See over time in Charts".

### 5.3 Tabs

**Shares:** Overview · Scores and ranks · Valuation · Fundamentals · Price and risk · Dividends · Ownership · Evidence and assessments.

**Funds and ETFs:** the Fundamentals tab is replaced by **Holdings and look-through**. A fund has no financial statements of its own, and the page says so.

### 5.4 Overview tab

**Factor cards ("the instrument at a glance")**
- One card per Renshaw factor:
  - the percentile;
  - a generated comparison ("above the universe median");
  - a C-2 bar with the median line;
  - the component signals with their values and units.
- A separate **trend-state card**: up or down, 12–1 for stocks and 12–0 for funds, ETFs and indices (S48-D1), with the underlying return.
- Technical-indicator readings never appear here under the word "momentum" (T-9).

**Price chart**
- Period selector; **compare chips**: the main index, the sector, and the relevant factor portfolio.
- Total return or price return, labelled.

**"Where it stands"**
- **Strongest and weakest factor:** descriptive, e.g. "Strongest: momentum, above 90% of Norway".
- **Matrix:** rows are the four factors plus diagnostics; columns are the comparison universes (whole declared universe, country, sector), each with N.
- **Diagnostics:** F-score (raw 0–9), Altman Z, Beneish M, as CANDIDATE descriptors with badges.
- Each universe is its own descriptor (T-3).

**Upcoming events**
- Report date with session timing; dividend with amount and ex-date; macro events in the instrument's country (rate decision, inflation release).

**Funds that hold it (reverse look-through)**
- Fund, share of the fund in this instrument, fund cost, fund type, the holdings as-of date.
- Share classes are merged into one row, with the range of their costs.
- "Show all N".

**Key metrics grid**
- Customisable tiles, each with a window label ("5 years · quarterly", "1 year · daily") and a "what it means" popover.

**Assessment summary**
- The latest agent assessment card for this instrument (§6), collapsed, with a link to the Evidence and assessments tab.

### 5.5 Scores and ranks tab

- **Score history:** a line per factor over time, from stored point-in-time values (C-4 rule), next to price against the main indices.
- **Rank tables:** per universe (sector, industry, country, whole universe), "no. 9 of 47; median 55".
- **Against its own history:** today against its own average, lowest and highest over the period, and "higher than on 88% of days since [date]".
- **Score stability (engine addition):** how much the percentile moves (e.g. its range and standard deviation over 12 months). A factor score that swings from 10 to 95 within a few years carries less information per reading than a stable one, and the user should see that.

### 5.6 Valuation tab

| Widget | Content |
|---|---|
| **Price against peers over time** | The instrument's multiple (P/E, P/B, P/S, EV/EBITDA, dividend yield) against the median and interquartile band of its sector, country or universe; windows 1, 3, 5 and 10 years and all. The note states that loss years and one-off years are excluded for both the instrument and the group |
| **Generated headline** | e.g. "More expensive than its sector in 1 of the last 4 years; today 14.1 against 10.2" (§7) |
| **Against its own history** | Table: measure, now, 3-, 5- and 10-year averages, difference against the 5-year average in % ("35% more expensive", "in line", "10% cheaper") |
| **What shareholders get back** | Dividends, net buybacks and net debt paydown, each as % of market value over the last 12 months, and their sum. The dividend figure **is the same trailing-12-month yield used everywhere else** (UX-12); an annual-report figure carries its own label |
| **Long-run valuation** | One bar per fiscal year-end and today, with the median of all years as a line; loss years have no bar and say so |

### 5.7 Fundamentals tab (shares)

- Income statement, balance sheet and cash flow, annual and quarterly.
- Each period carries its **filing date** (point-in-time; DR-1), currency and a restatement flag.
- A toggle switches between "as first reported" and "latest restated". Scores always use the point-in-time version.

### 5.8 Price and risk tab

- **Returns with dividends** over 1 week, 1, 3 and 6 months, year to date, 1 year, and 3, 5 and 10 years per year. The note says that multi-year figures are annualised.
- **Price and dividend decomposition:** price return, total return and the dividend contribution, per window.
- **Position in the 52-week range.**
- **Distance to moving averages:** 20, 50, 100 and 200 days.
- **Drawdowns:** current, and the worst over 1, 3 and 5 years.
- **Volatility; beta with the benchmark named.**
- **Technical indicators** (RSI, MACD, ADX, stochastic, moving-average crossovers):
  - shown as display-only descriptors with the conventional reading in neutral words ("above 70 is conventionally read as overbought");
  - never labelled "momentum" or "trend score" (T-9);
  - not inputs unless admitted;
  - there is no standalone technical agent (ADR-0026 §8.7).

### 5.9 Dividends tab

- History, yield, payout ratio, ex-dates and growth.
- **Account context from the registry:** dividends inside ASK are not taxed on payout; US dividends carry withholding layers (W1–W9). The tab shows the applicable facts with their versions and never computes the user's tax here (S13a).

### 5.10 Ownership tab

- Funds holding the instrument (§5.4, full list).
- Where available, public ownership data with source and date.

### 5.11 Evidence and assessments tab

- **Evidence:** the full evidence packet for this instrument as the agents received it: cells, versions, timestamps, staleness, provenance.
- **Assessments:** the agent assessment cards (§6) and their disagreement records.

### 5.12 Fund and ETF analysis

| Element | Content |
|---|---|
| **Identity** | Name, ISIN, type (index fund, active equity, bond, balanced, ETF), domicile, currency, share classes |
| **KPIs** | Latest price (NAV) and date; total cost at the selected broker; 3-year annualised return; volatility |
| **Trend state** | As for indices (12–0) |
| **Cost** | Ongoing charge and platform fee. **Missing cost:** "not stated: see the fund's KID" (NR-1 with the document named) |
| **ASK status** | Three states with the rule text from the registry fact (`@2`): domicile in the EEA and equity share > 80% at the start of the income year. Unknown if the equity share has not been measured |
| **Key figures** | Volatility (1 year), maximum drawdown (5 years), beta and alpha **with the benchmark named** (a beta or alpha without a stated benchmark is not shown) |
| **Holdings and look-through** | Top holdings with weights and the holdings as-of date; look-through exposures by factor, sector, country and currency |
| **Peer comparison** | Against funds of the same type: descriptive only, with the rule stated and a minimum history (e.g. no rank below 3 years) |
| **Sustainability** | Disclosure class if available, else "not stated" |

---

## 6. Agent assessment panel (structured; not a chat)

The three areas contain **no chat box and no free-form generated commentary**. Agent work appears as **assessment cards** produced by the run. They sit in a container that is visually distinct from the deterministic widgets and is labelled "Interpretation".

**Card contents:**

| Field | Content | Rule |
|---|---|---|
| Role and mandate | e.g. "AC/CMA · equities (security sleeve)", "Macro / Regime", "CRO"; mandate version | ADR-0026 §3 |
| Model and run | Model identifier and version, run ID, as-of | R7; DR-9 |
| Thesis | One or two sentences | — |
| Citations | Every number in the text is a link to a cell (descriptor ID, as-of, method version); hovering highlights the cell on the page | R8; RQ-34 ("R8 lint") |
| Challenges | Structured notes against cells, e.g. "P/E not meaningful: loss-making year", "EV distorted by lease liabilities" | T-4 |
| Confidence | A class derived by code (e.g. from the dispersion of candidate estimates), not a free number | RQ-12 |
| Dissent and disagreements | Open disagreements of three kinds: between scores (T-6), between agents, and between an agent and a deterministic signal. Each has a link to its record | S4.17 |
| Status | Draft / reviewed / superseded | ADR-0026 §9 |

**Rules:**
- An assessment never contains a number that is not a citation.
- Where no assessment exists for an instrument, the panel says "No assessment in this run". It never generates text to fill the space.
- Agents read the same artefacts the page shows (T-8). They never see colours, layout or sort order (T-7).

---

## 7. Generated sentences (deterministic, from templates)

Plain-language sentences ("Markets moved in different directions"; "The policy rate is 0.6 points above inflation"; "More expensive than its sector in 1 of the last 4 years") are produced by **code from a versioned template catalogue**, not by a language model.

- **Template record:** ID, version, the condition that selects it (e.g. "index returns have mixed signs"), slots filled from named cells, and the wording in each supported language (Norwegian and English).
- **Selection:** deterministic and documented; ties are broken by a fixed order.
- **Storage:** the generated sentence is stored with the artefact, together with its template ID and the cells it used. The sentence is therefore reproducible, translatable and auditable.
- **Words:** neutral and descriptive; never "buy", "sell", "attractive", "best" or "strongest overall" (ADR-0017).

---

## 8. Data contract per widget

| Widget | Artefact (one source) | Producer | Key fields | Null handling | Stage / data |
|---|---|---|---|---|---|
| Summary strip; breadth; histogram; movers | Cross-sectional price snapshot for the universe and period | Deterministic market-data service | Returns (local, NOK), value traded, relative volume, trend state, as-of, coverage | Instruments without a price on the date are excluded and counted | S6 (prices); S9a |
| Factor portfolio panel | Factor portfolio series (Renshaw construction) | Deterministic construction service | Returns, method version, weights, timing state | Not shown until the series exists (prospective; REN-D5) | S9c, S7 |
| Market-state panel | Market-state descriptors | Deterministic service | Dispersion, correlation, volatility; shadow-mode readings | Shadow badge | S9a; REN-D5 |
| Calendar | Event calendar | Deterministic ingest | Event type, date, session timing, values, source | Missing timing shown as "time not announced" | S6 |
| Rates and inflation | Macro series | Deterministic ingest (official sources) | Policy rate, CPI, decision dates, next meeting | Not-yet-published shown as such | S6 |
| Results table; Analysis scores | Score Table artefact | Deterministic scoring service | Cells per §9.2 | NR-1 … NR-6 | S9c (T-8) |
| Eligibility badges | Eligibility result | Deterministic predicate over registry facts and instrument attributes | State, fact ID and version, attribute used | Unknown (ADR-0019 item 5) | S3 registry; S6 attributes |
| Fund costs | Registry broker records + KID cost data | Deterministic | Ongoing charge, platform fee, dates | NR-1 naming the KID | S3 registry; S6 |
| Look-through | Fund holdings | Deterministic ingest | Holdings, weights, as-of | "Holdings not available" | S6 (source undecided) |
| Assessment cards | Agent assessment records | Agent roles under mandate, archived (R7) | §6 fields | "No assessment in this run" | S12; RQ-34 |
| Generated sentences | Template outputs stored with each artefact | Deterministic | Template ID, version, cells used | Template not selected → no sentence | S8 |

---

## 9. What not to build

- No headline total score as the lead column, no "strongest", "best" or "top pick" banner, and no default sort by any score (T-1; ADR-0017).
- No buy/sell/hold labels or icons.
- No colour stored in an artefact, sent to an agent or used in an analysis (T-7).
- No named style buckets with marketing names. Only the engine's factor portfolios, under neutral names.
- No strategy-backtest panels with headline returns. Backtests are evaluation (S7): shown only with costs, net figures, method, period, status and stated limitations, and outside these three areas.
- No chat assistant and no free-form generated commentary (§6).
- No community or social features.
- No number without an as-of date and source; no silent blanks.
- No price alerts that trigger trades. Watch conditions belong to monitoring (stage 11) and to the CIO's invalidation conditions.
- No recomputation of stored history with restated data.
- No second headline momentum score (the Sørensen 12–1 lives in the drill-down) and no "trend" label on a cross-sectional score (T-9).

---

## 10. Dependencies and gaps

What these pages need that the engine does not yet have:
- **Point-in-time fundamentals,** including quarterly data for Oslo (S6); ESEF is annual only.
- **Fund holdings and KID cost data** for look-through, fund ASK eligibility and fund factor exposures (source undecided, S6).
- **Fund assets under management** for treemap sizing (UX-11 fallback until then).
- **A sector and industry classification licence** (S6).
- **Calendar data:** report dates, dividends, macro releases (S6).
- **Announcements and news:** readable sources exist without an API (S6).
- **Analyst revisions** (missing, REN-D6); short interest (Norway: public positions ≥ 0.5% only); hedge-fund holdings (US 13F only).
- **Every runtime layer** (S8–S14): the scoring service, factor portfolios, evidence-packet schema (RQ-34), assessment records, Decision Records, report template (RQ-20).
- **The personal-data policy for hosted components** (RQ-40).

---

## 11. Open questions for the developer (for G8a)

1. **Widget framework:** layout persistence per user and the binding of a widget to an artefact type.
2. **URL state (UX-13):** how artefact versions and the as-of snapshot appear in a shareable link.
3. **Performance:** virtualised tables for several thousand rows; server-side or local filtering of the Score Table.
4. **Accessibility:** a colour-blind-safe palette; non-colour equivalents for every coloured element (T-7); keyboard navigation of tables and charts.
5. **Localisation:** Norwegian and English template catalogues (§7); number and date formats.
6. **Local-first operation** (ADR-0014): which widgets work offline from the local store.
7. **Citation links:** how an assessment's citation resolves to a cell on the page (shared IDs between the evidence packet and the Score Table).

---

## 12. Traceability: pattern → rule

| Pattern in this document | Rule or record |
|---|---|
| Score bars against a stated universe; drill-down to components | T-3; §9.1–§9.2; `../s4/S4_SCORING_RENSHAW_ANG.md` §2–§3 |
| Multifactor shown only as a labelled aggregation; no "strongest" banner; no default score sort | T-1 (P3, 2026-10-25); ADR-0012 §4; ADR-0017 |
| Red/green allowed as presentation only | T-7 (revised by P3, 2026-10-25) |
| "Momentum" vs "Trend"; technical indicators under their own names | T-9 (P2, 2026-10-25); `../s4/S4_MOMENTUM.md` §0 |
| Trend state as a context column, not a score | §9.1 (P1, 2026-10-25); S48-D1 |
| Sørensen 12–1 in the drill-down only | REN-D2; §9.1 (P1) |
| Factor portfolios instead of style buckets | T-1; RQ-32; REN-D1 |
| Timing models shown in shadow only | REN-D5 |
| Null reasons in plain language | §9.3 |
| One artefact for page and agents | T-8; RQ-34 |
| Assessment cards with citations; no chat | R8; T-4; ADR-0026 §8–§9; R7 |
| Security-sleeve review by the host class's AC/CMA | P6 (`../s4/S4_ACCOUNTABILITY.md` §2) |
| Three-state eligibility; unknown ≠ not eligible | ADR-0019 item 5; `no.wrapper.ask.eligible_holdings@2` |
| Total cost at a broker from registry facts | 03 §4; ADR-0019 item 12 (descriptive account comparison) |
| Funds judged by look-through and cost | ADR-0025; R-7b |
| Generated sentences from templates, not a language model | R1; R8; ADR-0017 |
| Point-in-time history, never recomputed | §9.2 (History); DR-1 |
| Process-numbered navigation; CIO report as later stages | 12-stage interface; RQ-20 (candidate S14 template, P7) |
| Workspace shell and widget model | DR-11; OB-2 as amended 2026-10-25 |
