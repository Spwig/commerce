"""
Tax calculation service.

Handles matching TaxRate rules to addresses, calculating taxes
with compound support, and loading preset tax configurations.
"""
import logging
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q

logger = logging.getLogger(__name__)

TWOPLACES = Decimal('0.01')


class TaxService:
    """Service for tax calculation, matching, and preset loading."""

    @staticmethod
    def get_applicable_taxes(country, state='', city='', postal_code='', product=None):
        """
        Find all active TaxRate rules matching the given address.

        Uses specificity-based matching: more specific geographic rules
        score higher. Within the same specificity, higher priority wins.

        Args:
            country: ISO 3166-1 alpha-2 code or full country name
            state: State/province name or code
            city: City name
            postal_code: Postal/zip code
            product: Optional Product instance for exemption filtering

        Returns:
            List of TaxRate objects ordered by specificity then priority.
        """
        from cart.models import TaxRate

        country_code = TaxService._resolve_country_code(country)
        if not country_code:
            return []

        rates = (
            TaxRate.objects
            .filter(is_active=True, country=country_code)
            .prefetch_related('exempt_categories')
        )

        matched = []
        for rate in rates:
            # State filter: blank means "all states"
            if rate.state and rate.state.lower() != state.lower():
                continue
            # City filter: blank means "all cities"
            if rate.city and rate.city.lower() != city.lower():
                continue
            # Postal code filter: empty list means "all codes"
            if rate.postal_codes and postal_code not in rate.postal_codes:
                continue
            # Product exemption check
            if product and not rate.applies_to_product(product):
                continue

            # Specificity score: more specific = higher score
            specificity = 0
            if rate.state:
                specificity += 1
            if rate.city:
                specificity += 2
            if rate.postal_codes:
                specificity += 4

            matched.append((specificity, rate.priority, rate))

        # Sort: highest specificity first, then highest priority
        matched.sort(key=lambda x: (-x[0], -x[1]))
        return [m[2] for m in matched]

    @staticmethod
    def calculate_tax(items, shipping_cost, country, state='', city='', postal_code=''):
        """
        Calculate all applicable taxes for a set of items and shipping.

        Args:
            items: List of (product, quantity, line_total) tuples
            shipping_cost: Decimal shipping cost
            country: Country code or name
            state: State/province
            city: City name
            postal_code: Postal/zip code

        Returns:
            Tuple of (total_tax: Decimal, breakdown: list[dict])
        """
        country_code = TaxService._resolve_country_code(country)
        if not country_code:
            return Decimal('0.00'), []

        from cart.models import TaxRate

        # Get all applicable rates for this location (without product filter)
        all_rates = TaxService.get_applicable_taxes(
            country_code, state, city, postal_code
        )

        if not all_rates:
            return Decimal('0.00'), []

        # Build per-rate taxable amounts
        rate_amounts = {}  # tax_rate_id -> taxable_amount
        for rate in all_rates:
            taxable = Decimal('0.00')
            for product, quantity, line_total in items:
                if rate.applies_to_product(product):
                    taxable += line_total
            if rate.applies_to_shipping and shipping_cost:
                taxable += Decimal(str(shipping_cost))
            rate_amounts[rate.id] = taxable

        # Separate compound vs non-compound
        non_compound = [r for r in all_rates if not r.compound]
        compound = [r for r in all_rates if r.compound]

        breakdown = []
        total_tax = Decimal('0.00')
        non_compound_total = Decimal('0.00')

        # Phase 1: Non-compound taxes on base amounts
        for rate in non_compound:
            base = rate_amounts.get(rate.id, Decimal('0.00'))
            if base <= 0:
                continue
            amount = (base * rate.rate).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
            non_compound_total += amount
            total_tax += amount
            breakdown.append(TaxService._build_breakdown_entry(rate, amount))

        # Phase 2: Compound taxes on (base + non-compound total)
        for rate in compound:
            base = rate_amounts.get(rate.id, Decimal('0.00'))
            if base <= 0:
                continue
            compound_base = base + non_compound_total
            amount = (compound_base * rate.rate).quantize(TWOPLACES, rounding=ROUND_HALF_UP)
            total_tax += amount
            breakdown.append(TaxService._build_breakdown_entry(rate, amount))

        # Calculate shipping-specific tax for breakdown summary
        shipping_tax = Decimal('0.00')
        if shipping_cost:
            shipping_decimal = Decimal(str(shipping_cost))
            for rate in all_rates:
                if rate.applies_to_shipping:
                    tax_on_shipping = (shipping_decimal * rate.rate).quantize(
                        TWOPLACES, rounding=ROUND_HALF_UP
                    )
                    shipping_tax += tax_on_shipping

        return total_tax, breakdown

    @staticmethod
    def load_preset(group_key, skip_existing=True):
        """
        Load a preset tax configuration from the DB into active TaxRate records.

        Args:
            group_key: TaxPresetGroup.key (e.g., 'eu_vat')
            skip_existing: If True, skip rates that already exist

        Returns:
            Tuple of (created_count, skipped_count)
        """
        from cart.models import TaxRate, TaxPresetGroup

        try:
            group = TaxPresetGroup.objects.prefetch_related('rates').get(
                key=group_key, is_active=True
            )
        except TaxPresetGroup.DoesNotExist:
            logger.warning(f"Tax preset group not found: {group_key}")
            return 0, 0

        created = 0
        skipped = 0

        for preset_rate in group.rates.filter(is_active=True):
            if skip_existing:
                exists = TaxRate.objects.filter(
                    country=preset_rate.country,
                    state=preset_rate.state,
                    tax_type=preset_rate.tax_type,
                ).exists()
                if exists:
                    skipped += 1
                    continue

            name = preset_rate.country_name
            if preset_rate.state_name:
                name = f"{preset_rate.state_name} {group.tax_type.upper()}"

            TaxRate.objects.create(
                name=name,
                country=preset_rate.country,
                state=preset_rate.state,
                rate=preset_rate.rate,
                tax_type=preset_rate.tax_type,
                is_active=True,
                priority=0,
            )
            created += 1

        logger.info(
            f"Loaded preset '{group_key}': {created} created, {skipped} skipped"
        )
        return created, skipped

    @staticmethod
    def _resolve_country_code(country_value):
        """
        Resolve a country value to ISO alpha-2 code.

        Handles both 2-char codes and full country names by looking up
        CountryMapping when needed.
        """
        if not country_value:
            return ''

        value = str(country_value).strip()

        # Already an ISO code
        if len(value) == 2:
            return value.upper()

        # Try to look up by country name
        try:
            from geoip.models import CountryMapping
            mapping = CountryMapping.objects.filter(
                country_name__iexact=value
            ).first()
            if mapping:
                return mapping.country_code.upper()
        except Exception:
            pass

        logger.warning(f"Could not resolve country code for: {value}")
        return ''

    @staticmethod
    def _build_breakdown_entry(rate, amount):
        """Build a standardized breakdown dict entry for a tax rate."""
        jurisdiction = rate.country
        if rate.state:
            jurisdiction += f", {rate.state}"
        if rate.city:
            jurisdiction += f", {rate.city}"

        return {
            'tax_rate_id': rate.id,
            'name': rate.name,
            'rate': str(rate.rate),
            'rate_display': f"{rate.rate * 100}%",
            'amount': str(amount),
            'jurisdiction': jurisdiction,
            'tax_type': rate.tax_type,
            'compound': rate.compound,
        }
