# Spiral Governance Ledger

A Python-first repository for stewardship key rotation, audit validation, and governance tooling.

This project includes operational scripts for:
- rotating Steward keys
- auditing WORM vaults and manifests
- verifying cryptographic digests
- notifying operators via webhooks

## Repository layout

```text
.
├── .github/
│   └── workflows/
│       ├── steward-key-rotation.yml
│       └── ci.yaml
├── docs/
├── scripts/
│   ├── audit_worm_vault.py
│   ├── rotate_steward_keys.py
│   └── steward_webhook_notifier.py
├── test/
├── .gitignore
├── README.md
├── requirements.txt
├── package.json
├── LICENSE
└── SECURITY.md
```

## Prerequisites

- Python 3.11+
- Git
- Optional: AWS CLI for vault inspection
- Optional: Node.js for JavaScript tooling if present in the repo

Create a virtual environment and install dependencies:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `requirements.txt` is missing, install the minimum tools required for local development:

```bash
python -m pip install boto3 botocore pytest
```

## Local setup

Clone the repository:

```bash
git clone https://github.com/skullfuker/-spiral-governance-ledger-.git
cd -spiral-governance-ledger-
```

Do not commit secrets or private materials. Keep local secrets in environment variables or a local `.env` file, and ensure `.env` is excluded from git.

## Run tests

```bash
python -m pytest test/ -v
```

If the project uses a different test path or runner, use the commands defined by the active CI workflow in `.github/workflows/`.

## Steward key rotation

The rotation script accepts `--force`, `--node-id`, and `--test` flags.

Example:

```bash
python scripts/rotate_steward_keys.py --test
python scripts/rotate_steward_keys.py --force=true
```

This command creates a manifest under the `build/manifests/` directory and writes a digest for audit verification.

## WORM vault audit

The audit script verifies the latest manifest and supports sandbox/local validation when remote AWS access is unavailable.

Example:

```bash
python scripts/audit_worm_vault.py --verify-latest
python scripts/audit_worm_vault.py --verify-latest --sha3 <digest>
```

## GitHub Actions workflow

The scheduled workflow runs weekly and also supports manual dispatch.

Required repository variables/secrets:
- `STEWARD_WEBHOOK_URL`
- `STEWARD_NODE_ID`
- `STEWARD_KEY_ID`
- `STEWARD_WEBHOOK_PLATFORM` (optional; defaults to `discord`)
- `STEWARD_AUDIT_MANIFEST_PATH` (optional; defaults to `build/manifests/latest.json`)

Important:
- AWS OIDC credentials must be configured before any AWS-dependent key rotation or audit step executes.
- Never hardcode webhook URLs or AWS credential values in the repository.
- Only send non-sensitive identifiers and manifest digests to external channels.

## Webhook notifications

The notifier script sends a manifest digest and status summary to a configured Discord or Slack incoming webhook.

Example:

```bash
export STEWARD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
export STEWARD_WEBHOOK_PLATFORM="discord"
export STEWARD_NODE_ID="node-01"
export STEWARD_KEY_ID="ed25519_key_v2"
export STEWARD_STATUS="ROTATION_SUCCESS"
export AUDIT_MANIFEST_PATH="build/manifests/latest.json"
python scripts/steward_webhook_notifier.py
```

## Operational checklist

Before approving a production rotation:

- confirm the target node and environment
- validate the manifest file exists
- verify the digest matches the latest audit output
- ensure the AWS OIDC trust policy is restricted to the correct repository and branch
- confirm the webhook only sends non-secret metadata
- retain audit artifacts according to the project retention policy

## Security guidance

- Do not commit credentials or private keys.
- Never disclose the raw webhook URL in pull requests or issue comments.
- Do not bypass security checks to make CI green.
- Treat all audit outputs as security-sensitive data.

## Troubleshooting

Common issues:

- Missing dependency: install the project requirements and activate the virtual environment.
- Missing manifest: verify the rotation script wrote to `build/manifests/`.
- AWS access denied: verify the OIDC role trust policy and workflow permissions.
- Webhook failure: confirm the secret is configured and the endpoint is valid.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
