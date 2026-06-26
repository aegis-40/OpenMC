import fitz
PDF = "/mnt/d/projects/literature/OpenMC.pdf"
doc = fitz.open(PDF)
print(f"pages: {doc.page_count}\n")
print("===== FIRST PAGE (title/authors/abstract) =====")
print(doc.load_page(0).get_text()[:1800])

terms = ["depletion", "serpent", "2.4", "pincell", "pin cell", "pin-cell",
         "burnup", "107989", "Depletion capabilities", "predictor", "CRAM",
         "k_eff", "k-eff", "keff", "BEAVRS", "isotop"]
hits = {t: [] for t in terms}
for i in range(doc.page_count):
    txt = doc.load_page(i).get_text().lower()
    for t in terms:
        if t.lower() in txt:
            hits[t].append(i + 1)
print("\n===== keyword pages =====")
for t in terms:
    print(f"  {t:22s} -> {hits[t][:12]}")
