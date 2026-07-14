"""
Utility Registry System for Page Builder

This module provides a registry for managing reusable utility components
that can be used across different page builder elements.
"""

import logging
from typing import Any

from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class UtilityConfig:
    """Configuration for a utility component."""

    def __init__(self, name: str, config: dict[str, Any]):
        self.name = name
        self.display_name = config.get("display_name", name.title())
        self.description = config.get("description", "")
        self.component_type = config.get("component_type", "widget")  # widget, inline, popup
        self.js_class = config.get("js_class", "")
        self.css_files = config.get("css_files", [])
        self.js_files = config.get("js_files", [])
        self.template = config.get("template", "")
        self.supported_properties = config.get("supported_properties", [])
        self.options = config.get("options", {})
        self.translations = config.get("translations", {})

    def get_translated_name(self, language_code: str = "en") -> str:
        """Get the translated display name."""
        if language_code in self.translations:
            return self.translations[language_code].get("display_name", self.display_name)
        return self.display_name

    def get_translated_description(self, language_code: str = "en") -> str:
        """Get the translated description."""
        if language_code in self.translations:
            return self.translations[language_code].get("description", self.description)
        return self.description

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "component_type": self.component_type,
            "js_class": self.js_class,
            "css_files": self.css_files,
            "js_files": self.js_files,
            "template": self.template,
            "supported_properties": self.supported_properties,
            "options": self.options,
        }


class UtilityRegistry:
    """Registry for managing reusable utility components."""

    def __init__(self):
        self._utilities: dict[str, UtilityConfig] = {}
        self._property_map: dict[str, list[str]] = {}  # Maps property types to utility names
        self._initialized = False

    def initialize(self):
        """Initialize the registry with built-in utilities."""
        if self._initialized:
            return

        # Register built-in utilities
        self.register_builtin_utilities()
        self._initialized = True

    def register_builtin_utilities(self):
        """Register all built-in utility components."""

        # Color Picker
        self.register_utility(
            "color_picker",
            {
                "display_name": _("Color Picker"),
                "description": _("Advanced color picker with opacity and format support"),
                "component_type": "popup",
                "js_class": "ColorPickerUtility",
                "css_files": ["css/page_builder/utilities/color_picker.css"],
                "js_files": ["js/page_builder/utilities/color_picker.js"],
                "template": "page_builder/utilities/color_picker.html",
                "supported_properties": [
                    "color",
                    "background_color",
                    "border_color",
                    "text_color",
                    "hover_background_color",
                    "hover_border_color",
                    "overlay_color",
                    "dark_background_color",
                    "dark_border_color",
                ],
                "options": {
                    "show_opacity": True,
                    "show_swatches": True,
                    "show_recent": True,
                    "formats": ["hex", "rgb", "rgba", "hsl", "hsla"],
                },
                "translations": {
                    "es": {
                        "display_name": "Selector de Color",
                        "description": "Selector de color avanzado con opacidad y soporte de formato",
                    },
                    "fr": {
                        "display_name": "Sélecteur de Couleur",
                        "description": "Sélecteur de couleur avancé avec opacité et support de format",
                    },
                    "de": {
                        "display_name": "Farbwähler",
                        "description": "Erweiterter Farbwähler mit Deckkraft und Formatunterstützung",
                    },
                },
            },
        )

        # Gradient Creator
        self.register_utility(
            "gradient_creator",
            {
                "display_name": _("Gradient Creator"),
                "description": _("Create and edit CSS gradients visually"),
                "component_type": "popup",
                "js_class": "GradientCreatorUtility",
                "css_files": ["css/page_builder/utilities/gradient_creator.css"],
                "js_files": ["js/page_builder/utilities/gradient_creator.js"],
                "template": "page_builder/utilities/gradient_creator.html",
                "supported_properties": [
                    "background_gradient",
                    "hover_background_gradient",
                    "overlay_gradient",
                    "hover_overlay_gradient",
                ],
                "options": {
                    "types": ["linear", "radial", "conic"],
                    "presets": True,
                    "color_picker_integration": True,
                },
            },
        )

        # Border Editor
        self.register_utility(
            "border_editor",
            {
                "display_name": _("Border Editor"),
                "description": _("Comprehensive border and border-radius editor"),
                "component_type": "popup",
                "js_class": "BorderEditorUtility",
                "css_files": ["css/page_builder/utilities/border_editor.css"],
                "js_files": ["js/page_builder/utilities/border_editor.js"],
                "template": "page_builder/utilities/border_editor.html",
                "supported_properties": [
                    "border_type",
                    "border_width",
                    "border_color",
                    "border_radius",
                    "border_radius_top",
                    "border_radius_right",
                    "border_radius_bottom",
                    "border_radius_left",
                    "custom_border",
                ],
                "options": {
                    "individual_sides": True,
                    "individual_corners": True,
                    "color_picker_integration": True,
                    "presets": ["rounded", "pill", "circle"],
                },
            },
        )

        # Spacing Editor
        self.register_utility(
            "spacing_editor",
            {
                "display_name": _("Spacing Editor"),
                "description": _("Visual padding and margin editor"),
                "component_type": "inline",
                "js_class": "SpacingEditorUtility",
                "css_files": ["css/page_builder/utilities/spacing_editor.css"],
                "js_files": ["js/page_builder/utilities/spacing_editor.js"],
                "template": "page_builder/utilities/spacing_editor.html",
                "supported_properties": [
                    "padding",
                    "padding_top",
                    "padding_right",
                    "padding_bottom",
                    "padding_left",
                    "margin",
                    "margin_top",
                    "margin_right",
                    "margin_bottom",
                    "margin_left",
                ],
                "options": {
                    "visual_box_model": True,
                    "link_sides": True,
                    "unit_selector_integration": True,
                    "negative_margins": True,
                    "auto_margins": True,
                },
            },
        )

        # Shadow Editor
        self.register_utility(
            "shadow_editor",
            {
                "display_name": _("Shadow Editor"),
                "description": _("Box and text shadow editor"),
                "component_type": "popup",
                "js_class": "ShadowEditorUtility",
                "css_files": ["css/page_builder/utilities/shadow_editor.css"],
                "js_files": ["js/page_builder/utilities/shadow_editor.js"],
                "template": "page_builder/utilities/shadow_editor.html",
                "supported_properties": ["box_shadow", "hover_box_shadow", "text_shadow"],
                "options": {
                    "multiple_shadows": True,
                    "inset_support": True,
                    "color_picker_integration": True,
                    "presets": ["small", "medium", "large", "elevation"],
                },
            },
        )

        # Unit Selector
        self.register_utility(
            "unit_selector",
            {
                "display_name": _("Unit Selector"),
                "description": _("CSS unit selector and converter"),
                "component_type": "inline",
                "js_class": "UnitSelectorUtility",
                "css_files": ["css/page_builder/utilities/unit_selector.css"],
                "js_files": ["js/page_builder/utilities/unit_selector.js"],
                "template": "page_builder/utilities/unit_selector.html",
                "supported_properties": [
                    "width_unit",
                    "height_unit",
                    "padding_unit",
                    "margin_unit",
                    "gap_unit",
                    "min_height_unit",
                    "max_height_unit",
                ],
                "options": {
                    "units": ["px", "%", "rem", "em", "vw", "vh", "auto"],
                    "calc_support": True,
                    "conversion_helper": True,
                },
            },
        )

        # Background Editor
        self.register_utility(
            "background_editor",
            {
                "display_name": _("Background Editor"),
                "description": _(
                    "Comprehensive background styling editor with images, gradients, and patterns"
                ),
                "component_type": "popup",
                "js_class": "BackgroundEditorUtility",
                "css_files": ["css/page_builder/utilities/background_editor.css"],
                "js_files": ["js/page_builder/utilities/background_editor.js"],
                "template": "page_builder/utilities/background_editor.html",
                "supported_properties": [
                    "background_type",
                    "background_color",
                    "background_image",
                    "background_size",
                    "background_position",
                    "background_repeat",
                    "background_attachment",
                    "background_gradient",
                ],
                "options": {
                    "color_picker_integration": True,
                    "gradient_integration": True,
                    "image_upload": True,
                    "patterns": True,
                    "overlay_support": True,
                },
            },
        )

        # Typography Editor
        self.register_utility(
            "typography_editor",
            {
                "display_name": _("Typography Editor"),
                "description": _("Advanced text styling and typography controls"),
                "component_type": "popup",
                "js_class": "TypographyEditorUtility",
                "css_files": ["css/page_builder/utilities/typography_editor.css"],
                "js_files": ["js/page_builder/utilities/typography_editor.js"],
                "template": "page_builder/utilities/typography_editor.html",
                "supported_properties": [
                    "font_family",
                    "font_size",
                    "font_weight",
                    "font_style",
                    "line_height",
                    "letter_spacing",
                    "text_align",
                    "text_transform",
                    "text_decoration",
                    "text_color",
                ],
                "options": {
                    "google_fonts": True,
                    "system_fonts": True,
                    "custom_fonts": True,
                    "responsive_sizing": True,
                    "color_picker_integration": True,
                },
            },
        )

        # Translation Editor
        self.register_utility(
            "translation_editor",
            {
                "display_name": _("Translation Editor"),
                "description": _("Multi-language content editor for translatable fields"),
                "component_type": "popup",
                "js_class": "TranslationEditorUtility",
                "css_files": ["css/page_builder/utilities/translation_editor.css"],
                "js_files": ["js/page_builder/utilities/translation_editor.js"],
                "template": "page_builder/utilities/translation_editor.html",
                "supported_properties": [
                    "translatable_text",
                    "translatable_content",
                    "translatable_title",
                    "translatable_description",
                ],
                "options": {
                    "language_tabs": True,
                    "fallback_language": "en",
                    "rtl_support": True,
                    "machine_translation_integration": False,
                },
            },
        )

        # Base Utility
        self.register_utility(
            "base",
            {
                "display_name": _("Base Utility"),
                "description": _("Core utility functionality and shared components"),
                "component_type": "inline",
                "js_class": "BaseUtility",
                "css_files": ["css/page_builder/utilities/base.css"],
                "js_files": ["js/page_builder/utilities/base.js"],
                "template": "page_builder/utilities/base.html",
                "supported_properties": [],
                "options": {
                    "provides_common_helpers": True,
                    "event_system": True,
                    "validation_helpers": True,
                },
            },
        )

    def register_utility(self, name: str, config: dict[str, Any]):
        """Register a utility component."""
        utility = UtilityConfig(name, config)
        self._utilities[name] = utility

        # Map properties to this utility
        for prop in utility.supported_properties:
            if prop not in self._property_map:
                self._property_map[prop] = []
            if name not in self._property_map[prop]:
                self._property_map[prop].append(name)

        logger.info(f"Registered utility: {name}")

    def unregister_utility(self, name: str):
        """Unregister a utility component."""
        if name in self._utilities:
            utility = self._utilities[name]

            # Remove from property map
            for prop in utility.supported_properties:
                if prop in self._property_map and name in self._property_map[prop]:
                    self._property_map[prop].remove(name)

            del self._utilities[name]
            logger.info(f"Unregistered utility: {name}")

    def get_utility(self, name: str) -> UtilityConfig | None:
        """Get a utility configuration by name."""
        if not self._initialized:
            self.initialize()
        return self._utilities.get(name)

    def get_all_utilities(self) -> dict[str, UtilityConfig]:
        """Get all registered utilities."""
        if not self._initialized:
            self.initialize()
        return self._utilities.copy()

    def get_utilities_for_property(self, property_name: str) -> list[UtilityConfig]:
        """Get utilities that support a specific property."""
        if not self._initialized:
            self.initialize()

        utility_names = self._property_map.get(property_name, [])
        return [self._utilities[name] for name in utility_names if name in self._utilities]

    def get_utility_assets(self) -> dict[str, list[str]]:
        """Get all CSS and JS files needed for utilities."""
        if not self._initialized:
            self.initialize()

        assets = {"css": [], "js": []}

        for utility in self._utilities.values():
            assets["css"].extend(utility.css_files)
            assets["js"].extend(utility.js_files)

        # Remove duplicates while preserving order
        assets["css"] = list(dict.fromkeys(assets["css"]))
        assets["js"] = list(dict.fromkeys(assets["js"]))

        return assets

    def to_json(self) -> dict[str, Any]:
        """Export registry data for client-side use."""
        if not self._initialized:
            self.initialize()

        return {
            "utilities": {name: utility.to_dict() for name, utility in self._utilities.items()},
            "property_map": self._property_map,
        }

    def get_discovered_assets(self) -> dict[str, list[str]]:
        """
        Get CSS and JS assets from auto-discovered utilities.
        Uses the discovery system to dynamically find installed utilities.

        Returns:
            Dictionary with 'css' and 'js' keys containing lists of asset paths.
        """
        from .utility_discovery import get_utility_assets

        return get_utility_assets()


# Global registry instance
_registry = UtilityRegistry()


def get_utility_registry() -> UtilityRegistry:
    """Get the global utility registry instance."""
    return _registry


def get_utility_assets() -> dict[str, list[str]]:
    """
    Convenience function to get utility assets using auto-discovery.
    This bypasses the old registry system and uses the new discovery system.

    Returns:
        Dictionary with 'css' and 'js' keys containing lists of asset paths.
    """
    from .utility_discovery import get_utility_assets as discover_assets

    return discover_assets()
