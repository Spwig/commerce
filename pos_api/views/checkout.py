"""
POS Checkout API views.

Handles payment processing and order creation for POS transactions.
Creates Order directly from cart without the web checkout flow.
All endpoints require staff authentication, valid POS license, and an open shift.
"""

from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import AUTH_REQUIRED, NO_OPEN_SHIFT, POS_LICENSE_REQUIRED
from pos_api.permissions import IsStaffUser
from pos_api.serializers.order import POSOrderSerializer
from pos_api.serializers.payment import (
    POSCardPaymentSerializer,
    POSCashPaymentSerializer,
    POSGiftCardPaymentSerializer,
    POSSplitTenderSerializer,
)
from pos_api.serializers.terminal_provider import POSTerminalCardPaymentSerializer
from pos_api.views.utils import get_open_shift, get_terminal


def _get_pos_order_language():
    """Get language for POS orders (uses site default since POS is merchant-facing)."""
    try:
        from core.models import SiteSettings

        return SiteSettings.get_settings().default_language or "en"
    except Exception:
        return "en"


def _resolve_customer(request):
    """Resolve optional customer_id from request data to a User object."""
    from django.contrib.auth import get_user_model

    User = get_user_model()

    customer_id = request.data.get("customer_id")
    if not customer_id:
        return None
    try:
        return User.objects.get(pk=customer_id)
    except User.DoesNotExist:
        return None


def _award_loyalty_points(order, customer_user):
    """
    Try to award loyalty points for this order. Non-blocking — never prevents a sale.
    Returns the number of points awarded, or 0.
    """
    if not customer_user:
        return 0
    try:
        member = customer_user.loyalty_member
        if not member or not member.is_active:
            return 0
        from loyalty.services.points_engine import PointsEngine

        engine = PointsEngine()
        txn = engine.award_order_points(order, member)
        return txn.points if txn else 0
    except Exception:
        return 0


def _get_loyalty_points_awarded(order):
    """Check if loyalty points were awarded for this order and return the amount."""
    try:
        from loyalty.models import LoyaltyTransaction

        txn = LoyaltyTransaction.objects.filter(
            related_object_type="order",
            related_object_id=str(order.id),
            transaction_type="earn",
        ).first()
        return txn.points if txn else 0
    except Exception:
        return 0


def _get_cart_for_checkout(user):
    """Get the user's cart and validate it has items."""
    from cart.services.cart_service import CartService

    cart = CartService.get_or_create_cart(user=user)
    items = cart.items.filter(parent_bundle__isnull=True)
    if not items.exists():
        return (
            None,
            None,
            Response(
                {
                    "success": False,
                    "error": {"code": "EMPTY_CART", "message": "Cart is empty."},
                },
                status=status.HTTP_400_BAD_REQUEST,
            ),
        )
    return cart, items, None


def _to_decimal(value):
    """
    Safely convert a value to Decimal.
    Handles Money objects, Decimals, floats, strings, and formatted currency strings.
    """
    import re

    if value is None:
        return Decimal("0")
    # Money object - use .amount attribute
    if hasattr(value, "amount"):
        return Decimal(str(value.amount))
    # Already a Decimal
    if isinstance(value, Decimal):
        return value
    # String that might be formatted (e.g., "$42.00", "€1,234.56", "42.00")
    if isinstance(value, str):
        # Strip thousand separators, then extract numeric portion
        cleaned = value.replace(",", "")
        match = re.search(r"-?\d+\.?\d*", cleaned)
        if match:
            return Decimal(match.group())
        return Decimal("0")
    # Float or int
    return Decimal(str(value))


def _calculate_order_total(cart):
    """Calculate the order total from cart fields."""
    subtotal = _to_decimal(cart.subtotal)
    total = _to_decimal(cart.grand_total)

    discount = Decimal("0")
    if hasattr(cart, "voucher_discount_amount") and cart.voucher_discount_amount:
        discount = _to_decimal(cart.voucher_discount_amount)

    return subtotal, discount, total


@transaction.atomic
def _create_pos_order(
    request, cart, cart_items, terminal, shift, customer_user=None, currency=None
):
    """
    Create an Order from the POS cart.

    Returns the created Order instance.
    """
    from djmoney.money import Money

    from orders.models import Order, OrderItem

    if not currency:
        currency = terminal.effective_currency
    order_user = customer_user or request.user

    subtotal, discount, total = _calculate_order_total(cart)

    # Calculate tax using terminal's warehouse address
    tax_amount_decimal = Decimal("0")
    try:
        from cart.services.tax_service import TaxService

        warehouse = terminal.warehouse
        if warehouse and warehouse.country:
            items = []
            for item in cart_items:
                unit_price = (
                    item.unit_price.amount
                    if hasattr(item.unit_price, "amount")
                    else Decimal(str(item.unit_price))
                )
                line_total = unit_price * item.quantity
                items.append((item.product, item.quantity, line_total))

            tax_amount_decimal, tax_breakdown_list = TaxService.calculate_tax(
                items=items,
                shipping_cost=Decimal("0"),
                country=warehouse.country,
                state=warehouse.state_province or "",
                city=warehouse.city or "",
                postal_code=warehouse.postal_code or "",
            )
            total += tax_amount_decimal
    except Exception:
        import logging

        logging.getLogger(__name__).warning("POS tax calculation failed", exc_info=True)

    from core.license import is_sandbox_mode

    order = Order(
        user=order_user,
        email=order_user.email or request.user.email,
        status="processing",
        channel="pos",
        pos_terminal=terminal,
        cashier=request.user,
        subtotal=Money(subtotal, currency),
        tax_amount=Money(tax_amount_decimal, currency),
        shipping_cost=Money(0, currency),
        discount_amount=Money(discount, currency),
        total_amount=Money(total, currency),
        payment_status="paid",
        paid_at=timezone.now(),
        amount_paid=Money(total, currency),
        shipping_name=order_user.get_full_name() or "Walk-in Customer",
        shipping_address1="In-store purchase",
        shipping_city="",
        shipping_state="",
        shipping_postal_code="",
        shipping_country="",
        is_test_order=is_sandbox_mode(),
        language=_get_pos_order_language(),
    )
    order.save()

    # Create order items from cart
    for item in cart_items:
        unit_price = (
            item.unit_price.amount
            if hasattr(item.unit_price, "amount")
            else Decimal(str(item.unit_price))
        )
        line_total = (
            item.total_price.amount
            if hasattr(item.total_price, "amount")
            else Decimal(str(item.total_price))
        )

        OrderItem.objects.create(
            order=order,
            product=item.product,
            variant=item.variant,
            product_name=str(item.product.name),
            variant_name=item.variant.name if item.variant else "",
            sku=(item.variant.sku if item.variant and item.variant.sku else item.product.sku) or "",
            quantity=item.quantity,
            unit_price=Money(unit_price, currency),
            total_price=Money(line_total, currency),
        )

    # Allocate stock from terminal's warehouse
    _allocate_pos_stock(cart_items, terminal.warehouse_id)

    return order


def _allocate_pos_stock(cart_items, warehouse_id):
    """
    Fulfill stock from the terminal's warehouse for POS items.

    POS items leave the warehouse immediately at sale time.
    If a cart-level stock reservation exists, converts it to fulfillment.
    Otherwise, does direct fulfillment with proper row-level locking.
    """
    import logging

    from django.db.models import F

    from catalog.models import StockItem, Warehouse
    from catalog.services.stock_reservation import StockReservationService

    logger = logging.getLogger(__name__)
    warehouse = Warehouse.objects.get(pk=warehouse_id)

    for item in cart_items:
        if not item.product.track_inventory:
            continue

        # Try reservation-based fulfillment first
        converted = StockReservationService.convert_pos_reservation_to_fulfillment(
            cart_item=item,
            warehouse=warehouse,
        )
        if converted:
            continue

        # No reservation — direct fulfillment with proper locking
        try:
            stock_query = StockItem.objects.select_for_update().filter(
                product=item.product,
                warehouse_id=warehouse_id,
            )
            if item.variant:
                stock_query = stock_query.filter(variant=item.variant)
            else:
                stock_query = stock_query.filter(variant__isnull=True)

            stock = stock_query.get()

            if stock.available < item.quantity:
                # POS policy: never block a sale due to stock. Log warning and
                # allow on_hand to go negative. Negative stock is reconciled
                # during inventory counts. This prevents lost sales when stock
                # records are inaccurate (common in retail environments).
                logger.warning(
                    f"Insufficient stock for POS sale: {item.product.sku} "
                    f"at warehouse {warehouse_id} "
                    f"(need {item.quantity}, available {stock.available})"
                )

            StockItem.objects.filter(pk=stock.pk).update(on_hand=F("on_hand") - item.quantity)

        except StockItem.DoesNotExist:
            logger.warning(
                f"No stock record for {item.product.sku} "
                f"(variant: {item.variant}) at warehouse {warehouse_id}"
            )


def _get_refund_methods(order):
    """Build available refund methods: order's payments (suggested) + other POS methods."""
    from pos_app.models import POSPayment

    methods = []
    seen = set()

    # 1. Order's original POS payments (suggested/default)
    for p in order.pos_payments.all():
        if p.method not in seen:
            methods.append(
                {
                    "key": p.method,
                    "label": p.get_method_display(),
                    "suggested": True,
                    "has_provider": bool(p.provider_payment_id),
                    "card_last_four": p.card_last_four or "",
                }
            )
            seen.add(p.method)

    # 2. Web payment transactions (for web orders returned at POS)
    if order.channel == "web":
        from payment_providers.models import PaymentTransaction

        for t in PaymentTransaction.objects.filter(
            order=order, transaction_type="charge", status="succeeded"
        ).select_related("provider_account__component"):
            key = f"provider_{t.provider_account.component.slug}"
            if key not in seen:
                methods.append(
                    {
                        "key": key,
                        "label": t.provider_account.display_name
                        or t.provider_account.component.name,
                        "suggested": True,
                        "has_provider": True,
                        "card_last_four": t.payment_method_last4 or "",
                    }
                )
                seen.add(key)

    # 3. Other standard POS methods as alternatives
    for value, label in POSPayment.PAYMENT_METHODS:
        if value not in seen:
            methods.append(
                {
                    "key": value,
                    "label": str(label),
                    "suggested": False,
                    "has_provider": False,
                }
            )
            seen.add(value)

    return methods


def _serialize_order(order):
    """Build POS order response dict."""
    currency = str(order.total_amount.currency)

    items = []
    for item in order.items.all():
        items.append(
            {
                "id": item.id,
                "product_name": item.product_name,
                "variant_name": item.variant_name,
                "sku": item.sku,
                "quantity": item.quantity,
                "unit_price": str(item.unit_price.amount),
                "line_total": str(item.total_price.amount),
            }
        )

    payments = []
    for p in order.pos_payments.all():
        payments.append(
            {
                "id": p.id,
                "method": p.method,
                "method_display": p.get_method_display(),
                "amount": str(p.amount.amount) if hasattr(p.amount, "amount") else str(p.amount),
                "amount_tendered": str(p.amount_tendered.amount)
                if p.amount_tendered and hasattr(p.amount_tendered, "amount")
                else None,
                "change_given": str(p.change_given.amount)
                if p.change_given and hasattr(p.change_given, "amount")
                else None,
                "card_last_four": p.card_last_four or "",
                "card_brand": p.card_brand or "",
                "has_provider": bool(p.provider_payment_id),
            }
        )

    # Web order payment transactions (for return/refund scenarios)
    web_payments = []
    if order.channel == "web":
        from payment_providers.models import PaymentTransaction

        txns = PaymentTransaction.objects.filter(
            order=order, transaction_type="charge", status="succeeded"
        ).select_related("provider_account__component")
        for t in txns:
            web_payments.append(
                {
                    "id": t.id,
                    "provider_name": t.provider_account.display_name
                    or t.provider_account.component.name,
                    "provider_slug": t.provider_account.component.slug,
                    "amount": str(t.amount.amount)
                    if hasattr(t.amount, "amount")
                    else str(t.amount),
                    "last4": t.payment_method_last4 or "",
                    "provider_transaction_id": t.provider_transaction_id,
                    "can_refund": True,
                }
            )

    # Refund history
    refunds = []
    if hasattr(order, "refunds"):
        for r in order.refunds.all():
            refunds.append(
                {
                    "id": r.id,
                    "refund_type": r.refund_type,
                    "refund_method": r.refund_method,
                    "refund_method_display": r.refund_method_display,
                    "reason": r.reason,
                    "total_amount": str(r.total_amount.amount),
                    "items": r.items_json,
                    "created_at": r.created_at.isoformat(),
                    "processed_by": r.processed_by.get_full_name() if r.processed_by else None,
                }
            )

    # Available refund methods (original payments suggested, plus other POS methods)
    available_refund_methods = _get_refund_methods(order)

    data = {
        "id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "payment_status": order.payment_status,
        "channel": order.channel,
        "items": items,
        "payments": payments,
        "subtotal": str(order.subtotal.amount),
        "tax_amount": str(order.tax_amount.amount),
        "discount_amount": str(order.discount_amount.amount),
        "total": str(order.total_amount.amount),
        "currency": currency,
        "customer_name": order.user.get_full_name() if order.user else None,
        "customer_email": order.email or None,
        "cashier_name": order.cashier.get_full_name() if order.cashier else None,
        "terminal_name": order.pos_terminal.name if order.pos_terminal else None,
        "created_at": order.created_at.isoformat(),
        "refunds": refunds,
        "available_refund_methods": available_refund_methods,
    }
    if web_payments:
        data["web_payments"] = web_payments

    return data


@extend_schema(
    summary=_("Process cash payment"),
    description=_(
        "Complete a POS transaction with cash payment. Validates that the amount "
        "tendered covers the order total and calculates change. "
        "Creates an Order with channel='pos' and a POSPayment record. "
        "Requires an open shift on the terminal. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSCashPaymentSerializer,
    responses={
        200: POSOrderSerializer,
        400: OpenApiResponse(description=_("Empty cart or insufficient cash tendered")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Checkout"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def checkout_cash(request):
    """Process a cash payment for the current cart."""
    from cart.services.cart_service import CartService
    from pos_app.models import POSPayment

    terminal, err = get_terminal(request)
    if err:
        return err
    shift, err = get_open_shift(request, terminal)
    if err:
        return err

    serializer = POSCashPaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    amount_tendered = serializer.validated_data["amount_tendered"]

    cart, cart_items, err = _get_cart_for_checkout(request.user)
    if err:
        return err

    _, _, order_total = _calculate_order_total(cart)

    if amount_tendered < order_total:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INSUFFICIENT_PAYMENT",
                    "message": f"Amount tendered ({amount_tendered}) is less than total ({order_total}).",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    change = amount_tendered - order_total
    currency = terminal.effective_currency

    customer_user = _resolve_customer(request)

    with transaction.atomic():
        order = _create_pos_order(
            request,
            cart,
            cart_items,
            terminal,
            shift,
            customer_user=customer_user,
            currency=currency,
        )

        POSPayment.objects.create(
            order=order,
            shift=shift,
            method="cash",
            amount=order_total,
            amount_tendered=amount_tendered,
            change_given=change,
        )

        shift.total_sales = (shift.total_sales or Decimal("0")) + order_total
        shift.total_transactions = (shift.total_transactions or 0) + 1
        shift.save(update_fields=["total_sales", "total_transactions"])

        CartService.clear_cart(cart)

    # Award loyalty points after commit (non-blocking)
    loyalty_pts = _award_loyalty_points(order, customer_user)

    resp = {
        "success": True,
        "order": _serialize_order(order),
        "change_given": str(change),
    }
    if loyalty_pts:
        resp["loyalty_points_earned"] = loyalty_pts
    return Response(resp)


@extend_schema(
    summary=_("Process card payment"),
    description=_(
        "Complete a POS transaction with card payment. Card processing is assumed "
        "to be handled by an external card terminal. This endpoint records the "
        "card reference and last four digits. "
        "Requires an open shift on the terminal. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSCardPaymentSerializer,
    responses={
        200: POSOrderSerializer,
        400: OpenApiResponse(description=_("Empty cart")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Checkout"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def checkout_card(request):
    """Process a card payment for the current cart."""
    from cart.services.cart_service import CartService
    from pos_app.models import POSPayment

    terminal, err = get_terminal(request)
    if err:
        return err
    shift, err = get_open_shift(request, terminal)
    if err:
        return err

    serializer = POSCardPaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    cart, cart_items, err = _get_cart_for_checkout(request.user)
    if err:
        return err

    _, _, order_total = _calculate_order_total(cart)
    currency = terminal.effective_currency

    customer_user = _resolve_customer(request)

    with transaction.atomic():
        order = _create_pos_order(
            request,
            cart,
            cart_items,
            terminal,
            shift,
            customer_user=customer_user,
            currency=currency,
        )

        POSPayment.objects.create(
            order=order,
            shift=shift,
            method="card",
            amount=order_total,
            card_last_four=data.get("card_last_four", ""),
            card_reference=data.get("card_reference", ""),
        )

        shift.total_sales = (shift.total_sales or Decimal("0")) + order_total
        shift.total_transactions = (shift.total_transactions or 0) + 1
        shift.save(update_fields=["total_sales", "total_transactions"])

        CartService.clear_cart(cart)

    loyalty_pts = _award_loyalty_points(order, customer_user)

    resp = {"success": True, "order": _serialize_order(order)}
    if loyalty_pts:
        resp["loyalty_points_earned"] = loyalty_pts
    return Response(resp)


@extend_schema(
    summary=_("Check gift card balance"),
    description=_(
        "Check the balance of a gift card for POS checkout. "
        "Returns the current balance if valid, or an error message if invalid. "
        "Requires staff authentication."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Gift card code"},
            },
            "required": ["code"],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Gift card balance info")),
        400: OpenApiResponse(description=_("Invalid gift card or missing code")),
    },
    tags=["POS - Checkout"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def check_gift_card_balance(request):
    """Check gift card balance for POS checkout."""
    from catalog.services.gift_card_service import GiftCardService
    from pos_api.views.utils import get_terminal_currency

    code = request.data.get("code", "").strip().upper()
    if not code:
        return Response(
            {"success": False, "error": "Gift card code is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        is_valid, balance_or_error = GiftCardService.validate_card(code)
        if not is_valid:
            return Response(
                {"success": False, "error": balance_or_error},
                status=status.HTTP_400_BAD_REQUEST,
            )

        currency = get_terminal_currency(request)

        return Response(
            {
                "success": True,
                "code": code,
                "balance": str(balance_or_error),
                "currency": currency,
            }
        )
    except Exception as e:
        return Response(
            {"success": False, "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(
    summary=_("Process gift card payment"),
    description=_(
        "Complete a POS transaction using a gift card. Validates the gift card "
        "has sufficient balance. If the gift card balance is less than the order "
        "total, use the split tender endpoint instead. "
        "Requires an open shift on the terminal. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSGiftCardPaymentSerializer,
    responses={
        200: POSOrderSerializer,
        400: OpenApiResponse(
            description=_("Empty cart, invalid gift card, or insufficient balance")
        ),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Checkout"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def checkout_gift_card(request):
    """Process a gift card payment for the current cart."""
    from cart.services.cart_service import CartService
    from catalog.services.gift_card_service import GiftCardService
    from pos_app.models import POSPayment

    terminal, err = get_terminal(request)
    if err:
        return err
    shift, err = get_open_shift(request, terminal)
    if err:
        return err

    serializer = POSGiftCardPaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    gift_card_code = data["gift_card_code"]
    payment_amount = data.get("amount")

    cart, cart_items, err = _get_cart_for_checkout(request.user)
    if err:
        return err

    _, _, order_total = _calculate_order_total(cart)
    currency = terminal.effective_currency

    # Validate gift card
    try:
        gc_valid, gc_balance = GiftCardService.validate_card(gift_card_code)
    except Exception:
        return Response(
            {
                "success": False,
                "error": {"code": "GIFT_CARD_INVALID", "message": "Invalid gift card code."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not gc_valid:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "GIFT_CARD_INVALID",
                    "message": "Gift card is expired or invalid.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Determine amount to charge
    charge_amount = payment_amount if payment_amount else order_total
    if charge_amount > gc_balance:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INSUFFICIENT_BALANCE",
                    "message": f"Gift card balance ({gc_balance}) is less than amount ({charge_amount}). Use split tender.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if charge_amount < order_total:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INSUFFICIENT_PAYMENT",
                    "message": "Gift card amount does not cover the full order. Use split tender.",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    customer_user = _resolve_customer(request)

    try:
        with transaction.atomic():
            order = _create_pos_order(
                request,
                cart,
                cart_items,
                terminal,
                shift,
                customer_user=customer_user,
                currency=currency,
            )

            # Deduct from gift card (check return value — rolls back order on failure)
            gc_success, gc_msg = GiftCardService.deduct_balance(
                gift_card_code, charge_amount, order=order
            )
            if not gc_success:
                raise ValueError(gc_msg)

            POSPayment.objects.create(
                order=order,
                shift=shift,
                method="gift_card",
                amount=order_total,
                gift_card_code=gift_card_code,
            )

            shift.total_sales = (shift.total_sales or Decimal("0")) + order_total
            shift.total_transactions = (shift.total_transactions or 0) + 1
            shift.save(update_fields=["total_sales", "total_transactions"])

            CartService.clear_cart(cart)
    except ValueError as e:
        return Response(
            {
                "success": False,
                "error": {"code": "GIFT_CARD_DEDUCT_FAILED", "message": str(e)},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    loyalty_pts = _award_loyalty_points(order, customer_user)

    resp = {"success": True, "order": _serialize_order(order)}
    if loyalty_pts:
        resp["loyalty_points_earned"] = loyalty_pts
    return Response(resp)


@extend_schema(
    summary=_("Process split tender payment"),
    description=_(
        "Complete a POS transaction using multiple payment methods (split tender). "
        "The total of all payments must cover the order total. Change is calculated "
        "on the last cash payment if the total exceeds the order amount. "
        "Requires an open shift on the terminal. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSSplitTenderSerializer,
    responses={
        200: POSOrderSerializer,
        400: OpenApiResponse(description=_("Empty cart, invalid payments, or insufficient total")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Checkout"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def checkout_split(request):
    """Process a split tender payment for the current cart."""
    from cart.services.cart_service import CartService
    from catalog.services.gift_card_service import GiftCardService
    from pos_app.models import POSPayment

    terminal, err = get_terminal(request)
    if err:
        return err
    shift, err = get_open_shift(request, terminal)
    if err:
        return err

    serializer = POSSplitTenderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    payments_data = serializer.validated_data["payments"]

    cart, cart_items, err = _get_cart_for_checkout(request.user)
    if err:
        return err

    _, _, order_total = _calculate_order_total(cart)
    currency = terminal.effective_currency

    # Validate total payments cover order
    payment_sum = sum(Decimal(str(p["amount"])) for p in payments_data)
    if payment_sum < order_total:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "INSUFFICIENT_PAYMENT",
                    "message": f"Total payments ({payment_sum}) do not cover order total ({order_total}).",
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Pre-validate all gift card payments before creating order
    gift_card_payments = []
    for pmt in payments_data:
        if pmt["method"] == "gift_card":
            gc_code = (pmt.get("gift_card_code") or "").strip().upper()
            gc_amount = Decimal(str(pmt["amount"]))
            if not gc_code:
                return Response(
                    {
                        "success": False,
                        "error": {
                            "code": "MISSING_GIFT_CARD_CODE",
                            "message": "Gift card code is required for gift card payments.",
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                gc_valid, gc_balance = GiftCardService.validate_card(gc_code)
            except Exception:
                gc_valid = False
                gc_balance = "Invalid gift card code."
            if not gc_valid:
                return Response(
                    {
                        "success": False,
                        "error": {
                            "code": "GIFT_CARD_INVALID",
                            "message": f"Gift card {gc_code} is invalid or expired.",
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if gc_amount > gc_balance:
                return Response(
                    {
                        "success": False,
                        "error": {
                            "code": "INSUFFICIENT_BALANCE",
                            "message": f"Gift card {gc_code} balance ({gc_balance}) is less than payment amount ({gc_amount}).",
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            gift_card_payments.append({"code": gc_code, "amount": gc_amount})

    customer_user = _resolve_customer(request)

    try:
        with transaction.atomic():
            order = _create_pos_order(
                request,
                cart,
                cart_items,
                terminal,
                shift,
                customer_user=customer_user,
                currency=currency,
            )

            # Deduct gift card balances inside the atomic block
            for gc_pmt in gift_card_payments:
                gc_success, gc_msg = GiftCardService.deduct_balance(
                    gc_pmt["code"], gc_pmt["amount"], order=order
                )
                if not gc_success:
                    raise ValueError(f"Gift card deduction failed for {gc_pmt['code']}: {gc_msg}")

            # Calculate change on last cash payment if over-tendered
            overage = payment_sum - order_total
            change_given = Decimal("0")

            for i, pmt in enumerate(payments_data):
                amount = Decimal(str(pmt["amount"]))
                method = pmt["method"]

                is_last_cash = (
                    method == "cash"
                    and overage > 0
                    and not any(p["method"] == "cash" for p in payments_data[i + 1 :])
                )

                payment_kwargs = {
                    "order": order,
                    "shift": shift,
                    "method": method,
                    "amount": amount if not is_last_cash else amount - overage,
                }

                if method == "cash":
                    payment_kwargs["amount_tendered"] = amount
                    if is_last_cash:
                        change_given = overage
                        payment_kwargs["change_given"] = overage
                elif method == "card":
                    payment_kwargs["card_last_four"] = pmt.get("card_last_four", "")
                    payment_kwargs["card_reference"] = pmt.get("card_reference", "")
                elif method == "terminal_card":
                    payment_kwargs["provider_payment_id"] = pmt.get("provider_payment_id", "")
                    payment_kwargs["card_last_four"] = pmt.get("card_last_four", "")
                    payment_kwargs["card_brand"] = pmt.get("card_brand", "")
                elif method == "gift_card":
                    payment_kwargs["gift_card_code"] = pmt.get("gift_card_code", "")

                POSPayment.objects.create(**payment_kwargs)

            shift.total_sales = (shift.total_sales or Decimal("0")) + order_total
            shift.total_transactions = (shift.total_transactions or 0) + 1
            shift.save(update_fields=["total_sales", "total_transactions"])

            CartService.clear_cart(cart)
    except ValueError as e:
        return Response(
            {
                "success": False,
                "error": {"code": "GIFT_CARD_DEDUCT_FAILED", "message": str(e)},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    loyalty_pts = _award_loyalty_points(order, customer_user)

    response_data = {"success": True, "order": _serialize_order(order)}
    if change_given > 0:
        response_data["change_given"] = str(change_given)
    if loyalty_pts:
        response_data["loyalty_points_earned"] = loyalty_pts
    return Response(response_data)


@extend_schema(
    summary=_("Process terminal card payment"),
    description=_(
        "Complete a POS transaction with an integrated card terminal payment. "
        "The frontend must have already collected payment via the terminal SDK "
        "and obtained a provider_payment_id (e.g. Stripe PaymentIntent). "
        "This endpoint verifies the payment succeeded before creating the order. "
        "Requires an open shift on the terminal. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSTerminalCardPaymentSerializer,
    responses={
        200: POSOrderSerializer,
        400: OpenApiResponse(description=_("Empty cart or payment verification failed")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Checkout"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def checkout_terminal_card(request):
    """Process a terminal card payment for the current cart."""
    import logging

    from cart.services.cart_service import CartService
    from pos_api.views.terminal_provider import _get_provider_instance
    from pos_app.models import POSPayment

    logger = logging.getLogger(__name__)

    terminal, err = get_terminal(request)
    if err:
        return err
    shift, err = get_open_shift(request, terminal)
    if err:
        return err

    serializer = POSTerminalCardPaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    provider_payment_id = data["provider_payment_id"]

    cart, cart_items, err = _get_cart_for_checkout(request.user)
    if err:
        return err

    _, _, order_total = _calculate_order_total(cart)
    currency = terminal.effective_currency

    # Verify the payment actually succeeded via the provider
    provider_instance, provider_account = _get_provider_instance(terminal)
    card_last_four = data.get("card_last_four", "")
    card_brand = data.get("card_brand", "")

    if provider_instance and provider_account and provider_account.provider_key != "manual":
        try:
            capture_result = provider_instance.capture_payment_intent(provider_payment_id)
            if not capture_result.get("success"):
                return Response(
                    {
                        "success": False,
                        "error": {
                            "code": "PAYMENT_NOT_CONFIRMED",
                            "message": f"Terminal payment not confirmed: {capture_result.get('status', 'unknown')}",
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Use card details from provider if not supplied by frontend
            if not card_last_four and capture_result.get("last4"):
                card_last_four = capture_result["last4"]
            if not card_brand and capture_result.get("card_brand"):
                card_brand = capture_result["card_brand"]
        except Exception as e:
            logger.error(f"Terminal card verification error: {e}")
            return Response(
                {
                    "success": False,
                    "error": {
                        "code": "VERIFICATION_ERROR",
                        "message": f"Could not verify terminal payment: {e}",
                    },
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    customer_user = _resolve_customer(request)

    with transaction.atomic():
        order = _create_pos_order(
            request,
            cart,
            cart_items,
            terminal,
            shift,
            customer_user=customer_user,
            currency=currency,
        )

        POSPayment.objects.create(
            order=order,
            shift=shift,
            method="terminal_card",
            amount=order_total,
            provider_payment_id=provider_payment_id,
            card_last_four=card_last_four,
            card_brand=card_brand,
        )

        shift.total_sales = (shift.total_sales or Decimal("0")) + order_total
        shift.total_transactions = (shift.total_transactions or 0) + 1
        shift.save(update_fields=["total_sales", "total_transactions"])

        CartService.clear_cart(cart)

    loyalty_pts = _award_loyalty_points(order, customer_user)

    resp = {"success": True, "order": _serialize_order(order)}
    if loyalty_pts:
        resp["loyalty_points_earned"] = loyalty_pts
    return Response(resp)
