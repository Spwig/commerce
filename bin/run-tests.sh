#!/usr/bin/env bash
# ============================================================
# Spwig Release Test Runner
# Usage: ./bin/run-tests.sh [suite] [extra pytest args...]
#
# Suites:
#   all          Run everything including E2E (default)
#   fast         Skip E2E and slow tests
#   integration  API/service tests only
#   e2e          Browser tests only
#   checkout     All checkout-related tests
#   coverage     Tests with coverage report
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

SUITE="${1:-all}"
shift 2>/dev/null || true

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${CYAN}[test]${NC} $*"; }
warn() { echo -e "${YELLOW}[warn]${NC} $*"; }
fail() { echo -e "${RED}[fail]${NC} $*"; exit 1; }
ok()   { echo -e "${GREEN}[ok]${NC} $*"; }

# ----------------------------------------------------------
# 1. Check prerequisites
# ----------------------------------------------------------
command -v python3 >/dev/null 2>&1 || fail "python3 not found"
command -v pip >/dev/null 2>&1     || fail "pip not found"

# Check test deps installed
if ! python3 -c "import pytest" 2>/dev/null; then
    warn "pytest not installed. Installing test dependencies..."
    pip install -r requirements-dev.txt -q
fi

# For E2E: check Playwright browsers
if [[ "$SUITE" == "e2e" || "$SUITE" == "all" ]]; then
    if ! python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
        warn "Playwright not installed. Installing..."
        pip install pytest-playwright -q
        playwright install chromium
    fi
fi

# ----------------------------------------------------------
# 2. Run tests
# ----------------------------------------------------------
log "Running test suite: ${CYAN}${SUITE}${NC}"
echo ""

case "$SUITE" in
    all)
        pytest tests/ -v "$@"
        ;;
    fast)
        pytest tests/ -v -m "not e2e and not slow" "$@"
        ;;
    integration)
        pytest tests/integration/ -v "$@"
        ;;
    e2e)
        pytest tests/e2e/ -v "$@"
        ;;
    checkout)
        pytest tests/ -v -m checkout "$@"
        ;;
    coverage)
        pytest tests/ -m "not e2e" \
            --cov=cart --cov=orders --cov=shipping --cov=payment_providers --cov=catalog \
            --cov-report=term-missing \
            --cov-report=html:htmlcov \
            "$@"
        ok "Coverage report: htmlcov/index.html"
        ;;
    *)
        fail "Unknown suite: $SUITE. Use: all, fast, integration, e2e, checkout, coverage"
        ;;
esac

echo ""
ok "Test suite '${SUITE}' completed successfully."
