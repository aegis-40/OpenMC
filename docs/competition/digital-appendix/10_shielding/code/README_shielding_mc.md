# Converged operational-shield dose MAP — how to run (Task A)

`aegis40_shielding_mc.py` is the full-physics Monte-Carlo replacement for the point-kernel
estimate: a fixed neutron+gamma core source transported through the adopted lead-free radial
stack with MAGIC weight windows, tallied on a cylindrical (r,z) mesh → a dose-rate **map**.

The figure committed here (`../figures/shield_dose_map.png`) is the **absolute** dose result:
- (top) the 2D neutron+gamma dose FIELD from the weight-window MC, µSv/h;
- (bottom) the mid-plane radial dose — MC markers **agree with the ANS-6.4 point-kernel**
  across the overlap (RPV→~230 cm), and the point-kernel carries the dose to the outer
  concrete face at **0.23 µSv/h** (40× under the 10 µSv/h target).

Normalisation note (important): OpenMC source `strength` values here are ABSOLUTE emission
rates [part/s], so the mesh flux/dose tallies come out already rate-normalised — do NOT
multiply by the source rate again (that was a factor-1e19 bug, now fixed). Verified: the MC
mid-plane dose overlays the point-kernel with no free scaling.

The MC alone is converged out to ~230-250 cm; the deepest ~1 m is weight-window frontier.
For a **pure-MC converged map all the way to the outer face** (optional refinement, since the
point-kernel already carries it), run on the workstation / friend's PC with many cores:

```bash
conda activate openmc          # OpenMC 0.15.x with ENDF/B-VIII.0 (incl. photon data)
export OPENMC_CROSS_SECTIONS=/path/to/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_THREADS=$(nproc)

cd 10_shielding/code
TASKA_STAT=final TASKA_WW=1 python aegis40_shielding_mc.py   # ~high stats, weight windows on
python plot_dose_map.py                                       # renders the map from the .npz
```

Notes for convergence to the outer face (3 m of shield):
- `TASKA_STAT=final` = 100 batches × 500 k particles; **raise batches further** if the outer
  concrete face still reads 0 — the online weight-window generator needs enough batches to
  mature before the deep tally fills in.
- For a rigorous **two-stage** MAGIC: run once to write `weight_windows.h5`, then a production
  run that loads it (`settings.weight_windows = openmc.hdf5_to_wws('weight_windows.h5')`,
  generators off). Single-stage (the default here) is usually enough for a dose map.
- The absolute outer-face dose to compare against is **0.23 µSv/h** (point-kernel,
  `point_kernel_dose.py`) versus the 10 µSv/h design target.
- Runtime is source-particles-bound; on 32 cores expect tens of minutes at `final`.

Output: `../outputs/shield_dose_map.npz` (r, z, neutron/photon/total dose grids) →
`plot_dose_map.py` → `../figures/shield_dose_map.png`.
