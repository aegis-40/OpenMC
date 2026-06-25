#!/bin/bash
# Detached 10k-particle Option-C depletion benchmark (BEAVRS 2.4% pincell).
# Launched via setsid so it survives the launching shell; writes to ext4.
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/d/conda-envs/openmc-py311
cd /mnt/d/projects/teknofest-2026-aegis-40-ipwr
RUNDIR=$HOME/aegis_run/pincell_10k
mkdir -p "$RUNDIR/out"
echo "[wrapper] start $(date)"
PYTHONPATH=src python -u scripts/benchmark_depletion_pincell.py \
  --optc \
  --particles 10000 --batches 115 --inactive 15 \
  --cross-sections "$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml" \
  --chain "$HOME/openmc_data/chain_endfb80_pwr.xml" \
  --workdir "$RUNDIR" \
  --outdir "$RUNDIR/out"
RC=$?
echo "[wrapper] python exit $RC $(date)"
if [ $RC -eq 0 ]; then
  DEST=/mnt/d/projects/teknofest-2026-aegis-40-ipwr/docs/competition/digital-appendix/pincell_run_10k
  mkdir -p "$DEST"
  cp -f "$RUNDIR"/out/* "$DEST"/ 2>/dev/null
  cp -f "$RUNDIR"/depletion_results.h5 "$DEST"/ 2>/dev/null
  echo "[wrapper] copied artifacts -> $DEST"
fi
echo "[wrapper] ALL DONE $(date)"
