#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/d/conda-envs/openmc-py311
EXT4XS=/home/samira/openmc_data/endfb-vii.1-hdf5
if [ ! -f "$EXT4XS/cross_sections.xml" ]; then
  echo "[states] copying VII.1 (5.9G) to ext4 ..."
  cp -r /mnt/d/openmc_data/endfb71/endfb-vii.1-hdf5 /home/samira/openmc_data/
fi
export OPENMC_CROSS_SECTIONS=$EXT4XS/cross_sections.xml
export PYTHONPATH=/home/samira/aegis_run/nuscale_bench/deck/omc
mkdir -p /home/samira/aegis_run/nuscale_bench/states_run
cd /home/samira/aegis_run/nuscale_bench/states_run
echo "[states] start $(date) | XS=$OPENMC_CROSS_SECTIONS | B=${NS_BATCHES} P=${NS_PARTICLES}"
python -u /mnt/d/projects/teknofest-2026-aegis-40-ipwr/scripts/_run_nuscale_states.py
RC=$?
echo "[states] python exit $RC $(date)"
DEST=/mnt/d/projects/teknofest-2026-aegis-40-ipwr/docs/competition/digital-appendix/nuscale_benchmark
mkdir -p "$DEST"
cp -f nuscale_states_results.json "$DEST"/ 2>/dev/null
echo "[states] results -> $DEST"
