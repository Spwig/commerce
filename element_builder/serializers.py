"""
Element Builder Serializers

DRF serializers for custom element API endpoints.
Uses page_builder Element model for element tree structure.
"""
from rest_framework import serializers

from .models import CustomElement, ElementBinding
from .registry import BINDABLE_MODELS


class ElementBindingSerializer(serializers.ModelSerializer):
    """Serializer for element data bindings."""

    class Meta:
        model = ElementBinding
        fields = [
            'id', 'element', 'content_field', 'model_field', 'thumbnail_preset'
        ]


class ElementTreeSerializer(serializers.Serializer):
    """
    Recursive serializer for page_builder Element tree.
    Represents the element tree structure for the visual builder.
    """
    id = serializers.IntegerField(read_only=True)
    element_type = serializers.CharField()
    content = serializers.JSONField()
    order = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField(default=True)
    children = serializers.SerializerMethodField()
    binding = serializers.SerializerMethodField()

    def get_children(self, obj):
        """Recursively serialize child elements."""
        children = obj.child_elements.filter(is_active=True).order_by('order')
        return ElementTreeSerializer(children, many=True, context=self.context).data

    def get_binding(self, obj):
        """Get binding for this element if exists."""
        custom_element = self.context.get('custom_element')
        if not custom_element:
            return None
        try:
            binding = custom_element.bindings.get(element=obj)
            return {
                'content_field': binding.content_field,
                'model_field': binding.model_field,
                'thumbnail_preset': binding.thumbnail_preset,
            }
        except ElementBinding.DoesNotExist:
            return None


class CustomElementListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    target_model_label = serializers.SerializerMethodField()
    has_root_element = serializers.SerializerMethodField()

    class Meta:
        model = CustomElement
        fields = [
            'id', 'name', 'slug', 'description', 'target_model',
            'target_model_label', 'icon', 'is_active', 'has_root_element', 'updated_at'
        ]

    def get_target_model_label(self, obj):
        """Get human-readable label for the target model."""
        if not obj.target_model:
            return 'None (Static Element)'
        model_config = BINDABLE_MODELS.get(obj.target_model, {})
        return str(model_config.get('label', obj.target_model))

    def get_has_root_element(self, obj):
        """Check if element has a root element tree."""
        return obj.root_element_id is not None


class CustomElementDetailSerializer(serializers.ModelSerializer):
    """Full serializer including element tree for builder."""
    target_model_label = serializers.SerializerMethodField()
    element_tree = serializers.SerializerMethodField()
    bindings = ElementBindingSerializer(many=True, read_only=True)

    class Meta:
        model = CustomElement
        fields = [
            'id', 'name', 'slug', 'description', 'target_model',
            'target_model_label', 'icon', 'category',
            'is_active', 'root_element', 'element_tree', 'bindings',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'root_element']

    def get_target_model_label(self, obj):
        """Get human-readable label for the target model."""
        if not obj.target_model:
            return 'None (Static Element)'
        model_config = BINDABLE_MODELS.get(obj.target_model, {})
        return str(model_config.get('label', obj.target_model))

    def get_element_tree(self, obj):
        """Serialize the element tree starting from root_element."""
        if not obj.root_element:
            return None
        context = {'custom_element': obj}
        return ElementTreeSerializer(obj.root_element, context=context).data

    def validate_target_model(self, value):
        """Validate that the target model is a valid bindable model or empty (static element)."""
        # Allow empty string for static elements with no model binding
        if value == '' or value is None:
            return value
        if value not in BINDABLE_MODELS:
            raise serializers.ValidationError(
                f"Invalid target model. Must be one of: {', '.join(BINDABLE_MODELS.keys())}"
            )
        return value


class ElementCreateSerializer(serializers.Serializer):
    """Serializer for creating a new Element in the tree."""
    element_type = serializers.CharField()
    content = serializers.JSONField(default=dict)
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    order = serializers.IntegerField(default=0)


class BindingCreateSerializer(serializers.Serializer):
    """Serializer for creating/updating element bindings."""
    element_id = serializers.IntegerField()
    content_field = serializers.CharField()
    model_field = serializers.CharField()
    thumbnail_preset = serializers.CharField(required=False, allow_blank=True, default='')


class BindableModelFieldSerializer(serializers.Serializer):
    """Serializer for bindable model field configuration."""
    type = serializers.CharField()  # 'text', 'image', or 'url'
    label = serializers.CharField()
    fk_to = serializers.CharField(required=False, allow_null=True)
    computed = serializers.BooleanField(required=False, default=False)
    description = serializers.CharField(required=False, allow_null=True)
    group = serializers.CharField(required=False, allow_null=True)  # For UI grouping


class BindableModelSerializer(serializers.Serializer):
    """Serializer for bindable model configuration."""
    label = serializers.CharField()
    icon = serializers.CharField(required=False)
    fields = serializers.DictField(child=BindableModelFieldSerializer())


class ThumbnailPresetSerializer(serializers.Serializer):
    """Serializer for thumbnail size preset."""
    slug = serializers.CharField()
    name = serializers.CharField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
