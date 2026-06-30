import fitz
doc = fitz.open("/mnt/d/projects/literature/jne-06-00044-v2.pdf")
for p in [2, 5, 6, 7, 8]:
    print("\n" + "#" * 22 + f" PAGE {p} " + "#" * 22)
    print(doc.load_page(p - 1).get_text()[:3600])
