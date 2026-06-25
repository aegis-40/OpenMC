# NuScale-like Core Neutronics Benchmark — Aegis-40 OpenMC reproduction

**Purpose (FER §8.13 V&V).** Code-to-code validation of the Aegis-40 OpenMC toolchain on a
**NuScale-like, soluble-boron-free, Gd₂O₃ core** — the design anchor for Aegis-40 (37 FA, 17×17,
2.0 m). Confirms our transport + control-rod modelling reproduces a published Monte-Carlo reference.

## Benchmark source
- **Definition + reference solution:** E. Fridman, Y. Bilodid, V. Valtavirta, *"Definition of the
  neutronics benchmark of the NuScale-like core,"* Nucl. Eng. Technol. (2023); dataset **RODARE 2457**
  (`https://rodare.hzdr.de/record/2457`) — Serpent reference k_eff + material compositions.
- **OpenMC deck:** A. Ez Aldeen et al., *"Simulation of NuScale-Like SMR Benchmark with OpenMC,"*
  J. Nucl. Eng. **6**, 44 (2025); inputs at **Zenodo 15231335**.

## Our run
- Library: **ENDF/B-VII.1** (matches the benchmark; B₄C carbon C12+C13 → C0 for the VII.1 HDF5 set).
- Statistics: 100 batches × 80 k particles (σ ≈ 30–45 pcm) — vs the paper's 2700 × 1 M HPC run.
- Driver: `scripts/_run_nuscale_states.py`; results `nuscale_states_results.json`.

## Result (all-rods-out → all-rods-in)

| State | Aegis-40 k_eff ± σ | Serpent ref | Δk (pcm) | our CRW | ref CRW |
|---|---|---|---|---|---|
| ARO | 1.02762 ± 34 | 1.02768 | −6 | — | — |
| RE1 | 1.00741 ± 36 | 1.00723 | +18 | −1953 | −1975 |
| RE2 | 1.00371 ± 44 | 1.00313 | +58 | −2318 | −2381 |
| SH3 | 0.98953 ± 31 | 0.98978 | −25 | −3746 | −3726 |
| SH4 | 0.99007 ± 34 | 0.98971 | +36 | −3691 | −3733 |
| ARI (SCRAM) | 0.85711 ± 37 | 0.85791 | −80 | −19359 | −19255 |

**k_eff agrees within −80…+58 pcm; control-rod worths within ~0.5–3 %** (the −19,255 pcm SCRAM worth
to +0.5 %). Figures: `nuscale_keff_states.png`, `nuscale_crw_parity.png`.
