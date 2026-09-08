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

# Control-rod-cluster assemblies — 16 CRAs = 12 checkerboard + 4 central-cross
# (N5C final design; extras at (1,3),(3,1),(3,5),(5,3); central FA (3,3) = instrument)
CR_MAP = np.array([
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
])
N_CR_CLUSTERS = int(CR_MAP.sum())         # 16

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
HM_MASS_T      = 9.39       # 37 FA
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


B10_ENRICH = 0.90   # 90% B-10 enriched B4C control rods (final locked design; solid, SBF intact)

def mat_b4c(temp=600.0):
    m = openmc.Material(name="B4C", temperature=temp)
    m.set_density("g/cm3", RHO_B4C)
    if B10_ENRICH > 0:
        m.add_nuclide("B10", 4.0 * B10_ENRICH)
        m.add_nuclide("B11", 4.0 * (1.0 - B10_ENRICH))
    else:
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

# control rods inserted, by centrality (n of the CRAs; enriched-B10 in the locked design)
_cra = [(i,j) for j in range(N_CORE) for i in range(N_CORE) if CR_MAP[N_CORE-1-j,i]==1]
_cc = (N_CORE-1)//2
_cra_sorted = sorted(_cra, key=lambda p:(p[0]-_cc)**2 + (p[1]-_cc)**2)
def _rods(n): return set(_cra_sorted[:int(n)])
_NR = N_CR_CLUSTERS                                 # full bank size (rods 0.._NR)

# Design = wide LHS over the operating envelope (trains k/power-map) + a DENSE cluster near
# the HFP operating point (556 K / 900 K / rods 0 / void 0) so the LOCAL reactivity
# coefficients (MTC/DTC/void, rod worth) are resolved accurately -- the fix for the coarse
# coefficient derivatives seen in the first (wide-only) sweep.
N_LOCAL = int(os.environ.get("TWIN_NLOCAL", "48"))
_lo = _np.array([294., 600., 0., 0.00]); _hi = _np.array([560., 1200., float(_NR), 0.20])
try:
    from scipy.stats.qmc import LatinHypercube
    _uw = LatinHypercube(d=4, seed=SEED).random(N_PTS)
    _ul = LatinHypercube(d=4, seed=SEED+1).random(N_LOCAL)
except Exception:
    _rng = _np.random.default_rng(SEED)
    _uw = _rng.random((N_PTS, 4)); _ul = _rng.random((N_LOCAL, 4))
_Xw = _lo + _uw * (_hi - _lo)                       # wide envelope
_op = _np.array([556., 900., 0., 0.0])              # HFP operating point
_half = _np.array([14., 70., 3., 0.03])             # tight local box for dk/dinput
_Xl = _np.clip(_op + (2*_ul - 1) * _half, _lo, _hi) # dense near-operating cluster
X = _np.vstack([_Xw, _Xl])
X[:, 2] = _np.clip(_np.round(X[:, 2]), 0, _NR)      # n_rods -> integer 0.._NR
N_PTS = len(X)

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
