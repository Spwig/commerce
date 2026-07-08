"""
Communication Preferences Admin Tests.

Tests Django admin interface for CommunicationPreference model including
list display, filters, actions, and SiteSettings integration.
"""
import pytest
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from django.contrib.messages import get_messages
from django.http import HttpResponse
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from io import StringIO
import csv

from accounts.admin import CommunicationPreferenceAdmin
from accounts.models import CommunicationPreference
from core.models import SiteSettings
from tests.factories import UserFactory, CommunicationPreferenceFactory

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
def admin_user(db):
    """Staff user with admin access."""
    user = UserFactory()
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user


@pytest.fixture
def admin_request(request_factory, admin_user):
    """Request with authenticated admin user."""
    request = request_factory.get('/admin/')
    request.user = admin_user
    return request


@pytest.fixture
def site_settings(db):
    """SiteSettings instance."""
    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_name': 'Test Store',
            'admin_email': 'admin@test.com',
            'default_currency': 'USD',
            'default_language': 'en',
        }
    )
    return settings


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
        'user_email',
        'email_status',
        'sms_status',
        'marketing_status',
        'verification_status',
        'consent_source_display',
        'updated_at',
    ]
    assert preference_admin.list_display == expected_fields


def test_admin_list_filters(preference_admin):
    """Admin list_filter includes all preference fields."""
    expected_filters = [
        'email_enabled',
        'sms_enabled',
        'email_marketing',
        'sms_marketing',
        'email_verified',
        'sms_verified',
        'consent_source',
        'language_code',
    ]
    assert preference_admin.list_filter == expected_filters


def test_admin_search_fields(preference_admin):
    """Admin search_fields includes user details and token."""
    expected_fields = [
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
        'unsubscribe_token',
    ]
    assert preference_admin.search_fields == expected_fields


def test_admin_readonly_fields(preference_admin):
    """Admin has appropriate readonly fields."""
    expected_readonly = [
        'unsubscribe_token',
        'consent_timestamp',
        'consent_ip',
        'consent_user_agent',
        'created_at',
        'updated_at',
        'email_verified_at',
        'sms_verified_at',
    ]
    assert preference_admin.readonly_fields == expected_readonly


# ============================================================
# Admin Display Methods
# ============================================================

def test_user_email_display(preference_admin, admin_request):
    """user_email displays email with link to user admin."""
    user = UserFactory(email='test@example.com')
    prefs = user.communication_preferences

    result = preference_admin.user_email(prefs)

    assert 'test@example.com' in result
    assert 'admin:auth_user_change' in result


def test_email_status_display_enabled(preference_admin):
    """email_status shows green check when enabled."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_enabled = True
    prefs.save()

    result = preference_admin.email_status(prefs)

    assert 'green' in result
    assert '✓' in result


def test_email_status_display_disabled(preference_admin):
    """email_status shows gray circle when disabled."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_enabled = False
    prefs.save()

    result = preference_admin.email_status(prefs)

    assert 'gray' in result
    assert '○' in result


def test_sms_status_display(preference_admin):
    """sms_status shows appropriate icon."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Disabled
    prefs.sms_enabled = False
    prefs.save()
    result = preference_admin.sms_status(prefs)
    assert 'gray' in result

    # Enabled
    prefs.sms_enabled = True
    prefs.save()
    result = preference_admin.sms_status(prefs)
    assert 'green' in result


def test_marketing_status_display_opted_in(preference_admin):
    """marketing_status shows 'Opted In' when either email or SMS marketing enabled."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Email marketing enabled
    prefs.email_marketing = True
    prefs.save()
    result = preference_admin.marketing_status(prefs)
    assert 'Opted In' in result
    assert 'green' in result

    # SMS marketing enabled
    prefs.email_marketing = False
    prefs.sms_marketing = True
    prefs.save()
    result = preference_admin.marketing_status(prefs)
    assert 'Opted In' in result


def test_marketing_status_display_opted_out(preference_admin):
    """marketing_status shows 'Opted Out' when both disabled."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = False
    prefs.sms_marketing = False
    prefs.save()

    result = preference_admin.marketing_status(prefs)

    assert 'Opted Out' in result
    assert 'gray' in result


def test_verification_status_display(preference_admin):
    """verification_status shows email and SMS verification badges."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Both unverified
    result = preference_admin.verification_status(prefs)
    assert '📧○' in result  # Email unverified
    assert '📱○' in result  # SMS unverified

    # Email verified
    prefs.email_verified = True
    prefs.save()
    result = preference_admin.verification_status(prefs)
    assert '📧✓' in result

    # Both verified
    prefs.sms_verified = True
    prefs.save()
    result = preference_admin.verification_status(prefs)
    assert '📧✓' in result
    assert '📱✓' in result


def test_consent_source_display(preference_admin):
    """consent_source_display shows icon and label."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Registration
    prefs.consent_source = 'registration'
    prefs.save()
    result = preference_admin.consent_source_display(prefs)
    assert '📝' in result

    # Checkout
    prefs.consent_source = 'checkout'
    prefs.save()
    result = preference_admin.consent_source_display(prefs)
    assert '🛒' in result


# ============================================================
# Admin Actions - Bulk Verify Email
# ============================================================

def test_bulk_verify_email_action(preference_admin, admin_request):
    """bulk_verify_email marks selected users as verified."""
    user1 = UserFactory()
    user2 = UserFactory()

    prefs1 = user1.communication_preferences
    prefs2 = user2.communication_preferences

    # Both unverified
    assert prefs1.email_verified is False
    assert prefs2.email_verified is False

    # Run action
    queryset = CommunicationPreference.objects.filter(pk__in=[prefs1.pk, prefs2.pk])
    preference_admin.bulk_verify_email(admin_request, queryset)

    # Check verified
    prefs1.refresh_from_db()
    prefs2.refresh_from_db()
    assert prefs1.email_verified is True
    assert prefs2.email_verified is True
    assert prefs1.email_verified_at is not None
    assert prefs2.email_verified_at is not None


def test_bulk_verify_email_invalidates_cache(preference_admin, admin_request):
    """bulk_verify_email invalidates preference cache."""
    from django.core.cache import cache
    from accounts.services.preference_service import PreferenceService

    user = UserFactory()
    prefs = user.communication_preferences

    # Populate cache
    PreferenceService.check_email_permission(user, 'newsletter')
    cache_key = f'comm_pref_{user.id}'
    assert cache.get(cache_key) is not None

    # Run action
    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    preference_admin.bulk_verify_email(admin_request, queryset)

    # Cache should be cleared
    assert cache.get(cache_key) is None


# ============================================================
# Admin Actions - Bulk Unsubscribe
# ============================================================

def test_bulk_unsubscribe_marketing_action(preference_admin, admin_request):
    """bulk_unsubscribe_marketing disables all marketing for selected users."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Enable all marketing
    prefs.email_marketing = True
    prefs.sms_marketing = True
    prefs.app_preferences['blog']['enabled'] = True
    prefs.app_preferences['loyalty']['enabled'] = True
    prefs.app_preferences['referrals']['enabled'] = True
    prefs.app_preferences['affiliate']['enabled'] = True
    prefs.save()

    # Run action
    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    preference_admin.bulk_unsubscribe_marketing(admin_request, queryset)

    # Check all disabled
    prefs.refresh_from_db()
    assert prefs.email_marketing is False
    assert prefs.sms_marketing is False
    assert prefs.app_preferences['blog']['enabled'] is False
    assert prefs.app_preferences['loyalty']['enabled'] is False
    assert prefs.app_preferences['referrals']['enabled'] is False
    assert prefs.app_preferences['affiliate']['enabled'] is False


def test_bulk_unsubscribe_keeps_transactional(preference_admin, admin_request):
    """bulk_unsubscribe_marketing keeps transactional emails enabled."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Enable transactional
    prefs.email_transactional = True
    prefs.sms_transactional = True
    prefs.save()

    # Run action
    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    preference_admin.bulk_unsubscribe_marketing(admin_request, queryset)

    # Transactional still enabled
    prefs.refresh_from_db()
    assert prefs.email_transactional is True
    assert prefs.sms_transactional is True


# ============================================================
# Admin Actions - Export CSV
# ============================================================

def test_export_preferences_csv_action(preference_admin, admin_request):
    """export_preferences_csv generates CSV file."""
    user1 = UserFactory(email='user1@test.com')
    user2 = UserFactory(email='user2@test.com')

    # Customize preferences
    prefs1 = user1.communication_preferences
    prefs1.email_marketing = True
    prefs1.email_verified = True
    prefs1.save()

    queryset = CommunicationPreference.objects.filter(pk__in=[prefs1.pk, user2.communication_preferences.pk])
    response = preference_admin.export_preferences_csv(admin_request, queryset)

    # Check response type
    assert isinstance(response, HttpResponse)
    assert response['Content-Type'] == 'text/csv'
    assert 'communication_preferences.csv' in response['Content-Disposition']

    # Parse CSV content
    content = response.content.decode('utf-8')
    csv_reader = csv.reader(StringIO(content))
    rows = list(csv_reader)

    # Check headers
    assert 'User Email' in rows[0]
    assert 'Email Marketing' in rows[0]
    assert 'SMS Enabled' in rows[0]

    # Check data rows (1 header + 2 data rows)
    assert len(rows) == 3
    assert 'user1@test.com' in rows[1]


def test_export_csv_includes_app_preferences(preference_admin, admin_request):
    """export_preferences_csv includes app-specific preferences."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.app_preferences['blog']['enabled'] = True
    prefs.app_preferences['loyalty']['enabled'] = False
    prefs.save()

    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    response = preference_admin.export_preferences_csv(admin_request, queryset)

    content = response.content.decode('utf-8')
    csv_reader = csv.reader(StringIO(content))
    rows = list(csv_reader)

    # Check headers include app fields
    headers = rows[0]
    assert 'Blog Enabled' in headers
    assert 'Loyalty Enabled' in headers
    assert 'Referrals Enabled' in headers
    assert 'Affiliate Enabled' in headers


# ============================================================
# SiteSettings Integration
# ============================================================

def test_site_settings_has_communication_fields(site_settings):
    """SiteSettings model has communication preference fields."""
    assert hasattr(site_settings, 'enable_double_opt_in')
    assert hasattr(site_settings, 'default_marketing_opt_in')
    assert hasattr(site_settings, 'preference_center_enabled')
    assert hasattr(site_settings, 'require_sms_verification')
    assert hasattr(site_settings, 'show_unsubscribe_reasons')


def test_site_settings_default_values(site_settings):
    """SiteSettings communication fields have correct defaults."""
    # GDPR-compliant defaults
    assert site_settings.enable_double_opt_in is True  # Require email verification
    assert site_settings.default_marketing_opt_in is False  # Opt-out by default
    assert site_settings.preference_center_enabled is True  # Allow preference management
    assert site_settings.require_sms_verification is False  # Optional SMS verification
    assert site_settings.show_unsubscribe_reasons is True  # Collect feedback


def test_site_settings_fields_are_editable(site_settings):
    """SiteSettings communication fields can be updated."""
    site_settings.enable_double_opt_in = False
    site_settings.default_marketing_opt_in = True
    site_settings.preference_center_enabled = False
    site_settings.save()

    site_settings.refresh_from_db()
    assert site_settings.enable_double_opt_in is False
    assert site_settings.default_marketing_opt_in is True
    assert site_settings.preference_center_enabled is False


# ============================================================
# Queryset Optimization
# ============================================================

def test_admin_queryset_uses_select_related(preference_admin, admin_request):
    """Admin queryset uses select_related for performance."""
    UserFactory()
    UserFactory()

    queryset = preference_admin.get_queryset(admin_request)

    # Check select_related is applied
    assert 'user' in queryset.query.select_related


# ============================================================
# Edge Cases
# ============================================================

def test_admin_handles_missing_app_preferences(preference_admin):
    """Admin displays correctly when app_preferences are corrupted."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.app_preferences = {}  # Empty/corrupted
    prefs.save()

    # Export CSV should not crash
    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    response = preference_admin.export_preferences_csv(RequestFactory().get('/'), queryset)

    assert isinstance(response, HttpResponse)


def test_bulk_unsubscribe_handles_missing_app_keys(preference_admin, admin_request):
    """bulk_unsubscribe_marketing handles missing app_preference keys."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.app_preferences = {'blog': {}}  # Missing other apps
    prefs.save()

    # Should not crash
    queryset = CommunicationPreference.objects.filter(pk=prefs.pk)
    preference_admin.bulk_unsubscribe_marketing(admin_request, queryset)

    # Should complete without error
    prefs.refresh_from_db()
    assert prefs.email_marketing is False
