"""
Integration test fixtures — API client setup + shared infrastructure.
"""

import pytest
from django.test import Client
from rest_framework.test import APIClient

# ============================================================
# Email account fixture for preference integration cluster
# ============================================================
#
# Many preference-integration tests exercise ``EmailSendingService`` end to
# end. The service raises ``ValueError("No active email account available")``
# if there is no default account for the site — which used to leak stack
# traces into every affiliate/referrals test. We expose an ``email_account``
# fixture that creates a default active account tied to Site id=1.


@pytest.fixture
def email_account(_integration_django_site, _integration_site_settings):
    """Create a default active EmailAccount tied to Site id=1."""
    from tests.factories import EmailAccountFactory

    return EmailAccountFactory(default=True, site=_integration_django_site)


# ============================================================
# Core Infrastructure (single-tenant middleware needs these)
# ============================================================
#
# Middleware (currency, GeoIP, etc.) calls ``SiteSettings.get_settings()``
# on every request, which triggers ``full_clean`` on an empty row and
# raises ``ValidationError`` when ``admin_email`` is blank. The Sites
# framework also needs a Site with id=1 (see SITE_ID=1 invariant).
# We autouse these in tests/integration/ so any integration test that
# hits middleware or ``get_current_site`` works out of the box.


def _needs_db(request):
    """Return False when the test's class explicitly forbids DB access.

    SimpleTestCase-based tests use inspect / hasattr / import-time checks
    and mustn't touch the DB. When our autouse fixtures request `db`
    unconditionally they force those tests to error with
    DatabaseOperationForbidden. Return early instead.
    """
    if request.cls is None:
        return True
    from django.test import SimpleTestCase, TestCase

    return not (issubclass(request.cls, SimpleTestCase) and not issubclass(request.cls, TestCase))


@pytest.fixture(autouse=True)
def _integration_site_settings(request):
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
def _integration_django_site(request):
    """Ensure Django Sites framework has a site with id=1."""
    if not _needs_db(request):
        return None
    request.getfixturevalue("db")
    from django.contrib.sites.models import Site

    site, _ = Site.objects.get_or_create(
        id=1, defaults={"domain": "localhost", "name": "Test Site"}
    )
    return site


# ============================================================
# Communication preferences convenience shim
# ============================================================
#
# Many preference tests assume ``user.communication_preferences`` is
# populated immediately after ``UserFactory()``. There is no signal that
# auto-creates ``CommunicationPreference`` on user save — the model
# exposes ``get_or_create_for_user`` for that purpose. We monkey-patch
# ``UserFactory._create`` for the duration of a test module so tests can
# rely on the convenience accessor.
#
# We activate this only when the current test module actually imports
# ``CommunicationPreference`` or ``PreferenceService`` — that keeps the
# shim scoped to preference tests and leaves everything else untouched.


@pytest.fixture(autouse=True)
def _auto_create_communication_preferences(request, monkeypatch):
    """Auto-create CommunicationPreference for every user in preference tests."""
    module = getattr(request, "module", None)
    if module is None:
        yield
        return

    module_name = getattr(module, "__name__", "")
    preference_modules = (
        "test_communication_preferences_model",
        "test_communication_preferences_api",
        "test_communication_preferences_admin",
        "test_communication_preferences_views",
        "test_preference_service",
        "test_preference_history",
        "test_preference_analytics",
        "test_smart_defaults",
        # Phase 4b: preference-integration cluster
        "test_email_preference_integration",
        "test_sms_preference_integration",
        "test_blog_preference_integration",
        "test_affiliate_preference_integration",
        "test_referrals_preference_integration",
        "test_affiliate_monthly_reports",
    )
    if not any(module_name.endswith(name) for name in preference_modules):
        yield
        return

    from tests.factories import UserFactory

    original_create = UserFactory._create.__func__

    @classmethod
    def _create_with_prefs(cls, model_class, *args, **kwargs):
        user = original_create(cls, model_class, *args, **kwargs)
        # Create preferences using the model's own helper so app defaults,
        # unsubscribe_token, and consent metadata all get set correctly.
        from accounts.models import CommunicationPreference

        CommunicationPreference.get_or_create_for_user(user)
        return user

    monkeypatch.setattr(UserFactory, "_create", _create_with_prefs)
    yield


# ============================================================
# API / Client fixtures
# ============================================================


@pytest.fixture
def api_client():
    """Unauthenticated API client."""
    return APIClient()


@pytest.fixture
def auth_client(customer_user):
    """Authenticated API client for customer_user."""
    client = APIClient()
    client.force_authenticate(user=customer_user)
    return client


@pytest.fixture
def admin_client(admin_user):
    """Authenticated API client for admin_user."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def customer_client(customer_user):
    """Django test client authenticated as customer_user (for view tests, not API)."""
    client = Client()
    client.force_login(customer_user)
    return client
