#!/usr/bin/env python3
"""Validate a local demo manifest only; this is not an AWS/WORM audit."""

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
        help="Production verification is intentionally unavailable in this demo implementation.",
    )
    parser.add_argument(
        "--manifest-path",
        default=os.environ.get("STEWARD_AUDIT_MANIFEST_PATH", "build/manifests/latest.json"),
    )
    args = parser.parse_args()

    if args.mode == "production-check":
        print(
            "ERROR: live S3 Object Lock/KMS verification is not implemented; refusing to report success.",
            file=sys.stderr,
        )
        return 2

    path = Path(args.manifest_path)
    if not path.is_file():
        print(f"ERROR: demo manifest not found: {path}", file=sys.stderr)
        return 1
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read valid JSON manifest: {exc}", file=sys.stderr)
        return 1

    if data.get("status") != "DEMO_DRY_RUN_NON_PRODUCTION":
        print("ERROR: refusing to label a non-demo manifest as locally validated.", file=sys.stderr)
        return 1
    if data.get("key_rotation_performed") is not False or data.get("aws_contacted") is not False:
        print("ERROR: manifest demo markers are missing or inconsistent.", file=sys.stderr)
        return 1

    print(f"Local demo manifest is valid: {path}. This is NOT an AWS/WORM audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
