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
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from catalog.middleware import invalidate_region_cache
from catalog.models import DigitalAsset, LicenseKey, LicenseProvider, SalesRegion
from catalog.services.license_generator import LicenseKeyGenerator
from catalog.services.license_sync import LicenseProviderService
from catalog.services.webhook_dispatcher import LicenseWebhookDispatcher, LicenseWebhookEvents
from email_system.services.email_sender import EmailSendingService
from email_system.services.template_renderer import TemplateRenderer
from orders.models import Order, OrderItem

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=SalesRegion)
@receiver(post_delete, sender=SalesRegion)
def invalidate_region_cache_on_change(sender, **kwargs):
    """Drop cached SalesRegion lookups whenever a region changes.

    A priority bump, deactivation, or edit to a region's country list must take
    effect immediately: without this, visitors keep being routed to a stale
    region — and therefore its stock, availability, and currency — for up to the
    one-hour cache timeout.

    The bump is deferred to ``on_commit`` so it lands only after the write is
    visible. Bumping mid-transaction would let a concurrent reader see the new
    version, query the still-committed old priorities, and re-cache the former
    default under the new version for another full hour.
    """
    transaction.on_commit(invalidate_region_cache)


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

    # Find items needing license generation on payment. Exclude items that
    # already have a license key so this stays per-item idempotent: an order
    # mixing an on_order product (already keyed at creation) with an on_payment
    # product must still key the second item, and a re-save of an already-paid
    # order (e.g. an amount_paid write-back) becomes a no-op instead of
    # regenerating keys or re-sending the delivery email.
    from django.db.models import Q

    items_needing_license = (
        instance.items.filter(
            Q(product__requires_license=True, product__license_generation_trigger="on_payment")
            | Q(
                product__digital_assets__requires_license=True,
                product__digital_assets__is_active=True,
            )
        )
        .exclude(license_keys__isnull=False)
        .distinct()
    )

    if not items_needing_license.exists():
        logger.debug(f"Order {instance.order_number} has no items requiring license on payment")
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

    # Checkout and POS create the Order first and its OrderItem rows afterward,
    # all inside one transaction. At post_save time instance.items is still
    # empty, so the work is deferred to on_commit — by then the items are
    # committed and visible, and a rolled-back order never generates a key.
    def _process():
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

    transaction.on_commit(_process)


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
        # LicenseKey.is_lifetime defaults to True and short-circuits is_expired,
        # so a key with a calculated expiry must be marked non-lifetime or it
        # would never expire (is_valid stays True forever).
        is_lifetime=expires_at is None,
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
        # Re-raise so _process_order_licenses runs its delivery-failure path
        # (the "keys generated but email failed" OrderNote) instead of logging
        # the order as successfully processed and losing the recovery signal.
        raise


# ============================================================================
# Back-In-Stock Notification Signals
# ============================================================================

from catalog.models import StockItem, StockNotification


@receiver(pre_save, sender=StockItem)
def _cache_previous_availability(sender, instance, update_fields=None, **kwargs):
    """Stash the pre-save available quantity so post_save can detect a genuine
    out-of-stock -> in-stock transition, not fire on every save.

    Availability is ``on_hand - allocated``, so a transition can be caused by
    ``on_hand`` rising (restock) *or* ``allocated`` falling (a released/expired
    reservation). A save touching neither field cannot change availability
    (e.g. threshold or timestamp updates) and is short-circuited here — no query
    on those paths. ``_prev_available = None`` signals post_save to skip.
    """
    if update_fields is not None and not (
        "on_hand" in update_fields or "allocated" in update_fields
    ):
        instance._prev_available = None
        return
    if instance.pk:
        prev = StockItem.objects.filter(pk=instance.pk).values("on_hand", "allocated").first()
        instance._prev_available = max(0, prev["on_hand"] - prev["allocated"]) if prev else 0
    else:
        instance._prev_available = 0


@receiver(post_save, sender=StockItem)
def check_and_send_back_in_stock_notifications(
    sender, instance, created, update_fields=None, **kwargs
):
    """Dispatch back-in-stock notifications when a stock item crosses from zero
    to positive availability.

    The heavy work (finding subscribers, rendering, queuing email) runs in the
    ``catalog.send_back_in_stock_notifications`` Celery task, dispatched only on
    the 0 -> positive transition and only ``on_commit`` so a rolled-back stock
    change never emails anyone and the task never reads a row that isn't there.
    """
    prev_available = getattr(instance, "_prev_available", 0)
    if prev_available is None:  # save changed neither on_hand nor allocated
        return
    if prev_available > 0:
        # Item was already in stock, so this save cannot be a 0 -> positive
        # transition. Skip the second read/lookup — this is the hot allocation
        # path (add-to-cart) where availability only ever drops.
        return

    # Read the just-saved quantities from the DB: callers mutate on_hand/
    # allocated with F() expressions, so instance.available may hold an
    # unresolved expression at signal time. The committed row has real integers.
    row = StockItem.objects.filter(pk=instance.pk).values("on_hand", "allocated").first()
    if not row:
        return
    curr_available = max(0, row["on_hand"] - row["allocated"])
    if not (prev_available <= 0 < curr_available):
        return

    # Only pay for the subscriber lookup on a real transition.
    if not StockNotification.objects.filter(
        product_id=instance.product_id, notified_at__isnull=True
    ).exists():
        return

    stock_item_id = instance.pk

    def _dispatch():
        from catalog.tasks import send_back_in_stock_notifications

        send_back_in_stock_notifications.delay(stock_item_id)

    transaction.on_commit(_dispatch)


# Import models at module level to avoid issues


def _credit_captures_to_amount_paid(order, captures):
    """
    Add settled gift card value to ``Order.amount_paid``.

    Invariant I2: ``amount_paid == sum of settlement_amount`` over completed
    charge/capture rows. The gateway leg is assigned by
    ``PaymentOrchestrationService.handle_payment_success`` as
    ``amount_paid = intent.amount``, and that intent is now raised for
    ``amount_due`` — net of tenders — so without this the gift card leg is
    never credited and every split-tender order reads as permanently
    part-paid. That is not cosmetic: ``RefundService`` caps refunds at
    ``amount_paid``, so an under-stated figure silently blocks refunding money
    the customer actually handed over.

    Re-reads the row inside the update so a concurrent gateway write does not
    clobber the increment, and skips captures already reflected so a retried
    webhook cannot inflate the total.
    """
    from django.db import transaction as db_transaction

    from orders.models import Order as OrderModel

    amounts = [c.settlement_amount for c in captures if c.settlement_amount is not None]
    if not amounts:
        return
    # Money does not sum from an int zero, so fold instead of sum().
    settled = amounts[0]
    for extra in amounts[1:]:
        settled = settled + extra
    if settled.amount <= 0:
        return

    with db_transaction.atomic():
        fresh = OrderModel.objects.select_for_update().get(pk=order.pk)
        if fresh.amount_paid.currency != settled.currency:
            logger.error(
                f"Cannot credit {settled} to order {fresh.order_number}: "
                f"amount_paid is in {fresh.amount_paid.currency}. Left alone "
                f"rather than guessing a conversion — needs reconciliation."
            )
            return
        fresh.amount_paid = fresh.amount_paid + settled
        fresh.save(update_fields=["amount_paid", "updated_at"])
        order.amount_paid = fresh.amount_paid

    logger.info(
        f"Credited {settled} of gift card tender to order {order.order_number}; "
        f"amount_paid now {order.amount_paid}"
    )


@receiver(post_save, sender=Order)
def issue_gift_cards_on_payment_confirmed(sender, instance, created, **kwargs):
    """
    Mint and deliver the gift cards an order paid for, once payment is confirmed.

    Until P2.3 this never ran. ``GiftCardService.create_gift_cards_for_order``
    was reachable only from ``CheckoutService.process_payment_completion``,
    which had zero callers repo-wide — so a merchant could sell a gift card and
    the customer would receive nothing. That orphaned entry point is what the
    whole phase exists to fix, and it is why the test suite asserts this
    receiver is *registered*, not merely that the service works.

    **Deliberately no ``if created: return``.** The sibling receiver
    ``settle_tenders_on_payment_confirmed`` has that guard and is right to,
    but copying it here would silently break every in-store sale: POS builds
    the Order with ``payment_status="paid"`` inline
    (``pos_api/views/checkout.py``), so ``created`` is True on the only
    post_save it ever gets. A guard would mean the till takes the money and no
    card is ever minted — the exact failure this phase removes.

    Idempotency is NOT this receiver's job. It fires more than once per order by
    design (webhook retry, admin re-save, the settlement receiver's own
    ``amount_paid`` write-back), and the guarantee lives in a unique database
    constraint on ``(order_item, issue_index)``. The self-write filter below is
    an optimisation that keeps the constraint off the hot path, not the safety
    property.

    Deferred to ``on_commit`` so a rollback cannot leave a funded card — with
    its code already emailed — attached to an order that never existed.
    """
    if instance.payment_status != "paid":
        return

    # Skip our own and the settlement receiver's write-backs.
    update_fields = kwargs.get("update_fields")
    if update_fields and set(update_fields) <= {
        "amount_paid",
        "amount_paid_base",
        "updated_at",
        "paid_at",
    }:
        return

    order_pk = instance.pk

    def _issue():
        from catalog.tasks import issue_gift_cards_for_order

        # Dispatched by pk, never by instance: a pickled model in a Celery
        # message can be stale by the time a worker picks it up.
        try:
            issue_gift_cards_for_order.delay(order_pk)
        except Exception:
            # Broker unreachable. Do it inline rather than lose the issuance —
            # the customer has paid. The periodic reconcile task is the net if
            # even this fails.
            logger.exception(
                f"Could not queue gift card issuance for order {order_pk}; running inline"
            )
            from catalog.services.gift_card_service import GiftCardService
            from orders.models import Order as OrderModel

            try:
                GiftCardService.create_gift_cards_for_order(OrderModel.objects.get(pk=order_pk))
            except Exception:
                logger.exception(
                    f"Inline gift card issuance failed for order {order_pk} — "
                    f"customer paid and holds no card; needs reconciliation"
                )

    transaction.on_commit(_issue)


@receiver(post_save, sender=Order)
def settle_tenders_on_payment_confirmed(sender, instance, created, **kwargs):
    """
    Capture gift card holds once an order's payment is confirmed.

    Modelled on process_licenses_on_payment_confirmed above, which is the
    proven hook: it fires on ANY path that flips payment_status to "paid" —
    the orchestration service, the legacy webhook handler, capture, and POS —
    rather than only the gateway path that
    PaymentOrchestrationService._trigger_post_payment_flows covers.

    Three properties matter here, all of them about money:

    * **Idempotent.** GiftCardTenderService.capture_for_order skips any
      (order, card) pair that already has a capture row, so a retried webhook
      cannot debit a card twice.
    * **After commit.** Capture is deferred with transaction.on_commit, so a
      rollback later in the same transaction cannot leave cards debited for an
      order that never existed. The licences receiver above does NOT do this
      and has the same latent problem.
    * **Never rolls back a successful charge.** A capture failure is recorded
      and surfaced, but must not undo a gateway payment that already
      succeeded — the customer has been charged.

    KNOWN GAP: `orders/admin.py` "Mark as Paid" uses `queryset.update()`,
    which bypasses post_save entirely, so this does not fire for orders marked
    paid in bulk from the admin. That is fixed alongside this receiver.
    """
    if created:
        return

    if instance.payment_status != "paid":
        return

    # Ignore our own write-back. _credit_captures_to_amount_paid saves
    # amount_paid, which re-fires this receiver; without this the capture pass
    # would run again on every credit.
    update_fields = kwargs.get("update_fields")
    if update_fields and set(update_fields) <= {"amount_paid", "amount_paid_base", "updated_at"}:
        return

    def _capture():
        from catalog.services.gift_card_tender_service import GiftCardTenderService
        from payment_providers.models import PaymentTransaction
        from wallet.tender_service import WalletTenderService

        try:
            # Which capture rows already existed. capture_for_order is
            # idempotent and returns pre-existing rows alongside new ones, so
            # crediting its whole return value would re-add settled value every
            # time an order is re-saved as paid. Covers BOTH internal tenders.
            already = set(
                PaymentTransaction.objects.filter(
                    order=instance,
                    tender_type__in=PaymentTransaction.INTERNAL_TENDERS,
                    transaction_type="capture",
                ).values_list("pk", flat=True)
            )

            # Fixed, documented order: gift cards first, wallet second. Both
            # cap the debit at what the order still owes counting EVERY
            # completed capture and charge, so whichever runs second sees the
            # first's captures and cannot jointly over-capture a cart that
            # shrank between hold and payment.
            captures = list(GiftCardTenderService.capture_for_order(instance))
            captures += list(WalletTenderService.capture_for_order(instance))

            newly_settled = [c for c in captures if c.pk not in already]
            if newly_settled:
                _credit_captures_to_amount_paid(instance, newly_settled)
            if captures:
                logger.info(
                    f"Settled {len(captures)} internal tender(s) for order {instance.order_number}"
                )
        except Exception as e:
            # Deliberately swallowed at this boundary: the payment has already
            # succeeded, and raising here would roll back nothing useful while
            # breaking the request. Surface it loudly instead — an unsettled
            # hold means the customer's card was not debited for an order they
            # paid for, which needs a human.
            logger.exception(
                f"FAILED to settle gift card tenders for order "
                f"{instance.order_number}: {e}. The order is paid but one or "
                f"more gift cards were not debited — reconcile manually."
            )
            try:
                from orders.models import OrderNote

                OrderNote.objects.create(
                    order=instance,
                    note=(
                        f"Gift card tender settlement failed: {e}. "
                        f"Card(s) not debited — needs manual reconciliation."
                    ),
                    # Staff-facing, not shown to the customer.
                    is_customer_note=False,
                )
            except Exception:  # pragma: no cover - note is best-effort
                logger.exception("Could not record settlement failure as an OrderNote")

    transaction.on_commit(_capture)
