# S3 — Research findings (external facts as of 2026-10-01)

**Document status:** DRAFT (S3, for G3) · **Verified on:** 2026-10-01 · **Records:** [../facts/](../facts/) · **Architecture:** [S3_REGISTRY_ARCHITECTURE.md](S3_REGISTRY_ARCHITECTURE.md)

**Nature of this document:**
- It records externally sourced facts. It is **not tax, legal, or investment advice**.
- Accepting it into registry v1 means accepting the facts on the stated evidence as of the stated date. A later change in the world produces a new effective-dated fact version, not an ADR.
- Verification levels follow S3_REGISTRY_ARCHITECTURE §1: **V-full** (passage read) · **V-abs** (official summary, or a search summary of an official page — to be read in full) · **V-bib** (existence only).

## 1. Principal findings (summary)

1. **Norwegian share-income taxation 2026:** ordinary income rate 22%, upward adjustment factor 1.72, so share income is taxed at 37.84%. The shielding rate for 2025 is 3.6%; the 2026 rate is not yet published.
2. **Wealth tax 2026:**
   - threshold NOK 1,900,000;
   - combined rate 1.00% (municipal 0.35% + state 0.65%), rising to 1.10% above NOK 21.5 million;
   - listed shares and the share component of funds valued at 80%.

   A commission report (NOU 2026:9) proposes removing valuation discounts. That is **proposed, not effective**.
3. **2027 parameters are unavailable.** The 2027 budget proposition had not been published as of 2026-10-01.
4. **ASK:**
   - eligible holdings: EEA-domiciled listed shares, and EEA funds with a share component above 80%;
   - tax-deferred; no interest on cash;
   - losses deductible only on closing the account;
   - **foreign withholding actually deducted is treated as taken out of the ASK, reducing the input value.** Whether a credit is available inside ASK is not established.
5. **US dividend withholding is layered:**
   - statutory 30%;
   - treaty maximum 15% of gross (Norway–US treaty Art. 8(2) as amended);
   - W-8BEN to claim it;
   - Norwegian credit capped at Norwegian tax and at the treaty rate, with 5-year carry-forward;
   - Nordnet applies treaty rates at source for US shares traded on their local market;
   - eToro's practice is unverified.
6. **Exit tax (from 20 Nov 2024)** covers shares, fund units, and ASK, with a NOK 3,000,000 basic deduction and a 12-year rule. This is relevant to RQ-46.
7. **Product access:**
   - The Norwegian PRIIPs law (in force 1 Oct 2024) requires a key information document in Norwegian before retail access.
   - Retail CFD restrictions apply from 1 Aug 2018: leverage caps 30:1 to 2:1, 50% margin close-out, negative-balance protection.
8. **RQ-45:** the appropriateness assessment is a firm obligation. The broker's assessment or test, not the engine user's self-reported experience, is what governs access.
9. **RQ-49:** authoritative sources tie regulated investment services to provision **to third parties / clients on a business basis**, to **personal recommendations**, and to acting **on behalf of clients** or with **discretion**. No source examined addresses self-hosted, user-configured software directly. Boundaries and architectural consequences are recorded in §6 without a legal conclusion.
10. **Brokers:**
    - Nordnet: Norwegian branch of a Swedish bank; dual supervision; verified fees, FX spreads, and margin rate; API closed to new subscriptions.
    - eToro: CySEC-regulated EU entity; real shares for unleveraged buys, CFDs otherwise; NOK conversion fees verified. Several capabilities are unknown, and the inactivity fee is conflicting.

## 2. Norway — tax and account facts

| Fact | Value | Effective | Source | Level | Status |
|---|---|---|---|---|---|
| Ordinary income tax rate | 22% | Income year 2026 | Skatteetaten, *Forskuddsutskrivingen 2026* (15 Dec 2025) | V-full | verified |
| Upward adjustment factor, share income | 1.72 (effective rate 37.84%) | Income year 2026 | Forskuddsutskrivingen 2026; Skatteetaten rates page | V-full | verified |
| Losses on shares | Deductible, also multiplied by 1.72 | 2026 | Skatteetaten rates page | V-full | verified |
| Shielding rate, personal shareholders | 3.6% | Income year 2025 | Skatteetaten "Risk-free interest rate" page (method: 3-month T-bill average 4.1480% + 0.5 pp, after 22% tax) | V-full | verified |
| Shielding rate 2026 | — | Income year 2026 | Not published as of 2026-10-01 | — | unavailable |
| Mutual fund taxation | Share component > 80% at start of year → share treatment; < 20% → interest (22%); in between → proportional split; for gains, share component = average of acquisition and sale years; shielding applies to share part | In force at verification; start date not recorded | Skatteetaten "Taxation of units in mutual funds" | V-full | verified (effective_from unavailable) |
| Interest income | Ordinary income, 22% | 2026 | Forskuddsutskrivingen 2026 (rate); fund page | V-full | verified |
| Wealth tax threshold (individuals) | NOK 1,900,000 | Income year 2026 | Forskuddsutskrivingen 2026 | V-full | verified |
| Wealth tax rates | Municipal 0.35%; state 0.65% (tranche 1), 0.75% above NOK 21.5 m; combined 1.00% / 1.10% | 2026 | Forskuddsutskrivingen 2026 | V-full | verified |
| Valuation discount | Listed and unlisted shares, and the share component of securities funds, valued at 80% | 2026 | Forskuddsutskrivingen 2026; Skatteetaten valuation-discount page | V-full | verified |
| Proposal: remove valuation discounts; lower wealth-tax rates; higher threshold; separate primary-residence deduction | — | Not effective | NOU 2026:9 hearing note (regjeringen.no) | V-abs (search summary) | **proposed** |
| 2027 tax parameters | — | 2027 | Prop. 1 LS (2026–2027) not published as of 2026-10-01 | — | unavailable |
| ASK — eligible holdings | Listed shares domiciled in the EEA; units in EEA-domiciled funds with share component > 80% at start of income year; no money-market funds | In force | Skatteetaten "Share savings account (ASK)" | V-full | verified |
| ASK — cash | Allowed; no interest accrues | In force | Same | V-full | verified |
| ASK — dividends | Not taxed on payout; taxed on withdrawal | In force (dividends deferred from 2019) | Same; search summary of Skatteetaten | V-full | verified |
| ASK — withdrawals | Up to cost basis tax-free; excess taxed as share income (37.84% in 2025–2026) after shielding | 2025–2026 | Same | V-full | verified |
| ASK — losses | Deductible only when the account is closed | In force | Same | V-full | verified |
| ASK — foreign withholding | Actual withholding "must be considered taken out of ASK and the input value is reduced" | In force | Same | V-full | verified |
| ASK — credit for foreign tax | — | — | Not stated on the page | — | **unavailable** |
| ASK — accounts, transfers | Unlimited number of accounts; ASK→ASK transfers tax-neutral; transfers from ordinary account are a taxable realisation (FIFO) | In force | Same | V-full | verified |
| Ordinary (taxable) account | Realisation-based taxation | In force | Skatteetaten tax-rules pages | V-full | verified |
| Foreign holdings at foreign institutions | Not pre-filled; taxpayer must add them | In force | Skatteetaten "Foreign shares and other financial products" | V-full | verified |
| Credit deduction for foreign tax (individuals) | Same income, same year, assessed and paid, similar tax; cannot exceed Norwegian tax on it; limited to treaty rate; carry forward up to 5 years | In force | Skatteetaten "Double taxation" | V-full | verified |
| Exit tax | Shares, fund units (both components), **ASK**, among others; NOK 3,000,000 basic deduction on latent gain/loss; pay within 12 years unless moving back; options to pay immediately, by instalment, or defer with security | Relocations from 20 Nov 2024 | Skatteetaten "Exit tax" | V-full | verified |
| Non-pension wrappers in scope | ASK; ordinary taxable account (e.g. Aksje- og fondskonto) | — | As above | V-full | verified |

## 3. Foreign withholding (US source, Norwegian resident)

| Layer | Finding | Source | Level | Status |
|---|---|---|---|---|
| W1 statutory | 30% on US-source FDAP income (incl. dividends) to foreign persons | IRS "NRA withholding" | V-full | verified |
| W2 treaty | "shall not exceed 15 percent of the gross amount actually distributed" (Art. 8(2) as amended by protocol) | US–Norway Income and Property Tax Convention, IRS treaty text | V-full | verified |
| W3 eligibility | W-8BEN to the withholding agent/payer before payment; valid until the last day of the third succeeding calendar year (absent change of circumstances); failure may lead to 30% | IRS Instructions for Form W-8BEN (Rev. 10/2021) | V-full | verified |
| W4 relief at source | Treaty rate applied by the withholding agent on valid W-8BEN | Same (interpretation of mechanism) | V-full | **interpretation** |
| W5 actually withheld — Nordnet | Applies treaty rates for Sweden, Finland, USA, Canada for customers tax-registered in NO/SE/DK/FI, "as long as the share is traded on its local market" | Nordnet FAQ (foreign dividends) | V-full | verified |
| W5 actually withheld — eToro | — | Not found | — | **unavailable** |
| W6 reclaim (US) | — | Not researched in primary sources | — | unavailable |
| W7 Norwegian credit | See §2 (capped at Norwegian tax and the treaty rate; 5-year carry-forward) | Skatteetaten | V-full | verified |
| W8 ASK | Withholding treated as a withdrawal reducing input value; credit availability not stated | Skatteetaten ASK page | V-full / — | verified / unavailable |
| W9 fund level | — | No authoritative source located | — | **unavailable** (RQ-51) |

**Consequence:**
- Treaty rate (15%) and actually-withheld rate are separate facts. For Nordnet, the actually-withheld rate equals the treaty rate *only under the stated condition* (local-market listing).
- Inside ASK, withholding reduces input value rather than producing a confirmed credit.

## 4. Regulation and product access

| Rule | Finding | Source | Level | Status |
|---|---|---|---|---|
| PRIIPs (Norway) | PRIIPs law in force **1 Oct 2024**. Retail investors given access to a PRIIP must receive key information in good time before investing. Producers prepare it **in Norwegian**. Finanstilsynet supervises | Finanstilsynet PRIIPs page; Lovdata LOV-2024-06-21-40 | V-full | verified |
| US-domiciled ETFs | Retail access requires a Norwegian KID; US-domiciled ETFs without one cannot be made available to retail investors | Inference from the PRIIPs requirement | — | **interpretation** (to confirm with a direct Finanstilsynet/ESMA statement) |
| MiFID II definitions | Investment firm: person whose occupation or business is providing investment services on a professional basis; investment advice: personal recommendations on transactions in financial instruments; execution of orders on behalf of clients; portfolio management: discretionary, client-by-client under mandates | Directive 2014/65/EU Art. 4(1)(1), (4), (5), (8) | V-full (definitions) | verified |
| MiFID II appropriateness / execution-only | Art. 25(3) (appropriateness based on knowledge and experience) and 25(4) (execution-only for non-complex instruments) | Directive 2014/65/EU | V-abs (the retrieved summary was unreliable on detail) | obligated party (the firm): verified (V-abs); exact conditions: **unavailable pending re-read** |
| Personal recommendation | Presented as suitable for the person or based on their circumstances; not issued exclusively to the public | Delegated Regulation (EU) 2017/565 Art. 9 | V-abs | verified (summary) — re-read |
| Norwegian implementation | Investment services list (§ 2-1); investment advice = personal recommendation to a customer (§ 2-3(4)); portfolio management = discretionary management of investors' portfolios on an individual basis (§ 2-3(3)); investment firm = provides investment services to third parties or performs investment activity on a business basis (§ 2-7) | Verdipapirhandelloven (LOV-2007-06-29-75), ch. 2 | V-full | verified |
| CFD retail restrictions | Leverage caps 30:1 (major FX) / 20:1 / 10:1 / 5:1 (single equities) / 2:1 (crypto); 50% margin close-out per account; negative-balance protection; no incentives; standardised risk warning | ESMA final product-intervention measures (press release) | V-abs | verified (summary) |
| CFD restrictions in Norway | Restrictions on marketing, distribution, and sale of CFDs to non-professional customers effective **1 Aug 2018**; binary options banned 2 Jul 2018; basis MiFIR and the Norwegian MiFIR regulation | Finanstilsynet news (2018) | V-full | verified |
| Advice perimeter guidance | ESMA35-43-3861 (2023): personal-recommendation tests; generic advice is not investment advice unless part of the advice process (¶48); advice may be given through an interactive software system, e.g. robo-advice (¶84); filtering by itself is not automatically a recommendation (¶36); emphasis on one product can amount to one (¶62); the briefing "might also be used" to assess non-regulated persons (¶7); **not binding** (¶9) | ESMA supervisory briefing | V-full (passages) | verified |

## 5. RQ-45 — legal requirement vs. broker implementation

| Layer | Finding | Level |
|---|---|---|
| 1. Law | MiFID II Art. 25(3) places the appropriateness assessment on the **firm**, for non-advised services in complex instruments | V-abs (re-read pending) |
| 2. ESMA | ESMA has guidelines on appropriateness and execution-only (referenced in ESMA35-43-3861 ¶64); not separately read | V-bib |
| 3. Finanstilsynet / Norway | MiFID II supplementary regulation has a section on suitability and appropriateness (Lovdata FOR-2017-12-20-2300, ch. 6, section 3); not read in full | V-bib |
| 4. Nordnet | Knowledge tests for complex products (options, futures, warrants); short selling requires leverage and short-selling tests and is available on Aksje- og fondskonto only | V-abs |
| 5. eToro | Appropriateness implementation not verified | — |

**Finding:** access is governed by the firm's assessment, performed by the
broker. Self-reported experience in this engine has no legitimate
eligibility consumer. Field `INV.investment_experience` (1.7) has no
independent consumer identified (decision D3-07).

## 6. RQ-49 — regulatory boundaries of a self-directed investment application

**Framing:** a general-purpose, self-directed application that individuals
run locally with their own configuration and accounts. The question is not
whether the developers provide services to friends.

### 6.1 Authoritative statements (what sources establish)

| # | Statement | Source | Level |
|---|---|---|---|
| A1 | Investment firm status attaches to persons whose regular occupation or business is providing investment services (to third parties) or performing investment activities on a professional basis | MiFID II Art. 4(1)(1) | V-full; the "third parties" wording is to be re-quoted verbatim (U7) |
| A2 | In Norway, an investment firm provides investment services **to third parties** or performs investment activity **on a business basis** | Vphl § 2-7(1) | V-full |
| A3 | Investment advice = personal recommendations to a client/customer | MiFID II Art. 4(1)(4); vphl § 2-3(4) | V-full |
| A4 | Personal recommendation = presented as suitable or based on the person's circumstances; not exclusively to the public | Del. Reg. 2017/565 Art. 9 | V-abs |
| A5 | Generic advice is not investment advice unless part of the advice process | ESMA35-43-3861 ¶48 | V-full |
| A6 | Advice can be provided through an automated or semi-automated client-facing system / interactive software (robo-advice) | ESMA35-43-3861 ¶24, ¶84 | V-full |
| A7 | Portfolio management = discretionary management on a client-by-client basis under client mandates | MiFID II Art. 4(1)(8); vphl § 2-3(3) | V-full |
| A8 | Reception/transmission and execution of orders are services when performed on behalf of clients | MiFID II Art. 4(1)(5); vphl § 2-1(1)(1)–(2) | V-full |
| A9 | ESMA's briefing may be used to assess whether a non-regulated person engages in advice; it is not binding | ESMA35-43-3861 ¶7, ¶9 | V-full |

**Not established by any source examined:** whether developing or
distributing self-hosted software that computes outputs from the user's
own configuration, for the user's own decisions, constitutes the
developer/distributor providing investment advice, portfolio management,
or order transmission. This is a **gap**, not a conclusion either way.

### 6.2 Capability → rule structure (architectural inference, labelled)

| Capability (S3 brief #) | Relevant rule/source | Jurisdiction | Possible triggering condition | Possible consequence | Architectural implication (inference) | Status |
|---|---|---|---|---|---|---|
| Market, portfolio, generic analytics (1–3) | A5 | EEA/NO | — (generic) | None indicated | None | interpretation |
| User-configured profile; personalised analysis; beliefs; risk; construction; candidate comparison; target portfolio; rebalancing calculations (4–12) | A1–A4, A6 | EEA/NO | A provider, acting as a business toward third parties, presents outputs as suitable or based on the person's circumstances | Could be characterised as investment advice by that provider (authorisation) | Keep provider role absent from the user's decision loop (local, self-configured, user-held data). Keep methodology transparent. Do not rely on disclaimers alone (ESMA ¶64, perimeter issues). **Professional legal review before broad public or commercial distribution of personalised-output features** | gap / interpretation |
| Trade-list generation (13) | A3–A4 (recommendation to buy/sell a particular instrument) | EEA/NO | As above | As above | As above; trade lists remain user-confirmed (S2 authority model) | gap / interpretation |
| Order staging, broker API connectivity, order submission (14–16) | A8 | EEA/NO | Orders received/transmitted or executed **on behalf of clients** by the provider | Investment service | **Local execution with user-held broker credentials**; no hosted order relay by the developers without legal review; broker performs execution | interpretation |
| Rule-based automated rebalancing; signal-driven target changes; unattended execution (17–19) | A7, A8 | EEA/NO | Discretion exercised **for a client** under a mandate | Portfolio management | Keep authority grants (ADR-0017) user-held and revocable; unattended execution gated by S13 safeguards **and** legal review before enabling in distributed builds | gap / interpretation |

### 6.3 Distinctions requested at S3 approval

| Distinction | What sources establish | Open |
|---|---|---|
| Developing software vs. providing a service | Services attach to provision to clients/third parties on a business basis (A1, A2) | Application to software distribution |
| Distributing/licensing vs. personally advising | Same | Same |
| Generic analytics vs. personalised outputs | A4, A5 | — |
| User-configured deterministic calculations vs. recommendations | A4 (recommendation = presented as suitable / based on circumstances) | Whether self-configured computations by the user count as anyone's "recommendation" |
| Personalised recommendations vs. portfolio management | A3 vs. A7 | — |
| User-directed construction vs. discretionary decisions for a client | A7 | — |
| Construction vs. trade generation | A4 (transactions in particular instruments) | — |
| Trade generation vs. execution | A8 | — |
| User-confirmed vs. unattended execution | Not addressed directly | Yes |
| Broker functionality vs. application functionality | A8 (execution by the authorised broker) | Status of API tooling |
| Local/self-hosted vs. externally hosted | Not addressed directly | Yes |
| Private use vs. wider distribution | Not addressed directly | Yes |

**Overall:** no regulatory status is inferred. The architecture keeps every
capability representable. The S2 authority model and the local execution
pattern preserve options. Professional legal review is the identified
trigger before enabling personalised-output or execution capabilities in
publicly distributed builds (decision D3-08).

## 7. Nordnet registry summary (Norwegian retail, as of 2026-10-01)

| Attribute | Finding | Source | Level | Status |
|---|---|---|---|---|
| Legal entity | Nordnet Bank NUF, Norwegian branch of Nordnet Bank AB | nordnet.no "Sikkerhet og garanti" | V-full | verified |
| Supervision | Finansinspektionen (SE) and Finanstilsynet (NO) | Same | V-full | verified |
| Deposit guarantee | Up to NOK 2,000,000 (Bankenes sikringsfond and Riksgälden); certain life-event deposits unlimited | Same | V-full | verified |
| Investor protection | Up to SEK 250,000 (Swedish investor protection) | Same | V-full | verified |
| Custody | Norwegian securities on Aksje- og fondskonto registered on the customer's own VPS account; foreign securities held with custodian(s) in Nordnet's name | Same | V-full | verified |
| Account types (non-pension) | ASK; Aksje- og fondskonto | nordnet.no account pages | V-abs | verified (summary) |
| ASK market scope | EU/EEA-listed only; no US/Canadian shares | nordnet.no ASK page (search summary); consistent with law | V-abs | verified (summary) |
| Commission — Nordic markets | Mini 0.15% (min NOK 29); Normal 0.049% (min 79); Bonus 0.04% (min 69); VIP 0.035% (min 39) | nordnet.no price list | V-full | verified |
| Commission — US/other | Mini 0.2% (min 49); Normal 0.1% (min 99); Bonus 0.09% (min 89); VIP 0.08% (min 79) | Same | V-full | verified |
| FX | Automatic conversion 0.5% spread (0.25% per side); with currency account 0.15% (0.075% per side) | Same | V-full | verified |
| Fund platform fees | Active equity funds 0.29%; Nordnet index funds 0.19%; external index funds 0.15% | Same | V-full | verified |
| Margin lending (NOK) | 7.34% nominal / 7.59% effective; over-leverage rate 11.75% | Same | V-full | verified (supersedes legacy-unverified 7.32%) |
| Short selling | Aksje- og fondskonto only; requires leverage and short-selling knowledge tests | nordnet.no FAQ (search summary) | V-abs | verified (summary) |
| Complex-product tests | Required for complex securities (options, futures, warrants), citing MiFID II | nordnet.no (search summary) | V-abs | verified (summary) |
| API | Nordnet External API "closed for new subscriptions", no reopening date; waitlist via customer service | nordnet.se FAQ | V-full (scope: Nordnet group API) | verified |
| Tax reporting | Euronext VPS reports Norwegian funds and Oslo Børs shares; Nordnet reports foreign securities, ETFs, dividends, and wealth; options/forwards/futures self-reported | nordnet.no "Hvem rapporterer hva" | V-full | verified |
| Withholding practice | §3 W5 | — | V-full | verified |
| Fractional shares; order types; detailed exchange list | — | Not verified | — | **unknown** |

## 8. eToro registry summary (EEA retail, as of 2026-10-01)

| Attribute | Finding | Source | Level | Status |
|---|---|---|---|---|
| Legal entity (EU/EEA) | eToro (Europe) Ltd, CySEC licence 109/10 | etoro.com "Regulation and License" | V-full | verified |
| Entity for Norwegian residents | Expected to be the EU/EEA entity; no Norway-specific statement found | Same | — | **interpretation** |
| Investor compensation | Cyprus Investor Compensation Fund up to €20,000; local deposit guarantee up to €100,000 for deposits at EEA partner banks | Same | V-full | verified |
| Crypto coverage by ICF | Not covered | Search summary of regulation page | V-abs | verified (summary) |
| Ownership model | Unleveraged buy positions in stocks are real assets in a segregated omnibus account; short, leveraged, and certain other positions are CFDs | eToro help (search summary) | V-abs | verified (summary) |
| Stock commission | $1 or $2 per open/close depending on country of residence and exchange; Norway-specific value not shown | etoro.com/trading/fees | V-full (rule) | verified (rule) / **unknown** (Norway value) |
| ETF commission | Zero | Same | V-full | verified |
| Stock CFDs | 0.15% per trade | Same | V-full | verified |
| NOK conversion (USD account) | Card 1%; wallets 1600 pips; online banking 1600 pips; bank transfer 1%; Club-tier discounts | etoro.com/trading/fees/conversion | V-full | verified |
| Withdrawal fee | $5 from USD account; free from local-currency accounts | etoro.com/trading/fees | V-full | verified |
| Inactivity fee | Fee page shows "Free" (Club caveat); help/summary source states $10/month after 12 months without login | Two eToro sources | V-full / V-abs | **unresolved_conflicting** |
| Norwegian wrapper (ASK) at eToro | No eToro source found | — | — | **unknown** (not false) |
| API | Public API with personal keys (x-api-key, x-user-key) allowing actions on the user's own verified account; builder programme terms titled "BETA PRODUCT" | builders.etoro.com (search summary); terms PDF | V-abs / V-bib | verified (summary) |
| API regional eligibility | — | Not verified | — | **unknown** |
| Tax report | eToro provides a tax report for Norwegian residents (Club-tier eligibility; March release window) | eToro help (search summary) | V-abs | verified (summary) |
| Reporting to Skatteetaten | Not confirmed by eToro. Skatteetaten states foreign institutions' holdings are not pre-filled (general rule) | Skatteetaten | V-full (general rule) | **interpretation** for eToro |
| Withholding practice; appropriateness implementation; fractional shares; margin specifics | — | Not verified | — | **unknown** |

## 9. Unresolved facts and research gaps

| # | Gap | Next step |
|---|---|---|
| U1 | Shielding rate 2026 | Record when published (January 2027) |
| U2 | 2027 tax parameters | Record on publication of Prop. 1 LS (2026–2027) and Storting adoption |
| U3 | NOU 2026:9 content (read directly) | Read the hearing note; keep `proposed` |
| U4 | Credit for foreign withholding inside ASK | Skatte-ABC A-10 (current) direct read |
| U5 | Fund-level withholding (W9) | RQ-51 |
| U6 | US reclaim mechanism (W6) | IRS primary sources |
| U7 | MiFID II Art. 25(3)/(4) exact text; Del. Reg. 2017/565 Art. 9 | Re-read EUR-Lex |
| U8 | ESMA appropriateness guidelines; Norwegian MiFID II supplementary regulation ch. 6 §3 | Read directly |
| U9 | Direct authority on US-domiciled ETF retail access under PRIIPs | Finanstilsynet/ESMA statement |
| U10 | eToro: Norway-specific commission, entity applicability, ASK, withholding, appropriateness, API eligibility, inactivity-fee conflict | Read terms (eToro EU T&C, 2026 version) and help articles directly |
| U11 | Nordnet: fractional shares, order types, exchange list; full read of the account, short-selling, and knowledge-test pages | Direct reads |
| U12 | Fund taxation rule effective date | Skatte-ABC |
| U13 | RQ-49: application of service definitions to self-hosted software distribution | Professional legal review (D3-08) |
