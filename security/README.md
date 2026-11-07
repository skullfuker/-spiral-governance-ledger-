# Sovereign Lattice (Coil ID: 77-AE-VIGILANCE)

> **CRITICAL SECURITY NOTICE**: This repository is currently in a **NON-PRODUCTION / DEMO DRY-RUN STATE**. 
> - The automated key rotation workflow is strictly manual-only (`workflow_dispatch`) and must not be run against production environments until verified AWS OIDC roles and production-checked scripts are fully deployed.
> - **Never commit secrets, `.env` files, or private keys.**

## Architecture Overview

The Sovereign Lattice is a non-extractive, non-profit governance system designed for stewardship, survivor-led accountability, and the correction of structural systemic betrayal.

## Security & Remediation Guidelines

1. **No Production Execution**: Workflows run strictly in dry-run or demo mode unless explicit `production-check` environmental variables and verified OIDC roles are configured.
2. **Secret Hygiene**: Tracked secret files have been purged from git history. Always use local environment variables or GitHub Secrets.
3. **Fail-Closed Scripts**: Rotation and audit scripts enforce strict validation checks and will fail closed if required parameters are missing.

## Local Setup & Testing

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest test/ -v 
