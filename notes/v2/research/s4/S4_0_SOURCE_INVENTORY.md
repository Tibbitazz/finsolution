# S4.0 — Source and artefact inventory

**Document status:** DRAFT (S4.0 output, for owner review before S4.1) · **Prepared:** 2026-10-02 · **Amended:** 2026-10-07 (ABD 2014 obtained and identity verified; owner decision D-5 on AQR as TPA specification source); 2026-10-15 (§16: Paleologo 2025, the S4.8 momentum and trend set, the Michaud monitoring application); 2026-10-18 (§17: the S4.9 alpha and transfer-coefficient sources; §18: the S4.10 benchmark sources; §19: the S4.12a sources read from the existing library; §20: the S4.12b TPA sources); 2026-10-19 (§21: the three TPA papers, owner uploads; §22: sources located for S4.15b families T6 and T12 and two S9c candidates); 2026-10-25 (§23: Renshaw et al. 2026, the STOXX whitepaper and the iSTOXX methodology guide §118) · **Plan:** [S4_PLAN.md](S4_PLAN.md)

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
| Jegadeesh & Titman (1993), *JF* | AVAILABLE · *read for S4.8, 2026-10-15 (construction sections in full; `S4_MOMENTUM.md` §1), md5 ee332e58c9eb* | RPT/Momentum/Returns to Buying Winners…pdf |
| Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum," *JFE* | AVAILABLE · *read for S4.8, 2026-10-15 (construction sections in full; `S4_MOMENTUM.md` §1), md5 fab78eb489bb* | RPT/Momentum/Time series momentum.pdf (duplicate "copy") |
| Asness, Moskowitz & Pedersen (2013), "Value and Momentum Everywhere," *JF* | AVAILABLE · *read for S4.8, 2026-10-15 (construction sections in full; `S4_MOMENTUM.md` §1), md5 06c4c28235df* | RPT/Momentum/Value and Momentum Everywhere.pdf.pdf |
| Hurst, Ooi & Pedersen (2017), "A Century of Evidence on Trend-Following" | AVAILABLE (SSRN copy, abstract 2993026; the *JPM* version governs) · *read for S4.8, 2026-10-15 (construction sections in full; `S4_MOMENTUM.md` §1), md5 87b778184b2f* | RPT/Momentum/… |
| Daniel & Moskowitz (2016), "Momentum Crashes" | AVAILABLE · *read for S4.8, 2026-10-15 (construction sections in full; `S4_MOMENTUM.md` §1), md5 1bf00383678a* | RPT/Momentum/… |
| Barroso & Santa-Clara (2015), "Momentum Has Its Moments" | AVAILABLE · *read for S4.8, 2026-10-15 (construction sections in full; `S4_MOMENTUM.md` §1), md5 dcc5343503cf* | RPT/Momentum/… (duplicate) |
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
| *Added 2026-10-08 (S4.1 §13.2; `CANDIDATE SOURCE`, bibliographic data unchecked):* Bollerslev (1990), constant-conditional-correlation multivariate GARCH (CCC-GARCH), *REStat* | MISSING | To locate; COV inventory (S4.13 → S10) |
| J.P. Morgan/Reuters (1996), *RiskMetrics — Technical Document* (EWMA) | MISSING | To locate; COV inventory |
| Higham (2002), "Computing the nearest correlation matrix", *IMA J. Numer. Anal.* | MISSING | To locate; Assembling Σ from separately estimated rows (ANG-33) |
| Elton & Gruber (1973), constant-correlation model, *JF* | MISSING | To locate; Constant-correlation shrinkage target |

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

Identity verified against each document's own text, not its filename. These support ADR-0026 (ACCEPTED 2026-10-08) and the S4.2b / S4.15b work. They are not PC-method sources.

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
| Glasserman & Lin (2023), "Assessing Look-Ahead Bias in Stock Return Predictions Generated By GPT Sentiment Analysis", arXiv 2309.17322 v1 (Sep 2023) | AVAILABLE (read in full in the sandbox context, 2026-10-02) | `DOC/Finsol Research Papers/…GPT Sentiment Analysis.pdf` (17 pp., md5 04a5203b0b35) | RQ-26: anonymised headlines did better in-sample, so the direction of bias is not known in advance. *Scope (2026-10-07): this holds for named vs anonymised inputs only. Cutoff-based evidence (§12) shows inflated in-sample accuracy* |
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

## 12. Sources added 2026-10-07 (owner upload: look-ahead contamination and LLM agent behaviour)

Context: `S4_LIT_LOOKAHEAD_2026-10-07.md`. Two retrievals were made with the owner's per-item permission (D-4): the arXiv v3 HTML of P1 and the P3 procedure file. Both were read through a summarising fetch and neither is archived locally.

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Henning, Ojha, Spoon, Han & Camerer, "LLM Agents Do Not Replicate Human Market Traders: Evidence From Experimental Finance", arXiv 2502.15800 **v3** (11 Oct 2025) | AVAILABLE (v1 local; v3 read online, newest) · preprint · **PARTIAL** | v1: owner upload, md5 1b1814ab1025; v3: arxiv.org/html/2502.15800v3 | RQ-56, RQ-55, RQ-22 |
| Liang, "Look-Ahead Bias in Financial Forecasts Generated by Large Language Models", 9 May 2026 | AVAILABLE · working paper · **PARTIAL** | Owner upload, md5 750513a6f17d | RQ-26 |
| Gao, Jiang & Yan, "Detecting Lookahead Bias in LLM Forecasts", arXiv 2512.23847 **v2** (12 Jun 2026) | AVAILABLE (newest) · preprint · **FITS** | Owner upload, md5 7a282ef636dd | RQ-26, RQ-37; DR-10 |
| Gao, Jiang & Yan, `CLAUDE.md` procedure file (undated) | READ (data only; never executed) | yutongyan.xyz/files/lookahead_bias_test/CLAUDE.md (linked from P3 PDF pp. 1, 51) | S7 diagnostic X-1 |
| Didisheim, Fraschini & Somoza, "AI's predictable memory in financial analysis", *Economics Letters* 256 (2025) 112602 | AVAILABLE · peer-reviewed · **FITS** | Owner upload, md5 132d26281a67 | RQ-26, RQ-55; X-2, X-3 |
| "Assessing Look-Ahead Bias … GPT Sentiment Analysis 2.pdf" | DUPLICATE | md5 04a5203b0b35 = Glasserman & Lin (2023), §11 | — |

## 13. Sources added 2026-10-08 (owner uploads; permitted download; S4.4)

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Michaud (1989), "The Markowitz Optimization Enigma: Is 'Optimized' Optimal?", *FAJ* 45(1):31–42 — JSTOR copy with text layer | AVAILABLE (published version; read in full) | Owner upload, `Finsol Research Papers/The Markowitz optimization enigma- Is ‘optimized’ optimal?.pdf`, 13 pp. incl. JSTOR cover, md5 28cd76210bbf. Supersedes the image scan of §2 for text extraction | S4.6; PC-B4 motivation (not its procedure); `S4_RISK_MODEL_CHOICE.md` |
| Kirby & Ostdiek, "It's All in the Timing: Simple Active Portfolio Strategies that Outperform Naïve Diversification" — working version, 9 May 2010 (initial draft 18 Nov 2009) | AVAILABLE (working version; the *JFQA* 47(2) version governs, D-3) | Owner upload, `Finsol Research Papers/It’s All in the Timing- … .pdf`, 43 pp., md5 8da209076a0e | PC-A3, PC-A4 (ANG-13 resolved) |
| Maillard, Roncalli & Teïletche, "On the Properties of Equally-Weighted Risk Contributions Portfolios" — working version, May 2009 (first version June 2008) | AVAILABLE (working version; the *JPM* 36(4) version governs) | Downloaded 2026-10-08 with owner permission from thierry-roncalli.com/download/erc.pdf (author-hosted) to `Finsol Research Papers/Downloaded 2026-10-08/MRT2010_ERC/erc.pdf`, 23 pp., md5 885b0373e72c | PC-C2 |
| B. Gerard, "Constructing an Optimal Active Portfolio & the Optimal Active Share in an Overall Portfolio", GRA 6531 course note, BI, 13 Jan 2026 | SECONDARY (teaching material) | `RPT/Portfolio Optimization /Optimal Combination of New Investments w- Existing Ptf - Treynor Black Approach.pdf`, 8 pp., md5 7295450f59a2 | PC-D4 weight mechanics (lead) |
| Michaud & Michaud (2008), "Estimation Error and Portfolio Optimization: A Resampling Solution", *JOIM* 6(1) | MISSING — LOCATED (JOIM, free guest account; authors' pre-publication copy open at New Frontier Advisors) | — | PC-B4 procedure (governing) |
| Michaud & Michaud (2008), *Efficient Asset Management: A Practical Guide to Stock Portfolio Optimization and Asset Allocation*, 2nd ed., Oxford University Press | AVAILABLE (book; read ch. 6 front pages for S4.4; **read in full, ch. 1–12 and epilogue, 2026-10-15**) | Owner upload, `Finsol Research Papers/Efficient Asset Management.pdf`, 145 pp., md5 d1ae84ec9ade | PC-B4 procedure (governing): ch. 6, pp. 42–58; App. A p. 56. p. 42 fn. 1: patented procedure, exclusive licensee |
| Varadi, Kapler, Bee & Rittenhouse (2012), minimum correlation — authors' channels | LOCATED (identity route) | Release post, CSS Analytics blog, 21 Sep 2012; authors' Scribd upload doc 106570475; author spreadsheet; co-author R code (`min.corr.portfolio`, `min.corr2.portfolio`) | PC-C5 (ANG-38) |
| Varadi, Kapler, Bee & Rittenhouse (2012), *The Minimum Correlation Algorithm: A Practical Diversification Tool*, CSS Analytics, September 2012 | AVAILABLE (authors' release; identity confirmed 2026-10-08) | Owner upload, `Finsol Research Papers/ 1 The Minimum Correlation Algorithm- A Practical Diversification Tool.pdf`, 91 pp., md5 c56c05f40ef4 (byte-identical to the rybn.org mirror) | PC-C5; source issues MCA-1 … MCA-3 |
| Kapler, Systematic Investor Toolbox `R/strategy.r` (`min.corr`, `min.corr2`) | READ via the web (never executed) | github.com/systematicinvestor/SIT | PC-C5 cross-check |
| Moreira & Muir (2017), *JF* 72(4):1611–1644 | AVAILABLE (re-supplied by the owner as a zip; same published file as §3) | `RPT/Downside Risk/Volatility-Managed Portfolios.pdf`, md5 4e9dbe517e91 | PC-A5 |

SSRN refused scripted access and showed a security verification in the in-app browser; it was not bypassed. The remaining permitted SSRN items are listed for manual download in `S4_PC_SOURCE_MAP.md` §6.

## 14. Sources added 2026-10-08, third round (owner uploads: the six SSRN items)

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| He & Litterman (1999), GSAM working paper (PDF of 2002) | AVAILABLE · reviewed · reproduced | `Finsol Research Papers/The Intuition Behind Black-Litterman Model Portfolios.pdf`, 27 pp., md5 a03589438332 | PC-B2 |
| Idzorek, draft of 26 Apr 2005 (SSRN 3479867) | AVAILABLE · reviewed · reproduced | `Finsol Research Papers/ Add Paper to My Library Share- … Confidence Levels.pdf` (file name carries SSRN page text), 34 pp., md5 cf1ee81ea46d | PC-B2 |
| Spinu (2013), SSRN 2297383 | AVAILABLE · reviewed · reproduced | `Finsol Research Papers/An Algorithm for Computing Risk Parity Weight.pdf`, 6 pp., md5 7152aad7f6f6 | PC-C2 |
| López de Prado (2016), version of 23 May 2016 | AVAILABLE (working version; *JPM* governs) · reviewed · Exhibit 7 reproduced | `Finsol Research Papers/Building Diversified Portfolios that Outperform Out-of-Sample.pdf`, 31 pp., md5 575345cad8d5 | PC-C3 |
| Chekhlov, Uryasev & Zabarankin, UF report 2003-15 (25 Jun 2003) | AVAILABLE (working version; *IJTAF* governs) · reviewed | `Finsol Research Papers/Drawdown Measure in Portfolio Optimization.pdf`, 41 pp., md5 597c81fcff3f | PC-D2 |
| Boudt, Carl & Peterson, version of 24 May 2012 | AVAILABLE (working version; *J. Risk* governs) · reviewed | `Finsol Research Papers/Asset Allocation with Conditional Value-at-Risk Budgets.pdf`, 36 pp., md5 a6b28ba66935 | PC-D3 |

Reviews and reproductions: `S4_SOURCE_REVIEWS_2026-10-08.md`; scripts `verification/s44_*.py`.

## 15. Sources added 2026-10-08, fifth round (owner uploads: the four BI items and Treynor & Black)

Identity checked against title page, journal, volume and pages; md5 of the PDF inside each zip.

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Goldfarb & Iyengar (2003), *Math. Oper. Res.* 28(1):1–38 | AVAILABLE (published, JSTOR) | `Finsol Research Papers/Robust Portfolio Selection Problems.pdf`, 39 pp., md5 09a33510a521 | PC-B3 (S4.7) |
| Clarke, de Silva & Thorley (**2011**), "Minimum-Variance Portfolio Composition", *JPM* 37(2):31–45 | AVAILABLE (published) · **not the cited paper** | `Finsol Research Papers/Minimum-Variance Portfolio Composition.pdf`, 15 pp., md5 925a66809d51 | PC-C1, **supporting** only. ANG cites CdST **2006**, "Minimum-Variance Portfolios in the U.S. Equity Market", *JPM* 33(1):10–24 (ANG references). The 2006 paper is still needed (S4.11) |
| Choueifaty & Coignard (2008), "Toward Maximum Diversification", *JPM* 35(1) (Fall 2008):40–51 | AVAILABLE (published) | `Finsol Research Papers/Toward Maximum Diversification.pdf`, 12 pp., md5 6c2a655f2c23 | PC-C4 (S4.11) |
| Rockafellar & Uryasev, "Optimization of Conditional Value-at-Risk" | AVAILABLE (author version, pdfTeX, with numerical tables; the published *J. Risk* 2(3):21–41 governs, D-3) | `Finsol Research Papers/Optimization of Conditional Value-at-Risk.pdf`, 26 pp., md5 ee8f86ef5b31 | PC-D1 (S4.12) |
| Treynor & Black (1973), "How to Use Security Analysis to Improve Portfolio Selection", *J. Business* 46(1):66–86 | AVAILABLE (published, JSTOR) | `Finsol Research Papers/How to Use Security Analysis to Improve Portfolio Selection.pdf`, 22 pp., md5 4a0b5496a175 | PC-D4 primary for appraisal-ratio sizing (S4.12) |
| Clarke, de Silva & Thorley (**2006**), "Minimum-Variance Portfolios in the U.S. Equity Market", *JPM* 33(1) (Fall 2006):10–24 | AVAILABLE (published; image scan, no text layer) · added 2026-10-08 (sixth upload) | `Finsol Research Papers/Minimum-Variance Portfolios in the U.S. Equity Market.pdf`, 14 PDF pages, md5 8c12d860cd02. Contents: article pp. 10, 12, 14–24, plus p. 4 of the issue (unrelated). pp. 11 and 13 are absent, but the text runs on mid-sentence across both gaps (p. 10 → 12, p. 12 → 14), Exhibits 1–2 (first cited p. 14) are on p. 15, and the article ends on p. 24 with its references, so no article content is missing (the two pages were most likely advertisements; INFERENCE) | PC-C1 governing source (S4.11) |

Result: 21 of 22 governing PC sources in hand (`S4_PC_SOURCE_MAP.md` §1). Open: CdST 2006 (PC-C1). *[2026-10-08, later]* CdST 2006 received and verified: **all 22 governing PC sources in hand.**

## 16. Sources added 2026-10-15 (owner uploads: Paleologo 2025; the S4.8 momentum and trend set; Michaud monitoring application)

Identity checked against title page, version and page count; md5 of the PDF inside each zip (of the zip for the EPUB). As the owner asked, the papers are read when their step needs them; "identity only" means not yet read.

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Paleologo (2025), *The Elements of Quantitative Investing*, Wiley, 1st ed., ISBN 9781394265466 | AVAILABLE (EPUB) · read: ch. 2 in full (incl. App. 2.4), ch. 5 §5.1, ch. 6 §6.3–6.4 and p. 135, ch. 9 §9.5–9.6; other chapters not read | `~/Desktop/The Elements of Quantitative Investing.epub.zip`, md5 da184634cc3f | S4.8 (EWMA and trend filters), S7 and S10 (volatility losses; short-term volatility updating); issues PAL-1 … PAL-8 (`ANG_ISSUES_REGISTER.md`); `verification/s48_kalman_ewma_paleologo.py` (PASS) |
| Ang (2023), "Trends and Cycles of Style Factors in the 20th and 21st Centuries", *JPM*, Quantitative Special Issue 2023 | AVAILABLE (published; volume and pages to confirm) · identity only | `Finsol Research Papers/Trends and Cycles of Style Factors in the 20th and 21st Centuries.pdf`, 25 pp., md5 770cc536dee5 | S4.8 (supporting: trend–cycle filters; the Hodrick–Prescott filter is two-sided), S9a (regimes, factor cycles) |
| Bruder, Dao, Richard & Roncalli (2011), "Trend Filtering Methods for Momentum Strategies", Lyxor R&D, December 2011 (SSRN 2289097) | AVAILABLE (working paper; no later version known) · read for S4.8, 2026-10-15 (construction sections; `S4_MOMENTUM.md` §1) | `…/Trend Filtering Methods for Momentum Strategies.pdf`, 49 pp., md5 8f7106e1a709 | S4.8 (TSMOM filters: linear incl. Kalman, non-linear incl. L1) |
| Huang, "The Momentum Gap and Return Predictability", version of 11 Sep 2021 | AVAILABLE (working version; the *RFS* 2022 published version governs and is not in hand) · identity only | `…/The Momentum Gap.pdf`, 57 pp., md5 abdb3aced9b1 | S4.8 (conditioning of XSMOM; registered for S9/S13) |
| Blitz, Huij & Martens (2011), "Residual Momentum", *JEF* 18(3) | AVAILABLE (accepted manuscript, doi 10.1016/j.jempfin.2011.01.003; the published version governs) · read for S4.8, 2026-10-15 (construction sections; `S4_MOMENTUM.md` §1) | `…/Residual Momentum.pdf`, 61 pp., md5 592eb60dd285 | S4.8 (XSMOM construction variant) |
| Novy-Marx, "Fundamentally, Momentum Is Fundamental Momentum", version of 5 Mar 2015 (NBER w20984) | AVAILABLE (working paper) · identity only | `…/Fundamentally, momentum is fundamental momentum.pdf`, 45 pp., md5 17bdbadef248 | S9c (earnings momentum; needs point-in-time quarterly earnings with announcement dates, S6) |
| Gupta & Kelly (2019), "Factor Momentum Everywhere", *JPM*, Quantitative Special Issue 2019 | AVAILABLE (published) · read for S4.8, 2026-10-15 (construction sections; `S4_MOMENTUM.md` §1) | `…/Factor Momentum Everywhere .pdf`, 26 pp., md5 5a964230d581 | S4.8 (TSMOM applied to factor returns), S9 |
| Ehsani & Linnainmaa, "Factor Momentum and the Momentum Factor", NBER WP 25551, February 2019 | AVAILABLE (working version) · read for S4.8, 2026-10-15 (construction sections; `S4_MOMENTUM.md` §1) · **newer version exists:** *JF* 77(3) (2022), which governs under the newest-version rule; requested | `…/Factor Momentum and the Momentum Factor.pdf`, 54 pp., md5 b3d8c5ec4392 | S4.8, S9 |
| Michaud, Michaud & Esch, US 2012/0116994 A1, "Dynamic Portfolio Monitoring" (filed 2011-09-16; priority 2010-09-17) | AVAILABLE (patent application publication; abandoned per Google Patents) · identity only | `…/Dynamic Portfolio Monitoring.pdf`, 16 pp., md5 65444c74ace8 | S13b (need-to-trade threshold for successive datasets; S47-D7) |
| Levine & Pedersen (2016), "Which Trend Is Your Friend?", *FAJ* 72(3):51–66 | **MISSING — LOCATED** (open publisher's version on the CBS research portal) | — | S4.8 (equivalence of trend filters incl. Kalman and HP) |

Patent texts for the closed Michaud family (US 6,003,018; 6,928,418; 7,412,414; 7,624,060) are public on Google Patents and are read when S13b specifies the need-to-trade rule (S47-D7).

## 17. Sources added 2026-10-18 (owner uploads: S4.9 alpha mapping and transfer coefficient)

Identity checked against title page, page count and content; md5 of the PDF inside each zip (zip md5 in brackets). Scanned or font-garbled pages were read from rendered page images.

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Grinold (1994), "Alpha is Volatility Times IC Times Score", *JPM* 20(4) (Summer):9–16 | AVAILABLE (published; ProQuest scan) · read in full 2026-10-18 | `Finsol Research Papers/Alpha is volatility times IC times score.pdf.zip`, 8 pp., md5 65257025e2d7 (zip 751c1e63bc57) | EQ-MAP-3 (primary predecessor); R-1, R-2, R-7c; issues GRI-1, GRI-2; `verification/s49_alpha_sources.py` (PASS) |
| Clarke, de Silva & Thorley (2002), "Portfolio Constraints and the Fundamental Law of Active Management", *FAJ* 58(5):48–66 | AVAILABLE (published; Taylor & Francis re-host) · read in full 2026-10-18 | `…/Portfolio Constraints and the Fundamental Law ofActive Management.pdf.zip`, 20 pp., md5 259e5b289c0e (zip 01cb1ee3427f) | EQ-TC-1; R-7a; S4.16 (diagnostic), S13 (turnover), S17 (ex post decomposition) |
| Grinold & Kahn, *Advances in Active Portfolio Management* (McGraw-Hill; companion and successor to *Active Portfolio Management*; publication year to confirm, the copy has no copyright page; text written about 2019) | AVAILABLE (printed to PDF; equations and exhibits are images) · read: ch. 3 Insights 4–5 (incl. eqs. 19–20, 35–37, Exhibit 11, the four examples); ch. 6–7 and ch. 9 introductions; contents. Other chapters not read | `…/Advances in Active Portfolio Management.pdf.zip`, 801 pp., md5 096bdb504af3 (zip e821d8c6b641) | **Governing version** for EQ-MAP-3 and EQ-TC-1. Later steps: ch. 9 Signal Weighting (S9d, RQ-32, S48-D6); ch. 20 benchmark efficiency (S4.10); ch. 32 mean–variance vs scenarios (S4.12); ch. 27 downside risk (S4.12); ch. 29 optimal gearing (EQ-SPLIT-1); ch. 7–11 dynamic portfolios and trading rules (S13); ch. 13 attribution (S17); ch. 16 equity premium (S9b); ch. 21–25 smart beta (RQ-28, RQ-32) |
| Gallego, IEOR4706 Financial Engineering I, Lecture 7 "Active Portfolio Management" (Columbia, Autumn 2000) | AVAILABLE · secondary teaching note "based on" Grinold & Kahn; **not** the book · read in full 2026-10-18 | `…/Active Portfolio Management.pdf.zip`, 7 pp., md5 b46f3e4e3379 (zip 9a5127fd6e6a) | R-2 (benchmark alpha-neutrality), secondary; issue LEC-1 |
| Grinold & Kahn, *Active Portfolio Management*, 2nd ed. (McGraw-Hill, 1999/2000) | MISSING · low priority (forecasting rule and fundamental law now covered by Grinold 1994, *Advances* ch. 3 and CdST App. A; still useful for alpha refinement: trimming, factor and cash neutralisation) | — | R-2 (S9d) |
| Grinold (1989), "The Fundamental Law of Active Management", *JPM* 15(3):30–37 | MISSING · low priority (proof reproduced in CdST App. A) | — | EQ-TC-1 |
| Leads for the research-lane constructions (S49-D1), from memory, not verified: Baltas (2015) on trend following with correlation-aware risk parity; Bai, Scheinberg & Tütüncü (2016) on risk parity by orthant | NOT LOCATED | — | Admissibility review of the research-lane constructions (S4.14) |
| Faber (2007), "A Quantitative Approach to Tactical Asset Allocation" (equal-weight trend timing; from memory, not verified) | NOT LOCATED · optional | — | Supporting the V1 cell A1 × O3, long-only version |

## 18. Sources added 2026-10-18, second round (owner uploads: S4.10 benchmark sources)

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Roll (1992), "A Mean/Variance Analysis of Tracking Error", *JPM* 18(4) (Summer):13–22 | AVAILABLE (published; scan) · read in full 2026-10-18 | `Finsol Research Papers/A Mean:Variance Analysis of Tracking Error.pdf.zip`, 10 pp., md5 72aacfe8d9c7 (zip 6035a5943b58) | EQ-TEV-1; S410-D6; issue ROLL-1 |
| Jorion (2003), "Portfolio Optimization with Tracking-Error Constraints", *FAJ* 59(5):70–82 | AVAILABLE (published) · read in full 2026-10-18 | `…/Portfolio Optimization with Tracking-Error Constraints.pdf.zip`, 13 pp., md5 95459d8a7589 (zip 321bd35eb785) | EQ-TEV-2; S410-D6 |
| Grinold & Kahn, *Advances*, ch. 20 "Are Benchmark Portfolios Efficient?" (Grinold 1992, revised October 2018) | In hand (§17) · read 2026-10-18 | — | EQ-GRS-1; issue GKA-1 |
| Gibbons, Ross & Shanken (1989), "A Test of the Efficiency of a Given Portfolio", *Econometrica* 57 | MISSING · optional (only if the GRS diagnostic is adopted at S7/S16) | — | EQ-GRS-1 |
| Global multi-asset market-portfolio weights (lead from memory, not verified: Doeswijk, Lam & Swinkels 2014) | NOT LOCATED · needed only for an asset-class market-capitalisation anchor | — | S410-D2/D3; S6 |

## 19. Sources read 2026-10-18 for S4.12a (existing library; no new uploads)

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Rockafellar & Uryasev, "Optimization of Conditional Value-at-Risk", *J. Risk* 2(3), 2000 | AVAILABLE (preprint dated 5 Sep 1999; the published version governs) · read in full 2026-10-18 | `Finsol Research Papers/Optimization of Conditional Value-at-Risk.pdf`, 26 pp., md5 ee8f86ef5b31 | PC-D1; EQ-NT-1; RU-1 … RU-3 |
| Rockafellar & Uryasev, "Conditional value-at-risk for general loss distributions", *J. Banking & Finance* 26, 2002 | MISSING · optional (formal result for discrete scenarios; RU-2 verified numerically) | — | EQ-NT-1 |
| Sortino & van der Meer, "Downside Risk", *JPM* 17(4) (Summer 1991):27–31 | AVAILABLE (scan) · read in full from page images 2026-10-18 | RPT/Downside Risk/Downside Risk.pdf, md5 b1756aecbd53 | PC-B5; EQ-DS-1; SVDM-1 |
| Markowitz, Todd, Xu & Yamane, "Computation of mean-semivariance efficient sets by the Critical Line Algorithm", *Ann. Oper. Res.* 45:307–317, 1993 | AVAILABLE (published) · read in full | RPT/Portfolio Optimization /Computation of mean-semivariance efficient sets.pdf, 12 pp., md5 edc9c17c056a | PC-B5; EQ-DS-1, EQ-DS-2 |
| Cesarone, Corradini, Giunta & Lampariello, "Semivariance, semicovariance matrix and lower partial moments for portfolio selection: Analytical and numerical results", *Finance Research Letters* 91:109424, 2026 (CC BY) | AVAILABLE (published) · §1–§5 read | RPT/Portfolio Optimization /Semivariance, semicovariance matrix and lower partial moments for portfolio selection.pdf, 12 pp., md5 1807243dfd4b | PC-B5; EQ-DS-2 |
| Estrada, "Mean-Semivariance Optimization: A Heuristic Approach", *J. Appl. Finance* 18(1), 2008 | AVAILABLE (published) · method sections read | RPT/Portfolio Optimization /Mean-Semivariance Optimization- A Heuristic Approach.pdf, 16 pp., md5 5e1e193381c9 | PC-B5 (heuristic, not adopted) |
| Grinold & Kahn, *Advances*, ch. 26–28 intros; ch. 27 Kahn & Stefek "Heat, Light, and Downside Risk" (BARRA white paper, Dec 1996); ch. 32 Grinold "Mean-Variance and Scenario-Based Approaches to Portfolio Selection" (revision of *JPM* Winter 1999:10–22) | In hand (§17) · read in full 2026-10-18 | PDF pp. 559–591, 592–595, 664–686 | EQ-DS-1 (A5–A10); EQ-SCN-1; KS-1 |
| Sortino & Price, "Performance Measurement in a Downside Risk Framework", *J. Investing* 3(3):59–64, 1994 | MISSING · optional (defines the Sortino ratio; cited by Kahn & Stefek and Nassar & Ephrem) | — | PC-B5 (ratio citation) |
| Boudt, Peterson & Croux (2008), modified ES | MISSING · optional | — | PC-D3 (modified CVaR) |
| Hogan & Warren (1974), *JFQA* 9(1):1–11; Cumova & Nawrocki (2014), *J. Econ. Bus.* 71:68–89; Sortino, van der Meer & Plantinga, "The Dutch Triangle", *JPM* Fall 1999 (scan); Landsman, Makov, Yao & Zhou (2022), *Eur. J. Finance*; Nassar & Ephrem (2020 note); Martin, Ulcer Index (web page) | AVAILABLE · identity only (not needed for S4.12a) | RPT/Downside Risk/, RPT/Sortino/; md5 87a2fdc97bc1, b332fbb6b9ca, 98df2daee861, 3321ff3e5148, dc0d83bf1fd7, abc68548f4a5 | PC-B5, PC-D2 context |

## 20. Sources read 2026-10-18 for S4.12b (existing library; no new uploads)

| Source | Status | Location / identity | Maps to |
|---|---|---|---|
| Treynor & Black (1973), *J. Business* 46(1):66–86 | AVAILABLE (published, JSTOR) · **read in full 2026-10-18** | `Finsol Research Papers/How to Use Security Analysis to Improve Portfolio Selection.pdf`, 22 pp., md5 4a0b5496a175 | PC-D4 sizing; EQ-NT-4; TB-1; primary form of EQ-MAP-3 (eq. 28) |
| Ang, Brandt & Denison (2014) | In hand (§ PC-D4 row) · §III.C and App. B–C re-read 2026-10-18 | md5 da26aa3090d0 | EQ-NT-4; TPA-1, TPA-2 |
| AQR (2026), *Alternative Thinking* Issue 2 | In hand · pp. 3–16 re-read 2026-10-18 | md5 16bf8f961f21 | EQ-NT-4 (fns. 11–12) |
| Gerard, GRA 6531 note (2026) | SECONDARY · read 2026-10-18 | md5 7295450f59a2 | Teaching derivation; nothing new |
| Cavaglia, Han & Seshadri (2026), "Applying the Appraisal Ratio and Style Analysis to Total Portfolio Management", *JPM* 52(6); Elkamhi & Lee (2025), "Total Portfolio Approach", *JPM* 51(8) (both cited by AQR) | MISSING · optional | — | PC-D4 variants (gap memo §10) *[2026-10-19]* Obtained with Gilmore & Simonian 2025: §21 |

## 21. Sources added 2026-10-19 (owner uploads: the three TPA papers; S4.12b)

Each arrived as a zip and was extracted into its own empty scratch directory before reading. Read 2026-10-18 for the S412-D4 discussion; findings in `S4_NON_TRADITIONAL.md` §9.8.

| Source | Status | Location / identity (md5 zip / pdf) | Maps to |
|---|---|---|---|
| Gilmore & Simonian (2025), "Some Practical Considerations for the Total Portfolio Approach to Pension Fund Management", *JPM* 51(10):40–48 (*Future of Asset Management 2025*) | AVAILABLE (published) · read in full | `Finsol Research Papers/Some Practical Considerations for the Total Portfolio Approach to Pension Fund Management.pdf.zip`, 10 pp., `9f42284f7dd0` / `a2598d982802` | PC-D4 (§9.8); ANG-15, ANG-22 (cited in ANG §3.3) |
| Elkamhi & Lee (2025), "Total Portfolio Approach", *JPM* 51(8) (*Portfolio Manager Perspectives 2025*, pp. 110 ff.) | AVAILABLE (published) · read in full | `Finsol Research Papers/Total Portfolio Approach.pdf.zip`, 20 pp., `9a04b3d83470` / `8f7d10133090` | PC-D4 (§9.8) |
| Cavaglia, Han & Seshadri (2026), "Applying the Appraisal Ratio and Style Analysis to Total Portfolio Management", *JPM* 52(6), April 2026 (pp. 74 ff.) | AVAILABLE (published) · read in full; AR section pp. 75–76 re-checked 2026-10-19 | `Finsol Research Papers/Applying the Appraisal Ratio and Style Analysis to Total Portfolio Management.pdf.zip`, 26 pp., `debdd580831d` / `017eb7e9302a` | PC-D4 (§9.8); funding-report lens (S4.16); single-candidate weight verified (`s412b_tpa.py`) |

## 22. Sources located 2026-10-19 (bibliographic records only; not obtained, not read)

Identified during the owner's methodological review of 2026-10-19 (areas 3, 5 and 8). Status `MISSING — LOCATED`: identity and venue checked against a publisher, index or author record; no copy in the library. They are evidence leads for the stages named, not adopted methods.

| Source | Status | Location | Maps to |
|---|---|---|---|
| Brock, Lakonishok & LeBaron (1992), "Simple Technical Trading Rules and the Stochastic Properties of Stock Returns", *JF* 47(5):1731–1764 | MISSING — LOCATED | [RePEc](https://ideas.repec.org/a/bla/jfinan/v47y1992i5p1731-64.html) | S4.15b T6; RQ-35 |
| Sullivan, Timmermann & White (1999), "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap", *JF* 54(5):1647–1691 | MISSING — LOCATED | [LSE FMG discussion paper 303](https://ideas.repec.org/p/fmg/fmgdps/dp303.html) | T6, T12; RQ-35 |
| Lo, Mamaysky & Wang (2000), "Foundations of Technical Analysis", *JF* 55(4):1705–1765 | MISSING — LOCATED | [NBER w7613](https://www.nber.org/papers/w7613) | T6 (chart patterns); RQ-35 |
| Park & Irwin (2007), "What Do We Know About the Profitability of Technical Analysis?", *J. Economic Surveys* 21(4):786–826 | MISSING — LOCATED | [RePEc](https://ideas.repec.org/a/bla/jecsur/v21y2007i4p786-826.html) | T6 (survey) |
| Zhu & Zhou (2009), "Technical Analysis: An Asset Allocation Perspective on the Use of Moving Averages", *JFE* 92(3):519–544 | MISSING — LOCATED | [Author record](https://profiles.wustl.edu/en/publications/technical-analysis-an-asset-allocation-perspective-on-the-use-of-/) | T6 |
| Bajgrowicz & Scaillet (2012), "Technical Trading Revisited: False Discoveries, Persistence Tests, and Transaction Costs", *JFE* 106(3):473–491 | MISSING — LOCATED | [RePEc](https://ideas.repec.org/a/eee/jfinec/v106y2012i3p473-491.html) | T6, T12; RQ-35 |
| Han, Yang & Zhou (2013), "A New Anomaly: The Cross-Sectional Profitability of Technical Analysis", *JFQA* 48(5):1433–1461 | MISSING — LOCATED | [RePEc](https://ideas.repec.org/a/cup/jfinqa/v48y2013i05p1433-1461_00.html) | T6 |
| Neely, Rapach, Tu & Zhou (2014), "Forecasting the Equity Risk Premium: The Role of Technical Indicators", *Management Science* 60(7):1772–1791 | MISSING — LOCATED | [Author record](https://profiles.wustl.edu/en/publications/forecasting-the-equity-risk-premium-the-role-of-technical-indicat/) | T6; S9a |
| White (2000), "A Reality Check for Data Snooping", *Econometrica* 68(5):1097–1126 | MISSING — LOCATED | Index record (Econometrica) | T12; S7 |
| Hansen (2005), "A Test for Superior Predictive Ability", *J. Business & Economic Statistics* 23(4):365–380 | MISSING — LOCATED | Index record (JBES) | T12; S7 |
| Romano & Wolf (2005), "Stepwise Multiple Testing as Formalized Data Snooping", *Econometrica* 73(4):1237–1282 | MISSING — LOCATED | [Econometric Society](https://www.econometricsociety.org/publications/econometrica/browse/2005/07/01/stepwise-multiple-testing-formalized-data-snooping) | T12; S7 |
| Benjamini & Hochberg (1995), "Controlling the False Discovery Rate", *JRSS B* 57(1):289–300 | MISSING — LOCATED | Index record (JRSS B) | T12; S7 |
| Bailey & López de Prado (2014), "The Deflated Sharpe Ratio", *JPM* 40(5):94–107 | MISSING — LOCATED (open working paper) | [SSRN 2460551](https://papers.ssrn.com/abstract=2460551) | T12; RQ-37 D-4 |
| Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting", *J. Computational Finance* 20(4):39–69 | MISSING — LOCATED (open working paper) | [SSRN 2326253](https://papers.ssrn.com/abstract=2326253) | T12; S7 |
| Alford (1992), "The Effect of the Set of Comparable Firms on the Accuracy of the Price-Earnings Valuation Method", *J. Accounting Research* 30(1):94–108 | MISSING — LOCATED | [RePEc](https://ideas.repec.org/a/bla/joares/v30y1992i1p94-108.html) | RQ-30 note (pricing accuracy, not return prediction) |
| Liu, Nissim & Thomas (2002), "Equity Valuation Using Multiples", *J. Accounting Research* 40(1):135–172 | MISSING — LOCATED | [RePEc](https://ideas.repec.org/a/bla/joares/v40y2002i1p135-172.html) | RQ-30 note (pricing accuracy, not return prediction) |
| Asness, Porter & Stevens (2000), "Predicting Stock Returns Using Industry-Relative Firm Characteristics", AQR working paper (not peer-reviewed) | MISSING — LOCATED (open) | [AQR](https://www.aqr.com/Insights/Research/Working-Paper/Predicting-Stock-Returns-Using-IndustryRelative-Firm-Characteristics) | S9c candidate: within- and across-industry components (RQ-30) |
| Ball, Gerakos, Linnainmaa & Nikolaev (2016), "Accruals, Cash Flows, and Operating Profitability in the Cross Section of Stock Returns", *JFE* 121(1):28–45 | MISSING — LOCATED (author copy) | [Author copy](https://faculty.tuck.dartmouth.edu/images/uploads/faculty/joseph-gerakos/Ball,_Gerakos,_Linnainmaa,_et_al._2016.pdf) | S9c candidate: cash-based operating profitability (RQ-28) |

## 23. Sources added 2026-10-25 (owner upload; STOXX downloads with the owner's per-item permission)

The July paper arrived as a zip and was extracted into its own empty scratch directory; the August whitepaper and the methodology guide were downloaded on 2026-10-25 into separate empty directories. Owner decision 2026-10-25: reference specification for the multifactor composite (construction only; FinSol uses its own universe and datasets). The methodology guide is the newest, rule-level source; the July paper is the only source for the market-similarity configuration (App. C). All three are SECONDARY (index-provider material, not peer-reviewed).

| Source | Status | Location / identity (md5 zip / pdf) | Maps to |
|---|---|---|---|
| Renshaw, Gu, Candar & Ang (July 2026), "Diversification all the way down: Multifactor investing within factors, across factors and across time", STOXX research paper | AVAILABLE · read in full 2026-10-24 | `Finsol Research Papers/Diversification all the Way Down- Multifactor Investing Within Factors, Across Factors and Across Time.pdf.zip`, 40 pp., `66921059025e` / `8828567fbd66` | RQ-11, RQ-28, RQ-31, RQ-32; S48-D6 |
| Renshaw, Gu, Candar & Ang (August 2026), "Real-world diversification in multifactor indices", STOXX whitepaper | AVAILABLE · read in full 2026-10-25; result tables identical to the July paper; omits App. C and the bibliography | STOXX website PDF, 15 pp., `aa7059c760c3` | as above |
| STOXX, *iSTOXX Equity Indices Methodology Guide*, §118 "iSTOXX Ang Research Enhanced Index Family" (version of 13 Oct 2026) | AVAILABLE · §118 read in full 2026-10-25 | STOXX website PDF, 833 pp., `5132886537fc` | as above (rule-level construction) |
| Eisfeldt, Kim & Papanikolaou, "Intangible Value", NBER WP 28056 (version of Nov 2021) | AVAILABLE (working version; *Critical Finance Review* 11(2):299–332, 2022 governs) · §2.2 read 2026-10-25 (capitalisation convention: perpetual inventory of SG&A, δ = 0.2, initial stock SG&A/(g + δ), g = 0.1; goodwill removed) | NBER PDF (open), 68 pp., `5c861121091e`; downloaded with owner permission | Intangible asset ratio, O-R5 |
| Stewart (2009), "EVA Momentum: The One Ratio That Tells the Whole Story", *J. Applied Corporate Finance* 21(2):74–86 | MISSING — LOCATED (no legitimate open copy; owner to supply) | RePEc record | Signal 9; O-R4 |
| Lev & Sougiannis (1996), "The Capitalization, Amortization, and Value-Relevance of R&D", *J. Accounting and Economics* 21:107–138 | MISSING — LOCATED (owner to supply) | RePEc record | O-R5 |
| Sloan (1996), "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?", *Accounting Review* 71(3):289–315 | MISSING — LOCATED (only a re-hosted JSTOR copy found, not used; owner to supply) | Index record | Signal 18; O-R6 |
