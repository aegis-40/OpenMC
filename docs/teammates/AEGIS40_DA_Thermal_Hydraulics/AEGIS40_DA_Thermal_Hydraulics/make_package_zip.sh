#!/bin/zsh
# Regenerate checksums and the zip for the Aegis-40 thermal-hydraulics
# Digital-Appendix package.
set -e
cd "$(dirname "$0")"

find . -type f ! -name checksums.txt ! -name "*.zip" ! -name .DS_Store \
  | sort | xargs shasum -a 256 > 04_VV_and_benchmarking/checksums.txt
echo "checksums: $(wc -l < 04_VV_and_benchmarking/checksums.txt) files"

cd ..
rm -f AEGIS40_DA_Thermal_Hydraulics.zip
zip -rq AEGIS40_DA_Thermal_Hydraulics.zip AEGIS40_DA_Thermal_Hydraulics -x "*.DS_Store"
echo "wrote $(du -h AEGIS40_DA_Thermal_Hydraulics.zip | cut -f1) AEGIS40_DA_Thermal_Hydraulics.zip"
