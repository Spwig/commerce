"""
Django signal handlers for triggering webhooks.

This module connects Django model signals to the webhook system,
automatically triggering webhooks when relevant events occur.
"""

import logging

from django.apps import apps
from django.db.models.signals import post_delete, post_save, pre_save
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
    _previous_states[key] = {field: getattr(instance, field, None) for field in fields}


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
# Model classes (senders)
# =============================================================================
# Django's signal dispatcher matches senders by object identity, not by label:
# a string like "orders.Order" is never resolved, so a receiver connected with
# one silently never fires. Resolve the real model classes here (the module is
# imported from WebhooksConfig.ready(), so the app registry is populated) and
# connect every receiver below against the class.
Order = apps.get_model("orders", "Order")
Product = apps.get_model("catalog", "Product")
StockItem = apps.get_model("catalog", "StockItem")
CustomerProfile = apps.get_model("accounts", "CustomerProfile")
Shipment = apps.get_model("shipping", "Shipment")
CustomerSubscription = apps.get_model("subscriptions", "CustomerSubscription")


# =============================================================================
# Order Signals
# =============================================================================


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    """Store order state before save for change detection."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _store_previous_state(old_instance, ["status"])
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for order events."""
    from .services import trigger_webhook

    if created:
        trigger_webhook("order.created", instance=instance)
        logger.debug(f"Triggered order.created webhook for order {instance.order_number}")
    else:
        previous_state = _get_previous_state(instance)
        if _has_field_changed(instance, "status", previous_state):
            old_status = previous_state.get("status") if previous_state else None

            # Trigger specific status events
            if instance.status == "shipped":
                trigger_webhook("order.fulfilled", instance=instance, previous_status=old_status)
            elif instance.status == "cancelled":
                trigger_webhook("order.cancelled", instance=instance, previous_status=old_status)
            elif instance.status == "refunded":
                trigger_webhook("order.refunded", instance=instance, previous_status=old_status)

            # Always trigger the generic status change event
            trigger_webhook(
                "order.status_changed",
                instance=instance,
                previous_status=old_status,
                new_status=instance.status,
            )
            logger.debug(
                f"Triggered order.status_changed webhook for order {instance.order_number} "
                f"({old_status} -> {instance.status})"
            )


# =============================================================================
# Product Signals
# =============================================================================


@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    """Store product state before save for change detection."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _store_previous_state(old_instance, ["status"])
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for product events."""
    from .services import trigger_webhook

    if created:
        trigger_webhook("product.created", instance=instance)
        logger.debug(f"Triggered product.created webhook for product {instance.pk}")
    else:
        previous_state = _get_previous_state(instance)

        # Publication is driven by the stored `status` field (draft/published/
        # discontinued), not by `is_active` (a read-only property) or a
        # nonexistent stock field. Stock transitions live on StockItem below.
        if previous_state:
            old_status = previous_state.get("status")
            new_status = getattr(instance, "status", None)

            if old_status != "published" and new_status == "published":
                trigger_webhook("product.published", instance=instance)
            elif old_status == "published" and new_status != "published":
                trigger_webhook("product.unpublished", instance=instance)

        # Always trigger product.updated for non-created saves
        trigger_webhook("product.updated", instance=instance)


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    """Trigger webhook when a product is deleted."""
    from .services import trigger_webhook

    trigger_webhook(
        "product.deleted",
        data={
            "id": instance.pk,
            "sku": getattr(instance, "sku", ""),
            "name": str(instance),
        },
    )
    logger.debug(f"Triggered product.deleted webhook for product {instance.pk}")


# =============================================================================
# Inventory Signals
# =============================================================================
# Stock is owned by StockItem, not Product (Product has no stock field — its
# `total_stock` property aggregates on_hand across warehouses). Out-of-stock and
# restock transitions must therefore be detected on StockItem saves.


@receiver(pre_save, sender=StockItem)
def stock_item_pre_save(sender, instance, **kwargs):
    """Store a product's total stock before a stock change for transition detection."""
    product = instance.product
    if product is not None:
        _previous_states[f"stock:{product.pk}"] = {"total_stock": product.total_stock}


@receiver(post_save, sender=StockItem)
def stock_item_post_save(sender, instance, created, **kwargs):
    """Trigger inventory webhooks when a product's total stock crosses zero."""
    from .services import trigger_webhook

    product = instance.product
    if product is None:
        return

    previous_state = _previous_states.pop(f"stock:{product.pk}", None)
    old_stock = (previous_state or {}).get("total_stock", 0) or 0
    new_stock = product.total_stock or 0

    if old_stock == new_stock:
        return

    payload = {
        "product_id": product.pk,
        "product_sku": getattr(product, "sku", ""),
        "product_name": str(product),
        "previous_stock": old_stock,
        "current_stock": new_stock,
    }

    if old_stock > 0 and new_stock == 0:
        trigger_webhook("inventory.out_of_stock", data=payload)
    elif old_stock == 0 and new_stock > 0:
        trigger_webhook("inventory.restocked", data=payload)


# =============================================================================
# Customer Signals
# =============================================================================


@receiver(post_save, sender=CustomerProfile)
def customer_profile_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for customer profile events."""
    from .services import trigger_webhook

    # Only trigger for non-staff users (actual customers)
    user = getattr(instance, "user", None)
    if user and getattr(user, "is_staff", False):
        return

    if created:
        trigger_webhook("customer.created", instance=instance)
        logger.debug(f"Triggered customer.created webhook for customer {instance.pk}")
    else:
        trigger_webhook("customer.updated", instance=instance)


# =============================================================================
# Shipment Signals
# =============================================================================


@receiver(pre_save, sender=Shipment)
def shipment_pre_save(sender, instance, **kwargs):
    """Store shipment state before save for change detection."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _store_previous_state(old_instance, ["status"])
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender=Shipment)
def shipment_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for shipment events."""
    from .services import trigger_webhook

    if created:
        trigger_webhook("shipment.created", instance=instance)
        logger.debug(f"Triggered shipment.created webhook for shipment {instance.pk}")
    else:
        previous_state = _get_previous_state(instance)
        if _has_field_changed(instance, "status", previous_state):
            old_status = previous_state.get("status") if previous_state else None

            # Map shipment status to webhook events. Keys must match
            # Shipment.STATUS_CHOICES: "labeled" is the point a package is
            # dispatched, and "exception" is the delivery-failure status
            # (there is no "shipped"/"failed" status on the model).
            status = getattr(instance, "status", "")
            status_event_map = {
                "labeled": "shipment.shipped",
                "in_transit": "shipment.in_transit",
                "out_for_delivery": "shipment.out_for_delivery",
                "delivered": "shipment.delivered",
                "exception": "shipment.failed",
                "returned": "shipment.returned",
            }

            if status in status_event_map:
                trigger_webhook(
                    status_event_map[status], instance=instance, previous_status=old_status
                )
                logger.debug(
                    f"Triggered {status_event_map[status]} webhook for shipment {instance.pk}"
                )

            # Always trigger tracking update
            trigger_webhook(
                "shipment.tracking_updated",
                instance=instance,
                previous_status=old_status,
                new_status=status,
            )


# =============================================================================
# Subscription Signals
# =============================================================================


@receiver(pre_save, sender=CustomerSubscription)
def subscription_pre_save(sender, instance, **kwargs):
    """Store subscription state before save for change detection."""
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            _store_previous_state(old_instance, ["status"])
        except sender.DoesNotExist:
            pass


@receiver(post_save, sender=CustomerSubscription)
def subscription_post_save(sender, instance, created, **kwargs):
    """Trigger webhooks for subscription events."""
    from .services import trigger_webhook

    if created:
        trigger_webhook("subscription.created", instance=instance)
        logger.debug(f"Triggered subscription.created webhook for subscription {instance.pk}")
    else:
        previous_state = _get_previous_state(instance)
        if _has_field_changed(instance, "status", previous_state):
            old_status = previous_state.get("status") if previous_state else None
            status = getattr(instance, "status", "")

            # Map subscription status to webhook events. CustomerSubscription
            # stores the cancellation status as "canceled" (single "l").
            status_event_map = {
                "active": "subscription.activated",
                "canceled": "subscription.cancelled",
                "expired": "subscription.expired",
                "paused": "subscription.paused",
            }

            if status in status_event_map:
                trigger_webhook(
                    status_event_map[status], instance=instance, previous_status=old_status
                )
                logger.debug(
                    f"Triggered {status_event_map[status]} webhook for subscription {instance.pk}"
                )


# =============================================================================
# Payment Signals (if Payment model exists)
# =============================================================================

try:
    PaymentTransaction = apps.get_model("payment_providers", "PaymentTransaction")

    PAYMENT_STATUS_EVENT_MAP = {
        "completed": "payment.received",
        "failed": "payment.failed",
        "pending": "payment.pending",
    }

    @receiver(pre_save, sender=PaymentTransaction)
    def payment_pre_save(sender, instance, **kwargs):
        """Store payment status before save for change detection."""
        if instance.pk:
            try:
                old_instance = sender.objects.get(pk=instance.pk)
                _store_previous_state(old_instance, ["status"])
            except sender.DoesNotExist:
                pass

    @receiver(post_save, sender=PaymentTransaction)
    def payment_post_save(sender, instance, created, **kwargs):
        """Trigger webhooks for payment events on creation and status changes."""
        from .services import trigger_webhook

        # A transaction is often created as "pending" and later settled or
        # failed, so react on the initial save and on any later status change.
        if created:
            changed = True
        else:
            previous_state = _get_previous_state(instance)
            changed = _has_field_changed(instance, "status", previous_state)

        if not changed:
            return

        event = PAYMENT_STATUS_EVENT_MAP.get(getattr(instance, "status", ""))
        if event:
            trigger_webhook(event, instance=instance)
except LookupError:
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
