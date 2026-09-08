#!/bin/bash
# ============================================================================
# Aegis-40 digital-twin sweep — PORTABLE launcher (run on any OpenMC machine)
# 16-CRA, 90%-enriched-B-10 design. 168 points (120 wide LHS + 48 near-op cluster).
# Resumable: re-run this script any time; it skips points already in core_sweep.csv.
# ----------------------------------------------------------------------------
# PREREQS on the target PC:
#   1) `python -c "import openmc; print(openmc.__version__)"`  works (0.15.x)
#   2) ENDF/B-VIII.0 HDF5 data + a depletion chain available
#   3) point the two env vars below at them (edit the two paths, or export first)
# ============================================================================
set -u

# ---- EDIT THESE TWO to the friend's data paths (or export them before running) ----
export OPENMC_CROSS_SECTIONS="${OPENMC_CROSS_SECTIONS:-/path/to/endfb-viii.0-hdf5/cross_sections.xml}"
export OPENMC_CHAIN_FILE="${OPENMC_CHAIN_FILE:-/path/to/chain_endfb80_pwr.xml}"
# -----------------------------------------------------------------------------------

# use all cores by default (this is the whole point of the big machine)
export OPENMC_THREADS="${OPENMC_THREADS:-$( (nproc 2>/dev/null) || echo 8 )}"
export TWIN_STAT="${TWIN_STAT:-medium}"     # medium = 180 batches / 20k particles (FER quality)
export TWIN_N="${TWIN_N:-120}"              # wide-envelope LHS points
export TWIN_NLOCAL="${TWIN_NLOCAL:-48}"     # dense near-operating-point cluster
export TWIN_SEED="${TWIN_SEED:-12345}"
cd "$(dirname "$0")" || exit 1
export TWIN_OUT="${TWIN_OUT:-$PWD/twin_sweep_v2}"
mkdir -p "$TWIN_OUT"
LOG="$TWIN_OUT/run.log"

# sanity: data files present?
[ -f "$OPENMC_CROSS_SECTIONS" ] || { echo "!! OPENMC_CROSS_SECTIONS not found: $OPENMC_CROSS_SECTIONS"; echo "   edit the path at the top of this script."; exit 2; }
python -c "import openmc" 2>/dev/null || { echo "!! 'import openmc' failed — activate your OpenMC env first."; exit 3; }

echo "[run] threads=$OPENMC_THREADS  stat=$TWIN_STAT  points=$((TWIN_N+TWIN_NLOCAL))  out=$TWIN_OUT"
echo "[run] control rods: $(grep -m1 'N_CR_CLUSTERS = int' twin_sweep.py)  (expect 16)"

# resumable retry loop — restarts on any crash, skipping completed points
for attempt in $(seq 1 80); do
    echo "[run] attempt $attempt  $(date)" | tee -a "$LOG"
    python -u twin_sweep.py 2>&1 | tee -a "$LOG"
    if grep -q TWIN_SWEEP_COMPLETE "$LOG"; then
        echo "[run] ===== SWEEP COMPLETE ====="; break
    fi
    done=$(( $(wc -l < "$TWIN_OUT/core_sweep.csv" 2>/dev/null || echo 1) - 1 ))
    echo "[run] restart (banked $done / $((TWIN_N+TWIN_NLOCAL))); resuming in 5s..."; sleep 5
done

echo ""
echo "[run] DONE.  ==> Send BACK the whole folder:  $TWIN_OUT"
echo "     It contains core_sweep.csv + maps/*.npy — that's all I need to retrain the twin."
echo "     Easiest: zip it and drop in the shared Drive."
