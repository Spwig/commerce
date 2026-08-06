"""
API Views for Cart, Wishlist, and Checkout
"""

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.api.authentication import HeadlessAPIMixin

from .models import (
    Cart,
    CartItem,
    CheckoutSession,
    RecentlyViewed,
    ShippingMethod,
    TaxPresetGroup,
    TaxRate,
    Wishlist,
    WishlistItem,
)
from .permissions import IsAuthenticatedOrGuestCheckoutAllowed
from .serializers import (
    AddToCartSerializer,
    AddToWishlistSerializer,
    ApplyVoucherSerializer,
    CartSerializer,
    CheckoutSessionSerializer,
    RecentlyViewedSerializer,
    SetBillingAddressSerializer,
    SetPaymentMethodSerializer,
    SetShippingAddressSerializer,
    SetShippingMethodSerializer,
    ShippingMethodSerializer,
    TaxCalculationRequestSerializer,
    TaxPresetGroupSerializer,
    TaxPresetRateSerializer,
    TaxRateSerializer,
    UpdateCartItemSerializer,
    WishlistSerializer,
)
from .services import CartService, CheckoutService, TaxService, WishlistService


@extend_schema_view(
    list=extend_schema(
        tags=["Cart"],
        summary=_("Get current cart"),
        description=_(
            "Get the current cart for authenticated user or session. Returns cart items, subtotal, discounts, taxes, and total. Automatically creates cart if it doesn't exist."
        ),
    ),
    add=extend_schema(
        tags=["Cart"],
        summary=_("Add item to cart"),
        description=_(
            "Add a product to cart with specified quantity. Optionally include variant ID, customizations, and notes. Validates stock availability and merges with existing cart item if same product/variant. For subscription products, include is_subscription=true with subscription_plan_id and optionally pricing_tier_id (the shopper must be authenticated). No payment token is required here — the reusable payment method is captured at the checkout payment step and bound via the attach-subscription-token endpoint."
        ),
        request=AddToCartSerializer,
    ),
    attach_subscription_token=extend_schema(
        tags=["Cart"],
        summary=_("Attach payment token to a subscription cart item"),
        description=_(
            "Bind a saved reusable payment method (PaymentToken) to a subscription cart item before checkout. The token must belong to the authenticated user, be active, and its payment provider must support subscriptions. Called after minting the token at the checkout payment step so recurring billing has a method to charge."
        ),
    ),
    update_item=extend_schema(
        tags=["Cart"],
        summary=_("Update cart item"),
        description=_(
            "Update cart item quantity, customizations, or notes. Validates new quantity against stock availability. Returns updated cart with recalculated totals."
        ),
    ),
    remove_item=extend_schema(
        tags=["Cart"],
        summary=_("Remove cart item"),
        description=_(
            "Remove a specific item from cart. Recalculates cart totals and revalidates any applied vouchers against new cart total."
        ),
    ),
    clear=extend_schema(
        tags=["Cart"],
        summary=_("Clear cart"),
        description=_(
            "Remove all items from cart. Also removes any applied vouchers. Cart object persists but becomes empty."
        ),
    ),
    apply_voucher=extend_schema(
        tags=["Cart"],
        summary=_("Apply voucher code"),
        description=_(
            "Apply a voucher code to cart. Validates voucher eligibility, minimum purchase requirements, and usage limits. Calculates and applies discount to cart total."
        ),
    ),
    remove_voucher=extend_schema(
        tags=["Cart"],
        summary=_("Remove voucher"),
        description=_(
            "Remove a specific voucher from cart by code. Recalculates cart total without the voucher discount. User can reapply the voucher later if eligible."
        ),
    ),
    summary=extend_schema(
        tags=["Cart"],
        summary=_("Get cart summary"),
        description=_(
            "Get lightweight cart summary with item count, subtotal, and total. Faster than full cart endpoint. Useful for header cart badge or quick total display."
        ),
    ),
)
class CartViewSet(HeadlessAPIMixin, viewsets.GenericViewSet):
    """
    ViewSet for cart operations

    Endpoints:
    - GET /cart/ - Get current cart
    - POST /cart/add/ - Add item to cart
    - PATCH /cart/items/{id}/ - Update cart item
    - DELETE /cart/items/{id}/ - Remove cart item
    - POST /cart/clear/ - Clear cart
    - POST /cart/apply-voucher/ - Apply voucher code
    - DELETE /cart/remove-voucher/{code}/ - Remove voucher
    - GET /cart/summary/ - Get cart summary
    """

    queryset = Cart.objects.none()  # Required for schema generation
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get_cart(self, request):
        """Get or create cart for current user/session"""
        if request.user.is_authenticated:
            return CartService.get_or_create_cart(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart = CartService.get_or_create_cart(session_key=session_key)
            # Remember the guest cart in session DATA — it survives the
            # session-key rotation Django performs at login, so the
            # user_logged_in receiver can merge this cart into the account
            if request.session.get("guest_cart_id") != cart.id:
                request.session["guest_cart_id"] = cart.id
            return cart

    def list(self, request):
        """Get current cart"""
        cart = self.get_cart(request)
        serializer = self.get_serializer(cart)
        data = serializer.data

        # Add display-only mode metadata for dual-currency display
        from core.models import SiteSettings

        settings = SiteSettings.get_settings()
        if (
            settings.enable_multi_currency
            and getattr(settings, "multi_currency_checkout_mode", "full") == "display_only"
        ):
            visitor_currency = getattr(request, "currency", None) or request.session.get("currency")
            if visitor_currency and visitor_currency != settings.default_currency:
                try:
                    from exchange_rates.services.exchange_service import ExchangeRateService

                    fx_service = ExchangeRateService()
                    rate = fx_service.get_rate(settings.default_currency, visitor_currency)
                    data["display_only_mode"] = True
                    data["display_currency"] = visitor_currency
                    data["charge_currency"] = settings.default_currency
                    data["display_exchange_rate"] = float(rate) if rate else None
                except Exception:
                    pass

        return Response(data)

    @action(detail=False, methods=["post"])
    def add(self, request):
        """Add item to cart"""
        serializer = AddToCartSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        cart = self.get_cart(request)

        # Get customer's active currency from middleware
        customer_currency = getattr(request, "currency", None) or request.session.get("currency")

        success, message, cart_item = CartService.add_item(
            cart=cart,
            product_id=serializer.validated_data["product_id"],
            quantity=serializer.validated_data["quantity"],
            variant_id=serializer.validated_data.get("variant_id"),
            customizations=serializer.validated_data.get("customizations", {}),
            notes=serializer.validated_data.get("notes", ""),
            variant_selections=serializer.validated_data.get("variant_selections"),
            excluded_optional_items=serializer.validated_data.get("excluded_optional_items"),
            configuration=serializer.validated_data.get("configuration"),
            preset_id=serializer.validated_data.get("preset_id"),
            booking_data=serializer.validated_data.get("booking_data"),
            gift_card_data=serializer.validated_data.get("gift_card_data"),
            is_subscription=serializer.validated_data.get("is_subscription", False),
            subscription_plan=serializer.validated_data.get("subscription_plan"),
            pricing_tier=serializer.validated_data.get("pricing_tier"),
            payment_token=serializer.validated_data.get("payment_token"),
            customer_currency=customer_currency,
        )

        if success:
            cart_serializer = CartSerializer(cart)

            # Also include mini-cart formatted data for frontend
            from .mini_cart_api import format_cart_for_minicart

            mini_cart_data = format_cart_for_minicart(
                cart, just_added_item_id=cart_item.id if cart_item else None
            )

            return Response(
                {
                    "success": True,
                    "message": str(message),
                    "cart": cart_serializer.data,
                    # Mini-cart fields for frontend
                    "cart_count": mini_cart_data["cart_count"],
                    "item_count": mini_cart_data["item_count"],
                    "items": mini_cart_data["items"],
                    "subtotal": mini_cart_data["subtotal"],
                    "subtotal_formatted": mini_cart_data["subtotal_formatted"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=["post"],
        url_path="items/(?P<item_id>[^/.]+)/attach-subscription-token",
    )
    def attach_subscription_token(self, request, item_id=None):
        """Attach a saved PaymentToken to a subscription cart item.

        The storefront defers card capture to the checkout payment step: the
        client mints a reusable PaymentToken (POST /api/subscriptions/tokens/)
        and binds it to each subscription line here, so
        CheckoutService._create_subscriptions has a token to charge for the
        first cycle and every renewal.
        """
        if not request.user.is_authenticated:
            return Response(
                {"success": False, "message": str(_("Authentication required."))},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        payment_token_id = request.data.get("payment_token_id")
        if not payment_token_id:
            return Response(
                {"success": False, "message": str(_("payment_token_id is required."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if not cart_item.is_subscription:
            return Response(
                {"success": False, "message": str(_("This item is not a subscription."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from subscriptions.models import PaymentToken
        from subscriptions.provider_base import is_subscription_supported

        try:
            token = PaymentToken.objects.get(
                token_id=payment_token_id, user=request.user, is_active=True
            )
        except PaymentToken.DoesNotExist:
            return Response(
                {"success": False, "message": str(_("Invalid or inactive payment token."))},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # The token's provider account must support subscriptions, or renewal
        # billing would be impossible after the sale.
        if not is_subscription_supported(token.provider_account):
            return Response(
                {
                    "success": False,
                    "message": str(_("This payment method cannot be used for subscriptions.")),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item.payment_token = token
        cart_item.save(update_fields=["payment_token", "updated_at"])

        return Response(
            {"success": True, "message": str(_("Payment method attached to subscription."))}
        )

    @action(detail=False, methods=["patch"], url_path="items/(?P<item_id>[^/.]+)")
    def update_item(self, request, item_id=None):
        """Update cart item quantity or customizations"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        # Guard: reject operations on child/component items
        if cart_item.parent_bundle is not None:
            return Response(
                {
                    "success": False,
                    "message": str(
                        _(
                            "Component items cannot be modified directly. Update the parent product instead."
                        )
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success, message = CartService.update_item(
            cart_item=cart_item,
            quantity=serializer.validated_data.get("quantity"),
            customizations=serializer.validated_data.get("customizations"),
            notes=serializer.validated_data.get("notes"),
        )

        if success:
            cart_serializer = CartSerializer(cart)
            return Response(
                {"success": True, "message": str(message), "cart": cart_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["delete"], url_path="items/(?P<item_id>[^/.]+)")
    def remove_item(self, request, item_id=None):
        """Remove item from cart"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        # Guard: reject removal of child/component items
        if cart_item.parent_bundle is not None:
            return Response(
                {
                    "success": False,
                    "message": str(
                        _(
                            "Component items cannot be removed directly. Remove the parent product instead."
                        )
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        success, message = CartService.remove_item(cart_item)

        cart_serializer = CartSerializer(cart)
        return Response({"success": True, "message": str(message), "cart": cart_serializer.data})

    @action(detail=False, methods=["post"])
    def clear(self, request):
        """Clear all items from cart"""
        cart = self.get_cart(request)
        success, message = CartService.clear_cart(cart)

        return Response({"success": True, "message": str(message)})

    @action(detail=False, methods=["post"], url_path="apply-voucher")
    def apply_voucher(self, request):
        """Apply voucher code to cart"""
        serializer = ApplyVoucherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self.get_cart(request)
        user = request.user if request.user.is_authenticated else None

        success, message, discount_amount = CartService.apply_voucher(
            cart=cart, voucher_code=serializer.validated_data["code"], user=user
        )

        if success:
            cart_serializer = CartSerializer(cart)
            # Success hands back a Money; failure paths return a bare Decimal
            amount = getattr(discount_amount, "amount", discount_amount)
            return Response(
                {
                    "success": True,
                    "message": str(message),
                    "discount_amount": float(amount),
                    "cart": cart_serializer.data,
                }
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["delete"], url_path="remove-voucher/(?P<code>[^/.]+)")
    def remove_voucher(self, request, code=None):
        """Remove voucher from cart"""
        cart = self.get_cart(request)
        success, message = CartService.remove_voucher(cart, code)

        if success:
            cart_serializer = CartSerializer(cart)
            return Response(
                {"success": True, "message": str(message), "cart": cart_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Get cart summary (lightweight)"""
        cart = self.get_cart(request)
        summary = CartService.get_cart_summary(cart)
        return Response(summary)


@extend_schema_view(
    list=extend_schema(
        tags=["Wishlist"],
        summary=_("List user wishlists"),
        description=_(
            "Get all wishlists for the authenticated user. Users can have multiple wishlists for different purposes (e.g., 'Birthday', 'Wedding', 'Ideas'). Returns wishlist names, item counts, and privacy settings."
        ),
    ),
    create=extend_schema(
        tags=["Wishlist"],
        summary=_("Create wishlist"),
        description=_(
            "Create a new wishlist for the authenticated user. Specify name, description, and privacy setting (public/private). Public wishlists can be shared via URL."
        ),
    ),
    retrieve=extend_schema(
        tags=["Wishlist"],
        summary=_("Get wishlist details"),
        description=_(
            "Get detailed information about a specific wishlist including all items, prices, availability, and sharing settings. Only accessible to wishlist owner unless publicly shared."
        ),
    ),
    update=extend_schema(
        tags=["Wishlist"],
        summary=_("Update wishlist"),
        description=_(
            "Update wishlist information including name, description, or privacy settings. Can make wishlist public or private. Only owner can update."
        ),
    ),
    partial_update=extend_schema(
        tags=["Wishlist"],
        summary=_("Partially update wishlist"),
        description=_(
            "Update specific wishlist fields without sending full wishlist data. Useful for toggling privacy or renaming wishlist."
        ),
    ),
    destroy=extend_schema(
        tags=["Wishlist"],
        summary=_("Delete wishlist"),
        description=_(
            "Permanently delete a wishlist and all its items. Cannot be undone. Only owner can delete."
        ),
    ),
    add=extend_schema(
        tags=["Wishlist"],
        summary=_("Add item to wishlist"),
        description=_(
            "Add a product to wishlist with optional variant, quantity, and notes. Prevents duplicates. Can add to default wishlist or specify wishlist ID."
        ),
    ),
    remove_item=extend_schema(
        tags=["Wishlist"],
        summary=_("Remove item from wishlist"),
        description=_(
            "Remove a specific item from wishlist. Item can be added back later. Does not affect product availability."
        ),
    ),
    move_to_cart=extend_schema(
        tags=["Wishlist"],
        summary=_("Move item to cart"),
        description=_(
            "Move a wishlist item directly to shopping cart. Validates stock availability. Item is removed from wishlist after successful cart addition."
        ),
    ),
    get_shared=extend_schema(
        tags=["Wishlist"],
        summary=_("Get public wishlist by share slug"),
        description=_(
            "View a public wishlist using its share URL slug. Anyone with the link can view public wishlists. Useful for gift registries and wish lists shared with family/friends."
        ),
    ),
    product_ids=extend_schema(
        tags=["Wishlist"],
        summary=_("Get wishlisted product IDs"),
        description=_(
            "Returns a mapping of product IDs to wishlist item IDs for the current user's default wishlist. Used by the storefront to show wishlist heart icons on product listings without fetching full wishlist data."
        ),
        responses={
            200: OpenApiResponse(
                description=_("Map of product IDs to wishlist item IDs"),
                response={
                    "type": "object",
                    "properties": {
                        "wishlisted": {
                            "type": "object",
                            "additionalProperties": {"type": "integer"},
                            "description": _(
                                "Keys are product IDs (as strings), values are wishlist item IDs"
                            ),
                            "example": {"42": 7, "108": 12},
                        }
                    },
                },
            ),
            401: OpenApiResponse(description=_("Authentication required")),
        },
    ),
)
class WishlistViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for wishlist operations

    Endpoints:
    - GET /wishlists/ - List user's wishlists
    - POST /wishlists/ - Create new wishlist
    - GET /wishlists/{id}/ - Get wishlist details
    - PATCH /wishlists/{id}/ - Update wishlist
    - DELETE /wishlists/{id}/ - Delete wishlist
    - POST /wishlists/add/ - Add item to wishlist
    - DELETE /wishlists/items/{id}/ - Remove wishlist item
    - POST /wishlists/items/{id}/move-to-cart/ - Move item to cart
    - GET /wishlists/shared/{slug}/ - Get public wishlist by slug
    - GET /wishlists/product-ids/ - Get wishlisted product IDs
    """

    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get wishlists for current user"""
        return Wishlist.objects.filter(user=self.request.user).prefetch_related("items__product")

    def perform_create(self, serializer):
        """Create wishlist for current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def add(self, request):
        """Add item to wishlist"""
        serializer = AddToWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get or create wishlist
        if serializer.validated_data.get("wishlist_id"):
            wishlist = get_object_or_404(
                Wishlist, id=serializer.validated_data["wishlist_id"], user=request.user
            )
        else:
            wishlist = WishlistService.get_or_create_default_wishlist(request.user)

        success, message, wishlist_item = WishlistService.add_item(
            wishlist=wishlist,
            product_id=serializer.validated_data["product_id"],
            variant_id=serializer.validated_data.get("variant_id"),
            notes=serializer.validated_data.get("notes", ""),
            priority=serializer.validated_data.get("priority", "medium"),
            notify_when_available=serializer.validated_data.get("notify_when_available", False),
            notify_when_on_sale=serializer.validated_data.get("notify_when_on_sale", False),
        )

        if success:
            wishlist_serializer = WishlistSerializer(wishlist)
            return Response(
                {"success": True, "message": str(message), "wishlist": wishlist_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="item_id",
                type=int,
                location=OpenApiParameter.PATH,
                description=_("ID of the wishlist item to remove"),
            )
        ]
    )
    @action(detail=False, methods=["delete"], url_path="items/(?P<item_id>[^/.]+)")
    def remove_item(self, request, item_id=None):
        """Remove item from wishlist"""
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)

        success, message = WishlistService.remove_item(wishlist_item)

        return Response({"success": True, "message": str(message)})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="item_id",
                type=int,
                location=OpenApiParameter.PATH,
                description=_("ID of the wishlist item to move to cart"),
            )
        ]
    )
    @action(detail=False, methods=["post"], url_path="items/(?P<item_id>[^/.]+)/move-to-cart")
    def move_to_cart(self, request, item_id=None):
        """Move wishlist item to cart"""
        wishlist_item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)

        # Get cart
        from .views import CartViewSet

        cart_viewset = CartViewSet()
        cart = cart_viewset.get_cart(request)

        quantity = request.data.get("quantity", 1)
        success, message = WishlistService.move_to_cart(wishlist_item, cart, quantity)

        if success:
            return Response({"success": True, "message": str(message)})
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="slug",
                type=str,
                location=OpenApiParameter.PATH,
                description=_("Share slug of the public wishlist"),
            )
        ]
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="shared/(?P<slug>[^/.]+)",
        permission_classes=[AllowAny],
    )
    def get_shared(self, request, slug=None):
        """Get public wishlist by share slug"""
        wishlist = WishlistService.get_public_wishlist(slug)

        if not wishlist:
            return Response(
                {"success": False, "message": _("Wishlist not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(wishlist)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="product-ids", permission_classes=[AllowAny])
    def product_ids(self, request):
        """Return wishlisted product IDs with their wishlist item IDs for the current user's default wishlist.

        Called on every storefront page to render heart-button state, so guests
        must get a valid empty response rather than a 401.
        """
        if not request.user.is_authenticated:
            return Response({"wishlisted": {}})
        wishlist = WishlistService.get_or_create_default_wishlist(request.user)
        items = wishlist.items.values_list("id", "product_id")
        wishlisted = {str(product_id): item_id for item_id, product_id in items}
        return Response({"wishlisted": wishlisted})


@extend_schema_view(
    list=extend_schema(tags=["Checkout"], summary=_("Get checkout session")),
    set_shipping_address=extend_schema(tags=["Checkout"], summary=_("Set shipping address")),
    set_billing_address=extend_schema(tags=["Checkout"], summary=_("Set billing address")),
    get_shipping_methods=extend_schema(
        tags=["Checkout"], summary=_("Get available shipping methods")
    ),
    get_payment_providers=extend_schema(
        tags=["Checkout"],
        summary=_("Get available payment providers"),
        description=_(
            "Returns payment providers available for the customer's country and currency. Filters based on shipping countries, provider capabilities, and merchant configuration."
        ),
    ),
    set_shipping_method=extend_schema(tags=["Checkout"], summary=_("Set shipping method")),
    set_payment_method=extend_schema(tags=["Checkout"], summary=_("Set payment method")),
    validate=extend_schema(tags=["Checkout"], summary=_("Validate checkout")),
    complete=extend_schema(tags=["Checkout"], summary=_("Complete checkout")),
    list_tenders=extend_schema(
        tags=["Checkout"],
        summary=_("List applied tenders"),
        description=_(
            "Gift card and store credit holds against this checkout, plus the "
            "amount still due. amount_due — not total_amount — is what a "
            "payment provider should be asked to charge; it can legitimately "
            "be zero when tenders cover the whole order. Includes the "
            "signed-in customer's spendable wallet balance (null for guests, "
            "missing wallets, frozen wallets, or a currency mismatch)."
        ),
    ),
    add_gift_card_tender=extend_schema(
        tags=["Checkout"],
        summary=_("Apply a gift card"),
        description=_(
            "Places a hold on the card as a PAYMENT, not a discount: it "
            "settles the post-tax total and never reduces the tax base. "
            "Nothing is debited until payment is confirmed, so an abandoned "
            "checkout costs the customer nothing. Error messages are "
            "deliberately uniform — this endpoint sits on stored value and "
            "must not act as an enumeration oracle."
        ),
    ),
    add_wallet_tender=extend_schema(
        tags=["Checkout"],
        summary=_("Apply store credit"),
        description=_(
            "Holds the signed-in customer's wallet balance against this "
            "checkout, up to the amount due. Guests receive 403 — wallets "
            "belong to accounts. Single-currency: a wallet cannot part-pay an "
            "order in another currency."
        ),
    ),
    remove_tender=extend_schema(
        tags=["Checkout"],
        summary=_("Remove a tender"),
        description=_(
            "Releases a hold. Nothing was debited, so this only frees the "
            "reservation; the checkout's amount_due rises accordingly."
        ),
    ),
)
class CheckoutViewSet(HeadlessAPIMixin, viewsets.GenericViewSet):
    """
    ViewSet for checkout operations

    Endpoints:
    - GET /checkout/ - Get checkout session
    - POST /checkout/shipping-address/ - Set shipping address
    - POST /checkout/billing-address/ - Set billing address
    - GET /checkout/shipping-methods/ - Get available shipping methods
    - GET /checkout/payment-providers/ - Get available payment providers (filtered by country/currency)
    - POST /checkout/shipping-method/ - Select shipping method
    - POST /checkout/payment-method/ - Select payment method
    - POST /checkout/complete/ - Complete checkout and create order
    - POST /checkout/validate/ - Validate checkout before payment
    """

    queryset = CheckoutSession.objects.none()  # Required for schema generation
    serializer_class = CheckoutSessionSerializer
    permission_classes = [IsAuthenticatedOrGuestCheckoutAllowed]

    def get_session(self, request):
        """Get or create checkout session for user's cart"""
        from .views import CartViewSet

        cart_viewset = CartViewSet()
        cart_viewset.request = request
        cart = cart_viewset.get_cart(request)
        return CheckoutService.get_or_create_session(cart)

    def list(self, request):
        """Get current checkout session"""
        session = self.get_session(request)
        # Always recalculate totals from current cart state
        session.recalculate_totals()
        serializer = self.get_serializer(session)
        return Response({"success": True, "session": serializer.data})

    @action(detail=False, methods=["post"], url_path="contact")
    def contact(self, request):
        """Persist the customer's contact details, and — when a password is
        supplied (opt-in account creation) — create a real account and sign
        them into this session. The password is used immediately and never
        stored on the session or returned. Guests without a password are still
        materialised as a guest user at order time; here we just record their
        email/name so order creation and the confirmation flow have them.
        """
        session = self.get_session(request)
        email = (request.data.get("email") or "").strip()
        if not email:
            return Response(
                {"success": False, "message": _("Email is required")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        first_name = (request.data.get("first_name") or "").strip()
        last_name = (request.data.get("last_name") or "").strip()
        password = request.data.get("password") or ""

        # Record email/name on the session for order creation (this is the only
        # place a no-shipping guest's email gets persisted before payment).
        if not session.metadata:
            session.metadata = {}
        session.metadata["email"] = email[:254]
        full_name = f"{first_name} {last_name}".strip()
        if full_name:
            session.metadata["contact_name"] = full_name[:200]
        session.save(update_fields=["metadata"])

        # Only create an account now when the customer opted in with a password.
        if password:
            success, message = CheckoutService.ensure_checkout_user(
                session,
                {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": password,
                },
            )
            if not success:
                return Response(
                    {"success": False, "message": str(message)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = session.cart.user
            if (
                user is not None
                and not user.username.startswith("guest_")
                and not request.user.is_authenticated
            ):
                from django.contrib.auth import login

                login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        session_serializer = self.get_serializer(session)
        return Response({"success": True, "session": session_serializer.data})

    @action(detail=False, methods=["post"], url_path="shipping-address")
    def set_shipping_address(self, request):
        """Set shipping address for checkout"""
        serializer = SetShippingAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = self.get_session(request)

        address_data = None
        if not serializer.validated_data.get("address_id"):
            address_data = {
                "address_type": "shipping",
                "name": serializer.validated_data["name"],
                "company": serializer.validated_data.get("company", ""),
                "address1": serializer.validated_data["address1"],
                "address2": serializer.validated_data.get("address2", ""),
                "city": serializer.validated_data["city"],
                "state": serializer.validated_data.get("state", ""),
                "postal_code": serializer.validated_data["postal_code"],
                "country": serializer.validated_data["country"],
                "phone": serializer.validated_data.get("phone", ""),
            }

        success, message = CheckoutService.set_shipping_address(
            session=session,
            address_id=serializer.validated_data.get("address_id"),
            address_data=address_data,
            email=serializer.validated_data.get("email"),
            phone=serializer.validated_data.get("phone", ""),
        )

        if success:
            session_serializer = self.get_serializer(session)
            return Response(
                {"success": True, "message": str(message), "session": session_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"], url_path="billing-address")
    def set_billing_address(self, request):
        """Set billing address for checkout"""
        session = self.get_session(request)

        # No-shipping carts (digital / booking only) submit a minimal
        # billing record — name + country (+ optional postal) — instead of
        # a full street address; the serializer relaxes accordingly.
        serializer = SetBillingAddressSerializer(
            data=request.data,
            context={"cart_requires_shipping": session.cart.requires_shipping},
        )
        serializer.is_valid(raise_exception=True)

        same_as_shipping = serializer.validated_data.get("same_as_shipping", True)
        address_id = serializer.validated_data.get("address_id")

        address_data = None
        if not same_as_shipping and not address_id:
            address_data = {
                "address_type": "billing",
                "name": serializer.validated_data.get("name", ""),
                "company": serializer.validated_data.get("company", ""),
                "address1": serializer.validated_data.get("address1", ""),
                "address2": serializer.validated_data.get("address2", ""),
                "city": serializer.validated_data.get("city", ""),
                "state": serializer.validated_data.get("state", ""),
                "postal_code": serializer.validated_data.get("postal_code", ""),
                "country": serializer.validated_data.get("country", ""),
                "phone": serializer.validated_data.get("phone", ""),
            }

        success, message = CheckoutService.set_billing_address(
            session=session,
            same_as_shipping=same_as_shipping,
            address_id=address_id,
            address_data=address_data,
            # A bare name may ride along with same_as_shipping for carts
            # that never show an address form (digital-only guest checkout)
            contact_name=serializer.validated_data.get("name", ""),
            email=serializer.validated_data.get("email", ""),
        )

        if success:
            session_serializer = self.get_serializer(session)
            return Response(
                {"success": True, "message": str(message), "session": session_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"], url_path="shipping-methods")
    def get_shipping_methods(self, request):
        """Get available shipping methods"""
        session = self.get_session(request)

        refresh = request.query_params.get("refresh", "false").lower() == "true"
        methods = CheckoutService.get_available_shipping_methods(session, refresh=refresh)

        return Response({"shipping_methods": methods})

    @staticmethod
    def _geo_country(request) -> str:
        """Country code from the GeoIP middleware, '' when unavailable."""
        geo_location = getattr(request, "geo_location", None)
        if not geo_location:
            return ""
        try:
            if isinstance(geo_location, dict):
                return geo_location.get("country_code", "") or ""
            return getattr(geo_location, "country_code", "") or ""
        except Exception:
            return ""

    @action(detail=False, methods=["get"], url_path="payment-providers")
    def get_payment_providers(self, request):
        """Get available payment providers for checkout"""
        session = self.get_session(request)

        # Get available providers based on customer country and currency.
        # No-shipping carts have no shipping address — the checkout page
        # sends the billing-country field value as a ?country= hint (GeoIP
        # is the fallback when it hasn't been typed yet). Only used when no
        # address on the session carries a country, and it's a filter input
        # only — the authoritative billing country is what the customer
        # submits with the billing address before payment.
        fallback_country = request.query_params.get("country", "")[:64] or self._geo_country(
            request
        )
        available_providers = CheckoutService.get_available_payment_providers(
            session, fallback_country=fallback_country
        )

        # Get customer country for serializer context — same resolution
        # order as the provider filter (shipping → billing → hint/GeoIP)
        customer_country = CheckoutService.get_customer_country(
            session, fallback_country=fallback_country
        )
        if customer_country:
            from payment_providers.services.payment_method_filter import PaymentMethodFilter

            customer_country = PaymentMethodFilter._normalize_country_code(customer_country)
        else:
            customer_country = None

        # Serialize provider data
        from payment_providers.serializers import PaymentProviderAccountSerializer

        serializer = PaymentProviderAccountSerializer(
            available_providers,
            many=True,
            context={"request": request, "customer_country": customer_country},
        )

        return Response({"payment_providers": serializer.data})

    @action(detail=False, methods=["post"], url_path="shipping-method")
    def set_shipping_method(self, request):
        """Select shipping method"""
        serializer = SetShippingMethodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = self.get_session(request)

        success, message = CheckoutService.set_shipping_method(
            session=session, shipping_method_id=serializer.validated_data["shipping_method_id"]
        )

        if success:
            session_serializer = self.get_serializer(session)
            return Response(
                {"success": True, "message": str(message), "session": session_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"], url_path="payment-method")
    def set_payment_method(self, request):
        """Select payment method"""
        serializer = SetPaymentMethodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = self.get_session(request)

        # Resolve provider — accept UUID or slug.
        # `provider_slug` is not a column on PaymentProviderAccount; the slug
        # lives on the related ComponentRegistry row. Filter by
        # `component__slug` (and prefer the default account when a merchant
        # has more than one active account for the same provider, e.g. a
        # test+live pair).
        provider_id = serializer.validated_data.get("payment_provider_id")
        if not provider_id:
            provider_slug = serializer.validated_data.get("provider")
            from payment_providers.models import PaymentProviderAccount

            account = (
                PaymentProviderAccount.objects.filter(component__slug=provider_slug, is_active=True)
                .order_by("-is_default", "sort_order", "created_at")
                .first()
            )
            if not account:
                return Response(
                    {"success": False, "message": f'Payment provider "{provider_slug}" not found.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            provider_id = account.id

        success, message = CheckoutService.set_payment_method(
            session=session, payment_provider_id=provider_id
        )

        if success:
            session_serializer = self.get_serializer(session)
            return Response(
                {"success": True, "message": str(message), "session": session_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"])
    def validate(self, request):
        """Validate checkout is ready for payment"""
        session = self.get_session(request)

        is_valid, errors = CheckoutService.validate_checkout(session)

        return Response({"is_valid": is_valid, "errors": [str(e) for e in errors]})

    @action(detail=False, methods=["get"], url_path="tenders")
    def list_tenders(self, request):
        """
        Tenders held against this checkout, and what is still due.

        `amount_due` — not `total_amount` — is what a payment provider should
        be asked to charge. It can legitimately be zero when gift cards cover
        the order.
        """
        from payment_providers.models import PaymentTransaction

        session = self.get_session(request)
        session.recalculate_totals()

        holds = PaymentTransaction.objects.filter(
            checkout_session=session,
            transaction_type="authorize",
            status="authorized",
        ).select_related("gift_card", "wallet")

        # The wallet row in the checkout UI needs to know whether to render at
        # all and what balance to offer. Spendable (balance minus live holds
        # across every session), never the raw stored balance — offering money
        # another tab has already promised invites a refusal one click later.
        wallet_spendable = None
        if request.user.is_authenticated:
            from wallet.models import CustomerWallet
            from wallet.tender_service import WalletTenderService

            user_wallet = CustomerWallet.objects.filter(
                customer=request.user, is_active=True
            ).first()
            if user_wallet is not None and str(user_wallet.available_balance.currency) == str(
                session.total_amount.currency
            ):
                wallet_spendable = str(WalletTenderService.spendable_balance(user_wallet).amount)

        return Response(
            {
                "success": True,
                "total_amount": str(session.total_amount.amount),
                "tendered_amount": str(session.tendered_amount.amount),
                "amount_due": str(session.amount_due.amount),
                "currency": str(session.total_amount.currency),
                # None when signed out, no wallet, frozen, or currency-mismatched
                # (D5): the UI simply hides the row in all four cases.
                "wallet_spendable": wallet_spendable,
                "tenders": [
                    {
                        "id": str(t.pk),
                        "tender_type": t.tender_type,
                        "amount": str(t.amount.amount),
                        "currency": str(t.amount.currency),
                        # Never echo the full code back — it is bearer credential.
                        "gift_card_last4": t.gift_card.code[-4:] if t.gift_card else None,
                        # Human label the UI can render without knowing tender
                        # internals: "Gift card ••••1234" / "Store credit".
                        "label": (
                            f"Gift card \u2022\u2022\u2022\u2022{t.gift_card.code[-4:]}"
                            if t.gift_card
                            else str(_("Store credit"))
                            if t.wallet_id
                            else t.get_tender_type_display()
                        ),
                    }
                    for t in holds
                ],
            }
        )

    @action(detail=False, methods=["post"], url_path="tenders/gift-card")
    def add_gift_card_tender(self, request):
        """
        Apply a gift card to this checkout as a payment, not a discount.

        Places a hold: the card is not debited until payment is confirmed, so
        an abandoned checkout costs the customer nothing.
        """
        from catalog.services.gift_card_tender_service import (
            GiftCardTenderError,
            GiftCardTenderService,
            InsufficientGiftCardBalance,
        )

        code = (request.data.get("code") or "").strip()
        if not code:
            return Response(
                {"success": False, "message": _("Gift card code is required")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = self.get_session(request)
        session.recalculate_totals()

        # Never hold more than the order needs — the rest stays on the card.
        due = session.amount_due
        if due.amount <= 0:
            return Response(
                {"success": False, "message": _("This order is already fully paid")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            GiftCardTenderService.authorize_for_session(session, code, amount=due)
        except InsufficientGiftCardBalance:
            # Not an error the customer can act on beyond using another card;
            # hold whatever the card has and let them add a second one.
            try:
                GiftCardTenderService.authorize_for_session(session, code, amount=None)
            except GiftCardTenderError as exc:
                return Response(
                    {"success": False, "message": str(exc)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except GiftCardTenderError as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.list_tenders(request)

    @action(detail=False, methods=["post"], url_path="tenders/wallet")
    def add_wallet_tender(self, request):
        """
        Apply the customer's wallet balance to this checkout as a payment.

        Logged-in only — guests have no wallet. One click, no code entry: the
        wallet is resolved from the authenticated account, and the hold
        defaults to min(spendable, amount due). Nothing is debited until
        payment is confirmed, so an abandoned checkout costs nothing.
        """
        from wallet.tender_service import (
            InsufficientWalletBalance,
            WalletTenderError,
            WalletTenderService,
        )

        if not request.user.is_authenticated:
            # The viewset itself permits guests (carts do not require an
            # account), so this action gates explicitly.
            return Response(
                {"success": False, "message": _("Sign in to pay with your wallet")},
                status=status.HTTP_403_FORBIDDEN,
            )

        session = self.get_session(request)
        session.recalculate_totals()

        due = session.amount_due
        if due.amount <= 0:
            return Response(
                {"success": False, "message": _("This order is already fully paid")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            WalletTenderService.authorize_for_session(session, request.user)
        except (InsufficientWalletBalance, WalletTenderError) as exc:
            return Response(
                {"success": False, "message": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.list_tenders(request)

    @action(detail=False, methods=["delete"], url_path="tenders/(?P<tender_id>[^/.]+)")
    def remove_tender(self, request, tender_id=None):
        """Release a hold. Nothing was debited, so this only frees the reservation."""
        from payment_providers.models import PaymentTransaction

        session = self.get_session(request)
        updated = PaymentTransaction.objects.filter(
            pk=tender_id,
            checkout_session=session,
            transaction_type="authorize",
            status="authorized",
        ).update(status="voided")

        if not updated:
            return Response(
                {"success": False, "message": _("Tender not found")},
                status=status.HTTP_404_NOT_FOUND,
            )
        return self.list_tenders(request)

    @action(detail=False, methods=["post"])
    def complete(self, request):
        """Complete checkout and create order"""
        from commerce import OrderPlacementService, PlacementRequest

        session = self.get_session(request)

        # Route through the placement facade: it re-prices the cart and, in
        # enforce mode, refuses if the stored total no longer matches a fresh
        # quote. Warn-only by default (SPWIG_ENFORCE_QUOTE_DRIFT), so this is
        # behaviourally identical to create_order until the flag is flipped.
        result = OrderPlacementService.place_order(PlacementRequest(session=session))
        success, message, order = result.ok, result.message, result.order

        if success:
            from orders.serializers import OrderSerializer

            # Guests aren't authenticated — let this browser view the
            # confirmation page for the order it just placed.
            CheckoutService.grant_guest_order_access(request, order)

            order_serializer = OrderSerializer(order)
            return Response(
                {"success": True, "message": str(message), "order": order_serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema_view(
    list=extend_schema(tags=["Cart"], summary=_("Get recently viewed products")),
    retrieve=extend_schema(tags=["Cart"], summary=_("Get recently viewed details")),
)
class RecentlyViewedViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for recently viewed products

    Endpoints:
    - GET /recently-viewed/ - List recently viewed products
    """

    serializer_class = RecentlyViewedSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Get recently viewed products for user or session"""
        if self.request.user.is_authenticated:
            return RecentlyViewed.objects.filter(user=self.request.user).select_related("product")[
                :20
            ]
        else:
            session_key = self.request.session.session_key
            if session_key:
                return RecentlyViewed.objects.filter(session_key=session_key).select_related(
                    "product"
                )[:20]
            return RecentlyViewed.objects.none()


@extend_schema_view(
    list=extend_schema(tags=["Shipping"], summary=_("List shipping methods")),
    retrieve=extend_schema(tags=["Shipping"], summary=_("Get shipping method details")),
)
class ShippingMethodViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for shipping methods (read-only)

    Endpoints:
    - GET /shipping-methods/ - List active shipping methods
    - GET /shipping-methods/{id}/ - Get shipping method details
    """

    serializer_class = ShippingMethodSerializer
    permission_classes = [AllowAny]
    queryset = ShippingMethod.objects.filter(is_active=True)


# Admin AJAX Views
# ==========================================
# Tax Rate API ViewSets
# ==========================================


@extend_schema_view(
    list=extend_schema(tags=["Tax"], summary=_("List tax rates")),
    retrieve=extend_schema(tags=["Tax"], summary=_("Get tax rate details")),
    create=extend_schema(tags=["Tax"], summary=_("Create tax rate")),
    update=extend_schema(tags=["Tax"], summary=_("Update tax rate")),
    partial_update=extend_schema(tags=["Tax"], summary=_("Partial update tax rate")),
    destroy=extend_schema(tags=["Tax"], summary=_("Delete tax rate")),
)
class TaxRateViewSet(viewsets.ModelViewSet):
    """CRUD API for tax rates (admin only)."""

    serializer_class = TaxRateSerializer
    permission_classes = [IsAdminUser]
    queryset = TaxRate.objects.all().order_by("-priority", "country", "state")

    @extend_schema(
        tags=["Tax"],
        summary=_("Calculate applicable taxes"),
        request=TaxCalculationRequestSerializer,
        responses={200: dict},
    )
    @action(detail=False, methods=["post"])
    def calculate(self, request):
        """Calculate taxes for a given address and items."""
        serializer = TaxCalculationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        from decimal import Decimal

        from catalog.models import Product

        items = []
        for item_data in data["items"]:
            try:
                product = Product.objects.get(id=item_data["product_id"])
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product {item_data['product_id']} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            line_total = Decimal(str(item_data["price"])) * item_data["quantity"]
            items.append((product, item_data["quantity"], line_total))

        total_tax, breakdown = TaxService.calculate_tax(
            items=items,
            shipping_cost=data.get("shipping_cost", Decimal("0")),
            country=data["country"],
            state=data.get("state", ""),
            city=data.get("city", ""),
            postal_code=data.get("postal_code", ""),
        )

        return Response(
            {
                "total_tax": str(total_tax),
                "breakdown": breakdown,
            }
        )

    @extend_schema(
        tags=["Tax"],
        summary=_("Tax rates grouped by country"),
        responses={200: dict},
    )
    @action(detail=False, methods=["get"])
    def by_country(self, request):
        """Return tax rates grouped by country."""
        from collections import OrderedDict

        rates = TaxRate.objects.filter(is_active=True).order_by("country", "state")
        grouped = OrderedDict()
        for rate in rates:
            if rate.country not in grouped:
                grouped[rate.country] = []
            grouped[rate.country].append(TaxRateSerializer(rate).data)

        return Response(grouped)

    @extend_schema(
        tags=["Tax"],
        summary=_("Load preset tax rates"),
        request={
            "type": "object",
            "properties": {
                "group_key": {"type": "string"},
            },
        },
        responses={200: dict},
    )
    @action(detail=False, methods=["post"], url_path="load-preset")
    def load_preset(self, request):
        """Load a preset tax configuration into active TaxRates."""
        group_key = request.data.get("group_key", "")
        if not group_key:
            return Response(
                {"error": "group_key is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created, skipped = TaxService.load_preset(group_key, skip_existing=True)

        return Response(
            {
                "success": True,
                "created": created,
                "skipped": skipped,
            }
        )


@extend_schema_view(
    list=extend_schema(tags=["Tax"], summary=_("List tax preset groups")),
    retrieve=extend_schema(tags=["Tax"], summary=_("Get preset group details")),
)
class TaxPresetViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for tax preset groups and their rates (admin only)."""

    serializer_class = TaxPresetGroupSerializer
    permission_classes = [IsAdminUser]
    queryset = TaxPresetGroup.objects.filter(is_active=True).order_by("region", "name")

    @extend_schema(
        tags=["Tax"],
        summary=_("List rates in a preset group"),
        responses={200: TaxPresetRateSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def rates(self, request, pk=None):
        """Get all rates for a specific preset group."""
        group = self.get_object()
        rates = group.rates.filter(is_active=True).order_by("country", "state")
        serializer = TaxPresetRateSerializer(rates, many=True)
        return Response(serializer.data)


# ==========================================
# Admin AJAX Views
# ==========================================

import json
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone


@staff_member_required
def filter_carts(request):
    """
    AJAX endpoint for filtering shopping carts in admin

    Query Parameters:
    - search: Search by username, email, or session key
    - user_type: Filter by registered/guest
    - status: Filter by active/abandoned/empty
    - shipping: Filter by has_shipping/no_shipping
    - min_value: Minimum cart value
    - max_value: Maximum cart value
    - date_from: Created date from
    - date_to: Created date to
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all carts
    carts = Cart.objects.select_related("user", "shipping_method").prefetch_related("items")

    # Search filter
    search = request.GET.get("search", "").strip()
    if search:
        carts = carts.filter(
            Q(user__username__icontains=search)
            | Q(user__email__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(session_key__icontains=search)
        )

    # User type filter
    user_type = request.GET.get("user_type", "")
    if user_type == "registered":
        carts = carts.filter(user__isnull=False)
    elif user_type == "guest":
        carts = carts.filter(user__isnull=True)

    # Cart status filter
    status_filter = request.GET.get("status", "")
    if status_filter == "active":
        # Updated in last 24 hours
        active_threshold = timezone.now() - timedelta(hours=24)
        carts = carts.filter(updated_at__gte=active_threshold)
    elif status_filter == "abandoned":
        # Not updated in last 24 hours and has items
        abandoned_threshold = timezone.now() - timedelta(hours=24)
        carts = (
            carts.filter(updated_at__lt=abandoned_threshold)
            .annotate(items_count=Count("items"))
            .filter(items_count__gt=0)
        )
    elif status_filter == "empty":
        # No items
        carts = carts.annotate(items_count=Count("items")).filter(items_count=0)

    # Shipping filter
    shipping_filter = request.GET.get("shipping", "")
    if shipping_filter == "has_shipping":
        carts = carts.filter(shipping_method__isnull=False)
    elif shipping_filter == "no_shipping":
        carts = carts.filter(shipping_method__isnull=True)

    # Cart value filters
    min_value = request.GET.get("min_value", "")
    if min_value:
        try:
            min_value = float(min_value)
            # Filter using annotated total - will need to compute in Python
            # For now, we'll fetch all and filter after
        except ValueError:
            pass

    max_value = request.GET.get("max_value", "")
    if max_value:
        try:
            max_value = float(max_value)
        except ValueError:
            pass

    # Date range filters
    date_from = request.GET.get("date_from", "")
    if date_from:
        try:
            from django.utils.dateparse import parse_date

            date_from_parsed = parse_date(date_from)
            if date_from_parsed:
                carts = carts.filter(created_at__date__gte=date_from_parsed)
        except Exception:
            pass

    date_to = request.GET.get("date_to", "")
    if date_to:
        try:
            from django.utils.dateparse import parse_date

            date_to_parsed = parse_date(date_to)
            if date_to_parsed:
                carts = carts.filter(created_at__date__lte=date_to_parsed)
        except Exception:
            pass

    # Order by most recently updated
    carts = carts.order_by("-updated_at")

    # Apply value filters if needed (post-query filtering)
    if min_value or max_value:
        filtered_carts = []
        for cart in carts:
            total = (
                float(cart.total_amount.amount)
                if hasattr(cart.total_amount, "amount")
                else float(cart.total_amount or 0)
            )
            if min_value and total < float(min_value):
                continue
            if max_value and total > float(max_value):
                continue
            filtered_carts.append(cart)
        carts = filtered_carts
        count = len(filtered_carts)
    else:
        count = carts.count()

    # Render results as HTML
    html = render_to_string(
        "admin/cart/partials/cart_cards.html",
        {
            "carts": carts[:100],  # Limit to 100 results
        },
        request=request,
    )

    return JsonResponse({"html": html, "count": count})


# ==========================================
# Tax Rate Admin Views
# ==========================================


@staff_member_required
def filter_tax_rates(request):
    """AJAX endpoint for filtering tax rates in admin."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    from cart.models import TaxRate

    rates = TaxRate.objects.prefetch_related("exempt_categories").all()

    search = request.GET.get("search", "").strip()
    if search:
        rates = rates.filter(
            Q(name__icontains=search)
            | Q(country__icontains=search)
            | Q(state__icontains=search)
            | Q(city__icontains=search)
        )

    country = request.GET.get("country", "")
    if country:
        rates = rates.filter(country=country)

    tax_type = request.GET.get("tax_type", "")
    if tax_type:
        rates = rates.filter(tax_type=tax_type)

    status_filter = request.GET.get("status", "")
    if status_filter == "active":
        rates = rates.filter(is_active=True)
    elif status_filter == "inactive":
        rates = rates.filter(is_active=False)

    rates = rates.order_by("-priority", "country", "state", "city")

    # Add computed properties
    for rate in rates:
        rate.rate_percent = f"{rate.rate * 100}%"
        rate.exempt_count = rate.exempt_categories.count()

    html = render_to_string(
        "admin/cart/taxrate/partials/tax_rate_cards.html", {"tax_rates": rates}, request=request
    )

    return JsonResponse(
        {"html": html, "count": rates.count() if hasattr(rates, "count") else len(rates)}
    )


@staff_member_required
def load_tax_preset(request):
    """AJAX endpoint for loading a tax preset group into active TaxRates."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
        group_key = data.get("group_key", "")
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    if not group_key:
        return JsonResponse({"success": False, "error": "group_key required"}, status=400)

    from cart.services.tax_service import TaxService

    created, skipped = TaxService.load_preset(group_key, skip_existing=True)

    return JsonResponse(
        {
            "success": True,
            "created": created,
            "skipped": skipped,
        }
    )
