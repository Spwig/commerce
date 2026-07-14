import logging
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money

from .models import Address, OrderItem, OrderNote

logger = logging.getLogger(__name__)


def validate_order_editable(order):
    """
    Check if an order can be edited based on its status
    Returns tuple: (is_editable, reason)
    """
    # Allow editing for draft, pending and processing orders
    editable_statuses = ["draft", "pending", "processing"]

    if order.status in editable_statuses:
        return True, None

    # For other statuses, provide specific reasons
    status_messages = {
        "shipped": _("Cannot edit order - already shipped. Please create a return/refund instead."),
        "delivered": _(
            "Cannot edit order - already delivered. Please create a return/refund instead."
        ),
        "cancelled": _("Cannot edit cancelled order. Please create a new order instead."),
        "refunded": _("Cannot edit refunded order."),
    }

    return False, status_messages.get(order.status, _("This order cannot be edited"))


def recalculate_order_totals(order):
    """
    Recalculate all order totals (subtotal, tax, shipping, discounts, total)
    This is the main calculation engine for orders

    Returns: Updated order instance (not saved - caller must save)
    """
    # 1. Calculate subtotal from items (with item-level discounts applied)
    subtotal = Money(0, order.subtotal.currency)
    voucher_eligible_subtotal = Money(0, order.subtotal.currency)

    for item in order.items.all():
        # Apply item-level discount if present
        if item.has_discount() and item.base_price:
            discount_amount = item.get_discount_amount()
            item.unit_price = item.base_price - discount_amount

        # Calculate item total
        item.total_price = item.unit_price * item.quantity
        item.save()
        subtotal += item.total_price

        # Track items eligible for voucher discounts
        if not item.exclude_from_vouchers:
            voucher_eligible_subtotal += item.total_price

    order.subtotal = subtotal

    # 2. Calculate discounts from applied vouchers
    # Only apply vouchers to items that are not excluded
    discount_amount = Money(0, order.subtotal.currency)

    # Get applied vouchers (from cart or order)
    try:
        from vouchers.models import AppliedVoucher

        applied_vouchers = AppliedVoucher.objects.filter(order=order).select_related("voucher")

        for applied in applied_vouchers:
            voucher = applied.voucher

            if voucher.discount_type == "percentage":
                # Calculate percentage discount on voucher-eligible items only
                discount = (voucher_eligible_subtotal * Decimal(voucher.discount_value)) / Decimal(
                    100
                )

                # Apply max discount limit if set
                if voucher.max_discount_amount:
                    discount = min(
                        discount, Money(voucher.max_discount_amount.amount, order.subtotal.currency)
                    )

                discount_amount += discount

            elif voucher.discount_type == "fixed":
                # Fixed amount discount (applied to eligible items only)
                # If fixed amount exceeds eligible subtotal, cap it
                fixed_discount = Money(voucher.discount_value, order.subtotal.currency)
                if fixed_discount.amount > voucher_eligible_subtotal.amount:
                    fixed_discount = voucher_eligible_subtotal
                discount_amount += fixed_discount

            elif voucher.discount_type == "gift_card":
                # Gift card value
                order.gift_card_discount = Money(voucher.discount_value, order.subtotal.currency)

    except Exception as e:
        logger.warning(f"Error calculating voucher discounts for order {order.order_number}: {e}")

    order.discount_amount = discount_amount

    # 3. Calculate tax
    # Note: Tax calculation would typically call a tax service here
    # For now, we'll preserve existing tax or calculate basic rate
    if not order.tax_amount or order.tax_amount.amount == 0:
        # Simple tax calculation - 10% default (should be replaced with proper tax service)
        taxable_amount = subtotal - discount_amount
        order.tax_amount = taxable_amount * Decimal("0.10")

    # 4. Calculate shipping cost
    # Shipping cost is typically set by shipping method selection
    # We preserve existing shipping cost unless it needs recalculation
    if not order.shipping_cost:
        order.shipping_cost = Money(0, order.subtotal.currency)

    # 5. Calculate final total
    order.total_amount = (
        order.subtotal
        + order.tax_amount
        + order.shipping_cost
        - order.discount_amount
        - order.gift_card_discount
    )

    # Ensure total is never negative
    if order.total_amount.amount < 0:
        order.total_amount = Money(0, order.subtotal.currency)

    return order


def apply_voucher_to_order(order, voucher_code_str):
    """
    Apply a voucher code to an order

    Args:
        order: Order instance
        voucher_code_str: Voucher code string

    Returns:
        tuple: (success, message, voucher or None)

    Raises:
        ValidationError: If voucher is invalid
    """
    from django.utils import timezone

    from vouchers.models import AppliedVoucher, VoucherCode, VoucherUsage

    # Normalize code
    code = voucher_code_str.strip().upper()

    # Get voucher
    try:
        voucher = VoucherCode.objects.get(code=code)
    except VoucherCode.DoesNotExist:
        raise ValidationError(_("Invalid voucher code"))

    # Check if already applied
    if hasattr(AppliedVoucher, "objects"):
        existing = AppliedVoucher.objects.filter(order=order, voucher=voucher).exists()
        if existing:
            raise ValidationError(_("This voucher is already applied to this order"))

    # Validate voucher timing
    now = timezone.now()

    if voucher.start_date and voucher.start_date > now:
        raise ValidationError(_("This voucher is not yet active"))

    if voucher.end_date and voucher.end_date < now:
        raise ValidationError(_("This voucher has expired"))

    # Check usage limits
    if voucher.max_uses_total and voucher.current_uses >= voucher.max_uses_total:
        raise ValidationError(_("This voucher has reached its usage limit"))

    # Check customer-specific usage limits
    if order.user and voucher.max_uses_per_customer and hasattr(VoucherUsage, "objects"):
        customer_uses = VoucherUsage.objects.filter(voucher=voucher, user=order.user).count()
        if customer_uses >= voucher.max_uses_per_customer:
            raise ValidationError(
                _("Customer has already used this voucher the maximum number of times")
            )

    # Check minimum order value
    if voucher.min_order_value and order.subtotal < voucher.min_order_value:
        raise ValidationError(
            _("Minimum order value of %(amount)s required for this voucher")
            % {"amount": voucher.min_order_value}
        )

    # Check application scope
    if voucher.application_scope == "products":
        # Validate that order contains eligible products
        if hasattr(voucher, "eligible_products"):
            eligible_product_ids = voucher.eligible_products.values_list("id", flat=True)
            order_product_ids = order.items.values_list("product_id", flat=True)

            if not any(pid in eligible_product_ids for pid in order_product_ids):
                raise ValidationError(_("This voucher is not valid for products in your cart"))

    elif voucher.application_scope == "categories":
        # Validate that order contains products from eligible categories
        if hasattr(voucher, "eligible_categories"):
            eligible_category_ids = voucher.eligible_categories.values_list("id", flat=True)
            order_categories = order.items.values_list("product__category_id", flat=True)

            if not any(cid in eligible_category_ids for cid in order_categories):
                raise ValidationError(_("This voucher is not valid for products in your cart"))

    # All validations passed - apply the voucher
    try:
        with transaction.atomic():
            # Create AppliedVoucher record if model exists
            if hasattr(AppliedVoucher, "objects"):
                AppliedVoucher.objects.create(order=order, voucher=voucher)

            # Recalculate totals
            order = recalculate_order_totals(order)
            order.save()

            return True, _("Voucher applied successfully"), voucher

    except Exception as e:
        logger.error(f"Error applying voucher {code} to order {order.order_number}: {e}")
        raise ValidationError(_("Error applying voucher. Please try again."))


def remove_voucher_from_order(order, voucher):
    """
    Remove a voucher from an order

    Args:
        order: Order instance
        voucher: VoucherCode instance

    Returns:
        tuple: (success, message)
    """
    from vouchers.models import AppliedVoucher

    try:
        with transaction.atomic():
            # Remove AppliedVoucher record
            if hasattr(AppliedVoucher, "objects"):
                AppliedVoucher.objects.filter(order=order, voucher=voucher).delete()

            # Recalculate totals
            order = recalculate_order_totals(order)
            order.save()

            return True, _("Voucher removed successfully")

    except Exception as e:
        logger.error(f"Error removing voucher from order {order.order_number}: {e}")
        raise ValidationError(_("Error removing voucher. Please try again."))


def sync_address_to_customer(customer, address_data, address_type="shipping"):
    """
    Save order address to customer's address book

    Args:
        customer: User instance
        address_data: Dict with address fields
        address_type: 'shipping' or 'billing'

    Returns:
        Address instance
    """
    # Check if customer already has a matching address
    existing = Address.objects.filter(
        user=customer,
        name=address_data.get("name"),
        address1=address_data.get("address1"),
        city=address_data.get("city"),
        postal_code=address_data.get("postal_code"),
    ).first()

    if existing:
        # Update existing address
        for key, value in address_data.items():
            setattr(existing, key, value)
        existing.address_type = address_type
        existing.save()
        return existing

    # Create new address
    address = Address.objects.create(
        user=customer,
        address_type=address_type,
        is_default=False,  # Don't override existing default
        **address_data,
    )

    return address


def update_order_customer(order, new_user=None, guest_email=None, guest_phone=None):
    """
    Change the customer associated with an order

    Args:
        order: Order instance
        new_user: User instance (for existing customer) or None for guest
        guest_email: Email for guest checkout
        guest_phone: Phone for guest checkout

    Returns:
        Updated order instance
    """
    with transaction.atomic():
        if new_user:
            # Assign to existing customer
            order.user = new_user
            order.email = new_user.email
            order.phone = guest_phone or getattr(new_user, "phone", "")
        else:
            # Guest checkout - create or get guest user
            if not guest_email:
                raise ValidationError(_("Guest email is required"))

            from django.contrib.auth import get_user_model

            User = get_user_model()

            # Try to find existing guest user or create new one
            guest_user, created = User.objects.get_or_create(
                email=guest_email,
                defaults={
                    "username": guest_email,
                    "is_active": True,
                },
            )

            order.user = guest_user
            order.email = guest_email
            order.phone = guest_phone or ""

        order.save()

        # Log the change
        OrderNote.objects.create(
            order=order,
            note=_("Customer changed to %(email)s") % {"email": order.email},
            is_customer_note=False,
        )

        return order


def validate_order_item_stock(product, variant=None, quantity=1):
    """
    Check if sufficient stock is available for an order item

    Args:
        product: Product instance
        variant: ProductVariant instance (optional)
        quantity: Quantity requested

    Returns:
        tuple: (available, stock_count, message)
    """
    # Determine which item to check stock for
    stock_item = variant if variant else product

    # Check if stock tracking is enabled
    if not hasattr(stock_item, "track_inventory") or not stock_item.track_inventory:
        return True, None, _("Stock tracking disabled")

    # Get available stock
    available_stock = stock_item.stock_quantity or 0 if hasattr(stock_item, "stock_quantity") else 0

    if quantity > available_stock:
        return (
            False,
            available_stock,
            _("Insufficient stock. Only %(available)d available.") % {"available": available_stock},
        )

    return True, available_stock, _("Stock available")


def add_order_item(order, product, variant=None, quantity=1, unit_price=None, customizations=None):
    """
    Add an item to an order

    Args:
        order: Order instance
        product: Product instance
        variant: ProductVariant instance (optional)
        quantity: Quantity to add
        unit_price: Override price (optional, uses product price if not provided)
        customizations: Dict of customization options

    Returns:
        OrderItem instance
    """
    # Validate stock
    stock_available, stock_count, message = validate_order_item_stock(product, variant, quantity)
    if not stock_available:
        raise ValidationError(message)

    # Determine price (captures promotional prices if active)
    if unit_price is None:
        if variant and hasattr(variant, "price"):
            unit_price = variant.price
        elif hasattr(product, "price"):
            unit_price = product.price
        else:
            raise ValidationError(_("Unable to determine product price"))

    # Capture base price from product (for discount tracking)
    # This will be the same as unit_price for new items unless a discount is applied
    base_price = unit_price

    # Create order item
    with transaction.atomic():
        # Snapshot product details
        product_name = product.name
        variant_name = variant.name if variant else ""
        sku = variant.sku if variant and hasattr(variant, "sku") else product.sku

        # Calculate total
        total_price = unit_price * quantity

        # Create item
        item = OrderItem.objects.create(
            order=order,
            product=product,
            variant=variant,
            product_name=product_name,
            variant_name=variant_name,
            sku=sku,
            quantity=quantity,
            unit_price=unit_price,
            base_price=base_price,
            total_price=total_price,
            discount_type="none",
            discount_value=0,
            discount_reason="",
            exclude_from_vouchers=False,
            customizations=customizations or {},
        )

        # Recalculate order totals
        order = recalculate_order_totals(order)
        order.save()

        # Log the addition
        OrderNote.objects.create(
            order=order,
            note=_("Added item: %(name)s (qty: %(qty)d)") % {"name": product_name, "qty": quantity},
            is_customer_note=False,
        )

        return item


def update_order_item(
    item,
    quantity=None,
    unit_price=None,
    discount_type=None,
    discount_value=None,
    discount_reason=None,
    exclude_from_vouchers=None,
):
    """
    Update an existing order item

    Args:
        item: OrderItem instance
        quantity: New quantity (optional)
        unit_price: New unit price (optional)
        discount_type: Discount type (optional)
        discount_value: Discount value (optional)
        discount_reason: Reason for discount (optional)
        exclude_from_vouchers: Exclude from order-level vouchers (optional)

    Returns:
        Updated OrderItem instance
    """
    from decimal import Decimal

    with transaction.atomic():
        changed = False

        if quantity is not None and quantity != item.quantity:
            # Validate stock for new quantity
            stock_available, stock_count, message = validate_order_item_stock(
                item.product, item.variant, quantity
            )
            if not stock_available:
                raise ValidationError(message)

            item.quantity = quantity
            changed = True

        # Handle discount updates
        if discount_type is not None or discount_value is not None:
            # Explicit discount was provided
            if discount_type is not None:
                item.discount_type = discount_type
                changed = True
            if discount_value is not None:
                item.discount_value = Decimal(str(discount_value))
                changed = True
            if discount_reason is not None:
                item.discount_reason = discount_reason
                changed = True

            # Recalculate unit_price based on discount
            if item.discount_type != "none" and item.discount_value > 0 and item.base_price:
                discount_amount = item.get_discount_amount()
                item.unit_price = item.base_price - discount_amount
                changed = True
            elif item.discount_type == "none":
                # Remove discount - restore base price
                if item.base_price:
                    item.unit_price = item.base_price
                    changed = True

        # Handle price updates with auto-discount detection
        if unit_price is not None and unit_price != item.unit_price:
            # Ensure base_price is set
            if not item.base_price:
                # Set base_price to the current product price
                if item.variant and hasattr(item.variant, "price"):
                    item.base_price = item.variant.price
                elif hasattr(item.product, "price"):
                    item.base_price = item.product.price
                else:
                    item.base_price = item.unit_price

            # Auto-detect discount if price is lower than base price
            if unit_price.amount < item.base_price.amount and discount_type is None:
                # Calculate discount automatically
                discount_amount = item.base_price - unit_price
                discount_percentage = (discount_amount.amount / item.base_price.amount) * 100

                item.discount_type = "percentage"
                item.discount_value = Decimal(str(round(discount_percentage, 2)))
                item.unit_price = unit_price
                changed = True
            else:
                item.unit_price = unit_price
                changed = True

        # Handle exclude_from_vouchers flag
        if (
            exclude_from_vouchers is not None
            and exclude_from_vouchers != item.exclude_from_vouchers
        ):
            item.exclude_from_vouchers = exclude_from_vouchers
            changed = True

        if changed:
            item.total_price = item.unit_price * item.quantity
            item.save()

            # Recalculate order totals
            order = recalculate_order_totals(item.order)
            order.save()

            # Log the update
            discount_info = (
                f", discount: {item.get_discount_percentage()}%" if item.has_discount() else ""
            )
            OrderNote.objects.create(
                order=item.order,
                note=_("Updated item: %(name)s (qty: %(qty)d, price: %(price)s%(discount)s)")
                % {
                    "name": item.product_name,
                    "qty": item.quantity,
                    "price": item.unit_price,
                    "discount": discount_info,
                },
                is_customer_note=False,
            )

        return item


def remove_order_item(item):
    """
    Remove an item from an order

    Args:
        item: OrderItem instance

    Returns:
        None
    """
    order = item.order
    product_name = item.product_name
    quantity = item.quantity

    with transaction.atomic():
        item.delete()

        # Recalculate order totals
        order = recalculate_order_totals(order)
        order.save()

        # Log the removal
        OrderNote.objects.create(
            order=order,
            note=_("Removed item: %(name)s (qty: %(qty)d)")
            % {"name": product_name, "qty": quantity},
            is_customer_note=False,
        )
