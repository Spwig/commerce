"""
Local conftest for cart/tests/.

Provides the autouse core-infrastructure fixtures the shared
``tests/conftest.py`` defines but which is not visible from an app-level test
package. Any Django test ``client`` request (and ``CartService.add_item`` via
``cart.effective_currency`` → ``SiteSettings.get_settings()``) needs a
single-tenant ``SiteSettings`` row with a non-blank ``admin_email``; without it
``get_or_create`` fails ``full_clean`` and 500s. See the referrals conftest for
the same pattern.
"""

import pytest


@pytest.fixture(autouse=True)
def _cart_site_settings(db):
    """Materialise the single-tenant SiteSettings row (idempotent)."""
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
def _cart_django_site(db):
    """Ensure the Django Sites framework has a Site with id=1 (SITE_ID=1)."""
    from django.contrib.sites.models import Site

    site, _ = Site.objects.get_or_create(
        id=1, defaults={"domain": "localhost", "name": "Test Site"}
    )
    return site
