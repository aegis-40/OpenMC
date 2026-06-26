import fitz
doc = fitz.open("/mnt/d/projects/literature/OpenMC.pdf")
for p in [3, 7]:
    print("\n" + "=" * 28 + f" PAGE {p} " + "=" * 28)
    print(doc.load_page(p - 1).get_text()[:2400])
