#!/usr/bin/env bash
set -euo pipefail

MANIFEST="${1:-manifest.json}"

usage() {
  cat <<EOF
Usage: $0 <command> [manifest.json]
Commands:
  genkeys               Generate Ed25519 keypair (privkey.pem, pubkey.pem)
  canonicalize [file]   Canonicalize JSON using RFC8785 -> canonical.json
  sign [file]           Sign canonical.json with privkey.pem -> manifest.sig (base64)
  verify [file]         Verify manifest.sig (base64) against canonical.json using pubkey.pem
  leaf [file]           Produce SHA-256 leaf hash (hex) of canonical.json -> manifest.leaf.hex
  all [file]            Run canonicalize, sign, leaf in sequence
EOF
  exit 1
}

require_file() {
  if [ ! -f "$1" ]; then
    echo "ERROR: required file not found: $1" >&2
    exit 2
  fi
}

cmd="${1:-help}"
case "$cmd" in
  genkeys)
    echo "Generating Ed25519 keypair (privkey.pem, pubkey.pem)..."
    openssl genpkey -algorithm Ed25519 -out privkey.pem
    openssl pkey -in privkey.pem -pubout -out pubkey.pem
    echo "Done. Keep privkey.pem secret."
    exit 0
    ;;
  canonicalize)
    infile="${2:-manifest.json}"
    require_file "$infile"
    echo "Canonicalizing '$infile' (RFC8785) -> canonical.json"
    python - <<'PY' "$infile"
import sys, json
try:
    import rfc8785
except Exception:
    sys.exit("Missing Python dependency: pip install rfc8785")
infile = sys.argv[1]
# Load JSON
with open(infile, 'rb') as f:
    obj = json.load(f)
# Use rfc8785.dumps to get canonical bytes
canonical_bytes = rfc8785.dumps(obj)
with open('canonical.json', 'wb') as out:
    out.write(canonical_bytes)
PY
    echo "Canonical bytes written to canonical.json"
    exit 0
    ;;
  sign)
    infile="${2:-canonical.json}"
    require_file "$infile"
    require_file "privkey.pem"
    echo "Signing '$infile' with privkey.pem (Ed25519) -> manifest.sig (base64)"
    openssl pkeyutl -sign -inkey privkey.pem -in "$infile" -out manifest.sig.bin
    base64 manifest.sig.bin > manifest.sig
    rm -f manifest.sig.bin
    echo "Signature (base64) written to manifest.sig"
    exit 0
    ;;
  verify)
    infile="${2:-canonical.json}"
    require_file "$infile"
    require_file "pubkey.pem"
    require_file "manifest.sig"
    echo "Verifying manifest.sig against '$infile' using pubkey.pem..."
    base64 -d manifest.sig > manifest.sig.bin
    if openssl pkeyutl -verify -pubin -inkey pubkey.pem -sigfile manifest.sig.bin -in "$infile" >/dev/null 2>&1; then
      echo "Signature Verified Successfully"
      rm -f manifest.sig.bin
      exit 0
    else
      echo "Signature Verification FAILED" >&2
      rm -f manifest.sig.bin
      exit 3
    fi
    ;;
  leaf)
    infile="${2:-canonical.json}"
    require_file "$infile"
    echo "Computing SHA-256 leaf (hex) of '$infile' -> manifest.leaf.hex"
    openssl dgst -sha256 -hex "$infile" | awk '{print $2}' > manifest.leaf.hex
    echo "Leaf hex written to manifest.leaf.hex"
    echo "Leaf: $(cat manifest.leaf.hex)"
    exit 0
    ;;
  all)
    infile="${2:-manifest.json}"
    "$0" canonicalize "$infile"
    "$0" sign canonical.json
    "$0" leaf canonical.json
    echo "All steps complete. Files produced: canonical.json, manifest.sig, manifest.leaf.hex"
    exit 0
    ;;
  *)
    usage
    ;;
esac
