"""
API Views for Cart, Wishlist, and Checkout
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsAuthenticatedOrGuestCheckoutAllowed
from core.api.authentication import HeadlessAPIMixin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter

from .models import (
    Cart, CartItem, Wishlist, WishlistItem,
    RecentlyViewed, ShippingMethod, CheckoutSession,
    TaxRate, TaxPresetGroup,
)
from .serializers import (
    CartSerializer, CartSummarySerializer, CartItemSerializer,
    AddToCartSerializer, UpdateCartItemSerializer, ApplyVoucherSerializer,
    ApplyGiftCardSerializer, AppliedGiftCardSerializer,
    WishlistSerializer, WishlistItemSerializer, AddToWishlistSerializer,
    RecentlyViewedSerializer, ShippingMethodSerializer,
    CheckoutSessionSerializer, SetShippingAddressSerializer, SetBillingAddressSerializer,
    SetShippingMethodSerializer, SetPaymentMethodSerializer,
    TaxRateSerializer, TaxPresetGroupSerializer, TaxPresetRateSerializer,
    TaxCalculationRequestSerializer,
)
from .services import CartService, WishlistService, CheckoutService, TaxService


@extend_schema_view(
    list=extend_schema(
        tags=['Cart'],
        summary=_("Get current cart"),
        description=_("Get the current cart for authenticated user or session. Returns cart items, subtotal, discounts, taxes, and total. Automatically creates cart if it doesn't exist.")
    ),
    add=extend_schema(
        tags=['Cart'],
        summary=_("Add item to cart"),
        description=_("Add a product to cart with specified quantity. Optionally include variant ID, customizations, and notes. Validates stock availability and merges with existing cart item if same product/variant. For subscription products, include is_subscription=true with subscription_plan_id, payment_token_id, and optionally pricing_tier_id."),
        request=AddToCartSerializer,
    ),
    update_item=extend_schema(
        tags=['Cart'],
        summary=_("Update cart item"),
        description=_("Update cart item quantity, customizations, or notes. Validates new quantity against stock availability. Returns updated cart with recalculated totals.")
    ),
    remove_item=extend_schema(
        tags=['Cart'],
        summary=_("Remove cart item"),
        description=_("Remove a specific item from cart. Recalculates cart totals and revalidates any applied vouchers against new cart total.")
    ),
    clear=extend_schema(
        tags=['Cart'],
        summary=_("Clear cart"),
        description=_("Remove all items from cart. Also removes any applied vouchers. Cart object persists but becomes empty.")
    ),
    apply_voucher=extend_schema(
        tags=['Cart'],
        summary=_("Apply voucher code"),
        description=_("Apply a voucher code to cart. Validates voucher eligibility, minimum purchase requirements, and usage limits. Calculates and applies discount to cart total.")
    ),
    remove_voucher=extend_schema(
        tags=['Cart'],
        summary=_("Remove voucher"),
        description=_("Remove a specific voucher from cart by code. Recalculates cart total without the voucher discount. User can reapply the voucher later if eligible.")
    ),
    apply_gift_card=extend_schema(
        tags=['Cart'],
        summary=_("Apply gift card"),
        description=_("Apply a gift card code to cart. Validates gift card status, balance, and currency. Gift cards cannot be used to purchase other gift cards. Amount applied is limited to gift card balance or remaining cart total.")
    ),
    remove_gift_card=extend_schema(
        tags=['Cart'],
        summary=_("Remove gift card"),
        description=_("Remove a specific gift card from cart by code. The gift card balance is not affected until checkout is completed. User can reapply the gift card.")
    ),
    summary=extend_schema(
        tags=['Cart'],
        summary=_("Get cart summary"),
        description=_("Get lightweight cart summary with item count, subtotal, and total. Faster than full cart endpoint. Useful for header cart badge or quick total display.")
    )
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
            return CartService.get_or_create_cart(session_key=session_key)

    def list(self, request):
        """Get current cart"""
        cart = self.get_cart(request)
        serializer = self.get_serializer(cart)
        data = serializer.data

        # Add display-only mode metadata for dual-currency display
        from core.models import SiteSettings
        settings = SiteSettings.get_settings()
        if (settings.enable_multi_currency
                and getattr(settings, 'multi_currency_checkout_mode', 'full') == 'display_only'):
            visitor_currency = (
                getattr(request, 'currency', None)
                or request.session.get('currency')
            )
            if visitor_currency and visitor_currency != settings.default_currency:
                try:
                    from exchange_rates.services.exchange_service import ExchangeRateService
                    fx_service = ExchangeRateService()
                    rate = fx_service.get_rate(settings.default_currency, visitor_currency)
                    data['display_only_mode'] = True
                    data['display_currency'] = visitor_currency
                    data['charge_currency'] = settings.default_currency
                    data['display_exchange_rate'] = float(rate) if rate else None
                except Exception:
                    pass

        return Response(data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add item to cart"""
        serializer = AddToCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        cart = self.get_cart(request)

        # Get customer's active currency from middleware
        customer_currency = (
            getattr(request, 'currency', None)
            or request.session.get('currency')
        )

        success, message, cart_item = CartService.add_item(
            cart=cart,
            product_id=serializer.validated_data['product_id'],
            quantity=serializer.validated_data['quantity'],
            variant_id=serializer.validated_data.get('variant_id'),
            customizations=serializer.validated_data.get('customizations', {}),
            notes=serializer.validated_data.get('notes', ''),
            variant_selections=serializer.validated_data.get('variant_selections'),
            excluded_optional_items=serializer.validated_data.get('excluded_optional_items'),
            configuration=serializer.validated_data.get('configuration'),
            preset_id=serializer.validated_data.get('preset_id'),
            booking_data=serializer.validated_data.get('booking_data'),
            is_subscription=serializer.validated_data.get('is_subscription', False),
            subscription_plan=serializer.validated_data.get('subscription_plan'),
            pricing_tier=serializer.validated_data.get('pricing_tier'),
            payment_token=serializer.validated_data.get('payment_token'),
            customer_currency=customer_currency,
        )

        if success:
            cart_serializer = CartSerializer(cart)

            # Also include mini-cart formatted data for frontend
            from .mini_cart_api import format_cart_for_minicart
            mini_cart_data = format_cart_for_minicart(
                cart,
                just_added_item_id=cart_item.id if cart_item else None
            )

            return Response({
                'success': True,
                'message': str(message),
                'cart': cart_serializer.data,
                # Mini-cart fields for frontend
                'cart_count': mini_cart_data['cart_count'],
                'item_count': mini_cart_data['item_count'],
                'items': mini_cart_data['items'],
                'subtotal': mini_cart_data['subtotal'],
                'subtotal_formatted': mini_cart_data['subtotal_formatted'],
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='items/(?P<item_id>[^/.]+)')
    def update_item(self, request, item_id=None):
        """Update cart item quantity or customizations"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        # Guard: reject operations on child/component items
        if cart_item.parent_bundle is not None:
            return Response({
                'success': False,
                'message': str(_("Component items cannot be modified directly. Update the parent product instead."))
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success, message = CartService.update_item(
            cart_item=cart_item,
            quantity=serializer.validated_data.get('quantity'),
            customizations=serializer.validated_data.get('customizations'),
            notes=serializer.validated_data.get('notes')
        )

        if success:
            cart_serializer = CartSerializer(cart)
            return Response({
                'success': True,
                'message': str(message),
                'cart': cart_serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """Remove item from cart"""
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        # Guard: reject removal of child/component items
        if cart_item.parent_bundle is not None:
            return Response({
                'success': False,
                'message': str(_("Component items cannot be removed directly. Remove the parent product instead."))
            }, status=status.HTTP_400_BAD_REQUEST)

        success, message = CartService.remove_item(cart_item)

        cart_serializer = CartSerializer(cart)
        return Response({
            'success': True,
            'message': str(message),
            'cart': cart_serializer.data
        })

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from cart"""
        cart = self.get_cart(request)
        success, message = CartService.clear_cart(cart)

        return Response({
            'success': True,
            'message': str(message)
        })

    @action(detail=False, methods=['post'], url_path='apply-voucher')
    def apply_voucher(self, request):
        """Apply voucher code to cart"""
        serializer = ApplyVoucherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self.get_cart(request)
        user = request.user if request.user.is_authenticated else None

        success, message, discount_amount = CartService.apply_voucher(
            cart=cart,
            voucher_code=serializer.validated_data['code'],
            user=user
        )

        if success:
            cart_serializer = CartSerializer(cart)
            return Response({
                'success': True,
                'message': str(message),
                'discount_amount': float(discount_amount),
                'cart': cart_serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='remove-voucher/(?P<code>[^/.]+)')
    def remove_voucher(self, request, code=None):
        """Remove voucher from cart"""
        cart = self.get_cart(request)
        success, message = CartService.remove_voucher(cart, code)

        if success:
            cart_serializer = CartSerializer(cart)
            return Response({
                'success': True,
                'message': str(message),
                'cart': cart_serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get cart summary (lightweight)"""
        cart = self.get_cart(request)
        summary = CartService.get_cart_summary(cart)
        return Response(summary)

    @action(detail=False, methods=['post'], url_path='apply-gift-card')
    def apply_gift_card(self, request):
        """Apply gift card code to cart"""
        serializer = ApplyGiftCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = self.get_cart(request)

        # Get customer's active currency for foreign-currency gift card validation
        customer_currency = (
            request.session.get('currency')
            or getattr(request, 'currency', None)
            or None
        )

        success, message, discount_amount = CartService.apply_gift_card(
            cart=cart,
            gift_card_code=serializer.validated_data['code'],
            customer_currency=customer_currency,
        )

        if success:
            cart_serializer = CartSerializer(cart)
            return Response({
                'success': True,
                'message': str(message),
                'discount_applied': float(discount_amount),
                'cart': cart_serializer.data,
                'applied_gift_cards': cart.get_gift_card_summary()
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='remove-gift-card/(?P<code>[^/.]+)')
    def remove_gift_card(self, request, code=None):
        """Remove gift card from cart"""
        cart = self.get_cart(request)
        success, message = CartService.remove_gift_card(cart, code)

        if success:
            cart_serializer = CartSerializer(cart)
            return Response({
                'success': True,
                'message': str(message),
                'cart': cart_serializer.data,
                'applied_gift_cards': cart.get_gift_card_summary()
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    list=extend_schema(
        tags=['Wishlist'],
        summary=_("List user wishlists"),
        description=_("Get all wishlists for the authenticated user. Users can have multiple wishlists for different purposes (e.g., 'Birthday', 'Wedding', 'Ideas'). Returns wishlist names, item counts, and privacy settings.")
    ),
    create=extend_schema(
        tags=['Wishlist'],
        summary=_("Create wishlist"),
        description=_("Create a new wishlist for the authenticated user. Specify name, description, and privacy setting (public/private). Public wishlists can be shared via URL.")
    ),
    retrieve=extend_schema(
        tags=['Wishlist'],
        summary=_("Get wishlist details"),
        description=_("Get detailed information about a specific wishlist including all items, prices, availability, and sharing settings. Only accessible to wishlist owner unless publicly shared.")
    ),
    update=extend_schema(
        tags=['Wishlist'],
        summary=_("Update wishlist"),
        description=_("Update wishlist information including name, description, or privacy settings. Can make wishlist public or private. Only owner can update.")
    ),
    partial_update=extend_schema(
        tags=['Wishlist'],
        summary=_("Partially update wishlist"),
        description=_("Update specific wishlist fields without sending full wishlist data. Useful for toggling privacy or renaming wishlist.")
    ),
    destroy=extend_schema(
        tags=['Wishlist'],
        summary=_("Delete wishlist"),
        description=_("Permanently delete a wishlist and all its items. Cannot be undone. Only owner can delete.")
    ),
    add=extend_schema(
        tags=['Wishlist'],
        summary=_("Add item to wishlist"),
        description=_("Add a product to wishlist with optional variant, quantity, and notes. Prevents duplicates. Can add to default wishlist or specify wishlist ID.")
    ),
    remove_item=extend_schema(
        tags=['Wishlist'],
        summary=_("Remove item from wishlist"),
        description=_("Remove a specific item from wishlist. Item can be added back later. Does not affect product availability.")
    ),
    move_to_cart=extend_schema(
        tags=['Wishlist'],
        summary=_("Move item to cart"),
        description=_("Move a wishlist item directly to shopping cart. Validates stock availability. Item is removed from wishlist after successful cart addition.")
    ),
    get_shared=extend_schema(
        tags=['Wishlist'],
        summary=_("Get public wishlist by share slug"),
        description=_("View a public wishlist using its share URL slug. Anyone with the link can view public wishlists. Useful for gift registries and wish lists shared with family/friends.")
    ),
    product_ids=extend_schema(
        tags=['Wishlist'],
        summary=_("Get wishlisted product IDs"),
        description=_("Returns a mapping of product IDs to wishlist item IDs for the current user's default wishlist. Used by the storefront to show wishlist heart icons on product listings without fetching full wishlist data."),
        responses={
            200: OpenApiResponse(
                description=_("Map of product IDs to wishlist item IDs"),
                response={
                    'type': 'object',
                    'properties': {
                        'wishlisted': {
                            'type': 'object',
                            'additionalProperties': {'type': 'integer'},
                            'description': _('Keys are product IDs (as strings), values are wishlist item IDs'),
                            'example': {'42': 7, '108': 12}
                        }
                    }
                }
            ),
            401: OpenApiResponse(description=_("Authentication required")),
        }
    )
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
        return Wishlist.objects.filter(user=self.request.user).prefetch_related('items__product')

    def perform_create(self, serializer):
        """Create wishlist for current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add item to wishlist"""
        serializer = AddToWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get or create wishlist
        if serializer.validated_data.get('wishlist_id'):
            wishlist = get_object_or_404(
                Wishlist,
                id=serializer.validated_data['wishlist_id'],
                user=request.user
            )
        else:
            wishlist = WishlistService.get_or_create_default_wishlist(request.user)

        success, message, wishlist_item = WishlistService.add_item(
            wishlist=wishlist,
            product_id=serializer.validated_data['product_id'],
            variant_id=serializer.validated_data.get('variant_id'),
            notes=serializer.validated_data.get('notes', ''),
            priority=serializer.validated_data.get('priority', 'medium'),
            notify_when_available=serializer.validated_data.get('notify_when_available', False),
            notify_when_on_sale=serializer.validated_data.get('notify_when_on_sale', False)
        )

        if success:
            wishlist_serializer = WishlistSerializer(wishlist)
            return Response({
                'success': True,
                'message': str(message),
                'wishlist': wishlist_serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='item_id',
                type=int,
                location=OpenApiParameter.PATH,
                description=_('ID of the wishlist item to remove')
            )
        ]
    )
    @action(detail=False, methods=['delete'], url_path='items/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """Remove item from wishlist"""
        wishlist_item = get_object_or_404(
            WishlistItem,
            id=item_id,
            wishlist__user=request.user
        )

        success, message = WishlistService.remove_item(wishlist_item)

        return Response({
            'success': True,
            'message': str(message)
        })

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='item_id',
                type=int,
                location=OpenApiParameter.PATH,
                description=_('ID of the wishlist item to move to cart')
            )
        ]
    )
    @action(detail=False, methods=['post'], url_path='items/(?P<item_id>[^/.]+)/move-to-cart')
    def move_to_cart(self, request, item_id=None):
        """Move wishlist item to cart"""
        wishlist_item = get_object_or_404(
            WishlistItem,
            id=item_id,
            wishlist__user=request.user
        )

        # Get cart
        from .views import CartViewSet
        cart_viewset = CartViewSet()
        cart = cart_viewset.get_cart(request)

        quantity = request.data.get('quantity', 1)
        success, message = WishlistService.move_to_cart(wishlist_item, cart, quantity)

        if success:
            return Response({
                'success': True,
                'message': str(message)
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='slug',
                type=str,
                location=OpenApiParameter.PATH,
                description=_('Share slug of the public wishlist')
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='shared/(?P<slug>[^/.]+)', permission_classes=[AllowAny])
    def get_shared(self, request, slug=None):
        """Get public wishlist by share slug"""
        wishlist = WishlistService.get_public_wishlist(slug)

        if not wishlist:
            return Response({
                'success': False,
                'message': _("Wishlist not found")
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(wishlist)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='product-ids', permission_classes=[AllowAny])
    def product_ids(self, request):
        """Return wishlisted product IDs with their wishlist item IDs for the current user's default wishlist.

        Called on every storefront page to render heart-button state, so guests
        must get a valid empty response rather than a 401.
        """
        if not request.user.is_authenticated:
            return Response({'wishlisted': {}})
        wishlist = WishlistService.get_or_create_default_wishlist(request.user)
        items = wishlist.items.values_list('id', 'product_id')
        wishlisted = {str(product_id): item_id for item_id, product_id in items}
        return Response({'wishlisted': wishlisted})


@extend_schema_view(
    list=extend_schema(tags=['Checkout'], summary=_("Get checkout session")),
    set_shipping_address=extend_schema(tags=['Checkout'], summary=_("Set shipping address")),
    set_billing_address=extend_schema(tags=['Checkout'], summary=_("Set billing address")),
    get_shipping_methods=extend_schema(tags=['Checkout'], summary=_("Get available shipping methods")),
    get_payment_providers=extend_schema(
        tags=['Checkout'],
        summary=_("Get available payment providers"),
        description=_("Returns payment providers available for the customer's country and currency. Filters based on shipping countries, provider capabilities, and merchant configuration.")
    ),
    set_shipping_method=extend_schema(tags=['Checkout'], summary=_("Set shipping method")),
    set_payment_method=extend_schema(tags=['Checkout'], summary=_("Set payment method")),
    validate=extend_schema(tags=['Checkout'], summary=_("Validate checkout")),
    complete=extend_schema(tags=['Checkout'], summary=_("Complete checkout"))
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
        return Response({
            'success': True,
            'session': serializer.data
        })

    @action(detail=False, methods=['post'], url_path='shipping-address')
    def set_shipping_address(self, request):
        """Set shipping address for checkout"""
        serializer = SetShippingAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = self.get_session(request)

        address_data = None
        if not serializer.validated_data.get('address_id'):
            address_data = {
                'address_type': 'shipping',
                'name': serializer.validated_data['name'],
                'company': serializer.validated_data.get('company', ''),
                'address1': serializer.validated_data['address1'],
                'address2': serializer.validated_data.get('address2', ''),
                'city': serializer.validated_data['city'],
                'state': serializer.validated_data.get('state', ''),
                'postal_code': serializer.validated_data['postal_code'],
                'country': serializer.validated_data['country'],
                'phone': serializer.validated_data.get('phone', ''),
            }

        success, message = CheckoutService.set_shipping_address(
            session=session,
            address_id=serializer.validated_data.get('address_id'),
            address_data=address_data,
            email=serializer.validated_data.get('email')
        )

        if success:
            session_serializer = self.get_serializer(session)
            return Response({
                'success': True,
                'message': str(message),
                'session': session_serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='billing-address')
    def set_billing_address(self, request):
        """Set billing address for checkout"""
        serializer = SetBillingAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = self.get_session(request)

        same_as_shipping = serializer.validated_data.get('same_as_shipping', True)
        address_id = serializer.validated_data.get('address_id')

        address_data = None
        if not same_as_shipping and not address_id:
            address_data = {
                'address_type': 'billing',
                'name': serializer.validated_data.get('name', ''),
                'company': serializer.validated_data.get('company', ''),
                'address1': serializer.validated_data.get('address1', ''),
                'address2': serializer.validated_data.get('address2', ''),
                'city': serializer.validated_data.get('city', ''),
                'state': serializer.validated_data.get('state', ''),
                'postal_code': serializer.validated_data.get('postal_code', ''),
                'country': serializer.validated_data.get('country', ''),
                'phone': serializer.validated_data.get('phone', ''),
            }

        success, message = CheckoutService.set_billing_address(
            session=session,
            same_as_shipping=same_as_shipping,
            address_id=address_id,
            address_data=address_data
        )

        if success:
            session_serializer = self.get_serializer(session)
            return Response({
                'success': True,
                'message': str(message),
                'session': session_serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='shipping-methods')
    def get_shipping_methods(self, request):
        """Get available shipping methods"""
        session = self.get_session(request)

        refresh = request.query_params.get('refresh', 'false').lower() == 'true'
        methods = CheckoutService.get_available_shipping_methods(session, refresh=refresh)

        return Response({
            'shipping_methods': methods
        })

    @action(detail=False, methods=['get'], url_path='payment-providers')
    def get_payment_providers(self, request):
        """Get available payment providers for checkout"""
        session = self.get_session(request)

        # Get available providers based on shipping country and currency
        available_providers = CheckoutService.get_available_payment_providers(session)

        # Get customer country for serializer context
        customer_country = None
        address = session.shipping_address or session.shipping_address_data
        if address:
            customer_country = address.country if hasattr(address, 'country') else address.get('country')
            # Normalize country to ISO code (handles both "Australia" and "AU")
            if customer_country:
                from payment_providers.services.payment_method_filter import PaymentMethodFilter
                customer_country = PaymentMethodFilter._normalize_country_code(customer_country)

        # Serialize provider data
        from payment_providers.serializers import PaymentProviderAccountSerializer
        serializer = PaymentProviderAccountSerializer(
            available_providers,
            many=True,
            context={
                'request': request,
                'customer_country': customer_country
            }
        )

        return Response({
            'payment_providers': serializer.data
        })

    @action(detail=False, methods=['post'], url_path='shipping-method')
    def set_shipping_method(self, request):
        """Select shipping method"""
        serializer = SetShippingMethodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = self.get_session(request)

        success, message = CheckoutService.set_shipping_method(
            session=session,
            shipping_method_id=serializer.validated_data['shipping_method_id']
        )

        if success:
            session_serializer = self.get_serializer(session)
            return Response({
                'success': True,
                'message': str(message),
                'session': session_serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='payment-method')
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
        provider_id = serializer.validated_data.get('payment_provider_id')
        if not provider_id:
            provider_slug = serializer.validated_data.get('provider')
            from payment_providers.models import PaymentProviderAccount
            account = (
                PaymentProviderAccount.objects
                .filter(component__slug=provider_slug, is_active=True)
                .order_by('-is_default', 'sort_order', 'created_at')
                .first()
            )
            if not account:
                return Response({
                    'success': False,
                    'message': f'Payment provider "{provider_slug}" not found.'
                }, status=status.HTTP_400_BAD_REQUEST)
            provider_id = account.id

        success, message = CheckoutService.set_payment_method(
            session=session,
            payment_provider_id=provider_id
        )

        if success:
            session_serializer = self.get_serializer(session)
            return Response({
                'success': True,
                'message': str(message),
                'session': session_serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def validate(self, request):
        """Validate checkout is ready for payment"""
        session = self.get_session(request)

        is_valid, errors = CheckoutService.validate_checkout(session)

        return Response({
            'is_valid': is_valid,
            'errors': [str(e) for e in errors]
        })

    @action(detail=False, methods=['post'])
    def complete(self, request):
        """Complete checkout and create order"""
        session = self.get_session(request)

        success, message, order = CheckoutService.create_order(session)

        if success:
            from orders.serializers import OrderSerializer
            order_serializer = OrderSerializer(order)
            return Response({
                'success': True,
                'message': str(message),
                'order': order_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': str(message)
            }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(tags=['Cart'], summary=_("Get recently viewed products")),
    retrieve=extend_schema(tags=['Cart'], summary=_("Get recently viewed details"))
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
            return RecentlyViewed.objects.filter(
                user=self.request.user
            ).select_related('product')[:20]
        else:
            session_key = self.request.session.session_key
            if session_key:
                return RecentlyViewed.objects.filter(
                    session_key=session_key
                ).select_related('product')[:20]
            return RecentlyViewed.objects.none()


@extend_schema_view(
    list=extend_schema(tags=['Shipping'], summary=_("List shipping methods")),
    retrieve=extend_schema(tags=['Shipping'], summary=_("Get shipping method details"))
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
    list=extend_schema(tags=['Tax'], summary=_('List tax rates')),
    retrieve=extend_schema(tags=['Tax'], summary=_('Get tax rate details')),
    create=extend_schema(tags=['Tax'], summary=_('Create tax rate')),
    update=extend_schema(tags=['Tax'], summary=_('Update tax rate')),
    partial_update=extend_schema(tags=['Tax'], summary=_('Partial update tax rate')),
    destroy=extend_schema(tags=['Tax'], summary=_('Delete tax rate')),
)
class TaxRateViewSet(viewsets.ModelViewSet):
    """CRUD API for tax rates (admin only)."""
    serializer_class = TaxRateSerializer
    permission_classes = [IsAdminUser]
    queryset = TaxRate.objects.all().order_by('-priority', 'country', 'state')

    @extend_schema(
        tags=['Tax'],
        summary=_('Calculate applicable taxes'),
        request=TaxCalculationRequestSerializer,
        responses={200: dict},
    )
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """Calculate taxes for a given address and items."""
        serializer = TaxCalculationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        from catalog.models import Product
        from decimal import Decimal

        items = []
        for item_data in data['items']:
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except Product.DoesNotExist:
                return Response(
                    {'error': f"Product {item_data['product_id']} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            line_total = Decimal(str(item_data['price'])) * item_data['quantity']
            items.append((product, item_data['quantity'], line_total))

        total_tax, breakdown = TaxService.calculate_tax(
            items=items,
            shipping_cost=data.get('shipping_cost', Decimal('0')),
            country=data['country'],
            state=data.get('state', ''),
            city=data.get('city', ''),
            postal_code=data.get('postal_code', ''),
        )

        return Response({
            'total_tax': str(total_tax),
            'breakdown': breakdown,
        })

    @extend_schema(
        tags=['Tax'],
        summary=_('Tax rates grouped by country'),
        responses={200: dict},
    )
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Return tax rates grouped by country."""
        from django.db.models import Count
        from collections import OrderedDict

        rates = TaxRate.objects.filter(is_active=True).order_by('country', 'state')
        grouped = OrderedDict()
        for rate in rates:
            if rate.country not in grouped:
                grouped[rate.country] = []
            grouped[rate.country].append(TaxRateSerializer(rate).data)

        return Response(grouped)

    @extend_schema(
        tags=['Tax'],
        summary=_('Load preset tax rates'),
        request={'type': 'object', 'properties': {
            'group_key': {'type': 'string'},
        }},
        responses={200: dict},
    )
    @action(detail=False, methods=['post'], url_path='load-preset')
    def load_preset(self, request):
        """Load a preset tax configuration into active TaxRates."""
        group_key = request.data.get('group_key', '')
        if not group_key:
            return Response(
                {'error': 'group_key is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created, skipped = TaxService.load_preset(group_key, skip_existing=True)

        return Response({
            'success': True,
            'created': created,
            'skipped': skipped,
        })


@extend_schema_view(
    list=extend_schema(tags=['Tax'], summary=_('List tax preset groups')),
    retrieve=extend_schema(tags=['Tax'], summary=_('Get preset group details')),
)
class TaxPresetViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for tax preset groups and their rates (admin only)."""
    serializer_class = TaxPresetGroupSerializer
    permission_classes = [IsAdminUser]
    queryset = TaxPresetGroup.objects.filter(is_active=True).order_by('region', 'name')

    @extend_schema(
        tags=['Tax'],
        summary=_('List rates in a preset group'),
        responses={200: TaxPresetRateSerializer(many=True)},
    )
    @action(detail=True, methods=['get'])
    def rates(self, request, pk=None):
        """Get all rates for a specific preset group."""
        group = self.get_object()
        rates = group.rates.filter(is_active=True).order_by('country', 'state')
        serializer = TaxPresetRateSerializer(rates, many=True)
        return Response(serializer.data)


# ==========================================
# Admin AJAX Views
# ==========================================

import json
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta


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
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Start with all carts
    carts = Cart.objects.select_related('user', 'shipping_method').prefetch_related('items')

    # Search filter
    search = request.GET.get('search', '').strip()
    if search:
        carts = carts.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(session_key__icontains=search)
        )

    # User type filter
    user_type = request.GET.get('user_type', '')
    if user_type == 'registered':
        carts = carts.filter(user__isnull=False)
    elif user_type == 'guest':
        carts = carts.filter(user__isnull=True)

    # Cart status filter
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        # Updated in last 24 hours
        active_threshold = timezone.now() - timedelta(hours=24)
        carts = carts.filter(updated_at__gte=active_threshold)
    elif status_filter == 'abandoned':
        # Not updated in last 24 hours and has items
        abandoned_threshold = timezone.now() - timedelta(hours=24)
        carts = carts.filter(updated_at__lt=abandoned_threshold).annotate(
            items_count=Count('items')
        ).filter(items_count__gt=0)
    elif status_filter == 'empty':
        # No items
        carts = carts.annotate(items_count=Count('items')).filter(items_count=0)

    # Shipping filter
    shipping_filter = request.GET.get('shipping', '')
    if shipping_filter == 'has_shipping':
        carts = carts.filter(shipping_method__isnull=False)
    elif shipping_filter == 'no_shipping':
        carts = carts.filter(shipping_method__isnull=True)

    # Cart value filters
    min_value = request.GET.get('min_value', '')
    if min_value:
        try:
            min_value = float(min_value)
            # Filter using annotated total - will need to compute in Python
            # For now, we'll fetch all and filter after
        except ValueError:
            pass

    max_value = request.GET.get('max_value', '')
    if max_value:
        try:
            max_value = float(max_value)
        except ValueError:
            pass

    # Date range filters
    date_from = request.GET.get('date_from', '')
    if date_from:
        try:
            from django.utils.dateparse import parse_date
            date_from_parsed = parse_date(date_from)
            if date_from_parsed:
                carts = carts.filter(created_at__date__gte=date_from_parsed)
        except:
            pass

    date_to = request.GET.get('date_to', '')
    if date_to:
        try:
            from django.utils.dateparse import parse_date
            date_to_parsed = parse_date(date_to)
            if date_to_parsed:
                carts = carts.filter(created_at__date__lte=date_to_parsed)
        except:
            pass

    # Order by most recently updated
    carts = carts.order_by('-updated_at')

    # Apply value filters if needed (post-query filtering)
    if min_value or max_value:
        filtered_carts = []
        for cart in carts:
            total = float(cart.total_amount.amount) if hasattr(cart.total_amount, 'amount') else float(cart.total_amount or 0)
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
    html = render_to_string('admin/cart/partials/cart_cards.html', {
        'carts': carts[:100],  # Limit to 100 results
    }, request=request)

    return JsonResponse({
        'html': html,
        'count': count
    })


# ==========================================
# Tax Rate Admin Views
# ==========================================

@staff_member_required
def filter_tax_rates(request):
    """AJAX endpoint for filtering tax rates in admin."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    from cart.models import TaxRate

    rates = TaxRate.objects.prefetch_related('exempt_categories').all()

    search = request.GET.get('search', '').strip()
    if search:
        rates = rates.filter(
            Q(name__icontains=search) |
            Q(country__icontains=search) |
            Q(state__icontains=search) |
            Q(city__icontains=search)
        )

    country = request.GET.get('country', '')
    if country:
        rates = rates.filter(country=country)

    tax_type = request.GET.get('tax_type', '')
    if tax_type:
        rates = rates.filter(tax_type=tax_type)

    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        rates = rates.filter(is_active=True)
    elif status_filter == 'inactive':
        rates = rates.filter(is_active=False)

    rates = rates.order_by('-priority', 'country', 'state', 'city')

    # Add computed properties
    for rate in rates:
        rate.rate_percent = f"{rate.rate * 100}%"
        rate.exempt_count = rate.exempt_categories.count()

    html = render_to_string(
        'admin/cart/taxrate/partials/tax_rate_cards.html',
        {'tax_rates': rates},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': rates.count() if hasattr(rates, 'count') else len(rates)
    })


@staff_member_required
def load_tax_preset(request):
    """AJAX endpoint for loading a tax preset group into active TaxRates."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
        group_key = data.get('group_key', '')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    if not group_key:
        return JsonResponse({'success': False, 'error': 'group_key required'}, status=400)

    from cart.services.tax_service import TaxService

    created, skipped = TaxService.load_preset(group_key, skip_existing=True)

    return JsonResponse({
        'success': True,
        'created': created,
        'skipped': skipped,
    })
