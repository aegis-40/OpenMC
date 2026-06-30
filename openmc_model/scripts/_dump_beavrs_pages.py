import fitz
PDF = "/mnt/d/Engineering/SMR research/literature/BEAVRS_2.0.2_spec.pdf"
doc = fitz.open(PDF)
for p in [6, 12, 47, 57, 58, 88]:
    print("\n" + "=" * 30 + f" PAGE {p} " + "=" * 30)
    print(doc.load_page(p - 1).get_text()[:2600])
