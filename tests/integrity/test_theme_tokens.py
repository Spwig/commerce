"""
Theme Token Integrity Tests

Validates all 6 themes maintain consistent token structure.
Checks category completeness, value formats, and variable references.
"""
import pytest
import re


pytestmark = [pytest.mark.integrity]


# All 6 themes
THEME_NAMES = [
    'starter', 'modern-shop', 'modern-dark',
    'elegant-shop', 'tech-theme', 'apparel-theme'
]

# Expected token categories (19 total)
REQUIRED_CATEGORIES = [
    'colors', 'dark', 'typography', 'spacing', 'borders',
    'shadows', 'transitions', 'breakpoints', 'responsive',
    'z-index', 'container', 'menu', 'header', 'footer',
    'search', 'button-primary', 'button-secondary', 'button-neutral',
    'button-danger', 'card-default', 'card-elevated', 'card-bordered',
    'card-minimal', 'elements', 'widgets'
]

# Dark mode required tokens
DARK_MODE_TOKENS = [
    'bg-primary', 'bg-secondary', 'bg-tertiary',
    'surface-primary', 'surface-secondary', 'surface-hover',
    'text-primary', 'text-secondary', 'text-muted',
    'border-primary', 'border-secondary', 'overlay'
]


class TestThemeCategoryCompleteness:
    """All themes have the same category structure"""

    def test_all_themes_loaded(self, all_theme_tokens):
        """Verify all 6 themes were loaded"""
        assert len(all_theme_tokens) == 6, (
            f"Expected 6 themes, loaded {len(all_theme_tokens)}: {list(all_theme_tokens.keys())}"
        )

    def test_all_themes_have_required_categories(self, all_theme_tokens):
        """Each theme has all required token categories"""
        issues = []

        for theme_name, tokens in all_theme_tokens.items():
            missing = [cat for cat in REQUIRED_CATEGORIES if cat not in tokens]
            if missing:
                issues.append(f"{theme_name}: missing {missing}")

        assert not issues, "Missing token categories:\n  " + "\n  ".join(issues)

    def test_all_themes_have_same_color_keys(self, all_theme_tokens):
        """All themes define the same color token keys"""
        # Use starter as reference
        reference_keys = set(all_theme_tokens['starter']['colors'].keys())

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            if theme_name == 'starter':
                continue

            theme_keys = set(tokens['colors'].keys())
            missing = reference_keys - theme_keys
            extra = theme_keys - reference_keys

            if missing:
                issues.append(f"{theme_name}: missing color keys {missing}")
            if extra:
                issues.append(f"{theme_name}: extra color keys {extra}")

        assert not issues, "Color key mismatches:\n  " + "\n  ".join(issues)

    def test_all_themes_have_dark_mode_tokens(self, all_theme_tokens):
        """All themes define dark mode token structure"""
        issues = []

        for theme_name, tokens in all_theme_tokens.items():
            if 'dark' not in tokens:
                issues.append(f"{theme_name}: missing 'dark' category")
                continue

            missing = [t for t in DARK_MODE_TOKENS if t not in tokens['dark']]
            if missing:
                issues.append(f"{theme_name}: missing dark tokens {missing}")

        assert not issues, "Dark mode issues:\n  " + "\n  ".join(issues)


class TestThemeValueFormats:
    """Token values use correct formats"""

    def test_color_values_are_valid(self, all_theme_tokens):
        """Color values are hex codes, rgb(), or var() references"""
        color_pattern = re.compile(
            r'^(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|var\(--[^)]+\))$'
        )

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            for key, value in tokens.get('colors', {}).items():
                if not color_pattern.match(str(value)):
                    issues.append(f"{theme_name}.colors.{key}: '{value}'")

        assert not issues, f"Invalid color formats:\n  " + "\n  ".join(issues[:10])

    def test_spacing_values_are_valid(self, all_theme_tokens):
        """Spacing values are 0, rem, px, or var() references"""
        spacing_pattern = re.compile(r'^(0|[\d.]+(?:rem|px|em)|var\(--[^)]+\))$')

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            for key, value in tokens.get('spacing', {}).items():
                if not spacing_pattern.match(str(value)):
                    issues.append(f"{theme_name}.spacing.{key}: '{value}'")

        assert not issues, f"Invalid spacing formats:\n  " + "\n  ".join(issues[:10])


class TestHeaderFooterZones:
    """Validate header/footer zone token structure"""

    def test_header_zones_are_complete(self, all_theme_tokens):
        """Header zones have all required properties"""
        required_zones = ['top-bar', 'main-header', 'bottom-bar', 'mega-menu-bar']
        required_props = ['background', 'text-color', 'border-color', 'height']

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            if 'header' not in tokens or 'zones' not in tokens['header']:
                issues.append(f"{theme_name}: missing header.zones")
                continue

            zones = tokens['header']['zones']
            for zone_name in required_zones:
                if zone_name not in zones:
                    issues.append(f"{theme_name}: missing header zone {zone_name}")
                    continue

                for prop in required_props:
                    if prop not in zones[zone_name]:
                        issues.append(
                            f"{theme_name}.header.zones.{zone_name}: missing {prop}"
                        )

        assert not issues, "Header zone issues:\n  " + "\n  ".join(issues[:10])
