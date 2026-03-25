"""
AWS Lambda handler — fractal lineage iteration.

Entry point: lineage.handler.iterate

Request schema  (application/json or application/x-protobuf):
{
    "SessionId":   "<uuid>",
    "EntityId":    "<string>",
    "SourceTier":  "bronze" | "silver" | "gold",
    "TargetTier":  "bronze" | "silver" | "gold",
    "FractalParams": {
        "CurrentZ":    {"real": <float>, "imaginary": <float>},
        "iteration":   <int>          // optional, defaults to 0
    },
    "MimeType":  "application/x-protobuf" | "application/json",
    "Language":  "<BCP-47>"              // optional, defaults to "en"
}

Response schema:
{
    "SessionId":  "<uuid>",
    "EntityId":   "<string>_<target_tier>",
    "Tier":       "<target_tier>",
    "FractalResult": {
        "NewZ":           {"real": <float>, "imaginary": <float>},
        "Magnitude":      <float>,
        "Bounded":        <bool>,
        "AttractorClass": <str>,
        "IterationCount": <int>
    },
    "LineageEdge": {
        "from":    "<source_entity_id>",
        "to":      "<derived_entity_id>",
        "formula": "z² + c_<target_tier>"
    },
    "Language": "<BCP-47>",
    "Status":   "fulfilled" | "anomaly"
}
"""

from __future__ import annotations

import os
import logging

from src.fractal import TIER_CONSTANTS, ESCAPE_RADIUS, classify_attractor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_ESCAPE_RADIUS = float(os.environ.get("ESCAPE_RADIUS", str(ESCAPE_RADIUS)))


def iterate(event: dict, context) -> dict:
    """Lambda entry point — single fractal iteration step.

    Reads the current complex state z_n from the event, applies
    z_(n+1) = z_n² + c_target_tier, and returns the lineage edge result.
    """
    session_id  = event["SessionId"]
    entity_id   = event["EntityId"]
    target_tier = event["TargetTier"]
    lang        = event.get("Language", "en")

    fp        = event.get("FractalParams", {})
    current_z = fp.get("CurrentZ", {})
    z         = complex(
        float(current_z.get("real",      -1)),
        float(current_z.get("imaginary",  0)),
    )
    iteration = int(fp.get("iteration", 0))

    if target_tier not in TIER_CONSTANTS:
        raise ValueError(f"Unknown tier '{target_tier}'")

    c         = TIER_CONSTANTS[target_tier]
    z_new     = z ** 2 + c
    magnitude = abs(z_new)
    bounded   = magnitude <= _ESCAPE_RADIUS
    attractor = classify_attractor(z_new) if bounded else "divergent"

    derived_id = f"{entity_id}_{target_tier}"

    logger.info(
        "Fractal step | session=%s entity=%s tier=%s z=%s→%s bounded=%s",
        session_id, entity_id, target_tier, z, z_new, bounded,
    )

    return {
        "SessionId": session_id,
        "EntityId":  derived_id,
        "Tier":      target_tier,
        "FractalResult": {
            "NewZ":           {"real": z_new.real, "imaginary": z_new.imag},
            "Magnitude":      magnitude,
            "Bounded":        bounded,
            "AttractorClass": attractor,
            "IterationCount": iteration + 1,
        },
        "LineageEdge": {
            "from":    entity_id,
            "to":      derived_id,
            "formula": f"z\u00b2 + c_{target_tier}",
        },
        "Language": lang,
        "Status":   "fulfilled" if bounded else "anomaly",
    }
