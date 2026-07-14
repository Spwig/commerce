"""
Payout Provider Webhook Views

Endpoints for receiving webhook notifications from payout providers
(PayPal Payouts, Airwallex Transfers, etc.)
"""

import json
import logging

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ..loader import get_provider_class
from ..models import PayoutProviderAccount, PayoutWebhookLog

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def paypal_webhook(request):
    """
    Handle PayPal payout webhooks.

    PayPal sends webhooks for:
    - PAYMENT.PAYOUTSBATCH.SUCCESS
    - PAYMENT.PAYOUTSBATCH.DENIED
    - PAYMENT.PAYOUTS-ITEM.SUCCEEDED
    - PAYMENT.PAYOUTS-ITEM.FAILED
    - PAYMENT.PAYOUTS-ITEM.UNCLAIMED
    """
    return _handle_webhook(request, "paypal")


@csrf_exempt
@require_POST
def airwallex_webhook(request):
    """
    Handle Airwallex transfer webhooks.

    Airwallex sends webhooks for:
    - transfer.confirmed
    - transfer.completed
    - transfer.failed
    - transfer.returned
    """
    return _handle_webhook(request, "airwallex")


def _handle_webhook(request, provider_type: str) -> HttpResponse:
    """
    Generic webhook handler for all payout providers.

    1. Logs the webhook
    2. Verifies signature (if provider account found)
    3. Queues for async processing

    Args:
        request: Django HTTP request
        provider_type: Type of provider ('paypal', 'airwallex')

    Returns:
        HttpResponse with appropriate status code
    """
    # Get raw payload
    try:
        payload = request.body
        payload_str = payload.decode("utf-8")
        payload_data = json.loads(payload_str)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"Invalid {provider_type} webhook payload: {e}")
        return HttpResponse("Invalid payload", status=400)

    # Extract headers
    headers = dict(request.headers.items())

    # Try to determine provider account and event info
    event_type = _extract_event_type(payload_data, provider_type)
    event_id = _extract_event_id(payload_data, provider_type)

    # Find matching provider account
    provider_account = PayoutProviderAccount.objects.filter(
        provider_type=provider_type, is_active=True
    ).first()

    # Create webhook log
    webhook_log = PayoutWebhookLog.objects.create(
        provider_account=provider_account,
        provider_type=provider_type,
        event_type=event_type,
        event_id=event_id,
        payload=payload_data,
        headers=headers,
        received_at=timezone.now(),
    )

    logger.info(f"Received {provider_type} webhook: {event_type} (ID: {event_id})")

    # Verify signature if we have a provider account
    signature_valid = None
    if provider_account:
        provider_class = get_provider_class(provider_type, provider_account.component)

        if provider_class:
            config = provider_account.credentials
            config.update(provider_account.settings)
            provider = provider_class(config)

            try:
                signature_valid = provider.verify_webhook_signature(payload, headers)
            except Exception as e:
                logger.error(f"Webhook signature verification failed: {e}")
                signature_valid = False

            webhook_log.signature_valid = signature_valid
            webhook_log.save()

            if signature_valid is False:
                logger.warning(f"Invalid signature for {provider_type} webhook {event_id}")
                # Still return 200 to prevent retries, but don't process
                return HttpResponse("Invalid signature", status=200)

    # Queue for async processing
    try:
        from ..tasks import handle_webhook_event

        handle_webhook_event.delay(webhook_log.id)
    except Exception as e:
        logger.error(f"Failed to queue webhook for processing: {e}")
        # Still return success - webhook is logged

    return HttpResponse("OK", status=200)


def _extract_event_type(payload: dict, provider_type: str) -> str:
    """Extract event type from webhook payload."""
    if provider_type == "paypal":
        return payload.get("event_type", "")
    elif provider_type == "airwallex":
        return payload.get("name", "")
    return ""


def _extract_event_id(payload: dict, provider_type: str) -> str:
    """Extract event ID from webhook payload."""
    if provider_type == "paypal" or provider_type == "airwallex":
        return payload.get("id", "")
    return ""
