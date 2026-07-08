"""
Translation configuration for Page Builder Utilities

This module provides integration with Django's translation system
for the utilities components.
"""
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from pathlib import Path


class UtilityTranslations:
    """Centralized translations for all utilities"""

    # Color Picker translations
    COLOR_PICKER = {
        'title': _('Color Picker'),
        'description': _('Advanced color picker with opacity and format support'),
        'select_color': _('Select Color'),
        'presets': _('Presets'),
        'recent': _('Recent'),
        'recent_colors': _('Recent Colors'),
        'clear': _('Clear'),
        'apply': _('Apply'),
        'cancel': _('Cancel'),
        'close': _('Close'),
        'enter_color_value': _('Enter color value'),
        'open_color_picker': _('Open color picker'),
        'opacity': _('Opacity'),
        'hue': _('Hue'),
        'saturation': _('Saturation'),
        'lightness': _('Lightness'),
        'red': _('Red'),
        'green': _('Green'),
        'blue': _('Blue'),
        'alpha': _('Alpha'),
        'hex_color': _('Hex Color'),
        'rgb_color': _('RGB Color'),
        'hsl_color': _('HSL Color'),
    }

    # Unit Selector translations
    UNIT_SELECTOR = {
        'title': _('Unit Selector'),
        'description': _('CSS unit selector and converter'),
        'calc_expression': _('CSS calc() expression'),
        'convert_unit': _('Convert unit'),
        'calc_editor': _('Calc Expression Editor'),
        'calc_help': _('Create complex CSS calculations using calc()'),
        'examples': _('Examples'),
        'unit_converter': _('Unit Converter'),
        'current_value': _('Current Value'),
        'convert_to': _('Convert To'),
        'reference_values': _('Reference Values'),
        'root_font_size': _('root font size'),
        'parent_font_size': _('parent font size'),
        'viewport_width': _('viewport width'),
        'viewport_height': _('viewport height'),
        'pixels': _('Pixels'),
        'percent': _('Percent'),
        'rem': _('Rem'),
        'em': _('Em'),
        'viewport_width_unit': _('Viewport Width'),
        'viewport_height_unit': _('Viewport Height'),
        'auto': _('Auto'),
    }

    # Border Editor translations
    BORDER_EDITOR = {
        'title': _('Border Editor'),
        'description': _('Comprehensive border and border-radius editor'),
        'border_style': _('Border Style'),
        'none': _('None'),
        'solid': _('Solid'),
        'dashed': _('Dashed'),
        'dotted': _('Dotted'),
        'double': _('Double'),
        'groove': _('Groove'),
        'ridge': _('Ridge'),
        'inset': _('Inset'),
        'outset': _('Outset'),
        'border_width': _('Border Width'),
        'border_color': _('Border Color'),
        'border_radius': _('Border Radius'),
        'top_left': _('Top Left'),
        'top_right': _('Top Right'),
        'bottom_left': _('Bottom Left'),
        'bottom_right': _('Bottom Right'),
        'all_corners': _('All Corners'),
        'individual_corners': _('Individual Corners'),
        'top': _('Top'),
        'right': _('Right'),
        'bottom': _('Bottom'),
        'left': _('Left'),
        'all_sides': _('All Sides'),
        'individual_sides': _('Individual Sides'),
        'link_sides': _('Link Sides'),
        'unlink_sides': _('Unlink Sides'),
        'border_presets': _('Border Presets'),
        'rounded': _('Rounded'),
        'pill': _('Pill'),
        'circle': _('Circle'),
    }

    # Spacing Editor translations
    SPACING_EDITOR = {
        'title': _('Spacing Editor'),
        'description': _('Visual padding and margin editor'),
        'padding': _('Padding'),
        'margin': _('Margin'),
        'padding_top': _('Padding Top'),
        'padding_right': _('Padding Right'),
        'padding_bottom': _('Padding Bottom'),
        'padding_left': _('Padding Left'),
        'margin_top': _('Margin Top'),
        'margin_right': _('Margin Right'),
        'margin_bottom': _('Margin Bottom'),
        'margin_left': _('Margin Left'),
        'link_values': _('Link Values'),
        'unlink_values': _('Unlink Values'),
        'box_model': _('Box Model'),
        'visual_editor': _('Visual Editor'),
        'spacing_presets': _('Spacing Presets'),
        'small': _('Small'),
        'medium': _('Medium'),
        'large': _('Large'),
        'extra_large': _('Extra Large'),
        'custom': _('Custom'),
    }

    # Shadow Editor translations
    SHADOW_EDITOR = {
        'title': _('Shadow Editor'),
        'description': _('Box and text shadow editor'),
        'box_shadow': _('Box Shadow'),
        'text_shadow': _('Text Shadow'),
        'x_offset': _('X Offset'),
        'y_offset': _('Y Offset'),
        'blur_radius': _('Blur Radius'),
        'spread_radius': _('Spread Radius'),
        'shadow_color': _('Shadow Color'),
        'inset_shadow': _('Inset Shadow'),
        'add_shadow': _('Add Shadow'),
        'remove_shadow': _('Remove Shadow'),
        'shadow_presets': _('Shadow Presets'),
        'elevation': _('Elevation'),
        'inner_shadow': _('Inner Shadow'),
        'multiple_shadows': _('Multiple Shadows'),
    }

    # Gradient Creator translations
    GRADIENT_CREATOR = {
        'title': _('Gradient Creator'),
        'description': _('Create and edit CSS gradients visually'),
        'gradient_type': _('Gradient Type'),
        'linear': _('Linear'),
        'radial': _('Radial'),
        'conic': _('Conic'),
        'angle': _('Angle'),
        'add_color_stop': _('Add Color Stop'),
        'remove_color_stop': _('Remove Color Stop'),
        'position': _('Position'),
        'color': _('Color'),
        'gradient_presets': _('Gradient Presets'),
        'custom_gradient': _('Custom Gradient'),
        'copy_css': _('Copy CSS'),
        'import': _('Import'),
        'export': _('Export'),
    }

    # Common terms used across utilities
    COMMON = {
        'default': _('Default'),
        'custom': _('Custom'),
        'reset': _('Reset'),
        'save': _('Save'),
        'load': _('Load'),
        'copy': _('Copy'),
        'paste': _('Paste'),
        'delete': _('Delete'),
        'edit': _('Edit'),
        'preview': _('Preview'),
        'settings': _('Settings'),
        'help': _('Help'),
        'documentation': _('Documentation'),
        'value': _('Value'),
        'type': _('Type'),
        'format': _('Format'),
        'options': _('Options'),
        'properties': _('Properties'),
        'advanced': _('Advanced'),
        'basic': _('Basic'),
        'horizontal': _('Horizontal'),
        'vertical': _('Vertical'),
        'center': _('Center'),
        'start': _('Start'),
        'end': _('End'),
        'stretch': _('Stretch'),
        'baseline': _('Baseline'),
    }

    # Error messages
    ERRORS = {
        'invalid_color_format': _('Invalid color format'),
        'invalid_value': _('Invalid value'),
        'value_out_of_range': _('Value out of range'),
        'required_field': _('Required field'),
        'invalid_css_expression': _('Invalid CSS expression'),
        'conversion_not_available': _('Conversion not available'),
    }

    # Success messages
    SUCCESS = {
        'color_applied': _('Color applied successfully'),
        'value_updated': _('Value updated'),
        'settings_saved': _('Settings saved'),
        'copied_to_clipboard': _('Copied to clipboard'),
    }

    # Tooltips
    TOOLTIPS = {
        'click_to_select': _('Click to select color'),
        'drag_to_adjust': _('Drag to adjust'),
        'shift_fine_adjust': _('Hold Shift for fine adjustment'),
        'alt_small_increments': _('Hold Alt for 0.1 increments'),
        'arrow_keys_adjust': _('Use arrow keys to adjust'),
        'right_click_options': _('Right-click for options'),
        'double_click_edit': _('Double-click to edit'),
    }

    @classmethod
    def get_all_translations(cls):
        """Get all translations as a dictionary"""
        return {
            'color_picker': cls.COLOR_PICKER,
            'unit_selector': cls.UNIT_SELECTOR,
            'border_editor': cls.BORDER_EDITOR,
            'spacing_editor': cls.SPACING_EDITOR,
            'shadow_editor': cls.SHADOW_EDITOR,
            'gradient_creator': cls.GRADIENT_CREATOR,
            'common': cls.COMMON,
            'errors': cls.ERRORS,
            'success': cls.SUCCESS,
            'tooltips': cls.TOOLTIPS,
        }

    @classmethod
    def get_js_translations(cls, utility_name=None):
        """Get translations formatted for JavaScript use"""
        import json
        from django.utils.translation import get_language

        current_language = get_language()

        if utility_name:
            # Get translations for specific utility
            translations_dict = getattr(cls, utility_name.upper(), {})
        else:
            # Get all translations
            translations_dict = cls.get_all_translations()

        # Convert lazy translations to strings
        js_translations = {}
        for key, value in translations_dict.items():
            if isinstance(value, dict):
                js_translations[key] = {
                    k: str(v) for k, v in value.items()
                }
            else:
                js_translations[key] = str(value)

        return json.dumps(js_translations)


def get_utilities_locale_path():
    """Get the path to utilities locale directory"""
    return Path(settings.BASE_DIR) / 'page_builder' / 'utilities' / 'locale'


def register_utilities_locale():
    """Register utilities locale path with Django settings"""
    locale_path = get_utilities_locale_path()

    if hasattr(settings, 'LOCALE_PATHS'):
        if str(locale_path) not in settings.LOCALE_PATHS:
            settings.LOCALE_PATHS = list(settings.LOCALE_PATHS) + [str(locale_path)]
    else:
        settings.LOCALE_PATHS = [str(locale_path)]