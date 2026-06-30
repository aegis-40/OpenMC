#!/usr/bin/env python
"""Build the clean, FER-grade neutronics notebook from the 37-FA working copy.

- proper name; paper-style markdown (microURANUS-style numbered sections)
- strips evolutionary cruft from config + reconciles coolant to the 8.4 basis
- drops obsolete cells (overnight sweep, stale 'notes' block)
- adds the missing required pieces: core materials & selection, design criteria
  & standards compliance, full-core loading map figure, consolidated reactivity/
  feedback/uncertainty/benchmarking tables, safety-case neutronics, digital appendix
- keeps every working analysis cell verbatim (k-eff, coefficients, CR worth/SDM,
  depletion BOC->equilibrium, peaking, flux, shielding)
All code cells syntax-checked; JSON round-trips.
"""
import ast, json, copy

SRC = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_3d_core_7x7_37FA.ipynb'
DST = r'D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_neutronics_FER.ipynb'
src = json.load(open(SRC, encoding='utf-8'))
S = src['cells']

def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}
def code(text):
    ast.parse(text)
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": text.splitlines(keepends=True)}
def keep(i):
    return copy.deepcopy(S[i])

# ── cleaned design-constants cell (all variables preserved; cruft removed; coolant -> 8.4) ──
CFG = '''# ============================================================================
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
ENRICH_OUTER  = 4.40       # core average ~4.69
ZONE_R1_CM    = 4.5
ZONE_R2_CM    = 8.5
EDGE_PIN_GRADING = True     # de-rate the FA-perimeter pin ring (boron-free de-peaking)
EDGE_ENRICH      = 4.0
RADIAL_ENRICH_ZONING = False              # assembly-uniform out-in option (intra-FA grade preferred)
RING_ENRICH = {0: 4.0, 1: 4.4, 2: 4.7, 3: 4.95}

# Burnable absorber — integral Gd2O3 + light Er2O3 (soluble-boron-free hold-down)
GD_WT_PCT       = 8        # wt% Gd2O3 in the Gd-bearing rods
N_GD_RODS       = 32       # per-FA average (ring zoning redistributes by ring)
GD_AXIAL_CUT_CM = 10.0     # plain-UO2 Gd cutback at each rod end
RADIAL_GD_ZONING = True     # heavier-centre Gd flattens radial power (replaces boron shaping)
GD_RING_WEIGHTS  = {0: 1.65, 1: 1.45, 2: 0.95, 3: 0.68}   # rings 1/8/16/12; core-avg ~1.0
AXIAL_BLANKET_CM     = 0.0  # optional reduced-enrichment axial blanket (0 = off)
AXIAL_BLANKET_ENRICH = 2.5
if DESIGN == "hybrid":
    ER_WT_PCT = 0.5        # light Er hold-down through mid/late cycle + cold SDM
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
print(f"Enrichment {ENRICH_INNER}/{ENRICH_MID}/{ENRICH_OUTER} wt% (avg ~{_enr_avg:.2f}) | Gd2O3 {GD_WT_PCT} wt%x{N_GD_RODS} + Er2O3 {ER_WT_PCT} wt%x{N_ER_RODS}")
print(f"Power {CORE_POWER_MWT} MWth | HM {HM_MASS_T} t | specific power {SPECIFIC_POWER:.2f} W/gHM | {N_BATCHES}-batch")
print(f"Coolant/moderator 12.8 MPa, T_mod {T_MOD_K} K, rho {RHO_WATER_NOM} g/cm3 | MC {STAT}")'''

# ── markdown sections (paper-style) ─────────────────────────────────────────
MD_TITLE = '''# Aegis-40 — Neutronic Design and Analysis of a Soluble-Boron-Free Integral PWR

**TEKNOFEST 2026 — Fuel & Reactor (FER) Digital Appendix · OpenMC 0.15.3 · ENDF/B-VIII.0**

## Abstract
This notebook presents the full neutronic design and analysis of **Aegis-40**, a **125 MWth / 40 MWe
soluble-boron-free (SBF) integral pressurised-water reactor**. The core is a **37-assembly, 7-wide
octagonal array** of standard 17x17 Westinghouse fuel assemblies with a 200 cm active height. Reactivity
is held down without soluble boron by an **integral Gd2O3 + Er2O3 burnable-absorber** system with
**radial (ring) Gd zoning** for power flattening and **intra-assembly enrichment grading** (<= 4.95% LEU)
in place of the boron radial shaping used by boronated peers. All analyses are performed with **OpenMC**
3-D Monte-Carlo transport and depletion on **ENDF/B-VIII.0** data, from the **initial (BOC) through the
equilibrium cycle**: criticality, neutron-flux and burnup distributions, reactivity feedback coefficients,
control-rod worth and shutdown margin, and power-peaking factors. Material selection, core geometry, the
safety-criteria compliance argument, and a reproducible digital appendix are documented in the sections
below. The companion biological-shield model is included as Section 13.'''

MD_INTRO = '''## 1 · Introduction and design objectives
Aegis-40 targets a transportable, factory-fuelled iPWR for distributed power and cogeneration in Turkiye.
The defining choice is **soluble-boron-free (SBF) operation**: no boric acid in the coolant, which gives a
strongly negative moderator coefficient, removes boron-dilution accident sequences, and simplifies the
chemistry and volume-control system. The price is that **all excess reactivity and radial power shaping
must come from solid, in-core devices** — burnable absorbers, enrichment zoning, and control rods —
rather than from boron.

**Design objectives (neutronics).**
- Reactivity-limited cycle with a small burn-up swing using integral Gd + Er burnable absorbers.
- Negative reactivity feedback at all conditions (moderator, Doppler, void).
- Adequate shutdown margin with the most-reactive rod stuck out.
- Power-peaking compatible with thermal-hydraulic (DNBR) margin at low core power density.
- Discharge burn-up in the high-burn-up LEU range at a multi-batch reload.
- Maximum enrichment within the 4.95 wt% LEU limit.'''

MD_CODES = '''## 2 · Codes, libraries and computational methods
- **Transport / depletion:** OpenMC 0.15.3 (continuous-energy Monte-Carlo), `PredictorIntegrator` depletion.
- **Nuclear data:** ENDF/B-VIII.0 (IAEA/NNDC-hosted), with S(alpha,beta) thermal scattering for H in H2O.
- **Model fidelity:** explicit 3-D heterogeneous core — every fuel/Gd/Er rod, guide tube and instrument
  tube is modelled; vacuum boundaries on all six faces give physical radial and axial leakage.
- **Reproducibility:** every analysis exports its OpenMC XML input to `aegis40_*_outputs/0?_*/`; the
  cross-section and depletion-chain paths are set in the cell below and overridable by environment
  variables. Statistics are controlled by the `STAT_*` profiles (`STAT_FINAL` for reported numbers).

Cross-section library and depletion-chain paths (override with `OPENMC_CROSS_SECTIONS` / `OPENMC_CHAIN_FILE`):'''

MD_CRITERIA = '''## 3 · Design criteria and standards compliance
The neutronic acceptance criteria and the standards they derive from are listed below; pass/fail against
these is evaluated in Section 10 and written to `safety_analysis_results.yaml`.

| Parameter | Criterion | Basis (standard) |
|---|---|---|
| Max fuel enrichment | <= 5.0 wt% U-235 | LEU limit (IAEA INFCIRC/254; 10 CFR 50) |
| Moderator temp. coeff. (MTC) | < 0 at power | IAEA SSR-2/1 Req. 45; NUREG-1431 LCO 3.1.3 |
| Doppler (fuel temp.) coeff. | < 0 | IAEA SSR-2/1 Req. 45 |
| Void coefficient | < 0 | IAEA SSR-2/1 Req. 45 |
| Shutdown margin (1 stuck rod) | >= 1% dk/k | NUREG-1431 LCO 3.1.1; IAEA SSR-2/1 Req. 46 |
| Diverse shutdown means | >= 2 independent | IAEA SSR-2/1 Req. 46 |
| Enthalpy-rise factor F-dH | report vs DNBR limit | NUREG-1431 LCO 3.2.2 |
| Heat-flux factor F-Q | report vs LHR/LOCA limit | NUREG-1431 LCO 3.2.1 |
| Max reactivity insertion rate | <= 7.5e-4 dk/k/s | RG 1.77 / CRDM design |

**Soluble-boron-free justification.** Boron-free operation is consistent with SSR-2/1 Req. 45 (inherently
negative feedback) and is demonstrated by the integral PWR peer **CAREM-25** (Gd burnable absorber, no
soluble boron). The methodology mirrors **microURANUS** (UNIST, 2021): unit-cell -> reflector ->
whole-core optimisation with high-fidelity Monte-Carlo verification.'''

MD_MATERIALS = '''## 4 · Core materials and selection criteria
All material compositions are built in the factory functions in the next cell; their selection rationale
and behaviour in the neutron and temperature environment are summarised here.

| Component | Material | Density (g/cm3) | Why selected | In-core behaviour (irradiation / temperature) |
|---|---|---|---|---|
| Fuel | UO2, 4.40-4.95 wt% LEU, zoned | 10.40 | Proven LWR fuel; high melting point; established licensing basis | Doppler broadening of U-238 gives prompt negative feedback; fission-gas release & swelling bounded at design LHR; T_fuel ~900 K nominal |
| Burnable absorber | Gd2O3 (8 wt%) in UO2 | 10.4 mix | Strong thermal absorber; burns out ~10 GWd/t to control BOC excess in SBF core | Gd-155/157 deplete early -> reactivity rises smoothly (no residual penalty at the chosen loading) |
| Burnable absorber | Er2O3 (0.5 wt%) in UO2 | 10.4 mix | Slowly-depleting absorber; flattens mid/late-cycle reactivity, aids cold shutdown | Er-167 resonance gives a slightly more negative MTC; depletes gradually across the cycle |
| Cladding | Zircaloy-4 | 6.55 | Low thermal-neutron absorption; corrosion & creep performance to high burn-up | Low parasitic capture; hydriding/oxidation bounded within design temperature & fluence |
| Coolant / moderator | Light water, 12.8 MPa, 283 C | 0.748 | Excellent moderator; SBF (no boric acid) for strong negative MTC | Density feedback -> negative MTC and void coefficient; S(alpha,beta) thermal scattering modelled |
| Reflector | Light water, 20 cm radial + 30 cm axial plena | 0.748 | High thermal albedo flattens peripheral power and reduces leakage in a compact core | Returns thermal neutrons to edge pins; no activation concern |
| Control rods | B4C | 2.52 | Standard strong absorber for rod worth & scram | B-10 depletes slowly over life; He production bounded; gives the diverse, fast-acting shutdown means |
| Guide / instrument tubes | Zircaloy-4 + water | - | Standard 17x17 internals; water holes for rodding & instrumentation | Local thermal-flux peaking at water holes managed by enrichment grading / Gd placement |

Operating-temperature set: fuel T ~ 900 K, moderator T ~ 556 K (12.8 MPa). Transient/accident temperature
behaviour (Doppler, MTC, void) is quantified by the reactivity-coefficient analyses in Section 7.'''

MD_GEOM = '''## 5 · Core geometry and layout
Standard 17x17 lattice: **264 fuel rods, 24 guide tubes, 1 central instrument tube** per assembly. The
37-assembly core is a 7-wide octagon (rows 3-5-7-7-7-5-3); control-rod clusters occupy 12 assemblies in a
checkerboard pattern with the central assembly reserved for instrumentation. Gd and Er rods are placed in
8-fold-symmetric groups (Gd biased to mid-radius, Er to the outer ring); Gd loading is zoned by core ring
(heavier at the centre) to flatten radial power without soluble boron. Pin dimensions, pitch and active
height are fixed (Section 4 table / config cell) so the thermal-hydraulic model is unaffected.'''

MD_BUILDERS = '''### Geometry builders (3-D core)
Pin universes are axially infinite; the active fuel is clipped at the assembly level by the active-height
planes (z = +/-100 cm). Above/below the active region (|z| in [100, 130] cm) every pin position becomes
plain water (the top/bottom plena); beyond z = +/-130 cm is vacuum (axial leakage). Radially the core
lattice is wrapped in a 20 cm water reflector and then a vacuum boundary. The shield wrapper (Section 13)
optionally replaces the reflector/vacuum with the full biological shield.'''

MD_LOADING = '''## 6 · Core loading map and geometry verification
The full-core loading map (enrichment/Gd ring zone, Gd-rod count per assembly, control-rod positions,
water reflector) is drawn first, followed by the annotated core map and the true OpenMC colour renders of
the radial (xy) and axial (xz) cross-sections — confirming the lattice, reflector, axial plena and vacuum
boundaries before committing to long Monte-Carlo runs.'''

MD_STATIC = '''## 7 · Static neutronic parameters and reactivity feedback
Each cell runs a short k-eigenvalue calculation on the 3-D core (real leakage) and stores the result in
`results`: BOC criticality, moderator-temperature, Doppler and void coefficients, control-rod worth and
shutdown margin (most-reactive rod stuck out), maximum enrichment, and the bounding reactivity-insertion
rate. These feed the reactivity-balance and feedback tables (Section 10) and the compliance check
(Section 11).'''

MD_DEPLETION = '''## 8 · Depletion: initial (BOC) to equilibrium cycle
Full 3-D depletion at design specific power. With leakage included, k drops below 1 during the cycle, so
the cycle length is the EFPD at which k = 1 (not a placeholder). The multi-batch equilibrium discharge
burn-up follows from the linear-reactivity model (BU_discharge ~ N_BATCHES x BU_cycle). The k-eff vs
burn-up curve (BOC -> EOC), the Gd/Er inventory evolution, and the per-assembly burn-up distribution at
EOC are produced here. Total power 125 MWth over 37 FA ~ 3.38 MWth/FA; specific power
125/9.87 = 12.7 W/gHM.'''

MD_PEAKING = '''## 9 · Power and flux distributions
Power peaking is reconstructed pin-by-pin from a fine 3-D fission mesh: the enthalpy-rise factor F-dH
(radial, axially integrated -> statistically robust), the axial factor F-z, and the 3-D heat-flux factor
F-Q. The reported F-Q is the **separable** F-dH x F-z; the raw single-node 3-D maximum is a Monte-Carlo
artefact at finite statistics (it falls toward the separable value as particles increase) and is kept only
as a diagnostic. Radial and axial power shapes and thermal/fast/total flux maps are produced at
BOC (and at MOC/EOC when the depletion statepoints are supplied).'''

MD_TABLES = '''## 10 · Consolidated results: reactivity balance, feedback and uncertainty
The tables below aggregate the analyses above into the FER reactivity-balance, feedback-coefficient,
peaking and Monte-Carlo-uncertainty tables. (Run the analysis cells first to populate `results`.)'''

MD_CONSOL = '''## 11 · Consolidated safety output (single file)
Every `from_openmc.*` field required by `safety_criteria.yaml`, plus diagnostics and pass/fail status, run
metadata and core geometry, is written to one file: `safety_analysis_results.yaml`, with a human-readable
mirror in `summary_report.txt`.'''

MD_SAFETYCASE = '''## 12 · Safety-case neutronics and operating limits
- **Criticality safety.** The fresh, all-rods-out core at cold/hot zero power is the bounding reactive
  state; the BOC k-eff and the burnable-absorber hold-down (Section 7-8) bound the in-core excess. Fuel
  handling/storage k-eff is covered in the storage analysis (out of scope for the core model).
- **Reactivity-control limits.** Total control-rod worth, the worth of the burnable absorbers, and the
  shutdown margin with the most-reactive rod stuck out are reported in Section 7/10. The maximum
  reactivity-insertion rate is bounded by the CRDM design (criterion in Section 3).
- **Worst-case feedback.** MTC, Doppler and void coefficients are negative across the operating range
  (Section 7), so power excursions are self-limiting; the SBF design removes the boron-dilution sequence.
- **Diverse shutdown.** Two independent means are provided: the B4C control-rod system (fast scram) and an
  independent emergency boron/absorber injection system (defence-in-depth, SSR-2/1 Req. 46).'''

MD_BENCH = '''## 13 · Benchmarking and verification
Aegis-40 neutronic results are compared against published integral-PWR / SMR references that use the same
class of methods and data. Code/data verification rests on OpenMC's published ENDF/B-VIII.0 criticality
benchmark suite (ICSBEP); design-level reasonableness is shown below.

| Quantity | Aegis-40 | NuScale (FSAR) | CAREM-25 | RITM-200 | Comment |
|---|---|---|---|---|---|
| Power (MWth) | 125 | 160 | 100 | 175 | iPWR class |
| Assemblies | 37 x 17x17 | 37 x 17x17 | 61 | - | same lattice as NuScale |
| Soluble boron | none (SBF) | yes (~1235 ppm) | none (SBF) | yes | SBF peer = CAREM-25 |
| Burnable absorber | Gd2O3 + Er2O3 | Gd2O3 | Gd2O3 | - | integral Gd |
| Max enrichment (wt%) | 4.95 | <5 | 3.1 | ~20 (HALEU) | LEU |
| F-dH | (this run) | 1.39 | ~1.5 | - | NuScale lower due to boron shaping |
| MTC (pcm/C) | (this run) | 0 to -60 | <0 | <0 | negative, SBF stronger |
| Discharge burn-up (GWd/t) | (this run) | ~30 | ~24 | - | high-burn-up target |

NuScale reaches a lower F-dH because soluble boron flattens the radial flux; the SBF Aegis-40 and CAREM-25
shape power with zoning + burnable absorber and justify peaking on DNBR margin at low power density.'''

MD_SHIELD = '''## 14 · Radiation shielding (biological shield)
The actual 17x17 core lattice is wrapped in a lead-free cylindrical biological shield and run as a coupled
neutron + photon eigenvalue transport (the real fission source drives both). Lead is excluded (toxicity)
and tungsten reserved for casks; the bulk shield is magnetite (heavy) concrete with a borated-polyethylene
thermal-neutron layer. Design criterion: total dose < 10 uSv/h behind the last layer. Outputs: dose vs
radius (plot + CSV), RPV fast flux (E > 1 MeV) for vessel fluence, n/gamma spectra at three interfaces,
and heating. Statistics are low by default — raise `STAT_SHIELD` for reported numbers.'''

MD_CASK = '''## 15 · Spent-fuel cask (companion)
The dry-cask shield (decay-photon source built from the depletion results) is the companion script
`aegis40_cask_v7.py` in this folder; run it separately:

```bash
export AEGIS_DEPLETION_H5=.../depletion/depletion_results.h5
python aegis40_cask_v7.py     # -> out_taskB/ (surface / 1 m / 2 m dose vs SSR-6)
```'''

MD_APPENDIX = '''## 16 · Digital appendix and reproducibility
- **Sample input.** Every analysis exports its complete OpenMC XML (`geometry.xml`, `materials.xml`,
  `settings.xml`, `tallies.xml`) to `aegis40_*_outputs/0?_*/` — any one directory is a self-contained,
  runnable sample input for the FER appendix ZIP.
- **Assumptions & conditions.** 3-D heterogeneous core, vacuum BCs (full leakage), ENDF/B-VIII.0, fuel
  900 K / moderator 556 K @ 12.8 MPa, design specific power; statistics per the `STAT_*` profile printed
  by each run.
- **Repeatability.** Fixed model; results reproduce within the reported Monte-Carlo sigma. Increasing
  `STAT` reduces sigma and collapses the raw 3-D F-Q toward the separable value.
- **Benchmarking / data provenance.** ENDF/B-VIII.0 (IAEA/NNDC); OpenMC is verified against the ICSBEP
  criticality suite. Design-level comparison in Section 13.
- **Outputs.** `safety_analysis_results.yaml` (+ `summary_report.txt`), the figures saved under
  `.../plots/`, and the depletion HDF5 are the reportable artefacts.'''

# ── new code: full-core loading map (pure matplotlib; no transport) ──────────
CODE_LOADING = '''# Full-core loading map (FER figure): core ring zone + Gd rods/FA + control-rod positions
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
fig, ax = plt.subplots(figsize=(7.5, 7.5))
half = (N_CORE - 1) / 2.0
ring_col = {0: "#b2182b", 1: "#ef8a62", 2: "#fddbc7", 3: "#d1e5f0"}
for j in range(N_CORE):
    for i in range(N_CORE):
        if CORE_MAP[N_CORE - 1 - j, i] != 1:
            continue
        r = _core_ring_of(i, j)
        x = (i - half) * FA_PITCH - FA_PITCH / 2
        y = (j - half) * FA_PITCH - FA_PITCH / 2
        ax.add_patch(Rectangle((x, y), FA_PITCH, FA_PITCH,
                               facecolor=ring_col.get(r, "#dddddd"), edgecolor="k", lw=1.2))
        ngd = int(round(N_GD_RODS * (GD_RING_WEIGHTS.get(r, 1.0) if RADIAL_GD_ZONING else 1.0)))
        cx = (i - half) * FA_PITCH
        cy = (j - half) * FA_PITCH
        ax.text(cx, cy + 4.5, f"r{r}", ha="center", fontsize=8, weight="bold")
        ax.text(cx, cy - 1.0, f"{ngd} Gd", ha="center", fontsize=7)
        if CR_MAP[N_CORE - 1 - j, i] == 1:
            ax.text(cx, cy - 6.5, "CR", ha="center", fontsize=7, color="navy", weight="bold")
refl = N_CORE * FA_PITCH / 2
ax.add_patch(plt.Circle((0, 0), refl + RADIAL_REFLECTOR_CM, fill=False, ls="--", color="navy", lw=1.3))
lim = refl + RADIAL_REFLECTOR_CM + 6
ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
ax.set_xlabel("x (cm)"); ax.set_ylabel("y (cm)")
ax.set_title(f"Aegis-40 full-core loading map ({N_FA_TOTAL} FA)\\n"
             "core ring (r0 centre..r3 outer) | Gd rods/FA | CR = control-rod cluster | dashed = water reflector")
ax.legend(handles=[Patch(facecolor=ring_col[k], edgecolor="k", label=f"ring {k}") for k in (0, 1, 2, 3)],
          loc="upper right", fontsize=8, framealpha=0.9)
try:
    fig.savefig(PLOTS / "core_loading_map.png", dpi=200, bbox_inches="tight")
except Exception:
    fig.savefig("core_loading_map.png", dpi=200, bbox_inches="tight")
plt.show()'''

# ── new code: consolidated FER tables from the results dict (defensive .get) ──
CODE_TABLES = '''# Consolidated FER tables — reactivity balance, feedback coefficients, peaking, uncertainty.
# Pulls from the `results` dict populated by the analysis cells above (run them first).
def _r(*keys, d="(run analysis cell)"):
    for k in keys:
        if k in results and results[k] is not None:
            return results[k]
    return d

print("="*64)
print("TABLE A — REACTIVITY BALANCE & CONTROL")
print("="*64)
print(f"  BOC k-effective (ARO)        : {_r('k_eff_bol','k_eff_operating')}")
print(f"  Control-rod worth (ARO->ARI) : {_r('control_rod_worth_aro_pcm','control_rod_worth_aro')} pcm")
print(f"  Shutdown margin (1 stuck rod): {_r('shutdown_margin_dk_pct','shutdown_margin')} % dk/k")
print(f"  Max reactivity insertion rate: {_r('max_reactivity_rate','max_reactivity_insertion_rate')} dk/k/s")

print("\\n" + "="*64)
print("TABLE B — REACTIVITY FEEDBACK COEFFICIENTS")
print("="*64)
print(f"  Moderator temp. coeff (MTC)  : {_r('mtc_full_power_pcm_per_K','mtc_full_power')} pcm/K")
print(f"  Doppler / fuel temp. (DTC)   : {_r('dtc_pcm_per_K','dtc_doppler')} pcm/K")
print(f"  Void coefficient             : {_r('void_coeff_pcm_per_pct','void_coefficient')} pcm/%void")

print("\\n" + "="*64)
print("TABLE C — POWER PEAKING")
print("="*64)
print(f"  F-dH (radial, per-pin)       : {_r('radial_peaking_FdeltaH_raw','radial_peaking_FdeltaH')}")
print(f"  F-z  (axial)                 : {_r('axial_peaking_Fz')}")
print(f"  F-radial (assembly)          : {_r('assembly_peaking_F_radial')}")
_fdh = _r('radial_peaking_FdeltaH_raw','radial_peaking_FdeltaH', d=None)
_fz  = _r('axial_peaking_Fz', d=None)
if isinstance(_fdh,(int,float)) and isinstance(_fz,(int,float)):
    print(f"  F-Q (separable F-dH x F-z)   : {_fdh*_fz:.3f}   <- report this (raw 3-D max is MC noise)")

print("\\n" + "="*64)
print("TABLE D — MONTE-CARLO UNCERTAINTY")
print("="*64)
print(f"  Active / inactive batches    : {STAT['batches']-STAT['inactive']} / {STAT['inactive']}")
print(f"  Particles per batch          : {STAT['particles']}")
print(f"  k-eff std. dev.              : {_r('k_eff_bol_sigma_pcm','k_eff_sigma','k_eff_std_pcm')} pcm")
print("  (peaking tally relative errors reported by the peaking cell)")
print("\\nFull results dict:")
for _k in sorted(results):
    print(f"    {_k} = {results[_k]}")'''

# ── assemble the clean notebook ─────────────────────────────────────────────
replace = {0: md(MD_TITLE), 1: md(MD_CODES), 3: code(CFG), 4: md(MD_GEOM),
           7: md(MD_BUILDERS), 13: md(MD_LOADING), 16: md(MD_STATIC),
           24: md(MD_DEPLETION), 27: md(MD_PEAKING), 30: md(MD_CONSOL), 38: md(MD_SHIELD),
           44: md(MD_CASK)}
drop = {32, 33, 34, 35, 36, 37}
insert_after = {
    0: [md(MD_INTRO)],            # 1 Introduction
    2: [md(MD_CRITERIA)],         # 3 Design criteria (after env code)
    5: [md(MD_MATERIALS)],        # 4 Core materials (before materials factories cell 6)
    13: [code(CODE_LOADING)],     # loading-map figure (before plot cells)
    31: [code(CODE_TABLES), md(MD_SAFETYCASE), md(MD_BENCH)],  # tables + safety-case + benchmarking
    44: [md(MD_APPENDIX)],        # 16 digital appendix (after cask)
}

new_cells = []
for i, c in enumerate(S):
    if i in drop:
        continue
    new_cells.append(replace[i] if i in replace else keep(i))
    for nc in insert_after.get(i, []):
        new_cells.append(nc)

out = dict(src)
out['cells'] = new_cells
json.dump(out, open(DST, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.load(open(DST, encoding='utf-8'))  # round-trip

# verify every code cell compiles (skip the %matplotlib magic cell)
bad = 0
for i, c in enumerate(out['cells']):
    if c['cell_type'] != 'code':
        continue
    s = ''.join(c['source'])
    if '%matplotlib' in s or s.lstrip().startswith('%'):
        continue
    try:
        ast.parse(s)
    except SyntaxError as e:
        print("COMPILE FAIL", i, e); bad += 1
print("OK clean FER notebook written:" if not bad else f"{bad} cells FAILED:")
print("   ", DST)
print(f"    cells: {len(S)} -> {len(new_cells)}  (dropped {len(drop)}, added {sum(len(v) for v in insert_after.values())})")
