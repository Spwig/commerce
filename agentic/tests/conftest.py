"""Shared fixtures for the agentic test suite."""

import pytest


@pytest.fixture
def site_settings(db):
    """The single-tenant SiteSettings row (pk=1), required for pricing/currency."""
    from core.models import SiteSettings

    obj, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
        },
    )
    return obj
