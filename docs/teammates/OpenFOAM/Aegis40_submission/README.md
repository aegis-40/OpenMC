# Aegis-40 — Thermal-Hydraulic Design & Safety Analysis

OpenFOAM `chtMultiRegionFoam` conjugate heat-transfer model (fuel / cladding / coolant)
of the **Aegis-40** reactor — a **125 MWth / 40 MWe soluble-boron-free (SBF),
natural-circulation integral PWR** — coupled to a correlation-based safety
post-processor (MDNBR, PCT). Every thermal-hydraulic input is taken one-for-one from
the locked **OpenMC** neutronics (FER notebook): geometry, operating temperatures and
pin-power peaking. The toolchain was first verified & validated against the published
**NuScale NPM-160** reference — included here as [`NuScale_validation/`](NuScale_validation/).

## Key results (cycle-resolved OpenMC peaking; binding = the MOC COLR envelope)

- **Energy-conservative** — advected power = source to ×1.00 on every mesh (GATE-1);
  the single-phase constant-property problem is linear in power, so the V&V holds at
  every cycle state.
- **Mesh-independent** — ASME V&V-20 GCI < 0.15 % on outlet, clad & near-wall T.
- **CFD ↔ correlation stack agree to < 9 K** on every quantity (bulk & fuel < 1 K) —
  the CFD near-wall heat transfer reproduces Dittus-Boelter.
- **Cycle peaking resolved (BOC 1.937 / MOC-hump 2.435 / EOC 2.121)** and bound by a
  design-specific **COLR envelope F_q 2.468 (F_ΔH 1.750 × F_z 1.410)** set by the MOC
  Gd-burnout hump. **MDNBR with the record axial shapes: BOC 1.54/2.66 · MOC 1.35/2.15
  · EOC 1.46/2.50 · envelope 1.33 (W-3, conservative) / 2.13 (Bowring, in-range)** —
  all ≥ 1.3. Bounding **AOO (118 % P / 80 % G): 1.57** (Bowring, record shape). The
  Groeneveld CHF look-up table (K1·K4·K5 per IAEA-TECDOC-1203 Table 3.3) corroborates
  with envelope MDNBR 6.18.
- At the envelope the hot channel runs saturated at the top (exit quality 7.5 %);
  peak clad **353 °C** (Jens-Lottes), peak fuel **828 °C** (≪ melt); **PCT 353 °C**
  (≪ 1200 °C accident limit).
- **Natural circulation** delivers the FER design flow (ΔT 50 K → G 543) at a riser
  thermal-centre height **H_tc ≥ 4 m** (the design value; the analysis at 4.0 m bounds
  any larger as-built height), giving a compact (~10 m) **NuScale-class** integral
  vessel with the steam generator in the annulus above the core. The analytical
  loop-loss budget (K ≈ 5 vs the assumed 12) shows the flow is conservative; even the
  worst-case envelope K ≈ 17 keeps MDNBR ≥ 2.48 (Bowring).
- **Flow stability:** Ledinegg excursion-stable by construction; density-wave
  (Ishii–Zuber, conservative screen at the COLR envelope) — design point ×4.2 inside
  the boundary with NO spacer-grid credit, bounding AOO corner ×1.17 (×1.60 crediting
  the five real grids); average channels stay subcooled (no DWO mode).
- **Passive decay-heat removal (PRHR/IRWST):** ≥ 240 h grace for a 250 m³ vented
  (boiling) pool at ×1.15 decay-heat uncertainty; ~95 m³ suffices for 72 h.
- **SBLOCA & containment** substantiated by explicit bounding-by-reference to the
  NRC-licensed NuScale envelope (0.78 × module power, same 37-FA core, immersed
  high-pressure steel CNV) — see `docs/Aegis40_F3_F6_bounding.md`.

Full write-up → [`docs/Aegis40_TH_report.docx`](docs/Aegis40_TH_report.docx).

---

## Repository layout

### CFD cases — mesh-independence (GCI) set
| Folder | Mesh | Role |
|---|---|---|
| `pin_coarse/` | 35.7 k cells | grid-convergence coarse level |
| `pin/`        | 103.6 k cells | **production / medium** |
| `pin_fine/`   | 279.9 k cells | grid-convergence fine level |

The three meshes are geometrically similar — only the resolution knobs in
`system/blockMeshDict` differ; every physics input (source, properties, BCs, schemes)
is byte-identical across the set, so the GCI isolates discretisation error. Each is a
standard OpenFOAM multi-region case:

```
pin/
├── 0.orig/             initial & boundary fields per region (fuel/clad/coolant)
├── system/
│   ├── controlDict       run control + function objects (bulkTout, massFlow)
│   ├── fvSchemes, fvSolution, decomposeParDict
│   ├── blockMeshDict     PARAMETRIC butterfly O-grid (mesh knobs n*, g*)
│   └── fuel/ clad/ coolant/   per-region fvSchemes / fvSolution / decomposeParDict
├── constant/
│   ├── regionProperties        lists the fluid/solid regions
│   ├── g                       gravity
│   ├── fuel/fvOptions          chopped-cosine heat source (scalarCodedSource) ★
│   ├── fuel|clad|coolant/thermophysicalProperties
│   └── coolant/turbulenceProperties   (k-ω SST)
├── Allmesh             blockMesh -> splitMeshRegions -> seed 0/ from 0.orig
└── Allrun              Allmesh -> chtMultiRegionFoam
```
★ `fuel/fvOptions` holds `qpeak` (2.996e8 W/m³ = the COLR design envelope, F_q 2.4675,
Le 2.2667 m / F_z 1.410) and the GATE-1 energy-balance note. All three cases carry a
byte-identical `fvOptions`.

> **Generated data is not included** (`0/`, time dirs, `constant/*/polyMesh`,
> `dynamicCode/`, `processor*/`, `postProcessing/`, logs) — it is reproducible with
> `./Allrun`. The validated results live in the figures, the report and the
> post-processors below.

### Post-processors — `tools/` (python3; matplotlib for figures, python-docx for the report)
| Script | Purpose |
|---|---|
| `meshindep.py` | Field-direct mesh-independence / **ASME V&V-20 GCI** + GATE-1 energy balance (reads the latest-time fields straight off disk). |
| `mdnbr.py` | **MDNBR** — W-3 CHF + Tong F-factor; **Bowring-1972** (low-flow-valid, `--chf bowring`); Groeneveld LUT with K1+K4+K5 (`--chf groeneveld`, corroboration); two-phase equilibrium-quality cap at the outlet. |
| `thermal_stack.py` | **PCT** & fuel centreline — Dittus-Boelter film + 1-D radial conduction stack (film→clad→He-gap→fuel) + Jens-Lottes subcooled-boiling clamp. |
| `natcirc.py` | 1-D natural-circulation buoyancy balance ṁ(H_tc, P) — fixes the core flow G. |
| `aegis_sweep.py` | Feasibility sweep over riser height H_tc → G, MDNBR, PCT (single source of truth for the shared design constants). |
| `aoo_dnbr.py` | Bounding **AOO transient MDNBR envelope** — quasi-steady power × flow sweep (Bowring CHF). |
| `f5_prhr.py` | **Passive decay-heat (PRHR/IRWST) grace period** — ANS-5.1-class decay + pool sensible + boil-off. |
| `b2_loss_budget.py` | Analytical **natural-circulation loss budget** (per-component K referenced to core velocity). |
| `stability_map.py` | **Flow-stability screen** — Ledinegg (excursive) + Ishii–Zuber density-wave map (N_sub–N_pch), with/without spacer-grid credit, figure F10. |
| `cycle_mdnbr.py` | **Cycle MDNBR (BOC/MOC/EOC + COLR envelope)** — W-3 + Bowring + PCT/fuel + DWO per state; `--shapes` feeds the record axial tallies (`tools/data/axial_profile_BOC_MOC_EOC.csv`) directly to the correlations. |
| `groeneveld.py` | Groeneveld-2006 CHF **LUT interpolator** — K1 diameter + K4 heated-length + K5 axial-flux (IAEA-TECDOC-1203 Tab. 3.3); corroborates W-3/Bowring. |
| `make_figs_aegis.py` | Generates report figures **F1–F8** → `docs/figs/` (pulls GCI/GATE-1/stack live). |
| `make_paraview_figs.py` | Headless ParaView (`pvbatch`) renders **F9a–c** from the medium-mesh latest-time fields. |
| `build_report_aegis.py` | Builds the report `docs/Aegis40_TH_report.docx`. |

### `NuScale_validation/`
The validation companion: the same conjugate-pin toolchain applied to the published
**NuScale NPM-160** operating point *before* Aegis-40 — energy-conservative (GATE-1),
mesh-independent (GCI), natural-circulation ṁ(P) within 7 % of published full-scale
data with no tuning, and the published hot-leg / saturation-boundary / clad
temperatures reproduced. Contains its own README, the three CFD cases, tools and
`docs/NuScale_validation_report.docx`.

### `docs/`
| Item | What |
|---|---|
| `Aegis40_TH_report.docx` | The design & safety report (regenerable; 12 embedded figures). |
| `Aegis40_F3_F6_bounding.md` | SBLOCA & containment bounding-by-reference substantiation (NuScale envelope). |
| `Aegis40_bowring_verification.md` | Term-for-term verification of the Bowring-1972 coefficients vs Todreas & Kazimi. |
| `neutronics_cycle_record.md` | The high-statistics neutronics record (cycle peaking, 16 CRA, REA/PDIL) — source of the COLR envelope. |
| `figs/` | Figures F1–F8 (generated), **F9a–c** ParaView renders, **F10** stability map. |

---

## Reproducing the results

**1 — Run a CFD case.** OpenFOAM v2412 in Docker, **non-root** (the `scalarCodedSource`
heat source compiles C++ at runtime and will not run as root). Parallel (8 cores):

```bash
docker run --rm --platform linux/amd64 --shm-size=1g \
  --user $(id -u):$(id -g) -e HOME=/tmp \
  -v $(pwd):/home/ofuser/OpenFOAM/Aegis40 \
  opencfd/openfoam-default:2412 \
  bash -c "source /usr/lib/openfoam/openfoam2412/etc/bashrc && set -o pipefail && \
           cd /home/ofuser/OpenFOAM/Aegis40/pin && \
           ./Allmesh && decomposePar -allRegions && \
           mpirun -np 8 chtMultiRegionFoam -parallel && reconstructPar -allRegions -latestTime"
```
For serial, replace the `decomposePar … reconstructPar` chain with `./Allrun`.

**2 — Post-process (host python3 — no OpenFOAM needed):**
```bash
python3 tools/meshindep.py            # GCI / mesh-independence + GATE-1 (reads the fields)
python3 tools/aegis_sweep.py          # natural-circulation feasibility (H_tc sweep, MDNBR, PCT)
python3 tools/mdnbr.py --chf bowring  # hot-channel DNBR (bare run = the design point)
python3 tools/aoo_dnbr.py             # bounding AOO MDNBR envelope
python3 tools/f5_prhr.py --vol 250 --unc 1.15   # PRHR / pool grace period
python3 tools/cycle_mdnbr.py --shapes --aoo     # BOC/MOC/EOC + COLR envelope, record shapes
python3 tools/stability_map.py --png docs/figs/F10_stability_map.png   # flow stability
python3 tools/make_figs_aegis.py      # figures F1–F8 -> docs/figs/
pvbatch tools/make_paraview_figs.py   # figures F9a–c (ParaView >= 5.10, optional)
python3 tools/build_report_aegis.py   # the .docx report
```

## Method in one sentence
The conjugate CFD provides the energy-conservative flow field, axial heat flux q″(z)
and coolant bulk T(z); the correlation stack (the COBRA/VIPRE/CTF industry standard)
turns those into MDNBR and PCT — used because it carries the CHF and subcooled-boiling
physics a single-phase CFD cannot, **not** because the CFD is inaccurate (its near-wall
heat transfer matches Dittus-Boelter to < 9 K).
