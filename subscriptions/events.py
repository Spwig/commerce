"""
Standardized Subscription Event Definitions

Provider-agnostic event types and data structures for subscription lifecycle events.
Used by both webhook processing (native providers) and fallback billing engine.
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Optional
from django.utils import timezone
import uuid


class SubscriptionEventType(str, Enum):
    """Standardized subscription event types across all providers."""

    CREATED = 'subscription.created'
    ACTIVATED = 'subscription.activated'
    PAYMENT_SUCCEEDED = 'subscription.payment_succeeded'
    PAYMENT_FAILED = 'subscription.payment_failed'
    PAST_DUE = 'subscription.past_due'
    CANCELED = 'subscription.canceled'
    EXPIRED = 'subscription.expired'
    PAUSED = 'subscription.paused'
    RESUMED = 'subscription.resumed'
    UPDATED = 'subscription.updated'
    TRIAL_ENDING = 'subscription.trial_ending'
    RENEWAL_UPCOMING = 'subscription.renewal_upcoming'
    PLAN_UPGRADED = 'subscription.plan_upgraded'
    PLAN_DOWNGRADED = 'subscription.plan_downgraded'
    REACTIVATED = 'subscription.reactivated'


@dataclass
class SubscriptionEvent:
    """
    Provider-agnostic subscription event.
    Created from webhook payloads (native) or Celery task state changes (fallback).
    """

    event_type: SubscriptionEventType
    event_id: str
    source: str  # 'webhook' or 'fallback'

    # Provider identifiers
    provider_subscription_id: str = ''
    provider_customer_id: str = ''
    provider_event_type: str = ''  # Original provider event type

    # Event data
    data: Dict[str, Any] = field(default_factory=dict)

    # Financial details (for payment events)
    amount: Optional[Decimal] = None
    currency: str = ''

    # Period details (for billing events)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None

    # Error details (for failure events)
    error_code: str = ''
    error_message: str = ''

    # Timestamp
    occurred_at: Optional[datetime] = None

    def __post_init__(self):
        if self.occurred_at is None:
            self.occurred_at = timezone.now()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict for storage in SubscriptionWebhookEvent.event_data."""
        result = {
            'event_type': self.event_type.value,
            'event_id': self.event_id,
            'source': self.source,
            'provider_subscription_id': self.provider_subscription_id,
            'provider_customer_id': self.provider_customer_id,
            'provider_event_type': self.provider_event_type,
            'data': self.data,
            'currency': self.currency,
            'error_code': self.error_code,
            'error_message': self.error_message,
            'occurred_at': self.occurred_at.isoformat() if self.occurred_at else None,
        }
        if self.amount is not None:
            result['amount'] = str(self.amount)
        if self.period_start:
            result['period_start'] = self.period_start.isoformat()
        if self.period_end:
            result['period_end'] = self.period_end.isoformat()
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubscriptionEvent':
        """Reconstruct from stored dict (for retry processing)."""
        from dateutil.parser import parse as parse_date

        kwargs = {
            'event_type': SubscriptionEventType(data['event_type']),
            'event_id': data['event_id'],
            'source': data['source'],
            'provider_subscription_id': data.get('provider_subscription_id', ''),
            'provider_customer_id': data.get('provider_customer_id', ''),
            'provider_event_type': data.get('provider_event_type', ''),
            'data': data.get('data', {}),
            'currency': data.get('currency', ''),
            'error_code': data.get('error_code', ''),
            'error_message': data.get('error_message', ''),
        }
        if data.get('amount'):
            kwargs['amount'] = Decimal(data['amount'])
        if data.get('period_start'):
            kwargs['period_start'] = parse_date(data['period_start'])
        if data.get('period_end'):
            kwargs['period_end'] = parse_date(data['period_end'])
        if data.get('occurred_at'):
            kwargs['occurred_at'] = parse_date(data['occurred_at'])
        return cls(**kwargs)

    @staticmethod
    def generate_fallback_event_id(subscription_id: str, event_type: str) -> str:
        """Generate a unique event ID for fallback (non-webhook) events."""
        return f"fallback_{subscription_id}_{event_type}_{uuid.uuid4().hex[:12]}"
