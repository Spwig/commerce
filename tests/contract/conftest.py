"""
Contract test fixtures and utilities
"""

import json
from pathlib import Path
from typing import Any

import pytest
from rest_framework.test import APIClient

# Schema baseline directory
SCHEMA_DIR = Path(__file__).parent / "schemas"


# ============================================================
# Core Infrastructure (single-tenant middleware needs these)
# ============================================================
#
# Contract tests hit real API endpoints through the currency/i18n
# middleware, which calls ``SiteSettings.get_settings()`` and
# ``full_clean`` on every request — raising ``ValidationError`` when
# ``admin_email`` is blank. Autouse these so any contract test that
# makes an HTTP call works out of the box.


def _needs_db(request):
    """Return False when the test's class explicitly forbids DB access."""
    if request.cls is None:
        return True
    from django.test import SimpleTestCase, TestCase

    return not (issubclass(request.cls, SimpleTestCase) and not issubclass(request.cls, TestCase))


@pytest.fixture(autouse=True)
def _contract_site_settings(request):
    """Create SiteSettings so currency/i18n middleware can resolve."""
    if not _needs_db(request):
        return None
    request.getfixturevalue("db")
    from core.models import SiteSettings

    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )
    return settings


@pytest.fixture(autouse=True)
def _contract_django_site(request):
    """Ensure Django Sites framework has a site with id=1."""
    if not _needs_db(request):
        return None
    request.getfixturevalue("db")
    from django.contrib.sites.models import Site

    site, _ = Site.objects.get_or_create(
        id=1, defaults={"domain": "localhost", "name": "Test Site"}
    )
    return site


@pytest.fixture
def contract_client(db):
    """API client for contract testing"""
    client = APIClient()
    return client


@pytest.fixture
def auth_contract_client(db, customer_user):
    """Authenticated API client for contract testing"""
    client = APIClient()
    client.force_authenticate(user=customer_user)
    return client


@pytest.fixture
def admin_contract_client(db, admin_user):
    """Admin API client for contract testing"""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


def load_schema_baseline(
    api_module: str, serializer_name: str, version: str = "v1"
) -> dict[str, Any]:
    """
    Load baseline schema from version-controlled JSON file

    Args:
        api_module: Module name (e.g., 'catalog', 'cart')
        serializer_name: Serializer class name (e.g., 'ProductListSerializer')
        version: API version (default: 'v1')

    Returns:
        Dict containing the baseline schema

    Raises:
        FileNotFoundError: If baseline schema file doesn't exist
    """
    schema_path = SCHEMA_DIR / api_module / version / f"{serializer_name}.json"
    if not schema_path.exists():
        raise FileNotFoundError(
            f"Baseline schema not found: {schema_path}\n"
            f"Run: python scripts/generate_contract_baselines.py --module {api_module} "
            f"--serializer {serializer_name}"
        )

    with open(schema_path) as f:
        return json.load(f)


def save_schema_baseline(
    api_module: str, serializer_name: str, schema: dict[str, Any], version: str = "v1"
):
    """
    Save schema as baseline (only run when updating contracts)

    Args:
        api_module: Module name (e.g., 'catalog', 'cart')
        serializer_name: Serializer class name
        schema: Schema dict to save
        version: API version (default: 'v1')
    """
    schema_dir = SCHEMA_DIR / api_module / version
    schema_dir.mkdir(parents=True, exist_ok=True)

    schema_path = schema_dir / f"{serializer_name}.json"
    with open(schema_path, "w") as f:
        json.dump(schema, f, indent=2, sort_keys=True)
