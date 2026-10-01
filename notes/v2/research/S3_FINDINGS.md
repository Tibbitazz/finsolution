# S3 — Research findings (external facts as of 2026-10-01)

**Document status:** DRAFT (S3, for G3; revised 2026-10-01 per owner corrections) · **Verified on:** 2026-10-01 · **Records:** [../facts/](../facts/) · **Architecture:** [S3_REGISTRY_ARCHITECTURE.md](S3_REGISTRY_ARCHITECTURE.md)

**Nature of this document:**
- It records externally sourced facts. It is **not tax, legal, or investment advice**.
- Verification levels follow S3_REGISTRY_ARCHITECTURE §1: **V-full** (passage read) · **V-abs** (official summary, or a search summary of an official page — to be read in full) · **V-bib** (existence only).
- **Scope exclusions:** pension saving (ADR-0020) and wealth tax (ADR-0021) are not researched or recorded.

**What accepting these facts at G3 means:** each fact is accepted into
registry v1 at its stated source, scope, verification level, valid-time
coordinates, and knowledge-time coordinates, based on the evidence
available on the verification date. Acceptance does not certify a fact
forever. Later authoritative changes create new effective-dated facts and
never rewrite historical ones.

## 1. Principal findings (summary)

1. **Norwegian share-income taxation 2026:** ordinary income rate 22%, upward adjustment factor 1.72 (effective 37.84%). The shielding rate for 2025 is 3.6%; the 2026 rate is unpublished (`unavailable`). 2027 parameters are `unavailable`.
2. **ASK — rules:** eligible holdings, tax-exempt dividends inside the account, withdrawal ordering and taxation, in-kind withdrawals not a realisation, losses only on closure, FX gains inside ASK outside the exemption. All verified against Skatte-ABC 2025/2026 A-10.
3. **ASK — foreign withholding (corrected).**
   - Withheld tax is deemed withdrawn and reduces input value (verified).
   - **The credit rules for foreign withholding on dividends may apply on a taxable withdrawal** (verified, Skatte-ABC A-10-5.4.1). This is a conditional rule, not an unconditional entitlement.
   - The calculation inside ASK, tracking of withheld tax, interaction with the input-value reduction, and how carry-forward applies to the gap between dividend year and withdrawal year are **not established**.
4. **US dividend withholding is layered:** 30% statutory → 15% treaty → W-8BEN → Nordnet applies the treaty rate (conditional on local-market listing) → Norwegian credit capped. eToro's practice, reclaim, and fund-level withholding are unknown.
5. **Exit tax (from 20 Nov 2024):** covers shares, fund units, and ASK; NOK 3 m basic deduction; 12-year rule (RQ-46).
6. **PRIIPs chain:**
   - Investment funds are PRIIPs.
   - A seller or adviser must provide the KID before the retail investor is bound, also when the sale is solely on the customer's initiative.
   - The KID must be in Norwegian, and no exemption is in force.
   - Breach is sanctionable.

   The **conditional rule** "PRIIP without a Norwegian KID cannot lawfully be sold to Norwegian retail investors" is promoted to verified. **"US-domiciled ETFs are unavailable"** stays an interpretation, because "no Norwegian KID exists" is a per-instrument fact supported only by secondary sources.
7. **RQ-45:** appropriateness is the firm's obligation; Nordnet implements tests. No legitimate engine consumer of self-reported experience has been established, but none has been ruled out. The field stays inactive (revised D3-07).
8. **RQ-49:** authoritative statements are separated from inference. The closest authoritative analogue to "user-declared rules computed deterministically" is ESMA ¶36/¶38: filtering, and assisting a person's own choice. Both are non-binding and firm-oriented. **No source determines the question.** RQ-49 stays open, and capabilities are gated only where a genuine dependency exists (revised D3-08).
9. **Brokers:** facts recorded with unknown kept distinct from verified-unsupported (§9). The eToro inactivity-fee conflict is unresolved after a second attempt (§8).

## 2. Norway — tax and account facts

| Fact | Value | Effective | Source | Level | Status |
|---|---|---|---|---|---|
| Ordinary income tax rate | 22% | 2026 | Skatteetaten, *Forskuddsutskrivingen 2026* (15 Dec 2025) | V-full | verified |
| Upward adjustment factor | 1.72 (effective 37.84%); losses symmetric | 2026 | Same; Skatteetaten rates page | V-full | verified |
| Shielding rate | 3.6% | 2025 | Skatteetaten rate page | V-full | verified |
| Shielding rate | — | 2026 | Not published as of 2026-10-01 | — | unavailable |
| 2027 parameters | — | 2027 | Prop. 1 LS (2026–2027) not published | — | unavailable |
| Fund taxation | > 80% share component → share treatment; < 20% → interest; otherwise proportional; average share component for gains; shielding on share part | In force (start date unrecorded, U12) | Skatteetaten fund page | V-full | verified |
| ASK — eligible holdings | EEA-listed shares; EEA funds > 80% shares; no money-market funds; cash earns no interest | In force | Skatteetaten ASK page | V-full | verified |
| ASK — dividends | Tax-exempt inside the account; taxed only through withdrawals; pre-2019 taxed dividends count as contributed capital | From 2019 | Skatte-ABC 2025/2026 A-10-5.4.1 | V-full | verified |
| ASK — withdrawals | Contributions out first; excess over contributions + shielding taxable, × 1.72; in-kind withdrawals at market value, **not a realisation**, value becomes new input value outside ASK | In force | Skatte-ABC A-10-6.1 | V-full | verified |
| ASK — foreign currency | Account funds cannot buy currency; FX gain/loss outside the ASK exemption, realised on conversion to NOK, withdrawal, or purchase of securities | In force | Skatte-ABC A-10-5.2 | V-full | verified |
| ASK — losses | Deductible only on closure | In force | Skatteetaten ASK page; A-10-6.1 | V-full | verified |
| ASK — transfers | Unlimited accounts; ASK→ASK tax-neutral (contributions and unused shielding follow pro rata); transfer in from ordinary account taxable (FIFO) | In force | ASK page; Skatte-ABC A-10-6.4 | V-full | verified |
| ASK — foreign withholding | Deemed withdrawn; reduces input value | In force | Skatteetaten ASK page | V-full | verified |
| ASK — credit | See §2.1 | | | | |
| Ordinary account | Realisation-based; dividends taxed when received | In force | Skatteetaten | V-abs | verified (summary) |
| Foreign holdings at foreign institutions | Not pre-filled | In force | Skatteetaten | V-full | verified |
| Credit deduction (general) | Same income, same year, assessed and paid, similar tax; cap = Norwegian tax on that income; treaty-rate limit; 5-year carry-forward within category; claim in tax return (time limits sktl. § 16-25) | In force | Skatteetaten "Double taxation"; Skatte-ABC U-20-4.16, U-20-4.20 | V-full | verified |
| Exit tax | Shares, fund units, ASK; NOK 3 m basic deduction; 12-year rule; payment options | From 20 Nov 2024 | Skatteetaten "Exit tax" | V-full | verified |

**Removed from the S3 draft (ADR-0021, owner scope decision):** wealth-tax
threshold, wealth-tax rates, valuation discounts, and the NOU 2026:9
wealth-tax proposal. These were provisional records and never accepted, so
no registry history is affected.

### 2.1 ASK foreign-withholding credit — decomposition (corrected)

The S3 draft was wrong to classify credit availability inside ASK as
unknown. The corrected position:

| # | Question | Finding | Source | Status |
|---|---|---|---|---|
| 1 | Can Norwegian credit rules apply in principle? | **Yes, may apply on a taxable withdrawal:** «Reglene om kreditfradrag for kildeskatt betalt i utlandet på mottatt utbytte kan komme til anvendelse ved skattepliktig uttak fra kontoen» | Skatte-ABC 2025/2026 A-10-5.4.1 | verified (V-full). "May apply" is conditional: entitlement in a case depends on the general credit conditions (row 3) |
| 2 | When may the credit be claimed? | Trigger: a taxable withdrawal. General rule: in the tax return for the year the income is taxable in Norway. No source says a credit arises at dividend receipt (dividends are exempt then) | A-10-5.4.1; U-20-4.20 (general) | verified trigger; ASK-specific claim procedure not stated |
| 3 | How is it calculated and limited? | General: capped at the Norwegian tax on the foreign income within the income category; treaty-rate limit. **How the "foreign income" portion of an ASK withdrawal is determined is not established** | Skatteetaten; U-20 (general) | general verified; ASK application **unavailable** (U4a) |
| 4 | How is withholding tracked through the ASK? | The provider's account record must show, among other things, dividends received and taxable withdrawals in the year (FSFIN § 10-21-4). Foreign tax withheld is **not** among the listed items | Skatte-ABC A-10-12.4 | verified list; tracking of withheld tax **not stated** (U4b) |
| 5 | Interaction with the input-value reduction | The reduction is verified. Its interaction with a later credit claim (e.g. whether the deemed withdrawal is itself part of a taxable withdrawal) is not established | ASK page | **unavailable** (U4c) |
| 6 | Timing / carry-forward | General: unused credit carried forward up to 5 years within the category (sktl. § 16-22); timing differences handled by claiming in the year taxed abroad and carrying forward (U-20-4.7.3). Neither addresses the multi-year gap between withholding in the dividend year and an ASK withdrawal | U-20-4.7.3; U-20-4.16 | general verified; ASK application **not stated** (U4d) |
| 7 | Broker information | Nordnet's credit guidance covers Aksje- og fondskonto only; Nordnet states it cannot help with corrections or refunds. Nothing ASK-specific found for either broker | Nordnet FAQ | **unavailable** (U4e) |

## 3. Foreign withholding (US source, Norwegian resident)

| Layer | Finding | Source | Level | Status |
|---|---|---|---|---|
| W1 statutory | 30% on US-source FDAP income to foreign persons | IRS "NRA withholding" | V-full | verified |
| W2 treaty | ≤ 15% of the gross amount actually distributed (Art. 8(2) as amended) | US–Norway Convention (IRS text) | V-full | verified |
| W3 eligibility | W-8BEN to the withholding agent; valid to end of third succeeding calendar year; failure may lead to 30% | IRS Instructions W-8BEN (10/2021) | V-full | verified |
| W4 relief at source | Treaty rate applied by agent on valid W-8BEN | Same | V-full | interpretation |
| W5 Nordnet | Treaty rates for SE, FI, US, CA when the share trades on its local market | Nordnet FAQ | V-full | verified |
| W5 eToro | — | — | — | unavailable |
| W6 reclaim | — | — | — | unavailable |
| W7 credit | Cap = Norwegian tax on the income; treaty-rate limit; 5-year carry-forward | Skatteetaten; Skatte-ABC U-20-4.16 | V-full | verified |
| W8 ASK | Input value reduced (verified); credit rules may apply on taxable withdrawal (verified); mechanics partly unestablished (§2.1) | Skatteetaten; Skatte-ABC A-10-5.4.1 | V-full | verified (components 3–7 partly unavailable) |
| W9 fund level | — | — | — | unavailable (RQ-51) |

## 4. Regulation and product access

| Rule | Finding | Source | Level | Status |
|---|---|---|---|---|
| MiFID II definitions | Investment firm; investment advice (personal recommendations to a client); execution on behalf of clients; portfolio management (discretionary, client-by-client, under mandates) | Dir. 2014/65/EU Art. 4(1)(1), (4), (5), (8) | V-full | verified; the "third parties" wording of 4(1)(1) to be re-quoted (U7) |
| MiFID II appropriateness | Obligation of the firm; exact conditions unrecorded | Art. 25(3)–(4) | V-abs | verified (obligated party only) |
| Personal recommendation | Presented as suitable or based on the person's circumstances; not exclusively to the public | Del. Reg. 2017/565 Art. 9 | V-abs | verified (summary) |
| Norwegian implementation | §§ 2-1, 2-3(3)–(4), 2-7 | Vphl ch. 2 | V-full | verified |
| CFD retail measures | Leverage caps 30:1 … 2:1; 50% margin close-out; negative-balance protection; no incentives; risk warning | ESMA | V-abs | verified (summary) |
| CFD/binary in Norway | CFD restrictions from 1 Aug 2018; binary options banned from 2 Jul 2018 | Finanstilsynet (2018) | V-full | verified; current status re-check due |
| ESMA advice briefing | Non-binding (¶9); usable for non-regulated persons (¶7); automated tools (¶24, ¶84); presentation test (¶16); emphasis by person or software (¶30, ¶62); filtering (¶36); assisting own choice (¶38); model portfolios (¶40–41); generic advice (¶48); disclaimers (¶64–65); public lists (¶81) | ESMA35-43-3861 | V-full | verified. **Correction:** the disclaimer point is ¶64–65, not ¶64 alone |

### 4.1 PRIIPs chain for US-domiciled ETFs

| Step | Finding | Source | Status |
|---|---|---|---|
| 1. Instrument is a PRIIP | PRIP = amount repayable fluctuates with reference values or assets not directly purchased by the retail investor (Art. 4(1)); PRIIP includes PRIP (Art. 4(3)); recital 6 lists **investment funds**; recital 7: directly held shares are not PRIIPs. An ETF is an investment fund regardless of domicile | Reg. (EU) 1286/2014 (as adopted; legislation.gov.uk archive) | verified (V-full; consolidated amendments not checked, U7b) |
| 2. KID requirement applies | Manufacturer draws up and publishes the KID before the product is made available (Art. 5(1)); seller or adviser provides it before the retail investor is bound (Art. 13(1)); Art. 13(3) allows delivery after the transaction only for customer-initiated distance sales, which presupposes a KID exists. In Norway the requirement applies even when the sale is solely on the customer's own initiative (Finanstilsynet); the KID must be in Norwegian (PRIIPs-loven § 4); no exemption in the PRIIPs-forskriften | Reg. Art. 5, 13; Finanstilsynet; LOV-2024-06-21-40 § 4; FOR-2024-09-16-2162 | verified (V-full) |
| 3. Compliant KID unavailable | That US issuers generally publish no Norwegian KID is reported by press and broker-review sources. No issuer or regulator source was found. This is a **per-instrument** fact | Secondary only | **interpretation** (U9); S6 instrument attribute `kid_available_no` |
| 4. Consequence | Finanstilsynet may suspend or prohibit marketing (§ 6) and fine breaches of Art. 5(1) and 13(1) (§ 7). A seller cannot meet Art. 13(1) for a PRIIP with no Norwegian KID | PRIIPs-loven §§ 2, 6, 7 | verified (V-full) |

**Result:**
- **Promoted (verified):** *a PRIIP for which no Norwegian KID is available cannot lawfully be sold to a Norwegian retail investor.* This is a one-step application of mandatory provisions; no source sentence uses the word "prohibited".
- **Not promoted (interpretation):** *US-domiciled ETFs are unavailable to Norwegian retail investors.* It depends on step 3 for each instrument.
- **Not researched:** whether marketing rules for non-UCITS funds under the AIF law add a separate barrier (U9b).

## 5. RQ-45 — self-reported experience vs. appropriateness (revised)

| Layer | Finding | Level |
|---|---|---|
| Law | Appropriateness assessment is an obligation of the firm (MiFID II Art. 25(3)) | V-abs |
| ESMA / Norway | Guidelines and supplementary regulation exist; not read in full | V-bib |
| Nordnet | Knowledge tests for complex products, leverage, short selling | V-abs |
| eToro | Not verified | — |

**Finding (bounded):**
- Regulatory and broker access is determined by the applicable rules and the broker's process, not by the engine.
- Self-reported experience therefore **cannot independently grant product eligibility**, and the engine must not substitute its own assessment for a broker-required test.
- This does **not** establish that experience has no legitimate downstream consumer; candidates such as explanation depth or warnings are unresearched.
- Field 1.7 stays an inactive, conditional schema capability, not collected by default, pending completion of RQ-45 (D3-07 revised).

## 6. RQ-49 — regulatory boundaries of a self-directed investment application

**Framing:** reusable software that individuals use at their own discretion
for their own investments. The developers do not provide financial
services to friends or family or manage portfolios on anyone's behalf.
That framing does not by itself resolve every regulatory question.

### 6.1 What authoritative sources establish

| # | Statement | Source | Level |
|---|---|---|---|
| A1 | Investment-firm status attaches to providing investment services (to third parties) or performing investment activities on a professional basis | MiFID II Art. 4(1)(1) | V-full (re-quote U7) |
| A2 | Norwegian investment firm: provides investment services to third parties or performs investment activity on a business basis | Vphl § 2-7 | V-full |
| A3 | Investment advice = personal recommendations to a client | MiFID II 4(1)(4); vphl § 2-3(4) | V-full |
| A4 | A personal recommendation is **made to a person** in their capacity as investor (¶25); it is presented as suitable or based on that person's circumstances, judged from a reasonable observer's view (¶16); not if issued exclusively to the public | Del. Reg. 2017/565 Art. 9; ESMA ¶16, ¶25 | V-abs / V-full |
| A5 | Advice may be provided through automated or semi-automated client-facing tools | ESMA ¶24, ¶84 | V-full |
| A6 | Letting a client filter information "does not automatically mean that a recommendation is being given by the firm" | ESMA ¶36 | V-full |
| A7 | "A critical factor would be whether the process is limited to assisting the person to make their own choice of product which has particular features which the person regards as important"; if so, a personal recommendation is "unlikely" | ESMA ¶38 | V-full |
| A8 | Model portfolios: case-by-case; profile → model portfolio positioned as the appropriate action can amount to advice | ESMA ¶40–41 | V-full |
| A9 | Emphasis by a person **or software** that tends to influence selection can amount to a recommendation | ESMA ¶30, ¶62 | V-full |
| A10 | Generic advice is not investment advice unless part of the advice process; public lists normally not advice | ESMA ¶48, ¶81 | V-full |
| A11 | Disclaimers can be of some use but cannot prevent the qualification | ESMA ¶64–65 | V-full |
| A12 | Portfolio management = discretionary, client-by-client, under mandates; execution/transmission = on behalf of clients | MiFID II 4(1)(5), (8); vphl §§ 2-1, 2-3(3) | V-full |
| A13 | The ESMA briefing is non-binding, is addressed to supervisors and firms, and may be used to assess non-regulated persons | ESMA ¶7, ¶9 | V-full |

### 6.2 Distinction A vs. B

- **A:** the application independently makes a personalised recommendation.
- **B:** the user declares a Policy Statement, methodology, and permitted rules, and deterministic software calculates or implements the consequences of those instructions.

| Question | What sources establish | What they do not establish |
|---|---|---|
| Is there a recommendation "made to a person" by someone? | A4: a recommendation is made **by** a provider **to** a person. A13: the framework addresses firms and persons providing services | Whether the developer or distributor of user-configured software is the person "making" an output the user's own instructions determine |
| Does user-directed processing differ from recommendation? | A6, A7: processes limited to assisting a person's own choice based on features the person regards as important are unlikely to be personal recommendations. These are the closest analogues to B | They concern **firms** offering filtering to **clients**; they do not address software the user runs locally, or optimisation that produces specific instruments and weights |
| Can B slide into A? | A8, A9: positioning outputs as the appropriate action, or emphasis by software, can create a recommendation | Where the line falls for an optimiser whose objective and constraints the user chose |
| Do disclaimers decide it? | A11: no | — |

**Conclusion:** A and B are **neither established as legally equivalent
nor as legally different.** The sources give relevant factors (who makes
the output, presentation, emphasis, whether the process assists the user's
own choice) but no determination for self-hosted, user-configured software.

### 6.3 Capability register (owner's format)

Format: `capability → evidence/regulatory status → unresolved issue → required dependency/safeguard → enablement status`.

| Capability | Evidence / regulatory status | Unresolved issue | Required dependency / safeguard | Enablement status |
|---|---|---|---|---|
| Generic analytics | A10: generic, not advice | — | — | Enablable when built (no regulatory dependency identified) |
| Personalised analytics (descriptive, of the user's own holdings) | Not a recommendation on its face (no instrument recommended) | Whether personalised descriptive outputs fall under A4 | Neutral presentation; no emphasis (A9) | Enablable when built |
| Deterministic implementation of user-selected rules | Closest analogue A6/A7 (unlikely recommendation) | A vs. B (§6.2) | User-declared configuration recorded (S1/S2); neutral presentation; provenance of every rule to the user's declaration | Enablable for the user's own use; distribution posture open (RQ-49) |
| Model portfolios | A8: case-by-case; positioning matters | Whether any are offered and how presented | Not positioned as "appropriate for you"; no profile → portfolio mapping presented as advice | Gated on design decision at S11/S14 (no regulatory finding forces exclusion) |
| Personalised target portfolios | A vs. B unresolved | Whether an optimiser output computed from user-chosen objective and constraints is a personal recommendation by anyone | Methodology selected or admitted by the user (S2 authority model); transparent derivation; no "suitable for you" framing (A4, A11) | Gated: unresolved dependency at S11/S14; not removed |
| Recommendations (application-originated, A) | A3–A5: if made to a client by a provider, investment advice | Whether any A-type output is intended | If intended: regulatory status must be resolved first | Gated: RQ-49 must be resolved for this capability before enablement |
| Portfolio optimisation (method) | Computation; regulatory relevance arises only through presentation and use | As target portfolios | As target portfolios | As target portfolios |
| Trade lists | A4 (transactions in particular instruments) if a recommendation | As target portfolios | User confirmation (ADR-0017 grant 5); derivation from the user's target and rules | Gated with target portfolios (S13e/S14) |
| Order staging | Not addressed directly | Whether staging inside the user's own environment is reception of orders by anyone | User-held broker credentials; local execution path | Gated: S13 safeguards (ADR-0017); regulatory note at S13f |
| User-confirmed execution | A12: execution/transmission is a service when **on behalf of clients** | Whether a locally run tool submitting the user's own orders via the user's own broker credentials acts "on behalf of" anyone | Local execution with user-held credentials; per-order confirmation; broker performs execution | Gated: S13 safeguards and broker API facts (RQ-19); RQ-49 note at S13f |
| Rule-based automated execution | A12 (discretion for a client) | Whether user-authored rules executed automatically constitute discretion exercised for anyone | Authority grants scoped, limited, revocable (ADR-0017); S13 safeguards | Gated: S13 safeguards; RQ-49 resolution for distributed builds |
| Unattended execution | Not addressed directly | As above, plus operational-risk safeguards | Grant 8 (ADR-0017); S13 safeguards; monitoring (S16) | Gated: S13 safeguards and S16 monitoring; RQ-49 resolution for distributed builds |

**What this does and does not do:**
- No capability is removed from the architecture, and the S2 authority model is unchanged.
- No universal requirement for legal review is created.
- Where RQ-49 is a genuine dependency (application-originated recommendations; and the posture for distributing execution and target-portfolio capabilities), the capability is gated until that dependency is resolved.
- The owner may later choose professional legal review as a project-governance safeguard. It is not adopted here.

## 7. Nordnet registry summary (Norwegian retail, as of 2026-10-01)

| Attribute | Finding | Source | Level | Status |
|---|---|---|---|---|
| Legal entity / supervision | Nordnet Bank NUF, branch of Nordnet Bank AB; Finansinspektionen and Finanstilsynet | nordnet.no "Sikkerhet og garanti" | V-full | verified |
| Deposit guarantee / investor protection | NOK 2,000,000 / SEK 250,000 | Same | V-full | verified |
| Custody | Norwegian securities on customer's VPS account; foreign securities with custodians in Nordnet's name | Same | V-full | verified |
| Account types (non-pension) | ASK; Aksje- og fondskonto | nordnet.no | V-abs | verified (summary) |
| Commissions (Nordic; US/other), FX, fund platform fees, margin 7.34%/7.59% | As recorded | nordnet.no price list | V-full | verified |
| Short selling | Aksje- og fondskonto only; tests required | nordnet.no FAQ | V-abs | verified (summary) |
| Complex-product tests | Required | nordnet.no | V-abs | verified (summary) |
| API | Closed for new subscriptions; **no reopening date announced** (verified absence, not unknown) | nordnet.se FAQ | V-full | verified |
| Tax reporting | VPS: Norwegian funds and Oslo Børs shares; Nordnet: foreign securities, ETFs, dividends; self-reported: derivatives | nordnet.no | V-full | verified (wealth-value reporting omitted, ADR-0021) |
| Fractional shares; order types | — | — | — | unavailable (unknown) |

## 8. eToro registry summary (EEA retail, as of 2026-10-01)

| Attribute | Finding | Level | Status |
|---|---|---|---|
| Entity | eToro (Europe) Ltd, CySEC 109/10 | V-full | verified |
| Entity for Norwegian residents | eToro (Europe) Ltd expected | — | interpretation |
| Investor compensation | ICF €20,000; EEA deposit guarantee €100,000; crypto not covered | V-full / V-abs | verified |
| Ownership model | Unleveraged buys = real assets (omnibus); short/leveraged = CFDs | V-abs | verified (summary) |
| Commissions | Stocks $1/$2 rule (verified); **Norway amount: separate unknown record**; ETFs 0; stock CFDs 0.15% | V-full | verified / unknown |
| NOK conversion; withdrawal fee | As recorded | V-full | verified |
| Inactivity fee | **Unresolved conflict** (below) | — | unresolved_conflicting |
| ASK | — | — | unknown (not "not offered") |
| API | Personal keys, own account, beta (verified, V-abs); **regional eligibility: separate unknown record** | V-abs | verified / unknown |
| Tax report for Norwegian residents | Provided (V-abs); **direct reporting to Skatteetaten: separate unknown record** | V-abs | verified / unknown |
| Withholding practice; appropriateness; fractional shares | — | — | unknown |

**Inactivity-fee conflict, second attempt (2026-10-01):**

| Candidate cause | Evidence | Assessment |
|---|---|---|
| Legal entity / jurisdiction | Fee page footer lists several eToro entities and states no applicable entity; it reads "Inactivity fee: Free" | Possible; not established |
| Account type | No account-type distinction found on either source | Not supported by evidence |
| eToro Club status | Fee page: Club members may get discounts or exemptions, but "Free" is stated without condition | Does not explain "Free" vs. $10 |
| Effective date / stale documentation | The help article that carried the $10 claim now renders no body text (checked in a browser). Broker-review sites (secondary, leads only) report removal of the $10 fee during 2026, at least for UK clients | Most consistent with the leads, but not established from authoritative current material |

**Result:** not resolved. Both records are preserved as linked
`unresolved_conflicting` facts; neither is chosen (FX3-11).

## 9. Unknown vs. verified-unsupported — audit

Rule: **absence of evidence that a broker supports a feature is not
evidence that it does not.**
- A capability is recorded as *not offered* only where a source states it, e.g. Nordnet short selling not on ASK, Nordnet API closed to new subscriptions, eToro ICF not covering crypto.
- Everything else without evidence is `unavailable` (unknown).

**Audit of both broker registries:**
- Every `false` or negative value cites a source statement.
- Three eToro records previously labelled `verified` while hiding null sub-values were split into separate unknown records: the Norway commission amount, API regional eligibility, and direct reporting to Skatteetaten.
- Nordnet's "reopening date: null" was re-expressed as a verified absence of an announced date.
- A naming collision between verification status `unavailable` (unknown) and the broker admissibility value "unavailable" (not offered) was fixed: the broker layer now uses `offered · not_offered · unknown` (architecture §4).

## 10. Unresolved items, classified by consequence

**Classes:**
- **A** — non-blocking.
- **B** — capability-gating, with the capability gated and the stage by which it must be resolved.
- **C** — G3-blocking.

| # | Item | Class | If B: question → capability gated → resolve by |
|---|---|---|---|
| U1 | Shielding rate 2026 | B | 2026 rate → after-tax projections and tax-aware calculations for income year 2026 → S13a (record on publication, Jan 2027) |
| U2 | 2027 tax parameters | B | 2027 parameters → tax calculations for 2027 → S13a (record on publication) |
| U3 | NOU 2026:9 | — | **Withdrawn:** wealth tax out of scope (ADR-0021) |
| U4a | ASK credit: calculation and limit inside ASK | B | Calculation → after-tax return modelling of foreign dividends in ASK, and ASK vs. ordinary-account comparison illustrations that include credit → S13a |
| U4b | ASK: tracking of withheld tax | B | Tracking → per-account tax reporting aids for ASK → S13a (and S14 report) |
| U4c | ASK: input-value interaction with credit | B | Interaction → ASK after-tax modelling → S13a |
| U4d | ASK: carry-forward across dividend-year/withdrawal-year gap | B | Timing → multi-year ASK tax projections → S13a |
| U4e | ASK: broker information for credit | B | Broker information → per-broker tax-reporting support claims in the comparison → S13a |
| U5 | Fund-level withholding (RQ-51) | B | W9 → after-tax expected-return inputs for funds/ETFs → S6 (instrument attributes) / S13a |
| U6 | US reclaim mechanism (W6) | A | — |
| U7 | Verbatim MiFID II Art. 4(1)(1), 25(3)–(4); Del. Reg. 2017/565 Art. 9 | A | (re-read before any reliance; no G3 decision depends on the exact wording) |
| U7b | PRIIPs consolidated amendments vs. articles read | A | — |
| U7c | EU application dates (MiFID II, PRIIPs) | A | — |
| U8 | ESMA appropriateness guidelines; Norwegian supplementary regulation ch. 6 §3 | A | — |
| U9 | Per-instrument Norwegian KID availability (US ETFs) | B | KID availability → legal admissibility layer for third-country funds in the universe → S5/S6 (instrument attribute `kid_available_no`) |
| U9b | AIF-law marketing barrier for non-UCITS funds | B | → same capability → S5/S6 |
| U10 | eToro: Norway commission, entity applicability, ASK, withholding, appropriateness, API eligibility, direct reporting, inactivity conflict | B | eToro facts → feasibility, cost illustration, and execution for eToro configurations → S5 (availability), S13a (costs), S13f (API/execution) |
| U11 | Nordnet: fractional shares, order types, exchange list; full reads of V-abs pages | B | → sizing/rounding and execution for Nordnet → S13e/S13f |
| U12 | Fund taxation rule start date | A | — (current rule verified; history needed only for long backtests → S7 note) |
| U13 | RQ-49 resolution | B | A vs. B and distribution posture → application-originated recommendations; distributed builds' target-portfolio, trade-list, and execution capabilities → S11/S14 (recommendation framing), S13f (execution) |
| U14 | CFD/binary national measures: current status on Lovdata | A | — |

**Class C: none.** No unresolved item undermines a fact or architectural
decision that G3 depends on. The corrected ASK finding (U4) was the one
candidate for C. It is resolved at the level G3 needs (applicability
verified); the open mechanics are B.
