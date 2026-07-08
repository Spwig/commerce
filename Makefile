.PHONY: test test-fast test-e2e test-integration test-checkout test-custom-fields test-pos coverage test-deps test-all help install-hooks build-prod push-prod build-bundles test-health test-health-fast audit-admin audit-storefront audit-api audit-all audit-baseline audit-regression

# Build version - auto-read from core/version.py (single source of truth)
VERSION := $(shell python3 -c "import re; print(re.search(r'__version__\s*=\s*\"(.+?)\"', open('core/version.py').read()).group(1))" 2>/dev/null || echo "0.0.0")
REGISTRY ?= registry.spwig.com
CYTHON_MODULES ?= core,payment_providers,upgrader

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test-deps: ## Install test dependencies + Playwright browsers
	pip install -r requirements-dev.txt
	playwright install chromium

test: ## Run all pipeline tests (unit + integration, no E2E)
	pytest tests/ -v -m "not e2e"

test-fast: ## Run fast tests only (skip E2E and slow)
	pytest tests/ -v -m "not e2e and not slow"

test-e2e: ## Run E2E browser tests (requires running server)
	pytest tests/e2e/ -v

test-integration: ## Run integration/API tests only
	pytest tests/integration/ -v

test-checkout: ## Run all checkout-related tests
	pytest tests/ -v -m checkout

test-custom-fields: ## Run custom fields tests
	pytest tests/ -v -m custom_fields

test-pos: ## Run POS (point of sale) tests
	pytest tests/integration/pos/ -v

test-all: ## Run everything including E2E
	pytest tests/ -v

test-health: ## Run all site health audit tests (requires running server)
	pytest tests/audit/ -v -m site_health

test-health-fast: ## Run API-only health tests (no browser needed)
	pytest tests/audit/test_api_health.py -v

coverage: ## Run tests with coverage report
	pytest tests/ -m "not e2e" \
		--cov=cart --cov=orders --cov=shipping --cov=payment_providers --cov=catalog --cov=custom_fields --cov=pos_api --cov=pos_app \
		--cov-report=term-missing \
		--cov-report=html:htmlcov
	@echo "\n  Coverage report: htmlcov/index.html"

install-hooks: ## Install git hooks for development
	bash scripts/install-hooks.sh

lint: ## Run code quality checks (future)
	@echo "Linting not yet configured. Add ruff/mypy to requirements-dev.txt."

# =============================================================================
# Docker Build & Push (Production)
# =============================================================================

build-prod: ## Build protected production image (version from core/version.py)
	docker build -f Dockerfile.protected \
		--build-arg CYTHON_MODULES="$(CYTHON_MODULES)" \
		--build-arg BUILD_VERSION=$(VERSION) \
		-t $(REGISTRY)/shop:$(VERSION) .
	@echo "\n  Built: $(REGISTRY)/shop:$(VERSION)"

push-prod: ## Push production image to registry
	docker push $(REGISTRY)/shop:$(VERSION)
	@echo "\n  Pushed: $(REGISTRY)/shop:$(VERSION)"

build-push-prod: build-prod push-prod ## Build and push production image

# =============================================================================
# Component Bundles
# =============================================================================

build-bundles: ## Build preinstalled component packages (themes + utilities) into preinstalled/
	python manage.py build_preinstalled_packages
	@echo "\n  Bundles ready in preinstalled/"

# =============================================================================
# Site Health Audits (standalone scripts, no pytest)
# =============================================================================

audit-admin: ## Audit all admin sidebar pages (requires running server)
	python scripts/admin_sidebar_audit.py

audit-storefront: ## Audit storefront pages (requires running server)
	python scripts/site_health_audit.py --scope storefront

audit-api: ## Audit API endpoints (fast, no browser needed)
	python scripts/site_health_audit.py --scope api

audit-all: ## Run full site health audit (admin + storefront + API)
	python scripts/site_health_audit.py --scope all

audit-baseline: ## Save current audit results as baseline
	python scripts/site_health_audit.py --scope all --save-baseline

audit-regression: ## Compare current audit to saved baseline
	python scripts/site_health_audit.py --scope all --compare-baseline
