# Running `aegis40_neutronics_FER.ipynb` on a Windows PC with Docker

For Laziz (or anyone): how to run the fixed notebook on a fresh Windows machine
using Docker Desktop. Total setup ~30 min + the data download.

**What you need:** Docker Desktop (running), ~15 GB free disk, the two files from
this repo folder: `aegis40_neutronics_FER.ipynb` (the notebook) and this README.

---

## 1. Get the nuclear data (once)

Two items, ~2 GB total:

| Item | What | Where |
|---|---|---|
| Cross sections | **ENDF/B-VIII.0 HDF5** (`endfb-viii.0-hdf5/`, contains `cross_sections.xml`) | https://openmc.org/official-data-libraries/ |
| Depletion chain | **PWR chain for ENDF/B-VIII.0** (`chain_endfb80_pwr.xml`) | https://openmc.org/depletion-chains/ |

**Easier alternative:** copy both from Samira's laptop (WSL path `~/openmc_data/`)
— guaranteed byte-identical to what produced all previous results. Zip
`endfb-viii.0-hdf5/` + `chain_endfb80_pwr.xml` and transfer.

Put them on the new PC at, e.g., `C:\openmc_data\`:
```
C:\openmc_data\endfb-viii.0-hdf5\cross_sections.xml   (+ neutron/*.h5 ...)
C:\openmc_data\chain_endfb80_pwr.xml
```

## 2. Pull the OpenMC image and create the container

In PowerShell:

```powershell
docker pull openmc/openmc:latest          # official image, OpenMC + Python API
mkdir C:\aegis_run                        # results will be copied back here

docker run -it --name aegis40 `
  -p 8888:8888 `
  -v C:\openmc_data:/data:ro `
  -v C:\aegis_run:/out `
  openmc/openmc:latest bash
```

## 3. THE SPEED TRICK (same idea as our WSL-ext4 trick)

Windows bind-mounts (`/data`) are slow for the thousands of small `.h5` reads
OpenMC does. **Copy the library to the container's native (Linux) filesystem
first** — this alone is worth ~3-4x on library loading:

```bash
# inside the container
mkdir -p /root/openmc_data
cp -r /data/endfb-viii.0-hdf5 /root/openmc_data/       # ~2 min, once
cp /data/chain_endfb80_pwr.xml /root/openmc_data/
export OPENMC_CROSS_SECTIONS=/root/openmc_data/endfb-viii.0-hdf5/cross_sections.xml
export OPENMC_CHAIN_FILE=/root/openmc_data/chain_endfb80_pwr.xml
```

(The notebook's setup cell reads these env vars first, so no path editing needed.)

## 4. Install the Python extras + Jupyter

```bash
pip install jupyterlab matplotlib pyyaml pandas
```

## 5. Threads + run location

```bash
export OPENMC_THREADS=<PHYSICAL cores, e.g. 32>   # notebook reads this
mkdir -p /root/work && cd /root/work              # run on native FS, NOT /out
cp /out/aegis40_neutronics_FER.ipynb .            # put the notebook in C:\aegis_run first
jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

Open the printed `http://127.0.0.1:8888/...` link in the Windows browser.

> Outputs land in `/root/work/aegis40_neutronics_outputs/` (native FS = fast
> statepoint writes). Copy back to Windows when done:
> `cp -r /root/work/aegis40_neutronics_outputs /out/`

## 6. Run order in the notebook

1. **Cells top-to-bottom through section 7** (setup → config → materials →
   geometry → core map). Smoke-check: the config cell must print
   `16 control-rod clusters`, `Gd2O3 6 wt%x20 + Er2O3 0.75 wt%x16`, `1-batch`.
2. **Quick sanity run first**: set `STAT = STAT_FAST` in the config cell and run
   the BOC k-eff cell (~2 min). Expect k ≈ 1.15. Then set back `STAT = STAT_FINAL`.
3. **Depletion**: run `calc_depletion()` (section 8).
   - Watch the first lines: it must print `note: 'UO2_3.6' not in geometry ->
     excluded from depletion` and **NO** `WARNING: volume fallback` lines.
     A fallback warning = STOP, something regressed (it will actually hard-error now).
   - STAT_FINAL at 32 threads: roughly 6-12 h (36 steps; the chain solver is a
     fixed per-step cost regardless of statistics).
4. **After depletion**: `calc_cycle_peaking()` (BOC/MOC/EOC F_dH table + radial
   maps + axial shapes), `calc_burnup_map()` (EOC burnup distribution),
   `calc_rea_envelope()` (REA <1$ check), then sections 10-11 (consolidated
   tables / safety file).

## 7. Practical notes

- **Don't let Windows sleep** — Docker Desktop pauses the VM and the depletion
  cannot resume mid-run (it restarts from step 0). Power settings → sleep = Never.
- If the container is stopped: `docker start -ai aegis40` (files in `/root` persist).
- Headless alternative (no browser, survives closing the terminal):
  ```bash
  cd /root/work && nohup jupyter nbconvert --to notebook --execute \
      --ExecutePreprocessor.timeout=-1 aegis40_neutronics_FER.ipynb \
      --output executed.ipynb > run.log 2>&1 &
  ```
  …but note the notebook's analysis calls after depletion are commented — for a
  fully headless run, uncomment `calc_depletion()` etc. first, or run interactively.
- Version pin: results to date are OpenMC **0.15.3** / ENDF/B-VIII.0. If the
  `latest` image is newer and k shifts by more than ~50 pcm, pin the image:
  `docker pull openmc/openmc:v0.15.3` (if available) and re-check.

## 8. What "success" looks like

- k_BOL ≈ **1.153–1.154** (matches the audited BOC).
- k(BU) shows the Gd hump then a smooth decline; **edge assemblies stay alive**
  in the MOC/EOC radial maps (no 0.05 values — that was the old volume bug).
- `cycle_peaking` table: F_dH ≤ 1.65 / F_q ≤ 2.32 at all three states = PASS.
- B1 (k=1 crossing) → the corrected cycle length & once-through discharge burnup;
  the summary also prints the LRM 3-batch equilibrium option.
