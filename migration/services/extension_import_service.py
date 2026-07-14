"""
WooCommerce Extension Import Service

Handles importing WooCommerce product extension data (subscriptions, add-ons,
bundles, gift cards, composite products, bookings) into Spwig's native models.

Each method follows the pattern: accept product + raw WC data, create the
Spwig model records, return success/failure. Extension import failures never
block product creation.
"""

import logging
from decimal import Decimal, InvalidOperation
from typing import Any

from django.utils.text import slugify

logger = logging.getLogger(__name__)


class WooCommerceExtensionImportService:
    """
    Service for importing WooCommerce product extension data
    into Spwig's native models.
    """

    def __init__(self, migration_job, currency="USD"):
        self.job = migration_job
        self.currency = currency
        self._subscription_plan_cache = {}  # Cache plans to reuse across products

    # =====================================================================
    # Gap 1: WooCommerce Subscriptions → SubscriptionPlan + PlanPricingTier
    # =====================================================================

    def import_subscription_data(
        self, product, product_data: dict, subscription_details: dict
    ) -> Any | None:
        """
        Create SubscriptionPlan + PlanPricingTier from WooCommerce subscription meta.

        Maps:
            _subscription_period → PlanPricingTier.billing_cycle
            _subscription_sign_up_fee → SubscriptionPlan.setup_fee
            _subscription_trial_period + length → SubscriptionPlan.trial_period_days
            _subscription_length → SubscriptionPlan.max_billing_cycles

        Returns:
            SubscriptionPlan instance or None
        """
        from djmoney.money import Money

        from subscriptions.models import PlanPricingTier, SubscriptionPlan

        meta = subscription_details.get("meta", {})
        if not meta:
            logger.warning(f"No subscription meta for product {product.name}")
            return None

        # Extract subscription parameters
        period = meta.get("_subscription_period", "month")
        interval = self._safe_int(meta.get("_subscription_period_interval", "1"), 1)
        setup_fee = self._safe_decimal(meta.get("_subscription_sign_up_fee", "0"))
        trial_days = self._calculate_trial_days(
            meta.get("_subscription_trial_period", ""), meta.get("_subscription_trial_length", "0")
        )
        max_cycles = self._safe_int(meta.get("_subscription_length", "0"), 0)
        billing_cycle = self._map_wc_period_to_billing_cycle(period)

        # Build cache key to reuse identical plans across products
        cache_key = (billing_cycle, interval, str(setup_fee), trial_days, max_cycles)
        if cache_key in self._subscription_plan_cache:
            plan = self._subscription_plan_cache[cache_key]
            product.is_subscription_enabled = True
            product.allow_one_time_purchase = False
            product.subscription_plans.add(plan)
            product.save(update_fields=["is_subscription_enabled", "allow_one_time_purchase"])
            return plan

        # Create new SubscriptionPlan
        plan_name = f"{product.name} - Subscription"
        plan_slug = slugify(f"{product.slug}-subscription")

        # Ensure unique slug
        counter = 1
        original_slug = plan_slug
        while SubscriptionPlan.objects.filter(slug=plan_slug).exists():
            plan_slug = f"{original_slug}-{counter}"
            counter += 1

        plan = SubscriptionPlan.objects.create(
            name=plan_name,
            slug=plan_slug,
            pricing_model="tiered",
            setup_fee=Money(setup_fee, self.currency),
            trial_period_days=trial_days,
            cancellation_policy="anytime",
            max_billing_cycles=max_cycles if max_cycles > 0 else None,
            is_active=True,
            is_public=True,
        )

        # Create the billing tier
        tier_name = self._build_tier_name(billing_cycle, interval)
        PlanPricingTier.objects.create(
            plan=plan,
            tier_name=tier_name,
            billing_cycle=billing_cycle,
            billing_interval=interval,
            discount_percentage=Decimal("0.00"),
            is_default=True,
            is_active=True,
        )

        # Link plan to product
        product.is_subscription_enabled = True
        product.allow_one_time_purchase = False
        product.subscription_plans.add(plan)
        product.save(update_fields=["is_subscription_enabled", "allow_one_time_purchase"])

        # Cache for reuse
        self._subscription_plan_cache[cache_key] = plan

        logger.info(f"Created subscription plan '{plan_name}' for product '{product.name}'")
        return plan

    def _map_wc_period_to_billing_cycle(self, wc_period: str) -> str:
        """Map WC period strings to Spwig billing cycle choices."""
        mapping = {
            "day": "daily",
            "week": "weekly",
            "month": "monthly",
            "year": "annual",
        }
        return mapping.get(wc_period, "monthly")

    def _calculate_trial_days(self, trial_period: str, trial_length: str) -> int:
        """Convert WC trial period + length to total trial days."""
        length = self._safe_int(trial_length, 0)
        if length <= 0:
            return 0

        period_to_days = {
            "day": 1,
            "week": 7,
            "month": 30,
            "year": 365,
        }
        return length * period_to_days.get(trial_period, 0)

    def _build_tier_name(self, billing_cycle: str, interval: int) -> str:
        """Build human-readable tier name."""
        if interval == 1:
            names = {
                "daily": "Daily",
                "weekly": "Weekly",
                "monthly": "Monthly",
                "quarterly": "Quarterly",
                "semiannual": "Semi-Annual",
                "annual": "Annual",
            }
            return names.get(billing_cycle, billing_cycle.title())
        return f"Every {interval} {billing_cycle.replace('ly', '').replace('ial', '')}s"

    # =====================================================================
    # Gap 2: WooCommerce Product Add-Ons → CustomizationOption
    # =====================================================================

    def import_product_addons(self, product, product_data: dict) -> list:
        """
        Create CustomizationOption records from WooCommerce Product Add-Ons meta.

        Maps WC add-on types to Spwig CustomizationOption.option_type and pricing.

        Returns:
            List of created CustomizationOption instances
        """

        meta_data = product_data.get("meta_data", [])
        addons = None
        for item in meta_data:
            if item.get("key") == "_product_addons":
                addons = item.get("value")
                break

        if not addons:
            return []

        if isinstance(addons, str):
            import json

            try:
                addons = json.loads(addons)
            except (json.JSONDecodeError, TypeError):
                return []

        if not isinstance(addons, list):
            return []

        created_options = []
        for idx, addon in enumerate(addons):
            option = self._create_customization_from_addon(product, addon, idx)
            if option:
                created_options.append(option)

        # Enable customization on the product
        if created_options:
            product.allow_customization = True
            product.save(update_fields=["allow_customization"])

        return created_options

    def _create_customization_from_addon(self, product, addon_data: dict, sort_order: int):
        """Create a single CustomizationOption from a WC add-on definition."""
        from djmoney.money import Money

        from catalog.models import CustomizationOption

        addon_name = addon_data.get("name", "") or addon_data.get("title", "")
        if not addon_name:
            return None

        # Map WC add-on type to Spwig option_type
        wc_type = addon_data.get("type", "")
        option_type = self._map_addon_type(wc_type)
        if option_type is None:
            # Heading type or unmapped - skip
            return None

        # Map pricing
        pricing_type, price_amount = self._map_addon_pricing(addon_data)

        # Build slug
        option_slug = slugify(addon_name) or f"addon-{sort_order}"

        # Ensure unique slug for this product
        counter = 1
        original_slug = option_slug
        while CustomizationOption.objects.filter(product=product, slug=option_slug).exists():
            option_slug = f"{original_slug}-{counter}"
            counter += 1

        # Build choices for select/radio/checkbox types
        choices = []
        wc_options = addon_data.get("options", [])
        if wc_options and option_type == "select":
            for opt in wc_options:
                choice = {
                    "value": slugify(opt.get("label", "")) or f"option-{len(choices)}",
                    "label": opt.get("label", ""),
                }
                opt_price = self._safe_decimal(opt.get("price", "0"))
                if opt_price > 0:
                    choice["price_modifier"] = float(opt_price)
                choices.append(choice)

        # Build option
        option = CustomizationOption.objects.create(
            product=product,
            name=addon_name,
            slug=option_slug,
            option_type=option_type,
            is_required=bool(addon_data.get("required", 0)),
            sort_order=sort_order,
            pricing_type=pricing_type,
            price_amount=Money(price_amount, self.currency),
            choices=choices if choices else [],
            max_length=self._safe_int(addon_data.get("max"), None)
            if option_type in ("text", "textarea")
            else None,
            min_value=self._safe_decimal(addon_data.get("min"))
            if option_type == "number"
            else None,
            max_value=self._safe_decimal(addon_data.get("max"))
            if option_type == "number"
            else None,
        )

        return option

    def _map_addon_type(self, wc_type: str) -> str | None:
        """Map WC add-on type to Spwig CustomizationOption.option_type."""
        mapping = {
            "custom_text": "text",
            "custom_text_area": "textarea",
            "custom_textarea": "textarea",
            "file_upload": "file",
            "input_multiplier": "number",
            "select": "select",
            "radiobutton": "select",
            "checkbox": "select",
            "custom_price": "number",
            "quantity": "number",
            "custom_letters_only": "text",
            "custom_digits_only": "number",
            "custom_letters_or_digits": "text",
            "custom_email": "text",
        }
        return mapping.get(wc_type)  # Returns None for 'heading' and unmapped

    def _map_addon_pricing(self, addon_data: dict) -> tuple:
        """Map WC add-on pricing to Spwig pricing_type + price_amount."""
        adjust_price = addon_data.get("adjust_price")
        if not adjust_price or str(adjust_price) == "0":
            return "free", Decimal("0.00")

        price_type = addon_data.get("price_type", "flat_fee")
        price = self._safe_decimal(addon_data.get("price", "0"))

        mapping = {
            "flat_fee": "fixed",
            "quantity_based": "per_unit",
            "percentage_based": "percentage",
        }
        return mapping.get(price_type, "fixed"), price

    # =====================================================================
    # Gap 3: WooCommerce Product Bundles → BundleItem
    # =====================================================================

    def import_bundle_data(self, product, product_data: dict, bundle_details: dict) -> list:
        """
        Create BundleItem records from WooCommerce Product Bundles plugin data.

        Handles deferred resolution: if a component product hasn't been imported yet,
        stores the reference in imported_meta for post-import resolution.

        Returns:
            List of created BundleItem instances
        """
        from catalog.models import BundleItem
        from catalog.models import Product as CatalogProduct

        bundled_items = bundle_details.get("items", {})
        if not bundled_items:
            return []

        # Handle both dict and list formats
        if isinstance(bundled_items, dict):
            items_list = list(bundled_items.values())
        elif isinstance(bundled_items, list):
            items_list = bundled_items
        else:
            return []

        created_items = []
        deferred_items = []
        all_priced_individually = True
        none_priced_individually = True

        for idx, item_data in enumerate(items_list):
            wc_product_id = str(item_data.get("product_id", ""))
            if not wc_product_id:
                continue

            # Look up component product by external_id
            component = CatalogProduct.objects.filter(external_id=wc_product_id).first()

            if not component:
                # Component not yet imported - defer
                deferred_items.append(
                    {
                        "product_id": wc_product_id,
                        "quantity": self._safe_int(item_data.get("quantity_default", "1"), 1),
                        "is_optional": item_data.get("optional", "no") == "yes",
                        "sort_order": idx,
                        "allow_variant_selection": bool(item_data.get("allowed_variations")),
                    }
                )
                logger.warning(
                    f"Bundle component product {wc_product_id} not found for '{product.name}', deferring"
                )
                continue

            is_optional = item_data.get("optional", "no") == "yes"
            quantity = self._safe_int(item_data.get("quantity_default", "1"), 1)
            priced_individually = item_data.get("priced_individually", "no") == "yes"

            if priced_individually:
                none_priced_individually = False
            else:
                all_priced_individually = False

            bundle_item = BundleItem.objects.create(
                bundle=product,
                component_product=component,
                quantity=quantity,
                sort_order=idx,
                is_optional=is_optional,
                allow_variant_selection=bool(item_data.get("allowed_variations")),
            )
            created_items.append(bundle_item)

        # Store deferred items for post-import resolution
        if deferred_items:
            meta = product.imported_meta or {}
            meta["deferred_bundle_items"] = deferred_items
            product.imported_meta = meta
            product.save(update_fields=["imported_meta"])

        # Set bundle pricing strategy
        if created_items:
            if all_priced_individually:
                product.bundle_pricing_strategy = "components_sum"
            elif none_priced_individually:
                product.bundle_pricing_strategy = "fixed"
            else:
                product.bundle_pricing_strategy = "fixed"  # Safest fallback for mixed
            product.save(update_fields=["bundle_pricing_strategy"])

        return created_items

    # =====================================================================
    # Gap 4: WooCommerce Gift Cards → gift_card product type
    # =====================================================================

    def import_gift_card_data(self, product, product_data: dict, gift_card_details: dict) -> None:
        """
        Configure product as gift_card type with proper denomination settings.

        Supports multiple WC gift card plugins (Official, YITH, PW, AFGC).
        """
        # Extract denomination amounts from multiple possible fields
        amounts = gift_card_details.get("amounts", [])

        if isinstance(amounts, str):
            import json

            try:
                amounts = json.loads(amounts)
            except (json.JSONDecodeError, TypeError):
                amounts = []

        # Parse amounts to list of decimals
        denominations = []
        for a in amounts if isinstance(amounts, list) else []:
            val = self._safe_decimal(a)
            if val and val > 0:
                denominations.append(float(val))

        # Check YITH amounts_type
        amounts_type = gift_card_details.get("amounts_type", "")

        # Determine denomination type
        if denominations and amounts_type == "both":
            denomination_type = "both"
        elif denominations:
            denomination_type = "fixed"
        else:
            denomination_type = "custom"

        # Update product
        product.product_type = "gift_card"
        product.is_digital = True

        product.gift_card_denomination_type = denomination_type
        if denominations:
            product.gift_card_denominations = denominations

        # Set min/max for custom amounts
        if denomination_type in ("custom", "both"):
            if denominations:
                product.gift_card_min_amount = min(denominations)
                product.gift_card_max_amount = max(denominations) * 2  # Reasonable max
            else:
                product.gift_card_min_amount = 5.00
                product.gift_card_max_amount = 500.00

        product.save()

        logger.info(
            f"Configured gift card '{product.name}': "
            f"{denomination_type} denominations ({len(denominations)} amounts)"
        )

    # =====================================================================
    # Gap 5: WooCommerce Composite Products → ConfigurationSlot/Option
    # =====================================================================

    def import_composite_data(self, product, product_data: dict, composite_details: dict) -> list:
        """
        Create ConfigurationSlot + ConfigurationSlotOption records from
        WooCommerce Composite Products data.

        Returns:
            List of created ConfigurationSlot instances
        """
        from catalog.models import (
            ConfigurationSlot,
            ConfigurationSlotOption,
        )
        from catalog.models import (
            Product as CatalogProduct,
        )

        components = composite_details.get("components", [])
        if not components:
            return []

        # Handle dict format (keyed by component ID)
        if isinstance(components, dict):
            components = list(components.values())

        created_slots = []
        deferred_items = []
        all_priced_individually = True
        none_priced_individually = True

        for idx, comp in enumerate(components):
            comp_name = comp.get("title", "") or comp.get("name", "") or f"Component {idx + 1}"
            comp_slug = slugify(comp_name) or f"component-{idx}"

            # Ensure unique slug
            counter = 1
            original_slug = comp_slug
            while ConfigurationSlot.objects.filter(product=product, slug=comp_slug).exists():
                comp_slug = f"{original_slug}-{counter}"
                counter += 1

            is_required = comp.get("optional", "no") != "yes"
            min_qty = self._safe_int(comp.get("quantity_min", "1"), 1)
            max_qty = self._safe_int(comp.get("quantity_max", "1"), 1)

            slot = ConfigurationSlot.objects.create(
                product=product,
                name=comp_name,
                slug=comp_slug,
                description=comp.get("description", ""),
                is_required=is_required,
                min_selections=min_qty if is_required else 0,
                max_selections=max_qty,
                sort_order=self._safe_int(comp.get("sort_order", str(idx)), idx),
            )

            # Create options from assigned product IDs
            assigned_ids = comp.get("assigned_ids", []) or comp.get("assigned_id", [])
            if isinstance(assigned_ids, (str, int)):
                assigned_ids = [assigned_ids]

            default_id = comp.get("default_id", None)
            priced_individually = comp.get("priced_individually", "no") == "yes"

            if priced_individually:
                none_priced_individually = False
            else:
                all_priced_individually = False

            options_created = 0
            for opt_idx, wc_id in enumerate(assigned_ids):
                wc_id_str = str(wc_id)
                option_product = CatalogProduct.objects.filter(external_id=wc_id_str).first()

                if not option_product:
                    deferred_items.append(
                        {
                            "slot_id": slot.id,
                            "product_id": wc_id_str,
                            "is_default": str(wc_id) == str(default_id),
                            "sort_order": opt_idx,
                        }
                    )
                    logger.warning(
                        f"Composite component product {wc_id_str} not found for "
                        f"slot '{comp_name}' in '{product.name}', deferring"
                    )
                    continue

                ConfigurationSlotOption.objects.create(
                    slot=slot,
                    option_product=option_product,
                    is_default=(str(wc_id) == str(default_id)),
                    sort_order=opt_idx,
                )
                options_created += 1

            if options_created > 0:
                created_slots.append(slot)
            elif not deferred_items:
                # No options resolved and nothing deferred - remove empty slot
                slot.delete()

        # Store deferred items for post-import resolution
        if deferred_items:
            meta = product.imported_meta or {}
            meta["deferred_composite_items"] = deferred_items
            product.imported_meta = meta
            product.save(update_fields=["imported_meta"])

        # Set configurator pricing strategy
        if all_priced_individually:
            product.configurator_pricing_strategy = "components_sum"
        elif none_priced_individually:
            product.configurator_pricing_strategy = "fixed"
        else:
            product.configurator_pricing_strategy = "base_plus_adjustments"
        product.save(update_fields=["configurator_pricing_strategy"])

        return created_slots

    # =====================================================================
    # Gap 6 & 7: WooCommerce Bookings (preserve data for future module)
    # =====================================================================

    def import_booking_data(self, product, product_data: dict, booking_details: dict) -> Any | None:
        """
        Import WooCommerce Bookings data into Spwig's native booking models.

        Creates BookingConfig, BookingResource, BookingPersonType, and
        BookingAvailabilityRule records from WC _wc_booking_* meta fields.

        Maps:
            _wc_booking_duration → BookingConfig.duration
            _wc_booking_duration_type → BookingConfig.duration_type
            _wc_booking_duration_unit → BookingConfig.duration_unit
            _wc_booking_has_resources → BookingResource records
            _wc_booking_has_persons → BookingPersonType records
            _wc_booking_availability → BookingAvailabilityRule records
            accommodation-booking → BookingConfig.booking_type = 'accommodation'

        Returns:
            BookingConfig instance or None
        """
        from catalog.models import (
            BookingConfig,
        )

        meta = booking_details.get("meta", {})
        is_accommodation = booking_details.get("is_accommodation", False)

        # Map WC duration unit to Spwig duration unit
        wc_unit_map = {
            "minute": "minute",
            "hour": "hour",
            "day": "day",
            "month": "day",  # approximation
        }

        # Map WC duration type
        wc_duration_type = meta.get("_wc_booking_duration_type", "fixed")
        duration_type = "customer_selected" if wc_duration_type == "customer" else "fixed"

        # Duration
        duration = self._safe_int(meta.get("_wc_booking_duration", 60))
        duration_unit = wc_unit_map.get(meta.get("_wc_booking_duration_unit", "hour"), "hour")

        # For accommodation, use 'night' as duration unit
        if is_accommodation:
            duration_unit = "night"
            duration = 1  # Accommodation is per-night

        # Min/max duration for customer-selected
        min_duration = self._safe_int(meta.get("_wc_booking_min_duration")) or None
        max_duration = self._safe_int(meta.get("_wc_booking_max_duration")) or None

        # Buffer times
        buffer_before = self._safe_int(meta.get("_wc_booking_buffer_period", 0))

        # Advance booking
        min_advance = self._safe_int(meta.get("_wc_booking_min_date", 0))
        min_advance_unit = meta.get("_wc_booking_min_date_unit", "day")
        max_advance = self._safe_int(meta.get("_wc_booking_max_date", 365))
        max_advance_unit = meta.get("_wc_booking_max_date_unit", "month")

        # Map WC advance units to Spwig
        advance_unit_map = {"hour": "hour", "day": "day", "week": "week", "month": "month"}
        min_advance_unit = advance_unit_map.get(min_advance_unit, "day")
        max_advance_unit = advance_unit_map.get(max_advance_unit, "day")

        # Capacity
        max_bookings = self._safe_int(meta.get("_wc_booking_qty", 1)) or 1

        # Confirmation
        requires_confirmation = meta.get("_wc_booking_requires_confirmation") == "yes"

        # Cancellation
        cancellation_enabled = meta.get("_wc_booking_user_can_cancel") == "yes"

        # Calendar display
        calendar_display = "date_range" if is_accommodation else "calendar"

        # Check-in/check-out for accommodation
        check_in_time = None
        check_out_time = None
        if is_accommodation:
            try:
                from datetime import time

                ci = meta.get("_wc_accommodation_booking_check_in_time", "")
                co = meta.get("_wc_accommodation_booking_check_out_time", "")
                if ci:
                    parts = ci.split(":")
                    check_in_time = time(int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
                if co:
                    parts = co.split(":")
                    check_out_time = time(int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
            except (ValueError, IndexError):
                pass

        # Create BookingConfig
        booking_config, _ = BookingConfig.objects.update_or_create(
            product=product,
            defaults={
                "booking_type": "accommodation" if is_accommodation else "appointment",
                "duration_type": duration_type,
                "duration": duration,
                "duration_unit": duration_unit,
                "min_duration": min_duration,
                "max_duration": max_duration,
                "buffer_before": buffer_before,
                "buffer_after": 0,
                "min_advance": min_advance,
                "min_advance_unit": min_advance_unit,
                "max_advance": max_advance,
                "max_advance_unit": max_advance_unit,
                "max_bookings_per_slot": max_bookings,
                "confirmation_required": requires_confirmation,
                "cancellation_allowed": cancellation_enabled,
                "calendar_display": calendar_display,
                "customer_timezone_enabled": True,
                "check_in_time": check_in_time,
                "check_out_time": check_out_time,
            },
        )

        # Import resources
        resource_count = 0
        if booking_details.get("has_resources"):
            resource_count = self._import_booking_resources(product, meta)

        # Import person types
        person_count = 0
        if booking_details.get("has_persons"):
            person_count = self._import_booking_person_types(product, meta)

        # Import availability rules
        rule_count = self._import_booking_availability_rules(product, meta)

        # Store original meta for reference
        imported_meta = product.imported_meta or {}
        imported_meta["booking_import"] = {
            "original_type": booking_details.get("original_type"),
            "resources_imported": resource_count,
            "persons_imported": person_count,
            "rules_imported": rule_count,
        }
        product.imported_meta = imported_meta
        product.save(update_fields=["imported_meta"])

        logger.info(
            f"Imported booking config for '{product.name}': "
            f"type={'accommodation' if is_accommodation else 'appointment'}, "
            f"{resource_count} resources, {person_count} person types, {rule_count} rules"
        )
        return booking_config

    def _import_booking_resources(self, product, meta: dict) -> int:
        """Import WC booking resources as BookingResource records."""
        from catalog.models import BookingResource

        # WC stores resources as serialized data in _wc_booking_resources
        resources_data = meta.get("_wc_booking_resources", [])
        if isinstance(resources_data, str):
            try:
                import json

                resources_data = json.loads(resources_data)
            except (json.JSONDecodeError, TypeError):
                return 0

        if not isinstance(resources_data, list):
            return 0

        count = 0
        assignment = meta.get("_wc_booking_resources_assignment", "customer")
        assignment_type = "customer_selected" if assignment == "customer" else "automatic"

        for idx, res in enumerate(resources_data):
            if not isinstance(res, dict):
                continue

            name = res.get("title", res.get("resource_title", f"Resource {idx + 1}"))
            cost = self._safe_decimal(res.get("base_cost", res.get("block_cost", 0)))

            BookingResource.objects.create(
                product=product,
                name=name,
                resource_type="staff",  # WC doesn't differentiate
                quantity=self._safe_int(res.get("qty", 1)) or 1,
                base_cost_adjustment=cost,
                assignment_type=assignment_type,
                sort_order=idx,
                is_active=True,
            )
            count += 1

        return count

    def _import_booking_person_types(self, product, meta: dict) -> int:
        """Import WC booking person types as BookingPersonType records."""
        from catalog.models import BookingPersonType

        # WC stores person types in _wc_booking_person_types
        person_data = meta.get("_wc_booking_person_types", [])
        if isinstance(person_data, str):
            try:
                import json

                person_data = json.loads(person_data)
            except (json.JSONDecodeError, TypeError):
                return 0

        if not isinstance(person_data, list):
            return 0

        # If no explicit person types but persons enabled, create a default
        if not person_data:
            min_p = self._safe_int(meta.get("_wc_booking_min_persons_group", 1))
            max_p = self._safe_int(meta.get("_wc_booking_max_persons_group", 10))
            BookingPersonType.objects.create(
                product=product,
                name="Guest",
                cost_adjustment=Decimal("0.00"),
                min_persons=min_p or 1,
                max_persons=max_p or 10,
                sort_order=0,
            )
            return 1

        count = 0
        for idx, pt in enumerate(person_data):
            if not isinstance(pt, dict):
                continue

            name = pt.get("name", pt.get("block_cost_name", f"Person Type {idx + 1}"))
            cost = self._safe_decimal(pt.get("cost", pt.get("block_cost", 0)))
            min_p = self._safe_int(pt.get("min", 0))
            max_p = self._safe_int(pt.get("max", 10))

            BookingPersonType.objects.create(
                product=product,
                name=name,
                cost_adjustment=cost,
                min_persons=min_p,
                max_persons=max_p or 10,
                sort_order=idx,
            )
            count += 1

        return count

    def _import_booking_availability_rules(self, product, meta: dict) -> int:
        """Import WC booking availability rules."""
        import json as json_mod
        from datetime import date, time

        from catalog.models import BookingAvailabilityRule

        # WC stores availability in _wc_booking_availability
        avail_data = meta.get("_wc_booking_availability", [])
        if isinstance(avail_data, str):
            try:
                avail_data = json_mod.loads(avail_data)
            except (json_mod.JSONDecodeError, TypeError):
                return 0

        if not isinstance(avail_data, list):
            return 0

        count = 0
        for idx, rule in enumerate(avail_data):
            if not isinstance(rule, dict):
                continue

            rule_type = rule.get("type", "")
            bookable = rule.get("bookable", "yes") == "yes"

            spwig_rule_type = "available" if bookable else "unavailable"

            # Map WC rule types to Spwig scope
            scope = "all_dates"
            start_date = None
            end_date = None
            start_time = None
            end_time = None
            days_of_week = None

            try:
                if rule_type == "custom":
                    # Date range
                    scope = "date_range"
                    if rule.get("from"):
                        start_date = date.fromisoformat(rule["from"])
                    if rule.get("to"):
                        end_date = date.fromisoformat(rule["to"])

                elif rule_type == "months":
                    # Specific month range
                    scope = "date_range"
                    # WC uses month numbers; approximate as date range
                    if rule.get("from"):
                        start_date = date(2026, int(rule["from"]), 1)
                    if rule.get("to"):
                        end_date = date(2026, int(rule["to"]), 28)

                elif rule_type == "weeks":
                    # Day-of-week range
                    scope = "days_of_week"
                    # WC uses 1=Sunday to 7=Saturday
                    from_day = self._safe_int(rule.get("from", 1))
                    to_day = self._safe_int(rule.get("to", 7))
                    # Convert to 0=Monday
                    wc_to_iso = {1: 6, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5}
                    days = []
                    for d in range(from_day, to_day + 1):
                        if d in wc_to_iso:
                            days.append(wc_to_iso[d])
                    days_of_week = sorted(set(days))

                elif rule_type == "days":
                    scope = "days_of_week"
                    from_day = self._safe_int(rule.get("from", 1))
                    to_day = self._safe_int(rule.get("to", 7))
                    wc_to_iso = {1: 6, 2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5}
                    days = []
                    for d in range(from_day, to_day + 1):
                        if d in wc_to_iso:
                            days.append(wc_to_iso[d])
                    days_of_week = sorted(set(days))

                elif rule_type == "time" or rule_type == "time:range":
                    scope = "time_range"
                    if rule.get("from"):
                        parts = str(rule["from"]).split(":")
                        start_time = time(int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
                    if rule.get("to"):
                        parts = str(rule["to"]).split(":")
                        end_time = time(int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)

            except (ValueError, TypeError, IndexError) as e:
                logger.debug(f"Skipping booking rule due to parse error: {e}")
                continue

            BookingAvailabilityRule.objects.create(
                product=product,
                resource=None,
                rule_type=spwig_rule_type,
                scope=scope,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                days_of_week=days_of_week or [],
                priority=idx,
            )
            count += 1

        return count

    # =====================================================================
    # Post-Import: Deferred Resolution
    # =====================================================================

    def resolve_deferred_extensions(self):
        """
        Second pass: resolve bundle/composite components that weren't
        available during first-pass import.
        """
        from catalog.models import BundleItem, ConfigurationSlot, ConfigurationSlotOption
        from catalog.models import Product as CatalogProduct

        resolved_count = 0

        # Resolve deferred bundle items
        products_with_bundles = CatalogProduct.objects.filter(
            migration_job=self.job,
            imported_meta__has_key="deferred_bundle_items",
        )

        for product in products_with_bundles:
            deferred = product.imported_meta.get("deferred_bundle_items", [])
            resolved = []

            for item in deferred:
                component = CatalogProduct.objects.filter(
                    external_id=str(item["product_id"])
                ).first()

                if component:
                    BundleItem.objects.create(
                        bundle=product,
                        component_product=component,
                        quantity=item.get("quantity", 1),
                        is_optional=item.get("is_optional", False),
                        sort_order=item.get("sort_order", 0),
                        allow_variant_selection=item.get("allow_variant_selection", False),
                    )
                    resolved.append(item["product_id"])
                    resolved_count += 1

            # Clean up resolved items from meta
            if resolved:
                remaining = [i for i in deferred if i["product_id"] not in resolved]
                if remaining:
                    product.imported_meta["deferred_bundle_items"] = remaining
                else:
                    del product.imported_meta["deferred_bundle_items"]
                product.save(update_fields=["imported_meta"])

        # Resolve deferred composite items
        products_with_composites = CatalogProduct.objects.filter(
            migration_job=self.job,
            imported_meta__has_key="deferred_composite_items",
        )

        for product in products_with_composites:
            deferred = product.imported_meta.get("deferred_composite_items", [])
            resolved = []

            for item in deferred:
                option_product = CatalogProduct.objects.filter(
                    external_id=str(item["product_id"])
                ).first()

                if option_product:
                    try:
                        slot = ConfigurationSlot.objects.get(id=item["slot_id"])
                        ConfigurationSlotOption.objects.create(
                            slot=slot,
                            option_product=option_product,
                            is_default=item.get("is_default", False),
                            sort_order=item.get("sort_order", 0),
                        )
                        resolved.append(item["product_id"])
                        resolved_count += 1
                    except ConfigurationSlot.DoesNotExist:
                        pass

            # Clean up resolved items from meta
            if resolved:
                remaining = [i for i in deferred if i["product_id"] not in resolved]
                if remaining:
                    product.imported_meta["deferred_composite_items"] = remaining
                else:
                    del product.imported_meta["deferred_composite_items"]
                product.save(update_fields=["imported_meta"])

        if resolved_count > 0:
            logger.info(f"Resolved {resolved_count} deferred extension references")

        return resolved_count

    # =====================================================================
    # Utility Methods
    # =====================================================================

    def _safe_int(self, value, default=0):
        """Safely convert value to int."""
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _safe_decimal(self, value, default=None):
        """Safely convert value to Decimal."""
        if value is None or value == "":
            return default if default is not None else Decimal("0.00")
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return default if default is not None else Decimal("0.00")
