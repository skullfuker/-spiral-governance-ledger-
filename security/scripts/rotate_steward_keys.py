#!/usr/bin/env python3
import os
import sys
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Steward Key Rotation Script")
    parser.add_argument(
        "--mode",
        choices=["dry-run", "production-check"],
        default="dry-run",
        help="Only production-check is allowed for live AWS validation."
    )
    parser.add_argument(
        "--force",
        type=str,
        default="false",
        help="Force rotation override."
    )

    args = parser.parse_args()

    print(f"[INFO] Initializing Steward Key Rotation in mode: {args.mode}")

    if args.mode == "production-check":
        required = [
            "AWS_REGION",
            "AWS_KMS_KEY_ID",
            "AWS_S3_BUCKET",
            "AWS_ROLE_ARN",
        ]
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            print(f"[ERROR] Missing required AWS values for production-check: {missing}", file=sys.stderr)
            sys.exit(1)
        print("[SUCCESS] Production environment variables verified.")
    else:
        print("[INFO] Running in dry-run mode. No production keys modified.")

    os.makedirs("build/manifests", exist_ok=True)
    manifest_path = os.getenv("STEWARD_AUDIT_MANIFEST_PATH", "build/manifests/latest.json")
    
    manifest = {
        "status": "DEMO_DRY_RUN_NON_PRODUCTION" if args.mode != "production-check" else "PRODUCTION_VERIFIED",
        "mode": args.mode,
        "force": args.force
    }
    
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"[SUCCESS] Manifest written to {manifest_path}")

if __name__ == "__main__":
    main()
