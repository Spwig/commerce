"""
Serializers for menu builder API
"""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .header_footer_models import Menu, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer for menu items with resolved values"""

    resolved_url = serializers.SerializerMethodField()
    resolved_title = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    category_tree_items = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "menu",
            "parent",
            "item_type",
            "title",
            "url",
            "resolved_url",
            "resolved_title",
            "page_reference",
            "category_reference",
            "target",
            "icon",
            "badge_text",
            "badge_color",
            "style_config",
            "widget_config",
            "tree_config",
            "mega_menu_content",
            "visibility_rules",
            "translations",
            "order",
            "is_active",
            "css_classes",
            "has_children",
            "children",
            "category_tree_items",
        ]
        read_only_fields = [
            "resolved_url",
            "resolved_title",
            "has_children",
            "children",
            "category_tree_items",
        ]

    def get_resolved_url(self, obj):
        return obj.get_resolved_url()

    def get_resolved_title(self, obj):
        return obj.get_resolved_title()

    def get_has_children(self, obj):
        return obj.has_children()

    def get_children(self, obj):
        """Get nested children for tree display"""
        children = obj.children.filter(is_active=True).order_by("order")
        return MenuItemSerializer(children, many=True).data

    def get_category_tree_items(self, obj):
        """Get dynamic category tree for category_tree type items"""
        if obj.item_type == "category_tree":
            return obj.get_category_tree_items()
        return []


class MenuItemCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating menu items"""

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "menu",
            "parent",
            "item_type",
            "title",
            "url",
            "page_reference",
            "category_reference",
            "target",
            "icon",
            "badge_text",
            "badge_color",
            "style_config",
            "widget_config",
            "tree_config",
            "mega_menu_content",
            "visibility_rules",
            "translations",
            "order",
            "is_active",
            "css_classes",
        ]

    def validate(self, data):
        """Validate item data based on item_type"""
        item_type = data.get("item_type", "link")

        # Validate page reference for page type
        if item_type == "page" and not data.get("page_reference"):
            # Allow empty page_reference, will use URL fallback
            pass

        # Validate category reference for category type
        if item_type == "category" and not data.get("category_reference"):
            # Allow empty category_reference, will use URL fallback
            pass

        return data


class MenuListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for menu list views"""

    item_count = serializers.SerializerMethodField()
    location_display = serializers.SerializerMethodField()
    display_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "location",
            "location_display",
            "display_type",
            "display_type_display",
            "is_active",
            "item_count",
            "created_at",
            "updated_at",
        ]

    def get_item_count(self, obj):
        # Prefer the annotated count (set by the list queryset) to avoid an
        # extra COUNT query per menu; fall back for un-annotated instances
        # (e.g. the object returned straight after a create).
        annotated = getattr(obj, "active_item_count", None)
        if annotated is not None:
            return annotated
        return obj.items.filter(is_active=True).count()

    def get_location_display(self, obj):
        return obj.get_location_display()

    def get_display_type_display(self, obj):
        return obj.get_display_type_display()


class MenuDetailSerializer(serializers.ModelSerializer):
    """Full serializer for menu with nested items tree"""

    items_tree = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    location_display = serializers.SerializerMethodField()
    display_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "location",
            "location_display",
            "display_type",
            "display_type_display",
            "custom_css",
            "css_classes",
            "global_style",
            "mobile_config",
            "translations",
            "is_active",
            "item_count",
            "items_tree",
            "created_at",
            "updated_at",
        ]

    def get_items_tree(self, obj):
        """Get menu items as nested tree"""
        return obj.get_all_items_tree()

    def get_item_count(self, obj):
        return obj.items.filter(is_active=True).count()

    def get_location_display(self, obj):
        return obj.get_location_display()

    def get_display_type_display(self, obj):
        return obj.get_display_type_display()


class MenuItemReorderItemSerializer(serializers.Serializer):
    """Serializer for individual item in reorder request"""

    id = serializers.IntegerField()
    order = serializers.IntegerField()
    parent_id = serializers.IntegerField(required=False, allow_null=True)


class MenuReorderSerializer(serializers.Serializer):
    """Serializer for batch reorder request"""

    items = MenuItemReorderItemSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Items list cannot be empty")
        return value


class MenuStructureMenuSerializer(serializers.Serializer):
    """Validate the editable menu-level properties of a save-structure request."""

    name = serializers.CharField(required=False)
    display_type = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    custom_css = serializers.CharField(required=False, allow_blank=True)
    css_classes = serializers.CharField(required=False, allow_blank=True)
    global_style = serializers.JSONField(required=False)
    mobile_config = serializers.JSONField(required=False)


class MenuStructureItemSerializer(serializers.Serializer):
    """Validate a single (recursive) node of a save-structure request.

    Guards the write loop against malformed payloads: null items, wrong field
    types, unknown ``item_type`` values, non-existent page/category references,
    and children that are not a list of valid items.
    """

    id = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(required=False, allow_blank=True, default="")
    item_type = serializers.ChoiceField(
        choices=MenuItem.ITEM_TYPE_CHOICES, required=False, default="link"
    )
    url = serializers.CharField(required=False, allow_blank=True, default="")
    target = serializers.CharField(required=False, allow_blank=True, default="_self")
    icon = serializers.CharField(required=False, allow_blank=True, default="")
    badge_text = serializers.CharField(required=False, allow_blank=True, default="")
    badge_color = serializers.CharField(required=False, allow_blank=True, default="")
    css_classes = serializers.CharField(required=False, allow_blank=True, default="")
    is_active = serializers.BooleanField(required=False, default=True)
    page_reference_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    category_reference_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    style_config = serializers.JSONField(required=False, default=dict)
    widget_config = serializers.JSONField(required=False, default=dict)
    tree_config = serializers.JSONField(required=False, default=dict)
    visibility_rules = serializers.JSONField(required=False, default=list)

    def get_fields(self):
        fields = super().get_fields()
        # Recursive children: each child is validated as a full item structure.
        fields["children"] = MenuStructureItemSerializer(many=True, required=False, default=list)
        return fields

    def validate_page_reference_id(self, value):
        if value is not None:
            from page_builder.models import Page

            if not Page.objects.filter(pk=value).exists():
                raise serializers.ValidationError(_("Referenced page does not exist."))
        return value

    def validate_category_reference_id(self, value):
        if value is not None:
            from catalog.models import Category

            if not Category.objects.filter(pk=value).exists():
                raise serializers.ValidationError(_("Referenced category does not exist."))
        return value


class MenuStructureSerializer(serializers.Serializer):
    """Validate a complete menu-structure save request before any DB writes."""

    menu = MenuStructureMenuSerializer(required=False)
    items = MenuStructureItemSerializer(many=True, required=False, default=list)


class MenuTokensSerializer(serializers.Serializer):
    """Validate the design-token payload before it is written to ThemeBranding.

    ``tokens`` must be an object mapping token names to flat values (or a
    responsive object); a non-object body would later crash CSS generation
    when it calls ``value.items()``.
    """

    tokens = serializers.DictField(required=False, default=dict)

    def validate_tokens(self, value):
        for token_name, token_value in value.items():
            if not isinstance(token_name, str):
                raise serializers.ValidationError(_("Token names must be strings."))
            if not isinstance(token_value, (str, int, float, dict)):
                raise serializers.ValidationError(
                    _("Token '%(name)s' must be a string, number, or object.")
                    % {"name": token_name}
                )
        return value
