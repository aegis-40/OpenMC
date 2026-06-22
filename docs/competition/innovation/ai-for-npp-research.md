# AI for Nuclear Power Plants — Research Landscape & Aegis-40 Originality Note

*Research brief, 2026-06-19. Supports FER §8.7.6 (digital-twin advisory, originality feature) and the §8.12 FOM originality scoring. Grounded in 2023–2026 literature (see Sources).*

---

## 0. Why this note exists

The Aegis-40 FER already claims a **non-safety digital twin** (§8.7.6) as an originality feature: it mirrors Layer-1 signals through a one-way data diode and provides *soft sensors* (MDNBR, fuel-centreline temperature), anomaly detection and predictive maintenance, as **Category-C software that cannot actuate any device**. This brief surveys what the current AI-for-NPP research field actually does, separates the feasible from the science-fiction (notably the "camera watching the core melt" idea), and maps the credible pieces onto our boron-free passive iPWR so the FER can claim a *defensible* novelty rather than a hand-wave.

---

## 1. The "camera monitoring the core" idea — feasibility

**Direct optical imaging of an operating core is not feasible.** A camera in the RPV faces ~300 °C, 12.8 MPa, and a neutron/gamma field that degrades CMOS sensors and darkens optics within minutes to hours; the coolant offers no useful view of fuel. No vendor monitors core melt with an in-vessel camera.

**Core state / melt onset is instead inferred from sensors**, and AI's role is to *predict* it:
- Inputs: core-exit thermocouples, self-powered neutron detectors (SPNDs), RPV/pressurizer level & pressure, containment radiation, ex-core flux.
- AI役: supervised / reinforcement-learning models that predict **remaining time to reactor-vessel failure** and recommend accident-management actions, validated against severe-accident codes (MELCOR/MAAP). Explainable-AI (XAI) variants exist specifically so an operator can trust the prediction (see §2-E).

**Where cameras + vision AI are genuinely used** (and where the user's instinct is correct):
- **Spent-fuel-pool & refuelling**: CNN defect/scratch detection on fuel assemblies (Faster R-CNN, ~0.98 true-positive @ 0.1 false-positive); **Cherenkov-glow imaging** (Cherenkov Viewing Device, CVD) for IAEA safeguards verification of declared spent-fuel inventory — anomalous assemblies stand out by their Cherenkov-light signature.
- **Inspection robots / underwater drones** for in-pool and dry-cask survey (e.g. pre-batched inspection strategies, ML damage-ID on sealed canisters).
- **Containment / ex-vessel & decommissioning**: radiation-hardened cameras + vision AI for leak detection, debris characterisation (Fukushima/Sellafield-class problems), thermal imaging of pipework.

> **FER takeaway:** reframe "AI camera on the core" as **(a)** a digital-twin *virtual sensor* that infers core thermal margin & predicts melt-onset from qualified instrumentation, plus **(b)** vision-AI for fuel-handling/safeguards in the SFP (§8.8.6). Both are real, cited, and defensible; an in-core camera is not.

---

## 2. Current research areas (taxonomy)

### A. Fault Detection & Diagnosis (FDD) — the largest, most mature area
Classify the plant's condition (normal / specific fault / accident type) from sensor streams.
- Gradient-boosted trees (**LightGBM**) and CNN **transfer-learning** backbones (VGG16, ResNet50V2, Xception, DenseNet121, MobileNetV2) for accident-event detection & identification; LightGBM tends to top precision/recall/F1 on tabular signal features.
- Mature enough that review papers now catalogue methods & applications across the FDD space.
- Adjacent: **human-error detection/identification** via AI to catch operator mistakes.
- **TRL/use:** advisory/operator-support today; not yet credited in the safety chain.

### B. Digital twins + virtual ("soft") sensing — fastest-growing area
A calibrated real-time model running alongside the plant, estimating un-measured quantities and detecting drift.
- **PUR-1 (Purdue)** research reactor digital twin: simultaneous reactor-physics assessment + ML prediction + anomaly detection on off-normal operation.
- **Deep neural operators** (DeepONet-class) for **virtual sensing** — estimate fields you can't instrument directly, in real time.
- **Graph neural networks** treating the whole plant as a heterogeneous graph (graph convolution + temporal attention) for **whole-system** digital twins coupled to system codes (e.g. SAM).
- **Argonne** published a general digital-twin construction methodology (2025); twins can run real-time at ~1 Hz to feed state estimates to a controller.
- **TRL/use:** monitoring, predictive maintenance, operator decision support; condition-monitoring reviews now exist.

### C. Anomaly detection & I&C cybersecurity
- Unsupervised **explainable** deep frameworks to localize **replay attacks** in reactor signals (concurrent-attack localization).
- **Adversarial robustness** is now itself a research topic: gradient-free attacks on neural-operator T-H surrogates show DT/AI surrogates can be fooled — directly relevant to why AI must stay *advisory* and *air-gapped* from Class 1E (our data-diode choice).

### D. Autonomous & self-correcting control
- AI **autonomous-control architectures for SMRs**: modular monitoring/diagnosis → strategy formulation → assessment, including **emergency-operation** control models.
- Reinforcement-learning controllers trained against a calibrated 1 Hz digital twin.
- **LLM-integrated** AI thermal-fluid testbeds for advanced SMRs (digital twin + large language models for operator interaction / reasoning) — 2025 frontier work.
- Reviews stress the open gap: moving from simulators to **real reactors**, especially advanced/SMRs.

### E. Severe-accident prediction & accident management
- Supervised model predicting **remaining time to reactor-vessel failure**; RL strategies validated against severe-accident-code simulations.
- **Explainable AI (XAI)** for reliable prediction of severe-accident **progression** — explicitly to make the prediction trustworthy to operators/regulators.
- This is the rigorous version of the user's "is it about to melt?" question.

### F. Computer vision (the camera family, done right)
- **Fuel-assembly defect detection** via deep neural networks (Faster R-CNN scratch detection).
- **Cherenkov-light** digital imaging for **safeguards** verification of spent fuel; combined Cherenkov + gamma-emission tomography for automated defect detection.
- **Inspection robots** (in-pool, dry-cask, canister) with ML damage identification.

### G. Reactor physics & design surrogates (where *your* OpenMC work lives)
- **pyMAISE** — automated-ML platform building NPP models (e.g. **critical-heat-flux prediction**, electronics fault detection).
- **AI in reactor physics** reviews (surrogate cross-sections, flux/power-map emulation, depletion acceleration).
- **ML/AI multi-scale modelling** for high-burnup **accident-tolerant fuels** (ATF) in LWR SMRs.
- **AI-driven uncertainty quantification** + multi-physics for micro-reactor cladding.
- Transparency tooling so these models are auditable for nuclear engineering use.

---

## 3. Cross-cutting barriers (the honest part — judges reward this)

1. **Interpretability** — end-to-end nets are hard to explain; hence the XAI sub-field. A black box cannot enter a safety case.
2. **V&V & qualification** — no accepted pathway yet to qualify a learning system as Class 1E (IEEE 603 / IEC 60880 assume deterministic software). This is *why* credible designs keep AI strictly **advisory / Category-C**, exactly as our §8.7.6 does.
3. **Adversarial & cyber fragility** — surrogates can be fooled; replay/false-data attacks are demonstrated. Reinforces the one-way data-diode / no-actuation boundary.
4. **Data scarcity** — real accident data is essentially nonexistent; models train on simulator output (MELCOR/RELAP/SAM), so generalization to a real plant is unproven.
5. **Regulatory acceptance** — NRC/IAEA frameworks for AI in safety I&C are still emerging.

---

## 4. What is realistic & original for Aegis-40

Keep AI strictly on the **advisory (Category-C), de-energize-to-actuate-isolated** side already drawn in §8.7. Concretely, the FER can claim — and lightly justify — these, in increasing novelty:

| # | Feature | What it does | Maturity / risk | FER hook |
|---|---|---|---|---|
| 1 | **Soft sensors (DeepONet/virtual sensing)** | Real-time MDNBR, fuel-centreline T, core thermal-margin where no instrument exists | Established (§2-B) | §8.7.6 (already stated) — name the method |
| 2 | **Anomaly / drift detection** | Unsupervised model flags off-normal vs the twin; predictive maintenance | Established (PUR-1, §2-B/A) | §8.7.6 + §8.8 condition-based maintenance |
| 3 | **XAI severe-accident-margin advisor** | Predicts time-to-uncovery / margin from core-exit TC + SPND + level; *explainable* | Emerging (§2-E) | §8.6/§8.7.5 operator decision support |
| 4 | **Vision-AI in the SFP** | CNN fuel-defect detection + Cherenkov safeguards imaging at refuelling | Established (§2-F) | §8.8.6 fuel handling + §8.11/3S safeguards |
| 5 | **Cyber-hardened twin** | Replay/false-data-attack detection on the diode-fed mirror | Emerging (§2-C) | §8.7.1/§8.7.7 cybersecurity (RG 5.71) |

**Strongest single original claim for Aegis-40:** an **explainable digital-twin "thermal-margin & accident-precursor advisor"** that fuses the SBF iPWR's passive-design instrumentation (core-exit TCs, SPND flux map, level, containment radiation) into a real-time soft-sensor + anomaly layer, delivering MDNBR / time-to-margin estimates to the MCR — **advisory only, behind the data diode, never actuating** — with XAI so every alert is traceable. This is novel *and* honest: it leans into our passive, boron-free, reduced-staffing concept (the twin enables condition-based maintenance and the §8.7.6 reduced-staffing case) without ever touching the Class 1E qualification boundary.

**Phrase it against the barriers in §3** — explicitly state AI is Category-C advisory because qualification/interpretability/adversarial limits forbid it in the safety chain. Acknowledging the limits is what makes the originality claim credible to a technical judge rather than naive.

---

## 5. Suggested FER wording hook (drop-in for §8.7.6)

> The digital twin employs deep-neural-operator *virtual sensors* to estimate un-instrumented thermal-margin quantities (MDNBR, fuel-centreline temperature) in real time, an unsupervised anomaly-detection layer benchmarked against the twin's nominal trajectory, and an *explainable* accident-precursor advisor that fuses core-exit thermocouple, SPND, and level signals to indicate time-to-thermal-margin for the operator. Consistent with the current state of the field — where interpretability, formal V&V, and adversarial-robustness limits preclude learning systems from safety actuation — all AI functions are **Category-C, advisory only, fed through the unidirectional data diode, and incapable of actuating any device** (§8.7.1). [refs: PUR-1 DT; DeepONet virtual sensing; XAI severe-accident progression]

---

## Sources

Fault detection & diagnosis: [Efficient AI fault diagnosis (ScienceDirect 2024)](https://www.sciencedirect.com/science/article/abs/pii/S0149197024005304) · [Review of AI for FDD in NPPs (ScienceDirect 2024)](https://www.sciencedirect.com/science/article/abs/pii/S0149197024004244) · [Human-error detection via AI (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/pii/S2590123025026854) · [AI-driven real-time diagnostics & self-correcting control (ResearchGate 2025)](https://www.researchgate.net/publication/395890369)

Digital twins & virtual sensing: [DT for reactor dynamics: ML + MPC (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/abs/pii/S0952197625009406) · [DT framework for remote monitoring (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/pii/S0029549325007629) · [PWR startup DT + edge computing (arXiv 2407.12011)](https://arxiv.org/pdf/2407.12011) · [Whole-system DT with GNN + SAM (Nuclear Technology 2024)](https://www.tandfonline.com/doi/full/10.1080/00295450.2024.2385214) · [Virtual-sensing DT via deep neural operators (OSTI / arXiv 2410.13762)](https://arxiv.org/pdf/2410.13762) · [Argonne DT methodology (ANS 2025)](https://www.ans.org/news/2025-06-04/article-7089/argonne-creates-new-methodology-for-digital-twins/) · [Advances in DT & AI/ML condition monitoring (Frontiers 2026)](https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2026.1716514/full)

Anomaly detection & cyber: [Unsupervised XAI replay-attack localization (arXiv 2508.09162)](https://arxiv.org/pdf/2508.09162) · [Adversarial attacks on neural-operator DT surrogates (arXiv 2603.22525)](https://arxiv.org/pdf/2603.22525)

Autonomous control & accident management: [Autonomous control for SMR emergency operation (ScienceDirect 2023)](https://www.sciencedirect.com/science/article/abs/pii/S0306454923001937) · [Advancements & challenges of ML/DL in autonomous reactor control (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/abs/pii/S0306454925004608) · [AI thermal-fluid testbed: DT + LLMs for SMRs (arXiv 2507.06399)](https://arxiv.org/html/2507.06399v1) · [XAI for severe-accident progression prediction (ScienceDirect 2025)](https://www.sciencedirect.com/science/article/abs/pii/S0951832025005083)

Computer vision & safeguards: [Fuel-assembly defect detection by deep NN (ScienceDirect 2019)](https://www.sciencedirect.com/science/article/abs/pii/S0306454919305808) · [ML damage-ID of spent-fuel in dry canister (ScienceDirect 2023)](https://www.sciencedirect.com/science/article/abs/pii/S0952197623016688) · [Pre-batched inspection-strategy robot (ScienceDirect 2023)](https://www.sciencedirect.com/science/article/pii/S1738573323004047) · [Cherenkov digital-imaging fuel verification (ResearchGate)](https://www.researchgate.net/publication/223086282) · [Cherenkov viewing device for used-fuel verification (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/016800290090753S)

Reactor physics & fuel surrogates: [AI in reactor physics: status & prospects (arXiv 2503.02440)](https://arxiv.org/pdf/2503.02440) · [ML/AI multi-scale modelling for ATF in LWR SMRs (arXiv 2209.12146)](https://arxiv.org/pdf/2209.12146) · [AI-driven UQ for micro-reactor cladding (arXiv 2503.14679)](https://arxiv.org/pdf/2503.14679) · [pyMAISE / transparent nuclear ML models (U-Michigan NERS 2025)](https://ners.engin.umich.edu/2025/01/22/streamlining-ai-development-for-transparent-nuclear-engineering-models/)
