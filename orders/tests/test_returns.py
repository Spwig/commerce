"""
Tests for the Returns & RMA workflow (Phase 7).

This file focuses on the surfaces that are unique to this module and are not
already covered by ``tests/unit/test_orders_models.py``:

* the ``ReturnRequestViewSet.create_for_order`` custom action
  (``POST /api/return-requests/create-for-order/<order_number>/``), including
  its validation branches and access-control behaviour;
* the ``return_label`` custom action
  (``GET /api/return-requests/<pk>/return-label/``);
* the six ``orders.emails`` notification helpers -- verified by asserting
  that ``EmailSendingService.send_template_email`` is invoked with the
  correct ``template_type`` and recipient, since the platform routes all
  outbound mail through ``EmailOutbox`` rather than ``django.core.mail``;
* ``DocumentService.generate_return_label`` returns a well-formed PDF
  data-URI for a return request.

Model-level state transitions (approve / reject / mark_received /
mark_inspected / process_refund / complete / cancel / calculate_refund_amount
/ get_items_summary) are already covered by
``tests/unit/test_orders_models.py::TestReturnRequestModel`` -- we don't
duplicate them here.
"""

import base64
from decimal import Decimal
from unittest.mock import patch

import pytest
from djmoney.money import Money
from rest_framework import status
from rest_framework.test import APIClient

from orders.models import ReturnRequest
from tests.factories import (
    OrderFactory,
    OrderItemFactory,
    RefundFactory,
    ReturnRequestFactory,
    UserFactory,
)

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def _core_infra(site_settings, django_site):
    """Middleware (currency + geoip) reads ``SiteSettings`` on every
    request. Without a materialised row, the auto-``get_or_create``
    call in ``SiteSettings.get_settings`` triggers ``full_clean`` and
    fails on the required ``admin_email`` field, producing a 500 for
    every API test. Use the shared conftest fixtures so the row exists
    and matches the single-tenant invariant (``SITE_ID = 1``).
    """
    return site_settings


# ---------------------------------------------------------------------------
# ``create-for-order`` custom action
# ---------------------------------------------------------------------------


class TestCreateReturnForOrderAPI:
    """Cover ``POST /api/return-requests/create-for-order/<order_number>/``.

    The endpoint lives on ``ReturnRequestViewSet.create_for_order`` and is
    the customer-facing path for filing a new return; the standard
    ``POST /api/return-requests/`` route (tested in
    ``tests/integration/test_orders_api.py``) is a distinct surface.
    """

    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        # A paid, delivered order with a single 2-quantity item -- the state
        # that make an order eligible for returns.
        self.order = OrderFactory(
            user=self.user,
            paid_order=True,
            delivered=True,
        )
        self.order_item = OrderItemFactory(
            order=self.order,
            quantity=2,
            unit_price=Money(Decimal("100.00"), "USD"),
        )

    def _url(self, order_number=None):
        return f"/api/return-requests/create-for-order/{order_number or self.order.order_number}/"

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_create_return_request_success(self, mock_send):
        """A valid POST creates a ReturnRequest and queues the confirmation email.

        We assert on the confirmation call (template_type +
        recipient) rather than ``mail.outbox`` because the platform
        routes outbound mail through ``EmailOutbox`` via
        ``EmailSendingService``.
        """
        data = {
            "reason": "defective",
            "items": [
                {
                    "order_item_id": self.order_item.id,
                    "quantity": 1,
                    "reason": "defective",
                    "notes": "Screen flickering",
                }
            ],
            "customer_notes": "Would like replacement if possible",
        }

        response = self.client.post(self._url(), data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert "return_request" in response.data

        return_request = ReturnRequest.objects.get(order=self.order)
        assert return_request.reason == "defective"
        assert return_request.status == "pending"
        assert return_request.user == self.user
        assert return_request.customer_notes == "Would like replacement if possible"
        assert len(return_request.items_json) == 1
        assert return_request.items_json[0]["order_item_id"] == self.order_item.id
        assert return_request.items_json[0]["quantity"] == 1

        # Confirmation email was queued with the correct template + recipient.
        mock_send.assert_called()
        call_kwargs = mock_send.call_args.kwargs
        assert call_kwargs["template_type"] == "return_request_confirmation"
        assert call_kwargs["to_email"] == self.user.email

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_reject_non_delivered_order(self, mock_send):
        """Non-delivered orders return 400 with an explanatory message."""
        pending_order = OrderFactory(user=self.user, status="pending")

        response = self.client.post(
            self._url(pending_order.order_number),
            {
                "reason": "defective",
                "items": [
                    {"order_item_id": self.order_item.id, "quantity": 1, "reason": "defective"}
                ],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert "delivered orders" in str(response.data["message"])
        assert not ReturnRequest.objects.filter(order=pending_order).exists()
        # No confirmation email should be queued on rejection.
        mock_send.assert_not_called()

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_reject_quantity_exceeding_ordered(self, mock_send):
        """Requested quantity may not exceed the OrderItem's ordered quantity."""
        response = self.client.post(
            self._url(),
            {
                "reason": "defective",
                "items": [
                    {
                        "order_item_id": self.order_item.id,
                        "quantity": self.order_item.quantity + 5,
                        "reason": "defective",
                    }
                ],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert "cannot exceed ordered quantity" in str(response.data["message"])
        assert not ReturnRequest.objects.filter(order=self.order).exists()
        mock_send.assert_not_called()

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_reject_invalid_order_item_id(self, mock_send):
        """Referencing an order_item that doesn't belong to the order returns 400."""
        response = self.client.post(
            self._url(),
            {
                "reason": "defective",
                "items": [{"order_item_id": 999_999, "quantity": 1, "reason": "defective"}],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert "Invalid order item ID" in str(response.data["message"])
        assert not ReturnRequest.objects.filter(order=self.order).exists()
        mock_send.assert_not_called()

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_reject_order_belonging_to_another_user(self, mock_send):
        """``OrderService.get_order_detail`` scopes by user, so foreign
        orders return 404 (not 403)."""
        other_user = UserFactory()
        foreign_order = OrderFactory(user=other_user, paid_order=True, delivered=True)

        response = self.client.post(
            self._url(foreign_order.order_number),
            {
                "reason": "defective",
                "items": [{"order_item_id": 1, "quantity": 1, "reason": "defective"}],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["success"] is False
        assert not ReturnRequest.objects.filter(order=foreign_order).exists()
        mock_send.assert_not_called()

    def test_unauthenticated_access_denied(self):
        """Unauthenticated callers cannot create returns."""
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self._url(),
            {"reason": "defective", "items": []},
            format="json",
        )
        # DRF returns 401 (with token/session auth) or 403 (session-only)
        # depending on configuration -- accept either "not authenticated" code.
        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )


# ---------------------------------------------------------------------------
# ``return-label`` custom action
# ---------------------------------------------------------------------------


class TestReturnLabelAPI:
    """Cover ``GET /api/return-requests/<pk>/return-label/``."""

    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.order = OrderFactory(user=self.user, paid_order=True, delivered=True)

    def _url(self, pk):
        return f"/api/return-requests/{pk}/return-label/"

    def test_returns_label_when_generated(self):
        return_request = ReturnRequestFactory(
            order=self.order,
            user=self.user,
            status="label_sent",
            return_label_generated=True,
            return_label_url="https://example.com/label.pdf",
            return_tracking_number="TRACK123",
        )

        response = self.client.get(self._url(return_request.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["tracking_number"] == "TRACK123"
        assert response.data["label_url"] == "https://example.com/label.pdf"
        assert response.data["status"] == "label_sent"
        assert response.data["return_request_id"] == return_request.id

    def test_returns_404_when_label_not_generated(self):
        return_request = ReturnRequestFactory(
            order=self.order,
            user=self.user,
            status="pending",
            return_label_generated=False,
        )

        response = self.client.get(self._url(return_request.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["success"] is False
        assert "not been generated yet" in str(response.data["message"])

    def test_returns_404_when_label_url_missing(self):
        """``return_label_generated=True`` but no URL still returns 404."""
        return_request = ReturnRequestFactory(
            order=self.order,
            user=self.user,
            status="label_sent",
            return_label_generated=True,
            return_label_url="",  # generated flag flipped but URL missing
            return_tracking_number="TRACK-EMPTY",
        )

        response = self.client.get(self._url(return_request.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["success"] is False

    def test_user_cannot_access_other_users_label(self):
        other_user = UserFactory()
        other_order = OrderFactory(user=other_user, paid_order=True, delivered=True)
        foreign_return = ReturnRequestFactory(
            order=other_order,
            user=other_user,
            status="label_sent",
            return_label_generated=True,
            return_label_url="https://example.com/label.pdf",
            return_tracking_number="FOREIGN-TRACK",
        )

        response = self.client.get(self._url(foreign_return.id))
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ---------------------------------------------------------------------------
# Listing / detail / auth
# ---------------------------------------------------------------------------


class TestReturnRequestListAndDetail:
    """Cover the standard list/retrieve DRF paths for the current user only."""

    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_list_only_returns_current_users_requests(self):
        my_order = OrderFactory(user=self.user, paid_order=True, delivered=True)
        mine = ReturnRequestFactory(order=my_order, user=self.user)

        other_user = UserFactory()
        other_order = OrderFactory(user=other_user, paid_order=True, delivered=True)
        ReturnRequestFactory(order=other_order, user=other_user)

        response = self.client.get("/api/return-requests/")

        assert response.status_code == status.HTTP_200_OK
        # Response is paginated (OrderPagination) with a ``results`` key.
        results = response.data["results"]
        assert len(results) == 1
        assert results[0]["id"] == mine.id

    def test_retrieve_own_return_returns_detail(self):
        my_order = OrderFactory(user=self.user, paid_order=True, delivered=True)
        rr = ReturnRequestFactory(order=my_order, user=self.user, status="approved")

        response = self.client.get(f"/api/return-requests/{rr.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == rr.id
        assert response.data["status"] == "approved"

    def test_retrieve_other_users_return_is_404(self):
        other_user = UserFactory()
        other_order = OrderFactory(user=other_user, paid_order=True, delivered=True)
        foreign = ReturnRequestFactory(order=other_order, user=other_user)

        response = self.client.get(f"/api/return-requests/{foreign.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unauthenticated_list_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/return-requests/")
        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )


# ---------------------------------------------------------------------------
# Email notification helpers
# ---------------------------------------------------------------------------


class TestReturnEmailNotifications:
    """The six ``orders.emails`` helpers each dispatch to
    ``EmailSendingService.send_template_email`` -- verify the template_type
    and recipient rather than ``django.core.mail.outbox`` (the platform
    doesn't route through Django's default backend)."""

    def setup_method(self):
        self.user = UserFactory()
        self.order = OrderFactory(user=self.user, paid_order=True, delivered=True)

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_send_return_request_confirmation(self, mock_send):
        from orders.emails import send_return_request_confirmation

        rr = ReturnRequestFactory(order=self.order, user=self.user, status="pending")
        mock_send.reset_mock()  # ignore any calls fired by factory-driven signals

        result = send_return_request_confirmation(rr)

        assert result is True
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args.kwargs
        assert call_kwargs["template_type"] == "return_request_confirmation"
        assert call_kwargs["to_email"] == self.user.email
        assert call_kwargs["context"]["order_number"] == self.order.order_number

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_send_return_approved_notification(self, mock_send):
        from orders.emails import send_return_approved_notification

        rr = ReturnRequestFactory(
            order=self.order,
            user=self.user,
            status="approved",
            return_tracking_number="TRACK123",
        )
        mock_send.reset_mock()

        send_return_approved_notification(rr)

        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args.kwargs
        assert call_kwargs["template_type"] == "return_request_approved"
        assert call_kwargs["to_email"] == self.user.email
        assert call_kwargs["context"]["return_tracking_number"] == "TRACK123"

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_send_return_rejected_notification(self, mock_send):
        from orders.emails import send_return_rejected_notification

        rr = ReturnRequestFactory(
            order=self.order,
            user=self.user,
            status="rejected",
            rejection_reason="Outside return window",
        )
        mock_send.reset_mock()

        send_return_rejected_notification(rr)

        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args.kwargs
        assert call_kwargs["template_type"] == "return_request_rejected"
        assert call_kwargs["to_email"] == self.user.email
        assert call_kwargs["context"]["rejection_reason"] == "Outside return window"

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_send_return_received_notification(self, mock_send):
        from orders.emails import send_return_received_notification

        rr = ReturnRequestFactory(order=self.order, user=self.user, status="received")
        mock_send.reset_mock()

        send_return_received_notification(rr)

        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args.kwargs
        assert call_kwargs["template_type"] == "return_received"
        assert call_kwargs["to_email"] == self.user.email
        assert call_kwargs["context"]["order_number"] == self.order.order_number

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_send_inspection_reminder_to_staff(self, mock_send):
        """Staff reminder emails go to every active staff user."""
        from orders.emails import send_inspection_reminder_to_staff

        staff1 = UserFactory(staff=True, email="staff1@test.spwig.com")
        staff2 = UserFactory(staff=True, email="staff2@test.spwig.com")
        # inactive staff -- must NOT be notified
        UserFactory(staff=True, is_active=False, email="inactive@test.spwig.com")

        rr = ReturnRequestFactory(order=self.order, user=self.user, status="received")
        mock_send.reset_mock()

        send_inspection_reminder_to_staff(rr)

        called_recipients = {call.kwargs["to_email"] for call in mock_send.call_args_list}
        called_templates = {call.kwargs["template_type"] for call in mock_send.call_args_list}
        assert staff1.email in called_recipients
        assert staff2.email in called_recipients
        assert "inactive@test.spwig.com" not in called_recipients
        assert called_templates == {"admin_return_inspection_reminder"}

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_send_refund_processed_notification(self, mock_send):
        from orders.emails import send_refund_processed_notification

        rr = ReturnRequestFactory(order=self.order, user=self.user, status="completed")
        refund = RefundFactory(
            order=self.order,
            refund_type="full",
            reason="defective",
            status="approved",
            total_amount=Decimal("100.00"),
        )
        rr.refund = refund
        rr.save()
        mock_send.reset_mock()

        send_refund_processed_notification(rr)

        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args.kwargs
        assert call_kwargs["template_type"] == "return_refund_processed"
        assert call_kwargs["to_email"] == self.user.email
        assert call_kwargs["context"]["refund_amount"] == "100.00"

    @patch("email_system.services.email_sender.EmailSendingService.send_template_email")
    def test_refund_processed_short_circuits_when_no_refund_linked(self, mock_send):
        """If ``return_request.refund`` is ``None``, no email is sent."""
        from orders.emails import send_refund_processed_notification

        rr = ReturnRequestFactory(order=self.order, user=self.user, status="completed")
        assert rr.refund is None
        mock_send.reset_mock()

        send_refund_processed_notification(rr)

        mock_send.assert_not_called()


# ---------------------------------------------------------------------------
# Return-label PDF generation
# ---------------------------------------------------------------------------


class TestReturnLabelGeneration:
    """``DocumentService.generate_return_label`` renders a PDF data-URI."""

    def setup_method(self):
        self.user = UserFactory()
        self.order = OrderFactory(user=self.user, paid_order=True, delivered=True)

    def test_generates_pdf_data_uri(self):
        from shipping.services.document_service import DocumentService

        rr = ReturnRequestFactory(order=self.order, user=self.user, status="approved")

        data_uri = DocumentService.generate_return_label(rr)

        assert data_uri is not None
        assert data_uri.startswith("data:application/pdf;base64,")
        assert len(data_uri) > 200

    def test_generated_pdf_is_valid(self):
        """Decoded payload has the PDF magic-number header."""
        from shipping.services.document_service import DocumentService

        rr = ReturnRequestFactory(order=self.order, user=self.user, status="approved")

        data_uri = DocumentService.generate_return_label(rr)
        pdf_bytes = base64.b64decode(data_uri.split(",", 1)[1])

        assert pdf_bytes.startswith(b"%PDF")
