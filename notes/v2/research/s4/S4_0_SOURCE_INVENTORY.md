# S4.0 — Source and artefact inventory

**Document status:** DRAFT (S4.0 output, for owner review before S4.1) · **Prepared:** 2026-10-02 · **Amended:** 2026-10-07 (ABD 2014 obtained and identity verified; owner decision D-5 on AQR as TPA specification source) · **Plan:** [S4_PLAN.md](S4_PLAN.md)

**Scope of S4.0:**
- Locate, identify and classify every source and prior artefact S4 needs.
- No mathematics has been extracted or reviewed.
- No method has been assessed or ranked.

**How the inventory was produced:**
- Every PDF under the two local research roots was fingerprinted (MD5) and title-extracted: 457 files, 222 unique. All 14 local zip archives were extracted to a scratch area.
- Large compiled PDFs were full-text searched; the matches found were citations, not the papers.
- Scanned files with no text layer were identified from their first-page images.
- Missing primaries were located online. **Nothing was downloaded** (downloads need owner permission; see D-4).

**Status classes (kept separate, per owner instruction):**
- **AVAILABLE** — local copy whose identity is confirmed.
- **MISSING** — no local copy. Sub-status `LOCATED` means an authoritative location was found, with its access type.
- **IDENTITY UNCONFIRMED** — local or located copy whose version or identity is not yet confirmed.
- **UNUSABLE/CORRUPT** — cannot be used as a source.
- **SECONDARY** — may not govern mathematics when a primary source exists.

**Local roots:**
- `RPT` = `~/Desktop/Research Papers Thesis/`
- `DOC` = `~/Documents/Documents – Oliver's MacBook Pro/Portfolio Optimization/`

Paths are given relative to these roots. Local files are not copied into the repository (copyright).

---

## 1. Baseline and EPO

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Ang, Azimbayev & Kim, *The Self-Driving Portfolio*, version dated 21 Sep 2026, 40 pp | AVAILABLE | DOC/Portfolio Optimization/Self-Driving Portfolio.pdf (identical copy inside the owner-supplied zip) | All architecture; S4.1 |
| Pedersen, Babu & Levine (2021), "Enhanced Portfolio Optimization," *FAJ* 77(2):124–151 — final published version, 30 pp, CC BY-NC-ND | AVAILABLE | RPT/Portfolio Optimization/EPO Full.pdf (= EPO Detailed.pdf, same document); appendix sections present | PC-B6, PC-B7; S4.7, S4.10 |
| Pedersen, Babu & Levine — author version, 49 pp | AVAILABLE | RPT/Portfolio Optimization/Enhanced Portfolio Optimization.pdf; contains Appendix (pp. 11, 32 ff.) and propositions | PC-B6, PC-B7 (cross-check against the FAJ version) |
| PBL author code / online supplement | MISSING | Not searched yet | S4.7 |
| "Improving Portfolio Optimization with Enhanced Portfolio Optimization — An Empirical Study" | **UNUSABLE/CORRUPT** | RPT/Portfolio Optimization/… (pypdf: "Cannot find Root object") | Not evidence (owner instruction) |
| Larsen (2022), CBS master's thesis, EPO of factor strategies | SECONDARY | RPT/Portfolio Optimization/ENHANCED PORTFOLIO OPTIMIZATION OF FACTOR INVESTMENT STRATEGIES.pdf | Replication context only |

## 2. Mean–variance foundation and estimation error (S4.6–S4.7)

| Source | Status | Location | Maps to |
|---|---|---|---|
| Markowitz (1952), "Portfolio Selection," *JF* | AVAILABLE | RPT/Portfolio Optimization/Portfolio Selection.pdf | MVO; PC-B1; PC-C1 |
| Markowitz (1991), "Foundations of Portfolio Theory," *JF* 46(2) | AVAILABLE (identity confirmed from page image) | RPT/Portfolio Optimization/Foundations of Portfolio Theory.pdf | MVO context |
| Tobin (1958), "Liquidity Preference as Behavior Towards Risk" | AVAILABLE | RPT/Portfolio Optimization/… | PC-B1 (risk-free asset, separation) |
| Sharpe (1964), "Capital Asset Prices" | AVAILABLE | RPT/Portfolio Optimization/CAPITAL ASSET PRICES…pdf | PC-A2, PC-B1 |
| Michaud (1989), "The Markowitz Optimization Enigma: Is 'Optimized' Optimal?" *FAJ* Jan–Feb 1989 | AVAILABLE (identity confirmed from page image) | RPT/Portfolio Optimization/Optimization Enigma.pdf | Estimation-error problem; PC-B4 context |
| Jorion (1986), "Bayes–Stein Estimation for Portfolio Analysis," *JFQA* | AVAILABLE | RPT/Portfolio Optimization/Bayes-Stein…pdf | Estimation error (S4.6), S9 |
| DeMiguel, Garlappi, Nogales & Uppal (2009), "A Generalized Approach … Constraining Portfolio Norms," *Mgmt Sci* | AVAILABLE | RPT/Portfolio Optimization/A Generalized Approach…pdf | Candidate (norm-constrained MVO) |
| Ang (2012), "Mean-Variance Investing" (book-chapter working paper) | SECONDARY | RPT/Portfolio Optimization/Mean‐Variance Investing.pdf | Exposition only |
| Kan & Zhou (2007), *JFQA* | MISSING | Not yet located | Estimation-error context |
| Jagannathan & Ma (2003), *JF* | MISSING | Not yet located | PC-C1 constraints context |

## 3. ANG fixed PC methods — primary sources

| ID | Method | Primary source (as cited by ANG unless marked) | Status | Location / route |
|---|---|---|---|---|
| PC-A1 | Equal weight | DeMiguel, Garlappi & Uppal (2009), *RFS* | AVAILABLE | RPT/Portfolio Optimization/Optimal Versus Naive Diversification…pdf |
| PC-A2 | Market-cap weight | Sharpe (1964) | AVAILABLE | as §2 |
| PC-A3 / A4 | Inverse volatility / inverse variance | Kirby & Ostdiek (2012), "It's All in the Timing," *JFQA* 47(2):437–467 | MISSING — LOCATED | Author page [Kirby research](https://belkcollegeofbusiness.charlotte.edu/ckirby10/research/); Academia.edu copy (IDENTITY UNCONFIRMED); JFQA (paywalled) |
| PC-A5 | Volatility targeting | Moreira & Muir (2017), "Volatility-Managed Portfolios," *JF* | AVAILABLE | RPT/Downside Risk/Volatility-Managed Portfolios.pdf |
| PC-B1 | Maximum Sharpe | Markowitz (1952); add Tobin (1958), Sharpe (1964) | AVAILABLE | as §2 |
| PC-B2 | Black–Litterman | Black & Litterman (1992), *FAJ* 48(5) | AVAILABLE | RPT/Portfolio Optimization/Global Portfolio Optimization.pdf |
| PC-B2 (supporting) | — | He & Litterman (1999), "The Intuition Behind Black–Litterman Model Portfolios" | MISSING — LOCATED (open) | [SSRN 334304](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=334304) |
| PC-B2 (supporting) | — | Idzorek (2005/2007) | MISSING | Not yet located |
| PC-B3 | Robust mean–variance | Goldfarb & Iyengar (2003), *Math. Oper. Res.* 28(1):1–38, doi 10.1287/moor.28.1.1.14260 | MISSING — LOCATED (paywalled) | [INFORMS](https://pubsonline.informs.org/doi/10.1287/moor.28.1.1.14260) |
| PC-B3 (supporting) | — | Tütüncü & Koenig (2004); Ceria & Stubbs (2006) | MISSING | Not yet located |
| PC-B4 | Resampled efficient frontier | Michaud (1998), *Efficient Asset Management*, HBS Press (book; 2nd ed. 2008) | MISSING — LOCATED (book, purchase) | Publisher/retailer; related US patent 6,003,018 ([Google Patents](https://patents.google.com/patent/US6003018A/en)) — **IP status to check** (owner decision D-2, 2026-10-07: the check is done before PC-B4 is implemented; it does not block registration or the specification) |
| PC-B4 (supporting) | — | Michaud & Michaud, "Estimation Error and Portfolio Optimization: A Resampling Solution" (author note) | MISSING — LOCATED (open) | [New Frontier Advisors PDF](https://newfrontieradvisors.com/media/rxbld4hq/estimation-error-and-portfolio-optimization-12-05.pdf) — SECONDARY-to-book; IDENTITY UNCONFIRMED |
| PC-B4 (critique) | — | Scherer (2002) | MISSING | Not yet located |
| PC-B5 | Mean–downside risk (Sortino) | Sortino & van der Meer (1991), "Downside Risk," *JPM* 17(4):27–31 | AVAILABLE (identity confirmed from page image; scanned, no text layer) | RPT/Downside Risk/Downside Risk.pdf |
| PC-B5 (supporting) | — | Estrada, mean–semivariance heuristic; Markowitz et al., semivariance efficient sets; semicovariance/LPM paper; Hogan & Warren / semivariance CAPM | AVAILABLE | RPT/Portfolio Optimization/… ; RPT/Downside Risk/… |
| PC-C1 | Global minimum variance | Clarke, de Silva & Thorley (2006), *JPM* 33(1):10–24, doi 10.3905/jpm.2006.661366 | MISSING — LOCATED | [Hillsdale Investments page](https://www.hillsdaleinv.com/research/minimum-variance-portfolios-in-the-u.s.-equity-market) (author-affiliated; IDENTITY UNCONFIRMED until retrieved); JPM (paywalled) |
| PC-C2 | Risk parity (ERC) | Maillard, Roncalli & Teïletche (2010), *JPM* 36(4):60–70, doi 10.3905/jpm.2010.36.4.060 | MISSING — LOCATED (open working version) | [SSRN 1271972](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1271972); [Roncalli risk-parity page](http://www.thierry-roncalli.com/RiskParity.html) |
| PC-C3 | Hierarchical risk parity | López de Prado (2016), *JPM* 42(4):59–69 | MISSING — LOCATED (open) | [SSRN 2708678](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2708678) |
| PC-C4 | Maximum diversification | Choueifaty & Coignard (2008), *JPM* 35(1):40–51 | MISSING — LOCATED (paywalled) | [PM Research](https://www.pm-research.com/content/iijpormgmt/35/1/40) |
| PC-C4 (supporting) | — | Choueifaty, Froidure & Reynier (2013) | MISSING | Not yet located |
| PC-C5 | Minimum correlation | Varadi, Kapler, Bee & Rittenhouse (2012), CSS Analytics working paper | MISSING — LOCATED (open; working paper) | [rybn.org PDF](https://rybn.org/halloffame/PDFS/2012-09_The%20Minimum%20Correlation%20Algorithm%20A%20Practical%20Diversification%20Tool.pdf) — **IDENTITY UNCONFIRMED** (third-party mirror; original author host not found) |
| PC-D1 | CVaR | Rockafellar & Uryasev (2000), *J. Risk* 2(3):21–41 | MISSING — LOCATED (paywalled; author copies likely) | [Semantic Scholar record](https://www.semanticscholar.org/paper/Optimization-of-conditional-value-at-risk-Rockafellar-Uryasev/58444c142b6ea5c71a435cac7a0b4c66d6c68869) |
| PC-D1 (supporting) | — | Rockafellar & Uryasev (2002), general distributions, *JBF* | MISSING | Not yet located |
| PC-D2 | Max drawdown-constrained | Chekhlov, Uryasev & Zabarankin (2005), *IJTAF* 8(1):13–58 | MISSING — LOCATED (open working version) | [SSRN 544742](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=544742); a UPenn-hosted PDF titled "Portfolio Optimization with Drawdown Constraints" ([link](https://www.cis.upenn.edu/~mkearns/finread/drawdown.pdf)) is probably an earlier version (IDENTITY UNCONFIRMED) |
| PC-D3 | Tail-risk parity | Boudt, Carl & Peterson (2013), *J. Risk* 15(3):39–68 | MISSING — LOCATED (open working version) | [SSRN 1885293](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1885293) |
| PC-D3 (supporting) | — | Boudt, Peterson & Croux (2008), modified ES | MISSING | Not yet located |
| PC-D4 | TPA two-factor | Ang, Brandt & Denison (2014), *Review of the Active Management of the Norwegian Government Pension Fund Global*, report to the Norwegian Ministry of Finance (20 Jan 2014) | **AVAILABLE** (owner-supplied 2026-10-02; read in full 2026-10-02; identity re-verified 2026-10-07) | `DOC/Finsol Research Papers/angbrandtdenison_2014.pdf`, 163 PDF pp., md5 da26aa3090d0. Title page, date (20 January 2014) and authors match ANG's reference-list entry. Printed page = PDF page − 2. The earlier URL candidates are superseded and were never fetched. **Content for PC-D4:** ABD's TPA / Opportunity Cost Model is a *funding and benchmarking* framework: $1 in a β = 1.3 asset ≡ $1.30 equities − $0.30 bonds (Eq. (4), p. 74). A constrained-OLS funding mix for one asset (Eq. (A.3), p. 121). **No portfolio weight-producing rule.** Internal issues ABD-1 … ABD-5 are recorded in `ANG_ISSUES_REGISTER.md` |
| PC-D4 (also cited in ANG text) | — | Gilmore & Simonian (2025), *JPM* 51(10):40–48 | MISSING — LOCATED (paywalled) | [PM Research](https://www.pm-research.com/content/iijpormgmt/51/10/40) |
| PC-D4 | — | AQR Portfolio Solutions Group (Hecht, Heffernan, Ilmanen, Maloney, McQuinn & Sachdev), "Total Portfolio Approach: A Quant Lens," *AQR Alternative Thinking* 2026 Issue 2 (22 pp.) | SECONDARY (practitioner) — **read in full 2026-10-02** | RPT/Portfolio Optimization/Total Portfolio Approach.pdf; owner-supplied copy `AQR Alternative Thinking - Total Portfolio Approach.pdf` (md5 16bf8f961f21). **Not a substitute for ABD 2014 as ANG's cited source.** Usable as a *specification lead* for a TPA-family candidate: "no single definition of TPA" (p. 3); two-factor stock/bond regression and appraisal ratio AR = α/σ_ε (p. 6); unconstrained results SR²_max = SR²_current + AR² and allocation ∝ AR/σ_ε (p. 6 fn. 11–12; verified numerically 2026-10-02); explicitly assumes leverage and shorting (p. 7). Cites ABD 2014 only for "TPA and its application to funding and benchmarking investments" (p. 3 fn. 2). Primary for the appraisal-ratio mathematics: Treynor & Black (1973), *Journal of Business* 46(1) (per AQR reference list; not yet obtained). **Owner decision D-5 (2026-10-07):** AQR may substitute for ABD as the *specification source for TPA weight mechanics* wherever it is more informative, i.e. for how TPA becomes portfolio weights. ABD remains ANG's cited source for the TPA concept (complement, not replacement). **`VERIFIED-DERIVATION` (2026-10-07):** without constraints, AQR's sizing equals the max-Sharpe (tangency) portfolio under a factor-structured Σ with diagonal residuals: max abs difference 1.6 × 10⁻¹⁴ in a numerical check; SR²_max = SR²_factors + Σ AR² holds. A distinct TPA-family method therefore needs a reference-relative, funded, constrained formulation (S4.12) |
| PC-E1 (example) | Researcher — max entropy | Bera & Park (2008), *Econometric Reviews* 27(4–6):484–512, doi 10.1080/07474930801960394 | MISSING — LOCATED (paywalled) | [RePEc](https://ideas.repec.org/a/taf/emetrv/v27y2008i4-6p484-512.html) |
| PC-E2 | Adversarial diversifier | ANG §3.3 only (no external source) | AVAILABLE (ANG) | — |

## 4. Momentum (S4.8–S4.9)

| Source | Status | Location / route |
|---|---|---|
| Jegadeesh & Titman (1993), *JF* | AVAILABLE | RPT/Momentum/Returns to Buying Winners…pdf |
| Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum," *JFE* | AVAILABLE | RPT/Momentum/Time series momentum.pdf (duplicate "copy") |
| Asness, Moskowitz & Pedersen (2013), "Value and Momentum Everywhere," *JF* | AVAILABLE | RPT/Momentum/Value and Momentum Everywhere.pdf.pdf |
| Hurst, Ooi & Pedersen (2017), "A Century of Evidence on Trend-Following" | AVAILABLE | RPT/Momentum/… |
| Daniel & Moskowitz (2016), "Momentum Crashes" | AVAILABLE | RPT/Momentum/… |
| Barroso & Santa-Clara (2015), "Momentum Has Its Moments" | AVAILABLE | RPT/Momentum/… (duplicate) |
| Moskowitz & Grinblatt (1999), "Do Industries Explain Momentum?" | AVAILABLE | RPT/Momentum/… |
| "Time-series and cross-sectional momentum strategies under alternative implementation strategies" | AVAILABLE (author and venue to confirm) | RPT/Momentum/… |
| Goyal & Jegadeesh (2018), *RFS* 31(5):1784–1824, doi 10.1093/rfs/hhx131 | MISSING — LOCATED | [OUP](https://academic.oup.com/rfs/article-abstract/31/5/1784/4636242); author page may host a copy |
| Kim, Tse & Wald (2016), *J. Financial Markets* 30:103–124, doi 10.1016/j.finmar.2016.05.003 | MISSING — LOCATED (open working version) | [SSRN 2786955](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2786955) |
| Wang, Yan & Zheng, TSMOM/XSMOM in anomaly returns (*EFM*) | AVAILABLE (SECONDARY to the primaries) | RPT/Momentum/TSMOM and XSMOM in rets.pdf |
| Kivelä (2025), bachelor's thesis, XSMOM/TSMOM in the S&P 500 | SECONDARY | RPT/Momentum/XSMOM and TSMOM in SP500.pdf |

## 5. Upstream CMA, regime, judge (S4.15 → S9)

| Source | Status | Location / route |
|---|---|---|
| Merton (1980), "On Estimating the Expected Return on the Market" | AVAILABLE | RPT/Active vs Passive/… |
| Black & Litterman (1992) | AVAILABLE | as §3 |
| Gordon (1959), *REStat* | MISSING | JSTOR (not yet located) |
| Grinold & Kroner (2002), *Investment Insights* 5(3), BGI | MISSING — LOCATED (third-party mirrors only) | e.g. silo.tips copy — IDENTITY UNCONFIRMED; CFA Institute literature reviews cite it |
| Campbell & Shiller (1998), *JPM* 24(2):11–26 | MISSING — LOCATED (paywalled) | [PM Research](https://www.pm-research.com/content/iijpormgmt/24/2/11); 2001 update NBER w8221 (a different paper) |
| Zheng et al. (2023), LLM-as-a-judge | MISSING — LOCATED (open) | [arXiv 2306.05685](https://arxiv.org/abs/2306.05685) |
| Du et al. (2023), multi-agent debate | MISSING — LOCATED (open; arXiv 2305.14325 per the ANG bibliography) | arXiv |

## 6. Risk / covariance inventory (S4.13 → S10)

| Source | Status | Location / route |
|---|---|---|
| Ledoit & Wolf (2003), single-index shrinkage | AVAILABLE | RPT/Correlation Shrinkage/Improved estimation…pdf |
| Ledoit & Wolf (2004), well-conditioned | AVAILABLE | RPT/Correlation Shrinkage/A well-conditioned estimator… |
| Ledoit & Wolf (2017), nonlinear shrinkage | AVAILABLE | RPT/Correlation Shrinkage/Nonlinear Shrinkage… |
| Laloux, Cizeau & Potters, RMT and financial correlations | AVAILABLE | RPT/Correlation Shrinkage/… |
| Bun, Bouchaud & Potters (2017), cleaning large correlation matrices | AVAILABLE (two versions: 109 pp and 165 pp) | RPT/Correlation Shrinkage/…; RPT/Portfolio Optimization/… |
| Wang (2005), shrinkage / model uncertainty | AVAILABLE | RPT/Correlation Shrinkage/Wang-ShrinkageApproachModel-2005.pdf |
| Semicovariance / LPM papers | AVAILABLE | RPT/Portfolio Optimization/… |
| Engle (2002), DCC, *JBES* 20(3):339–350, doi 10.1198/073500102288618487 | MISSING — LOCATED (author copy) | [NYU Stern PDF](https://pages.stern.nyu.edu/~rengle/dccfinal.pdf) |
| Aielli (2013), cDCC, *JBES* 31(3):282–299, doi 10.1080/07350015.2013.771027 | MISSING — LOCATED (paywalled) | ResearchGate record |
| Bollerslev (1986), GARCH | MISSING | Not yet located |
| Glosten, Jagannathan & Runkle (1993) | MISSING | Not yet located (the local "Glosten" match is Glosten–Milgrom 1985, a false positive) |

## 7. Diagnostics, ensembles, deliberation (S4.16–S4.18 → S12)

| Source | Status | Location / route |
|---|---|---|
| Meucci (2009), "Managing Diversification," *Risk* | MISSING — LOCATED (open) | [SSRN 1358533](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1358533) |
| Bates & Granger (1969) | MISSING | Not yet located |
| Acerbi & Tasche (2002), ES | MISSING | Not yet located |
| Spinu (2013), ERC algorithm | MISSING | Not yet located |
| Sortino & Price (1994) | MISSING | Not yet located |

## 8. Prior project artefacts (leads only; ADR-0001)

| Artefact | Location | Use in S4 |
|---|---|---|
| ENGINE_V1 R code: solvers (mean_variance, risk_budget, utility), operators (anchor, shrinkage), signals (basic, cross_sectional), GARCH module, core APIs | `~/Desktop/ENGINE_V1/` | Not a source of equations. May be consulted only to identify historical design intentions. **Contains no UEPO/SEPO/DEPO identifiers** (case-sensitive search) |
| ENGINE_V1 notes: SPECIFICATION.md, MATHEMATICAL_APPENDIX.md, momentum (signal construction, taxonomy), shrinkage (LW2003, LW2004, Wang2005), RMT background, agentic-SAA review | `~/Desktop/ENGINE_V1/notes/` | Leads only; superseded (09_LEGACY_SUPERSEDED) |
| Repository-root SPECIFICATION.md, MATHEMATICAL_APPENDIX.md | finsolution root | Legacy, non-authoritative |
| Thesis artefacts: Oversikt EPO Thesis.pdf, Plots V54 merged.pdf, Thesis Idea.pdf, Earlier Thesis Papers.zip | RPT | Leads only. Any UEPO/SEPO/DEPO content is excluded (L) |
| REF-01 memo (S0) | notes/v2/research | Prior reading of the same ANG version; S4.1 rebuilds from the paper |

## 10. Accountability, implementation and short-horizon sources (added 2026-10-02; NBIM/trading-layer review)

Identity verified against each document's own text, not its filename. These support ADR-0026 (PROPOSED) and the S4.2b / S4.15b work. They are not PC-method sources.

| Source | Status | Location | Supports (scope) |
|---|---|---|---|
| Bauer, Christiansen & Døskeland (2022), *A Review of the Active Management of Norway's Government Pension Fund Global*, report to the Ministry of Finance (3 Jan 2022), 117 pp. | AVAILABLE (read in full) | Owner download `Evaluation_GPFG.pdf` (md5 b80c7593ae88); to be filed in RPT | Institutional/accountability evidence: mandates, mapping performance to units, "container" categories, rebalancing decided by the Ministry, implementation as a value source, statistical power |
| Sharpe (1981), "Decentralized Investment Management," *JF* 36(2), 217–234 | AVAILABLE (relevant sections read) | Owner zip `Finsol S4 papers.zip` | Diversification of judgement vs style (pp. 220, 232–233); eq. (22a), p. 230 (mean–variance case) |
| van Binsbergen, Brandt & Koijen (2008), "Optimal Decentralized Investment Management," *JF* 63(4), 1849–1895 | AVAILABLE (abstract, structure, conclusions) | Owner zip | Delegation misalignments; benchmark design as mitigation |
| Sensoy (2009), "Performance Evaluation and Self-Designated Benchmark Indexes in the Mutual Fund Industry," *JFE* 92(1), 25–39 | AVAILABLE (abstract) | Owner zip | Self-designated benchmarks can be strategically mismatched even when specified in advance |
| Perold (1988), "The Implementation Shortfall: Paper versus Reality," *JPM* Spring 1988, pp. 4–9 (scanned) | AVAILABLE (read in full) | Owner zip | Shortfall = execution cost + opportunity cost (App. B); paper portfolio at decision-time mid; pace of trading |
| Perold & Sharpe (1988), "Dynamic Strategies for Asset Allocation," *FAJ* 44(1), 16–27 | AVAILABLE (abstract, conclusion) | Owner zip | Rebalancing rules embody investor risk tolerance and path exposure (p. 26) |
| Jegadeesh (1990), "Evidence of Predictable Behavior of Security Returns," *JF* 45(3), 881–898 | AVAILABLE (abstract, cost passage) | Owner zip | Short-horizon reversal family located (monthly, individual stocks) |
| Lehmann (1990), "Fads, Martingales, and Market Efficiency," *QJE* 105(1), 1–28 | AVAILABLE (abstract, cost passage) | Owner zip | Short-horizon reversal family located (weekly, individual stocks); closing-price data limitation (fn. 16) |
| Wermers (2011), "Performance Measurement of Mutual Funds, Hedge Funds, and Institutional Accounts," *ARFE* 3(1), 537–574 | SECONDARY via BCD App. C (p. 98) | — | Benchmark properties as restated by BCD; primary optional |
| *Misidentified file:* "Active Management in Mostly Efficient Markets.pdf" | IDENTITY ≠ REQUESTED | Owner zip | Is Jones & Wermers (2011), *FAJ* 67(6), 29–45 — not Wermers (2011) *ARFE*; supports no current claim |
| *Misidentified file:* "NBIM_September_22_2014.pdf" (image-only) | IDENTITY ≠ REQUESTED | Owner zip | NBIM news page and CEO speech (22 Sep 2014); neither ABD 2014 nor NBIM (2014) "Benchmark Design for an Active Investment Process" |

## 9. Summary counts (primaries needed for the ANG fixed methods + EPO)

| Class | Count | Items |
|---|---|---|
| AVAILABLE | 9 | DGU 2009, Sharpe 1964, Moreira–Muir 2017, Markowitz 1952, Black–Litterman 1992, Sortino–van der Meer 1991, PBL 2021 (two versions), ANG, Ang–Brandt–Denison 2014 (obtained 2026-10-02; recorded 2026-10-07) |
| MISSING — LOCATED, open | 6 | Maillard–Roncalli–Teïletche, López de Prado, Varadi (mirror), Chekhlov–Uryasev–Zabarankin (working paper), Boudt–Carl–Peterson (working paper), He–Litterman (supporting) |
| MISSING — LOCATED, paywalled or book | 7 | Kirby–Ostdiek, Goldfarb–Iyengar, Michaud 1998 (book), Clarke–de Silva–Thorley, Choueifaty–Coignard, Rockafellar–Uryasev 2000, Gilmore–Simonian |
| UNUSABLE/CORRUPT | 1 | EPO empirical-study PDF |

**Working-version caveat:** where only an SSRN working version is open, the journal version governs. Differences are checked at S4.4 (rule: the published version governs; differences are recorded). **Owner decision D-3 (2026-10-07):** open SSRN or author working versions are accepted as working sources on this rule.

**Owner decision D-4 (2026-10-07):** unchanged. The owner supplies papers; any download needs explicit per-item permission. Two items were permitted on 2026-10-07: arXiv 2502.15800 v3 and the Gao–Jiang–Yan procedure file.

## 11. Sources added 2026-10-07 (ANG lecture, its references, third-party code, contamination and correlated-error literature)

Context: `S4_INPUTS_2026-10-07.md` and `S4_GITHUB_IMPL_REVIEW.md`. Nothing was downloaded except the read-only retrieval of the public GitHub repository's text files, which the owner asked for (never executed).

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Ang, *The Self-Driving Portfolio* (Q Group lecture), Oct 2026, 41 slides | AVAILABLE; SECONDARY (same author; newest authorial statement) | `~/Downloads/Self driving portfolioPP.pdf` (md5 24ae5f9d2479); `~/Downloads/Q Group Oct 2026.pptx` (md5 1f2f5aa17f91; speaker notes on slides 13, 22, 27, 31, 38; two silent demo clips) | S4.1; ANG-24 … ANG-27 |
| ANG April 1, 2026 draft (arXiv 2604.02279 v1) | SUPERSEDED (v2 = 21 Sep 2026 per arXiv, checked 2026-10-07) | `~/Downloads/The Self-Driving Portfolio_ …pdf` (32 pp., md5 13478390a196) | Tracing third-party code only |
| chirindaopensource, *agentic_architecture_for_institutional_asset_management* (GitHub; MIT; Apr 2026; implements v1) | PRACTITIONER / THIRD-PARTY CODE (lead; verified reuse only) | github.com/chirindaopensource/agentic_architecture_for_institutional_asset_management (15 commits, 14–18 Apr 2026) | `S4_GITHUB_IMPL_REVIEW.md` |
| Glasserman & Lin (2023), "Assessing Look-Ahead Bias in Stock Return Predictions Generated By GPT Sentiment Analysis", arXiv 2309.17322 v1 (Sep 2023) | AVAILABLE (read in full in the sandbox context, 2026-10-02) | `DOC/Finsol Research Papers/…GPT Sentiment Analysis.pdf` (17 pp., md5 04a5203b0b35) | RQ-26: anonymised headlines did better in-sample, so the direction of bias is not known in advance |
| Atil et al. (2025), "Non-Determinism of 'Deterministic' LLM System Settings in Hosted Environments" | MISSING (cited by ANG) | Not located | 04 §2 (S8) |
| He et al. (2025), "Defeating Nondeterminism in LLM Inference" (Thinking Machines) | MISSING — LOCATED (open) | thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ (lecture s21) | 04 §2 (S8) |
| Yan, Tang, Gao, Jiang & Lu (2026), "DatedGPT" | MISSING — LOCATED (open) | arXiv 2603.11838 (lecture s17; cited by ANG p. 23) | RQ-26 |
| Kelly, Malamud, Schwab & Xu (2026), "Scaling Point-in-Time Language Models", NBER WP 35247 | MISSING (cited by ANG p. 23) | NBER | RQ-26 |
| Pappu et al. (2026), "Self-Organizing Agent Teams Learn to Reason Together" | MISSING — LOCATED; `UNVERIFIED` (only the slide seen) | arXiv 2609.22682 (lecture s37) | RQ-16 |
| Wang et al. (2026), "Macro Economists in the Machine: A Multi-Agent LLM Framework for Commodity-Related ETF Portfolio Construction" | MISSING — LOCATED; `UNVERIFIED` (seen only as a bot summary on lecture s8) | arXiv 2606.08283 | RQ-26 (effect-size prior), RQ-16 |
| Kim, Garg, Peng & Garg (2025), "Correlated Errors in Large Language Models", ICML 2025 | MISSING — LOCATED (abstract verified 2026-10-07) | arXiv 2506.07962; PMLR v267 | RQ-56 |
| Kleinberg & Raghavan (2021), "Algorithmic Monoculture and Social Welfare", *PNAS* | MISSING — LOCATED (`VERIFIED-SECONDARY`) | arXiv 2101.05853 | RQ-56 |
| Panickssery, Bowman & Feng (2024), "LLM Evaluators Recognize and Favor Their Own Generations", NeurIPS 2024 | MISSING — LOCATED (`VERIFIED-SECONDARY`) | arXiv 2404.13076 | RQ-56 |
| Liang et al. (2024), "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate", EMNLP 2024 | MISSING — LOCATED (`VERIFIED-SECONDARY`) | arXiv 2305.19118 | RQ-16, RQ-56 |
| Schoenegger, Tuminauskaite, Park & Tetlock (2024), "Wisdom of the Silicon Crowd" | MISSING — LOCATED (`VERIFIED-SECONDARY`) | arXiv 2402.19379 | ANG-12; checklist M-6 |
| Nordnet price list (prisliste) | VERIFIED-SOURCE (retrieved 2026-10-07) | nordnet.no/kundeservice/prisliste | CB-17, CB-18; RQ-18 |
| *Reviewed, not used:* Altbridge internal model benchmark (lecture s11); Top Traders Unplugged podcast (s25); IPE and Bloomberg news items (s3, s9, s35) | DOES NOT FIT (no verifiable methodology; news used only as illustration) | — | — |
