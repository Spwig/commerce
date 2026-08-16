from django.db.models import Q

from catalog.models import ProductDependency


def check_hard_dependencies(product, user, cart=None):
    """
    Check all 'requires'-type dependencies for a product.

    Returns:
        (True, []) if all satisfied.
        (False, [blocking_deps]) if any are unmet.
    """
    hard_deps = list(
        ProductDependency.objects.filter(
            product=product,
            dependency_type="requires",
        ).select_related("required_product")
    )
    if not hard_deps:
        return True, []

    authenticated = bool(user and user.is_authenticated)

    blocking = []
    for dep in hard_deps:
        owned = _user_owns_product(user, dep.required_product_id) if authenticated else False
        in_cart = _product_in_cart(cart, dep.required_product_id) if cart else False
        if not owned and not in_cart:
            blocking.append(dep)

    if blocking:
        return False, blocking
    return True, []


def get_recommendations(product):
    """Return all 'recommends'-type dependencies (display-only)."""
    return list(
        ProductDependency.objects.filter(
            product=product,
            dependency_type="recommends",
        )
        .select_related("required_product")
        .order_by("sort_order", "id")
    )


def _user_owns_product(user, product_id):
    """
    Check if user owns a product via:
    1. A paid (non-refunded) order containing the product.
    2. An active LicenseKey for the product.
    """
    from django.utils import timezone

    from catalog.models import LicenseKey
    from orders.models import OrderItem

    # Check order history. A fully paid order always proves ownership, but a
    # partially refunded order only does so for items with purchased quantity
    # not yet covered by completed item-level refunds.
    order_items = OrderItem.objects.filter(
        order__user=user,
        product_id=product_id,
        order__payment_status__in=["paid", "partially_refunded"],
    ).select_related("order")
    for item in order_items:
        if item.order.payment_status == "paid":
            return True
        if _unrefunded_quantity(item) > 0:
            return True

    # Check active, non-expired license keys (linked through order_item → product).
    now = timezone.now()
    has_license = (
        LicenseKey.objects.filter(
            user=user,
            status="active",
            order_item__product_id=product_id,
        )
        .filter(Q(is_lifetime=True) | Q(expires_at__isnull=True) | Q(expires_at__gt=now))
        .exists()
    )
    return has_license


def _unrefunded_quantity(order_item):
    """Return the purchased quantity of an order item not covered by completed refunds."""
    from orders.models import Refund

    refunded = 0
    items_jsons = Refund.objects.filter(
        order_id=order_item.order_id,
        status="completed",
    ).values_list("items_json", flat=True)
    for items_json in items_jsons:
        for entry in items_json or []:
            if entry.get("order_item_id") == order_item.id:
                refunded += entry.get("quantity", 0)
    return order_item.quantity - refunded


def _product_in_cart(cart, product_id):
    """Check if product is in the cart as a top-level item."""
    if not cart:
        return False
    return cart.items.filter(
        product_id=product_id,
        parent_bundle__isnull=True,
    ).exists()
