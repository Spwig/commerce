"""
Design Layout Sync Serializer

Handles export/import of layout-related models:
- HeaderTemplate
- FooterTemplate
- Widget
- WidgetPlacement
- Menu (with MenuItem children)
"""

import logging

from django.db import transaction

from ..file_handler import export_file_field, import_file_field
from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

HEADER_FIELDS = [
    "name",
    "slug",
    "description",
    "layout_type",
    "is_sticky",
    "sticky_offset",
    "has_top_bar",
    "top_bar_content",
    "enable_notification_zone",
    "notification_zone_config",
    "zone_overrides",
    "zone_layouts",
    "zones",
    "mobile_layout",
    "mobile_menu_position",
    "custom_css",
    "css_classes",
    "is_active",
    "is_default",
    "is_preset",
    "preset_category",
    "source",
    "draft_data",
    "published_data",
    "has_unpublished_changes",
]

FOOTER_FIELDS = [
    "name",
    "slug",
    "description",
    "layout_type",
    "column_count",
    "zones",
    "has_bottom_bar",
    "bottom_bar_content",
    "custom_css",
    "css_classes",
    "background_color",
    "text_color",
    "is_active",
    "is_default",
    "is_preset",
    "preset_category",
    "source",
    "draft_data",
    "published_data",
    "has_unpublished_changes",
]

WIDGET_FIELDS = [
    "name",
    "widget_type",
    "config",
    "content",
    "translations",
    "show_on_mobile",
    "show_on_tablet",
    "show_on_desktop",
    "visibility_rules",
    "custom_css",
    "css_classes",
    "cache_duration",
    "is_active",
]

WIDGET_PLACEMENT_FIELDS = [
    "zone",
    "order",
    "override_config",
    "is_active",
]

MENU_FIELDS = [
    "name",
    "slug",
    "description",
    "location",
    "display_type",
    "custom_css",
    "css_classes",
    "global_style",
    "mobile_config",
    "translations",
    "is_active",
]

MENU_ITEM_FIELDS = [
    "item_type",
    "title",
    "url",
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


class DesignLayoutSerializer(CollectionSyncSerializer):
    """Serializer for layout components: headers, footers, widgets, and menus.

    Models handled:
        - HeaderTemplate: Header layout definitions
        - FooterTemplate: Footer layout definitions
        - Widget: Reusable widget definitions
        - WidgetPlacement: Widget placement configuration
        - Menu: Navigation menu structures
        - MenuItem: Individual menu items with hierarchy
    """

    category_key = "design_layout"
    natural_key_fields = ["name"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from design.models import Menu

        self.model_class = Menu

    def get_count(self):
        from design.models import (
            FooterTemplate,
            HeaderTemplate,
            Menu,
            Widget,
            WidgetPlacement,
        )

        return (
            HeaderTemplate.objects.count()
            + FooterTemplate.objects.count()
            + Widget.objects.count()
            + WidgetPlacement.objects.count()
            + Menu.objects.count()
        )

    def export(self, credential_mode="redact"):
        from design.models import (
            FooterTemplate,
            HeaderTemplate,
            Menu,
            Widget,
        )

        items = []
        files = {}

        # Headers
        for header in HeaderTemplate.objects.all():
            data = {f: getattr(header, f) for f in HEADER_FIELDS}
            data["_source_pk"] = header.pk
            data["_model"] = "HeaderTemplate"

            file_data = export_file_field(header, "preview_image")
            if file_data:
                key = f"HeaderTemplate:{header.slug}:preview_image"
                files[key] = file_data
                data["_preview_image_key"] = key

            # Include widget placements
            data["_placements"] = []
            for p in header.widget_placements.select_related("widget").all():
                pd = {f: getattr(p, f) for f in WIDGET_PLACEMENT_FIELDS}
                pd["_widget_name"] = p.widget.name if p.widget else None
                data["_placements"].append(pd)

            items.append(data)

        # Footers
        for footer in FooterTemplate.objects.all():
            data = {f: getattr(footer, f) for f in FOOTER_FIELDS}
            data["_source_pk"] = footer.pk
            data["_model"] = "FooterTemplate"

            file_data = export_file_field(footer, "preview_image")
            if file_data:
                key = f"FooterTemplate:{footer.slug}:preview_image"
                files[key] = file_data
                data["_preview_image_key"] = key

            data["_placements"] = []
            for p in footer.widget_placements.select_related("widget").all():
                pd = {f: getattr(p, f) for f in WIDGET_PLACEMENT_FIELDS}
                pd["_widget_name"] = p.widget.name if p.widget else None
                data["_placements"].append(pd)

            items.append(data)

        # Widgets (standalone, not placements)
        for widget in Widget.objects.all():
            data = {f: getattr(widget, f) for f in WIDGET_FIELDS}
            data["_source_pk"] = widget.pk
            data["_model"] = "Widget"
            items.append(data)

        # Menus with items
        for menu in Menu.objects.prefetch_related("items", "items__children").all():
            data = {f: getattr(menu, f) for f in MENU_FIELDS}
            data["_source_pk"] = menu.pk
            data["_model"] = "Menu"

            # Export items as flat list with parent references
            data["_items"] = []
            for item in menu.items.filter(parent__isnull=True).order_by("order"):
                self._export_menu_item(item, data["_items"])

            items.append(data)

        return {
            "category": self.category_key,
            "sync_type": "collection",
            "items": items,
            "total": len(items),
            "files": files,
        }

    def _export_menu_item(self, item, items_list, parent_title=None):
        data = {f: getattr(item, f) for f in MENU_ITEM_FIELDS}
        data["_parent_title"] = parent_title
        data["_page_slug"] = item.page_reference.slug if item.page_reference else None
        data["_category_slug"] = item.category_reference.slug if item.category_reference else None
        items_list.append(data)

        for child in item.children.all().order_by("order"):
            self._export_menu_item(child, items_list, parent_title=item.title)

    def import_data(self, data, dry_run=False, sync_mode="additive"):
        if dry_run:
            return self.generate_diff(data)

        items = data.get("items", [])
        files = data.get("files", {})
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        # Import order: Widgets -> Headers -> Footers -> Menus
        ordered = sorted(
            items,
            key=lambda x: {
                "Widget": 0,
                "HeaderTemplate": 1,
                "FooterTemplate": 2,
                "Menu": 3,
            }.get(x.get("_model", ""), 99),
        )

        for item in ordered:
            model_type = item.get("_model")
            try:
                with transaction.atomic():
                    if model_type == "Widget":
                        self._import_widget(item)
                    elif model_type == "HeaderTemplate":
                        self._import_header(item, files)
                    elif model_type == "FooterTemplate":
                        self._import_footer(item, files)
                    elif model_type == "Menu":
                        self._import_menu(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('name') or item.get('slug', 'Unknown')}: {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_widget(self, item):
        from design.models import Widget

        existing = Widget.objects.filter(name=item["name"], widget_type=item["widget_type"]).first()

        if existing:
            for f in WIDGET_FIELDS:
                if f in item:
                    setattr(existing, f, item[f])
            existing.save()
        else:
            widget = Widget()
            for f in WIDGET_FIELDS:
                if f in item:
                    setattr(widget, f, item[f])
            widget.save()

    def _import_header(self, item, files):
        from design.models import HeaderTemplate, Widget, WidgetPlacement

        existing = HeaderTemplate.objects.filter(slug=item["slug"]).first()

        if existing:
            header = existing
            for f in HEADER_FIELDS:
                if f in item:
                    setattr(header, f, item[f])
        else:
            header = HeaderTemplate()
            for f in HEADER_FIELDS:
                if f in item:
                    setattr(header, f, item[f])

        # Import preview image
        file_key = item.get("_preview_image_key")
        if file_key and file_key in files:
            import_file_field(header, "preview_image", files[file_key])

        header.save()

        # Import placements
        header.widget_placements.all().delete()
        for pd in item.get("_placements", []):
            widget_name = pd.get("_widget_name")
            if widget_name:
                widget = Widget.objects.filter(name=widget_name).first()
                if widget:
                    placement = WidgetPlacement(widget=widget, header=header)
                    for f in WIDGET_PLACEMENT_FIELDS:
                        if f in pd:
                            setattr(placement, f, pd[f])
                    placement.save()

    def _import_footer(self, item, files):
        from design.models import FooterTemplate, Widget, WidgetPlacement

        existing = FooterTemplate.objects.filter(slug=item["slug"]).first()

        if existing:
            footer = existing
            for f in FOOTER_FIELDS:
                if f in item:
                    setattr(footer, f, item[f])
        else:
            footer = FooterTemplate()
            for f in FOOTER_FIELDS:
                if f in item:
                    setattr(footer, f, item[f])

        file_key = item.get("_preview_image_key")
        if file_key and file_key in files:
            import_file_field(footer, "preview_image", files[file_key])

        footer.save()

        footer.widget_placements.all().delete()
        for pd in item.get("_placements", []):
            widget_name = pd.get("_widget_name")
            if widget_name:
                widget = Widget.objects.filter(name=widget_name).first()
                if widget:
                    placement = WidgetPlacement(widget=widget, footer=footer)
                    for f in WIDGET_PLACEMENT_FIELDS:
                        if f in pd:
                            setattr(placement, f, pd[f])
                    placement.save()

    def _import_menu(self, item):
        from design.models import Menu, MenuItem

        existing = Menu.objects.filter(slug=item["slug"]).first()

        if existing:
            menu = existing
            for f in MENU_FIELDS:
                if f in item:
                    setattr(menu, f, item[f])
            menu.save()
            menu.items.all().delete()
        else:
            menu = Menu()
            for f in MENU_FIELDS:
                if f in item:
                    setattr(menu, f, item[f])
            menu.save()

        # Import menu items preserving hierarchy
        item_map = {}  # title -> MenuItem instance
        for mi_data in item.get("_items", []):
            mi = MenuItem(menu=menu)
            for f in MENU_ITEM_FIELDS:
                if f in mi_data:
                    setattr(mi, f, mi_data[f])

            # Resolve parent
            parent_title = mi_data.get("_parent_title")
            if parent_title and parent_title in item_map:
                mi.parent = item_map[parent_title]

            # Resolve page reference
            page_slug = mi_data.get("_page_slug")
            if page_slug:
                try:
                    from page_builder.models import Page

                    mi.page_reference = Page.objects.filter(slug=page_slug).first()
                except Exception:
                    pass

            # Resolve category reference
            cat_slug = mi_data.get("_category_slug")
            if cat_slug:
                try:
                    from catalog.models import Category

                    mi.category_reference = Category.objects.filter(slug=cat_slug).first()
                except Exception:
                    pass

            mi.save()
            if mi.title:
                item_map[mi.title] = mi

    def _delete_absent(self, remote_items):
        from design.models import (
            FooterTemplate,
            HeaderTemplate,
            Menu,
            Widget,
        )

        remote_header_slugs = set()
        remote_footer_slugs = set()
        remote_widget_keys = set()
        remote_menu_slugs = set()

        for item in remote_items:
            m = item.get("_model")
            if m == "HeaderTemplate":
                remote_header_slugs.add(item.get("slug"))
            elif m == "FooterTemplate":
                remote_footer_slugs.add(item.get("slug"))
            elif m == "Widget":
                remote_widget_keys.add((item.get("name"), item.get("widget_type")))
            elif m == "Menu":
                remote_menu_slugs.add(item.get("slug"))

        deleted = 0
        for h in HeaderTemplate.objects.all():
            if h.slug not in remote_header_slugs:
                h.delete()
                deleted += 1
        for f in FooterTemplate.objects.all():
            if f.slug not in remote_footer_slugs:
                f.delete()
                deleted += 1
        for w in Widget.objects.all():
            if (w.name, w.widget_type) not in remote_widget_keys:
                w.delete()
                deleted += 1
        for m in Menu.objects.all():
            if m.slug not in remote_menu_slugs:
                m.delete()
                deleted += 1
        return deleted

    def generate_diff(self, remote_data):
        from design.models import FooterTemplate, HeaderTemplate, Menu, Widget

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")
            name = item.get("name") or item.get("slug", "Unknown")

            if model_type == "HeaderTemplate":
                existing = HeaderTemplate.objects.filter(slug=item.get("slug")).first()
                fields = HEADER_FIELDS
            elif model_type == "FooterTemplate":
                existing = FooterTemplate.objects.filter(slug=item.get("slug")).first()
                fields = FOOTER_FIELDS
            elif model_type == "Widget":
                existing = Widget.objects.filter(
                    name=item.get("name"), widget_type=item.get("widget_type")
                ).first()
                fields = WIDGET_FIELDS
            elif model_type == "Menu":
                existing = Menu.objects.filter(slug=item.get("slug")).first()
                fields = MENU_FIELDS
            else:
                continue

            if existing:
                field_changes = self._compute_field_diff(existing, item, fields)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": model_type,
                            "name": name,
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": model_type,
                        "name": name,
                        "fields": {k: v for k, v in item.items() if not k.startswith("_")},
                    }
                )

        adds = sum(1 for c in changes if c["type"] == "add")
        mods = sum(1 for c in changes if c["type"] == "modify")
        parts = []
        if adds:
            parts.append(f"{adds} addition(s)")
        if mods:
            parts.append(f"{mods} modification(s)")

        return {
            "changes": changes,
            "warnings": [],
            "summary": ", ".join(parts) if parts else "No changes",
        }

    def snapshot_current(self):
        return self.export(credential_mode="skip")

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {"restored": result.get("synced", 0), "errors": result.get("errors", [])}
        except Exception as e:
            return {"restored": 0, "errors": [str(e)]}
