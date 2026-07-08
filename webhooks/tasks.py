"""
Celery tasks for webhook delivery.

This module provides async tasks for delivering webhooks with
retry logic and exponential backoff.
"""
import hmac
import hashlib
import json
import time
import logging
import requests
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


def generate_signature(secret: str, timestamp: int, payload: str) -> str:
    """
    Generate HMAC-SHA256 signature for webhook payload.

    The signature is computed as:
        HMAC-SHA256(secret, timestamp + '.' + payload)

    Args:
        secret: The webhook endpoint's secret key
        timestamp: Unix timestamp when the webhook is sent
        payload: The JSON payload string

    Returns:
        The hex-encoded signature
    """
    signature_payload = f"{timestamp}.{payload}"
    return hmac.new(
        secret.encode('utf-8'),
        signature_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def calculate_retry_delay(attempt: int, base_delay: int = 60, max_delay: int = 3600) -> int:
    """
    Calculate exponential backoff delay for retries.

    Delays: 1m, 2m, 4m, 8m, 16m, 32m, 60m (capped at max_delay)

    Args:
        attempt: Current attempt number (1-indexed)
        base_delay: Base delay in seconds (default 60)
        max_delay: Maximum delay in seconds (default 3600 = 1 hour)

    Returns:
        Delay in seconds
    """
    delay = base_delay * (2 ** (attempt - 1))
    return min(delay, max_delay)


@shared_task(
    bind=True,
    name='webhooks.deliver_webhook',
    max_retries=5,
    default_retry_delay=60,
    acks_late=True,
    reject_on_worker_lost=True,
    autoretry_for=(requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    retry_backoff=True,
    retry_backoff_max=3600,
    retry_jitter=True,
)
def deliver_webhook(self, delivery_id: str):
    """
    Deliver a webhook to the configured endpoint.

    This task handles:
    - HMAC signature generation
    - HTTP POST with timeout
    - Response logging
    - Retry with exponential backoff
    - Endpoint health tracking

    Args:
        delivery_id: UUID of the WebhookDelivery record
    """
    from .models import WebhookDelivery

    try:
        delivery = WebhookDelivery.objects.select_related('endpoint').get(id=delivery_id)
    except WebhookDelivery.DoesNotExist:
        logger.error(f"WebhookDelivery {delivery_id} not found")
        return

    endpoint = delivery.endpoint

    # Check if endpoint is active
    if not endpoint.is_active:
        logger.info(f"Webhook endpoint {endpoint.id} is inactive, skipping delivery {delivery_id}")
        delivery.status = WebhookDelivery.Status.FAILED
        delivery.error_message = "Endpoint is inactive"
        delivery.save(update_fields=['status', 'error_message'])
        return

    if endpoint.is_disabled_by_failures:
        logger.info(f"Webhook endpoint {endpoint.id} is disabled due to failures, skipping delivery {delivery_id}")
        delivery.status = WebhookDelivery.Status.FAILED
        delivery.error_message = "Endpoint is disabled due to consecutive failures"
        delivery.save(update_fields=['status', 'error_message'])
        return

    # Prepare payload
    try:
        payload_json = json.dumps(delivery.payload, default=str, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        logger.error(f"Failed to serialize payload for delivery {delivery_id}: {e}")
        delivery.status = WebhookDelivery.Status.FAILED
        delivery.error_message = f"Failed to serialize payload: {e}"
        delivery.save(update_fields=['status', 'error_message'])
        return

    # Generate signature
    timestamp = int(time.time())
    signature = generate_signature(endpoint.secret, timestamp, payload_json)

    # Prepare headers
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'X-Spwig-Signature': f"t={timestamp},v1={signature}",
        'X-Spwig-Event': delivery.event_type,
        'X-Spwig-Delivery-Id': str(delivery.id),
        'X-Spwig-Timestamp': str(timestamp),
        'User-Agent': 'Spwig-Webhooks/1.0',
    }

    # Increment attempt count
    delivery.attempt_count += 1
    delivery.status = WebhookDelivery.Status.RETRYING
    delivery.save(update_fields=['attempt_count', 'status'])

    # Send request
    start_time = time.time()
    response_time_ms = None
    response_code = None
    response_body = None
    response_headers = {}

    try:
        logger.info(f"Delivering webhook {delivery_id} to {endpoint.url} (attempt {delivery.attempt_count})")

        response = requests.post(
            endpoint.url,
            data=payload_json.encode('utf-8'),
            headers=headers,
            timeout=endpoint.timeout_seconds,
            allow_redirects=False,  # Don't follow redirects for security
        )

        response_time_ms = int((time.time() - start_time) * 1000)
        response_code = response.status_code
        response_body = response.text[:10000] if response.text else ''  # Truncate large responses
        response_headers = dict(response.headers)

        # Check for success (2xx status codes)
        if 200 <= response.status_code < 300:
            logger.info(
                f"Webhook {delivery_id} delivered successfully "
                f"(status={response_code}, time={response_time_ms}ms)"
            )
            delivery.mark_success(
                response_code=response_code,
                response_body=response_body,
                response_time_ms=response_time_ms,
                response_headers=response_headers,
            )
            return

        # Non-2xx response - this is a delivery failure
        error_msg = f"Received non-2xx response: {response.status_code}"
        logger.warning(f"Webhook {delivery_id} failed: {error_msg}")
        raise requests.exceptions.HTTPError(error_msg, response=response)

    except requests.exceptions.Timeout as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_msg = f"Request timed out after {endpoint.timeout_seconds}s"
        logger.warning(f"Webhook {delivery_id} timed out: {error_msg}")
        _handle_delivery_failure(
            self, delivery, error_msg, response_code, response_body,
            response_time_ms, response_headers
        )
        raise  # Let Celery handle retry

    except requests.exceptions.ConnectionError as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_msg = f"Connection error: {str(e)}"
        logger.warning(f"Webhook {delivery_id} connection error: {error_msg}")
        _handle_delivery_failure(
            self, delivery, error_msg, response_code, response_body,
            response_time_ms, response_headers
        )
        raise  # Let Celery handle retry

    except requests.exceptions.HTTPError as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_msg = str(e)
        _handle_delivery_failure(
            self, delivery, error_msg, response_code, response_body,
            response_time_ms, response_headers
        )

        # Only retry for certain status codes (server errors, rate limits)
        if response_code and response_code in (429, 500, 502, 503, 504):
            raise requests.exceptions.ConnectionError(error_msg)  # Trigger retry
        else:
            # Client errors (4xx except 429) - don't retry
            delivery.status = WebhookDelivery.Status.FAILED
            delivery.save(update_fields=['status'])
            return

    except requests.exceptions.RequestException as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_msg = f"Request error: {str(e)}"
        logger.error(f"Webhook {delivery_id} request error: {error_msg}")
        _handle_delivery_failure(
            self, delivery, error_msg, response_code, response_body,
            response_time_ms, response_headers
        )
        raise  # Let Celery handle retry


def _handle_delivery_failure(task, delivery, error_message, response_code=None,
                            response_body=None, response_time_ms=None, response_headers=None):
    """
    Handle a delivery failure by updating the delivery record.

    Args:
        task: The Celery task instance
        delivery: WebhookDelivery instance
        error_message: Error message describing the failure
        response_code: HTTP response code if available
        response_body: Response body if available
        response_time_ms: Response time in milliseconds
        response_headers: Response headers dict
    """
    max_retries = delivery.endpoint.max_retries
    current_attempt = delivery.attempt_count
    will_retry = current_attempt < max_retries

    if will_retry:
        # Calculate next retry time
        retry_delay = calculate_retry_delay(current_attempt)
        next_retry_at = timezone.now() + timedelta(seconds=retry_delay)
    else:
        next_retry_at = None

    delivery.mark_failed(
        error_message=error_message,
        response_code=response_code,
        response_body=response_body,
        response_time_ms=response_time_ms,
        will_retry=will_retry,
        next_retry_at=next_retry_at,
    )

    if will_retry:
        logger.info(
            f"Webhook delivery {delivery.id} will retry "
            f"(attempt {current_attempt}/{max_retries}, next retry at {next_retry_at})"
        )
    else:
        logger.warning(
            f"Webhook delivery {delivery.id} failed permanently "
            f"after {current_attempt} attempts"
        )


@shared_task(name='webhooks.send_test_webhook')
def send_test_webhook(endpoint_id: str):
    """
    Send a test webhook to verify endpoint configuration.

    Args:
        endpoint_id: UUID of the WebhookEndpoint

    Returns:
        dict with success status and details
    """
    from .models import WebhookEndpoint

    try:
        endpoint = WebhookEndpoint.objects.get(id=endpoint_id)
    except WebhookEndpoint.DoesNotExist:
        return {
            'success': False,
            'error': f'Endpoint {endpoint_id} not found'
        }

    # Create test payload
    test_payload = {
        'event': 'test.webhook',
        'data': {
            'message': 'This is a test webhook from Spwig',
            'timestamp': timezone.now().isoformat(),
            'endpoint_id': str(endpoint.id),
            'endpoint_name': endpoint.name,
        }
    }

    payload_json = json.dumps(test_payload, default=str, ensure_ascii=False)
    timestamp = int(time.time())
    signature = generate_signature(endpoint.secret, timestamp, payload_json)

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'X-Spwig-Signature': f"t={timestamp},v1={signature}",
        'X-Spwig-Event': 'test.webhook',
        'X-Spwig-Test': 'true',
        'X-Spwig-Timestamp': str(timestamp),
        'User-Agent': 'Spwig-Webhooks/1.0',
    }

    start_time = time.time()

    try:
        response = requests.post(
            endpoint.url,
            data=payload_json.encode('utf-8'),
            headers=headers,
            timeout=endpoint.timeout_seconds,
            allow_redirects=False,
        )

        response_time_ms = int((time.time() - start_time) * 1000)

        return {
            'success': 200 <= response.status_code < 300,
            'status_code': response.status_code,
            'response_time_ms': response_time_ms,
            'response_body': response.text[:1000] if response.text else '',
        }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': f'Request timed out after {endpoint.timeout_seconds}s',
            'response_time_ms': int((time.time() - start_time) * 1000),
        }

    except requests.exceptions.ConnectionError as e:
        return {
            'success': False,
            'error': f'Connection error: {str(e)}',
        }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Request error: {str(e)}',
        }


@shared_task(name='webhooks.retry_failed_deliveries')
def retry_failed_deliveries():
    """
    Retry failed webhook deliveries that are due for retry.

    This task should be run periodically (e.g., every minute) to
    pick up deliveries that need to be retried.
    """
    from .models import WebhookDelivery

    # Find deliveries that are due for retry
    due_deliveries = WebhookDelivery.objects.filter(
        status=WebhookDelivery.Status.RETRYING,
        next_retry_at__lte=timezone.now(),
    ).select_related('endpoint')

    count = 0
    for delivery in due_deliveries:
        if delivery.endpoint.is_active and not delivery.endpoint.is_disabled_by_failures:
            deliver_webhook.delay(str(delivery.id))
            count += 1

    if count > 0:
        logger.info(f"Queued {count} webhook deliveries for retry")

    return count


@shared_task(name='webhooks.cleanup_old_deliveries')
def cleanup_old_deliveries(days: int = 30):
    """
    Clean up old webhook delivery records.

    Args:
        days: Delete deliveries older than this many days

    Returns:
        Number of deleted records
    """
    from .models import WebhookDelivery

    cutoff = timezone.now() - timedelta(days=days)
    deleted, _ = WebhookDelivery.objects.filter(
        created_at__lt=cutoff,
        status__in=[WebhookDelivery.Status.SUCCESS, WebhookDelivery.Status.FAILED],
    ).delete()

    if deleted > 0:
        logger.info(f"Cleaned up {deleted} old webhook delivery records")

    return deleted
