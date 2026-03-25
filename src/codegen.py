"""
Stem-code generator — renders Jinja2 templates from fractal_medallion_lineage.xml
into concrete Python modules for each medallion tier.

Usage:
    python -m src.codegen [--out-dir src/transforms]
"""

from __future__ import annotations

import argparse
import pathlib
import sys

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("jinja2 not installed — run: pip install jinja2", file=sys.stderr)
    sys.exit(1)

# ── Tier definitions (mirrors XML TierConstants) ──────────────────────────────

TIERS = [
    {
        "name":        "bronze",
        "order":       0,
        "c_real":      -0.75,
        "c_imaginary":  0.00,
        "input_tier":  "source",
        "proto_message": "RawEntity",
        "operations": [
            {"type": "validate_mime",          "lang_sensitive": False},
            {"type": "attach_fractal_state",   "lang_sensitive": False},
        ],
    },
    {
        "name":        "silver",
        "order":       1,
        "c_real":      -0.12,
        "c_imaginary":  0.74,
        "input_tier":  "bronze",
        "proto_message": "CuratedEntity",
        "operations": [
            {"type": "deduplicate",                  "lang_sensitive": True},
            {"type": "conform_schema",               "lang_sensitive": False},
            {"type": "resolve_multilingual_entities","lang_sensitive": True},
        ],
    },
    {
        "name":        "gold",
        "order":       2,
        "c_real":       0.285,
        "c_imaginary":  0.01,
        "input_tier":  "silver",
        "proto_message": "BusinessEntity",
        "operations": [
            {"type": "aggregate",      "lang_sensitive": False},
            {"type": "quality_score",  "lang_sensitive": False},
            {"type": "regulatory_tag", "lang_sensitive": False},
        ],
    },
]

CONTEXT = {
    "seed":            {"real": -1, "imaginary": 0},
    "escape_radius":   2.0,
    "max_iterations":  256,
    "default_lang":    "en",
    "supported_langs": ["en", "fr", "fa"],
    "tiers":           TIERS,
    "session_id":      "{{session_id}}",   # kept as template placeholder
}


def render_tier_transforms(template_dir: pathlib.Path, out_dir: pathlib.Path) -> None:
    env = Environment(loader=FileSystemLoader(str(template_dir)), keep_trailing_newline=True)
    tmpl = env.get_template("tier_transform.py.j2")

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "__init__.py").write_text("# Auto-generated tier transforms\n")

    for tier in TIERS:
        ctx = {**CONTEXT, "tier": tier}
        code = tmpl.render(ctx)
        out_path = out_dir / f"transform_{tier['name']}.py"
        out_path.write_text(code)
        print(f"  Generated: {out_path}")


def render_dockerfile(template_dir: pathlib.Path, out_dir: pathlib.Path) -> None:
    env = Environment(loader=FileSystemLoader(str(template_dir)), keep_trailing_newline=True)
    tmpl = env.get_template("Dockerfile.j2")
    code = tmpl.render(CONTEXT)
    out_path = out_dir / "Dockerfile.lineage"
    out_path.write_text(code)
    print(f"  Generated: {out_path}")


def render_lambda_handler(template_dir: pathlib.Path, out_dir: pathlib.Path) -> None:
    env = Environment(loader=FileSystemLoader(str(template_dir)), keep_trailing_newline=True)
    tmpl = env.get_template("lambda_handler.py.j2")
    code = tmpl.render(CONTEXT)
    out_path = out_dir / "lambda_handler.py"
    out_path.write_text(code)
    print(f"  Generated: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fractal Medallion Lineage code generator")
    parser.add_argument("--template-dir", default="templates/j2",     help="Jinja2 template directory")
    parser.add_argument("--out-dir",      default="src/transforms",   help="Python output directory")
    parser.add_argument("--root",         default=".",                 help="Repository root")
    args = parser.parse_args()

    root         = pathlib.Path(args.root).resolve()
    template_dir = root / args.template_dir
    out_dir      = root / args.out_dir

    print(f"Fractal Medallion Lineage — code generation")
    print(f"  Templates : {template_dir}")
    print(f"  Output    : {out_dir}")
    print()

    render_tier_transforms(template_dir, out_dir)
    render_dockerfile(template_dir, root)
    render_lambda_handler(template_dir, root / "lineage" / "handler")

    print("\nDone.")


if __name__ == "__main__":
    main()
