# OpenMC Simulations – Aegis-40

This repository contains neutronics simulations for the **Aegis-40 SMR** using [OpenMC](https://openmc.org/).

## 📌 Scope

| Module | Description |
|---|---|
| `src/geometry/` | Core geometry modeling (fuel pin, assembly, full core) |
| `src/criticality/` | Criticality (k-eff) calculations |
| `src/depletion/` | Burnup / depletion simulations |
| `src/reactivity/` | Reactivity coefficient calculations |
| `src/flux/` | Flux distribution tallies |
| `models/` | Integrated Aegis-40 model entry point |
| `tests/` | Unit tests |

## 🛠 Requirements

- Python 3.10+
- OpenMC v0.15+
- Nuclear data library: **ENDF/B-VIII.0**

## 🚀 Setup

### Option A – Conda (recommended)

```bash
conda env create -f environment.yml
conda activate openmc-env
```

### Option B – pip

```bash
pip install -r requirements.txt
```

### Nuclear data

Download the ENDF/B-VIII.0 cross-section library and set the environment variable:

```bash
export OPENMC_CROSS_SECTIONS=/path/to/endfb-viii.0-hdf5/cross_sections.xml
```

## 🔬 Running simulations

### Criticality (k-eff)

```bash
python src/criticality/keff_calculation.py
```

### Burnup / Depletion

```bash
python src/depletion/burnup_simulation.py
```

### Reactivity coefficients

```bash
python src/reactivity/reactivity_coefficients.py
```

### Flux distributions

```bash
python src/flux/flux_distribution.py
```

### Full Aegis-40 integrated model

```bash
python models/aegis40_model.py
```

## 🏗 Repository structure

```
OpenMC-/
├── README.md
├── environment.yml          # conda environment
├── requirements.txt         # pip requirements
├── .gitignore
├── src/
│   ├── geometry/
│   │   └── core_geometry.py
│   ├── criticality/
│   │   └── keff_calculation.py
│   ├── depletion/
│   │   └── burnup_simulation.py
│   ├── reactivity/
│   │   └── reactivity_coefficients.py
│   └── flux/
│       └── flux_distribution.py
├── models/
│   └── aegis40_model.py
└── tests/
    ├── test_geometry.py
    └── test_settings.py
```

## ⚙️ Aegis-40 Core Parameters

| Parameter | Value |
|---|---|
| Reactor type | PWR-type SMR |
| Thermal power | ~300 MWt |
| Fuel | UO₂, 4.25 wt% ²³⁵U enrichment |
| Cladding | Zircaloy-4 |
| Moderator/Coolant | Light water (H₂O) |
| Fuel pellet radius | 0.4096 cm |
| Clad outer radius | 0.4750 cm |
| Pin pitch | 1.26 cm |
| Assembly array | 17 × 17 |
| Active fuel height | 365.76 cm |
