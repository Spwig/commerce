from django.contrib import admin

from .models import GeometryAsset, NodeMapping, SceneConfig, TextureAsset


class NodeMappingInline(admin.TabularInline):
    model = NodeMapping
    extra = 0
    fields = ("slot_option", "action_type", "target_node", "action_data", "sort_order")


class GeometryAssetInline(admin.TabularInline):
    model = GeometryAsset
    extra = 0
    fields = ("label", "media_asset", "target_node", "node_data")


class TextureAssetInline(admin.TabularInline):
    model = TextureAsset
    extra = 0
    fields = ("label", "media_asset", "texture_type")


@admin.register(SceneConfig)
class SceneConfigAdmin(admin.ModelAdmin):
    list_display = ("product", "is_enabled", "updated_at")
    list_filter = ("is_enabled",)
    inlines = [NodeMappingInline, GeometryAssetInline, TextureAssetInline]
    readonly_fields = ("node_tree", "created_at", "updated_at")
