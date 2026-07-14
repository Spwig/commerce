"""
Page Content Sync Serializer

Handles export/import of page-related models:
- Page (with Element children)
- PageTemplate
- ElementTemplate
"""

import logging

from django.db import transaction

from ..file_handler import export_file_field, import_file_field
from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

PAGE_FIELDS = [
    "title",
    "slug",
    "page_type",
    "status",
    "meta_title",
    "meta_description",
    "meta_keywords",
    "seo_auto_generated",
    "translations",
    "is_default_for_type",
    "is_system_page",
    "requires_auth",
    "cache_timeout",
    "hide_header",
    "hide_footer",
    "page_design_config",
    "template_variant",
    "css_classes",
    "layout_config",
    "style_overrides",
    "responsive_config",
    "inherit_parent_theme",
]

ELEMENT_FIELDS = [
    "element_type",
    "name",
    "content",
    "translations",
    "order",
    "column_span",
    "column_offset",
    "text_align",
    "vertical_align",
    "is_active",
    "show_on_mobile",
    "show_on_tablet",
    "show_on_desktop",
    "link_url",
    "link_target",
    "template_variant",
    "css_classes",
    "layout_config",
    "style_overrides",
    "responsive_config",
    "inherit_parent_theme",
]

PAGE_TEMPLATE_FIELDS = [
    "name",
    "description",
    "page_type",
    "template_data",
    "version",
    "category",
    "is_premium",
    "is_public",
]

ELEMENT_TEMPLATE_FIELDS = [
    "name",
    "description",
    "element_type",
    "template_data",
    "category",
    "tags",
    "is_public",
]


class PageContentSerializer(CollectionSyncSerializer):
    """Serializer for pages, page templates, and element templates.

    Models handled:
        - Page: CMS pages with nested Element children
        - PageTemplate: Reusable page layout templates
        - ElementTemplate: Reusable element templates
    """

    category_key = "page_content"
    natural_key_fields = ["slug"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from page_builder.models import Page

        self.model_class = Page

    def get_count(self):
        from page_builder.models import ElementTemplate, Page, PageTemplate

        return Page.objects.count() + PageTemplate.objects.count() + ElementTemplate.objects.count()

    def export(self, credential_mode="redact"):
        from page_builder.models import Element, ElementTemplate, Page, PageTemplate

        items = []
        files = {}

        # Pages with elements
        for page in Page.objects.select_related(
            "theme", "header_template", "footer_template"
        ).all():
            data = {f: getattr(page, f) for f in PAGE_FIELDS}
            data["_source_pk"] = page.pk
            data["_model"] = "Page"

            # Cross-category refs stored as slugs
            data["_theme_slug"] = page.theme.slug if page.theme else None
            data["_header_slug"] = page.header_template.slug if page.header_template else None
            data["_footer_slug"] = page.footer_template.slug if page.footer_template else None

            # Export elements as nested tree
            data["_elements"] = []
            root_elements = Element.objects.filter(page=page, parent_element__isnull=True).order_by(
                "order"
            )
            for elem in root_elements:
                self._export_element(elem, data["_elements"])

            # Datetime
            if page.published_at:
                data["_published_at"] = page.published_at.isoformat()

            items.append(data)

        # Page templates
        for pt in PageTemplate.objects.all():
            data = {f: getattr(pt, f) for f in PAGE_TEMPLATE_FIELDS}
            data["_source_pk"] = pt.pk
            data["_model"] = "PageTemplate"

            file_data = export_file_field(pt, "preview_image")
            if file_data:
                key = f"PageTemplate:{pt.name}:preview_image"
                files[key] = file_data
                data["_preview_image_key"] = key

            items.append(data)

        # Element templates
        for et in ElementTemplate.objects.all():
            data = {f: getattr(et, f) for f in ELEMENT_TEMPLATE_FIELDS}
            data["_source_pk"] = et.pk
            data["_model"] = "ElementTemplate"

            file_data = export_file_field(et, "preview_image")
            if file_data:
                key = f"ElementTemplate:{et.name}:preview_image"
                files[key] = file_data
                data["_preview_image_key"] = key

            items.append(data)

        return {
            "category": self.category_key,
            "sync_type": "collection",
            "items": items,
            "total": len(items),
            "files": files,
        }

    def _export_element(self, elem, elements_list, parent_name=None):
        data = {f: getattr(elem, f) for f in ELEMENT_FIELDS}
        data["_parent_name"] = parent_name
        elements_list.append(data)

        for child in elem.child_elements.all().order_by("order"):
            self._export_element(child, elements_list, parent_name=elem.name)

    def import_data(self, data, dry_run=False, sync_mode="additive"):
        if dry_run:
            return self.generate_diff(data)

        items = data.get("items", [])
        files = data.get("files", {})
        synced = 0
        skipped = 0
        failed = 0
        errors = []

        # Import order: PageTemplate, ElementTemplate, then Pages
        ordered = sorted(
            items,
            key=lambda x: {
                "PageTemplate": 0,
                "ElementTemplate": 1,
                "Page": 2,
            }.get(x.get("_model", ""), 99),
        )

        for item in ordered:
            model_type = item.get("_model")
            try:
                with transaction.atomic():
                    if model_type == "PageTemplate":
                        self._import_page_template(item, files)
                    elif model_type == "ElementTemplate":
                        self._import_element_template(item, files)
                    elif model_type == "Page":
                        self._import_page(item)
                    else:
                        skipped += 1
                        continue
                    synced += 1
            except Exception as e:
                failed += 1
                errors.append(f"{item.get('name') or item.get('title', 'Unknown')}: {e}")

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}

        if sync_mode == "mirror":
            deleted = self._delete_absent(items)
            result["deleted"] = deleted

        return result

    def _import_page_template(self, item, files):
        from page_builder.models import PageTemplate

        existing = PageTemplate.objects.filter(name=item["name"]).first()

        if existing:
            pt = existing
            for f in PAGE_TEMPLATE_FIELDS:
                if f in item:
                    setattr(pt, f, item[f])
        else:
            pt = PageTemplate()
            for f in PAGE_TEMPLATE_FIELDS:
                if f in item:
                    setattr(pt, f, item[f])

        file_key = item.get("_preview_image_key")
        if file_key and file_key in files:
            import_file_field(pt, "preview_image", files[file_key])

        pt.save()

    def _import_element_template(self, item, files):
        from page_builder.models import ElementTemplate

        existing = ElementTemplate.objects.filter(name=item["name"]).first()

        if existing:
            et = existing
            for f in ELEMENT_TEMPLATE_FIELDS:
                if f in item:
                    setattr(et, f, item[f])
        else:
            et = ElementTemplate()
            for f in ELEMENT_TEMPLATE_FIELDS:
                if f in item:
                    setattr(et, f, item[f])

        file_key = item.get("_preview_image_key")
        if file_key and file_key in files:
            import_file_field(et, "preview_image", files[file_key])

        et.save()

    def _import_page(self, item):
        from page_builder.models import Element, Page

        existing = Page.objects.filter(slug=item["slug"]).first()

        if existing:
            page = existing
            for f in PAGE_FIELDS:
                if f in item:
                    setattr(page, f, item[f])
        else:
            page = Page()
            for f in PAGE_FIELDS:
                if f in item:
                    setattr(page, f, item[f])

        # Resolve cross-category refs
        theme_slug = item.get("_theme_slug")
        if theme_slug:
            try:
                from design.models import Theme

                page.theme = Theme.objects.filter(slug=theme_slug).first()
            except Exception:
                pass

        header_slug = item.get("_header_slug")
        if header_slug:
            try:
                from design.models import HeaderTemplate

                page.header_template = HeaderTemplate.objects.filter(slug=header_slug).first()
            except Exception:
                pass

        footer_slug = item.get("_footer_slug")
        if footer_slug:
            try:
                from design.models import FooterTemplate

                page.footer_template = FooterTemplate.objects.filter(slug=footer_slug).first()
            except Exception:
                pass

        page.save()

        # Clear and re-import elements
        Element.objects.filter(page=page).delete()

        elem_map = {}  # name -> Element instance
        for elem_data in item.get("_elements", []):
            elem = Element(page=page)
            for f in ELEMENT_FIELDS:
                if f in elem_data:
                    setattr(elem, f, elem_data[f])

            parent_name = elem_data.get("_parent_name")
            if parent_name and parent_name in elem_map:
                elem.parent_element = elem_map[parent_name]

            elem.save()
            if elem.name:
                elem_map[elem.name] = elem

    def _delete_absent(self, remote_items):
        from page_builder.models import ElementTemplate, Page, PageTemplate

        remote_page_slugs = set()
        remote_pt_names = set()
        remote_et_names = set()
        for item in remote_items:
            m = item.get("_model")
            if m == "Page":
                remote_page_slugs.add(item.get("slug"))
            elif m == "PageTemplate":
                remote_pt_names.add(item.get("name"))
            elif m == "ElementTemplate":
                remote_et_names.add(item.get("name"))

        deleted = 0
        for page in Page.objects.all():
            if page.slug not in remote_page_slugs:
                page.delete()
                deleted += 1
        for pt in PageTemplate.objects.all():
            if pt.name not in remote_pt_names:
                pt.delete()
                deleted += 1
        for et in ElementTemplate.objects.all():
            if et.name not in remote_et_names:
                et.delete()
                deleted += 1
        return deleted

    def generate_diff(self, remote_data):
        from page_builder.models import ElementTemplate, Page, PageTemplate

        items = remote_data.get("items", [])
        changes = []

        for item in items:
            model_type = item.get("_model")
            name = item.get("name") or item.get("title") or item.get("slug", "Unknown")

            if model_type == "Page":
                existing = Page.objects.filter(slug=item.get("slug")).first()
                fields = PAGE_FIELDS
            elif model_type == "PageTemplate":
                existing = PageTemplate.objects.filter(name=item.get("name")).first()
                fields = PAGE_TEMPLATE_FIELDS
            elif model_type == "ElementTemplate":
                existing = ElementTemplate.objects.filter(name=item.get("name")).first()
                fields = ELEMENT_TEMPLATE_FIELDS
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
