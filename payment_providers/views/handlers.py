"""
Payment Provider Webhook Handlers

Handles incoming webhooks from payment providers (Stripe, AirWallex, etc.)
Also includes admin API endpoints for provider management.
"""

import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from payment_providers.models import PaymentProviderAccount, PaymentWebhook
from payment_providers.providers.registry import ProviderRegistry
from payment_providers.services.webhook_service import WebhookService

logger = logging.getLogger(__name__)


# =============================================================================
# Admin Webhook Handler (Legacy - for admin URLs)
# =============================================================================


@csrf_exempt
@require_http_methods(["POST"])
def webhook_handler(request, provider_slug):
    """
    Handle webhook events from payment providers (legacy admin URL).
    This is the original webhook handler at /admin/payment-providers/webhook/<slug>/

    For new integrations, use the public webhook endpoint at /webhooks/payments/<slug>/
    """
    try:
        # Parse webhook payload
        payload = json.loads(request.body.decode("utf-8"))

        # Extract event information (varies by provider)
        event_id = payload.get("id") or payload.get("event_id") or payload.get("txn_id")
        event_type = payload.get("type") or payload.get("event_type") or payload.get("txn_type")

        # Get all HTTP headers for signature verification
        headers = {key: value for key, value in request.META.items() if key.startswith("HTTP_")}

        # Store webhook for processing (provider_account will be determined later)
        PaymentWebhook.objects.create(
            provider_slug=provider_slug,
            event_id=event_id or "unknown",
            event_type=event_type or "unknown",
            payload=payload,
            headers=headers,
        )

        logger.info(f"Received webhook from {provider_slug}: {event_type} (ID: {event_id})")

        return HttpResponse(status=200)

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in webhook from {provider_slug}")
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Error processing webhook from {provider_slug}: {str(e)}", exc_info=True)
        return HttpResponse(status=500)


# =============================================================================
# Admin API Endpoints
# =============================================================================


@staff_member_required
@require_http_methods(["POST"])
def test_provider_connection(request, account_id):
    """
    Test connection to a payment provider account (admin only)
    """
    try:
        account = get_object_or_404(PaymentProviderAccount, id=account_id)

        # Test the connection using the account's test_connection method
        result = account.test_connection()

        return JsonResponse(
            {
                "success": result.get("success", False),
                "message": result.get("message", ""),
                "details": result.get("details", {}),
            }
        )

    except Exception as e:
        logger.error(f"Error testing provider connection: {str(e)}", exc_info=True)
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def provider_info(request, provider_key):
    """
    Get information about a specific provider from the registry (admin only)
    """
    try:
        # Get provider info from registry
        info = ProviderRegistry.get_provider_info(provider_key)

        if not info:
            return JsonResponse({"error": _("Provider not found")}, status=404)

        return JsonResponse(info)

    except Exception as e:
        logger.error(f"Error getting provider info: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)


# =============================================================================
# Public Payment Webhook Handler (for orchestration API)
# =============================================================================


@csrf_exempt
@require_POST
def payment_webhook_handler(request, provider_slug: str) -> HttpResponse:
    """
    Handle incoming payment provider webhooks.

    This endpoint receives webhook notifications from payment providers
    like Stripe, AirWallex, PayPal, etc. It verifies the webhook signature,
    stores the event for audit purposes, and processes the event.

    URL: /webhooks/payments/<provider_slug>/
    Example: /webhooks/payments/airwallex/

    Args:
        request: Django HTTP request
        provider_slug: Provider identifier (e.g., 'airwallex', 'stripe')

    Returns:
        HTTP 200 on success (required by most providers)
        HTTP 400 on validation failure
        HTTP 500 on processing error
    """
    try:
        # Get raw payload for signature verification
        raw_payload = request.body

        # Parse JSON payload
        try:
            payload = json.loads(raw_payload.decode("utf-8"))
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in webhook payload: {e}")
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        # Extract headers for signature verification
        headers = dict(request.headers.items())

        # Get signature from headers (varies by provider)
        signature = _get_webhook_signature(headers, provider_slug)

        # Log webhook receipt
        event_type = payload.get("type", payload.get("name", payload.get("event_type", "unknown")))
        event_id = payload.get("id", payload.get("event_id", "unknown"))
        logger.info(f"Received webhook from {provider_slug}: type={event_type}, id={event_id}")

        # Process webhook through service
        success, message = WebhookService.process_webhook(
            provider_slug=provider_slug,
            payload=payload,
            headers=headers,
            raw_payload=raw_payload,
            signature=signature,
        )

        if success:
            # Return 200 immediately (most providers require quick response)
            return HttpResponse(status=200)
        else:
            logger.warning(f"Webhook processing returned failure: {message}")
            # Still return 200 to prevent provider from retrying
            # (webhook is stored and can be retried internally)
            return HttpResponse(status=200)

    except Exception as e:
        logger.error(f"Error handling webhook from {provider_slug}: {e}", exc_info=True)
        # Return 200 to prevent infinite retries from provider
        # The webhook is stored and can be retried internally
        return HttpResponse(status=200)


def _get_webhook_signature(headers: dict, provider_slug: str) -> str:
    """
    Extract webhook signature from headers based on provider.

    Different providers use different header names for signatures:
    - Stripe: 'Stripe-Signature'
    - AirWallex: 'x-signature' with 'x-timestamp'
    - PayPal: Various depending on version

    Args:
        headers: Request headers
        provider_slug: Provider identifier

    Returns:
        Signature string or empty string if not found
    """
    # Normalize headers to lowercase keys
    normalized = {k.lower(): v for k, v in headers.items()}

    # Provider-specific signature headers
    signature_headers = {
        "stripe": "stripe-signature",
        "airwallex": "x-signature",
        "paypal": "paypal-transmission-sig",
        "adyen": "hmac-signature",
        "square": "x-square-signature",
        "braintree": "bt-signature",
    }

    # Get provider-specific header or try common ones
    header_name = signature_headers.get(provider_slug.lower())
    if header_name and header_name in normalized:
        return normalized[header_name]

    # Try common signature header names
    common_headers = [
        "x-signature",
        "signature",
        "x-hub-signature-256",
        "x-webhook-signature",
    ]

    for header in common_headers:
        if header in normalized:
            return normalized[header]

    return ""
