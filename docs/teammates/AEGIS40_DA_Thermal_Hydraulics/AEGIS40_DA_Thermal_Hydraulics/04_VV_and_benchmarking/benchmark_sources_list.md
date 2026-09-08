# Benchmark & data sources (reliability-ranked)

## IAEA
- **IAEA-TECDOC-1203**, *Thermohydraulic relationships for advanced water cooled
  reactors*, 2001 — CHF look-up-table correction factors K1–K8 (Table 3.3) used in the
  Groeneveld MDNBR corroboration.
- **IAEA SSG-52**, *Design of the Reactor Core for Nuclear Power Plants* — engineering
  allowance on F_ΔH (3.18(f)).

## US NRC (licensing-grade)
- **NuScale NPM-160 / US600 Design Certification** documentation — the published
  reference against which the whole conjugate-CFD + correlation toolchain was
  validated before use on Aegis-40 (natural circulation, core ΔT, ECCS/containment
  envelope; e.g. ML24326A095 on peaking/LCO practice).
- **NUREG-1431** (Standard Technical Specifications, Westinghouse plants) — COLR
  practice for cycle-specific peaking limits; Salem-1 COLR example (ML23306A028).
- **10 CFR 50.46** — PCT 1204 °C, oxidation 17 %, H₂ 1 % acceptance criteria.
- **SRP 15.4.8** — rod-ejection accident evaluation framing.

## Consensus standards
- **ASME V&V 20** (and Celik et al., *J. Fluids Eng.* 130 (2008) 078001) — GCI
  mesh-independence procedure.
- **ANS-5.1** — decay-heat curve class used for the PRHR grace-period analysis.

## Archival literature (correlations & methods)
- Tong, L.S., *Boiling Crisis and Critical Heat Flux*, 1972 — W-3 CHF + F-factor.
- Todreas & Kazimi, *Nuclear Systems I/II* — Bowring-1972 SI form (verified
  term-for-term), Ishii-Zuber stability, single-phase friction.
- Groeneveld, D.C., et al., "The 2006 CHF look-up table," *Nuclear Engineering and
  Design* 237 (2007) 1909–1922 — CHF LUT data planes (12 000 / 14 000 kPa).
- Bowring, R.W., AEEW-R789 (1972) — original CHF correlation.
- Jens & Lottes (1951) — subcooled-boiling wall superheat.
- Idel'chik, *Handbook of Hydraulic Resistance* — loop form-loss coefficients.
- Kakac & Bon, *Int. J. Heat Mass Transfer* 51 (2008) — two-phase instability review.
- MASLWR/OSU test programme publications — natural-circulation ṁ ~ P^(1/3) trend.
- CAREM-25 (OSTI 20194765) and SMART design publications — SMR peaking/MDNBR precedent;
  CAREM-25 pressure-suppression containment (Delmastro et al., IAEA) — closest
  architectural analogue for the Aegis-40 suppression/IRWST baseline.
- SMART100 CPRSS passive-containment studies (Park et al.) and SISTA1/SISTA2 test
  programme (Yang et al., 2024) — direct-contact condensation / passive
  pressure-suppression experimental precedent.
- **NEA/CSNI** pressure-suppression state-of-the-art report and **NUREG-0800 SRP 6.5.5**
  — suppression-pool physics and review criteria (F6 screening support).

*(Full URLs / accession numbers for the NRC ADAMS documents are kept in the project
source-data notes; verify accession IDs before final submission.)*
