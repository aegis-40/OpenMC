# Appendix A — Digital Appendices (content list)

All computational evidence supporting this report is provided in a single compressed archive,
**`Aegis40-Digital-Appendix.zip`**, submitted separately from this report as required by the
FDR digital-appendix rule. For every code used in the analyses, the archive provides one
representative sample input file, an explanation of the conditions and approach for which the
input was created, the results obtained from the corresponding output, and reproducibility /
benchmarking / repeatability evidence drawn from reliable sources (OECD/NEA ICSBEP, US NRC,
IAEA, IAPWS and consensus standards). Each item below is a self-contained folder laid out as
`code/` · `inputs/` · `outputs/` · `evidence/` · `figures/`, each with its own `README.md`
stating the case conditions, approach, outputs and verification basis.

## A.1 Content list

| ID | Archive folder | Code / analysis | Reliable-source V&V | Report section(s) |
|---|---|---|---|---|
| **DA-0** | `0_icsbep_criticality/` | OpenMC criticality vs measured critical experiments | **OECD/NEA ICSBEP** LEU-COMP-THERM-008 (mean bias ≈ −50 pcm) | §8.2 |
| **DA-1** | `1_core_transport/` | Full-core OpenMC transport deck + authoritative neutronics notebook | Validated by DA-0 / DA-2 | §8.2 |
| **DA-2** | `2_depletion_benchmark/` | OpenMC depletion (BEAVRS pincell) + Aegis-40 cycle depletion driver | Code-to-code vs Serpent (Romano 2021) | §8.2, §8.11 |
| **DA-3** | `3_storage_criticality/` | Spent-fuel storage-rack criticality (k(95/95) ≤ 0.95) | Kim/Jung/Yoon (2024) SBF band; 10 CFR 50.68 | §8.11 |
| **DA-4** | `4_safety_neutronics/` | SDM / rod worth, EBIS, SFP, MSLB, cycle peaking, REA | NuScale-like SMR benchmark (±80 pcm) + ICSBEP | §8.5, §8.6 |
| **DA-5** | `5_digital_twin/` | OpenMC eigenvalue sweep + GP/POD surrogate digital twin | Surrogate validation set (parity, coefficients) | §8.7 |
| **DA-6** | `6_waste_results/` | Back-end fuel cycle: discharge inventory, decay heat, source term, safeguards FOM | ANSI/ANS-5.1 decay-heat standard | §8.11 |
| **DA-7** | `7_energy_cycle/` | Rankine cycle + SOE-H₂ schedule + TCES district-heat balance; LCOE, exergy | IAPWS-IF97 steam properties | §8.9, §8.12 |
| **DA-8** | `8_thermal_hydraulics/` | OpenFOAM v2412 conjugate-heat-transfer CFD + Python safety toolchain (MDNBR, PCT, natural circulation) | ASME V&V-20 grid convergence; NuScale validation; US NRC correlations | §8.4, §8.5 |
| **DA-9** | `9_tces_model/` | Thermochemical energy-storage thermodynamic model | Reproduces Yan et al. (2020) COPh / γ_h | §8.9 |
| **DA-10** | `10_shielding/` | Operating biological-shield dose (MC + ANS-6.4 point-kernel) and RPV fast fluence | Rockwell TID-7004, Chilton-Shultis-Faw, NIST-XCOM, ICRP-116 | §8.2.6 |
| **DA-F** | `figures/` | Representative model renders and result plots (core/pin maps, geometry, power distribution, k(BU), shield cross-section) | — | §8.2, §8.11 |

Folders **DA-5** and **DA-8** are self-contained discipline packages contributed by the digital-twin
and thermal-hydraulic teams; they follow the same input/output/V&V separation under their own
internal layout. The archive root `README.md` records the locked design basis and the full V&V
mapping (reproducibility, repeatability, benchmarking).

## A.2 Cross-references to be inserted in the main report

Per the FDR requirement, each supported section of the main report carries an in-text link to the
corresponding Digital Appendix item. The callouts to insert are:

| Report section | In-text cross-reference to add |
|---|---|
| §8.2 Core & neutronics | *"Neutronics models, criticality validation and burnup evolution: Digital Appendix **DA-0, DA-1, DA-2** (and figures **DA-F**)."* |
| §8.2.6 Shielding / dose | *"Radiation-shielding model, dose and RPV fluence results: Digital Appendix **DA-10**."* |
| §8.4 Thermal-hydraulics | *"CFD conjugate-heat-transfer case and DNBR/PCT safety toolchain: Digital Appendix **DA-8**."* |
| §8.5 Safety analysis | *"Safety-neutronics suite and thermal-hydraulic safety margins: Digital Appendix **DA-4, DA-8**."* |
| §8.6 Shutdown & PRA | *"Shutdown-margin, EBIS, MSLB and rod-ejection evaluations: Digital Appendix **DA-4**."* |
| §8.7 I&C / digital twin | *"Physics-trained surrogate digital twin: Digital Appendix **DA-5**."* |
| §8.9 Energy cycle & cogeneration | *"Power-conversion, hydrogen and district-heat balances: Digital Appendix **DA-7, DA-9**."* |
| §8.11 Waste & back-end | *"Discharge inventory, decay heat, source term, storage criticality and safeguards: Digital Appendix **DA-2, DA-3, DA-6**."* |
| §8.12 Economics | *"LCOE and cogeneration economics inputs: Digital Appendix **DA-7**."* |

*(Rendered as hyperlinks in the electronic report; the archive item ID resolves to the matching
folder inside `Aegis40-Digital-Appendix.zip`.)*
