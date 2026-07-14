"""
MigrationMapping Model
Custom field mappings for source platform custom fields/metadata.
Allows mapping WooCommerce meta fields, Shopify metafields, etc. to platform fields.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class MigrationMapping(models.Model):
    """
    Custom field mappings for source platform custom fields.
    Allows merchants to map custom meta fields from WooCommerce, Shopify, etc.
    to their platform's fields.

    Example: Map WooCommerce _custom_brand → Platform Brand field
    """

    job = models.ForeignKey(
        "migration.MigrationJob",
        on_delete=models.CASCADE,
        related_name="mappings",
        help_text=_("Parent migration job"),
    )

    # Source field (from WooCommerce, Shopify, etc.)
    SOURCE_TYPES = [
        ("product", _("Product")),
        ("product_variant", _("Product Variant")),
        ("category", _("Category")),
        ("customer", _("Customer")),
        ("order", _("Order")),
        ("review", _("Review")),
        ("blog_post", _("Blog Post")),
        ("blog_category", _("Blog Category")),
        ("blog_tag", _("Blog Tag")),
    ]
    source_type = models.CharField(
        max_length=50, choices=SOURCE_TYPES, help_text=_("Type of source data")
    )

    source_field = models.CharField(
        max_length=100, help_text=_("Source field name (e.g., '_custom_brand', 'metafields.brand')")
    )

    source_field_label = models.CharField(
        max_length=200, blank=True, help_text=_("Human-readable label for source field")
    )

    # Destination field (on our platform)
    DEST_MODELS = [
        ("Product", _("Product")),
        ("ProductVariant", _("Product Variant")),
        ("Category", _("Category")),
        ("User", _("Customer")),
        ("Order", _("Order")),
        ("Review", _("Review")),
        ("BlogPost", _("Blog Post")),
        ("BlogCategory", _("Blog Category")),
        ("BlogTag", _("Blog Tag")),
    ]
    dest_model = models.CharField(
        max_length=50, choices=DEST_MODELS, help_text=_("Destination model name")
    )

    dest_field = models.CharField(
        max_length=100, help_text=_("Destination field name (e.g., 'brand', 'short_description')")
    )

    dest_field_label = models.CharField(
        max_length=200, blank=True, help_text=_("Human-readable label for destination field")
    )

    # Transformation Rules
    TRANSFORM_TYPES = [
        ("none", _("No Transformation")),
        ("string", _("Convert to String")),
        ("integer", _("Convert to Integer")),
        ("decimal", _("Convert to Decimal")),
        ("boolean", _("Convert to Boolean")),
        ("json", _("Parse JSON")),
        ("date", _("Parse Date")),
        ("url", _("Validate URL")),
        ("email", _("Validate Email")),
        # WooCommerce-specific transforms
        ("money", _("Convert to Money")),
        ("integer_nullable", _("Integer (allow null)")),
        ("decimal_nullable", _("Decimal (allow null)")),
        ("woocommerce_status", _("WooCommerce Status")),
        ("woocommerce_type", _("WooCommerce Product Type")),
        ("woocommerce_backorders", _("WooCommerce Backorders")),
        ("meta_array", _("Meta Data Array")),
        ("category_array", _("Category Array")),
        ("image_array", _("Image Array")),
        ("category_parent", _("Category Parent Resolution")),
        ("custom", _("Custom Function")),
        # Shopify-specific transforms
        ("shopify_status", _("Shopify Product Status")),
        ("shopify_order_status", _("Shopify Order Status")),
        ("shopify_discount_type", _("Shopify Discount Type")),
        ("shopify_discount_value", _("Shopify Discount Value")),
        ("shopify_inventory_tracked", _("Shopify Inventory Tracked")),
        ("shopify_inventory_policy", _("Shopify Inventory Policy")),
        ("comma_separated", _("Comma-Separated to List")),
        # Magento-specific transforms
        ("magento_status", _("Magento Product Status")),
        ("magento_visibility", _("Magento Product Visibility")),
        ("magento_order_status", _("Magento Order Status")),
        ("magento_discount_type", _("Magento Discount Type")),
    ]
    transform_type = models.CharField(
        max_length=30,
        choices=TRANSFORM_TYPES,
        default="none",
        help_text=_("Data transformation to apply"),
    )

    # Custom transformation function name (if transform_type='custom')
    transform_function = models.CharField(
        max_length=100, blank=True, help_text=_("Python function name for custom transformation")
    )

    # Default value if source field is empty
    default_value = models.TextField(
        blank=True, help_text=_("Default value if source field is missing or empty")
    )

    # Mapping rules
    is_required = models.BooleanField(
        default=False, help_text=_("Whether this field is required (skip item if missing)")
    )

    skip_if_empty = models.BooleanField(
        default=False, help_text=_("Skip entire item if this field is empty")
    )

    # Usage statistics
    times_used = models.IntegerField(
        default=0, help_text=_("Number of times this mapping was applied")
    )

    times_failed = models.IntegerField(
        default=0, help_text=_("Number of times transformation failed")
    )

    # Auto-detected or manually created
    is_auto_detected = models.BooleanField(
        default=False, help_text=_("Whether this mapping was auto-detected from data")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Migration Mapping")
        verbose_name_plural = _("Migration Mappings")
        unique_together = ["job", "source_type", "source_field"]
        indexes = [
            models.Index(fields=["job", "source_type"]),
            models.Index(fields=["source_type", "source_field"]),
        ]

    def __str__(self):
        return f"{self.source_field} → {self.dest_model}.{self.dest_field}"

    def apply_transformation(self, value):
        """
        Apply transformation to a value.
        Returns (success, transformed_value, error_message)
        """
        if value is None or value == "":
            if self.default_value:
                return True, self.default_value, None
            if self.skip_if_empty:
                return False, None, "Field is empty and skip_if_empty is True"
            return True, None, None

        try:
            if self.transform_type == "none":
                return True, value, None

            elif self.transform_type == "string":
                return True, str(value), None

            elif self.transform_type == "integer":
                return True, int(value), None

            elif self.transform_type == "decimal":
                from decimal import Decimal

                return True, Decimal(str(value)), None

            elif self.transform_type == "boolean":
                # Handle various boolean representations
                if isinstance(value, bool):
                    return True, value, None
                if isinstance(value, str):
                    return True, value.lower() in ("true", "yes", "1", "on"), None
                return True, bool(value), None

            elif self.transform_type == "json":
                import json

                if isinstance(value, str):
                    return True, json.loads(value), None
                return True, value, None

            elif self.transform_type == "date":
                from django.utils.dateparse import parse_date, parse_datetime

                if isinstance(value, str):
                    parsed = parse_datetime(value) or parse_date(value)
                    if parsed:
                        return True, parsed, None
                    return False, None, f"Could not parse date: {value}"
                return True, value, None

            elif self.transform_type == "url":
                from django.core.exceptions import ValidationError
                from django.core.validators import URLValidator

                validator = URLValidator()
                try:
                    validator(value)
                    return True, value, None
                except ValidationError as e:
                    return False, None, f"Invalid URL: {str(e)}"

            elif self.transform_type == "email":
                from django.core.exceptions import ValidationError
                from django.core.validators import EmailValidator

                validator = EmailValidator()
                try:
                    validator(value)
                    return True, value, None
                except ValidationError as e:
                    return False, None, f"Invalid email: {str(e)}"

            elif self.transform_type == "custom":
                if not self.transform_function:
                    return False, None, "Custom transform function not specified"

                # Import and call custom function
                try:
                    from importlib import import_module

                    module_path, function_name = self.transform_function.rsplit(".", 1)
                    module = import_module(module_path)
                    func = getattr(module, function_name)
                    result = func(value)
                    return True, result, None
                except Exception as e:
                    return False, None, f"Custom transformation failed: {str(e)}"

            elif self.transform_type == "shopify_status":
                from ..utils.shopify_transformers import transform_shopify_status

                return True, transform_shopify_status(value), None

            elif self.transform_type == "shopify_order_status":
                from ..utils.shopify_transformers import transform_shopify_order_status

                return True, transform_shopify_order_status(value), None

            elif self.transform_type == "shopify_discount_type":
                from ..utils.shopify_transformers import transform_shopify_discount_type

                return True, transform_shopify_discount_type(value), None

            elif self.transform_type == "shopify_discount_value":
                from ..utils.shopify_transformers import transform_shopify_discount_value

                return True, transform_shopify_discount_value(value), None

            elif self.transform_type == "shopify_inventory_tracked":
                from ..utils.shopify_transformers import transform_shopify_inventory_tracked

                return True, transform_shopify_inventory_tracked(value), None

            elif self.transform_type == "shopify_inventory_policy":
                from ..utils.shopify_transformers import transform_shopify_inventory_policy

                return True, transform_shopify_inventory_policy(value), None

            elif self.transform_type == "comma_separated":
                from ..utils.shopify_transformers import parse_shopify_tags

                return True, parse_shopify_tags(value), None

            elif self.transform_type == "magento_status":
                from ..utils.magento_transformers import transform_magento_status

                return True, transform_magento_status(value), None

            elif self.transform_type == "magento_visibility":
                from ..utils.magento_transformers import transform_magento_visibility

                return True, transform_magento_visibility(value), None

            elif self.transform_type == "magento_order_status":
                from ..utils.magento_transformers import transform_magento_order_status

                return True, transform_magento_order_status(value), None

            elif self.transform_type == "magento_discount_type":
                from ..utils.magento_transformers import transform_magento_discount_type

                return True, transform_magento_discount_type(value), None

            else:
                return False, None, f"Unknown transformation type: {self.transform_type}"

        except Exception as e:
            self.times_failed += 1
            self.save(update_fields=["times_failed"])
            return False, None, str(e)

    def increment_usage(self):
        """Increment usage counter"""
        self.times_used += 1
        self.save(update_fields=["times_used"])

    @classmethod
    def get_mappings_for_source_type(cls, job, source_type):
        """Get all mappings for a specific source type"""
        return cls.objects.filter(job=job, source_type=source_type)

    @classmethod
    def create_from_detection(cls, job, source_type, source_field, dest_model, dest_field):
        """Create an auto-detected mapping"""
        mapping, created = cls.objects.get_or_create(
            job=job,
            source_type=source_type,
            source_field=source_field,
            defaults={
                "dest_model": dest_model,
                "dest_field": dest_field,
                "is_auto_detected": True,
            },
        )
        return mapping
