import fitz
doc = fitz.open("/mnt/d/Engineering/optimization research/NuScale.pdf")
for p in [11, 12, 13, 14]:
    print("\n" + "#" * 24 + f" PAGE {p} " + "#" * 24)
    print(doc.load_page(p - 1).get_text()[:4200])
