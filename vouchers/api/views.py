"""
Vouchers API Views
REST API endpoints for voucher management
"""

from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.api.authentication import HeadlessAPIMixin
from core.api.throttling import AuthenticatedUserThrottle, VoucherValidationThrottle
from core.utils import get_default_currency
from vouchers.api.serializers import (
    AppliedVoucherSerializer,
    GiftCardSerializer,
    VoucherApplicationSerializer,
    VoucherCodeListSerializer,
    VoucherCodeSerializer,
    VoucherRestrictionSerializer,
    VoucherUsageSerializer,
    VoucherValidationSerializer,
)
from vouchers.models import AppliedVoucher, GiftCard, VoucherCode, VoucherRestriction, VoucherUsage


@extend_schema_view(
    list=extend_schema(
        tags=["Vouchers"],
        summary=_("List all vouchers"),
        description=_(
            "Get all voucher codes. Customers see only active vouchers. Staff see all vouchers with filtering by status and discount type. Supports search by code or name."
        ),
    ),
    create=extend_schema(
        tags=["Vouchers"],
        summary=_("Create new voucher"),
        description=_(
            "Create a new voucher code (admin only). Specify discount type (percentage, fixed, gift_card), value, validity dates, usage limits, and product/category restrictions."
        ),
    ),
    retrieve=extend_schema(
        tags=["Vouchers"],
        summary=_("Get voucher details"),
        description=_(
            "Get detailed information about a specific voucher including discount rules, usage limits, restrictions, and eligible products/categories."
        ),
    ),
    update=extend_schema(
        tags=["Vouchers"],
        summary=_("Update voucher"),
        description=_(
            "Update voucher configuration (admin only). Can modify discount value, dates, usage limits, and restrictions. Active vouchers should be updated carefully."
        ),
    ),
    partial_update=extend_schema(
        tags=["Vouchers"],
        summary=_("Partially update voucher"),
        description=_(
            "Update specific voucher fields (admin only). Useful for extending expiry dates or adjusting usage limits without resending full voucher data."
        ),
    ),
    destroy=extend_schema(
        tags=["Vouchers"],
        summary=_("Delete voucher"),
        description=_(
            "Delete a voucher code (admin only). Warning: This permanently removes the voucher and all usage history. Consider deactivating instead."
        ),
    ),
    validate_code=extend_schema(
        tags=["Vouchers"],
        summary=_("Validate voucher code"),
        description=_(
            "Validate a voucher code and check if it can be used by the authenticated user. Requires authentication to prevent enumeration attacks. Rate limited to 10 requests/minute. Returns discount amount if cart total provided."
        ),
    ),
    check_eligibility=extend_schema(
        tags=["Vouchers"],
        summary=_("Check customer eligibility"),
        description=_(
            "Check if the authenticated user is eligible to use a specific voucher. Validates usage limits, customer restrictions, and account requirements. Rate limited to 10 requests/minute."
        ),
    ),
    calculate_discount=extend_schema(
        tags=["Vouchers"],
        summary=_("Calculate discount amount"),
        description=_(
            "Calculate the discount amount for a given cart total. Applies percentage or fixed discount rules, minimum purchase requirements, and maximum discount caps."
        ),
    ),
    usage_stats=extend_schema(
        tags=["Vouchers"],
        summary=_("Get voucher usage statistics"),
        description=_(
            "Get detailed usage statistics for a voucher including total uses, unique customers, total discount given, average discount per use, and recent usage history."
        ),
    ),
    bulk_generate=extend_schema(
        tags=["Vouchers"],
        summary=_("Bulk generate voucher codes"),
        description=_(
            "Bulk generate multiple voucher codes (admin only). Maximum 1000 codes per request. All generated codes share the same discount rules and restrictions but have unique codes."
        ),
    ),
)
class VoucherCodeViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing voucher codes
    """

    queryset = VoucherCode.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Use list serializer for list action"""
        if self.action == "list":
            return VoucherCodeListSerializer
        return VoucherCodeSerializer

    def get_permissions(self):
        """
        Admin-only for create/update/delete
        Authenticated required for all other operations (security best practice)
        """
        if self.action in ["create", "update", "partial_update", "destroy", "bulk_generate"]:
            return [IsAdminUser()]
        # All voucher operations now require authentication to prevent enumeration attacks
        return [IsAuthenticated()]

    def get_throttles(self):
        """Apply strict rate limiting to validation endpoints"""
        if self.action in ["validate_code", "check_eligibility", "calculate_discount"]:
            return [VoucherValidationThrottle()]
        return [AuthenticatedUserThrottle()]

    def get_queryset(self):
        """Filter vouchers based on user permissions"""
        queryset = VoucherCode.objects.select_related("created_by").prefetch_related(
            "restrictions", "eligible_products", "eligible_categories"
        )

        # Admins see all, customers only see active valid vouchers
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True, start_date__lte=timezone.now()).filter(
                Q(end_date__isnull=True) | Q(end_date__gte=timezone.now())
            )

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter == "active":
            queryset = queryset.filter(is_active=True)
        elif status_filter == "expired":
            queryset = queryset.filter(Q(end_date__lt=timezone.now()) | Q(is_active=False))

        # Filter by type
        discount_type = self.request.query_params.get("discount_type")
        if discount_type:
            queryset = queryset.filter(discount_type=discount_type)

        # Search by code or name
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(Q(code__icontains=search) | Q(name__icontains=search))

        return queryset

    @action(detail=False, methods=["post"], url_path="validate")
    def validate_code(self, request):
        """
        Validate a voucher code (requires authentication)
        POST /api/vouchers/validate/
        Body: {"code": "SUMMER2024", "cart_total": "100.00"}

        Security: Authentication required to prevent voucher code enumeration attacks.
        Rate limited to 10 requests per minute per user.
        """
        serializer = VoucherValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        cart_total = serializer.validated_data.get("cart_total")

        try:
            voucher = VoucherCode.objects.get(code=code.upper())

            # Check basic validity
            if not voucher.is_valid:
                return Response(
                    {"valid": False, "message": "This voucher is not currently valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check customer eligibility (user is guaranteed to be authenticated)
            can_use, message = voucher.can_be_used_by_customer(request.user)
            if not can_use:
                return Response(
                    {"valid": False, "message": message}, status=status.HTTP_400_BAD_REQUEST
                )

            # Calculate discount if cart total provided
            discount = None
            if cart_total:
                cart_money = Money(cart_total, get_default_currency())
                discount = voucher.calculate_discount(cart_money)

            return Response(
                {
                    "valid": True,
                    "voucher": VoucherCodeSerializer(voucher).data,
                    "discount_amount": str(discount.amount) if discount else None,
                    "message": "Voucher is valid",
                }
            )

        except VoucherCode.DoesNotExist:
            return Response(
                {"valid": False, "message": "Invalid voucher code"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=["post"], url_path="check-eligibility")
    def check_eligibility(self, request, pk=None):
        """
        Check if current user can use this voucher (requires authentication)
        POST /api/vouchers/{id}/check-eligibility/

        Security: Authentication required. Rate limited to 10 requests per minute.
        """
        voucher = self.get_object()

        # User is guaranteed to be authenticated by permission class
        can_use, message = voucher.can_be_used_by_customer(request.user)

        return Response(
            {
                "eligible": can_use,
                "message": message,
                "voucher": VoucherCodeSerializer(voucher).data,
            }
        )

    @action(detail=True, methods=["post"], url_path="calculate-discount")
    def calculate_discount(self, request, pk=None):
        """
        Calculate discount for given cart total
        POST /api/vouchers/{id}/calculate-discount/
        Body: {"cart_total": "100.00"}
        """
        voucher = self.get_object()
        cart_total = request.data.get("cart_total")

        if not cart_total:
            return Response({"error": "cart_total is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_money = Money(cart_total, get_default_currency())
            discount = voucher.calculate_discount(cart_money)

            return Response(
                {
                    "cart_total": str(cart_total),
                    "discount_amount": str(discount.amount),
                    "discount_currency": discount.currency.code,
                    "final_total": str(cart_money.amount - discount.amount),
                }
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="usage-stats")
    def usage_stats(self, request, pk=None):
        """
        Get usage statistics for a voucher
        GET /api/vouchers/{id}/usage-stats/
        """
        voucher = self.get_object()

        usage = VoucherUsage.objects.filter(voucher=voucher)

        stats = {
            "total_uses": usage.count(),
            "unique_customers": usage.filter(user__isnull=False).values("user").distinct().count(),
            "total_discount_given": usage.aggregate(total=Sum("discount_amount"))["total"]
            or Money(0, get_default_currency()),
            "average_discount": usage.aggregate(avg=Sum("discount_amount"))["avg"]
            or Money(0, get_default_currency()),
            "uses_remaining": voucher.uses_remaining,
            "recent_uses": VoucherUsageSerializer(usage.order_by("-used_at")[:10], many=True).data,
        }

        return Response(stats)

    @action(detail=False, methods=["post"], url_path="bulk-generate")
    def bulk_generate(self, request):
        """
        Bulk generate voucher codes
        POST /api/vouchers/bulk-generate/
        Body: {
            "count": 100,
            "name_prefix": "SUMMER2024",
            "discount_type": "percentage",
            "discount_value": "10.00",
            ...
        }
        """
        count = request.data.get("count", 1)
        if count > 1000:
            return Response(
                {"error": "Cannot generate more than 1000 vouchers at once"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                vouchers = []
                for _i in range(count):
                    # Copy voucher data and generate unique code
                    voucher_data = request.data.copy()
                    voucher_data.pop("count", None)
                    voucher_data.pop("code", None)  # Will be auto-generated

                    serializer = VoucherCodeSerializer(data=voucher_data)
                    if serializer.is_valid():
                        voucher = serializer.save(created_by=request.user)
                        vouchers.append(voucher)
                    else:
                        raise ValueError(serializer.errors)

            return Response(
                {
                    "created": len(vouchers),
                    "vouchers": VoucherCodeListSerializer(vouchers, many=True).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                e.args[0] if e.args else {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema_view(
    list=extend_schema(
        tags=["Vouchers"],
        summary=_("List voucher usage history"),
        description=_(
            "Get voucher usage history for the authenticated user. Staff can view all usage. Filter by voucher ID or user ID. Shows when voucher was used, discount applied, and associated order."
        ),
    ),
    retrieve=extend_schema(
        tags=["Vouchers"],
        summary=_("Get usage details"),
        description=_(
            "Get detailed information about a specific voucher usage including timestamp, user, order, discount amount applied, and voucher code used."
        ),
    ),
)
class VoucherUsageViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing voucher usage history (read-only)
    """

    queryset = VoucherUsage.objects.all()
    serializer_class = VoucherUsageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter usage based on permissions"""
        queryset = VoucherUsage.objects.select_related("voucher", "user", "order")

        # Non-admins only see their own usage
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        # Filter by voucher
        voucher_id = self.request.query_params.get("voucher")
        if voucher_id:
            queryset = queryset.filter(voucher_id=voucher_id)

        # Filter by user
        user_id = self.request.query_params.get("user")
        if user_id and self.request.user.is_staff:
            queryset = queryset.filter(user_id=user_id)

        return queryset


@extend_schema_view(
    list=extend_schema(
        tags=["Vouchers"],
        summary=_("List gift cards"),
        description=_(
            "Get gift cards for the authenticated user. Shows gift cards purchased by user or received by email. Staff can view all gift cards. Filter by status (active, partially_used, fully_used, expired)."
        ),
    ),
    create=extend_schema(
        tags=["Vouchers"],
        summary=_("Create gift card"),
        description=_(
            "Create a new gift card (admin only). Specify original value, recipient email, optional message, and expiry date. Automatically generates unique gift card code."
        ),
    ),
    retrieve=extend_schema(
        tags=["Vouchers"],
        summary=_("Get gift card details"),
        description=_(
            "Get detailed information about a specific gift card including original value, current balance, recipient, status, and usage history."
        ),
    ),
    update=extend_schema(
        tags=["Vouchers"],
        summary=_("Update gift card"),
        description=_(
            "Update gift card information (admin only). Can modify balance, status, or expiry date. Use carefully as this affects customer balances."
        ),
    ),
    partial_update=extend_schema(
        tags=["Vouchers"],
        summary=_("Partially update gift card"),
        description=_(
            "Update specific gift card fields (admin only). Useful for extending expiry date or adjusting status without sending full gift card data."
        ),
    ),
    destroy=extend_schema(
        tags=["Vouchers"],
        summary=_("Delete gift card"),
        description=_(
            "Delete a gift card (admin only). Warning: This permanently removes the gift card and remaining balance. Ensure customer has been refunded if applicable."
        ),
    ),
    check_balance=extend_schema(
        tags=["Vouchers"],
        summary=_("Check gift card balance"),
        description=_(
            "Check the current balance of a gift card by code. Returns original value, remaining balance, currency, and status. Does not require owning the gift card."
        ),
    ),
    redeem=extend_schema(
        tags=["Vouchers"],
        summary=_("Redeem gift card amount"),
        description=_(
            "Redeem a specific amount from a gift card. Validates sufficient balance and updates remaining balance. Returns new balance after redemption."
        ),
    ),
)
class GiftCardViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing gift cards
    """

    queryset = GiftCard.objects.all()
    serializer_class = GiftCardSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Admin-only for create/update/delete"""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter gift cards based on permissions"""
        queryset = GiftCard.objects.select_related("voucher", "purchased_by")

        # Non-admins only see cards they purchased or received
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(purchased_by=self.request.user) | Q(recipient_email=self.request.user.email)
            )

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=False, methods=["post"], url_path="check-balance")
    def check_balance(self, request):
        """
        Check gift card balance by code
        POST /api/gift-cards/check-balance/
        Body: {"code": "GIFT123"}
        """
        code = request.data.get("code")
        if not code:
            return Response({"error": "code is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            voucher = VoucherCode.objects.get(code=code.upper(), discount_type="gift_card")
            gift_card = voucher.gift_card

            return Response(
                {
                    "code": voucher.code,
                    "balance": str(gift_card.balance.amount) if gift_card.balance else "0.00",
                    "currency": gift_card.balance.currency.code
                    if gift_card.balance
                    else get_default_currency(),
                    "original_value": str(gift_card.original_value.amount)
                    if gift_card.original_value
                    else "0.00",
                    "status": gift_card.status,
                }
            )

        except VoucherCode.DoesNotExist:
            return Response({"error": "Invalid gift card code"}, status=status.HTTP_404_NOT_FOUND)
        except GiftCard.DoesNotExist:
            return Response(
                {"error": "This voucher is not a gift card"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["post"], url_path="redeem")
    def redeem(self, request, pk=None):
        """
        Redeem amount from gift card
        POST /api/gift-cards/{id}/redeem/
        Body: {"amount": "25.00"}
        """
        gift_card = self.get_object()
        amount = request.data.get("amount")

        if not amount:
            return Response({"error": "amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount_decimal = float(amount)
            if gift_card.redeem_amount(amount_decimal):
                return Response(
                    {
                        "success": True,
                        "redeemed_amount": amount,
                        "remaining_balance": str(gift_card.balance.amount)
                        if gift_card.balance
                        else "0.00",
                    }
                )
            else:
                return Response(
                    {"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        tags=["Vouchers"],
        summary=_("List voucher restrictions"),
        description=_(
            "Get all voucher restrictions (admin only). Filter by voucher ID to see restrictions for a specific voucher. Includes minimum purchase, customer group, and usage limit rules."
        ),
    ),
    create=extend_schema(
        tags=["Vouchers"],
        summary=_("Add voucher restriction"),
        description=_(
            "Add a new restriction to a voucher (admin only). Can restrict by minimum purchase amount, customer group, product category, or usage limits per customer."
        ),
    ),
    retrieve=extend_schema(
        tags=["Vouchers"],
        summary=_("Get restriction details"),
        description=_(
            "Get detailed information about a specific voucher restriction including restriction type, conditions, and affected voucher."
        ),
    ),
    update=extend_schema(
        tags=["Vouchers"],
        summary=_("Update restriction"),
        description=_(
            "Update a voucher restriction (admin only). Can modify restriction conditions, thresholds, and applicability rules."
        ),
    ),
    partial_update=extend_schema(
        tags=["Vouchers"],
        summary=_("Partially update restriction"),
        description=_(
            "Update specific restriction fields (admin only). Useful for adjusting thresholds or conditions without resending full restriction data."
        ),
    ),
    destroy=extend_schema(
        tags=["Vouchers"],
        summary=_("Remove restriction"),
        description=_(
            "Remove a restriction from a voucher (admin only). This makes the voucher less restrictive and may increase its applicability."
        ),
    ),
)
class VoucherRestrictionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing voucher restrictions (admin-only)
    """

    queryset = VoucherRestriction.objects.all()
    serializer_class = VoucherRestrictionSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """Filter by voucher if specified"""
        queryset = VoucherRestriction.objects.select_related("voucher")

        voucher_id = self.request.query_params.get("voucher")
        if voucher_id:
            queryset = queryset.filter(voucher_id=voucher_id)

        return queryset


@extend_schema_view(
    list=extend_schema(
        tags=["Vouchers"],
        summary=_("List applied vouchers in cart"),
        description=_(
            "Get all vouchers currently applied to the authenticated user's cart. Shows voucher codes, discount amounts, and application status."
        ),
    ),
    create=extend_schema(
        tags=["Vouchers"],
        summary=_("Apply voucher to cart"),
        description=_(
            "Apply a voucher to the user's cart. Validates voucher eligibility, calculates discount, and adds to cart. Returns error if voucher is invalid or already applied."
        ),
    ),
    retrieve=extend_schema(
        tags=["Vouchers"],
        summary=_("Get applied voucher details"),
        description=_(
            "Get detailed information about a specific voucher applied to cart including discount amount, voucher code, and application timestamp."
        ),
    ),
    update=extend_schema(
        tags=["Vouchers"],
        summary=_("Update applied voucher"),
        description=_(
            "Update an applied voucher in the cart. Can refresh discount calculation if cart contents changed."
        ),
    ),
    partial_update=extend_schema(
        tags=["Vouchers"],
        summary=_("Partially update applied voucher"),
        description=_(
            "Update specific fields of an applied voucher. Useful for recalculating discounts without full voucher reapplication."
        ),
    ),
    destroy=extend_schema(
        tags=["Vouchers"],
        summary=_("Remove voucher from cart"),
        description=_(
            "Remove a voucher from the cart. Discount is recalculated without this voucher. User can reapply the same voucher later if still eligible."
        ),
    ),
    apply_to_cart=extend_schema(
        tags=["Vouchers"],
        summary=_("Apply voucher code to cart"),
        description=_(
            "Apply a voucher to cart by entering voucher code. Validates code, checks eligibility, prevents duplicate application, and calculates discount. Returns applied voucher details or error message."
        ),
    ),
)
class AppliedVoucherViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing vouchers applied to carts
    """

    queryset = AppliedVoucher.objects.all()
    serializer_class = AppliedVoucherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only show applied vouchers for user's cart"""
        queryset = AppliedVoucher.objects.select_related("voucher", "cart")

        # Filter by user's cart
        if hasattr(self.request.user, "cart"):
            queryset = queryset.filter(cart=self.request.user.cart)
        else:
            queryset = queryset.none()

        return queryset

    @action(detail=False, methods=["post"], url_path="apply")
    def apply_to_cart(self, request):
        """
        Apply a voucher code to cart
        POST /api/applied-vouchers/apply/
        Body: {"code": "SUMMER2024"}
        """
        serializer = VoucherApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        # Get or create cart for user
        if not hasattr(request.user, "cart"):
            return Response({"error": "No active cart found"}, status=status.HTTP_400_BAD_REQUEST)

        cart = request.user.cart

        try:
            voucher = VoucherCode.objects.get(code=code.upper())

            # Check if already applied
            if AppliedVoucher.objects.filter(cart=cart, voucher=voucher).exists():
                return Response(
                    {"error": "This voucher is already applied to your cart"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check eligibility
            can_use, message = voucher.can_be_used_by_customer(request.user)
            if not can_use:
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate discount
            cart_total = cart.get_total()  # Assumes cart has get_total() method
            discount = voucher.calculate_discount(cart_total)

            # Apply voucher
            applied = AppliedVoucher.objects.create(
                cart=cart, voucher=voucher, discount_amount=discount
            )

            return Response(
                {
                    "success": True,
                    "message": "Voucher applied successfully",
                    "applied_voucher": AppliedVoucherSerializer(applied).data,
                },
                status=status.HTTP_201_CREATED,
            )

        except VoucherCode.DoesNotExist:
            return Response({"error": "Invalid voucher code"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
