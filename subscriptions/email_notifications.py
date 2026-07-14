"""
Subscription Email Notifications

Signal handler that dispatches email notifications for subscription lifecycle events.
Connected to the subscription_event_processed signal in apps.py ready().
"""

import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.sites.models import Site
from django.dispatch import receiver
from django.utils import timezone

from .events import SubscriptionEventType
from .signals import subscription_event_processed

logger = logging.getLogger(__name__)

# ============================================================================
# Event Type → Email Template Mapping
# ============================================================================

_EVENT_TEMPLATE_MAP = {
    SubscriptionEventType.CREATED: "subscription_created",
    SubscriptionEventType.ACTIVATED: "subscription_created",  # Same welcome template
    SubscriptionEventType.PAYMENT_SUCCEEDED: "subscription_payment_success",
    SubscriptionEventType.PAYMENT_FAILED: "subscription_payment_failed",
    # PAST_DUE: no email — covered by PAYMENT_FAILED
    SubscriptionEventType.CANCELED: "subscription_canceled",
    SubscriptionEventType.EXPIRED: "subscription_expired",
    SubscriptionEventType.PAUSED: "subscription_paused",
    SubscriptionEventType.RESUMED: "subscription_resumed",
    SubscriptionEventType.TRIAL_ENDING: "subscription_trial_ending",
    SubscriptionEventType.RENEWAL_UPCOMING: "subscription_renewal_reminder",
    SubscriptionEventType.PLAN_UPGRADED: "subscription_plan_upgraded",
    SubscriptionEventType.PLAN_DOWNGRADED: "subscription_plan_downgraded",
    SubscriptionEventType.REACTIVATED: "subscription_reactivated",
    # UPDATED: no email — too generic
}


# ============================================================================
# Signal Handler
# ============================================================================


@receiver(subscription_event_processed)
def handle_subscription_event(sender, event, subscription, **kwargs):
    """
    Send email notification when a subscription event is processed.

    This handler is registered via the @receiver decorator when the module
    is imported in SubscriptionsConfig.ready().

    Args:
        sender: SubscriptionEventProcessor class
        event: SubscriptionEvent instance
        subscription: CustomerSubscription instance
    """
    template_type = _EVENT_TEMPLATE_MAP.get(event.event_type)
    if not template_type:
        return

    try:
        from email_system.services.email_sender import EmailSendingService

        context = _build_email_context(subscription, event)
        from email_system.utils.language import get_user_email_language

        language = get_user_email_language(subscription.user)

        EmailSendingService.send_template_email(
            to_email=subscription.user.email,
            template_type=template_type,
            context=context,
            language=language,
            enable_tracking=True,
        )

        logger.info(
            f"Queued {template_type} email for subscription "
            f"{subscription.subscription_id} ({subscription.user.email})"
        )

    except Exception as e:
        # Never crash the event processor — log and move on
        logger.error(
            f"Failed to send {template_type} email for subscription "
            f"{subscription.subscription_id}: {e}",
            exc_info=True,
        )


# ============================================================================
# Context Builders
# ============================================================================


def _get_site_url():
    """Get the site URL for building absolute links."""
    try:
        site = Site.objects.get_current()
        return f"http://{site.domain}" if settings.DEBUG else f"https://{site.domain}"
    except Exception:
        return getattr(settings, "SITE_URL", "http://localhost:8000")


def _get_subscription_amount(subscription):
    """
    Get the display-formatted subscription amount per billing cycle.

    Returns a string like "USD 29.99" or "EUR 45.00".
    """
    try:
        tier = subscription.pricing_tier
        product = subscription.product
        variant = subscription.variant

        if product:
            price = tier.calculate_price(product, variant)
            return f"{price.currency} {price.amount}"

        # Fallback: check latest successful billing log
        latest_log = (
            subscription.billing_logs.filter(status="successful").order_by("-billing_date").first()
        )
        if latest_log:
            return f"{latest_log.total_amount_currency} {latest_log.total_amount}"

        return tier.tier_name
    except Exception:
        return ""


def _build_email_context(subscription, event):
    """
    Build the template context dict for subscription emails.

    Produces common context variables shared across all templates,
    plus event-specific additions.
    """
    site_url = _get_site_url()
    from email_system.utils.language import get_user_email_language

    language = get_user_email_language(subscription.user)
    sub_id = str(subscription.subscription_id)

    # Base URL path for subscription management
    base_url = f"{site_url}/{language}/account/subscriptions/{sub_id}"

    # Common context — available for ALL subscription email templates
    context = {
        "customer_name": subscription.user.get_full_name() or subscription.user.email,
        "customer_email": subscription.user.email,
        "plan_name": subscription.plan.name,
        "product_name": subscription.product.name if subscription.product else "",
        "subscription_amount": _get_subscription_amount(subscription),
        "billing_cycle": subscription.pricing_tier.get_billing_display(),
        "next_billing_date": subscription.next_billing_date,
        "trial_end_date": subscription.trial_end_date,
        "trial_period": (
            subscription.plan.trial_period_days if subscription.plan.trial_period_days else None
        ),
        "payment_method": str(subscription.payment_token),
        "manage_subscription_url": f"{base_url}/",
        "cancel_subscription_url": f"{base_url}/cancel/",
        "update_payment_url": f"{base_url}/payment/",
        "resume_subscription_url": f"{base_url}/resume/",
        "reactivate_url": f"{base_url}/reactivate/",
        "renew_url": f"{base_url}/renew/",
        "feedback_url": f"{site_url}/{language}/contact/",
        "download_receipt_url": f"{base_url}/receipts/",
    }

    # Event-specific context additions
    _add_event_context(context, subscription, event)

    return context


def _add_event_context(context, subscription, event):
    """Add event-type-specific context variables."""
    now = timezone.now()

    if event.event_type == SubscriptionEventType.PAYMENT_SUCCEEDED:
        context["amount_paid"] = (
            f"{event.currency} {event.amount}"
            if event.amount is not None
            else context.get("subscription_amount", "")
        )
        context["payment_date"] = event.occurred_at or now
        context["transaction_id"] = event.data.get("transaction_id", "")

    elif event.event_type == SubscriptionEventType.PAYMENT_FAILED:
        context["failure_reason"] = event.error_message or "Payment could not be processed"
        grace_days = subscription.plan.grace_period_days or 3
        context["retry_days"] = grace_days
        if subscription.next_billing_date:
            context["retry_date"] = subscription.next_billing_date + timedelta(days=grace_days)

    elif event.event_type == SubscriptionEventType.CANCELED:
        context["cancellation_date"] = subscription.canceled_at or now
        if subscription.cancellation_type == "end_of_period":
            context["access_until"] = subscription.current_period_end

    elif event.event_type == SubscriptionEventType.EXPIRED:
        context["expiration_date"] = event.occurred_at or now

    elif event.event_type == SubscriptionEventType.PAUSED:
        context["pause_date"] = subscription.paused_at or now

    elif event.event_type == SubscriptionEventType.RESUMED:
        context["resume_date"] = event.occurred_at or now

    elif event.event_type == SubscriptionEventType.TRIAL_ENDING:
        if subscription.trial_end_date:
            delta = subscription.trial_end_date - now
            context["days_remaining"] = max(0, delta.days)

    elif event.event_type == SubscriptionEventType.RENEWAL_UPCOMING:
        if subscription.next_billing_date:
            delta = subscription.next_billing_date - now
            context["days_until_renewal"] = max(0, delta.days)

    elif event.event_type in (
        SubscriptionEventType.PLAN_UPGRADED,
        SubscriptionEventType.PLAN_DOWNGRADED,
    ):
        context["old_plan_name"] = event.data.get("old_plan_name", "")
        context["new_plan_name"] = event.data.get("new_plan_name", "")
        context["upgrade_date"] = event.occurred_at or now
        context["downgrade_date"] = event.occurred_at or now
        context["change_date"] = event.occurred_at or now
        context["new_price"] = event.data.get("new_price", "")
        context["billing_period"] = event.data.get("billing_period", "")
        context["effective_date"] = event.data.get("effective_date", "")
        context["account_url"] = context.get("manage_subscription_url", "")
        context["upgrade_url"] = context.get("manage_subscription_url", "")
        context["support_url"] = context.get("feedback_url", "")
        if event.data.get("prorated_charge"):
            context["prorated_charge"] = event.data["prorated_charge"]
        if event.data.get("credit_amount"):
            context["credit_amount"] = event.data["credit_amount"]
            context["credit_applied"] = True

    elif event.event_type == SubscriptionEventType.REACTIVATED:
        context["reactivation_date"] = event.occurred_at or now
        context["new_billing_date"] = subscription.next_billing_date
        context["previous_cancellation_date"] = event.data.get("previous_cancellation_date", "")


# ============================================================================
# Payment Method Expiry Email (called directly from Celery task)
# ============================================================================


def send_payment_method_expiry_email(subscription):
    """
    Send payment method expiring notification for a specific subscription.

    Called from the send_payment_method_expiry_warnings Celery task.
    """
    try:
        from datetime import date

        from email_system.services.email_sender import EmailSendingService

        site_url = _get_site_url()
        from email_system.utils.language import get_user_email_language

        language = get_user_email_language(subscription.user)
        sub_id = str(subscription.subscription_id)
        base_url = f"{site_url}/{language}/account/subscriptions/{sub_id}"
        token = subscription.payment_token

        # Build expiration date from card exp month/year
        exp_date = None
        if token.card_exp_month and token.card_exp_year:
            exp_date = date(token.card_exp_year, token.card_exp_month, 1)

        context = {
            "customer_name": subscription.user.get_full_name() or subscription.user.email,
            "plan_name": subscription.plan.name,
            "payment_method": str(token),
            "expiration_date": exp_date,
            "next_billing_date": subscription.next_billing_date,
            "update_payment_url": f"{base_url}/payment/",
            "manage_subscription_url": f"{base_url}/",
        }

        EmailSendingService.send_template_email(
            to_email=subscription.user.email,
            template_type="subscription_payment_method_expiring",
            context=context,
            language=language,
            enable_tracking=True,
        )

        logger.info(
            f"Queued payment method expiry email for subscription "
            f"{subscription.subscription_id} ({subscription.user.email})"
        )

    except Exception as e:
        logger.error(
            f"Failed to send payment method expiry email for subscription "
            f"{subscription.subscription_id}: {e}",
            exc_info=True,
        )


# ============================================================================
# Dunning Final Notice Email (called directly from Celery task)
# ============================================================================


def send_dunning_final_notice_email(subscription):
    """
    Send dunning final notice email for a subscription whose grace period
    is about to expire.

    Called from the send_dunning_final_notices Celery task.
    """
    try:
        from email_system.services.email_sender import EmailSendingService

        site_url = _get_site_url()
        from email_system.utils.language import get_user_email_language

        language = get_user_email_language(subscription.user)
        sub_id = str(subscription.subscription_id)
        base_url = f"{site_url}/{language}/account/subscriptions/{sub_id}"
        now = timezone.now()

        # Calculate days until cancellation
        days_until = 0
        cancellation_date = now
        if subscription.grace_period_end_date:
            delta = subscription.grace_period_end_date - now
            days_until = max(0, delta.days)
            cancellation_date = subscription.grace_period_end_date

        # Get last failed billing log for error details
        last_failed_log = (
            subscription.billing_logs.filter(status="failed").order_by("-billing_date").first()
        )

        context = {
            "customer_name": (subscription.user.get_full_name() or subscription.user.email),
            "plan_name": subscription.plan.name,
            "amount_due": _get_subscription_amount(subscription),
            "retry_count": (last_failed_log.retry_count if last_failed_log else 0),
            "last_retry_date": (last_failed_log.billing_date if last_failed_log else now),
            "days_until_cancellation": days_until,
            "cancellation_date": cancellation_date,
            "payment_error_message": (
                last_failed_log.error_message
                if last_failed_log
                else "Payment could not be processed"
            ),
            "update_payment_url": f"{base_url}/payment/",
            "support_url": f"{site_url}/{language}/contact/",
            "manage_subscription_url": f"{base_url}/",
        }

        EmailSendingService.send_template_email(
            to_email=subscription.user.email,
            template_type="subscription_dunning_final_notice",
            context=context,
            language=language,
            enable_tracking=True,
        )

        logger.info(
            f"Queued dunning final notice email for subscription "
            f"{subscription.subscription_id} ({subscription.user.email})"
        )

    except Exception as e:
        logger.error(
            f"Failed to send dunning final notice for subscription "
            f"{subscription.subscription_id}: {e}",
            exc_info=True,
        )
