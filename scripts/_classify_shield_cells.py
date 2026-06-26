import json
nb = json.load(open("/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/"
                    "rev7_shielding/aegis40_3d_core_shielding_rev7.ipynb",
                    encoding="utf-8"))
ci = 0
for c in nb["cells"]:
    if c["cell_type"] == "markdown":
        txt = "".join(c["source"]).strip().splitlines()
        h = txt[0][:70] if txt else ""
        print(f"   [md]            {h}")
        continue
    src = "".join(c["source"])
    lines = [l for l in src.splitlines() if l.strip()]
    head = lines[0][:66] if lines else ""
    # crude: does this cell actually RUN openmc (vs just def/const)?
    runs = any(k in src for k in ["model.run(", ".run(", "sp_path", "openmc.run(",
                                  "integrate(", "StatePoint(", "run_depletion"])
    defs = src.lstrip().startswith(("def ", "class ", "#", "STAT", "import",
                                    "from ", "SHIELD", "T_", "ENRICH", "N_", "GD_"))
    tag = "RUN!" if runs else ("def " if defs else "    ")
    print(f"#{ci:<3}[{tag}] {head}")
    ci += 1
