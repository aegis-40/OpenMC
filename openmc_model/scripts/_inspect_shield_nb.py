import json, re
nb = json.load(open("/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/"
                    "rev7_shielding/aegis40_3d_core_shielding_rev7.ipynb",
                    encoding="utf-8"))
cells = nb["cells"]
code = [c for c in cells if c["cell_type"] == "code"]
print(f"total cells={len(cells)}  code cells={len(code)}")

KEY = ["cross_section", "config[", "OPENMC_CROSS", "weight_window", "WeightWindow",
       "openmc.Source", "IndependentSource", "settings.run_mode", "run_mode",
       "fixed source", "fixed-source", ".run(", "STAT", "build_core",
       "homog", "shield", "magic", "WORKDIR", "outputs", "deplet"]
for i, c in enumerate(code):
    src = "".join(c["source"])
    hits = [k for k in KEY if k.lower() in src.lower()]
    if hits:
        first = src.strip().splitlines()[0][:70] if src.strip() else ""
        print(f"\n--- code#{i}  hits={hits}")
        print(f"    1st: {first}")
