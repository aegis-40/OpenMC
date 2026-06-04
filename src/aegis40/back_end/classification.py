"""Indicative IAEA-style radioactive-waste classification (FER §8.11).

Implements a simplified screening against the IAEA GSG-1 waste classes so that a
stream (spent fuel, or a secondary stream such as spent resin / evaporator
concentrate) can be tagged EW / VLLW / LLW / ILW / HLW from its specific activity,
decay-heat density and dominant half-life.

These thresholds are **indicative screening values** for design-stage sorting.
The authoritative classification for the submission must follow the Turkish
nuclear regulator (NDK) waste-classification regulation and IAEA GSG-1 in full;
cite those, and use this only to justify the segregation logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .source_term import YEAR_S


class WasteClass(str, Enum):
    EW = "exempt"                       # exempt / clearable
    VLLW = "very_low_level"
    LLW = "low_level"
    ILW = "intermediate_level"
    HLW = "high_level"


# Screening thresholds (indicative; see module docstring).
HLW_HEAT_W_PER_M3 = 2.0e3               # heat-generating -> HLW (IAEA ~2 kW/m3)
ILW_ACTIVITY_BQ_PER_G = 4.0e6           # above near-surface LLW capacity
LLW_ACTIVITY_BQ_PER_G = 4.0e2           # above clearance/exempt order of magnitude
SHORT_LIVED_HALF_LIFE_S = 30.0 * YEAR_S  # Cs-137/Sr-90 class boundary


@dataclass(frozen=True)
class ClassificationResult:
    waste_class: WasteClass
    rationale: str


def classify(
    specific_activity_bq_per_g: float,
    decay_heat_w_per_m3: float = 0.0,
    dominant_half_life_s: float | None = None,
) -> ClassificationResult:
    """Screen a waste stream into an indicative IAEA GSG-1 class.

    Parameters
    ----------
    specific_activity_bq_per_g:
        Specific activity of the stream (Bq/g).
    decay_heat_w_per_m3:
        Volumetric decay-heat density (W/m^3). The HLW discriminator.
    dominant_half_life_s:
        Half-life of the activity-dominating nuclide, used to separate
        short-lived (near-surface-disposable) from long-lived streams.
    """
    if specific_activity_bq_per_g < 0 or decay_heat_w_per_m3 < 0:
        raise ValueError("activity and heat must be non-negative")

    if decay_heat_w_per_m3 >= HLW_HEAT_W_PER_M3:
        return ClassificationResult(
            WasteClass.HLW,
            f"decay heat {decay_heat_w_per_m3:.3g} W/m^3 >= "
            f"{HLW_HEAT_W_PER_M3:.0f} W/m^3 (heat-generating)",
        )

    long_lived = (
        dominant_half_life_s is not None and dominant_half_life_s > SHORT_LIVED_HALF_LIFE_S
    )

    if specific_activity_bq_per_g >= ILW_ACTIVITY_BQ_PER_G or long_lived:
        why = (
            f"specific activity {specific_activity_bq_per_g:.3g} Bq/g "
            f">= {ILW_ACTIVITY_BQ_PER_G:.0g} Bq/g"
            if specific_activity_bq_per_g >= ILW_ACTIVITY_BQ_PER_G
            else "long-lived activity beyond near-surface-disposal scope"
        )
        return ClassificationResult(WasteClass.ILW, why)

    if specific_activity_bq_per_g >= LLW_ACTIVITY_BQ_PER_G:
        return ClassificationResult(
            WasteClass.LLW,
            f"specific activity {specific_activity_bq_per_g:.3g} Bq/g within "
            "near-surface (LLW) range, short-lived dominant",
        )

    if specific_activity_bq_per_g > 0.0:
        return ClassificationResult(
            WasteClass.VLLW,
            f"specific activity {specific_activity_bq_per_g:.3g} Bq/g near "
            "clearance level",
        )

    return ClassificationResult(WasteClass.EW, "negligible activity (exempt)")
