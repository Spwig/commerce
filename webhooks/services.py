"""
Webhook service functions.

This module provides the main interface for triggering webhooks
from anywhere in the application.
"""
import logging
from typing import Any, Optional
from urllib.parse import urlparse

from django.db.models import Model
from django.utils import timezone

from .events import is_valid_event, WEBHOOK_EVENTS

logger = logging.getLogger(__name__)

# Hostnames considered localhost (safe for sandbox delivery)
_LOCALHOST_HOSTS = frozenset({
    'localhost', '127.0.0.1', '::1', '[::1]',
})


def _is_localhost_url(url: str) -> bool:
    """Check if a URL points to localhost."""
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ''
        return hostname in _LOCALHOST_HOSTS
    except Exception:
        return False


def trigger_webhook(
    event_type: str,
    instance: Optional[Model] = None,
    data: Optional[dict] = None,
    **extra_data
) -> int:
    """
    Trigger webhooks for an event type.

    This function finds all active webhook endpoints subscribed to the
    given event type and queues webhook deliveries for each.

    Args:
        event_type: The webhook event type (e.g., 'order.created')
        instance: Optional model instance to serialize (if data not provided)
        data: Optional pre-serialized data payload
        **extra_data: Additional data to include in the payload

    Returns:
        Number of webhook deliveries queued

    Example:
        # Trigger with a model instance (auto-serialized)
        trigger_webhook('order.created', instance=order)

        # Trigger with pre-built data
        trigger_webhook('inventory.low_stock', data={
            'product_id': 123,
            'product_name': 'Widget',
            'current_stock': 5,
            'threshold': 10,
        })
    """
    from .models import WebhookEndpoint, WebhookDelivery
    from .tasks import deliver_webhook
    from .serializers import get_payload_for_event

    # Validate event type
    if not is_valid_event(event_type):
        logger.warning(f"Unknown webhook event type: {event_type}")
        # Still allow it - custom events may be useful

    # Find all active endpoints subscribed to this event
    endpoints = WebhookEndpoint.objects.filter(
        is_active=True,
        is_disabled_by_failures=False,
    )

    # Filter by subscribed events
    # JSONField contains check for the event in the list
    subscribed_endpoints = [
        ep for ep in endpoints
        if event_type in ep.events or '*' in ep.events
    ]

    if not subscribed_endpoints:
        logger.debug(f"No endpoints subscribed to event {event_type}")
        return 0

    # Build payload
    if data is not None:
        payload_data = data
    elif instance is not None:
        payload_data = get_payload_for_event(event_type, instance)
    else:
        payload_data = {}

    # Add extra data
    payload_data.update(extra_data)

    # Create full payload
    payload = {
        'event': event_type,
        'created_at': timezone.now().isoformat(),
        'data': payload_data,
    }

    # Add sandbox flag when in sandbox mode
    from core.license import is_sandbox_mode
    if is_sandbox_mode():
        payload['sandbox'] = True

    # Queue deliveries
    count = 0
    sandbox = is_sandbox_mode()
    for endpoint in subscribed_endpoints:
        # In sandbox mode, only deliver to localhost URLs
        if sandbox and not _is_localhost_url(endpoint.url):
            delivery = WebhookDelivery.objects.create(
                endpoint=endpoint,
                event_type=event_type,
                payload=payload,
                status='sandbox_blocked',
            )
            logger.info(
                f"[SANDBOX] Webhook to {endpoint.url} blocked "
                f"(external URL in sandbox mode), delivery_id={delivery.id}"
            )
            count += 1
            continue

        delivery = WebhookDelivery.objects.create(
            endpoint=endpoint,
            event_type=event_type,
            payload=payload,
        )
        deliver_webhook.delay(str(delivery.id))
        count += 1
        logger.debug(f"Queued webhook delivery {delivery.id} for {event_type} to {endpoint.name}")

    if count > 0:
        logger.info(f"Triggered {count} webhook(s) for event {event_type}")

    return count


def trigger_webhook_sync(
    event_type: str,
    instance: Optional[Model] = None,
    data: Optional[dict] = None,
    **extra_data
) -> list:
    """
    Trigger webhooks synchronously (for testing/debugging).

    This is NOT recommended for production use as it blocks
    the current thread until all webhooks are delivered.

    Args:
        event_type: The webhook event type
        instance: Optional model instance to serialize
        data: Optional pre-serialized data payload
        **extra_data: Additional data to include in the payload

    Returns:
        List of delivery results
    """
    from .models import WebhookEndpoint, WebhookDelivery
    from .tasks import deliver_webhook
    from .serializers import get_payload_for_event

    endpoints = WebhookEndpoint.objects.filter(
        is_active=True,
        is_disabled_by_failures=False,
    )

    subscribed_endpoints = [
        ep for ep in endpoints
        if event_type in ep.events or '*' in ep.events
    ]

    if not subscribed_endpoints:
        return []

    if data is not None:
        payload_data = data
    elif instance is not None:
        payload_data = get_payload_for_event(event_type, instance)
    else:
        payload_data = {}

    payload_data.update(extra_data)

    payload = {
        'event': event_type,
        'created_at': timezone.now().isoformat(),
        'data': payload_data,
    }

    # Add sandbox flag when in sandbox mode
    from core.license import is_sandbox_mode
    if is_sandbox_mode():
        payload['sandbox'] = True

    sandbox = is_sandbox_mode()
    results = []
    for endpoint in subscribed_endpoints:
        # In sandbox mode, only deliver to localhost URLs
        if sandbox and not _is_localhost_url(endpoint.url):
            delivery = WebhookDelivery.objects.create(
                endpoint=endpoint,
                event_type=event_type,
                payload=payload,
                status='sandbox_blocked',
            )
            results.append({
                'delivery_id': str(delivery.id),
                'endpoint': endpoint.name,
                'status': 'sandbox_blocked',
                'response_code': None,
            })
            logger.info(
                f"[SANDBOX] Webhook to {endpoint.url} blocked "
                f"(external URL in sandbox mode), delivery_id={delivery.id}"
            )
            continue

        delivery = WebhookDelivery.objects.create(
            endpoint=endpoint,
            event_type=event_type,
            payload=payload,
        )
        # Run synchronously
        deliver_webhook(str(delivery.id))
        delivery.refresh_from_db()
        results.append({
            'delivery_id': str(delivery.id),
            'endpoint': endpoint.name,
            'status': delivery.status,
            'response_code': delivery.response_status_code,
        })

    return results


def get_endpoint_stats(endpoint_id: str) -> dict:
    """
    Get delivery statistics for a webhook endpoint.

    Args:
        endpoint_id: UUID of the WebhookEndpoint

    Returns:
        Dictionary with delivery statistics
    """
    from .models import WebhookEndpoint, WebhookDelivery
    from django.db.models import Count, Avg, Q
    from datetime import timedelta

    try:
        endpoint = WebhookEndpoint.objects.get(id=endpoint_id)
    except WebhookEndpoint.DoesNotExist:
        return {}

    # Get stats for last 24 hours
    since = timezone.now() - timedelta(hours=24)

    stats = WebhookDelivery.objects.filter(
        endpoint=endpoint,
        created_at__gte=since,
    ).aggregate(
        total=Count('id'),
        success=Count('id', filter=Q(status=WebhookDelivery.Status.SUCCESS)),
        failed=Count('id', filter=Q(status=WebhookDelivery.Status.FAILED)),
        retrying=Count('id', filter=Q(status=WebhookDelivery.Status.RETRYING)),
        pending=Count('id', filter=Q(status=WebhookDelivery.Status.PENDING)),
        avg_response_time=Avg('response_time_ms', filter=Q(response_time_ms__isnull=False)),
    )

    # Calculate success rate
    total = stats['total'] or 0
    success = stats['success'] or 0
    success_rate = (success / total * 100) if total > 0 else 0

    return {
        'endpoint_id': str(endpoint_id),
        'endpoint_name': endpoint.name,
        'period': '24h',
        'total_deliveries': total,
        'successful': success,
        'failed': stats['failed'] or 0,
        'retrying': stats['retrying'] or 0,
        'pending': stats['pending'] or 0,
        'success_rate': round(success_rate, 1),
        'avg_response_time_ms': round(stats['avg_response_time'] or 0, 0),
        'is_healthy': endpoint.consecutive_failures < 5 and not endpoint.is_disabled_by_failures,
        'consecutive_failures': endpoint.consecutive_failures,
        'is_disabled': endpoint.is_disabled_by_failures,
    }


def list_available_events() -> list:
    """
    Get a list of all available webhook event types.

    Returns:
        List of event dictionaries with type and description
    """
    from .events import get_events_by_category

    events = []
    for category, category_events in get_events_by_category().items():
        for event_info in category_events:
            events.append({
                'event': event_info['event'],
                'description': event_info['description'],
                'category': category,
            })

    return sorted(events, key=lambda x: x['event'])


def verify_webhook_signature(
    payload: str,
    signature_header: str,
    secret: str,
    tolerance_seconds: int = 300
) -> tuple[bool, str]:
    """
    Verify a webhook signature.

    This is a utility function that can be used by webhook receivers
    to verify incoming webhooks.

    Args:
        payload: The raw request body as a string
        signature_header: The X-Spwig-Signature header value
        secret: The webhook endpoint's secret
        tolerance_seconds: Maximum age of signature in seconds (default 5 min)

    Returns:
        Tuple of (is_valid, error_message)
    """
    import hmac
    import hashlib
    import time

    try:
        # Parse signature header: "t=1234567890,v1=abc123..."
        parts = {}
        for part in signature_header.split(','):
            key, value = part.split('=', 1)
            parts[key] = value

        timestamp_str = parts.get('t')
        signature = parts.get('v1')

        if not timestamp_str or not signature:
            return False, "Missing timestamp or signature in header"

        timestamp = int(timestamp_str)

        # Check timestamp age
        current_time = int(time.time())
        if abs(current_time - timestamp) > tolerance_seconds:
            return False, f"Signature timestamp too old (>{tolerance_seconds}s)"

        # Compute expected signature
        signature_payload = f"{timestamp}.{payload}"
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            signature_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Compare signatures using constant-time comparison
        if hmac.compare_digest(signature, expected_signature):
            return True, ""
        else:
            return False, "Signature mismatch"

    except (ValueError, KeyError) as e:
        return False, f"Invalid signature format: {e}"
