name: CI

on:
  push:
    branches:
      - spiral-governance-ledge
      - 'fix/**'
      - 'security/**'
  pull_request:
    branches:
      - spiral-governance-ledge

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    env:
      MIN_COVERAGE_THRESHOLD: "95"

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          set -euo pipefail
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then
            python -m pip install -r requirements.txt
          fi
          python -m pip install pytest==8.3.2 pytest-cov==5.0.0

      - name: Run pytest with coverage
        shell: bash
        env:
          PYTHONPATH: ${{ github.workspace }}
        run: |
          set -euo pipefail
          python -m pytest -q --maxfail=1 \
            --cov=. \
            --cov-report=term-missing \
            --cov-report=xml:coverage.xml \
            --cov-fail-under="${MIN_COVERAGE_THRESHOLD}"

      - name: Upload coverage artifact
        if: always() && hashFiles('coverage.xml') != ''
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml