# Run the digital-twin sweep on the friend's PC (~2 h on 32 cores)

**Goal:** produce a fresh 16-CRA OpenMC sweep so I can retrain the twin (tight coefficients + rod worth 21,509 pcm). The whole sweep is **168 points** and fully **resumable**.

## What to copy over
Just **one file** is required — the sweep is self-contained:
- `openmc_model/digital_twin/twin_sweep.py`  ← the 16-CRA model (check line 97 says `# 16`)
- `openmc_model/digital_twin/run_on_friend_pc.sh`  ← the launcher

Put both in the same folder on the friend's PC.

## Prereqs on the friend's PC
1. OpenMC 0.15.x working: `python -c "import openmc; print(openmc.__version__)"`
2. **ENDF/B-VIII.0** HDF5 cross-section data + a depletion chain file (they almost certainly have a library if they run OpenMC; VIII.0 preferred to match our FER).

## Steps
```bash
# 1) activate their OpenMC environment (conda/venv/module — however they normally do)
conda activate openmc            # example

# 2) tell it where their data is (edit to their real paths)
export OPENMC_CROSS_SECTIONS=/path/to/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=/path/to/chain_endfb80_pwr.xml

# 3) run it — uses ALL cores automatically, resumes if interrupted
bash run_on_friend_pc.sh
```
That's it. It prints progress like `[twin] 42/168 ... k=1.089`. On 32 cores expect **~40 s/point → ~2 h total**. If it stops for any reason, just run the same command again — it skips finished points.

## When it finishes — send back
Zip the output folder and drop it in the shared Drive:
```bash
zip -r twin_sweep_v2.zip twin_sweep_v2/     # core_sweep.csv + maps/*.npy  (~10 MB)
```
Send me `twin_sweep_v2.zip`. I'll run `fit_surrogates.py` on it (~1 min), refresh the DT artifacts + dashboard with the new numbers, regenerate checksums, and report the tightened coefficients vs the STAT_FINAL reference (MTC −26.87, DTC −1.91, void −173.2, rod worth 21,509 pcm).

## Notes
- **Don't change** `TWIN_SEED` (keeps the run reproducible/citable).
- Want it faster for a first look? `TWIN_STAT=fast bash run_on_friend_pc.sh` (~4× quicker, noisier — fine for a smoke check, but do the default `medium` for the FER-quality result).
- Nothing here touches the friend's system beyond writing the `twin_sweep_v2/` folder next to the script.
