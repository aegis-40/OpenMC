import fitz
doc = fitz.open("/mnt/d/projects/literature/nsc-doc2013-1.pdf")
for p in [9, 14, 15, 16, 20, 25]:
    print("\n" + "=" * 26 + f" PAGE {p} " + "=" * 26)
    print(doc.load_page(p - 1).get_text()[:2800])
