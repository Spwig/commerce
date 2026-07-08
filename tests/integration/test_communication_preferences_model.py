"""
Communication Preferences Model Tests.

Tests CommunicationPreference model creation, defaults, methods, and behavior.
"""
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import CommunicationPreference
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.communication_preferences]


# ============================================================
# Model Creation & Defaults
# ============================================================

def test_communication_preference_created_on_user_save(db):
    """CommunicationPreference auto-created via post_save signal when user is created."""
    user = UserFactory()

    # Should auto-create preference
    assert hasattr(user, 'communication_preferences')
    prefs = user.communication_preferences

    # Check defaults (GDPR opt-out for marketing)
    assert prefs.email_enabled is True
    assert prefs.sms_enabled is False  # SMS requires explicit opt-in
    assert prefs.email_transactional is True
    assert prefs.email_marketing is False  # GDPR opt-out
    assert prefs.sms_transactional is False
    assert prefs.sms_marketing is False
    assert prefs.email_verified is False
    assert prefs.sms_verified is False
    assert prefs.language_code == 'en'


def test_unsubscribe_token_auto_generated(db):
    """Unsubscribe token is auto-generated on save and is unique."""
    user1 = UserFactory()
    user2 = UserFactory()

    prefs1 = user1.communication_preferences
    prefs2 = user2.communication_preferences

    # Tokens should be generated
    assert prefs1.unsubscribe_token
    assert prefs2.unsubscribe_token
    assert len(prefs1.unsubscribe_token) == 64

    # Tokens should be unique
    assert prefs1.unsubscribe_token != prefs2.unsubscribe_token


def test_default_app_preferences_structure(db):
    """app_preferences JSONField has correct default structure."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Should have all app sections
    assert 'blog' in prefs.app_preferences
    assert 'loyalty' in prefs.app_preferences
    assert 'referrals' in prefs.app_preferences
    assert 'affiliate' in prefs.app_preferences

    # Blog defaults
    assert prefs.app_preferences['blog']['enabled'] is True
    assert prefs.app_preferences['blog']['frequency'] == 'weekly'
    assert prefs.app_preferences['blog']['categories'] == []

    # Loyalty defaults
    loyalty = prefs.app_preferences['loyalty']
    assert loyalty['enabled'] is True
    assert loyalty['frequency'] == 'immediate'
    assert loyalty['points_earned'] is True
    assert loyalty['tier_changes'] is True
    assert loyalty['rewards_available'] is True
    assert loyalty['points_expiring'] is True
    assert loyalty['birthday_bonus'] is True
    assert loyalty['campaign_offers'] is False  # Marketing opt-out


def test_consent_metadata_recorded(db):
    """Consent tracking fields are populated correctly."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Should have consent metadata
    assert prefs.consent_source == 'registration'
    assert prefs.consent_timestamp is not None
    assert isinstance(prefs.consent_timestamp, timezone.datetime)


# ============================================================
# Model Methods - should_send_email
# ============================================================

def test_should_send_email_transactional_always_true(db):
    """Transactional emails always allowed regardless of preferences."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Even with all email disabled
    prefs.email_enabled = False
    prefs.email_transactional = False
    prefs.save()

    # Transactional types still allowed
    assert prefs.should_send_email('order_confirmation') is True
    assert prefs.should_send_email('order_shipped') is True
    assert prefs.should_send_email('password_reset') is True


def test_should_send_email_marketing_requires_verified(db):
    """Marketing emails require email_marketing=True AND email_verified=True."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Opted in but not verified
    prefs.email_marketing = True
    prefs.email_verified = False
    prefs.save()

    assert prefs.should_send_email('newsletter') is False

    # Verified but not opted in
    prefs.email_marketing = False
    prefs.email_verified = True
    prefs.save()

    assert prefs.should_send_email('newsletter') is False

    # Both opted in and verified
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    assert prefs.should_send_email('newsletter') is True


def test_should_send_email_app_specific(db):
    """App-specific email types check app preferences."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Enable marketing and verify
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    # Blog enabled
    assert prefs.should_send_email('blog_post_published') is True

    # Disable blog
    prefs.app_preferences['blog']['enabled'] = False
    prefs.save()

    assert prefs.should_send_email('blog_post_published') is False

    # Loyalty - specific event disabled
    prefs.app_preferences['loyalty']['campaign_offers'] = False
    prefs.save()

    assert prefs.should_send_email('loyalty_campaign_offer') is False

    # But other loyalty events still enabled
    assert prefs.should_send_email('loyalty_points_earned') is True


def test_should_send_email_master_toggle(db):
    """email_enabled=False blocks all emails except critical transactional."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Set everything to true
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.save()

    # Disable master toggle
    prefs.email_enabled = False
    prefs.save()

    # Critical transactional still work
    assert prefs.should_send_email('order_confirmation') is True
    assert prefs.should_send_email('password_reset') is True

    # Everything else blocked
    assert prefs.should_send_email('newsletter') is False
    assert prefs.should_send_email('blog_post_published') is False
    assert prefs.should_send_email('loyalty_points_earned') is False


# ============================================================
# Model Methods - should_send_sms
# ============================================================

def test_should_send_sms_requires_opt_in(db):
    """All SMS requires explicit opt-in (TCPA compliance)."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Default state - all SMS disabled
    assert prefs.should_send_sms('order_shipped') is False
    assert prefs.should_send_sms('promotional_offer') is False

    # Enable transactional SMS
    prefs.sms_transactional = True
    prefs.save()

    assert prefs.should_send_sms('order_shipped') is True
    assert prefs.should_send_sms('promotional_offer') is False  # Still needs marketing opt-in

    # Enable marketing SMS
    prefs.sms_marketing = True
    prefs.save()

    assert prefs.should_send_sms('promotional_offer') is True


def test_should_send_sms_master_toggle(db):
    """sms_enabled=False blocks all SMS."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Enable both transactional and marketing
    prefs.sms_transactional = True
    prefs.sms_marketing = True
    prefs.save()

    # Disable master toggle
    prefs.sms_enabled = False
    prefs.save()

    assert prefs.should_send_sms('order_shipped') is False
    assert prefs.should_send_sms('promotional_offer') is False


# ============================================================
# Model Methods - get_app_preference / update_app_preference
# ============================================================

def test_get_app_preference_returns_value(db):
    """get_app_preference retrieves nested app preference values."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Get nested value
    assert prefs.get_app_preference('blog', 'enabled') is True
    assert prefs.get_app_preference('blog', 'frequency') == 'weekly'
    assert prefs.get_app_preference('loyalty', 'points_earned') is True

    # Get with default for missing key
    assert prefs.get_app_preference('blog', 'nonexistent', default='fallback') == 'fallback'
    assert prefs.get_app_preference('nonexistent_app', 'key', default=None) is None


def test_update_app_preference_modifies_json(db):
    """update_app_preference modifies nested app preferences."""
    user = UserFactory()
    prefs = user.communication_preferences

    # Update a single key
    prefs.update_app_preference('blog', {'frequency': 'immediate'})
    prefs.refresh_from_db()

    assert prefs.app_preferences['blog']['frequency'] == 'immediate'
    # Other keys preserved
    assert prefs.app_preferences['blog']['enabled'] is True

    # Update multiple keys
    prefs.update_app_preference('loyalty', {
        'points_earned': False,
        'tier_changes': False,
    })
    prefs.refresh_from_db()

    assert prefs.app_preferences['loyalty']['points_earned'] is False
    assert prefs.app_preferences['loyalty']['tier_changes'] is False
    # Other keys preserved
    assert prefs.app_preferences['loyalty']['rewards_available'] is True


# ============================================================
# Edge Cases
# ============================================================

def test_preference_survives_user_updates(db):
    """CommunicationPreference persists when user model is updated."""
    user = UserFactory()
    original_token = user.communication_preferences.unsubscribe_token

    # Update user
    user.first_name = 'Updated'
    user.save()

    # Preference still exists with same token
    user.refresh_from_db()
    assert user.communication_preferences.unsubscribe_token == original_token


def test_unique_unsubscribe_token_constraint(db):
    """Unsubscribe tokens are unique across all users."""
    user1 = UserFactory()
    user2 = UserFactory()

    prefs1 = user1.communication_preferences
    prefs2 = user2.communication_preferences

    # Try to set duplicate token (should fail on save)
    prefs2.unsubscribe_token = prefs1.unsubscribe_token

    with pytest.raises(Exception):  # IntegrityError
        prefs2.save()
