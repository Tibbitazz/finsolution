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
| PC-A3 | Inverse volatility | Kirby & Ostdiek 2012 | Kirby & Ostdiek 2012, *JFQA* 47(2):437–467 | — | **In hand: working version** (9 May 2010, 43 pp., md5 `8da209076a0e`; owner upload 2026-10-08). Published version governs (D-3) | **SOURCE LOCATED** | S4.5 |
| PC-A4 | Inverse variance | Kirby & Ostdiek 2012 | Same | — | Same | **SOURCE LOCATED** | S4.5 |
| PC-A5 | Volatility targeting | Moreira & Muir 2017 | Moreira & Muir 2017, *JF* 72(4) | — | In hand | **SOURCE LOCATED** | S4.5 |
| PC-B1 | Maximum Sharpe ratio | Markowitz 1952 | Markowitz 1952; Tobin 1958; Sharpe 1964 | Michaud 1989; Jorion 1986 (estimation error) | In hand | **SOURCE LOCATED** | S4.6 |
| PC-B2 | Black–Litterman | Black & Litterman 1992 | BL 1992, *FAJ* 48(5) | He & Litterman 1999 (open, SSRN 334304); Idzorek 2005 (open, SSRN) | Primary in hand; supporting open | **SOURCE LOCATED** | S4.7 |
| PC-B3 | Robust mean–variance | Goldfarb & Iyengar 2003 | G&I 2003, *Math. Oper. Res.* 28(1):1–38 | Tütüncü & Koenig 2004; Ceria & Stubbs 2006 (paywalled) | Paywalled | **SOURCE LOCATED** (acquisition needed) | S4.7 |
| PC-B4 | Resampled efficient frontier | Michaud 1998 | **Michaud & Michaud 2008, *Efficient Asset Management*, 2nd ed., Oxford University Press** (the originators; the book states the procedure was "originally described in Michaud (1998, Chapter 6)"). Procedure: ch. 6, pp. 42–58, with rank- vs λ-associated averaging in App. A (p. 56) | Michaud 1989 (in hand; motivation only); Michaud & Michaud 2008, *JOIM* 6(1) (not needed now); Scherer 2002 critique (paywalled); US patent 6,003,018 | **In hand** (owner upload 2026-10-08; 145 pp., md5 `d1ae84ec9ade`). The book states RE is "a U.S. patented procedure" with an exclusive worldwide licensee (p. 42, fn. 1) | **SOURCE LOCATED** (IP check before implementation, D-2) | S4.7 |
| PC-B5 | Mean–downside risk (Sortino) | Sortino & van der Meer 1991 | S&vdM 1991, *JPM* 17(4):27–31 | Estrada (mean–semivariance heuristic); Markowitz, Todd, Xu & Yamane 1993; semicovariance/LPM paper; Hogan & Warren 1974 (all in hand) | In hand (scan; no text layer, read from page images) | **SOURCE LOCATED** | S4.5 / S4.12 |
| PC-B6 | Simple EPO | (not in ANG) | Pedersen, Babu & Levine 2021, *FAJ* 77(2):124–151 | Author version (49 pp., in hand); author code (not yet searched) | In hand | **SOURCE LOCATED** | S4.7 |
| PC-B7 | Anchored EPO | (not in ANG) | Same | Same | In hand | **SOURCE LOCATED** | S4.7, S4.10 |
| PC-C1 | Global minimum variance | Clarke, de Silva & Thorley 2006 | CdST 2006, *JPM* 33(1):10–24 | Markowitz 1952; Jagannathan & Ma 2003 (abstract verified 2026-10-08; full text missing) | Paywalled; author-affiliated page (identity unconfirmed until retrieved) | **SOURCE LOCATED** (acquisition needed) | S4.11 |
| PC-C2 | Risk parity (ERC) | Maillard, Roncalli & Teïletche 2010 | MRT 2010, *JPM* 36(4):60–70 | Spinu 2013 (algorithm; SSRN 2297383 only) | **In hand: working version** (May 2009, 23 pp., md5 `885b0373e72c`; author-hosted at thierry-roncalli.com; downloaded 2026-10-08 with owner permission). Published version governs | **SOURCE LOCATED** | S4.11 |
| PC-C3 | Hierarchical risk parity | López de Prado 2016 | LdP 2016, *JPM* 42(4):59–69 | — | Open working version (SSRN 2708678) | **SOURCE LOCATED** | S4.11 |
| PC-C4 | Maximum diversification | Choueifaty & Coignard 2008 | C&C 2008, *JPM* 35(1):40–51 | Choueifaty, Froidure & Reynier 2013 (not located) | Paywalled | **SOURCE LOCATED** (acquisition needed) | S4.11 |
| PC-C5 | Minimum correlation | Varadi et al. 2012 | Varadi, Kapler, Bee & Rittenhouse, *The Minimum Correlation Algorithm: A Practical Diversification Tool*, CSS Analytics, September 2012 (authors' release; never journal-published) | Co-author Kapler's R implementation (`min.corr`, `min.corr2`, SIT `strategy.r`; read only, never executed); authors' spreadsheet | **In hand** (owner upload 2026-10-08; 91 pp., md5 `c56c05f40ef4`). **Identity confirmed** (§7) | **SOURCE LOCATED** | S4.11 |
| PC-D1 | CVaR optimisation | Rockafellar & Uryasev 2000 | R&U 2000, *J. Risk* 2(3):21–41 | R&U 2002, *JBF* (not located) | Paywalled; author copies likely | **SOURCE LOCATED** (acquisition needed) | S4.12 |
| PC-D2 | Maximum drawdown-constrained | Chekhlov, Uryasev & Zabarankin 2005 | CUZ 2005, *IJTAF* 8(1):13–58 | Earlier version "Portfolio Optimization with Drawdown Constraints" (identity unconfirmed) | Open working version (SSRN 544742) | **SOURCE LOCATED** | S4.12 |
| PC-D3 | Tail-risk parity | Boudt, Carl & Peterson 2013 | BCP 2013, *J. Risk* 15(3):39–68 | Boudt, Peterson & Croux 2008 (modified ES; not located) | Open working version (SSRN 1885293) | **SOURCE LOCATED** | S4.12 |
| PC-D4 | TPA two-factor (equity, bonds) | Ang, Brandt & Denison 2014 (text also cites Gilmore & Simonian 2025) | **Concept:** ABD 2014 (in hand). **Weight mechanics:** AQR 2026 (in hand; D-5) with Treynor & Black 1973 as the primary for appraisal-ratio sizing | Gilmore & Simonian 2025, *JPM* 51(10) (paywalled); BI course note (Gerard 2026; local, SECONDARY) | Concept and specification lead in hand; Treynor & Black and Gilmore & Simonian paywalled | **SOURCE LOCATED** (Treynor & Black needed for the primary sizing mathematics) | S4.12 |
| PC-E2 | Adversarial diversifier | — (ANG §3.3 only) | ANG v2 §3.3, p. 10 | — | In hand | **SOURCE LOCATED** (ANG is the only source; formulation gaps, ANG-16) | S4.14 |
| PC-E1 | Researcher (role) | — | ANG v2 §3.3; example method: Bera & Park 2008, *Econometric Reviews* 27(4–6) | — | Bera & Park paywalled | Not a method (F-1); its example source is LOCATED · paywalled | S4.14 |

**Result (updated 2026-10-08, second round):** **all 22 methods are SOURCE LOCATED.**
- 15 have the governing source in hand: A1, A2, A3, A4, A5, B1, B2, B4, B5, B6, B7, C2, C5, E2, and D4 for the concept. A3, A4 and C2 are working versions; the published version governs.
- 3 are open working versions on SSRN only, awaiting the owner's manual download: C3, D2, D3.
- 4 need BI library access: B3, C1, C4, D1.
---

## 2. ANG-vs-source differences known before the mathematics is read

These come from ANG's own text and the issues register. **Everything else is checked when each source is read** (S4.5–S4.14). Nothing here is inferred from a source not yet in hand.

| Method(s) | Difference or gap | Ref | Resolved at |
|---|---|---|---|
| PC-A3, PC-A4 | ANG cites Kirby & Ostdiek for both 1/σ and 1/σ². **Resolved 2026-10-08** from KO's working version: both belong to KO's volatility-timing family VT(η), weights ∝ (1/σ̂²)^η; 1/σ is η = ½ and 1/σ² is η = 1 (eqs. 12, 14). KO test only η ∈ {1, 2, 4}, so **ANG's inverse volatility (η = ½) is in KO's family but outside KO's evidence**. KO's σ̂ is a 120-month rolling sample estimate of monthly excess-return volatility, rebalanced monthly; ANG states none of these | ANG-13 | S4.5 (specification) |
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
| PC-C5 | ANG cites Varadi et al. without saying which variant or tuning. The paper itself defines two variants (MinCorr, MinCorr2), and the co-author's code adds a rank-power parameter (default 1). The paper's worked examples carry swapped labels (source issues MCA-1 … MCA-3) | ANG-38 (M) | S4.11 |

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

## 6. Status after the owner's actions of 2026-10-08

**Obtained:**
- Kirby & Ostdiek, working version of 9 May 2010 (owner upload). Read for S4.4: resolves ANG-13 (§2).
- Michaud 1989, JSTOR text copy of the published article (owner upload; md5 `28cd76210bbf`). Read in full. It **diagnoses** error maximisation (Jobson–Korkie simulation, p. 34), non-uniqueness of optimal portfolios (p. 35) and remedies (constraints, pp. 34 and 40; benchmark asset allocation, Bayes–Stein, IC adjustment, p. 37). It **does not specify the resampled efficient frontier**, so it cannot govern PC-B4's procedure. For PC-B4 the procedure source is Michaud & Michaud 2008 (*JOIM* 6(1)), a published article by the method's originators.
- Maillard, Roncalli & Teïletche, working version of May 2009, from Roncalli's own site (download permitted by the owner).

**Not obtained, and why:**
- SSRN refuses scripted access (HTTP 403). In the in-app browser it showed a security verification that did not clear on its own. **Bot checks are never bypassed**, so the remaining six permitted items need a manual download by the owner, into `Finsol Research Papers/Downloaded 2026-10-08/`:

  | Item | SSRN abstract | Needed by |
  |---|---|---|
  | He & Litterman 1999 | 334304 | S4.7 |
  | Idzorek 2005 | SSRN (also a course-reading copy at cis.upenn.edu, third-party, versions 2002/2005/2007 differ) | S4.7 |
  | Spinu 2013 | 2297383 | S4.11 |
  | López de Prado 2016 | 2708678 | S4.11 |
  | Chekhlov, Uryasev & Zabarankin 2005 | 544742 | S4.12 |
  | Boudt, Carl & Peterson 2013 | 1885293 (no open copy found elsewhere; a 2010 companion vignette by the same authors exists on CRAN) | S4.12 |

**PC-C5: what the identity gap means, and the options.**
- *Why identity matters.* ADR-0025 admits a method only with a primary source and a **verified reproduction** of it. Reproduction checks our implementation against the source's own definitions and numbers. If the copy we read is not the authors' text (an altered or older draft), the reproduction oracle itself may be wrong, and the G4 claim "we implement the method ANG cites" is unsupported.
- *What was found.* The paper was only ever released by the authors as a draft: the blog post calls it a "draft preview", and it was posted to Scribd from the authors' account rather than published in a journal. The authors also released a spreadsheet, and co-author Kapler released R code with two variants (ANG-38).
- *Options:*
  1. **Confirm identity through the authors' channels (recommended).** Compare the mirror copy with the authors' Scribd upload (the owner can view it with a Scribd account), and cross-check the algorithm against the two author-produced implementations (spreadsheet, R code; read only, never executed). If they agree, PC-C5 becomes SOURCE LOCATED with the authors' release as the governing version.
  2. **Use the mirror as a working source labelled IDENTITY UNCONFIRMED.** Faster; the method can be specified, but admission (ADR-0025) carries an open identity caveat until option 1 is done.
  3. **Specify our own minimum-correlation-type method from the published algorithm descriptions only.** No claim to reproduce Varadi et al.; ANG conformance would be by family, not by source.
- *Side effect to disclose.* A web fetch of the mirror (to read its algorithm) automatically saved a copy of that PDF in this session's tool-results folder. The mirror was not on the permitted list, so that copy has **not** been read or used and awaits the owner's decision.

## 7. Second round, 2026-10-08: Michaud & Michaud, and PC-C5 identity (owner confirmed option 1)

**PC-B4.** The owner supplied Michaud & Michaud, *Efficient Asset Management* (2nd ed., OUP 2008), the originators' book. Chapter 6 defines the resampled efficient frontier: RE-optimal portfolios are averages of the weights of simulated efficient portfolios, associated by rank or by risk-aversion parameter (App. A). It governs PC-B4's procedure. The JOIM article is not needed. The book's own statement that RE is a patented, exclusively licensed procedure (p. 42, fn. 1) confirms that the D-2 IP check must precede implementation.

**PC-C5: identity confirmed (option 1).**

| Check | Result |
|---|---|
| Owner's upload vs the third-party mirror (the copy auto-saved earlier, §6; used only for this hash comparison) | Byte-identical (md5 `c56c05f40ef4`, 2,091,460 bytes) |
| Document metadata | Authors "David Varadi, Michael Kapler, Henry Bee, Corey Rittenhouse"; created 20 Sep 2012, one day before Varadi's release post (21 Sep 2012) |
| Authors' Scribd upload (doc 106570475) | Same page count (91). A byte comparison needs a Scribd login and was not done |
| Algorithm vs the co-author's code | Our own Python transcription (below) of Kapler's `min.corr` and `min.corr2` (SIT `strategy.r`, read via the web; **never executed**) reproduces the paper's three-asset worked example to rounding, including every intermediate (μ_ρ = 0.817, σ_ρ = 0.104; row averages [0.29, 0.54, 0.62]; μ₀ = 0.544, σ₀ = 0.035; transformed [0.13, 0.63, 0.79]) |

**Conclusion:** the uploaded file is the authors' release. It governs PC-C5, with the co-author's code as an independent cross-check of the algorithm.

**Source issues found in the check** (recorded in `ANG_ISSUES_REGISTER.md`, MCA-1 … MCA-3):
- **MCA-1:** the worked examples' labels are swapped. The example headed "Minimum Correlation" computes MinCorr2 and gives [0.50, 0.30, 0.20]. The example headed "Minimum Correlation 2" computes MinCorr and gives [0.21, 0.31, 0.48]. The step definitions (pp. 13–14) and the code agree with each other.
- **MCA-2:** the definition says to use the mean and SD of "all elements" of the correlation matrix. The example and the code use the off-diagonal elements only (sample SD), and exclude the diagonal from the row averages.
- **MCA-3:** the rank formula does not state the direction. The code ranks descending (`rank(-x)`): the most diversifying asset gets rank 1, which is the smallest rank weight. Final weights come from multiplying the rank weights by the adjusted matrix and then dividing by volatility.

**The owner's pasted script** is the co-author's comparison backtest: 8 ETFs, weekly rebalancing, EW / RP / MV / MD / MC / MC2. It loads the toolbox by downloading and `source()`-ing remote code and uses Yahoo data. It was read for its test design only and was **not run** (third-party code is never executed; Yahoo data does not fit our licence findings). S4.11 can mirror the design on synthetic data.

```python
# Our transcription (S4.4 identity check); reproduces Varadi et al. (2012) pp. 15-16
import numpy as np
from math import erf, sqrt
Phi = lambda x, m, s: 0.5 * (1 + erf((x - m) / (s * sqrt(2))))
def rank_desc(x):  # R: rank(-x)
    o = np.argsort(-np.asarray(x)); r = np.empty(len(x)); r[o] = np.arange(1, len(x) + 1); return r
def min_corr(R, sig, power=1):     # Kapler's min.corr (MinCorr)
    n = len(sig); iu = np.triu_indices(n, 1); c = R[iu]; mu, sd = c.mean(), c.std(ddof=1)
    A = np.zeros((n, n)); A[iu] = [1 - Phi(v, mu, sd) for v in c]; A = A + A.T
    avg = A.sum(1) / (n - 1); wr = rank_desc(avg) ** power; wr = wr / wr.sum()
    w = wr @ A; w = w / w.sum(); x = w / sig; return x / x.sum()
def min_corr2(R, sig, power=1):    # Kapler's min.corr2 (MinCorr2)
    C = R.copy(); np.fill_diagonal(C, 0); avg = C.mean(1); mu, sd = avg.mean(), avg.std(ddof=1)
    t = np.array([1 - Phi(v, mu, sd) for v in avg]); wr = rank_desc(t) ** power; wr = wr / wr.sum()
    w = wr @ (1 - C); w = w / w.sum(); x = w / sig; return x / x.sum()
R = np.array([[1, .90, .85], [.90, 1, .70], [.85, .70, 1]]); sig = np.array([14, 18, 22.])
print(min_corr(R, sig).round(2), min_corr2(R, sig).round(2))   # [0.21 0.31 0.48] [0.5 0.3 0.2]
```

## 5. Exit check

| Criterion (S4_PLAN §G row S4.4) | Status |
|---|---|
| Final §D with sources per method | §1 (supersedes the draft §D's source columns; §D stays as history) |
| ANG-vs-source differences listed | §2 (known now); the rest at each extraction step |
| Every PC method at SOURCE LOCATED or a documented acquisition gap | **All 22 SOURCE LOCATED** (second round, §7) |
| ANG-35 disposition | Recorded (§2) |
