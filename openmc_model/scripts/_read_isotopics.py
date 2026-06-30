import openmc.deplete as d
import numpy as np

r = d.Results("/home/samira/aegis_run/pincell_10k/depletion_results.h5")
steps = [0.1, 0.4, 0.5] + [1.0] * 5 + [5.0] * 5
bu = np.concatenate([[0.0], np.cumsum(steps)])

mat = "1"  # UO2 fuel material id in pwr_pin_cell
nucs = ["U235", "Pu239", "Pu240", "Pu241", "Xe135", "Sm149", "Cs137", "Sr90"]

cols = {}
n = None
for nuc in nucs:
    try:
        _, atoms = r.get_atoms(mat, nuc)
        cols[nuc] = np.asarray(atoms, float)
        n = len(atoms)
    except Exception as e:
        cols[nuc] = None

print(f"completed steps with full isotopics: {n}")
hdr = "BU(MWd/kg) | " + " | ".join(f"{x:>10}" for x in nucs)
print(hdr)
print("-" * len(hdr))
for i in range(n):
    row = f"{bu[i]:9.2f}  | " + " | ".join(
        (f"{cols[x][i]:10.3e}" if cols[x] is not None else f"{'n/a':>10}") for x in nucs)
    print(row)
print("\n(atoms per cm of pin; every nuclide in the chain is stored, this is just a sample)")
