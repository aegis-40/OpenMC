#!/usr/bin/env python3
"""Run the Aegis-DT v0.6 sample input against the exported GP/POD model files.

This script is provided for the FER digital appendix. It reproduces the sample
surrogate-sensitivity output CSV from inputs/aegis_dt_v06_sample_input.json and
models/surrogate_*.pkl. The HTML dashboard itself embeds equivalent exported
model coefficients in JavaScript and does not require Python at runtime.
"""
from __future__ import annotations
import csv
import json
import pickle
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "inputs" / "aegis_dt_v06_sample_input.json"
OUT = ROOT / "outputs" / "aegis_dt_v06_surrogate_sample_output.csv"
ORDER = ["T_mod_K", "T_fuel_K", "n_rods_in", "void"]


def load_pickle(name: str):
    with open(ROOT / "models" / name, "rb") as f:
        return pickle.load(f)


def predict(block: dict, inp: dict) -> float:
    x = np.array([[float(inp[k]) for k in ORDER]])
    z = (x - np.asarray(block["Xm"], dtype=float)) / np.asarray(block["Xs"], dtype=float)
    return float(block["gp"].predict(z)[0])


def coeffs(kblock: dict, inp: dict) -> dict:
    eps_t = 1.0
    eps_v = 0.005
    mtc = (predict(kblock, {**inp, "T_mod_K": inp["T_mod_K"] + eps_t}) - predict(kblock, {**inp, "T_mod_K": inp["T_mod_K"] - eps_t})) / (2 * eps_t) * 1e5
    dtc = (predict(kblock, {**inp, "T_fuel_K": inp["T_fuel_K"] + eps_t}) - predict(kblock, {**inp, "T_fuel_K": inp["T_fuel_K"] - eps_t})) / (2 * eps_t) * 1e5
    vlo = max(0.0, inp["void"] - eps_v)
    vhi = min(0.2, inp["void"] + eps_v)
    void_coeff = (predict(kblock, {**inp, "void": vhi}) - predict(kblock, {**inp, "void": vlo})) / (vhi - vlo) * 1000
    rod_worth = (predict(kblock, {**inp, "n_rods_in": 0}) - predict(kblock, {**inp, "n_rods_in": 12})) * 1e5
    return {"MTC_pcm_per_K": mtc, "DTC_pcm_per_K": dtc, "void_coeff_pcm_per_percent": void_coeff, "rod_worth_0_to_12_pcm": rod_worth}


def power_map_summary(pm: dict, inp: dict) -> dict:
    x = np.array([[float(inp[k]) for k in ORDER]])
    z = (x - np.asarray(pm["Xm"], dtype=float)) / np.asarray(pm["Xs"], dtype=float)
    scores = np.array([float(g.predict(z)[0]) for g in pm["mode_gps"]])
    flat = pm["pca"].inverse_transform(scores.reshape(1, -1))[0]
    arr = flat.reshape(pm["shape"])
    finite = arr[np.isfinite(arr)]
    return {
        "powermap_min": float(np.nanmin(finite)),
        "powermap_max": float(np.nanmax(finite)),
        "powermap_sum": float(np.nansum(finite)),
    }


def main() -> None:
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    kblock = load_pickle("surrogate_k_eff.pkl")
    fblock = load_pickle("surrogate_F_assembly.pkl")
    pm = load_pickle("surrogate_powermap.pkl")
    rows = []
    for case in data["surrogate_sensitivity_cases"]:
        inp = {k: float(case[k]) for k in ORDER}
        row = {
            "case_id": case["case_id"],
            **inp,
            "k_eff_GP": predict(kblock, inp),
            "F_assembly_GP": predict(fblock, inp),
            **coeffs(kblock, inp),
            **power_map_summary(pm, inp),
        }
        rows.append(row)
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
