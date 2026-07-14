"""
Mini-cart API endpoints for the slide-out cart component.

Provides a lightweight DRF-based interface for cart operations used by
the frontend mini-cart JavaScript module.
"""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import serializers, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.api.authentication import HeadlessAPIMixin

from .models import CartItem
from .services import CartService
from .services.cart_recommendation_service import CartRecommendationService


def _format_price(amount, currency_code):
    """Format a price amount with the correct currency symbol using Babel."""
    try:
        from babel.numbers import format_currency as babel_format_currency
        from django.utils.translation import get_language

        locale = get_language() or "en"
        return babel_format_currency(amount, currency_code, locale=locale)
    except Exception:
        return f"{currency_code} {amount:.2f}"


# =============================================================================
# Serializers for API Documentation
# =============================================================================


class CartItemSerializer(serializers.Serializer):
    """Serializer for cart item in mini-cart response."""

    id = serializers.IntegerField(help_text="Cart item ID")
    product_id = serializers.IntegerField(help_text="Product ID")
    name = serializers.CharField(help_text="Product name")
    variant_name = serializers.CharField(
        allow_null=True, help_text="Variant name (e.g., 'Large / Blue')"
    )
    quantity = serializers.IntegerField(help_text="Item quantity")
    price = serializers.CharField(help_text="Unit price as string")
    price_formatted = serializers.CharField(help_text="Formatted price (e.g., '$29.99')")
    image_url = serializers.CharField(allow_null=True, help_text="Product/variant image URL")
    url = serializers.CharField(help_text="Product detail page URL")
    just_added = serializers.BooleanField(
        help_text="Whether this item was just added (for highlighting)"
    )


class MiniCartResponseSerializer(serializers.Serializer):
    """Serializer for mini-cart GET response."""

    success = serializers.BooleanField(help_text="Operation success status")
    item_count = serializers.IntegerField(help_text="Total number of items in cart")
    cart_count = serializers.IntegerField(help_text="Alias for item_count")
    items = CartItemSerializer(many=True, help_text="List of cart items")
    subtotal = serializers.CharField(help_text="Cart subtotal as string")
    subtotal_formatted = serializers.CharField(help_text="Formatted subtotal (e.g., '$99.99')")


class CartUpdateRequestSerializer(serializers.Serializer):
    """Serializer for cart update request."""

    item_id = serializers.IntegerField(required=True, help_text="Cart item ID to update")
    quantity = serializers.IntegerField(
        required=True, min_value=0, help_text="New quantity (0 to remove item)"
    )


class CartRemoveRequestSerializer(serializers.Serializer):
    """Serializer for cart remove request."""

    item_id = serializers.IntegerField(required=True, help_text="Cart item ID to remove")


class CartErrorResponseSerializer(serializers.Serializer):
    """Serializer for cart error responses."""

    success = serializers.BooleanField(default=False, help_text="Always false for errors")
    message = serializers.CharField(help_text="Error message")


class RecommendationProductSerializer(serializers.Serializer):
    """Serializer for a recommended product."""

    id = serializers.IntegerField(help_text="Product ID")
    name = serializers.CharField(help_text="Product name")
    slug = serializers.CharField(help_text="Product URL slug")
    url = serializers.CharField(help_text="Product detail page URL")
    image_url = serializers.CharField(allow_null=True, help_text="Product image URL")
    price = serializers.FloatField(help_text="Product price")
    price_formatted = serializers.CharField(help_text="Formatted price (e.g., '$29.99')")
    on_sale = serializers.BooleanField(help_text="Whether product is on sale")
    sale_price = serializers.FloatField(allow_null=True, help_text="Sale price if on sale")
    sale_price_formatted = serializers.CharField(allow_null=True, help_text="Formatted sale price")
    category = serializers.CharField(allow_null=True, help_text="Product category name")


class RecommendationSectionSerializer(serializers.Serializer):
    """Serializer for a recommendation section."""

    type = serializers.ChoiceField(
        choices=["recently_viewed", "related", "on_sale", "trending", "featured"],
        help_text="Section type identifier",
    )
    label = serializers.CharField(help_text="Display label for section (e.g., 'Continue Shopping')")
    products = RecommendationProductSerializer(many=True, help_text="Products in this section")


class CartRecommendationsResponseSerializer(serializers.Serializer):
    """Serializer for cart recommendations response."""

    sections = RecommendationSectionSerializer(
        many=True, help_text="Recommendation sections with labels and products"
    )
    total_count = serializers.IntegerField(help_text="Total number of recommended products")


# =============================================================================
# Helper Functions
# =============================================================================


def get_cart_for_request(request):
    """Get or create cart for current user/session."""
    if request.user.is_authenticated:
        return CartService.get_or_create_cart(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        return CartService.get_or_create_cart(session_key=session_key)


def format_cart_for_minicart(cart, just_added_item_id=None):
    """Format cart data for the mini-cart component."""
    items = []
    currency_code = cart.effective_currency

    # Only return parent/top-level items (exclude child components)
    parent_items = cart.items.select_related("product", "variant").filter(
        parent_bundle__isnull=True
    )

    for item in parent_items:
        # Get image URL (use thumbnails to save bandwidth)
        image_url = None
        if item.variant and item.variant.image_asset:
            image_url = item.variant.image_asset.thumbnail_small
        elif hasattr(item.product, "primary_image"):
            primary_img = item.product.primary_image
            if primary_img:
                image_url = (
                    primary_img.get_thumbnail("small")
                    if hasattr(primary_img, "get_thumbnail")
                    else primary_img.get_display_url()
                )

        # Get product URL
        product_url = reverse(
            "page_builder:product_detail", kwargs={"product_slug": item.product.slug}
        )

        # Format variant name
        variant_name = None
        if item.variant:
            variant_name = item.variant.name

        # Format price — extract Decimal and use cart currency for formatting
        price = item.unit_price
        item_currency = currency_code
        if hasattr(price, "currency"):
            item_currency = str(price.currency)
        if hasattr(price, "amount"):
            price = price.amount

        # Calculate item total (price × quantity)
        item_total = price * item.quantity

        item_data = {
            "id": item.id,
            "product_id": item.product.id,
            "name": item.product.name,
            "variant_name": variant_name,
            "quantity": item.quantity,
            "price": str(price),
            "price_formatted": _format_price(price, item_currency),
            "item_total": str(item_total),
            "item_total_formatted": _format_price(item_total, item_currency),
            "image_url": image_url,
            "url": product_url,
            "just_added": item.id == just_added_item_id,
            "is_configurable": False,
            "components": [],
        }

        # Include component breakdown for configurable/bundle products
        children = cart.items.filter(parent_bundle=item).select_related(
            "product", "variant", "variant__image_asset"
        )
        if children.exists():
            item_data["is_configurable"] = True
            for child in children:
                child_price = child.unit_price
                child_currency = currency_code
                if hasattr(child_price, "currency"):
                    child_currency = str(child_price.currency)
                if hasattr(child_price, "amount"):
                    child_price = child_price.amount

                # Get component image (use small thumbnail for mini-cart)
                child_image_url = None
                if child.variant and child.variant.image_asset:
                    child_image_url = child.variant.image_asset.thumbnail_small
                elif hasattr(child.product, "primary_image"):
                    pi = child.product.primary_image
                    if pi:
                        child_image_url = (
                            pi.get_thumbnail("small")
                            if hasattr(pi, "get_thumbnail")
                            else pi.get_display_url()
                        )

                item_data["components"].append(
                    {
                        "id": child.id,
                        "name": str(child.product.name),
                        "variant_name": child.variant.name if child.variant else None,
                        "quantity": child.quantity,
                        "price": str(child_price),
                        "price_formatted": _format_price(child_price, child_currency),
                        "image_url": child_image_url,
                    }
                )

        items.append(item_data)

    # Calculate totals
    subtotal = cart.subtotal
    subtotal_currency = currency_code
    if hasattr(subtotal, "currency"):
        subtotal_currency = str(subtotal.currency)
    if hasattr(subtotal, "amount"):
        subtotal = subtotal.amount

    # Count only parent items for display
    parent_count = parent_items.count()

    return {
        "success": True,
        "item_count": parent_count,
        "cart_count": parent_count,
        "currency": subtotal_currency,
        "items": items,
        "subtotal": str(subtotal),
        "subtotal_formatted": _format_price(subtotal, subtotal_currency),
    }


# =============================================================================
# API Endpoints
# =============================================================================


@extend_schema(
    summary=_("Get mini-cart data"),
    description=_("""
    Retrieve the current cart contents formatted for the mini-cart component.

    Works for both authenticated users (cart linked to user account) and
    anonymous users (cart linked to session). Cart data includes all items
    with product details, quantities, prices, and images.

    **Use Cases:**
    - Initial mini-cart load on page
    - Refreshing cart after external changes
    - Checking cart status before checkout

    **Authentication:** None required (uses session for anonymous users)
    """),
    tags=["Cart"],
    responses={
        200: OpenApiResponse(
            response=MiniCartResponseSerializer,
            description=_("Cart data retrieved successfully"),
            examples=[
                OpenApiExample(
                    "Cart with items",
                    value={
                        "success": True,
                        "item_count": 2,
                        "cart_count": 2,
                        "items": [
                            {
                                "id": 1,
                                "product_id": 42,
                                "name": "Classic T-Shirt",
                                "variant_name": "Large / Blue",
                                "quantity": 2,
                                "price": "29.99",
                                "price_formatted": "$29.99",
                                "image_url": "/media/products/tshirt.jpg",
                                "url": "/products/classic-t-shirt/",
                                "just_added": False,
                            }
                        ],
                        "subtotal": "59.98",
                        "subtotal_formatted": "$59.98",
                    },
                ),
                OpenApiExample(
                    "Empty cart",
                    value={
                        "success": True,
                        "item_count": 0,
                        "cart_count": 0,
                        "items": [],
                        "subtotal": "0.00",
                        "subtotal_formatted": "$0.00",
                    },
                ),
            ],
        )
    },
)
@api_view(["GET"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def mini_cart_get(request):
    """Get current cart data formatted for mini-cart."""
    cart = get_cart_for_request(request)
    data = format_cart_for_minicart(cart)
    return Response(data)


@extend_schema(
    summary=_("Update cart item quantity"),
    description=_("""
    Update the quantity of an item in the cart.

    Set quantity to 0 to remove the item entirely. The endpoint validates
    stock availability before updating and returns the full updated cart.

    **Use Cases:**
    - Increment/decrement quantity buttons in mini-cart
    - Direct quantity input changes
    - Removing items (quantity=0)

    **Authentication:** None required (validates item belongs to user's cart)

    **Validation:**
    - Item must exist in user's cart
    - Quantity must be non-negative integer
    - Stock availability is checked for inventory-tracked products
    """),
    tags=["Cart"],
    request=CartUpdateRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=MiniCartResponseSerializer, description=_("Cart updated successfully")
        ),
        400: OpenApiResponse(
            response=CartErrorResponseSerializer,
            description=_("Invalid request data or insufficient stock"),
            examples=[
                OpenApiExample(
                    "Invalid data", value={"success": False, "message": "Invalid request data"}
                ),
                OpenApiExample(
                    "Insufficient stock",
                    value={"success": False, "message": "Only 3 items available in stock"},
                ),
            ],
        ),
        404: OpenApiResponse(
            response=CartErrorResponseSerializer,
            description=_("Cart item not found"),
            examples=[
                OpenApiExample(
                    "Item not found", value={"success": False, "message": "Item not found in cart"}
                )
            ],
        ),
    },
)
@api_view(["POST"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def mini_cart_update(request):
    """Update cart item quantity."""
    serializer = CartUpdateRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"success": False, "message": "Invalid request data"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    item_id = serializer.validated_data["item_id"]
    quantity = serializer.validated_data["quantity"]

    cart = get_cart_for_request(request)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {"success": False, "message": "Item not found in cart"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Guard: reject operations on child/component items
    if cart_item.parent_bundle is not None:
        return Response(
            {"success": False, "message": "Cannot modify component items directly"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if quantity < 1:
        # Remove item if quantity is 0 or less
        CartService.remove_item(cart_item)
    else:
        success, message = CartService.update_item(cart_item=cart_item, quantity=quantity)
        if not success:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    # Refresh cart and return updated data
    cart.refresh_from_db()
    data = format_cart_for_minicart(cart)
    return Response(data)


@extend_schema(
    summary=_("Remove item from cart"),
    description=_("""
    Remove an item from the cart entirely.

    Returns the updated cart data after removal.

    **Use Cases:**
    - Delete button on cart items
    - Clearing specific items

    **Authentication:** None required (validates item belongs to user's cart)
    """),
    tags=["Cart"],
    request=CartRemoveRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=MiniCartResponseSerializer, description=_("Item removed successfully")
        ),
        400: OpenApiResponse(
            response=CartErrorResponseSerializer, description=_("Invalid request data")
        ),
        404: OpenApiResponse(
            response=CartErrorResponseSerializer, description=_("Cart item not found")
        ),
    },
)
@api_view(["POST"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def mini_cart_remove(request):
    """Remove item from cart."""
    serializer = CartRemoveRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"success": False, "message": "Invalid request data"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    item_id = serializer.validated_data["item_id"]
    cart = get_cart_for_request(request)

    try:
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response(
            {"success": False, "message": "Item not found in cart"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Guard: reject removal of child/component items
    if cart_item.parent_bundle is not None:
        return Response(
            {"success": False, "message": "Cannot remove component items directly"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    CartService.remove_item(cart_item)

    # Refresh cart and return updated data
    cart.refresh_from_db()
    data = format_cart_for_minicart(cart)
    return Response(data)


@extend_schema(
    summary=_("Get empty cart recommendations"),
    description=_("""
    Get intelligent product recommendations for the empty cart state.

    Returns personalized suggestions organized into labeled sections based on:
    - **Recently viewed**: Products the user has browsed (session-based for anonymous users)
    - **Related**: Products in the same categories as recently viewed items
    - **On sale**: Currently discounted products
    - **Trending**: Popular products by views/sales
    - **Featured**: Editor-picked products as fallback

    All returned products are verified to be in stock and available for purchase.

    **Use Cases:**
    - Empty cart state in mini-cart
    - "You might like" sections
    - Cross-sell opportunities

    **Authentication:** None required (uses session for anonymous users)

    **Personalization:**
    - Anonymous users: Based on session recently-viewed products
    - Authenticated users: Based on account history and preferences
    """),
    tags=["Cart"],
    parameters=[
        OpenApiParameter(
            name="limit",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Maximum number of products to return (default: 6, max: 12)"),
            required=False,
            examples=[
                OpenApiExample("Default", value=6),
                OpenApiExample("Maximum", value=12),
            ],
        )
    ],
    responses={
        200: OpenApiResponse(
            response=CartRecommendationsResponseSerializer,
            description=_("Recommendations retrieved successfully"),
            examples=[
                OpenApiExample(
                    "With recently viewed",
                    value={
                        "sections": [
                            {
                                "type": "recently_viewed",
                                "label": "Continue Shopping",
                                "products": [
                                    {
                                        "id": 1,
                                        "name": "Classic T-Shirt",
                                        "slug": "classic-t-shirt",
                                        "url": "/products/classic-t-shirt/",
                                        "image_url": "/media/products/tshirt.jpg",
                                        "price": 29.99,
                                        "price_formatted": "$29.99",
                                        "on_sale": False,
                                        "sale_price": None,
                                        "sale_price_formatted": None,
                                        "category": "Clothing",
                                    }
                                ],
                            },
                            {
                                "type": "on_sale",
                                "label": "On Sale Now",
                                "products": [
                                    {
                                        "id": 5,
                                        "name": "Summer Dress",
                                        "slug": "summer-dress",
                                        "url": "/products/summer-dress/",
                                        "image_url": "/media/products/dress.jpg",
                                        "price": 79.99,
                                        "price_formatted": "$79.99",
                                        "on_sale": True,
                                        "sale_price": 49.99,
                                        "sale_price_formatted": "$49.99",
                                        "category": "Clothing",
                                    }
                                ],
                            },
                        ],
                        "total_count": 2,
                    },
                ),
                OpenApiExample(
                    "New visitor (no history)",
                    value={
                        "sections": [
                            {"type": "trending", "label": "Popular Right Now", "products": []}
                        ],
                        "total_count": 0,
                    },
                ),
            ],
        )
    },
)
@api_view(["GET"])
@authentication_classes(HeadlessAPIMixin.authentication_classes)
@permission_classes([AllowAny])
def cart_empty_recommendations(request):
    """Get intelligent recommendations for empty cart state."""
    # Get limit from query params (default 6, max 12)
    try:
        limit = min(int(request.query_params.get("limit", 6)), 12)
    except (ValueError, TypeError):
        limit = 6

    recommendations = CartRecommendationService.get_empty_cart_recommendations(request, limit=limit)

    return Response(recommendations)
