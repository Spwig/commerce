"""
Checkout Service - Business logic for checkout process
"""

from datetime import timedelta
from decimal import Decimal
from typing import Any

from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from catalog.models import CustomizationOption, CustomizationValue
from catalog.services.stock_reservation import StockReservationService
from core.utils import get_default_currency
from orders.models import Address, Order, OrderItem
from payment_providers.models import PaymentProviderAccount
from payment_providers.services.payment_method_filter import PaymentMethodFilter

from ..models import Cart, CheckoutSession, ShippingMethod


class VoucherNoLongerValid(Exception):
    """
    A voucher passed validation when applied to the cart but not at checkout.

    Raised from inside ``create_order``'s transaction so the whole order rolls
    back — no order, no charge, and the customer returns to the cart to see why.
    Deliberately NOT swallowed: the previous code caught every exception here
    and continued, which would make any cap enforcement inert and leave a
    single-use code unboundedly spendable.
    """


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
                "expires_at": timezone.now() + timedelta(hours=CheckoutService.SESSION_EXPIRY_HOURS)
            },
        )

        # Refresh expiry if session exists
        if not created:
            session.expires_at = timezone.now() + timedelta(
                hours=CheckoutService.SESSION_EXPIRY_HOURS
            )
            session.save(update_fields=["expires_at"])

        return session

    @staticmethod
    @transaction.atomic
    def ensure_checkout_user(session: "CheckoutSession", contact_data: dict) -> tuple[bool, str]:
        """
        Ensure cart has a user based on account creation timing

        Args:
            session: CheckoutSession instance
            contact_data: Dict with email, first_name, last_name, optional password

        Returns:
            Tuple of (success: bool, message: str)
        """
        from accounts.services.account_creation_service import AccountCreationService
        from core.utils import get_site_settings

        settings = get_site_settings()
        cart = session.cart

        # Already has full account
        if cart.user and not cart.user.username.startswith("guest_"):
            return True, "Account exists"

        # Handle timing
        if settings.account_creation_timing == "before_checkout":
            if not contact_data.get("password"):
                return False, _("Account creation required to proceed")
            # Create full account
            success, message, user = AccountCreationService.create_account_during_checkout(
                email=contact_data["email"],
                password=contact_data["password"],
                first_name=contact_data.get("first_name", ""),
                last_name=contact_data.get("last_name", ""),
            )
            if success:
                cart.user = user
                cart.save()
            return success, message

        elif settings.account_creation_timing == "during_checkout":
            if contact_data.get("password"):
                # User chose to create account
                success, message, user = AccountCreationService.create_account_during_checkout(
                    email=contact_data["email"],
                    password=contact_data["password"],
                    first_name=contact_data.get("first_name", ""),
                    last_name=contact_data.get("last_name", ""),
                )
            else:
                # Continue as guest
                user = AccountCreationService.create_guest_user(
                    email=contact_data["email"],
                    first_name=contact_data.get("first_name", ""),
                    last_name=contact_data.get("last_name", ""),
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
                    email=contact_data["email"],
                    first_name=contact_data.get("first_name", ""),
                    last_name=contact_data.get("last_name", ""),
                )
                cart.save()
            return True, "Guest checkout"

    @staticmethod
    def grant_guest_order_access(request, order) -> None:
        """Allow this browser session to view ``order``'s confirmation page.

        Guest checkout creates a guest ``User`` server-side but never
        authenticates the browser, and the confirmation view 404s anonymous
        visitors. Without an allow-list a guest who just paid can't see their
        own confirmation. We record the order number in the session (capped, so
        it can't grow unbounded) rather than exposing every order by number.
        """
        if request is None or order is None:
            return
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            return
        numbers = request.session.get("guest_order_numbers", [])
        if order.order_number not in numbers:
            numbers.append(order.order_number)
            request.session["guest_order_numbers"] = numbers[-20:]
            request.session.modified = True

    @staticmethod
    @transaction.atomic
    def set_shipping_address(
        session: CheckoutSession,
        address_id: int | None = None,
        address_data: dict | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> tuple[bool, str]:
        """
        Set shipping address for checkout session

        Args:
            session: CheckoutSession instance
            address_id: Existing address ID (optional)
            address_data: New address data dict (optional)
            email: Customer email (optional, for guest checkout persistence)
            phone: Supplemental phone for a saved address that has none
                (carriers need a delivery contact number)

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Remember the destination we had before this call so we can tell a
        # real address change (rates differ → the method must be re-chosen)
        # apart from a no-op re-submit of the same saved address — e.g. a
        # returning customer only attaching a supplemental phone, which never
        # affects shipping rates. Blindly clearing the method in that case
        # bounces express-checkout customers back to re-pick shipping before
        # the payment form can mount.
        previous_address_id = session.shipping_address_id

        if address_id:
            # Use saved address (authenticated users only)
            try:
                address = Address.objects.get(id=address_id, user=session.cart.user)
            except Address.DoesNotExist:
                return False, _("Address not found")

            # Shipping needs a delivery contact number. Older saved
            # addresses may predate the phone requirement — accept a
            # supplemental phone and complete the saved record with it.
            if not address.phone:
                phone = (phone or "").strip()
                if not phone:
                    return False, _(
                        "This saved address has no phone number. Please add one so the "
                        "carrier can contact you about delivery."
                    )
                address.phone = phone[:20]
                address.save(update_fields=["phone", "updated_at"])

            session.shipping_address = address
            session.shipping_address_data = None  # Clear JSON data when using saved address

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
            session.metadata["email"] = email

        # Clear the previous shipping method selection only when the
        # destination actually changed. Re-submitting the same saved address
        # (to complete it with a phone number) leaves rates untouched, so the
        # method — and the customer's place in the flow — is preserved.
        destination_unchanged = bool(address_id) and address_id == previous_address_id
        if not destination_unchanged:
            session.selected_shipping_method = None
            session.shipping_cost = Decimal("0.00")
            session.estimated_delivery_date = None
            session.available_shipping_methods = []

        session.step_completed = "shipping_address"
        session.save()

        # Recalculate totals
        session.recalculate_totals()

        return True, _("Shipping address set")

    @staticmethod
    @transaction.atomic
    def set_billing_address(
        session: CheckoutSession,
        same_as_shipping: bool = True,
        address_id: int | None = None,
        address_data: dict | None = None,
        contact_name: str | None = None,
        email: str | None = None,
    ) -> tuple[bool, str]:
        """
        Set billing address for checkout session

        Args:
            session: CheckoutSession instance
            same_as_shipping: Use shipping address for billing
            address_id: Existing address ID (optional)
            address_data: New address data dict (optional)
            contact_name: Customer's full name when no address carries one
                (digital-only carts skip the shipping form, so guest
                checkouts would otherwise reach payment nameless)

        Returns:
            Tuple of (success: bool, message: str)
        """
        session.billing_same_as_shipping = same_as_shipping

        # Persist the contact name so order creation (billing_name, guest
        # user) and payment providers get a customer name even when no
        # billing/shipping address is collected (digital-only carts).
        if contact_name and contact_name.strip():
            if not session.metadata:
                session.metadata = {}
            session.metadata["contact_name"] = contact_name.strip()[:200]

        # Persist the email too — digital-only carts skip the shipping step
        # that would otherwise record it, so guest order creation (which reads
        # metadata['email']) would have nothing without this.
        if email and email.strip():
            if not session.metadata:
                session.metadata = {}
            session.metadata["email"] = email.strip()[:254]

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
        session: CheckoutSession, refresh: bool = False
    ) -> list[dict[str, Any]]:
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
    def set_shipping_method(session: CheckoutSession, shipping_method_id: int) -> tuple[bool, str]:
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
            user=session.cart.user if session.cart.user_id else None,
        )
        shipping_cost = calculation["final_cost"].amount

        # Set shipping method
        session.selected_shipping_method = shipping_method
        session.shipping_cost = shipping_cost
        session.estimated_delivery_date = shipping_method.get_estimated_delivery_date()
        session.step_completed = "shipping_method"
        session.save()

        # Recalculate totals with new shipping cost
        session.recalculate_totals()

        return True, _("Shipping method selected")

    @staticmethod
    def get_customer_country(session: CheckoutSession, fallback_country: str = "") -> str:
        """
        Resolve the customer's country for payment provider filtering.

        Order: shipping address → billing address → fallback (typically the
        GeoIP country supplied by the calling view). Carts with no shippable
        items never collect a shipping address, so billing (a minimal
        country/postal collected at the payment step) or GeoIP is all there
        is until the customer types something.

        Args:
            session: CheckoutSession instance
            fallback_country: Country to use when no address carries one

        Returns:
            Country string ("" when nothing is known). May be an ISO code or
            a full name — PaymentMethodFilter normalizes either.
        """
        for address in (
            session.shipping_address or session.shipping_address_data,
            session.billing_address or session.billing_address_data,
        ):
            if not address:
                continue
            country = address.country if hasattr(address, "country") else address.get("country")
            if country:
                return str(country)
        return fallback_country or ""

    @staticmethod
    def get_available_payment_providers(
        session: CheckoutSession, fallback_country: str = ""
    ) -> list[PaymentProviderAccount]:
        """
        Get payment providers available for checkout session.

        Filters providers based on:
        - Customer's country (shipping address; billing/GeoIP for carts
          with no shippable items)
        - Cart currency
        - Provider availability and enablement
        - Currency support

        Args:
            session: CheckoutSession instance
            fallback_country: GeoIP country from the calling view — used only
                for no-shipping carts that have no address on file yet

        Returns:
            List of available PaymentProviderAccount instances
        """
        cart_requires_shipping = session.cart.requires_shipping

        if cart_requires_shipping:
            # Shipping carts: the shipping address drives everything —
            # without one there is nothing meaningful to offer yet.
            address = session.shipping_address or session.shipping_address_data
            if not address:
                return []
            customer_country = (
                address.country if hasattr(address, "country") else address.get("country")
            )
        else:
            # No-shipping carts (digital / booking only): billing country if
            # collected, else the caller's GeoIP fallback.
            customer_country = CheckoutService.get_customer_country(session, fallback_country)

        if not customer_country:
            return []

        # Get cart currency from Money field
        cart_currency = (
            session.cart.total_amount.currency.code
            if session.cart.total_amount
            else get_default_currency()
        )

        # Use PaymentMethodFilter service to get available providers.
        # The merchant's ships-to gate only applies to carts that ship.
        return PaymentMethodFilter.get_available_providers_for_checkout(
            customer_country=customer_country,
            currency=cart_currency,
            amount=session.total_amount,
            require_ships_to=cart_requires_shipping,
        )

    @staticmethod
    @transaction.atomic
    def set_payment_method(session: CheckoutSession, payment_provider_id: str) -> tuple[bool, str]:
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
                id=payment_provider_id, is_active=True
            )
        except PaymentProviderAccount.DoesNotExist:
            return False, _("Payment provider not found")

        # Verify provider is connected
        if payment_provider.connection_status != "connected":
            return False, _("Payment provider is not properly configured")

        # Verify provider is available for customer's country and currency.
        # Same country source as get_available_payment_providers: shipping
        # address, else billing (no-shipping carts collect only that). When
        # no country is known yet — a no-shipping cart selects its provider
        # BEFORE the billing step submits a country — the check is skipped,
        # matching the pre-existing behaviour for address-less sessions.
        # This is a merchant-config/UX filter, not an authorization
        # boundary: currency and method acceptance are enforced by the
        # gateway when the intent is created.
        customer_country = CheckoutService.get_customer_country(session)
        if customer_country:
            cart_currency = (
                session.cart.total_amount.currency.code
                if session.cart.total_amount
                else get_default_currency()
            )

            available_providers = PaymentMethodFilter.get_available_providers_for_checkout(
                customer_country=customer_country,
                currency=cart_currency,
                amount=session.total_amount,
                require_ships_to=session.cart.requires_shipping,
            )

            # Check if selected provider is in the available list
            if payment_provider not in available_providers:
                return False, _("Payment provider is not available for your location or currency")

        session.payment_provider = payment_provider
        session.step_completed = "payment"
        session.save()

        return True, _("Payment method selected")

    @staticmethod
    def validate_checkout(session: CheckoutSession) -> tuple[bool, list[str]]:
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
        is_marketplace = session.metadata.get("marketplace", False) if session.metadata else False
        billing_address = session.billing_address or session.billing_address_data

        def _addr_field(addr, field):
            if not addr:
                return ""
            return (getattr(addr, field, "") if hasattr(addr, field) else addr.get(field, "")) or ""

        if not is_marketplace:
            if not session.cart.requires_shipping:
                # Nothing ships, so "billing same as shipping" is meaningless
                # (there is no shipping address to mirror). Require a real,
                # complete billing address — this is the server-side backstop
                # for the full billing form the UI now collects, so a headless
                # or stale client can't create an order with blank billing.
                required = ["name", "address1", "city", "postal_code", "country"]
                if not billing_address or any(
                    not str(_addr_field(billing_address, f)).strip() for f in required
                ):
                    errors.append(_("A complete billing address is required"))
            elif not billing_address and not session.billing_same_as_shipping:
                errors.append(_("Billing address is required"))

        # Check payment method — unless tenders already cover the whole order.
        # amount_due can legitimately be zero (gift cards / wallet credit), and
        # demanding a provider then would force the customer to mount a gateway
        # widget for 0.00 that create_payment_intent has no zero guard against.
        if not session.payment_provider and session.amount_due.amount > 0:
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

                    country_code = (
                        address.country if hasattr(address, "country") else address.get("country")
                    )
                    if country_code:
                        regions = SalesRegion.objects.filter(is_active=True).order_by("-priority")
                        for r in regions:
                            if isinstance(r.countries, list) and country_code in r.countries:
                                region = r
                                break

                availability = fulfillment_service.check_stock_availability(
                    product=product, quantity=item.quantity, region=region, variant=item.variant
                )

                # Pre-order/backorder products are sold without on-hand stock;
                # they are accepted here and recorded as unallocated at
                # allocation time below.
                if not availability["available"] and not product.can_sell_without_stock():
                    errors.append(
                        _("Insufficient stock for {product}").format(product=product.name)
                    )

        # Dependency re-validation
        from catalog.services.dependency_service import check_hard_dependencies

        for item in session.cart.items.filter(parent_bundle__isnull=True):
            satisfied, blocking = check_hard_dependencies(
                product=item.product,
                user=session.cart.user,
                cart=session.cart,
            )
            if not satisfied:
                dep = blocking[0]
                errors.append(
                    dep.customer_message
                    or _('"%(product)s" requires prior ownership of "%(required)s".')
                    % {"product": item.product.name, "required": dep.required_product.name}
                )

        # Subscription lines MUST carry a reusable payment token before the order
        # is created — the token is captured at the checkout payment step and
        # attached via /api/cart/items/<id>/attach-subscription-token/. Failing
        # here (which runs inside create_order, before any payment intent is
        # raised) guarantees a customer is never charged for a subscription that
        # would then fail to create for lack of a token.
        if session.cart.items.filter(is_subscription=True, payment_token__isnull=True).exists():
            errors.append(_("A payment method is required to complete a subscription."))

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
            value = customization_data.get("value")
            calculated_price_str = customization_data.get("calculated_price", "0")

            # Store value in appropriate field based on option type
            value_fields = {
                "text_value": "",
                "file_value": None,
                "choice_value": "",
                "number_value": None,
            }

            if option.option_type in ("text", "textarea"):
                value_fields["text_value"] = str(value)
            elif option.option_type == "file":
                # File value should be MediaAsset ID
                from media_library.models import MediaAsset

                try:
                    file_asset = MediaAsset.objects.get(id=int(value))
                    value_fields["file_value"] = file_asset
                except (MediaAsset.DoesNotExist, ValueError, TypeError):
                    value_fields["text_value"] = str(value)  # Fallback
            elif option.option_type in ("select", "color"):
                value_fields["choice_value"] = str(value)
            elif option.option_type == "number":
                try:
                    value_fields["number_value"] = Decimal(str(value))
                except (ValueError, TypeError):
                    value_fields["text_value"] = str(value)  # Fallback

            # Create CustomizationValue record
            CustomizationValue.objects.create(
                order_item=order_item,
                customization_option=option,
                calculated_price=Money(
                    Decimal(calculated_price_str), order_item.total_price.currency
                ),
                **value_fields,
            )

    @staticmethod
    def _create_design_snapshot(order_item, design_data):
        """
        Create a DesignSnapshot from a DesignDraft for visual design editor orders.
        Queues async rendering for fulfillment images.
        """
        try:
            from customizable_product.models import DesignDraft, DesignSnapshot

            token = design_data.get("token")
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
        session: CheckoutSession, clear_session: bool = True, channel: str = "web"
    ) -> tuple[bool, str, Order | None]:
        """
        Create order from checkout session

        Args:
            session: CheckoutSession instance
            clear_session: Whether to clear cart items and delete session after order creation.
                          Set to False when using payment orchestration (session cleared after payment).
            channel: Sales channel to stamp on the Order ("web", "pos", "agent"). An
                     unrecognised value falls back to "web" so a caller can never write
                     an invalid channel.

        Returns:
            Tuple of (success: bool, message: str, order: Order)
        """
        import logging

        from catalog.services import InsufficientStockError, fulfillment_service

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
            return (
                getattr(address, field_name, None)
                if hasattr(address, field_name)
                else address.get(field_name, default)
            )

        # Get address data (prefer JSONField during checkout)
        shipping_address = session.shipping_address or session.shipping_address_data
        billing_address = session.billing_address or session.billing_address_data

        # Ensure cart has a user (create guest user if needed for guest checkout)
        if not cart.user:
            # Get email from shipping address (name field often contains full name or email)
            # or extract from address data
            email = get_address_field(shipping_address, "email", "")
            if not email:
                # Fallback: try to get from metadata or generate placeholder
                email = session.metadata.get("email", "") if session.metadata else ""

            # Get name from shipping address, else billing, else the
            # contact name captured for digital-only carts
            name = (
                get_address_field(shipping_address, "name", "")
                or get_address_field(billing_address, "name", "")
                or (session.metadata.get("contact_name", "") if session.metadata else "")
            )
            first_name = ""
            last_name = ""
            if name:
                name_parts = name.split(" ", 1)
                first_name = name_parts[0]
                last_name = name_parts[1] if len(name_parts) > 1 else ""

            if email:
                # Create guest user
                from accounts.services.account_creation_service import AccountCreationService

                cart.user = AccountCreationService.create_guest_user(
                    email=email, first_name=first_name, last_name=last_name
                )
                cart.save()
                logger.info(f"Created guest user {cart.user.username} for order creation")
            else:
                # No email found - this should not happen if validation passed
                return False, _("Customer email is required"), None

        # Contact name captured at the billing/contact step for carts with
        # no shipping form (digital-only) — billing_name must not be empty
        # on the order, payment providers reject nameless customers.
        contact_name = session.metadata.get("contact_name", "") if session.metadata else ""

        # Create order
        order_kwargs = {
            "user": cart.user,
            "email": cart.user.email,
            "phone": get_address_field(shipping_address, "phone")
            or get_address_field(billing_address, "phone"),
            # Shipping address
            "shipping_name": get_address_field(shipping_address, "name"),
            "shipping_address1": get_address_field(shipping_address, "address1"),
            "shipping_address2": get_address_field(shipping_address, "address2"),
            "shipping_city": get_address_field(shipping_address, "city"),
            "shipping_state": get_address_field(shipping_address, "state"),
            "shipping_postal_code": get_address_field(shipping_address, "postal_code"),
            "shipping_country": get_address_field(shipping_address, "country"),
            "shipping_phone": get_address_field(shipping_address, "phone"),
            # Billing address
            "billing_same_as_shipping": session.billing_same_as_shipping,
            "billing_name": get_address_field(billing_address, "name") or contact_name,
            "billing_address1": get_address_field(billing_address, "address1"),
            "billing_address2": get_address_field(billing_address, "address2"),
            "billing_city": get_address_field(billing_address, "city"),
            "billing_state": get_address_field(billing_address, "state"),
            "billing_postal_code": get_address_field(billing_address, "postal_code"),
            "billing_country": get_address_field(billing_address, "country"),
            "billing_phone": get_address_field(billing_address, "phone"),
            # Totals
            "subtotal": session.subtotal,
            "tax_amount": session.tax_amount,
            "shipping_cost": session.shipping_cost,
            "discount_amount": session.discount_amount,
            "total_amount": session.total_amount,
            # Capture customer's browsing language at checkout
            # Prefer language from session metadata (set by spwig.com frontend)
            # over get_language() which is unreliable for external API calls
            "language": (session.metadata.get("language") if session.metadata else None)
            or get_language()
            or "en",
            # Sales channel (validated against the model choices; unknown -> web).
            "channel": (channel if channel in dict(Order.CHANNEL_CHOICES) else "web"),
        }
        # Copy metadata from checkout session to order
        if session.metadata:
            order_kwargs["metadata"] = session.metadata
        # Flag test orders in sandbox mode
        from core.license import is_sandbox_mode

        if is_sandbox_mode():
            order_kwargs["is_test_order"] = True

        # Add metadata for guest orders to prompt account creation post-purchase
        if cart.user and cart.user.username.startswith("guest_"):
            if "metadata" not in order_kwargs:
                order_kwargs["metadata"] = {}
            order_kwargs["metadata"]["is_guest_order"] = True
            order_kwargs["metadata"]["prompt_account_creation"] = True

        order = Order.objects.create(**order_kwargs)

        # Capture FX data and compute base-currency equivalents
        from core.models import SiteSettings

        settings = SiteSettings.get_settings()
        store_base_currency = settings.default_currency
        order_currency = (
            str(session.total_amount.currency)
            if hasattr(session.total_amount, "currency")
            else store_base_currency
        )

        order.customer_currency = order_currency
        order.base_currency = store_base_currency

        # Display-only mode: force base currency, no FX conversion needed
        if getattr(settings, "multi_currency_checkout_mode", "full") == "display_only":
            order.customer_currency = store_base_currency
            order.fx_policy = "none"
        elif order_currency != store_base_currency and settings.enable_multi_currency:
            try:
                from exchange_rates.services.exchange_service import ExchangeRateService

                fx_service = ExchangeRateService()
                rate = fx_service.get_rate(store_base_currency, order_currency)
                snapshot = fx_service.snapshot_rate_for_order(
                    from_currency=store_base_currency, to_currency=order_currency, order=order
                )
                order.exchange_rate_used = rate
                order.exchange_rate_provider = snapshot.provider_name
                order.fx_policy = "spot"
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
                order.fx_policy = "spot"
        else:
            order.fx_policy = "none"

        order.compute_base_amounts()
        order.save(
            update_fields=[
                "customer_currency",
                "base_currency",
                "exchange_rate_used",
                "exchange_rate_provider",
                "fx_policy",
                "subtotal_base",
                "tax_amount_base",
                "shipping_cost_base",
                "discount_amount_base",
                "gift_card_discount_base",
                "total_amount_base",
                "amount_paid_base",
                "amount_refunded_base",
            ]
        )

        # Prepare cart items for warehouse selection and build index mapping.
        # order_items_data indices correspond to warehouse_allocation keys.
        # cart_item_warehouse_map tracks: cart_item_pk -> warehouse
        order_items_data = []
        cart_item_index_map = {}  # cart_item.pk -> index in order_items_data
        parent_cart_items = list(cart.items.filter(parent_bundle__isnull=True))

        for cart_item in parent_cart_items:
            if cart_item.product.product_type in ("bundle", "configurable"):
                for component in cart_item.component_items.all():
                    cart_item_index_map[component.pk] = len(order_items_data)
                    order_items_data.append(
                        {
                            "product": component.product,
                            "variant": component.variant,
                            "quantity": component.quantity,
                        }
                    )
            else:
                cart_item_index_map[cart_item.pk] = len(order_items_data)
                order_items_data.append(
                    {
                        "product": cart_item.product,
                        "variant": cart_item.variant,
                        "quantity": cart_item.quantity,
                    }
                )

        # Select optimal warehouse(s) for order fulfillment
        # Returns {index: warehouse} keyed by position in order_items_data
        try:
            warehouse_allocation = fulfillment_service.select_warehouse_for_order(
                order=order, order_items=order_items_data
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
                item.unit_price_base = (
                    item.unit_price.amount
                    if hasattr(item.unit_price, "amount")
                    else Decimal(str(item.unit_price or 0))
                )
                item.total_price_base = (
                    item.total_price.amount
                    if hasattr(item.total_price, "amount")
                    else Decimal(str(item.total_price or 0))
                )
            else:
                rate = order.exchange_rate_used or Decimal("1")
                if rate == 0:
                    rate = Decimal("1")
                up = (
                    item.unit_price.amount
                    if hasattr(item.unit_price, "amount")
                    else Decimal(str(item.unit_price or 0))
                )
                tp = (
                    item.total_price.amount
                    if hasattr(item.total_price, "amount")
                    else Decimal(str(item.total_price or 0))
                )
                item.unit_price_base = (up / rate).quantize(Decimal("0.01"))
                item.total_price_base = (tp / rate).quantize(Decimal("0.01"))
            item.save(update_fields=["unit_price_base", "total_price_base"])

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
                # Carries gift card recipient/schedule across to the order. The
                # cart is deleted below, so without this the post-payment
                # issuance receiver has nothing to read.
                gift_card_data=cart_item.gift_card_data,
                warehouse=None,  # Set below for regular products; bundles stay None
                stock_allocated=False,
                stock_fulfilled=False,
                parent_bundle=None,
            )
            _set_item_base_amounts(parent_order_item)

            CheckoutService._create_customization_values(parent_order_item)

            # Create design snapshot for visual design editor orders
            if cart_item.customizations and "_design" in cart_item.customizations:
                CheckoutService._create_design_snapshot(
                    parent_order_item, cart_item.customizations["_design"]
                )

            if cart_item.product.product_type in ("bundle", "configurable"):
                for component_cart_item in cart_item.component_items.all():
                    component_warehouse = cart_item_warehouse.get(component_cart_item.pk)
                    component_order_item = OrderItem.objects.create(
                        order=order,
                        product=component_cart_item.product,
                        variant=component_cart_item.variant,
                        product_name=component_cart_item.product.name,
                        variant_name=component_cart_item.variant.name
                        if component_cart_item.variant
                        else "",
                        sku=component_cart_item.variant.sku
                        if component_cart_item.variant
                        else component_cart_item.product.sku,
                        quantity=component_cart_item.quantity,
                        unit_price=component_cart_item.unit_price,
                        total_price=component_cart_item.total_price,
                        customizations=component_cart_item.customizations,
                        warehouse=component_warehouse,
                        stock_allocated=False,
                        stock_fulfilled=False,
                        parent_bundle=parent_order_item,
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
                            component_order_item.save(update_fields=["stock_allocated"])
                        else:
                            raise Exception("reservation_mismatch")
                    except Exception:
                        try:
                            fulfillment_service.allocate_stock(
                                order_item=component_order_item,
                                warehouse=component_order_item.warehouse,
                            )
                            component_order_item.stock_allocated = True
                            component_order_item.save(update_fields=["stock_allocated"])
                        except InsufficientStockError as e:
                            # Pre-order/backorder component: accept it unallocated
                            # (backordered) rather than failing the whole order.
                            if component_order_item.product.can_sell_without_stock():
                                component_order_item.stock_allocated = False
                                component_order_item.save(update_fields=["stock_allocated"])
                                logger.info(
                                    f"Backordered component {component_order_item.sku} — "
                                    f"no stock to allocate: {e}"
                                )
                            else:
                                logger.error(
                                    f"Stock allocation failed for component {component_order_item.sku}: {e}"
                                )
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
                parent_order_item.save(update_fields=["warehouse"])

                try:
                    converted = StockReservationService.convert_reservation_to_order_allocation(
                        cart_item=cart_item,
                        warehouse=parent_order_item.warehouse,
                    )
                    if converted:
                        parent_order_item.stock_allocated = True
                        parent_order_item.save(update_fields=["stock_allocated"])
                    else:
                        raise Exception("reservation_mismatch")
                except Exception:
                    try:
                        fulfillment_service.allocate_stock(
                            order_item=parent_order_item, warehouse=parent_order_item.warehouse
                        )
                        parent_order_item.stock_allocated = True
                        parent_order_item.save(update_fields=["stock_allocated"])
                    except InsufficientStockError as e:
                        # Pre-order/backorder items are expected to have no
                        # on-hand stock. Accept the order with the item left
                        # unallocated (backordered) — it is allocated later when
                        # stock arrives — instead of failing the whole order.
                        if parent_order_item.product.can_sell_without_stock():
                            parent_order_item.stock_allocated = False
                            parent_order_item.save(update_fields=["stock_allocated"])
                            logger.info(
                                f"Backordered {parent_order_item.sku} — no stock to allocate: {e}"
                            )
                        else:
                            logger.error(
                                f"Stock allocation failed for {parent_order_item.sku}: {e}"
                            )
                            _rollback_allocated_stock()
                            order.delete()
                            return False, _("Insufficient stock to complete order"), None
                    except Exception as e:
                        logger.error(f"Stock allocation error: {e}")
                        _rollback_allocated_stock()
                        order.delete()
                        return False, _("Error processing order. Please try again."), None

        # Re-home gift card holds from the checkout session onto the order.
        #
        # MUST happen before `session.delete()` below. Holds reference the
        # session with on_delete=SET_NULL, so deleting it would leave them with
        # neither a session nor an order — orphaned, invisible to
        # GiftCardTenderService.capture_for_order, and never settled. The
        # customer's card would silently never be debited.
        CheckoutService._attach_tenders_to_order(session, order)

        # Process applied vouchers - increment usage counters and create usage records
        #
        # A voucher that has been fully used since it was applied to the cart
        # aborts the whole order. set_rollback keeps create_order's documented
        # (success, message, order) contract — every caller unpacks that tuple,
        # so raising out of here would turn a refused checkout into a 500 —
        # while still discarding the order, its items, and its tender holds.
        try:
            CheckoutService._process_voucher_usage(cart, order)
        except VoucherNoLongerValid as exc:
            transaction.set_rollback(True)
            logger.warning(f"Checkout refused for cart {cart.pk}: {exc}")
            return False, str(exc), None

        # Create bookings for booking items
        CheckoutService._create_bookings(cart, order)

        # Clear cart and session (unless using payment orchestration)
        if clear_session:
            # Create subscriptions for subscription items
            # (orchestration flow defers this to handle_payment_success for payment safety)
            CheckoutService._create_subscriptions(cart, order)
            cart.items.all().delete()
            cart.applied_vouchers.all().delete()
            session.delete()

        # Zero-due: tenders cover the whole order, so there is nothing to charge.
        #
        # Done AFTER the session is cleared so the order is in its final state,
        # and deliberately by marking it paid rather than sending a zero-value
        # charge to a provider — PaymentService.validate_payment_amount rejects
        # `amount <= 0`, correctly, because a gateway has no business being
        # asked for nothing. Marking paid fires the post_save receiver, which
        # captures the holds and debits the cards.
        CheckoutService._settle_if_fully_tendered(order)

        return True, _("Order created successfully"), order

    @staticmethod
    def _settle_if_fully_tendered(order):
        """
        Mark an order paid when its tenders already cover the total.

        Returns:
            bool: True if the order was marked paid here.
        """
        import logging

        from djmoney.money import Money

        from payment_providers.models import PaymentTransaction

        logger = logging.getLogger(__name__)

        if order.payment_status == "paid":
            return False

        currency = order.total_amount.currency
        held = PaymentTransaction.objects.filter(
            order=order,
            transaction_type="authorize",
            status="authorized",
        ).values_list("settlement_amount", "settlement_amount_currency")

        tendered = Money(Decimal("0"), currency)
        for amount, amount_currency in held:
            if amount is None or str(amount_currency) != str(currency):
                # Anything unexpected here means we cannot be confident the
                # order is covered — fall through to normal payment rather
                # than marking an order paid on a figure we do not trust.
                return False
            tendered += Money(amount, currency)

        if tendered < order.total_amount:
            return False

        from django.utils import timezone

        order.payment_status = "paid"
        order.paid_at = timezone.now()
        order.amount_paid = order.total_amount
        # Full save, not update_fields: the settlement receiver keys off
        # post_save, and this is the transition it exists to catch.
        order.save()

        logger.info(
            f"Order {order.order_number} fully covered by tenders "
            f"({tendered}) — marked paid without a gateway charge"
        )
        return True

    @staticmethod
    def _attach_tenders_to_order(session, order):
        """
        Point this session's live tender holds at the order.

        Holds are created against a CheckoutSession because the order does not
        exist yet. Once it does, they belong to the order — the session is
        transient and is deleted at the end of create_order.

        Returns:
            int: number of holds re-homed.
        """
        from payment_providers.models import PaymentTransaction

        return PaymentTransaction.objects.filter(
            checkout_session=session,
            transaction_type="authorize",
            status="authorized",
            order__isnull=True,
        ).update(order=order)

    @staticmethod
    def _create_subscriptions(cart, order, payment_token=None):
        """
        Create subscriptions for any subscription items in the cart.

        Args:
            cart: Cart instance
            order: Order instance created from cart
            payment_token: Optional PaymentToken to bind to subscription items
                that don't already carry one (e.g. minted from the succeeded
                payment). Each cart item's own payment_token takes precedence.

        Returns:
            List of created subscription IDs
        """
        import logging

        from subscriptions.manager import SubscriptionManager

        logger = logging.getLogger(__name__)

        # Idempotency is handled per line by SubscriptionManager.create_subscription,
        # which returns the EXISTING subscription for a repeated
        # (originating_order, product, plan). That is safer than an order-level
        # early-return: it dedups the two settlement paths (sync create_order and
        # orchestration handle_payment_success) AND still retries any line that
        # failed on a previous attempt.
        created_subscriptions = []
        failures = []

        # Process each cart item that is a subscription
        for cart_item in cart.items.filter(is_subscription=True):
            token = cart_item.payment_token or payment_token

            if not cart_item.subscription_plan or not token:
                # The customer has already paid, so a missing plan/token must not
                # be silently dropped. Record it loudly and stamp the order so ops
                # can reconcile (create the subscription manually or refund).
                logger.critical(
                    f"Order {order.order_number}: cart item {cart_item.id} is a subscription "
                    f"but is missing a plan or payment token; subscription NOT created."
                )
                failures.append(cart_item.id)
                continue

            # Resolve pricing tier (stored on cart item, or fall back to plan default)
            pricing_tier = cart_item.pricing_tier or cart_item.subscription_plan.get_default_tier()
            if not pricing_tier:
                logger.critical(
                    f"Order {order.order_number}: subscription plan for cart item {cart_item.id} "
                    f"has no pricing tiers configured; subscription NOT created."
                )
                failures.append(cart_item.id)
                continue

            try:
                # Create subscription using SubscriptionManager
                manager = SubscriptionManager(token.provider_account)
                subscription = manager.create_subscription(
                    user=cart.user,
                    plan=cart_item.subscription_plan,
                    pricing_tier=pricing_tier,
                    payment_token=token,
                    product=cart_item.product,
                    variant=cart_item.variant,
                    quantity=cart_item.quantity,
                    originating_order=order,
                )

                created_subscriptions.append(subscription.subscription_id)
                logger.info(
                    f"Created subscription {subscription.subscription_id} for order {order.order_number}"
                )

            except Exception as e:
                logger.critical(
                    f"Order {order.order_number}: failed to create subscription for cart item "
                    f"{cart_item.id}: {e}"
                )
                failures.append(cart_item.id)
                # Continue processing other subscriptions even if one fails

        if failures:
            # Leave a reconcilable breadcrumb on the order for any gap.
            meta = order.metadata or {}
            meta["subscription_creation_failures"] = failures
            order.metadata = meta
            try:
                order.save(update_fields=["metadata", "updated_at"])
            except Exception:
                logger.exception(
                    f"Order {order.order_number}: could not persist subscription failure metadata"
                )

        return created_subscriptions

    @staticmethod
    def _create_bookings(cart, order):
        """
        Create Booking records for any booking items in the cart.

        When a cart contains booking products with booking_data,
        converts the cart item into a confirmed Booking record.
        Also cleans up any slot reservations.
        """
        import logging
        from datetime import datetime

        from catalog.services.booking_service import BookingAvailabilityService

        logger = logging.getLogger(__name__)
        created_bookings = []

        for cart_item in cart.items.filter(product__product_type="booking"):
            if not cart_item.booking_data:
                continue

            booking_data = cart_item.booking_data

            # Parse datetime strings
            try:
                start_dt = datetime.fromisoformat(
                    booking_data["start_datetime"].replace("Z", "+00:00")
                )
                end_dt = datetime.fromisoformat(booking_data["end_datetime"].replace("Z", "+00:00"))
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
                    "start_datetime": start_dt,
                    "end_datetime": end_dt,
                    "resource_id": booking_data.get("resource_id"),
                    "persons": booking_data.get("persons", {}),
                    "total_cost": cart_item.total_price.amount if cart_item.total_price else 0,
                    "price_breakdown": booking_data.get("price_breakdown", {}),
                    "customer_name": order.shipping_name or "",
                    "customer_email": order.email or "",
                    "customer_phone": order.phone or "",
                    "customer_notes": cart_item.notes or "",
                    "customer_timezone": booking_data.get("timezone", ""),
                }

                success, msg, booking = BookingAvailabilityService.confirm_booking(
                    order_item=order_item,
                    booking_data=booking_data_full,
                )

                if success and booking:
                    created_bookings.append(booking.pk)
                    logger.info(f"Created booking #{booking.pk} for order {order.order_number}")
                else:
                    logger.warning(f"Booking creation returned: {msg} for cart item {cart_item.pk}")

            except Exception as e:
                logger.error(f"Failed to create booking for cart item {cart_item.pk}: {e}")

        return created_bookings

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
        import logging

        from django.db.models import F

        from vouchers.models import VoucherCode, VoucherUsage

        logger = logging.getLogger(__name__)

        for applied_voucher in cart.applied_vouchers.select_related("voucher").all():
            voucher = applied_voucher.voucher

            # Lock, re-check, THEN increment.
            #
            # The old code called an unconditional F() increment "atomic to
            # prevent race conditions". Atomic incrementing is not the same as
            # enforcing a cap: max_uses_total was checked when the voucher was
            # applied to the cart, minutes earlier, and never again. Two carts
            # holding the same single-use code both passed that check and both
            # incremented, so the code was spent twice. Nothing re-validated
            # expiry or per-customer limits at checkout either.
            #
            # Same shape as LedgerService.record_redemption, fixed in R1.
            locked = VoucherCode.objects.select_for_update().get(pk=voucher.pk)

            if locked.max_uses_total is not None and (locked.current_uses >= locked.max_uses_total):
                # Refuse the order rather than silently dropping the voucher and
                # charging full price: the customer authorised a specific
                # amount, and billing more than they agreed to is worse than
                # sending them back to the cart. Raising rolls back
                # create_order, so no order and no charge results.
                raise VoucherNoLongerValid(
                    _("The voucher %(code)s has just been fully used.") % {"code": locked.code}
                )

            if not locked.is_valid:
                raise VoucherNoLongerValid(
                    _("The voucher %(code)s is no longer valid.") % {"code": locked.code}
                )

            locked.current_uses = F("current_uses") + 1
            locked.save(update_fields=["current_uses"])

            VoucherUsage.objects.create(
                voucher=voucher,
                user=cart.user if cart.user and cart.user.is_authenticated else None,
                order=order,
                discount_amount=applied_voucher.discount_amount,
                cart_total=cart.total_amount,
                session_key=getattr(cart, "session_key", None),
            )

            logger.info(
                f"Recorded usage of voucher {voucher.code} for order {order.order_number} "
                f"(discount: {applied_voucher.discount_amount})"
            )

    @staticmethod
    def cleanup_expired_sessions():
        """
        Clean up expired checkout sessions
        Should be run periodically via cron/celery
        """
        expired_sessions = CheckoutSession.objects.filter(expires_at__lt=timezone.now())
        count = expired_sessions.count()
        expired_sessions.delete()
        return count
