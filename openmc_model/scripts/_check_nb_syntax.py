import sys, json, ast
nb = json.load(open(sys.argv[1], encoding="utf-8"))
print("valid JSON,", len(nb["cells"]), "cells")
nbad = 0
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = "".join(c["source"])
    src = "\n".join("" if l.strip().startswith("%") else l for l in src.split("\n"))
    try:
        ast.parse(src)
    except SyntaxError as e:
        nbad += 1
        print(f"  CELL {i} SYNTAX ERROR line {e.lineno}: {e.msg}")
        print("   >>", (e.text or "").rstrip())
print("syntax check:", "ALL CODE CELLS OK" if nbad == 0 else f"{nbad} FAILED")
