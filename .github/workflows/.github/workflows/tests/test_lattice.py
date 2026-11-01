- name: Run Pytest Suite with Coverage & 95% Threshold Gate
  run: |
    set -euo pipefail
    echo "=== STAGE 1: RUNNING PYTEST VALIDATION & COVERAGE THRESHOLD GATE ==="

    if [ -d "tests" ] && find tests -maxdepth 1 -type f | grep -q ".py"; then
      echo "Running tests under tests/"
      pytest tests -v \
        --cov=. \
        --cov-report=term-missing \
        --cov-report=xml:coverage.xml \
        --cov-fail-under="${MIN_COVERAGE_THRESHOLD}"
    elif [ -f "test_worm_policy.py" ]; then
      echo "Running fallback test script"
      pytest test_worm_policy.py -v \
        --cov=. \
        --cov-report=term-missing \
        --cov-report=xml:coverage.xml \
        --cov-fail-under="${MIN_COVERAGE_THRESHOLD}"
    else
      echo "No Python tests found for the project."
      echo "Add test_worm_policy.py or add the real repo test files."
      exit 1
    fi