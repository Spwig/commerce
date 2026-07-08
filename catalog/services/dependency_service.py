from django.utils.translation import gettext_lazy as _

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
            product=product, dependency_type='requires',
        ).select_related('required_product')
    )
    if not hard_deps:
        return True, []

    if not user or not user.is_authenticated:
        return False, hard_deps

    blocking = []
    for dep in hard_deps:
        owned = _user_owns_product(user, dep.required_product_id)
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
            product=product, dependency_type='recommends',
        ).select_related('required_product').order_by('sort_order', 'id')
    )


def _user_owns_product(user, product_id):
    """
    Check if user owns a product via:
    1. A paid (non-refunded) order containing the product.
    2. An active LicenseKey for the product.
    """
    from orders.models import OrderItem
    from catalog.models import LicenseKey

    # Check order history
    has_order = OrderItem.objects.filter(
        order__user=user,
        product_id=product_id,
        order__payment_status__in=['paid', 'partially_refunded'],
    ).exclude(
        order__payment_status='refunded',
    ).exists()
    if has_order:
        return True

    # Check active license keys (linked through order_item → product)
    has_license = LicenseKey.objects.filter(
        user=user,
        status='active',
        order_item__product_id=product_id,
    ).exists()
    return has_license


def _product_in_cart(cart, product_id):
    """Check if product is in the cart as a top-level item."""
    if not cart:
        return False
    return cart.items.filter(
        product_id=product_id,
        parent_bundle__isnull=True,
    ).exists()
