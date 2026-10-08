# S4 record — risk-model choice: how much it matters, whether one model is better, how and when we choose

**Document status:** DRAFT (S4 record, 2026-10-08). Nothing is selected here; selection is S10 → G10. · **Feeds:** S4.13, S4.16, S4.20, S7, S10 (RQ-14), S11, S8, S17. · **Basis:**
- owner question 2026-10-08: the risk model "has a large effect on the optimizers, especially the mean-variance based ones (see Michaud 1989)"; establish (a) whether any risk model is better, (b) which to choose, (c) at what stage and how;
- ADR-0027 D3 r3 (Option A, owner decision 2026-10-08): one authoritative risk model per problem (universe × horizon × risk object).

**Evidence labels:**
- `VERIFIED-SOURCE`: primary text read (ANG v2; Pedersen, Babu & Levine 2021; the third-party code);
- `VERIFIED-ABSTRACT`: abstract read at the publisher, NBER or RePEc;
- `VERIFIED-SECONDARY`: only described by other authors; full text not read;
- `VERIFIED-DERIVATION`: our synthetic computation (Appendix; one design; illustrative).

## 0. Short answer
- **The risk model is a first-order governance item.**
  - It is the only input to risk-based methods (minimum variance, risk parity, maximum diversification, HRP).
  - It drives every risk limit and risk report.
  - It changes recommendations materially in unconstrained and high-dimensional problems.
- **It is not the dominant input in general.**
  - For mean–variance methods the dominant error source is expected returns. The covariance matrix matters mostly through how much it amplifies or dampens those errors (Michaud's "error maximisation").
  - In long-only, bounded asset-class allocation (ANG's setting), the choice among reasonable estimators changed the loss by ≤ 2 bp/yr and moved 2–5% of the weights (M-1).
- **(a)** No estimator is best everywhere. The ranking depends on dimension, sample length, horizon, constraints and the use. Some estimators are reliably poor in specific problems (§2).
- **(b)** Choose per problem by a pre-registered out-of-sample risk-accuracy test. Leading candidates per problem are in §3.
- **(c)** Decided at S10 → G10 under the S7 protocol; inventoried in S4.13; implemented in S8 as the risk role's versioned artefact; CRO sensitivity on every run; re-evaluated in S17. The original plan covers this; no plan change is needed (§4).

## 1. How much does the risk model matter?

### 1.1 Literature

| Claim | Source | Status |
|---|---|---|
| Mean–variance optimisation tends to maximise the effects of errors in input assumptions; unconstrained MV can be inferior to equal weighting; its value improves when inputs are adjusted and constraints reflect fundamental considerations | Michaud 1989, *FAJ* 45(1) | `VERIFIED-ABSTRACT` |
| None of 14 optimised models consistently beats 1/N; the sample-based MV strategy needs an estimation window of about 3,000 months (25 assets) to beat it | DeMiguel, Garlappi & Uppal 2009, *RFS* 22(5) (cited by ANG p. 9) | `VERIFIED-ABSTRACT` |
| Errors in means matter far more than errors in variances, which matter more than errors in covariances; the ratio depends on risk aversion and is disputed | Chopra & Ziemba 1993, *JPM* 19(2) | `VERIFIED-SECONDARY` |
| The precision of a mean estimate depends on the calendar span, not the sampling frequency; variance estimates improve with frequency. ANG uses this to motivate risk-based methods | Merton 1980, *JFE* 8(4); ANG p. 9 | Merton `VERIFIED-SECONDARY`; ANG's use `VERIFIED-SOURCE` |
| MVO's "problem portfolios" are the least important principal components: lowest (and underestimated) risk, too-high expected returns, hence large estimated Sharpe ratios and large bets | Pedersen, Babu & Levine 2021, *FAJ* 77(2), p. 125 | `VERIFIED-SOURCE` |
| Fixing the risk model alone needs about 5–10% correlation shrinkage; EPO uses about 75% because expected-return errors also need it; the parameter is chosen out of sample | PBL 2021, pp. 126–127 | `VERIFIED-SOURCE` |
| A no-short-sale constraint is equivalent to shrinking large covariance elements; with it, the sample matrix performs as well as factor and shrinkage estimators | Jagannathan & Ma 2003, *JF* 58(4) | `VERIFIED-ABSTRACT` |
| Minimum-variance and maximum-diversification portfolios are sensitive to covariance misspecification; equal-risk-contribution and inverse-volatility portfolios are relatively robust | Ardia, Bolliger, Boudt & Gagnon-Fleury 2017, *Ann. Oper. Res.* 254(1) | `VERIFIED-ABSTRACT` |

### 1.2 Our check in the asset-class setting (M-1)
**Design:**
- the 17-asset-class design of `S4_ANG_BASELINE.md` Appendix B, with expected excess returns of 0.10–0.33 Sharpe per class;
- 120 months of Gaussian returns;
- mean–variance utility, with risk aversion set so that the true long-only optimum has 9% volatility;
- 200 simulations.

Each cell is the mean certainty-equivalent loss against the true optimum, in bp per year. "Weight change" is half the sum of absolute weight differences when only the risk model changes from sample to correlation shrinkage (LW-corr).

| Constraints | Expected-return input | True Σ | Sample | LW-corr | LW-identity | Weight change |
|---|---|---|---|---|---|---|
| Budget only | True | 0.0 | 71.5 | 59.2 | 58.2 | 332% |
| Budget only | CMA error (Sharpe s.d. 0.10) | 997.5 | 1,655.4 | 674.0 | 625.8 | 1,024% |
| Budget only | Sample mean (10 years) | 1,858.5 | 3,047.7 | 2,039.7 | 1,935.2 | 680% |
| Long-only | True | 0.0 | 8.7 | 8.8 | 8.8 | 4.9% |
| Long-only | CMA error | 52.4 | 58.5 | 58.4 | 59.4 | 3.1% |
| Long-only | Sample mean | 167.1 | 170.6 | 170.3 | 172.0 | 1.9% |
| Long-only, cap 25% | True | 0.0 | 8.1 | 8.7 | 8.5 | 4.2% |
| Long-only, cap 25% | CMA error | 40.9 | 44.2 | 45.2 | 45.3 | 1.8% |
| Long-only, cap 25% | Sample mean | 97.7 | 98.5 | 100.1 | 99.9 | 1.2% |

**Findings:**
1. **Expected-return error dominates in every constraint set.** With the true covariance, CMA error alone costs 41–998 bp/yr. With true expected returns, covariance error alone costs 8–72 bp/yr. This is Chopra–Ziemba's ordering, in our design.
2. **Unconstrained, the risk model matters enormously, mostly through its interaction with return errors.** With CMA error, swapping the sample matrix for correlation shrinkage cuts the loss from 1,655 to 674 bp/yr and changes the portfolio beyond recognition. Shrinkage even beats the true covariance (674 vs 998), because it dampens the problem portfolios (PBL p. 125).
3. **Long-only (ANG's setting), estimator choice is second-order:** ≤ 2 bp/yr and 2–5% of the weights. The constraints do the regularising (Jagannathan & Ma 2003).
4. **"Better" depends on the use.** The scaled-identity target, harmful for minimum variance (Appendix B: up to 10.7×), is harmless here. A ranking only exists for a stated loss (§3).

### 1.3 Regularise inside the method, or swap the risk model? (M-2)
Same design; CMA error (Sharpe s.d. 0.10); risk aversion set for 6%, 9% and 12% target volatility. "EPO 0.75" multiplies the off-diagonal correlations by 0.25 before optimising (PBL p. 126, simple EPO).

| Target vol | Constraints | True Σ | Sample | LW-corr | Sample + EPO 0.75 | LW-corr + EPO 0.75 |
|---|---|---|---|---|---|---|
| 6% | Budget only | 584.5 | 970.4 | 397.1 | 332.6 | 353.3 |
| 6% | Long-only, cap 25% | 36.1 | 42.8 | 44.1 | 139.0 | 145.5 |
| 9% | Budget only | 997.5 | 1,655.4 | 674.0 | 528.2 | 561.4 |
| 9% | Long-only, cap 25% | 40.9 | 44.2 | 45.2 | 116.8 | 120.7 |
| 12% | Budget only | 1,855.6 | 3,079.3 | 1,250.0 | 942.7 | 1,002.1 |
| 12% | Long-only, cap 25% | 44.6 | 46.1 | 46.2 | 67.1 | 67.8 |

**Findings:**
5. **Unconstrained:** method-level regularisation gives the lowest loss at every risk aversion, and once it is applied the base estimator matters little (528 vs 561 at 9%).
6. **Long-only with caps:** the same shrinkage raises the loss 1.5–3.3× relative to the same estimator without it (e.g. 117 vs 44 at 9%). The constraints already regularise, and extra shrinkage over-corrects. A method's regularisation parameter must be tuned per constraint regime under protocol, as PBL tune it out of sample (p. 127).
7. The ordering is the same at 6%, 9% and 12% target volatility.

**Conclusion of §1.** The covariance matrix is decisive:
- for risk-based methods and risk limits;
- in unconstrained or weakly constrained mean–variance methods, where it governs how return errors are amplified;
- in high-dimensional problems (`S4_ANG_BASELINE.md` §13.3: 300 stocks; the sample matrix is singular).

It is second-order in long-only, bounded asset-class allocation, where CMA quality dominates. The heavy regularisation that mean–variance methods need is best supplied **inside the method** (EPO, Black–Litterman, resampling, robust optimisation), not by giving those methods a different risk model. This is the basis of ADR-0027 D3 r3.

## 2. (a) Are some risk models better?

| Regularity | Conditions | Source |
|---|---|---|
| The sample matrix is a poor optimiser input unless T is large relative to N; it is singular when T ≤ N | General | Ledoit & Wolf 2004, *JPM* 30(4) (working-paper abstract, `VERIFIED-ABSTRACT`); linear algebra; §13.3 |
| Shrinkage toward a structured target improves on the sample matrix for stock portfolios | Moderate to large N | Ledoit & Wolf 2004 |
| Nonlinear shrinkage dominates linear shrinkage when N is comparable to T | Stock universes | Ledoit & Wolf 2017, *RFS* 30(12) (`VERIFIED-ABSTRACT`) |
| The shrinkage target must fit the structure: a scaled-identity target is harmful for minimum variance across asset classes with very different volatilities | Asset classes | Appendix B (`VERIFIED-DERIVATION`) |
| RMT eigenvalue clipping is harmful for 17 asset classes and best for 100–300 stocks | Dimension and spectrum shape | Appendix C (`VERIFIED-DERIVATION`) |
| Under long-only constraints, estimator differences are small | Constrained minimum variance and mean–variance | Jagannathan & Ma 2003; Chan, Karceski & Lakonishok 1999, *RFS* 12(5) (`VERIFIED-ABSTRACT`); Appendix B; M-1 |
| Tracking-error objectives need richer risk models than minimum variance | Benchmark-relative use | Chan, Karceski & Lakonishok 1999 |
| Dynamic correlation models (DCC; DCC with nonlinear shrinkage) improve short-horizon risk estimates | Daily to monthly horizons | Engle 2002 (`CANDIDATE SOURCE`); Engle, Ledoit & Wolf 2019, *JBES* (`VERIFIED-SECONDARY`) |
| At a 3-year horizon, GARCH-type deviations have mostly decayed (share 0.066 at φ = 0.98) | SAA horizon | `S4_ANG_BASELINE.md` §13.2 (`VERIFIED-DERIVATION`) |

**Conclusion:** there is no universal winner, but there are reliable losers in specific problems. Differences are large where N/T is large, constraints are loose or the horizon is short. They are small for long-only asset-class allocation at a 3-year horizon.

## 3. (b) Which to choose: candidates per problem (S10 decides)

| Problem | Candidates to test | Excluded now (evidence) | Leading candidate (not a decision) |
|---|---|---|---|
| Asset-class SAA (≈ 15–20 classes; monthly data; 3-year horizon; long-only with Policy Statement bounds) | Sample correlation with sample volatilities; linear shrinkage toward a constant-correlation target (Ledoit & Wolf 2004); correlation-only shrinkage; EWMA with a long half-life; window lengths set by S6 data | Scaled-identity target (Appendix B); RMT clipping (Appendix C); fixed shrinkage intensity (§13.2 finding 3) | Shrinkage that keeps each asset's volatility, with data-driven intensity. If indistinguishable from the sample matrix (likely, M-1), take the simpler |
| Short horizon (CRO risk reports, volatility targeting, monitoring, Trader evidence) | EWMA; GARCH/DCC; cDCC | — | DCC-type or EWMA, judged on short-horizon forecast accuracy |
| Security sleeve (N ≥ 50; T may be ≤ N) | Nonlinear shrinkage (Ledoit & Wolf 2017); RMT clipping or rotationally invariant estimators (Bun, Bouchaud & Potters 2017); factor models | Sample matrix when T ≤ N | Nonlinear shrinkage |

**Selection rule per problem** (pre-registered in S7, run in S10):
1. **Loss functions:**
   - out-of-sample realised variance of minimum-variance portfolios and of tracking-error portfolios (Chan, Karceski & Lakonishok 1999; Jagannathan & Ma 2003);
   - volatility-forecast losses that remain reliable when the realised-volatility benchmark is noisy (Patton 2011, *J. Econometrics* 160(1), `VERIFIED-ABSTRACT`; MSE and QLIKE per its working-paper version, `VERIFIED-SECONDARY`);
   - calibration of ex-ante against realised risk.
2. **Statistical comparison:** the model confidence set on walk-forward losses (Hansen, Lunde & Nason 2011, *Econometrica* 79(2), `VERIFIED-ABSTRACT`).
3. **Tie rule:** if several models remain in the set, choose the simplest.
4. **Portfolio returns are not a selection criterion for the risk model.** Selecting on backtested returns overfits (Bailey, Borwein, López de Prado & Zhu 2014, *Notices AMS* 61(5), `VERIFIED-SECONDARY`).
5. **Method regularisation parameters** (EPO shrinkage, Black–Litterman τ, resampling settings) are tuned as part of their methods under S7/S11, given the chosen risk model and per constraint regime (M-2 finding 6).

## 4. (c) Stage and implementation (original plan; no change)

| Stage | What happens | Deliverable |
|---|---|---|
| S4.13 | Per PC method: required risk representation; estimator candidates registered per problem (no selection) | `S4_RISK_DEPENDENCIES.md` |
| S4.16 | CRO contract: risk under the authoritative model plus a sensitivity line under at least one alternative admissible estimator; a material change of the recommendation is flagged | `S4_CRO_CONTRACT.md` |
| S4.20 | Risk-model artefact fields: universe, horizon, risk object, estimator, window, data snapshot, version, units | Typed contracts |
| S6 | Point-in-time return data, frequency and history length, which fix T and N/T per problem | Data contracts |
| S7 | Pre-registered losses, walk-forward design, model confidence set, tie rule, re-evaluation cadence | Evaluation protocol |
| S10 → G10 | Run the comparison per problem; select; RMT eligibility record | Risk specification |
| S11 | Tune method regularisation per constraint regime with the selected risk model | Method registry |
| S8 | Risk role as a deterministic service (no LLM in the numbers); artefact by ID; PSD check; sensitivity runs | Software |
| S17 | Scheduled re-evaluation; change only on evidence plus approval; rollback | Model governance |

**Per-run flow:**
1. A data snapshot is taken.
2. The risk role computes the authoritative model for each problem (versioned).
3. PC methods consume it by ID.
4. The CRO computes risk under it and under the registered alternatives.
5. Candidate cards show both.
6. If the CIO recommendation changes materially under a plausible alternative, the board memo flags it and the human decides.

**Before G10:** S8 may use a labelled placeholder estimator for plumbing only. It is not a decision and must never be reported as one.

## 5. Caveats
- One synthetic design: 17 classes, Gaussian i.i.d. stationary returns. CMA errors are independent across assets; correlated errors would change the magnitudes.
- Single-period mean–variance utility; no transaction costs.
- Chopra–Ziemba's ratios are `VERIFIED-SECONDARY` and disputed. M-1 reproduces their ordering in our design, not their ratios.
- Literature claims are checked at abstract level, except ANG and PBL (full text).

## Appendix — simulation script (synthetic; reproduces M-1 and M-2; seed 20261008; runs in about 10 s)

```python
# M-1: how much do covariance errors vs expected-return errors cost a mean-variance investor,
# and how much does the covariance ESTIMATOR matter, by constraint set? (synthetic; seed 20261008)
import numpy as np, warnings; from scipy.optimize import minimize
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
vol=np.array([.16,.20,.16,.19,.17,.21,.02,.05,.12,.07,.10,.08,.07,.11,.19,.15,.20])   # Appendix B design
g=['E']*6+['T','T','T','C','H','S','C','M','R','G','K']
def rho(a,b):
    if a==b: return {'E':.80,'T':.85,'C':.80}.get(a,.6)
    s={a,b}
    if s<={'E','R','H','M'}: return .60
    if 'E' in s and s&{'T','S'}: return -.10
    if 'E' in s and 'C' in s: return .30
    if s<={'T','S','C'}: return .55
    return .05 if 'G' in s else (.25 if 'K' in s else .20)
N=17; R=np.array([[1 if i==j else rho(g[i],g[j]) for j in range(N)] for i in range(N)])
e,V=np.linalg.eigh(R); R=V@np.diag(np.clip(e,1e-3,None))@V.T; d=np.sqrt(np.diag(R)); R/=np.outer(d,d)
Sig=np.outer(vol,vol)*R                                         # annual covariance
SR=np.array([.30,.28,.32,.30,.27,.33,.20,.25,.22,.30,.30,.15,.30,.25,.25,.10,.15])
mu=SR*vol                                                       # annual expected excess returns
def lw(X):                                   # Ledoit-Wolf (2004), scaled-identity target
    T,n=X.shape; Xc=X-X.mean(0); S=Xc.T@Xc/T; m=np.trace(S)/n; d2=np.sum((S-m*np.eye(n))**2)/n
    b2=min(sum(np.sum((np.outer(x,x)-S)**2) for x in Xc)/n/T**2,d2); return (b2/d2)*m*np.eye(n)+((d2-b2)/d2)*S
def lw_corr(X):                              # LW on standardised data: shrunk correlation, sample vols kept
    s=X.std(0); C=lw((X-X.mean(0))/s); d=np.sqrt(np.diag(C)); return np.outer(s,s)*C/np.outer(d,d)
EST={'oracle':None,'sample':lambda X:np.cov(X,rowvar=False,bias=True),'LW-corr':lw_corr,'LW-identity':lw}
def solve(m,S,gam,cons):
    if cons=='budget only':                  # max w'm - gam/2 w'Sw  s.t. 1'w = 1 (closed form)
        Si1=np.linalg.solve(S,np.ones(N)); Sim=np.linalg.solve(S,m)
        lam=(np.ones(N)@Sim-gam)/(np.ones(N)@Si1); return (Sim-lam*Si1)/gam
    ub=1.0 if cons=='long-only' else 0.25
    f=lambda w:-(w@m-gam/2*w@S@w); gr=lambda w:-(m-gam*S@w)
    best=None
    for x0 in (np.ones(N)/N,):
        r=minimize(f,x0,jac=gr,bounds=[(0,ub)]*N,constraints=[{'type':'eq','fun':lambda w:w.sum()-1,'jac':lambda w:np.ones(N)}],
                   method='SLSQP',options={'maxiter':1000,'ftol':1e-14})
        best=r.x if best is None or f(r.x)<f(best) else best
    return best
CE=lambda w,gam: w@mu-gam/2*w@Sig@w
# risk aversion: true long-only optimum has ~9% volatility
lo,hi=0.5,50
for _ in range(60):
    gam=(lo+hi)/2; w=solve(mu,Sig,gam,'long-only'); v=np.sqrt(w@Sig@w)
    lo,hi=(gam,hi) if v>.09 else (lo,gam)
print(f"gamma = {gam:.2f}; true long-only optimum vol = {np.sqrt(w@Sig@w):.4f}")
rng=np.random.default_rng(20261008); T=120; NS=200
cons_list=['budget only','long-only','long-only, cap 25%']
wstar={c:solve(mu,Sig,gam,c) for c in cons_list}
res={}; dist={}
for sim in range(NS):
    X=rng.multivariate_normal(mu/12,Sig/12,T)                    # 10 years of monthly returns
    z=rng.standard_normal(N)
    MU={'true mu':mu,'CMA error (SR sd 0.10)':mu+0.10*vol*z,'sample mean (10y)':X.mean(0)*12}
    SIG={k:(Sig if f is None else f(X)*12) for k,f in EST.items()}
    for c in cons_list:
        W={}
        for mk,m in MU.items():
            for sk,S in SIG.items():
                w=solve(m,S,gam,c); W[(mk,sk)]=w
                res.setdefault((c,mk,sk),[]).append(CE(wstar[c],gam)-CE(w,gam))
        for mk in MU:                                            # recommendation change when only the risk model changes
            dist.setdefault((c,mk),[]).append(0.5*np.abs(W[(mk,'sample')]-W[(mk,'LW-corr')]).sum())
            dist.setdefault((c,mk,'id'),[]).append(0.5*np.abs(W[(mk,'sample')]-W[(mk,'LW-identity')]).sum())
print("M-1 mean certainty-equivalent loss vs the true optimum, bp per year (200 sims; T = 120 months)")
for c in cons_list:
    print(f"  [{c}]")
    for mk in ['true mu','CMA error (SR sd 0.10)','sample mean (10y)']:
        row=" | ".join(f"{sk} {1e4*np.mean(res[(c,mk,sk)]):8.1f}" for sk in EST)
        print(f"    mu = {mk:24s}: {row}")
    for mk in ['true mu','CMA error (SR sd 0.10)','sample mean (10y)']:
        print(f"    weight change sample -> LW-corr, mu = {mk:24s}: {100*np.mean(dist[(c,mk)]):5.1f}% | sample -> LW-identity: {100*np.mean(dist[(c,mk,'id')]):5.1f}%")
print("min loss (should be >= 0):", min(min(v) for v in res.values()))

# M-2: method-level regularisation (EPO correlation shrinkage) vs swapping the risk model; robustness to risk aversion
def epo(S,w=.75):                                # PBL (2021) simple EPO: off-diagonal correlations x (1-w)
    s=np.sqrt(np.diag(S)); C=S/np.outer(s,s); C=(1-w)*C+w*np.eye(len(S)); return np.outer(s,s)*C
def gam_for(target,cons='long-only'):
    lo,hi=0.2,80
    for _ in range(60):
        g_=(lo+hi)/2; w=solve(mu,Sig,g_,cons); v=np.sqrt(w@Sig@w); lo,hi=(g_,hi) if v>target else (lo,g_)
    return g_
cons_list=['budget only','long-only, cap 25%']
for target in (.06,.09,.12):
    gam=gam_for(target); wstar={c:solve(mu,Sig,gam,c) for c in cons_list}
    rng=np.random.default_rng(20261008); out={}
    for sim in range(200):
        X=rng.multivariate_normal(mu/12,Sig/12,120); z=rng.standard_normal(N)
        m=mu+0.10*vol*z; Ss=np.cov(X,rowvar=False,bias=True)*12; Sl=lw_corr(X)*12
        cand={'true Sigma':Sig,'sample':Ss,'LW-corr':Sl,'sample + EPO 0.75':epo(Ss),'LW-corr + EPO 0.75':epo(Sl)}
        for c in cons_list:
            for k,S in cand.items(): out.setdefault((c,k),[]).append(CE(wstar[c],gam)-CE(solve(m,S,gam,c),gam))
    print(f"target vol {target:.0%} (gamma {gam:.2f}); CMA error SR sd 0.10; mean CE loss bp/yr")
    for c in cons_list: print(f"   [{c}] "+" | ".join(f"{k} {1e4*np.mean(out[(c,k)]):7.1f}" for k in cand))
```
