# Reproducibility — step-by-step

Every FER thermal-hydraulic number can be regenerated from this appendix plus the
project repository. All post-processing is deterministic (bit-identical re-runs).

## 1. CFD case (OpenFOAM v2412, Docker)

The `scalarCodedSource` heat source compiles C++ at runtime — the container MUST run
**non-root**:

```bash
cd <repo>/pin          # or pin_coarse / pin_fine, or 01_OpenFOAM_CFD/sample_case
docker run --rm --platform linux/amd64 --shm-size=1g \
  --user $(id -u):$(id -g) -e HOME=/tmp \
  -v $(pwd)/..:/home/ofuser/OpenFOAM/Aegis40 \
  opencfd/openfoam-default:2412 \
  bash -c "source /usr/lib/openfoam/openfoam2412/etc/bashrc && \
           cd /home/ofuser/OpenFOAM/Aegis40/pin && \
           ./Allmesh && decomposePar -allRegions && \
           mpirun -np 8 chtMultiRegionFoam -parallel && \
           reconstructPar -allRegions -latestTime"
```
Serial alternative: `./Allrun`. Expected: steady state by the final time; the
`bulkTout` / `massFlow` function objects log the mixing-cup outlet and flow.

**Acceptance (in order):**
1. GATE-1 energy balance ×1.00 (`python3 tools/meshindep.py`, worst dev ≤ 2 %);
2. GCI table mesh-independent (temperature change < 0.4 % medium→fine);
3. CFD ↔ correlation stack < 9 K (figure F3, `make_figs_aegis.py`).

## 2. Safety post-processing (host python3, no OpenFOAM required)

```bash
python3 tools/natcirc.py                        # G 542 kg/m2s, dT 50 K @ H_tc 4 m
python3 tools/mdnbr.py --chf bowring            # envelope design point
python3 tools/mdnbr.py --chf groeneveld         # LUT corroboration (MDNBR 6.18)
python3 tools/cycle_mdnbr.py --shapes --aoo     # binding table: 1.33 / 2.13; AOO 1.57
python3 tools/thermal_stack.py                  # PCT 353 C, fuel 828 C
python3 tools/stability_map.py                  # DWO x4.2 / Ledinegg stable
python3 tools/f5_prhr.py --vol 250 --unc 1.15   # >= 240 h grace
python3 tools/aegis_sweep.py                    # H_tc sweep (3 m FAILS, >= 4 m PASSES)
```
Expected values are printed with validity warnings; they must match the FER §8
metrics table to the printed precision.

## 3. Figures & report

```bash
python3 tools/make_figs_aegis.py            # F1-F8 (reads the CFD fields + tools live)
pvbatch tools/make_paraview_figs.py         # F9a-c (ParaView >= 5.10)
python3 tools/stability_map.py --png docs/figs/F10_stability_map.png
python3 tools/build_report_aegis.py         # docs/Aegis40_TH_report.docx
```

## 4. Repeatability evidence

- CFD: three independent runs (distinct field write-times, audited by
  `meshindep.py`) converge to GCI-consistent solutions.
- Python stack: pure functions of their inputs — re-running reproduces every digit.
- The mixing-cup/mass-flow reductions in `meshindep.py` were verified to reproduce
  the solver's own function objects to all printed digits (independent
  implementation of the same integral).
