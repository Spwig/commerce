"""
Variant Serializers for Admin API

Serializers for product variant management.
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from catalog.models import ProductVariant, AttributeValue


class AdminVariantListSerializer(serializers.ModelSerializer):
    """Serializer for variant list view."""
    price_amount = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    available_stock = serializers.IntegerField(read_only=True)
    attributes = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'name',
            'sku',
            'pricing_strategy',
            'price_amount',
            'currency',
            'is_active',
            'available_stock',
            'attributes',
            'barcode',
            'image_url',
            'created_at',
        ]

    def get_price_amount(self, obj):
        if obj.price:
            return str(obj.price.amount)
        return None

    def get_currency(self, obj):
        if obj.price:
            return str(obj.price.currency)
        return None

    def get_available_stock(self, obj):
        if hasattr(obj, '_available_stock'):
            return obj._available_stock
        return 0

    def get_attributes(self, obj):
        return [
            {
                'id': av.id,
                'attribute_name': av.attribute.name,
                'value': av.value,
                'color_hex': av.color_hex,
            }
            for av in obj.selected_attributes.select_related('attribute').all()
        ]

    def get_image_url(self, obj):
        if obj.image_asset:
            return obj.image_asset.get_thumbnail('medium') or obj.image_asset.get_display_url()
        return None


class VariantCreateSerializer(serializers.Serializer):
    """Serializer for creating a variant."""
    name = serializers.CharField(max_length=100)
    sku = serializers.CharField(max_length=100)
    pricing_strategy = serializers.ChoiceField(
        choices=[('inherit', 'Inherit'), ('custom', 'Custom')], default='inherit'
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    currency = serializers.CharField(max_length=3, required=False, allow_blank=True)
    weight = serializers.DecimalField(
        max_digits=10, decimal_places=3, required=False, allow_null=True
    )
    barcode = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')
    is_active = serializers.BooleanField(default=True)
    attribute_value_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list
    )
    initial_stock = serializers.IntegerField(default=0, min_value=0)

    def validate_sku(self, value):
        if ProductVariant.objects.filter(sku=value).exists():
            raise serializers.ValidationError(_("A variant with this SKU already exists."))
        return value

    def validate_attribute_value_ids(self, value):
        if value:
            existing = set(AttributeValue.objects.filter(id__in=value).values_list('id', flat=True))
            missing = set(value) - existing
            if missing:
                raise serializers.ValidationError(
                    _("Attribute value IDs not found: %(ids)s") % {'ids': list(missing)}
                )
        return value


class VariantUpdateSerializer(serializers.Serializer):
    """Serializer for partial update of a variant."""
    name = serializers.CharField(max_length=100, required=False)
    sku = serializers.CharField(max_length=100, required=False)
    pricing_strategy = serializers.ChoiceField(
        choices=[('inherit', 'Inherit'), ('custom', 'Custom')], required=False
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    currency = serializers.CharField(max_length=3, required=False, allow_blank=True)
    weight = serializers.DecimalField(
        max_digits=10, decimal_places=3, required=False, allow_null=True
    )
    barcode = serializers.CharField(max_length=50, required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    attribute_value_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    def validate_sku(self, value):
        variant = self.context.get('variant')
        qs = ProductVariant.objects.filter(sku=value)
        if variant:
            qs = qs.exclude(id=variant.id)
        if qs.exists():
            raise serializers.ValidationError(_("A variant with this SKU already exists."))
        return value

    def validate_attribute_value_ids(self, value):
        if value:
            existing = set(AttributeValue.objects.filter(id__in=value).values_list('id', flat=True))
            missing = set(value) - existing
            if missing:
                raise serializers.ValidationError(
                    _("Attribute value IDs not found: %(ids)s") % {'ids': list(missing)}
                )
        return value
