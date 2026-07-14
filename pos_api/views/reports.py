"""
POS Reports and Shift Management API views.

Shift opening/closing, cash movements, and sales reports.
All endpoints require staff authentication and a valid POS license.
"""

from datetime import date
from decimal import Decimal

from django.db.models import Count, Sum
from django.utils.translation import gettext_lazy as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from core.api.api_descriptions import AUTH_REQUIRED, NO_OPEN_SHIFT, POS_LICENSE_REQUIRED
from pos_api.permissions import IsStaffUser, check_pos_permission
from pos_api.serializers.report import POSDailyReportSerializer, POSTopProductSerializer
from pos_api.serializers.shift import (
    POSCashMovementSerializer,
    POSShiftCloseSerializer,
    POSShiftOpenSerializer,
    POSShiftSerializer,
)
from pos_api.views.utils import get_terminal


def _serialize_shift(shift):
    """Build POS shift response dict."""
    from pos_app.models import POSPayment

    net_sales = (shift.total_sales or Decimal("0")) - (shift.total_refunds or Decimal("0"))

    # Payment method breakdown
    payment_breakdown = (
        POSPayment.objects.filter(
            shift=shift,
            amount__gt=0,
        )
        .values("method")
        .annotate(
            total=Sum("amount"),
            count=Count("id"),
        )
    )

    cash_total = Decimal("0")
    card_total = Decimal("0")
    gift_card_total = Decimal("0")

    for pb in payment_breakdown:
        amount = pb["total"] or Decimal("0")
        if pb["method"] == "cash":
            cash_total = amount
        elif pb["method"] == "card":
            card_total = amount
        elif pb["method"] == "gift_card":
            gift_card_total = amount

    return {
        "id": shift.id,
        "terminal_name": shift.terminal.name,
        "cashier_name": shift.cashier.get_full_name(),
        "started_at": shift.started_at.isoformat(),
        "ended_at": shift.ended_at.isoformat() if shift.ended_at else None,
        "is_open": shift.is_open,
        "opening_cash": str(shift.opening_cash or 0),
        "total_sales": str(shift.total_sales or 0),
        "total_refunds": str(shift.total_refunds or 0),
        "total_transactions": shift.total_transactions or 0,
        "total_manual_discounts": str(shift.total_manual_discounts or 0),
        "manual_discount_count": shift.manual_discount_count or 0,
        "net_sales": str(net_sales),
        "cash_total": str(cash_total),
        "card_total": str(card_total),
        "gift_card_total": str(gift_card_total),
        "currency": shift.terminal.effective_currency,
    }


@extend_schema(
    summary=_("Get current shift summary"),
    description=_(
        "Returns the open shift summary for the current cashier on the terminal, "
        "including totals, transaction count, and payment method breakdown. "
        "Returns null shift if no shift is open. "
        "Requires staff authentication and valid POS license."
    ),
    responses={
        200: POSShiftSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Reports"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def current_shift_summary(request):
    """Get the current open shift summary."""
    from pos_app.models import POSShift

    terminal, err = get_terminal(request)
    if err:
        return err

    shift = (
        POSShift.objects.filter(
            terminal=terminal,
            cashier=request.user,
            ended_at__isnull=True,
        )
        .select_related("terminal", "cashier")
        .first()
    )

    if not shift:
        return Response({"success": True, "shift": None})

    return Response({"success": True, "shift": _serialize_shift(shift)})


@extend_schema(
    summary=_("Open a new shift"),
    description=_(
        "Start a new shift on the terminal. Only one open shift is allowed "
        "per terminal at any time. Records the opening cash amount. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSShiftOpenSerializer,
    responses={
        201: POSShiftSerializer,
        400: OpenApiResponse(description=_("Invalid opening cash amount")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        409: OpenApiResponse(description=_("A shift is already open on this terminal")),
    },
    tags=["POS - Reports"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def open_shift(request):
    """Open a new shift on the terminal."""
    from pos_app.models import POSShift

    terminal, err = get_terminal(request)
    if err:
        return err

    serializer = POSShiftOpenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    opening_cash = serializer.validated_data.get("opening_cash", Decimal("0"))

    # Check for existing open shift on this terminal
    existing = POSShift.objects.filter(
        terminal=terminal,
        ended_at__isnull=True,
    ).first()

    if existing:
        return Response(
            {
                "success": False,
                "error": {
                    "code": "SHIFT_ALREADY_OPEN",
                    "message": f"A shift is already open on this terminal (cashier: {existing.cashier.get_full_name()}).",
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    shift = POSShift.objects.create(
        terminal=terminal,
        cashier=request.user,
        opening_cash=opening_cash,
        total_sales=Decimal("0"),
        total_refunds=Decimal("0"),
        total_transactions=0,
    )

    return Response(
        {"success": True, "message": "Shift opened.", "shift": _serialize_shift(shift)},
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    summary=_("Close current shift"),
    description=_(
        "Close the current open shift. Records the closing cash amount and "
        "calculates the expected vs actual cash difference. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSShiftCloseSerializer,
    responses={
        200: POSShiftSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Reports"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def close_shift(request):
    """Close the current shift with cash reconciliation."""
    from pos_app.models import POSShift

    # Check POS close shift permission
    err = check_pos_permission(request, "pos_close_shift")
    if err:
        return err

    terminal, err = get_terminal(request)
    if err:
        return err

    serializer = POSShiftCloseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    closing_cash = serializer.validated_data["closing_cash"]
    notes = serializer.validated_data.get("notes", "")

    shift = (
        POSShift.objects.filter(
            terminal=terminal,
            cashier=request.user,
            ended_at__isnull=True,
        )
        .select_related("terminal", "cashier")
        .first()
    )

    if not shift:
        return Response(
            {
                "success": False,
                "error": {"code": "NO_OPEN_SHIFT", "message": "No open shift found."},
            },
            status=status.HTTP_409_CONFLICT,
        )

    shift.close_shift(closing_cash_amount=closing_cash)
    if notes:
        shift.notes = notes
        shift.save(update_fields=["notes"])

    shift_data = _serialize_shift(shift)
    shift_data["closing_cash"] = str(shift.closing_cash or 0)
    shift_data["expected_cash"] = str(shift.expected_cash or 0)
    shift_data["cash_difference"] = str(shift.cash_difference or 0)

    return Response({"success": True, "message": "Shift closed.", "shift": shift_data})


@extend_schema(
    summary=_("Record cash movement"),
    description=_(
        "Record a cash-in or cash-out movement during the shift. "
        "Examples: adding float, removing for deposit, petty cash. "
        "Requires an open shift on the terminal. "
        "Requires staff authentication and valid POS license."
    ),
    request=POSCashMovementSerializer,
    responses={
        201: OpenApiResponse(description=_("Cash movement recorded")),
        400: OpenApiResponse(description=_("Invalid movement data")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
        409: OpenApiResponse(description=NO_OPEN_SHIFT),
    },
    tags=["POS - Reports"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def record_cash_movement(request):
    """Record a cash in/out movement."""
    from pos_api.views.utils import get_open_shift
    from pos_app.models import CashMovement

    # Check POS cash management permission
    err = check_pos_permission(request, "pos_cash_management")
    if err:
        return err

    terminal, err = get_terminal(request)
    if err:
        return err
    shift, err = get_open_shift(request, terminal)
    if err:
        return err

    serializer = POSCashMovementSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    movement = CashMovement.objects.create(
        shift=shift,
        movement_type=data["movement_type"],
        amount=data["amount"],
        reason=data["reason"],
        performed_by=request.user,
    )

    return Response(
        {
            "success": True,
            "message": f"Cash {data['movement_type']} recorded.",
            "movement": {
                "id": movement.id,
                "movement_type": movement.movement_type,
                "amount": str(movement.amount),
                "reason": movement.reason,
                "performed_by": request.user.get_full_name(),
                "created_at": movement.created_at.isoformat(),
            },
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    summary=_("Get daily sales report"),
    description=_(
        "Returns an aggregated daily sales report for the terminal including "
        "totals, transaction count, average transaction value, and payment "
        "method breakdown. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "date",
            OpenApiTypes.DATE,
            description=_("Report date (ISO format, default: today)"),
        ),
    ],
    responses={
        200: POSDailyReportSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Reports"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def daily_report(request):
    """Get a daily sales report for the terminal."""
    from orders.models import Order
    from pos_app.models import POSPayment

    # Check POS report viewing permission
    err = check_pos_permission(request, "pos_view_reports")
    if err:
        return err

    terminal, err = get_terminal(request)
    if err:
        return err

    currency = terminal.effective_currency

    date_str = request.query_params.get("date")
    if date_str:
        try:
            report_date = date.fromisoformat(date_str)
        except ValueError:
            report_date = date.today()
    else:
        report_date = date.today()

    # Aggregate orders
    orders = Order.objects.filter(
        channel="pos",
        pos_terminal=terminal,
        created_at__date=report_date,
    ).exclude(status="cancelled")

    stats = orders.aggregate(
        total_sales=Sum("total_amount"),
        total_refunds=Sum("amount_refunded"),
        total_transactions=Count("id"),
    )

    total_sales = stats["total_sales"] or Decimal("0")
    total_refunds = stats["total_refunds"] or Decimal("0")
    net_sales = total_sales - total_refunds
    total_transactions = stats["total_transactions"] or 0
    avg_transaction = net_sales / total_transactions if total_transactions > 0 else Decimal("0")

    # Payment breakdown
    payment_breakdown = (
        POSPayment.objects.filter(
            order__channel="pos",
            order__pos_terminal=terminal,
            order__created_at__date=report_date,
            amount__gt=0,
        )
        .values("method")
        .annotate(
            total=Sum("amount"),
            count=Count("id"),
        )
    )

    breakdown = []
    for pb in payment_breakdown:
        breakdown.append(
            {
                "method": pb["method"],
                "total": str(pb["total"] or 0),
                "count": pb["count"] or 0,
            }
        )

    return Response(
        {
            "success": True,
            "report": {
                "date": str(report_date),
                "total_sales": str(total_sales),
                "total_refunds": str(total_refunds),
                "net_sales": str(net_sales),
                "total_transactions": total_transactions,
                "average_transaction": str(avg_transaction.quantize(Decimal("0.01"))),
                "payment_breakdown": breakdown,
                "currency": currency,
            },
        }
    )


@extend_schema(
    summary=_("Get top selling products"),
    description=_(
        "Returns the top selling products for the terminal on a given date, "
        "ranked by quantity sold. "
        "Requires staff authentication and valid POS license."
    ),
    parameters=[
        OpenApiParameter(
            "date",
            OpenApiTypes.DATE,
            description=_("Report date (ISO format, default: today)"),
        ),
        OpenApiParameter(
            "limit",
            OpenApiTypes.INT,
            description=_("Number of products to return (default: 10, max: 50)"),
        ),
    ],
    responses={
        200: POSTopProductSerializer(many=True),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=POS_LICENSE_REQUIRED),
    },
    tags=["POS - Reports"],
)
@api_view(["GET"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def top_products(request):
    """Get top selling products for the terminal."""
    from orders.models import OrderItem

    # Check POS report viewing permission
    err = check_pos_permission(request, "pos_view_reports")
    if err:
        return err

    terminal, err = get_terminal(request)
    if err:
        return err

    currency = terminal.effective_currency

    date_str = request.query_params.get("date")
    if date_str:
        try:
            report_date = date.fromisoformat(date_str)
        except ValueError:
            report_date = date.today()
    else:
        report_date = date.today()

    limit = min(int(request.query_params.get("limit", 10)), 50)

    top_items = (
        OrderItem.objects.filter(
            order__channel="pos",
            order__pos_terminal=terminal,
            order__created_at__date=report_date,
        )
        .exclude(
            order__status="cancelled",
        )
        .values(
            "product_id",
            "product_name",
        )
        .annotate(
            total_quantity=Sum("quantity"),
            total_revenue=Sum("total_price"),
        )
        .order_by("-total_quantity")[:limit]
    )

    results = []
    for item in top_items:
        results.append(
            {
                "product_id": item["product_id"],
                "product_name": item["product_name"],
                "sku": "",
                "total_quantity": item["total_quantity"],
                "total_revenue": str(item["total_revenue"] or 0),
                "currency": currency,
            }
        )

    return Response(
        {
            "success": True,
            "date": str(report_date),
            "products": results,
        }
    )
