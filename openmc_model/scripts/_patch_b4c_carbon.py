"""Patch the NuScale-benchmark deck: ENDF/B-VII.1 HDF5 has natural carbon as 'C0'
(not split C12/C13), so replace B4C's C12+C13 with C0 at the summed atom density.
1.89720E-02 + 2.12520E-04 = 1.918452E-02 (the ratio is exactly natural abundance)."""
import re
p = "/home/samira/aegis_run/nuscale_bench/deck/omc/nuscale/materials.py"
s = open(p).read()
before = s
s = re.sub(r"mats\['B4C'\]\.add_nuclide\('C12'[^\n]*\n",
           "mats['B4C'].add_nuclide('C0' ,1.918452E-02 )\n", s)
s = re.sub(r"mats\['B4C'\]\.add_nuclide\('C13'[^\n]*\n", "", s)
if s != before:
    open(p, "w").write(s)
    print("patched B4C carbon -> C0")
else:
    print("NO CHANGE (pattern not found)")
# show the B4C block
for ln in s.splitlines():
    if "B4C" in ln:
        print("  ", ln)
