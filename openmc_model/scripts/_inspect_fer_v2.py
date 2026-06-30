import json, re
NB = "/mnt/c/Users/User/Downloads/Telegram Desktop/aegis40_neutronics_FER_v2.ipynb"
raw = open(NB, "rb").read()
print("first bytes:", raw[:12])
txt = raw.decode("utf-8-sig", errors="replace")
nb = json.loads(txt)
code = [c for c in nb["cells"] if c["cell_type"] == "code"]
print(f"code cells: {len(code)}")

CFG = ["GD_WT", "ER_WT", "GD2O3", "ER2O3", "ENRICH", "N_GD", "N_ER", "N_ER_RODS",
       "GD_POSITIONS", "ER_POSITIONS", "GD_RING", "RADIAL_GD", "wt%", "gd_wt", "er_wt",
       "ENRICH_INNER", "ENRICH_MID", "ENRICH_OUTER", "GD_WT_PCT", "ER_WT_PCT"]
print("\n===== CONFIG LINES =====")
for c in code:
    for ln in "".join(c["source"]).splitlines():
        s = ln.strip()
        if any(k in s for k in CFG) and ("=" in s) and not s.startswith("#") and len(s) < 90:
            print("  ", s)

print("\n===== k_eff / keff IN OUTPUTS =====")
for i, c in enumerate(code):
    for o in c.get("outputs", []):
        txt = ""
        if o.get("output_type") == "stream":
            txt = "".join(o.get("text", []))
        elif "data" in o and "text/plain" in o["data"]:
            txt = "".join(o["data"]["text/plain"])
        for ln in txt.splitlines():
            if re.search(r"k[_-]?eff|k_inf|keff|reactivit|BOC|EOC|SDM|critical", ln, re.I) \
               or re.search(r"\b0\.9\d{3}\b|\b1\.[01]\d{3}\b", ln):
                print(f"  [cell {i}] {ln.strip()[:110]}")
