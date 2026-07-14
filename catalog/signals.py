"""
Digital Products Post-Purchase Automation Signals

Handles automatic license key generation and email delivery when orders
containing digital products are completed.
"""

import hashlib
import logging
import os

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from catalog.models import DigitalAsset, LicenseKey, LicenseProvider
from catalog.services.license_generator import LicenseKeyGenerator
from catalog.services.license_sync import LicenseProviderService
from catalog.services.webhook_dispatcher import LicenseWebhookDispatcher, LicenseWebhookEvents
from email_system.services.email_sender import EmailSendingService
from email_system.services.template_renderer import TemplateRenderer
from orders.models import Order, OrderItem

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def process_licenses_on_payment_confirmed(sender, instance, created, **kwargs):
    """
    Trigger license generation when payment is confirmed.

    This signal handler processes products configured with:
    - requires_license=True AND license_generation_trigger='on_payment'
    - Legacy: digital assets with requires_license=True

    Args:
        sender: Order model class
        instance: Order instance
        created: Boolean indicating if this is a new order
        **kwargs: Additional keyword arguments
    """
    # Skip newly created orders (payment won't be confirmed yet)
    if created:
        return

    # Only process when payment is confirmed (status = 'paid')
    if instance.payment_status != "paid":
        return

    # Find items needing license generation on payment
    from django.db.models import Q

    items_needing_license = instance.items.filter(
        Q(product__requires_license=True, product__license_generation_trigger="on_payment")
        | Q(product__digital_assets__requires_license=True, product__digital_assets__is_active=True)
    ).distinct()

    if not items_needing_license.exists():
        logger.debug(f"Order {instance.order_number} has no items requiring license on payment")
        return

    # Check if we've already processed licenses for this order
    existing_licenses = LicenseKey.objects.filter(order_item__order=instance).exists()

    if existing_licenses:
        logger.debug(f"Order {instance.order_number} already has license keys, skipping")
        return

    logger.info(f"Processing licenses (on_payment trigger) for order {instance.order_number}")
    _process_order_licenses(instance, items_needing_license)


@receiver(post_save, sender=Order)
def process_licenses_on_order_created(sender, instance, created, **kwargs):
    """
    Trigger license generation when order is created.

    This signal handler processes products configured with:
    - requires_license=True AND license_generation_trigger='on_order'

    Args:
        sender: Order model class
        instance: Order instance
        created: Boolean indicating if this is a new order
        **kwargs: Additional keyword arguments
    """
    # Only process newly created orders
    if not created:
        return

    # Find items needing license generation on order creation
    items_needing_license = instance.items.filter(
        product__requires_license=True, product__license_generation_trigger="on_order"
    ).distinct()

    if not items_needing_license.exists():
        logger.debug(
            f"Order {instance.order_number} has no items requiring license on order creation"
        )
        return

    logger.info(f"Processing licenses (on_order trigger) for order {instance.order_number}")
    _process_order_licenses(instance, items_needing_license)


def _process_order_licenses(instance, items_needing_license):
    """
    Common license processing logic for both triggers.

    Args:
        instance: Order instance
        items_needing_license: QuerySet of OrderItem objects needing licenses
    """
    # Import OrderNote for creating audit trail
    from orders.models import OrderNote

    licenses_generated = []
    license_errors = []

    # Step 1: Generate license keys (in transaction, separate from email)
    try:
        with transaction.atomic():
            for order_item in items_needing_license:
                try:
                    result = process_digital_product_order_item(order_item, instance)
                    if result:
                        licenses_generated.extend(result)
                except Exception as e:
                    license_errors.append(f"{order_item.product_name}: {str(e)}")
                    logger.error(f"Failed to generate license for {order_item.product_name}: {e}")

    except Exception as e:
        logger.error(
            f"Failed to process digital products for order {instance.order_number}: {e}",
            exc_info=True,
        )
        # Create error note on order
        try:
            OrderNote.objects.create(
                order=instance,
                author=None,
                note=f"⚠️ License generation failed: {str(e)}",
                is_customer_note=False,
            )
        except Exception:
            pass
        return

    # Step 2: Create success note for license generation
    if licenses_generated:
        try:
            license_summary = "\n".join(
                [f"• {lk.key} ({lk.order_item.product_name})" for lk in licenses_generated]
            )
            OrderNote.objects.create(
                order=instance,
                author=None,
                note=f"🔑 License keys generated:\n{license_summary}",
                is_customer_note=False,
            )
        except Exception as e:
            logger.error(f"Failed to create license note: {e}")

    # Log any partial errors
    if license_errors:
        try:
            OrderNote.objects.create(
                order=instance,
                author=None,
                note="⚠️ Some licenses could not be generated:\n" + "\n".join(license_errors),
                is_customer_note=False,
            )
        except Exception:
            pass

    # Step 3: Send delivery email (separate from license generation)
    try:
        send_digital_product_delivery_email(instance)
        logger.info(
            f"Successfully processed {len(licenses_generated)} digital products "
            f"for order {instance.order_number}"
        )
    except Exception as e:
        logger.error(
            f"Failed to send delivery email for order {instance.order_number}: {e}", exc_info=True
        )
        # Create note about email failure (licenses still generated)
        try:
            OrderNote.objects.create(
                order=instance,
                author=None,
                note=f"⚠️ License keys were generated but delivery email failed: {str(e)}\nPlease resend manually or contact customer.",
                is_customer_note=False,
            )
        except Exception:
            pass


def process_digital_product_order_item(order_item: OrderItem, order: Order) -> list:
    """
    Process a single order item for license generation.

    Supports two modes:
    1. Product-level licensing: Product.requires_license=True (no asset needed)
    2. Asset-level licensing: DigitalAsset.requires_license=True (legacy support)

    Args:
        order_item: OrderItem instance
        order: Parent Order instance

    Returns:
        List of generated LicenseKey objects
    """
    product = order_item.product
    generated_licenses = []

    # Mode 1: Product-level licensing (license-only products, no asset required)
    if product.requires_license:
        # Check if product-level license already exists for this order item
        existing_product_license = LicenseKey.objects.filter(
            order_item=order_item,
            digital_asset__isnull=True,  # Product-level license has no asset
        ).first()

        if existing_product_license:
            logger.debug(
                f"Product-level license already exists for {product.name} "
                f"in order {order.order_number}"
            )
        else:
            # Generate product-level license (asset=None)
            license_key = generate_license_key(order, order_item, asset=None)
            generated_licenses.append(license_key)

            logger.info(
                f"Generated product-level license {license_key.key} for "
                f"{product.name} in order {order.order_number}"
            )

    # Mode 2: Asset-level licensing (legacy - digital assets with requires_license)
    digital_assets = DigitalAsset.objects.filter(
        product=product, is_active=True, requires_license=True
    )

    for asset in digital_assets:
        # Check if license already exists for this order item + asset
        existing_license = LicenseKey.objects.filter(
            order_item=order_item, digital_asset=asset
        ).first()

        if existing_license:
            logger.debug(
                f"License key already exists for asset {asset.id} in order {order.order_number}"
            )
            continue

        # Generate asset-level license
        license_key = generate_license_key(order, order_item, asset)
        generated_licenses.append(license_key)

        logger.info(
            f"Generated asset-level license {license_key.key} for "
            f"asset {asset.filename} in order {order.order_number}"
        )

    return generated_licenses


def generate_license_key(
    order: Order, order_item: OrderItem, asset: DigitalAsset = None
) -> LicenseKey:
    """
    Generate a unique license key using custom template or default format.

    Supports two modes:
    1. Product-level license: asset=None, uses product settings
    2. Asset-level license: asset provided (legacy support)

    If the product has a license_template configured, uses that template.
    Otherwise, uses default format: XXXX-XXXX-XXXX-XXXX (16 characters, grouped in 4s)

    Args:
        order: Order instance
        order_item: OrderItem instance
        asset: DigitalAsset instance or None for product-level license

    Returns:
        LicenseKey: Created license key instance
    """
    product = order_item.product

    # Get template from product (or None for default)
    template = product.license_template

    # Prepare context for template placeholders
    context = {
        "order_id": order.id,
        "product_sku": product.sku or "",
    }

    # Generate key using template or default format
    generator = LicenseKeyGenerator()
    try:
        formatted_key = generator.generate(template, context)
    except Exception as e:
        logger.error(f"Failed to generate license key with template: {e}")
        # Fall back to old method - handle asset=None
        asset_id = asset.id if asset else 0
        unique_string = f"{order.id}-{product.id}-{asset_id}-{os.urandom(16).hex()}"
        hash_digest = hashlib.sha256(unique_string.encode()).hexdigest()[:16].upper()
        formatted_key = "-".join([hash_digest[i : i + 4] for i in range(0, 16, 4)])

    # Use product-level settings if available, otherwise defaults
    key_type = product.default_license_type or "perpetual"
    max_activations = (
        product.default_max_activations if product.default_max_activations is not None else 5
    )

    # Calculate expiry date if validity days is set
    expires_at = None
    if product.default_validity_days:
        expires_at = timezone.now() + timezone.timedelta(days=product.default_validity_days)

    # Create license key
    license_key = LicenseKey.objects.create(
        order_item=order_item,
        digital_asset=asset,  # Can be None for product-level licenses
        user=order.user,
        key=formatted_key,
        key_type=key_type,
        max_activations=max_activations,
        current_activations=0,
        status="active",
        expires_at=expires_at,
    )

    # Sync to product's configured provider (preferred) or fall back to global providers
    try:
        if product.license_provider and product.license_provider.is_active:
            # Product has a specific provider configured
            sync_service = LicenseProviderService(product.license_provider)
            sync_service.create_license(license_key, product, order)
            logger.info(
                f"Synced license {license_key.key} to product provider {product.license_provider.name}"
            )
        else:
            # Fall back to global providers with product mapping
            active_providers = LicenseProvider.objects.filter(is_active=True, sync_on_order=True)

            for provider in active_providers:
                # Check if this product is mapped to this provider
                product_id_str = str(product.id)
                if provider.product_mapping and product_id_str not in provider.product_mapping:
                    continue  # Skip if product not mapped to this provider

                # Sync license to provider
                sync_service = LicenseProviderService(provider)
                sync_service.create_license(license_key, product, order)
                logger.info(f"Synced license {license_key.key} to provider {provider.name}")

    except Exception as e:
        logger.exception(f"Error syncing license to external providers: {e}")
        # Don't fail license generation if external sync fails

    # Dispatch webhook events
    try:
        LicenseWebhookDispatcher.dispatch(
            LicenseWebhookEvents.LICENSE_GENERATED,
            license_key,
            data={
                "order_number": order.order_number,
                "product_name": product.name,
            },
        )
    except Exception as e:
        logger.exception(f"Error dispatching license webhook: {e}")
        # Don't fail license generation if webhook fails

    return license_key


def send_digital_product_delivery_email(order: Order):
    """
    Send delivery email with download links and license keys.

    Handles:
    - Products with licenses only (no downloadable assets)
    - Products with downloadable assets only (no license)
    - Products with both licenses and downloadable assets

    Args:
        order: Order instance containing digital products or licenses
    """
    try:
        # Prepare email context
        digital_items = []

        # Get items that have licenses OR digital assets
        from django.db.models import Q

        relevant_items = order.items.filter(
            Q(product__requires_license=True) | Q(product__is_digital=True)
        ).distinct()

        for order_item in relevant_items:
            product = order_item.product

            # Get digital assets (downloadable files)
            assets = DigitalAsset.objects.filter(product=product, is_active=True)

            # Get ALL license keys for this order item (product-level and asset-level)
            license_keys = LicenseKey.objects.filter(order_item=order_item)

            digital_items.append(
                {
                    "product_name": order_item.product_name,
                    "quantity": order_item.quantity,
                    "assets": [
                        {
                            "filename": asset.filename,
                            "version": asset.version,
                            "size": asset.get_file_size_display(),
                            "download_limit": asset.download_limit,
                            "expiration_days": asset.expiration_days,
                        }
                        for asset in assets
                    ],
                    "license_keys": [
                        {
                            "key": key.key,
                            "type": key.key_type,
                            "max_activations": key.max_activations,
                        }
                        for key in license_keys
                    ],
                }
            )

        context = {
            "customer_name": order.user.get_full_name() or order.user.email,
            "order_number": order.order_number,
            "order_date": order.created_at,
            "digital_items": digital_items,
            "account_url": "/account/digital-products/",  # Customer dashboard URL
        }

        # Render email template
        renderer = TemplateRenderer()

        # Get language preference from order or user settings
        from email_system.utils.language import get_order_email_language

        language = get_order_email_language(order)

        subject, html_body, plain_text_body = renderer.render(
            template_type="digital_product_delivery",
            context=context,
            language=language,
            enable_tracking=True,
        )

        # Queue email for sending
        EmailSendingService.queue_email(
            to_email=order.email,
            subject=subject,
            html_body=html_body,
            text_body=plain_text_body,
            template_type="digital_product_delivery",
        )

        logger.info(
            f"Queued digital product delivery email to {order.email} for order {order.order_number}"
        )

    except Exception as e:
        logger.error(
            f"Failed to queue digital product delivery email for order {order.order_number}: {e}",
            exc_info=True,
        )


# ============================================================================
# Back-In-Stock Notification Signals
# ============================================================================

from catalog.models import StockItem, StockNotification


@receiver(post_save, sender=StockItem)
def check_and_send_back_in_stock_notifications(sender, instance, created, **kwargs):
    """
    Check if a product has come back in stock and send notifications to subscribers.

    This signal is triggered when StockItem is updated (e.g., stock added).
    It checks if the product now has available stock and sends notifications
    to users who subscribed via the "Notify Me" feature.

    Args:
        sender: StockItem model class
        instance: StockItem instance that was saved
        created: Boolean indicating if this is a new stock item
        **kwargs: Additional keyword arguments
    """
    # Skip if no stock available
    if instance.available <= 0:
        return

    # Get pending notifications for this product and variant
    pending_notifications = StockNotification.objects.filter(
        product=instance.product,
        notified_at__isnull=True,  # Not yet notified
    )

    # Filter by variant if applicable
    if instance.variant:
        pending_notifications = pending_notifications.filter(variant=instance.variant)
    else:
        # For base product stock, notify subscribers without variant
        pending_notifications = pending_notifications.filter(variant__isnull=True)

    # Filter by warehouse preference if set
    pending_notifications = pending_notifications.filter(
        models.Q(preferred_warehouse__isnull=True)
        | models.Q(preferred_warehouse=instance.warehouse)
    )

    if not pending_notifications.exists():
        return

    logger.info(
        f"Sending back-in-stock notifications for {instance.product.name}: "
        f"{pending_notifications.count()} subscribers"
    )

    for notification in pending_notifications:
        try:
            send_back_in_stock_email(notification, instance)
            notification.notified_at = timezone.now()
            notification.save(update_fields=["notified_at"])
            logger.info(f"Sent back-in-stock notification to {notification.email}")
        except Exception as e:
            logger.error(
                f"Failed to send back-in-stock notification to {notification.email}: {e}",
                exc_info=True,
            )


def send_back_in_stock_email(notification: StockNotification, stock_item: StockItem):
    """
    Send a back-in-stock email notification to a subscriber.

    Args:
        notification: StockNotification instance
        stock_item: StockItem that has come back in stock
    """
    from django.urls import reverse

    product = notification.product
    variant = notification.variant

    # Build product URL
    product_url = reverse("page_builder:product_detail", kwargs={"product_slug": product.slug})

    # Get product image
    image_url = None
    if hasattr(product, "primary_image_url"):
        image_url = product.primary_image_url
    elif variant and variant.image_asset:
        image_url = variant.image_asset.get_display_url()

    # Prepare context
    context = {
        "product_name": product.name,
        "variant_name": variant.name if variant else None,
        "product_url": product_url,
        "product_image_url": image_url,
        "subscriber_email": notification.email,
    }

    try:
        # Render email template
        renderer = TemplateRenderer()
        from core.translation_utils import get_primary_language

        subject, html_body, plain_text_body = renderer.render(
            template_type="back_in_stock",
            context=context,
            language=get_primary_language(),
            enable_tracking=True,
        )

        # Queue email for sending
        EmailSendingService.queue_email(
            to_email=notification.email,
            subject=subject,
            html_body=html_body,
            text_body=plain_text_body,
            template_type="back_in_stock",
        )

    except Exception as e:
        logger.error(
            f"Failed to render/queue back-in-stock email for {notification.email}: {e}",
            exc_info=True,
        )
        raise  # Re-raise to be caught by the caller


# Import models at module level to avoid issues
from django.db import models
