import fitz
papers = {
    "JNE": "/mnt/d/projects/literature/jne-06-00044-v2.pdf",
    "JANG": "/mnt/d/projects/literature/Intl J of Energy Research - 2020 - Jang - "
            "Conceptual design of long‐cycle boron‐free small modular "
            "pressurized water.pdf",
}
terms = ["boron-free", "boron free", "smr", "small modular", "k-eff", "keff",
         "k_eff", "k-inf", "cycle length", "efpd", "enrichment", "gadolinium",
         "gd2o3", "er2o3", "erbium", "17x17", "assembl", "mwth", "mw th",
         "peaking", "coefficient", "burnup", "openmc", "mcnp", "serpent",
         "casmo", "pin pitch", "active", "wt%"]
for tag, path in papers.items():
    try:
        d = fitz.open(path)
    except Exception as e:
        print(f"\n### {tag}: OPEN FAILED {e}"); continue
    print("\n" + "=" * 30 + f" {tag}  ({d.page_count} pp) " + "=" * 30)
    print(d.load_page(0).get_text()[:1400])
    hits = {t: [] for t in terms}
    for i in range(d.page_count):
        tl = d.load_page(i).get_text().lower()
        for t in terms:
            if t in tl:
                hits[t].append(i + 1)
    print("  --- key terms (pages) ---")
    for t in terms:
        if hits[t]:
            print(f"   {t:16s} {hits[t][:8]}")
