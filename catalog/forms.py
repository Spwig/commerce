"""
Forms for Catalog app admin customization
"""
import json
from decimal import Decimal, InvalidOperation

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ProductVariant, AttributeValue, ProductAttributeAssignment


class CommaSeparatedDecimalField(forms.CharField):
    """
    A form field that accepts comma-separated decimal values and stores them as a JSON list.

    Input: "25, 50, 100, 200"
    Output (to model): [25, 50, 100, 200]

    This provides a user-friendly interface for entering gift card denominations
    without requiring merchants to understand JSON syntax.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', _('Enter amounts separated by commas (e.g., 25, 50, 100)'))
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        """
        Convert JSON list to comma-separated string for display.
        [25, 50, 100] -> "25, 50, 100"
        """
        if value is None:
            return ''

        if isinstance(value, str):
            # If it's already a string (e.g., from form POST), return as is
            # but check if it's JSON first
            try:
                value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value

        if isinstance(value, list):
            # Format numbers nicely - remove trailing zeros for whole numbers
            formatted = []
            for v in value:
                if isinstance(v, (int, float, Decimal)):
                    if v == int(v):
                        formatted.append(str(int(v)))
                    else:
                        formatted.append(str(v))
                else:
                    formatted.append(str(v))
            return ', '.join(formatted)

        return str(value) if value else ''

    def to_python(self, value):
        """
        Convert comma-separated string to Python list.
        "25, 50, 100" -> [25, 50, 100]
        """
        if not value:
            return []

        # Handle case where value is already a list
        if isinstance(value, list):
            return value

        # Split by comma and process each value
        result = []
        parts = value.split(',')

        for part in parts:
            part = part.strip()
            if not part:
                continue

            try:
                # Try to convert to Decimal first for precision
                decimal_val = Decimal(part)
                # Convert to int if it's a whole number, otherwise float
                if decimal_val == int(decimal_val):
                    result.append(int(decimal_val))
                else:
                    result.append(float(decimal_val))
            except (InvalidOperation, ValueError):
                raise forms.ValidationError(
                    _('Invalid value "%(value)s". Please enter numbers only, separated by commas.'),
                    code='invalid',
                    params={'value': part}
                )

        return result

    def validate(self, value):
        """Validate that all values are positive numbers."""
        super().validate(value)

        if value:
            for v in value:
                if v <= 0:
                    raise forms.ValidationError(
                        _('All amounts must be positive numbers. Found: %(value)s'),
                        code='invalid',
                        params={'value': v}
                    )


class ProductVariantForm(forms.ModelForm):
    """
    Custom form for ProductVariant with context-aware attribute filtering.

    Only shows attribute values for attributes that are assigned to the product.
    This prevents merchants from seeing irrelevant attribute values.
    """

    class Meta:
        model = ProductVariant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Note: The actual queryset filtering is handled by ProductVariantInline.formfield_for_manytomany
        # This form primarily handles other customizations and validations

        # Get product from instance (for existing variants)
        product = None
        if self.instance and self.instance.product_id:
            product = self.instance.product

        # Update help text based on context
        if product:
            assigned_attrs = ProductAttributeAssignment.objects.filter(
                product=product
            ).exists()

            if assigned_attrs:
                self.fields['selected_attributes'].help_text = _(
                    "Select attribute values for this variant. "
                    "Only values for attributes assigned to this product are shown."
                )
            else:
                self.fields['selected_attributes'].help_text = _(
                    "No attributes assigned to this product yet. "
                    "Add attributes in the 'Product Attributes & Variations' section above."
                )
