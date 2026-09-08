# Aegis-40 Digital Twin — Day-1 OpenMC sweep

Generates the **neutronics training data** for the surrogate core twin
(`docs/competition/digital-twin-plan.md`). Reuses the locked 37-FA `build_core`.

## What it runs
A **Latin-Hypercube sweep (default 120 points)** at BOC over the operating envelope:

| Input | Range | drives |
|---|---|---|
| moderator T (+ water density) | 294–560 K | k, MTC |
| fuel T | 600–1200 K | DTC |
| control rods inserted | 0–12 CRAs (by centrality) | rod worth, SDM |
| void fraction | 0–0.20 | void coeff |

Per point it runs an OpenMC **eigenvalue + a 7×7×10 fission mesh** and logs to
`core_sweep.csv`: `id, T_mod, T_fuel, n_rods, void, k_eff, k_sigma_pcm, F_assembly`,
plus the per-assembly×axial power map → `maps/map_###.npy`. **k(inputs)** trains the
reactivity surrogate; **∂k/∂input** gives MTC/DTC/void (no extra runs); the maps train
the POD spatial surrogate. (Burnup axis is handled later by overlaying the existing
`depletion_results.h5` k(BU) curve — no re-depletion here.)

## How to launch
```bash
# set threads to your physical-core count first (32 on the workstation):
OPENMC_THREADS=32 bash run_twin_sweep.sh
```
- Default statistics **220×25k** (~45–50 pcm/run) → **~120 points ≈ 6 h on 8 threads / ~1.5–2 h on 32**.
- **Resumable + sleep-proof:** it checkpoints in `core_sweep.csv` and skips done points; the launcher
  re-runs until `TWIN_SWEEP_COMPLETE`. If the box sleeps, just re-run the same command.
- **Detached (survives closing the terminal):** `bash resume_detached.sh` — reports progress and
  relaunches (via `setsid`) only if not already running; safe to re-run after any sleep.
- Outputs land on ext4 at `~/aegis_run/twin_sweep/` (CSV + `maps/`). Copy to this folder when done:
  `cp ~/aegis_run/twin_sweep/core_sweep.csv ~/aegis_run/twin_sweep/maps -r .`

## Knobs (env)
`TWIN_N` (points) · `TWIN_STAT` (custom [default, 220×25k] | fast | medium | final) · `TWIN_SEED` ·
`TWIN_OUT` · `OPENMC_THREADS`.
Quick smoke test first: `TWIN_N=4 TWIN_STAT=fast bash run_twin_sweep.sh` (~1 min) to confirm it writes
`core_sweep.csv` + 4 maps, then launch the full 120.

## Regenerate the script (if the notebook config changes)
`python ../../scripts/_gen_twin_sweep.py`  (re-extracts `build_core` from `ref_neutronics.ipynb`).

## Next (Days 2–7)
Day 3 fits scalar surrogates on `core_sweep.csv`; Day 4 POD on `maps/`; Day 5 Streamlit dashboard.
