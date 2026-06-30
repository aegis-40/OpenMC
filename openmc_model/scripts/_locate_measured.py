import fitz, re
doc = fitz.open("/mnt/d/projects/literature/nsc-doc2013-1.pdf")
N = doc.page_count

# find appendix headers (A/B/C) appearing as a section title near top of page
for i in range(N):
    t = doc.load_page(i).get_text()
    m = re.search(r"Appendix\s+([ABC])\s*[:\-]", t)
    if m:
        line = t[m.start():m.start()+90].replace("\n", " ")
        print(f"[APX {m.group(1)}] p{i+1}: {line}")

# find pages that look like measured/experimental data tables
print("\n--- candidate measured-data pages ---")
for i in range(N):
    tl = doc.load_page(i).get_text().lower()
    score = 0
    for w in ["experimental", "measure", "sfcompo", "uncertaint", "mg/g", "g/tu",
              "atom ratio", "c/e", "exp."]:
        if w in tl:
            score += 1
    nuc = sum(x in tl for x in ["nd-148", "nd148", "cs-137", "u-235", "pu-239", "pu-240"])
    if score >= 2 and nuc >= 1:
        print(f"p{i+1}: data-score={score} nuclide-hits={nuc} :: "
              + doc.load_page(i).get_text()[:80].replace(chr(10), ' '))
