- name: Install Python test dependencies
  run: python -m pip install pytest pytest-cov

- name: Run ledger tests with coverage
  run: |
    pytest tests/test_lattice_ledger.py -v \
      --cov=lattice_ledger \
      --cov-report=term-missing \
      --cov-report=xml:coverage.xml \
      --cov-fail-under=95