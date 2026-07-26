"""
Local conftest for ``vouchers/tests/``.

Mirrors ``referrals/tests/conftest.py``. The shared ``tests/conftest.py`` is
not visible from an app-level test package, and several code paths reachable
from these tests (``core.utils.get_default_currency``, and the loyalty
auto-enrolment ``post_save`` receiver that fires whenever a ``User`` is
created) call ``SiteSettings.get_settings()``. Without a ``SiteSettings`` row
carrying a non-blank ``admin_email`` that raises ``ValidationError``.
"""

import pytest


@pytest.fixture(autouse=True)
def _vouchers_site_settings(db):
    """Materialise the single-tenant ``SiteSettings`` row."""
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
def _vouchers_django_site(db):
    """Ensure the Sites framework has ``id=1`` (the ``SITE_ID = 1`` invariant)."""
    from django.contrib.sites.models import Site

    site, _ = Site.objects.get_or_create(
        id=1, defaults={"domain": "localhost", "name": "Test Site"}
    )
    return site
