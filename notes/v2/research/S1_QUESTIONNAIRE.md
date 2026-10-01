# S1 — Investor Profile questionnaire (public template)

**Document status:** DRAFT (S1) · **Stage:** S1 → gate G1 · **Basis:** ADR-0014 (proposed), ADR-0010 · **Resolves:** RQ-01 (inputs), RQ-02a (what to elicit)

**This is a public template for any local user. It contains questions only.**
Answers are personal and are stored only in the user's git-ignored local
workspace (`local/profiles/<profile-id>/`). They are never committed, never
used as system defaults, and never translated into model parameters at S1.

## Conventions

**Nature** (ADR-0014 §4):
- **F** — factual investor input: an objective user-specific fact.
- **P** — user preference: the user is entitled to choose it.
- **R** — preliminary / research-dependent: the user states it now, but the options or the implementation depend on later research (stage shown).

**Interface type:** dropdown · multi-select · numeric · range · toggle · table (repeating rows) · free text · system-derived (read-only, shown later).

**Need:** **G1** = needed to close S1 · **later (Sx)** = may be answered at stage Sx.

**Necessity:** **Req** = required to form an Effective Policy Statement · **Opt** = improves decisions; the engine works without it.

**Purpose limitation (ADR-0014 §8):** the last column lists each field's decision purpose and its *exhaustive* permitted consumers. Any other use requires a schema change recorded in an ADR. No personal field feeds market beliefs or signals.

**Always available on every question:** "Don't know" and "Prefer not to say".
No option is pre-selected. Listed options are not defaults. Unanswered means
unanswered — the engine infers nothing.

---

## Section 1 — Jurisdiction, identity, experience

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 1.1 | In which country are you tax-resident? | F | dropdown (registry-driven) | Norway · Other (specify) | G1 | Req | Tax and wrapper rules (S3a); unsupported-jurisdiction handling (RQ-42) |
| 1.2 | Do you expect your tax residence to change within your investment horizon? | F | toggle + numeric + dropdown | Yes / No; if yes: approx. year, country | G1 | Req | Tax-rule time-variation; wrapper suitability |
| 1.3 | Year of birth (or age band) | F | numeric / dropdown | Year, or band (<30, 30–39, 40–49, 50–59, 60+) | G1 | Opt | Horizon and goal validation; human-capital and risk-capacity research (RQ-02, S5). **Never** a signal or a belief input (ADR-0014 §8) |
| 1.4 | In which currencies do you consume, and hold or expect liabilities, now and in future? (Not the currencies of investments — FX exposure of holdings is handled separately) | F | multi-select + numeric | Currency + approx. % share each | G1 | Req | Definition of currency risk relative to consumption/liabilities; hedging research (RQ-07) |
| 1.5 | In which currency should the engine report results? | P | dropdown | NOK · EUR · USD · Other | G1 | Req | Reporting and benchmark currency |
| 1.6 | Are you subject to external trading restrictions (employer policy, insider lists, professional rules)? | F | toggle + free text | Yes / No; details | G1 | Req | Hard constraints on universe and timing |
| 1.7 | Which instruments have you invested in before? | F | multi-select | None · Mutual funds · ETFs · Individual stocks · Bonds · Leveraged products · CFDs · Options/futures · Crypto · Other | G1 | Req | Gating of complex products (S3c, S4); report depth |
| 1.8 | Have you completed a broker knowledge/appropriateness test for complex products? | F | table | Broker · product type · yes/no/don't know | G1 | Opt | Whether complex instruments are feasible (S3c) |

## Section 2 — Goals and horizons

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 2.1 | List your investment goals | P | table | Per goal: name (free text) · purpose (dropdown: retirement, home purchase, education, wealth building, income, other) · target amount in today's NOK (numeric or "no specific amount") · target year or horizon in years · priority rank · flexibility (dropdown: essential / important / aspirational) | G1 | Req | Goal→Portfolio units (ADR-0006); horizon per portfolio (forecast horizon, ADR-0009); soft return targets; conflict ordering (RQ-23) |
| 2.2 | For each goal, how will the money be used? | P | dropdown per goal | Lump sum at target date · Gradual withdrawals (state period) · No planned use | G1 | Req | Liquidity profile; glide-path research (S5) |
| 2.3 | Should separate goals be managed as separate portfolios, or combined? | R (S2/S5) | dropdown | Separate · Combined · No view | G1 | Opt | Number of portfolios; multi-goal research |

## Section 3 — Liquidity

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 3.1 | Planned withdrawals from the invested money | F | table | Amount (NOK) · year · certainty (certain / likely / possible) | G1 | Req | Cash-buffer hard constraint; rebalancing (S13b) |
| 3.2 | Do you hold an emergency buffer *outside* the accounts the engine manages? | F | toggle + numeric | Yes / No; size in months of expenses | G1 | Req | Whether the engine must hold a reserve |
| 3.3 | Should the engine itself keep a cash reserve? | P | toggle + numeric | Yes / No; % or NOK | G1 | Req | Minimum-cash constraint |
| 3.4 | If something unexpected happened, how quickly might you need access to part of the money? | F | dropdown | Within days · weeks · months · not within a year | G1 | Req | Liquidity constraints; instrument eligibility |

## Section 4 — Capital and cash flows

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 4.1 | Total capital you intend the engine to manage now | F | numeric | NOK (per-account split in 6.1) | G1 | Req | Feasibility Engine: commission drag, minimum orders, diversification (ADR-0007); universe size (S5) |
| 4.2 | Planned contributions | F | numeric + dropdown | Amount (NOK) · frequency (monthly / quarterly / yearly / irregular) · reliability (fixed / likely / uncertain) | G1 | Req | Rebalancing via cash flows; trade sizing (S13) |
| 4.3 | How stable is your income? | F | dropdown | Very stable · Fairly stable · Variable · No earned income | G1 | Opt | Risk capacity (RQ-02) |
| 4.4 | In which sector do you work, and is your employer listed? | F | dropdown + toggle + free text | Sector list · listed yes/no · name (optional) | G1 | Opt | Human-capital concentration; possible underweight (S5) |

## Section 5 — Wealth outside the engine, and debt

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 5.1 | Other assets not managed by the engine | F | table | Type (home equity · employer pension · other pension · bank savings · other investments · crypto · employer shares · other) · approx. NOK or band | G1 | Opt | Total-wealth context; concentration limits |
| 5.2 | Debts | F | table | Type · balance (NOK or band) · interest rate · fixed/floating | G1 | Opt | Risk capacity; leverage policy; debt repayment as opportunity cost |
| 5.3 | Should the engine consider your total wealth, or only the accounts it manages? | R (S5/S7) | dropdown | Managed accounts only · Consider total wealth · No view | G1 | Opt | Optimisation scope; benchmark (S7) |

## Section 6 — Accounts and holdings

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 6.1 | Accounts you hold or plan to use | F | table | Broker (Nordnet · eToro · Other) · account type (e.g. ASK, ordinary account, other — list finalised from S3a) · currency · approx. value (NOK) · planned / existing | G1 | Req | Registry scope (S3); account configuration (G3); asset location (S13a) |
| 6.2 | Holdings you want to keep regardless of recommendations | P | table | Instrument · account · reason (optional) | G1 | Opt | Hard constraints; transition plan |
| 6.3 | Are you willing to open new accounts if analysis shows a benefit? | P | dropdown + free text | Yes · Only with a clear benefit · No | G1 | Opt | Option set at G3 |
| 6.4 | Are you willing to use currency accounts at a broker? | P | toggle | Yes / No | G1 | Opt | FX-cost options (S3b) |
| 6.5 | Detailed holdings: instrument, quantity, cost basis, purchase date | F | table / file import | — | later (S3/S13) | Opt | Tax lots; transition costs |

## Section 7 — Risk preference (stored exactly as given; no γ is derived)

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 7.1 | How would you describe your risk preference? | P | dropdown (+ advanced) | Conservative · Moderate · Aggressive · Custom (describe) | G1 | Req | Raw input to the calibration layer (RQ-02); model parameters system-derived later with a derivation record (ADR-0014 §6) |
| 7.2 | Largest decline over one year you could accept without changing your plan | P | numeric (% and NOK) | % of portfolio and NOK | G1 | Req | Soft drawdown target and monitoring trigger; CRO thresholds; calibration |
| 7.3 | What would you most likely do if your portfolio fell by 10% / 20% / 35%? | P | dropdown per level | Buy more · Hold · Sell some · Sell all | G1 | Req | Behavioural tolerance; realism of the drawdown target; trigger responses |
| 7.4 | What did you actually do in past market declines (e.g. 2020, 2022), if invested? | F | dropdown + free text | Not invested · Bought more · Held · Sold some · Sold all | G1 | Opt | Stated vs. revealed preference cross-check |
| 7.5 | Do you have a preferred range for year-to-year fluctuation? | P | range or toggle | Low–high % per year, or "no view" | G1 | Opt | Soft volatility band; calibration cross-check |
| 7.6 | Short set of choice questions (certainty-equivalent / lottery items) | P | system-presented battery | Designed in S2 | later (S2) | Opt | Model-consistent calibration (RQ-02c/d) |

## Section 8 — Universe and instruments

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 8.1 | Markets/regions you want included | R (S3/S5) | multi-select | Norway · Nordics · Europe · USA · Other developed · Emerging · Global/no preference | G1 | Req | Feasible universe (S5, RQ-07); comparison universe (RQ-38) |
| 8.2 | Markets/regions you want excluded | P | multi-select | Same list + free text | G1 | Opt | Universe filters |
| 8.3 | View on overweighting Norway relative to its global market share | P | dropdown | Prefer overweight · Neutral · Prefer underweight · No view | G1 | Opt | Home-bias research input (S5) |
| 8.4 | Which instruments may the engine use? | R (S3c/S4) | matrix: allow / deny / undecided | Individual stocks · ETFs · Mutual funds · Bonds / bond funds · Leveraged products · CFDs · Options · Futures · Short selling · Crypto | G1 | Req | Hard constraints; method eligibility; regulatory feasibility |
| 8.5 | Leverage | R (S3/S4) | dropdown (+ advanced numeric) | No leverage · Limited (state maximum) · Permitted | G1 | Req | Constraint set; financing costs; eligibility |
| 8.6 | Exclusions (ethical, sector, specific companies) | P | multi-select + free text | Weapons · Tobacco · Fossil fuels · Gambling · Other (specify) | G1 | Opt | Universe filters; comparison-universe question (RQ-38) |
| 8.7 | Do you want the engine to select individual securities, or allocate across asset classes/funds only? | R (S5) | dropdown + strength | Individual securities · Asset classes/funds only · Both · No view; strength: strong / mild | G1 | Req | Allocation unit (RQ-07); scope of cross-sectional scoring (S9c) |
| 8.8 | Currency-hedging preference for foreign investments | R (S5, RQ-07) | dropdown | Unhedged · Partly hedged · Hedged · No view | G1 | Opt | Currency policy |

## Section 9 — Engagement and implementation

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 9.1 | Hours per month you are willing to spend on the portfolio | F | numeric | Hours | G1 | Req | Rebalancing cadence; tactical-layer feasibility (S13c) |
| 9.2 | Maximum number of trades per month you are willing to place yourself | P | numeric | Trades | G1 | Req | Trade-count limits; execution design (S13f) |
| 9.3 | How often do you want to review recommendations? | P | dropdown | Weekly · Monthly · Quarterly · Only when action is needed | G1 | Req | Run cadence; report scheduling |
| 9.4 | What may the engine decide without asking you? | R (S2) | dropdown + free text | Nothing (approve everything) · Small rebalancing only · Within agreed limits · Other | later (S2) | Opt | Approval matrix |
| 9.5 | Preferred report depth | P | dropdown | Short summary · Standard · Full detail | later (S14) | Opt | Report specification |

## Section 10 — Tax position (optional) and comparison

| ID | Question | Nature | Interface | Options / format | Need | Necessity | Purpose → permitted consumers (exhaustive) |
|---|---|---|---|---|---|---|---|
| 10.1 | Wealth-tax position | F | dropdown (optional) | Below threshold · Above threshold · Don't know | later (S3/S13a) | Opt | Value of tax-aware decisions |
| 10.2 | Realised gains/losses this tax year (band) | F | dropdown (optional) | Bands | later (S13a) | Opt | Tax-aware rebalancing |
| 10.3 | What would you naturally compare your results against? | R (S7) | free text | — | G1 | Opt | Candidate benchmark set (RQ-09) |

## Minimum set to close G1

Sections 1–5; 6.1–6.4; 7.1–7.5; Section 8; 9.1–9.3; 10.3.
