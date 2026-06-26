import json, re
nb = json.loads(open("/home/samira/fer4.ipynb", "rb").read().decode("utf-8-sig", "replace"))
ci = 0
RUN = re.compile(r"_run_dir\(|_run_model\(|build_core\(|run_core_depletion\(|"
                 r"plot_core|\.run\(|\.integrate\(|run_sweep|_keff\(|results\[")
for c in nb["cells"]:
    if c["cell_type"] == "markdown":
        h = "".join(c["source"]).strip().splitlines()
        if h:
            print(f"        md: {h[0][:64]}")
        continue
    src = "".join(c["source"])
    top = [l for l in src.splitlines()
           if l[:1] not in (" ", "\t")
           and not l.lstrip().startswith(("def ", "class ", "import ", "from ", "@", "#"))]
    toptxt = "\n".join(top)
    flag = "RUN " if RUN.search(toptxt) else "def "
    # first signal line
    first = next((l.strip() for l in src.splitlines()
                  if l.strip() and not l.strip().startswith("#")), "")
    # which run-call appears at top level
    hits = ",".join(sorted(set(re.findall(
        r"_run_dir|_run_model|build_core|run_core_depletion|plot_core|\.run|\.integrate|_keff|results\[",
        toptxt))))
    print(f"#{ci:<2}[{flag}] {first[:54]:54} | top-calls: {hits}")
    ci += 1
