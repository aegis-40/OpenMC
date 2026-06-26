import json, re, sys
NB = sys.argv[1] if len(sys.argv) > 1 else "/home/samira/ref_neutronics.ipynb"
nb = json.loads(open(NB, "rb").read().decode("utf-8-sig", "replace"))
code = [c for c in nb["cells"] if c["cell_type"] == "code"]
ncode = len(code)
ntot = len(nb["cells"])
print("%d code cells, %d total" % (ncode, ntot))
pat = re.compile(r"^\s*[A-Z_][A-Z0-9_]{2,}\s*=\s*[-0-9.\"']", re.M)
seen = set()
for c in code:
    s = "".join(c["source"])
    for line in s.splitlines():
        if pat.match(line):
            key = line.strip().split("=")[0].strip()
            if key not in seen:
                seen.add(key)
                print("   " + line.strip()[:74])
print("---- markdown headers ----")
for c in nb["cells"]:
    if c["cell_type"] == "markdown":
        h = "".join(c["source"]).strip().splitlines()
        if h and h[0].startswith("#"):
            print("   " + h[0][:74])
