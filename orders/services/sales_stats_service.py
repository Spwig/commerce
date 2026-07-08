import logging
from collections import defaultdict

from django.db import transaction
from django.db.models import F

logger = logging.getLogger(__name__)


def update_product_sales_counts(order):
    """
    Atomically increment Product.sales_count for each item in a paid order.

    Uses F() expressions for concurrent safety, only counts top-level items
    (excludes bundle components), and is idempotent via order.metadata flag
    protected by a row lock to prevent TOCTOU races.
    """
    # Skip test/sandbox orders
    if order.is_test_order:
        return

    from orders.models import Order

    with transaction.atomic():
        # Re-fetch with row lock to prevent concurrent double-counting
        order = Order.objects.select_for_update().get(pk=order.pk)

        if order.metadata and order.metadata.get('sales_count_updated'):
            logger.info(f"Sales counts already updated for order {order.order_number}")
            return

        # Aggregate quantities by product_id (handles same product in multiple line items)
        product_quantities = defaultdict(int)
        for item in order.items.filter(parent_bundle__isnull=True):
            product_quantities[item.product_id] += item.quantity

        if not product_quantities:
            return

        # Atomic F() update for each product
        from catalog.models import Product
        for product_id, quantity in product_quantities.items():
            Product.objects.filter(pk=product_id).update(
                sales_count=F('sales_count') + quantity
            )

        # Mark idempotency flag
        if order.metadata is None:
            order.metadata = {}
        order.metadata['sales_count_updated'] = True
        order.save(update_fields=['metadata'])

    logger.info(
        f"Updated sales counts for order {order.order_number}: "
        f"{len(product_quantities)} products, "
        f"{sum(product_quantities.values())} total units"
    )
