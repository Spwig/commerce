"""
Serializers for Header/Footer Builder API
DRF-compliant serializers for all builder endpoints
"""

from rest_framework import serializers
from .header_footer_models import (
    HeaderTemplate, FooterTemplate, Widget,
    WidgetPlacement, Menu
)


# ============================================================
# Widget Serializers
# ============================================================

class WidgetPlacementSerializer(serializers.Serializer):
    """Serializer for widget placement data in builder responses"""
    id = serializers.IntegerField(read_only=True)
    widget_id = serializers.IntegerField(source='widget.id', read_only=True)
    widget_name = serializers.CharField(source='widget.name', read_only=True)
    widget_type = serializers.CharField(source='widget.widget_type', read_only=True)
    order = serializers.IntegerField()
    config = serializers.SerializerMethodField()

    def get_config(self, obj):
        """Merge widget base config with placement overrides"""
        return {**obj.widget.config, **obj.override_config}


class WidgetPlacementCreateSerializer(serializers.Serializer):
    """Serializer for creating widget placements"""
    widget_id = serializers.IntegerField(required=True)
    zone = serializers.CharField(required=True)
    order = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField(default=True)
    header_id = serializers.IntegerField(required=False, allow_null=True)
    footer_id = serializers.IntegerField(required=False, allow_null=True)
    override_config = serializers.JSONField(required=False, default=dict)

    def validate(self, data):
        """Ensure either header_id or footer_id is provided"""
        if not data.get('header_id') and not data.get('footer_id'):
            raise serializers.ValidationError(
                "Must specify either header_id or footer_id"
            )
        if data.get('header_id') and data.get('footer_id'):
            raise serializers.ValidationError(
                "Cannot specify both header_id and footer_id"
            )
        return data


class WidgetPlacementUpdateSerializer(serializers.Serializer):
    """Serializer for updating widget placements"""
    zone = serializers.CharField(required=False)
    order = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)
    override_config = serializers.JSONField(required=False)


class ReorderPlacementItemSerializer(serializers.Serializer):
    """Serializer for a single placement reorder item"""
    id = serializers.IntegerField()
    order = serializers.IntegerField()


class ReorderPlacementsSerializer(serializers.Serializer):
    """Serializer for reordering multiple placements"""
    placements = ReorderPlacementItemSerializer(many=True)


# ============================================================
# Header Serializers
# ============================================================

class HeaderBuilderResponseSerializer(serializers.Serializer):
    """Serializer for header builder GET response"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    layout_type = serializers.CharField()
    is_sticky = serializers.BooleanField()
    has_top_bar = serializers.BooleanField()
    mobile_layout = serializers.CharField()
    zones = serializers.DictField()
    zone_overrides = serializers.JSONField()
    zone_layouts = serializers.JSONField()


class HeaderBuilderUpdateSerializer(serializers.Serializer):
    """Serializer for updating header template"""
    name = serializers.CharField(required=False)
    layout_type = serializers.CharField(required=False)
    is_sticky = serializers.BooleanField(required=False)
    has_top_bar = serializers.BooleanField(required=False)
    mobile_layout = serializers.CharField(required=False)


class HeaderDuplicateSerializer(serializers.Serializer):
    """Serializer for duplicating a header"""
    name = serializers.CharField(required=False, default="Copy of Preset")


class HeaderDuplicateResponseSerializer(serializers.Serializer):
    """Response serializer for header duplication"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    message = serializers.CharField(required=False)


# ============================================================
# Footer Serializers
# ============================================================

class FooterBuilderResponseSerializer(serializers.Serializer):
    """Serializer for footer builder GET response"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    layout_type = serializers.CharField()
    column_count = serializers.IntegerField()
    has_bottom_bar = serializers.BooleanField()
    background_color = serializers.CharField(allow_null=True, allow_blank=True)
    text_color = serializers.CharField(allow_null=True, allow_blank=True)
    zones = serializers.DictField()
    zone_overrides = serializers.JSONField()
    zone_layouts = serializers.JSONField()


class FooterBuilderUpdateSerializer(serializers.Serializer):
    """Serializer for updating footer template"""
    name = serializers.CharField(required=False)
    layout_type = serializers.CharField(required=False)
    column_count = serializers.IntegerField(required=False)
    has_bottom_bar = serializers.BooleanField(required=False)
    background_color = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    text_color = serializers.CharField(required=False, allow_null=True, allow_blank=True)


# ============================================================
# Widget Library Serializers
# ============================================================

class WidgetLibraryItemSerializer(serializers.Serializer):
    """Serializer for a single widget in the library"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField(source='widget_type')
    type_display = serializers.CharField(source='get_widget_type_display')
    config = serializers.JSONField()
    show_on_mobile = serializers.BooleanField()
    show_on_tablet = serializers.BooleanField()
    show_on_desktop = serializers.BooleanField()


class WidgetLibraryResponseSerializer(serializers.Serializer):
    """Response serializer for widget library"""
    widgets = serializers.DictField(
        child=WidgetLibraryItemSerializer(many=True)
    )


# ============================================================
# Preset Serializers
# ============================================================

class HeaderPresetSerializer(serializers.ModelSerializer):
    """Serializer for header presets"""
    preview_image = serializers.SerializerMethodField()
    category = serializers.CharField(source='preset_category')

    class Meta:
        model = HeaderTemplate
        fields = ['id', 'name', 'description', 'layout_type', 'category', 'preview_image']

    def get_preview_image(self, obj):
        return obj.preview_image.url if obj.preview_image else None


class FooterPresetSerializer(serializers.ModelSerializer):
    """Serializer for footer presets"""
    preview_image = serializers.SerializerMethodField()
    category = serializers.CharField(source='preset_category')

    class Meta:
        model = FooterTemplate
        fields = ['id', 'name', 'description', 'layout_type', 'column_count', 'category', 'preview_image']

    def get_preview_image(self, obj):
        return obj.preview_image.url if obj.preview_image else None


class ClonePresetSerializer(serializers.Serializer):
    """Serializer for cloning a preset"""
    name = serializers.CharField(required=False, default="Copy of Preset")


class ClonePresetResponseSerializer(serializers.Serializer):
    """Response serializer for preset cloning"""
    id = serializers.IntegerField()
    name = serializers.CharField()


# ============================================================
# Menu Serializers
# ============================================================

class MenuListSerializer(serializers.ModelSerializer):
    """Serializer for menu list"""
    class Meta:
        model = Menu
        fields = ['id', 'name', 'display_type']


# ============================================================
# Widget Schemas Serializer
# ============================================================

class WidgetSchemaFieldSerializer(serializers.Serializer):
    """Serializer for a single schema field"""
    key = serializers.CharField()
    label = serializers.CharField()
    type = serializers.CharField()
    placeholder = serializers.CharField(required=False, allow_blank=True)
    help = serializers.CharField(required=False, allow_blank=True)
    default = serializers.JSONField(required=False)
    options = serializers.ListField(required=False)


class WidgetSchemaGroupSerializer(serializers.Serializer):
    """Serializer for a schema field group"""
    id = serializers.CharField()
    title = serializers.CharField()
    expanded = serializers.BooleanField(default=True)
    singleColumn = serializers.BooleanField(required=False, default=False)
    fields = WidgetSchemaFieldSerializer(many=True)


class WidgetSchemaSerializer(serializers.Serializer):
    """Serializer for a single widget schema"""
    type = serializers.CharField()
    icon = serializers.CharField()
    label = serializers.CharField()
    groups = WidgetSchemaGroupSerializer(many=True)


class WidgetSchemasResponseSerializer(serializers.Serializer):
    """Response serializer for widget schemas endpoint"""
    schemas = serializers.DictField(
        child=WidgetSchemaSerializer()
    )


# ============================================================
# Common Response Serializers
# ============================================================

class SuccessResponseSerializer(serializers.Serializer):
    """Generic success response"""
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    """Generic error response"""
    error = serializers.CharField()
    details = serializers.CharField(required=False)
