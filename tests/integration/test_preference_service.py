"""
PreferenceService Integration Tests.

Tests the centralized preference service including permission checks,
caching, and preference updates.
"""
import pytest
from unittest.mock import patch
from django.core.cache import cache
from django.contrib.auth import get_user_model

from accounts.models import CommunicationPreference
from accounts.services.preference_service import PreferenceService
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.preference_service]


# ============================================================
# Setup & Teardown
# ============================================================

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before each test to avoid cross-test contamination."""
    cache.clear()
    yield
    cache.clear()


# ============================================================
# get_or_create_for_user
# ============================================================

def test_get_or_create_creates_on_first_call(db):
    """get_or_create_for_user creates preference if doesn't exist."""
    user = UserFactory()

    # Delete auto-created preference to test creation
    if hasattr(user, 'communication_preferences'):
        user.communication_preferences.delete()

    prefs, created = PreferenceService.get_or_create_for_user(user)

    assert created is True
    assert isinstance(prefs, CommunicationPreference)
    assert prefs.user == user


def test_get_or_create_returns_existing(db):
    """get_or_create_for_user returns existing preference without creating duplicate."""
    user = UserFactory()
    existing_prefs = user.communication_preferences
    original_token = existing_prefs.unsubscribe_token

    prefs, created = PreferenceService.get_or_create_for_user(user)

    assert created is False
    assert prefs.pk == existing_prefs.pk
    assert prefs.unsubscribe_token == original_token


# ============================================================
# check_email_permission
# ============================================================

def test_check_email_permission_transactional_always_allowed(db):
    """Transactional emails always allowed regardless of preferences."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Disable everything
    prefs.email_enabled = False
    prefs.email_transactional = False
    prefs.email_marketing = False
    prefs.save()

    # Transactional still allowed
    assert PreferenceService.check_email_permission(user, 'order_confirmation') is True
    assert PreferenceService.check_email_permission(user, 'order_shipped') is True
    assert PreferenceService.check_email_permission(user, 'password_reset') is True


def test_check_email_permission_marketing_requires_verification(db):
    """Marketing emails require email_marketing=True AND email_verified=True."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Not opted in
    prefs.email_marketing = False
    prefs.email_verified = True
    prefs.save()

    assert PreferenceService.check_email_permission(user, 'newsletter') is False

    # Opted in but not verified
    prefs.email_marketing = True
    prefs.email_verified = False
    prefs.save()

    assert PreferenceService.check_email_permission(user, 'newsletter') is False

    # Both conditions met
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    assert PreferenceService.check_email_permission(user, 'newsletter') is True


def test_check_email_permission_app_specific(db):
    """App-specific email types check nested app preferences."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Enable marketing & verify
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    # Blog enabled by default
    assert PreferenceService.check_email_permission(user, 'blog_post_published') is True

    # Disable blog app
    prefs.app_preferences['blog']['enabled'] = False
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_email_permission(user, 'blog_post_published') is False

    # Loyalty - specific event type
    prefs.app_preferences['loyalty']['points_earned'] = False
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_email_permission(user, 'loyalty_points_earned') is False


def test_check_email_permission_unknown_type_defaults_to_marketing(db):
    """Unknown message types default to marketing permission check."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Not opted into marketing
    prefs.email_marketing = False
    prefs.save()

    assert PreferenceService.check_email_permission(user, 'some_unknown_type') is False

    # Opted in and verified
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_email_permission(user, 'some_unknown_type') is True


# ============================================================
# check_sms_permission
# ============================================================

def test_check_sms_permission_requires_opt_in(db):
    """All SMS requires explicit opt-in (TCPA compliance)."""
    user = UserFactory()

    # Default state - all SMS disabled
    assert PreferenceService.check_sms_permission(user, 'order_shipped') is False

    # Enable transactional SMS
    prefs = user.communication_preferences
    prefs.sms_transactional = True
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_sms_permission(user, 'order_shipped') is True


def test_check_sms_permission_marketing_requires_separate_opt_in(db):
    """Marketing SMS requires separate sms_marketing opt-in."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Only transactional enabled
    prefs.sms_transactional = True
    prefs.save()

    assert PreferenceService.check_sms_permission(user, 'promotional_offer') is False

    # Enable marketing
    prefs.sms_marketing = True
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_sms_permission(user, 'promotional_offer') is True


def test_check_sms_permission_master_toggle(db):
    """sms_enabled=False blocks all SMS."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Enable everything
    prefs.sms_transactional = True
    prefs.sms_marketing = True
    prefs.save()

    # Disable master toggle
    prefs.sms_enabled = False
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_sms_permission(user, 'order_shipped') is False
    assert PreferenceService.check_sms_permission(user, 'promotional_offer') is False


# ============================================================
# Caching Behavior
# ============================================================

def test_permission_check_uses_cache(db):
    """Permission checks are cached to reduce DB queries."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    # First call should hit DB
    with patch.object(CommunicationPreference.objects, 'get') as mock_get:
        mock_get.return_value = prefs
        result1 = PreferenceService.check_email_permission(user, 'newsletter')
        assert result1 is True
        assert mock_get.called

    # Second call should use cache
    with patch.object(CommunicationPreference.objects, 'get') as mock_get:
        result2 = PreferenceService.check_email_permission(user, 'newsletter')
        assert result2 is True
        assert not mock_get.called  # Cache hit, no DB query


def test_invalidate_cache_clears_user_preferences(db):
    """invalidate_cache() removes cached preferences for user."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    # Populate cache
    PreferenceService.check_email_permission(user, 'newsletter')

    # Verify cache exists
    cache_key = f'comm_pref_{user.id}'
    assert cache.get(cache_key) is not None

    # Invalidate
    PreferenceService.invalidate_cache(user.id)

    # Verify cache cleared
    assert cache.get(cache_key) is None


def test_cache_timeout_is_5_minutes(db):
    """Cached preferences expire after 5 minutes (300 seconds)."""
    user = UserFactory()

    with patch('django.core.cache.cache.set') as mock_set:
        PreferenceService.check_email_permission(user, 'newsletter')
        # Verify cache.set called with 300 second timeout
        assert mock_set.called
        call_args = mock_set.call_args
        assert call_args[0][0] == f'comm_pref_{user.id}'  # Key
        assert call_args[1]['timeout'] == 300  # 5 minutes


# ============================================================
# update_preference
# ============================================================

def test_update_preference_modifies_field(db):
    """update_preference updates the specified preference field."""
    user = UserFactory()

    # Update email marketing
    PreferenceService.update_preference(
        user=user,
        channel='email',
        message_type='marketing',
        enabled=True,
    )

    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is True


def test_update_preference_invalidates_cache(db):
    """update_preference invalidates cache after update."""
    user = UserFactory()

    # Populate cache
    PreferenceService.check_email_permission(user, 'newsletter')
    cache_key = f'comm_pref_{user.id}'
    assert cache.get(cache_key) is not None

    # Update preference
    PreferenceService.update_preference(
        user=user,
        channel='email',
        message_type='marketing',
        enabled=True,
    )

    # Cache should be cleared
    assert cache.get(cache_key) is None


def test_update_preference_app_specific(db):
    """update_preference can update app-specific preferences."""
    user = UserFactory()

    # Update blog frequency
    PreferenceService.update_preference(
        user=user,
        channel='email',
        message_type='blog',
        enabled=True,
        frequency='immediate',
    )

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.app_preferences['blog']['enabled'] is True
    assert prefs.app_preferences['blog']['frequency'] == 'immediate'


# ============================================================
# Edge Cases & Error Handling
# ============================================================

def test_check_permission_creates_preference_if_missing(db):
    """Permission check auto-creates preference if user doesn't have one."""
    user = UserFactory()

    # Delete preference
    if hasattr(user, 'communication_preferences'):
        user.communication_preferences.delete()

    # Check permission should auto-create
    result = PreferenceService.check_email_permission(user, 'order_confirmation')

    assert result is True
    user.refresh_from_db()
    assert hasattr(user, 'communication_preferences')


def test_permission_check_handles_none_user(db):
    """Permission checks gracefully handle None user (guest checkout)."""
    # For transactional, should allow (guest checkout scenario)
    result = PreferenceService.check_email_permission(None, 'order_confirmation')
    assert result is True

    # For marketing, should deny
    result = PreferenceService.check_email_permission(None, 'newsletter')
    assert result is False
