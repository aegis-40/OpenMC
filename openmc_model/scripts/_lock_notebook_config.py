"""Lock aegis40_neutronics_FER.ipynb to the chosen design (Approach B, Gd 20@6,
in-out enrichment + edge de-rate) and insert the run-instructions section, so it
is ready for an end-to-end STAT_FINAL run on any machine. Backs up the original."""
import json, shutil, sys, datetime, io

NB = "/mnt/d/conda-envs/openmc-py311/SMRs/Shielding/aegis40_neutronics_FER.ipynb"
REF = "/home/samira/ref_neutronics.ipynb"
INSTR = "/mnt/c/Users/User/AppData/Local/Temp/claude/D--projects-teknofest-2026-aegis-40-ipwr/526f8ecb-67ef-4d55-b945-caf221357cd7/scratchpad/run_instructions.md"

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy(NB, NB + f".bak_prelock_{stamp}")

nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))

# ---- targeted config replacements (cell 1: locked design constants) ----
REPL = [
    ("EDGE_ENRICH      = 4.0",
     "EDGE_ENRICH      = 3.6     # LOCKED: sharper FA-perimeter de-rate (de-peak)"),
    ("RADIAL_ENRICH_ZONING = False              # assembly-uniform out-in option (intra-FA grade preferred)",
     "RADIAL_ENRICH_ZONING = True               # LOCKED: discrete uniform-enrichment assemblies (Approach B)"),
    ("RING_ENRICH = {0: 4.0, 1: 4.4, 2: 4.7, 3: 4.95}",
     "RING_ENRICH = {0: 4.95, 1: 4.7, 2: 4.4, 3: 4.0}   # LOCKED in-out: high centre (Gd-suppressed) / low periphery"),
    ("GD_WT_PCT       = 8        # wt% Gd2O3 in the Gd-bearing rods",
     "GD_WT_PCT       = 6        # wt% Gd2O3 in the Gd-bearing rods (LOCKED)"),
    ("N_GD_RODS       = 32       # per-FA average (ring zoning redistributes by ring)",
     "N_GD_RODS       = 20       # per-FA average, ring-zoned (LOCKED; was 32 -> over-loaded keff)"),
]

hits = {old: 0 for old, _ in REPL}
for c in nb["cells"]:
    if c["cell_type"] != "code":
        continue
    s = "".join(c["source"])
    if "RADIAL_ENRICH_ZONING" not in s and "N_GD_RODS" not in s:
        continue
    for old, new in REPL:
        if old in s:
            s = s.replace(old, new); hits[old] += 1
    c["source"] = s.splitlines(keepends=True)

missing = [o for o, n in hits.items() if n == 0]
if missing:
    print("WARNING: these strings were NOT found (config not fully locked):")
    for m in missing:
        print("   !! " + m[:70])
    sys.exit(1)

# ---- insert run-instructions markdown after the title cell ----
instr_src = io.open(INSTR, encoding="utf-8").read()
already = any(c["cell_type"] == "markdown" and "How to run this notebook" in "".join(c["source"])
              for c in nb["cells"])
if not already:
    md = {"cell_type": "markdown", "metadata": {}, "source": instr_src.splitlines(keepends=True)}
    # find first markdown title cell, insert right after it
    ins = 1
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "markdown" and "".join(c["source"]).lstrip().startswith("# Aegis"):
            ins = i + 1; break
    nb["cells"].insert(ins, md)
    print(f"inserted run-instructions markdown at cell index {ins}")
else:
    print("run-instructions markdown already present (skipped)")

out = json.dumps(nb, ensure_ascii=False, indent=1)
open(NB, "w", encoding="utf-8").write(out)
open(REF, "w", encoding="utf-8").write(out)
print(f"locked config written to:\n  {NB}\n  {REF}")
print("replacements applied:", {o[:24]: n for o, n in hits.items()})
