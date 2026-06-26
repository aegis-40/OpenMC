"""Verify our pincell INPUTS (material + geometry) against the BEAVRS 2.0.2 spec.

This is the only valid 'overlay' against the spec: BEAVRS provides the authoritative
input definition (Table 5 = 2.4% fuel; geometry source tables), NOT a single-pincell
k_inf(BU) reference curve. We confirm our config-acceptance run really is on the
BEAVRS basis.
"""
import openmc

# --- our pincell as actually run ---
m = openmc.examples.pwr_pin_cell()
fuel = next(x for x in m.materials if (x.name or "").lower().startswith("uo2"))
dens = fuel.get_nuclide_atom_densities()   # atom/b-cm

print("=== FUEL MATERIAL: our pwr_pin_cell vs BEAVRS Table 5 (2.4%) ===")
beavrs = {  # Table 5, p.58
    "U234": 4.4842e-06, "U235": 5.5814e-04, "U238": 2.2407e-02,
    "O16": 4.5830e-02, "O17": 1.7411e-05, "O18": 9.1898e-05,
}
print(f"{'nuclide':8} {'ours (a/b-cm)':>16} {'BEAVRS':>14} {'rel.diff':>10}")
for n, b in beavrs.items():
    o = float(dens.get(n, 0.0))
    rd = (o - b) / b * 100 if b else float("nan")
    print(f"{n:8} {o:16.5e} {b:14.5e} {rd:9.2f}%")
print(f"\nfuel density: ours set by composition; BEAVRS Table 5 = 10.29748 g/cc")

# --- geometry: pull radii + pitch from the model ---
print("\n=== GEOMETRY: our pincell cells ===")
for cid, cell in m.geometry.get_all_cells().items():
    reg = str(cell.region) if cell.region is not None else ""
    print(f"  cell {cid} '{cell.name}' fill={getattr(cell.fill,'name',cell.fill)}  region={reg[:70]}")
# surfaces (cylinders -> radii) and the lattice/box pitch
print("\n  surfaces:")
for sid, s in m.geometry.get_all_surfaces().items():
    if s.type == "z-cylinder":
        print(f"    z-cyl id{sid} r = {s.r:.5f} cm")
    elif s.type.startswith("x-plane") or s.type.startswith("y-plane"):
        print(f"    {s.type} id{sid} x0/y0 = {getattr(s,'x0',getattr(s,'y0',None))}")
print("\nBEAVRS spec geometry (source tables): pellet r=0.39218, clad ID=0.40005,")
print("clad OD=0.45720 cm, pin pitch=1.25984 cm (Tables 8-10, 4).")
