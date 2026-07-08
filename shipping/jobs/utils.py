"""
Utility functions for shipping Celery tasks

Helper functions used by tasks for common operations like
validation, data formatting, and error handling.
"""
import logging
import hashlib
import json
from typing import Dict, List, Optional, Any
from decimal import Decimal
from django.utils import timezone

logger = logging.getLogger(__name__)


def validate_shipment_data(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate shipment data for rate fetching or label generation.

    Args:
        data: Dictionary with shipment details

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['origin_country', 'dest_country']

    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"

    # Validate country codes (2 characters)
    if len(data['origin_country']) != 2:
        return False, "origin_country must be 2-character ISO code"

    if len(data['dest_country']) != 2:
        return False, "dest_country must be 2-character ISO code"

    # Validate weight if provided
    if 'weight' in data and data['weight']:
        try:
            weight = Decimal(str(data['weight']))
            if weight <= 0:
                return False, "weight must be positive"
        except (ValueError, TypeError):
            return False, "Invalid weight format"

    return True, None


def format_rate_response(provider_rates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format rate response from provider to standardized format.

    Args:
        provider_rates: Raw response from provider

    Returns:
        Standardized rate dictionary
    """
    # TODO (Future Phase): Implement provider-specific formatting
    # This will normalize different provider responses into a standard format

    return {
        'provider_account_id': provider_rates.get('provider_account_id'),
        'carrier': provider_rates.get('carrier', 'Unknown'),
        'service': provider_rates.get('service', 'Unknown'),
        'rate': str(provider_rates.get('rate', '0.00')),
        'currency': provider_rates.get('currency', 'USD'),
        'delivery_days': provider_rates.get('delivery_days'),
        'delivery_date': provider_rates.get('delivery_date'),
        'raw_data': provider_rates.get('raw_data', {})
    }


def format_tracking_event(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format tracking event from provider to standardized format.

    Args:
        event_data: Raw event data from provider

    Returns:
        Standardized tracking event dictionary
    """
    # TODO (Future Phase): Implement provider-specific formatting

    return {
        'status': event_data.get('status', 'in_transit'),
        'description': event_data.get('description', ''),
        'location': event_data.get('location', ''),
        'occurred_at': event_data.get('timestamp') or timezone.now(),
        'raw': event_data
    }


def hash_tracking_event(event_data: Dict[str, Any]) -> str:
    """
    Generate a unique hash for a tracking event to prevent duplicates.

    Args:
        event_data: Tracking event data

    Returns:
        SHA256 hash string
    """
    # Create a deterministic string from key event data
    hash_input = (
        f"{event_data.get('status', '')}"
        f"{event_data.get('description', '')}"
        f"{event_data.get('location', '')}"
        f"{event_data.get('occurred_at', '')}"
    )

    return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()


def should_poll_shipment(shipment) -> bool:
    """
    Determine if a shipment should be polled for tracking updates.

    Args:
        shipment: Shipment model instance

    Returns:
        bool: True if shipment should be polled
    """
    # Don't poll completed/terminal states
    terminal_statuses = ['delivered', 'returned', 'canceled']
    if shipment.status in terminal_statuses:
        return False

    # Don't poll manual shipments (no API)
    if not shipment.provider_account:
        return False

    # Don't poll if tracking_id is missing
    if not shipment.tracking_id:
        return False

    # Don't poll inactive providers
    if not shipment.provider_account.is_active:
        return False

    return True


def get_retry_delay(attempt: int, base_delay: int = 60, max_delay: int = 3600) -> int:
    """
    Calculate exponential backoff delay for retries.

    Args:
        attempt: Current retry attempt (0-indexed)
        base_delay: Base delay in seconds (default: 60)
        max_delay: Maximum delay in seconds (default: 3600)

    Returns:
        int: Delay in seconds
    """
    # Exponential backoff: base_delay * (2 ** attempt)
    delay = base_delay * (2 ** attempt)

    # Cap at max_delay
    return min(delay, max_delay)


def format_error_response(error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Format exception into standardized error response.

    Args:
        error: Exception instance
        context: Additional context information

    Returns:
        Dictionary with error details
    """
    return {
        'success': False,
        'error': str(error),
        'error_type': type(error).__name__,
        'context': context or {},
        'timestamp': timezone.now().isoformat()
    }


def sanitize_webhook_payload(payload: Dict[str, Any], provider_key: str) -> Dict[str, Any]:
    """
    Sanitize webhook payload for logging (remove sensitive data).

    Args:
        payload: Raw webhook payload
        provider_key: Provider identifier

    Returns:
        Sanitized payload safe for logging
    """
    # TODO (Future Phase): Implement provider-specific sanitization
    # Different providers may have different sensitive fields

    sensitive_fields = [
        'api_key',
        'secret',
        'password',
        'token',
        'authorization',
        'credit_card',
        'ssn',
    ]

    def sanitize_dict(d: Dict) -> Dict:
        """Recursively sanitize dictionary"""
        sanitized = {}
        for key, value in d.items():
            # Check if key contains sensitive field name
            if any(sensitive in key.lower() for sensitive in sensitive_fields):
                sanitized[key] = '*** REDACTED ***'
            elif isinstance(value, dict):
                sanitized[key] = sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    sanitize_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized

    return sanitize_dict(payload)


def parse_tracking_status(provider_status: str, provider_key: str) -> str:
    """
    Map provider-specific tracking status to our standardized status.

    Args:
        provider_status: Status string from provider
        provider_key: Provider identifier

    Returns:
        str: Standardized status (matches TrackingEvent.STATUS_CHOICES)
    """
    # TODO (Future Phase): Implement provider-specific mappings

    # Generic mappings (case-insensitive)
    status_lower = provider_status.lower()

    if 'delivered' in status_lower:
        return 'delivered'
    elif 'out for delivery' in status_lower:
        return 'out_for_delivery'
    elif any(word in status_lower for word in ['in transit', 'transit', 'moving']):
        return 'in_transit'
    elif any(word in status_lower for word in ['exception', 'problem', 'issue']):
        return 'exception'
    elif any(word in status_lower for word in ['return', 'returned']):
        return 'returned'
    else:
        return 'info_received'


def batch_shipments(shipment_queryset, batch_size: int = 100):
    """
    Yield shipments in batches for efficient processing.

    Args:
        shipment_queryset: Django queryset of Shipment objects
        batch_size: Number of shipments per batch

    Yields:
        Lists of shipment objects
    """
    offset = 0
    while True:
        batch = list(shipment_queryset[offset:offset + batch_size])
        if not batch:
            break

        yield batch
        offset += batch_size


def calculate_task_eta(delay_seconds: int):
    """
    Calculate ETA for delayed task execution.

    Args:
        delay_seconds: Delay in seconds

    Returns:
        datetime: ETA for task execution
    """
    from datetime import timedelta
    return timezone.now() + timedelta(seconds=delay_seconds)


def log_task_metrics(task_name: str, metrics: Dict[str, Any]):
    """
    Log task execution metrics in structured format.

    Args:
        task_name: Name of the Celery task
        metrics: Dictionary of metrics to log
    """
    logger.info(
        f"Task metrics - {task_name}",
        extra={
            'task': task_name,
            'metrics': metrics,
            'timestamp': timezone.now().isoformat()
        }
    )


class TaskExecutionContext:
    """
    Context manager for tracking task execution.

    Usage:
        with TaskExecutionContext('task_name') as ctx:
            # do work
            ctx.add_metric('records_processed', 100)
    """

    def __init__(self, task_name: str):
        self.task_name = task_name
        self.start_time = None
        self.metrics = {}

    def __enter__(self):
        self.start_time = timezone.now()
        logger.info(f"Task {self.task_name} started")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (timezone.now() - self.start_time).total_seconds()
        self.metrics['duration_seconds'] = duration

        if exc_type:
            self.metrics['success'] = False
            self.metrics['error'] = str(exc_val)
            logger.error(
                f"Task {self.task_name} failed after {duration:.2f}s",
                exc_info=True
            )
        else:
            self.metrics['success'] = True
            logger.info(
                f"Task {self.task_name} completed in {duration:.2f}s"
            )

        log_task_metrics(self.task_name, self.metrics)

    def add_metric(self, key: str, value: Any):
        """Add a metric to track"""
        self.metrics[key] = value
