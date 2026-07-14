"""
PayPal Payouts Provider

Implements the PayPal Payouts API for sending payments to affiliates.
https://developer.paypal.com/docs/api/payments.payouts-batch/v1/
"""

import logging
import uuid
from decimal import Decimal
from typing import Any

import requests

from .base import (
    BasePayoutProvider,
    BatchPayoutResult,
    PayoutMethod,
    PayoutRequest,
    PayoutResult,
    PayoutStatus,
)

logger = logging.getLogger(__name__)


class PayPalPayoutProvider(BasePayoutProvider):
    """
    PayPal Payouts API Provider

    Supports batch payouts to PayPal accounts using the recipient's email address.
    Up to 15,000 payments can be sent in a single batch.
    """

    SANDBOX_API_BASE = "https://api-m.sandbox.paypal.com"
    PRODUCTION_API_BASE = "https://api-m.paypal.com"

    # PayPal payout status mapping
    STATUS_MAP = {
        "SUCCESS": PayoutStatus.COMPLETED,
        "PENDING": PayoutStatus.PENDING,
        "PROCESSING": PayoutStatus.PROCESSING,
        "UNCLAIMED": PayoutStatus.PENDING,
        "RETURNED": PayoutStatus.RETURNED,
        "ONHOLD": PayoutStatus.PENDING,
        "BLOCKED": PayoutStatus.FAILED,
        "REFUNDED": PayoutStatus.RETURNED,
        "REVERSED": PayoutStatus.RETURNED,
        "FAILED": PayoutStatus.FAILED,
        "DENIED": PayoutStatus.FAILED,
    }

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self._access_token = None
        self._token_expires_at = None

    @property
    def provider_name(self) -> str:
        return "paypal"

    @property
    def display_name(self) -> str:
        return "PayPal Payouts"

    @property
    def supported_methods(self) -> list[PayoutMethod]:
        return [PayoutMethod.PAYPAL]

    @property
    def supported_currencies(self) -> list[str]:
        return [
            "USD",
            "EUR",
            "GBP",
            "CAD",
            "AUD",
            "JPY",
            "CNY",
            "HKD",
            "NZD",
            "SGD",
            "CHF",
            "SEK",
            "NOK",
            "DKK",
            "PLN",
            "HUF",
            "CZK",
            "ILS",
            "MXN",
            "BRL",
            "MYR",
            "PHP",
            "THB",
            "TWD",
            "RUB",
        ]

    @property
    def credential_schema(self) -> dict[str, Any]:
        return {
            "client_id": {
                "type": "string",
                "required": True,
                "label": "Client ID",
                "help_text": "PayPal REST API Client ID",
            },
            "client_secret": {
                "type": "string",
                "required": True,
                "label": "Client Secret",
                "sensitive": True,
                "help_text": "PayPal REST API Client Secret",
            },
            "environment": {
                "type": "select",
                "required": True,
                "label": "Environment",
                "options": [
                    {"value": "sandbox", "label": "Sandbox (Testing)"},
                    {"value": "production", "label": "Production (Live)"},
                ],
                "default": "sandbox",
            },
            "webhook_id": {
                "type": "string",
                "required": False,
                "label": "Webhook ID",
                "help_text": "PayPal Webhook ID for signature verification",
            },
        }

    @property
    def _api_base(self) -> str:
        """Get API base URL based on environment"""
        env = self.config.get("environment", "sandbox")
        return self.PRODUCTION_API_BASE if env == "production" else self.SANDBOX_API_BASE

    def _get_access_token(self) -> str:
        """
        Get OAuth 2.0 access token from PayPal.

        Returns:
            Access token string
        """
        import time

        # Return cached token if still valid
        if self._access_token and self._token_expires_at:
            if time.time() < self._token_expires_at - 60:  # 60 second buffer
                return self._access_token

        client_id = self.config.get("client_id")
        client_secret = self.config.get("client_secret")

        if not client_id or not client_secret:
            raise ValueError("PayPal client_id and client_secret are required")

        response = requests.post(
            f"{self._api_base}/v1/oauth2/token",
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials"},
            headers={"Accept": "application/json"},
            timeout=30,
        )

        if response.status_code != 200:
            logger.error(f"PayPal auth failed: {response.text}")
            raise ValueError(f"PayPal authentication failed: {response.status_code}")

        data = response.json()
        self._access_token = data["access_token"]
        self._token_expires_at = time.time() + data.get("expires_in", 3600)

        return self._access_token

    def _make_request(
        self, method: str, endpoint: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """
        Make authenticated request to PayPal API.

        Args:
            method: HTTP method
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON data
        """
        token = self._get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        url = f"{self._api_base}{endpoint}"

        response = requests.request(
            method=method, url=url, json=data, params=params, headers=headers, timeout=60
        )

        # Log for debugging
        logger.debug(f"PayPal API {method} {endpoint}: {response.status_code}")

        return {
            "status_code": response.status_code,
            "data": response.json() if response.text else {},
            "headers": dict(response.headers),
        }

    def validate_credentials(self) -> dict[str, Any]:
        """Validate PayPal credentials"""
        try:
            self._get_access_token()
            return {"valid": True}
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def test_connection(self) -> dict[str, Any]:
        """Test connection to PayPal API"""
        try:
            # Get access token to verify credentials
            self._get_access_token()

            # Make a simple API call to verify access
            result = self._make_request("GET", "/v1/identity/openid-connect/userinfo?schema=openid")

            if result["status_code"] in (200, 401):  # 401 is expected for this endpoint
                return {
                    "success": True,
                    "message": "Successfully connected to PayPal API",
                    "environment": self.config.get("environment", "sandbox"),
                }

            return {"success": False, "message": f"Unexpected response: {result['status_code']}"}

        except Exception as e:
            logger.error(f"PayPal connection test failed: {e}")
            return {"success": False, "message": str(e)}

    def create_payout(self, request: PayoutRequest) -> PayoutResult:
        """
        Create a single payout to a PayPal account.

        For single payouts, we still use the batch API with one item.
        """
        batch_result = self.create_batch_payout([request])

        if batch_result.results:
            return batch_result.results[0]

        return PayoutResult(
            success=False,
            status=PayoutStatus.FAILED,
            message=batch_result.message or "Failed to create payout",
        )

    def create_batch_payout(self, requests: list[PayoutRequest]) -> BatchPayoutResult:
        """
        Create batch payout to multiple PayPal accounts.

        Args:
            requests: List of PayoutRequest objects

        Returns:
            BatchPayoutResult with batch reference and individual item statuses
        """
        if not requests:
            return BatchPayoutResult(success=False, message="No payout requests provided")

        # Generate unique batch ID
        batch_id = f"spwig_payout_{uuid.uuid4().hex[:16]}"

        # Build payout items
        items = []
        for req in requests:
            if not req.recipient.email:
                logger.warning(f"Payout {req.payout_id} has no email, skipping")
                continue

            item = {
                "recipient_type": "EMAIL",
                "amount": {"value": str(req.amount), "currency": req.currency},
                "receiver": req.recipient.email,
                "sender_item_id": req.reference,  # Our internal reference
            }

            if req.note:
                item["note"] = req.note[:4000]  # PayPal limit

            items.append(item)

        if not items:
            return BatchPayoutResult(success=False, message="No valid payout items after filtering")

        # Build batch request
        payload = {
            "sender_batch_header": {
                "sender_batch_id": batch_id,
                "email_subject": "You have received a payment",
                "email_message": "Thank you for your partnership. You have received a commission payout.",
            },
            "items": items,
        }

        try:
            result = self._make_request("POST", "/v1/payments/payouts", data=payload)

            if result["status_code"] == 201:
                data = result["data"]
                batch_header = data.get("batch_header", {})

                return BatchPayoutResult(
                    success=True,
                    batch_reference=batch_header.get("payout_batch_id"),
                    message=f"Batch created with status: {batch_header.get('batch_status')}",
                    raw_response=data,
                    results=[
                        PayoutResult(
                            success=True,
                            provider_reference=batch_header.get("payout_batch_id"),
                            status=PayoutStatus.PENDING,
                            raw_response=data,
                        )
                        for _ in requests
                    ],
                )
            else:
                error_data = result["data"]
                error_msg = error_data.get("message", f"HTTP {result['status_code']}")

                # Check for duplicate batch ID
                if error_data.get("name") == "BATCH_NOT_UNIQUE":
                    error_msg = (
                        "Duplicate batch ID detected. Payout may have already been processed."
                    )

                return BatchPayoutResult(success=False, message=error_msg, raw_response=error_data)

        except Exception as e:
            logger.error(f"PayPal batch payout failed: {e}")
            return BatchPayoutResult(success=False, message=str(e))

    def get_payout_status(self, provider_reference: str) -> PayoutResult:
        """
        Get status of a payout batch.

        Args:
            provider_reference: PayPal payout_batch_id

        Returns:
            PayoutResult with current status
        """
        try:
            result = self._make_request("GET", f"/v1/payments/payouts/{provider_reference}")

            if result["status_code"] == 200:
                data = result["data"]
                batch_header = data.get("batch_header", {})
                batch_status = batch_header.get("batch_status", "PENDING")

                return PayoutResult(
                    success=True,
                    provider_reference=provider_reference,
                    status=self.STATUS_MAP.get(batch_status, PayoutStatus.PENDING),
                    message=batch_status,
                    raw_response=data,
                )
            else:
                return PayoutResult(
                    success=False,
                    status=PayoutStatus.FAILED,
                    message=result["data"].get("message", f"HTTP {result['status_code']}"),
                    raw_response=result["data"],
                )

        except Exception as e:
            logger.error(f"Failed to get PayPal payout status: {e}")
            return PayoutResult(success=False, status=PayoutStatus.FAILED, message=str(e))

    def cancel_payout(self, provider_reference: str) -> PayoutResult:
        """
        Cancel a payout item (if possible).

        Note: PayPal only allows canceling UNCLAIMED items.
        """
        # First get the batch to find item IDs
        status_result = self.get_payout_status(provider_reference)

        if not status_result.success:
            return status_result

        # Check if any items are UNCLAIMED
        items = status_result.raw_response.get("items", [])
        unclaimed_items = [item for item in items if item.get("transaction_status") == "UNCLAIMED"]

        if not unclaimed_items:
            return PayoutResult(
                success=False, status=PayoutStatus.FAILED, message="No unclaimed items to cancel"
            )

        # Cancel each unclaimed item
        cancelled = 0
        for item in unclaimed_items:
            item_id = item.get("payout_item_id")
            try:
                result = self._make_request("POST", f"/v1/payments/payouts-item/{item_id}/cancel")
                if result["status_code"] == 200:
                    cancelled += 1
            except Exception as e:
                logger.error(f"Failed to cancel item {item_id}: {e}")

        return PayoutResult(
            success=cancelled > 0,
            provider_reference=provider_reference,
            status=PayoutStatus.CANCELLED if cancelled > 0 else PayoutStatus.FAILED,
            message=f"Cancelled {cancelled} of {len(unclaimed_items)} items",
        )

    def verify_webhook_signature(self, payload: bytes, headers: dict[str, str]) -> bool:
        """
        Verify PayPal webhook signature.

        PayPal uses a combination of headers and webhook ID for verification.
        """
        webhook_id = self.config.get("webhook_id")
        if not webhook_id:
            logger.warning("No webhook_id configured, skipping signature verification")
            return True  # Allow webhooks if not configured

        # Get required headers
        transmission_id = headers.get("paypal-transmission-id", "")
        timestamp = headers.get("paypal-transmission-time", "")
        cert_url = headers.get("paypal-cert-url", "")
        auth_algo = headers.get("paypal-auth-algo", "")
        transmission_sig = headers.get("paypal-transmission-sig", "")

        if not all([transmission_id, timestamp, transmission_sig]):
            logger.warning("Missing required webhook headers")
            return False

        # PayPal webhook verification would typically use their verification endpoint
        # For now, we'll use a simplified approach
        try:
            result = self._make_request(
                "POST",
                "/v1/notifications/verify-webhook-signature",
                data={
                    "auth_algo": auth_algo,
                    "cert_url": cert_url,
                    "transmission_id": transmission_id,
                    "transmission_sig": transmission_sig,
                    "transmission_time": timestamp,
                    "webhook_id": webhook_id,
                    "webhook_event": payload.decode("utf-8")
                    if isinstance(payload, bytes)
                    else payload,
                },
            )

            if result["status_code"] == 200:
                verification_status = result["data"].get("verification_status")
                return verification_status == "SUCCESS"

            return False

        except Exception as e:
            logger.error(f"Webhook verification failed: {e}")
            return False

    def handle_webhook(self, event_data: dict[str, Any]) -> dict[str, Any]:
        """
        Process PayPal webhook event.

        Relevant event types:
        - PAYMENT.PAYOUTSBATCH.SUCCESS
        - PAYMENT.PAYOUTSBATCH.DENIED
        - PAYMENT.PAYOUTS-ITEM.SUCCEEDED
        - PAYMENT.PAYOUTS-ITEM.FAILED
        - PAYMENT.PAYOUTS-ITEM.UNCLAIMED
        """
        event_type = event_data.get("event_type", "")
        resource = event_data.get("resource", {})

        # Extract reference based on event type
        if "BATCH" in event_type:
            payout_ref = resource.get("batch_header", {}).get("payout_batch_id")
            status_str = resource.get("batch_header", {}).get("batch_status", "PENDING")
        else:
            payout_ref = resource.get("payout_batch_id")
            status_str = resource.get("transaction_status", "PENDING")

        status = self.STATUS_MAP.get(status_str, PayoutStatus.PENDING)

        return {
            "event_type": event_type,
            "payout_reference": payout_ref,
            "status": status,
            "message": status_str,
            "raw_data": event_data,
        }

    def estimate_fees(self, amount: Decimal, currency: str, method: PayoutMethod) -> Decimal | None:
        """
        Estimate PayPal payout fees.

        PayPal typically charges 2% capped at certain amounts per currency.
        """
        # PayPal Payouts fee structure (approximate)
        fee_rate = Decimal("0.02")  # 2%
        max_fees = {
            "USD": Decimal("20.00"),
            "EUR": Decimal("18.00"),
            "GBP": Decimal("15.00"),
            "CAD": Decimal("25.00"),
            "AUD": Decimal("25.00"),
        }

        fee = amount * fee_rate
        max_fee = max_fees.get(currency, Decimal("20.00"))

        return min(fee, max_fee)

    def get_estimated_arrival(self, method: PayoutMethod, country: str) -> str | None:
        """Get estimated arrival time for PayPal payouts"""
        return "Typically within minutes to 1 business day"
