# Aegis-40 — Verification & Validation Summary (all executed benchmarks)

*Status 2026-07-04. Everything below is executed and archived in the Digital Appendix
(`docs/competition/digital-appendix/` → `Aegis40-Digital-Appendix.zip`) unless marked otherwise.
Toolchain: OpenMC 0.15.3, ENDF/B-VIII.0 continuous-energy, chain_endfb80_pwr.*

---

## 1. Experimental validation — OECD/NEA ICSBEP (measured critical experiments)

**LEU-COMP-THERM-008** (International Handbook of Evaluated Criticality Safety Benchmark
Experiments, NEA/NSC/DOC(95)03): low-enriched UO2 pin lattices in light water — the Aegis-40
physics class. Four cases run with the production toolchain (250×20k, σ ≈ 40–45 pcm);
benchmark-model k_eff = 1.0007 ± 0.0016.

| Case | k_calc ± σ | C − E (pcm) | vs combined 1σ (≈166 pcm) |
|---|---|---|---|
| case-1 | 1.00047 ± 0.00044 | −23 | 0.14 σ |
| case-2 | 1.00042 ± 0.00045 | −28 | 0.17 σ |
| case-5 | 1.00062 ± 0.00040 | −8 | 0.05 σ |
| case-7 | 0.99927 ± 0.00042 | −143 | 0.86 σ |

**Verdict: mean bias ≈ −50 pcm; every case within the handbook experimental uncertainty.**
This directly satisfies the Technical-Specification requirement that data from reliable sources
(IAEA / OECD-NEA) be used in the verification process. → appendix `0_icsbep_criticality/`.

## 2. Code-to-code validation — NuScale-like SMR core (published reference)

Open benchmark deck (Fridman, RODARE 2457; Ez-Aldeen et al., Zenodo 15231335), ENDF/B-VII.1 to
match the reference. Six control-rod states spanning ~19 400 pcm of rod worth:

| State | k (this work) | ref. Serpent | Δk (pcm) |
|---|---|---|---|
| all-rods-out | 1.02762 | 1.02768 | −6 |
| RE1 | 1.00741 | 1.00723 | +18 |
| RE2 | 1.00371 | 1.00313 | +58 |
| SH3 | 0.98953 | 0.98978 | −25 |
| SH4 | 0.99007 | 0.98971 | +36 |
| all-rods-in | 0.85711 | 0.85791 | −80 |

**Verdict: all states within ±80 pcm (≈2σ combined); control-rod worths on the parity line.**
Directly relevant: the benchmark core is geometrically the Aegis-40 class. → results in the
benchmark report + appendix.

## 3. Depletion — published validation, reproduced configuration

OpenMC's depletion capability is **validated by the published Romano et al., Ann. Nucl. Energy 152
(2021) 107989** OpenMC–Serpent comparison (BEAVRS 2.4 wt% pincell to 50 MWd/kg: k within ~20 pcm,
actinides/fission products within ~1 %). Our run **reproduces that exact case configuration**
(identical built-in model, burnup schedule, PredictorIntegrator, chain) and demonstrates
**repeatability** (independent-seed reruns agree within Monte-Carlo σ). At our statistics
(76–95 pcm/step) this is a configuration/reproducibility check — the quantitative code-to-code
agreement is the published result, cited. → appendix `2_depletion_benchmark/`.

## 4. Storage criticality — literature cross-check

Burnup-credit storage-rack methodology per Cabrera (2023); credited configurations
(record 29.6 GWd/tHM compositions): Boral k(95/95) = 0.837, Metamic 0.847 — both PASS ≤ 0.95,
two independent absorber materials agreeing within ~1 %Δk. Bounding ladder retained (fresh bare
1.363 → burnup-credit bare 1.148 → fresh-in-rack 1.107 → credited 0.837). Cross-checked against
the published SBF small-PWR envelope (Kim, Jung & Yoon, 2024). Formal OECD/NEA Burnup-Credit
Phase II bias derivation identified as the licensing-grade follow-up. → appendix
`3_storage_criticality/` + `6_waste_results/`.

## 5. Internal verification (correct-use evidence)

- **Cycle statics vs depletion:** independent full-core criticality calculations with injected
  depleted compositions reproduce the depletion k-curve to **0.5–70 pcm** at BOC/MOC/EOC.
- **Volume/geometry audit:** per-material heavy-metal inventories verified against independent
  geometric pin counts to <1 % (hard-error guard added against silent normalization faults).
- **Dual-correlation T-H:** DNBR reported with both W-3 (conservative, extrapolated) and
  Bowring-1972 (valid at low mass flux); Groeneveld-2006 LUT cross-check in the T-H package.
- **D4 symmetry folding** of pin-power maps; **×1.03 engineering allowance** on peaking (SSG-52).

## 6. Cited published validation (per accepted practice for established open-source codes)

ICSBEP full suite, C5G7 (OECD/NEA), BEAVRS (MIT-CRPG), VERA progression — OpenMC developers'
published validation; IAPWS-IF97 (steam properties); ANS-5.1 (decay heat); FRAPCON/Halden/IFPE
envelope data for fuel-performance screening. Mapping: `docs/competition/code-benchmark-matrix.md`.

---

## 7. Digital-Appendix compliance check — "one sample input per code + explanations"

| Code used in the analyses | Sample input in appendix? | Conditions/approach/results explained? |
|---|---|---|
| OpenMC (transport/criticality) | ✅ `1_core_transport/*.xml` + `0_icsbep_criticality/case-*/` | ✅ master README + per-folder README |
| OpenMC (depletion) | ✅ `2_depletion_benchmark/benchmark_depletion_pincell.py` (self-building input) | ✅ |
| Back-end fuel-cycle physics (Python, `src/aegis40/back_end`) | ✅ driver scripts in `3_storage_criticality/` + outputs in `6_waste_results/` | ✅ |
| Digital-twin ML (Python/scikit-learn) | ✅ `5_digital_twin/` (sweep + fit + exporter + site data) | ✅ |
| **OpenFOAM (T-H CFD)** | ⚠️ **in the T-H package (Aegis40_upload: `pin/`, `pin_coarse/`, `pin_fine/` case folders + tools) — must be MERGED into the final ZIP or uploaded alongside it** | ✅ in Aegis40_TH_report + T-H docs |
| T-H correlation stack (`mdnbr.py`, `cycle_mdnbr.py`, Groeneveld LUT) | ⚠️ same — in the T-H package | ✅ |
| Energy-cycle scripts (`thermo_cycle.py`, `soe_h2_schedule.py`, `tces_dh_balance.py`) | ⚠️ **not yet in the appendix — add a `7_energy_cycle/` folder (scripts + state-point CSV)** | partially (cycle docs) |
| Shielding (OpenMC, separate notebook) | ⚠️ separate `aegis40_shielding_FER.ipynb` — include or reference explicitly in §8.13 |  |

**Action items to be fully compliant:** (1) merge Adilbek's OpenFOAM case folders + T-H tools into
the final upload ZIP (or state in §8.13 that the T-H appendix is a second archive); (2) add
`7_energy_cycle/` with the three cycle scripts + `cycle_state_points.csv`; (3) one line in §8.13
referencing the shielding notebook. Everything else is already in place.
