# Archived FER section drafts (superseded 2026-06-22)

These per-section drafts have been **consolidated into the single master document**
[`../Aegis40-FER-master.md`](../Aegis40-FER-master.md) (master r1, 37-FA design basis). They are kept
here for traceability — the master carries their full substance, plus the cross-section
reconciliation, the 37-FA results-pending markers, and the requirements-coverage matrix.

| Archived file | Now lives in the master as |
|---|---|
| `section-8.1-general-parameters.md` | §8.1 |
| `section-8.2-8.3-core-and-fuel.md` | §8.2, §8.3 (re-based 21-FA → 37-FA) |
| `section-8.4-cooling-circuit.md` | §8.4 |
| `section-8.9-energy-cycle.md` | §8.9 |
| `section-8.11-waste.md` | §8.11 |
| `section-8.12-economics.md` | §8.12 |
| `FER_Aegis40_safety_ic_layout_draft.md` | §8.5, §8.6, §8.7, §8.8, §8.10 |

**Key change at consolidation:** the design basis moved from the 21-FA core to the **37-FA / 7×7**
core (CAD `cad/aegis40-geometry-spec-37fa.md`). The 37-FA *neutronic results* (k_eff, burnup, cycle
length, peaking, reactivity coefficients, rod worth, SDM, discharge inventory) are produced by a
STAT_FINAL OpenMC run that is still in progress; in the master they are marked **⏳[37FA-PENDING]** and
shown alongside the previously-locked 21-FA values as a conservative reference. The archived drafts
here contain the original 21-FA prose verbatim.

Still-live source/support docs (NOT archived — cited by the master): `../enrichment-zoning-benchmark-rev7.md`,
`../nonproliferation-assessment.md`, `../neutronics-openmc-requirements-and-plan.md`,
`../../design-basis-locked.md`.
