import fitz
PDF = "/mnt/d/projects/literature/nsc-doc2013-1.pdf"
doc = fitz.open(PDF)
print(f"pages: {doc.page_count}\n")
print("===== FIRST 2 PAGES =====")
print(doc.load_page(0).get_text()[:1500])
print("----")
print(doc.load_page(1).get_text()[:1200])

terms = ["benchmark", "criticalit", "experiment", "measured", "k-eff", "keff",
         "k_eff", "enrich", "wt%", "PWR", "BWR", "MOX", "burnup", "depletion",
         "pin", "assembly", "lattice", "ICSBEP", "LEU", "uncertainty", "boron",
         "reactivity", "doppler", "void", "spent fuel", "isotop"]
hits = {t: [] for t in terms}
for i in range(doc.page_count):
    t = doc.load_page(i).get_text().lower()
    for term in terms:
        if term.lower() in t:
            hits[term].append(i + 1)
print("\n===== keyword pages (first 10 each) =====")
for term in terms:
    print(f"  {term:14s} -> {hits[term][:10]}")
