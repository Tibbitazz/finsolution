"""S4.13 registry check for S4_RISK_DEPENDENCIES.md (risk and covariance dependency inventory).

Checks registry completeness and internal consistency, not econometric validity:
1. every method record in S4.5-S4.12 (from the record headings) has a row in the method map, and no row lacks a record;
   the §0 counts match the tables;
2. every input has a type, existing objects, and units, horizon and minimum-data cells with a status marker;
3. scenario and path rows cite S412-D6 with the location class its decision text assigns to that method (a clean
   failure, not a crash, if that text cannot be read);
4. minimum data are declared or marked unresolved (rows and objects);
5. every candidate has a declared kind (a conditional kind names two kinds and its condition); non-MEASURE candidates
   name the objects they build; constructed-by and consumer lists agree; MEASURE candidates only read an object;
6. Binding = weakest status of a row's markers and objects; ADR-0027 is never an established basis and is still
   PROPOSED; ASSUMED/OPEN rows are not established;
7. every decision ID cited in the document (S4x-Dy, OB-x, ADR-nnnn) occurs in another notes/v2 document (HANDOFF.md
   excluded), and every cited ADR has a file;
8. no candidate selection: status 'candidate', no threshold set, method rows never name a candidate, no selection
   wording ("not the default" allowed);
plus the facts behind two minimum-data entries (sample-covariance rank; regression identifiability) and finding F-1
(scenario return basis): the exact ERC-CVaR existence condition under normality and on fat-tailed scenarios, D1 V0's
invariance in LP form, and the distribution-free single-asset bound.
Mutation tests (2026-10-20, 2026-10-24) show what it cannot detect: a consistent wrong object mapping, a cutoff added
beside "No threshold set", a wrong tag from the vocabulary, wrong content, an edited §6.1 number (the F-1 values
are this script's constants, not parsed from the text). Run: python3 s413_risk_dependencies.py"""
import re
import warnings
from pathlib import Path
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize, linprog
warnings.filterwarnings('ignore'); np.seterr(all='ignore')   # numpy 2.0 matmul raises spurious FP warnings on macOS Accelerate

S4 = Path(__file__).resolve().parent.parent
V2 = S4.parent.parent
DOC = (S4 / 'S4_RISK_DEPENDENCIES.md').read_text()
RECORDS = ['S4_HEURISTICS.md', 'S4_MVO_FAMILY.md', 'S4_MOMENTUM.md', 'S4_RISK_STRUCTURED.md', 'S4_NON_TRADITIONAL.md']
ADR27 = next((V2 / 'decisions').glob('ADR-0027*.md')).read_text()
errors = []
def err(msg): errors.append(msg)

# ---------------------------------------------------------------- parsing
def table(marker):
    i = DOC.index(f'<!-- s413:{marker} -->')
    lines, rows = DOC[i:].split('\n')[1:], []
    for ln in lines:
        if ln.startswith('|'): rows.append(ln)
        elif rows: break
    cells = lambda ln: [c.strip() for c in ln.strip().strip('|').split('|')]
    hdr = cells(rows[0]); out = []
    for r in rows[2:]:
        c = cells(r)
        if len(c) != len(hdr): err(f'[{marker}] wrong cell count ({len(c)} vs {len(hdr)}): {r[:70]}'); continue
        out.append(dict(zip(hdr, c)))
    return out

problems, objects, methods, cross, estimators = (table(m) for m in ('problems', 'objects', 'methods', 'crosscutting', 'estimators'))
EST = re.compile(r'\[established: ([^\]]+)\]'); PROV = re.compile(r'\[provisional: ([^\]]+)\]')
UNR = re.compile(r'\[unresolved → ([^\]]*)\]'); OBJ = re.compile(r'\[object: (RO-\d+)\]')
BAD = re.compile(r'\[(established|provisional|unresolved|object)(?!: | →)')
RANK = {'unresolved': 0, 'provisional': 1, 'established': 2}
ALLOWED_BASIS = re.compile(r'S4\d{1,2}-D\d+|S4\.\d+[ab]? record|ADR-00(0[1-9]|1\d|2[0-6])\b|\b0\d §\d+|EQ-[A-Z]+-\d+|'
                           r'\bI-\d\b|\bR-\d\b|\bAC-\d\b|\bOB-\d\b|VERIFIED-DERIVATION|RQ-07 owner instruction')
TAGS = ['VERIFIED-SOURCE', 'VERIFIED-DERIVATION', 'VERIFIED-SECONDARY', 'ESTABLISHED', 'ASSUMED', 'OPEN']
TYPES = {'COV', 'VOL', 'SCN', 'PATH', 'COMOM', 'FACTOR', 'INTERNAL', 'NONE'}
VIEW = {'VOL': {'COV', 'VOL', 'FACTOR'}, 'COV': {'COV'}, 'SCN': {'SCN'}, 'PATH': {'PATH'}, 'COMOM': {'COMOM'}, 'FACTOR': {'FACTOR'}}
KINDS = {'ESTIMATOR', 'TRANSFORMATION', 'COMPOSITION', 'GENERATOR', 'DATA-PREP', 'MEASURE'}
COND = re.compile(r'^([A-Z-]+) / ([A-Z-]+) \(conditional on [^)]+\)$')
refs = lambda s, p='RO': re.findall(rf'\b{p}-\d+\b', s)

def markers(row, label, skip=('Binding', 'Status')):
    """Status values of all markers in a row; also validates marker syntax and the established basis."""
    found = []
    for col, v in row.items():
        if col in skip: continue
        if BAD.search(v): err(f'{label}: malformed status marker in "{col}": {v[:60]}')
        for b in EST.findall(v):
            if 'ADR-0027' in b: err(f'{label}: ADR-0027 (PROPOSED) used as an established basis')
            elif not ALLOWED_BASIS.search(b): err(f'{label}: established basis not a decision, record or derivation: "{b}"')
            found.append('established')
        for b in PROV.findall(v): found.append('provisional')
        for b in UNR.findall(v):
            if not b.strip(): err(f'{label}: unresolved marker without a destination')
            found.append('unresolved')
    return found

def tags_ok(row, label):
    t = [g for g in TAGS if re.search(rf'\b{g}\b', row['Evidence'])]
    if not t: err(f'{label}: evidence tag not in the 02 §A vocabulary: "{row["Evidence"]}"')
    return t

# ---------------------------------------------------------------- problems and objects
P = {r['Problem']: r for r in problems}
for pid, r in P.items():
    m = markers(r, pid)
    for col in ('Universe', 'Horizon', 'Data'):
        if not (EST.search(r[col]) or PROV.search(r[col]) or UNR.search(r[col])): err(f'{pid}: "{col}" has no status marker')
    if r['Binding'] != min(m, key=RANK.get): err(f'{pid}: Binding {r["Binding"]} != weakest marker {min(m, key=RANK.get)}')
O = {r['Object']: r for r in objects}
for oid, r in O.items():
    if r['Type'] not in TYPES - {'INTERNAL', 'NONE'}: err(f'{oid}: type "{r["Type"]}" not allowed for an object')
    probs = re.findall(r'P-[A-Z]+', r['Problem'])
    if not probs or any(p not in P for p in probs): err(f'{oid}: unknown or missing problem in "{r["Problem"]}"')
    for col in ('Units and conventions', 'Minimum data'):
        if not (EST.search(r[col]) or PROV.search(r[col]) or UNR.search(r[col])): err(f'{oid}: "{col}" has no status marker')
    st = markers(r, oid) + [P[p]['Binding'] for p in probs if p in P]
    r['_status'] = min(st, key=RANK.get) if st else None
    if r['Binding'] != r['_status']: err(f'{oid}: Binding {r["Binding"]} != weakest status {r["_status"]}')
    tags_ok(r, oid)

# ---------------------------------------------------------------- S412-D6 location classes from the decision text
nt = (S4 / 'S4_NON_TRADITIONAL.md').read_text()
d6 = next((l for l in nt.split('\n') if l.startswith('| **S412-D6**')), '')
mf, mc = re.search(r'μ-free \(([^)]+)\)', d6), re.search(r'consume μ \(([^)]+)\)', d6)
EXPECT = {}
if not (mf and mc): err('S412-D6: decision row not found or reworded in S4_NON_TRADITIONAL.md; location classes not checked')
else:
    for txt, cls in ((mf.group(1), 'demeaned'), (mc.group(1), 'centred')):
        for item in txt.split(','):
            m = re.match(r'\s*([A-E]\d)(?: (V\d))?', item)
            if m: EXPECT[('PC-' + m.group(1), m.group(2))] = cls
            else: err(f'S412-D6: cannot read method "{item.strip()}" in the decision text')
loc_class = lambda s: ('demeaned' if 'demeaned' in s else '') + ('centred' if 'centred on S9 μ' in s else '')

# ---------------------------------------------------------------- method coverage from record headings
HEAD = re.compile(r'^#{3,4} .*?(PC-[A-E]\d|SIG-\d(?: variant [A-Z])?|EQ-SIG-\d)', re.M)
in_scope = set()
for f in RECORDS:
    for k in HEAD.findall((S4 / f).read_text()):
        in_scope.add(re.sub(r'(SIG-\d) variant ([A-Z])', r'\1/\2', k))
out_of_scope = {k for k in in_scope if k.startswith('PC-E')}   # agentic roles belong to S4.14
in_scope -= out_of_scope
key = lambda r: r.get('Method', r.get('Consumer')).split(' — ')[0].strip()
mapped = {key(r) for r in methods}
for k in sorted(in_scope - mapped): err(f'coverage: method record {k} has no row in the method map')
for k in sorted(mapped - in_scope): err(f'coverage: method-map row {k} has no method record in S4.5-S4.12')

# ---------------------------------------------------------------- method and cross-cutting rows
consumers, scn_checked = {o: set() for o in O}, 0
for r in methods + cross:
    k, label = key(r), r.get('Method', r.get('Consumer'))
    t = r['Type']
    if t not in TYPES: err(f'{label}: type "{t}" not in {sorted(TYPES)}'); continue
    if re.search(r'\bCOV-\d+', ' '.join(r.values())): err(f'{label}: a method row names a candidate (objects only)')
    ros = refs(r['Object']) + OBJ.findall(' '.join(r.values()))
    for o in ros:
        if o not in O: err(f'{label}: unknown object {o}'); continue
        consumers[o].add(k)
    if t in ('NONE', 'INTERNAL'):
        if r['Object'] != '—': err(f'{label}: type {t} must have no object')
    else:
        if not refs(r['Object']): err(f'{label}: type {t} needs an object')
        for o in refs(r['Object']):
            if o in O and O[o]['Type'] not in VIEW[t]: err(f'{label}: input type {t} cannot come from {o} ({O[o]["Type"]})')
    for col in ('Units and conventions', 'Horizon', 'Minimum data'):
        v = r[col]; has = bool(EST.search(v) or PROV.search(v) or UNR.search(v) or OBJ.search(v))
        if not v: err(f'{label}: "{col}" is empty')
        elif t == 'NONE' and col != 'Minimum data' and v == 'n/a': pass
        elif not has: err(f'{label}: "{col}" has no status marker (declare it or mark it unresolved)')
    loc = r['Location rule']
    if t in ('SCN', 'PATH'):
        scn_checked += 1
        cls = loc_class(loc)
        if 'S412-D6' not in loc or cls not in ('demeaned', 'centred'): err(f'{label}: scenario row must cite S412-D6 with one location class')
        var = (re.search(r'\bV\d\b', label) or [None])[0]
        exp = EXPECT.get((k, var), EXPECT.get((k, None)))
        if not EXPECT: pass                                      # already reported: decision text unreadable
        elif exp is None: err(f'{label}: scenario method not classified by the S412-D6 decision text')
        elif cls != exp: err(f'{label}: location "{cls}" but S412-D6 assigns "{exp}"')
        for o in refs(r['Object']):
            if o in O and loc_class(O[o]['Location rule']) != cls: err(f'{label}: location differs from its object {o}')
    elif loc != 'n/a': err(f'{label}: location rule must be n/a for a {t} input')
    st = markers(r, label) + [O[o]['_status'] for o in set(ros) if o in O and O[o]['_status']]
    if not st: err(f'{label}: no status marker anywhere in the row'); continue
    weakest = min(st, key=RANK.get)
    if r['Binding'] != weakest: err(f'{label}: Binding {r["Binding"]} != weakest status {weakest}')
    tg = tags_ok(r, label)
    if r['Binding'] == 'established' and {'ASSUMED', 'OPEN'} & set(tg): err(f'{label}: ASSUMED/OPEN evidence cannot be established')
for o, r in O.items():
    listed = {c.strip() for c in r['Consumers'].split(',')}
    if listed != consumers[o]: err(f'{o}: consumers listed {sorted(listed ^ consumers[o])} differ from the rows using it')
    if not consumers[o]: err(f'{o}: no consumer')

# ---------------------------------------------------------------- candidates
E, built, read = {r['ID']: r for r in estimators}, {o: set() for o in O}, {o: set() for o in O}
SEL = re.compile(r'(?<!not )(?<!no )\b(selected|chosen|winner|preferred|recommended|default)\b', re.I)
ALLOWED_NEG = re.compile(r'\b(not the|not a|no) default\b', re.I)
for eid, r in E.items():
    cm = COND.match(r['Kind']); ks = list(cm.groups()) if cm else [r['Kind']]
    if any(k not in KINDS for k in ks): err(f'{eid}: kind "{r["Kind"]}" not in {sorted(KINDS)} or a conditional "A / B (conditional on …)"')
    if cm and (ks[0] == ks[1] or {'MEASURE', 'GENERATOR'} & set(ks)): err(f'{eid}: conditional kind must name two different non-generator, non-measure kinds')
    if '→' not in r['Acts on → produces']: err(f'{eid}: state what it acts on and what it produces')
    tos = refs(r['Objects'])
    if not tos: err(f'{eid}: names no risk object')
    for o in tos:
        if o not in O: err(f'{eid}: unknown object {o}'); continue
        if ks == ['MEASURE']: read[o].add(eid); continue        # a measure reads an object and builds none
        built[o].add(eid)
        is_gen, scn = 'GENERATOR' in ks, O[o]['Type'] in ('SCN', 'PATH')
        if is_gen != scn: err(f'{eid}: {r["Kind"]} cannot construct {o} ({O[o]["Type"]})')
    if not re.findall(r'P-[A-Z]+', r['Problems']) or any(p not in P for p in re.findall(r'P-[A-Z]+', r['Problems'])):
        err(f'{eid}: unknown or missing problem')
    if r['Status'] != 'candidate': err(f'{eid}: status "{r["Status"]}" (S4.13 registers candidates only)')
    if 'No threshold set' not in r['Eligibility']: err(f'{eid}: eligibility must say "No threshold set" (no cutoffs exist)')
    m = SEL.search(ALLOWED_NEG.sub('', ' '.join(v for c, v in r.items() if c != 'Status')))
    if m: err(f'{eid}: selection wording "{m.group(0)}"')
    for mm in re.finditer(r'ADR-0027', ' '.join(r.values())):
        if 'PROPOSED' not in ' '.join(r.values())[mm.end(): mm.end() + 40]: err(f'{eid}: ADR-0027 cited without "(PROPOSED)"')
    tags_ok(r, eid)
for o, r in O.items():
    listed = set(refs(r['Constructed by'], 'COV'))
    if listed & {e for e in E if E[e]['Kind'] == 'MEASURE'}: err(f'{o}: a MEASURE candidate is listed as constructing it')
    if not listed: err(f'{o}: no constructing candidate')
    if listed != built[o]: err(f'{o}: constructed-by {sorted(listed ^ built[o])} disagrees with §5')
    if read[o] and not built[o]: err(f'{o}: read by {sorted(read[o])} but built by no candidate')
if '**Status:** PROPOSED' not in ADR27: err('ADR-0027 is no longer PROPOSED: revisit every [provisional: ADR-0027 …] marker')

# ---------------------------------------------------------------- decision IDs exist elsewhere in the repository
CORPUS = ' '.join(p.read_text() for p in V2.rglob('*.md') if p.name not in ('S4_RISK_DEPENDENCIES.md', 'HANDOFF.md'))
cited = sorted(set(re.findall(r'\bS4\d{1,2}-D\d+\b|\bOB-\d+\b|\bADR-\d{4}\b', DOC)))
for d in cited:
    if not re.search(rf'\b{d}\b', CORPUS): err(f'decision ID {d} occurs in no other notes/v2 document')
    if d.startswith('ADR-') and not list((V2 / 'decisions').glob(f'{d}-*.md')): err(f'{d} has no file in decisions/')

# ---------------------------------------------------------------- §0 counts match the tables
for phrase in (f'{len(in_scope)} method records', f'in {len(methods)} input rows', f'{len(cross)} cross-cutting consumers',
               f'**{len(E)} candidates**'):
    if phrase not in DOC: err(f'§0: count "{phrase}" not stated (tables changed?)')

# ---------------------------------------------------------------- facts behind minimum-data entries
rng = np.random.default_rng(20261019)
N = 8
for T, singular in ((5, True), (8, True), (9, False)):   # sample covariance of T draws has rank <= T - 1
    S_hat = np.cov(rng.standard_normal((T, N)), rowvar=False)
    if (np.linalg.matrix_rank(S_hat) < N) != singular: err(f'rank fact fails at T = {T}, N = {N}')
m_f = 3                                                   # regression with m factors and an intercept: s^2 = RSS/(p - m - 1)
for p, defined in ((m_f + 1, False), (m_f + 2, True)):
    X = np.c_[np.ones(p), rng.standard_normal((p, m_f))]; y = rng.standard_normal(p)
    rss = np.sum((y - X @ np.linalg.lstsq(X, y, rcond=None)[0]) ** 2)
    if (p - m_f - 1 > 0 and rss > 1e-12) != defined: err(f'identifiability fact fails at p = {p}')

# ---------------------------------------------------------------- finding F-1 (§6.1)
# ERC-CVaR (S412-D3) = argmin CVaR(y) - mean ln y. With a common per-period cash return r in the location,
# CVaR(y; Y + r) = CVaR(y; Y) - r 1'y, so a solution exists iff the long-only min CVaR on zero-location scenarios > r.
b = .95; c2 = norm.pdf(norm.ppf(b)) / (1 - b); rf = .04
gcv = lambda w, m, Sig: -w @ m + c2 * np.sqrt(w @ Sig @ w)                    # Gaussian CVaR (S4.12a)
gct = lambda w, m, Sig: w * (-m + c2 * (Sig @ w) / np.sqrt(w @ Sig @ w))      # Euler contributions
cs = {'type': 'eq', 'fun': lambda w: w.sum() - 1}
def erc_barrier(m, Sig):
    y = minimize(lambda y: gcv(y, m, Sig) - np.log(y).mean(), np.ones(len(m)) / len(m), bounds=[(1e-12, None)] * len(m),
                 method='L-BFGS-B', options={'ftol': 1e-15, 'gtol': 1e-12, 'maxiter': 5000}).x
    w = y / y.sum(); return w, gct(w, m, Sig) / gcv(w, m, Sig)
def lo_gmv(Sig):
    w = minimize(lambda w: w @ Sig @ w, np.ones(len(Sig)) / len(Sig), method='SLSQP', bounds=[(0, 1)] * len(Sig), constraints=[cs],
                 options={'ftol': 1e-16, 'maxiter': 1000}).x
    return w, np.sqrt(w @ Sig @ w)
if not abs(c2 - 2.0627) < 1e-4 or not abs(rf / c2 - .0194) < 1e-4 or not abs(rf * np.sqrt(1 / 12) / c2 - .0056) < 1e-4:
    err('F-1: c2 or the normal volatility bounds differ from §6.1')
vol = np.array([.16, .06, .015]); C = np.array([[1, .1, 0], [.1, 1, .2], [0, .2, 1]]); S = np.outer(vol, vol) * C
I3 = np.eye(3); cases = {}                                                     # name: (Sigma, LO-GMV vol in §6.1, solution exists)
for name, v, Cm, g, exists in (('base', vol, C, .0149, False), ('B', np.array([.16, .025, .025]), I3, .0176, False),
                               ('C', np.array([.16, .03, .03]), I3, .0210, True)):
    Sg = np.outer(v, v) * Cm; wg, sg = lo_gmv(Sg)
    if abs(sg - g) > 1e-4: err(f'F-1 case {name}: long-only minimum-variance volatility {sg:.4f} differs from §6.1 ({g})')
    if (sg > rf / c2) != exists: err(f'F-1 case {name}: exact condition gives the wrong existence verdict')
    if not exists and not gcv(wg, np.full(3, rf), Sg) < 0: err(f'F-1 case {name}: CVaR at the minimum-variance mix should be < 0 (objective unbounded)')
    if exists and not np.allclose(erc_barrier(np.full(3, rf), Sg)[1], 1 / 3, atol=1e-4): err(f'F-1 case {name}: ERC-CVaR should exist')
    if name == 'B' and not (v > rf / c2).all(): err('F-1 case B: every asset should exceed the single-asset bound')
W = rng.dirichlet(np.ones(3), 20000)      # sufficient single-asset bound (BCP-4): asset 3 has sigma <= r_F/c2, so its
WS = W @ S                                # contribution is negative in every long-only mix at the annual horizon
c3 = W[:, 2] * (-rf + c2 * WS[:, 2] / np.sqrt(np.einsum('ij,ij->i', WS, W)))
if not (np.isfinite(c3).all() and rf >= c2 * vol[2] and (c3 < 0).all()): err('F-1: BCP-4 single-asset condition not reproduced')
w_zero, sh_zero = erc_barrier(np.zeros(3), S)
if not (np.allclose(sh_zero, 1 / 3, atol=1e-4) and np.allclose(w_zero, [.073, .178, .749], atol=1e-3)):
    err(f'F-1: zero-location ERC-CVaR {w_zero.round(3)} should exist and equal §6.1')
dt = 1 / 12
w0, s0 = erc_barrier(np.zeros(3), S * dt); w1, s1 = erc_barrier(np.full(3, rf * dt), S * dt)
if not (np.allclose(s0, 1 / 3, atol=1e-4) and np.allclose(s1, 1 / 3, atol=1e-4)): err('F-1: monthly solutions should both exist')
if not (np.allclose(w0, [.073, .178, .749], atol=1e-3) and np.allclose(w1, [.056, .138, .806], atol=1e-3)):
    err(f'F-1: monthly weights {w0.round(3)} / {w1.round(3)} differ from §6.1')
if not np.allclose([gcv(w, np.full(3, rf * dt), S * dt) - gcv(w, np.zeros(3), S * dt) for w in W[:200]], -rf * dt):
    err('F-1: uniform-shift invariance of Gaussian CVaR not reproduced')
# fat-tailed scenario CVaR (the decided object): seeded t(4) scenarios with a crash jump, demeaned (zero location)
r7 = np.random.default_rng(7); q = 4000; kq = int(round(q * (1 - b)))
Z = r7.standard_t(4, (q, 3)) @ np.linalg.cholesky(S).T * np.sqrt(.5); Z[:, 0] -= .10 * (r7.random(q) < .05); Z -= Z.mean(0)
hcv = lambda w, Y: np.sort(-Y @ w)[-kq:].mean()
def hct(w, Y): i = np.argsort(-Y @ w)[-kq:]; return w * (-Y[i].mean(0))
def min_cvar_lp(Y):                       # D1 V0: Rockafellar-Uryasev LP, long-only and fully invested
    n = len(Y); res = linprog(np.r_[np.zeros(3), 1, np.ones(n) / (n * (1 - b))], A_ub=np.c_[-Y, -np.ones(n), -np.eye(n)], b_ub=np.zeros(n),
                              A_eq=[np.r_[np.ones(3), 0, np.zeros(n)]], b_eq=[1], bounds=[(0, None)] * 3 + [(None, None)] + [(0, None)] * n, method='highs')
    return res.x[:3], res.fun
def erc_scn(Y):
    best = min((minimize(lambda y: hcv(y, Y) - np.log(y).mean() if (y > 0).all() else 1e9, np.random.default_rng(s).uniform(.2, 3, 3),
                         method='Powell', options={'xtol': 1e-12, 'ftol': 1e-14, 'maxiter': 200000}) for s in range(4)), key=lambda r: r.fun)
    w = best.x / best.x.sum(); return w, hct(w, Y) / hcv(w, Y)
scn = {}
for h, lab, v_doc, exists in ((1., 'annual', .0337, False), (dt, 'monthly', .0097, True)):
    Y0 = Z * np.sqrt(h); x0, v0 = min_cvar_lp(Y0); xr, vr = min_cvar_lp(Y0 + rf * h)
    if abs(v0 - v_doc) > 1e-4 or (v0 > rf * h) != exists: err(f'F-1 scenarios {lab}: min zero-location CVaR {v0:.4f} vs r {rf * h:.4f} differs from §6.1')
    if not (np.allclose(x0, xr, atol=1e-7) and abs(vr - v0 + rf * h) < 1e-9): err(f'F-1 scenarios {lab}: D1 V0 not invariant to the shift')
    if exists: scn[lab] = (erc_scn(Y0), erc_scn(Y0 + rf * h))
(wz, shz), (wr, shr) = scn['monthly']
if not (np.allclose(shz, 1 / 3, atol=5e-3) and np.allclose(shr, 1 / 3, atol=5e-3)): err('F-1 scenarios monthly: ERC-CVaR should exist under both locations')
if not (np.allclose(wz, [.072, .172, .756], atol=1e-3) and np.allclose(wr, [.056, .133, .811], atol=1e-3)):
    err(f'F-1 scenarios monthly: weights {wz.round(3)} / {wr.round(3)} differ from §6.1')
# distribution-free bound: E[-x_i | tail] <= sigma_i / sqrt(1 - beta) (Cauchy-Schwarz), so sigma_i <= r_F sqrt(dt) sqrt(1 - beta) suffices
if abs(rf * np.sqrt(1 - b) - .0089) > 1e-4: err('F-1: distribution-free bound differs from §6.1')
for w in W[:50]:
    if not (-Z[np.argsort(-Z @ w)[-kq:]].mean(0) <= Z.std(0) / np.sqrt(1 - b)).all(): err('F-1: Cauchy-Schwarz tail bound violated'); break

assert not errors, 'S4.13 registry check failed:\n  - ' + '\n  - '.join(errors)
cnt = lambda rows, col: {v: sum(r[col] == v for r in rows) for v in sorted({r[col] for r in rows})}
kinds = cnt([{'K': 'CONDITIONAL' if COND.match(r['Kind']) else r['Kind']} for r in estimators], 'K')
print(f"PASS S4.13 registry: {len(in_scope)} method records (from headings; {len(out_of_scope)} S4.14 roles excluded) in "
      f"{len(methods)} rows + {len(cross)} cross-cutting consumers; {len(O)} objects, {len(P)} problems; {len(E)} candidates "
      f"{kinds}, all 'candidate', no threshold set; Binding {cnt(methods + cross, 'Binding')}; "
      f"{scn_checked} scenario/path rows match S412-D6 {EXPECT}; {len(cited)} decision IDs found elsewhere; facts: sample "
      f"covariance singular for T <= N, residual variance needs p > m + 1; F-1: exact condition (normal: LO-GMV vol > "
      f"{rf / c2:.4f} annual; cases base/B/C), scenario CVaR annual none / monthly {wz.round(3)} -> {wr.round(3)}, D1 V0 "
      f"invariant, distribution-free bound {rf * np.sqrt(1 - b):.4f}. Not checked: estimator suitability, the object "
      f"partition, tag assignment beyond vocabulary, the records' own correctness.")
