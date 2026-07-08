"""
Theme Preset Installer Service

Installs and uninstalls header/footer presets that are bundled with theme packages.
Theme presets are stored as JSON files under a theme's presets/ directory:
    presets/headers/*.json
    presets/footers/*.json

Each preset JSON defines a complete HeaderTemplate or FooterTemplate including
its widget placements, which are created automatically on install.
"""

import json
import logging
from pathlib import Path

from django.db import transaction
from django.utils.text import slugify

from design.header_footer_models import (
    FooterTemplate,
    HeaderTemplate,
    Widget,
    WidgetPlacement,
)

logger = logging.getLogger(__name__)


class ThemePresetInstaller:
    """Installs/uninstalls header and footer presets from theme packages."""

    @classmethod
    def install_presets(cls, theme_slug: str, presets_dir: Path) -> dict:
        """Install presets from a theme's presets/ directory.

        Reads JSON files from:
        - presets_dir/headers/*.json
        - presets_dir/footers/*.json

        Creates HeaderTemplate/FooterTemplate + Widget + WidgetPlacement records
        with source='theme:{theme_slug}'.

        Returns dict with counts: {'headers_created': N, 'footers_created': N}
        """
        headers_created = 0
        footers_created = 0

        headers_dir = presets_dir / 'headers'
        footers_dir = presets_dir / 'footers'

        # Install header presets
        if headers_dir.is_dir():
            for json_file in sorted(headers_dir.glob('*.json')):
                try:
                    preset_data = json.loads(json_file.read_text(encoding='utf-8'))
                    header = cls._create_header_from_preset(preset_data, theme_slug)
                    if header:
                        headers_created += 1
                        logger.info(
                            "Installed header preset '%s' from theme '%s'",
                            header.name, theme_slug,
                        )
                except (json.JSONDecodeError, KeyError) as e:
                    logger.error(
                        "Failed to parse header preset %s: %s",
                        json_file.name, e,
                    )
                except Exception as e:
                    logger.error(
                        "Failed to install header preset %s: %s",
                        json_file.name, e,
                    )

        # Install footer presets
        if footers_dir.is_dir():
            for json_file in sorted(footers_dir.glob('*.json')):
                try:
                    preset_data = json.loads(json_file.read_text(encoding='utf-8'))
                    footer = cls._create_footer_from_preset(preset_data, theme_slug)
                    if footer:
                        footers_created += 1
                        logger.info(
                            "Installed footer preset '%s' from theme '%s'",
                            footer.name, theme_slug,
                        )
                except (json.JSONDecodeError, KeyError) as e:
                    logger.error(
                        "Failed to parse footer preset %s: %s",
                        json_file.name, e,
                    )
                except Exception as e:
                    logger.error(
                        "Failed to install footer preset %s: %s",
                        json_file.name, e,
                    )

        result = {
            'headers_created': headers_created,
            'footers_created': footers_created,
        }
        logger.info(
            "Theme '%s' preset installation complete: %d headers, %d footers",
            theme_slug, headers_created, footers_created,
        )
        return result

    @classmethod
    def uninstall_presets(cls, theme_slug: str) -> dict:
        """Remove all presets installed by a theme.

        Deletes HeaderTemplate/FooterTemplate records where source='theme:{theme_slug}'.
        Cascading deletes handle WidgetPlacement records.

        Returns dict with counts: {'headers_deleted': N, 'footers_deleted': N}
        """
        source = f'theme:{theme_slug}'

        with transaction.atomic():
            headers_qs = HeaderTemplate.objects.filter(source=source)
            headers_deleted = headers_qs.count()
            headers_qs.delete()

            footers_qs = FooterTemplate.objects.filter(source=source)
            footers_deleted = footers_qs.count()
            footers_qs.delete()

        result = {
            'headers_deleted': headers_deleted,
            'footers_deleted': footers_deleted,
        }
        logger.info(
            "Theme '%s' preset uninstall complete: %d headers, %d footers removed",
            theme_slug, headers_deleted, footers_deleted,
        )
        return result

    @classmethod
    def _create_header_from_preset(cls, preset_data: dict, theme_slug: str) -> HeaderTemplate:
        """Create a HeaderTemplate + WidgetPlacements from a preset JSON definition.

        Expected preset_data format:
        {
            "name": "Dark Centered Header",
            "description": "Centered logo with full-width menu below",
            "layout_type": "boutique",
            "is_sticky": true,
            "enable_notification_zone": false,
            "preset_category": "modern",
            "zone_layouts": {
                "main-header": ["center"],
                "bottom-bar": ["full"]
            },
            "zone_overrides": {},
            "widget_placements": [
                {"widget_type": "logo", "zone": "main-header_center", "order": 0, "config": {"height": 60}},
                {"widget_type": "menu", "zone": "bottom-bar_full", "order": 0}
            ]
        }
        """
        source = f'theme:{theme_slug}'
        preset_name = preset_data['name']
        preset_slug = f'theme-{theme_slug}-{slugify(preset_name)}'

        # Skip if already installed (idempotent)
        existing = HeaderTemplate.objects.filter(slug=preset_slug).first()
        if existing:
            logger.debug(
                "Header preset '%s' already exists (slug=%s), skipping",
                preset_name, preset_slug,
            )
            return None

        with transaction.atomic():
            header = HeaderTemplate.objects.create(
                name=preset_name,
                slug=preset_slug,
                description=preset_data.get('description', ''),
                layout_type=preset_data.get('layout_type', 'classic'),
                is_sticky=preset_data.get('is_sticky', False),
                enable_notification_zone=preset_data.get('enable_notification_zone', True),
                zone_layouts=preset_data.get('zone_layouts', {}),
                zone_overrides=preset_data.get('zone_overrides', {}),
                is_preset=True,
                preset_category=preset_data.get('preset_category', 'modern'),
                source=source,
                is_active=True,
                is_default=preset_data.get('is_default', False),
            )

            # Create widget placements
            cls._create_widget_placements(
                preset_data.get('widget_placements', []),
                header=header,
                footer=None,
            )

        return header

    @classmethod
    def _create_footer_from_preset(cls, preset_data: dict, theme_slug: str) -> FooterTemplate:
        """Create a FooterTemplate + WidgetPlacements from a preset JSON definition.

        Expected preset_data format:
        {
            "name": "Dark Multi-Column Footer",
            "description": "4-column footer with dark background",
            "layout_type": "columns",
            "column_count": 4,
            "has_bottom_bar": true,
            "preset_category": "modern",
            "widget_placements": [
                {"widget_type": "links", "zone": "column_1", "order": 0, "config": {...}},
                {"widget_type": "newsletter", "zone": "column_4", "order": 0}
            ]
        }
        """
        source = f'theme:{theme_slug}'
        preset_name = preset_data['name']
        preset_slug = f'theme-{theme_slug}-{slugify(preset_name)}'

        # Skip if already installed (idempotent)
        existing = FooterTemplate.objects.filter(slug=preset_slug).first()
        if existing:
            logger.debug(
                "Footer preset '%s' already exists (slug=%s), skipping",
                preset_name, preset_slug,
            )
            return None

        with transaction.atomic():
            footer = FooterTemplate.objects.create(
                name=preset_name,
                slug=preset_slug,
                description=preset_data.get('description', ''),
                layout_type=preset_data.get('layout_type', 'columns'),
                column_count=preset_data.get('column_count', 4),
                has_bottom_bar=preset_data.get('has_bottom_bar', True),
                zones=preset_data.get('zones', {}),
                is_preset=True,
                preset_category=preset_data.get('preset_category', 'modern'),
                source=source,
                is_active=True,
                is_default=preset_data.get('is_default', False),
            )

            # Create widget placements
            cls._create_widget_placements(
                preset_data.get('widget_placements', []),
                header=None,
                footer=footer,
            )

        return footer

    @classmethod
    def _create_widget_placements(
        cls,
        placements_data: list,
        header: HeaderTemplate = None,
        footer: FooterTemplate = None,
    ) -> list:
        """Create WidgetPlacement records for a header or footer template.

        Each placement dict should have:
        - widget_type: str (required) - matches Widget.widget_type
        - zone: str (required) - zone identifier (e.g., 'main-header_left')
        - order: int (optional, default 0)
        - config: dict (optional) - override_config for the placement

        Widgets are looked up or created via get_or_create on widget_type.
        """
        # Build a mapping of widget_type -> display name for auto-creation
        widget_type_names = dict(Widget.WIDGET_TYPES)

        created_placements = []
        for placement_data in placements_data:
            widget_type = placement_data.get('widget_type')
            if not widget_type:
                logger.warning("Skipping placement with no widget_type: %s", placement_data)
                continue

            # Get or create the shared widget for this type
            display_name = str(widget_type_names.get(widget_type, widget_type.replace('_', ' ').title()))
            widget, _ = Widget.objects.get_or_create(
                widget_type=widget_type,
                defaults={
                    'name': display_name,
                    'config': {},
                    'is_active': True,
                },
            )

            placement = WidgetPlacement.objects.create(
                widget=widget,
                header=header,
                footer=footer,
                zone=placement_data.get('zone', ''),
                order=placement_data.get('order', 0),
                override_config=placement_data.get('config', {}),
                is_active=True,
            )
            created_placements.append(placement)

        return created_placements
