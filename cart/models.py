from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from decimal import Decimal
from design.models import DesignMixin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Cart(DesignMixin):
    """Shopping cart with design customization and shipping integration"""
    # Session-based or user-based cart
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("User")
    )
    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Session Key")
    )

    # Cart currency — tracks which currency this cart operates in.
    # Set when the first item is added. All items in the cart must share
    # this currency. If empty, defaults to the store's base currency.
    currency = models.CharField(
        max_length=3,
        blank=True,
        default='',
        verbose_name=_("Cart Currency"),
        help_text=_("Currency code for all items in this cart (e.g. EUR, NZD). "
                    "Empty means store default currency.")
    )

    # Cart customization
    CART_LAYOUTS = [
        ('default', _('Default Layout')),
        ('compact', _('Compact View')),
        ('detailed', _('Detailed View')),
        ('minimal', _('Minimal View')),
        ('sidebar', _('Sidebar Cart')),
        ('overlay', _('Overlay Cart')),
    ]

    cart_layout = models.CharField(
        max_length=20,
        choices=CART_LAYOUTS,
        default='default',
        help_text=_("How the cart is displayed"),
        verbose_name=_("Cart Layout")
    )

    # Cart behavior
    show_product_images = models.BooleanField(
        default=True,
        verbose_name=_("Show Product Images")
    )
    show_product_variants = models.BooleanField(
        default=True,
        verbose_name=_("Show Product Variants")
    )
    show_remove_button = models.BooleanField(
        default=True,
        verbose_name=_("Show Remove Button")
    )
    show_quantity_controls = models.BooleanField(
        default=True,
        verbose_name=_("Show Quantity Controls")
    )

    # Pricing display
    show_item_totals = models.BooleanField(
        default=True,
        verbose_name=_("Show Item Totals")
    )
    show_cart_summary = models.BooleanField(
        default=True,
        verbose_name=_("Show Cart Summary")
    )
    show_savings = models.BooleanField(
        default=True,
        verbose_name=_("Show Savings")
    )

    # Checkout process design
    checkout_flow = models.CharField(
        max_length=20,
        choices=[
            ('single_page', _('Single Page Checkout')),
            ('multi_step', _('Multi-Step Checkout')),
            ('accordion', _('Accordion Style')),
            ('wizard', _('Wizard Style')),
        ],
        default='multi_step',
        verbose_name=_("Checkout Flow")
    )

    # Shipping information (set during checkout)
    shipping_address = models.ForeignKey(
        'orders.Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='carts_as_shipping',
        verbose_name=_("Shipping Address")
    )

    shipping_method = models.ForeignKey(
        'ShippingMethod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Shipping Method")
    )

    shipping_cost = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        default=0,
        help_text=_("Calculated shipping cost"),
        verbose_name=_("Shipping Cost")
    )

    estimated_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Estimated Delivery Date")
    )

    shipping_notes = models.TextField(
        blank=True,
        verbose_name=_("Shipping Notes")
    )

    # POS manual cart-level discount (staff-applied discounts)
    DISCOUNT_TYPE_CHOICES = [
        ('none', _('None')),
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed Amount')),
    ]
    pos_manual_discount_type = models.CharField(
        _('POS manual discount type'),
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='none'
    )
    pos_manual_discount_value = models.DecimalField(
        _('POS manual discount value'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Discount value (percentage or fixed amount)')
    )
    pos_manual_discount_applied_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pos_cart_discounts',
        verbose_name=_('POS discount applied by')
    )
    pos_manual_discount_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pos_cart_discount_approvals',
        verbose_name=_('POS discount approved by'),
        help_text=_('Manager who approved the discount if it exceeded staff limit')
    )
    pos_manual_discount_reason = models.CharField(
        _('POS discount reason'),
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Shopping Cart")
        verbose_name_plural = _("Shopping Carts")
        # Anonymous visitors get exactly one cart per session_key.
        # PostgreSQL `unique_together` cannot enforce this when user_id is
        # NULL (NULL != NULL for unique constraints), so we use a partial
        # unique index instead.
        #
        # We deliberately do NOT enforce one-cart-per-user — license_checkout,
        # marketplace_checkout, and developer_portal create separate user-bound
        # carts on purpose (each holds its own OneToOne CheckoutSession). The
        # "regular shopping cart" for a user is the one with session_key IS NULL,
        # which CartService.get_or_create_cart looks up specifically.
        constraints = [
            models.UniqueConstraint(
                fields=['session_key'],
                condition=models.Q(user__isnull=True) & ~models.Q(session_key=''),
                name='cart_unique_anon_per_session',
            ),
        ]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['shipping_method', 'shipping_address']),
        ]

    def __str__(self):
        if self.user:
            return _("Cart for {username}").format(username=self.user.username)
        return _("Cart (Session: {session})").format(session=self.session_key[:8] if self.session_key else "N/A")
    
    @property
    def effective_currency(self):
        """Get the cart's operating currency (stored currency or store default)."""
        if self.currency:
            return self.currency
        from core.utils import get_default_currency
        return get_default_currency()

    @property
    def total_items(self):
        """Total number of items in cart (excludes bundle component items)"""
        return sum(item.quantity for item in self.items.all() if item.parent_bundle_id is None)

    @property
    def total_amount(self):
        """Total cart value before voucher discounts (excludes bundle component items).

        The `currency` fallback ensures an empty cart returns Money(0, cart_currency)
        rather than Money(0, site_default_currency), so downstream arithmetic against
        item-priced Money values doesn't crash when the two disagree.
        """
        from core.utils import safe_money_sum
        return safe_money_sum(
            (item.total_price for item in self.items.all() if item.parent_bundle_id is None),
            currency=self.effective_currency,
        )

    @property
    def total_savings(self):
        """Total savings from product discounts (not voucher discounts, excludes bundle components)"""
        from core.utils import safe_money_sum
        return safe_money_sum(
            (item.savings for item in self.items.all() if item.parent_bundle_id is None),
            currency=self.effective_currency,
        )

    @property
    def voucher_discount_amount(self):
        """Total discount from applied vouchers"""
        from core.utils import safe_money_sum
        return safe_money_sum(
            (voucher.discount_amount for voucher in self.applied_vouchers.all()),
            currency=self.effective_currency,
        )

    @property
    def gift_card_discount_amount(self):
        """Total discount from applied gift cards"""
        from core.utils import safe_money_sum
        return safe_money_sum(
            (gift_card.discount_amount for gift_card in self.applied_gift_cards.all()),
            currency=self.effective_currency,
        )

    @property
    def final_amount(self):
        """Final cart total after all discounts including vouchers and gift cards"""
        from djmoney.money import Money
        result = self.total_amount - self.voucher_discount_amount - self.gift_card_discount_amount
        # Ensure we don't return negative amounts
        if result.amount < 0:
            return Money(0, result.currency)
        return result

    @property
    def total_all_savings(self):
        """Total savings from product discounts, vouchers, and gift cards"""
        return self.total_savings + self.voucher_discount_amount + self.gift_card_discount_amount

    @property
    def requires_shipping(self):
        """Check if cart contains physical products requiring shipping"""
        return any(
            item.product.requires_shipping
            for item in self.items.select_related('product').all()
        )

    @property
    def total_weight(self):
        """
        Calculate total cart weight for shipping calculation.
        Uses variant weights when available, falls back to product weight.
        """
        total = Decimal('0.00')
        for item in self.items.select_related('product', 'variant').all():
            # Use variant weight if available, otherwise fall back to product weight
            if item.variant:
                weight = item.variant.get_effective_weight()
            else:
                weight = item.product.weight

            if weight:
                total += weight * item.quantity
        return total

    @property
    def shipping_dimensions(self):
        """
        Get shipping dimensions (for API-based rate calculation)
        Returns dict with weight, items_count, requires_shipping
        """
        return {
            'weight': float(self.total_weight),
            'items_count': self.total_items,
            'requires_shipping': self.requires_shipping
        }

    def calculate_required_packages(self, optimize_for: str = 'cost'):
        """
        Calculate optimal shipping packages for cart items using bin-packing algorithm.

        Args:
            optimize_for: Optimization strategy:
                - 'cost': Minimize total shipping cost (default)
                - 'volume': Maximize volume utilization
                - 'count': Minimize number of packages

        Returns:
            List of PackingResult instances, or empty list if:
            - Cart has no items requiring shipping
            - No shipping packages are defined
            - Items don't have dimensions/weight

        Example:
            >>> cart = Cart.objects.get(id=123)
            >>> packages = cart.calculate_required_packages()
            >>> for pkg in packages:
            >>>     print(f"{pkg.package.name}: {len(pkg.items)} items, {pkg.total_weight}kg")
        """
        if not self.requires_shipping:
            return []

        # Get items that require shipping
        shippable_items = self.items.filter(
            product__requires_shipping=True
        ).select_related('product', 'variant')

        if not shippable_items.exists():
            return []

        # Use packing algorithm
        from shipping.utils.packing import pack_cart_items
        return pack_cart_items(shippable_items, optimize_for=optimize_for)

    def get_shipping_parcels(self):
        """
        Get parcels array formatted for shipping provider APIs.

        Returns:
            List of parcel dictionaries with format:
            [
                {
                    'length': 10,    # cm
                    'width': 10,     # cm
                    'height': 5,     # cm
                    'weight': 500,   # grams
                    'package_name': 'Small Box',
                    'items_count': 3
                }
            ]

        Falls back to item dimensions if no packages are configured.
        """
        packages = self.calculate_required_packages()

        if packages:
            # Use calculated packages with external dimensions for carriers
            parcels = []
            for pkg_result in packages:
                # Get external dimensions (internal + wall thickness)
                # Shipping carriers need external dimensions for rate calculations
                external_dims = pkg_result.package.get_external_dimensions()

                parcels.append({
                    'length': float(external_dims['length']),
                    'width': float(external_dims['width']),
                    'height': float(external_dims['height']),
                    'weight': float(pkg_result.total_weight * 1000),  # Convert kg to grams
                    'package_name': pkg_result.package.name,
                    'items_count': len(pkg_result.items)
                })
            return parcels

        # Fallback: use individual item dimensions
        parcels = []
        for item in self.items.filter(product__requires_shipping=True).select_related('product', 'variant'):
            if item.variant:
                dims = item.variant.get_shipping_dimensions()
                weight = item.variant.get_shipping_weight()
            else:
                dims = {
                    'length': item.product.length,
                    'width': item.product.width,
                    'height': item.product.height
                }
                weight = item.product.weight

            if all([dims.get('length'), dims.get('width'), dims.get('height'), weight]):
                parcels.append({
                    'length': float(dims['length']),
                    'width': float(dims['width']),
                    'height': float(dims['height']),
                    'weight': float(weight * 1000 * item.quantity),  # kg to grams * quantity
                    'package_name': None,
                    'items_count': item.quantity
                })

        return parcels

    @property
    def subtotal(self):
        """Subtotal before shipping and tax (alias for total_amount)"""
        return self.total_amount

    @property
    def tax_amount(self):
        """Tax amount (calculated during checkout)"""
        # Will be calculated by TaxService
        return getattr(self, '_calculated_tax', Decimal('0.00'))

    @property
    def grand_total(self):
        """Final total including shipping, tax, minus discounts"""
        from djmoney.money import Money
        final = self.final_amount
        shipping = self.shipping_cost
        # Normalize shipping currency to match cart items currency (shipping_cost field
        # defaults to USD but the store may use a different currency)
        if shipping.currency != final.currency:
            shipping = Money(shipping.amount, final.currency)
        return final + shipping + self.tax_amount

    def calculate_shipping(self, shipping_address=None, shipping_method=None, user=None):
        """
        Calculate shipping cost for cart with rule engine integration

        Args:
            shipping_address: Address object or dict for destination
            shipping_method: ShippingMethod object (if None, returns available methods)
            user: User instance (optional, for customer-specific rules)

        Returns:
            dict with shipping_cost, estimated_delivery, available_methods, rules_applied
        """
        if not self.requires_shipping:
            from djmoney.money import Money
            from core.utils import get_default_currency
            return {
                'shipping_cost': Money(0, get_default_currency()),
                'estimated_delivery': None,
                'message': _('No shipping required'),
                'rules_applied': []
            }

        # If no shipping address provided, cannot calculate
        if not shipping_address:
            return {
                'shipping_cost': None,
                'estimated_delivery': None,
                'available_methods': [],
                'message': _('Shipping address required'),
                'rules_applied': []
            }

        # If no shipping method specified, return available methods
        if not shipping_method:
            available_methods = []
            for method in ShippingMethod.objects.filter(is_active=True):
                # Check if method is available for this cart and address
                cart_available, _reason = method.is_available_for_cart(self)
                address_available, _reason = method.is_available_for_address(shipping_address)

                if cart_available and address_available:
                    # Calculate cost with rules
                    from shipping.services import ShippingRuleService
                    calculation = ShippingRuleService.calculate_shipping_for_cart(
                        cart=self,
                        shipping_method=method,
                        address=shipping_address,
                        user=user
                    )

                    available_methods.append({
                        'id': method.id,
                        'name': method.name,
                        'description': method.description,
                        'cost': calculation['final_cost'],
                        'base_cost': calculation['base_cost'],
                        'min_delivery_days': method.min_delivery_days,
                        'max_delivery_days': method.max_delivery_days,
                        'estimated_delivery': method.get_estimated_delivery_date(),
                        'rules_applied': calculation['rules_applied'],
                        'total_discount': calculation['total_discount'],
                        'total_surcharge': calculation['total_surcharge'],
                    })

            return {
                'shipping_cost': None,
                'estimated_delivery': None,
                'available_methods': available_methods,
                'message': _('Available shipping methods retrieved'),
                'rules_applied': []
            }

        # Calculate shipping for specific method with rule engine
        from shipping.services import ShippingRuleService
        calculation = ShippingRuleService.calculate_shipping_for_cart(
            cart=self,
            shipping_method=shipping_method,
            address=shipping_address,
            user=user
        )

        return {
            'shipping_cost': calculation['final_cost'],
            'base_cost': calculation['base_cost'],
            'estimated_delivery': shipping_method.get_estimated_delivery_date(),
            'method_name': calculation['method_name'],
            'method_type': calculation['method_type'],
            'rules_applied': calculation['rules_applied'],
            'total_discount': calculation['total_discount'],
            'total_surcharge': calculation['total_surcharge'],
            'calculation_breakdown': calculation['calculation_breakdown'],
            'message': _('Shipping calculated successfully')
        }

    def set_shipping_method(self, shipping_method, shipping_cost=None):
        """
        Set shipping method and update cart totals

        Args:
            shipping_method: ShippingMethod instance
            shipping_cost: Calculated shipping cost (optional if method has flat rate)
        """
        self.shipping_method = shipping_method

        if shipping_cost is not None:
            self.shipping_cost = shipping_cost
        elif shipping_method and hasattr(shipping_method, 'flat_rate_cost'):
            self.shipping_cost = shipping_method.flat_rate_cost
        else:
            self.shipping_cost = Decimal('0.00')

        self.save(update_fields=['shipping_method', 'shipping_cost'])

    def clear_shipping(self):
        """Clear shipping information (useful when address changes)"""
        self.shipping_method = None
        self.shipping_cost = Decimal('0.00')
        self.estimated_delivery_date = None
        self.save(update_fields=['shipping_method', 'shipping_cost', 'estimated_delivery_date'])

    def clear(self):
        """Clear all items from cart"""
        self.items.all().delete()
    
    def apply_voucher(self, voucher_code, user=None):
        """
        Apply a voucher to the cart
        Returns (success: bool, message: str, discount_amount: Decimal)
        """
        from vouchers.models import VoucherCode, AppliedVoucher
        from decimal import Decimal
        
        try:
            voucher = VoucherCode.objects.get(code=voucher_code, is_active=True)
        except VoucherCode.DoesNotExist:
            return False, "Invalid voucher code", Decimal('0.00')
        
        # Check if voucher is already applied
        if self.applied_vouchers.filter(voucher=voucher).exists():
            return False, "Voucher already applied", Decimal('0.00')
        
        # Check if user can use this voucher
        if user:
            can_use, message = voucher.can_be_used_by_customer(user)
            if not can_use:
                return False, message, Decimal('0.00')
        
        # Check voucher combination rules
        if voucher.cannot_combine_with_other_vouchers and self.applied_vouchers.exists():
            return False, "This voucher cannot be combined with other vouchers", Decimal('0.00')

        # Reverse check: if cart already has a non-combinable voucher, reject new one
        if self.applied_vouchers.filter(voucher__cannot_combine_with_other_vouchers=True).exists():
            return False, "Cart already has a voucher that cannot be combined with others", Decimal('0.00')
        
        # Check if cart has sale items (if voucher restricts this)
        if voucher.cannot_combine_with_sale_items:
            from djmoney.money import Money
            has_sale_items = any(item.savings > Money(0, item.savings.currency) for item in self.items.all())
            if has_sale_items:
                return False, "This voucher cannot be used with sale items", Decimal('0.00')

        # Check minimum order value
        if voucher.min_order_value and self.total_amount < voucher.min_order_value:
            return False, f"Minimum order value ${voucher.min_order_value.amount} required", Decimal('0.00')

        # Calculate eligible amount for discount
        eligible_amount = self._calculate_eligible_amount_for_voucher(voucher)

        from djmoney.money import Money
        if eligible_amount == Money(0, eligible_amount.currency):
            return False, "No eligible items for this voucher", Decimal('0.00')

        # Calculate discount
        discount_amount = voucher.calculate_discount(self.total_amount, eligible_amount)

        if discount_amount == Money(0, discount_amount.currency):
            return False, "Voucher provides no discount", Decimal('0.00')
        
        # Apply the voucher
        AppliedVoucher.objects.create(
            cart=self,
            voucher=voucher,
            discount_amount=discount_amount
        )
        
        return True, "Voucher applied successfully", discount_amount
    
    def remove_voucher(self, voucher_code):
        """Remove a voucher from the cart"""
        removed = self.applied_vouchers.filter(voucher__code=voucher_code).delete()[0]
        return removed > 0
    
    def _calculate_eligible_amount_for_voucher(self, voucher):
        """Calculate the amount eligible for voucher discount"""
        from djmoney.money import Money
        from core.utils import safe_money_sum

        if voucher.application_scope == 'cart':
            # Whole cart eligible
            eligible_amount = self.total_amount

            # Exclude sale items if required
            if voucher.exclude_sale_items:
                eligible_amount = safe_money_sum(
                    (item.total_price for item in self.items.all()
                     if item.savings == Money(0, item.savings.currency)),
                    currency=self.effective_currency,
                )

        elif voucher.application_scope == 'products':
            # Only specific products eligible
            eligible_products = voucher.eligible_products.all()
            eligible_amount = safe_money_sum(
                (item.total_price for item in self.items.all()
                 if item.product in eligible_products and
                 (not voucher.exclude_sale_items or item.savings == Money(0, item.savings.currency))),
                currency=self.effective_currency,
            )

        elif voucher.application_scope == 'categories':
            # Only specific categories eligible
            eligible_categories = voucher.eligible_categories.all()
            eligible_amount = safe_money_sum(
                (item.total_price for item in self.items.all()
                 if item.product.category in eligible_categories and
                 (not voucher.exclude_sale_items or item.savings == Money(0, item.savings.currency))),
                currency=self.effective_currency,
            )

        else:
            eligible_amount = Money(0, self.effective_currency)

        return eligible_amount
    
    def recalculate_voucher_discounts(self):
        """Recalculate all applied voucher discounts (useful after cart changes)"""
        for applied_voucher in self.applied_vouchers.all():
            voucher = applied_voucher.voucher
            eligible_amount = self._calculate_eligible_amount_for_voucher(voucher)
            new_discount = voucher.calculate_discount(self.total_amount, eligible_amount)
            
            if new_discount != applied_voucher.discount_amount:
                applied_voucher.discount_amount = new_discount
                applied_voucher.save()
    
    def apply_gift_card(self, gift_card_code, customer_currency=None):
        """
        Apply a gift card to the cart.

        Args:
            gift_card_code: Gift card code to apply
            customer_currency: Customer's active currency code (from session/middleware).
                Used to validate foreign-currency gift cards. If None, falls back to
                cart's internal currency (base currency).

        Returns:
            tuple: (success, message, discount_amount)
        """
        from catalog.models import GiftCard
        from djmoney.money import Money
        from decimal import Decimal

        try:
            gift_card = GiftCard.objects.get(code=gift_card_code)
        except GiftCard.DoesNotExist:
            return False, _("Invalid gift card code"), Decimal('0.00')

        # Check if gift card is already applied
        if self.applied_gift_cards.filter(gift_card=gift_card).exists():
            return False, _("Gift card already applied"), Decimal('0.00')

        # Check if gift card is valid
        if not gift_card.is_valid:
            if not gift_card.is_active:
                return False, _("Gift card is not active"), Decimal('0.00')
            elif gift_card.is_expired:
                return False, _("Gift card has expired"), Decimal('0.00')
            elif gift_card.is_fully_redeemed:
                return False, _("Gift card has been fully redeemed"), Decimal('0.00')
            else:
                return False, _("Gift card cannot be used"), Decimal('0.00')

        gc_currency = gift_card.current_balance.currency.code
        cart_currency = self.total_amount.currency.code
        is_foreign_currency_gc = gc_currency != cart_currency

        # Currency validation
        if is_foreign_currency_gc:
            # Foreign-currency gift card: validate against customer's active currency
            if not customer_currency:
                return False, _(
                    "Currency mismatch. Gift card is in {card_currency}, "
                    "cart is in {cart_currency}"
                ).format(
                    card_currency=gc_currency,
                    cart_currency=cart_currency
                ), Decimal('0.00')

            if gc_currency != customer_currency:
                return False, _(
                    "This gift card is in {card_currency}. Please switch your "
                    "currency to {card_currency} to use it."
                ).format(card_currency=gc_currency), Decimal('0.00')

        # Cannot use gift cards to pay for other gift cards
        has_gift_card_products = self.items.filter(product__product_type='gift_card').exists()
        if has_gift_card_products:
            return False, _("Gift cards cannot be used to purchase other gift cards"), Decimal('0.00')

        # Calculate remaining cart total (in base currency) after vouchers and other gift cards
        amount_after_vouchers = self.total_amount - self.voucher_discount_amount
        remaining_total = amount_after_vouchers - self.gift_card_discount_amount

        if remaining_total.amount <= 0:
            return False, _("Cart total is already covered"), Decimal('0.00')

        if is_foreign_currency_gc:
            # Foreign-currency gift card: convert balance to base currency for cart calculations
            from exchange_rates.services.exchange_service import ExchangeRateService
            try:
                fx_service = ExchangeRateService()
                # Convert gift card balance to base currency
                gc_balance_in_base = fx_service.convert(
                    gift_card.current_balance.amount, gc_currency, cart_currency
                )
                rate = fx_service.get_rate(gc_currency, cart_currency)

                # discount_amount is in base currency (for cart math)
                discount_base = Money(
                    min(gc_balance_in_base, remaining_total.amount),
                    cart_currency
                )

                # Calculate the corresponding amount in the gift card's currency
                if discount_base.amount == gc_balance_in_base:
                    # Using full gift card balance
                    original_amount = gift_card.current_balance
                else:
                    # Partial use: convert the base discount back to gc currency
                    original_in_gc = fx_service.convert(
                        discount_base.amount, cart_currency, gc_currency
                    )
                    original_amount = Money(original_in_gc, gc_currency)

                AppliedGiftCard.objects.create(
                    cart=self,
                    gift_card=gift_card,
                    discount_amount=discount_base,
                    original_currency_amount=original_amount,
                    gc_exchange_rate=rate,
                )
                applied_discount = discount_base.amount
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Gift card currency conversion failed: {e}")
                return False, _("Unable to process gift card currency conversion"), Decimal('0.00')
        else:
            # Same-currency gift card (base currency): existing simple logic
            discount_amount = Money(
                min(gift_card.current_balance.amount, remaining_total.amount),
                cart_currency
            )
            AppliedGiftCard.objects.create(
                cart=self,
                gift_card=gift_card,
                discount_amount=discount_amount
            )
            applied_discount = discount_amount.amount

        return True, _("Gift card applied successfully"), applied_discount

    def remove_gift_card(self, gift_card_code):
        """
        Remove a gift card from the cart.

        Args:
            gift_card_code: Gift card code to remove

        Returns:
            bool: True if removed, False if not found
        """
        removed = self.applied_gift_cards.filter(gift_card__code=gift_card_code).delete()[0]
        return removed > 0

    def recalculate_gift_card_discounts(self):
        """
        Recalculate all applied gift card discounts.
        Useful after cart changes to ensure gift card discounts are still valid.
        Handles both base-currency and foreign-currency gift cards.
        """
        from djmoney.money import Money

        cart_currency = self.total_amount.currency.code

        # Calculate amount after vouchers
        amount_after_vouchers = self.total_amount - self.voucher_discount_amount
        remaining_total = amount_after_vouchers

        for applied_gift_card in self.applied_gift_cards.all():
            gift_card = applied_gift_card.gift_card

            # Check if gift card is still valid
            if not gift_card.is_valid:
                applied_gift_card.delete()
                continue

            gc_currency = gift_card.current_balance.currency.code
            is_foreign = gc_currency != cart_currency

            if is_foreign:
                # Foreign-currency gift card: re-convert with current rate
                try:
                    from exchange_rates.services.exchange_service import ExchangeRateService
                    fx_service = ExchangeRateService()
                    gc_balance_in_base = fx_service.convert(
                        gift_card.current_balance.amount, gc_currency, cart_currency
                    )
                    rate = fx_service.get_rate(gc_currency, cart_currency)

                    new_discount = Money(
                        min(gc_balance_in_base, remaining_total.amount),
                        cart_currency
                    )

                    if new_discount.amount <= 0:
                        applied_gift_card.delete()
                        continue

                    # Calculate corresponding native currency amount
                    if new_discount.amount == gc_balance_in_base:
                        original_amount = gift_card.current_balance
                    else:
                        original_in_gc = fx_service.convert(
                            new_discount.amount, cart_currency, gc_currency
                        )
                        original_amount = Money(original_in_gc, gc_currency)

                    updated = False
                    if new_discount != applied_gift_card.discount_amount:
                        applied_gift_card.discount_amount = new_discount
                        updated = True
                    if original_amount != applied_gift_card.original_currency_amount:
                        applied_gift_card.original_currency_amount = original_amount
                        updated = True
                    if rate != applied_gift_card.gc_exchange_rate:
                        applied_gift_card.gc_exchange_rate = rate
                        updated = True
                    if updated:
                        applied_gift_card.save()

                    remaining_total -= new_discount

                except Exception:
                    # If conversion fails, remove the gift card from cart
                    import logging
                    logging.getLogger(__name__).warning(
                        f"Failed to recalculate foreign currency gift card {gift_card.code}, removing"
                    )
                    applied_gift_card.delete()
            else:
                # Base-currency gift card: simple recalculation
                new_discount = Money(
                    min(gift_card.current_balance.amount, remaining_total.amount),
                    cart_currency
                )

                if new_discount.amount <= 0:
                    applied_gift_card.delete()
                elif new_discount != applied_gift_card.discount_amount:
                    applied_gift_card.discount_amount = new_discount
                    applied_gift_card.save()

                remaining_total -= new_discount

    def get_gift_card_summary(self):
        """Get summary of applied gift cards for display"""
        summary = []
        for agc in self.applied_gift_cards.all():
            entry = {
                'code': agc.gift_card.code,
                'discount_amount': float(agc.discount_amount.amount),
                'currency': agc.discount_amount.currency.code,
                'remaining_balance': float(agc.gift_card.current_balance.amount),
                'gift_card_currency': agc.gift_card.current_balance.currency.code,
                'applied_at': agc.applied_at.isoformat(),
            }
            # Include original currency info for foreign-currency gift cards
            if agc.original_currency_amount:
                entry['original_discount_amount'] = float(agc.original_currency_amount.amount)
                entry['original_discount_currency'] = agc.original_currency_amount.currency.code
            summary.append(entry)
        return summary

    def get_voucher_summary(self):
        """Get summary of applied vouchers for display"""
        return [
            {
                'code': av.voucher.code,
                'name': av.voucher.name,
                'discount_amount': av.discount_amount,
                'discount_type': av.voucher.discount_type,
                'description': av.voucher.description
            }
            for av in self.applied_vouchers.select_related('voucher').all()
        ]


class CartItem(models.Model):
    """Individual items in shopping cart"""
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_("Cart")
    )

    # Product references
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        verbose_name=_("Product")
    )
    variant = models.ForeignKey(
        'catalog.ProductVariant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Variant")
    )

    # Quantity and pricing
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantity")
    )
    unit_price = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        verbose_name=_("Unit Price")
    )

    # Customization options (for personalized products)
    customizations = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Product customizations with calculated prices: {customization_option_id: {'value': '...', 'calculated_price': '10.00'}}"),
        verbose_name=_("Customizations")
    )

    # Subscription configuration (for subscription products)
    is_subscription = models.BooleanField(
        default=False,
        verbose_name=_("Is Subscription"),
        help_text=_("Whether this item will be purchased as a subscription")
    )
    subscription_plan = models.ForeignKey(
        'subscriptions.SubscriptionPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Subscription Plan"),
        help_text=_("Selected subscription plan for recurring billing")
    )
    pricing_tier = models.ForeignKey(
        'subscriptions.PlanPricingTier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Pricing Tier"),
        help_text=_("Selected pricing tier (billing frequency) for subscription")
    )
    payment_token = models.ForeignKey(
        'subscriptions.PaymentToken',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Payment Token"),
        help_text=_("Saved payment method for subscription billing (required for subscriptions)")
    )

    # Bundle tracking
    parent_bundle = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='component_items',
        verbose_name=_("Parent Bundle"),
        help_text=_("If this is a bundle component, reference to bundle CartItem")
    )

    # Booking data (for booking products)
    booking_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Booking details: {start_datetime, end_datetime, resource_id, persons, timezone}"),
        verbose_name=_("Booking Data")
    )

    # Cart item notes
    notes = models.TextField(
        blank=True,
        help_text=_("Customer notes for this item"),
        verbose_name=_("Notes")
    )

    # POS manual item-level discount (staff-applied discounts)
    DISCOUNT_TYPE_CHOICES = [
        ('none', _('None')),
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed Amount')),
    ]
    manual_discount_type = models.CharField(
        _('manual discount type'),
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default='none'
    )
    manual_discount_value = models.DecimalField(
        _('manual discount value'),
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text=_('Discount value (percentage or fixed amount)')
    )
    manual_discount_applied_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pos_item_discounts',
        verbose_name=_('discount applied by')
    )
    manual_discount_approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pos_item_discount_approvals',
        verbose_name=_('discount approved by'),
        help_text=_('Manager who approved the discount if it exceeded staff limit')
    )
    manual_discount_reason = models.CharField(
        _('discount reason'),
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        # Note: No unique_together constraint to allow multiple items with same product but different customizations
        # Deduplication logic is handled in cart service layer
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        variant_info = f" - {self.variant.name}" if self.variant else ""
        return f"{self.quantity}x {self.product.name}{variant_info}"

    @property
    def customization_price(self):
        """Total customization price (per unit)"""
        from djmoney.money import Money
        from decimal import Decimal

        if not self.customizations:
            return Money(0, self.unit_price.currency)

        total = Decimal('0.00')
        for option_id, customization_data in self.customizations.items():
            if isinstance(customization_data, dict):
                price = customization_data.get('calculated_price', 0)
                total += Decimal(str(price))

        return Money(total, self.unit_price.currency)

    @property
    def total_price(self):
        """Total price for this line item (including customizations)"""
        return (self.unit_price + self.customization_price) * self.quantity

    @property
    def savings(self):
        """Savings from product discount (difference between regular price and unit price)"""
        from djmoney.money import Money
        if self.product.price > self.unit_price:
            return (self.product.price - self.unit_price) * self.quantity
        return Money(0, self.product.price.currency)

    @property
    def requires_shipping(self):
        """Check if this item requires shipping"""
        return self.product.requires_shipping

    @property
    def item_weight(self):
        """Total weight for this line item"""
        if self.product.weight:
            return self.product.weight * self.quantity
        return Decimal('0.00')

    @property
    def shipping_class(self):
        """Get shipping class for rate calculation"""
        return getattr(self.product, 'shipping_class', None)

    def save(self, *args, **kwargs):
        # Set unit price from product/variant if not set
        if not self.unit_price:
            # Use the cart's operating currency for price lookup
            cart_currency = self.cart.effective_currency if self.cart_id else None
            base_currency = str(self.product.price.currency) if self.product.price else None

            if cart_currency and base_currency and cart_currency != base_currency:
                self.unit_price = self.product.get_price_in_currency(cart_currency)
            elif self.variant:
                self.unit_price = self.variant.get_price()
            else:
                self.unit_price = self.product.price
        super().save(*args, **kwargs)


class Wishlist(DesignMixin):
    """Customer wishlist with design customization"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    name = models.CharField(
        max_length=200,
        default=_("My Wishlist"),
        verbose_name=_("Name")
    )

    # Wishlist display options
    WISHLIST_LAYOUTS = [
        ('grid', _('Grid Layout')),
        ('list', _('List Layout')),
        ('compact', _('Compact View')),
        ('detailed', _('Detailed View')),
    ]

    wishlist_layout = models.CharField(
        max_length=20,
        choices=WISHLIST_LAYOUTS,
        default='grid',
        help_text=_("How wishlist items are displayed"),
        verbose_name=_("Wishlist Layout")
    )

    # Privacy and sharing
    is_public = models.BooleanField(
        default=False,
        verbose_name=_("Is Public")
    )
    share_slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Share Slug")
    )

    # Display preferences
    show_prices = models.BooleanField(
        default=True,
        verbose_name=_("Show Prices")
    )
    show_availability = models.BooleanField(
        default=True,
        verbose_name=_("Show Availability")
    )
    show_add_to_cart = models.BooleanField(
        default=True,
        verbose_name=_("Show Add to Cart")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    @property
    def total_items(self):
        """Total number of items in wishlist"""
        return self.items.count()

    @property
    def total_value(self):
        """Total value of wishlist items"""
        from core.utils import safe_money_sum
        return safe_money_sum((item.product.price for item in self.items.all()))


class WishlistItem(models.Model):
    """Individual items in wishlist"""
    wishlist = models.ForeignKey(
        Wishlist,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name=_("Wishlist")
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        verbose_name=_("Product")
    )
    variant = models.ForeignKey(
        'catalog.ProductVariant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Variant")
    )

    # Item notes and preferences
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes")
    )
    priority = models.CharField(
        max_length=10,
        choices=[
            ('low', _('Low')),
            ('medium', _('Medium')),
            ('high', _('High')),
        ],
        default='medium',
        verbose_name=_("Priority")
    )

    # Notifications
    notify_when_available = models.BooleanField(
        default=False,
        verbose_name=_("Notify When Available")
    )
    notify_when_on_sale = models.BooleanField(
        default=False,
        verbose_name=_("Notify When On Sale")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Wishlist Item")
        verbose_name_plural = _("Wishlist Items")
        unique_together = ['wishlist', 'product', 'variant']

    def __str__(self):
        variant_info = f" - {self.variant.name}" if self.variant else ""
        return f"{self.product.name}{variant_info}"


class RecentlyViewed(models.Model):
    """Track recently viewed products for personalization"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("User")
    )
    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Session Key")
    )
    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        verbose_name=_("Product")
    )

    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Viewed At"))
    view_count = models.PositiveIntegerField(default=1, verbose_name=_("View Count"))

    class Meta:
        verbose_name = _("Recently Viewed Product")
        verbose_name_plural = _("Recently Viewed Products")
        unique_together = ['user', 'session_key', 'product']
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['user', '-viewed_at']),
            models.Index(fields=['session_key', '-viewed_at']),
        ]

    def __str__(self):
        user_info = self.user.username if self.user else _("Session: {session}").format(session=self.session_key[:8] if self.session_key else "N/A")
        return _("{product} viewed by {user}").format(product=self.product.name, user=user_info)

class ShippingMethod(DesignMixin):
    """
    Shipping methods available for checkout
    Supports various pricing types and eligibility rules
    Will be moved to dedicated shipping app in future
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )

    # Method type
    METHOD_TYPES = [
        ('flat_rate', _('Flat Rate')),
        ('real_time', _('Real-Time Carrier Rates')),
        ('local_pickup', _('Local Pickup')),
        ('table_rate', _('Table Rate')),
    ]
    method_type = models.CharField(
        max_length=20,
        choices=METHOD_TYPES,
        verbose_name=_("Method Type")
    )

    # Pricing
    flat_rate_cost = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        help_text=_("Fixed shipping cost (for flat_rate type)"),
        verbose_name=_("Flat Rate Cost")
    )

    # Shipping zones (zone-based geographic configuration)
    zones = models.ManyToManyField(
        'shipping.ShippingZone',
        blank=True,
        related_name='shipping_methods',
        verbose_name=_("Shipping Zones"),
        help_text=_("Zones where this shipping method is available. If empty, legacy country/state restrictions apply.")
    )

    # Pickup locations (for local_pickup method type)
    pickup_locations = models.ManyToManyField(
        'shipping.Location',
        blank=True,
        related_name='pickup_methods',
        verbose_name=_("Pickup Locations"),
        help_text=_("Locations where customers can pick up orders using this shipping method. Only applies to 'local_pickup' method type.")
    )

    # Delivery time
    min_delivery_days = models.PositiveIntegerField(
        default=3,
        help_text=_("Minimum delivery time in business days"),
        verbose_name=_("Minimum Delivery Days")
    )

    max_delivery_days = models.PositiveIntegerField(
        default=7,
        help_text=_("Maximum delivery time in business days"),
        verbose_name=_("Maximum Delivery Days")
    )

    # Display
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Font Awesome icon class (e.g., 'fa-truck', 'fa-box')"),
        verbose_name=_("Icon")
    )

    image = models.ForeignKey(
        'media_library.MediaAsset',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='shipping_method_uses',
        help_text=_("Custom shipping method image from media library. If provided, this takes priority over icon."),
        verbose_name=_("Image")
    )

    sort_order = models.IntegerField(
        default=0,
        verbose_name=_("Sort Order")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )

    # Carrier integration (for real-time rates)
    CARRIER_CHOICES = [
        ('usps', 'USPS'),
        ('fedex', 'FedEx'),
        ('ups', 'UPS'),
        ('dhl', 'DHL'),
        ('custom', _('Custom Carrier')),
    ]
    carrier = models.CharField(
        max_length=50,
        blank=True,
        choices=CARRIER_CHOICES,
        verbose_name=_("Carrier")
    )

    carrier_service_code = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("Carrier-specific service code"),
        verbose_name=_("Carrier Service Code")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Shipping Method")
        verbose_name_plural = _("Shipping Methods")
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'sort_order']),
            models.Index(fields=['method_type', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def is_available_for_cart(self, cart):
        """
        Check if this shipping method is available for given cart

        Args:
            cart: Cart instance

        Returns:
            tuple: (is_available: bool, reason: str)
        """
        if not self.is_active:
            return False, _("Shipping method is not active")

        # Check if cart requires shipping
        if not cart.requires_shipping and self.method_type != 'local_pickup':
            return False, _("Cart contains only digital products")

        # Check visibility promotions (controls_visibility=True)
        from shipping.models import ShippingPromotion
        visibility_promotions = ShippingPromotion.objects.filter(
            is_active=True,
            controls_visibility=True,
            shipping_methods=self,
        )
        if visibility_promotions.exists():
            # At least one visibility promotion targets this method
            # The method is only shown if ANY visibility promotion's conditions are met
            any_match = False
            for promo in visibility_promotions:
                user = cart.user if cart.user_id else None
                applies, _reason = promo.applies_to_cart(
                    cart=cart,
                    address=getattr(cart, '_shipping_address', None),
                    shipping_method=self,
                    user=user
                )
                if applies:
                    any_match = True
                    break
            if not any_match:
                return False, _("Not available for this cart")

        return True, _("Available")

    def is_available_for_address(self, address):
        """
        Check if this shipping method is available for given address

        Checks zones first (Phase 2), then falls back to legacy restrictions.

        Args:
            address: Address instance or dict with country and state

        Returns:
            tuple: (is_available: bool, reason: str)
        """
        # Handle both model instances and dicts (from JSONField)
        if hasattr(address, 'country'):
            country = address.country
            state = address.state
            postal_code = address.postal_code
        else:
            country = address.get('country') if address else None
            state = address.get('state', '') if address else ''
            postal_code = address.get('postal_code', '') if address else ''

        if not country:
            return True, _("No geographic restrictions")

        # Check if method has zones assigned
        zones = self.zones.filter(is_active=True)
        if zones.exists():
            # If zones are assigned, check if address matches any zone
            for zone in zones:
                if zone.matches_address(address):
                    return True, _("Available in {zone}").format(zone=zone.name)

            # Address doesn't match any assigned zone
            return False, _("Not available in your location")

        # No zones assigned - available worldwide
        return True, _("Available worldwide")

    def calculate_cost(self, cart, address=None):
        """
        Calculate base shipping cost for this method

        Returns base cost only. For final cost with promotions applied,
        use ShippingPromotionService.calculate_shipping_for_cart().

        Args:
            cart: Cart instance
            address: Address instance (optional)

        Returns:
            Decimal: Base shipping cost (before rules)
        """
        base_cost = Decimal('0.00')

        if self.method_type == 'flat_rate':
            base_cost = self.flat_rate_cost.amount if self.flat_rate_cost else Decimal('0.00')

        elif self.method_type == 'table_rate':
            # Use rate tables (weight, price, or quantity based)
            from shipping.services import ShippingRuleService
            rate = ShippingRuleService.calculate_rate_table_cost(
                shipping_method=self,
                cart=cart,
                address=address
            )
            base_cost = rate.amount if rate else Decimal('0.00')

        elif self.method_type == 'real_time':
            # Placeholder - will integrate with carrier APIs
            base_cost = Decimal('0.00')

        elif self.method_type == 'local_pickup':
            base_cost = Decimal('0.00')

        return base_cost

    def get_estimated_delivery_date(self):
        """Get estimated delivery date based on min delivery days"""
        from django.utils import timezone
        from datetime import timedelta

        today = timezone.now().date()
        min_date = today + timedelta(days=self.min_delivery_days)

        return min_date


class TaxRate(models.Model):
    """
    Tax rates by geographic region
    Supports state/province, city, and postal code level taxation
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name")
    )

    # Geographic scope
    country = models.CharField(
        max_length=2,
        help_text=_("ISO 3166-1 alpha-2 country code"),
        verbose_name=_("Country")
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("State/Province/Region"),
        verbose_name=_("State")
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("City name (optional)"),
        verbose_name=_("City")
    )

    postal_codes = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of specific postal codes (optional)"),
        verbose_name=_("Postal Codes")
    )

    # Tax rate
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        help_text=_("Tax rate as decimal (e.g., 0.0825 for 8.25%)"),
        verbose_name=_("Rate")
    )

    # Tax type
    TAX_TYPES = [
        ('sales_tax', _('Sales Tax')),
        ('vat', 'VAT'),
        ('gst', 'GST'),
        ('custom', _('Custom Tax')),
    ]
    tax_type = models.CharField(
        max_length=20,
        choices=TAX_TYPES,
        default='sales_tax',
        verbose_name=_("Tax Type")
    )

    # Application rules
    applies_to_shipping = models.BooleanField(
        default=False,
        help_text=_("Apply tax to shipping costs"),
        verbose_name=_("Applies to Shipping")
    )

    compound = models.BooleanField(
        default=False,
        help_text=_("Calculate on top of other taxes (compound tax)"),
        verbose_name=_("Compound Tax")
    )

    # Product eligibility
    exempt_product_types = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Product types exempt from this tax (e.g., ['digital', 'service'])"),
        verbose_name=_("Exempt Product Types")
    )

    exempt_categories = models.ManyToManyField(
        'catalog.Category',
        blank=True,
        help_text=_("Categories exempt from this tax"),
        verbose_name=_("Exempt Categories")
    )

    # Priority (for overlapping rules)
    priority = models.IntegerField(
        default=0,
        help_text=_("Higher priority rules take precedence"),
        verbose_name=_("Priority")
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Tax Rate")
        verbose_name_plural = _("Tax Rates")
        ordering = ['-priority', 'country', 'state', 'city']
        indexes = [
            models.Index(fields=['country', 'state', 'city']),
            models.Index(fields=['is_active', '-priority']),
        ]

    def __str__(self):
        location = self.country
        if self.state:
            location += f", {self.state}"
        if self.city:
            location += f", {self.city}"
        return _("{name} ({location}) - {rate}%").format(
            name=self.name,
            location=location,
            rate=self.rate * 100
        )

    def applies_to_product(self, product):
        """Check if tax applies to given product"""
        # Check product type exemptions
        if product.product_type in self.exempt_product_types:
            return False

        # Check category exemptions
        if self.exempt_categories.filter(id=product.category_id).exists():
            return False

        return True

    def calculate_tax(self, amount):
        """Calculate tax amount for given subtotal"""
        return amount * self.rate


class TaxPresetGroup(models.Model):
    """
    A collection of preset tax rates for a region/jurisdiction.
    Stored in DB so rates can be updated via API/upgrade server
    without code changes.
    """
    REGION_CHOICES = [
        ('europe', _('Europe')),
        ('north_america', _('North America')),
        ('asia_pacific', _('Asia Pacific')),
        ('middle_east', _('Middle East')),
        ('africa', _('Africa')),
        ('latin_america', _('Latin America')),
        ('oceania', _('Oceania')),
    ]

    key = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Unique identifier (e.g., eu_vat, us_sales_tax)"),
        verbose_name=_("Key")
    )
    name = models.CharField(
        max_length=200,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    icon = models.CharField(
        max_length=50,
        default='fas fa-percentage',
        help_text=_("Font Awesome icon class"),
        verbose_name=_("Icon")
    )
    tax_type = models.CharField(
        max_length=20,
        choices=TaxRate.TAX_TYPES,
        default='vat',
        verbose_name=_("Default Tax Type")
    )
    region = models.CharField(
        max_length=30,
        choices=REGION_CHOICES,
        verbose_name=_("Region")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )
    version = models.CharField(
        max_length=20,
        default='2026.02',
        help_text=_("Version for tracking rate updates"),
        verbose_name=_("Version")
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Updated")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    class Meta:
        verbose_name = _("Tax Preset Group")
        verbose_name_plural = _("Tax Preset Groups")
        ordering = ['region', 'name']

    def __str__(self):
        return self.name


class TaxPresetRate(models.Model):
    """
    Individual preset tax rate within a group.
    Used as templates that merchants can load into their active TaxRate table.
    """
    group = models.ForeignKey(
        TaxPresetGroup,
        on_delete=models.CASCADE,
        related_name='rates',
        verbose_name=_("Preset Group")
    )
    country = models.CharField(
        max_length=2,
        help_text=_("ISO 3166-1 alpha-2 country code"),
        verbose_name=_("Country Code")
    )
    country_name = models.CharField(
        max_length=100,
        verbose_name=_("Country Name")
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("State/province code (for US/CA presets)"),
        verbose_name=_("State Code")
    )
    state_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("State Name")
    )
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        help_text=_("Tax rate as decimal (e.g., 0.20 for 20%)"),
        verbose_name=_("Rate")
    )
    tax_type = models.CharField(
        max_length=20,
        choices=TaxRate.TAX_TYPES,
        default='vat',
        verbose_name=_("Tax Type")
    )
    notes = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Optional notes (e.g., 'Raised from 22% in July 2025')"),
        verbose_name=_("Notes")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active")
    )

    class Meta:
        verbose_name = _("Tax Preset Rate")
        verbose_name_plural = _("Tax Preset Rates")
        ordering = ['group', 'country', 'state']
        indexes = [
            models.Index(fields=['group', 'country']),
        ]

    def __str__(self):
        location = self.country_name
        if self.state_name:
            location += f", {self.state_name}"
        return f"{location} - {self.rate * 100}%"


class CheckoutSession(models.Model):
    """
    Temporary checkout session data
    Stores checkout state including shipping and tax calculations
    """
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE,
        related_name='checkout_session',
        verbose_name=_("Cart")
    )

    # Addresses
    shipping_address = models.ForeignKey(
        'orders.Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checkout_sessions_as_shipping',
        verbose_name=_("Shipping Address")
    )

    billing_address = models.ForeignKey(
        'orders.Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checkout_sessions_as_billing',
        verbose_name=_("Billing Address")
    )

    billing_same_as_shipping = models.BooleanField(
        default=True,
        verbose_name=_("Billing Same as Shipping")
    )

    # Temporary address data (for guest users or during checkout)
    # These store address data without creating Address records until order is placed
    shipping_address_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Shipping Address Data"),
        help_text=_("Temporary shipping address data (not saved to Address model until order placed)")
    )

    billing_address_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Billing Address Data"),
        help_text=_("Temporary billing address data (not saved to Address model until order placed)")
    )

    # Shipping selection
    selected_shipping_method = models.ForeignKey(
        'ShippingMethod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Selected Shipping Method")
    )

    # Calculated shipping
    shipping_cost = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        default=0,
        verbose_name=_("Shipping Cost")
    )

    estimated_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Estimated Delivery Date")
    )

    # Available shipping methods (cached)
    available_shipping_methods = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Cached list of available shipping methods with rates"),
        verbose_name=_("Available Shipping Methods")
    )

    # Tax calculation
    tax_breakdown = models.JSONField(
        default=dict,
        blank=True,
        help_text=_("Detailed tax breakdown by jurisdiction"),
        verbose_name=_("Tax Breakdown")
    )

    tax_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        default=0,
        verbose_name=_("Tax Amount")
    )

    # Payment
    payment_provider = models.ForeignKey(
        'payment_providers.PaymentProviderAccount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='checkout_sessions',
        verbose_name=_("Payment Provider")
    )

    # Order totals (calculated)
    subtotal = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        default=0,
        verbose_name=_("Subtotal")
    )

    discount_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        default=0,
        verbose_name=_("Discount Amount")
    )

    gift_card_discount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        default=0,
        verbose_name=_("Gift Card Discount"),
        help_text=_("Total discount from applied gift cards")
    )

    total_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        default=0,
        help_text=_("Final total: subtotal + shipping + tax - discounts"),
        verbose_name=_("Total Amount")
    )

    # Session management
    CHECKOUT_STEPS = [
        ('cart', _('Cart Review')),
        ('shipping_address', _('Shipping Address')),
        ('shipping_method', _('Shipping Method')),
        ('billing', _('Billing Information')),
        ('payment', _('Payment Method')),
        ('review', _('Order Review')),
    ]
    step_completed = models.CharField(
        max_length=20,
        choices=CHECKOUT_STEPS,
        default='cart',
        verbose_name=_("Step Completed")
    )

    expires_at = models.DateTimeField(verbose_name=_("Expires At"))
    metadata = models.JSONField(
        default=dict, blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Extra metadata (e.g., marketplace purchase info)")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Checkout Session")
        verbose_name_plural = _("Checkout Sessions")
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return _("Checkout for {cart}").format(cart=self.cart)

    def recalculate_totals(self):
        """
        Recalculate all totals (subtotal, shipping, tax, final total)
        Should be called whenever cart items, shipping, or address changes
        """
        from djmoney.money import Money

        # Use the cart's operating currency (respects multi-currency)
        currency = self.cart.effective_currency
        zero = Money(0, currency)

        # Subtotal from cart
        self.subtotal = self.cart.subtotal

        # Discount from cart vouchers
        self.discount_amount = self.cart.voucher_discount_amount

        # Gift card discount from cart
        self.gift_card_discount = self.cart.gift_card_discount_amount

        # Shipping cost (recalculate with promo-aware service)
        # Check both ForeignKey and JSONField for address
        address = self.shipping_address or self.shipping_address_data
        if address and self.selected_shipping_method:
            from shipping.services import ShippingRuleService
            calculation = ShippingRuleService.calculate_shipping_for_cart(
                cart=self.cart,
                shipping_method=self.selected_shipping_method,
                address=address,
                user=self.cart.user if self.cart.user_id else None
            )
            self.shipping_cost = calculation['final_cost']
        else:
            self.shipping_cost = zero

        # Tax calculation
        # Check both ForeignKey and JSONField for address
        if address:
            self.tax_amount, self.tax_breakdown = self._calculate_tax()
        else:
            self.tax_amount = zero
            self.tax_breakdown = {}

        # Ensure all Money values use the same currency before arithmetic
        for attr in ('shipping_cost', 'tax_amount', 'discount_amount', 'gift_card_discount'):
            val = getattr(self, attr)
            if hasattr(val, 'currency') and val.currency != currency:
                setattr(self, attr, Money(val.amount, currency))

        # Final total (subtract both voucher discounts and gift card discounts)
        self.total_amount = (
            self.subtotal +
            self.shipping_cost +
            self.tax_amount -
            self.discount_amount -
            self.gift_card_discount
        )

        # Ensure total doesn't go negative
        if self.total_amount.amount < 0:
            self.total_amount = zero

        self.save(update_fields=[
            'subtotal',
            'shipping_cost',
            'tax_amount',
            'tax_breakdown',
            'discount_amount',
            'gift_card_discount',
            'total_amount'
        ])

    def _calculate_tax(self):
        """
        Calculate tax based on shipping address using TaxService.
        Returns: (total_tax: Decimal, breakdown: dict)
        """
        # Check both ForeignKey and JSONField for address
        addr = self.shipping_address or self.shipping_address_data
        if not addr:
            return Decimal('0.00'), {}

        from cart.services.tax_service import TaxService

        # Gather cart items as (product, quantity, line_total) tuples
        items = []
        for item in self.cart.items.select_related('product', 'variant'):
            items.append((
                item.product,
                item.quantity,
                item.total_price.amount,  # Extract Decimal amount from Money object
            ))

        if not items:
            return Decimal('0.00'), {}

        # Handle both model instance and dict
        if hasattr(addr, 'country'):
            country = addr.country
            state = getattr(addr, 'state', '') or ''
            city = getattr(addr, 'city', '') or ''
            postal_code = getattr(addr, 'postal_code', '') or ''
        else:
            country = addr.get('country', '')
            state = addr.get('state', '')
            city = addr.get('city', '')
            postal_code = addr.get('postal_code', '')

        total_tax, breakdown = TaxService.calculate_tax(
            items=items,
            shipping_cost=self.shipping_cost.amount if self.shipping_cost else Decimal('0.00'),
            country=country,
            state=state,
            city=city,
            postal_code=postal_code,
        )

        return total_tax, {'taxes': breakdown}

    def get_available_shipping_methods(self, refresh=False):
        """
        Get available shipping methods for current cart and address

        Integrates Phases 2, 3, and 4:
        - Phase 2: Filters by shipping zones
        - Phase 3: Applies shipping rules to costs
        - Phase 4: Includes pickup locations for local_pickup methods

        Args:
            refresh: Force refresh of cached methods

        Returns:
            list: Available shipping methods with calculated rates, rules applied, and locations
        """
        if not refresh and self.available_shipping_methods:
            return self.available_shipping_methods

        # Get address - use JSONField data if ForeignKey is not set
        # (during checkout, address is stored in shipping_address_data until order is placed)
        address = self.shipping_address or self.shipping_address_data

        if not address:
            return []

        from shipping.services import ShippingRuleService

        methods = []
        for method in ShippingMethod.objects.filter(is_active=True).prefetch_related('pickup_locations', 'zones'):
            # Check if method is available for cart
            cart_available, cart_reason = method.is_available_for_cart(self.cart)
            if not cart_available:
                continue

            # Check if method is available for address (includes Phase 2 zone checking)
            address_available, address_reason = method.is_available_for_address(
                address
            )
            if not address_available:
                continue

            # Calculate shipping with rules (Phase 3 integration)
            calculation = ShippingRuleService.calculate_shipping_for_cart(
                cart=self.cart,
                shipping_method=method,
                address=address,
                user=self.cart.user if hasattr(self.cart, 'user') else None
            )

            method_data = {
                'id': method.id,
                'name': method.name,
                'description': method.description,
                'method_type': method.method_type,
                'base_cost': float(calculation['base_cost'].amount),
                'final_cost': float(calculation['final_cost'].amount),
                'currency': calculation['final_cost'].currency.code,
                'min_delivery_days': method.min_delivery_days,
                'max_delivery_days': method.max_delivery_days,
                'estimated_delivery': method.get_estimated_delivery_date().isoformat() if method.min_delivery_days else None,
                'icon': method.icon,
                'rules_applied': [
                    {
                        'rule_name': rule.get('promotion_name', rule.get('rule_name', '')),
                        'rule_type': rule.get('promotion_type', rule.get('rule_type', '')),
                        'adjustment': float(rule['adjustment'].amount),
                    }
                    for rule in calculation.get('rules_applied', [])
                ],
                'total_discount': float(calculation['total_discount'].amount),
                'total_surcharge': float(calculation['total_surcharge'].amount),
            }

            # Phase 4: Add pickup locations for local_pickup methods
            if method.method_type == 'local_pickup':
                locations = method.pickup_locations.filter(is_active=True)
                method_data['pickup_locations'] = [
                    {
                        'id': str(location.id),
                        'name': location.name,
                        'address': location.address,
                        'city': location.city,
                        'state': location.state,
                        'postal_code': location.postal_code,
                        'country': location.country,
                        'phone': location.phone,
                        'instructions': location.instructions,
                        'business_hours': location.business_hours,
                    }
                    for location in locations
                ]

            methods.append(method_data)

        # Cache the results
        self.available_shipping_methods = methods
        self.save(update_fields=['available_shipping_methods'])

        return methods


class AppliedGiftCard(models.Model):
    """
    Tracks gift cards applied to a cart.
    Similar to AppliedVoucher but for gift card redemptions.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='applied_gift_cards',
        verbose_name=_("Cart")
    )

    gift_card = models.ForeignKey(
        'catalog.GiftCard',
        on_delete=models.PROTECT,
        related_name='cart_applications',
        verbose_name=_("Gift Card")
    )

    discount_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        verbose_name=_("Discount Amount"),
        help_text=_("Amount in base currency (used for cart calculations)")
    )

    # For foreign-currency gift cards: tracks the amount in the gift card's native currency
    original_currency_amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=None,
        null=True,
        blank=True,
        verbose_name=_("Original Currency Amount"),
        help_text=_("Discount in the gift card's native currency (for foreign-currency gift cards)")
    )

    # Exchange rate used when converting between gift card currency and base currency
    gc_exchange_rate = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_("Exchange Rate"),
        help_text=_("Rate: gift card currency -> base currency at time of application")
    )

    applied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Applied At")
    )

    class Meta:
        verbose_name = _("Applied Gift Card")
        verbose_name_plural = _("Applied Gift Cards")
        unique_together = [['cart', 'gift_card']]
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.gift_card.code} - {self.discount_amount} on Cart {self.cart.id}"

    @property
    def redemption_amount(self):
        """Amount to deduct from the gift card at checkout (in gift card's native currency)."""
        return self.original_currency_amount or self.discount_amount

    def clean(self):
        """Validate gift card application"""
        from django.core.exceptions import ValidationError

        if not self.gift_card.is_valid:
            raise ValidationError(_("This gift card cannot be used"))

        # Check amount doesn't exceed balance (compare in gift card's native currency)
        redemption = self.original_currency_amount or self.discount_amount
        if redemption.amount > self.gift_card.current_balance.amount:
            raise ValidationError(_("Discount amount exceeds gift card balance"))
