#!/bin/bash
# Reliable (STAT_MEDIUM) A-vs-B static comparison: per-pin F_q max needs more
# histories/pin than STAT_FAST gives. Same Gd (20@6 + Er 16@0.5) in both so the
# only variable is the loading approach. Writes static_<tag>.json + *_med.log.
set -e
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/d/conda-envs/openmc-py311
export OPENMC_CROSS_SECTIONS=$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=$HOME/openmc_data/chain_endfb80_pwr.xml
export OPENMC_THREADS=8
cd /home/samira/aegis_run/ref_static
export FER_OUTJSON_DIR=$PWD
export FER_N_GD=20 FER_GD_WT=6 FER_N_ER=16 FER_ER_WT=0.5 FER_STAT=medium

echo "[chain] === Approach A (intra-FA grading) STAT_MEDIUM $(date) ==="
FER_RADIAL_ENRICH=0 FER_EDGE_GRADE=1 FER_TAG=A_intraFA_med \
    python -u run_ref_static.py > A_med.log 2>&1
echo "[chain] A done $(date)"

echo "[chain] === Approach B (discrete uniform-FA) STAT_MEDIUM $(date) ==="
FER_RADIAL_ENRICH=1 FER_EDGE_GRADE=0 FER_TAG=B_discrete_med \
    python -u run_ref_static.py > B_med.log 2>&1
echo "[chain] B done $(date)"
echo "[chain] ALL DONE $(date)"
