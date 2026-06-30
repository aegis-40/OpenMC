import fitz
doc = fitz.open("/mnt/d/projects/literature/nsc-doc2013-1.pdf")
for p in [17, 18, 23, 111, 112, 113, 114, 115, 116, 117, 118]:
    print("\n" + "#" * 24 + f" PAGE {p} " + "#" * 24)
    print(doc.load_page(p - 1).get_text()[:5000])
