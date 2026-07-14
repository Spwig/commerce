"""
Design Theme Sync Serializer

Handles export/import of theme-related models:
- Theme: Theme definitions, package files, compiled CSS
- GlobalDesignSettings: Global design configuration singleton
- DesignToken: Brand builder token overrides (priority 1 only)
- CustomCSS: Custom CSS snippets
- ThemeBranding: Per-theme brand customizations

Includes file handling for theme packages (ZIP) and logo/favicon images.
Content type FKs (active_theme, theme) are serialized as slug references
for portability between instances.
"""

import logging

from django.db import transaction

from ..file_handler import export_file_field, import_file_field
from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

THEME_FIELDS = [
    "name",
    "slug",
    "description",
    "version",
    "engine_min_version",
    "engine_max_version",
    "author",
    "author_email",
    "author_website",
    "license",
    "manifest",
    "feature_flags",
    "token_migrations",
    "compiled_css",
    "css_hash",
    "preview_images",
    "is_active",
    "is_default",
    "is_marketplace",
]

GLOBAL_DESIGN_FIELDS = [
    "site_name",
    "brand_colors",
    "primary_font",
    "secondary_font",
    "container_max_width",
    "default_spacing",
    "global_css",
    "force_light_mode",
    "default_meta_description",
]

GLOBAL_DESIGN_FILE_FIELDS = ["logo", "favicon", "default_og_image"]

DESIGN_TOKEN_FIELDS = [
    "name",
    "token_type",
    "value",
    "description",
    "source",
    "priority_level",
    "tier_restriction",
    "is_active",
    "is_locked",
]

CUSTOM_CSS_FIELDS = [
    "name",
    "description",
    "css_code",
    "apply_to_pages",
    "is_active",
    "load_order",
]

THEME_BRANDING_FIELDS = [
    "color_tokens",
    "typography_tokens",
    "spacing_tokens",
    "border_tokens",
    "shadow_tokens",
    "animation_tokens",
    "transition_tokens",
    "header_tokens",
    "footer_tokens",
    "menu_tokens",
    "search_tokens",
    "element_tokens",
    "component_overrides",
    "custom_css",
    "generated_css",
    "css_hash",
]


class DesignThemeSerializer(CollectionSyncSerializer):
    """Serializer for theme configuration and design settings.

    Models handled:
        - Theme: Theme definitions and compiled CSS
        - GlobalDesignSettings: Global design configuration singleton
        - DesignToken: Brand builder token overrides only (source='brand_builder')
        - CustomCSS: Custom CSS snippets
        - ThemeBranding: Per-theme brand customizations

    Import order: Themes → GlobalDesignSettings → DesignTokens → CustomCSS → ThemeBranding
    (dependency-driven: themes must exist before GDS and branding can reference them)
    """

    category_key = "design_theme"
    natural_key_fields = ["slug"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from design.theme_models import Theme

        self.model_class = Theme

    def get_count(self):
        from design.models import CustomCSS, DesignToken, GlobalDesignSettings
        from design.theme_models import Theme, ThemeBranding

        return (
            Theme.objects.count()
            + (1 if GlobalDesignSettings.objects.exists() else 0)
            + DesignToken.objects.filter(source="brand_builder").count()
            + CustomCSS.objects.count()
            + ThemeBranding.objects.count()
        )

    # -- Export --

    def export(self, credential_mode="redact"):
        from design.models import CustomCSS, DesignToken, GlobalDesignSettings
        from design.theme_models import Theme, ThemeBranding

        items = []
        files = {}

        # 1. Themes
        for theme in Theme.objects.all():
            data = {field: getattr(theme, field) for field in THEME_FIELDS}
            data["_source_pk"] = theme.pk
            data["_model"] = "Theme"
            items.append(data)

            # Export package_file via file_handler
            file_data = export_file_field(theme, "package_file")
            if file_data:
                files[f"Theme:{theme.slug}:package_file"] = file_data

        # 2. GlobalDesignSettings (singleton)
        gds = GlobalDesignSettings.objects.first()
        if gds:
            data = {field: getattr(gds, field) for field in GLOBAL_DESIGN_FIELDS}
            data["_source_pk"] = gds.pk
            data["_model"] = "GlobalDesignSettings"
            data["_active_theme_slug"] = gds.active_theme.slug if gds.active_theme else None
            items.append(data)

            for file_field in GLOBAL_DESIGN_FILE_FIELDS:
                file_data = export_file_field(gds, file_field)
                if file_data:
                    files[f"GlobalDesignSettings:{file_field}"] = file_data

        # 3. DesignTokens (brand_builder only)
        for token in DesignToken.objects.filter(source="brand_builder"):
            data = {field: getattr(token, field) for field in DESIGN_TOKEN_FIELDS}
            data["_source_pk"] = token.pk
            data["_model"] = "DesignToken"
            items.append(data)

        # 4. CustomCSS
        for css in CustomCSS.objects.all():
            data = {field: getattr(css, field) for field in CUSTOM_CSS_FIELDS}
            data["_source_pk"] = css.pk
            data["_model"] = "CustomCSS"
            items.append(data)

        # 5. ThemeBranding
        for branding in ThemeBranding.objects.select_related("theme").all():
            data = {field: getattr(branding, field) for field in THEME_BRANDING_FIELDS}
            data["_source_pk"] = branding.pk
            data["_model"] = "ThemeBranding"
            data["_theme_slug"] = branding.theme.slug if branding.theme else None
            items.append(data)

        return {
            "category": self.category_key,
            "sync_type": "collection",
            "items": items,
            "total": len(items),
            "files": files,
        }

    # -- Import --

    def import_data(self, data, dry_run=False, sync_mode="additive"):
        if dry_run:
            return self.generate_diff(data)

        items = data.get("items", [])
        files = data.get("files", {})
        synced = 0
        skipped = 0
        failed = 0
        deleted = 0
        errors = []

        try:
            with transaction.atomic():
                # Separate items by model type
                themes = [i for i in items if i.get("_model") == "Theme"]
                gds_list = [i for i in items if i.get("_model") == "GlobalDesignSettings"]
                tokens = [i for i in items if i.get("_model") == "DesignToken"]
                css_items = [i for i in items if i.get("_model") == "CustomCSS"]
                brandings = [i for i in items if i.get("_model") == "ThemeBranding"]

                # Pass 1: Themes (must exist before GDS and ThemeBranding)
                for item in themes:
                    try:
                        self._import_theme(item, files)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"Theme '{item.get('slug', '?')}': {e}")
                        logger.error("Failed to import theme '%s': %s", item.get("slug"), e)

                # Pass 2: GlobalDesignSettings (references active_theme)
                for item in gds_list:
                    try:
                        self._import_global_design_settings(item, files)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"GlobalDesignSettings: {e}")
                        logger.error("Failed to import GlobalDesignSettings: %s", e)

                # Pass 3: DesignTokens (brand_builder overrides)
                for item in tokens:
                    try:
                        self._import_design_token(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"DesignToken '{item.get('name', '?')}': {e}")
                        logger.error("Failed to import design token '%s': %s", item.get("name"), e)

                # Pass 4: CustomCSS
                for item in css_items:
                    try:
                        self._import_custom_css(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"CustomCSS '{item.get('name', '?')}': {e}")
                        logger.error("Failed to import custom CSS '%s': %s", item.get("name"), e)

                # Pass 5: ThemeBranding (references theme FK)
                for item in brandings:
                    try:
                        self._import_theme_branding(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"ThemeBranding for '{item.get('_theme_slug', '?')}': {e}")
                        logger.error("Failed to import theme branding: %s", e)

                # Mirror mode: delete local items not in remote data
                if sync_mode == "mirror":
                    deleted = self._delete_absent(items)

        except Exception as e:
            logger.error("Design theme import failed: %s", e)
            return {"synced": 0, "skipped": 0, "failed": 1, "errors": [str(e)]}

        result = {"synced": synced, "skipped": skipped, "failed": failed, "errors": errors}
        if sync_mode == "mirror":
            result["deleted"] = deleted
        return result

    def _import_theme(self, item, files):
        """Import or update a theme."""
        from design.theme_models import Theme

        slug = item["slug"]
        existing = Theme.objects.filter(slug=slug).first()

        if existing:
            for field in THEME_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])

            # Import package_file if provided
            file_key = f"Theme:{slug}:package_file"
            if file_key in files:
                import_file_field(existing, "package_file", files[file_key])
                existing.extracted_path = ""  # Force re-extraction

            existing.save()

            # Re-extract if package was updated
            if file_key in files:
                try:
                    existing.extract_theme()
                except Exception as e:
                    logger.warning(
                        "Theme '%s' extract_theme() failed (CSS served from DB): %s", slug, e
                    )
        else:
            theme = Theme()
            for field in THEME_FIELDS:
                if field in item:
                    setattr(theme, field, item[field])

            # Import package_file if provided
            file_key = f"Theme:{slug}:package_file"
            if file_key in files:
                import_file_field(theme, "package_file", files[file_key])

            theme.save()

            # Extract theme assets from package
            if file_key in files:
                try:
                    theme.extract_theme()
                except Exception as e:
                    logger.warning(
                        "Theme '%s' extract_theme() failed (CSS served from DB): %s", slug, e
                    )

    def _import_global_design_settings(self, item, files):
        """Import or update GlobalDesignSettings singleton."""
        from design.models import GlobalDesignSettings
        from design.theme_models import Theme

        gds = GlobalDesignSettings.get_settings()

        for field in GLOBAL_DESIGN_FIELDS:
            if field in item:
                setattr(gds, field, item[field])

        # Resolve active_theme FK from slug
        theme_slug = item.get("_active_theme_slug")
        if theme_slug:
            theme = Theme.objects.filter(slug=theme_slug).first()
            if theme:
                gds.active_theme = theme
            else:
                logger.warning(
                    "Active theme '%s' not found, setting active_theme to None", theme_slug
                )
                gds.active_theme = None
        else:
            gds.active_theme = None

        gds.save()

        # Import file fields (direct ImageFields)
        for file_field in GLOBAL_DESIGN_FILE_FIELDS:
            file_key = f"GlobalDesignSettings:{file_field}"
            if file_key in files:
                if import_file_field(gds, file_field, files[file_key]):
                    gds.save(update_fields=[file_field])

    def _import_design_token(self, item):
        """Import or update a brand_builder design token."""
        from design.models import DesignToken

        existing = DesignToken.objects.filter(name=item["name"], source="brand_builder").first()

        if existing:
            for field in DESIGN_TOKEN_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
        else:
            token = DesignToken()
            for field in DESIGN_TOKEN_FIELDS:
                if field in item:
                    setattr(token, field, item[field])
            # Ensure brand_builder source and priority
            token.source = "brand_builder"
            token.priority_level = 1
            token.save()

    def _import_custom_css(self, item):
        """Import or update a custom CSS rule."""
        from design.models import CustomCSS

        existing = CustomCSS.objects.filter(name=item["name"]).first()

        if existing:
            for field in CUSTOM_CSS_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
        else:
            css = CustomCSS()
            for field in CUSTOM_CSS_FIELDS:
                if field in item:
                    setattr(css, field, item[field])
            css.save()

    def _import_theme_branding(self, item):
        """Import or update theme branding."""
        from design.theme_models import Theme, ThemeBranding

        theme_slug = item.get("_theme_slug")
        theme = None

        if theme_slug:
            theme = Theme.objects.filter(slug=theme_slug).first()
            if not theme:
                raise ValueError(f"Theme '{theme_slug}' not found for branding import")

        # Match by theme (one branding per theme)
        if theme:
            existing = ThemeBranding.objects.filter(theme=theme).first()
        else:
            existing = ThemeBranding.objects.filter(theme__isnull=True).first()

        if existing:
            for field in THEME_BRANDING_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
        else:
            branding = ThemeBranding(theme=theme)
            for field in THEME_BRANDING_FIELDS:
                if field in item:
                    setattr(branding, field, item[field])
            branding.save()

    def _delete_absent(self, items):
        """In mirror mode, delete local items not present in remote data."""
        from design.models import CustomCSS, DesignToken
        from design.theme_models import Theme, ThemeBranding

        deleted_count = 0

        remote_theme_slugs = {i["slug"] for i in items if i.get("_model") == "Theme"}
        remote_token_names = {i["name"] for i in items if i.get("_model") == "DesignToken"}
        remote_css_names = {i["name"] for i in items if i.get("_model") == "CustomCSS"}
        remote_branding_slugs = {
            i.get("_theme_slug") for i in items if i.get("_model") == "ThemeBranding"
        }

        # 1. ThemeBranding (references theme, delete first)
        for branding in ThemeBranding.objects.select_related("theme").all():
            slug = branding.theme.slug if branding.theme else None
            if slug not in remote_branding_slugs:
                branding.delete()
                deleted_count += 1

        # 2. CustomCSS
        for css in CustomCSS.objects.all():
            if css.name not in remote_css_names:
                css.delete()
                deleted_count += 1

        # 3. DesignToken (brand_builder only)
        for token in DesignToken.objects.filter(source="brand_builder"):
            if token.name not in remote_token_names:
                token.delete()
                deleted_count += 1

        # 4. Themes (ThemeBranding FK is SET_NULL so safe)
        for theme in Theme.objects.all():
            if theme.slug not in remote_theme_slugs:
                theme.delete()
                deleted_count += 1

        return deleted_count

    # -- Diff --

    def generate_diff(self, remote_data):
        from design.models import CustomCSS, DesignToken, GlobalDesignSettings
        from design.theme_models import Theme, ThemeBranding

        items = remote_data.get("items", [])
        if not items:
            return {"changes": [], "warnings": [], "summary": "No data to sync"}

        changes = []
        warnings = []

        for item in items:
            model_type = item.get("_model")

            if model_type == "Theme":
                existing = Theme.objects.filter(slug=item.get("slug")).first()
                compare_fields = THEME_FIELDS
                display_name = f"Theme: {item.get('name', item.get('slug'))}"

            elif model_type == "GlobalDesignSettings":
                existing = GlobalDesignSettings.objects.first()
                compare_fields = GLOBAL_DESIGN_FIELDS
                display_name = "Global Design Settings"

            elif model_type == "DesignToken":
                existing = DesignToken.objects.filter(
                    name=item.get("name"), source="brand_builder"
                ).first()
                compare_fields = DESIGN_TOKEN_FIELDS
                display_name = f"Token: {item.get('name')}"

            elif model_type == "CustomCSS":
                existing = CustomCSS.objects.filter(name=item.get("name")).first()
                compare_fields = CUSTOM_CSS_FIELDS
                display_name = f"Custom CSS: {item.get('name')}"

            elif model_type == "ThemeBranding":
                theme_slug = item.get("_theme_slug")
                if theme_slug:
                    theme = Theme.objects.filter(slug=theme_slug).first()
                    existing = ThemeBranding.objects.filter(theme=theme).first() if theme else None
                else:
                    existing = ThemeBranding.objects.filter(theme__isnull=True).first()
                compare_fields = THEME_BRANDING_FIELDS
                display_name = f"Branding: {theme_slug or 'Global'}"

            else:
                warnings.append(f"Unknown model type: {model_type}")
                continue

            if existing:
                field_changes = self._compute_field_diff(existing, item, compare_fields)
                if field_changes:
                    changes.append(
                        {
                            "type": "modify",
                            "model": model_type,
                            "name": display_name,
                            "changes": field_changes,
                        }
                    )
            else:
                changes.append(
                    {
                        "type": "add",
                        "model": model_type,
                        "name": display_name,
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
            "warnings": warnings,
            "summary": ", ".join(parts) if parts else "No changes",
        }

    # -- Snapshot & Restore --

    def snapshot_current(self):
        return self.export(credential_mode="skip")

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {"restored": result.get("synced", 0), "errors": result.get("errors", [])}
        except Exception as e:
            return {"restored": 0, "errors": [str(e)]}
