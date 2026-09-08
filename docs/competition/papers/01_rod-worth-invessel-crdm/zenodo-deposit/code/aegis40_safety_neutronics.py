import matplotlib
matplotlib.use('Agg')
import os

# ===== ref cell #0 =====
import os, sys, math, time, json
from pathlib import Path
from datetime import datetime

import numpy as np
import yaml

import openmc
import openmc.deplete

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Threads ──────────────────────────────────────────────────────────────
THREADS = int(os.environ.get("OPENMC_THREADS", "6"))
os.environ["OMP_NUM_THREADS"] = str(THREADS)

# ── Data library paths ───────────────────────────────────────────────────
XS = Path(os.environ.get(
    "OPENMC_CROSS_SECTIONS",
    "/mnt/d/openmc_data/endfb-viii.0-hdf5/cross_sections.xml"))
CHAIN = Path(os.environ.get(
    "OPENMC_CHAIN_FILE",
    "/mnt/d/openmc_data/chain_endfb80_pwr.xml"))

if not XS.is_file():
    raise FileNotFoundError(
        f"Cross-section file not found: {XS}\nSet OPENMC_CROSS_SECTIONS.")
if not CHAIN.is_file():
    raise FileNotFoundError(
        f"Depletion chain not found: {CHAIN}\nSet OPENMC_CHAIN_FILE.")

os.environ["OPENMC_CROSS_SECTIONS"] = str(XS)
os.environ["OPENMC_CHAIN_FILE"]     = str(CHAIN)
openmc.config["cross_sections"]     = str(XS)
openmc.config["chain_file"]         = str(CHAIN)

# ── Output tree ──────────────────────────────────────────────────────────
DESIGN = "hybrid"   # "hybrid" = Gd₂O₃ + Er₂O₃
ROOT  = Path("./aegis40_neutronics_outputs").resolve()
ROOT.mkdir(parents=True, exist_ok=True)
PLOTS = ROOT / "plots"; PLOTS.mkdir(exist_ok=True)

print("=" * 60)
print("Aegis-40 OpenMC — 3D CORE notebook")
print(f"  XS:      {XS}")
print(f"  Chain:   {CHAIN}")
print(f"  Threads: {THREADS}")
print(f"  Design:  {DESIGN}")
print(f"  Output:  {ROOT}")
print(f"  OpenMC:  {openmc.__version__}")
print("=" * 60)

# ===== ref cell #1 =====
# ============================================================================
# Aegis-40 — locked neutronic design constants
# ============================================================================

# Fuel rod / lattice geometry — Westinghouse 17x17 (FIXED: defines the T-H mesh)
N_PIN         = 17
PIN_PITCH     = 1.2623     # cm
FA_PITCH      = 21.6038    # cm
FUEL_RADIUS   = 0.40958    # cm   pellet
CLAD_INNER_R  = 0.41873    # cm
CLAD_OUTER_R  = 0.47600    # cm   Zircaloy-4
ACTIVE_HEIGHT = 200.0      # cm

# Core layout — 37 FA, 7-wide octagonal (rows 3-5-7-7-7-5-3)
N_CORE        = 7
CORE_MAP = np.array([
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0, 0],
])
N_FA_TOTAL = int(CORE_MAP.sum())          # 37

# Control-rod-cluster assemblies — 12 CRAs (checkerboard; central FA = instrument)
CR_MAP = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
])
N_CR_CLUSTERS = int(CR_MAP.sum())         # 12

# Reflector / plena — 20 cm radial water reflector, 30 cm axial water plena, vacuum BCs
RADIAL_REFLECTOR_CM   = 20.0
AXIAL_REFLECTOR_CM    = 30.0
RADIAL_REFLECTOR_MODE = "water"           # "water" | "steel" (heavy reflector option)

# Enrichment — 3-zone intra-assembly radial grade (centre-hot / edge-cool), <= 4.95% LEU
ENRICH_INNER  = 4.95       # wt% U-235, assembly centre
ENRICH_MID    = 4.70
ENRICH_OUTER  = 4.40       # zone grade; true core-avg computed in cell 27
ZONE_R1_CM    = 4.5
ZONE_R2_CM    = 8.5
EDGE_PIN_GRADING = True     # de-rate the FA-perimeter pin ring (boron-free de-peaking)
EDGE_ENRICH      = 3.6     # LOCKED: sharper FA-perimeter de-rate (de-peak)
RADIAL_ENRICH_ZONING = True               # LOCKED: discrete uniform-enrichment assemblies (Approach B)
RING_ENRICH = {0: 4.95, 1: 4.7, 2: 4.4, 3: 4.0}   # LOCKED in-out: high centre (Gd-suppressed) / low periphery

# Burnable absorber — integral Gd2O3 + light Er2O3 (soluble-boron-free hold-down)
GD_WT_PCT       = 6        # wt% Gd2O3 in the Gd-bearing rods (LOCKED)
N_GD_RODS       = 20       # per-FA average, ring-zoned (LOCKED; was 32 -> over-loaded keff)
GD_AXIAL_CUT_CM = 10.0     # plain-UO2 Gd cutback at each rod end
RADIAL_GD_ZONING = True     # heavier-centre Gd flattens radial power (replaces boron shaping)
GD_RING_WEIGHTS  = {0: 1.65, 1: 1.45, 2: 0.95, 3: 0.68}   # rings 1/8/16/12; core-avg ~1.0
AXIAL_BLANKET_CM     = 0.0  # optional reduced-enrichment axial blanket (0 = off)
AXIAL_BLANKET_ENRICH = 2.5
if DESIGN == "hybrid":
    ER_WT_PCT = 0.75        # light Er hold-down through mid/late cycle + cold SDM
    N_ER_RODS = 16
else:
    ER_WT_PCT = 0.0
    N_ER_RODS = 0

# Optional WABA B4C guide-tube rods (solid, SBF-compatible) — off in the locked design
WABA_ENABLE  = False
WABA_RINGS   = (2,)
WABA_B4C_WT  = 12.0
WABA_R_IN    = 0.286
WABA_R_OUT   = 0.404

# Material densities (g/cm3)
RHO_UO2 = 10.40; RHO_GD2O3 = 7.41; RHO_ER2O3 = 8.64
RHO_ZIRC = 6.55; RHO_HE = 0.0001786; RHO_B4C = 2.52

# Primary operating conditions (FER section 8.4 design basis: 12.8 MPa, Tavg 283 C)
T_FUEL_K      = 900.0
T_MOD_K       = 556.0      # core-average moderator, 283 C @ 12.8 MPa
RHO_WATER_NOM = 0.748      # g/cm3, IAPWS-IF97 @ 556 K, 12.8 MPa

# Core power / fuel cycle
CORE_POWER_MWT = 125.0
HM_MASS_T      = 9.87       # 37 FA
SPECIFIC_POWER = CORE_POWER_MWT / HM_MASS_T
N_BATCHES      = 4

# Monte Carlo statistics (bump to STAT_FINAL for reported numbers)
STAT_FAST   = dict(batches=80,  inactive=25, particles=5000)
STAT_MEDIUM = dict(batches=180, inactive=50, particles=20000)
STAT_FINAL  = dict(batches=400, inactive=80, particles=50000)
STAT = STAT_MEDIUM

_enr_avg = (ENRICH_INNER + 2*ENRICH_MID + ENRICH_OUTER) / 4.0
print(f"Core: {N_FA_TOTAL} FA (7-wide octagon) | {N_CR_CLUSTERS} control-rod clusters")
print(f"Enrichment {ENRICH_INNER}/{ENRICH_MID}/{ENRICH_OUTER} wt% (zone-avg ~{_enr_avg:.2f}, excl. edge/BA) | Gd2O3 {GD_WT_PCT} wt%x{N_GD_RODS} + Er2O3 {ER_WT_PCT} wt%x{N_ER_RODS}")
print(f"Power {CORE_POWER_MWT} MWth | HM {HM_MASS_T} t | specific power {SPECIFIC_POWER:.2f} W/gHM | {N_BATCHES}-batch")
print(f"Coolant/moderator 12.8 MPa, T_mod {T_MOD_K} K, rho {RHO_WATER_NOM} g/cm3 | MC {STAT}")

# ===== ref cell #2 =====
# ============================================================================
# Material factories
# ============================================================================

def mat_uo2(enrichment, temp=T_FUEL_K, name=None):
    m = openmc.Material(name=name or f"UO2_{enrichment:.2f}pct", temperature=temp)
    m.set_density("g/cm3", RHO_UO2)
    m.add_element("U", 1.0, enrichment=enrichment)
    m.add_element("O", 2.0)
    m.depletable = True
    return m


def _mixed_fuel(base_enrich, gd_wt=0.0, er_wt=0.0, temp=T_FUEL_K, name="fuel"):
    uo2_frac = 1.0 - (gd_wt + er_wt) / 100.0
    components, fracs = [], []
    uo2 = mat_uo2(base_enrich, temp=temp, name=f"{name}_uo2")
    components.append(uo2); fracs.append(uo2_frac)
    if gd_wt > 0:
        m = openmc.Material(name=f"{name}_gd2o3", temperature=temp)
        m.set_density("g/cm3", RHO_GD2O3)
        m.add_element("Gd", 2.0); m.add_element("O", 3.0)
        components.append(m); fracs.append(gd_wt / 100.0)
    if er_wt > 0:
        m = openmc.Material(name=f"{name}_er2o3", temperature=temp)
        m.set_density("g/cm3", RHO_ER2O3)
        m.add_element("Er", 2.0); m.add_element("O", 3.0)
        components.append(m); fracs.append(er_wt / 100.0)
    mixed = openmc.Material.mix_materials(components, fracs,
                                          percent_type="wo", name=name)
    mixed.temperature = temp
    mixed.depletable = True
    return mixed


def mat_water(temp=T_MOD_K, density=RHO_WATER_NOM, name="H2O"):
    m = openmc.Material(name=name, temperature=temp)
    m.set_density("g/cm3", density)
    m.add_element("H", 2.0); m.add_element("O", 1.0)
    m.add_s_alpha_beta("c_H_in_H2O")
    return m


def mat_zircaloy(temp=600.0):
    m = openmc.Material(name="Zircaloy-4", temperature=temp)
    m.set_density("g/cm3", RHO_ZIRC)
    m.add_element("Zr", 0.9823, percent_type="wo")
    m.add_element("Sn", 0.0145, percent_type="wo")
    m.add_element("Fe", 0.0021, percent_type="wo")
    m.add_element("Cr", 0.0011, percent_type="wo")
    return m


def mat_helium(temp=T_FUEL_K):
    m = openmc.Material(name="He gap", temperature=temp)
    m.set_density("g/cm3", RHO_HE)
    m.add_element("He", 1.0)
    return m


def mat_b4c(temp=600.0):
    m = openmc.Material(name="B4C", temperature=temp)
    m.set_density("g/cm3", RHO_B4C)
    m.add_element("B", 4.0)
    m.add_element("C", 1.0)
    return m


def mat_waba(b4c_wt=None, temp=T_MOD_K, name="WABA_B4C_Al2O3"):
    """WABA absorber annulus: B4C dispersed in an Al2O3 matrix — a SOLID burnable
       poison (not soluble boron). Depletable so B-10 burns out like a real WABA."""
    if b4c_wt is None:
        b4c_wt = WABA_B4C_WT
    al2o3 = openmc.Material(name="Al2O3", temperature=temp)
    al2o3.set_density("g/cm3", 3.97)
    al2o3.add_element("Al", 2.0); al2o3.add_element("O", 3.0)
    m = openmc.Material.mix_materials([mat_b4c(temp=temp), al2o3],
                                      [b4c_wt / 100.0, 1.0 - b4c_wt / 100.0],
                                      percent_type="wo", name=name)
    m.temperature = temp
    m.depletable = True
    return m

# ===== ref cell #3 =====
# ── Intra-FA pin map ────────────────────────────────────────────────────
CENTER_IDX     = (N_PIN - 1) // 2
INSTRUMENT_POS = (CENTER_IDX, CENTER_IDX)

GUIDE_ALL = [
    (5,2),(8,2),(11,2),(3,3),(13,3),
    (2,5),(5,5),(8,5),(11,5),(14,5),
    (5,8),(8,8),(11,8),(2,8),(14,8),
    (2,11),(5,11),(8,11),(11,11),(14,11),
    (3,13),(13,13),(5,14),(8,14),(11,14),
]
GUIDE_POS = [p for p in GUIDE_ALL if p != INSTRUMENT_POS]              # 24 guides
FUEL_POS  = [(i,j) for j in range(N_PIN) for i in range(N_PIN)
             if (i,j) not in set(GUIDE_ALL)]                           # 264 fuel pins
assert len(FUEL_POS) == 264 and len(GUIDE_POS) == 24


def _pin_radius(i, j):
    cx = (N_PIN - 1) / 2.0
    return math.hypot((i - cx) * PIN_PITCH, (j - cx) * PIN_PITCH)


def _enrichment_for_pin(i, j):
    # Outermost pin ring (FA perimeter) faces the inter-assembly water gaps, where
    # thermal flux — and hence per-pin power — peaks: the main driver of F_ΔH.
    # Give that ring its own, lower enrichment when EDGE_PIN_GRADING is on.
    if EDGE_PIN_GRADING and (i in (0, N_PIN - 1) or j in (0, N_PIN - 1)):
        return EDGE_ENRICH
    r = _pin_radius(i, j)
    if r < ZONE_R1_CM:   return ENRICH_INNER
    if r < ZONE_R2_CM:   return ENRICH_MID
    return ENRICH_OUTER


def _symmetry_group(i, j, exclude=None):
    c = N_PIN - 1
    pts = {(i,j),(c-i,j),(i,c-j),(c-i,c-j),
           (j,i),(c-j,i),(j,c-i),(c-j,c-i)}
    ex = set(exclude or [])
    return tuple(sorted(p for p in pts if p in set(FUEL_POS) and p not in ex))


def _select_sym_positions(n, bias="mid", exclude=None):
    exclude = set(exclude or [])
    seen, groups = set(), []
    for ij in FUEL_POS:
        if ij in exclude: continue
        g = _symmetry_group(*ij, exclude=exclude)
        if not g or g in seen: continue
        seen.add(g)
        r_mean = sum(_pin_radius(*p) for p in g) / len(g)
        if   bias == "inner": score =  r_mean
        elif bias == "outer": score = -r_mean
        else:                 score = abs(r_mean - 5.2 * PIN_PITCH)
        groups.append((score, g))
    chosen = []
    for _, g in sorted(groups):
        if len(chosen) + len(g) <= n: chosen.extend(g)
        if len(chosen) == n: break
    return chosen[:n]


GD_POSITIONS = set(_select_sym_positions(N_GD_RODS, bias="mid"))
ER_POSITIONS = set(_select_sym_positions(N_ER_RODS, bias="outer", exclude=GD_POSITIONS))
print(f"Gd rods/FA (avg): {len(GD_POSITIONS)}  |  Er rods/FA: {len(ER_POSITIONS)}")


# ── Radial (assembly) ring helpers for Gd power-flattening ──────────
def _core_ring_of(i, j):
    """Radial ring of a core position: 0=centre, 1=inner8, 2=mid16, 3=outer12."""
    cc = (N_CORE - 1) // 2                          # centre index = 3 for 7-wide
    return min(max(abs(i - cc), abs(j - cc)), 3)    # Chebyshev distance, capped at 3

def _gd_count_for_ring(ring):
    """Per-ring Gd-rod count; uniform N_GD_RODS unless RADIAL_GD_ZONING."""
    if not RADIAL_GD_ZONING:
        return N_GD_RODS
    return int(round(N_GD_RODS * GD_RING_WEIGHTS.get(ring, 1.0)))

def _gd_positions_for_ring(ring):
    return set(_select_sym_positions(_gd_count_for_ring(ring), bias="mid"))

def _er_positions_for_ring(ring):
    gd = _gd_positions_for_ring(ring)
    return set(_select_sym_positions(N_ER_RODS, bias="outer", exclude=gd))

if RADIAL_GD_ZONING:
    print("Radial Gd zoning per ring (centre→edge): "
          + ", ".join(f"r{r}={_gd_count_for_ring(r)}" for r in (0, 1, 2, 3)))

# ===== ref cell #4 =====
# ============================================================================
# Pin universe — radially structured; axial fuel bounds applied here
# ============================================================================
def _make_pin_universe(fuel_mat, water_mat, clad_mat, gap_mat,
                       name="pin", gd_cut_bot=0.0, gd_cut_top=0.0, cutback_mat=None,
                       blanket_mat=None, blanket_cm=0.0):
    """Pin universe valid for **all z**. Inside z ∈ [-H/2, +H/2] is fuel+clad+gap+moderator;
       outside (axial plena) every radial position becomes water.
       If blanket_mat/blanket_cm given, the top & bottom blanket_cm of the active
       column become reduced-enrichment blanket fuel (applies to EVERY pin and
       supersedes the Gd axial cutback). Otherwise the optional Gd axial cutback
       (plain UO₂) is applied at the top/bottom of the active region."""
    fuel_cyl = openmc.ZCylinder(r=FUEL_RADIUS)
    clad_i   = openmc.ZCylinder(r=CLAD_INNER_R)
    clad_o   = openmc.ZCylinder(r=CLAD_OUTER_R)
    zbot = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0)
    ztop = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0)

    cutback_mat = cutback_mat or fuel_mat
    cells = []

    if blanket_mat is not None and blanket_cm > 0:
        # — Reduced-enrichment axial blanket at each end (all pins) —
        zbb = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0 + blanket_cm)
        ztb = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0 - blanket_cm)
        cells.append(openmc.Cell(name=f"{name}_blk_bot", fill=blanket_mat,
                                 region=-fuel_cyl & +zbot & -zbb))
        cells.append(openmc.Cell(name=f"{name}_fuel", fill=fuel_mat,
                                 region=-fuel_cyl & +zbb & -ztb))
        cells.append(openmc.Cell(name=f"{name}_blk_top", fill=blanket_mat,
                                 region=-fuel_cyl & +ztb & -ztop))
    else:
        # — Active-region fuel column with optional Gd axial cutback —
        if gd_cut_bot > 0:
            zb = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0 + gd_cut_bot)
            cells.append(openmc.Cell(name=f"{name}_bot_cut", fill=cutback_mat,
                                     region=-fuel_cyl & +zbot & -zb))
        else:
            zb = zbot

        if gd_cut_top > 0:
            zt = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0 - gd_cut_top)
            cells.append(openmc.Cell(name=f"{name}_fuel", fill=fuel_mat,
                                     region=-fuel_cyl & +zb & -zt))
            cells.append(openmc.Cell(name=f"{name}_top_cut", fill=cutback_mat,
                                     region=-fuel_cyl & +zt & -ztop))
        else:
            zt = ztop
            cells.append(openmc.Cell(name=f"{name}_fuel", fill=fuel_mat,
                                     region=-fuel_cyl & +zb & -zt))

    # gap + clad + moderator (only inside active region)
    cells.append(openmc.Cell(name=f"{name}_gap",  fill=gap_mat,
                             region=+fuel_cyl & -clad_i & +zbot & -ztop))
    cells.append(openmc.Cell(name=f"{name}_clad", fill=clad_mat,
                             region=+clad_i & -clad_o & +zbot & -ztop))
    cells.append(openmc.Cell(name=f"{name}_mod",  fill=water_mat,
                             region=+clad_o & +zbot & -ztop))

    # Axial water plenum (above and below active region — radially unbounded)
    cells.append(openmc.Cell(name=f"{name}_plenum_top", fill=water_mat,
                             region=+ztop))
    cells.append(openmc.Cell(name=f"{name}_plenum_bot", fill=water_mat,
                             region=-zbot))

    return openmc.Universe(name=name, cells=cells)


def _make_guide_universe(water_mat, b4c_mat=None, waba_mat=None, name="guide"):
    """Guide tube. b4c_mat → B4C control rod in active region (ARI). waba_mat →
       WABA burnable-poison annulus (water centre, B4C-Al2O3 ring, water gap).
       Neither → plain water (ARO). Axially open with water plena outside H."""
    gt_inner = openmc.ZCylinder(r=0.5624)
    gt_outer = openmc.ZCylinder(r=0.6020)
    zbot = openmc.ZPlane(z0=-ACTIVE_HEIGHT / 2.0)
    ztop = openmc.ZPlane(z0= ACTIVE_HEIGHT / 2.0)
    cells = []
    if waba_mat is not None and b4c_mat is None:
        r_in  = openmc.ZCylinder(r=WABA_R_IN)
        r_out = openmc.ZCylinder(r=WABA_R_OUT)
        cells.append(openmc.Cell(fill=water_mat, region=-r_in & +zbot & -ztop))
        cells.append(openmc.Cell(fill=waba_mat,  region=+r_in & -r_out & +zbot & -ztop))
        cells.append(openmc.Cell(fill=water_mat, region=+r_out & -gt_inner & +zbot & -ztop))
    else:
        inner_fill = b4c_mat if b4c_mat is not None else water_mat
        cells.append(openmc.Cell(fill=inner_fill, region=-gt_inner & +zbot & -ztop))
    cells.append(openmc.Cell(fill=water_mat, region=+gt_inner & -gt_outer & +zbot & -ztop))
    cells.append(openmc.Cell(fill=water_mat, region=+gt_outer & +zbot & -ztop))
    cells.append(openmc.Cell(fill=water_mat, region=+ztop))
    cells.append(openmc.Cell(fill=water_mat, region=-zbot))
    return openmc.Universe(name=name, cells=cells)

# ===== ref cell #5 =====
# ============================================================================
# Assembly universe builder
# ============================================================================
def _build_fa_universe(fuel_temp, mod_temp, water, clad, gap, b4c,
                       plain_mats, gd_mat, gd_cut_mat, er_mat,
                       insert_cr, name="FA",
                       gd_positions=None, er_positions=None, blanket_mat=None,
                       waba_mat=None, fa_enrich=None):
    """Return a Universe containing the 17×17 pin lattice inside an FA-pitch square.
       insert_cr: True → guide tubes filled with B4C (control rod inserted)
                  False → guide tubes filled with water (rod out)
       gd_positions / er_positions: per-assembly BA pin sets (default = the
       uniform/ring-average globals)."""
    if gd_positions is None: gd_positions = GD_POSITIONS
    if er_positions is None: er_positions = ER_POSITIONS

    pin_universes = {}
    for (i, j) in FUEL_POS:
        e = fa_enrich if fa_enrich is not None else _enrichment_for_pin(i, j)
        ukey = f"plain_{e:.1f}"
        if ukey not in pin_universes:
            pin_universes[ukey] = _make_pin_universe(
                plain_mats[f"UO2_{e:.1f}"], water, clad, gap, name=f"{name}_{ukey}",
                blanket_mat=blanket_mat, blanket_cm=AXIAL_BLANKET_CM)

    gd_pin_u = _make_pin_universe(gd_mat, water, clad, gap, name=f"{name}_Gd_pin",
                                  gd_cut_bot=GD_AXIAL_CUT_CM,
                                  gd_cut_top=GD_AXIAL_CUT_CM,
                                  cutback_mat=gd_cut_mat,
                                  blanket_mat=blanket_mat, blanket_cm=AXIAL_BLANKET_CM)
    pin_universes["gd"] = gd_pin_u

    er_pin_u = None
    if er_mat is not None and er_positions:
        er_pin_u = _make_pin_universe(er_mat, water, clad, gap, name=f"{name}_Er_pin",
                                      blanket_mat=blanket_mat, blanket_cm=AXIAL_BLANKET_CM)
        pin_universes["er"] = er_pin_u

    guide_aro_u = _make_guide_universe(water, b4c_mat=None,
                                       name=f"{name}_guide_aro")
    guide_ari_u = _make_guide_universe(water, b4c_mat=b4c,
                                       name=f"{name}_guide_ari")
    guide_waba_u = (_make_guide_universe(water, waba_mat=waba_mat,
                                         name=f"{name}_guide_waba")
                    if waba_mat is not None else None)
    instrument_u = guide_aro_u   # instrument tube never gets a rod

    lattice = openmc.RectLattice(name=f"{name}_pinlattice")
    lattice.pitch = (PIN_PITCH, PIN_PITCH)
    lattice.lower_left = (-N_PIN * PIN_PITCH / 2.0, -N_PIN * PIN_PITCH / 2.0)
    lattice.outer = openmc.Universe(cells=[openmc.Cell(fill=water)])

    grid = []
    for j in range(N_PIN - 1, -1, -1):
        row = []
        for i in range(N_PIN):
            pos = (i, j)
            if pos == INSTRUMENT_POS:
                row.append(instrument_u)
            elif pos in set(GUIDE_POS):
                if insert_cr:
                    row.append(guide_ari_u)
                elif guide_waba_u is not None:
                    row.append(guide_waba_u)
                else:
                    row.append(guide_aro_u)
            elif pos in gd_positions:
                row.append(gd_pin_u)
            elif pos in er_positions and er_pin_u is not None:
                row.append(er_pin_u)
            else:
                e = fa_enrich if fa_enrich is not None else _enrichment_for_pin(i, j)
                row.append(pin_universes[f"plain_{e:.1f}"])
        grid.append(row)
    lattice.universes = grid

    # FA cell: pin lattice clipped to one FA pitch (square)
    half_fa = FA_PITCH / 2.0
    xlo = openmc.XPlane(-half_fa)
    xhi = openmc.XPlane( half_fa)
    ylo = openmc.YPlane(-half_fa)
    yhi = openmc.YPlane( half_fa)
    fa_cell = openmc.Cell(name=f"{name}_cell", fill=lattice,
                          region=+xlo & -xhi & +ylo & -yhi)

    return openmc.Universe(name=f"{name}_universe", cells=[fa_cell])


def _water_assembly_universe(water, name="water_FA"):
    """Pure-water universe used for the corners of the core lattice."""
    half_fa = FA_PITCH / 2.0
    xlo = openmc.XPlane(-half_fa); xhi = openmc.XPlane(half_fa)
    ylo = openmc.YPlane(-half_fa); yhi = openmc.YPlane(half_fa)
    cell = openmc.Cell(name=f"{name}_cell", fill=water,
                       region=+xlo & -xhi & +ylo & -yhi)
    return openmc.Universe(name=name, cells=[cell])

# ===== ref cell #6 =====
# ============================================================================
# build_core — full 3D core model (this is what every analysis now uses)
# ============================================================================
def build_core(fuel_temp=T_FUEL_K, mod_temp=T_MOD_K,
               water_density=RHO_WATER_NOM,
               control_rod_state="aro",     # "aro" | "ari" | iterable of (i,j) inserted FA positions
               void_fraction=0.0,
               stats=None):
    """Build the 3D 37-FA core model with vacuum BCs on all 6 outer surfaces.
       Returns (model, mat_dict, fa_volume_info)."""
    stats = stats or STAT
    eff_density = water_density * (1.0 - void_fraction)

    water = mat_water(temp=mod_temp, density=eff_density, name="H2O_active")
    clad  = mat_zircaloy(temp=mod_temp)
    gap   = mat_helium(temp=fuel_temp)
    b4c   = mat_b4c(temp=600.0)

    # Distinct cool water for radial+axial reflector (own depletable=False)
    refl_water = mat_water(temp=mod_temp, density=RHO_WATER_NOM, name="H2O_reflector")
    # Optional SS-304 heavy reflector replacing the water radial reflector
    refl_steel = None
    if RADIAL_REFLECTOR_MODE == "steel":
        refl_steel = openmc.Material(name="SS304_reflector", temperature=mod_temp)
        refl_steel.set_density("g/cm3", 7.90)
        for _el, _f in (("Fe", .685), ("Cr", .190), ("Ni", .095),
                        ("Mn", .020), ("Si", .010)):
            refl_steel.add_element(_el, _f, "wo")
        refl_steel.depletable = False
    refl_fill = refl_steel if refl_steel is not None else refl_water

    _enr_levels = {ENRICH_INNER, ENRICH_MID, ENRICH_OUTER}
    if EDGE_PIN_GRADING: _enr_levels.add(EDGE_ENRICH)
    if RADIAL_ENRICH_ZONING: _enr_levels.update(RING_ENRICH.values())
    plain_mats = {}
    for e in sorted(_enr_levels):
        plain_mats[f"UO2_{e:.1f}"] = mat_uo2(e, temp=fuel_temp, name=f"UO2_{e:.1f}")

    gd_mat     = _mixed_fuel(ENRICH_MID, gd_wt=GD_WT_PCT, er_wt=0.0,
                             temp=fuel_temp, name="Gd_fuel")
    gd_cut_mat = mat_uo2(ENRICH_MID, temp=fuel_temp, name="Gd_cutback_UO2")
    blanket_mat = (mat_uo2(AXIAL_BLANKET_ENRICH, temp=fuel_temp, name="UO2_blanket")
                   if AXIAL_BLANKET_CM > 0 else None)
    waba_mat = mat_waba(temp=mod_temp) if WABA_ENABLE else None

    if N_ER_RODS > 0 and ER_WT_PCT > 0:
        er_mat = _mixed_fuel(ENRICH_MID, gd_wt=0.0, er_wt=ER_WT_PCT,
                             temp=fuel_temp, name="Er_fuel")
    else:
        er_mat = None

    mat_dict = {"water": water, "refl_water": refl_water, "clad": clad,
                "gap": gap, "b4c": b4c, "gd_fuel": gd_mat, "gd_cutback": gd_cut_mat}
    if blanket_mat is not None: mat_dict["blanket"] = blanket_mat
    if waba_mat is not None: mat_dict["waba"] = waba_mat
    if er_mat is not None: mat_dict["er_fuel"] = er_mat
    mat_dict.update(plain_mats)

    # Decide which FA positions have CR inserted
    if control_rod_state == "aro":
        cr_inserted_positions = set()
    elif control_rod_state == "ari":
        cr_inserted_positions = {(i, j) for j in range(N_CORE) for i in range(N_CORE)
                                 if CR_MAP[N_CORE - 1 - j, i] == 1}
    else:
        cr_inserted_positions = set(control_rod_state)

    # ── Per-ring FA universes (radial Gd zoning) ──────────────────
    # Ring 0 = centre FA, 1 = inner 8, 2 = outer 12.  Heavier Gd at the centre
    # pushes power outward.  CR clusters only live in the central 3×3 (rings 0-1),
    # so the CR-in flavour is only built for those rings.
    def _ring_ba(ring):
        if RADIAL_GD_ZONING:
            return _gd_positions_for_ring(ring), _er_positions_for_ring(ring)
        return GD_POSITIONS, ER_POSITIONS

    fa_aro_by_ring, fa_ari_by_ring = {}, {}
    for ring in (0, 1, 2, 3):
        gd, er = _ring_ba(ring)
        fa_aro_by_ring[ring] = _build_fa_universe(
            fuel_temp, mod_temp, water, clad, gap, b4c,
            plain_mats, gd_mat, gd_cut_mat, er_mat,
            insert_cr=False, name=f"FA_aro_r{ring}",
            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat,
            waba_mat=(waba_mat if ring in WABA_RINGS else None),
            fa_enrich=(RING_ENRICH[ring] if RADIAL_ENRICH_ZONING else None))
    for ring in (0, 1, 2, 3):
        gd, er = _ring_ba(ring)
        fa_ari_by_ring[ring] = _build_fa_universe(
            fuel_temp, mod_temp, water, clad, gap, b4c,
            plain_mats, gd_mat, gd_cut_mat, er_mat,
            insert_cr=True, name=f"FA_ari_r{ring}",
            gd_positions=gd, er_positions=er, blanket_mat=blanket_mat,
            fa_enrich=(RING_ENRICH[ring] if RADIAL_ENRICH_ZONING else None))
    water_u = _water_assembly_universe(refl_fill, name="water_FA")

    # ── Core RectLattice (7-wide, 37 FA) ──────────────────────────────────
    core_lat = openmc.RectLattice(name="core_lattice")
    core_lat.pitch = (FA_PITCH, FA_PITCH)
    core_lat.lower_left = (-N_CORE * FA_PITCH / 2.0, -N_CORE * FA_PITCH / 2.0)
    core_lat.outer = water_u

    grid = []
    n_cr_actually_inserted = 0
    for j in range(N_CORE - 1, -1, -1):    # row 0 is bottom in OpenMC convention
        row = []
        for i in range(N_CORE):
            ij = (i, j)
            if CORE_MAP[N_CORE - 1 - j, i] == 0:
                row.append(water_u)
            else:
                ring = _core_ring_of(i, j)
                if ij in cr_inserted_positions and ring in fa_ari_by_ring:
                    row.append(fa_ari_by_ring[ring]); n_cr_actually_inserted += 1
                else:
                    row.append(fa_aro_by_ring[ring])
        grid.append(row)
    core_lat.universes = grid

    # ── Cells: core lattice → radial reflector → outer vacuum box ─────────
    core_half = N_CORE * FA_PITCH / 2.0
    outer_half = core_half + RADIAL_REFLECTOR_CM
    H = ACTIVE_HEIGHT / 2.0
    Z_OUTER = H + AXIAL_REFLECTOR_CM      # vacuum BC at ±(H + axial reflector)

    # Inner core region (lattice covers full radial extent of outer_half — pin universes
    # have their own water plena beyond active height, so axially the lattice is valid
    # everywhere in z).  We bound the lattice in a square of side = 2*core_half.
    xlo_c = openmc.XPlane(-core_half); xhi_c = openmc.XPlane(core_half)
    ylo_c = openmc.YPlane(-core_half); yhi_c = openmc.YPlane(core_half)

    # Outer vacuum box
    xlo = openmc.XPlane(-outer_half, boundary_type="vacuum")
    xhi = openmc.XPlane( outer_half, boundary_type="vacuum")
    ylo = openmc.YPlane(-outer_half, boundary_type="vacuum")
    yhi = openmc.YPlane( outer_half, boundary_type="vacuum")
    zlo = openmc.ZPlane(-Z_OUTER, boundary_type="vacuum")
    zhi = openmc.ZPlane( Z_OUTER, boundary_type="vacuum")

    core_cell = openmc.Cell(name="core_lat_cell", fill=core_lat,
                            region=+xlo_c & -xhi_c & +ylo_c & -yhi_c
                                   & +zlo & -zhi)
    refl_cell = openmc.Cell(name="radial_reflector", fill=refl_fill,
                            region=(+xlo & -xhi & +ylo & -yhi & +zlo & -zhi)
                                   & ~(+xlo_c & -xhi_c & +ylo_c & -yhi_c))

    geom = openmc.Geometry(openmc.Universe(cells=[core_cell, refl_cell]))

    # ── Settings ──────────────────────────────────────────────────────────
    settings = openmc.Settings()
    settings.batches   = stats["batches"]
    settings.inactive  = stats["inactive"]
    settings.particles = stats["particles"]
    settings.temperature = {"method": "nearest", "tolerance": 400.0}
    # Sample initial fission sites only inside the active core region
    settings.source = openmc.IndependentSource(
        space=openmc.stats.Box([-core_half, -core_half, -H],
                               [ core_half,  core_half,  H]),
        constraints={"fissionable": True},
        particle="neutron")

    # Collect every distinct material
    all_mats, seen = [], set()
    def _add(m):
        if m is not None and id(m) not in seen:
            seen.add(id(m)); all_mats.append(m)
    all_fa_us = list(fa_aro_by_ring.values()) + list(fa_ari_by_ring.values())
    for u in all_fa_us:
        for c in u.get_all_cells().values():
            if c.fill is None: continue
            if isinstance(c.fill, openmc.Material): _add(c.fill)
    # Walk sub-universes for nested cells (lattices)
    for u in all_fa_us:
        for sub_u in u.get_all_universes().values():
            for c in sub_u.cells.values():
                if isinstance(c.fill, openmc.Material): _add(c.fill)
    _add(water); _add(refl_water); _add(refl_steel); _add(clad); _add(gap); _add(b4c); _add(gd_cut_mat)
    for m in plain_mats.values(): _add(m)
    _add(gd_mat); _add(er_mat); _add(blanket_mat); _add(waba_mat)

    model = openmc.Model(geometry=geom, settings=settings,
                         materials=openmc.Materials(all_mats))

    # FA volume / inventory info (for depletion power normalisation)
    fa_vol_info = dict(
        n_fa=N_FA_TOTAL,
        n_cr_inserted=n_cr_actually_inserted,
        core_half_cm=core_half,
        outer_half_cm=outer_half,
        z_outer_cm=Z_OUTER,
    )
    return model, mat_dict, fa_vol_info

# ===== ref cell #8 =====
# ============================================================================
# Run helpers + results accumulator
# ============================================================================
results = {}
runtime_log = []

def _run_dir(*parts):
    d = ROOT.joinpath(*[str(p) for p in parts])
    d.mkdir(parents=True, exist_ok=True)
    return d


def _run_model(model, run_dir, threads=THREADS, clean=True, tag=""):
    run_dir = Path(run_dir)
    if clean:
        for pat in ("*.xml", "statepoint.*.h5", "summary.h5"):
            for f in run_dir.glob(pat):
                f.unlink(missing_ok=True)
    model.export_to_xml(str(run_dir))
    t0 = time.time()
    openmc.run(cwd=str(run_dir), threads=threads, output=False)
    dt = time.time() - t0
    runtime_log.append((tag or run_dir.name, dt))
    return dt


def _keff(run_dir):
    run_dir = Path(run_dir)
    sps = sorted(run_dir.glob("statepoint.*.h5"))
    if not sps:
        raise FileNotFoundError(f"No statepoint in {run_dir}")
    with openmc.StatePoint(str(sps[-1])) as sp:
        return float(sp.keff.nominal_value), float(sp.keff.std_dev)


def _rho(k):  return (k - 1.0) / k                        # reactivity
def _pcm(k1, k2):  return 1e5 * (_rho(k2) - _rho(k1))     # Δρ in pcm

print("Helpers ready.")

# ============================================================================
# SAFETY NEUTRONICS  (FER §8.5-8.6)  - N10 EBIS / N11 SFP rack / N12 MSLB cooldown
# ============================================================================
import json as _json
import numpy as _np
import matplotlib.pyplot as _plt

# --- redirect all run dirs + plots into this project's results/ folder ---
ROOT = Path(os.environ.get("SAFETY_OUT", os.path.join(os.path.dirname(__file__), "results"))).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
PLOTS = ROOT / "plots"; PLOTS.mkdir(exist_ok=True)

STAT_SAFETY = {"fast": STAT_FAST, "medium": STAT_MEDIUM, "final": STAT_FINAL}[
    os.environ.get("SAFETY_STAT", "medium")]
print(f"[safety] outputs -> {ROOT} | STAT={STAT_SAFETY}")

# water density vs T at 12.8 MPa (IAPWS-IF97), (T_K, rho g/cc); 556 K anchors the design
_RHO_T = [(294, 1.003), (323, 0.994), (373, 0.963), (423, 0.922),
          (473, 0.870), (523, 0.803), (556, 0.748)]
def _rho_at(T):
    return float(_np.interp(T, [t for t, _ in _RHO_T], [r for _, r in _RHO_T]))

# --- borate-able moderator: build_core looks up mat_water at call-time, so a
#     module-level redefinition + a BORON_PPM global injects soluble boron ---
BORON_PPM = 0.0
def mat_water(temp=T_MOD_K, density=RHO_WATER_NOM, name="H2O"):
    m = openmc.Material(name=name, temperature=temp)
    m.set_density("g/cm3", density)
    if BORON_PPM > 0:
        wB = BORON_PPM * 1e-6; wW = 1.0 - wB
        m.add_element("H", 0.111894 * wW, percent_type="wo")
        m.add_element("O", 0.888106 * wW, percent_type="wo")
        m.add_element("B", wB, percent_type="wo")     # natural B -> B10/B11
    else:
        m.add_element("H", 2.0); m.add_element("O", 1.0)
    m.add_s_alpha_beta("c_H_in_H2O")
    return m

# --- enriched-B10 control-rod absorber (SOLID B4C - NOT soluble; SBF preserved) ---
B10_ENRICH = 0.0   # 0 = natural boron (19.9% B-10); else B-10 atom fraction (e.g. 0.90)
def mat_b4c(temp=600.0):
    m = openmc.Material(name="B4C", temperature=temp)
    m.set_density("g/cm3", RHO_B4C)
    if B10_ENRICH > 0:
        m.add_nuclide("B10", 4.0 * B10_ENRICH)
        m.add_nuclide("B11", 4.0 * (1.0 - B10_ENRICH))
        m.add_element("C", 1.0)
    else:
        m.add_element("B", 4.0); m.add_element("C", 1.0)
    return m

def _interp_cross(xs, ys, target):
    """x where y crosses target (ys monotone over the bracket)."""
    for a in range(len(xs) - 1):
        y0, y1 = ys[a], ys[a + 1]
        if (y0 - target) * (y1 - target) <= 0 and y0 != y1:
            return float(xs[a] + (xs[a + 1] - xs[a]) * (target - y0) / (y1 - y0))
    return None


# --- RESUME: skip the transport if a statepoint already exists on disk ---
_orig_run_model = _run_model
def _run_model(model, run_dir, threads=THREADS, clean=True, tag=""):
    import glob as _g
    if _g.glob(os.path.join(str(run_dir), "statepoint.*.h5")):
        print("   [resume] %s: cached statepoint" % os.path.basename(str(run_dir)))
        return 0.0
    return _orig_run_model(model, run_dir, threads=threads, clean=clean, tag=tag)


# ----------------------------- N10 : EBIS boron -----------------------------
def run_N10_ebis(stat):
    global BORON_PPM
    print("\n[N10] EBIS soluble-boron sizing - cold 294 K / BOC / ARO / standalone (no rods)")
    T = 294.0; rho = _rho_at(T); rows = []
    for ppm in [0, 1000, 1800, 2400, 3000, 3600]:
        BORON_PPM = float(ppm)
        model, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=T,
                                 control_rod_state="aro", stats=stat)
        d = _run_dir(f"N10_ebis_{ppm}ppm"); _run_model(model, d, tag=f"ebis{ppm}")
        k, s = _keff(d); rows.append(dict(boron_ppm=ppm, keff=k, sigma_pcm=s * 1e5))
        print(f"   {ppm:5d} ppm -> k = {k:.5f} +/- {s*1e5:.0f} pcm")
    BORON_PPM = 0.0
    ppms = [r["boron_ppm"] for r in rows]; ks = [r["keff"] for r in rows]
    ppm100 = _interp_cross(ppms, ks, 1.00); ppm99 = _interp_cross(ppms, ks, 0.99)
    _plt.figure(figsize=(6, 4)); _plt.plot(ppms, ks, "o-", color="#1a6faf")
    _plt.axhline(1.0, color="k", ls="--", lw=1, label="critical")
    _plt.axhline(0.99, color="r", ls=":", lw=1, label="1% margin")
    _plt.xlabel("Soluble boron (ppm)"); _plt.ylabel("k_eff (cold, ARO)")
    _plt.title("N10 EBIS boron sizing"); _plt.legend(); _plt.grid(alpha=.3)
    _plt.savefig(PLOTS / "N10_ebis_boron.png", dpi=160, bbox_inches="tight"); _plt.close()
    print(f"   -> k=1.00 at ~{ppm100:.0f} ppm ; k=0.99 (1% SDM) at ~{ppm99:.0f} ppm")
    return dict(case="N10_EBIS",
                state="cold 294 K / BOC fresh / ARO (rods out) / soluble-boron only",
                sweep=rows, boron_for_keff_1p00_ppm=ppm100, boron_for_keff_0p99_ppm=ppm99,
                criterion="independent_shutdown_systems (EBIS alone cold-subcritical, k<=0.99)",
                refs=["IAEA SSR-2/1 Req.46 (two diverse shutdown systems)",
                      "10 CFR 50.68 / NUREG-0800 4.3"])


# --------------------------- N11 : SFP rack k_inf ---------------------------
def run_N11_sfp(stat):
    global BORON_PPM
    print("\n[N11] SFP storage-rack criticality - bounding fresh 4.95% FA (no BA credit),"
          " infinite array; per 10 CFR 50.68(b): unborated k<1.0 + borated k<=0.95")
    T = 294.0; rho = _rho_at(T)
    enr = ENRICH_INNER                                   # 4.95 = most reactive
    clad = mat_zircaloy(temp=T); gap = mat_helium(temp=T); b4c = mat_b4c(temp=600.0)
    # poison rack: flux-trap-style Boral (B4C-in-Al) sheet, tight pitch
    al = openmc.Material(name="Al6061", temperature=T); al.set_density("g/cm3", 2.70)
    al.add_element("Al", 1.0)
    boral = openmc.Material.mix_materials([mat_b4c(temp=T), al], [0.50, 0.50],
                                          percent_type="wo", name="Boral_B4C_Al")   # 50 wt% B4C
    boral.temperature = T
    ss = openmc.Material(name="SS304_rack", temperature=T); ss.set_density("g/cm3", 7.94)
    for el, f in (("Fe", .70), ("Cr", .19), ("Ni", .095), ("Mn", .015)):
        ss.add_element(el, f, percent_type="wo")
    RACK_PITCH = FA_PITCH + 1.4; WALL_T = 0.45        # tighter pitch, thicker poison

    def _build_model(rmat, ppm):
        global BORON_PPM; BORON_PPM = float(ppm)
        water = mat_water(temp=T, density=rho, name=f"SFP_water_{int(ppm)}ppm")
        plain = {f"UO2_{enr:.1f}": mat_uo2(enr, temp=T, name=f"UO2_{enr:.1f}")}
        gd_mat = _mixed_fuel(ENRICH_MID, gd_wt=GD_WT_PCT, er_wt=0.0, temp=T, name="SFP_Gd")
        gd_cut = mat_uo2(ENRICH_MID, temp=T, name="SFP_Gdcut")
        er_mat = _mixed_fuel(ENRICH_MID, gd_wt=0.0, er_wt=ER_WT_PCT, temp=T, name="SFP_Er")
        fa = _build_fa_universe(T, T, water, clad, gap, b4c, plain, gd_mat, gd_cut, er_mat,
                                insert_cr=False, name=f"SFP_FA_{int(ppm)}",
                                gd_positions=set(), er_positions=set(), fa_enrich=enr)
        hf = FA_PITCH/2.0; hw = RACK_PITCH/2.0; hi = hw - WALL_T; H = ACTIVE_HEIGHT/2.0
        bc = "reflective"
        xlo = openmc.XPlane(-hw, boundary_type=bc); xhi = openmc.XPlane(hw, boundary_type=bc)
        ylo = openmc.YPlane(-hw, boundary_type=bc); yhi = openmc.YPlane(hw, boundary_type=bc)
        zlo = openmc.ZPlane(-H, boundary_type=bc);  zhi = openmc.ZPlane(H, boundary_type=bc)
        fx0 = openmc.XPlane(-hf); fx1 = openmc.XPlane(hf)
        fy0 = openmc.YPlane(-hf); fy1 = openmc.YPlane(hf)
        ix0 = openmc.XPlane(-hi); ix1 = openmc.XPlane(hi)
        iy0 = openmc.YPlane(-hi); iy1 = openmc.YPlane(hi)
        zr = +zlo & -zhi; fa_box = +fx0 & -fx1 & +fy0 & -fy1; in_box = +ix0 & -ix1 & +iy0 & -iy1
        cell_fa = openmc.Cell(name="sfp_fa", fill=fa, region=fa_box & zr)
        cell_w  = openmc.Cell(name="sfp_water", fill=water, region=(in_box & zr) & ~fa_box)
        cell_wall = openmc.Cell(name="sfp_wall", fill=rmat,
                                region=(+xlo & -xhi & +ylo & -yhi & zr) & ~in_box)
        geom = openmc.Geometry(openmc.Universe(cells=[cell_fa, cell_w, cell_wall]))
        s = openmc.Settings(); s.batches = stat["batches"]; s.inactive = stat["inactive"]
        s.particles = stat["particles"]; s.temperature = {"method": "nearest", "tolerance": 400.0}
        s.source = openmc.IndependentSource(space=openmc.stats.Box([-hf]*3, [hf]*3),
                                            constraints={"fissionable": True})
        allm = [water, clad, gap, b4c, gd_mat, gd_cut, er_mat, rmat] + list(plain.values())
        return openmc.Model(geometry=geom, settings=s,
                            materials=openmc.Materials([m for m in allm if m]))

    cases = [("SS304_unborated", ss, 0),
             ("Boral_unborated", boral, 0),
             ("Boral_2000ppm_SFP_boron", boral, 2000)]
    rows = []
    for label, rmat, ppm in cases:
        model = _build_model(rmat, ppm)
        d = _run_dir(f"N11_sfp_{label}"); _run_model(model, d, tag=f"sfp_{label}")
        k, sg = _keff(d); rows.append(dict(rack=label, boron_ppm=ppm, k_inf=k, sigma_pcm=sg * 1e5))
        print(f"   {label:26s}: k_inf = {k:.5f} +/- {sg*1e5:.0f} pcm")
    BORON_PPM = 0.0
    return dict(case="N11_SFP_rack",
                fuel="bounding fresh 4.95% UO2 assembly, NO burnable-absorber credit",
                array="infinite (fully reflective) -> k_inf (bounds any finite rack)",
                rack="flux-trap Boral (50 wt% B4C-in-Al, 0.45 cm), pitch FA+1.4 cm",
                rack_pitch_cm=RACK_PITCH, wall_thickness_cm=WALL_T, results=rows,
                criterion="10 CFR 50.68(b): unborated k<1.0 (defence-in-depth) AND borated k<=0.95",
                note=("fresh 4.95% infinite array is the extreme bound; licensed storage of >4 wt%"
                      " fuel credits BURNUP + SFP soluble boron - the borated case is the design demo"),
                refs=["10 CFR 50.68(b)", "NUREG-0800 SRP 9.1.1", "ANSI/ANS-8.1", "IAEA SSG-15"])


# ------------------------- N12 : MSLB cooldown ------------------------------
def run_N12_mslb(stat):
    print("\n[N12] MSLB cooldown reactivity - most-reactive rod stuck OUT, hot -> cold")
    cra = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
           if CR_MAP[N_CORE - 1 - j, i] == 1]
    cc = (N_CORE - 1) // 2
    stuck = min(cra, key=lambda p: abs(p[0] - cc) + abs(p[1] - cc))   # most central ~ highest worth
    inserted = [p for p in cra if p != stuck]
    print(f"   {len(inserted)} of {len(cra)} CRAs inserted; rod {stuck} stuck OUT")
    rows = []
    for T in [556, 523, 473, 423, 373, 323, 294]:
        rho = _rho_at(T)
        model, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                                 control_rod_state=inserted, stats=stat)
        d = _run_dir(f"N12_mslb_T{T}"); _run_model(model, d, tag=f"mslb{T}")
        k, s = _keff(d); rows.append(dict(T_K=T, rho=rho, keff=k, sigma_pcm=s * 1e5))
        print(f"   T={T} K  rho={rho:.3f} -> k = {k:.5f} +/- {s*1e5:.0f} pcm")
    kmax = max(r["keff"] for r in rows)
    Ts = [r["T_K"] for r in rows]; ks = [r["keff"] for r in rows]
    _plt.figure(figsize=(6, 4)); _plt.plot(Ts, ks, "o-", color="#c0392b")
    _plt.axhline(1.0, color="k", ls="--", lw=1, label="critical")
    _plt.xlabel("Moderator temperature (K)"); _plt.ylabel("k_eff (rod stuck out)")
    _plt.title("N12 MSLB cooldown"); _plt.gca().invert_xaxis()
    _plt.legend(); _plt.grid(alpha=.3)
    _plt.savefig(PLOTS / "N12_mslb_cooldown.png", dpi=160, bbox_inches="tight"); _plt.close()
    print(f"   -> k_max on cooldown = {kmax:.5f}  "
          f"({'RETURN TO POWER' if kmax >= 1 else 'stays subcritical'})")
    return dict(case="N12_MSLB_cooldown",
                config=f"{len(inserted)}/{len(cra)} CRAs inserted; most-reactive rod {stuck} stuck OUT",
                sweep=rows, keff_max_on_cooldown=kmax, return_to_power=bool(kmax >= 1.0),
                criterion="MSLB no return-to-power: k<1 with most-reactive rod stuck out",
                refs=["NUREG-0800 SRP 15.1.5 (steam-line break)",
                      "IAEA SSG-2 (deterministic safety analysis)", "ANS-51.1 cooldown event"])


# --------------------- N5 : rod worth + shutdown margin ---------------------
def run_N5_sdm(stat):
    print("\n[N5] Control-rod worth + shutdown margin (SIGNED; hot trip & cold SDM)")
    all_cr = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
              if CR_MAP[N_CORE - 1 - j, i] == 1]
    cc = N_CORE // 2
    central = min(all_cr, key=lambda p: (p[0] - cc) ** 2 + (p[1] - cc) ** 2)
    stuck = [p for p in all_cr if p != central]   # all rods in except most-reactive
    def _kof(state, T, tag):
        rho = _rho_at(T)
        m, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=state, stats=stat)
        d = _run_dir(f"N5_{tag}"); _run_model(m, d, tag=tag)
        return _keff(d)[0]
    Th, Tc = T_MOD_K, 294.0
    k_aro_h   = _kof("aro",  Th, "aro_hot")
    k_ari_h   = _kof("ari",  Th, "ari_hot")
    k_ari_c   = _kof("ari",  Tc, "ari_cold")
    k_stuck_c = _kof(stuck,  Tc, "stuck_cold")
    bank = abs(_pcm(k_aro_h, k_ari_h))             # total bank worth, pcm
    def _sdm(k): return -(k - 1.0) / k * 100.0     # SIGNED: +ve = subcritical margin
    out = dict(case="N5_rod_worth_SDM",
               k_aro_hot=k_aro_h, k_ari_hot=k_ari_h, total_bank_worth_pcm=bank,
               k_ari_cold=k_ari_c, k_stuck_cold=k_stuck_c,
               sdm_all_rods_cold_pct=_sdm(k_ari_c),
               sdm_stuck_rod_cold_pct=_sdm(k_stuck_c),
               hot_trip_all_rods_subcritical=bool(k_ari_h < 1.0),
               rods_alone_cold_subcritical=bool(k_ari_c < 1.0),
               note=("boron-free high-excess core: control rods give the fast hot trip; "
                     "EBIS soluble boron (N10) provides/holds cold subcriticality - the "
                     "diverse 2nd shutdown system (SSR-2/1 Req.46). SDM reported SIGNED "
                     "(notebook calc uses abs() which masks a supercritical stuck-rod state)."),
               criterion="hot trip subcritical by rods; cold shutdown by rods+EBIS; SDM>=1%",
               refs=["IAEA SSR-2/1 Req.46 (two diverse shutdown systems)",
                     "NUREG-0800 SRP 4.3", "RG 1.77"])
    print(f"   bank worth (hot ARO->ARI) = {bank:.0f} pcm")
    print(f"   k_ARI hot   = {k_ari_h:.5f}   ({'subcritical' if k_ari_h<1 else 'SUPERCRIT'})")
    print(f"   k_ARI cold  = {k_ari_c:.5f}   ({'subcritical' if k_ari_c<1 else 'SUPERCRIT -> EBIS'})")
    print(f"   k_stuck cold= {k_stuck_c:.5f}  SDM(stuck,cold) = {_sdm(k_stuck_c):+.2f}% dk/k")
    return out


# ---------------- N12-B : MSLB cooldown + EBIS credited ---------------------
def run_N12b_mslb_ebis(stat, ebis_ppm=3000):
    global BORON_PPM
    print("\n[N12B] MSLB cooldown + EBIS (%d ppm) credited - stuck rod, hot->cold" % ebis_ppm)
    cra = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
           if CR_MAP[N_CORE - 1 - j, i] == 1]
    cc = (N_CORE - 1) // 2
    stuck = min(cra, key=lambda p: abs(p[0] - cc) + abs(p[1] - cc))
    inserted = [p for p in cra if p != stuck]
    rows = []
    for T in [556, 423, 294]:                      # hot, mid, cold (limiting) endpoint
        rho = _rho_at(T); BORON_PPM = float(ebis_ppm)
        m, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=inserted, stats=stat)
        d = _run_dir("N12B_mslb_ebis_T%d" % T); _run_model(m, d, tag="mslbE%d" % T)
        k, s = _keff(d); kadj = k + 2 * s + 0.005       # +2sigma + 500 pcm allowance
        rows.append(dict(T_K=T, boron_ppm=ebis_ppm, keff=k, sigma_pcm=s * 1e5, k_adj=round(kadj, 5)))
        print("   T=%dK +%dppm -> k=%.5f  k_adj=%.4f" % (T, ebis_ppm, k, kadj))
    BORON_PPM = 0.0
    kadj_cold = [r["k_adj"] for r in rows if r["T_K"] == 294][0]
    print("   -> cold (294 K) k_adj = %.4f  (%s 0.95)" % (kadj_cold, "<=" if kadj_cold <= 0.95 else ">"))
    return dict(case="N12B_MSLB_EBIS_credited",
                config="%d/%d CRAs in, rod %s stuck OUT, EBIS %d ppm" % (len(inserted), len(cra), stuck, ebis_ppm),
                ebis_ppm=ebis_ppm, sweep=rows, k_adj_cold=kadj_cold,
                subcritical_with_margin=bool(kadj_cold <= 0.95),
                criterion="credited MSLB termination (RT+MSI+EBIS): cold/stuck-rod k_adj <= 0.95",
                note=("credited safe state = reactor trip + main-steam isolation + EBIS; the rods-alone "
                      "N12 is the diagnostic limiting case that establishes the EBIS requirement"),
                refs=["NUREG-0800 SRP 15.1.5", "IAEA SSR-2/1 Req.46", "RG 1.77"])


# --------- N5-B : rod worth + SDM with ENRICHED B-10 solid rods -------------
def run_N5b_enriched_rods(stat, b10=0.90):
    global B10_ENRICH
    print("\n[N5B] Rod worth + SDM with ENRICHED B-10 (%.0f%%) SOLID B4C rods (SBF intact)" % (b10 * 100))
    all_cr = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
              if CR_MAP[N_CORE - 1 - j, i] == 1]
    cc = N_CORE // 2
    central = min(all_cr, key=lambda p: (p[0] - cc) ** 2 + (p[1] - cc) ** 2)
    stuck = [p for p in all_cr if p != central]
    def _kof(state, T, tag):
        rho = _rho_at(T)
        m, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=state, stats=stat)
        d = _run_dir(tag); _run_model(m, d, tag=tag); return _keff(d)
    B10_ENRICH = 0.0
    k_aro_h, _ = _kof("aro", T_MOD_K, "N5b_aro_hot")      # rods out -> enrichment irrelevant
    B10_ENRICH = float(b10)
    k_ari_h, s_ari_h = _kof("ari", T_MOD_K, "N5b_ari_hot")
    k_ari_c, _ = _kof("ari", 294.0, "N5b_ari_cold")
    k_stuck_c, s_st = _kof(stuck, 294.0, "N5b_stuck_cold")
    B10_ENRICH = 0.0
    bank = abs(_pcm(k_aro_h, k_ari_h))
    def _sdm(k): return -(k - 1.0) / k * 100.0
    kadj_ari_h = k_ari_h + 2 * s_ari_h + 0.005
    print("   bank worth (enriched) = %.0f pcm  (was 13287 natural)" % bank)
    print("   k_ARI hot = %.5f  k_adj = %.4f  (%s)" %
          (k_ari_h, kadj_ari_h, "subcritical TRIP OK" if kadj_ari_h <= 0.99 else "still supercrit"))
    print("   k_ARI cold = %.5f | k_stuck cold = %.5f  SDM(stuck) = %+.2f%%" %
          (k_ari_c, k_stuck_c, _sdm(k_stuck_c)))
    return dict(case="N5B_enriched_B10_rods", b10_enrichment=b10,
                k_aro_hot=k_aro_h, k_ari_hot=k_ari_h, total_bank_worth_pcm=bank,
                k_adj_ari_hot=round(kadj_ari_h, 5),
                k_ari_cold=k_ari_c, k_stuck_cold=k_stuck_c,
                sdm_all_rods_cold_pct=_sdm(k_ari_c), sdm_stuck_rod_cold_pct=_sdm(k_stuck_c),
                hot_trip_subcritical=bool(kadj_ari_h <= 0.99),
                note=("enriched-B10 SOLID B4C control rods - does NOT add soluble boron, SBF claim intact; "
                      "EBIS remains the diverse cold/standalone shutdown backup"),
                criterion="rod-based hot trip k_adj<=0.99 with SDM; cold shutdown by rods + EBIS",
                refs=["IAEA SSR-2/1 Req.46", "NUREG-0800 SRP 4.3"])


# ------- N5-C : enriched rods + extra CRA locations (margin booster) --------
def run_N5c_extra_cra(stat, b10=0.90):
    global B10_ENRICH
    base = [(i, j) for j in range(N_CORE) for i in range(N_CORE)
            if CR_MAP[N_CORE - 1 - j, i] == 1]
    extra = [(3, 5), (1, 3), (5, 3), (3, 1)]      # 4 central-cross fuel FAs (NOT instrument (3,3))
    ext = base + [p for p in extra if p not in base]
    cc = N_CORE // 2
    print("\n[N5C] enriched B-10 rods + %d extra CRAs (%d total) - hot-trip margin booster"
          % (len(extra), len(ext)))
    def _kof(state, T, tag):
        rho = _rho_at(T)
        m, _, _ = build_core(mod_temp=T, water_density=rho, fuel_temp=float(T),
                             control_rod_state=state, stats=stat)
        d = _run_dir(tag); _run_model(m, d, tag=tag); return _keff(d)
    B10_ENRICH = 0.0
    k_aro, _ = _kof("aro", T_MOD_K, "N5c_aro_hot")
    B10_ENRICH = float(b10)
    k_ari, s_ari = _kof(ext, T_MOD_K, "N5c_ari_hot")
    central = min(ext, key=lambda q: (q[0] - cc) ** 2 + (q[1] - cc) ** 2)
    stuck = [p for p in ext if p != central]
    k_stuck_c, _ = _kof(stuck, 294.0, "N5c_stuck_cold")
    B10_ENRICH = 0.0
    bank = abs(_pcm(k_aro, k_ari)); kadj = k_ari + 2 * s_ari + 0.005
    print("   %d CRAs enriched: bank = %.0f pcm | k_ARI hot = %.5f  k_adj = %.4f" %
          (len(ext), bank, k_ari, kadj))
    return dict(case="N5C_enriched_plus_extraCRA", n_cra=len(ext), n_extra=len(extra),
                b10_enrichment=b10, extra_cra=extra, k_aro_hot=k_aro, k_ari_hot=k_ari,
                total_bank_worth_pcm=bank, k_adj_ari_hot=round(kadj, 5), k_stuck_cold=k_stuck_c,
                hot_sdm_pct=round(-(k_ari - 1) / k_ari * 100, 2),
                note=("4 extra CRAs in central-cross fuel FAs (existing guide tubes; +4 CRDMs vs 12); "
                      "enriched-B10 SOLID rods, SBF intact; EBIS still the diverse cold backup"),
                criterion="hot trip k_adj<=0.98 (jury 'Good'); cold by rods + EBIS",
                refs=["IAEA SSR-2/1 Req.46", "NUREG-0800 SRP 4.3"])


# --------------------------------- driver -----------------------------------
_which = os.environ.get("SAFETY_RUN", "all")
_resfile = ROOT / "safety_neutronics_results.json"
_results = _json.load(open(_resfile)) if _resfile.exists() else {}   # merge / resume
def _save():
    open(_resfile, "w").write(_json.dumps(_results, default=str, indent=2))
_plan = [("N5", "N5_SDM", run_N5_sdm), ("N10", "N10_EBIS", run_N10_ebis),
         ("N11", "N11_SFP", run_N11_sfp), ("N12", "N12_MSLB", run_N12_mslb),
         ("N12B", "N12B_MSLB_EBIS", run_N12b_mslb_ebis),
         ("N5B", "N5B_enriched_rods", run_N5b_enriched_rods),
         ("N5C", "N5C_extra_cra", run_N5c_extra_cra)]
for _sel, _key, _fn in _plan:
    if _key in _results:
        print("[safety] %s already complete - skipping" % _key); continue
    if _which in ("all", _sel):
        _results[_key] = _fn(STAT_SAFETY); _save()       # checkpoint after each sim
_save()
_need = [k for _, k, _ in _plan]
if all(k in _results for k in _need):
    print("\nSAFETY_ALL_COMPLETE ->", _resfile)
else:
    print("\n[safety] partial:", [k for k in _need if k in _results], "->", _resfile)
