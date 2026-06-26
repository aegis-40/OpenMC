import fitz
PDF = "/mnt/d/projects/literature/Depletion capabilities.pdf"
doc = fitz.open(PDF)
print(f"pages: {doc.page_count}")
print("===== TITLE/AUTHORS =====")
print(doc.load_page(0).get_text()[:900])

# locate the pincell benchmark section
key = ["pin cell", "pincell", "pin-cell"]
pin_pages = []
for i in range(doc.page_count):
    t = doc.load_page(i).get_text().lower()
    if any(k in t for k in key):
        pin_pages.append(i + 1)
print("\npincell mentioned on pages:", pin_pages)

# dump the pincell-section pages so we can see the actual reference numbers
for p in pin_pages:
    print("\n" + "=" * 26 + f" PAGE {p} " + "=" * 26)
    print(doc.load_page(p - 1).get_text()[:3000])
