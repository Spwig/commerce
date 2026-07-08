"""
Referrals Preference Integration Tests.

Tests that referral email notifications respect communication preferences.
"""
import pytest
from unittest.mock import Mock, patch
from django.contrib.auth import get_user_model

from referrals.services.email_notifications import (
    send_referral_reward_email,
    send_referral_successful_email,
    send_reward_expiring_email,
    send_referral_invitation_email,
)
from email_system.models import EmailOutbox
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.referrals_preferences]


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def user_with_referrals_enabled(db):
    """User with referrals emails enabled."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences['referrals']['enabled'] = True
    prefs.save()
    return user


@pytest.fixture
def user_with_referrals_disabled(db):
    """User who disabled referral emails."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.app_preferences['referrals']['enabled'] = False
    prefs.save()
    return user


@pytest.fixture
def mock_reward(user_with_referrals_enabled):
    """Mock ReferralReward object."""
    reward = Mock()
    reward.customer = user_with_referrals_enabled
    reward.amount = 10.00
    reward.get_kind_display = Mock(return_value='Store Credit')
    reward.expires_at = None
    reward.attribution = None
    reward.referrer_identity = None
    return reward


@pytest.fixture
def mock_attribution(user_with_referrals_enabled):
    """Mock ReferralAttribution object."""
    attribution = Mock()
    identity = Mock()
    identity.customer = user_with_referrals_enabled
    identity.get_referral_link = Mock(return_value='https://shop.com/r/ABC123')
    attribution.referrer_identity = identity
    attribution.referee_customer = UserFactory()
    return attribution


# ============================================================
# Referral Reward Email - Preference Checking
# ============================================================

def test_referral_reward_email_sent_when_enabled(mock_reward, user_with_referrals_enabled):
    """Referral reward email sent when user has referrals enabled."""
    result = send_referral_reward_email(mock_reward, 'referrer')

    # Should be queued (returns True)
    assert result is True

    # Check outbox entry exists and is not skipped
    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_enabled.email).first()
    assert outbox is not None
    assert outbox.status in ['pending', 'queued']
    assert outbox.template_type == 'referral_reward_issued_referrer'


def test_referral_reward_email_skipped_when_disabled(user_with_referrals_disabled):
    """Referral reward email skipped when user disabled referrals."""
    reward = Mock()
    reward.customer = user_with_referrals_disabled
    reward.amount = 10.00
    reward.get_kind_display = Mock(return_value='Store Credit')
    reward.expires_at = None
    reward.attribution = None

    result = send_referral_reward_email(reward, 'referrer')

    # Should return False (skipped)
    assert result is False

    # Check outbox entry has skipped status
    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_disabled.email).first()
    assert outbox is not None
    assert outbox.status == 'skipped'
    assert outbox.skip_reason == 'user_preference_disabled'


def test_referral_reward_email_respects_email_verified(db):
    """Referral reward email requires email_verified=True."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = False  # Not verified
    prefs.app_preferences['referrals']['enabled'] = True
    prefs.save()

    reward = Mock()
    reward.customer = user
    reward.amount = 10.00
    reward.get_kind_display = Mock(return_value='Store Credit')
    reward.expires_at = None
    reward.attribution = None

    result = send_referral_reward_email(reward, 'referrer')

    # Should be skipped (not verified)
    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user.email).first()
    assert outbox.status == 'skipped'


# ============================================================
# Referral Successful Email - Preference Checking
# ============================================================

def test_referral_successful_email_sent_when_enabled(mock_attribution, user_with_referrals_enabled):
    """Referral successful email sent when enabled."""
    result = send_referral_successful_email(mock_attribution)

    assert result is True

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_enabled.email).first()
    assert outbox is not None
    assert outbox.status in ['pending', 'queued']
    assert outbox.template_type == 'referral_successful'


def test_referral_successful_email_skipped_when_disabled(user_with_referrals_disabled):
    """Referral successful email skipped when disabled."""
    attribution = Mock()
    identity = Mock()
    identity.customer = user_with_referrals_disabled
    identity.get_referral_link = Mock(return_value='https://shop.com/r/XYZ789')
    attribution.referrer_identity = identity
    attribution.referee_customer = UserFactory()

    result = send_referral_successful_email(attribution)

    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_disabled.email).first()
    assert outbox.status == 'skipped'


# ============================================================
# Reward Expiring Email - Preference Checking
# ============================================================

def test_reward_expiring_email_sent_when_enabled(mock_reward, user_with_referrals_enabled):
    """Reward expiring email sent when enabled."""
    from datetime import datetime, timedelta
    mock_reward.expires_at = datetime.now() + timedelta(days=7)

    result = send_reward_expiring_email(mock_reward, days_until_expiration=7)

    assert result is True

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_enabled.email).first()
    assert outbox is not None
    assert outbox.status in ['pending', 'queued']
    assert outbox.template_type == 'referral_reward_expiring'


def test_reward_expiring_email_skipped_when_disabled(user_with_referrals_disabled):
    """Reward expiring email skipped when disabled."""
    from datetime import datetime, timedelta

    reward = Mock()
    reward.customer = user_with_referrals_disabled
    reward.amount = 10.00
    reward.get_kind_display = Mock(return_value='Store Credit')
    reward.expires_at = datetime.now() + timedelta(days=7)

    result = send_reward_expiring_email(reward, days_until_expiration=7)

    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_disabled.email).first()
    assert outbox.status == 'skipped'


# ============================================================
# Referral Invitation Email - Guest Handling
# ============================================================

def test_referral_invitation_sent_to_guest(user_with_referrals_enabled):
    """Referral invitation to non-registered user (guest) is sent."""
    guest_email = 'newuser@example.com'

    # Guest doesn't exist in system
    assert not User.objects.filter(email=guest_email).exists()

    result = send_referral_invitation_email(
        referrer=user_with_referrals_enabled,
        referee_email=guest_email,
        personal_message='Join me!'
    )

    # Should be sent (guest users bypass preference checks)
    assert result is True

    outbox = EmailOutbox.objects.filter(to_email=guest_email).first()
    assert outbox is not None
    assert outbox.status in ['pending', 'queued']
    assert outbox.template_type == 'referral_invitation'


def test_referral_invitation_respects_registered_user_preferences(user_with_referrals_disabled):
    """Referral invitation to registered user respects their preferences."""
    result = send_referral_invitation_email(
        referrer=UserFactory(),
        referee_email=user_with_referrals_disabled.email,
        personal_message='Join me!'
    )

    # Should be skipped (registered user with referrals disabled)
    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_disabled.email).first()
    assert outbox.status == 'skipped'


# ============================================================
# Edge Cases
# ============================================================

def test_referral_email_uses_communication_preference_language(db):
    """Referral emails use CommunicationPreference.language_code for language."""
    user = UserFactory()

    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences['referrals']['enabled'] = True
    prefs.language_code = 'fr'
    prefs.save()

    reward = Mock()
    reward.customer = user
    reward.amount = 10.00
    reward.get_kind_display = Mock(return_value='Store Credit')
    reward.expires_at = None
    reward.attribution = None

    # Should not crash, uses CommunicationPreference language
    result = send_referral_reward_email(reward, 'referrer')

    assert result is True
