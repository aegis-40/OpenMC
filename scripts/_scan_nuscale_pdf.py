import fitz, re
PDF = "/mnt/d/Engineering/optimization research/NuScale.pdf"
doc = fitz.open(PDF)
print(f"pages: {doc.page_count}")

pats = ["thm", "mtu", " tu", "metric ton", "heavy metal", "specific power",
        "power density", "kw/kg", "w/g", "kgu", "kg u", "uranium mass",
        "fuel loading", "fuel mass", "loading", "gwd", "burnup", "burn-up",
        "linear heat", "mwd/kg", "tonne"]
for i in range(doc.page_count):
    t = doc.load_page(i).get_text()
    tl = t.lower()
    for p in pats:
        idx = 0
        while True:
            k = tl.find(p, idx)
            if k < 0:
                break
            ctx = t[max(0, k-55):k+55].replace("\n", " ")
            print(f"p{i+1} [{p}]: ...{ctx}...")
            idx = k + len(p)
