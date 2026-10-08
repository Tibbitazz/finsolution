# S6 lead — data sources, vendors and licences (review of 2026-10-08)

**Document status:** DRAFT (lead for S6; recorded early at the owner's request) · **Owner stage:** S6 → G6 (RQ-08), S8 design (CB-19, DR-7) · **Basis:** owner requests of 2026-10-08:
- review data and key alternatives in the researcher materials;
- review free API sources;
- identify the data vendors behind Simply Wall St and Investwiser;
- assess the Norges Bank open-data API.

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

## 5. Findings

| # | Finding | Status |
|---|---|---|
| F-1 | No researcher material provides or names a dataset. ANG's data is not public. Vendor selection is ours (S6) | `VERIFIED-SOURCE` |
| F-2 | **Licence, not price, is the binding constraint.** Every free or entry tier reviewed is personal or non-commercial, and the consumer platforms forbid reuse. The compliant architecture for a reusable, multi-user local engine is **per-user credentials and local storage, with no redistribution between users** (DR-7 refinement, §6; CB-19; ADR-0014) | `INFERENCE` from verified terms |
| F-3 | **Research data ≠ implementation data.** D-A can use long US proxy series from free sources. D-F needs European-listed UCITS instruments, which no free tier reliably covers; EODHD (≈$20/month, personal) is the cheapest verified option | Mixed; per-instrument KID availability `UNVERIFIED` |
| F-4 | **Sørensen value score:** point-in-time consensus forward P/E exists only in I/B/E/S-class sources. The options are owner decisions at S6/S9c, not blockers: (a) academic access for validation only; (b) collect consensus snapshots forward from now; (c) a declared trailing-P/E/B variant (EDGAR for the US; EODHD fundamentals for the Nordics, if not restated — `UNVERIFIED`). The momentum leg needs only prices | `VERIFIED-SECONDARY` (no free PIT source found) |
| F-5 | Commercial Nordic analytics products are built on EODHD (Investwiser) and S&P Capital IQ (Simply Wall St). Practical coverage evidence; neither is a usable source | §4 |
| F-6 | **EODHD's own disclaimer:** "We are not using exchanges data feeds for the pricing data, we are using OTC, peer to peer trades and trading platforms over 100+ sources … aggregating … via VWAP method". Prices are "indicative and not appropriate for trading purposes". Adjusted close is "recomputed, not stored". So EODHD is **research-grade**; execution prices come from the broker at S13. Adjusted series require snapshotting (S6) | `VERIFIED-SOURCE` (eodhd.com, 2026-10-08) |
| F-7 | Keys never enter the repository, logs or artefacts. The sandbox's EODHD and Tiingo keys remain to be rotated by the owner | Governance |

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
| Public, no key | Norges Bank, SSB, ECB, Ken French, AQR, Shiller, Damodaran, SEC EDGAR | Engine adapters; attribution displayed |
| Free key (user) | FRED, OpenFIGI, Tiingo (or FMP) | Each user |
| Low-cost subscription (user) | EODHD All World (+ fundamentals if S9c security scoring is enabled) | Each user, optional |
| Academic (owner only) | Bloomberg, FactSet or I/B/E/S via the university | Validation and reproduction oracles (e.g. Sørensen V0); never shipped |

## 8. Open checks for S6 vendor coverage tests
1. Official pages for Tiingo, FMP, Finnhub and Massive limits.
2. FRED's full licence and rate limit; Ken French's terms.
3. Whether EODHD's personal plan permits per-user use inside a distributed local engine, and whether its fundamentals are point-in-time or restated.
4. EODHD coverage, history depth and adjustment quality for Oslo and the main UCITS venues, against Norges Bank FX and official Oslo closes.
5. Stooq key status.
6. KID availability per candidate instrument (PRIIPs).

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
