"""
Contract test fixtures and utilities
"""

import json
import os
from pathlib import Path
from typing import Any

import pytest
from rest_framework.test import APIClient

# Schema baseline directory
SCHEMA_DIR = Path(__file__).parent / "schemas"

# Environment flag set by scripts/generate_contract_baselines.py. When on, a
# contract test that finds no baseline records one from the live response
# instead of skipping.
RECORD_ENV_VAR = "SPWIG_RECORD_CONTRACTS"


def recording_enabled() -> bool:
    """True when baselines should be recorded rather than asserted against."""
    return os.environ.get(RECORD_ENV_VAR) == "1"


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


def _unpin_nulls(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Rewrite ``{"type": "null"}`` nodes to the unpinned sentinel, recursively.

    A baseline recorded from one response cannot distinguish "this field is
    always null" from "this field happened to be null in the fixture". Recording
    the observed ``null`` would pin the contract to the fixture: a product that
    *does* have a brand would then fail with
    ``brand_name: Incorrect type. Expected: null, Got: string``, and the
    breaking-change detector would report a break that never happened.

    Presence is the assertion worth keeping; the type of a null is not knowable
    from the sample, so it is left unpinned. Populate the fixture if you want a
    field's type genuinely pinned.
    """
    from tests.contract.utils.contract_validator import UNPINNED_TYPE

    node = dict(schema)

    if node.get("type") == "null":
        node["type"] = UNPINNED_TYPE
        node["nullable"] = True

    if "properties" in node:
        node["properties"] = {k: _unpin_nulls(v) for k, v in node["properties"].items()}

    items = node.get("items")
    if isinstance(items, dict) and items:
        node["items"] = _unpin_nulls(items)

    return node


def record_or_skip(
    api_module: str,
    serializer_name: str,
    response_data: dict[str, Any],
    version: str = "v1",
):
    """
    Handle a missing baseline.

    In record mode (``SPWIG_RECORD_CONTRACTS=1``, set by
    ``scripts/generate_contract_baselines.py``) this writes the baseline from the
    live response and skips. Otherwise it skips with instructions.

    Baselines are recorded with :func:`extract_response_schema` — the same
    function the assertions compare against. Do **not** substitute
    ``generate_serializer_schema``: it marks only required, non-read-only fields
    as required, whereas response extraction marks every present key, so mixing
    the two reports breaking changes that have not happened.

    Call from a contract test's ``except FileNotFoundError`` branch::

        except FileNotFoundError:
            record_or_skip(self.SCHEMA_MODULE, self.SERIALIZER_NAME, product_data)
    """
    from tests.contract.utils.contract_validator import extract_response_schema

    if recording_enabled():
        schema = _unpin_nulls(extract_response_schema(response_data))
        save_schema_baseline(api_module, serializer_name, schema, version=version)
        pytest.skip(f"Recorded baseline for {api_module}/{version}/{serializer_name}")

    pytest.skip(
        f"No baseline for {api_module}/{version}/{serializer_name}. "
        f"Generate with: python scripts/generate_contract_baselines.py "
        f"--module {api_module} --serializer {serializer_name}"
    )
