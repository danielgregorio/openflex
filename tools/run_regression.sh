#!/bin/bash
# Regression Test Runner for OpenFlex Neo
# Run this script after major changes to verify integrity

set -e  # Exit on error

echo "=========================================="
echo "OpenFlex Neo - Regression Test Suite"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Navigate to project root
cd "$(dirname "$0")/.."

echo "📍 Working directory: $(pwd)"
echo ""

# Function to run tests and capture results
run_test_suite() {
    local suite_name=$1
    local test_path=$2
    local description=$3

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🧪 Testing: $suite_name"
    echo "   $description"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if python -m pytest "$test_path" -v --tb=short 2>&1 | tee /tmp/test_output.txt; then
        echo -e "${GREEN}✅ $suite_name: PASSED${NC}"
        return 0
    else
        echo -e "${RED}❌ $suite_name: FAILED${NC}"
        return 1
    fi
}

# Track overall status
FAILED_SUITES=()
PASSED_SUITES=()

# 1. Core Parser Tests
if run_test_suite "AS4 Parser" "tests/parser/test_as4_parser.py" "Core AS4 parsing functionality"; then
    PASSED_SUITES+=("AS4 Parser")
else
    FAILED_SUITES+=("AS4 Parser")
fi
echo ""

# 2. Type Checker Tests
if run_test_suite "Type Checker" "tests/analyzer/test_type_checker.py" "Type validation and inference"; then
    PASSED_SUITES+=("Type Checker")
else
    FAILED_SUITES+=("Type Checker")
fi
echo ""

# 3. MXML Parser Tests
if run_test_suite "MXML Parser" "tests/parser/test_mxml_basic.py" "MXML parsing basics"; then
    PASSED_SUITES+=("MXML Parser")
else
    FAILED_SUITES+=("MXML Parser")
fi
echo ""

# 4. MXML Integration Tests
if run_test_suite "MXML Integration" "tests/parser/test_mxml_integration.py" "End-to-end MXML parsing"; then
    PASSED_SUITES+=("MXML Integration")
else
    FAILED_SUITES+=("MXML Integration")
fi
echo ""

# 5. AS4 Features Regression Tests
if run_test_suite "AS4 Features" "tests/regression/test_as4_features.py" "Regression tests for AS4 features"; then
    PASSED_SUITES+=("AS4 Features")
else
    FAILED_SUITES+=("AS4 Features")
fi
echo ""

# Summary
echo "=========================================="
echo "📊 REGRESSION TEST SUMMARY"
echo "=========================================="
echo ""

if [ ${#PASSED_SUITES[@]} -gt 0 ]; then
    echo -e "${GREEN}✅ Passed (${#PASSED_SUITES[@]}):${NC}"
    for suite in "${PASSED_SUITES[@]}"; do
        echo "   - $suite"
    done
    echo ""
fi

if [ ${#FAILED_SUITES[@]} -gt 0 ]; then
    echo -e "${RED}❌ Failed (${#FAILED_SUITES[@]}):${NC}"
    for suite in "${FAILED_SUITES[@]}"; do
        echo "   - $suite"
    done
    echo ""
fi

# Calculate pass rate
TOTAL=$((${#PASSED_SUITES[@]} + ${#FAILED_SUITES[@]}))
PASS_RATE=$((${#PASSED_SUITES[@]} * 100 / TOTAL))

echo "Pass Rate: ${PASS_RATE}% (${#PASSED_SUITES[@]}/$TOTAL)"
echo ""

if [ ${#FAILED_SUITES[@]} -eq 0 ]; then
    echo -e "${GREEN}🎉 All regression tests passed!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please review the output above.${NC}"
    exit 1
fi
