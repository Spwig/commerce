"""
Local conftest for orders/tests/.

Provides the same core-infrastructure fixtures the shared ``tests/conftest.py``
defines, so tests colocated with the orders app don't have to depend on
``rootdir`` fixture discovery. Two fixtures are exposed:

* ``site_settings`` -- materialises a single-tenant ``SiteSettings`` row so
  currency/i18n middleware can resolve without triggering ``full_clean``
  on an empty ``admin_email`` field.
* ``django_site`` -- ensures the ``django.contrib.sites`` framework has a
  Site with ``id=1``, matching the ``SITE_ID = 1`` invariant.
"""

import pytest


@pytest.fixture
def site_settings(db):
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


@pytest.fixture
def django_site(db):
    """Ensure Django Sites framework has a site with ID=1."""
    from django.contrib.sites.models import Site

    site, _ = Site.objects.get_or_create(
        id=1, defaults={"domain": "localhost", "name": "Test Site"}
    )
    return site
