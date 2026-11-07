#!/usr/bin/env python3
"""Send a minimal Steward rotation notification with a SHA3-256 manifest digest.

Required environment variables:
  STEWARD_WEBHOOK_URL       HTTPS Discord webhook URL or Slack incoming webhook URL
  STEWARD_WEBHOOK_PLATFORM  "discord" or "slack"
  STEWARD_NODE_ID           Public/non-secret node identifier
  STEWARD_KEY_ID            Public/non-secret key identifier
  STEWARD_STATUS            Non-secret event status, e.g. ROTATION_SUCCESS
  AUDIT_MANIFEST_PATH       Path to the generated audit manifest

The manifest contents and secret key material are never included in the message;
only the SHA3-256 digest is sent.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Required environment variable is missing: {name}")
    return value


def manifest_digest(path: Path) -> str:
    if not path.is_file():
        raise ValueError("Audit manifest file does not exist or is not a regular file")
    digest = hashlib.sha3_256()
    with path.open("rb") as manifest:
        for chunk in iter(lambda: manifest.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_payload(platform: str, node_id: str, key_id: str, status: str,
                  digest: str, timestamp: str) -> dict:
    title = f"Steward Key Rotation: {status}"
    fields = [
        {"name": "Node ID", "value": node_id, "inline": True},
        {"name": "Key ID", "value": key_id, "inline": True},
        {"name": "SHA3-256 Manifest Digest", "value": f"`sha3-256:{digest}`", "inline": False},
        {"name": "Timestamp (UTC)", "value": timestamp, "inline": True},
        {"name": "Status", "value": status, "inline": True},
    ]

    if platform == "discord":
        return {
            "username": "Sovereign Lattice Sentinel",
            "embeds": [{
                "title": title,
                "color": 3055683,
                "fields": fields,
                "footer": {"text": "Steward key rotation audit"},
            }],
        }

    if platform == "slack":
        slack_fields = [
            {"title": field["name"], "value": field["value"], "short": field["inline"]}
            for field in fields
        ]
        return {
            "username": "Sovereign Lattice Sentinel",
            "attachments": [{
                "color": "#2e9b63",
                "title": title,
                "fields": slack_fields,
                "footer": "Steward key rotation audit",
                "ts": int(datetime.now(timezone.utc).timestamp()),
            }],
        }

    raise ValueError("STEWARD_WEBHOOK_PLATFORM must be 'discord' or 'slack'")


def main() -> int:
    try:
        webhook = required_env("STEWARD_WEBHOOK_URL")
        parsed = urllib.parse.urlparse(webhook)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("Webhook URL must be a valid HTTPS URL")

        platform = required_env("STEWARD_WEBHOOK_PLATFORM").lower()
        node_id = required_env("STEWARD_NODE_ID")
        key_id = required_env("STEWARD_KEY_ID")
        status = required_env("STEWARD_STATUS")
        manifest_path = Path(required_env("AUDIT_MANIFEST_PATH"))
        digest = manifest_digest(manifest_path)
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        payload = build_payload(platform, node_id, key_id, status, digest, timestamp)

        request = urllib.request.Request(
            webhook,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "steward-webhook-notifier/1.0"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            if not 200 <= response.status < 300:
                raise RuntimeError(f"Webhook returned HTTP status {response.status}")
        print(f"Notification sent ({platform}); SHA3-256 digest: {digest}")
        return 0
    except (OSError, ValueError, RuntimeError, urllib.error.URLError):
        # Do not print exception details: they may contain the secret webhook URL.
        print("Notification failed; check the webhook secret, manifest, and notifier configuration.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
