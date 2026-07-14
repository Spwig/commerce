"""
Referrals Preference Integration Tests.

Tests that referral email notifications respect communication preferences.
"""

from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from email_system.models import EmailOutbox
from referrals.services.email_notifications import (
    send_referral_invitation_email,
    send_referral_reward_email,
    send_referral_successful_email,
    send_reward_expiring_email,
)
from tests.factories import EmailAccountFactory, UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.referrals_preferences]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture(autouse=True)
def _default_email_account(_integration_django_site):
    """Create default EmailAccount so send_template_email doesn't raise."""
    return EmailAccountFactory(default=True, site=_integration_django_site)


@pytest.fixture(autouse=True)
def _disable_sandbox_mode():
    """Neutralise sandbox mode so email pathway reaches the preference guard."""
    with (
        patch("core.license.is_sandbox_mode", return_value=False),
        patch("email_system.services.email_sender.is_sandbox_mode", return_value=False),
        patch("core.sandbox.email_guard.is_sandbox_mode", return_value=False),
    ):
        yield


@pytest.fixture(autouse=True)
def _mock_template_renderer():
    """Stub the template renderer — no EmailTemplate rows in the test DB."""
    with patch(
        "email_system.services.template_renderer.TemplateRenderer.render",
        return_value=("Test Subject", "<p>Test HTML</p>", "Test text"),
    ):
        yield


@pytest.fixture(autouse=True)
def _mock_referral_program():
    """Referral service reads ReferralProgram.get_program() and calls
    ``get_referee_reward()``. Provide a stub so tests don't need to seed
    ReferralProgram rows."""
    program = Mock()
    program.get_referee_reward.return_value = {"amount": "10%", "kind": "percent"}
    with patch("referrals.models.ReferralProgram.get_program", return_value=program, create=True):
        yield


@pytest.fixture
def user_with_referrals_enabled(db):
    """User with referrals emails enabled."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["referrals"]["enabled"] = True
    prefs.save()
    return user


@pytest.fixture
def user_with_referrals_disabled(db):
    """User who disabled referral emails."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["referrals"]["enabled"] = False
    prefs.save()
    return user


def _make_reward(customer):
    """Build a Mock ReferralReward suitable for the notifier."""
    reward = Mock()
    reward.customer = customer
    reward.amount = 10.00
    reward.get_kind_display = Mock(return_value="Store Credit")
    reward.expires_at = None
    reward.attribution = None
    reward.referrer_identity = None
    return reward


def _make_attribution(referrer):
    """Build a Mock ReferralAttribution for send_referral_successful_email."""
    attribution = Mock()
    identity = Mock()
    identity.customer = referrer
    identity.get_referral_link = Mock(return_value="https://shop.com/r/ABC123")
    attribution.referrer_identity = identity
    attribution.referee_customer = UserFactory()
    return attribution


# ============================================================
# Referral Reward Email - Preference Checking
# ============================================================


def test_referral_reward_email_sent_when_enabled(user_with_referrals_enabled):
    """Referral reward email sent when user has referrals enabled."""
    reward = _make_reward(user_with_referrals_enabled)

    result = send_referral_reward_email(reward, "referrer")

    assert result is True

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_enabled.email).first()
    assert outbox is not None
    assert outbox.status in ("pending", "queued")
    assert outbox.template_type == "referral_reward_issued_referrer"


def test_referral_reward_email_skipped_when_disabled(user_with_referrals_disabled):
    """Referral reward email skipped when user disabled referrals."""
    reward = _make_reward(user_with_referrals_disabled)

    result = send_referral_reward_email(reward, "referrer")

    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_disabled.email).first()
    assert outbox is not None
    assert outbox.status == "skipped"
    assert outbox.skip_reason == "user_preference_disabled"


def test_referral_reward_email_respects_email_verified(db):
    """Referral reward email requires email_verified=True."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = False  # Not verified
    prefs.app_preferences["referrals"]["enabled"] = True
    prefs.save()

    reward = _make_reward(user)
    result = send_referral_reward_email(reward, "referrer")

    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user.email).first()
    assert outbox is not None
    assert outbox.status == "skipped"


# ============================================================
# Referral Successful Email - Preference Checking
# ============================================================


def test_referral_successful_email_sent_when_enabled(user_with_referrals_enabled):
    """Referral successful email sent when enabled."""
    attribution = _make_attribution(user_with_referrals_enabled)
    result = send_referral_successful_email(attribution)

    assert result is True

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_enabled.email).first()
    assert outbox is not None
    assert outbox.status in ("pending", "queued")
    assert outbox.template_type == "referral_successful"


def test_referral_successful_email_skipped_when_disabled(user_with_referrals_disabled):
    """Referral successful email skipped when disabled."""
    attribution = _make_attribution(user_with_referrals_disabled)
    result = send_referral_successful_email(attribution)

    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_disabled.email).first()
    assert outbox is not None
    assert outbox.status == "skipped"


# ============================================================
# Reward Expiring Email - Preference Checking
# ============================================================


def test_reward_expiring_email_sent_when_enabled(user_with_referrals_enabled):
    """Reward expiring email sent when enabled."""
    reward = _make_reward(user_with_referrals_enabled)
    reward.expires_at = timezone.now() + timedelta(days=7)

    result = send_reward_expiring_email(reward, days_until_expiration=7)

    assert result is True

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_enabled.email).first()
    assert outbox is not None
    assert outbox.status in ("pending", "queued")
    assert outbox.template_type == "referral_reward_expiring"


def test_reward_expiring_email_skipped_when_disabled(user_with_referrals_disabled):
    """Reward expiring email skipped when disabled."""
    reward = _make_reward(user_with_referrals_disabled)
    reward.expires_at = datetime.now() + timedelta(days=7)

    result = send_reward_expiring_email(reward, days_until_expiration=7)

    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_disabled.email).first()
    assert outbox is not None
    assert outbox.status == "skipped"


# ============================================================
# Referral Invitation Email - Guest Handling
# ============================================================


def test_referral_invitation_sent_to_guest(user_with_referrals_enabled):
    """Referral invitation to non-registered user (guest) is sent."""
    guest_email = "newuser@example.com"

    # Guest doesn't exist in system
    assert not User.objects.filter(email=guest_email).exists()

    result = send_referral_invitation_email(
        referrer=user_with_referrals_enabled,
        referee_email=guest_email,
        personal_message="Join me!",
    )

    # Should be sent (guest users bypass preference checks)
    assert result is True

    outbox = EmailOutbox.objects.filter(to_email=guest_email).first()
    assert outbox is not None
    assert outbox.status in ("pending", "queued")
    assert outbox.template_type == "referral_invitation"


def test_referral_invitation_respects_registered_user_preferences(user_with_referrals_disabled):
    """Referral invitation to registered user respects their preferences."""
    result = send_referral_invitation_email(
        referrer=UserFactory(),
        referee_email=user_with_referrals_disabled.email,
        personal_message="Join me!",
    )

    # Should be skipped (registered user with referrals disabled)
    assert result is False

    outbox = EmailOutbox.objects.filter(to_email=user_with_referrals_disabled.email).first()
    assert outbox is not None
    assert outbox.status == "skipped"


# ============================================================
# Edge Cases
# ============================================================


def test_referral_email_uses_communication_preference_language(db):
    """Referral emails read language from CommunicationPreference.language_code."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.email_marketing = True
    prefs.email_verified = True
    prefs.app_preferences["referrals"]["enabled"] = True
    prefs.language_code = "fr"
    prefs.save()

    reward = _make_reward(user)

    # Should not crash, uses CommunicationPreference language
    result = send_referral_reward_email(reward, "referrer")

    assert result is True
