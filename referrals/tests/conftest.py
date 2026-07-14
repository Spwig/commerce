"""
Local conftest for referrals/tests/.

Provides autouse core-infrastructure fixtures the shared ``tests/conftest.py``
defines. This is required because the referrals tests use Django's ``TestCase``
(not pytest fixtures) but still hit ``ReferralProgram.get_program()`` which
calls ``get_default_currency()`` → ``SiteSettings.get_settings()``. Without a
SiteSettings row with a non-blank ``admin_email``, ``get_or_create`` raises
``ValidationError``.

* ``_referrals_site_settings`` -- autouse: materialises a single-tenant
  ``SiteSettings`` row so currency/i18n middleware can resolve without
  triggering ``full_clean`` on an empty ``admin_email`` field.
* ``_referrals_django_site`` -- autouse: ensures the ``django.contrib.sites``
  framework has a Site with ``id=1`` (matches ``SITE_ID = 1`` invariant).
"""

import pytest


@pytest.fixture(autouse=True)
def _referrals_site_settings(db):
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
def _referrals_django_site(db):
    """Ensure Django Sites framework has a site with ID=1."""
    from django.contrib.sites.models import Site

    site, _ = Site.objects.get_or_create(
        id=1, defaults={"domain": "localhost", "name": "Test Site"}
    )
    return site
