#!/usr/bin/env python3
"""Local demo manifest generator; it does not rotate keys or call AWS."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("dry-run", "production-check"),
        default="dry-run",
        help="Production checks are intentionally unavailable in this demo implementation.",
    )
    parser.add_argument("--force", default="false", help="Accepted for compatibility; no key action occurs.")
    args = parser.parse_args()

    if args.mode == "production-check":
        print(
            "ERROR: production key rotation is not implemented; refusing to report success.",
            file=sys.stderr,
        )
        return 2

    manifest_path = Path(
        os.environ.get("STEWARD_AUDIT_MANIFEST_PATH", "build/manifests/latest.json")
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "status": "DEMO_DRY_RUN_NON_PRODUCTION",
        "mode": "dry-run",
        "key_rotation_performed": False,
        "aws_contacted": False,
        "force_requested": args.force.strip().lower() in {"1", "true", "yes", "on"},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Demo manifest written to {manifest_path}; no key operation was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
