#!/bin/bash
# Digital-Twin Day-1 OpenMC sweep — self-resuming launcher (survives laptop sleeps).
# The Python script checkpoints in core_sweep.csv and skips done points, so each
# re-launch continues. Outputs (CSV + per-point power maps) on ext4; copy to repo after.
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/d/conda-envs/openmc-py311
export OPENMC_CROSS_SECTIONS=$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=$HOME/openmc_data/chain_endfb80_pwr.xml
export OPENMC_THREADS=${OPENMC_THREADS:-8}     # set to your physical-core count (e.g. 32 on the workstation)
export TWIN_STAT=${TWIN_STAT:-medium}          # fast | medium | final  (medium = the recommended sweet spot)
export TWIN_N=${TWIN_N:-120}                    # number of LHS points
export TWIN_SEED=${TWIN_SEED:-12345}
export TWIN_OUT=${TWIN_OUT:-/home/samira/aegis_run/twin_sweep}
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
