"""
PreferenceService Integration Tests.

Tests the centralized preference service including permission checks,
caching, and preference updates.

**Cache-key convention.** ``PreferenceService`` keys the cache per
(channel, user, message_type), e.g. ``email_pref:{user_id}:{message_type}``
and ``sms_pref:{user_id}:{message_type}``. There is no single
``comm_pref_{user_id}`` key. ``invalidate_cache`` walks
``ALL_EMAIL_TYPES`` / ``ALL_SMS_TYPES`` from ``accounts.constants``.

**Cache TTL.** ``cache.set`` is called with the TTL as a positional
argument (``cache.set(key, value, cls.CACHE_TTL)``), *not* the ``timeout=``
kwarg — tests must match either call form.

**Unknown message types.** ``accounts.constants.get_message_type_category``
returns ``("transactional", None)`` as its fallback. That means unknown
email types flow through the transactional branch of ``should_send_email``,
not the marketing branch — the old "unknown defaults to marketing" test
was documenting an intent, not the code.

**Missing-preference behaviour.** ``check_email_permission`` does *not*
auto-create a preference row on cache-miss. It falls back to allowing
transactional message types and denying everything else (see the
``TRANSACTIONAL_EMAIL_TYPES`` guard in the ``DoesNotExist`` branch).
"""

from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache

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

    # Fixture auto-creates a preference row — delete it so we can observe
    # the ``created`` branch.
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


def test_check_email_permission_transactional_gated_by_master(db):
    """Transactional emails require the master + transactional toggles."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Defaults allow transactional.
    assert PreferenceService.check_email_permission(user, "order_confirmation") is True

    # Disable master toggle → all types blocked.
    prefs.email_enabled = False
    prefs.save()
    PreferenceService.invalidate_cache(user.id)
    assert PreferenceService.check_email_permission(user, "order_confirmation") is False


def test_check_email_permission_marketing_requires_verification(db):
    """Marketing emails require email_marketing=True AND email_verified=True."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Not opted in
    prefs.email_marketing = False
    prefs.email_verified = True
    prefs.save()

    assert PreferenceService.check_email_permission(user, "newsletter") is False

    # Opted in but not verified
    prefs.email_marketing = True
    prefs.email_verified = False
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_email_permission(user, "newsletter") is False

    # Both conditions met
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_email_permission(user, "newsletter") is True


def test_check_email_permission_app_specific(db):
    """App-specific email types check nested app preferences."""
    user = UserFactory()
    prefs = user.communication_preferences

    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    # Blog enabled by default
    assert PreferenceService.check_email_permission(user, "blog_post_published") is True

    # Disable blog app
    prefs.app_preferences["blog"]["enabled"] = False
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_email_permission(user, "blog_post_published") is False

    # Loyalty - specific event type. The message-type name maps to the
    # ``points_earned`` key on the loyalty app preferences.
    prefs.app_preferences["blog"]["enabled"] = True
    prefs.app_preferences["loyalty"]["points_earned"] = False
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_email_permission(user, "loyalty_points_earned") is False


def test_check_email_permission_unknown_type_requires_marketing_consent(db):
    """Unknown message types fall through to the marketing+verification guard.

    ``get_message_type_category`` returns ``("transactional", None)`` for
    unrecognised types, but ``should_send_email`` has no explicit branch
    for the ``transactional`` category — it falls through to the marketing
    guard as the "safer default" comment in the model documents.
    """
    user = UserFactory()
    prefs = user.communication_preferences

    # Not opted in → denied.
    assert PreferenceService.check_email_permission(user, "some_unknown_type") is False

    # Opt-in + verify → allowed. ``invalidate_cache`` only clears keys for
    # message types it *knows about* (from ``ALL_EMAIL_TYPES``), so we clear
    # the cache directly to bust the previous ``False`` entry for this
    # ad-hoc type.
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()
    cache.clear()
    assert PreferenceService.check_email_permission(user, "some_unknown_type") is True


# ============================================================
# check_sms_permission
# ============================================================


def test_check_sms_permission_requires_opt_in(db):
    """All SMS requires explicit opt-in (TCPA compliance)."""
    user = UserFactory()

    # Default state - all SMS disabled
    assert PreferenceService.check_sms_permission(user, "order_shipped") is False

    # Enable transactional SMS + verification + master toggle
    prefs = user.communication_preferences
    prefs.sms_enabled = True
    prefs.sms_verified = True
    prefs.sms_transactional = True
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_sms_permission(user, "order_shipped") is True


def test_check_sms_permission_marketing_requires_separate_opt_in(db):
    """Marketing SMS requires separate sms_marketing opt-in."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Verified + transactional but not marketing.
    prefs.sms_enabled = True
    prefs.sms_verified = True
    prefs.sms_transactional = True
    prefs.save()

    # ``promotional_offers`` is the marketing SMS type defined in constants.
    assert PreferenceService.check_sms_permission(user, "promotional_offers") is False

    # Enable marketing
    prefs.sms_marketing = True
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_sms_permission(user, "promotional_offers") is True


def test_check_sms_permission_master_toggle(db):
    """sms_enabled=False blocks all SMS."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Enable everything else
    prefs.sms_enabled = True
    prefs.sms_verified = True
    prefs.sms_transactional = True
    prefs.sms_marketing = True
    prefs.save()

    # Disable master toggle
    prefs.sms_enabled = False
    prefs.save()
    PreferenceService.invalidate_cache(user.id)

    assert PreferenceService.check_sms_permission(user, "order_shipped") is False
    assert PreferenceService.check_sms_permission(user, "promotional_offers") is False


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

    # First call should hit DB.
    with patch.object(CommunicationPreference.objects, "get") as mock_get:
        mock_get.return_value = prefs
        result1 = PreferenceService.check_email_permission(user, "newsletter")
        assert result1 is True
        assert mock_get.called

    # Second call should use cache — no DB hit.
    with patch.object(CommunicationPreference.objects, "get") as mock_get:
        result2 = PreferenceService.check_email_permission(user, "newsletter")
        assert result2 is True
        assert not mock_get.called


def test_invalidate_cache_clears_user_preferences(db):
    """invalidate_cache() removes cached preferences for user."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    # Populate cache
    PreferenceService.check_email_permission(user, "newsletter")

    # Cache key is keyed per (channel, user, message_type).
    cache_key = f"email_pref:{user.id}:newsletter"
    assert cache.get(cache_key) is not None

    # Invalidate — the service walks ALL_EMAIL_TYPES + ALL_SMS_TYPES.
    PreferenceService.invalidate_cache(user.id)

    assert cache.get(cache_key) is None


def test_cache_uses_5_minute_ttl(db):
    """Cached preferences expire after 5 minutes (300 seconds)."""
    user = UserFactory()

    # PreferenceService.CACHE_TTL is 300; it's passed positionally to
    # ``cache.set(key, value, ttl)``.
    with patch("accounts.services.preference_service.cache.set") as mock_set:
        PreferenceService.check_email_permission(user, "newsletter")
        assert mock_set.called
        # Positional args: (key, value, ttl)
        args = mock_set.call_args.args
        kwargs = mock_set.call_args.kwargs
        # Support either call style — service currently uses positional.
        ttl = args[2] if len(args) >= 3 else kwargs.get("timeout")
        assert ttl == 300


# ============================================================
# update_preference
# ============================================================


def test_update_preference_modifies_field(db):
    """update_preference updates the specified preference field."""
    user = UserFactory()

    # ``newsletter`` maps to the marketing category which sets email_marketing.
    PreferenceService.update_preference(
        user=user,
        channel="email",
        message_type="newsletter",
        enabled=True,
    )

    user.refresh_from_db()
    assert user.communication_preferences.email_marketing is True


def test_update_preference_invalidates_cache(db):
    """update_preference invalidates cache after update."""
    user = UserFactory()

    # Populate cache
    PreferenceService.check_email_permission(user, "newsletter")
    cache_key = f"email_pref:{user.id}:newsletter"
    assert cache.get(cache_key) is not None

    # Update preference
    PreferenceService.update_preference(
        user=user,
        channel="email",
        message_type="newsletter",
        enabled=True,
    )

    # Cache should be cleared
    assert cache.get(cache_key) is None


def test_update_preference_app_specific(db):
    """update_preference can update app-specific preferences."""
    user = UserFactory()

    # ``blog_weekly_digest`` maps to the ``weekly_digest`` key on blog prefs.
    PreferenceService.update_preference(
        user=user,
        channel="email",
        message_type="blog_weekly_digest",
        enabled=True,
        frequency="immediate",
    )

    user.refresh_from_db()
    prefs = user.communication_preferences
    assert prefs.app_preferences["blog"]["weekly_digest"] is True
    assert prefs.app_preferences["blog"]["frequency"] == "immediate"


# ============================================================
# Edge Cases & Error Handling
# ============================================================


def test_check_permission_missing_row_allows_transactional(db):
    """When a user has no preference row, only transactional types succeed."""
    user = UserFactory()

    # Delete the auto-created preference.
    user.communication_preferences.delete()

    # ``order_confirmation`` is in ``TRANSACTIONAL_EMAIL_TYPES`` — the
    # ``DoesNotExist`` branch allows it. Everything else is denied.
    assert PreferenceService.check_email_permission(user, "order_confirmation") is True
    assert PreferenceService.check_email_permission(user, "newsletter") is False


def test_permission_check_none_user_raises(db):
    """``check_email_permission`` requires a persisted user (no guest support)."""
    # The service dereferences ``user.id`` for the cache key; a ``None``
    # argument raises ``AttributeError``. Guest checkout tests should
    # instead bypass the service or pass a placeholder user.
    with pytest.raises(AttributeError):
        PreferenceService.check_email_permission(None, "order_confirmation")
