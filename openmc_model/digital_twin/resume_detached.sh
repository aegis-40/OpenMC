#!/bin/bash
# Detached, sleep-proof relauncher for the twin sweep.
# setsid+nohup so the launcher lives in the WSL VM independent of the wsl.exe
# call that starts it (survives the caller exiting AND laptop sleep/resume).
# Idempotent: if twin_sweep.py is already running, it just reports status.
OUTDIR=/home/samira/aegis_run/twin_sweep
MAPS="$OUTDIR/maps"
CSV="$OUTDIR/core_sweep.csv"

nmaps=$(ls "$MAPS"/*.npy 2>/dev/null | wc -l)
nrows=$(wc -l < "$CSV" 2>/dev/null)
running=$(pgrep -c -f twin_sweep.py)
echo "points-done(maps)=$nmaps  csv-rows=$nrows  twin_sweep.py-running=${running:-0}"

if [ "${running:-0}" -eq 0 ]; then
  cd /mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/digital_twin || exit 1
  export TWIN_STAT=custom OPENMC_THREADS=8 TWIN_N=120
  setsid nohup bash run_twin_sweep.sh >/dev/null 2>&1 </dev/null &
  echo "RELAUNCHED detached pid $!"
  sleep 4
  echo "verify: $(pgrep -c -f twin_sweep.py) twin_sweep.py proc(s) alive"
else
  echo "already running - left as is"
fi
