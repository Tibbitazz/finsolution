# S6 lead — data sources, vendors and licences (review of 2026-10-08)

**Document status:** DRAFT (lead for S6; recorded early at the owner's request; extended the same day with Seeking Alpha, S&P Global Market Intelligence and the original sources) · **Owner stage:** S6 → G6 (RQ-08), S8 design (CB-19, DR-7) · **Basis:** owner requests of 2026-10-08:
- review data and key alternatives in the researcher materials;
- review free API sources;
- identify the data vendors behind Simply Wall St, Investwiser and Seeking Alpha;
- assess the Norges Bank open-data API and the S&P Capital IQ products;
- establish where the original data comes from, and whether it is free or paid.

**What this is not:**
- **Not a vendor decision.** Nothing here is adopted, and no account was created or key obtained.
- **Not a source of facts for the registry.** Limits and prices are dated observations and must be re-checked at G6.

**Method and boundaries:**
- Read only public pages, terms, privacy notices, documentation and the public front-end code those sites serve.
- Made a handful of requests to the public endpoints the Investwiser page itself loads.
- No login, no account creation, no private or undocumented access beyond that, no scraping at scale.

**Evidence labels:**
- `VERIFIED-SOURCE`: the provider's own page, with its date.
- `VERIFIED-SECONDARY`: a third-party page.
- `INFERENCE`: reasoned from technical evidence.
- `UNVERIFIED`.

---

## 1. What the researcher materials say about data

| Source | Finding | Label |
|---|---|---|
| ANG v2 (21 Sep 2026) | No vendor is named. Agents "call scripts that fetch data from APIs" (p. 36). The macro agent "first fetches macro and market data" (p. 7). Flows and positioning come "via web search" (Exh. A.1 step 5, p. 38) | `VERIFIED-SOURCE` |
| Q Group lecture (Oct 2026), slides and speaker notes | No vendor is named. Slide 40 ("Where to get started") includes "In-house: no new data or models to buy". Slide 38 lists "Data leakage" as a risk | `VERIFIED-SOURCE` |
| Third-party code (chirindaopensource, v1) | **Runs on synthetic data.** README badge: "Bloomberg \| Apex Data \| FRED". "Live API Integration: … Bloomberg (B-PIPE) or FactSet" is listed only as a future extension. Universe of 18 asset classes keyed by Bloomberg codes: SPTR, RTY, SPVU, SPYG, MXEA, MXEF and 12 US ETFs (SHY, IEF, TLT, LQD, HYG, BWX, PICB, EMB, VNQ, GLD, PDBC, BIL). Web-search allowlist: fred.stlouisfed.org, bis.org | `VERIFIED-REPO` |

**Use of the third-party list:** its 10 input tables are a checklist of the data the ANG pipeline consumes.
1. Monthly macro.
2. Daily Fama–French factors and the risk-free rate.
3. OHLCV prices.
4. Valuation (CAPE, P/E, yields).
5. Technical and sentiment signals.
6. Total-return indices.
7. 60/40 benchmark legs.
8. Survey CMAs.
9. Treasury yields and credit spreads.
10. CPI.

**FactSet:** no free or student API tier was found. API access is a negotiated enterprise contract on top of a workstation licence; university access is academic and non-commercial (`VERIFIED-SECONDARY`).

## 2. Data the framework needs (requirement map)

| ID | Need | Consumers | Notes |
|---|---|---|---|
| D-A | Long asset-class total-return history (daily or monthly) | CMA, covariance, PC methods, S7 deterministic evaluation | Proxies acceptable for research |
| D-B | Macro and regime series: growth, inflation, policy rates, yields, spreads, financial conditions (US, euro area, Norway) | Macro agent, regime (S9a) | — |
| D-C | Valuation inputs: CAPE, earnings yield, equity risk premium | CMA methods (S9b) | — |
| D-D | Factor and benchmark returns | Attribution, controls, S7 | — |
| D-E | NOK numéraire: FX and NOK risk-free and yield curve | All NOK-based computation (RQ-07; D6) | — |
| D-F | Implementation instruments: UCITS ETF and fund prices on European venues; ISIN/FIGI identifiers; KID availability; broker costs | S13, Feasibility Engine; facts registry for costs (03) | Retail PRIIPs rules make US-listed ETFs generally unavailable to Norwegian retail investors (sandbox N2, unverified per instrument) |
| D-G | Security level (Sørensen scores): constituents, total-return prices, P/B, **point-in-time consensus forward P/E** | S9c (`research/s4/S4_SCORING_SORENSEN.md`) | The forward-P/E history is the hard part |
| D-H | Text and news (optional) | Sentiment evidence | Contamination risk (`S4_LIT_LOOKAHEAD_2026-10-07.md`) |

## 3. Candidate sources

Limits and prices were observed on 2026-10-08. "Personal" means the free or entry licence is for personal, non-commercial use.

| Source | Covers | Key | Free limits / price | Licence | Fit |
|---|---|---|---|---|---|
| **Norges Bank Datatorg** | D-E: 24 dataflows incl. EXR (exchange rates), IR (policy rate), SHORT_RATES, GOVT_ZEROCOUPON, GOVT_GENERIC_RATES, GOVT_IRS, SEC, MONEY_MARKET | **None** (test query succeeded 2026-10-08) | No limits stated | Copying allowed "dersom Norges Bank oppgis som kilde"; no changes to content; no links for commercial purposes (*Opphavsrett*, last changed 22 Aug 2020). No NLOD/CC licence named | **FITS** (`VERIFIED-SOURCE`; §4.3) |
| **FRED** | D-B, D-C (incl. Shiller CAPE) | Free key | Rate limit not verified | Agreement by use. Third-party copyrighted series need the owner's permission beyond personal use; FRED cannot grant it | **FITS** for macro (`VERIFIED-SOURCE`, partial read) |
| **SSB PxWebApi 2** | Norwegian CPI and statistics | None | — | CC BY 4.0 per data.norge.no; NLOD per an older review (conflict) | **FITS** (`VERIFIED-SECONDARY`) |
| **ECB Data Portal** | Euro yields, HICP | None (secondary) | — | Not verified | **FITS** (`VERIFIED-SECONDARY`) |
| **Ken French / AQR data libraries** | D-D | None | — | French: terms not located. AQR: terms tab in each file; credit AQR | **FITS** for research (`VERIFIED-SECONDARY`) |
| **Damodaran; Shiller** | D-C | None | — | Damodaran: "You are welcome to download and use this material" | **FITS** (`VERIFIED-SECONDARY`) |
| **SEC EDGAR** | US fundamentals, trailing only | None (contact User-Agent) | ≈10 requests/s | Public | **PARTIAL** (US only; no consensus) |
| **OpenFIGI** | Permanent identifiers (DR-7) | Free key | No daily cap; 25 requests per 6 s with key | Free; may require an institutional email (third-party claim) | **FITS** |
| **Tiingo** | D-A: US history (SPY from 1993, sandbox-verified) | Free key | ≈500 symbols/month, 50 requests/hour (secondary) | Personal | **FITS** for research proxies |
| **EODHD** | Global incl. XETRA, LSE, Oslo; INDX, FOREX, EUFUND virtual exchanges; fundamentals | Key | Free: 20 calls/day, 1 year (sandbox-verified). EOD All World $19.99/month (30+ years); fundamentals $59.99/month; 50% student discount | Free tier personal; commercial use needs the custom "Startups & Enterprise" plan | **Best low-cost candidate for D-F/D-G** (§4.2). Caveat: own disclaimer of non-exchange VWAP pricing (§5 F-6) |
| **FMP** | US EOD, fundamentals | Free key | 250 calls/day | Individual use | PARTIAL |
| **Twelve Data** | US free; XETRA and LSE need Grow ($29/month, EOD) | Free key | 800 credits/day, 8/minute | Basic and Grow: personal, non-commercial, no redistribution | PARTIAL |
| **Alpha Vantage / Finnhub / Massive (Polygon)** | US | Free key | 25/day / ≈60 per minute / 5 per minute with 2 years | Personal | Backups only |
| **Nasdaq Data Link** | Assorted free datasets | Free key | 50,000 calls/day | Per dataset | PARTIAL (old docs site retired 31 Aug 2026) |
| **Stooq** | Free CSV | Unclear (CAPTCHA key claim unverified) | Low daily quota; prices not adjusted | Unclear | Lead only |
| **Yahoo / yfinance** | Global | None | — | Unofficial; the library's notice says personal use | **DOES NOT FIT** a distributed engine |
| **Nordnet External API** | Quotes and trading | — | Closed to new subscribers; from SEK 1,290/month for existing users (FAQ, date unverified) | — | **DOES NOT FIT** now |
| **Euronext NextHistory** | Official Oslo Børs EOD (SFTP, CSV) | Contract | Commercial | Exchange licence | Reference only |
| **Bloomberg / FactSet / LSEG I/B/E/S (university)** | Everything incl. consensus history | Institutional | — | Academic, non-commercial | **Owner-only validation**, never a runtime dependency |
| **Simply Wall St** | Global equities (S&P Capital IQ data) | Business API by contract | Consumer plans | Personal, non-commercial; no reuse or retransmission (§4.1) | **DOES NOT FIT** as a source; reference for manual cross-checks only |
| **Investwiser** | Nordic equities (≈1,400–1,450 stocks) | — | Consumer plans | Personal use (Terms 1.6) | **DOES NOT FIT** as a source; peer reference (§4.2) |
| **Seeking Alpha** (Premium, Alpha Picks, PRO) | US-centred research; quant ratings; model portfolio | No official public API found; a RapidAPI listing exists but its official status is unclear | Premium ≈$299/year; Alpha Picks ≈$499/year (list; frequent promotions); PRO ≈$8,200/year (undated report) — all secondary | "You may not copy or redistribute information provided by Seeking Alpha" | **DOES NOT FIT** as a source; peer reference (§4.4) |
| **S&P Capital IQ Pro** (platform) | ≈109,000 public companies (49,000 with current financials); estimates for 19,200+ companies; ownership; transactions; macro | Enterprise login | No public price. Third-party estimates ≈$12,000–30,000 per user per year; contracts ≈$15,000–215,000 per year | Enterprise contract; academic via university licences | **DOES NOT FIT** a distributed engine; possible owner-only validation if the university licenses it (§4.5) |
| **S&P Capital IQ Financials** (Marketplace dataset) | Standardised and as-reported financials, 180,000+ companies; history from 1985 (significant from 1993); **point-in-time** (filing and delivery dates; Premium Snapshot keeps all changes) | Enterprise feed (Xpressfeed, Snowflake, API, ClariFI) | Price on request; samples behind sign-in | Enterprise | Institutional benchmark for PIT fundamentals (§4.5) |
| **S&P Capital IQ Estimates (+ Estimates Snapshot)** | Consensus, detail, revisions, guidance; **Snapshot = PIT history every 2 h since Aug 2016, with `spEffectiveDate` / `spToDate`** | Enterprise feed; Kensho LLM-ready API / MCP (Claude connector; entitlement likely required, `INFERENCE`) | Price on request | Enterprise | **The only vendor-level PIT consensus source found besides I/B/E/S**; paid (§4.5; F-4) |
| **filings.xbrl.org** (ESEF repository, XBRL International) | **Original filings:** EU/EEA annual reports in Inline XBRL; xBRL-JSON per filing; JSON-API | None (query returned data without login, 2026-10-08) | 958 Norwegian filings indexed; newest Norwegian addition seen 2025-05-21 (FY2024), so coverage lags | Not stated; repository of public filings; interim until ESAP | **Candidate free primary source** for Nordic as-filed fundamentals (§4.6) |
| **Euronext Oslo Børs official market data** | Official prices, NextHistory EOD files | Contract | Fee schedule "Information Services", valid from 1 Jan 2026 | Exchange licence | Reference / reconciliation only |
| **oanor (Oslo Børs API, third party)** | Oslo quotes | Key | Free tier 1,700 calls/month (secondary) | Not verified | Lead only |

## 4. Vendor identification

### 4.1 Simply Wall St → S&P Global Market Intelligence (S&P Capital IQ) · `VERIFIED-SOURCE` (stated by the company)

| Evidence | Quote / content | Where (accessed 2026-10-08) |
|---|---|---|
| Help centre, "Where do you source financial data?" (updated 22 Aug 2024) | "All of our data comes from S&P Global Market Intelligence". It covers fundamentals, management, pricing, past financials and consensus estimates. Industry and market averages are computed by Simply Wall St | support.simplywall.st, article 8908651462543 |
| Help centre, "When is your data and stock prices get updated?" (updated **6 Oct 2026**) | "All our data comes from S&P Global Market Intelligence." Share prices end of day (processing up to 6 h); consensus estimates within 24–48 h; earnings quarterly | article 8881088158991 |
| "Analysis and Financial Data Sources" page | "provided by our partners S&P Global Market Intelligence LLC". Coverage: 10 years of financials; +3 years of consensus; 30 years of market prices (example US source "ICE Market Data", Nasdaq/NYSE); end-of-day prices only. Analysis model public on GitHub (`SimplyWallSt/Company-Analysis-Model`) | simplywall.st/analysis-and-financial-data-sources |
| Terms and Conditions, "Special Conditions in relation to S&P Capital IQ" | "S&P Capital IQ is the major data provider to Simply Wall St … under a license arrangement". End users' use "solely for his/her personal non-commercial use". The subscriber may not "furnish such information … to any person or firm for reuse or retransmission without prior written approval" | simplywall.st/terms-and-conditions |
| Footer | "Financial Data provided by S&P Global Market Intelligence LLC … Copyright © 2026" | all pages |
| Business plans | "API — Gain access to our analysis and insights to build your own models or products" (contact sales) | simplywall.st/business-plans |

**Implications:**
- The data is S&P Capital IQ, enterprise-licensed. Use through Simply Wall St is personal and non-commercial, with no retransmission.
- It is **not usable as an engine source**. The owner may use it to cross-check our own computations by eye.
- Their public methodology on GitHub is a candidate **reading** for S9c and S14, as an example of transparent model documentation. It is not adopted.

### 4.2 Investwiser → EODHD (EOD Historical Data) for prices, symbols, profiles and fundamentals · `INFERENCE`, high confidence

**Facts about the product:**
- InvestWiser AS, org.nr. 828 468 642, Horten.
- Terms 1.7: "Financial data is provided by third-party suppliers for Nordic stocks … updated daily". No supplier is named.
- Privacy policy 2.4 lists "Markedsdataleverandører: Leverandører av kurs-, regnskaps- og selskapsdata for nordiske børser". Section 2.9 logs access "slik markedsdatalisensene krever".
- Front end: Next.js. All data goes through its own backend on Google Cloud Run (`backend-main-…-lz.a.run.app/v3/…`, EU/EØS, Finland), so the vendor is never called from the browser.

**Fingerprints.** Each was checked against EODHD's own documentation or files.

| # | Observation on Investwiser (public data and code) | EODHD convention | Check | Discriminating power |
|---|---|---|---|---|
| F-1 | UI translation key `v3.stockScreening.nullTooltip.unavailableEohd` → "Ikke tilgjengelig fra datakilden". It is attached to sector and industry fields sourced from `master_profile` | "EOHD" is a transposition of EODHD | — | **Very high** (names the vendor) |
| F-2 | Index codes `OSEBX.INDX`, `OBX.INDX`; code tests `t.endsWith(".INDX")` | Exchange code **INDX** for indices (e.g. `GSPC.INDX`, `DJI.INDX`) | EODHD EOD-API docs; EODHD forum (S&P 500 = `GSPC.INDX`) | High (Yahoo uses `^…`) |
| F-3 | FX codes `NOKUSD.FOREX`, `SEKUSD.FOREX`, `DKKUSD.FOREX`, `EURUSD.FOREX` | Exchange code **FOREX** for currency pairs | EODHD docs; eodhd.com page "NOKUSD.FOREX" exists | High (Yahoo uses `=X`) |
| F-4 | Fund exchange code `EUFUND` (fund tab, example `OBXD.OL`) | **EUFUND** virtual exchange (`ISIN.EUFUND`, ≈69,000 tickers; All World Extended) | eodhd.com/exchange/EUFUND | **Very high** (an EODHD-specific construct) |
| F-5 | `logo_url` values `/img/logos/CO/NOVO-B.png` and `/img/logos/ST/ELEC.png` (the latter for ELON.ST, the company's old ticker). **The paths return 404 on investwiser.no** | Relative logo path; files exist at eodhd.com/img/logos/CO/NOVO-B.png (13,184 bytes) and …/ST/ELEC.png (10,615 bytes) | Fetched 2026-10-08 | High: an unresolved pass-through of a vendor field, including the vendor's stale ticker |
| F-6 | Exchange codes OL / ST / HE / CO; secondary-listing codes such as `NDA-FI.HE`, `SAMPO-DKK.CO` | EODHD exchange codes | — | Medium (overlaps with Yahoo) |
| F-7 | Sector and industry strings in the Morningstar/Yahoo style (e.g. "Consumer Cyclical", " Software - Application" with a stray leading space) | EODHD `General.Sector` / `Industry` use these strings | — | Low (shared by several vendors) |
| F-8 | Nightly batch: `generated_at` 2026-10-08 01:45, `data_as_of` 2026-10-06 | EOD vendor | — | Low |

**Other sources the site states:**
- earnings-call transcripts "Quartr" (`VERIFIED-SOURCE`, UI text);
- exchange announcements "Oslo Børs og Nasdaq, med lenke til originalen";
- report dates, dividends and macro: "børsdata samlet av InvestWiser";
- AI: Anthropic Claude (Terms 1.7).

**Strongest alternative, rejected:** the backend could translate another vendor's symbols into EODHD format. That is implausible because F-1 (the vendor named in a key), F-4 (an EODHD-only construct) and F-5 (byte paths into EODHD's file store, including a stale ticker) would all need to be imitated.

**Not determined:**
- whether EODHD is the **only** price supplier (the policy says "leverandører", plural; a logged-in "Sanntid" watchlist may use another feed);
- the licence tier Investwiser holds (commercial use requires EODHD's custom plan).

**Implications:**
- A Norwegian commercial product evidently covers ≈1,400–1,450 Nordic stocks and fund series from EODHD. This is **practical evidence of EODHD's Nordic coverage**; S6 still measures it independently.
- Investwiser computes quality/value/momentum percentile ranks (`qvm_pct`, `quality_pct`, `value_pct`, `momentum_pct`, plus "Magic Formula" and "O'Shaughnessy" ranks). It back-tests a top-20 equal-weight quarterly portfolio "på data tilbake til 1996".
  - This is a **peer example** for S9c (`S4_SCORING_SORENSEN.md`), not a source.
  - Their back-test history is subject to the point-in-time and survivorship questions in O-5 (`UNVERIFIED` whether they handle them).
- The service is licensed for personal use (Terms 1.6), so it is **not usable as a data source**.

### 4.3 Norges Bank Datatorg · `VERIFIED-SOURCE`
- **Portal:** norges-bank.no/tema/statistikk/apne-data. REST API; query tool at app.norges-bank.no/query.
- **Base URL:** `https://data.norges-bank.no/api/data/{FLOW}/{KEY}`. Example key: `EXR/B.USD.NOK.SP` (frequency.base.quote.tenor). Parameters: `format` (`excel-both`, `excel-ts`, `csv`, `csv-ts`), `startPeriod`, `endPeriod`, `locale`.
- **Test 2026-10-08:** `EXR/B.USD+EUR.NOK.SP`, 28 Sep–6 Oct 2026, returned data **without authentication**. Example: USD/NOK 9.5643 and EUR/NOK 10.778 on 6 Oct.
  - The series is the ECB reference rate (14:15 CET concertation), in NOK per unit of base currency.
- **Dataflows (24):** ANN_FX_SPU, ANN_KPRA, ANN_TEST, CBC_CALENDAR, CBC_INSTRUMENTS, CBC_TRANSACTIONS, **EXR**, FAUCTION, FINANCIAL_INDICATORS, **GOVT_GENERIC_RATES**, **GOVT_IRS**, GOVT_KEYFIGURES, GOVT_PRIMARY_MARKET, GOVT_SECONDARY_MARKET, **GOVT_ZEROCOUPON**, **IR**, LENDINGSURVEY, LIQUIDITY_FORECAST, LIQUIDITY_STATISTICS, **MONEY_MARKET**, REGNET, **SEC**, SETTLEMENT_STATISTICS, **SHORT_RATES**.
- **Terms:** copying allowed with Norges Bank as the credited source; no alteration; no commercial-purpose links; no liability for rate, statistics or FX information. No rate limit is published. Contact: data@norges-bank.no.
- **Fit:** the primary candidate for D-E (NOK numéraire; NOK risk-free; Norwegian yield curve). It is also a candidate source for registry facts (03) where an official NOK rate is required.

### 4.4 Seeking Alpha → S&P Global Market Intelligence (fundamentals, estimates) and Quodd (prices) · `VERIFIED-SOURCE` (stated by the company)
The owner's link (an advertising URL) was opened **without its tracking parameters**: seekingalpha.com/alpha-picks/subscribe.

| Evidence | Quote / content | Where (accessed 2026-10-08) |
|---|---|---|
| Help centre, "Where Does Seeking Alpha Source Its Market Data From?" (undated) | **Prices:** "Real-time and delayed quotes … are provided by **Quodd (formerly Xignite)**"; real-time from "**Cboe BZX Exchange** (formerly BATS)"; delayed from the "**Nasdaq UTP delayed feed**". **Fundamentals:** "Fundamentals, estimates, and Wall Street analyst ratings are provided by **S&P Global Market Intelligence**." **Backtests:** "Backtest data and historical ratings performance are powered by **ClariFI**, S&P Global Market Intelligence LLC." Classification: GICS (MSCI and S&P property, licensed). Reuse: "You may not copy or redistribute information provided by Seeking Alpha" | help.seekingalpha.com/basic/where-do-you-source-your-market-data-from |
| Alpha Picks "about" page | A **rules-based model portfolio**, two picks a month (around the 1st and 15th) from Quant "Strong Buy" ratings. Buy criteria: Strong Buy for ≥ 75 consecutive days; US common stock; not a REIT; 3-month average market cap > $500M; price > $10; not recommended in the past year. Sell rules: rating falls to Sell/Strong Sell; or Hold for 180 days (winners: sell the initial stake only); M&A target; trim at 15% → 10%. Proceeds equal-weighted; dividends reinvested. Performance: open prices until 30 Jul 2024, VWAP after; time-weighted. "Not an investment product run with real money" and "Nor is it an audited GIPS compliant investment product" | seekingalpha.com/alpha-picks/about |
| Quant performance page | Grades on "value, growth, profitability, EPS Revisions, and price momentum metrics **vs. the peer sector**", "weighted to maximize the predictive value". Performance includes **backtested** results | seekingalpha.com/performance/quant |
| Pricing (secondary) | Premium ≈$299/year; Alpha Picks ≈$499/year list (promotions vary); bundle offers; PRO ≈$8,200/year (undated trade-press report) | financer.com; waterstechnology.com |
| API | No official public data API or enterprise data licence page found. A RapidAPI "Seeking Alpha API" exists; its official status is unclear (`UNVERIFIED`) | rapidapi.com blog |

**Implications:**
- **Not a data source.** Data is licensed from S&P and Quodd with no redistribution.
- Useful as a **peer reference** in two places, neither adopted:
  - its quant grades rank **within sector**, which is variant O-4 for our scoring;
  - Alpha Picks shows fully rule-specified buy, sell and trim rules (S11/S13 inspiration).
- **Referee caution:** grade weights "weighted to maximize the predictive value", combined with backtested performance, carry an in-sample selection risk; the model portfolio is not audited. This is the kind of evidence our S7 protocol is designed to exclude (P13, RQ-37).

### 4.5 S&P Global Market Intelligence (S&P Capital IQ): the upstream licensor behind Simply Wall St and Seeking Alpha · `VERIFIED-SOURCE`

| Product | What it is | Key facts (S&P pages, accessed 2026-10-08) | Access / price |
|---|---|---|---|
| **S&P Capital IQ Pro** | Desktop and web research platform | 109,000+ public companies (49,000 with current financials); 60M+ private companies; 140+ estimate metrics for 19,200+ companies in 110+ countries; Visible Alpha consensus line items; fixed income from Markit; ownership; transactions; macro; AI tools | "Request Access" / "Request a Demo"; no public price. Third-party estimates ≈$12,000–30,000 per user per year (CostBench) and contracts ≈$15,000–215,000 per year (Vendr via CostBench) — `VERIFIED-SECONDARY`. "Academia" is a listed customer segment |
| **S&P Capital IQ Financials** (Marketplace dataset, enhanced 2026-09-23) | Standardised and as-reported statements | 180,000+ companies (95,000+ public, active and inactive); 5,000+ items; history from 1985, significant from 1993. **Point in time: Yes ("Filing dates and product delivery date PIT")**. "Premium Financials Snapshot … with point-in-time observations, providing all changes to data items and their associated dates". Data source: "Publicly available documents, company filings, annual reports, press releases". Delivery: API, Snowflake, Xpressfeed, ClariFI, Databricks, FTP, Capital IQ Pro | "Request More Information" / "Try out this dataset"; sample data and dictionary behind sign-in. Its related price dataset on the Marketplace is supplied by **EDI** (a third-party vendor) |
| **S&P Capital IQ Estimates** | Consensus, detail, surprises, revisions, guidance, industry KPIs | **Estimates Snapshot: "Point-in-time history without look-ahead bias"; "Snapshot every 2 hours"; "all updates … since August 2016"; columns `spEffectiveDate` and `spToDate`.** Consensus uses majority-basis estimates only. Delivery: Capital IQ Pro, Xpressfeed, APIs, Excel, Snowflake/Databricks, and "Kensho's LLM-ready API, powered by the Model Context Protocol (MCP), including integrations with Claude" | "Request Demo"; package pricing (Global / International / North American) not public |
| **Kensho LLM-ready API / MCP** | AI access to S&P data | Covers Capital IQ Financials, Market Data, Earnings Call Transcripts and more; an S&P Global connector for Claude exists | Entitlement through an S&P contract appears required (`INFERENCE`) |
| **Academic route** | University licences | Capital IQ Pro via university licences at no direct cost to students (secondary). Compustat-Capital IQ via **WRDS** at many universities (academic, non-commercial). Whether the Estimates **Snapshot** is on WRDS: not confirmed | The owner's university must be asked |

**Implications:**
- **Not free.** Everything is enterprise-licensed, and no consumer or personal API exists.
- It is, however, the **institutional reference** for exactly what our framework lacks: point-in-time fundamentals and point-in-time consensus estimates (F-4).
- **Where it can play a role:**
  - **validation:** owner-only, academic licence; e.g. reproducing Sørensen V0 and auditing the look-ahead behaviour of free sources;
  - **later commercial option:** if the engine ever becomes a product (CB-19).
- **Pattern lead (DR-6/S8, not adopted):** the Kensho MCP connector shows a licensed data source exposed to agents through MCP with entitlement checks. It is consistent with R8 (agents consume deterministic, attributed data).

### 4.6 Where the original data comes from (data lineage)

| Data | Original (primary) source | Licensed aggregators seen in this review | Free access to the primary? |
|---|---|---|---|
| Financial statements | Company filings: SEC EDGAR (US); **ESEF Inline-XBRL annual reports** filed with national OAMs (EU/EEA, incl. Norway); press releases | S&P Capital IQ (→ Simply Wall St, Seeking Alpha); EODHD (→ Investwiser) | **Yes, as filed:** EDGAR (US); **filings.xbrl.org** for ESEF (958 Norwegian filings indexed, xBRL-JSON, public API; partial coverage and a lag). Standardisation and point-in-time history are what vendors add |
| Analyst estimates / consensus | Sell-side brokers and analysts (contributors) | S&P Capital IQ Estimates; LSEG I/B/E/S; FactSet; Visible Alpha; Bloomberg BEst | **No.** Contributor data is collected and licensed by vendors only |
| Prices | Exchanges: Cboe BZX and Nasdaq UTP (US); **Euronext Oslo Børs** and other venues (Europe) | Quodd/Xignite (→ Seeking Alpha); ICE (S&P example); EODHD (non-exchange VWAP aggregation); EDI | **No official free history.** Oslo Børs data is licensed (fee schedule valid from 1 Jan 2026). Free vendor tiers are personal-use |
| Company announcements | Oslo Børs **Newsweb** (NewsPoint → OAM, Newsweb and data vendors) | Bloomberg, Refinitiv, SIX (real-time distribution) | **Readable publicly** on newsweb; no official free API found |
| Classification | GICS (MSCI and S&P) | Licensed to platforms | No (licensed) |
| FX and NOK rates | Norges Bank (ECB reference rates for EXR) | — | **Yes** (§4.3) |

## 5. Findings

| # | Finding | Status |
|---|---|---|
| F-1 | No researcher material provides or names a dataset. ANG's data is not public. Vendor selection is ours (S6) | `VERIFIED-SOURCE` |
| F-2 | **Licence, not price, is the binding constraint.** Every free or entry tier reviewed is personal or non-commercial, and the consumer platforms forbid reuse. The compliant architecture for a reusable, multi-user local engine is **per-user credentials and local storage, with no redistribution between users** (DR-7 refinement, §6; CB-19; ADR-0014) | `INFERENCE` from verified terms |
| F-3 | **Research data ≠ implementation data.** D-A can use long US proxy series from free sources. D-F needs European-listed UCITS instruments, which no free tier reliably covers; EODHD (≈$20/month, personal) is the cheapest verified option | Mixed; per-instrument KID availability `UNVERIFIED` |
| F-4 | **Sørensen value score:** point-in-time consensus forward P/E exists only at vendor level: **S&P Capital IQ Estimates Snapshot (PIT since Aug 2016, every 2 h)** and LSEG I/B/E/S (often via WRDS). Both are paid or academic; no free source exists, because the primary data is broker contributions. The options are owner decisions at S6/S9c, not blockers: (a) academic access for validation only; (b) collect consensus snapshots forward from now; (c) a declared trailing-P/E/B variant from **as-filed primary data** (EDGAR for the US; **ESEF via filings.xbrl.org** for Norway and the EU), point-in-time by filing date. The momentum leg needs only prices | `VERIFIED-SOURCE` (S&P pages) and `VERIFIED-SECONDARY` |
| F-5 | Commercial Nordic analytics products are built on EODHD (Investwiser) and S&P Capital IQ (Simply Wall St). Practical coverage evidence; neither is a usable source | §4 |
| F-6 | **EODHD's own disclaimer:** "We are not using exchanges data feeds for the pricing data, we are using OTC, peer to peer trades and trading platforms over 100+ sources … aggregating … via VWAP method". Prices are "indicative and not appropriate for trading purposes". Adjusted close is "recomputed, not stored". So EODHD is **research-grade**; execution prices come from the broker at S13. Adjusted series require snapshotting (S6) | `VERIFIED-SOURCE` (eodhd.com, 2026-10-08) |
| F-7 | Keys never enter the repository, logs or artefacts. The sandbox's EODHD and Tiingo keys remain to be rotated by the owner | Governance |
| F-8 | **Consumer platforms are resellers, not sources.**<br>- Simply Wall St and Seeking Alpha both resell **S&P Capital IQ** (Seeking Alpha adds Quodd for prices and ClariFI for backtests).<br>- Investwiser resells **EODHD**.<br>- All three forbid reuse.<br>The real choice is between (i) licensed aggregators (S&P, LSEG, FactSet, Bloomberg, EODHD) and (ii) primary sources (filings, central banks, exchanges) | `VERIFIED-SOURCE` / `INFERENCE` (§4) |
| F-9 | **A free primary route exists for Nordic fundamentals:** ESEF Inline-XBRL annual reports via filings.xbrl.org. Limits: annual only (quarterly reports are not ESEF), as-filed (no vendor standardisation), partial coverage, indexing lag. It suits trailing value metrics (B/P, E/P) with point-in-time by filing date, after S6 coverage tests. Prices and consensus remain paid | `VERIFIED-SOURCE` (API query) + `INFERENCE` |

## 6. Developer requirement DR-7: refined (interface only; not accepted)

DR-7 (`S4_INPUTS_2026-10-07.md` §8) is refined as follows:
- **Identifiers:** permanent instrument identifiers (ISIN, FIGI) alongside vendor tickers. Vendor symbology (e.g. `.INDX`, `.FOREX`, `.EUFUND`) is mapped, never used as identity.
- **Credentials:** per-user vendor credentials, held only in the local user layer (ADR-0014). Never in the repository, logs, run manifests or exported artefacts.
- **Adapters and licences:** pluggable vendor adapters; a **licence class** per source (personal / research / commercial / public with attribution). The run manifest records which classes were used.
- **Provenance:** a stamp on every datum (vendor, endpoint, retrieved_at, adjusted vs raw).
- **No sharing:** no cross-user sharing of vendor data.

## 7. Candidate stack for S6 (not adopted)

| Tier | Sources | Who supplies it |
|---|---|---|
| Public, no key | Norges Bank, SSB, ECB, Ken French, AQR, Shiller, Damodaran, SEC EDGAR, **filings.xbrl.org (ESEF)** | Engine adapters; attribution displayed |
| Free key (user) | FRED, OpenFIGI, Tiingo (or FMP) | Each user |
| Low-cost subscription (user) | EODHD All World (+ fundamentals if S9c security scoring is enabled) | Each user, optional |
| Academic (owner only) | Bloomberg, FactSet, **S&P Capital IQ / Compustat (WRDS)** or I/B/E/S via the university | Validation and reproduction oracles (e.g. Sørensen V0; PIT audits of free sources); never shipped |
| Enterprise (only if the engine becomes a commercial product) | S&P Capital IQ Financials + Estimates Snapshot; or LSEG / FactSet equivalents | Contract; out of scope for a personal engine (CB-19) |

## 8. Open checks for S6 vendor coverage tests
1. Official pages for Tiingo, FMP, Finnhub and Massive limits.
2. FRED's full licence and rate limit; Ken French's terms.
3. Whether EODHD's personal plan permits per-user use inside a distributed local engine, and whether its fundamentals are point-in-time or restated.
4. EODHD coverage, history depth and adjustment quality for Oslo and the main UCITS venues, against Norges Bank FX and official Oslo closes.
5. Stooq key status.
6. KID availability per candidate instrument (PRIIPs).
7. **filings.xbrl.org for Norway:** coverage of Oslo-listed issuers, indexing lag, IFRS-taxonomy tagging quality, terms of use; the future ESAP replacement.
8. **University licences:** which of Bloomberg, FactSet, Capital IQ Pro, WRDS (Compustat-Capital IQ, I/B/E/S) the owner's university provides, and whether personal research use for validation is permitted.
9. Whether Seeking Alpha's RapidAPI listing is official (relevant only to rule it out).

## Sources (accessed 2026-10-08)
- Simply Wall St:
  - support.simplywall.st/hc/en-us/articles/8908651462543;
  - …/8881088158991;
  - …/8870680668815;
  - simplywall.st/analysis-and-financial-data-sources;
  - simplywall.st/terms-and-conditions;
  - simplywall.st/business-plans.
- Investwiser:
  - investwiser.no/home, /termsofuse, /personvern;
  - its public front-end bundles and public `/v3/` endpoints as loaded by the page;
  - eodhd.com/img/logos/CO/NOVO-B.png, …/ST/ELEC.png.
- EODHD:
  - eodhd.com/financial-apis/api-for-historical-data-and-volumes;
  - eodhd.com/exchange/EUFUND;
  - eodhd.com/financial-summary/NOKUSD.FOREX;
  - forum.eodhd.com (GSPC.INDX);
  - eodhd.com/pricing.
- Norges Bank:
  - norges-bank.no/tema/statistikk/apne-data, …/veiledning-til-norges-banks-datatorg, norges-bank.no/Opphavsrett;
  - data.norges-bank.no/api (test query and dataflow list).
- Seeking Alpha:
  - seekingalpha.com/alpha-picks/subscribe (opened without tracking parameters);
  - seekingalpha.com/alpha-picks/about;
  - seekingalpha.com/performance/quant;
  - help.seekingalpha.com/basic/where-do-you-source-your-market-data-from;
  - about.seekingalpha.com/terms.
- S&P Global:
  - spglobal.com/market-intelligence/en;
  - …/solutions/products/sp-capital-iq-pro;
  - …/solutions/capital-iq-estimates;
  - marketplace.spglobal.com/en/datasets/s-p-capital-iq-financials-(10);
  - kensho.com (LLM-ready API news; docs overview);
  - press.spglobal.com (2025-07-15, S&P Global × Anthropic).
- Original sources:
  - filings.xbrl.org/about and filings.xbrl.org/api/filings (country=NO query);
  - euronext.com Oslo Børs publication service;
  - connect2.euronext.com Oslo Børs price list.
- Secondary: costbench.com (Capital IQ Pro pricing), financer.com (Seeking Alpha pricing), waterstechnology.com (Seeking Alpha PRO), university library pages on WRDS.
- Other providers:
  - fred.stlouisfed.org/docs/api/terms_of_use.html;
  - ssb.no/en/api;
  - data.ecb.europa.eu/help/api/overview;
  - openfigi.com/api/documentation;
  - support.twelvedata.com (articles 5194820, 5735196, 5332349);
  - nordnet.se/externalapi/docs/faq;
  - msci.com/index-terms;
  - aqr.com data library;
  - pages.stern.nyu.edu/~adamodar.
- Secondary pages for Tiingo, FMP, Alpha Vantage, Finnhub, Massive, Nasdaq Data Link and Stooq, as cited in the session of 2026-10-08.
