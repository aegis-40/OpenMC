# Aegis-40 — STAT_FINAL Neutronics Results (record run, fixed volumes)

**Run:** 2026-07-03, OpenMC 0.15.3, ENDF/B-VIII.0, STAT_FINAL (400 batches / 80 inactive / 50 000
particles ≈ 16 M active histories, σ(k) ≈ 22–26 pcm), 32 threads (Laziz).
**Notebook:** `openmc_model/aegis40_neutronics_FER.ipynb` (cleaned + audited; ring-keyed depletion
volumes — BUGFIX 2026-07-02 verified in-run: all zones burn physically, no fallback warnings).
**Config (locked):** 37 FA · 17×17 · 2.0 m · ring enrichment 4.95/4.7/4.4/4.0 wt% · Gd₂O₃ 6 wt%×20
(ring-graded 1.65→0.68) · Er₂O₃ 0.75 wt%×16 · **16 CRA, 90 % enriched B-10** · once-through ·
HM = 9.39 tHM · 125 MWth.
**Outputs:** `openmc_model/aegis40_neutronics_outputs (2)/aegis40_neutronics_outputs/`
**Status:** ✅ final unless marked ⏳ (pipeline completing 2026-07-04).

---

## 1. Core static parameters (all PASS)

| Parameter | Value | Limit | Status |
|---|---|---|---|
| k_eff (BOL, HFP, ARO) | 1.1503 ± 26 pcm | — | INFO |
| MTC (full power) | −26.87 pcm/K | < 0 | PASS |
| DTC (Doppler) | −1.91 pcm/K | < 0 | PASS |
| Void coefficient | −173.2 pcm/%void | < 0 | PASS |
| Control-rod bank worth (16 CRA, ARO→ARI) | 21 509 pcm | ≥ 5 000 | PASS |
| Shutdown margin (hot, all rods in / ARI) | **7.85 % Δk/k (signed)** | ≥ 1.0 % | PASS |

> **Basis note.** k_eff, MTC, DTC, void and the fuel-cycle values above are from this 3 July full-power run (fuel 900 K). The **control-rod worth and shutdown margin rows are evaluated at isothermal hot zero power** (fuel = moderator = 556 K) in the safety-neutronics suite, which is the physically consistent state for a rods-in condition — the reactor is shut down, so the fuel is not at full-power temperature. Evaluating the same quantities with fuel held at 900 K gives 21,479 pcm and 7.68 %; the ~590 pcm difference is Doppler between the two states, not a discrepancy.

| Max reactivity insertion rate | 1.5×10⁻⁵ dk/k/s | ≤ 7.5×10⁻⁴ | PASS |
| Peak enrichment | 4.95 wt% | ≤ 5.0 | PASS |

## 2. Fuel cycle (once-through) — corrected record values

| Quantity | Value |
|---|---|
| Cycle length B1 (k = 1) | **2 224 EFPD = 6.09 FPY** |
| Discharge burnup (core-avg) | **29.6 GWd/tHM** |
| Depletion horizon computed | 2 510 EFPD / 33.4 GWd/tHM (k_end 0.968) |
| Gd/Er burnout hump | peak k = 1.135 at ~13.5 GWd/t — **below BOC 1.150 → BOC remains the bounding shutdown state** |
| LRM 3-batch equilibrium option | cycle ≈ 1 112 EFPD, discharge ≈ 44.4 GWd/tHM |
| Per-assembly burnup at EOC | 21 (edge) → **42 GWd/t (peak)** ≪ 62 GWd/MTU qualified limit |

## 3. Cycle peaking — BOC / MOC / EOC (injection statics, k-consistency verified ≤ 51 pcm)

| State | BU (GWd/t) | k | F_FA | **F_ΔH** (≤1.65) | F_z | **F_q** (≤2.32) | Verdict |
|---|---|---|---|---|---|---|---|
| BOC (STAT_FINAL) | 0.0 | 1.1502 | 1.238 | **1.513** | 1.280 | **1.937** | **PASS** |
| MOC hump (STAT_FINAL) | 13.5 | 1.1358 | 1.571 | **1.729** | 1.408 | **2.435** | **exceeds generic limit ~5 %** |
| EOC (STAT_FINAL) | 30.8 | 0.9910 | 1.302 | **1.497** | 1.417 | **2.121** | **PASS** |

F_ΔH includes the ×1.03 engineering allowance (SSG-52 3.18(f)); pin map D4-folded.

### MOC finding — honest statement and closure path
The Gd-burnout hump (~13.5 GWd/t) genuinely exceeds the **generic W-4-loop LCO limits**
(F_ΔH 1.73 vs 1.65; F_q 2.44 vs 2.32). This is a converged physical result, not statistics.
Closure (in order of preference):

1. **Design-specific COLR limit via MDNBR (primary — action: T-H/Adilbek).** At 13 kW/m core-average
   LHR, scaling the BOC MDNBR (~1.5+ at F_ΔH 1.51) to F_ΔH 1.73 indicates MDNBR ≈ 1.4 > 1.30.
   If the hot-channel calculation confirms MDNBR ≥ 1.30 at F_ΔH = 1.75, the FER adopts a
   design-specific COLR limit F_ΔH ≤ 1.75 (NUREG-1431 practice) → MOC = PASS with documented basis.
2. **Rod-program flattening (operational backup).** Shallow insertion of the central regulating
   group at MOC clips the central hump; state as an operating-procedure surveillance requirement.
   (Not yet quantified by simulation — optional 1-h static if numbers are wanted.)

## 4. REA envelope (SRP 15.4.8)

Ejected worth of the most-central CRA from full insertion at HFP: **783 ± 84 pcm = 1.20 $**
(β_eff = 650 pcm) → above the 1 $ prompt-criticality screen **for the full-insertion state**.

**FER statement (draft):** *"At power the Aegis-40 SBF core operates essentially all-rods-out (no
soluble-boron bite); power-dependent insertion limits (PDIL) administratively restrict inserted
worth so that the ejected-rod worth at power remains < 1 $. The bounding full-insertion single-rod
worth (1.20 $) applies only to startup/shutdown states, which are addressed by the standard
startup-REA analysis envelope at low power and by the de-energised (gravity-hold) CRDM state at
shutdown."*

## 5. Discharge inventory & safeguards (whole core at EOC step, 30.8 GWd/t)

| | Value |
|---|---|
| U-235 residual | 151 kg (from 415 kg loaded) |
| Total Pu | **78.1 kg** |
| Pu vector | Pu-238 1.6 / **Pu-239 61.6** / Pu-240 21.6 / Pu-241 11.6 / Pu-242 3.5 % |
| Grade | **reactor-grade** (≪ 93 % weapons threshold); fissile Pu 57.3 kg |
| Waste intensity | **4.40 tHM/TWhe** (9.39 t / 2.135 TWhe per once-through life) |

**§8.11 refresh — DONE (2026-07-04, vs the record H5):**

| Quantity | Record value |
|---|---|
| Decay heat at shutdown (rigorous) | **7.94 MW** (10.3 kW at ~10 yr) |
| Waste intensity | **4.40 tHM/TWhe — ~32 % below CAREM-25 (6.43)** |
| Storage rack k(95/95), burnup-credited | **Boral 0.837 / Metamic 0.847 — PASS** (bounding diagnostics retained) |
| Safeguards | spent-fuel U-235 1.52 wt%; SQ(core) 10.2; Pu heat 14.8 W/kg; plots refreshed |

Outputs: `docs/competition/waste/` + `docs/competition/safeguards/` (CSV/MD/plots).
*(Note: `run_waste_intensity.py` carried hardcoded rev_3 constants — corrected to the record basis
9.386 t / once-through / 2 224 EFPD / 29.6 GWd/t and rerun on 2026-07-04.)*

## 6. Figure index (all fixed-physics, in `docs/competition/digital-appendix/figures/`)

`fig_8.2-2` k(BU) final · `fig_8.2-5a` radial BOC/MOC/EOC · `fig_8.2-5b` axial shapes ·
`fig_8.2-5c` per-assembly burnup · `flux_maps_boc` · `core_loading_map` · `core_map` ·
`depletion_baseline` · `power_distribution_3d_boc` · `absorber_inventory` · `axial_verification` ·
geometry renders · FA diagram. *(Corrupted-era figures quarantined in
`.../plots/_OBSOLETE_corrupted_run/` — do not use.)*
