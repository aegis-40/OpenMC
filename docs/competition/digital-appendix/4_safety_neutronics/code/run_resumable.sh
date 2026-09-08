#!/bin/bash
# Self-resuming launcher for the safety-neutronics set. The Python script
# checkpoints after every sim and reuses any statepoint already on disk, so if
# the machine sleeps mid-run this loop simply re-launches on wake and continues
# from where it stopped. Stops when all four sims are complete.
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/d/conda-envs/openmc-py311
export OPENMC_CROSS_SECTIONS=$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=$HOME/openmc_data/chain_endfb80_pwr.xml
export OPENMC_THREADS=${OPENMC_THREADS:-8}
export SAFETY_STAT=${SAFETY_STAT:-medium}
export SAFETY_RUN=all
export SAFETY_OUT=${SAFETY_OUT:-/home/samira/aegis_run/safety_results}
cd /mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/safety_85_86
LOG=${SAFETY_LOG:-/home/samira/aegis_run/safety_run.log}
for i in $(seq 1 60); do
    echo "[launcher] attempt $i $(date)" >> "$LOG"
    python -u aegis40_safety_neutronics.py >> "$LOG" 2>&1
    if grep -q SAFETY_ALL_COMPLETE "$LOG"; then
        echo "[launcher] ALL COMPLETE after $i attempt(s) $(date)" >> "$LOG"
        break
    fi
    sleep 8
done
