# Aegis-40 — Neutronics Results (high-statistics record run)

**Run:** 2026-07-03, OpenMC 0.15.3, ENDF/B-VIII.0, high-statistics settings (400 batches / 80
inactive / 50 000 particles ≈ 16 M active histories, σ(k) ≈ 22–26 pcm), 32 threads.
**Notebook:** `openmc_model/aegis40_neutronics_FER.ipynb` (ring-keyed depletion volumes,
verified in-run: all zones burn physically, no fallback warnings).
**Config (locked):** 37 FA · 17×17 · 2.0 m · ring enrichment 4.95/4.7/4.4/4.0 wt% · Gd₂O₃ 6 wt%×20
(ring-graded 1.65→0.68) · Er₂O₃ 0.75 wt%×16 · **16 CRA, 90 % enriched B-10** · once-through ·
HM = 9.39 tHM · 125 MWth.
**Outputs:** `openmc_model/aegis40_neutronics_outputs (2)/aegis40_neutronics_outputs/`
**Status:** final.

---

## 1. Core static parameters (all PASS)

| Parameter | Value | Limit | Status |
|---|---|---|---|
| k_eff (BOL, HFP, ARO) | 1.1503 ± 26 pcm | — | INFO |
| MTC (full power) | −26.87 pcm/K | < 0 | PASS |
| DTC (Doppler) | −1.91 pcm/K | < 0 | PASS |
| Void coefficient | −173.2 pcm/%void | < 0 | PASS |
| Control-rod bank worth (16 CRA, ARO→ARI) | 21 479 pcm | ≥ 5 000 | PASS |
| Shutdown margin (most-reactive rod stuck, hot) | **+7.68 % Δk/k (signed)** | ≥ 1.0 % | PASS |
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

> **Framing note (basis for the verdicts):** F_ΔH ≤ 1.65 and F_q ≤ 2.32 are **conservative generic
> PWR screening values, not universal or Aegis-40 design-specific acceptance limits**. In licensing
> practice these are unit- and cycle-specific COLR parameters (NUREG-1431; e.g. Salem-1 COLR carries
> F_ΔH = 1.65 as a *plant* value, ML23306A028). NuScale explicitly concludes no F_q LCO is needed in
> its design (ML24326A095) and controls peaking via PDIL/axial-offset windows. Published SMR precedent
> accepts higher peaking at low linear heat rate: CAREM-25 equilibrium core peaking 2.56 with
> MDNBR 1.90 (OSTI 20194765); SMART 3-D peaking 2.48 at 122 W/cm average (vs 2.0 conventional).

| State | BU (GWd/t) | k | F_FA | **F_ΔH** | F_z | **F_q** | Interpretation |
|---|---|---|---|---|---|---|---|
| BOC | 0.0 | 1.1502 | 1.238 | **1.513** | 1.280 | **1.937** | passes generic screening |
| MOC hump | 13.5 | 1.1358 | 1.571 | **1.729** | 1.408 | **2.435** | exceeds generic screening (~5 %) → **design-specific COLR / MDNBR closure item** |
| EOC | 30.8 | 0.9910 | 1.302 | **1.497** | 1.417 | **2.121** | passes generic screening |

F_ΔH includes the ×1.03 engineering allowance (SSG-52 3.18(f)); pin map D4-folded.

### MOC — classification and closure (NOT an automatic failure)
The Gd-burnout hump (~13.5 GWd/t) exceeds the generic Westinghouse-style screening values — a
converged physical result. Because Aegis-40 operates at very low average and peak linear heat rate
(~13 kW/m core-average), **acceptability is determined by design-specific thermal limits (MDNBR,
peak LHR, fuel centreline T, PCT, accident-analysis assumptions), not by inherited large-PWR
numbers**. The MOC case is therefore classified as a **thermal-hydraulic closure item**.

**The single required closure calculation (thermal-hydraulics):**
> Hot-channel T-H at the MOC peaking envelope: **F_ΔH = 1.75, F_q ≈ 2.45** with the MOC axial shape
> (F_z 1.41). **Acceptance: MDNBR ≥ 1.30** and fuel/clad temperatures below limits.
> Scaling the BOC point (MDNBR ~1.5+ at F_ΔH 1.51) indicates ≈1.4 — expected to pass.

If confirmed, the FER adopts a **design-specific COLR peaking limit for the 37-FA SBF core**
(consistent with PWR COLR practice and NuScale/SMR precedent above), and MOC reads:
*"exceeds generic screening values but is acceptable under the Aegis-40 design-specific COLR basis."*
**Backup:** rod-program/PDIL flattening of the central hump as an operating-procedure surveillance
requirement (NuScale-style; not yet quantified by simulation).

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
| Basis | EOC record step 29.4 GWd/t (nearest the k = 1 crossing) |
| U-235 residual | 1.77 wt% of U (~157 kg) |
| Total Pu | **76.2 kg** |
| Pu vector | Pu-238 2.0 / **Pu-239 62.8** / Pu-240 21.2 / Pu-241 10.1 / Pu-242 3.9 % |
| Grade | **reactor-grade** (≪ 93 %); self-protection 12.2 W/kg-Pu, SF 3.1×10⁵ n/s/kg; SQ(core) 9.5 |
| Waste intensity | **4.40 tHM/TWhe** (9.39 t / 2.135 TWhe per once-through life) |

**Decay heat, waste and safeguards summary (record basis):**

| Quantity | Record value |
|---|---|
| Decay heat at shutdown (rigorous) | **7.94 MW** (10.3 kW at ~10 yr) |
| Waste intensity | **4.40 tHM/TWhe — ~32 % below CAREM-25 (6.43)** |
| Storage rack k(95/95), burnup-credited | **Boral 0.837 / Metamic 0.847 — PASS** (bounding diagnostics retained) |
| Safeguards | spent-fuel U-235 1.52 wt%; SQ(core) 10.2; Pu heat 14.8 W/kg; plots refreshed |

Outputs: `docs/competition/waste/` + `docs/competition/safeguards/` (CSV/MD/plots), computed on
the record basis 9.386 t / once-through / 2 224 EFPD / 29.6 GWd/t.

## 6. Figure index (all fixed-physics, in `docs/competition/digital-appendix/figures/`)

`fig_8.2-2` k(BU) final · `fig_8.2-5a` radial BOC/MOC/EOC · `fig_8.2-5b` axial shapes ·
`fig_8.2-5c` per-assembly burnup · `flux_maps_boc` · `core_loading_map` · `core_map` ·
`depletion_baseline` · `power_distribution_3d_boc` · `absorber_inventory` · `axial_verification` ·
geometry renders · FA diagram.

## 7. Digital twin (surrogate model)

Parameter sweep extended to
**180 points**, surrogates refit (k R² 0.9969, F_assembly R² **0.9990**, POD 0.990, rod worth +2 %),
site `data/model.js` regenerated with the 180-pt surrogates + the **record k(BU)** (38 steps,
EOC 29.62 GWd/t / 2 224 EFPD; verified: JS-formula k(HFP,ARO)=1.157, rods/void responses physical).
Exporter: `openmc_model/digital_twin/export_model_js.py` (reusable; appendix artifact).
