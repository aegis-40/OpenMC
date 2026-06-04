"""Shared project context values used by scripts and analyses."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectContext:
    project_name: str = "Aegis-40 iPWR"
    competition: str = "Teknofest 2026 — Nuclear Energy Technologies (Detailed Design)"
    nominal_power_mwe: float = 40.0
    design_principles: tuple[str, ...] = (
        "soluble-boron-free core",
        "open-source multiphysics modeling",
        "integrated TES and SOE applications",
        "digital twin–enabled predictive monitoring",
        "3S-by-design",
    )


DEFAULT_CONTEXT = ProjectContext()
