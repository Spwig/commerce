"""
Communication Preferences Admin Tests.

Tests Django admin interface for CommunicationPreference model including
list display, filters, actions, and SiteSettings integration.
"""

import csv
from io import StringIO

import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.test import RequestFactory

from accounts.admin import CommunicationPreferenceAdmin
from accounts.models import CommunicationPreference
from core.models import SiteSettings
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.admin_tests]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def admin_site():
    """Django admin site instance."""
    return AdminSite()


@pytest.fixture
def preference_admin(admin_site):
    """CommunicationPreferenceAdmin instance."""
    return CommunicationPreferenceAdmin(CommunicationPreference, admin_site)


@pytest.fixture
def request_factory():
    """Django request factory."""
    return RequestFactory()


@pytest.fixture
def preferences_admin_user(db):
    """Staff user with admin access (distinct from shared ``admin_user``)."""
    user = UserFactory()
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user


def _messages_enabled_request(request_factory, user):
    """Build a GET request that supports ``ModelAdmin.message_user``.

    Django admin actions call ``self.message_user(...)`` which requires
    ``django.contrib.messages`` middleware. ``RequestFactory`` doesn't run
    middleware, so we install a fallback storage backend manually.
    """
    request = request_factory.get("/admin/")
    request.user = user
    request.session = {}
    request._messages = FallbackStorage(request)
    return request


@pytest.fixture
def admin_request(request_factory, preferences_admin_user):
    """Request with authenticated admin user and messages storage attached."""
    return _messages_enabled_request(request_factory, preferences_admin_user)


@pytest.fixture
def site_settings_row(db):
    """Return the singleton SiteSettings row created by the autouse fixture."""
    return SiteSettings.objects.get(pk=1)


# ============================================================
# Admin Registration & Basic Setup
# ============================================================


def test_communication_preference_registered_in_admin():
    """CommunicationPreference model is registered in admin."""
    from django.contrib import admin

    assert CommunicationPreference in admin.site._registry


def test_admin_list_display(preference_admin):
    """Admin list_display includes all required columns."""
    expected_fields = [
        "user_email",
        "email_status",
        "sms_status",
        "marketing_status",
        "verification_status",
        "consent_source_display",
        "updated_at",
    ]
    assert preference_admin.list_display == expected_fields


def test_admin_list_filters(preference_admin):
    """Admin list_filter includes all preference fields."""
    expected_filters = [
        "email_enabled",
        "sms_enabled",
        "email_marketing",
        "sms_marketing",
        "email_verified",
        "sms_verified",
        "consent_source",
        "language_code",
    ]
    assert preference_admin.list_filter == expected_filters


def test_admin_search_fields(preference_admin):
    """Admin search_fields includes user details and token."""
    expected_fields = [
        "user__email",
        "user__username",
        "user__first_name",
        "user__last_name",
        "unsubscribe_token",
    ]
    assert preference_admin.search_fields == expected_fields


def test_admin_readonly_fields(preference_admin):
    """Admin has appropriate readonly fields."""
    expected_readonly = [
        "unsubscribe_token",
        "consent_timestamp",
        "consent_ip",
        "consent_user_agent",
        "created_at",
        "updated_at",
        "email_verified_at",
        "sms_verified_at",
    ]
    assert preference_admin.readonly_fields == expected_readonly


# ============================================================
# Admin Display Methods
# ============================================================


def test_user_email_display(preference_admin):
    """``user_email`` renders an anchor to the auth-user change form."""
    user = UserFactory(email="test@example.com")
    prefs = user.communication_preferences

    result = preference_admin.user_email(prefs)

    # The link goes to the resolved URL, not the URL name. Assert on the
    # rendered anchor rather than the reverse() input.
    assert "test@example.com" in result
    assert "/auth/user/" in result
    assert 'href="' in result


def test_email_status_display_enabled(preference_admin):
    """``email_status`` marks enabled preferences with the ``badge-yes`` class."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_enabled = True
    prefs.save()

    result = preference_admin.email_status(prefs)

    # Rendered as ``<span class="badge-yes" title="Email enabled">&#10003;</span>``.
    assert "badge-yes" in result
    assert "&#10003;" in result  # Check-mark HTML entity


def test_email_status_display_disabled(preference_admin):
    """``email_status`` marks disabled preferences with the ``badge-no`` class."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_enabled = False
    prefs.save()

    result = preference_admin.email_status(prefs)

    assert "badge-no" in result
    assert "&#9675;" in result  # Empty circle HTML entity


def test_sms_status_display(preference_admin):
    """``sms_status`` toggles between enabled/disabled badge classes."""
    user = UserFactory()
    prefs = user.communication_preferences

    prefs.sms_enabled = False
    prefs.save()
    assert "badge-no" in preference_admin.sms_status(prefs)

    prefs.sms_enabled = True
    prefs.save()
    assert "badge-yes" in preference_admin.sms_status(prefs)


def test_marketing_status_display_opted_in(preference_admin):
    """``marketing_status`` renders ``Opted In`` when either channel is opted in."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Email marketing enabled
    prefs.email_marketing = True
    prefs.save()
    result = preference_admin.marketing_status(prefs)
    assert "Opted In" in result
    assert "badge-yes" in result

    # SMS marketing enabled
    prefs.email_marketing = False
    prefs.sms_marketing = True
    prefs.save()
    result = preference_admin.marketing_status(prefs)
    assert "Opted In" in result


def test_marketing_status_display_opted_out(preference_admin):
    """``marketing_status`` renders ``Opted Out`` when both channels are off."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = False
    prefs.sms_marketing = False
    prefs.save()

    result = preference_admin.marketing_status(prefs)

    assert "Opted Out" in result
    assert "badge-no" in result


def test_verification_status_display(preference_admin):
    """``verification_status`` shows check/circle marks per channel.

    ``format_html`` percent-escapes the ampersand, so the HTML entities
    appear in the output as ``&amp;#9675;`` and ``&amp;#10003;`` rather
    than the literal entities. The admin passes them through
    ``format_html`` (which escapes) instead of ``mark_safe``.
    """
    user = UserFactory()
    prefs = user.communication_preferences

    circle = "&amp;#9675;"
    check = "&amp;#10003;"

    # Both unverified — two empty circles.
    result = preference_admin.verification_status(prefs)
    assert result.count(circle) == 2

    # Email verified — one check mark, one empty.
    prefs.email_verified = True
    prefs.save()
    result = preference_admin.verification_status(prefs)
    assert check in result
    assert circle in result

    # Both verified — two check marks.
    prefs.sms_verified = True
    prefs.save()
    result = preference_admin.verification_status(prefs)
    assert result.count(check) == 2


def test_consent_source_display(preference_admin):
    """``consent_source_display`` returns the human-readable choice label."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Registration → ``Account Registration``
    prefs.consent_source = "registration"
    prefs.save()
    assert preference_admin.consent_source_display(prefs) == "Account Registration"

    # Checkout → ``Checkout Process``
    prefs.consent_source = "checkout"
    prefs.save()
    assert preference_admin.consent_source_display(prefs) == "Checkout Process"


# ============================================================
# Admin Actions - Bulk Verify Email
# ============================================================


def test_bulk_verify_email_action(preference_admin, admin_request):
    """bulk_verify_email marks selected users as verified."""
    user1 = UserFactory()
    user2 = UserFactory()

    prefs1 = user1.communication_preferences
    prefs2 = user2.communication_preferences

    assert prefs1.email_verified is False
    assert prefs2.email_verified is False

    queryset = CommunicationPreference.objects.filter(pk__in=[prefs1.pk, prefs2.pk])
    preference_admin.bulk_verify_email(admin_request, queryset)

    prefs1.refresh_from_db()
    prefs2.refresh_from_db()
    assert prefs1.email_verified is True
    assert prefs2.email_verified is True
    assert prefs1.email_verified_at is not None
    assert prefs2.email_verified_at is not None


def test_bulk_verify_email_invalidates_cache(preference_admin, admin_request):
    """bulk_verify_email invalidates cached preference checks."""
    from django.core.cache import cache

    from accounts.services.preference_service import PreferenceService

    user = UserFactory()
    prefs = user.communication_preferences

    # Populate the cache with a permission check.
    PreferenceService.check_email_permission(user, "newsletter")
    cache_key = f"email_pref:{user.id}:newsletter"
    assert cache.get(cache_key) is not None

    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    preference_admin.bulk_verify_email(admin_request, queryset)

    # The action calls ``PreferenceService.invalidate_cache(user.id)`` which
    # walks every known message type and clears each key.
    assert cache.get(cache_key) is None


# ============================================================
# Admin Actions - Bulk Unsubscribe
# ============================================================


def test_bulk_unsubscribe_marketing_action(preference_admin, admin_request):
    """bulk_unsubscribe_marketing disables all marketing for selected users."""
    user = UserFactory()
    prefs = user.communication_preferences

    prefs.email_marketing = True
    prefs.sms_marketing = True
    prefs.app_preferences["blog"]["enabled"] = True
    prefs.app_preferences["loyalty"]["enabled"] = True
    prefs.app_preferences["referrals"]["enabled"] = True
    prefs.app_preferences["affiliate"]["enabled"] = True
    prefs.save()

    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    preference_admin.bulk_unsubscribe_marketing(admin_request, queryset)

    prefs.refresh_from_db()
    assert prefs.email_marketing is False
    assert prefs.sms_marketing is False
    assert prefs.app_preferences["blog"]["enabled"] is False
    assert prefs.app_preferences["loyalty"]["enabled"] is False
    assert prefs.app_preferences["referrals"]["enabled"] is False
    assert prefs.app_preferences["affiliate"]["enabled"] is False


def test_bulk_unsubscribe_keeps_transactional(preference_admin, admin_request):
    """bulk_unsubscribe_marketing keeps transactional emails enabled."""
    user = UserFactory()
    prefs = user.communication_preferences

    prefs.email_transactional = True
    prefs.sms_transactional = True
    prefs.save()

    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    preference_admin.bulk_unsubscribe_marketing(admin_request, queryset)

    prefs.refresh_from_db()
    assert prefs.email_transactional is True
    assert prefs.sms_transactional is True


# ============================================================
# Admin Actions - Export CSV
# ============================================================


def test_export_preferences_csv_action(preference_admin, admin_request):
    """export_preferences_csv generates a CSV response."""
    user1 = UserFactory(email="user1@test.com")
    user2 = UserFactory(email="user2@test.com")

    prefs1 = user1.communication_preferences
    prefs1.email_marketing = True
    prefs1.email_verified = True
    prefs1.save()

    queryset = CommunicationPreference.objects.filter(
        pk__in=[prefs1.pk, user2.communication_preferences.pk]
    ).order_by("pk")
    response = preference_admin.export_preferences_csv(admin_request, queryset)

    assert isinstance(response, HttpResponse)
    assert response["Content-Type"] == "text/csv"
    assert "communication_preferences.csv" in response["Content-Disposition"]

    content = response.content.decode("utf-8")
    rows = list(csv.reader(StringIO(content)))

    # Header + 2 data rows.
    assert len(rows) == 3
    assert "User Email" in rows[0]
    assert "Email Marketing" in rows[0]
    assert "SMS Enabled" in rows[0]

    # Verify both users appear regardless of ordering.
    email_column = {row[0] for row in rows[1:]}
    assert email_column == {"user1@test.com", "user2@test.com"}


def test_export_csv_includes_app_preferences(preference_admin, admin_request):
    """export_preferences_csv includes app-specific preferences."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.app_preferences["blog"]["enabled"] = True
    prefs.app_preferences["loyalty"]["enabled"] = False
    prefs.save()

    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    response = preference_admin.export_preferences_csv(admin_request, queryset)

    content = response.content.decode("utf-8")
    rows = list(csv.reader(StringIO(content)))

    headers = rows[0]
    assert "Blog Enabled" in headers
    assert "Loyalty Enabled" in headers
    assert "Referrals Enabled" in headers
    assert "Affiliate Enabled" in headers


# ============================================================
# SiteSettings Integration
# ============================================================


def test_site_settings_has_communication_fields(site_settings_row):
    """SiteSettings model exposes communication-preference toggles."""
    assert hasattr(site_settings_row, "enable_double_opt_in")
    assert hasattr(site_settings_row, "default_marketing_opt_in")
    assert hasattr(site_settings_row, "preference_center_enabled")
    assert hasattr(site_settings_row, "require_sms_verification")
    assert hasattr(site_settings_row, "show_unsubscribe_reasons")


def test_site_settings_default_values(site_settings_row):
    """SiteSettings communication fields have GDPR-friendly defaults."""
    assert site_settings_row.enable_double_opt_in is True
    assert site_settings_row.default_marketing_opt_in is False
    assert site_settings_row.preference_center_enabled is True
    assert site_settings_row.require_sms_verification is False
    assert site_settings_row.show_unsubscribe_reasons is True


def test_site_settings_fields_are_editable(site_settings_row):
    """SiteSettings communication fields can be updated."""
    site_settings_row.enable_double_opt_in = False
    site_settings_row.default_marketing_opt_in = True
    site_settings_row.preference_center_enabled = False
    site_settings_row.save()

    site_settings_row.refresh_from_db()
    assert site_settings_row.enable_double_opt_in is False
    assert site_settings_row.default_marketing_opt_in is True
    assert site_settings_row.preference_center_enabled is False


# ============================================================
# Queryset Optimization
# ============================================================


def test_admin_queryset_uses_select_related(preference_admin, admin_request):
    """Admin queryset uses select_related for performance."""
    UserFactory()
    UserFactory()

    queryset = preference_admin.get_queryset(admin_request)

    # Django's ModelAdmin builds a ``select_related`` dict when the admin
    # class asks for it via ``list_select_related`` or via the ``user_email``
    # ordering hint. Either way, ``user`` must be a key.
    assert "user" in queryset.query.select_related


# ============================================================
# Edge Cases
# ============================================================


def test_admin_handles_missing_app_preferences(
    preference_admin, request_factory, preferences_admin_user
):
    """Admin export handles a corrupted ``app_preferences`` blob without crashing."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.app_preferences = {}  # Empty/corrupted
    prefs.save()

    request = _messages_enabled_request(request_factory, preferences_admin_user)
    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    response = preference_admin.export_preferences_csv(request, queryset)

    assert isinstance(response, HttpResponse)


def test_bulk_unsubscribe_handles_missing_app_keys(preference_admin, admin_request):
    """bulk_unsubscribe_marketing handles missing app_preference keys."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.app_preferences = {"blog": {}}  # Missing other apps
    prefs.save()

    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    preference_admin.bulk_unsubscribe_marketing(admin_request, queryset)

    prefs.refresh_from_db()
    assert prefs.email_marketing is False
