"""
Promotion Service - Evaluate shipping promotions and calculate adjusted costs.

This service handles:
1. Promotion matching and evaluation based on cart conditions
2. Rate table lookups for tiered pricing
3. Promotion-based cost adjustments (discounts, surcharges, free shipping)
4. Integration with ShippingMethod base costs
"""

import logging
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from djmoney.money import Money

if TYPE_CHECKING:
    from shipping.models import ShippingPromotion

logger = logging.getLogger(__name__)


class ShippingPromotionService:
    """Service for evaluating shipping promotions and calculating adjusted costs."""

    @staticmethod
    def _resolve_currency(shipping_method):
        """Resolve currency from shipping method, falling back to site settings."""
        if hasattr(shipping_method, "flat_rate_cost") and shipping_method.flat_rate_cost:
            return shipping_method.flat_rate_cost.currency
        try:
            from core.models import SiteSettings

            settings = SiteSettings.objects.first()
            if settings and hasattr(settings, "default_currency") and settings.default_currency:
                return settings.default_currency
        except Exception:
            pass
        return "USD"

    @staticmethod
    def evaluate_rules(
        cart, address, shipping_method, user=None
    ) -> list[tuple["ShippingPromotion", str]]:
        """
        Find all applicable shipping promotions for given conditions.

        Args:
            cart: Cart instance
            address: Address instance or dict with country/state/postal_code
            shipping_method: ShippingMethod instance
            user: User instance (optional)

        Returns:
            List of tuples: [(promotion, reason_applies), ...]
            Promotions are returned in priority order (highest first)
        """
        from shipping.models import ShippingPromotion

        applicable_rules = []

        # Get all active promotions in priority order
        rules = (
            ShippingPromotion.objects.filter(is_active=True)
            .select_related("created_by")
            .prefetch_related(
                "zones",
                "shipping_methods",
                "requires_products",
                "requires_categories",
                "excludes_products",
                "excludes_categories",
                "customer_groups",
            )
            .order_by("-priority", "name")
        )

        logger.debug(f"Evaluating {rules.count()} active shipping promotions")

        for rule in rules:
            applies, reason = rule.applies_to_cart(
                cart=cart, address=address, shipping_method=shipping_method, user=user
            )

            if applies:
                logger.debug(f"Promotion '{rule.name}' applies: {reason}")
                applicable_rules.append((rule, reason))

                # Stop if this promotion has stop_further_promotions flag
                if rule.stop_further_promotions:
                    logger.debug(f"Promotion '{rule.name}' stops further promotion evaluation")
                    break
            else:
                logger.debug(f"Promotion '{rule.name}' does not apply: {reason}")

        return applicable_rules

    @staticmethod
    def calculate_shipping_with_rules(
        base_cost: Money, cart, address, shipping_method, user=None
    ) -> dict[str, Any]:
        """
        Calculate final shipping cost after applying all matching promotions.

        Args:
            base_cost: Base shipping cost from ShippingMethod
            cart: Cart instance
            address: Address instance or dict
            shipping_method: ShippingMethod instance
            user: User instance (optional)

        Returns:
            Dict with shipping calculation details:
            {
                'base_cost': Money,
                'final_cost': Money,
                'rules_applied': [
                    {
                        'promotion_name': str,
                        'promotion_type': str,
                        'adjustment': Money,
                        'reason': str
                    }
                ],
                'total_discount': Money,
                'total_surcharge': Money
            }
        """
        from djmoney.money import Money

        # Get applicable promotions
        applicable_rules = ShippingPromotionService.evaluate_rules(
            cart=cart, address=address, shipping_method=shipping_method, user=user
        )

        if not applicable_rules:
            logger.info("No shipping promotions apply")
            return {
                "base_cost": base_cost,
                "final_cost": base_cost,
                "rules_applied": [],
                "total_discount": Money(0, base_cost.currency),
                "total_surcharge": Money(0, base_cost.currency),
            }

        # Apply promotions in order
        current_cost = base_cost
        rules_applied = []
        total_discount = Money(0, base_cost.currency)
        total_surcharge = Money(0, base_cost.currency)

        for rule, reason in applicable_rules:
            # Calculate adjusted cost
            new_cost = rule.calculate_adjustment(current_cost)

            # Calculate the difference
            adjustment = new_cost - current_cost

            # Track discounts vs surcharges
            if adjustment.amount < 0:
                total_discount += abs(adjustment)
            elif adjustment.amount > 0:
                total_surcharge += adjustment

            rules_applied.append(
                {
                    "promotion_name": rule.name,
                    "promotion_type": rule.promotion_type,
                    "promotion_value": str(rule.promotion_value) if rule.promotion_value else None,
                    "adjustment": adjustment,
                    "cost_before": current_cost,
                    "cost_after": new_cost,
                    "reason": reason,
                }
            )

            logger.info(
                f"Applied promotion '{rule.name}' ({rule.promotion_type}): "
                f"{current_cost} → {new_cost}"
            )

            current_cost = new_cost

        return {
            "base_cost": base_cost,
            "final_cost": current_cost,
            "rules_applied": rules_applied,
            "total_discount": total_discount,
            "total_surcharge": total_surcharge,
        }

    @staticmethod
    def apply_rules_to_cost(
        base_cost: Decimal, shipping_method, cart, address, user=None
    ) -> Decimal:
        """
        Simpler wrapper around calculate_shipping_with_rules() that returns just final cost.

        This is used by ShippingMethod.calculate_cost() for promotion integration.

        Args:
            base_cost: Base shipping cost as Decimal
            shipping_method: ShippingMethod instance
            cart: Cart instance
            address: Address instance or dict
            user: User instance (optional)

        Returns:
            Decimal: Final cost after applying all rules
        """
        from djmoney.money import Money

        # Convert base_cost Decimal to Money using resolved currency
        currency = ShippingPromotionService._resolve_currency(shipping_method)
        base_cost_money = Money(base_cost, currency)

        # Calculate with rules
        calculation = ShippingPromotionService.calculate_shipping_with_rules(
            base_cost=base_cost_money,
            cart=cart,
            address=address,
            shipping_method=shipping_method,
            user=user,
        )

        # Return just the final cost amount as Decimal
        return calculation["final_cost"].amount

    @staticmethod
    def get_rate_from_table(rate_table, value: Decimal, address=None) -> Money | None:
        """
        Get shipping rate from a rate table based on a value.

        Args:
            rate_table: ShippingRateTable instance
            value: Cart weight, price, or quantity to lookup
            address: Address instance or dict (for zone matching)

        Returns:
            Money: Calculated rate, or None if no matching tier
        """
        # Check if table applies to address
        if address and not rate_table.applies_to_address(address):
            logger.debug(f"Rate table '{rate_table.name}' does not apply to address")
            return None

        # Get rate from table
        rate = rate_table.get_rate_for_value(value)

        if rate:
            logger.info(
                f"Rate table '{rate_table.name}' ({rate_table.basis_type}): {value} → {rate}"
            )
        else:
            logger.warning(f"No matching tier in rate table '{rate_table.name}' for value {value}")

        return rate

    @staticmethod
    def calculate_rate_table_cost(shipping_method, cart, address) -> Money | None:
        """
        Calculate shipping cost using rate tables linked to shipping method.

        This is called by ShippingMethod.calculate_cost() for table-rate methods.

        Args:
            shipping_method: ShippingMethod instance
            cart: Cart instance
            address: Address instance or dict

        Returns:
            Money: Calculated shipping cost, or None if no tables apply
        """

        # Get active rate tables for this shipping method
        rate_tables = shipping_method.rate_tables.filter(is_active=True)

        if not rate_tables.exists():
            logger.warning(
                f"No active rate tables found for shipping method '{shipping_method.name}'"
            )
            return None

        # Try each rate table in order
        for table in rate_tables:
            # Determine value based on table basis type
            if table.basis_type == "weight":
                value = cart.total_weight
            elif table.basis_type == "price":
                value = Decimal(str(cart.subtotal.amount))
            elif table.basis_type == "quantity":
                value = Decimal(str(cart.total_items))
            else:
                logger.error(f"Unknown basis_type: {table.basis_type}")
                continue

            # Try to get rate from this table
            rate = ShippingPromotionService.get_rate_from_table(
                rate_table=table, value=value, address=address
            )

            if rate:
                return rate

        logger.info(
            f"No matching rates found in any table for shipping method '{shipping_method.name}'"
        )
        return None

    @staticmethod
    def calculate_shipping_for_cart(cart, shipping_method, address, user=None) -> dict[str, Any]:
        """
        Complete shipping cost calculation with base cost + rules + tables.

        This is the main entry point for cart shipping calculations.

        Args:
            cart: Cart instance
            shipping_method: ShippingMethod instance
            address: Address instance or dict
            user: User instance (optional)

        Returns:
            Dict with complete calculation:
            {
                'method_name': str,
                'method_type': str,
                'base_cost': Money,
                'final_cost': Money,
                'rules_applied': List[Dict],
                'total_discount': Money,
                'total_surcharge': Money,
                'calculation_breakdown': str  # human-readable explanation
            }
        """
        from djmoney.money import Money

        logger.info(f"Calculating shipping for cart with method '{shipping_method.name}'")

        # Resolve currency from method or site settings
        currency = ShippingPromotionService._resolve_currency(shipping_method)

        # Step 1: Get base cost from shipping method
        # Check if method uses rate tables
        if shipping_method.method_type == "table_rate":
            base_cost = ShippingPromotionService.calculate_rate_table_cost(
                shipping_method=shipping_method, cart=cart, address=address
            )
            if base_cost is None:
                # Fallback to method's default if table lookup fails
                base_cost = Money(
                    shipping_method.flat_rate_cost.amount if shipping_method.flat_rate_cost else 0,
                    currency,
                )
        else:
            # Use standard method calculation
            base_cost_decimal = shipping_method.calculate_cost(cart, address)
            base_cost = Money(base_cost_decimal, currency)

        logger.info(f"Base shipping cost: {base_cost}")

        # Step 2: Apply shipping promotions
        calculation = ShippingPromotionService.calculate_shipping_with_rules(
            base_cost=base_cost,
            cart=cart,
            address=address,
            shipping_method=shipping_method,
            user=user,
        )

        # Step 3: Add method details
        calculation["method_name"] = shipping_method.name
        calculation["method_type"] = shipping_method.method_type

        # Step 4: Generate human-readable breakdown
        breakdown_parts = [
            f"Method: {shipping_method.name}",
            f"Base cost: {calculation['base_cost']}",
        ]

        if calculation["rules_applied"]:
            breakdown_parts.append(f"Promotions applied: {len(calculation['rules_applied'])}")
            for rule_info in calculation["rules_applied"]:
                breakdown_parts.append(
                    f"  - {rule_info['promotion_name']} ({rule_info['promotion_type']}): "
                    f"{rule_info['adjustment']}"
                )

        if calculation["total_discount"].amount > 0:
            breakdown_parts.append(f"Total discount: {calculation['total_discount']}")

        if calculation["total_surcharge"].amount > 0:
            breakdown_parts.append(f"Total surcharge: {calculation['total_surcharge']}")

        breakdown_parts.append(f"Final cost: {calculation['final_cost']}")

        calculation["calculation_breakdown"] = "\n".join(breakdown_parts)

        logger.info(f"Final shipping cost: {calculation['final_cost']}")

        return calculation
