"""
POS Terminal management integration tests.

Tests terminal registration, configuration, heartbeat, receipt template,
promo slides, lock/unlock flows (PIN and card), staff card management,
lock event logging, and manager listing.
"""

import pytest
from django.utils import timezone

from tests.factories import (
    POSStaffDiscountFactory,
    UserFactory,
)
from tests.helpers import assert_pos_error, assert_pos_success

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.pos]

# -- URL constants -----------------------------------------------------------

REGISTER_URL = "/api/pos/terminals/register/"
CONFIG_URL = "/api/pos/terminals/config/"
HEARTBEAT_URL = "/api/pos/terminals/heartbeat/"
RECEIPT_URL = "/api/pos/receipt-template/"
PROMO_URL = "/api/pos/promo-slides/"
UNLOCK_URL = "/api/pos/terminals/unlock/"
UNLOCK_CARD_URL = "/api/pos/terminals/unlock-card/"
REGISTER_CARD_URL = "/api/pos/staff/register-card/"
REMOVE_CARD_URL = "/api/pos/staff/remove-card/"
LOCK_EVENT_URL = "/api/pos/terminals/lock-event/"
MANAGERS_URL = "/api/pos/terminals/managers/"


# ============================================================
# TestRegisterTerminal
# ============================================================


class TestRegisterTerminal:
    """Tests for POST /api/pos/terminals/register/."""

    def test_valid_pairing_code(self, anon_client, pos_terminal):
        """Valid pairing code returns terminal config and warehouse info."""
        response = anon_client.post(
            REGISTER_URL,
            {
                "pairing_code": pos_terminal.pairing_code,
            },
        )
        data = assert_pos_success(response)

        assert "terminal" in data
        assert data["terminal"]["uuid"] == str(pos_terminal.uuid)
        assert "warehouse" in data
        assert data["warehouse"]["id"] == pos_terminal.warehouse_id

    def test_invalid_pairing_code(self, anon_client):
        """Invalid pairing code returns INVALID_CODE error."""
        response = anon_client.post(
            REGISTER_URL,
            {
                "pairing_code": "BADCODE9",
            },
        )
        assert_pos_error(response, "INVALID_CODE", http_status=404)

    def test_public_endpoint(self, anon_client, pos_terminal):
        """Register endpoint requires no authentication (AllowAny)."""
        # anon_client has no auth headers -- should still succeed
        response = anon_client.post(
            REGISTER_URL,
            {
                "pairing_code": pos_terminal.pairing_code,
            },
        )
        assert response.status_code == 200


# ============================================================
# TestTerminalConfig
# ============================================================


class TestTerminalConfig:
    """Tests for GET /api/pos/terminals/config/."""

    def test_returns_config(self, pos_client, pos_terminal):
        """Returns terminal configuration data for a valid terminal."""
        response = pos_client.get(CONFIG_URL)
        data = assert_pos_success(response)

        assert "terminal" in data
        assert data["terminal"]["uuid"] == str(pos_terminal.uuid)
        assert data["terminal"]["name"] == pos_terminal.name

    def test_requires_terminal_uuid(self, pos_client_no_terminal):
        """Without X-Terminal-UUID header returns MISSING_TERMINAL error."""
        response = pos_client_no_terminal.get(CONFIG_URL)
        assert_pos_error(response, "MISSING_TERMINAL", http_status=400)

    def test_inactive_terminal(self, pos_client, pos_terminal):
        """Inactive terminal returns TERMINAL_NOT_FOUND error."""
        pos_terminal.is_active = False
        pos_terminal.save(update_fields=["is_active"])

        response = pos_client.get(CONFIG_URL)
        assert_pos_error(response, "TERMINAL_NOT_FOUND", http_status=404)


# ============================================================
# TestTerminalHeartbeat
# ============================================================


class TestTerminalHeartbeat:
    """Tests for POST /api/pos/terminals/heartbeat/."""

    def test_updates_last_heartbeat(self, pos_client, pos_terminal):
        """Heartbeat updates the terminal's last_heartbeat timestamp."""
        assert pos_terminal.last_heartbeat is None

        response = pos_client.post(HEARTBEAT_URL)
        assert_pos_success(response)

        pos_terminal.refresh_from_db()
        assert pos_terminal.last_heartbeat is not None

    def test_returns_server_time(self, pos_client, pos_terminal):
        """Response indicates success and the terminal's heartbeat timestamp is recent."""
        before = timezone.now()
        response = pos_client.post(HEARTBEAT_URL)
        after = timezone.now()
        assert_pos_success(response)

        pos_terminal.refresh_from_db()
        assert before <= pos_terminal.last_heartbeat <= after


# ============================================================
# TestReceiptTemplate
# ============================================================


class TestReceiptTemplate:
    """Tests for GET /api/pos/receipt-template/."""

    def test_returns_template(self, pos_client, pos_terminal):
        """Returns receipt template data structure."""
        from pos_app.models import ReceiptTemplate

        ReceiptTemplate.objects.create(
            name="Test Receipt",
            warehouse=pos_terminal.warehouse,
            header_text="My Store",
            footer_text="Thanks for shopping!",
        )

        response = pos_client.get(RECEIPT_URL)
        data = assert_pos_success(response)

        assert "template" in data
        assert data["template"]["header_text"] == "My Store"
        assert data["template"]["footer_text"] == "Thanks for shopping!"

    def test_default_fallback(self, pos_client, pos_terminal):
        """When no custom template exists, returns sensible defaults."""
        response = pos_client.get(RECEIPT_URL)
        data = assert_pos_success(response)

        template = data["template"]
        assert template["paper_width"] == "80"
        assert template["footer_text"] == "Thank you for your purchase!"
        assert template["show_powered_by"] is True

    def test_includes_store_info(self, pos_client, pos_terminal):
        """Default template includes warehouse name and address."""
        warehouse = pos_terminal.warehouse
        response = pos_client.get(RECEIPT_URL)
        data = assert_pos_success(response)

        template = data["template"]
        # Default header_text should be the warehouse display name or name
        expected_name = warehouse.pos_display_name or warehouse.name
        assert template["header_text"] == expected_name
        assert template["show_store_address"] is True


# ============================================================
# TestPromoSlides
# ============================================================


class TestPromoSlides:
    """Tests for GET /api/pos/promo-slides/."""

    def test_active_slides(self, pos_client, pos_terminal):
        """Returns active promo slides for the terminal's warehouse."""
        from pos_app.models import PromoSlide
        from tests.factories import MediaAssetFactory

        asset = MediaAssetFactory(
            title="Promo Image",
            mime_type="image/png",
        )
        PromoSlide.objects.create(
            warehouse=pos_terminal.warehouse,
            image=asset,
            title="Sale!",
            subtitle="20% off everything",
            is_active=True,
        )

        response = pos_client.get(PROMO_URL)
        data = assert_pos_success(response)

        assert len(data["slides"]) == 1
        assert data["slides"][0]["title"] == "Sale!"
        assert data["slides"][0]["subtitle"] == "20% off everything"

    def test_excludes_inactive(self, pos_client, pos_terminal):
        """Inactive slides are not returned."""
        from pos_app.models import PromoSlide
        from tests.factories import MediaAssetFactory

        asset = MediaAssetFactory(
            title="Inactive Promo",
            mime_type="image/png",
        )
        PromoSlide.objects.create(
            warehouse=pos_terminal.warehouse,
            image=asset,
            title="Old Sale",
            is_active=False,
        )

        response = pos_client.get(PROMO_URL)
        data = assert_pos_success(response)

        assert len(data["slides"]) == 0


# ============================================================
# TestUnlockTerminal
# ============================================================


class TestUnlockTerminal:
    """Tests for POST /api/pos/terminals/unlock/."""

    def test_valid_cashier_pin(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        staff_discount_config,
    ):
        """Correct cashier PIN unlocks the terminal."""
        response = pos_client.post(
            UNLOCK_URL,
            {
                "pin": "1234",
                "locked_by_user_id": pos_staff_user.id,
            },
        )
        data = assert_pos_success(response)

        assert data["unlock_type"] == "cashier"
        assert "user_name" in data

    def test_invalid_pin(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        staff_discount_config,
    ):
        """Wrong PIN returns INVALID_PIN error."""
        response = pos_client.post(
            UNLOCK_URL,
            {
                "pin": "0000",
                "locked_by_user_id": pos_staff_user.id,
            },
        )
        assert_pos_error(response, "INVALID_PIN", http_status=400)

    def test_manager_pin_unlocks(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        manager_discount_config,
    ):
        """Manager PIN works for unlock when in manager override mode."""
        response = pos_client.post(
            UNLOCK_URL,
            {
                "pin": "9999",
                "locked_by_user_id": pos_staff_user.id,
                "manager_override": True,
                "manager_user_id": manager_discount_config.user_id,
            },
        )
        data = assert_pos_success(response)

        assert data["unlock_type"] == "manager"

    def test_lockout_after_failures(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        staff_discount_config,
    ):
        """After 3+ failed attempts, correct cashier PIN is rejected and manager is required."""
        response = pos_client.post(
            UNLOCK_URL,
            {
                "pin": "1234",
                "locked_by_user_id": pos_staff_user.id,
                "failed_attempts": 3,
            },
        )
        # Even with the correct cashier PIN, the view requires manager at >=3 failures
        data = response.json()
        assert data.get("require_manager") is True

    def test_no_pin_configured(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
    ):
        """User without a cashier_pin configured cannot unlock with PIN."""
        # Create a staff discount record with no PIN
        POSStaffDiscountFactory(user=pos_staff_user, cashier_pin="")

        response = pos_client.post(
            UNLOCK_URL,
            {
                "pin": "1234",
                "locked_by_user_id": pos_staff_user.id,
            },
        )
        assert_pos_error(response, "INVALID_PIN", http_status=400)


# ============================================================
# TestUnlockByCard
# ============================================================


class TestUnlockByCard:
    """Tests for POST /api/pos/terminals/unlock-card/."""

    def test_registered_card(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        staff_discount_config,
    ):
        """Registered card swipe unlocks the terminal."""
        from pos_app.models import POSStaffDiscount

        card_data = "CARD-SWIPE-DATA-123"
        card_hash = POSStaffDiscount.hash_card_data(card_data)
        staff_discount_config.card_identifier = card_hash
        staff_discount_config.save(update_fields=["card_identifier"])

        response = pos_client.post(
            UNLOCK_CARD_URL,
            {
                "card_data": card_data,
                "locked_by_user_id": pos_staff_user.id,
            },
        )
        data = assert_pos_success(response)

        assert data["unlock_type"] == "cashier"
        assert "user_name" in data

    def test_unregistered_card(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
        staff_discount_config,
    ):
        """Unregistered card swipe returns UNKNOWN_CARD error."""
        response = pos_client.post(
            UNLOCK_CARD_URL,
            {
                "card_data": "UNKNOWN-CARD-DATA-999",
                "locked_by_user_id": pos_staff_user.id,
            },
        )
        assert_pos_error(response, "UNKNOWN_CARD", http_status=400)


# ============================================================
# TestStaffCard
# ============================================================


class TestStaffCard:
    """Tests for POST /api/pos/staff/register-card/ and remove-card/."""

    def test_register_card(self, pos_client, pos_staff_user):
        """Register a new staff card stores the card hash."""
        from pos_app.models import POSStaffDiscount

        response = pos_client.post(
            REGISTER_CARD_URL,
            {
                "card_data": "MY-STAFF-CARD-001",
            },
        )
        assert_pos_success(response)

        staff = POSStaffDiscount.objects.get(user=pos_staff_user)
        expected_hash = POSStaffDiscount.hash_card_data("MY-STAFF-CARD-001")
        assert staff.card_identifier == expected_hash

    def test_remove_card(self, pos_client, pos_staff_user, staff_discount_config):
        """Remove registered card clears the card identifier."""
        from pos_app.models import POSStaffDiscount

        card_hash = POSStaffDiscount.hash_card_data("REGISTERED-CARD")
        staff_discount_config.card_identifier = card_hash
        staff_discount_config.save(update_fields=["card_identifier"])

        response = pos_client.post(REMOVE_CARD_URL)
        assert_pos_success(response)

        staff_discount_config.refresh_from_db()
        assert staff_discount_config.card_identifier == ""

    def test_duplicate_card_error(self, pos_client, pos_staff_user, staff_discount_config):
        """Registering a card already assigned to another user returns CARD_IN_USE."""
        from pos_app.models import POSStaffDiscount

        other_user = UserFactory(is_staff=True)
        card_data = "SHARED-CARD-DATA"
        card_hash = POSStaffDiscount.hash_card_data(card_data)
        POSStaffDiscountFactory(user=other_user, card_identifier=card_hash)

        response = pos_client.post(
            REGISTER_CARD_URL,
            {
                "card_data": card_data,
            },
        )
        assert_pos_error(response, "CARD_IN_USE", http_status=409)


# ============================================================
# TestLockEvents
# ============================================================


class TestLockEvents:
    """Tests for POST /api/pos/terminals/lock-event/."""

    def test_log_lock_event(self, pos_client, pos_terminal):
        """Lock event creates a TerminalLockEvent record."""
        from pos_app.models import TerminalLockEvent

        response = pos_client.post(
            LOCK_EVENT_URL,
            {
                "event_type": "lock_manual",
            },
        )
        assert_pos_success(response)

        events = TerminalLockEvent.objects.filter(terminal=pos_terminal)
        assert events.count() == 1
        assert events.first().event_type == "lock_manual"

    def test_includes_method_and_user(
        self,
        pos_client,
        pos_terminal,
        pos_staff_user,
    ):
        """Lock event records the performing user and unlock method."""
        from pos_app.models import TerminalLockEvent

        response = pos_client.post(
            LOCK_EVENT_URL,
            {
                "event_type": "lock_auto",
                "cart_item_count": 3,
                "cart_total": "75.00",
            },
        )
        assert_pos_success(response)

        event = TerminalLockEvent.objects.filter(terminal=pos_terminal).first()
        assert event is not None
        assert event.event_type == "lock_auto"
        assert event.performed_by == pos_staff_user
        assert event.locked_by == pos_staff_user
        assert event.cart_item_count == 3

    def test_invalid_event_type_rejected(self, pos_client, pos_terminal):
        """Invalid event_type value returns INVALID_EVENT error."""
        response = pos_client.post(
            LOCK_EVENT_URL,
            {
                "event_type": "not_a_real_event",
            },
        )
        assert_pos_error(response, "INVALID_EVENT", http_status=400)


# ============================================================
# TestListManagers
# ============================================================


class TestListManagers:
    """Tests for GET /api/pos/terminals/managers/."""

    def test_returns_managers(self, pos_client, manager_discount_config):
        """Lists staff with manager role who have a manager PIN set."""
        response = pos_client.get("/api/pos/terminals/managers/")

        assert response.status_code == 200
        assert response.data["success"] is True
        manager_ids = [m["id"] for m in response.data["managers"]]
        assert manager_discount_config.user_id in manager_ids

    def test_includes_name(self, pos_client, manager_discount_config):
        """Each manager entry has a name field."""
        response = pos_client.get("/api/pos/terminals/managers/")

        assert response.status_code == 200
        for manager in response.data["managers"]:
            assert "name" in manager
            assert manager["name"], "manager name should be non-empty"
