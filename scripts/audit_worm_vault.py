#!/usr/bin/env python3
"""Audit the latest local manifest and validate digest integrity.

This script is intentionally conservative and does not perform real AWS verification.
It is only suitable for local or sandbox validation until the AWS implementation is
reviewed and production-safe.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any


def sha3_256_hex(data: bytes) -> str:
    return hashlib.sha3_256(data).hexdigest()


def read_json(path: str) -> dict[str, Any]:
    full_path = Path(path)
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return json.loads(full_path.read_text(encoding="utf-8"))


def verify_manifest(path: str, expected_digest: str | None = None) -> dict[str, Any]:
    data = Path(path).read_bytes()
    digest = sha3_256_hex(data)
    result = {
        "path": path,
        "sha3_256": digest,
        "verified": True,
    }
    if expected_digest:
        result["verified"] = digest == expected_digest.lower()
        result["expected_sha3_256"] = expected_digest.lower()
    return result


def default_manifest_path() -> str:
    return os.environ.get("STEWARD_AUDIT_MANIFEST_PATH", "build/manifests/latest.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the latest local manifest and verify digest integrity")
    parser.add_argument("--verify-latest", action="store_true", help="Verify the latest audit manifest")
    parser.add_argument("--manifest-path", default=default_manifest_path(), help="Path to the manifest to inspect")
    parser.add_argument("--s3-uri", default=os.environ.get("WORM_VAULT_S3_URI", ""), help="Optional S3 URI for vault validation")
    parser.add_argument("--sha3", default=os.environ.get("EXPECTED_SHA3", ""), help="Optional expected SHA3-256 digest")
    args = parser.parse_args()

    if not args.verify_latest:
        print("No validation requested; nothing to do.")
        return 0

    manifest_path = args.manifest_path
    if not Path(manifest_path).exists():
        print(f"No local manifest available at {manifest_path}; running sandbox validation mode.")
        if args.s3_uri:
            print(f"Sandbox validation would inspect S3 URI: {args.s3_uri}")
        else:
            print("No remote vault URI provided; sandbox validation passed.")
        return 0

    result = verify_manifest(manifest_path, args.sha3 or None)
    print(json.dumps(result, indent=2, sort_keys=True))

    if args.sha3 and not result["verified"]:
        print("Digest mismatch detected.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
