"""
Fractal Medallion Lineage Engine — HTTP + gRPC server.

Endpoints:
  GET  /health            → 200 OK
  POST /lineage/traverse  → JSON lineage traversal result
  POST /lineage/step      → JSON single-tier step result

Environment variables:
  HOST              (default: 0.0.0.0)
  PORT              (default: 8080)
  FRACTAL_SEED      (default: -1+0i)
  MEDALLION_TIERS   (default: bronze,silver,gold)
  ESCAPE_RADIUS     (default: 2.0)
  MAX_ITERATIONS    (default: 256)
"""

from __future__ import annotations

import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from src.fractal import SEED, TIER_CONSTANTS, traverse, step_tier

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("lineage_engine")

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8080"))


class LineageHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler for the lineage engine."""

    def log_message(self, fmt, *args):  # silence default logging
        logger.info(fmt, *args)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def _send_json(self, status: int, body: dict) -> None:
        payload = json.dumps(body, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._send_json(200, {
                "status": "ok",
                "seed":   f"{SEED.real}+{SEED.imag}i",
                "tiers":  list(TIER_CONSTANTS),
            })
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self._read_body()
        except Exception as exc:
            self._send_json(400, {"error": f"invalid JSON: {exc}"})
            return

        if path == "/lineage/traverse":
            self._handle_traverse(body)
        elif path == "/lineage/step":
            self._handle_step(body)
        else:
            self._send_json(404, {"error": "not found"})

    def _handle_traverse(self, body: dict) -> None:
        entity_id   = body.get("entity_id", "unknown")
        source_tier = body.get("source_tier", "bronze")
        target_tier = body.get("target_tier", "gold")
        try:
            states = traverse(entity_id, source_tier, target_tier)
            self._send_json(200, {
                "entity_id":   entity_id,
                "source_tier": source_tier,
                "target_tier": target_tier,
                "steps":       [s.as_dict() for s in states],
                "bounded":     all(s.bounded for s in states),
            })
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})

    def _handle_step(self, body: dict) -> None:
        entity_id = body.get("entity_id", "unknown")
        tier      = body.get("tier", "bronze")
        z_real    = float(body.get("z_real",      SEED.real))
        z_imag    = float(body.get("z_imaginary", SEED.imag))
        z         = complex(z_real, z_imag)
        try:
            state = step_tier(tier, z)
            self._send_json(200, {
                "entity_id": f"{entity_id}_{tier}",
                "tier":      tier,
                **state.as_dict(),
            })
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})


def main() -> None:
    server = HTTPServer((HOST, PORT), LineageHandler)
    logger.info("Fractal Lineage Engine listening on %s:%d", HOST, PORT)
    logger.info("Seed z₀ = %s+%si  |  Tiers: %s", SEED.real, SEED.imag, list(TIER_CONSTANTS))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
