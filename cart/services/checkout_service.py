"""
Checkout Service - Business logic for checkout process
"""
from django.db import transaction
from django.utils.translation import gettext_lazy as _, get_language
from django.utils import timezone
from datetime import timedelta
from typing import Tuple, Optional, List, Dict, Any
from decimal import Decimal
from ..models import Cart, CheckoutSession, ShippingMethod
from orders.models import Address, Order, OrderItem
from payment_providers.models import PaymentProviderAccount
from payment_providers.services.payment_method_filter import PaymentMethodFilter
from catalog.models import CustomizationOption, CustomizationValue
from catalog.services.stock_reservation import StockReservationService
from core.utils import get_default_currency


class CheckoutService:
    """Service class for checkout operations"""

    SESSION_EXPIRY_HOURS = 2  # Checkout session expires after 2 hours

    @staticmethod
    def get_or_create_session(cart: Cart) -> CheckoutSession:
        """
        Get or create checkout session for cart

        Args:
            cart: Cart instance

        Returns:
            CheckoutSession instance
        """
        session, created = CheckoutSession.objects.get_or_create(
            cart=cart,
            defaults={
                'expires_at': timezone.now() + timedelta(hours=CheckoutService.SESSION_EXPIRY_HOURS)
            }
        )

        # Refresh expiry if session exists
        if not created:
            session.expires_at = timezone.now() + timedelta(hours=CheckoutService.SESSION_EXPIRY_HOURS)
            session.save(update_fields=['expires_at'])

        return session

    @staticmethod
    @transaction.atomic
    def ensure_checkout_user(session: 'CheckoutSession', contact_data: Dict) -> Tuple[bool, str]:
        """
        Ensure cart has a user based on account creation timing

        Args:
            session: CheckoutSession instance
            contact_data: Dict with email, first_name, last_name, optional password

        Returns:
            Tuple of (success: bool, message: str)
        """
        from core.utils import get_site_settings
        from accounts.services.account_creation_service import AccountCreationService

        settings = get_site_settings()
        cart = session.cart

        # Already has full account
        if cart.user and not cart.user.username.startswith('guest_'):
            return True, "Account exists"

        # Handle timing
        if settings.account_creation_timing == 'before_checkout':
            if not contact_data.get('password'):
                return False, _("Account creation required to proceed")
            # Create full account
            success, message, user = AccountCreationService.create_account_during_checkout(
                email=contact_data['email'],
                password=contact_data['password'],
                first_name=contact_data.get('first_name', ''),
                last_name=contact_data.get('last_name', '')
            )
            if success:
                cart.user = user
                cart.save()
            return success, message

        elif settings.account_creation_timing == 'during_checkout':
            if contact_data.get('password'):
                # User chose to create account
                success, message, user = AccountCreationService.create_account_during_checkout(
                    email=contact_data['email'],
                    password=contact_data['password'],
                    first_name=contact_data.get('first_name', ''),
                    last_name=contact_data.get('last_name', '')
                )
            else:
                # Continue as guest
                user = AccountCreationService.create_guest_user(
                    email=contact_data['email'],
                    first_name=contact_data.get('first_name', ''),
                    last_name=contact_data.get('last_name', '')
                )
                success = True
                message = "Guest checkout"

            if success:
                cart.user = user
                cart.save()
            return success, message

        else:  # post_purchase
            # Create guest user
            if not cart.user:
                cart.user = AccountCreationService.create_guest_user(
                    email=contact_data['email'],
                    first_name=contact_data.get('first_name', ''),
                    last_name=contact_data.get('last_name', '')
                )
                cart.save()
            return True, "Guest checkout"

    @staticmethod
    @transaction.atomic
    def set_shipping_address(
        session: CheckoutSession,
        address_id: Optional[int] = None,
        address_data: Optional[Dict] = None,
        email: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Set shipping address for checkout session

        Args:
            session: CheckoutSession instance
            address_id: Existing address ID (optional)
            address_data: New address data dict (optional)
            email: Customer email (optional, for guest checkout persistence)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if address_id:
            # Use saved address (authenticated users only)
            try:
                address = Address.objects.get(id=address_id, user=session.cart.user)
                session.shipping_address = address
                session.shipping_address_data = None  # Clear JSON data when using saved address
            except Address.DoesNotExist:
                return False, _("Address not found")

        elif address_data:
            # Store address data in JSON field (don't create Address record yet)
            # Address will be created when order is placed
            session.shipping_address = None  # Clear FK when using temporary data
            session.shipping_address_data = address_data

        else:
            return False, _("Either address_id or address_data must be provided")

        # Store email in metadata for guest checkout persistence across page refreshes
        if email:
            if not session.metadata:
                session.metadata = {}
            session.metadata['email'] = email

        # Clear previous shipping method selection when address changes
        session.selected_shipping_method = None
        session.shipping_cost = Decimal('0.00')
        session.estimated_delivery_date = None
        session.available_shipping_methods = []

        session.step_completed = 'shipping_address'
        session.save()

        # Recalculate totals
        session.recalculate_totals()

        return True, _("Shipping address set")

    @staticmethod
    @transaction.atomic
    def set_billing_address(
        session: CheckoutSession,
        same_as_shipping: bool = True,
        address_id: Optional[int] = None,
        address_data: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Set billing address for checkout session

        Args:
            session: CheckoutSession instance
            same_as_shipping: Use shipping address for billing
            address_id: Existing address ID (optional)
            address_data: New address data dict (optional)

        Returns:
            Tuple of (success: bool, message: str)
        """
        session.billing_same_as_shipping = same_as_shipping

        if same_as_shipping:
            # Copy both FK and JSON data from shipping
            session.billing_address = session.shipping_address
            session.billing_address_data = session.shipping_address_data
        elif address_id:
            # Use saved address
            try:
                address = Address.objects.get(id=address_id, user=session.cart.user)
                session.billing_address = address
                session.billing_address_data = None  # Clear JSON data when using saved address
            except Address.DoesNotExist:
                return False, _("Address not found")
        elif address_data:
            # Store billing address data in JSON field (don't create Address record yet)
            session.billing_address = None  # Clear FK when using temporary data
            session.billing_address_data = address_data
        else:
            return False, _("Billing address must be provided")

        session.save()
        return True, _("Billing address set")

    @staticmethod
    def get_available_shipping_methods(
        session: CheckoutSession,
        refresh: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get available shipping methods for checkout session

        Args:
            session: CheckoutSession instance
            refresh: Force refresh of cached methods

        Returns:
            List of available shipping methods with rates
        """
        # Check for address - use JSONField data if ForeignKey is not set
        # (during checkout, address is stored in shipping_address_data until order is placed)
        if not session.shipping_address and not session.shipping_address_data:
            return []

        return session.get_available_shipping_methods(refresh=refresh)

    @staticmethod
    @transaction.atomic
    def set_shipping_method(
        session: CheckoutSession,
        shipping_method_id: int
    ) -> Tuple[bool, str]:
        """
        Select shipping method for checkout

        Args:
            session: CheckoutSession instance
            shipping_method_id: ShippingMethod ID

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Get address - use JSONField data if ForeignKey is not set
        address = session.shipping_address or session.shipping_address_data

        if not address:
            return False, _("Shipping address must be set first")

        try:
            shipping_method = ShippingMethod.objects.get(id=shipping_method_id, is_active=True)
        except ShippingMethod.DoesNotExist:
            return False, _("Shipping method not found")

        # Verify method is available for cart
        cart_available, cart_reason = shipping_method.is_available_for_cart(session.cart)
        if not cart_available:
            return False, cart_reason

        # Verify method is available for address
        address_available, address_reason = shipping_method.is_available_for_address(address)
        if not address_available:
            return False, address_reason

        # Calculate shipping cost (with promotions/rules applied)
        from shipping.services.rule_service import ShippingPromotionService
        calculation = ShippingPromotionService.calculate_shipping_for_cart(
            cart=session.cart,
            shipping_method=shipping_method,
            address=address,
            user=session.cart.user if session.cart.user_id else None
        )
        shipping_cost = calculation['final_cost'].amount

        # Set shipping method
        session.selected_shipping_method = shipping_method
        session.shipping_cost = shipping_cost
        session.estimated_delivery_date = shipping_method.get_estimated_delivery_date()
        session.step_completed = 'shipping_method'
        session.save()

        # Recalculate totals with new shipping cost
        session.recalculate_totals()

        return True, _("Shipping method selected")

    @staticmethod
    def get_available_payment_providers(
        session: CheckoutSession
    ) -> List[PaymentProviderAccount]:
        """
        Get payment providers available for checkout session.

        Filters providers based on:
        - Customer's shipping country
        - Cart currency
        - Provider availability and enablement
        - Currency support

        Args:
            session: CheckoutSession instance

        Returns:
            List of available PaymentProviderAccount instances
        """
        # Get address - use JSONField data if ForeignKey is not set
        address = session.shipping_address or session.shipping_address_data

        if not address:
            return []

        # Get country from address (handle both Address object and dict)
        customer_country = address.country if hasattr(address, 'country') else address.get('country')
        if not customer_country:
            return []

        # Get cart currency from Money field
        cart_currency = session.cart.total_amount.currency.code if session.cart.total_amount else get_default_currency()

        # Use PaymentMethodFilter service to get available providers
        return PaymentMethodFilter.get_available_providers_for_checkout(
            customer_country=customer_country,
            currency=cart_currency,
            amount=session.total_amount
        )

    @staticmethod
    @transaction.atomic
    def set_payment_method(
        session: CheckoutSession,
        payment_provider_id: str
    ) -> Tuple[bool, str]:
        """
        Select payment method for checkout

        Args:
            session: CheckoutSession instance
            payment_provider_id: PaymentProviderAccount UUID

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            payment_provider = PaymentProviderAccount.objects.get(
                id=payment_provider_id,
                is_active=True
            )
        except PaymentProviderAccount.DoesNotExist:
            return False, _("Payment provider not found")

        # Verify provider is connected
        if payment_provider.connection_status != 'connected':
            return False, _("Payment provider is not properly configured")

        # Verify provider is available for customer's country and currency
        address = session.shipping_address or session.shipping_address_data
        if address:
            customer_country = address.country if hasattr(address, 'country') else address.get('country')
            cart_currency = session.cart.total_amount.currency.code if session.cart.total_amount else get_default_currency()

            if customer_country:
                available_providers = PaymentMethodFilter.get_available_providers_for_checkout(
                    customer_country=customer_country,
                    currency=cart_currency,
                    amount=session.total_amount
                )

                # Check if selected provider is in the available list
                if payment_provider not in available_providers:
                    return False, _(
                        "Payment provider is not available for your location or currency"
                    )

        session.payment_provider = payment_provider
        session.step_completed = 'payment'
        session.save()

        return True, _("Payment method selected")

    @staticmethod
    def validate_checkout(session: CheckoutSession) -> Tuple[bool, List[str]]:
        """
        Validate checkout session is ready for order creation

        Args:
            session: CheckoutSession instance

        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        errors = []

        # Check cart has items
        if session.cart.total_items == 0:
            errors.append(_("Cart is empty"))

        # Check shipping address (only if cart has physical products)
        if session.cart.requires_shipping:
            address = session.shipping_address or session.shipping_address_data
            if not address:
                errors.append(_("Shipping address is required"))
            if not session.selected_shipping_method:
                errors.append(_("Shipping method is required"))

        # Check billing address (skip for marketplace orders — billing handled externally)
        is_marketplace = session.metadata.get('marketplace', False) if session.metadata else False
        billing_address = session.billing_address or session.billing_address_data
        if not is_marketplace and not billing_address and not session.billing_same_as_shipping:
            errors.append(_("Billing address is required"))

        # Check payment method
        if not session.payment_provider:
            errors.append(_("Payment method is required"))

        # Check session expiry
        if session.expires_at < timezone.now():
            errors.append(_("Checkout session has expired"))

        # Check stock availability using multi-location inventory
        for item in session.cart.items.all():
            product = item.product
            if product.track_inventory:
                from catalog.services import fulfillment_service

                # Get region from shipping address or session
                region = None
                address = session.shipping_address or session.shipping_address_data
                if address:
                    from catalog.models import SalesRegion
                    country_code = address.country if hasattr(address, 'country') else address.get('country')
                    if country_code:
                        regions = SalesRegion.objects.filter(is_active=True).order_by('-priority')
                        for r in regions:
                            if isinstance(r.countries, list) and country_code in r.countries:
                                region = r
                                break

                availability = fulfillment_service.check_stock_availability(
                    product=product,
                    quantity=item.quantity,
                    region=region,
                    variant=item.variant
                )

                if not availability['available']:
                    errors.append(_("Insufficient stock for {product}").format(product=product.name))

        # Dependency re-validation
        from catalog.services.dependency_service import check_hard_dependencies
        for item in session.cart.items.filter(parent_bundle__isnull=True):
            satisfied, blocking = check_hard_dependencies(
                product=item.product, user=session.cart.user, cart=session.cart,
            )
            if not satisfied:
                dep = blocking[0]
                errors.append(dep.customer_message or _(
                    "\"%(product)s\" requires prior ownership of \"%(required)s\"."
                ) % {'product': item.product.name, 'required': dep.required_product.name})

        return len(errors) == 0, errors

    @staticmethod
    def _create_customization_values(order_item: OrderItem):
        """
        Create CustomizationValue records for an order item.

        Args:
            order_item: OrderItem with customizations dict

        The customizations dict has format:
        {option_id: {'value': '...', 'calculated_price': '10.00'}, ...}
        """
        if not order_item.customizations:
            return

        from djmoney.money import Money

        for option_id, customization_data in order_item.customizations.items():
            if not isinstance(customization_data, dict):
                continue

            try:
                # Get customization option
                option = CustomizationOption.objects.get(id=int(option_id))
            except (CustomizationOption.DoesNotExist, ValueError):
                # Skip invalid option IDs
                continue

            # Extract value and price
            value = customization_data.get('value')
            calculated_price_str = customization_data.get('calculated_price', '0')

            # Store value in appropriate field based on option type
            value_fields = {
                'text_value': '',
                'file_value': None,
                'choice_value': '',
                'number_value': None
            }

            if option.option_type in ('text', 'textarea'):
                value_fields['text_value'] = str(value)
            elif option.option_type == 'file':
                # File value should be MediaAsset ID
                from media_library.models import MediaAsset
                try:
                    file_asset = MediaAsset.objects.get(id=int(value))
                    value_fields['file_value'] = file_asset
                except (MediaAsset.DoesNotExist, ValueError, TypeError):
                    value_fields['text_value'] = str(value)  # Fallback
            elif option.option_type in ('select', 'color'):
                value_fields['choice_value'] = str(value)
            elif option.option_type == 'number':
                try:
                    value_fields['number_value'] = Decimal(str(value))
                except (ValueError, TypeError):
                    value_fields['text_value'] = str(value)  # Fallback

            # Create CustomizationValue record
            CustomizationValue.objects.create(
                order_item=order_item,
                customization_option=option,
                calculated_price=Money(Decimal(calculated_price_str), order_item.total_price.currency),
                **value_fields
            )

    @staticmethod
    def _create_design_snapshot(order_item, design_data):
        """
        Create a DesignSnapshot from a DesignDraft for visual design editor orders.
        Queues async rendering for fulfillment images.
        """
        try:
            from customizable_product.models import DesignDraft, DesignSnapshot
            from django.utils import timezone

            token = design_data.get('token')
            if not token:
                return

            draft = DesignDraft.objects.filter(token=token).first()
            if not draft:
                return

            snapshot = DesignSnapshot.objects.create(
                order_item=order_item,
                design_data=draft.design_data,
                rendered_images=draft.thumbnails or {},
                fulfillment_files={},
                is_rendered=False,
            )

            # Queue async rendering task
            try:
                from customizable_product.tasks import render_design_snapshot
                render_design_snapshot.delay(snapshot.pk)
            except Exception:
                pass  # Task queue may not be available

            # Clean up the draft
            draft.delete()

        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(
                f"Failed to create design snapshot for order item {order_item.pk}: {e}"
            )

    @staticmethod
    @transaction.atomic
    def create_order(
        session: CheckoutSession,
        clear_session: bool = True
    ) -> Tuple[bool, str, Optional[Order]]:
        """
        Create order from checkout session

        Args:
            session: CheckoutSession instance
            clear_session: Whether to clear cart items and delete session after order creation.
                          Set to False when using payment orchestration (session cleared after payment).

        Returns:
            Tuple of (success: bool, message: str, order: Order)
        """
        from catalog.services import fulfillment_service, InsufficientStockError
        import logging

        logger = logging.getLogger(__name__)

        # Validate checkout
        is_valid, errors = CheckoutService.validate_checkout(session)
        if not is_valid:
            return False, "; ".join(str(error) for error in errors), None

        cart = session.cart

        # Helper to get address field from either model instance or dict
        def get_address_field(address, field_name, default=""):
            if not address:
                return default
            return getattr(address, field_name, None) if hasattr(address, field_name) else address.get(field_name, default)

        # Get address data (prefer JSONField during checkout)
        shipping_address = session.shipping_address or session.shipping_address_data
        billing_address = session.billing_address or session.billing_address_data

        # Ensure cart has a user (create guest user if needed for guest checkout)
        if not cart.user:
            # Get email from shipping address (name field often contains full name or email)
            # or extract from address data
            email = get_address_field(shipping_address, 'email', '')
            if not email:
                # Fallback: try to get from metadata or generate placeholder
                email = session.metadata.get('email', '') if session.metadata else ''

            # Get name from shipping address
            name = get_address_field(shipping_address, 'name', '')
            first_name = ''
            last_name = ''
            if name:
                name_parts = name.split(' ', 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ''

            if email:
                # Create guest user
                from accounts.services.account_creation_service import AccountCreationService
                cart.user = AccountCreationService.create_guest_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                cart.save()
                logger.info(f"Created guest user {cart.user.username} for order creation")
            else:
                # No email found - this should not happen if validation passed
                return False, _("Customer email is required"), None

        # Create order
        order_kwargs = dict(
            user=cart.user,
            email=cart.user.email,
            phone=get_address_field(shipping_address, 'phone'),
            # Shipping address
            shipping_name=get_address_field(shipping_address, 'name'),
            shipping_address1=get_address_field(shipping_address, 'address1'),
            shipping_address2=get_address_field(shipping_address, 'address2'),
            shipping_city=get_address_field(shipping_address, 'city'),
            shipping_state=get_address_field(shipping_address, 'state'),
            shipping_postal_code=get_address_field(shipping_address, 'postal_code'),
            shipping_country=get_address_field(shipping_address, 'country'),
            # Billing address
            billing_same_as_shipping=session.billing_same_as_shipping,
            billing_name=get_address_field(billing_address, 'name'),
            billing_address1=get_address_field(billing_address, 'address1'),
            billing_address2=get_address_field(billing_address, 'address2'),
            billing_city=get_address_field(billing_address, 'city'),
            billing_state=get_address_field(billing_address, 'state'),
            billing_postal_code=get_address_field(billing_address, 'postal_code'),
            billing_country=get_address_field(billing_address, 'country'),
            # Totals
            subtotal=session.subtotal,
            tax_amount=session.tax_amount,
            shipping_cost=session.shipping_cost,
            discount_amount=session.discount_amount,
            gift_card_discount=cart.gift_card_discount_amount,
            total_amount=session.total_amount,
            # Capture customer's browsing language at checkout
            # Prefer language from session metadata (set by spwig.com frontend)
            # over get_language() which is unreliable for external API calls
            language=(session.metadata.get('language') if session.metadata else None)
                     or get_language() or 'en',
        )
        # Copy metadata from checkout session to order
        if session.metadata:
            order_kwargs['metadata'] = session.metadata
        # Flag test orders in sandbox mode
        from core.license import is_sandbox_mode
        if is_sandbox_mode():
            order_kwargs['is_test_order'] = True

        # Add metadata for guest orders to prompt account creation post-purchase
        if cart.user and cart.user.username.startswith('guest_'):
            if 'metadata' not in order_kwargs:
                order_kwargs['metadata'] = {}
            order_kwargs['metadata']['is_guest_order'] = True
            order_kwargs['metadata']['prompt_account_creation'] = True

        order = Order.objects.create(**order_kwargs)

        # Capture FX data and compute base-currency equivalents
        from core.models import SiteSettings
        settings = SiteSettings.get_settings()
        store_base_currency = settings.default_currency
        order_currency = str(session.total_amount.currency) if hasattr(session.total_amount, 'currency') else store_base_currency

        order.customer_currency = order_currency
        order.base_currency = store_base_currency

        # Display-only mode: force base currency, no FX conversion needed
        if getattr(settings, 'multi_currency_checkout_mode', 'full') == 'display_only':
            order.customer_currency = store_base_currency
            order.fx_policy = 'none'
        elif order_currency != store_base_currency and settings.enable_multi_currency:
            try:
                from exchange_rates.services.exchange_service import ExchangeRateService
                fx_service = ExchangeRateService()
                rate = fx_service.get_rate(store_base_currency, order_currency)
                snapshot = fx_service.snapshot_rate_for_order(
                    from_currency=store_base_currency,
                    to_currency=order_currency,
                    order=order
                )
                order.exchange_rate_used = rate
                order.exchange_rate_provider = snapshot.provider_name
                order.fx_policy = 'spot'
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(
                    f"FX rate capture failed for cross-currency order {order.order_number} "
                    f"({store_base_currency}->{order_currency}): {e}. "
                    f"Base amounts will be NULL until rate is manually set."
                )
                # Do NOT set exchange_rate_used=1 for cross-currency orders -- that would
                # produce silently wrong base amounts. Leave rate as None so base amounts
                # remain NULL, clearly flagging this order for manual review.
                order.fx_policy = 'spot'
        else:
            order.fx_policy = 'none'

        order.compute_base_amounts()
        order.save(update_fields=[
            'customer_currency', 'base_currency', 'exchange_rate_used',
            'exchange_rate_provider', 'fx_policy',
            'subtotal_base', 'tax_amount_base', 'shipping_cost_base',
            'discount_amount_base', 'gift_card_discount_base',
            'total_amount_base', 'amount_paid_base', 'amount_refunded_base',
        ])

        # Prepare cart items for warehouse selection and build index mapping.
        # order_items_data indices correspond to warehouse_allocation keys.
        # cart_item_warehouse_map tracks: cart_item_pk -> warehouse
        order_items_data = []
        cart_item_index_map = {}  # cart_item.pk -> index in order_items_data
        parent_cart_items = list(cart.items.filter(parent_bundle__isnull=True))

        for cart_item in parent_cart_items:
            if cart_item.product.product_type in ('bundle', 'configurable'):
                for component in cart_item.component_items.all():
                    cart_item_index_map[component.pk] = len(order_items_data)
                    order_items_data.append({
                        'product': component.product,
                        'variant': component.variant,
                        'quantity': component.quantity
                    })
            else:
                cart_item_index_map[cart_item.pk] = len(order_items_data)
                order_items_data.append({
                    'product': cart_item.product,
                    'variant': cart_item.variant,
                    'quantity': cart_item.quantity
                })

        # Select optimal warehouse(s) for order fulfillment
        # Returns {index: warehouse} keyed by position in order_items_data
        try:
            warehouse_allocation = fulfillment_service.select_warehouse_for_order(
                order=order,
                order_items=order_items_data
            )
        except InsufficientStockError as e:
            order.delete()
            return False, str(e), None
        except Exception as e:
            logger.error(f"Warehouse selection failed: {e}")
            order.delete()
            return False, _("Unable to allocate warehouse for order. Please contact support."), None

        # Build cart_item.pk -> warehouse mapping for easy lookup
        cart_item_warehouse = {}
        for cart_pk, idx in cart_item_index_map.items():
            cart_item_warehouse[cart_pk] = warehouse_allocation.get(idx)

        # Helper to rollback stock on failure
        def _rollback_allocated_stock():
            for prev_item in order.items.filter(stock_allocated=True):
                try:
                    fulfillment_service.release_stock(prev_item, prev_item.warehouse)
                except Exception as release_error:
                    logger.error(f"Failed to release stock during rollback: {release_error}")

        # Helper to compute base-currency amounts on order items
        def _set_item_base_amounts(item):
            if not order.customer_currency or order.customer_currency == order.base_currency:
                item.unit_price_base = item.unit_price.amount if hasattr(item.unit_price, 'amount') else Decimal(str(item.unit_price or 0))
                item.total_price_base = item.total_price.amount if hasattr(item.total_price, 'amount') else Decimal(str(item.total_price or 0))
            else:
                rate = order.exchange_rate_used or Decimal('1')
                if rate == 0:
                    rate = Decimal('1')
                up = item.unit_price.amount if hasattr(item.unit_price, 'amount') else Decimal(str(item.unit_price or 0))
                tp = item.total_price.amount if hasattr(item.total_price, 'amount') else Decimal(str(item.total_price or 0))
                item.unit_price_base = (up / rate).quantize(Decimal('0.01'))
                item.total_price_base = (tp / rate).quantize(Decimal('0.01'))
            item.save(update_fields=['unit_price_base', 'total_price_base'])

        # Create order items and allocate stock
        for cart_item in parent_cart_items:
            # Create parent order item
            parent_order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                variant=cart_item.variant,
                product_name=cart_item.product.name,
                variant_name=cart_item.variant.name if cart_item.variant else "",
                sku=cart_item.variant.sku if cart_item.variant else cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.total_price,
                customizations=cart_item.customizations,
                warehouse=None,  # Set below for regular products; bundles stay None
                stock_allocated=False,
                stock_fulfilled=False,
                parent_bundle=None
            )
            _set_item_base_amounts(parent_order_item)

            CheckoutService._create_customization_values(parent_order_item)

            # Create design snapshot for visual design editor orders
            if cart_item.customizations and '_design' in cart_item.customizations:
                CheckoutService._create_design_snapshot(parent_order_item, cart_item.customizations['_design'])

            if cart_item.product.product_type in ('bundle', 'configurable'):
                for component_cart_item in cart_item.component_items.all():
                    component_warehouse = cart_item_warehouse.get(component_cart_item.pk)
                    component_order_item = OrderItem.objects.create(
                        order=order,
                        product=component_cart_item.product,
                        variant=component_cart_item.variant,
                        product_name=component_cart_item.product.name,
                        variant_name=component_cart_item.variant.name if component_cart_item.variant else "",
                        sku=component_cart_item.variant.sku if component_cart_item.variant else component_cart_item.product.sku,
                        quantity=component_cart_item.quantity,
                        unit_price=component_cart_item.unit_price,
                        total_price=component_cart_item.total_price,
                        customizations=component_cart_item.customizations,
                        warehouse=component_warehouse,
                        stock_allocated=False,
                        stock_fulfilled=False,
                        parent_bundle=parent_order_item
                    )
                    _set_item_base_amounts(component_order_item)

                    CheckoutService._create_customization_values(component_order_item)

                    # Allocate stock for component — try converting reservation first
                    try:
                        converted = StockReservationService.convert_reservation_to_order_allocation(
                            cart_item=component_cart_item,
                            warehouse=component_order_item.warehouse,
                        )
                        if converted:
                            component_order_item.stock_allocated = True
                            component_order_item.save(update_fields=['stock_allocated'])
                        else:
                            raise Exception("reservation_mismatch")
                    except Exception:
                        try:
                            fulfillment_service.allocate_stock(
                                order_item=component_order_item,
                                warehouse=component_order_item.warehouse
                            )
                            component_order_item.stock_allocated = True
                            component_order_item.save(update_fields=['stock_allocated'])
                        except InsufficientStockError as e:
                            logger.error(f"Stock allocation failed for component {component_order_item.sku}: {e}")
                            _rollback_allocated_stock()
                            order.delete()
                            return False, _("Insufficient stock to complete order"), None
                        except Exception as e:
                            logger.error(f"Stock allocation error for component: {e}")
                            _rollback_allocated_stock()
                            order.delete()
                            return False, _("Error processing order. Please try again."), None

            else:
                # Regular product — look up warehouse by cart_item pk
                parent_order_item.warehouse = cart_item_warehouse.get(cart_item.pk)
                parent_order_item.save(update_fields=['warehouse'])

                try:
                    converted = StockReservationService.convert_reservation_to_order_allocation(
                        cart_item=cart_item,
                        warehouse=parent_order_item.warehouse,
                    )
                    if converted:
                        parent_order_item.stock_allocated = True
                        parent_order_item.save(update_fields=['stock_allocated'])
                    else:
                        raise Exception("reservation_mismatch")
                except Exception:
                    try:
                        fulfillment_service.allocate_stock(
                            order_item=parent_order_item,
                            warehouse=parent_order_item.warehouse
                        )
                        parent_order_item.stock_allocated = True
                        parent_order_item.save(update_fields=['stock_allocated'])
                    except InsufficientStockError as e:
                        logger.error(f"Stock allocation failed for {parent_order_item.sku}: {e}")
                        _rollback_allocated_stock()
                        order.delete()
                        return False, _("Insufficient stock to complete order"), None
                    except Exception as e:
                        logger.error(f"Stock allocation error: {e}")
                        _rollback_allocated_stock()
                        order.delete()
                        return False, _("Error processing order. Please try again."), None

        # Process applied gift cards - redeem them
        CheckoutService._process_gift_card_redemptions(cart, order)

        # Process applied vouchers - increment usage counters and create usage records
        CheckoutService._process_voucher_usage(cart, order)

        # Create bookings for booking items
        CheckoutService._create_bookings(cart, order)

        # Clear cart and session (unless using payment orchestration)
        if clear_session:
            # Create subscriptions for subscription items
            # (orchestration flow defers this to handle_payment_success for payment safety)
            CheckoutService._create_subscriptions(cart, order)
            cart.items.all().delete()
            cart.applied_vouchers.all().delete()
            cart.applied_gift_cards.all().delete()
            session.delete()

        return True, _("Order created successfully"), order

    @staticmethod
    def _create_subscriptions(cart, order):
        """
        Create subscriptions for any subscription items in the cart.

        Args:
            cart: Cart instance
            order: Order instance created from cart

        Returns:
            List of created subscription IDs
        """
        from subscriptions.manager import SubscriptionManager
        import logging

        logger = logging.getLogger(__name__)
        created_subscriptions = []

        # Process each cart item that is a subscription
        for cart_item in cart.items.filter(is_subscription=True):
            if not cart_item.subscription_plan or not cart_item.payment_token:
                logger.error(
                    f"Cart item {cart_item.id} marked as subscription but missing plan or token"
                )
                continue

            # Resolve pricing tier (stored on cart item, or fall back to plan default)
            pricing_tier = cart_item.pricing_tier or cart_item.subscription_plan.get_default_tier()
            if not pricing_tier:
                logger.error(
                    f"Cart item {cart_item.id} subscription plan has no pricing tiers configured"
                )
                continue

            try:
                # Create subscription using SubscriptionManager
                manager = SubscriptionManager(cart_item.payment_token.provider_account)
                subscription = manager.create_subscription(
                    user=cart.user,
                    plan=cart_item.subscription_plan,
                    pricing_tier=pricing_tier,
                    payment_token=cart_item.payment_token,
                    product=cart_item.product,
                    variant=cart_item.variant,
                    originating_order=order
                )

                created_subscriptions.append(subscription.subscription_id)
                logger.info(
                    f"Created subscription {subscription.subscription_id} for order {order.order_number}"
                )

            except Exception as e:
                logger.error(
                    f"Failed to create subscription for cart item {cart_item.id}: {e}"
                )
                # Continue processing other subscriptions even if one fails

        return created_subscriptions

    @staticmethod
    def _create_bookings(cart, order):
        """
        Create Booking records for any booking items in the cart.

        When a cart contains booking products with booking_data,
        converts the cart item into a confirmed Booking record.
        Also cleans up any slot reservations.
        """
        from catalog.services.booking_service import BookingAvailabilityService
        from datetime import datetime
        import logging

        logger = logging.getLogger(__name__)
        created_bookings = []

        for cart_item in cart.items.filter(product__product_type='booking'):
            if not cart_item.booking_data:
                continue

            booking_data = cart_item.booking_data

            # Parse datetime strings
            try:
                start_dt = datetime.fromisoformat(
                    booking_data['start_datetime'].replace('Z', '+00:00')
                )
                end_dt = datetime.fromisoformat(
                    booking_data['end_datetime'].replace('Z', '+00:00')
                )
            except (KeyError, ValueError) as e:
                logger.error(f"Invalid booking data for cart item {cart_item.pk}: {e}")
                continue

            # Find the corresponding order item
            order_item = order.items.filter(product=cart_item.product).first()
            if not order_item:
                logger.error(f"No order item found for booking cart item {cart_item.pk}")
                continue

            try:
                booking_data_full = {
                    'start_datetime': start_dt,
                    'end_datetime': end_dt,
                    'resource_id': booking_data.get('resource_id'),
                    'persons': booking_data.get('persons', {}),
                    'total_cost': cart_item.total_price.amount if cart_item.total_price else 0,
                    'price_breakdown': booking_data.get('price_breakdown', {}),
                    'customer_name': order.shipping_name or '',
                    'customer_email': order.email or '',
                    'customer_phone': order.phone or '',
                    'customer_notes': cart_item.notes or '',
                    'customer_timezone': booking_data.get('timezone', ''),
                }

                success, msg, booking = BookingAvailabilityService.confirm_booking(
                    order_item=order_item,
                    booking_data=booking_data_full,
                )

                if success and booking:
                    created_bookings.append(booking.pk)
                    logger.info(
                        f"Created booking #{booking.pk} for order {order.order_number}"
                    )
                else:
                    logger.warning(
                        f"Booking creation returned: {msg} for cart item {cart_item.pk}"
                    )

            except Exception as e:
                logger.error(f"Failed to create booking for cart item {cart_item.pk}: {e}")

        return created_bookings

    @staticmethod
    def _process_gift_card_redemptions(cart, order):
        """
        Process gift card redemptions for an order.

        Creates redemption transactions for all applied gift cards.

        Args:
            cart: Cart instance with applied gift cards
            order: Order instance created from cart
        """
        from catalog.models import GiftCard, GiftCardTransaction
        import logging

        logger = logging.getLogger(__name__)

        for applied_gift_card in cart.applied_gift_cards.all():
            gift_card = applied_gift_card.gift_card
            # Use the gift card's native currency amount for redemption (for foreign-currency GCs)
            # Falls back to discount_amount for base-currency gift cards
            redemption_amount = applied_gift_card.redemption_amount

            try:
                # Build notes with conversion info for foreign-currency gift cards
                notes = f"Redeemed for order {order.order_number}"
                if applied_gift_card.original_currency_amount and applied_gift_card.gc_exchange_rate:
                    notes += (
                        f" | Base currency equivalent: {applied_gift_card.discount_amount}"
                        f" (rate: {applied_gift_card.gc_exchange_rate})"
                    )

                # Redeem the gift card in its native currency
                gift_card.redeem(
                    amount=redemption_amount,
                    order=order,
                    notes=notes,
                )
                logger.info(
                    f"Redeemed {redemption_amount} from gift card {gift_card.code} "
                    f"for order {order.order_number}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to redeem gift card {gift_card.code} for order {order.order_number}: {e}"
                )
                # Continue processing other gift cards even if one fails

    @staticmethod
    def _process_voucher_usage(cart, order):
        """
        Process applied vouchers for an order.

        Increments voucher usage counters atomically and creates VoucherUsage
        records for audit trail and per-customer limit enforcement.

        Args:
            cart: Cart instance with applied vouchers
            order: Order instance created from cart
        """
        from vouchers.models import VoucherCode, VoucherUsage
        from django.db.models import F
        import logging

        logger = logging.getLogger(__name__)

        for applied_voucher in cart.applied_vouchers.select_related('voucher').all():
            voucher = applied_voucher.voucher

            try:
                # Atomically increment current_uses to prevent race conditions
                VoucherCode.objects.filter(pk=voucher.pk).update(
                    current_uses=F('current_uses') + 1
                )

                # Create usage record for audit trail and per-customer limit checks
                VoucherUsage.objects.create(
                    voucher=voucher,
                    user=cart.user if cart.user and cart.user.is_authenticated else None,
                    order=order,
                    discount_amount=applied_voucher.discount_amount,
                    cart_total=cart.total_amount,
                    session_key=getattr(cart, 'session_key', None),
                )

                logger.info(
                    f"Recorded usage of voucher {voucher.code} for order {order.order_number} "
                    f"(discount: {applied_voucher.discount_amount})"
                )
            except Exception as e:
                logger.error(
                    f"Failed to record voucher usage for {voucher.code} "
                    f"on order {order.order_number}: {e}"
                )
                # Continue processing other vouchers even if one fails

    @staticmethod
    @transaction.atomic
    def process_payment_completion(order) -> Tuple[int, List[str]]:
        """
        Process actions after payment is confirmed for an order.

        This method should be called when payment status becomes 'completed'.
        It handles:
        - Creating gift cards for gift card products in the order
        - Sending gift card delivery emails

        Args:
            order: Order instance with confirmed payment

        Returns:
            Tuple of (gift_cards_created: int, gift_card_codes: List[str])
        """
        from catalog.services.gift_card_service import GiftCardService
        import logging

        logger = logging.getLogger(__name__)

        # Create gift cards for any gift card products in the order
        count, codes = GiftCardService.create_gift_cards_for_order(order)

        if count > 0:
            logger.info(f"Created {count} gift card(s) for order {order.order_number}: {codes}")

        return count, codes

    @staticmethod
    def cleanup_expired_sessions():
        """
        Clean up expired checkout sessions
        Should be run periodically via cron/celery
        """
        expired_sessions = CheckoutSession.objects.filter(
            expires_at__lt=timezone.now()
        )
        count = expired_sessions.count()
        expired_sessions.delete()
        return count
