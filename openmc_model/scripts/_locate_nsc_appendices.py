import fitz, re
doc = fitz.open("/mnt/d/projects/literature/nsc-doc2013-1.pdf")
N = doc.page_count

# locate appendix headers
for i in range(N):
    t = doc.load_page(i).get_text()
    head = t[:120].replace("\n", " ")
    if re.search(r"Appendix\s+[ABC]\b", t[:400]):
        print(f"[APX HEADER] p{i+1}: {head[:100]}")

# flag pages with spec / history / measured signatures
sig = {
    "geom(g/cm,pitch,clad,radius)": ["pitch", "cladding", "clad ", "pellet", "radius", "guide tube"],
    "matl(atom dens,ppm,density)": ["atom/b", "atoms/b", "g/cm", "ppm", "number densit", "boron"],
    "history(GWd,EFPD,cycle,power)": ["gwd", "efpd", "mwd", "cycle 1", "cycle 2", "specific power", "cooling"],
    "measured(SFCOMPO,SF97,exp)": ["sf97", "sfcompo", "measured", "experimental value", "takahama"],
}
print("\n--- page signatures ---")
for i in range(N):
    tl = doc.load_page(i).get_text().lower()
    tags = [k for k, ws in sig.items() if sum(w in tl for w in ws) >= 2]
    if tags:
        print(f"p{i+1}: {', '.join(tags)}")
