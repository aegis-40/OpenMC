"""
aegis40_model.py
================
Integrated Aegis-40 SMR model entry point.

Provides a unified interface to run any combination of the available
simulation modules:
  - Geometry export
  - k-eff criticality calculation
  - Burnup / depletion simulation
  - Reactivity coefficient calculations
  - Flux distribution calculations

Usage
-----
    python models/aegis40_model.py [--help]
    python models/aegis40_model.py --mode keff
    python models/aegis40_model.py --mode depletion
    python models/aegis40_model.py --mode reactivity
    python models/aegis40_model.py --mode flux
    python models/aegis40_model.py --mode geometry   # export XML only
"""

import argparse
import os
import sys

# Ensure the repo root is on the path when running as a script
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Aegis-40 SMR – OpenMC simulation runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["geometry", "keff", "depletion", "reactivity", "flux"],
        default="keff",
        help=(
            "Simulation mode to run:\n"
            "  geometry   – export core geometry XML only\n"
            "  keff       – criticality (k-eff) calculation [default]\n"
            "  depletion  – burnup / depletion simulation\n"
            "  reactivity – reactivity coefficient calculations\n"
            "  flux       – flux distribution calculations"
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to write all simulation output (default: output/)",
    )
    parser.add_argument(
        "--export-only",
        action="store_true",
        help="Write XML input files only; do not run OpenMC",
    )
    return parser.parse_args()


def run(mode, output_dir="output", export_only=False):
    """
    Execute the requested simulation mode.

    Parameters
    ----------
    mode        : str  One of 'geometry', 'keff', 'depletion',
                       'reactivity', 'flux'.
    output_dir  : str  Base output directory.
    export_only : bool Write XML only, skip OpenMC execution.
    """
    os.makedirs(output_dir, exist_ok=True)

    if mode == "geometry":
        from src.geometry.core_geometry import build_model
        run_dir = os.path.join(output_dir, "geometry")
        os.makedirs(run_dir, exist_ok=True)
        orig = os.getcwd()
        os.chdir(run_dir)
        try:
            build_model(export=True)
            print(f"Geometry XML exported to: {run_dir}")
        finally:
            os.chdir(orig)

    elif mode == "keff":
        from src.criticality.keff_calculation import run_keff
        run_keff(
            output_dir=os.path.join(output_dir, "keff"),
            export_only=export_only,
        )

    elif mode == "depletion":
        from src.depletion.burnup_simulation import run_depletion
        run_depletion(
            output_dir=os.path.join(output_dir, "depletion"),
            export_only=export_only,
        )

    elif mode == "reactivity":
        from src.reactivity.reactivity_coefficients import run_all_coefficients
        run_all_coefficients(
            base_dir=os.path.join(output_dir, "reactivity"),
        )

    elif mode == "flux":
        from src.flux.flux_distribution import run_flux_distribution
        run_flux_distribution(
            output_dir=os.path.join(output_dir, "flux"),
            export_only=export_only,
        )

    else:
        raise ValueError(f"Unknown mode: {mode!r}")


if __name__ == "__main__":
    args = _parse_args()
    run(
        mode=args.mode,
        output_dir=args.output_dir,
        export_only=args.export_only,
    )
