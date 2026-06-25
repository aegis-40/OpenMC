"""Generate a headless, ext4-accelerated runner for the rev7 shielding §9 by
concatenating ONLY the cells §9 needs (definitions #0-#8 + shielding #27,28,30,31),
skipping the heavy core analyses (#9-#26). IPython magics are stripped."""
import json

NB = ("/mnt/d/projects/teknofest-2026-aegis-40-ipwr/openmc_model/"
      "rev7_shielding/aegis40_3d_core_shielding_rev7.ipynb")
OUT = "/home/samira/aegis_run/shielding/run_shielding_generated.py"

SELECT = [0, 1, 2, 3, 4, 5, 6, 7, 8, 27, 28, 30, 31]  # defs + §9 (skip 9-26, 29)

nb = json.load(open(NB, encoding="utf-8"))
code = [c for c in nb["cells"] if c["cell_type"] == "code"]

parts = [
    "# AUTO-GENERATED from aegis40_3d_core_shielding_rev7.ipynb (cells "
    f"{SELECT}).\n"
    "# Headless shielding-only run; ext4 cross-sections via env vars.\n"
    "import matplotlib\nmatplotlib.use('Agg')\n",
]
OVERRIDE = (
    "\n# ===== injected: env-driven STAT override (smoke vs full) =====\n"
    "import os as _os\n"
    "if _os.environ.get('AEGIS_SHIELD_BATCHES'):\n"
    "    STAT_SHIELD['batches'] = int(_os.environ['AEGIS_SHIELD_BATCHES'])\n"
    "if _os.environ.get('AEGIS_SHIELD_INACTIVE'):\n"
    "    STAT_SHIELD['inactive'] = int(_os.environ['AEGIS_SHIELD_INACTIVE'])\n"
    "if _os.environ.get('AEGIS_SHIELD_PARTICLES'):\n"
    "    STAT_SHIELD['particles'] = int(_os.environ['AEGIS_SHIELD_PARTICLES'])\n"
    "print('STAT_SHIELD ->', STAT_SHIELD, '| USE_WW =', USE_WW)\n"
)
for idx in SELECT:
    if idx == 30:                       # inject override just before the run cell
        parts.append(OVERRIDE)
    src = "".join(code[idx]["source"])
    lines = [l for l in src.splitlines()
             if not l.lstrip().startswith("%")          # strip %matplotlib etc.
             and "get_ipython()" not in l]
    parts.append(f"\n# ================= notebook code cell #{idx} =================\n")
    parts.append("\n".join(lines) + "\n")

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("".join(parts))
print(f"wrote {OUT}  ({sum(len(code[i]['source']) for i in SELECT)} src chars from "
      f"{len(SELECT)} cells)")
