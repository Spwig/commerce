"""
Serializers for Cart, Wishlist, Checkout, and Shipping models
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from .models import (
    Cart, CartItem, Wishlist, WishlistItem,
    RecentlyViewed, ShippingMethod, TaxRate, CheckoutSession
)
from catalog.serializers import ProductListSerializer, ProductVariantSerializer
from vouchers.models import AppliedVoucher
from subscriptions.serializers import SubscriptionPlanSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items with product details"""
    product = ProductListSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    customization_price = serializers.SerializerMethodField(
        help_text=_("Total customization price (per unit)")
    )
    total_price = serializers.SerializerMethodField()
    savings = serializers.SerializerMethodField()
    requires_shipping = serializers.BooleanField(read_only=True)
    item_weight = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    # Bundle-related fields
    delivery_type = serializers.SerializerMethodField(
        help_text=_("'instant' for digital items, 'shipping' for physical items")
    )
    is_bundle_component = serializers.SerializerMethodField(
        help_text=_("True if this item is a component of a bundle")
    )
    parent_bundle_id = serializers.SerializerMethodField(
        help_text=_("ID of parent bundle CartItem if this is a component")
    )
    bundle_components = serializers.SerializerMethodField(
        help_text=_("Child items if this is a bundle parent")
    )

    def get_customization_price(self, obj):
        """Extract decimal from Money object"""
        amount = obj.customization_price
        if amount is None:
            return "0.00"
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_total_price(self, obj):
        """Extract decimal from Money object"""
        amount = obj.total_price
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_savings(self, obj):
        """Extract decimal from Money object"""
        amount = obj.savings
        if amount is None:
            return "0.00"
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_delivery_type(self, obj):
        """
        Return delivery type based on product's digital status.
        Returns 'instant' for digital items, 'shipping' for physical items.
        """
        product = obj.product
        if product.is_digital:
            return 'instant'
        return 'shipping'

    def get_is_bundle_component(self, obj):
        """Check if this item is a component of a bundle"""
        return obj.parent_bundle_id is not None

    def get_parent_bundle_id(self, obj):
        """Get the parent bundle ID if this is a component"""
        return obj.parent_bundle_id

    def get_bundle_components(self, obj):
        """
        Get child items if this is a bundle or configurable parent.
        Groups components by delivery_type for easy frontend rendering.
        """
        if obj.product.product_type not in ('bundle', 'configurable'):
            return None

        components = obj.component_items.all()
        if not components:
            return None

        # Group by delivery type
        instant_items = []
        shipping_items = []

        for component in components:
            # Get component product image
            comp_images = []
            if hasattr(component.product, 'images'):
                for img in component.product.images.all()[:1]:
                    img_data = {}
                    if hasattr(img, 'media_asset') and img.media_asset:
                        ma = img.media_asset
                        img_data['thumbnail_url'] = ma.get_thumbnail('small') if hasattr(ma, 'get_thumbnail') else (ma.get_display_url() if hasattr(ma, 'get_display_url') else '')
                        img_data['url'] = ma.original_file.url if ma.original_file else ''
                    comp_images.append(img_data)

            component_data = {
                'id': component.id,
                'product': {
                    'id': component.product.id,
                    'name': component.product.name,
                    'sku': component.product.sku,
                    'is_digital': component.product.is_digital,
                    'images': comp_images,
                },
                'variant': {
                    'id': component.variant.id,
                    'name': component.variant.name,
                    'sku': component.variant.sku,
                } if component.variant else None,
                'quantity': component.quantity,
                'unit_price': str(component.unit_price.amount) if hasattr(component.unit_price, 'amount') else str(component.unit_price),
            }

            if component.product.is_digital:
                instant_items.append(component_data)
            else:
                shipping_items.append(component_data)

        return {
            'instant': instant_items if instant_items else None,
            'shipping': shipping_items if shipping_items else None,
            'total_count': len(components),
        }

    # Subscription fields
    subscription_plan_details = SubscriptionPlanSerializer(source='subscription_plan', read_only=True)

    # IDs are both read+write: clients send them when adding to cart, and the
    # headless SDK's CartItem type expects them on read for optimistic merge logic.
    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    subscription_plan_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    pricing_tier_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    payment_token_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    # Flat aliases for headless SDK consumers (the SDK's CartItem TS interface
    # declares product_name/product_image/variant_name/sku/currency as flat
    # fields, but `product` and `variant` are nested objects on this serializer).
    # Without these aliases, mini-cart components show items with no name or
    # image.
    product_name = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()
    variant_name = serializers.SerializerMethodField()
    sku = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name if obj.product_id else None

    def get_product_slug(self, obj):
        return obj.product.slug if obj.product_id else None

    def get_product_image(self, obj):
        """Best-effort thumbnail URL for SDK mini-cart consumers."""
        if not obj.product_id:
            return None
        img = (obj.product.images.filter(is_primary=True, show_in_listing=True).first()
               or obj.product.images.filter(show_in_listing=True).first())
        if img and img.media_asset:
            if hasattr(img.media_asset, 'get_thumbnail'):
                return img.media_asset.get_thumbnail('small')
            if hasattr(img.media_asset, 'get_display_url'):
                return img.media_asset.get_display_url()
        return None

    def get_variant_name(self, obj):
        return obj.variant.name if obj.variant_id else None

    def get_sku(self, obj):
        if obj.variant_id and obj.variant.sku:
            return obj.variant.sku
        return obj.product.sku if obj.product_id else None

    def get_currency(self, obj):
        if hasattr(obj.unit_price, 'currency'):
            return str(obj.unit_price.currency)
        return None

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'variant', 'quantity', 'unit_price',
            'customization_price', 'total_price', 'savings', 'customizations', 'notes',
            'requires_shipping', 'item_weight',
            'delivery_type', 'is_bundle_component', 'parent_bundle_id', 'bundle_components',
            'is_subscription', 'subscription_plan_details',
            'product_id', 'variant_id', 'subscription_plan_id', 'pricing_tier_id', 'payment_token_id',
            # Flat aliases for SDK consumers
            'product_name', 'product_slug', 'product_image',
            'variant_name', 'sku', 'currency',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'unit_price', 'customization_price', 'created_at', 'updated_at',
            'delivery_type', 'is_bundle_component', 'parent_bundle_id', 'bundle_components',
            'product_name', 'product_slug', 'product_image',
            'variant_name', 'sku', 'currency',
        ]

    def validate(self, data):
        """Validate subscription-related data"""
        is_subscription = data.get('is_subscription', False)
        subscription_plan_id = data.get('subscription_plan_id')
        payment_token_id = data.get('payment_token_id')

        if is_subscription:
            if not subscription_plan_id:
                raise serializers.ValidationError({
                    'subscription_plan_id': 'Subscription plan is required when is_subscription is True'
                })
            if not payment_token_id:
                raise serializers.ValidationError({
                    'payment_token_id': 'Payment token is required for subscription purchases'
                })

            # Verify subscription plan exists
            from subscriptions.models import SubscriptionPlan
            try:
                plan = SubscriptionPlan.objects.get(plan_id=subscription_plan_id, is_active=True)
                data['subscription_plan'] = plan
            except SubscriptionPlan.DoesNotExist:
                raise serializers.ValidationError({
                    'subscription_plan_id': 'Invalid or inactive subscription plan'
                })

            # Verify payment token exists and belongs to user
            from subscriptions.models import PaymentToken
            try:
                token = PaymentToken.objects.get(
                    token_id=payment_token_id,
                    user=self.context['request'].user,
                    is_active=True
                )
                data['payment_token'] = token
            except PaymentToken.DoesNotExist:
                raise serializers.ValidationError({
                    'payment_token_id': 'Invalid or inactive payment token'
                })

            # Verify pricing tier (optional — falls back to plan default)
            pricing_tier_id = data.get('pricing_tier_id')
            if pricing_tier_id:
                from subscriptions.models import PlanPricingTier
                try:
                    tier = PlanPricingTier.objects.get(tier_id=pricing_tier_id, plan=plan)
                    data['pricing_tier'] = tier
                except PlanPricingTier.DoesNotExist:
                    raise serializers.ValidationError({
                        'pricing_tier_id': 'Pricing tier not found or does not belong to selected plan'
                    })
            else:
                tier = plan.get_default_tier()
                if not tier:
                    raise serializers.ValidationError({
                        'pricing_tier_id': 'No pricing tier available for this plan'
                    })
                data['pricing_tier'] = tier

        return data


class CartAppliedVoucherSerializer(serializers.ModelSerializer):
    """Serializer for vouchers applied to cart"""
    code = serializers.CharField(source='voucher.code', read_only=True)
    name = serializers.CharField(source='voucher.name', read_only=True)
    description = serializers.CharField(source='voucher.description', read_only=True)
    discount_type = serializers.CharField(source='voucher.discount_type', read_only=True)

    class Meta:
        model = AppliedVoucher
        fields = ['id', 'code', 'name', 'description', 'discount_type', 'discount_amount']
        read_only_fields = ['id', 'discount_amount']


class CartSerializer(serializers.ModelSerializer):
    """Comprehensive cart serializer with all calculations"""
    items = serializers.SerializerMethodField()
    applied_vouchers = CartAppliedVoucherSerializer(many=True, read_only=True)
    # Applied gift cards as a parallel array to applied_vouchers. The
    # apply/remove gift card endpoints emit this same shape in their
    # response envelope; exposing it on the cart serializer means the
    # storefront's chip list survives a GET /api/cart/ refresh without
    # needing to also re-call apply.
    applied_gift_cards = serializers.SerializerMethodField()

    # Calculated fields - use SerializerMethodField to handle Money objects
    total_items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    total_savings = serializers.SerializerMethodField()
    voucher_discount_amount = serializers.SerializerMethodField()
    gift_card_discount_amount = serializers.SerializerMethodField()
    final_amount = serializers.SerializerMethodField()
    requires_shipping = serializers.BooleanField(read_only=True)
    total_weight = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    grand_total = serializers.SerializerMethodField()

    # Headless SDK aliases — the SDK uses subtotal/item_count/total/currency
    subtotal = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def get_total_items(self, obj):
        """Count only parent items (exclude bundle/configurable children)"""
        return sum(
            item.quantity for item in obj.items.filter(parent_bundle__isnull=True)
        )

    def get_total_amount(self, obj):
        """Extract decimal from Money object"""
        amount = obj.total_amount
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_total_savings(self, obj):
        """Extract decimal from Money object"""
        amount = obj.total_savings
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_voucher_discount_amount(self, obj):
        """Extract decimal from Money object"""
        amount = obj.voucher_discount_amount
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_gift_card_discount_amount(self, obj):
        """Extract decimal from Money object"""
        amount = obj.gift_card_discount_amount
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_applied_gift_cards(self, obj):
        """Return the cart's applied gift cards in the SDK chip shape."""
        return obj.get_gift_card_summary()

    def get_final_amount(self, obj):
        """Extract decimal from Money object"""
        amount = obj.final_amount
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_items(self, obj):
        """Only return parent/top-level items; children are nested via bundle_components."""
        parent_items = obj.items.filter(
            parent_bundle__isnull=True
        ).select_related(
            'product', 'variant'
        ).prefetch_related(
            'component_items__product', 'component_items__variant'
        )
        return CartItemSerializer(parent_items, many=True).data

    def get_grand_total(self, obj):
        """Extract decimal from Money object"""
        amount = obj.grand_total
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_subtotal(self, obj):
        """Alias for total_amount — used by the headless SDK."""
        return self.get_total_amount(obj)

    def get_item_count(self, obj):
        """Alias for total_items — used by the headless SDK."""
        return self.get_total_items(obj)

    def get_total(self, obj):
        """Alias for grand_total — used by the headless SDK."""
        return self.get_grand_total(obj)

    def get_currency(self, obj):
        """Cart operating currency for headless SDK."""
        return obj.effective_currency

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'session_key', 'cart_layout', 'checkout_flow',
            'show_product_images', 'show_product_variants', 'show_remove_button',
            'show_quantity_controls', 'show_item_totals', 'show_cart_summary',
            'show_savings', 'shipping_address', 'shipping_method', 'shipping_cost',
            'estimated_delivery_date', 'shipping_notes',
            'items', 'applied_vouchers', 'applied_gift_cards',
            'total_items', 'total_amount', 'total_savings',
            'voucher_discount_amount', 'gift_card_discount_amount',
            'final_amount',
            'requires_shipping', 'total_weight', 'grand_total',
            'subtotal', 'item_count', 'total', 'currency',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at',
            'total_items', 'total_amount', 'total_savings',
            'voucher_discount_amount', 'gift_card_discount_amount',
            'final_amount',
            'requires_shipping', 'total_weight', 'grand_total',
            'subtotal', 'item_count', 'total', 'currency'
        ]


class CartSummarySerializer(serializers.ModelSerializer):
    """Lightweight cart serializer for quick summary"""
    total_items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    grand_total = serializers.SerializerMethodField()

    # Headless SDK aliases
    item_count = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def get_total_items(self, obj):
        """Count only parent items (exclude bundle/configurable children)"""
        return sum(
            item.quantity for item in obj.items.filter(parent_bundle__isnull=True)
        )

    def get_total_amount(self, obj):
        """Extract decimal from Money object"""
        amount = obj.total_amount
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_grand_total(self, obj):
        """Extract decimal from Money object"""
        amount = obj.grand_total
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_item_count(self, obj):
        return self.get_total_items(obj)

    def get_subtotal(self, obj):
        return self.get_total_amount(obj)

    def get_total(self, obj):
        return self.get_grand_total(obj)

    def get_currency(self, obj):
        return obj.effective_currency

    class Meta:
        model = Cart
        fields = [
            'id', 'total_items', 'total_amount', 'grand_total',
            'item_count', 'subtotal', 'total', 'currency',
            'shipping_cost', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_items', 'total_amount', 'grand_total',
            'item_count', 'subtotal', 'total', 'currency', 'updated_at'
        ]


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart"""
    product_id = serializers.IntegerField(required=True)
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(required=True, min_value=1)
    customizations = serializers.JSONField(required=False, default=dict)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=500)

    # Bundle configuration - for bundle products where customer chooses variants
    variant_selections = serializers.DictField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
        help_text=_("Map of bundle_item_id to variant_id for customer-selected variants")
    )
    excluded_optional_items = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
        help_text=_("List of bundle_item_ids to exclude (for optional items customer doesn't want)")
    )

    # Configurator configuration - for configurable products
    configuration = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField()),
        required=False,
        allow_empty=True,
        help_text=_("Map of slot_id to list of selected option_ids for configurable products")
    )
    preset_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text=_("Configuration preset ID used as starting point")
    )

    # Booking configuration - for booking products
    booking_data = serializers.JSONField(
        required=False,
        default=None,
        help_text=_("Booking details: start_datetime, end_datetime, resource_id, persons, timezone")
    )

    # Subscription configuration
    is_subscription = serializers.BooleanField(required=False, default=False)
    subscription_plan_id = serializers.UUIDField(required=False, allow_null=True)
    pricing_tier_id = serializers.UUIDField(required=False, allow_null=True)
    payment_token_id = serializers.UUIDField(required=False, allow_null=True)

    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value < 1:
            raise serializers.ValidationError(_("Quantity must be at least 1"))
        return value

    def validate_variant_selections(self, value):
        """Convert string keys to integers if needed (JSON may send string keys)"""
        if value:
            return {int(k): int(v) for k, v in value.items()}
        return value

    def validate(self, data):
        """Validate subscription-related fields"""
        is_subscription = data.get('is_subscription', False)

        if is_subscription:
            if not data.get('subscription_plan_id'):
                raise serializers.ValidationError({
                    'subscription_plan_id': _('Subscription plan is required for subscription purchases')
                })
            if not data.get('payment_token_id'):
                raise serializers.ValidationError({
                    'payment_token_id': _('Payment token is required for subscription purchases')
                })

            # Validate product supports subscriptions
            from catalog.models import Product
            try:
                product = Product.objects.get(id=data['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError({
                    'product_id': _('Product not found')
                })

            if not product.is_subscription_enabled:
                raise serializers.ValidationError({
                    'is_subscription': _('This product does not support subscriptions')
                })

            # Validate plan exists, is active, and is linked to this product
            from subscriptions.models import SubscriptionPlan
            try:
                plan = SubscriptionPlan.objects.get(
                    plan_id=data['subscription_plan_id'], is_active=True
                )
            except SubscriptionPlan.DoesNotExist:
                raise serializers.ValidationError({
                    'subscription_plan_id': _('Invalid or inactive subscription plan')
                })

            if not product.subscription_plans.filter(plan_id=plan.plan_id).exists():
                raise serializers.ValidationError({
                    'subscription_plan_id': _('This plan is not available for this product')
                })

            data['subscription_plan'] = plan

            # Validate payment token
            from subscriptions.models import PaymentToken
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                try:
                    token = PaymentToken.objects.get(
                        token_id=data['payment_token_id'],
                        user=request.user,
                        is_active=True
                    )
                    data['payment_token'] = token
                except PaymentToken.DoesNotExist:
                    raise serializers.ValidationError({
                        'payment_token_id': _('Invalid or inactive payment token')
                    })

            # Validate pricing tier (optional — falls back to plan default)
            pricing_tier_id = data.get('pricing_tier_id')
            if pricing_tier_id:
                from subscriptions.models import PlanPricingTier
                try:
                    tier = PlanPricingTier.objects.get(tier_id=pricing_tier_id, plan=plan)
                    data['pricing_tier'] = tier
                except PlanPricingTier.DoesNotExist:
                    raise serializers.ValidationError({
                        'pricing_tier_id': _('Pricing tier not found or does not belong to selected plan')
                    })
            else:
                tier = plan.get_default_tier()
                if not tier:
                    raise serializers.ValidationError({
                        'pricing_tier_id': _('No pricing tier available for this plan')
                    })
                data['pricing_tier'] = tier

        return data


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating cart item quantity"""
    quantity = serializers.IntegerField(required=True, min_value=0)
    customizations = serializers.JSONField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=500)

    def validate_quantity(self, value):
        """Validate quantity (0 means remove)"""
        if value < 0:
            raise serializers.ValidationError(_("Quantity cannot be negative"))
        return value


class ApplyVoucherSerializer(serializers.Serializer):
    """Serializer for applying voucher code"""
    code = serializers.CharField(required=True, max_length=50)


class ApplyGiftCardSerializer(serializers.Serializer):
    """Serializer for applying gift card code"""
    code = serializers.CharField(
        required=True,
        max_length=50,
        help_text=_("Gift card code (e.g., GC-XXXX-XXXX-XXXX)")
    )


class AppliedGiftCardSerializer(serializers.Serializer):
    """Serializer for applied gift card display"""
    code = serializers.CharField(read_only=True)
    discount_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        help_text=_("Amount applied from this gift card (in base currency)")
    )
    remaining_balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        help_text=_("Remaining balance on gift card after this application")
    )
    currency = serializers.CharField(
        read_only=True,
        help_text=_("Base currency code")
    )
    gift_card_currency = serializers.CharField(
        read_only=True,
        help_text=_("Gift card's native currency code")
    )
    original_discount_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        required=False,
        allow_null=True,
        help_text=_("Discount in gift card's native currency (for foreign-currency gift cards)")
    )


class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer for wishlist items"""
    product = ProductListSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)

    # Write-only fields
    product_id = serializers.IntegerField(write_only=True)
    variant_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = WishlistItem
        fields = [
            'id', 'product', 'variant', 'notes', 'priority',
            'notify_when_available', 'notify_when_on_sale',
            'product_id', 'variant_id', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for wishlists"""
    items = WishlistItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Wishlist
        fields = [
            'id', 'user', 'name', 'wishlist_layout', 'is_public',
            'share_slug', 'show_prices', 'show_availability',
            'show_add_to_cart', 'items', 'total_items', 'total_value',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'share_slug', 'created_at', 'updated_at']


class AddToWishlistSerializer(serializers.Serializer):
    """Serializer for adding items to wishlist"""
    wishlist_id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=True)
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=500)
    priority = serializers.ChoiceField(
        choices=['low', 'medium', 'high'],
        default='medium'
    )
    notify_when_available = serializers.BooleanField(default=False)
    notify_when_on_sale = serializers.BooleanField(default=False)


class RecentlyViewedSerializer(serializers.ModelSerializer):
    """Serializer for recently viewed products"""
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = RecentlyViewed
        fields = ['id', 'product', 'viewed_at', 'view_count']
        read_only_fields = ['id', 'viewed_at', 'view_count']


class ShippingMethodSerializer(serializers.ModelSerializer):
    """Serializer for shipping methods with Phase 2-4 integration"""

    # Calculated fields for specific cart
    calculated_cost = serializers.SerializerMethodField()
    base_cost = serializers.SerializerMethodField()
    final_cost = serializers.SerializerMethodField()
    rules_applied = serializers.SerializerMethodField()
    total_discount = serializers.SerializerMethodField()
    total_surcharge = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    estimated_delivery = serializers.SerializerMethodField()

    # Phase 2: Zones
    zones_count = serializers.SerializerMethodField()
    zones = serializers.SerializerMethodField()

    # Phase 4: Pickup Locations
    pickup_locations = serializers.SerializerMethodField()

    class Meta:
        model = ShippingMethod
        fields = [
            'id', 'name', 'description', 'method_type', 'flat_rate_cost',
            'min_delivery_days', 'max_delivery_days', 'icon', 'sort_order',
            'is_active', 'carrier', 'carrier_service_code',
            # Calculated fields
            'calculated_cost', 'base_cost', 'final_cost',
            'rules_applied', 'total_discount', 'total_surcharge',
            'is_available', 'estimated_delivery',
            # Zone and location fields
            'zones_count', 'zones', 'pickup_locations'
        ]
        read_only_fields = ['id']

    def get_calculated_cost(self, obj) -> float | None:
        """Get calculated shipping cost (DEPRECATED - use final_cost)"""
        # Kept for backward compatibility
        return self.get_final_cost(obj)

    def get_base_cost(self, obj) -> float | None:
        """Get base shipping cost before rules"""
        cart = self.context.get('cart')
        address = self.context.get('address')
        if cart:
            return float(obj.calculate_cost(cart, address))
        return None

    def get_final_cost(self, obj) -> float | None:
        """Get final shipping cost after rules (Phase 3)"""
        cart = self.context.get('cart')
        address = self.context.get('address')
        user = self.context.get('user')

        if not cart:
            return None

        from shipping.services import ShippingRuleService

        calculation = ShippingRuleService.calculate_shipping_for_cart(
            cart=cart,
            shipping_method=obj,
            address=address,
            user=user
        )

        return float(calculation['final_cost'].amount)

    def get_rules_applied(self, obj) -> list:
        """Get list of rules applied (Phase 3)"""
        cart = self.context.get('cart')
        address = self.context.get('address')
        user = self.context.get('user')

        if not cart:
            return []

        from shipping.services import ShippingRuleService

        calculation = ShippingRuleService.calculate_shipping_for_cart(
            cart=cart,
            shipping_method=obj,
            address=address,
            user=user
        )

        return [
            {
                'rule_name': rule.get('promotion_name', rule.get('rule_name', '')),
                'rule_type': rule.get('promotion_type', rule.get('rule_type', '')),
                'adjustment': float(rule['adjustment'].amount),
            }
            for rule in calculation.get('rules_applied', [])
        ]

    def get_total_discount(self, obj) -> float | None:
        """Get total discount from rules (Phase 3)"""
        cart = self.context.get('cart')
        address = self.context.get('address')
        user = self.context.get('user')

        if not cart:
            return None

        from shipping.services import ShippingRuleService

        calculation = ShippingRuleService.calculate_shipping_for_cart(
            cart=cart,
            shipping_method=obj,
            address=address,
            user=user
        )

        return float(calculation['total_discount'].amount)

    def get_total_surcharge(self, obj) -> float | None:
        """Get total surcharge from rules (Phase 3)"""
        cart = self.context.get('cart')
        address = self.context.get('address')
        user = self.context.get('user')

        if not cart:
            return None

        from shipping.services import ShippingRuleService

        calculation = ShippingRuleService.calculate_shipping_for_cart(
            cart=cart,
            shipping_method=obj,
            address=address,
            user=user
        )

        return float(calculation['total_surcharge'].amount)

    def get_is_available(self, obj) -> bool | None:
        """Check if shipping method is available (Phase 2: includes zone checking)"""
        cart = self.context.get('cart')
        address = self.context.get('address')

        if not cart:
            return None

        cart_available, _ = obj.is_available_for_cart(cart)
        if not cart_available:
            return False

        if address:
            # This now includes Phase 2 zone checking
            address_available, _ = obj.is_available_for_address(address)
            return address_available

        return True

    def get_estimated_delivery(self, obj) -> str | None:
        """Get estimated delivery date"""
        if obj.min_delivery_days:
            return obj.get_estimated_delivery_date().isoformat()
        return None

    def get_zones_count(self, obj) -> int:
        """Get number of zones assigned (Phase 2)"""
        return obj.zones.filter(is_active=True).count()

    def get_zones(self, obj) -> list:
        """Get zones assigned to method (Phase 2)"""
        from shipping.api.serializers import ShippingZoneListSerializer

        zones = obj.zones.filter(is_active=True)
        return ShippingZoneListSerializer(zones, many=True).data

    def get_pickup_locations(self, obj) -> list | None:
        """Get pickup locations for local_pickup methods (Phase 4)"""
        if obj.method_type != 'local_pickup':
            return None

        from shipping.api.serializers import LocationListSerializer

        locations = obj.pickup_locations.filter(is_active=True)
        return LocationListSerializer(locations, many=True).data


class TaxRateSerializer(serializers.ModelSerializer):
    """Serializer for tax rates (admin use)"""
    rate_display = serializers.SerializerMethodField()

    class Meta:
        model = TaxRate
        fields = [
            'id', 'name', 'country', 'state', 'city', 'postal_codes',
            'rate', 'rate_display', 'tax_type', 'applies_to_shipping', 'compound',
            'exempt_product_types', 'exempt_categories', 'priority',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_rate_display(self, obj):
        return f"{obj.rate * 100}%"


class TaxPresetGroupSerializer(serializers.ModelSerializer):
    """Serializer for tax preset groups"""
    rates_count = serializers.IntegerField(source='rates.count', read_only=True)

    class Meta:
        from cart.models import TaxPresetGroup
        model = TaxPresetGroup
        fields = [
            'id', 'key', 'name', 'description', 'icon', 'tax_type',
            'region', 'is_active', 'version', 'rates_count',
            'last_updated', 'created_at'
        ]
        read_only_fields = ['id', 'last_updated', 'created_at']


class TaxPresetRateSerializer(serializers.ModelSerializer):
    """Serializer for individual preset rates"""
    rate_display = serializers.SerializerMethodField()

    class Meta:
        from cart.models import TaxPresetRate
        model = TaxPresetRate
        fields = [
            'id', 'country', 'country_name', 'state', 'state_name',
            'rate', 'rate_display', 'tax_type', 'notes', 'is_active'
        ]

    def get_rate_display(self, obj):
        return f"{obj.rate * 100}%"


class TaxCalculationItemSerializer(serializers.Serializer):
    """Individual item for tax calculation request"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class TaxCalculationRequestSerializer(serializers.Serializer):
    """Request body for tax calculation endpoint"""
    country = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100, required=False, default='')
    city = serializers.CharField(max_length=100, required=False, default='')
    postal_code = serializers.CharField(max_length=20, required=False, default='')
    items = TaxCalculationItemSerializer(many=True)
    shipping_cost = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )


class CheckoutAddressSerializer(serializers.ModelSerializer):
    """Lightweight address serializer for checkout session"""
    class Meta:
        from orders.models import Address
        model = Address
        fields = ['id', 'name', 'company', 'address1', 'address2',
                  'city', 'state', 'postal_code', 'country', 'phone']


class CheckoutShippingMethodSerializer(serializers.ModelSerializer):
    """Lightweight shipping method serializer for checkout session"""
    class Meta:
        model = ShippingMethod
        fields = [
            'id', 'name', 'description', 'method_type',
            'flat_rate_cost', 'min_delivery_days', 'max_delivery_days', 'icon',
        ]


class CheckoutSessionSerializer(serializers.ModelSerializer):
    """Serializer for checkout session"""
    cart = CartSerializer(read_only=True)
    available_shipping_methods = serializers.JSONField(read_only=True)
    shipping_address = CheckoutAddressSerializer(read_only=True)
    billing_address = CheckoutAddressSerializer(read_only=True)
    selected_shipping_method = CheckoutShippingMethodSerializer(read_only=True)
    payment_provider_name = serializers.SerializerMethodField()

    # Headless SDK aliases
    tax = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        model = CheckoutSession
        fields = [
            'id', 'cart', 'shipping_address', 'shipping_address_data',
            'billing_address', 'billing_address_data',
            'billing_same_as_shipping', 'selected_shipping_method',
            'shipping_cost', 'estimated_delivery_date',
            'available_shipping_methods', 'tax_breakdown', 'tax_amount',
            'payment_provider', 'payment_provider_name',
            'subtotal', 'discount_amount', 'total_amount',
            'tax', 'discount', 'total', 'currency',
            'step_completed', 'metadata', 'expires_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'cart', 'available_shipping_methods', 'tax_breakdown',
            'tax_amount', 'subtotal', 'discount_amount', 'total_amount',
            'tax', 'discount', 'total', 'currency',
            'expires_at', 'created_at', 'updated_at'
        ]

    def get_payment_provider_name(self, obj):
        if obj.payment_provider:
            return obj.payment_provider.display_name or obj.payment_provider.provider_name
        return None

    def get_tax(self, obj):
        amount = obj.tax_amount
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_discount(self, obj):
        amount = obj.discount_amount
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_total(self, obj):
        amount = obj.total_amount
        return str(amount.amount) if hasattr(amount, 'amount') else str(amount)

    def get_currency(self, obj):
        return obj.cart.effective_currency


class SetShippingAddressSerializer(serializers.Serializer):
    """Serializer for setting shipping address during checkout"""
    address_id = serializers.IntegerField(required=False, allow_null=True)
    # Or provide full address details
    name = serializers.CharField(required=False, max_length=200)
    company = serializers.CharField(required=False, allow_blank=True, max_length=200)
    address1 = serializers.CharField(required=False, max_length=200)
    address2 = serializers.CharField(required=False, allow_blank=True, max_length=200)
    city = serializers.CharField(required=False, max_length=100)
    state = serializers.CharField(required=False, allow_blank=True, max_length=100)
    postal_code = serializers.CharField(required=False, max_length=20)
    country = serializers.CharField(required=False, max_length=100)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    email = serializers.EmailField(required=False, allow_blank=True)

    def validate(self, data):
        """Ensure either address_id or full address is provided"""
        if not data.get('address_id'):
            required_fields = ['name', 'address1', 'city', 'postal_code', 'country']
            missing_fields = [f for f in required_fields if not data.get(f)]
            if missing_fields:
                raise serializers.ValidationError(
                    _("Either address_id or complete address details are required. Missing: {fields}").format(
                        fields=', '.join(missing_fields)
                    )
                )
        return data


class SetShippingMethodSerializer(serializers.Serializer):
    """Serializer for selecting shipping method during checkout"""
    shipping_method_id = serializers.IntegerField(required=True)


class SetBillingAddressSerializer(serializers.Serializer):
    """Serializer for setting billing address during checkout"""
    same_as_shipping = serializers.BooleanField(required=False, default=True)
    address_id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField(required=False, max_length=200)
    company = serializers.CharField(required=False, allow_blank=True, max_length=200)
    address1 = serializers.CharField(required=False, max_length=200)
    address2 = serializers.CharField(required=False, allow_blank=True, max_length=200)
    city = serializers.CharField(required=False, max_length=100)
    state = serializers.CharField(required=False, allow_blank=True, max_length=100)
    postal_code = serializers.CharField(required=False, max_length=20)
    country = serializers.CharField(required=False, max_length=100)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=20)

    def validate(self, data):
        if not data.get('same_as_shipping', True) and not data.get('address_id'):
            required_fields = ['name', 'address1', 'city', 'postal_code', 'country']
            missing_fields = [f for f in required_fields if not data.get(f)]
            if missing_fields:
                raise serializers.ValidationError(
                    _("Complete billing address details are required. Missing: {fields}").format(
                        fields=', '.join(missing_fields)
                    )
                )
        return data


class SetPaymentMethodSerializer(serializers.Serializer):
    """Serializer for selecting payment method during checkout.
    Accepts either payment_provider_id (UUID) or provider (slug string).
    """
    payment_provider_id = serializers.UUIDField(required=False)
    provider = serializers.CharField(required=False, max_length=100)

    def validate(self, data):
        if not data.get('payment_provider_id') and not data.get('provider'):
            raise serializers.ValidationError(
                _("Either payment_provider_id or provider slug is required.")
            )
        return data
