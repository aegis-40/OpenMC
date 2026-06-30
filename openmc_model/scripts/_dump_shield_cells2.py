import json
nb = json.load(open("/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/"
                    "rev7_shielding/aegis40_3d_core_shielding_rev7.ipynb",
                    encoding="utf-8"))
code = [c for c in nb["cells"] if c["cell_type"] == "code"]
for i in [8, 27, 30, 31]:
    print("\n" + "=" * 28 + f" CODE CELL #{i} " + "=" * 28)
    print("".join(code[i]["source"]))
