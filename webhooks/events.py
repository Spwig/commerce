"""
Webhook event types catalog.

This module defines all available webhook event types that can be
subscribed to by webhook endpoints.
"""
from django.utils.translation import gettext_lazy as _


class WebhookEventCategory:
    """Categories for grouping webhook events."""
    ORDER = 'order'
    PAYMENT = 'payment'
    SHIPMENT = 'shipment'
    INVENTORY = 'inventory'
    PRODUCT = 'product'
    CUSTOMER = 'customer'
    SUBSCRIPTION = 'subscription'
    CART = 'cart'
    REFUND = 'refund'
    TRANSLATION = 'translation'


# Webhook event definitions
# Format: event_type -> (description, category)
WEBHOOK_EVENTS = {
    # Order Events
    'order.created': (
        _('Fired when a new order is placed'),
        WebhookEventCategory.ORDER
    ),
    'order.paid': (
        _('Fired when payment for an order is confirmed'),
        WebhookEventCategory.ORDER
    ),
    'order.cancelled': (
        _('Fired when an order is cancelled'),
        WebhookEventCategory.ORDER
    ),
    'order.fulfilled': (
        _('Fired when all items in an order are shipped'),
        WebhookEventCategory.ORDER
    ),
    'order.partially_fulfilled': (
        _('Fired when some items in an order are shipped'),
        WebhookEventCategory.ORDER
    ),
    'order.status_changed': (
        _('Fired when order status changes'),
        WebhookEventCategory.ORDER
    ),
    'order.note_added': (
        _('Fired when a note is added to an order'),
        WebhookEventCategory.ORDER
    ),

    # Payment Events
    'payment.received': (
        _('Fired when a payment is received'),
        WebhookEventCategory.PAYMENT
    ),
    'payment.failed': (
        _('Fired when a payment attempt fails'),
        WebhookEventCategory.PAYMENT
    ),
    'payment.pending': (
        _('Fired when a payment is pending confirmation'),
        WebhookEventCategory.PAYMENT
    ),

    # Refund Events
    'refund.created': (
        _('Fired when a refund is initiated'),
        WebhookEventCategory.REFUND
    ),
    'refund.completed': (
        _('Fired when a refund is completed'),
        WebhookEventCategory.REFUND
    ),
    'refund.failed': (
        _('Fired when a refund fails'),
        WebhookEventCategory.REFUND
    ),

    # Shipment Events
    'shipment.created': (
        _('Fired when a shipment is created'),
        WebhookEventCategory.SHIPMENT
    ),
    'shipment.shipped': (
        _('Fired when a shipment is dispatched'),
        WebhookEventCategory.SHIPMENT
    ),
    'shipment.in_transit': (
        _('Fired when a shipment is in transit'),
        WebhookEventCategory.SHIPMENT
    ),
    'shipment.out_for_delivery': (
        _('Fired when a shipment is out for delivery'),
        WebhookEventCategory.SHIPMENT
    ),
    'shipment.delivered': (
        _('Fired when a shipment is delivered'),
        WebhookEventCategory.SHIPMENT
    ),
    'shipment.failed': (
        _('Fired when a shipment delivery fails'),
        WebhookEventCategory.SHIPMENT
    ),
    'shipment.returned': (
        _('Fired when a shipment is returned'),
        WebhookEventCategory.SHIPMENT
    ),
    'shipment.tracking_updated': (
        _('Fired when shipment tracking information is updated'),
        WebhookEventCategory.SHIPMENT
    ),

    # Inventory Events
    'inventory.low_stock': (
        _('Fired when product stock falls below threshold'),
        WebhookEventCategory.INVENTORY
    ),
    'inventory.out_of_stock': (
        _('Fired when a product goes out of stock'),
        WebhookEventCategory.INVENTORY
    ),
    'inventory.restocked': (
        _('Fired when a product is restocked'),
        WebhookEventCategory.INVENTORY
    ),
    'inventory.adjusted': (
        _('Fired when inventory is manually adjusted'),
        WebhookEventCategory.INVENTORY
    ),

    # Product Events
    'product.created': (
        _('Fired when a new product is created'),
        WebhookEventCategory.PRODUCT
    ),
    'product.updated': (
        _('Fired when product details are updated'),
        WebhookEventCategory.PRODUCT
    ),
    'product.deleted': (
        _('Fired when a product is deleted'),
        WebhookEventCategory.PRODUCT
    ),
    'product.published': (
        _('Fired when a product is published'),
        WebhookEventCategory.PRODUCT
    ),
    'product.unpublished': (
        _('Fired when a product is unpublished'),
        WebhookEventCategory.PRODUCT
    ),

    # Customer Events
    'customer.created': (
        _('Fired when a new customer registers'),
        WebhookEventCategory.CUSTOMER
    ),
    'customer.updated': (
        _('Fired when customer profile is updated'),
        WebhookEventCategory.CUSTOMER
    ),
    'customer.deleted': (
        _('Fired when a customer account is deleted'),
        WebhookEventCategory.CUSTOMER
    ),

    # Subscription Events
    'subscription.created': (
        _('Fired when a new subscription is created'),
        WebhookEventCategory.SUBSCRIPTION
    ),
    'subscription.activated': (
        _('Fired when a subscription is activated'),
        WebhookEventCategory.SUBSCRIPTION
    ),
    'subscription.renewed': (
        _('Fired when a subscription is renewed'),
        WebhookEventCategory.SUBSCRIPTION
    ),
    'subscription.cancelled': (
        _('Fired when a subscription is cancelled'),
        WebhookEventCategory.SUBSCRIPTION
    ),
    'subscription.expired': (
        _('Fired when a subscription expires'),
        WebhookEventCategory.SUBSCRIPTION
    ),
    'subscription.paused': (
        _('Fired when a subscription is paused'),
        WebhookEventCategory.SUBSCRIPTION
    ),
    'subscription.resumed': (
        _('Fired when a paused subscription is resumed'),
        WebhookEventCategory.SUBSCRIPTION
    ),
    'subscription.payment_failed': (
        _('Fired when a subscription payment fails'),
        WebhookEventCategory.SUBSCRIPTION
    ),

    # Cart Events
    'cart.abandoned': (
        _('Fired when a cart is abandoned (after configurable delay)'),
        WebhookEventCategory.CART
    ),
    'cart.recovered': (
        _('Fired when an abandoned cart is recovered'),
        WebhookEventCategory.CART
    ),

    # Translation Events
    'translation.job_completed': (
        _('Fired when a translation job completes successfully'),
        WebhookEventCategory.TRANSLATION
    ),
    'translation.job_failed': (
        _('Fired when a translation job fails'),
        WebhookEventCategory.TRANSLATION
    ),
}


def get_event_description(event_type: str) -> str:
    """Get the description for an event type."""
    event_info = WEBHOOK_EVENTS.get(event_type)
    if event_info:
        return str(event_info[0])
    return event_type


def get_event_category(event_type: str) -> str:
    """Get the category for an event type."""
    event_info = WEBHOOK_EVENTS.get(event_type)
    if event_info:
        return event_info[1]
    return event_type.split('.')[0] if '.' in event_type else 'unknown'


def get_events_by_category() -> dict:
    """Get all events grouped by category."""
    categorized = {}
    for event_type, (description, category) in WEBHOOK_EVENTS.items():
        if category not in categorized:
            categorized[category] = []
        categorized[category].append({
            'event': event_type,
            'description': str(description),
        })
    return categorized


def get_all_event_types() -> list:
    """Get a list of all available event types."""
    return list(WEBHOOK_EVENTS.keys())


def is_valid_event(event_type: str) -> bool:
    """Check if an event type is valid."""
    return event_type in WEBHOOK_EVENTS


def validate_events(event_types: list) -> tuple[list, list]:
    """
    Validate a list of event types.

    Returns:
        tuple: (valid_events, invalid_events)
    """
    valid = []
    invalid = []
    for event in event_types:
        if is_valid_event(event):
            valid.append(event)
        else:
            invalid.append(event)
    return valid, invalid
