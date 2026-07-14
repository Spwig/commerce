"""
Attribute Management Service for WooCommerce Migration.

Handles creation and matching of ProductAttribute and AttributeValue records
during product variation imports.
"""

import logging

from django.utils.text import slugify

from catalog.models import AttributeValue, ProductAttribute, ProductAttributeAssignment

logger = logging.getLogger(__name__)


class AttributeService:
    """
    Service for managing attributes during migration.

    Responsibilities:
    - Get or create ProductAttribute records
    - Get or create AttributeValue records
    - Create ProductAttributeAssignment for products
    - Cache lookups for performance

    Usage:
        service = AttributeService()
        attribute = service.get_or_create_attribute('Color')
        value = service.get_or_create_attribute_value(attribute, 'Red')
        pairs = service.parse_woocommerce_attributes(wc_attributes)
    """

    def __init__(self):
        # Cache for performance: {slug: ProductAttribute}
        self._attribute_cache: dict[str, ProductAttribute] = {}
        # Cache: {(attribute_id, value_slug): AttributeValue}
        self._value_cache: dict[tuple[int, str], AttributeValue] = {}

    def get_or_create_attribute(
        self, name: str, attribute_type: str = "select"
    ) -> ProductAttribute:
        """
        Get or create a ProductAttribute by name.

        Args:
            name: Attribute name (e.g., 'Color', 'Size')
            attribute_type: Display type ('select', 'color', 'button', 'radio')

        Returns:
            ProductAttribute instance
        """
        slug = slugify(name)

        # Check cache first
        if slug in self._attribute_cache:
            return self._attribute_cache[slug]

        # Database lookup or create
        attribute, created = ProductAttribute.objects.get_or_create(
            slug=slug,
            defaults={
                "name": name,
                "type": self._infer_attribute_type(name, attribute_type),
                "is_required": True,
                "sort_order": 0,
            },
        )

        if created:
            logger.info(f"Created ProductAttribute: {name}")

        # Cache it
        self._attribute_cache[slug] = attribute
        return attribute

    def get_or_create_attribute_value(
        self, attribute: ProductAttribute, value: str, color_hex: str = ""
    ) -> AttributeValue:
        """
        Get or create an AttributeValue for an attribute.

        Args:
            attribute: ProductAttribute instance
            value: Value label (e.g., 'Red', 'Large')
            color_hex: Optional hex color for color swatches

        Returns:
            AttributeValue instance
        """
        slug = slugify(value)
        cache_key = (attribute.id, slug)

        # Check cache
        if cache_key in self._value_cache:
            return self._value_cache[cache_key]

        # Database lookup or create
        attr_value, created = AttributeValue.objects.get_or_create(
            attribute=attribute,
            slug=slug,
            defaults={
                "value": value,
                "color_hex": color_hex,
                "sort_order": 0,
            },
        )

        if created:
            logger.debug(f"Created AttributeValue: {attribute.name}: {value}")

        # Cache it
        self._value_cache[cache_key] = attr_value
        return attr_value

    def ensure_product_attribute_assignment(
        self, product, attribute: ProductAttribute, values: list[AttributeValue]
    ) -> ProductAttributeAssignment:
        """
        Ensure a product has an attribute assignment with the given values.

        Creates or updates the ProductAttributeAssignment linking a product
        to an attribute with specific allowed values.

        Args:
            product: Product instance
            attribute: ProductAttribute instance
            values: List of AttributeValue instances to allow

        Returns:
            ProductAttributeAssignment instance
        """
        assignment, created = ProductAttributeAssignment.objects.get_or_create(
            product=product, attribute=attribute, defaults={"sort_order": 0}
        )

        # Add values to allowed_values M2M (idempotent)
        for value in values:
            assignment.allowed_values.add(value)

        if created:
            logger.debug(f"Created ProductAttributeAssignment: {product.name} -> {attribute.name}")

        return assignment

    def parse_woocommerce_attributes(
        self, wc_attributes: list[dict]
    ) -> list[tuple[ProductAttribute, AttributeValue]]:
        """
        Parse WooCommerce variation attributes and return Spwig equivalents.

        WooCommerce format:
        [
            {"id": 1, "name": "Color", "option": "Red"},
            {"id": 2, "name": "Size", "option": "Large"}
        ]

        Args:
            wc_attributes: List of WooCommerce attribute dicts

        Returns:
            List of (ProductAttribute, AttributeValue) tuples
        """
        result = []

        for attr_data in wc_attributes:
            attr_name = attr_data.get("name", "")
            attr_option = attr_data.get("option", "")

            if not attr_name or not attr_option:
                logger.debug(f"Skipping empty attribute: {attr_data}")
                continue

            # Detect color hex if attribute is a color type
            color_hex = ""
            if self._is_color_attribute(attr_name):
                color_hex = self._detect_color_hex(attr_option)

            # Get or create attribute and value
            attribute = self.get_or_create_attribute(attr_name)
            value = self.get_or_create_attribute_value(attribute, attr_option, color_hex=color_hex)

            result.append((attribute, value))

        return result

    def build_variant_name(
        self, attribute_pairs: list[tuple[ProductAttribute, AttributeValue]]
    ) -> str:
        """
        Build a variant name from attribute pairs.

        Args:
            attribute_pairs: List of (ProductAttribute, AttributeValue) tuples

        Returns:
            Variant name string (e.g., "Large / Red")
        """
        if not attribute_pairs:
            return "Default"

        return " / ".join([value.value for _, value in attribute_pairs])

    def _infer_attribute_type(self, name: str, default: str) -> str:
        """
        Infer attribute display type from name.

        Args:
            name: Attribute name
            default: Default type if not inferred

        Returns:
            Attribute type string
        """
        name_lower = name.lower()

        if "color" in name_lower or "colour" in name_lower:
            return "color"
        elif "size" in name_lower:
            return "button"

        return default

    def _is_color_attribute(self, name: str) -> bool:
        """Check if attribute is a color type."""
        name_lower = name.lower()
        return "color" in name_lower or "colour" in name_lower

    def _detect_color_hex(self, value: str) -> str:
        """
        Attempt to detect a hex color from a color value name.

        Common colors are mapped to their hex values.

        Args:
            value: Color value name (e.g., 'Red', 'Blue')

        Returns:
            Hex color code or empty string
        """
        # Common color mappings
        color_map = {
            "red": "#FF0000",
            "blue": "#0000FF",
            "green": "#008000",
            "yellow": "#FFFF00",
            "orange": "#FFA500",
            "purple": "#800080",
            "pink": "#FFC0CB",
            "black": "#000000",
            "white": "#FFFFFF",
            "gray": "#808080",
            "grey": "#808080",
            "brown": "#A52A2A",
            "navy": "#000080",
            "teal": "#008080",
            "maroon": "#800000",
            "olive": "#808000",
            "silver": "#C0C0C0",
            "gold": "#FFD700",
            "beige": "#F5F5DC",
            "coral": "#FF7F50",
            "cyan": "#00FFFF",
            "magenta": "#FF00FF",
            "lime": "#00FF00",
            "indigo": "#4B0082",
            "violet": "#EE82EE",
            "aqua": "#00FFFF",
            "tan": "#D2B48C",
            "khaki": "#F0E68C",
            "lavender": "#E6E6FA",
            "salmon": "#FA8072",
            "turquoise": "#40E0D0",
            "charcoal": "#36454F",
            "burgundy": "#800020",
            "cream": "#FFFDD0",
            "ivory": "#FFFFF0",
            "peach": "#FFCBA4",
            "mint": "#98FF98",
        }

        value_lower = value.lower().strip()

        # Check if value is already a hex code
        if value_lower.startswith("#") and len(value_lower) in [4, 7]:
            return value_lower.upper()

        # Look up in color map
        return color_map.get(value_lower, "")

    def clear_cache(self):
        """Clear internal caches."""
        self._attribute_cache.clear()
        self._value_cache.clear()
        logger.debug("AttributeService cache cleared")

    def get_cache_stats(self) -> dict[str, int]:
        """
        Get cache statistics.

        Returns:
            Dict with cache counts
        """
        return {
            "attributes_cached": len(self._attribute_cache),
            "values_cached": len(self._value_cache),
        }
