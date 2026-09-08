#!/bin/bash
# Digital-Twin OpenMC sweep v2 (FINAL design) — self-resuming launcher.
#   * 90%-enriched-B-10 control rods, 16-CRA bank (rod worth ~21,509 pcm, matches DA-4 N5C)
#   * 120 wide LHS points  +  48-point DENSE cluster at the HFP operating point
#     -> accurate local reactivity coefficients (fixes the coarse v1 dk/dinput)
# Checkpoints in core_sweep.csv and skips done points, so each re-launch continues.
# Runtime ~ 168 points x ~1-2 min at TWIN_STAT=medium  ->  ~3-6 h on 8 cores (less on more).
# After it finishes: python fit_surrogates.py  (1-minute retrain), then copy artifacts to repo.
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/d/conda-envs/openmc-py311
export OPENMC_CROSS_SECTIONS=$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=$HOME/openmc_data/chain_endfb80_pwr.xml
export OPENMC_THREADS=${OPENMC_THREADS:-8}     # set to physical-core count (e.g. 32 on a workstation)
export TWIN_STAT=${TWIN_STAT:-medium}          # fast | medium | final  (medium = recommended)
export TWIN_N=${TWIN_N:-120}                    # wide-envelope LHS points
export TWIN_NLOCAL=${TWIN_NLOCAL:-48}           # dense near-operating-point cluster
export TWIN_SEED=${TWIN_SEED:-12345}
export TWIN_OUT=${TWIN_OUT:-/home/samira/aegis_run/twin_sweep_v2}   # FRESH dir (do not mix with the v1 natural-B sweep)
cd /mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/digital_twin
LOG=${TWIN_LOG:-/home/samira/aegis_run/twin_sweep.log}
echo "[launcher] start $(date)  N=$TWIN_N STAT=$TWIN_STAT threads=$OPENMC_THREADS -> $TWIN_OUT" >> "$LOG"
for i in $(seq 1 80); do
    echo "[launcher] attempt $i $(date)" >> "$LOG"
    python -u twin_sweep.py >> "$LOG" 2>&1
    if grep -q TWIN_SWEEP_COMPLETE "$LOG"; then
        echo "[launcher] ALL COMPLETE after $i attempt(s) $(date)" >> "$LOG"; break
    fi
    sleep 8
done
