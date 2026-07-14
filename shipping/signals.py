"""
Django signals for shipping app
Handles bidirectional sync between Order and Shipment models
"""

import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver

from core.utils import get_shipping_origin_country

logger = logging.getLogger(__name__)

# ============================================================================
# Custom Signals (for future use)
# ============================================================================

# Define custom signals for shipping events
shipment_created = Signal()  # Args: shipment
label_purchased = Signal()  # Args: shipment
tracking_updated = Signal()  # Args: shipment, events
shipment_delivered = Signal()  # Args: shipment
shipment_exception = Signal()  # Args: shipment, error


# ============================================================================
# Signal Receivers - Order/Shipment Sync
# ============================================================================


@receiver(post_save, sender="shipping.Shipment")
def sync_tracking_to_order(sender, instance, created, **kwargs):
    """
    When Shipment.tracking_id changes, update Order.tracking_number
    This allows tracking numbers entered in shipments to appear in orders

    Guards against infinite loops by using update() instead of save()
    """
    if instance.tracking_id and instance.order:
        # Only update if tracking number actually changed
        if instance.order.tracking_number != instance.tracking_id:
            # Use update() to avoid triggering signals
            from orders.models import Order

            Order.objects.filter(pk=instance.order.pk).update(tracking_number=instance.tracking_id)
            logger.info(
                f"Synced tracking {instance.tracking_id} from Shipment {instance.pk} "
                f"to Order {instance.order.order_number}"
            )


@receiver(pre_save, sender="orders.Order")
def sync_tracking_from_order(sender, instance, **kwargs):
    """
    When Order.tracking_number changes manually (e.g., in admin),
    create or update a Shipment record

    This allows backward compatibility with existing Order.tracking_number field
    """
    # Skip if this is a new order
    if not instance.pk:
        return

    # Get the old instance to compare
    try:
        from orders.models import Order

        old_instance = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    # Check if tracking_number changed
    if old_instance.tracking_number == instance.tracking_number:
        return

    # If tracking number was cleared, don't create shipment
    if not instance.tracking_number:
        return

    # Import here to avoid circular imports
    from shipping.models import CarrierPreset, Shipment

    # Check if a shipment already exists for this order
    existing_shipment = Shipment.objects.filter(order=instance).order_by("-created_at").first()

    if existing_shipment:
        # Update existing shipment if tracking_id doesn't match
        if existing_shipment.tracking_id != instance.tracking_number:
            existing_shipment.tracking_id = instance.tracking_number
            # Use update_fields to avoid triggering signals unnecessarily
            existing_shipment.save(update_fields=["tracking_id", "updated_at"])
            logger.info(
                f"Updated Shipment {existing_shipment.pk} tracking to {instance.tracking_number} "
                f"from Order {instance.order_number}"
            )
    else:
        # Create new shipment with default carrier
        default_carrier = CarrierPreset.objects.filter(is_default=True, is_active=True).first()

        # If no default carrier, get the first active carrier
        if not default_carrier:
            default_carrier = CarrierPreset.objects.filter(is_active=True).first()

        if default_carrier:
            # Create shipment
            shipment = Shipment.objects.create(
                order=instance,
                user=instance.user if instance.user else None,
                carrier_preset=default_carrier,
                origin_country=get_shipping_origin_country(),
                dest_country=instance.shipping_country,
                tracking_id=instance.tracking_number,
                status="in_transit",  # Assume in transit if tracking added
            )
            logger.info(
                f"Created Shipment {shipment.pk} with tracking {instance.tracking_number} "
                f"from Order {instance.order_number} using carrier {default_carrier.name}"
            )
        else:
            logger.warning(
                f"Cannot create shipment for Order {instance.order_number}: "
                f"No active carriers available"
            )


# ============================================================================
# Custom Signal Handlers (for future use)
# ============================================================================


@receiver(shipment_created)
def log_shipment_created(sender, shipment, **kwargs):
    """Log when a new shipment is created"""
    logger.info(f"Shipment created: {shipment}")


@receiver(label_purchased)
def update_order_status_on_label(sender, shipment, **kwargs):
    """
    When label is purchased:
    1. Update Order status to 'shipped'
    2. Fulfill stock (reduce on_hand and allocated at warehouse)
    """
    if shipment.order and shipment.order.status != "shipped":
        from catalog.services import fulfillment_service
        from orders.models import Order

        # Update order status
        Order.objects.filter(pk=shipment.order.pk).update(status="shipped")
        logger.info(f"Updated Order {shipment.order.order_number} status to 'shipped'")

        # Fulfill stock for all order items
        order = shipment.order
        for order_item in order.items.all():
            # Only fulfill if stock was allocated and not yet fulfilled
            if (
                order_item.stock_allocated
                and not order_item.stock_fulfilled
                and order_item.warehouse
            ):
                try:
                    fulfillment_service.fulfill_stock(
                        order_item=order_item, warehouse=order_item.warehouse
                    )
                    # Mark as fulfilled
                    order_item.stock_fulfilled = True
                    order_item.save(update_fields=["stock_fulfilled"])
                    logger.info(
                        f"Fulfilled stock for {order_item.sku} at {order_item.warehouse.code} "
                        f"(Order: {order.order_number})"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to fulfill stock for {order_item.sku} at {order_item.warehouse.code}: {e}"
                    )
                    # Log error but don't block shipping - this can be resolved later
            elif not order_item.warehouse:
                logger.warning(
                    f"Order item {order_item.id} has no warehouse assigned - skipping stock fulfillment"
                )


@receiver(tracking_updated)
def log_tracking_updated(sender, shipment, events=None, **kwargs):
    """Log tracking updates"""
    event_count = len(events) if events else 0
    logger.info(f"Tracking updated for Shipment {shipment.pk}: {event_count} events")


@receiver(shipment_delivered)
def update_order_status_on_delivery(sender, shipment, **kwargs):
    """When shipment is delivered, update Order status to 'completed'"""
    if shipment.order and shipment.order.status != "completed":
        from orders.models import Order

        Order.objects.filter(pk=shipment.order.pk).update(status="completed")
        logger.info(f"Updated Order {shipment.order.order_number} status to 'completed'")


@receiver(shipment_exception)
def log_shipment_exception(sender, shipment, error=None, **kwargs):
    """Log shipment exceptions"""
    logger.warning(f"Shipment exception for {shipment.pk}: {error}")


# ============================================================================
# Carrier URL Feedback System
# ============================================================================


@receiver(post_save, sender="shipping.CarrierPreset")
def report_carrier_url_change(sender, instance, created, **kwargs):
    """
    Report URL override changes to update server for crowdsourced improvements.

    Only triggers for:
    - System carriers (is_system=True)
    - When override field has a value
    - Non-blocking (failures logged but don't prevent save)
    """

    # Only for system carriers with overrides
    if not instance.is_system or not instance.tracking_url_template_override:
        return

    # Skip if this is initial creation with no override
    if created and not instance.tracking_url_template_override:
        return

    try:
        # Import here to avoid circular dependencies
        import requests
        from django.utils import timezone

        try:
            from component_updates.utils import get_jwt_token, get_update_server_url
        except ImportError:
            logger.warning(
                f"component_updates not installed - skipping carrier URL feedback for {instance.slug}"
            )
            return

        feedback_data = {
            "carrier_slug": instance.slug,
            "carrier_name": instance.name,
            "country_code": instance.country_of_operation.code
            if instance.country_of_operation
            else "",
            "original_url": instance.tracking_url_template,
            "suggested_url": instance.tracking_url_template_override,
            "timestamp": timezone.now().isoformat(),
        }

        response = requests.post(
            f"{get_update_server_url()}/api/v1/feedback/carrier-url/",
            json=feedback_data,
            headers={
                "Authorization": f"Bearer {get_jwt_token()}",
                "Content-Type": "application/json",
            },
            timeout=5,  # Quick timeout to not block saves
        )

        if response.status_code == 201:
            logger.info(
                f"Carrier URL feedback sent successfully: {instance.slug} "
                f"({instance.tracking_url_template} → {instance.tracking_url_template_override})"
            )
        else:
            logger.warning(
                f"Failed to send carrier URL feedback: HTTP {response.status_code} "
                f"for {instance.slug}"
            )

    except requests.exceptions.Timeout:
        logger.warning(f"Timeout sending carrier URL feedback for {instance.slug}")
    except requests.exceptions.ConnectionError:
        logger.warning(f"Connection error sending carrier URL feedback for {instance.slug}")
    except Exception as e:
        logger.error(f"Error sending carrier URL feedback for {instance.slug}: {e}")
        # Don't raise - feedback is non-critical, shouldn't block saves


# ============================================================================
# Signal Receivers - Shipping Zone ↔ Shipping Country reconciliation
# ============================================================================


@receiver(post_save, sender="shipping.ShippingZone")
def reconcile_shipping_countries_from_zone(sender, instance, **kwargs):
    """
    Auto-create / reactivate ShippingCountry rows for every country a
    shipping zone explicitly lists, so merchants never have to touch the
    ShippingCountry admin directly.

    Why this exists: PaymentMethodFilter.get_available_providers_for_checkout
    silently filters every payment provider out if there's no
    ShippingCountry row matching the customer's country. Without this
    signal, merchants who set up shipping zones (the obvious "where do we
    ship?" UI) still see no payment options at checkout because the
    ShippingCountry table — a second, unsurfaced admin page — is empty.

    Intentional non-behaviours:
      * Empty `instance.countries` ("ships everywhere") is a no-op. We
        don't want to materialise 240 rows just because nothing is set.
      * Removing a country from a zone does NOT auto-deactivate the
        matching ShippingCountry row. The same country may be in another
        active zone, referenced by warehouse fallback, or carrying
        merchant-customised settings (e.g. source_warehouse). Silently
        flipping `is_active=False` here could brick checkout for real
        customers without warning. The merchant can deactivate manually
        from /admin/shipping/shippingcountry/ if they truly mean to stop
        shipping there.
    """
    # Avoid the late-import dance on every signal fire; the apps registry
    # is up by the time post_save fires.
    from shipping.models import ShippingCountry

    raw_codes = instance.countries or []
    codes: list[str] = []
    seen: set[str] = set()
    for raw in raw_codes:
        if not isinstance(raw, str):
            continue
        code = raw.strip().upper()
        if not code or code in seen:
            continue
        seen.add(code)
        codes.append(code)

    if not codes:
        return

    # Single-tenant assumption matches PaymentMethodFilter (site_id=1).
    # ShippingZone has no `site` FK today; if that ever changes we fall
    # back to 1 here.
    site_id = getattr(instance, "site_id", None) or 1

    for code in codes:
        country, created = ShippingCountry.objects.get_or_create(
            site_id=site_id,
            country_code=code,
            defaults={"is_active": True},
        )
        if not created and not country.is_active:
            country.is_active = True
            country.save(update_fields=["is_active", "updated_at"])
            logger.info(
                "ShippingCountry %s reactivated by ShippingZone %s save",
                code,
                instance.pk,
            )
