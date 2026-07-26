"""
Local conftest for wallet/tests/.

``tests/conftest.py`` is not visible from an app-level test package, so the
single-tenant infrastructure fixtures every wallet operation depends on are
re-declared here. ``WalletService.get_balance`` falls through to
``get_default_currency()`` → ``SiteSettings.get_settings()``, which raises
``ValidationError`` without a SiteSettings row carrying a non-blank
``admin_email``.
"""

import pytest


@pytest.fixture(autouse=True)
def _wallet_site_settings(db):
    """Create SiteSettings required for single-tenant operation."""
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
def _wallet_django_site(db):
    """Ensure Django Sites framework has a site with ID=1 (SITE_ID = 1)."""
    from django.contrib.sites.models import Site

    site, _ = Site.objects.get_or_create(
        id=1, defaults={"domain": "localhost", "name": "Test Site"}
    )
    return site
