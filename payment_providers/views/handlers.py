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


def _load_verified_webhook(request, provider_slug: str):
    """Parse, shape-validate, and signature-verify an incoming provider webhook.

    Both webhook endpoints are public and CSRF-exempt, so the provider signature
    is the only proof a request genuinely came from the provider. Verifying it
    (and rejecting malformed payloads) here — before any record is written or any
    payment state is touched — is what stops unauthenticated callers from
    spoofing events or mutating orders.

    Returns a ``(payload, raw_payload, headers, signature)`` tuple when the
    request is a well-formed JSON object carrying a valid provider signature, or
    an :class:`~django.http.HttpResponse` (HTTP 400) that the caller should
    return directly when the request is malformed or fails verification.
    """
    raw_payload = request.body

    try:
        payload = json.loads(raw_payload.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in webhook from {provider_slug}")
        return HttpResponse(status=400)

    if not isinstance(payload, dict):
        logger.error(f"Webhook payload from {provider_slug} is not a JSON object")
        return HttpResponse(status=400)

    # request.headers exposes canonical header names (e.g. 'X-Signature') that
    # _get_webhook_signature and the provider verifiers expect.
    headers = dict(request.headers.items())
    signature = _get_webhook_signature(headers, provider_slug)
    if not signature:
        logger.warning(f"Missing webhook signature from {provider_slug}")
        return HttpResponse(status=400)

    provider_accounts = PaymentProviderAccount.objects.filter(
        component__slug=provider_slug, is_active=True
    )
    if not provider_accounts.exists():
        logger.error(f"No active provider account for webhook: {provider_slug}")
        return HttpResponse(status=400)

    # A provider slug can have several active accounts (e.g. test + live keys,
    # or multiple merchant accounts), each with its own signing secret. The
    # request is authentic if it verifies against ANY of them — checking only
    # the first would reject webhooks legitimately signed by another account.
    signature_valid = any(
        WebhookService.verify_webhook_signature(
            provider_account=provider_account,
            payload=raw_payload,
            signature=signature,
            headers=headers,
        )
        for provider_account in provider_accounts
    )
    if not signature_valid:
        logger.warning(f"Webhook signature verification failed from {provider_slug}")
        return HttpResponse(status=400)

    return payload, raw_payload, headers, signature


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
    # Reject malformed or unsigned/spoofed requests before persisting anything.
    verified = _load_verified_webhook(request, provider_slug)
    if isinstance(verified, HttpResponse):
        return verified
    payload, _raw_payload, headers, _signature = verified

    try:
        # Extract event information (varies by provider)
        event_id = payload.get("id") or payload.get("event_id") or payload.get("txn_id")
        event_type = payload.get("type") or payload.get("event_type") or payload.get("txn_type")

        # Store webhook for processing (provider_account will be determined later)
        PaymentWebhook.objects.create(
            provider_slug=provider_slug,
            event_id=event_id or "unknown",
            event_type=event_type or "unknown",
            payload=payload,
            headers=headers,
            signature_verified=True,
        )

        logger.info(f"Received webhook from {provider_slug}: {event_type} (ID: {event_id})")

        return HttpResponse(status=200)

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
        HTTP 400 on validation failure (bad shape, missing/invalid signature)
        HTTP 500 on processing error (retryable by the provider)
    """
    # Parse, shape-validate, and verify the signature before any payment state is
    # mutated. A missing or invalid signature is rejected with 400 here so
    # WebhookService.process_webhook — which only logs verification failures — is
    # never reached with an unverified event.
    verified = _load_verified_webhook(request, provider_slug)
    if isinstance(verified, HttpResponse):
        return verified
    payload, raw_payload, headers, signature = verified

    try:
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
            # process_webhook persists the event record before processing, so it
            # can be retried internally — ack with 200 to avoid provider retries.
            return HttpResponse(status=200)

    except Exception as e:
        logger.error(f"Error handling webhook from {provider_slug}: {e}", exc_info=True)
        # Pre-persistence failure: nothing was stored for internal retry, so
        # return a retryable 5xx and let the provider redeliver the event.
        return HttpResponse(status=500)


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

    # 1. Pluggable path: the header the component DECLARES in its manifest
    #    (webhooks.signature_header, else webhooks.headers[0]). A new provider
    #    declares its header here and needs no core edit.
    declared = _manifest_signature_header(provider_slug)
    if declared and declared.lower() in normalized:
        return normalized[declared.lower()]

    # 2. Common signature header names (last-resort fallback). Providers declare
    #    their exact header in the manifest (step 1); this only catches a
    #    provider whose manifest omits it and uses a conventional name.
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


def _manifest_signature_header(provider_slug: str) -> str | None:
    """Return the signature header a component declares in its manifest, or None.

    Prefers ``webhooks.signature_header``; falls back to the first entry of
    ``webhooks.headers``. Any lookup failure returns None so the caller drops to
    its other resolution steps.
    """
    try:
        from component_updates.models import ComponentRegistry

        component = ComponentRegistry.objects.filter(slug=provider_slug).first()
        if not component:
            return None
        webhooks = (component.get_manifest() or {}).get("webhooks") or {}
        header = webhooks.get("signature_header")
        if not header:
            hdrs = webhooks.get("headers") or []
            header = hdrs[0] if hdrs else None
        return header
    except Exception:
        return None
