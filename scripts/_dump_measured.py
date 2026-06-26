import fitz
doc = fitz.open("/mnt/d/projects/literature/nsc-doc2013-1.pdf")
for p in [49, 50, 51, 126]:
    print("\n" + "#" * 22 + f" PAGE {p} " + "#" * 22)
    print(doc.load_page(p - 1).get_text()[:5500])
