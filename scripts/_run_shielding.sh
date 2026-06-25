#!/bin/bash
# ext4-accelerated headless run of the rev7 shielding §9.
source ~/miniconda3/etc/profile.d/conda.sh
conda activate /mnt/d/conda-envs/openmc-py311
export OPENMC_CROSS_SECTIONS=$HOME/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=$HOME/openmc_data/chain_endfb80_pwr.xml
export OPENMC_THREADS=8
cd $HOME/aegis_run/shielding
echo "[shield] start $(date) | XS=$OPENMC_CROSS_SECTIONS | batches=${AEGIS_SHIELD_BATCHES:-default} particles=${AEGIS_SHIELD_PARTICLES:-default}"
python -u run_shielding_generated.py
echo "[shield] exit $? $(date)"
