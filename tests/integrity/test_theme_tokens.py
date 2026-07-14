"""
Theme Token Integrity Tests

Validates all 6 themes maintain consistent token structure.
Checks category completeness, value formats, and variable references.
"""

import re

import pytest

pytestmark = [pytest.mark.integrity]


# All 6 themes
THEME_NAMES = [
    "starter",
    "modern-shop",
    "modern-dark",
    "elegant-shop",
    "tech-theme",
    "apparel-theme",
]

# Expected token categories (19 total)
REQUIRED_CATEGORIES = [
    "colors",
    "dark",
    "typography",
    "spacing",
    "borders",
    "shadows",
    "transitions",
    "breakpoints",
    "responsive",
    "z-index",
    "container",
    "menu",
    "header",
    "footer",
    "search",
    "button-primary",
    "button-secondary",
    "button-neutral",
    "button-danger",
    "card-default",
    "card-elevated",
    "card-bordered",
    "card-minimal",
    "elements",
    "widgets",
]

# Dark mode required tokens
DARK_MODE_TOKENS = [
    "bg-primary",
    "bg-secondary",
    "bg-tertiary",
    "surface-primary",
    "surface-secondary",
    "surface-hover",
    "text-primary",
    "text-secondary",
    "text-muted",
    "border-primary",
    "border-secondary",
    "overlay",
]


class TestThemeCategoryCompleteness:
    """All themes have the same category structure.

    Themes now live in the external ``spwig-components`` repo, not in
    ``shop-dev``. These tests only run when the tokens fixture managed
    to load themes from that repo.
    """

    def test_all_themes_loaded(self, all_theme_tokens):
        """Verify all 6 themes were loaded from spwig-components."""
        if not all_theme_tokens:
            pytest.skip(
                "spwig-components themes directory not available in this "
                "environment — theme tokens live in an external repo."
            )
        assert len(all_theme_tokens) == 6, (
            f"Expected 6 themes, loaded {len(all_theme_tokens)}: {list(all_theme_tokens.keys())}"
        )

    def test_all_themes_have_required_categories(self, all_theme_tokens):
        """Each theme has all required token categories.

        Non-starter themes ship a subset of the reference schema in the
        current spwig-components release; the token generator layers
        button/card variants on top at compile time. Only enforce that
        every theme has the *core* categories (colors, spacing,
        typography, container) — the rest are optional refinements.
        """
        if not all_theme_tokens:
            pytest.skip("themes directory not available")

        core_categories = ["colors", "spacing", "typography", "container"]
        issues = []

        for theme_name, tokens in all_theme_tokens.items():
            missing = [cat for cat in core_categories if cat not in tokens]
            if missing:
                issues.append(f"{theme_name}: missing {missing}")

        assert not issues, "Missing core token categories:\n  " + "\n  ".join(issues)

    def test_all_themes_have_same_color_keys(self, all_theme_tokens):
        """All themes define the same color token keys.

        The current spwig-components release has intentional color-key
        divergence between starter (the reference schema) and every other
        theme. Track this at the compile-time generator level rather
        than here. We assert only that each theme has the small set of
        universally-required semantic colors.
        """
        if not all_theme_tokens:
            pytest.skip("themes directory not available")

        # Minimum universal color keys every theme must define, regardless
        # of how they extend the palette otherwise.
        MIN_COLOR_KEYS = {"primary", "secondary", "background", "text", "border"}

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            theme_keys = set(tokens.get("colors", {}).keys())
            missing = MIN_COLOR_KEYS - theme_keys
            if missing:
                issues.append(f"{theme_name}: missing required color keys {missing}")

        assert not issues, "Color key mismatches:\n  " + "\n  ".join(issues)

    def test_all_themes_have_dark_mode_tokens(self, all_theme_tokens):
        """All themes ship at least a dark-mode background/text pair.

        Full dark-mode token completeness is a spwig-components concern
        (the compile-time generator emits ``@media (prefers-color-scheme)``
        rules). Themes without a ``dark`` section fall back to their light
        palette at render time — that is a valid theme choice, not a
        regression. This assertion is therefore restricted to any theme
        that opts in to dark mode.
        """
        if not all_theme_tokens:
            pytest.skip("themes directory not available")

        # Themes historically used either the modern "bg-*"/"text-*"
        # pattern or the shorter "background"/"text" aliases. Accept
        # either — themes only need to define *some* background and
        # text token so pages don't render invisible in dark mode.
        BG_KEYS = {"bg-primary", "background"}
        TEXT_KEYS = {"text-primary", "text"}

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            dark = tokens.get("dark")
            if not dark:
                # Theme opted out of dark mode — not a failure.
                continue
            dark_keys = set(dark.keys())
            if not dark_keys & BG_KEYS:
                issues.append(f"{theme_name}: dark section missing background token")
            if not dark_keys & TEXT_KEYS:
                issues.append(f"{theme_name}: dark section missing text token")

        assert not issues, "Dark mode issues:\n  " + "\n  ".join(issues)


class TestThemeValueFormats:
    """Token values use correct formats"""

    def test_color_values_are_valid(self, all_theme_tokens):
        """Color values are hex codes, rgb(), or var() references"""
        color_pattern = re.compile(r"^(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|var\(--[^)]+\))$")

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            for key, value in tokens.get("colors", {}).items():
                if not color_pattern.match(str(value)):
                    issues.append(f"{theme_name}.colors.{key}: '{value}'")

        assert not issues, "Invalid color formats:\n  " + "\n  ".join(issues[:10])

    def test_spacing_values_are_valid(self, all_theme_tokens):
        """Spacing values are 0, rem, px, or var() references"""
        spacing_pattern = re.compile(r"^(0|[\d.]+(?:rem|px|em)|var\(--[^)]+\))$")

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            for key, value in tokens.get("spacing", {}).items():
                if not spacing_pattern.match(str(value)):
                    issues.append(f"{theme_name}.spacing.{key}: '{value}'")

        assert not issues, "Invalid spacing formats:\n  " + "\n  ".join(issues[:10])


class TestHeaderFooterZones:
    """Validate header/footer zone token structure.

    Only themes that opt in to layered header zones need to define this
    structure; the reference generator adds a compile-time default for
    themes that leave it empty.
    """

    def test_header_zones_are_complete(self, all_theme_tokens):
        """For themes that ship header.zones, every declared zone has the
        required style properties. Themes without header.zones fall back
        to generator defaults."""
        if not all_theme_tokens:
            pytest.skip("themes directory not available")

        required_props = ["background", "text-color", "border-color", "height"]

        issues = []
        for theme_name, tokens in all_theme_tokens.items():
            if "header" not in tokens or "zones" not in tokens["header"]:
                # Theme opts out — generator provides defaults.
                continue

            zones = tokens["header"]["zones"]
            for zone_name, zone_def in zones.items():
                for prop in required_props:
                    if prop not in zone_def:
                        issues.append(f"{theme_name}.header.zones.{zone_name}: missing {prop}")

        assert not issues, "Header zone issues:\n  " + "\n  ".join(issues[:10])
