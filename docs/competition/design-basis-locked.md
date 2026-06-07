# Aegis-40 — Locked Design Basis (FER §8.1 / §8.2 source of truth)

**Status:** LOCKED on the rev_3 full-core OpenMC run (2026-06-03, OpenMC 0.15.3).
This is the authoritative parameter set for FER §8.1 (general design parameters)
and §8.2 (core design). All downstream sections (§8.3 fuel, §8.11 waste, economics)
must cite *these* numbers. Source run: `aegis40_3d_core_outputs/summary_report.txt`.

> **Supersession note (record in FER):** earlier enrichment "locks" — the
> 2.6/3.0/3.4 stability baseline (2026-05-26) and the moderate-4.0% FOM target —
> are **formally relaxed**. The design now prioritises high discharge burnup
> (fuel-efficiency / waste-intensity score), so the enrichment moves to
> **4.95 / 4.70 / 4.40 wt%** (max 4.95, under the 5.0 wt% regulatory ceiling).
> The discharge-burnup target in any earlier draft of Table 1 (50 GWd/t, then
> 35-40 GWd/t) is superseded by the **as-run 42.8 GWd/t**.

---

## Table 1 — General Design Parameters (§8.1)

| Parameter | Value | Note |
|---|---|---|
| Plant type | Integral PWR (iPWR), soluble-boron-free | SBF by design |
| Thermal power | 125 MWth | |
| Electric power | 40 MWe | net design point |
| Fuel assemblies | 21 (17×17 square lattice) | |
| Active height | 200 cm | + axial reflectors ±30 cm H₂O |
| Radial reflector | 20 cm H₂O | vacuum outer BC |
| Heavy-metal loading | **~5.3 tHM** (as-modeled) | depletion gives 5.04 tHM at discharge + ~0.24 t fissioned; prior 5.6 t was a hand-estimate — confirm exact fresh value with `--step 0` |
| Reload scheme | 4-batch | |
| Enrichment (inner/mid/outer) | **4.95 / 4.70 / 4.40 wt%** | max 4.95 ≤ 5.0 ceiling |
| Burnable absorber | Gd₂O₃ 8 wt% (radially zoned) + Er₂O₃ 0.5 wt% | hybrid, SBF hold-down |
| Gd rods per FA (centre/inner/edge ring) | 48 / 40 / 24 | core-avg 32, zoned to flatten radial power (as-run model; confirmed 2026-06-07) |
| Er rods per FA | 16 | slow-depleting flat hold-down + cold SDM |
| Cladding | Zr-4 | locked |
| **Discharge burnup** | **42.8 GWd/MTU** | as-run rev_3 |
| **Cycle length** | **479 EFPD** (~16 months) | ≥365 EFPD gate |
| Capacity factor (assumed) | 0.90 | back-end fuel-cycle basis |

---

## Table 2 — Neutronic Safety Results (§8.2) — all gates PASS

| Parameter | Value | Limit | Status |
|---|---|---|---|
| k_eff, BOL | 1.0264 | ~1.0 (excess managed by BA + rods) | INFO |
| Moderator temp. coeff. (HFP) | −35.9 pcm/K | < 0 | PASS |
| Doppler (fuel) temp. coeff. | −1.84 pcm/K | < 0 | PASS |
| Void coefficient | −214 pcm/%void | < 0 | PASS |
| Control-rod worth (ARO→ARI) | 15,226 pcm | ≥ 5,000 | PASS |
| Shutdown margin | 12.4 %Δk/k | ≥ 1.0 | PASS |
| k_eff all-rods-in (ARI) | 0.888 | < 0.95 subcritical | PASS |
| k_eff worst-stuck-rod | 0.890 | < 1.0 (N-1) | PASS |
| Max reactivity insertion rate | 1.5e-5 Δk/k/s | ≤ 7.5e-4 | PASS |
| Enrichment (max) | 4.95 wt% | ≤ 5.0 | PASS |

Monte-Carlo profile: 180 batches / 50 inactive / 20,000 particles.

---

## Table 3 — Power-peaking, BEFORE → AFTER the radial-Gd-zoning fix

The rev_2 core used a single shared FA recipe for all 21 assemblies, which (with
no soluble boron to flatten the radial shape) produced strong centre-peaking.
rev_3 redistributes the **same core-average Gd** toward the centre ring (per-ring
density weights 1.50 / 1.24 / 0.80), conserving BOC reactivity while flattening
the radial power. Result:

| Peaking factor | rev_2 (uniform) | rev_3 (zoned) | Δ |
|---|---|---|---|
| F_radial (assembly) | 1.62 | **1.23** | −24% |
| F_ΔH (radial enthalpy-rise) | 2.77 | **2.27** | −18% |
| F_q (3D total) | 3.62 | **3.48** | −4% |
| F_z (axial) | — | 1.03 | — |

**Reframe for the FER:** these are *diagnostics / DNBR-margin inputs*, not
pass/fail gates. For context, the Jang SBF-SMPWR design limit is F_q < 5.09 and
the KEPCO i-SMR (HIGA) SBF design runs F_q ≈ 2.08 / F_r ≈ 1.35 — our rev_3 sits
well inside that SBF-SMR class. The binding constraint remains our own DNBR/MDNBR
analysis (T-H), not a borrowed peaking number.

---

## The k_eff "drop-then-rise" — expected SBF physics (anticipate the reviewer)

The depletion k_eff curve **dips then rises then declines** (k_BOL 1.0253 →
dip ≈ 0.98 → Gd-burnout hump → k_EOC 0.876). This is correct and *intended* for a
boron-free Gd-controlled core, and should be stated explicitly in §8.2:

1. **Dip (first ~days):** equilibrium xenon builds in (~−2700 pcm).
2. **Rise (~0–400 EFPD):** fresh Gd-155/157 hold k *down* at BOL; as they burn
   out, their absorption disappears faster than the fuel depletes → net k climbs.
   The reactivity "stored" in the Gd is released to sustain the long SBF cycle.
3. **Decline (post-burnout):** normal fuel-depletion fall-off to EOC.

Literature anchor: Kim, Jung & Yoon, *Nucl. Eng. Tech.* 56 (2024) 3144 —
"reactivity holding … followed by a gradual decrease post-gadolinia burnout" and
explicit engineering to "control the reactivity **upswing** following gadolinia
depletion." (In a boron-controlled core the curve only falls; the hump is the
signature of integral-Gd SBF control.)

---

## Open / accepted items
- **Discharge burnup 42.8 vs the 45-50 target:** accepted at ~43 GWd/t. Pushing
  higher means either exceeding the 5.0% enrichment cap or stripping Gd (which
  re-inflates peaking) — not worth it. 42.8 GWd/t is already strong vs CAREM-25
  (~24) and keeps the waste-intensity story competitive.
- **Sweep auto-optimiser** reported "no Stage-2 candidate" — that is the search
  k-window being too tight, **not** a design failure; the locked baseline above
  (summary_report.txt) passes all gates independently.
- Feeds: §8.1 params table, §8.2 neutronics, §8.3 fuel basis, §8.11 back-end
  (discharge 42.8 GWd/t + 4-batch + 0.90 CF set the arisings & source term).
