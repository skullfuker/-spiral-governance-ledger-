# Spiral Governance Ledger

This repository contains local demo tooling for stewardship manifest generation and audit validation. It is not production-ready and must not be used to rotate real keys or validate live AWS WORM/KMS state until the remaining remediation steps are completed.

## Current status

The following items must be completed before any production use:

- restore or merge the original project README as needed
- remove tracked secrets and rotate any credentials previously committed to `.env`
- replace placeholder AWS role ARNs and OIDC trust configurations
- fix manifest path mismatches between workflow and scripts
- replace demo/local logic with reviewed AWS implementations that perform actual key rotation and remote verification

## Repository layout

```text
.
├── .github/
│   └── workflows/
│       ├── steward-key-rotation.yml
│       └── verify-manifest.yml
├── docs/
├── scripts/
│   ├── audit_worm_vault.py
│   ├── rotate_steward_keys.py
│   └── steward_webhook_notifier.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── package.json
├── LICENSE
├── SECURITY.md
└── verify_manifest.sh
```

## Security warning

- Do not run the steward key rotation workflow against production.
- Do not use the scripts in this repository as a replacement for actual AWS KMS, S3 Object Lock, or IAM validation.
- Treat all manifests, logs, and webhook payloads as security-sensitive metadata.
- Keep secrets in environment variables or a local untracked `.env` file; do not commit them to Git.

## Local setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Example local validation only

```bash
python scripts/rotate_steward_keys.py --test --manifest-path build/manifests/latest.json
python scripts/audit_worm_vault.py --verify-latest --manifest-path build/manifests/latest.json
```

## Required remediation before production

1. Restore or merge the original project README.
2. Remove tracked secret files from the repository and rotate all credentials they exposed.
3. Replace placeholder AWS role ARNs with the real IAM role.
4. Configure the AWS OIDC trust policy so it only allows the expected repository and branch.
5. Align manifest paths across workflow and script definitions.
6. Replace local/demo implementations with reviewed AWS logic that performs actual rotation and verification.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
