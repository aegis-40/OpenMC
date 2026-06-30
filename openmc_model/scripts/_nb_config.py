import json, re, sys
for path, tag in [("/home/samira/fer4.ipynb", "FER(4)"),
                  ("/home/samira/fer3.ipynb", "FER(3)")]:
    print("\n" + "=" * 20 + f" {tag}  {path} " + "=" * 20)
    try:
        nb = json.loads(open(path, "rb").read().decode("utf-8-sig", "replace"))
    except Exception as e:
        print("  PARSE FAIL:", e); continue
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    print(f"  code cells: {len(code)}")
    KEYS = ("N_FA", "N_CORE", "GD_WT", "ER_WT", "GD_WT_PCT", "ER_WT_PCT",
            "N_ER_RODS", "GD_POSITIONS", "ER_POSITIONS", "GD_RING_WEIGHTS",
            "ENRICH_INNER", "ENRICH_MID", "ENRICH_OUTER", "ENRICH", "RADIAL_GD",
            "HM_MASS", "SPECIFIC_POWER", "TIMESTEPS", "n_gd", "n_er",
            "gd_wt", "er_wt", "RHO_GD", "RHO_ER", "GD2O3", "ER2O3", "_gd_positions")
    for c in code:
        for ln in "".join(c["source"]).splitlines():
            s = ln.strip()
            if "=" in s and not s.startswith("#") and len(s) < 100 \
               and any(re.search(r"\b" + re.escape(k), s) for k in KEYS):
                print("   ", s)
