# Digital Appendix - Safety neutronics suite (SDM, EBIS, SFP, MSLB, peaking, REA)

The Chapter 8.5-8.6 safety-neutronics evidence: rod worth / shutdown margin, emergency boron (EBIS), spent-fuel-pool, main-steam-line-break re-criticality, cycle peaking and rod-ejection envelope.

**Design basis.** Aegis-40 basis: 125 MWth / 40 MWe integral PWR, soluble-boron-free, natural circulation; 37 fuel assemblies, 17x17, 2.0 m active height; in-out zoned 4.0-4.95 wt% U-235; integral 20 Gd rods/FA @ 6 wt% Gd2O3 + 16 Er rods/FA @ 0.75 wt% Er2O3; 16 B4C (90% B-10) control-rod assemblies; once-through cycle, ~29.6 GWd/tHM discharge, ~2224 EFPD. OpenMC 0.15.3, ENDF/B-VIII.0.

## Sample input (conditions)
`code/aegis40_safety_neutronics.py` (suite driver, `run_resumable.sh` wrapper) plus `code/run_cycle_peaking.py` and `code/run_rea_envelope.py`. Cases and acceptance targets set in-script.

## Approach
Each credited shutdown function evaluated with an adjusted eigenvalue k_adj = k_mean + 2sigma + 0.005 bias allowance; peaking from BOC/MOC/EOC statics; REA from ejected-rod worth envelope.

## Outputs obtained
`outputs/safety_neutronics_results.json` + plots (EBIS boron curve, MSLB cooldown). Every credited function clears its k_adj target with margin; MOC peaking closed via COLR (F_dH 1.75).

## How to reproduce
```bash
`bash code/run_resumable.sh` (self-resuming).
```

## Verification & validation (reliable sources)
NuScale-like SMR core benchmark (six rod states within +/-80 pcm of the published Serpent reference) validates the rod-worth/criticality capability; complemented by ICSBEP (folder 0).

---
*Layout: `code/` (scripts/notebook), `inputs/` (sample input), `outputs/` (sample results),
`evidence/` (V&V material), `figures/` (plots). Raw multi-GB statepoint/depletion `.h5`
artifacts are regenerable from these inputs and are not shipped.*
