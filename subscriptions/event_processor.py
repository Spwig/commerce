"""
Subscription Event Processor

Provider-agnostic processor that handles subscription lifecycle events from
both webhooks (native providers) and fallback billing engine (Celery tasks).
"""

import logging

from django.db import IntegrityError
from django.utils import timezone

from .events import SubscriptionEvent, SubscriptionEventType
from .models import CustomerSubscription, SubscriptionWebhookEvent
from .signals import subscription_event_processed

logger = logging.getLogger(__name__)


class SubscriptionEventProcessor:
    """
    Processes subscription events and maintains the audit trail.
    Handles idempotency, state machine updates, and signal emission.
    """

    @classmethod
    def process_event(cls, event: SubscriptionEvent) -> tuple:
        """
        Process a subscription lifecycle event.

        Args:
            event: SubscriptionEvent instance

        Returns:
            tuple: (success: bool, message: str)
        """
        # 1. Idempotency check - skip if already processed
        existing = SubscriptionWebhookEvent.objects.filter(
            event_id=event.event_id, source=event.source
        ).first()

        if existing and existing.status == "processed":
            logger.info(f"Duplicate event skipped: {event.event_id}")
            return True, "duplicate"

        # 2. Create or retrieve audit record
        try:
            webhook_event = SubscriptionWebhookEvent.objects.create(
                event_id=event.event_id,
                event_type=event.event_type.value,
                provider_event_type=event.provider_event_type,
                source=event.source,
                provider_subscription_id=event.provider_subscription_id,
                event_data=event.to_dict(),
                status="pending",
            )
        except IntegrityError:
            # Race condition: concurrent processing created the record
            webhook_event = SubscriptionWebhookEvent.objects.get(
                event_id=event.event_id, source=event.source
            )
            if webhook_event.status == "processed":
                return True, "duplicate"

        # 3. Find the subscription
        subscription = cls._find_subscription(event)

        if not subscription:
            # Subscription not found yet - mark as skipped for retry
            webhook_event.status = "skipped"
            webhook_event.processing_error = (
                f"Subscription not found for provider_subscription_id="
                f"'{event.provider_subscription_id}'"
            )
            webhook_event.save(update_fields=["status", "processing_error"])
            logger.warning(f"Subscription not found for event {event.event_id}, marked as skipped")
            return False, "subscription_not_found"

        # 4. Link subscription to audit record
        webhook_event.subscription = subscription

        # 5. Apply state changes
        try:
            cls._apply_event(subscription, event)
        except Exception as e:
            webhook_event.status = "failed"
            webhook_event.processing_error = str(e)
            webhook_event.save(update_fields=["status", "processing_error", "subscription"])
            logger.exception(f"Failed to apply event {event.event_id}: {e}")
            return False, str(e)

        # 6. Emit signal for downstream consumers (P2 email notifications)
        try:
            subscription_event_processed.send(
                sender=cls,
                event=event,
                subscription=subscription,
            )
        except Exception as e:
            # Signal handler failure should not fail the event processing
            logger.warning(f"Signal handler error for event {event.event_id}: {e}")

        # 7. Mark as processed
        webhook_event.status = "processed"
        webhook_event.processed_at = timezone.now()
        webhook_event.save(update_fields=["status", "processed_at", "subscription"])

        logger.info(
            f"Processed subscription event: {event.event_type.value} "
            f"for subscription {subscription.subscription_id}"
        )
        return True, "processed"

    @classmethod
    def _find_subscription(cls, event: SubscriptionEvent):
        """
        Find the CustomerSubscription for this event.
        Checks provider_subscription_id (webhook events) or
        internal_subscription_id (fallback events).
        """
        # Fallback events include internal subscription ID
        internal_id = event.data.get("internal_subscription_id")
        if internal_id:
            try:
                return CustomerSubscription.objects.get(subscription_id=internal_id)
            except CustomerSubscription.DoesNotExist:
                pass

        # Webhook events: look up by provider subscription ID
        if event.provider_subscription_id:
            try:
                return CustomerSubscription.objects.get(
                    provider_subscription_id=event.provider_subscription_id
                )
            except CustomerSubscription.DoesNotExist:
                pass

        return None

    @classmethod
    def _apply_event(cls, subscription: CustomerSubscription, event: SubscriptionEvent):
        """
        Apply state changes from event to subscription model.
        For fallback events, skip state mutations (already applied by Celery task)
        but still emit signal. For webhook events, apply state changes.
        """
        if event.source == "fallback":
            # Fallback tasks already updated the model directly.
            # We only need the audit trail and signal emission (handled by caller).
            return

        # Webhook events: apply state changes based on event type
        update_fields = []

        if event.event_type == SubscriptionEventType.CREATED:
            # Subscription created at provider - usually already handled by
            # SubscriptionManager.create_subscription(), but sync if needed
            if subscription.status not in ("active", "trial"):
                subscription.status = "active"
                update_fields.append("status")

        elif event.event_type == SubscriptionEventType.ACTIVATED:
            subscription.status = "active"
            update_fields.append("status")

        elif event.event_type == SubscriptionEventType.PAYMENT_SUCCEEDED:
            subscription.status = "active"
            subscription.last_billing_date = event.occurred_at
            subscription.last_billing_status = "successful"
            update_fields.extend(["status", "last_billing_date", "last_billing_status"])

            if event.period_start:
                subscription.current_period_start = event.period_start
                update_fields.append("current_period_start")
            if event.period_end:
                subscription.current_period_end = event.period_end
                subscription.next_billing_date = event.period_end
                update_fields.extend(["current_period_end", "next_billing_date"])

        elif event.event_type == SubscriptionEventType.PAYMENT_FAILED:
            subscription.status = "past_due"
            subscription.last_billing_status = "failed"
            update_fields.extend(["status", "last_billing_status"])

        elif event.event_type == SubscriptionEventType.PAST_DUE:
            subscription.status = "past_due"
            update_fields.append("status")

        elif event.event_type == SubscriptionEventType.CANCELED:
            subscription.status = "canceled"
            subscription.canceled_at = event.occurred_at or timezone.now()
            update_fields.extend(["status", "canceled_at"])

        elif event.event_type == SubscriptionEventType.EXPIRED:
            subscription.status = "expired"
            update_fields.append("status")

        elif event.event_type == SubscriptionEventType.PAUSED:
            subscription.status = "paused"
            subscription.paused_at = event.occurred_at or timezone.now()
            update_fields.extend(["status", "paused_at"])

        elif event.event_type == SubscriptionEventType.RESUMED:
            subscription.status = "active"
            subscription.paused_at = None
            subscription.pause_reason = ""
            subscription.auto_resume_date = None
            update_fields.extend(["status", "paused_at", "pause_reason", "auto_resume_date"])

        elif event.event_type == SubscriptionEventType.UPDATED:
            # Generic update - sync period dates if available
            if event.period_start:
                subscription.current_period_start = event.period_start
                update_fields.append("current_period_start")
            if event.period_end:
                subscription.current_period_end = event.period_end
                subscription.next_billing_date = event.period_end
                update_fields.extend(["current_period_end", "next_billing_date"])

        # TRIAL_ENDING and RENEWAL_UPCOMING are informational only -
        # they don't change subscription state, just trigger notifications via signal.

        if update_fields:
            subscription.save(update_fields=update_fields)

    @classmethod
    def retry_skipped_events(cls, max_retries: int = 5) -> int:
        """
        Retry events that were skipped because the subscription wasn't found yet.

        Returns:
            int: Number of events successfully processed
        """
        skipped_events = SubscriptionWebhookEvent.objects.filter(
            status="skipped",
            retry_count__lt=max_retries,
        ).order_by("created_at")

        processed_count = 0

        for webhook_event in skipped_events:
            webhook_event.retry_count += 1

            try:
                event = SubscriptionEvent.from_dict(webhook_event.event_data)
            except Exception as e:
                webhook_event.status = "failed"
                webhook_event.processing_error = f"Failed to deserialize event: {e}"
                webhook_event.save(update_fields=["status", "processing_error", "retry_count"])
                continue

            subscription = cls._find_subscription(event)
            if not subscription:
                webhook_event.save(update_fields=["retry_count"])
                continue

            webhook_event.subscription = subscription

            try:
                cls._apply_event(subscription, event)
            except Exception as e:
                webhook_event.status = "failed"
                webhook_event.processing_error = str(e)
                webhook_event.save(
                    update_fields=["status", "processing_error", "retry_count", "subscription"]
                )
                continue

            # Emit signal
            try:
                subscription_event_processed.send(
                    sender=cls,
                    event=event,
                    subscription=subscription,
                )
            except Exception:
                pass

            webhook_event.status = "processed"
            webhook_event.processed_at = timezone.now()
            webhook_event.save(
                update_fields=["status", "processed_at", "retry_count", "subscription"]
            )
            processed_count += 1

            logger.info(
                f"Retry succeeded for event {webhook_event.event_id} "
                f"(attempt {webhook_event.retry_count})"
            )

        return processed_count
