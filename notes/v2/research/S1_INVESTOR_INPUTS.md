# S1 — Investor inputs required (intake specification)

**Document status:** DRAFT (S1) · **Stage:** S1 → gate G1 · **Resolves:** RQ-01 (inputs); RQ-02a (what to elicit)

This document lists the investor inputs S1 needs and the later decisions each
one affects. It contains **questions only — no answers**. Answers are personal
and financial data. Where they are stored is decision D-S1-1 (§0); they are
not committed to this public repository unless the owner decides otherwise.

Column key:
- **Cat.** — Policy Statement decision category (07 §3): 1 user parameter · 2 hard constraint · 3 soft target · 7 human-approval rule.
- **Need** — **G1** required to close S1 · **later** may be answered at the listed stage.

## 0. Prerequisite decision

**D-S1-1 — Where investor answers are stored.** The repository is public.
Options:
(a) a local, git-ignored file outside the repository, with only the schema in Git;
(b) make the repository private;
(c) commit coarse ranges only.
Recommendation: (a). The developer needs the schema, not the values.

## A. Jurisdiction and identity

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| A1 | Tax residence now, and any expected change within the horizon | Country; yes/no + when | 1 | G1 | Tax and wrapper registries (S3a); kildeskatt/treaty rules (RQ-04); wealth-tax treatment |
| A2 | Consumption/base currency now and for future spending | Currency (+ share of future spending in others) | 1 | G1 | Return translation; currency-hedging policy (RQ-07); benchmark currency |
| A3 | Life stage: age band, or years to key milestones | Band / years | 1 | G1 | Horizon and risk capacity (RQ-02); lifecycle allocation research (S1/S5) |

## B. Goals and liquidity

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| B1 | Each goal: purpose, target amount (today's NOK), target date, priority, flexibility (essential vs. aspirational) | Table | 1/3 | G1 | Number of Goal→Portfolio units (ADR-0006); horizon per portfolio (forecast horizon, ADR-0009); return target (soft); conflict ordering (RQ-23) |
| B2 | Planned withdrawals: amounts, dates, certainty | Schedule | 1/2 | G1 | Cash-buffer hard constraint; liquidity constraints; rebalancing (S13b) |
| B3 | Emergency buffer held *outside* the engine? | Yes/no + amount | 1 | G1 | Whether the engine must hold a liquidity reserve |

## C. Capital and cash flows

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| C1 | Investable capital per account (continuous) | NOK per account | 1 | G1 | Feasibility Engine: minimum-commission drag, minimum orders, fractional availability, diversification feasibility (ADR-0007); feasible universe size (S5); eligible methods (S4) |
| C2 | Planned contributions: amount, frequency, stability | NOK / period | 1 | G1 | Rebalancing through cash flows (S13b); lump-sum vs. phased entry; trade sizing (S13e) |
| C3 | Income stability and employment sector | Qualitative | 1 | G1 | Risk capacity (RQ-02); possible exclusion or underweighting of the employer/sector (S5) |

## D. Wealth context outside the engine

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| D1 | Other assets: home equity, employer pension/EPK, other savings, crypto, employer shares | Approx. NOK by type | 1 | G1 | Whether the engine optimises in isolation or relative to total wealth; concentration constraints; benchmark choice (S7) |
| D2 | Debt: mortgage and other loans, rates | NOK, % | 1 | G1 | Risk capacity; leverage policy; debt repayment as an opportunity-cost benchmark |

## E. Risk preference — elicitation inputs, not γ (RQ-02; ADR-0010)

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| E1 | Self-assessed category (Aggressive / Moderate / Conservative), recorded as given | Choice | 1 | G1 | Calibration-layer input (RQ-02); not mapped to γ at S1 |
| E2 | Largest one-year decline you would accept without changing the plan, in % **and** NOK | %, NOK | 1/3 | G1 | Soft drawdown target and monitoring trigger (07 §3); CRO thresholds (S12); calibration (S11) |
| E3 | What you would do at −10%, −20%, −35%: hold / sell some / sell all / buy more | Choice per level | 1 | G1 | Behavioural risk tolerance; trigger responses; realism of drawdown targets |
| E4 | Revealed behaviour: actions in past drawdowns (e.g. 2020, 2022), if invested | Free text | 1 | G1 | Cross-check of E1–E3 (stated vs. revealed) |
| E5 | Preferred volatility range, if you have one | % band or "no view" | 3 | G1 | Soft volatility band; calibration cross-check |
| E6 | Short choice battery (certainty-equivalent / lottery items) | Answers | 1 | later (S2) | Model-consistent calibration (RQ-02c/d); the instrument itself is designed in S2 |

## F. Accounts and current holdings

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| F1 | Existing accounts: broker (Nordnet / eToro / other), wrapper (e.g. ASK, ordinary account), currency(ies), value | List | 1 | G1 | Scope of registry research (S3); account configuration (G3); asset location (S13a) |
| F2 | Current holdings per account, with cost basis and purchase date for taxable accounts | Holdings list | 1 | later (S3/S13) | Transition plan: realisation tax of moving to target; tax lots (ADR-0006) |
| F3 | Holdings to keep regardless (legacy, employer, sentimental) | List | 2 | G1 | Hard constraints; transition plan |
| F4 | Willingness to open new accounts or currency accounts | Yes/no/conditions | 1 | G1 | Option set at G3 |

## G. Universe and instrument preferences

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| G1 | Markets/regions wanted or refused; view on home bias | List / view | 1/2 | G1 | Feasible universe (S5, RQ-07); comparison universe (RQ-38) |
| G2 | Instruments permitted: single stocks, ETFs, funds, bonds, leveraged products, CFDs, options, short selling, crypto | Allow/deny each | 2 | G1 | Hard constraints; method eligibility (S4); regulatory checks (S3c) |
| G3 | Exclusions: ethical, sector, issuer | List | 2 | G1 | Universe filters; comparison-universe question (RQ-38) |
| G4 | Do you want security selection at all, or asset-class allocation only? | Preference + strength | 1 | G1 | Allocation unit (S5, RQ-07); whether cross-sectional stock scoring (S9c) is in scope |

## H. Implementation and engagement

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| H1 | Time available per month; maximum acceptable trading frequency (execution is manual unless decided otherwise) | Hours; trades/month | 1/2 | G1 | Rebalancing cadence (S13b); tactical-layer feasibility (S13c); trade-count limits |
| H2 | Autonomy: what the engine may decide without asking; what always needs approval | Choices | 7 | later (S2) | Approval matrix (S2) |
| H3 | Reporting: frequency and depth of the investment-case report | Choice | 1 | later (S14) | Report specification (S14) |

## I. Tax position (optional, sensitive)

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| I1 | Wealth-tax position (above/below threshold), other realised gains/losses this year | Bands | 1 | later (S3/S13a) | Value of tax-aware rebalancing and asset location |

## J. Experience, constraints, benchmark

| # | Input | Format | Cat. | Need | Affects |
|---|---|---|---|---|---|
| J1 | Investment experience; completed broker knowledge tests for complex products | Text / yes-no | 2 | G1 | Gating of complex instruments (S3c, S4) |
| J2 | External trading restrictions (employer policy, insider lists) | Yes/no + detail | 2 | G1 | Hard constraints on universe and timing |
| J3 | What you would naturally compare your results against | Free text | 1 | G1 | Candidate benchmark set (S7, RQ-09) — candidate only |

## Minimum set to close G1

A1–A3, B1–B3, C1–C3, D1–D2, E1–E5, F1, F3, F4, G1–G4, H1, J1–J3.
