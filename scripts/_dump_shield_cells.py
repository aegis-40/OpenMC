import json
nb = json.load(open("/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/"
                    "rev7_shielding/aegis40_3d_core_shielding_rev7.ipynb",
                    encoding="utf-8"))
code = [c for c in nb["cells"] if c["cell_type"] == "code"]
for i in [0, 6, 7, 28, 30]:
    print("\n" + "=" * 30 + f" CODE CELL #{i} " + "=" * 30)
    print("".join(code[i]["source"]))
