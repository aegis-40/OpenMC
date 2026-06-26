import sys
try:
    import fitz  # PyMuPDF
except Exception as e:
    print("NO_FITZ", e); sys.exit(0)

PDF = "/mnt/d/Engineering/SMR research/literature/BEAVRS_2.0.2_spec.pdf"
doc = fitz.open(PDF)
print(f"pages: {doc.page_count}")

terms = ["2.4", "enrich", "density", "pellet", "radius", "pitch", "clad",
         "depletion", "isotop", "pin cell", "pin-cell", "pincell",
         "boron", "letdown", "rod worth", "burnup", "S(a", "thermal scattering"]
hits = {t: [] for t in terms}
for i in range(doc.page_count):
    txt = doc.load_page(i).get_text().lower()
    for t in terms:
        if t.lower() in txt:
            hits[t].append(i + 1)
for t in terms:
    pp = hits[t][:14]
    print(f"  {t:20s} -> pages {pp}")
