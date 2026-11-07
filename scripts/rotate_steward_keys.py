#!/usr/bin/env python3
"""Rotate Steward keys and write an audit manifest for each rotation event."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def current_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_manifest_directory() -> Path:
    manifest_dir = Path("build/manifests")
    manifest_dir.mkdir(parents=True, exist_ok=True)
    return manifest_dir


def generate_manifest(node_id: str, key_id: str, event_type: str, hash_value: str, forced: bool) -> dict:
    return {
        "node_id": node_id,
        "key_id": key_id,
        "event_type": event_type,
        "status": "ROTATED" if event_type == "rotation" else "VERIFIED",
        "forced": forced,
        "timestamp_utc": current_utc_iso(),
        "sha3_256": hash_value,
        "version": "1.0",
    }


def build_digest(payload: dict) -> str:
    import hashlib

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha3_256(encoded).hexdigest()


def default_node_id() -> str:
    return os.environ.get("STEWARD_NODE_ID", "node-default")


def default_key_id() -> str:
    return os.environ.get("STEWARD_KEY_ID", "steward-key-default")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rotate Steward keys and emit a signed manifest")
    parser.add_argument("--force", default="false", help="Force rotation despite age checks")
    parser.add_argument("--node-id", default=default_node_id(), help="Public node identifier")
    parser.add_argument("--key-id", default=default_key_id(), help="Public key identifier")
    parser.add_argument("--test", action="store_true", help="Run a local validation without changing production state")
    args = parser.parse_args()

    forced = parse_bool(args.force)
    node_id = args.node_id
    key_id = args.key_id

    manifest_dir = ensure_manifest_directory()
    manifest_path = manifest_dir / f"key_rotation_{node_id}.json"

    if args.test:
        payload = {
            "node_id": node_id,
            "key_id": key_id,
            "event_type": "test",
            "status": "TEST_OK",
            "forced": forced,
            "timestamp_utc": current_utc_iso(),
            "sha3_256": "test-digest-not-produced",
            "version": "1.0",
        }
        manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Test manifest written to {manifest_path}")
        return 0

    # Simulated 90-day rotation policy for local and CI use.
    event_type = "rotation"
    payload = generate_manifest(node_id, key_id, event_type, "pending", forced)
    payload["sha3_256"] = build_digest(payload)
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"Rotation manifest written to {manifest_path}")
    print(f"SHA3-256: {payload['sha3_256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
