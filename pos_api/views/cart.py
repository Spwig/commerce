"""
POS Cart API views.

Wraps the existing CartService to provide POS-specific cart operations.
All endpoints require staff authentication and a valid POS license.
"""

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import (
    AUTH_REQUIRED,
    POS_LICENSE_REQUIRED,
    PRODUCT_NOT_FOUND,
)
from core.api.throttling import POSPINThrottle
from pos_api.permissions import IsStaffUser
from pos_api.serializers.cart import (
    POSAddToCartSerializer,
    POSApplyDiscountSerializer,
    POSApplyGiftCardSerializer,
    POSCartSerializer,
    POSUpdateCartItemSerializer,
)
from pos_api.views.utils import get_terminal, get_terminal_currency, serialize_cart


@extend_schema(
    summary=_("Get current POS cart"),
    description=_(
        "Returns the current cart for the authenticated cashier. "
        "Creates a new cart if one does not exist. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSCartSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def get_cart(request):
    """Get or create a cart for the current cashier."""
    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=request.user)
    return Response(
        {
            "success": True,
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Add item to POS cart"),
    description=_(
        "Add a product to the cashier's cart. Supports adding by product ID or barcode. "
        "When barcode is provided without product_id, it resolves the product automatically. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSAddToCartSerializer,
    responses={
        200: POSCartSerializer,
        400: OpenApiResponse(description=_("Invalid product, variant, or insufficient stock")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=PRODUCT_NOT_FOUND),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def add_to_cart(request):
    """Add an item to the POS cart."""
    from cart.services.cart_service import CartService
    from catalog.models import Product, ProductVariant

    serializer = POSAddToCartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    product_id = data.get("product_id")
    variant_id = data.get("variant_id")
    quantity = data.get("quantity", 1)
    barcode = data.get("barcode", "").strip()
    configuration = data.get("configuration")
    preset_id = data.get("preset_id")
    variant_selections = data.get("variant_selections")
    excluded_optional_items = data.get("excluded_optional_items")

    # Resolve barcode to product_id if needed
    if barcode and not product_id:
        try:
            product = Product.objects.get(
                barcode=barcode,
                status="published",
                sales_channel__in=["all", "pos_only"],
            )
            product_id = product.id
        except Product.DoesNotExist:
            # Try variant barcode
            try:
                variant = ProductVariant.objects.select_related("product").get(
                    barcode=barcode,
                    is_active=True,
                    product__status="published",
                    product__sales_channel__in=["all", "pos_only"],
                )
                product_id = variant.product_id
                variant_id = variant.id
            except ProductVariant.DoesNotExist:
                # Try SKU
                try:
                    product = Product.objects.get(
                        sku=barcode,
                        status="published",
                        sales_channel__in=["all", "pos_only"],
                    )
                    product_id = product.id
                except Product.DoesNotExist:
                    return Response(
                        {
                            "success": False,
                            "error": {
                                "code": "NOT_FOUND",
                                "message": f'No product found with barcode "{barcode}".',
                            },
                        },
                        status=status.HTTP_404_NOT_FOUND,
                    )

    if not product_id:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "MISSING_PRODUCT",
                    "message": "Either product_id or barcode is required.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart = CartService.get_or_create_cart(user=request.user)

    # Get terminal warehouse for stock reservation
    terminal, _err = get_terminal(request)
    pos_warehouse = terminal.warehouse if terminal else None

    success, message, cart_item = CartService.add_item(
        cart,
        product_id,
        quantity,
        variant_id=variant_id,
        channel="pos",
        warehouse=pos_warehouse,
        configuration=configuration,
        preset_id=preset_id,
        variant_selections=variant_selections,
        excluded_optional_items=excluded_optional_items,
        customer_currency=get_terminal_currency(request),
    )

    if not success:
        return Response(
            {"success": False, "error": {"code": "ADD_FAILED", "message": str(message)}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": str(message),
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Update cart item quantity"),
    description=_(
        "Update the quantity of a cart item. Set quantity to 0 to remove the item. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSUpdateCartItemSerializer,
    responses={
        200: POSCartSerializer,
        400: OpenApiResponse(description=_("Invalid quantity or insufficient stock")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=_("Cart item not found")),
    },
    tags=["POS - Cart"],
)
@api_view(["PATCH"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def update_cart_item(request, item_id):
    """Update a cart item's quantity."""
    from cart.models import CartItem
    from cart.services.cart_service import CartService

    serializer = POSUpdateCartItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    cart = CartService.get_or_create_cart(user=request.user)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Cart item not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Guard: reject operations on child/component items
    if cart_item.parent_bundle is not None:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "COMPONENT_ITEM",
                    "message": "Cannot modify component items directly.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    quantity = serializer.validated_data["quantity"]
    if quantity == 0:
        success, message = CartService.remove_item(cart_item)
    else:
        success, message = CartService.update_item(cart_item, quantity=quantity, channel="pos")

    if not success:
        return Response(
            {"success": False, "error": {"code": "UPDATE_FAILED", "message": str(message)}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": str(message),
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Remove item from cart"),
    description=_(
        "Remove a specific item from the cart. Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSCartSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=_("Cart item not found")),
    },
    tags=["POS - Cart"],
)
@api_view(["DELETE"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def remove_cart_item(request, item_id):
    """Remove an item from the POS cart."""
    from cart.models import CartItem
    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=request.user)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Cart item not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Guard: reject removal of child/component items
    if cart_item.parent_bundle is not None:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "COMPONENT_ITEM",
                    "message": "Cannot remove component items directly.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    success, message = CartService.remove_item(cart_item)
    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": str(message),
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Apply voucher to cart"),
    description=_(
        "Apply a voucher/discount code to the cart. "
        "Only one voucher can be active at a time. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSApplyDiscountSerializer,
    responses={
        200: POSCartSerializer,
        400: OpenApiResponse(description=_("Invalid or expired voucher code")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def apply_voucher(request):
    """Apply a voucher code to the POS cart."""
    from cart.services.cart_service import CartService

    serializer = POSApplyDiscountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data["code"]

    cart = CartService.get_or_create_cart(user=request.user)
    success, message, discount_amount = CartService.apply_voucher(cart, code, user=request.user)

    if not success:
        return Response(
            {"success": False, "error": {"code": "VOUCHER_INVALID", "message": str(message)}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": str(message),
            "discount_amount": str(discount_amount),
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Remove voucher from cart"),
    description=_(
        "Remove the applied voucher from the cart. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSCartSerializer,
        400: OpenApiResponse(description=_("No voucher applied")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["DELETE"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def remove_voucher(request):
    """Remove the voucher from the POS cart."""
    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=request.user)

    # Get current voucher code
    first_voucher = cart.applied_vouchers.first()
    if not first_voucher:
        return Response(
            {"success": False, "error": {"code": "NO_VOUCHER", "message": "No voucher applied."}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    voucher_code = (
        first_voucher.voucher.code if hasattr(first_voucher, "voucher") else str(first_voucher)
    )
    success, message = CartService.remove_voucher(cart, voucher_code)

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": str(message),
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Apply gift card to cart"),
    description=_(
        "Apply a gift card code to the cart to cover part or all of the total. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSApplyGiftCardSerializer,
    responses={
        200: POSCartSerializer,
        400: OpenApiResponse(description=_("Invalid gift card or insufficient balance")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def apply_gift_card(request):
    """Apply a gift card to the POS cart."""
    from cart.services.cart_service import CartService

    serializer = POSApplyGiftCardSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    code = serializer.validated_data["code"]

    cart = CartService.get_or_create_cart(user=request.user)
    success, message, discount_amount = CartService.apply_gift_card(cart, code)

    if not success:
        return Response(
            {"success": False, "error": {"code": "GIFT_CARD_INVALID", "message": str(message)}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": str(message),
            "gift_card_applied": str(discount_amount),
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Clear all items from cart"),
    description=_(
        "Remove all items, vouchers, and gift cards from the cart. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSCartSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def clear_cart(request):
    """Clear the POS cart."""
    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=request.user)
    CartService.clear_cart(cart)

    # Also clear any manual discounts
    cart.pos_manual_discount_type = "none"
    cart.pos_manual_discount_value = 0
    cart.pos_manual_discount_applied_by = None
    cart.pos_manual_discount_approved_by = None
    cart.pos_manual_discount_reason = ""
    cart.save(
        update_fields=[
            "pos_manual_discount_type",
            "pos_manual_discount_value",
            "pos_manual_discount_applied_by",
            "pos_manual_discount_approved_by",
            "pos_manual_discount_reason",
        ]
    )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": "Cart cleared.",
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


class _SuperuserDiscountLimits:
    """Virtual discount limits for superusers - unlimited permissions."""

    max_discount_percentage = 100
    max_discount_amount = None
    can_apply_item_discounts = True
    can_apply_cart_discounts = True
    requires_reason = False
    is_manager = True
    manager_pin = ""

    def verify_pin(self, pin):
        return False  # Superusers don't need PIN


def _get_staff_discount_limits(user):
    """Get the staff discount limits for a user, or defaults if not configured."""
    from pos_app.models import POSStaffDiscount

    # Superusers have unlimited discount permissions
    if user.is_superuser:
        return _SuperuserDiscountLimits()

    try:
        return user.pos_discount_limit
    except POSStaffDiscount.DoesNotExist:
        # Return None to indicate no discount permissions
        return None


def _validate_discount(user, discount_type, discount_value, cart_subtotal):
    """
    Validate a discount against user's limits.
    Returns (can_apply: bool, requires_approval: bool, max_allowed: Decimal, error: str or None)
    """
    from decimal import Decimal

    limits = _get_staff_discount_limits(user)
    if limits is None:
        return False, False, Decimal("0"), "You are not authorized to apply discounts."

    if discount_type == "percentage":
        if discount_value > limits.max_discount_percentage:
            return False, True, limits.max_discount_percentage, None
    elif discount_type == "fixed":
        if limits.max_discount_amount and discount_value > limits.max_discount_amount:
            return False, True, limits.max_discount_amount, None
        # Also check percentage equivalent
        if cart_subtotal > 0:
            pct_equivalent = (discount_value / cart_subtotal) * 100
            if pct_equivalent > limits.max_discount_percentage:
                return False, True, limits.max_discount_percentage, None

    return True, False, Decimal("0"), None


@extend_schema(
    summary=_("Apply manual discount to cart item"),
    description=_(
        "Apply a staff manual discount to a specific cart item. "
        "Returns requires_approval=true if the discount exceeds staff limits. "
        "Requires staff authentication and valid POS license."
    ),
    request={
        "type": "object",
        "properties": {
            "discount_type": {"type": "string", "enum": ["percentage", "fixed"]},
            "discount_value": {"type": "number"},
            "reason": {"type": "string"},
        },
        "required": ["discount_type", "discount_value"],
    },
    responses={
        200: OpenApiResponse(description=_("Discount applied or requires approval")),
        400: OpenApiResponse(description=_("Invalid discount or not authorized")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=_("Cart item not found")),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def apply_item_discount(request, item_id):
    """Apply a manual discount to a cart item."""
    from decimal import Decimal

    from cart.models import CartItem
    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=request.user)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Cart item not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if user can apply item discounts
    limits = _get_staff_discount_limits(request.user)
    if limits is None or not limits.can_apply_item_discounts:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NOT_AUTHORIZED",
                    "message": "You are not authorized to apply item discounts.",
                },
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    discount_type = request.data.get("discount_type")
    discount_value = Decimal(str(request.data.get("discount_value", 0)))
    reason = request.data.get("reason", "")

    if discount_type not in ("percentage", "fixed"):
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INVALID_TYPE",
                    "message": 'Invalid discount type. Use "percentage" or "fixed".',
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if discount_value <= 0:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INVALID_VALUE",
                    "message": "Discount value must be greater than 0.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if reason is required
    if limits.requires_reason and not reason.strip():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "REASON_REQUIRED",
                    "message": "A reason is required for this discount.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Calculate item subtotal for validation
    item_subtotal = cart_item.unit_price.amount * cart_item.quantity

    can_apply, requires_approval, max_allowed, error = _validate_discount(
        request.user, discount_type, discount_value, item_subtotal
    )

    if error:
        return Response(
            {"success": False, "error": {"code": "NOT_AUTHORIZED", "message": error}},
            status=status.HTTP_403_FORBIDDEN,
        )

    if requires_approval:
        return Response(
            {
                "success": False,
                "requires_approval": True,
                "max_allowed": str(max_allowed),
                "max_allowed_type": "percentage"
                if discount_type == "percentage" or limits.max_discount_amount is None
                else "fixed",
                "item_id": item_id,
                "discount_type": discount_type,
                "discount_value": str(discount_value),
                "reason": reason,
            }
        )

    # Apply the discount
    cart_item.manual_discount_type = discount_type
    cart_item.manual_discount_value = discount_value
    cart_item.manual_discount_applied_by = request.user
    cart_item.manual_discount_reason = reason
    cart_item.save(
        update_fields=[
            "manual_discount_type",
            "manual_discount_value",
            "manual_discount_applied_by",
            "manual_discount_reason",
        ]
    )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": f"Discount applied to {cart_item.product.name}.",
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Remove manual discount from cart item"),
    description=_(
        "Remove a staff manual discount from a specific cart item. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: OpenApiResponse(description=_("Discount removed")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=_("Cart item not found")),
    },
    tags=["POS - Cart"],
)
@api_view(["DELETE"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def remove_item_discount(request, item_id):
    """Remove a manual discount from a cart item."""
    from cart.models import CartItem
    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=request.user)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Cart item not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    cart_item.manual_discount_type = "none"
    cart_item.manual_discount_value = 0
    cart_item.manual_discount_applied_by = None
    cart_item.manual_discount_approved_by = None
    cart_item.manual_discount_reason = ""
    cart_item.save(
        update_fields=[
            "manual_discount_type",
            "manual_discount_value",
            "manual_discount_applied_by",
            "manual_discount_approved_by",
            "manual_discount_reason",
        ]
    )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": "Item discount removed.",
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Apply manual discount to cart"),
    description=_(
        "Apply a staff manual discount to the entire cart. "
        "Returns requires_approval=true if the discount exceeds staff limits. "
        "Requires staff authentication and valid POS license."
    ),
    request={
        "type": "object",
        "properties": {
            "discount_type": {"type": "string", "enum": ["percentage", "fixed"]},
            "discount_value": {"type": "number"},
            "reason": {"type": "string"},
        },
        "required": ["discount_type", "discount_value"],
    },
    responses={
        200: OpenApiResponse(description=_("Discount applied or requires approval")),
        400: OpenApiResponse(description=_("Invalid discount or not authorized")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def apply_cart_discount(request):
    """Apply a manual discount to the entire cart."""
    from decimal import Decimal

    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=request.user)

    # Check if user can apply cart discounts
    limits = _get_staff_discount_limits(request.user)
    if limits is None or not limits.can_apply_cart_discounts:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NOT_AUTHORIZED",
                    "message": "You are not authorized to apply cart discounts.",
                },
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    discount_type = request.data.get("discount_type")
    discount_value = Decimal(str(request.data.get("discount_value", 0)))
    reason = request.data.get("reason", "")

    if discount_type not in ("percentage", "fixed"):
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INVALID_TYPE",
                    "message": 'Invalid discount type. Use "percentage" or "fixed".',
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if discount_value <= 0:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INVALID_VALUE",
                    "message": "Discount value must be greater than 0.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if reason is required
    if limits.requires_reason and not reason.strip():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "REASON_REQUIRED",
                    "message": "A reason is required for this discount.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Calculate cart subtotal for validation
    cart_subtotal = (
        cart.total_amount.amount if hasattr(cart.total_amount, "amount") else Decimal("0")
    )

    can_apply, requires_approval, max_allowed, error = _validate_discount(
        request.user, discount_type, discount_value, cart_subtotal
    )

    if error:
        return Response(
            {"success": False, "error": {"code": "NOT_AUTHORIZED", "message": error}},
            status=status.HTTP_403_FORBIDDEN,
        )

    if requires_approval:
        return Response(
            {
                "success": False,
                "requires_approval": True,
                "max_allowed": str(max_allowed),
                "max_allowed_type": "percentage"
                if discount_type == "percentage" or limits.max_discount_amount is None
                else "fixed",
                "discount_type": discount_type,
                "discount_value": str(discount_value),
                "reason": reason,
            }
        )

    # Apply the discount
    cart.pos_manual_discount_type = discount_type
    cart.pos_manual_discount_value = discount_value
    cart.pos_manual_discount_applied_by = request.user
    cart.pos_manual_discount_reason = reason
    cart.save(
        update_fields=[
            "pos_manual_discount_type",
            "pos_manual_discount_value",
            "pos_manual_discount_applied_by",
            "pos_manual_discount_reason",
        ]
    )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": "Cart discount applied.",
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Remove manual discount from cart"),
    description=_(
        "Remove the staff manual discount from the cart. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: OpenApiResponse(description=_("Discount removed")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["DELETE"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def remove_cart_discount(request):
    """Remove the manual discount from the cart."""
    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=request.user)

    cart.pos_manual_discount_type = "none"
    cart.pos_manual_discount_value = 0
    cart.pos_manual_discount_applied_by = None
    cart.pos_manual_discount_approved_by = None
    cart.pos_manual_discount_reason = ""
    cart.save(
        update_fields=[
            "pos_manual_discount_type",
            "pos_manual_discount_value",
            "pos_manual_discount_applied_by",
            "pos_manual_discount_approved_by",
            "pos_manual_discount_reason",
        ]
    )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": "Cart discount removed.",
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Verify manager PIN"),
    description=_(
        "Verify if a PIN is valid for a manager who can approve discounts. "
        "Returns the manager's name if valid. "
        "Requires staff authentication and valid POS license."
    ),
    request={
        "type": "object",
        "properties": {
            "pin": {"type": "string", "description": "4-6 digit manager PIN"},
        },
        "required": ["pin"],
    },
    responses={
        200: OpenApiResponse(description=_("PIN verification result")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
@throttle_classes([POSPINThrottle])
def verify_manager_pin(request):
    """Verify a manager PIN for discount approval."""
    from pos_app.models import POSStaffDiscount

    pin = str(request.data.get("pin", "")).strip()

    if not pin or len(pin) < 4 or len(pin) > 6:
        return Response(
            {
                "valid": False,
                "message": "PIN must be 4-6 digits.",
            }
        )

    # Find a manager with this PIN (supports both hashed and legacy plaintext)
    for manager_limit in POSStaffDiscount.objects.select_related("user").filter(is_manager=True):
        if manager_limit.verify_pin(pin):
            manager_name = manager_limit.user.get_full_name() or manager_limit.user.username
            return Response(
                {
                    "valid": True,
                    "manager_id": manager_limit.user.id,
                    "manager_name": manager_name,
                }
            )
    return Response(
        {
            "valid": False,
            "message": "Invalid manager PIN.",
        }
    )


@extend_schema(
    summary=_("Approve discount with manager PIN"),
    description=_(
        "Apply a discount that exceeds staff limits with manager approval. "
        "Requires a valid manager PIN to proceed. "
        "Requires staff authentication and valid POS license."
    ),
    request={
        "type": "object",
        "properties": {
            "manager_pin": {"type": "string", "description": "Manager's approval PIN"},
            "discount_type": {"type": "string", "enum": ["percentage", "fixed"]},
            "discount_value": {"type": "number"},
            "reason": {"type": "string"},
            "item_id": {
                "type": "integer",
                "description": "Cart item ID (for item-level discounts)",
            },
        },
        "required": ["manager_pin", "discount_type", "discount_value"],
    },
    responses={
        200: OpenApiResponse(description=_("Discount approved and applied")),
        400: OpenApiResponse(description=_("Invalid PIN or discount parameters")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=_("Cart item not found")),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
@throttle_classes([POSPINThrottle])
def approve_discount(request):
    """Approve and apply a discount with manager authorization."""
    from decimal import Decimal

    from django.db.models import F

    from cart.models import CartItem
    from cart.services.cart_service import CartService
    from pos_app.models import POSShift, POSStaffDiscount

    cart = CartService.get_or_create_cart(user=request.user)

    manager_pin = str(request.data.get("manager_pin", "")).strip()
    discount_type = request.data.get("discount_type")
    discount_value = Decimal(str(request.data.get("discount_value", 0)))
    reason = request.data.get("reason", "")
    item_id = request.data.get("item_id")  # None for cart-level discount

    # Validate PIN
    if not manager_pin or len(manager_pin) < 4 or len(manager_pin) > 6:
        return Response(
            {
                "success": False,
                "error": {"code": "INVALID_PIN", "message": "PIN must be 4-6 digits."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Find manager with this PIN (supports both hashed and legacy plaintext)
    manager_limit = None
    for ml in POSStaffDiscount.objects.select_related("user").filter(is_manager=True):
        if ml.verify_pin(manager_pin):
            manager_limit = ml
            break
    if not manager_limit:
        return Response(
            {"success": False, "error": {"code": "INVALID_PIN", "message": "Invalid manager PIN."}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    manager = manager_limit.user

    # Validate discount parameters
    if discount_type not in ("percentage", "fixed"):
        return Response(
            {
                "success": False,
                "error": {"code": "INVALID_TYPE", "message": "Invalid discount type."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if discount_value <= 0:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INVALID_VALUE",
                    "message": "Discount value must be greater than 0.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    manager_name = manager.get_full_name() or manager.username

    # Calculate discount amount for shift tracking
    if discount_type == "percentage":
        if item_id:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            discount_amount = (
                (cart_item.unit_price.amount * cart_item.quantity) * discount_value / 100
            )
        else:
            cart_subtotal = (
                cart.total_amount.amount if hasattr(cart.total_amount, "amount") else Decimal("0")
            )
            discount_amount = cart_subtotal * discount_value / 100
    else:
        discount_amount = discount_value

    if item_id:
        # Item-level discount
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "error": {"code": "NOT_FOUND", "message": "Cart item not found."},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        cart_item.manual_discount_type = discount_type
        cart_item.manual_discount_value = discount_value
        cart_item.manual_discount_applied_by = request.user
        cart_item.manual_discount_approved_by = manager
        cart_item.manual_discount_reason = reason
        cart_item.save(
            update_fields=[
                "manual_discount_type",
                "manual_discount_value",
                "manual_discount_applied_by",
                "manual_discount_approved_by",
                "manual_discount_reason",
            ]
        )
        message = f"Discount approved by {manager_name} and applied to {cart_item.product.name}."
    else:
        # Cart-level discount
        cart.pos_manual_discount_type = discount_type
        cart.pos_manual_discount_value = discount_value
        cart.pos_manual_discount_applied_by = request.user
        cart.pos_manual_discount_approved_by = manager
        cart.pos_manual_discount_reason = reason
        cart.save(
            update_fields=[
                "pos_manual_discount_type",
                "pos_manual_discount_value",
                "pos_manual_discount_applied_by",
                "pos_manual_discount_approved_by",
                "pos_manual_discount_reason",
            ]
        )
        message = f"Cart discount approved by {manager_name} and applied."

    # Update shift discount tracking
    terminal, _ = get_terminal(request)
    if terminal:
        current_shift = POSShift.objects.filter(
            terminal=terminal,
            cashier=request.user,
            ended_at__isnull=True,
        ).first()
        if current_shift:
            POSShift.objects.filter(pk=current_shift.pk).update(
                total_manual_discounts=F("total_manual_discounts") + discount_amount,
                manual_discount_count=F("manual_discount_count") + 1,
            )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": message,
            "approved_by": manager_name,
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


# ============================================================================
# PARKED CARTS
# ============================================================================


@extend_schema(
    summary=_("Park current cart"),
    description=_(
        "Save the current cart state for later restoration. "
        "Used when a customer needs to step away and another customer needs to be served. "
        "Requires staff authentication and valid POS license."
    ),
    request={
        "type": "object",
        "properties": {
            "note": {"type": "string", "description": "Optional note about the parked cart"},
        },
    },
    responses={
        200: OpenApiResponse(description=_("Cart parked successfully")),
        400: OpenApiResponse(description=_("Cart is empty or cannot be parked")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def park_cart(request):
    """Park the current cart for later restoration."""
    from decimal import Decimal

    from cart.services.cart_service import CartService
    from pos_app.models import ParkedCart

    cart = CartService.get_or_create_cart(user=request.user)

    # Check if cart has items
    if cart.items.count() == 0:
        return Response(
            {
                "success": False,
                "error": {"code": "EMPTY_CART", "message": "Cannot park an empty cart."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    terminal, err = get_terminal(request)
    if not terminal:
        return Response(
            {
                "success": False,
                "error": {"code": "NO_TERMINAL", "message": "Terminal not configured."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Build cart snapshot
    currency = get_terminal_currency(request)
    cart_snapshot = serialize_cart(cart, currency=currency, request=request)

    # Calculate totals
    item_count = sum(item["quantity"] for item in cart_snapshot.get("items", []))
    total_amount = Decimal(str(cart_snapshot.get("total", 0)))
    customer_name = (
        cart_snapshot.get("customer", {}).get("name", "") if cart_snapshot.get("customer") else ""
    )

    # Create parked cart
    parked = ParkedCart.objects.create(
        terminal=terminal,
        created_by=request.user,
        cart_data=cart_snapshot,
        item_count=item_count,
        total_amount=total_amount,
        customer_name=customer_name,
    )

    # Clear the active cart
    CartService.clear_cart(cart)
    cart.pos_manual_discount_type = "none"
    cart.pos_manual_discount_value = 0
    cart.pos_manual_discount_applied_by = None
    cart.pos_manual_discount_approved_by = None
    cart.pos_manual_discount_reason = ""
    cart.save(
        update_fields=[
            "pos_manual_discount_type",
            "pos_manual_discount_value",
            "pos_manual_discount_applied_by",
            "pos_manual_discount_approved_by",
            "pos_manual_discount_reason",
        ]
    )

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": "Cart parked.",
            "parked_cart": {
                "id": parked.id,
                "item_count": parked.item_count,
                "total_amount": str(parked.total_amount),
                "customer_name": parked.customer_name,
                "parked_at": parked.parked_at.isoformat(),
            },
            "cart": serialize_cart(cart, currency=currency, request=request),
        }
    )


@extend_schema(
    summary=_("List parked carts"),
    description=_(
        "Get all parked carts for the current terminal. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: OpenApiResponse(description=_("List of parked carts")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Cart"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def list_parked_carts(request):
    """List all parked carts for the current terminal."""
    from pos_app.models import ParkedCart

    terminal, err = get_terminal(request)
    if not terminal:
        return Response(
            {
                "success": True,
                "parked_carts": [],
            }
        )

    parked_carts = ParkedCart.objects.filter(
        terminal=terminal,
        restored_at__isnull=True,
    ).order_by("-parked_at")

    result = []
    for parked in parked_carts:
        result.append(
            {
                "id": parked.id,
                "item_count": parked.item_count,
                "total_amount": str(parked.total_amount),
                "customer_name": parked.customer_name,
                "parked_at": parked.parked_at.isoformat(),
                "parked_by": parked.created_by.get_full_name() or parked.created_by.username,
            }
        )

    return Response(
        {
            "success": True,
            "parked_carts": result,
        }
    )


@extend_schema(
    summary=_("Restore parked cart"),
    description=_(
        "Restore a parked cart, replacing the current cart contents. "
        "The current cart will be cleared before restoration. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: OpenApiResponse(description=_("Cart restored successfully")),
        400: OpenApiResponse(description=_("Current cart is not empty")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=_("Parked cart not found")),
    },
    tags=["POS - Cart"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def restore_parked_cart(request, parked_id):
    """Restore a parked cart."""
    from django.utils import timezone

    from cart.services.cart_service import CartService
    from pos_app.models import ParkedCart

    terminal, err = get_terminal(request)

    try:
        parked = ParkedCart.objects.get(
            id=parked_id,
            terminal=terminal,
            restored_at__isnull=True,
        )
    except ParkedCart.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Parked cart not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    cart = CartService.get_or_create_cart(user=request.user)

    # Clear current cart first
    CartService.clear_cart(cart)
    cart.pos_manual_discount_type = "none"
    cart.pos_manual_discount_value = 0
    cart.pos_manual_discount_applied_by = None
    cart.pos_manual_discount_approved_by = None
    cart.pos_manual_discount_reason = ""
    cart.save(
        update_fields=[
            "pos_manual_discount_type",
            "pos_manual_discount_value",
            "pos_manual_discount_applied_by",
            "pos_manual_discount_approved_by",
            "pos_manual_discount_reason",
        ]
    )

    # Restore items from parked cart
    cart_data = parked.cart_data
    pos_warehouse = terminal.warehouse if terminal else None

    for item in cart_data.get("items", []):
        product_id = item.get("product_id")
        variant_id = item.get("variant_id")
        quantity = item.get("quantity", 1)

        if product_id:
            CartService.add_item(
                cart,
                product_id,
                quantity,
                variant_id=variant_id,
                channel="pos",
                warehouse=pos_warehouse,
                customer_currency=get_terminal_currency(request),
            )

    # Restore customer if present
    customer_data = cart_data.get("customer")
    if customer_data and customer_data.get("id"):
        from customers.models import Customer

        try:
            customer = Customer.objects.get(id=customer_data["id"])
            cart.customer = customer
            cart.save(update_fields=["customer"])
        except Customer.DoesNotExist:
            pass

    # Restore manual discount if present
    manual_discount = cart_data.get("manual_discount")
    if manual_discount and manual_discount.get("type") and manual_discount["type"] != "none":
        from decimal import Decimal

        cart.pos_manual_discount_type = manual_discount["type"]
        cart.pos_manual_discount_value = Decimal(str(manual_discount.get("value", 0)))
        cart.pos_manual_discount_reason = manual_discount.get("reason", "")
        cart.pos_manual_discount_applied_by = request.user
        cart.save(
            update_fields=[
                "pos_manual_discount_type",
                "pos_manual_discount_value",
                "pos_manual_discount_reason",
                "pos_manual_discount_applied_by",
            ]
        )

    # Mark parked cart as restored
    parked.restored_at = timezone.now()
    parked.save(update_fields=["restored_at"])

    cart.refresh_from_db()
    return Response(
        {
            "success": True,
            "message": "Cart restored.",
            "cart": serialize_cart(cart, currency=get_terminal_currency(request), request=request),
        }
    )


@extend_schema(
    summary=_("Delete parked cart"),
    description=_(
        "Permanently delete a parked cart. This cannot be undone. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: OpenApiResponse(description=_("Parked cart deleted")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        404: OpenApiResponse(description=_("Parked cart not found")),
    },
    tags=["POS - Cart"],
)
@api_view(["DELETE"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def delete_parked_cart(request, parked_id):
    """Delete a parked cart."""
    from pos_app.models import ParkedCart

    terminal, err = get_terminal(request)

    try:
        parked = ParkedCart.objects.get(
            id=parked_id,
            terminal=terminal,
            restored_at__isnull=True,
        )
    except ParkedCart.DoesNotExist:
        return Response(
            {"success": False, "error": {"code": "NOT_FOUND", "message": "Parked cart not found."}},
            status=status.HTTP_404_NOT_FOUND,
        )

    parked.delete()

    return Response(
        {
            "success": True,
            "message": "Parked cart deleted.",
        }
    )
