"""
Django signal handlers for triggering webhooks.

This module connects Django model signals to the webhook system,
automatically triggering webhooks when relevant events occur.
"""
import logging
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)

# Track previous states for detecting changes
_previous_states = {}


def _get_state_key(instance):
    """Generate a unique key for tracking instance state."""
    return f"{instance._meta.label}:{instance.pk}"


def _store_previous_state(instance, fields):
    """Store previous state of specified fields for comparison."""
    key = _get_state_key(instance)
    _previous_states[key] = {
        field: getattr(instance, field, None) for field in fields
    }


def _get_previous_state(instance):
    """Get previously stored state for an instance."""
    key = _get_state_key(instance)
    return _previous_states.pop(key, None)


def _has_field_changed(instance, field, previous_state):
    """Check if a specific field has changed."""
    if previous_state is None:
        return False
    return previous_state.get(field) != getattr(instance, field, None)


# =============================================================================
# Order Signals
# =============================================================================

@receiver(pre_save, sender='orders.Order')
def order_pre_save(sender, instance, **kwargs):
    """Store order state before save for change detection."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _store_previous_state(old_instance, ['status'])
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='orders.Order')
def order_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for order events."""
    from .services import trigger_webhook

    if created:
        trigger_webhook('order.created', instance=instance)
        logger.debug(f"Triggered order.created webhook for order {instance.order_number}")
    else:
        previous_state = _get_previous_state(instance)
        if _has_field_changed(instance, 'status', previous_state):
            old_status = previous_state.get('status') if previous_state else None

            # Trigger specific status events
            if instance.status == 'shipped':
                trigger_webhook('order.fulfilled', instance=instance, previous_status=old_status)
            elif instance.status == 'cancelled':
                trigger_webhook('order.cancelled', instance=instance, previous_status=old_status)
            elif instance.status == 'refunded':
                trigger_webhook('order.refunded', instance=instance, previous_status=old_status)

            # Always trigger the generic status change event
            trigger_webhook(
                'order.status_changed',
                instance=instance,
                previous_status=old_status,
                new_status=instance.status
            )
            logger.debug(
                f"Triggered order.status_changed webhook for order {instance.order_number} "
                f"({old_status} -> {instance.status})"
            )


# =============================================================================
# Product Signals
# =============================================================================

@receiver(pre_save, sender='catalog.Product')
def product_pre_save(sender, instance, **kwargs):
    """Store product state before save for change detection."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _store_previous_state(old_instance, ['status', 'is_active', 'stock_quantity'])
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='catalog.Product')
def product_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for product events."""
    from .services import trigger_webhook

    if created:
        trigger_webhook('product.created', instance=instance)
        logger.debug(f"Triggered product.created webhook for product {instance.pk}")
    else:
        previous_state = _get_previous_state(instance)

        # Check for publish/unpublish
        if previous_state:
            was_active = previous_state.get('is_active', False)
            is_active = getattr(instance, 'is_active', False)

            if not was_active and is_active:
                trigger_webhook('product.published', instance=instance)
            elif was_active and not is_active:
                trigger_webhook('product.unpublished', instance=instance)

            # Check for stock changes
            old_stock = previous_state.get('stock_quantity', 0) or 0
            new_stock = getattr(instance, 'stock_quantity', 0) or 0

            if old_stock > 0 and new_stock == 0:
                trigger_webhook('inventory.out_of_stock', data={
                    'product_id': instance.pk,
                    'product_sku': getattr(instance, 'sku', ''),
                    'product_name': str(instance),
                    'previous_stock': old_stock,
                    'current_stock': new_stock,
                })
            elif old_stock == 0 and new_stock > 0:
                trigger_webhook('inventory.restocked', data={
                    'product_id': instance.pk,
                    'product_sku': getattr(instance, 'sku', ''),
                    'product_name': str(instance),
                    'previous_stock': old_stock,
                    'current_stock': new_stock,
                })

        # Always trigger product.updated for non-created saves
        trigger_webhook('product.updated', instance=instance)


@receiver(post_delete, sender='catalog.Product')
def product_post_delete(sender, instance, **kwargs):
    """Trigger webhook when a product is deleted."""
    from .services import trigger_webhook

    trigger_webhook('product.deleted', data={
        'id': instance.pk,
        'sku': getattr(instance, 'sku', ''),
        'name': str(instance),
    })
    logger.debug(f"Triggered product.deleted webhook for product {instance.pk}")


# =============================================================================
# Customer Signals
# =============================================================================

@receiver(post_save, sender='accounts.CustomerProfile')
def customer_profile_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for customer profile events."""
    from .services import trigger_webhook

    # Only trigger for non-staff users (actual customers)
    user = getattr(instance, 'user', None)
    if user and getattr(user, 'is_staff', False):
        return

    if created:
        trigger_webhook('customer.created', instance=instance)
        logger.debug(f"Triggered customer.created webhook for customer {instance.pk}")
    else:
        trigger_webhook('customer.updated', instance=instance)


# =============================================================================
# Shipment Signals
# =============================================================================

@receiver(pre_save, sender='shipping.Shipment')
def shipment_pre_save(sender, instance, **kwargs):
    """Store shipment state before save for change detection."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _store_previous_state(old_instance, ['status'])
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='shipping.Shipment')
def shipment_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for shipment events."""
    from .services import trigger_webhook

    if created:
        trigger_webhook('shipment.created', instance=instance)
        logger.debug(f"Triggered shipment.created webhook for shipment {instance.pk}")
    else:
        previous_state = _get_previous_state(instance)
        if _has_field_changed(instance, 'status', previous_state):
            old_status = previous_state.get('status') if previous_state else None

            # Map shipment status to webhook events
            status = getattr(instance, 'status', '')
            status_event_map = {
                'shipped': 'shipment.shipped',
                'in_transit': 'shipment.in_transit',
                'out_for_delivery': 'shipment.out_for_delivery',
                'delivered': 'shipment.delivered',
                'failed': 'shipment.failed',
                'returned': 'shipment.returned',
            }

            if status in status_event_map:
                trigger_webhook(
                    status_event_map[status],
                    instance=instance,
                    previous_status=old_status
                )
                logger.debug(
                    f"Triggered {status_event_map[status]} webhook for shipment {instance.pk}"
                )

            # Always trigger tracking update
            trigger_webhook(
                'shipment.tracking_updated',
                instance=instance,
                previous_status=old_status,
                new_status=status
            )


# =============================================================================
# Subscription Signals
# =============================================================================

@receiver(pre_save, sender='subscriptions.CustomerSubscription')
def subscription_pre_save(sender, instance, **kwargs):
    """Store subscription state before save for change detection."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _store_previous_state(old_instance, ['status'])
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender='subscriptions.CustomerSubscription')
def subscription_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for subscription events."""
    from .services import trigger_webhook

    if created:
        trigger_webhook('subscription.created', instance=instance)
        logger.debug(f"Triggered subscription.created webhook for subscription {instance.pk}")
    else:
        previous_state = _get_previous_state(instance)
        if _has_field_changed(instance, 'status', previous_state):
            old_status = previous_state.get('status') if previous_state else None
            status = getattr(instance, 'status', '')

            # Map subscription status to webhook events
            status_event_map = {
                'active': 'subscription.activated',
                'cancelled': 'subscription.cancelled',
                'expired': 'subscription.expired',
                'paused': 'subscription.paused',
            }

            if status in status_event_map:
                trigger_webhook(
                    status_event_map[status],
                    instance=instance,
                    previous_status=old_status
                )
                logger.debug(
                    f"Triggered {status_event_map[status]} webhook for subscription {instance.pk}"
                )


# =============================================================================
# Payment Signals (if Payment model exists)
# =============================================================================

try:
    @receiver(post_save, sender='payment_providers.PaymentTransaction')
    def payment_post_save(sender, instance, created, **kwargs):
        """Trigger webhooks for payment events."""
        from .services import trigger_webhook

        if created:
            status = getattr(instance, 'status', '')
            if status == 'completed' or status == 'success':
                trigger_webhook('payment.received', instance=instance)
            elif status == 'failed':
                trigger_webhook('payment.failed', instance=instance)
            elif status == 'pending':
                trigger_webhook('payment.pending', instance=instance)
except Exception:
    # PaymentTransaction model may not exist
    pass


# =============================================================================
# Utility function to manually trigger webhooks
# =============================================================================

def trigger_manual_webhook(event_type: str, data: dict):
    """
    Manually trigger a webhook with custom data.

    This can be used for events that don't have model signals,
    or for testing purposes.

    Args:
        event_type: The webhook event type
        data: The payload data
    """
    from .services import trigger_webhook
    trigger_webhook(event_type, data=data)
