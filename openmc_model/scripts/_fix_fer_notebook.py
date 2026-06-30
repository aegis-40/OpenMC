"""One-shot targeted fixes to aegis40_neutronics_FER.ipynb (37-FA design).
Each replacement asserts an exact occurrence count so a silent miss fails loudly."""
import json, sys
from pathlib import Path

NB = Path(r"D:\conda-envs\openmc-py311\SMRs\Shielding\aegis40_neutronics_FER.ipynb")
nb = json.loads(NB.read_text(encoding="utf-8"))

def cell_text(idx):
    return "".join(nb["cells"][idx]["source"])

def sub(idx, old, new, count=1):
    txt = cell_text(idx)
    n = txt.count(old)
    if n != count:
        raise SystemExit(f"CELL {idx}: expected {count} of <<{old[:60]}...>>, found {n}")
    nb["cells"][idx]["source"] = (txt.replace(old, new)).splitlines(keepends=True)

# ---- Fix #4a: cell 13 stale docstring 21-FA -> 37-FA ----
sub(13, "Build the 3D 21-FA core model", "Build the 3D 37-FA core model")

# ---- Fix #4b: cell 40 stale design_id ----
sub(40, "aegis40-3d-core-rev_6", "aegis40-3d-core-37fa")

# ---- Fix #4c: cell 20 stale palette enrichment keys ----
sub(20, '        "UO2_3.4":        (255, 215, 0),', '        "UO2_4.0":        (255, 215, 0),')
sub(20, '        "UO2_3.7":        (255, 165, 0),', '        "UO2_4.4":        (255, 165, 0),')
sub(20, '        "UO2_4.0":        (255, 99, 71),',
        '        "UO2_4.7":        (255, 99, 71),\n        "UO2_4.95":       (220, 50, 40),')

# ---- Fix #2: cell 5 banner honesty + cell 27 count-weighted average ----
sub(5, "ENRICH_OUTER  = 4.40       # core average ~4.69",
       "ENRICH_OUTER  = 4.40       # zone grade; true core-avg computed in cell 27")
sub(5, "(avg ~{_enr_avg:.2f})", "(zone-avg ~{_enr_avg:.2f}, excl. edge/BA)")

sub(27, '    results["enrichment_avg_pct"] = (ENRICH_INNER + 2*ENRICH_MID + ENRICH_OUTER) / 4.0',
        '    # Count-weighted core average over the 264 fuel pins, honouring the\n'
        '    # FA-perimeter edge grading and Gd/Er pins (ENRICH_MID base U).\n'
        '    _gd = set(GD_POSITIONS); _er = set(ER_POSITIONS)\n'
        '    _e = [ENRICH_MID if (i, j) in _gd or (i, j) in _er\n'
        '          else _enrichment_for_pin(i, j) for (i, j) in FUEL_POS]\n'
        '    results["enrichment_avg_pct"] = round(float(np.mean(_e)), 3)')
sub(27, "| avg ~ {results['enrichment_avg_pct']:.2f} wt%\")",
        "| count-weighted avg ~ {results['enrichment_avg_pct']:.2f} wt% over {len(FUEL_POS)} pins\")")

# ---- Fix #1: cell 26 worst-stuck-rod must remove a REAL cluster, not (3,3) instrument ----
sub(26,
    '# ("worst stuck rod"). We approximate the highest-worth single cluster as the **central CR\n'
    '# cluster** (it has the largest neutronic importance in a small symmetric core).',
    '# ("worst stuck rod"). The geometric centre (N_CORE//2, N_CORE//2) is the instrument\n'
    '# assembly (no CRA), so we approximate the highest-worth cluster as the innermost ACTUAL\n'
    '# cluster (nearest the centre = largest neutronic importance in a small symmetric core).')
sub(26, "    # Worst stuck rod: insert all clusters except the central one (i=2, j=2)",
        "    # Worst stuck rod: insert all clusters except the most-reactive (innermost) one.")
sub(26, "    central = (N_CORE // 2, N_CORE // 2)",
        "    centre = (N_CORE // 2, N_CORE // 2)\n"
        "    central = min(all_cr, key=lambda p: (p[0]-centre[0])**2 + (p[1]-centre[1])**2)")

# ---- Fix #3: cell 33 report SEPARABLE F_q (match the Section 9 markdown) ----
sub(33, "    F_q  = float(pin_z_g.max()   / pin_z_g.mean())       # true 3-D hot spot",
        "    F_q_raw = float(pin_z_g.max() / pin_z_g.mean())      # raw single-node 3-D max (diagnostic)")
sub(33, "    F_z  = float(fz_norm.max())\n",
        "    F_z  = float(fz_norm.max())\n"
        "    F_q  = F_dh * F_z                                    # separable F_q = F_dH x F_z (reported)\n")
sub(33, '    results["pin_peaking_factor_Fq_raw"]  = round(F_q, 3)',
        '    results["pin_peaking_factor_Fq_raw"]  = round(F_q_raw, 3)')
sub(33, "F_q  (3-D, per-pin)    = {F_q:.3f} raw", "F_q  (separable FdH*Fz)= {F_q:.3f}")
sub(33, ", F_q={F_q:.2f} raw\")", ", F_q(sep)={F_q:.2f}\")")

NB.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print("All replacements applied and written:", NB)
