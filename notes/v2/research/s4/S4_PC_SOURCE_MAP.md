# S4.4 — PC method source map (final S4_PLAN §D)

**Document status:** DRAFT for owner review (S4.4; exit = "every PC method at SOURCE LOCATED or a documented acquisition gap") · **Prepared:** 2026-10-08 · **Entry:** S4.3 reviewed (`S4_TAXONOMY.md`) · **Basis:**
- S4_PLAN §D (draft map, verified against ANG v2 Exhibit 3, p. 11) and §D.1 (candidate additions);
- `S4_0_SOURCE_INVENTORY.md` §1–§3 and §9; `S4_0_ACQUISITION_CHECKLIST.md`;
- `ANG_ISSUES_REGISTER.md` (method-specific issues);
- owner decisions D-2 (Michaud IP check before implementation), D-3 (open working versions accepted; the published version governs), D-4 (downloads need per-item permission), D-5 (AQR as TPA weight-specification source).

**What this step does:**
- fixes, for every roster method, the **governing primary source**, supporting sources and the access route;
- sets each method's status to **SOURCE LOCATED** or records a **documented acquisition gap**, with the owner action that closes it;
- lists the **ANG-vs-source differences** known before the mathematics is read.

**What it does not do:** read or extract mathematics (S4.5–S4.14), download anything (D-4), or change the roster.

**Status terms used here:**
- **LOCATED · in hand**: identity-confirmed local copy (S4.0 AVAILABLE).
- **LOCATED · open**: an open working or author version exists at a known address; not yet downloaded. Under D-3 it is usable once downloaded, with the published version governing.
- **LOCATED · paywalled/book**: the published version is identified; access needs BI library access or a purchase.
- **GAP**: the governing source is not reliably identified, or its identity is unconfirmed.

**Local check, 2026-10-08:** the research folders and Downloads were searched again for every missing primary (by file name and date). **Nothing new was found** for the roster. One unlisted local file is relevant to PC-D4: a BI course note, B. Gerard, *Constructing an Optimal Active Portfolio & the Optimal Active Share in an Overall Portfolio* (GRA 6531, 13 Jan 2026, 8 pp., md5 `7295450f59a2`). It is SECONDARY teaching material on Treynor–Black-type active sizing.

---

## 1. Source map (roster v0; S4.3 types)

Roster v0 has 22 methods (type M.PC) and one role, PC-E1 Researcher (`S4_TAXONOMY.md` F-1).

| ID | Method (ANG name) | ANG-cited source (Exh. 3) | Governing primary | Supporting sources | Access status | S4.4 status | Extraction step |
|---|---|---|---|---|---|---|---|
| PC-A1 | Equal weight | DeMiguel, Garlappi & Uppal 2009 | DGU 2009, *RFS* 22(5) | — | In hand | **SOURCE LOCATED** | S4.5 |
| PC-A2 | Market-cap weight | Sharpe 1964 | Sharpe 1964, *JF* 19(3) | Asset-class capitalisation data (S6) | In hand | **SOURCE LOCATED** | S4.5 |
| PC-A3 | Inverse volatility | Kirby & Ostdiek 2012 | Kirby & Ostdiek 2012, *JFQA* 47(2):437–467 | — | Paywalled; author research page may hold a copy | **SOURCE LOCATED** (acquisition needed) | S4.5 |
| PC-A4 | Inverse variance | Kirby & Ostdiek 2012 | Same | — | Same | **SOURCE LOCATED** (acquisition needed) | S4.5 |
| PC-A5 | Volatility targeting | Moreira & Muir 2017 | Moreira & Muir 2017, *JF* 72(4) | — | In hand | **SOURCE LOCATED** | S4.5 |
| PC-B1 | Maximum Sharpe ratio | Markowitz 1952 | Markowitz 1952; Tobin 1958; Sharpe 1964 | Michaud 1989; Jorion 1986 (estimation error) | In hand | **SOURCE LOCATED** | S4.6 |
| PC-B2 | Black–Litterman | Black & Litterman 1992 | BL 1992, *FAJ* 48(5) | He & Litterman 1999 (open, SSRN 334304); Idzorek 2005 (open, SSRN) | Primary in hand; supporting open | **SOURCE LOCATED** | S4.7 |
| PC-B3 | Robust mean–variance | Goldfarb & Iyengar 2003 | G&I 2003, *Math. Oper. Res.* 28(1):1–38 | Tütüncü & Koenig 2004; Ceria & Stubbs 2006 (paywalled) | Paywalled | **SOURCE LOCATED** (acquisition needed) | S4.7 |
| PC-B4 | Resampled efficient frontier | Michaud 1998 | Michaud 1998, *Efficient Asset Management* (book; 2nd ed. 2008) | Michaud 1989 (in hand); Michaud & Michaud author note (open, identity unconfirmed); Scherer 2002 critique (paywalled); US patent 6,003,018 | Book (purchase) | **SOURCE LOCATED** (acquisition needed; IP check before implementation, D-2) | S4.7 |
| PC-B5 | Mean–downside risk (Sortino) | Sortino & van der Meer 1991 | S&vdM 1991, *JPM* 17(4):27–31 | Estrada (mean–semivariance heuristic); Markowitz, Todd, Xu & Yamane 1993; semicovariance/LPM paper; Hogan & Warren 1974 (all in hand) | In hand (scan; no text layer, read from page images) | **SOURCE LOCATED** | S4.5 / S4.12 |
| PC-B6 | Simple EPO | (not in ANG) | Pedersen, Babu & Levine 2021, *FAJ* 77(2):124–151 | Author version (49 pp., in hand); author code (not yet searched) | In hand | **SOURCE LOCATED** | S4.7 |
| PC-B7 | Anchored EPO | (not in ANG) | Same | Same | In hand | **SOURCE LOCATED** | S4.7, S4.10 |
| PC-C1 | Global minimum variance | Clarke, de Silva & Thorley 2006 | CdST 2006, *JPM* 33(1):10–24 | Markowitz 1952; Jagannathan & Ma 2003 (abstract verified 2026-10-08; full text missing) | Paywalled; author-affiliated page (identity unconfirmed until retrieved) | **SOURCE LOCATED** (acquisition needed) | S4.11 |
| PC-C2 | Risk parity (ERC) | Maillard, Roncalli & Teïletche 2010 | MRT 2010, *JPM* 36(4):60–70 | Spinu 2013 (algorithm; open, SSRN 2297383) | Open working version (SSRN 1271972) | **SOURCE LOCATED** | S4.11 |
| PC-C3 | Hierarchical risk parity | López de Prado 2016 | LdP 2016, *JPM* 42(4):59–69 | — | Open working version (SSRN 2708678) | **SOURCE LOCATED** | S4.11 |
| PC-C4 | Maximum diversification | Choueifaty & Coignard 2008 | C&C 2008, *JPM* 35(1):40–51 | Choueifaty, Froidure & Reynier 2013 (not located) | Paywalled | **SOURCE LOCATED** (acquisition needed) | S4.11 |
| PC-C5 | Minimum correlation | Varadi et al. 2012 | Varadi, Kapler, Bee & Rittenhouse 2012 (CSS Analytics working paper) | — | Third-party mirror only; original host not found | **GAP (identity)**: the source is a working paper with no published version, and the only copy found is a mirror | S4.11 |
| PC-D1 | CVaR optimisation | Rockafellar & Uryasev 2000 | R&U 2000, *J. Risk* 2(3):21–41 | R&U 2002, *JBF* (not located) | Paywalled; author copies likely | **SOURCE LOCATED** (acquisition needed) | S4.12 |
| PC-D2 | Maximum drawdown-constrained | Chekhlov, Uryasev & Zabarankin 2005 | CUZ 2005, *IJTAF* 8(1):13–58 | Earlier version "Portfolio Optimization with Drawdown Constraints" (identity unconfirmed) | Open working version (SSRN 544742) | **SOURCE LOCATED** | S4.12 |
| PC-D3 | Tail-risk parity | Boudt, Carl & Peterson 2013 | BCP 2013, *J. Risk* 15(3):39–68 | Boudt, Peterson & Croux 2008 (modified ES; not located) | Open working version (SSRN 1885293) | **SOURCE LOCATED** | S4.12 |
| PC-D4 | TPA two-factor (equity, bonds) | Ang, Brandt & Denison 2014 (text also cites Gilmore & Simonian 2025) | **Concept:** ABD 2014 (in hand). **Weight mechanics:** AQR 2026 (in hand; D-5) with Treynor & Black 1973 as the primary for appraisal-ratio sizing | Gilmore & Simonian 2025, *JPM* 51(10) (paywalled); BI course note (Gerard 2026; local, SECONDARY) | Concept and specification lead in hand; Treynor & Black and Gilmore & Simonian paywalled | **SOURCE LOCATED** (Treynor & Black needed for the primary sizing mathematics) | S4.12 |
| PC-E2 | Adversarial diversifier | — (ANG §3.3 only) | ANG v2 §3.3, p. 10 | — | In hand | **SOURCE LOCATED** (ANG is the only source; formulation gaps, ANG-16) | S4.14 |
| PC-E1 | Researcher (role) | — | ANG v2 §3.3; example method: Bera & Park 2008, *Econometric Reviews* 27(4–6) | — | Bera & Park paywalled | Not a method (F-1); its example source is LOCATED · paywalled | S4.14 |

**Result:** 21 of 22 methods are **SOURCE LOCATED**. PC-C5 is a **documented acquisition gap** (identity).
- 10 have their governing primary in hand: A1, A2, A5, B1, B2, B5, B6, B7, E2, and D4 for the concept.
- 4 are open working versions awaiting a download permission: C2, C3, D2, D3.
- 7 need BI library access or a purchase: A3, A4, B3, B4, C1, C4, D1.

---

## 2. ANG-vs-source differences known before the mathematics is read

These come from ANG's own text and the issues register. **Everything else is checked when each source is read** (S4.5–S4.14). Nothing here is inferred from a source not yet in hand.

| Method(s) | Difference or gap | Ref | Resolved at |
|---|---|---|---|
| PC-A3, PC-A4 | ANG cites Kirby & Ostdiek for both 1/σ and 1/σ². KO's volatility-timing rule has a tuning exponent; how ANG's two heuristics map to it is unknown | ANG-13 | S4.5 |
| PC-A5 | Moreira & Muir scale one factor's exposure over time. ANG gives no base portfolio, target level or treatment of the residual (cash) for a cross-asset version | ANG-14 (H) | S4.5 |
| PC-B5 | Objective unclear: maximise the Sortino ratio, a mean–semivariance frontier portfolio, or minimise downside deviation subject to a return floor | ANG-18 (H) | S4.5 / S4.12 |
| PC-B1 … B5, PC-C1 … C5, PC-D1 … D3 | ANG says PC agents take only CMAs and Σ. Several methods need more: capitalisations (A2), scenarios or paths (D1–D3), factor exposures (D4) | ANG-17 (H); handled by heterogeneous contracts (ADR-0024 §6) | S4.20 |
| PC-C1 | Named "Global min vol" in Exh. 4 and "Global minimum variance" in Exh. 3: the same portfolio (argmin σ = argmin σ² under the same constraints) | ANG-07 (L) | Recorded |
| PC-D1 | "CVaR optimization" (Exh. 3) vs "CVaR minimization" (Exh. 7–8): min-CVaR, mean–CVaR frontier, or maximum return subject to a CVaR limit | ANG-02 (H) | S4.12 |
| PC-D2 | Maximum drawdown vs conditional drawdown-at-risk formulation; which one ANG uses is not stated (to be settled from the source) | S4_PLAN §D note | S4.12 |
| PC-D4 | ABD 2014's TPA is a **funding and benchmarking** framework with no weight-producing rule (ABD-5). ANG gives no formulation (ANG-15). Two cited sources (ANG-22). Naming varies: "Approach" vs "Allocation" (ANG-06) | ABD-5; ANG-06, -15, -22 | S4.12 (own TPA-family candidate; amendment 14) |
| PC-E2 | Budget, bounds, which Sharpe ratio, risk-free rate, and solving a maximisation of a convex function (non-convex) are all unspecified | ANG-16 (H) | S4.14 |
| PC-E1 example | ANG describes maximum entropy as Shannon entropy of the weights with a Sharpe floor. Bera & Park (publisher record) use cross-entropy with side conditions from resampled moments | ANG-10 | S4.14 |
| Category sizes | ANG p. 9: "four to six methods per category"; Exh. 3 has 5 / 5 / 5 / 4 plus 2 agentic; no category has six | ANG-35 (L) | **Recorded here: loose wording; no method missing from Exh. 3 relative to the text** |

---

## 3. Candidate additions (S4_PLAN §D.1): source status

These are not roster methods; they are research-lane candidates (ADR-0024 §1). They are listed so that the source status is known if the owner admits one.

| Candidate | Primary source | Status |
|---|---|---|
| Maximum entropy | Bera & Park 2008 | Paywalled |
| Benchmark-relative MVO / minimum tracking error | Standard (no single primary named yet) | To identify if pursued |
| Norm-constrained MVO | DeMiguel, Garlappi, Nogales & Uppal 2009, *Mgmt Sci* 55(5) | In hand |
| Growth-optimal / Kelly | Not yet identified | To identify if pursued |
| General risk budgeting | Not yet identified (MRT 2010 covers the equal-budget case) | To identify if pursued |
| Effective-bets diversification | Meucci 2009, *Risk* 22(5):74–79 | Open (SSRN 1358533); also needed for the CRO/CIO diagnostic (ANG-11) |
| Signal-conditioned heuristics | Only if S4.9 shows a distinct, literature-supported construction | — |

---

## 4. Acquisition plan (owner actions; nothing downloaded)

Ordered by when each step needs its sources.

| # | Needed by | Items | Route | Owner action |
|---|---|---|---|---|
| 1 | S4.5 | Kirby & Ostdiek 2012 | BI library (JFQA) or the author page | Retrieve or permit download |
| 2 | S4.7 | Goldfarb & Iyengar 2003; Tütüncü & Koenig 2004; Ceria & Stubbs 2006; Scherer 2002 | BI library | Retrieve |
| 3 | S4.7 | He & Litterman 1999; Idzorek 2005 | Open (SSRN) | Permit download (per item, D-4) |
| 4 | S4.7 | Michaud 1998 (book) | Purchase; or proceed on Michaud 1989 (in hand) plus the author note and Scherer 2002, with the IP check before implementation (D-2) | Decide |
| 5 | S4.7 | PBL author code or supplement | Author pages (browsing only) | None: I can search it |
| 6 | S4.11 | MRT 2010; Spinu 2013; López de Prado 2016 | Open (SSRN) | Permit download |
| 7 | S4.11 | Clarke, de Silva & Thorley 2006; Choueifaty & Coignard 2008; Choueifaty, Froidure & Reynier 2013; Jagannathan & Ma 2003 | BI library | Retrieve |
| 8 | S4.11 | Varadi et al. 2012 | Original host unknown | Decide: accept the mirror as a working source labelled IDENTITY UNCONFIRMED, or treat PC-C5 as specified from its algorithm description only |
| 9 | S4.12 | CUZ 2005; Boudt, Carl & Peterson 2013 | Open (SSRN) | Permit download |
| 10 | S4.12 | Rockafellar & Uryasev 2000 and 2002; Boudt, Peterson & Croux 2008; Treynor & Black 1973; Gilmore & Simonian 2025 | BI library / JSTOR | Retrieve |
| 11 | S4.14 | Bera & Park 2008 | BI library | Retrieve |

**Rule for working versions (D-3):** where only a working version is read, the published version governs. Any difference found later is recorded against the method.

---

## 5. Exit check

| Criterion (S4_PLAN §G row S4.4) | Status |
|---|---|
| Final §D with sources per method | §1 (supersedes the draft §D's source columns; §D stays as history) |
| ANG-vs-source differences listed | §2 (known now); the rest at each extraction step |
| Every PC method at SOURCE LOCATED or a documented acquisition gap | 21 SOURCE LOCATED; PC-C5 documented gap (identity) |
| ANG-35 disposition | Recorded (§2) |
