"""
Attribute Serializers for Admin API

Serializers for product attribute management.
"""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from catalog.models import ProductAttribute, AttributeValue


class AdminAttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for attribute values."""
    class Meta:
        model = AttributeValue
        fields = ['id', 'value', 'slug', 'color_hex', 'sort_order']


class AdminAttributeListSerializer(serializers.ModelSerializer):
    """Serializer for attribute list with values."""
    values = AdminAttributeValueSerializer(many=True, read_only=True)
    value_count = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'slug', 'type', 'is_required', 'sort_order', 'values', 'value_count']

    def get_value_count(self, obj):
        return obj.values.count()


class AttributeValueInputSerializer(serializers.Serializer):
    """Serializer for a single attribute value in creation payload."""
    value = serializers.CharField(max_length=100)
    color_hex = serializers.CharField(max_length=7, required=False, allow_blank=True, default='')
    sort_order = serializers.IntegerField(default=0, min_value=0)


class AttributeCreateSerializer(serializers.Serializer):
    """Serializer for creating an attribute with optional values."""
    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(
        choices=[('select', 'Select'), ('color', 'Color'), ('button', 'Button'), ('radio', 'Radio')],
        default='select'
    )
    is_required = serializers.BooleanField(default=True)
    sort_order = serializers.IntegerField(default=0, min_value=0)
    values = AttributeValueInputSerializer(many=True, required=False, default=list)

    def validate_name(self, value):
        if ProductAttribute.objects.filter(name=value).exists():
            raise serializers.ValidationError(_("An attribute with this name already exists."))
        return value


class ProductAttributeAssignSerializer(serializers.Serializer):
    """Serializer for assigning attributes and their allowed values to a product."""
    assignments = serializers.ListField(child=serializers.DictField())

    def validate_assignments(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(_("At least one assignment is required."))
        for item in value:
            if 'attribute_id' not in item:
                raise serializers.ValidationError(
                    _("Each assignment must have an 'attribute_id' field.")
                )
            if 'value_ids' not in item:
                raise serializers.ValidationError(
                    _("Each assignment must have a 'value_ids' field.")
                )
        return value
