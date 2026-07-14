"""
Tests for the admin_api push notification service.

The previous version of this file was a manual interactive script that
queried live production data and hit push.spwig.com. It has been
rewritten as a proper pytest suite that exercises PushNotificationService
behaviour with mocked network I/O so it runs deterministically in CI.

Covered surfaces:
- PushNotificationService.send_new_order_notification
- PushNotificationService.send_low_stock_notification
- PushNotificationService.send_customer_message_notification
- PushNotificationService.send_payment_alert_notification
- Device filtering via DeviceRegistration.get_devices_for_notification
- Invalid token cleanup path via _remove_invalid_tokens
- Configuration probe via PushNotificationService.is_configured
"""

from unittest.mock import MagicMock, patch

import pytest

from admin_api.models import CustomerMessage, DeviceRegistration
from admin_api.services.push_client import PushResult
from admin_api.services.push_service import PushNotificationService
from tests.factories import (
    CustomerMessageFactory,
    OrderFactory,
    OrderNoteFactory,
    ProductFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db]


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def _make_device(user, *, platform="ios", token=None, **prefs):
    """Create a DeviceRegistration with sensible defaults for tests."""
    import uuid

    defaults = {
        "device_id": f"dev-{uuid.uuid4().hex[:8]}",
        "push_token": token or f"apns-token-{uuid.uuid4().hex}",
        "platform": platform,
        "notify_new_orders": True,
        "notify_low_stock": True,
        "notify_customer_messages": True,
        "is_active": True,
    }
    defaults.update(prefs)
    return DeviceRegistration.objects.create(user=user, **defaults)


def _push_result(*, sent=1, failed=0, results=None):
    """Build a PushResult stand-in that _send_notification_batch expects."""
    return PushResult(
        success=(sent > 0 and failed == 0),
        sent=sent,
        failed=failed,
        results=results if results is not None else [],
    )


@pytest.fixture
def staff_user():
    return UserFactory(is_staff=True)


@pytest.fixture
def ios_device(staff_user):
    return _make_device(staff_user, token="apns-ios-primary")


@pytest.fixture
def mock_client():
    """
    Patch PushClient at the point PushNotificationService imports it.

    The service creates a new client via cls._get_client(); the returned
    MagicMock is populated by each test with a PushResult return value.
    """
    with patch("admin_api.services.push_service.PushClient") as mock_cls:
        instance = MagicMock()
        # Default: single-token success
        instance.send_notification.return_value = _push_result(
            sent=1, failed=0, results=[{"token": "apns-ios-primary", "status": "sent"}]
        )
        instance.is_configured.return_value = True
        mock_cls.return_value = instance
        yield instance


# ---------------------------------------------------------------------------
# is_configured
# ---------------------------------------------------------------------------


class TestIsConfigured:
    def test_returns_true_when_client_is_configured(self, mock_client):
        mock_client.is_configured.return_value = True
        assert PushNotificationService.is_configured() is True

    def test_returns_false_when_client_reports_not_configured(self, mock_client):
        mock_client.is_configured.return_value = False
        assert PushNotificationService.is_configured() is False

    def test_returns_false_when_client_raises(self):
        with patch(
            "admin_api.services.push_service.PushClient",
            side_effect=RuntimeError("boom"),
        ):
            assert PushNotificationService.is_configured() is False


# ---------------------------------------------------------------------------
# Device selection
# ---------------------------------------------------------------------------


class TestDeviceFiltering:
    def test_get_devices_for_new_order_respects_preference(self, staff_user):
        active_opted_in = _make_device(staff_user, notify_new_orders=True)
        _make_device(UserFactory(is_staff=True), notify_new_orders=False)  # opted out

        qs = DeviceRegistration.get_devices_for_notification("new_order")

        assert list(qs.values_list("id", flat=True)) == [active_opted_in.id]

    def test_get_devices_for_low_stock_respects_preference(self, staff_user):
        opted_in = _make_device(staff_user, notify_low_stock=True)
        _make_device(UserFactory(is_staff=True), notify_low_stock=False)

        qs = DeviceRegistration.get_devices_for_notification("low_stock")

        assert list(qs.values_list("id", flat=True)) == [opted_in.id]

    def test_get_devices_excludes_inactive(self, staff_user):
        active = _make_device(staff_user, is_active=True)
        _make_device(UserFactory(is_staff=True), is_active=False)

        qs = DeviceRegistration.get_devices_for_notification("customer_message")

        assert list(qs.values_list("id", flat=True)) == [active.id]

    def test_exclude_user_removes_that_users_devices(self, staff_user):
        _make_device(staff_user)
        other = UserFactory(is_staff=True)
        other_device = _make_device(other)

        qs = DeviceRegistration.get_devices_for_notification("new_order", exclude_user=staff_user)

        assert list(qs.values_list("id", flat=True)) == [other_device.id]


# ---------------------------------------------------------------------------
# send_new_order_notification
# ---------------------------------------------------------------------------


class TestSendNewOrderNotification:
    def test_sends_to_ios_device_and_returns_count(self, ios_device, mock_client):
        order = OrderFactory()
        mock_client.send_notification.return_value = _push_result(
            sent=1, results=[{"token": ios_device.push_token, "status": "sent"}]
        )

        sent = PushNotificationService.send_new_order_notification(order)

        assert sent == 1
        assert mock_client.send_notification.called
        call_kwargs = mock_client.send_notification.call_args.kwargs
        assert call_kwargs["title"] == "New Order Received"
        assert order.order_number in call_kwargs["body"]
        assert call_kwargs["data"]["type"] == "new_order"
        assert call_kwargs["data"]["order_number"] == order.order_number
        assert call_kwargs["data"]["order_id"] == order.id
        assert ios_device.push_token in call_kwargs["tokens"]

    def test_no_devices_returns_zero_and_skips_network(self, mock_client):
        order = OrderFactory()

        sent = PushNotificationService.send_new_order_notification(order)

        assert sent == 0
        mock_client.send_notification.assert_not_called()

    def test_opted_out_device_receives_nothing(self, staff_user, mock_client):
        _make_device(staff_user, notify_new_orders=False)
        order = OrderFactory()

        sent = PushNotificationService.send_new_order_notification(order)

        assert sent == 0
        mock_client.send_notification.assert_not_called()

    def test_android_devices_are_skipped(self, staff_user, mock_client):
        _make_device(staff_user, platform="android")
        order = OrderFactory()

        sent = PushNotificationService.send_new_order_notification(order)

        assert sent == 0
        mock_client.send_notification.assert_not_called()


# ---------------------------------------------------------------------------
# send_low_stock_notification
# ---------------------------------------------------------------------------


class TestSendLowStockNotification:
    def test_sends_with_product_metadata(self, ios_device, mock_client):
        product = ProductFactory()
        mock_client.send_notification.return_value = _push_result(
            sent=1, results=[{"token": ios_device.push_token, "status": "sent"}]
        )

        sent = PushNotificationService.send_low_stock_notification(product, 3)

        assert sent == 1
        call_kwargs = mock_client.send_notification.call_args.kwargs
        assert call_kwargs["title"] == "Low Stock Alert"
        assert product.name in call_kwargs["body"]
        assert "3" in call_kwargs["body"]
        assert call_kwargs["data"]["type"] == "low_stock"
        assert call_kwargs["data"]["product_id"] == product.id
        assert call_kwargs["data"]["sku"] == product.sku
        assert call_kwargs["data"]["current_stock"] == 3

    def test_opted_out_device_receives_nothing(self, staff_user, mock_client):
        _make_device(staff_user, notify_low_stock=False)
        product = ProductFactory()

        sent = PushNotificationService.send_low_stock_notification(product, 2)

        assert sent == 0
        mock_client.send_notification.assert_not_called()


# ---------------------------------------------------------------------------
# send_customer_message_notification
# ---------------------------------------------------------------------------


class TestSendCustomerMessageNotification:
    def test_contact_form_source_uses_message_attrs(self, ios_device, mock_client):
        message = CustomerMessageFactory(name="Jane Doe", subject="Help please")
        mock_client.send_notification.return_value = _push_result(
            sent=1, results=[{"token": ios_device.push_token, "status": "sent"}]
        )

        sent = PushNotificationService.send_customer_message_notification(
            message, source="contact_form"
        )

        assert sent == 1
        call_kwargs = mock_client.send_notification.call_args.kwargs
        assert call_kwargs["title"] == "New Customer Message"
        assert "Jane Doe" in call_kwargs["body"]
        assert "Help please" in call_kwargs["body"]
        assert call_kwargs["data"]["source"] == "contact_form"
        assert call_kwargs["data"]["message_id"] == message.id
        assert call_kwargs["data"]["sender_name"] == "Jane Doe"

    def test_order_note_source_uses_order_metadata(self, ios_device, mock_client):
        note = OrderNoteFactory(customer_note=True, note="Please expedite")
        order = note.order
        mock_client.send_notification.return_value = _push_result(
            sent=1, results=[{"token": ios_device.push_token, "status": "sent"}]
        )

        sent = PushNotificationService.send_customer_message_notification(note, source="order_note")

        assert sent == 1
        call_kwargs = mock_client.send_notification.call_args.kwargs
        assert call_kwargs["title"] == "New Customer Message"
        assert order.order_number in call_kwargs["body"]
        assert call_kwargs["data"]["source"] == "order_note"
        assert call_kwargs["data"]["order_number"] == order.order_number
        assert call_kwargs["data"]["order_id"] == order.id

    def test_invalid_source_raises_value_error(self, ios_device, mock_client):
        message = CustomerMessageFactory()

        with pytest.raises(ValueError, match="Invalid source"):
            PushNotificationService.send_customer_message_notification(message, source="bogus")

    def test_opted_out_device_receives_nothing(self, staff_user, mock_client):
        _make_device(staff_user, notify_customer_messages=False)
        message = CustomerMessageFactory()

        sent = PushNotificationService.send_customer_message_notification(
            message, source="contact_form"
        )

        assert sent == 0
        mock_client.send_notification.assert_not_called()


# ---------------------------------------------------------------------------
# send_payment_alert_notification
# ---------------------------------------------------------------------------


class TestSendPaymentAlertNotification:
    def test_alert_targets_all_active_ios_devices_regardless_of_prefs(
        self, staff_user, mock_client
    ):
        # This device has ALL notification prefs disabled — payment alerts
        # ignore preferences by design.
        device = _make_device(
            staff_user,
            notify_new_orders=False,
            notify_low_stock=False,
            notify_customer_messages=False,
        )
        order = OrderFactory()
        mock_client.send_notification.return_value = _push_result(
            sent=1, results=[{"token": device.push_token, "status": "sent"}]
        )

        sent = PushNotificationService.send_payment_alert_notification(order, alert_type="failed")

        assert sent == 1
        call_kwargs = mock_client.send_notification.call_args.kwargs
        assert call_kwargs["title"] == "Payment Alert"
        assert "failed" in call_kwargs["body"].lower()
        assert order.order_number in call_kwargs["body"]
        assert call_kwargs["data"]["type"] == "payment_alert"
        assert call_kwargs["data"]["alert_type"] == "failed"

    def test_fraud_risk_body_contains_hint(self, ios_device, mock_client):
        order = OrderFactory()
        mock_client.send_notification.return_value = _push_result(
            sent=1, results=[{"token": ios_device.push_token, "status": "sent"}]
        )

        PushNotificationService.send_payment_alert_notification(
            order, alert_type="fraud_risk", details="score=0.92"
        )

        call_kwargs = mock_client.send_notification.call_args.kwargs
        assert "risk" in call_kwargs["body"].lower()
        assert "score=0.92" in call_kwargs["body"]

    def test_no_devices_returns_zero(self, mock_client):
        order = OrderFactory()

        sent = PushNotificationService.send_payment_alert_notification(order, alert_type="failed")

        assert sent == 0
        mock_client.send_notification.assert_not_called()


# ---------------------------------------------------------------------------
# Invalid token cleanup
# ---------------------------------------------------------------------------


class TestInvalidTokenCleanup:
    def test_invalid_tokens_are_removed_from_registrations(self, staff_user, mock_client):
        bad = _make_device(staff_user, token="bad-token")
        good = _make_device(UserFactory(is_staff=True), token="good-token")
        order = OrderFactory()

        mock_client.send_notification.return_value = _push_result(
            sent=1,
            failed=1,
            results=[
                {
                    "token": "bad-token",
                    "status": "failed",
                    "should_remove_token": True,
                },
                {"token": "good-token", "status": "sent"},
            ],
        )

        PushNotificationService.send_new_order_notification(order)

        assert not DeviceRegistration.objects.filter(id=bad.id).exists()
        assert DeviceRegistration.objects.filter(id=good.id).exists()

    def test_successful_send_updates_last_notification_at(self, ios_device, mock_client):
        order = OrderFactory()
        mock_client.send_notification.return_value = _push_result(
            sent=1,
            results=[{"token": ios_device.push_token, "status": "sent"}],
        )

        assert ios_device.last_notification_at is None
        PushNotificationService.send_new_order_notification(order)

        ios_device.refresh_from_db()
        assert ios_device.last_notification_at is not None
        assert ios_device.failed_attempts == 0

    def test_failed_send_increments_failed_attempts(self, ios_device, mock_client):
        order = OrderFactory()
        mock_client.send_notification.return_value = _push_result(
            sent=0,
            failed=1,
            results=[{"token": ios_device.push_token, "status": "failed"}],
        )

        PushNotificationService.send_new_order_notification(order)

        ios_device.refresh_from_db()
        assert ios_device.failed_attempts == 1
        assert ios_device.is_active is True  # not yet deactivated


# ---------------------------------------------------------------------------
# Model sanity
# ---------------------------------------------------------------------------


class TestDeviceRegistrationMethods:
    def test_mark_notification_sent_resets_failed_attempts(self, staff_user):
        device = _make_device(staff_user)
        device.failed_attempts = 3
        device.save(update_fields=["failed_attempts"])

        device.mark_notification_sent()

        device.refresh_from_db()
        assert device.failed_attempts == 0
        assert device.last_notification_at is not None

    def test_mark_notification_failed_deactivates_after_five(self, staff_user):
        device = _make_device(staff_user)
        for _ in range(4):
            device.mark_notification_failed()

        device.refresh_from_db()
        assert device.failed_attempts == 4
        assert device.is_active is True

        device.mark_notification_failed()
        device.refresh_from_db()
        assert device.failed_attempts == 5
        assert device.is_active is False

    def test_str_contains_email_and_platform(self, staff_user):
        device = _make_device(staff_user, platform="ios")
        rendered = str(device)
        assert staff_user.email in rendered
        assert "ios" in rendered


class TestCustomerMessageFactory:
    def test_factory_creates_saved_message(self):
        msg = CustomerMessageFactory()
        assert msg.pk is not None
        assert CustomerMessage.objects.filter(pk=msg.pk).exists()
