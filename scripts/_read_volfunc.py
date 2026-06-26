import json, re
nb = json.loads(open("/home/samira/fer4.ipynb", "rb").read().decode("utf-8-sig", "replace"))
allsrc = "\n\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
m = re.search(r"def _assign_depletion_volumes.*?(?=\n(?:def |# ===|class ))", allsrc, re.S)
print(m.group(0)[:3000] if m else "FUNC NOT FOUND")
print("\n\n===== run_core_depletion =====")
m2 = re.search(r"def run_core_depletion.*?(?=\n(?:def |# ===|class ))", allsrc, re.S)
print(m2.group(0)[:1800] if m2 else "not found")
