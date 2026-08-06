"""
Local conftest for subscriptions/tests/.

The pytest-style modules here (test_manager.py, test_billing_cycle.py) need a
single-tenant ``SiteSettings`` row: the renewal-order path
(``SubscriptionManager._create_renewal_order``) calls
``SiteSettings.get_settings()`` → ``get_or_create(pk=1)`` which fails
``full_clean`` on a blank ``admin_email``. The existing TestCase-based modules
(test_models.py, test_api.py) create it themselves via ``_ensure_site_settings``;
these autouse fixtures make it available to the fixture-based tests too. Mirrors
referrals/tests/conftest.py.
"""

import pytest


@pytest.fixture(autouse=True)
def _subscriptions_site_settings(db):
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
def _subscriptions_django_site(db):
    """Ensure the Django Sites framework has a Site with id=1 (SITE_ID=1)."""
    from django.contrib.sites.models import Site

    site, _ = Site.objects.get_or_create(
        id=1, defaults={"domain": "localhost", "name": "Test Site"}
    )
    return site
