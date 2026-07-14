"""
SMS System Preference Integration Tests.

Tests SMS sending with preference checking and skipped status tracking.
"""

from unittest.mock import Mock, patch

import pytest
from django.contrib.auth import get_user_model

from accounts.models import CustomerProfile
from sms_system.models import SMSOutbox, SMSProviderAccount
from sms_system.services.sms_sender import SMSSendingService
from tests.factories import UserFactory

User = get_user_model()

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.sms_preferences]


# ============================================================
# Fixtures
# ============================================================


@pytest.fixture(autouse=True)
def _disable_sandbox_mode():
    """SMS sandbox mode routes unwhitelisted numbers to ``sandbox_logged``.
    Preference tests here exercise the preference guard, not the sandbox
    guard, so we neutralise it."""
    with (
        patch("core.license.is_sandbox_mode", return_value=False),
        patch("core.sandbox.sms_guard.is_sandbox_mode", return_value=False),
    ):
        yield


@pytest.fixture
def sms_service():
    """SMS sending service instance."""
    return SMSSendingService()


@pytest.fixture
def sms_account(db, _integration_django_site):
    """SMS provider account with default_sms=True on the shared site."""
    account = SMSProviderAccount(
        site=_integration_django_site,
        provider_key="twilio",
        display_name="Test Twilio",
        is_default_sms=True,
        is_active=True,
    )
    account.set_credentials(
        {
            "account_sid": "test_sid",
            "auth_token": "test_token",
            "from_number": "+15555551234",
        }
    )
    account.save()
    return account


@pytest.fixture
def user_with_sms_opted_in(db):
    """User with SMS transactional and marketing enabled + verified."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.sms_enabled = True
    prefs.sms_transactional = True
    prefs.sms_marketing = True
    prefs.sms_verified = True
    prefs.save()

    # Create CustomerProfile with phone
    CustomerProfile.objects.update_or_create(user=user, defaults={"phone": "+15555555555"})

    return user


@pytest.fixture
def user_without_sms(db):
    """User who opted out of SMS."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.sms_enabled = False
    prefs.sms_transactional = False
    prefs.sms_marketing = False
    prefs.save()

    # Create CustomerProfile with phone
    CustomerProfile.objects.update_or_create(user=user, defaults={"phone": "+15555555556"})

    return user


@pytest.fixture
def mock_sms_provider():
    """Mock SMS provider that returns success."""
    with patch("sms_system.services.sms_sender.SMSSendingService._get_provider") as mock:
        provider = Mock()
        provider.send_sms.return_value = {"success": True, "message_id": "test_msg_123"}
        mock.return_value = provider
        yield provider


# ============================================================
# send_sms with Preference Checking
# ============================================================


def test_send_sms_transactional_sent_when_opted_in(
    sms_service, sms_account, user_with_sms_opted_in, mock_sms_provider
):
    """Transactional SMS sent when user opted in and verified."""
    phone = user_with_sms_opted_in.profile.phone

    result = sms_service.send_sms(
        phone=phone,
        message="Your order has shipped!",
        message_type="order_shipped",
    )

    assert result["success"] is True
    assert "outbox_id" in result

    # Check outbox entry
    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "sent"
    assert outbox.phone == phone


def test_send_sms_skipped_when_opted_out(sms_service, sms_account, user_without_sms):
    """SMS skipped when user has SMS disabled."""
    phone = user_without_sms.profile.phone

    result = sms_service.send_sms(
        phone=phone,
        message="Your order has shipped!",
        message_type="order_shipped",
    )

    assert result["success"] is False
    assert result.get("skipped") is True
    assert result.get("reason") == "user_preference_disabled"

    # Check outbox entry has skipped status
    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "skipped"
    assert outbox.skip_reason == "user_preference_disabled"


def test_send_sms_marketing_requires_opt_in(sms_service, sms_account, mock_sms_provider):
    """Marketing SMS requires explicit sms_marketing=True."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.sms_enabled = True
    prefs.sms_transactional = True
    prefs.sms_marketing = False  # Not opted into marketing
    prefs.sms_verified = True
    prefs.save()

    CustomerProfile.objects.update_or_create(user=user, defaults={"phone": "+15555555557"})
    phone = user.profile.phone

    result = sms_service.send_sms(
        phone=phone,
        message="Special offer for you!",
        message_type="promotional_offers",
    )

    assert result["success"] is False
    assert result.get("skipped") is True

    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "skipped"


def test_send_sms_marketing_sent_when_opted_in(
    sms_service, sms_account, user_with_sms_opted_in, mock_sms_provider
):
    """Marketing SMS sent when user explicitly opted in."""
    phone = user_with_sms_opted_in.profile.phone

    result = sms_service.send_sms(
        phone=phone,
        message="Special offer for you!",
        message_type="promotional_offers",
    )

    assert result["success"] is True

    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "sent"


def test_send_sms_guest_user_sent_normally(sms_service, sms_account, mock_sms_provider):
    """SMS to non-registered phone numbers (guests) are sent normally."""
    guest_phone = "+15555559999"

    # Phone doesn't exist in CustomerProfile
    assert not CustomerProfile.objects.filter(phone=guest_phone).exists()

    result = sms_service.send_sms(
        phone=guest_phone,
        message="Your order has shipped!",
        message_type="order_shipped",
    )

    # Should send successfully (guest checkout scenario)
    assert result["success"] is True

    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "sent"


# ============================================================
# send_template_sms with Preferences
# ============================================================


def test_send_template_sms_passes_message_type(sms_service, sms_account, user_without_sms):
    """send_template_sms passes template_type as message_type for preference check."""
    phone = user_without_sms.profile.phone

    with patch("sms_system.models.SMSTemplate.objects.get") as mock_get_template:
        # Mock template
        template = Mock()
        template.render.return_value = "Your order has shipped!"
        mock_get_template.return_value = template

        result = sms_service.send_template_sms(
            phone=phone,
            template_type="order_shipped",
            context={"order_number": "12345"},
        )

    # Should be skipped due to preferences (send_template_sms calls send_sms
    # internally which enforces the preference guard).
    assert result["success"] is False
    assert result.get("skipped") is True

    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "skipped"


# ============================================================
# SMS without message_type
# ============================================================


def test_send_sms_without_message_type_bypasses_check(
    sms_service, sms_account, user_without_sms, mock_sms_provider
):
    """SMS without message_type parameter bypasses preference checking."""
    phone = user_without_sms.profile.phone

    result = sms_service.send_sms(
        phone=phone,
        message="Generic SMS message",
        # No message_type specified
    )

    # Should be sent even though user has SMS disabled
    assert result["success"] is True

    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "sent"


# ============================================================
# SMSOutbox Status Tracking
# ============================================================


def test_skipped_status_recorded_in_sms_outbox(sms_service, sms_account, user_without_sms):
    """Skipped SMS are tracked in SMSOutbox with status='skipped'."""
    phone = user_without_sms.profile.phone

    result = sms_service.send_sms(
        phone=phone,
        message="Marketing SMS",
        message_type="promotional_offers",
    )

    assert result["success"] is False

    # Check outbox entry
    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "skipped"
    assert outbox.skip_reason == "user_preference_disabled"
    assert outbox.phone == phone


def test_skipped_sms_not_sent_to_provider(sms_service, sms_account, user_without_sms):
    """Skipped SMS are not sent to SMS provider."""
    phone = user_without_sms.profile.phone

    with patch(
        "sms_system.services.sms_sender.SMSSendingService._get_provider"
    ) as mock_get_provider:
        provider = Mock()
        mock_get_provider.return_value = provider

        sms_service.send_sms(
            phone=phone,
            message="Marketing SMS",
            message_type="promotional_offers",
        )

        # Provider should NOT be called
        assert not provider.send_sms.called


# ============================================================
# Master SMS Toggle
# ============================================================


def test_master_sms_toggle_blocks_all_sms(sms_service, sms_account):
    """sms_enabled=False blocks all SMS."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.sms_enabled = False
    prefs.sms_transactional = True  # Even with transactional enabled
    prefs.sms_marketing = True  # And marketing enabled
    prefs.sms_verified = True
    prefs.save()

    CustomerProfile.objects.update_or_create(user=user, defaults={"phone": "+15555555558"})
    phone = user.profile.phone

    # Transactional should be blocked
    result = sms_service.send_sms(
        phone=phone,
        message="Order shipped",
        message_type="order_shipped",
    )

    assert result["success"] is False
    assert result.get("skipped") is True

    # Marketing should also be blocked
    result2 = sms_service.send_sms(
        phone=phone,
        message="Promotion",
        message_type="promotional_offers",
    )

    assert result2["success"] is False
    assert result2.get("skipped") is True


# ============================================================
# Edge Cases
# ============================================================


def test_sms_to_user_without_customer_profile(sms_service, sms_account, mock_sms_provider):
    """SMS to user without CustomerProfile is sent normally (guest fallback)."""
    UserFactory()  # user without customer_profile phone

    # Try to send to a phone that doesn't match any profile
    result = sms_service.send_sms(
        phone="+15555550000",
        message="Test message",
        message_type="order_shipped",
    )

    # Should be sent (guest scenario)
    assert result["success"] is True


def test_sms_lookup_by_phone_number(sms_service, sms_account):
    """Preference check looks up user by phone number from CustomerProfile."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.sms_enabled = False
    prefs.save()

    phone = "+15555551111"
    CustomerProfile.objects.update_or_create(user=user, defaults={"phone": phone})

    result = sms_service.send_sms(
        phone=phone,
        message="Test",
        message_type="order_shipped",
    )

    # Should be skipped because preference lookup found user by phone
    assert result["success"] is False
    assert result.get("skipped") is True


def test_sms_provider_error_still_creates_outbox(sms_service, sms_account):
    """SMS provider errors are tracked in outbox as 'failed'."""
    user = UserFactory()
    prefs = user.communication_preferences
    prefs.sms_enabled = True
    prefs.sms_transactional = True
    prefs.sms_verified = True
    prefs.save()

    CustomerProfile.objects.update_or_create(user=user, defaults={"phone": "+15555551112"})
    phone = user.profile.phone

    # Mock provider that returns error
    with patch("sms_system.services.sms_sender.SMSSendingService._get_provider") as mock:
        provider = Mock()
        provider.send_sms.return_value = {"success": False, "error": "Provider error"}
        mock.return_value = provider

        result = sms_service.send_sms(
            phone=phone,
            message="Test",
            message_type="order_shipped",
        )

    assert result["success"] is False

    outbox = SMSOutbox.objects.get(pk=result["outbox_id"])
    assert outbox.status == "failed"
