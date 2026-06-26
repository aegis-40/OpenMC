#!/bin/bash
# Wait for the current ZONED STAT_MEDIUM run (PID 354) to finish, then fire the
# REGULAR (uniform-Gd) STAT_MEDIUM run at the same 16@5+Er loading — for the
# zoned-vs-regular peaking/cycle trade study.
PID=354
echo "[chain] waiting for zoned run PID $PID ... $(date)"
while kill -0 "$PID" 2>/dev/null; do sleep 120; done
echo "[chain] zoned run finished $(date); launching uniform-Gd run"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/d/conda-envs/openmc-py311
cd /home/samira/aegis_run/fer_smoke
export FER_N_GD=16 FER_GD_WT=5 FER_ER_WT=0.5 FER_N_ER=12 FER_STAT=medium FER_RADIAL_GD=0 FER_TAG=uniform16x5_med
python -u run_fer_smoke.py > uniform_run.log 2>&1
echo "[chain] uniform-Gd run finished $(date)"
