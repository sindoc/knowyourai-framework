
"""
Lambda handler for fractal lineage iteration.
Auto-generated from: fractal_medallion_lineage.xml / lambda_handler.py.j2
DO NOT EDIT — regenerate via: python -m src.codegen

Processes: MIME request → fractal transformation → proto response
Supported MIME types: application/x-protobuf | application/json
"""

import os
import json

# Import generated proto classes

from generated.lineage.bronze import RawEntity_pb2

from generated.lineage.silver import CuratedEntity_pb2

from generated.lineage.gold import BusinessEntity_pb2

from generated.lineage.common import fractal_state_pb2  # noqa: F401

# Tier transformation constants  c_tier = real + imaginary·i
TIER_CONSTANTS: dict[str, complex] = {

    "bronze": complex(-0.75, 0.0),

    "silver": complex(-0.12, 0.74),

    "gold": complex(0.285, 0.01),

}

ESCAPE_RADIUS  = float(os.environ.get("ESCAPE_RADIUS", "2.0"))
MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS", "256"))


def _classify_attractor(z: complex) -> str:
    mag = abs(z)
    if mag < 0.01:
        return "fixed_point"
    elif mag < 1.0:
        return "periodic"
    else:
        return "chaotic"


def iterate(event: dict, context) -> dict:
    """AWS Lambda entry point — fractal lineage iteration.

    Event schema is defined in the <lambda:RequestTemplate> section
    of fractal_medallion_lineage.xml.
    """
    session_id  = event["SessionId"]
    entity_id   = event["EntityId"]
    target_tier = event["TargetTier"]
    lang        = event.get("Language", "en")

    fp = event.get("FractalParams", {})
    z  = complex(
        float(fp.get("CurrentZ", {}).get("real",      "-1")),
        float(fp.get("CurrentZ", {}).get("imaginary",  "0")),
    )
    c          = TIER_CONSTANTS[target_tier]
    iteration  = int(fp.get("iteration", 0))

    # Core fractal step: z_(n+1) = z_n² + c
    z_new     = z ** 2 + c
    magnitude = abs(z_new)
    bounded   = magnitude <= ESCAPE_RADIUS

    return {
        "SessionId": session_id,
        "EntityId":  f"{entity_id}_{target_tier}",
        "Tier":      target_tier,
        "FractalResult": {
            "NewZ":           {"real": z_new.real, "imaginary": z_new.imag},
            "Magnitude":      magnitude,
            "Bounded":        bounded,
            "AttractorClass": _classify_attractor(z_new) if bounded else "divergent",
            "IterationCount": iteration + 1,
        },
        "LineageEdge": {
            "from":    entity_id,
            "to":      f"{entity_id}_{target_tier}",
            "formula": f"z\u00b2 + c_{target_tier}",
        },
        "Language": lang,
        "Status":   "fulfilled",
    }
