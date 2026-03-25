"""
Core fractal iteration engine for the Medallion Lineage system.

Seed z₀ = -1 + 0i (canonical Mandelbrot critical point).
Each medallion tier applies: z_(n+1) = z_n² + c_tier

Tier constants:
  bronze  c = -0.75 + 0.0i   (near period-2 bulb — minimal transform)
  silver  c = -0.12 + 0.74i  (Dendrite region — branching lineage)
  gold    c =  0.285 + 0.01i (Julia-connected — stable attractor)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

# ── Constants ────────────────────────────────────────────────────────────────

SEED: complex = complex(-1, 0)   # z₀ = -1 + 0i

TIER_CONSTANTS: dict[str, complex] = {
    "bronze": complex(-0.75,  0.00),
    "silver": complex(-0.12,  0.74),
    "gold":   complex( 0.285, 0.01),
}

ESCAPE_RADIUS:        float = 2.0
CONVERGENCE_THRESHOLD: float = 1e-10
MAX_ITERATIONS:        int   = 256

TIER_ORDER: dict[str, int] = {"bronze": 0, "silver": 1, "gold": 2}


# ── Data model ───────────────────────────────────────────────────────────────

@dataclass
class FractalState:
    """Snapshot of one fractal iteration step."""
    z:              complex
    iteration:      int
    bounded:        bool
    magnitude:      float
    attractor_class: Optional[str] = field(default=None)

    def as_dict(self) -> dict:
        return {
            "z_real":         self.z.real,
            "z_imaginary":    self.z.imag,
            "iteration":      self.iteration,
            "bounded":        self.bounded,
            "magnitude":      self.magnitude,
            "attractor_class": self.attractor_class,
        }


# ── Core functions ───────────────────────────────────────────────────────────

def iterate(z: complex, c: complex) -> tuple[complex, float, bool]:
    """Apply one fractal step: z_(n+1) = z_n² + c.

    Returns (z_new, magnitude, bounded).
    """
    z_new     = z ** 2 + c
    magnitude = abs(z_new)
    return z_new, magnitude, magnitude <= ESCAPE_RADIUS


def classify_attractor(z: complex) -> str:
    """Classify the attractor type from the current z value."""
    mag = abs(z)
    if mag < CONVERGENCE_THRESHOLD:
        return "fixed_point"
    elif mag < 1.0:
        return "periodic"
    else:
        return "chaotic"


def step_tier(tier: str, z: complex) -> FractalState:
    """Perform a single fractal iteration for the given medallion tier.

    Args:
        tier: One of "bronze", "silver", "gold".
        z:    Current complex value (z_n).

    Returns:
        FractalState with iteration n+1 values.
    """
    if tier not in TIER_CONSTANTS:
        raise ValueError(f"Unknown tier '{tier}'. Expected one of {list(TIER_CONSTANTS)}")

    c             = TIER_CONSTANTS[tier]
    z_new, mag, bounded = iterate(z, c)
    return FractalState(
        z=z_new,
        iteration=TIER_ORDER[tier] + 1,
        bounded=bounded,
        magnitude=mag,
        attractor_class=classify_attractor(z_new) if bounded else "divergent",
    )


def traverse(entity_id: str, source_tier: str = "bronze", target_tier: str = "gold") -> list[FractalState]:
    """Traverse the medallion stack from source_tier to target_tier.

    Starts from SEED (z₀ = -1 + 0i) and applies tier iterations in order.

    Returns:
        Ordered list of FractalState objects for each tier crossed.
    """
    tier_sequence = ["bronze", "silver", "gold"]
    try:
        start_idx = tier_sequence.index(source_tier)
        end_idx   = tier_sequence.index(target_tier)
    except ValueError as exc:
        raise ValueError(f"Invalid tier name: {exc}") from exc

    if start_idx > end_idx:
        raise ValueError(f"source_tier '{source_tier}' is after target_tier '{target_tier}'")

    z       = SEED
    states: list[FractalState] = []
    for tier in tier_sequence[start_idx : end_idx + 1]:
        state = step_tier(tier, z)
        states.append(state)
        if not state.bounded:
            # Anomaly: lineage diverges — stop traversal
            break
        z = state.z

    return states
