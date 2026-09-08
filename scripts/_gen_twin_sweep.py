"""Generate the DIGITAL-TWIN Day-1 OpenMC sweep from the locked design notebook.
Includes the notebook's def cells {0..6,8} (build_core etc.), then appends a
Latin-Hypercube sweep over {moderator T, fuel T, rods inserted, void} at BOC,
logging k_eff + the per-assembly power map per point. Resumable. STAT_MEDIUM."""
import json, re, os

NB  = "/home/samira/ref_neutronics.ipynb"
OUT = "/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/digital_twin/twin_sweep.py"
INCLUDE = {0, 1, 2, 3, 4, 5, 6, 8}
CALL = re.compile(r"(?:calc_\w+|plot_\w+|record_\w+|write_\w+|build_shielded_model|"
                  r"extract_absorber)\s*\(|\.(?:run|integrate)\s*\(")

def neutralize(src):
    out = []
    for l in src.splitlines():
        if l.lstrip().startswith("%") or "get_ipython()" in l:
            continue
        indented = l[:1] in (" ", "\t")
        isdef = l.lstrip().startswith(("def ", "class ", "import ", "from ", "@"))
        if (not indented) and (not isdef) and CALL.search(l):
            out.append("# [neutralized] " + l)
        else:
            out.append(l)
    return "\n".join(out)

nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))
code = [c for c in nb["cells"] if c["cell_type"] == "code"]
parts = ["import matplotlib\nmatplotlib.use('Agg')\nimport os\n"]
for idx, c in enumerate(code):
    if idx in INCLUDE:
        parts.append(f"\n# ===== ref cell #{idx} =====\n" + neutralize("".join(c["source"])) + "\n")

DRIVER = r'''
# ============================================================================
# DIGITAL-TWIN sweep (Day 1) — LHS over operating envelope at BOC; k + power map
# ============================================================================
import json as _json, numpy as _np, glob
from pathlib import Path

OUT = Path(os.environ.get("TWIN_OUT", os.path.join(os.path.dirname(__file__), "sweep")))
OUT.mkdir(parents=True, exist_ok=True); (OUT / "maps").mkdir(exist_ok=True)
N_PTS = int(os.environ.get("TWIN_N", "120"))
SEED  = int(os.environ.get("TWIN_SEED", "12345"))
_STAT_MAP = {"fast": STAT_FAST, "medium": STAT_MEDIUM, "final": STAT_FINAL}
STAT = _STAT_MAP.get(os.environ.get("TWIN_STAT", "custom"),
                     dict(batches=int(os.environ.get("TWIN_BATCHES", "220")),
                          inactive=int(os.environ.get("TWIN_INACTIVE", "50")),
                          particles=int(os.environ.get("TWIN_PARTICLES", "25000"))))
print(f"[twin] N={N_PTS} STAT={STAT} seed={SEED} -> {OUT}", flush=True)
ROOT = OUT / "runs"; ROOT.mkdir(parents=True, exist_ok=True)   # statepoints on ext4 (fast), not /mnt/d

# water density vs moderator T at 12.8 MPa (IAPWS-IF97)
_RHO_T = [(294,1.003),(323,0.994),(373,0.963),(423,0.922),(473,0.870),(523,0.803),(556,0.748)]
def _rho(T): return float(_np.interp(T, [t for t,_ in _RHO_T], [r for _,r in _RHO_T]))

# control rods inserted, by centrality (n of the 12 CRAs)
_cra = [(i,j) for j in range(N_CORE) for i in range(N_CORE) if CR_MAP[N_CORE-1-j,i]==1]
_cc = (N_CORE-1)//2
_cra_sorted = sorted(_cra, key=lambda p:(p[0]-_cc)**2 + (p[1]-_cc)**2)
def _rods(n): return set(_cra_sorted[:int(n)])

# Latin-Hypercube over [T_mod(294-560 K), T_fuel(600-1200 K), n_rods(0-12), void(0-0.20)]
_lo = _np.array([294., 600., 0., 0.00]); _hi = _np.array([560., 1200., 12., 0.20])
try:
    from scipy.stats.qmc import LatinHypercube
    _u = LatinHypercube(d=4, seed=SEED).random(N_PTS)
except Exception:
    _u = _np.random.default_rng(SEED).random((N_PTS, 4))
X = _lo + _u * (_hi - _lo)
X[:, 2] = _np.round(X[:, 2])                       # n_rods -> integer 0..12

# per-assembly x axial fission mesh (7x7x10)
_S = N_CORE * FA_PITCH; _H = ACTIVE_HEIGHT
def _tally():
    m = openmc.RegularMesh(); m.dimension = (N_CORE, N_CORE, 10)
    m.lower_left = (-_S/2, -_S/2, -_H/2); m.upper_right = (_S/2, _S/2, _H/2)
    t = openmc.Tally(name="fiss"); t.filters = [openmc.MeshFilter(m)]; t.scores = ["fission"]
    return t

_csv = OUT / "core_sweep.csv"
_done = set()
if _csv.exists():
    for ln in _csv.read_text().splitlines()[1:]:
        if ln.strip(): _done.add(int(ln.split(",")[0]))
else:
    _csv.write_text("id,T_mod_K,T_fuel_K,n_rods_in,void,k_eff,k_sigma_pcm,F_assembly\n")

for i in range(N_PTS):
    if i in _done:
        continue
    Tm, Tf, nr, vo = float(X[i,0]), float(X[i,1]), int(X[i,2]), float(X[i,3])
    model, _, _ = build_core(fuel_temp=Tf, mod_temp=Tm, water_density=_rho(Tm),
                             control_rod_state=_rods(nr), void_fraction=vo, stats=STAT)
    model.tallies = openmc.Tallies([_tally()])
    d = _run_dir(f"twin_{i:03d}"); _run_model(model, d, tag=f"twin{i}")
    k, s = _keff(d)
    sp = sorted(Path(d).glob("statepoint.*.h5"))[-1]
    with openmc.StatePoint(str(sp)) as st:
        fis = st.get_tally(name="fiss").mean.ravel()
    fmap = fis.reshape(10, N_CORE, N_CORE)          # [z, y, x]
    _np.save(OUT / "maps" / f"map_{i:03d}.npy", fmap)
    radial = fmap.sum(axis=0); nz = radial[radial > 0]
    fa = float(radial.max() / nz.mean()) if nz.size else 0.0
    with open(_csv, "a") as f:
        f.write(f"{i},{Tm:.1f},{Tf:.1f},{nr},{vo:.4f},{k:.6f},{s*1e5:.1f},{fa:.4f}\n")
    print(f"[twin] {i+1}/{N_PTS}  Tm={Tm:.0f} Tf={Tf:.0f} nrod={nr} void={vo:.3f}"
          f" -> k={k:.5f} ({s*1e5:.0f} pcm)  F_FA={fa:.3f}", flush=True)

if len(_done) + sum(1 for i in range(N_PTS) if i not in _done) >= N_PTS:
    print("TWIN_SWEEP_COMPLETE ->", _csv)
'''
parts.append(DRIVER)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write("".join(parts))
print(f"wrote {OUT} | cells {sorted(INCLUDE)}")
