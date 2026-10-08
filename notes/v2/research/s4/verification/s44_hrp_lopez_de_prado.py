"""S4.4 source reproduction: Lopez de Prado (2016, version of 23 May 2016), Exhibit 7 (Appendix A.3, seed 12345),
using an own Python-3 port of the published algorithm; plus the order-dependence finding (HRP-1) and the
order-invariant tree-split variant (paper p. 11, 'further research')."""
import numpy as np, pandas as pd, random, warnings
import scipy.cluster.hierarchy as sch
from scipy.optimize import minimize
warnings.filterwarnings('ignore')
def ivp(c): w = 1. / np.diag(c); return w / w.sum()
def cluster_var(cov, items): c = cov.loc[items, items].values; w = ivp(c); return w @ c @ w
def quasi_diag(link):
    link = link.astype(int); order = [link[-1, 0], link[-1, 1]]; n = link[-1, 3]
    while max(order) >= n:
        order = [x for o in order for x in ((link[o - n, 0], link[o - n, 1]) if o >= n else (o,))]
    return order
def rec_bipart(cov, order):
    w = pd.Series(1.0, index=order); items = [order]
    while items:
        items = [i[j:k] for i in items for j, k in ((0, len(i) // 2), (len(i) // 2, len(i))) if len(i) > 1]
        for a in range(0, len(items), 2):
            v0, v1 = cluster_var(cov, items[a]), cluster_var(cov, items[a + 1]); al = 1 - v0 / (v0 + v1)
            w[items[a]] *= al; w[items[a + 1]] *= 1 - al
    return w
def dist(corr): return ((1 - corr.clip(-1, 1)) / 2.) ** .5
def hrp(cov, corr):    # published algorithm: list bisection of the quasi-diagonal order
    link = sch.linkage(dist(corr), 'single')     # 2-D input: Euclidean distance between rows of D (the paper's d-tilde)
    return rec_bipart(cov, corr.index[quasi_diag(link)].tolist()).sort_index()
def hrp_tree(cov, corr):  # variant: split along the dendrogram's own children (order-invariant)
    link = sch.linkage(dist(corr), 'single'); n = len(cov); names = list(cov.index); mem = {i: [names[i]] for i in range(n)}
    for k, row in enumerate(link.astype(int)): mem[n + k] = mem[row[0]] + mem[row[1]]
    w = pd.Series(1.0, index=names)
    def split(node):
        if node < n: return
        a, b = link[node - n, :2].astype(int); v0, v1 = cluster_var(cov, mem[a]), cluster_var(cov, mem[b]); al = 1 - v0 / (v0 + v1)
        w[mem[a]] *= al; w[mem[b]] *= 1 - al; split(a); split(b)
    split(2 * n - 2); return w
# Exhibit 7 (generateData: nObs=10000, size0=5, size1=5, sigma1=.25; Python-2 randint(0,4) == int(random()*5))
np.random.seed(seed=12345); random.seed(12345)
x = np.random.normal(0, 1, size=(10000, 5)); cols = [int(random.random() * 5) for _ in range(5)]
x = pd.DataFrame(np.append(x, x[:, cols] + np.random.normal(0, .25, size=(10000, 5)), axis=1), columns=range(1, 11))
cov, corr = x.cov(), x.corr()
assert abs(np.linalg.cond(cov.values) - 150.9324) < 1e-3
H = hrp(cov, corr); I = ivp(cov.values)
C = minimize(lambda v: v @ cov.values @ v, np.ones(10) / 10, jac=lambda v: 2 * cov.values @ v, bounds=[(0, 1)] * 10,
             constraints=[{'type': 'eq', 'fun': lambda v: v.sum() - 1}], method='SLSQP', options={'ftol': 1e-15}).x
assert np.allclose(100 * H.values, [7.00, 7.59, 10.84, 19.03, 9.72, 10.19, 6.62, 9.10, 7.12, 12.79], atol=0.006)
assert np.allclose(100 * I, [10.36, 10.28, 10.36, 10.25, 10.31, 9.74, 9.80, 9.65, 9.64, 9.61], atol=0.006)
assert np.allclose(100 * C, [14.44, 19.93, 19.73, 19.87, 18.68, 0.00, 5.86, 1.49, 0.00, 0.00], atol=0.006)
# HRP-1: reordering the assets changes published-HRP weights; the tree-split variant is invariant
rng = np.random.default_rng(20261008); changed = 0; tree_changed = 0
for t in range(100):
    n = 12; L = rng.normal(size=(n, 3)); M = L @ L.T + np.diag(rng.uniform(.2, 1, n)); d = np.sqrt(np.diag(M))
    S_ = np.outer(s := rng.uniform(.1, .4, n), s) * M / np.outer(d, d); Rv = S_ / np.outer(np.sqrt(np.diag(S_)), np.sqrt(np.diag(S_)))
    np.fill_diagonal(Rv, 1); p = rng.permutation(n)
    cv, cr = pd.DataFrame(S_), pd.DataFrame(Rv); cvp, crp = pd.DataFrame(S_[np.ix_(p, p)]), pd.DataFrame(Rv[np.ix_(p, p)])
    for f, cnt in ((hrp, 'a'), (hrp_tree, 'b')):
        w0 = f(cv, cr); wp = f(cvp, crp); wp.index = [p[i] for i in wp.index]; diff = np.abs(w0.values - wp.sort_index().values).max()
        if cnt == 'a': changed += diff > 1e-9
        else: tree_changed += diff > 1e-9
assert changed > 0 and tree_changed == 0
print(f"PASS Lopez de Prado: Exhibit 7 reproduced (CLA/HRP/IVP, cond. no. 150.9324); published HRP order-dependent in {changed}/100 cases; tree-split variant invariant")
