# Spiral Governance Ledger

> **Security status: NOT PRODUCTION-READY for key rotation or AWS vault operations.** Do not use the key rotation workflow against production.

This repository contains governance documentation and local/demo tooling. The scripts and workflow do not perform real key rotation or verify AWS KMS or S3 Object Lock state. A successful demo run is not evidence of production validation.

For the repository's governance and architecture material, see [`SOVEREIGN_GOVERNANCE_README.md`](SOVEREIGN_GOVERNANCE_README.md).

## Local demo checks

Use Python 3.11 or newer. These commands create and validate a local demo manifest only:

```bash
python scripts/rotate_steward_keys.py --mode dry-run
python scripts/audit_worm_vault.py --mode dry-run
```

The `production-check` mode intentionally exits with an error. Supplying AWS environment variables does not turn these demo scripts into production implementations.

## Secret handling

- Never commit `.env` files, credentials, private keys, or certificates.
- `.gitignore` prevents many new untracked secret files from being added, but it does not untrack files already committed or remove past versions from Git history.
- The repository previously tracked `.env`. Rotate any real credentials that may have appeared there, remove the file from tracking with `git rm --cached .env`, and coordinate a separate history rewrite before claiming history is clean.

## Production prerequisites (not yet satisfied)

Before any production use, independently design, review, test, and approve actual AWS key lifecycle operations, least-privilege IAM/OIDC trust, S3 Object Lock verification, KMS key-state verification, audit artifact integrity, and operational recovery procedures. Do not add a production trigger until those controls are implemented and reviewed.
