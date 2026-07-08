"""
DRF serializers for custom fields.

CustomFieldsSerializerMixin - add to any model serializer to include custom fields
"""
from rest_framework import serializers

from .models import CustomFieldDefinition, CustomFieldGroup
from .validators import validate_custom_field_value


class CustomFieldGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFieldGroup
        fields = ['id', 'name', 'slug', 'sort_order', 'show_on_storefront']


class CustomFieldDefinitionSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    field_type_display = serializers.CharField(source='get_field_type_display', read_only=True)
    choices = serializers.SerializerMethodField()

    class Meta:
        model = CustomFieldDefinition
        fields = [
            'id', 'name', 'slug', 'field_type', 'field_type_display',
            'help_text_value', 'default_value', 'validation_config',
            'is_required', 'show_on_storefront', 'is_translatable',
            'sort_order', 'group_name',
            'choices',
        ]

    def get_choices(self, obj):
        return obj.get_choices()


class CustomFieldsSerializerMixin:
    """
    DRF serializer mixin to include custom_fields in model serialization.

    Usage:
        class ProductSerializer(CustomFieldsSerializerMixin, serializers.ModelSerializer):
            class Meta:
                model = Product
                fields = [..., 'custom_fields']

    Custom fields are included as a flat dict: {"field_slug": value, ...}
    """

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(instance, 'custom_fields') and 'custom_fields' not in data:
            data['custom_fields'] = instance.custom_fields or {}
        return data

    def validate_custom_fields(self, value):
        """Validate custom field values against definitions."""
        if not value:
            return value

        model = self.Meta.model
        definitions = CustomFieldDefinition.get_cached_for_model(model)
        errors = {}

        for field_def in definitions:
            if field_def.slug in value:
                try:
                    value[field_def.slug] = validate_custom_field_value(
                        field_def, value[field_def.slug]
                    )
                except Exception as e:
                    errors[field_def.slug] = str(e)

        if errors:
            raise serializers.ValidationError(errors)

        return value
