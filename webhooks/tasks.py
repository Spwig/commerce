"""
Celery tasks for webhook delivery.

This module provides async tasks for delivering webhooks with
retry logic and exponential backoff.
"""

import hashlib
import hmac
import json
import logging
import time
from datetime import timedelta

import requests
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)

# HTTP response codes that warrant a retry (transient server / rate-limit errors).
# All other non-2xx responses are permanent client errors and must not be retried.
RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


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
        secret.encode("utf-8"), signature_payload.encode("utf-8"), hashlib.sha256
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
    name="webhooks.deliver_webhook",
    # Retries are owned explicitly by _handle_delivery_failure via self.retry(), which
    # honours each endpoint's own max_retries. Celery's autoretry_for / retry_backoff are
    # intentionally omitted so retries fire from a single path (no duplicate deliveries) and
    # so the persisted next_retry_at schedule matches the actual retry countdown.
    max_retries=None,
    acks_late=True,
    reject_on_worker_lost=True,
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
        delivery = WebhookDelivery.objects.select_related("endpoint").get(id=delivery_id)
    except WebhookDelivery.DoesNotExist:
        logger.error(f"WebhookDelivery {delivery_id} not found")
        return

    endpoint = delivery.endpoint

    # Check if endpoint is active
    if not endpoint.is_active:
        logger.info(f"Webhook endpoint {endpoint.id} is inactive, skipping delivery {delivery_id}")
        delivery.status = WebhookDelivery.Status.FAILED
        delivery.error_message = "Endpoint is inactive"
        delivery.save(update_fields=["status", "error_message"])
        return

    if endpoint.is_disabled_by_failures:
        logger.info(
            f"Webhook endpoint {endpoint.id} is disabled due to failures, skipping delivery {delivery_id}"
        )
        delivery.status = WebhookDelivery.Status.FAILED
        delivery.error_message = "Endpoint is disabled due to consecutive failures"
        delivery.save(update_fields=["status", "error_message"])
        return

    # Prepare payload
    try:
        payload_json = json.dumps(delivery.payload, default=str, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        logger.error(f"Failed to serialize payload for delivery {delivery_id}: {e}")
        delivery.status = WebhookDelivery.Status.FAILED
        delivery.error_message = f"Failed to serialize payload: {e}"
        delivery.save(update_fields=["status", "error_message"])
        return

    # Generate signature
    timestamp = int(time.time())
    signature = generate_signature(endpoint.secret, timestamp, payload_json)

    # Prepare headers
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Spwig-Signature": f"t={timestamp},v1={signature}",
        "X-Spwig-Event": delivery.event_type,
        "X-Spwig-Delivery-Id": str(delivery.id),
        "X-Spwig-Timestamp": str(timestamp),
        "User-Agent": "Spwig-Webhooks/1.0",
    }

    # Increment attempt count
    delivery.attempt_count += 1
    delivery.status = WebhookDelivery.Status.RETRYING
    delivery.save(update_fields=["attempt_count", "status"])

    # Send request
    start_time = time.time()
    response_time_ms = None
    response_code = None
    response_body = None
    response_headers = {}

    try:
        logger.info(
            f"Delivering webhook {delivery_id} to {endpoint.url} (attempt {delivery.attempt_count})"
        )

        response = requests.post(
            endpoint.url,
            data=payload_json.encode("utf-8"),
            headers=headers,
            timeout=endpoint.timeout_seconds,
            allow_redirects=False,  # Don't follow redirects for security
        )

        response_time_ms = int((time.time() - start_time) * 1000)
        response_code = response.status_code
        response_body = response.text[:10000] if response.text else ""  # Truncate large responses
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

    except requests.exceptions.Timeout:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_msg = f"Request timed out after {endpoint.timeout_seconds}s"
        logger.warning(f"Webhook {delivery_id} timed out: {error_msg}")
        _handle_delivery_failure(
            self,
            delivery,
            error_msg,
            response_code,
            response_body,
            response_time_ms,
            response_headers,
            retryable=True,
        )

    except requests.exceptions.ConnectionError as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_msg = f"Connection error: {str(e)}"
        logger.warning(f"Webhook {delivery_id} connection error: {error_msg}")
        _handle_delivery_failure(
            self,
            delivery,
            error_msg,
            response_code,
            response_body,
            response_time_ms,
            response_headers,
            retryable=True,
        )

    except requests.exceptions.HTTPError as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_msg = str(e)
        # Only server errors / rate limits are retryable; other 4xx are permanent.
        _handle_delivery_failure(
            self,
            delivery,
            error_msg,
            response_code,
            response_body,
            response_time_ms,
            response_headers,
            retryable=response_code in RETRYABLE_STATUS_CODES,
        )

    except requests.exceptions.RequestException as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        error_msg = f"Request error: {str(e)}"
        logger.error(f"Webhook {delivery_id} request error: {error_msg}")
        _handle_delivery_failure(
            self,
            delivery,
            error_msg,
            response_code,
            response_body,
            response_time_ms,
            response_headers,
            retryable=True,
        )


def _handle_delivery_failure(
    task,
    delivery,
    error_message,
    response_code=None,
    response_body=None,
    response_time_ms=None,
    response_headers=None,
    *,
    retryable,
):
    """
    Handle a delivery failure by updating the delivery record and scheduling any retry.

    A retry is only scheduled when the error is retryable (transient) *and* the endpoint's
    own max_retries has not been reached. When it is, the Celery retry is scheduled with the
    exact same countdown that is persisted in next_retry_at, so the stored schedule describes
    the real retry. Otherwise the delivery is marked FAILED, which records a failure against
    the endpoint (driving consecutive_failures / auto-disable) and clears next_retry_at.

    Args:
        task: The Celery task instance
        delivery: WebhookDelivery instance
        error_message: Error message describing the failure
        response_code: HTTP response code if available
        response_body: Response body if available
        response_time_ms: Response time in milliseconds
        response_headers: Response headers dict
        retryable: Whether the underlying error is transient and eligible for retry
    """
    max_retries = delivery.endpoint.max_retries
    current_attempt = delivery.attempt_count
    will_retry = retryable and current_attempt < max_retries

    if will_retry:
        # Calculate next retry time from the same countdown used to schedule the Celery retry.
        retry_delay = calculate_retry_delay(current_attempt)
        next_retry_at = timezone.now() + timedelta(seconds=retry_delay)
    else:
        retry_delay = None
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
        # Own the retry explicitly so it fires exactly once, at next_retry_at.
        raise task.retry(countdown=retry_delay)

    logger.warning(
        f"Webhook delivery {delivery.id} failed permanently after {current_attempt} attempts"
    )


@shared_task(name="webhooks.send_test_webhook")
def send_test_webhook(endpoint_id: str):
    """
    Send a test webhook to verify endpoint configuration.

    Args:
        endpoint_id: UUID of the WebhookEndpoint

    Returns:
        dict with success status and details
    """
    from core.license import is_sandbox_mode

    from .models import WebhookEndpoint
    from .services import _is_localhost_url

    try:
        endpoint = WebhookEndpoint.objects.get(id=endpoint_id)
    except WebhookEndpoint.DoesNotExist:
        return {"success": False, "error": f"Endpoint {endpoint_id} not found"}

    # In sandbox mode only localhost URLs may be contacted, using the same validated policy
    # as the webhook delivery service. This closes the test path that would otherwise POST to
    # an external URL that normal triggers block as sandbox_blocked.
    if is_sandbox_mode() and not _is_localhost_url(endpoint.url):
        logger.info(
            f"[SANDBOX] Test webhook to {endpoint.url} blocked (external URL in sandbox mode)"
        )
        return {
            "success": False,
            "error": "Sandbox mode only allows test webhooks to localhost URLs",
            "sandbox_blocked": True,
        }

    # Create test payload
    test_payload = {
        "event": "test.webhook",
        "data": {
            "message": "This is a test webhook from Spwig",
            "timestamp": timezone.now().isoformat(),
            "endpoint_id": str(endpoint.id),
            "endpoint_name": endpoint.name,
        },
    }

    payload_json = json.dumps(test_payload, default=str, ensure_ascii=False)
    timestamp = int(time.time())
    signature = generate_signature(endpoint.secret, timestamp, payload_json)

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Spwig-Signature": f"t={timestamp},v1={signature}",
        "X-Spwig-Event": "test.webhook",
        "X-Spwig-Test": "true",
        "X-Spwig-Timestamp": str(timestamp),
        "User-Agent": "Spwig-Webhooks/1.0",
    }

    start_time = time.time()

    try:
        response = requests.post(
            endpoint.url,
            data=payload_json.encode("utf-8"),
            headers=headers,
            timeout=endpoint.timeout_seconds,
            allow_redirects=False,
        )

        response_time_ms = int((time.time() - start_time) * 1000)

        return {
            "success": 200 <= response.status_code < 300,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
            "response_body": response.text[:1000] if response.text else "",
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": f"Request timed out after {endpoint.timeout_seconds}s",
            "response_time_ms": int((time.time() - start_time) * 1000),
        }

    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "error": f"Connection error: {str(e)}",
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request error: {str(e)}",
        }


@shared_task(name="webhooks.cleanup_old_deliveries")
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
