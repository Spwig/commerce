"""
Cart Service - Business logic for cart operations
"""
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from typing import Tuple, Optional, Dict, Any, List
from ..models import Cart, CartItem
from catalog.models import Product, ProductVariant, CustomizationOption, ConfigurationSlot, ConfigurationSlotOption, CompatibilityRule
from catalog.services.stock_reservation import StockReservationService
from core.utils import get_default_currency


class CartService:
    """Service class for cart operations"""

    @staticmethod
    def _get_user_region(user):
        """Resolve the SalesRegion for a user, if available."""
        if user and hasattr(user, 'sales_region'):
            return user.sales_region
        return None

    @staticmethod
    def _sync_checkout_session(cart: Cart):
        """Recalculate active checkout session totals after cart mutations,
        and bump cart.updated_at so the deterministic '-updated_at, -id'
        ordering in get_or_create_cart stays meaningful."""
        # Bump the parent cart's updated_at — without this it stays at
        # created_at, making any duplicate-row resolution non-deterministic.
        cart.save(update_fields=['updated_at'])
        try:
            from ..models import CheckoutSession
            session = CheckoutSession.objects.filter(
                cart=cart, status='active'
            ).select_related('shipping_address', 'selected_shipping_method').first()
            if session:
                session.recalculate_totals()
        except Exception:
            pass  # Non-critical — checkout will recalculate on next step

    @staticmethod
    def _validate_customizations(
        product: Product,
        customizations: Optional[Dict]
    ) -> Tuple[bool, str, Optional[Dict]]:
        """
        Validate product customizations and calculate prices.

        Args:
            product: Product instance
            customizations: Dict of customization values {option_id: value, ...}

        Returns:
            Tuple of (is_valid: bool, error_message: str, validated_customizations: Dict)
            validated_customizations format: {option_id: {'value': '...', 'calculated_price': '10.00'}}
        """
        # If no customizations provided
        if not customizations:
            # Check if product requires customizations
            if product.allow_customization:
                required_options = product.customization_options.filter(is_required=True)
                if required_options.exists():
                    return False, _("This product requires customization"), None
            return True, "", {}

        # Handle visual design editor customizations
        if '_design' in customizations:
            design_data = customizations['_design']
            design_token = design_data.get('token')
            if not design_token:
                return False, _("Invalid design token"), None

            # Verify the design draft exists and is valid
            try:
                from customizable_product.models import DesignDraft
                from django.utils import timezone
                draft = DesignDraft.objects.get(
                    token=design_token,
                    product=product,
                    expires_at__gt=timezone.now(),
                )
                # Include the design pricing from the draft
                design_price = '0.00'
                if draft.pricing_breakdown:
                    design_price = str(draft.pricing_breakdown.get('total', '0.00'))

                validated = {
                    '_design': {
                        'token': str(design_token),
                        'surfaces_used': design_data.get('surfaces_used', []),
                        'element_counts': design_data.get('element_counts', {}),
                        'calculated_price': design_price,
                    }
                }
                return True, "", validated
            except Exception:
                return False, _("Design not found or expired"), None

        # Check if product allows customization
        if not product.allow_customization:
            return False, _("This product does not support customization"), None

        validated = {}

        # Get all customization options for the product
        options = {
            str(opt.id): opt
            for opt in product.customization_options.all()
        }

        # Validate each provided customization
        for option_id, value in customizations.items():
            option_id_str = str(option_id)

            # Check if option exists and belongs to this product
            if option_id_str not in options:
                return False, _("Invalid customization option"), None

            option = options[option_id_str]

            # Validate the value
            is_valid, error_msg = option.validate_value(value)
            if not is_valid:
                return False, _("Customization '{name}': {error}").format(
                    name=option.name,
                    error=error_msg
                ), None

            # Calculate price for this customization
            base_price = product.price
            customization_price = option.calculate_price(value, base_price)

            # Store validated customization with calculated price
            validated[option_id_str] = {
                'value': value,
                'calculated_price': str(customization_price.amount)
            }

        # Check if all required options are provided
        for option_id_str, option in options.items():
            if option.is_required and option_id_str not in validated:
                return False, _("Required customization '{name}' is missing").format(
                    name=option.name
                ), None

        return True, "", validated

    @staticmethod
    def _check_stock_availability(product: Product, quantity: int, variant: Optional[ProductVariant] = None, user=None, cart_item=None) -> Tuple[bool, str]:
        """
        Check if sufficient stock is available using multi-location inventory.

        Args:
            product: Product instance
            quantity: Quantity requested
            variant: ProductVariant instance (optional)
            user: User instance to determine region (optional)
            cart_item: CartItem instance — if provided, the item's own
                       reservation is added back so it doesn't block itself

        Returns:
            Tuple of (is_available: bool, message: str)
        """
        if not product.track_inventory:
            return True, ""

        from catalog.services import fulfillment_service

        # Get region from user if available
        region = None
        if user and hasattr(user, 'sales_region'):
            region = user.sales_region

        availability = fulfillment_service.check_stock_availability(
            product=product,
            quantity=quantity,
            region=region,
            variant=variant
        )

        if not availability['available']:
            # If this cart item already holds a reservation, that allocation
            # is "ours" and should not block an increase.
            if cart_item:
                from catalog.models import StockReservation
                own_reserved = sum(
                    r.quantity for r in
                    StockReservation.objects.filter(cart_item=cart_item)
                )
                if own_reserved > 0:
                    effective_qty = quantity - own_reserved
                    if effective_qty <= 0:
                        return True, ""
                    re_check = fulfillment_service.check_stock_availability(
                        product=product,
                        quantity=effective_qty,
                        region=region,
                        variant=variant,
                    )
                    if re_check['available']:
                        return True, ""
            return False, _("Insufficient stock")

        return True, ""

    @staticmethod
    @transaction.atomic
    def _add_bundle_to_cart(
        cart: Cart,
        product: Product,
        quantity: int,
        customizations: Optional[Dict],
        notes: str,
        unit_price,
        variant_selections: Optional[Dict[int, int]] = None,
        excluded_optional_items: Optional[List[int]] = None
    ) -> Tuple[bool, str, Optional[CartItem]]:
        """
        Add bundle product to cart by splitting it into components.
        Creates a parent CartItem for the bundle and child CartItems for each component.

        Args:
            cart: Cart instance
            product: Bundle Product instance
            quantity: Quantity of bundles to add
            customizations: Product customizations dict (optional)
            notes: Item notes (optional)
            unit_price: Price of the bundle
            variant_selections: Dict mapping bundle_item_id to variant_id for customer-selected variants
            excluded_optional_items: List of bundle_item_ids to exclude (for optional items customer doesn't want)

        Returns:
            Tuple of (success: bool, message: str, cart_item: CartItem)
        """
        from catalog.models import BundleItem

        # Normalize keys to int (JSON dict keys are always strings)
        variant_selections = {int(k): v for k, v in (variant_selections or {}).items()}
        excluded_optional_items = [int(x) for x in (excluded_optional_items or [])]

        # Get bundle components
        bundle_components = product.bundle_items.order_by('sort_order')

        if not bundle_components.exists():
            return False, _("Bundle has no components configured"), None

        # Validate variant selections for items that require customer selection
        for bundle_item in bundle_components:
            # Skip excluded optional items
            if bundle_item.id in excluded_optional_items:
                if not bundle_item.is_optional:
                    return False, _("Cannot exclude non-optional bundle component: {name}").format(
                        name=bundle_item.component_product.name
                    ), None
                continue

            # Check if variant selection is required
            if bundle_item.allow_variant_selection:
                if bundle_item.component_product.product_type == 'variable':
                    if bundle_item.id not in variant_selections:
                        return False, _("Variant selection required for: {name}").format(
                            name=bundle_item.component_product.name
                        ), None
                    # Validate that the selected variant belongs to the product
                    selected_variant_id = variant_selections[bundle_item.id]
                    if not ProductVariant.objects.filter(
                        id=selected_variant_id,
                        product=bundle_item.component_product
                    ).exists():
                        return False, _("Invalid variant selected for: {name}").format(
                            name=bundle_item.component_product.name
                        ), None

        # Check stock for all non-excluded components
        for bundle_item in bundle_components:
            # Skip excluded optional items
            if bundle_item.id in excluded_optional_items:
                continue

            component_quantity = bundle_item.quantity * quantity

            # Determine the variant to use (customer-selected or pre-configured)
            if bundle_item.allow_variant_selection and bundle_item.id in variant_selections:
                variant = ProductVariant.objects.get(id=variant_selections[bundle_item.id])
            else:
                variant = bundle_item.component_variant

            is_available, error_msg = CartService._check_stock_availability(
                product=bundle_item.component_product,
                quantity=component_quantity,
                variant=variant,
                user=cart.user
            )
            if not is_available:
                return False, _("Insufficient stock for bundle component: {name}").format(
                    name=bundle_item.component_product.name
                ), None

        # Calculate effective bundle price
        bundle_price = product.get_effective_bundle_price()

        # Store variant selections and excluded items in customizations for cart retrieval
        bundle_customizations = customizations.copy() if customizations else {}
        if variant_selections:
            bundle_customizations['_bundle_variant_selections'] = variant_selections
        if excluded_optional_items:
            bundle_customizations['_bundle_excluded_items'] = excluded_optional_items

        # Create parent cart item for the bundle
        parent_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=None,
            parent_bundle=None,  # Ensure it's a parent item
            defaults={
                'quantity': quantity,
                'unit_price': bundle_price,
                'customizations': bundle_customizations,
                'notes': notes
            }
        )

        if not created:
            # Update existing bundle
            parent_item.quantity += quantity
            parent_item.save()

            # Update component quantities
            for component_item in parent_item.component_items.all():
                # Find the corresponding bundle item to get the multiplier
                try:
                    bundle_item = bundle_components.get(
                        component_product=component_item.product,
                        component_variant=component_item.variant
                    )
                    component_item.quantity = parent_item.quantity * bundle_item.quantity
                    component_item.save()
                except BundleItem.DoesNotExist:
                    # Component may have customer-selected variant
                    pass

            message = _("Bundle quantity updated in cart")
        else:
            # Create new component cart items
            for bundle_item in bundle_components:
                # Skip excluded optional items
                if bundle_item.id in excluded_optional_items:
                    continue

                # Determine the variant to use (customer-selected or pre-configured)
                if bundle_item.allow_variant_selection and bundle_item.id in variant_selections:
                    variant = ProductVariant.objects.get(id=variant_selections[bundle_item.id])
                    # Use variant price for customer-selected variants
                    component_price = variant.get_price()
                else:
                    variant = bundle_item.component_variant
                    component_price = bundle_item.get_component_price()

                component_quantity = bundle_item.quantity * quantity

                CartItem.objects.create(
                    cart=cart,
                    product=bundle_item.component_product,
                    variant=variant,
                    quantity=component_quantity,
                    unit_price=component_price,
                    parent_bundle=parent_item,
                    customizations={},
                    notes=""
                )

            message = _("Bundle added to cart")

        # Recalculate voucher and gift card discounts if any
        cart.recalculate_voucher_discounts()
        cart.recalculate_gift_card_discounts()

        return True, message, parent_item

    @staticmethod
    def _validate_configuration(
        product: Product,
        configuration: Dict[int, List[int]],
    ) -> Tuple[bool, str, list]:
        """
        Validate a configurator configuration dict.

        Args:
            product: Configurable product instance
            configuration: {slot_id: [option_id, ...]}

        Returns:
            Tuple of (is_valid, error_message, resolved_options)
            resolved_options: list of (ConfigurationSlotOption, variant_or_none) tuples
        """
        slots = product.configuration_slots.prefetch_related('options').all()
        slot_map = {slot.pk: slot for slot in slots}

        # Normalize configuration keys to integers (JSON sends string keys)
        configuration = {int(k): v for k, v in configuration.items()}

        resolved_options = []

        # Check required slots are filled
        for slot in slots:
            selected_ids = configuration.get(slot.pk, [])
            if slot.is_required and not selected_ids:
                return False, _("Required slot '{name}' has no selection.").format(name=slot.name), []

            if selected_ids:
                # Validate selection count
                if len(selected_ids) < slot.min_selections:
                    return False, _("Slot '{name}' requires at least {min} selection(s).").format(
                        name=slot.name, min=slot.min_selections
                    ), []
                if len(selected_ids) > slot.max_selections:
                    return False, _("Slot '{name}' allows at most {max} selection(s).").format(
                        name=slot.name, max=slot.max_selections
                    ), []

        # Validate each selected option exists and belongs to the right slot
        all_selected_options = []
        for slot_id, option_ids in configuration.items():
            slot_id = int(slot_id)
            if slot_id not in slot_map:
                return False, _("Invalid slot ID: {id}").format(id=slot_id), []

            slot = slot_map[slot_id]
            valid_option_ids = set(slot.options.values_list('id', flat=True))

            for option_id in option_ids:
                option_id = int(option_id)
                if option_id not in valid_option_ids:
                    return False, _("Option {opt_id} is not valid for slot '{slot}'.").format(
                        opt_id=option_id, slot=slot.name
                    ), []

                option = slot.options.get(pk=option_id)
                all_selected_options.append(option)
                resolved_options.append((option, option.option_variant))

        # Validate compatibility rules
        rules = CompatibilityRule.objects.filter(
            configurable_product=product
        ).prefetch_related('compatible_options')

        selected_option_ids = {opt.pk for opt in all_selected_options}

        for rule in rules:
            if rule.source_option_id not in selected_option_ids:
                continue  # Rule not relevant (source not selected)

            # Get what's selected in the target slot
            target_slot_id = rule.target_slot_id
            selected_in_target = set(
                int(oid) for oid in configuration.get(target_slot_id, [])
            )

            if not selected_in_target:
                continue  # Nothing selected in target slot

            compatible_ids = set(rule.compatible_options.values_list('id', flat=True))

            if rule.rule_type == 'requires':
                # All selected options in target must be in the compatible set
                invalid = selected_in_target - compatible_ids
                if invalid:
                    return False, _("Incompatible selection in slot '{slot}'. Some options are not compatible with your other choices.").format(
                        slot=rule.target_slot.name
                    ), []
            elif rule.rule_type == 'excludes':
                # No selected options in target may be in the excluded set
                excluded = selected_in_target & compatible_ids
                if excluded:
                    return False, _("Excluded selection in slot '{slot}'. Some options conflict with your other choices.").format(
                        slot=rule.target_slot.name
                    ), []

        return True, "", resolved_options

    @staticmethod
    def _calculate_configurable_price(
        product: Product,
        resolved_options: list,
    ):
        """
        Calculate the total price for a configurable product.

        Args:
            product: Configurable product instance
            resolved_options: list of (ConfigurationSlotOption, variant_or_none) tuples

        Returns:
            Money amount
        """
        from djmoney.money import Money

        strategy = product.configurator_pricing_strategy

        if strategy == 'fixed':
            return product.price

        elif strategy == 'base_plus_adjustments':
            base = product.configurator_base_price or product.price
            total = base.amount if hasattr(base, 'amount') else Decimal(str(base))
            currency = base.currency if hasattr(base, 'currency') else get_default_currency()
            for option, variant in resolved_options:
                adj = option.price_adjustment
                if adj:
                    total += adj.amount if hasattr(adj, 'amount') else Decimal(str(adj))
            return Money(total, currency)

        else:  # components_sum
            total = Decimal('0.00')
            currency = get_default_currency()
            for option, variant in resolved_options:
                if variant:
                    price = variant.get_price()
                else:
                    price = option.option_product.price
                if price:
                    total += (price.amount if hasattr(price, 'amount') else Decimal(str(price))) * option.quantity
                    currency = price.currency if hasattr(price, 'currency') else currency
            return Money(total, currency)

    @staticmethod
    @transaction.atomic
    def _add_configurable_to_cart(
        cart: Cart,
        product: Product,
        quantity: int,
        configuration: Dict[int, List[int]],
        notes: str,
        channel: str = 'web',
        warehouse=None,
        preset_id: Optional[int] = None,
    ) -> Tuple[bool, str, Optional[CartItem]]:
        """
        Add configurable product to cart with selected component options.
        Creates a parent CartItem for the configurable product and child CartItems
        for each selected component option.

        Args:
            cart: Cart instance
            product: Configurable Product instance
            quantity: Quantity of configured products to add
            configuration: Dict mapping slot_id to list of selected option_ids
            notes: Item notes
            channel: 'web' or 'pos'
            warehouse: Preferred warehouse (optional)
            preset_id: ID of preset used as starting point (optional, for metadata)

        Returns:
            Tuple of (success, message, cart_item)
        """
        # Validate the configuration
        is_valid, error_msg, resolved_options = CartService._validate_configuration(
            product, configuration
        )
        if not is_valid:
            return False, error_msg, None

        # Check stock for all component options
        for option, variant in resolved_options:
            component_qty = option.quantity * quantity
            is_available, stock_error = CartService._check_stock_availability(
                product=option.option_product,
                quantity=component_qty,
                variant=variant,
                user=cart.user
            )
            if not is_available:
                return False, _("Insufficient stock for component: {name}").format(
                    name=option.option_product.name
                ), None

        # Calculate price
        unit_price = CartService._calculate_configurable_price(product, resolved_options)

        # Store configuration metadata in customizations
        config_metadata = {
            '_configuration': {str(k): v for k, v in configuration.items()},
        }
        if preset_id:
            config_metadata['_preset_id'] = preset_id

        # Create parent cart item
        parent_item = CartItem.objects.create(
            cart=cart,
            product=product,
            variant=None,
            quantity=quantity,
            unit_price=unit_price,
            customizations=config_metadata,
            notes=notes,
            parent_bundle=None,
        )

        # Create child cart items for each selected component
        for option, variant in resolved_options:
            component_qty = option.quantity * quantity

            if variant:
                component_price = variant.get_price()
            else:
                component_price = option.option_product.price

            child_item = CartItem.objects.create(
                cart=cart,
                product=option.option_product,
                variant=variant,
                quantity=component_qty,
                unit_price=component_price,
                parent_bundle=parent_item,
                customizations={},
                notes=""
            )

            # Reserve stock for each component
            try:
                StockReservationService.reserve_stock(
                    cart_item=child_item,
                    quantity=component_qty,
                    channel=channel,
                    warehouse=warehouse,
                    region=CartService._get_user_region(cart.user) if not warehouse else None,
                )
            except Exception:
                pass  # Reservation is best-effort

        # Recalculate voucher and gift card discounts
        cart.recalculate_voucher_discounts()
        cart.recalculate_gift_card_discounts()

        return True, _("Configured product added to cart"), parent_item

    @staticmethod
    def get_or_create_cart(user=None, session_key=None) -> Cart:
        """
        Get or create a cart for user or session

        Args:
            user: User instance (optional)
            session_key: Session key for anonymous users (optional)

        Returns:
            Cart instance
        """
        if user and user.is_authenticated:
            # A user may have multiple carts: the regular shopping cart
            # (session_key IS NULL) plus isolated checkout carts created
            # by license_checkout / marketplace_checkout / developer_portal
            # (each holds its own OneToOne CheckoutSession). The "regular"
            # cart is the one with session_key IS NULL; that's what we
            # look up here. Concurrent first-page-loads can still race and
            # create duplicates of the regular cart — guard with
            # select_for_update + atomic, and self-heal if any exist.
            with transaction.atomic():
                carts = list(
                    Cart.objects
                    .select_for_update()
                    .filter(user=user, session_key__isnull=True)
                    .order_by('-updated_at', '-id')
                )
                if not carts:
                    cart = Cart.objects.create(user=user, session_key=None)
                elif len(carts) == 1:
                    cart = carts[0]
                else:
                    cart = CartService._merge_duplicate_carts(carts)
        elif session_key:
            # Use select_for_update + atomic block to serialize concurrent
            # requests for the same session. Without this, two parallel page
            # loads can both miss the existing cart and both create a new one,
            # leaving duplicates that bounce non-deterministically on later
            # reads (see _merge_duplicate_carts).
            with transaction.atomic():
                carts = list(
                    Cart.objects
                    .select_for_update()
                    .filter(session_key=session_key, user=None)
                    .order_by('-updated_at', '-id')
                )
                if not carts:
                    cart = Cart.objects.create(
                        session_key=session_key,
                        user=None,
                    )
                elif len(carts) == 1:
                    cart = carts[0]
                else:
                    # Self-heal pre-existing duplicates (from before the
                    # partial unique constraint was added). Merge into the
                    # row with the most items so we don't lose any.
                    cart = CartService._merge_duplicate_carts(carts)
        else:
            raise ValueError(_("Either user or session_key must be provided"))

        return cart

    @staticmethod
    def _merge_duplicate_carts(carts: List[Cart]) -> Cart:
        """
        Merge a list of duplicate Cart rows into one keeper.

        Keeper = cart with the most items (then highest id). Items from losers
        are reassigned or quantity-merged into the keeper, vouchers/gift-cards
        are preserved when not already present on the keeper, then loser carts
        are deleted. Must be called inside an outer transaction.
        """
        from ..models import AppliedGiftCard
        from vouchers.models import AppliedVoucher

        keeper = max(carts, key=lambda c: (c.items.count(), c.id))
        losers = [c for c in carts if c.id != keeper.id]

        for loser in losers:
            # Move/merge each item from loser into keeper
            for item in list(loser.items.all()):
                if item.parent_bundle_id is not None:
                    # Children follow their parent on cart= reassignment
                    continue
                match = None
                for existing in keeper.items.filter(
                    product=item.product,
                    variant=item.variant,
                    parent_bundle__isnull=True,
                ):
                    if existing.customizations == item.customizations:
                        match = existing
                        break
                if match:
                    match.quantity += item.quantity
                    match.save(update_fields=['quantity', 'updated_at'])
                    item.delete()  # CASCADEs to its bundle children
                else:
                    # Move parent and any children to keeper
                    CartItem.objects.filter(
                        parent_bundle=item
                    ).update(cart=keeper)
                    item.cart = keeper
                    item.save(update_fields=['cart', 'updated_at'])

            # Preserve vouchers / gift cards not already on keeper
            for v in loser.applied_vouchers.all():
                if not keeper.applied_vouchers.filter(voucher=v.voucher).exists():
                    v.cart = keeper
                    v.save(update_fields=['cart'])
            for g in AppliedGiftCard.objects.filter(cart=loser):
                if not AppliedGiftCard.objects.filter(
                    cart=keeper, gift_card=g.gift_card
                ).exists():
                    g.cart = keeper
                    g.save(update_fields=['cart'])

            loser.delete()

        keeper.recalculate_voucher_discounts()
        keeper.recalculate_gift_card_discounts()
        keeper.save(update_fields=['updated_at'])
        return keeper

    @staticmethod
    @transaction.atomic
    def add_item(
        cart: Cart,
        product_id: int,
        quantity: int = 1,
        variant_id: Optional[int] = None,
        customizations: Optional[Dict] = None,
        notes: str = "",
        variant_selections: Optional[Dict[int, int]] = None,
        excluded_optional_items: Optional[List[int]] = None,
        channel: str = 'web',
        warehouse: Optional[Any] = None,
        configuration: Optional[Dict[int, List[int]]] = None,
        preset_id: Optional[int] = None,
        booking_data: Optional[Dict] = None,
        is_subscription: bool = False,
        subscription_plan=None,
        pricing_tier=None,
        payment_token=None,
        customer_currency: Optional[str] = None,
    ) -> Tuple[bool, str, Optional[CartItem]]:
        """
        Add item to cart

        Args:
            cart: Cart instance
            product_id: Product ID
            quantity: Quantity to add
            variant_id: Product variant ID (optional)
            customizations: Product customizations dict (optional)
            notes: Item notes (optional)
            variant_selections: Dict mapping bundle_item_id to variant_id for customer-selected variants (optional)
            excluded_optional_items: List of bundle_item_ids to exclude (for optional items customer doesn't want)
            configuration: Dict mapping slot_id to list of option_ids (for configurable products)
            preset_id: Configuration preset ID used as starting point (optional)
            is_subscription: Whether this is a subscription purchase
            subscription_plan: SubscriptionPlan instance (required if is_subscription)
            pricing_tier: PlanPricingTier instance (required if is_subscription)
            payment_token: PaymentToken instance (required if is_subscription)

        Returns:
            Tuple of (success: bool, message: str, cart_item: CartItem)
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return False, _("Product not found"), None

        # Validate product is not deleted
        if product.is_deleted:
            return False, _("This product is no longer available"), None

        # Check product dependencies
        from catalog.services.dependency_service import check_hard_dependencies
        deps_satisfied, blocking_deps = check_hard_dependencies(
            product=product, user=cart.user, cart=cart,
        )
        if not deps_satisfied:
            if not cart.user or not cart.user.is_authenticated:
                return False, _("You must be logged in to purchase this product."), None
            dep = blocking_deps[0]
            msg = dep.customer_message or _(
                "This product requires you to own \"%(required)s\" first."
            ) % {'required': dep.required_product.name}
            return False, msg, None

        variant = None
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product)
            except ProductVariant.DoesNotExist:
                return False, _("Product variant not found"), None

        # Handle configurable products early — stock is checked per-component
        if product.product_type == 'configurable':
            if not configuration:
                return False, _("Configuration is required for configurable products"), None
            return CartService._add_configurable_to_cart(
                cart=cart,
                product=product,
                quantity=quantity,
                configuration=configuration,
                notes=notes,
                channel=channel,
                warehouse=warehouse,
                preset_id=preset_id,
            )

        # Validate customizations if provided
        is_valid, error_msg, validated_customizations = CartService._validate_customizations(
            product=product,
            customizations=customizations
        )
        if not is_valid:
            return False, error_msg, None

        # Check stock availability using multi-location inventory
        is_available, error_msg = CartService._check_stock_availability(
            product=product,
            quantity=quantity,
            variant=variant,
            user=cart.user
        )
        if not is_available:
            return False, error_msg, None

        # Get unit price — use customer's currency when multi-currency is enabled
        from core.utils import get_default_currency
        cart_currency = cart.effective_currency

        # If cart has no currency yet, set it from the customer's preference
        # or fall back to store default
        if not cart.currency:
            from core.models import SiteSettings
            settings = SiteSettings.get_settings()
            if settings.enable_multi_currency and customer_currency:
                # Display-only mode: cart always operates in base currency
                if getattr(settings, 'multi_currency_checkout_mode', 'full') == 'display_only':
                    cart.currency = settings.default_currency
                    cart_currency = settings.default_currency
                else:
                    cart.currency = customer_currency
                    cart_currency = customer_currency
            else:
                cart.currency = get_default_currency()
                cart_currency = cart.currency
            cart.save(update_fields=['currency'])

        # Get price in the cart's operating currency.
        # Important: use *effective* price (sale price if a sale is active)
        # — `product.price` and the legacy `variant.get_price()` both return
        # the base / pre-sale price, which would charge customers the full
        # amount in the cart even though the storefront shows the sale price.
        if cart_currency != str(product.price.currency):
            # get_price_in_currency already calls get_effective_price internally
            unit_price = product.get_price_in_currency(cart_currency)
        elif variant:
            unit_price = variant.get_effective_price()
        else:
            unit_price = product.get_effective_price()

        # Handle bundle products - split into components
        if product.product_type == 'bundle':
            return CartService._add_bundle_to_cart(
                cart=cart,
                product=product,
                quantity=quantity,
                customizations=validated_customizations,
                notes=notes,
                unit_price=unit_price,
                variant_selections=variant_selections,
                excluded_optional_items=excluded_optional_items
            )

        # Booking products are never merged — each booking is a unique time slot
        if booking_data:
            # Calculate the real booking price (per-night, rules, surcharges)
            # instead of using raw product.price
            booking_unit_price = unit_price
            enriched_booking_data = dict(booking_data)
            try:
                from catalog.services.booking_service import BookingAvailabilityService
                from datetime import datetime as _dt
                _start = _dt.fromisoformat(
                    booking_data['start_datetime'].replace('Z', '+00:00')
                )
                _end = _dt.fromisoformat(
                    booking_data['end_datetime'].replace('Z', '+00:00')
                )
                _resource_id = booking_data.get('resource_id')
                _persons = booking_data.get('persons')
                calc_total, breakdown = (
                    BookingAvailabilityService.calculate_booking_price_with_breakdown(
                        product, _start, _end, _resource_id, _persons
                    )
                )
                from djmoney.money import Money
                import json
                booking_unit_price = Money(calc_total, unit_price.currency)
                # Sanitize breakdown for JSON storage (Decimal → str)
                enriched_booking_data['price_breakdown'] = json.loads(
                    json.dumps(breakdown, default=str)
                )
            except Exception:
                pass  # Fall back to raw product.price if calculation fails

            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                variant=variant,
                quantity=quantity,
                unit_price=booking_unit_price,
                customizations=validated_customizations,
                notes=notes,
                booking_data=enriched_booking_data,
            )
            cart.recalculate_voucher_discounts()
            return True, _("Booking added to cart"), cart_item

        # Check if identical item (same product, variant, AND customizations) already exists in cart
        existing_filter = CartItem.objects.filter(
            cart=cart,
            product=product,
            variant=variant,
            parent_bundle__isnull=True  # Only match standalone items, not bundle components
        )

        # Subscription items should not merge with one-time items (or different plans)
        if is_subscription:
            existing_filter = existing_filter.filter(
                is_subscription=True,
                subscription_plan=subscription_plan,
            )
        else:
            existing_filter = existing_filter.filter(is_subscription=False)

        # Find item with matching customizations
        cart_item = None
        for item in existing_filter:
            if item.customizations == validated_customizations:
                cart_item = item
                break

        if cart_item:
            # Update existing item with matching customizations
            cart_item.quantity += quantity

            # Check stock again for updated quantity using multi-location inventory
            is_available, error_msg = CartService._check_stock_availability(
                product=product,
                quantity=cart_item.quantity,
                variant=variant,
                user=cart.user,
                cart_item=cart_item,
            )
            if not is_available:
                return False, _("Insufficient stock for requested quantity"), None

            cart_item.save()
            message = _("Cart item quantity updated")
        else:
            # Create new cart item
            create_kwargs = dict(
                cart=cart,
                product=product,
                variant=variant,
                quantity=quantity,
                unit_price=unit_price,
                customizations=validated_customizations,
                notes=notes,
            )
            if booking_data:
                create_kwargs['booking_data'] = booking_data
            if is_subscription:
                create_kwargs.update(
                    is_subscription=True,
                    subscription_plan=subscription_plan,
                    pricing_tier=pricing_tier,
                    payment_token=payment_token,
                )
            cart_item = CartItem.objects.create(**create_kwargs)
            message = _("Item added to cart")

        # Reserve stock for this cart item (non-blocking — checkout still validates)
        try:
            StockReservationService.reserve_stock(
                cart_item=cart_item,
                quantity=cart_item.quantity,
                channel=channel,
                warehouse=warehouse,
                region=CartService._get_user_region(cart.user) if not warehouse else None,
            )
        except Exception:
            pass  # Reservation is best-effort; checkout does final validation

        # Recalculate voucher and gift card discounts if any
        cart.recalculate_voucher_discounts()
        cart.recalculate_gift_card_discounts()

        # Sync checkout session totals
        CartService._sync_checkout_session(cart)

        return True, message, cart_item

    @staticmethod
    @transaction.atomic
    def update_item(
        cart_item: CartItem,
        quantity: Optional[int] = None,
        customizations: Optional[Dict] = None,
        notes: Optional[str] = None,
        channel: str = 'web',
    ) -> Tuple[bool, str]:
        """
        Update cart item

        Args:
            cart_item: CartItem instance
            quantity: New quantity (if 0, item will be removed)
            customizations: Updated customizations dict
            notes: Updated notes
            channel: 'web' or 'pos' — used for reservation TTL

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Guard: reject direct updates on child/component items
        if quantity is not None and cart_item.parent_bundle is not None:
            return False, _("Component quantities cannot be changed directly. Update the parent product instead.")

        if quantity is not None:
            if quantity == 0:
                try:
                    StockReservationService.release_reservation(cart_item)
                except Exception:
                    pass
                cart = cart_item.cart
                cart_item.delete()
                cascade_removed = CartService._cascade_dependency_removals(cart)
                if cascade_removed:
                    names = ', '.join(cascade_removed)
                    return True, _("Item removed from cart. Also removed %(names)s (required product no longer in cart).") % {'names': names}
                return True, _("Item removed from cart")

            # Check stock using multi-location inventory
            # Skip parent stock check for configurable/bundle products — their
            # stock is tracked through component products, checked in cascade below
            if cart_item.product.product_type not in ('configurable', 'bundle'):
                is_available, error_msg = CartService._check_stock_availability(
                    product=cart_item.product,
                    quantity=quantity,
                    variant=cart_item.variant,
                    user=cart_item.cart.user,
                    cart_item=cart_item,
                )
                if not is_available:
                    return False, error_msg

            cart_item.quantity = quantity

        if customizations is not None:
            # Validate customizations
            is_valid, error_msg, validated_customizations = CartService._validate_customizations(
                product=cart_item.product,
                customizations=customizations
            )
            if not is_valid:
                return False, error_msg

            cart_item.customizations = validated_customizations

        if notes is not None:
            cart_item.notes = notes

        cart_item.save()

        # Update reservation if quantity changed
        if quantity is not None:
            try:
                StockReservationService.reserve_stock(
                    cart_item=cart_item,
                    quantity=cart_item.quantity,
                    channel=channel,
                    region=CartService._get_user_region(cart_item.cart.user),
                )
            except Exception:
                pass

            # Cascade quantity to child component items (configurable/bundle)
            children = cart_item.component_items.select_related('product', 'variant').all()
            if children.exists():
                config_meta = cart_item.customizations or {}
                configuration = config_meta.get('_configuration', {})

                for child in children:
                    base_qty = CartService._get_component_base_quantity(
                        child, configuration, cart_item.product.product_type
                    )
                    new_child_qty = base_qty * quantity

                    # Check stock for each child component
                    is_available, stock_error = CartService._check_stock_availability(
                        product=child.product,
                        quantity=new_child_qty,
                        variant=child.variant,
                        user=cart_item.cart.user,
                        cart_item=child,
                    )
                    if not is_available:
                        return False, _("Insufficient stock for component: {name}").format(
                            name=child.product.name
                        )

                    child.quantity = new_child_qty
                    child.save(update_fields=['quantity'])

                    # Update reservation for child
                    try:
                        StockReservationService.reserve_stock(
                            cart_item=child,
                            quantity=new_child_qty,
                            channel=channel,
                            region=CartService._get_user_region(cart_item.cart.user),
                        )
                    except Exception:
                        pass

        # Recalculate voucher and gift card discounts
        cart_item.cart.recalculate_voucher_discounts()
        cart_item.cart.recalculate_gift_card_discounts()

        # Sync checkout session totals
        CartService._sync_checkout_session(cart_item.cart)

        return True, _("Cart item updated")

    @staticmethod
    def _get_component_base_quantity(child_item, configuration, product_type):
        """
        Get the per-unit base quantity for a component from its source model.

        For configurable products: looks up ConfigurationSlotOption.quantity
        For bundle products: looks up BundleItem.quantity
        Falls back to 1 if lookup fails.
        """
        if product_type == 'configurable' and configuration:
            try:
                from catalog.models import ConfigurationSlotOption
                for slot_id, option_ids in configuration.items():
                    if not isinstance(option_ids, list):
                        continue
                    for opt_id in option_ids:
                        try:
                            opt = ConfigurationSlotOption.objects.get(pk=opt_id)
                            if (opt.option_product_id == child_item.product_id and
                                    opt.option_variant_id == child_item.variant_id):
                                return opt.quantity
                        except ConfigurationSlotOption.DoesNotExist:
                            continue
            except Exception:
                pass
        elif product_type == 'bundle':
            try:
                from catalog.models import BundleItem
                bundle_item = BundleItem.objects.filter(
                    bundle=child_item.parent_bundle.product,
                    product=child_item.product,
                ).first()
                if bundle_item:
                    return bundle_item.quantity
            except Exception:
                pass
        return 1

    @staticmethod
    @transaction.atomic
    def remove_item(cart_item: CartItem) -> Tuple[bool, str]:
        """
        Remove item from cart

        Args:
            cart_item: CartItem instance

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Guard: reject direct removal of child/component items
        if cart_item.parent_bundle is not None:
            return False, _("Component items cannot be removed directly. Remove the parent product instead.")

        cart = cart_item.cart

        # Release reservations for child components first
        for child in cart_item.component_items.all():
            try:
                StockReservationService.release_reservation(child)
            except Exception:
                pass

        try:
            StockReservationService.release_reservation(cart_item)
        except Exception:
            pass
        cart_item.delete()  # CASCADE deletes children

        # Cascade-remove items whose dependencies are no longer met
        cascade_removed = CartService._cascade_dependency_removals(cart)

        # Recalculate voucher and gift card discounts
        cart.recalculate_voucher_discounts()
        cart.recalculate_gift_card_discounts()

        # Sync checkout session totals
        CartService._sync_checkout_session(cart)

        if cascade_removed:
            names = ', '.join(cascade_removed)
            return True, _("Item removed from cart. Also removed %(names)s (required product no longer in cart).") % {'names': names}
        return True, _("Item removed from cart")

    @staticmethod
    def _cascade_dependency_removals(cart):
        """
        After an item is removed, check remaining items for unmet dependencies.
        Remove any items whose 'requires' dependencies are no longer satisfied
        (not owned by user AND not in the cart). Returns list of removed product names.
        """
        from catalog.services.dependency_service import check_hard_dependencies
        removed_names = []
        changed = True
        while changed:
            changed = False
            for item in cart.items.filter(parent_bundle__isnull=True):
                satisfied, _ = check_hard_dependencies(
                    product=item.product, user=cart.user, cart=cart,
                )
                if not satisfied:
                    removed_names.append(item.product.name)
                    try:
                        StockReservationService.release_reservation(item)
                    except Exception:
                        pass
                    item.delete()
                    changed = True
                    break  # Restart scan after deletion
        return removed_names

    @staticmethod
    @transaction.atomic
    def clear_cart(cart: Cart) -> Tuple[bool, str]:
        """
        Clear all items from cart

        Args:
            cart: Cart instance

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            StockReservationService.release_cart_reservations(cart)
        except Exception:
            pass
        cart.items.all().delete()
        cart.applied_vouchers.all().delete()
        cart.clear_shipping()

        # Sync checkout session totals
        CartService._sync_checkout_session(cart)

        return True, _("Cart cleared")

    @staticmethod
    @transaction.atomic
    def apply_voucher(
        cart: Cart,
        voucher_code: str,
        user=None
    ) -> Tuple[bool, str, Decimal]:
        """
        Apply voucher to cart

        Args:
            cart: Cart instance
            voucher_code: Voucher code to apply
            user: User instance for validation

        Returns:
            Tuple of (success: bool, message: str, discount_amount: Decimal)
        """
        result = cart.apply_voucher(voucher_code, user)
        if result[0]:  # success
            CartService._sync_checkout_session(cart)
        return result

    @staticmethod
    @transaction.atomic
    def remove_voucher(cart: Cart, voucher_code: str) -> Tuple[bool, str]:
        """
        Remove voucher from cart

        Args:
            cart: Cart instance
            voucher_code: Voucher code to remove

        Returns:
            Tuple of (success: bool, message: str)
        """
        removed = cart.remove_voucher(voucher_code)
        if removed:
            CartService._sync_checkout_session(cart)
            return True, _("Voucher removed")
        return False, _("Voucher not found in cart")

    @staticmethod
    @transaction.atomic
    def apply_gift_card(
        cart: Cart,
        gift_card_code: str,
        customer_currency: str = None
    ) -> Tuple[bool, str, Decimal]:
        """
        Apply gift card to cart

        Args:
            cart: Cart instance
            gift_card_code: Gift card code to apply
            customer_currency: Customer's active currency code (from session/middleware)

        Returns:
            Tuple of (success: bool, message: str, discount_amount: Decimal)
        """
        result = cart.apply_gift_card(gift_card_code, customer_currency=customer_currency)
        if result[0]:  # success
            CartService._sync_checkout_session(cart)
        return result

    @staticmethod
    @transaction.atomic
    def remove_gift_card(cart: Cart, gift_card_code: str) -> Tuple[bool, str]:
        """
        Remove gift card from cart

        Args:
            cart: Cart instance
            gift_card_code: Gift card code to remove

        Returns:
            Tuple of (success: bool, message: str)
        """
        removed = cart.remove_gift_card(gift_card_code)
        if removed:
            CartService._sync_checkout_session(cart)
            return True, _("Gift card removed")
        return False, _("Gift card not found in cart")

    @staticmethod
    @transaction.atomic
    def merge_carts(source_cart: Cart, target_cart: Cart) -> Tuple[bool, str]:
        """
        Merge source cart into target cart (used when anonymous user logs in)

        Args:
            source_cart: Cart to merge from (will be deleted)
            target_cart: Cart to merge into

        Returns:
            Tuple of (success: bool, message: str)
        """
        items_merged = 0
        items_skipped = 0

        for item in source_cart.items.all():
            # Skip bundle component items - they'll be handled when parent is merged
            if item.parent_bundle is not None:
                continue

            # Check if identical item (same product, variant, AND customizations) exists in target cart
            existing_items = target_cart.items.filter(
                product=item.product,
                variant=item.variant,
                parent_bundle__isnull=True  # Only match standalone items
            )

            # Find item with matching customizations
            matching_item = None
            for existing_item in existing_items:
                if existing_item.customizations == item.customizations:
                    matching_item = existing_item
                    break

            if matching_item:
                # Merge quantities for matching item
                matching_item.quantity += item.quantity
                matching_item.save()
                items_merged += 1
            else:
                # Move item to target cart (no matching customizations found)
                item.cart = target_cart
                item.save()
                items_merged += 1

        # Copy vouchers
        for voucher in source_cart.applied_vouchers.all():
            if not target_cart.applied_vouchers.filter(voucher=voucher.voucher).exists():
                voucher.cart = target_cart
                voucher.save()

        # Delete source cart
        source_cart.delete()

        # Recalculate target cart
        target_cart.recalculate_voucher_discounts()
        target_cart.recalculate_gift_card_discounts()
        target_cart.save(update_fields=['updated_at'])

        message = _("{count} items merged into cart").format(count=items_merged)
        return True, message

    @staticmethod
    def get_cart_summary(cart: Cart) -> Dict[str, Any]:
        """
        Get comprehensive cart summary

        Args:
            cart: Cart instance

        Returns:
            Dict with cart summary data
        """
        # Helper to safely extract amount from Money objects
        def to_float(value):
            if hasattr(value, 'amount'):
                return float(value.amount)
            return float(value) if value else 0

        # Count only parent/top-level items (exclude bundle/configurable children)
        parent_item_count = sum(
            item.quantity for item in cart.items.filter(parent_bundle__isnull=True)
        )

        return {
            'total_items': parent_item_count,
            'item_count': parent_item_count,  # Alias for mini-cart compatibility
            'subtotal': to_float(cart.subtotal),
            'total_savings': to_float(cart.total_savings),
            'voucher_discount': to_float(cart.voucher_discount_amount),
            'shipping_cost': to_float(cart.shipping_cost),
            'tax_amount': to_float(cart.tax_amount),
            'grand_total': to_float(cart.grand_total),
            'requires_shipping': cart.requires_shipping,
            'total_weight': float(cart.total_weight),
            'applied_vouchers': cart.get_voucher_summary()
        }
