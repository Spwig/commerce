"""
Standalone service for generating tokens.css from tokens.json (or a dict).

This module extracts the CSS generation logic from the management command so it
can be reused by both `manage.py generate_tokens_css` and `Theme.extract_theme()`.

The generated CSS uses standardized --theme- prefix naming conventions:
- colors       -> --theme-color-{name}
- spacing      -> --theme-space-{size}
- typography   -> --theme-{name} (font-*, line-height-*, letter-spacing-*)
- borders      -> --theme-border-width-{n} and --theme-radius-{name}
- shadows      -> --theme-shadow-{name}
- transitions  -> --theme-transition-{type}-{name}
- z-index      -> --theme-z-{name}
- container    -> --theme-container-{name}
- menu         -> --theme-menu-{name}
- elements     -> --theme-element-{category}-{name} (page builder element defaults)
- widgets      -> --theme-widget-{name}-{prop} (header/footer widget defaults)

The --theme- prefix ensures clear namespace separation from other CSS systems.
"""

import json
import re
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Patterns for transforming legacy var() references to --theme- prefix.
# These patterns match old variable references inside token values.
VAR_REFERENCE_PATTERNS = [
    # Colors
    (r"var\(--color-", "var(--theme-color-"),
    # Spacing
    (r"var\(--space-", "var(--theme-space-"),
    # Typography
    (r"var\(--font-size-", "var(--theme-font-size-"),
    (r"var\(--font-weight-", "var(--theme-font-weight-"),
    (r"var\(--font-family-", "var(--theme-font-family-"),
    (r"var\(--font-sans", "var(--theme-font-sans"),
    (r"var\(--font-serif", "var(--theme-font-serif"),
    (r"var\(--font-mono", "var(--theme-font-mono"),
    (r"var\(--line-height-", "var(--theme-line-height-"),
    (r"var\(--letter-spacing-", "var(--theme-letter-spacing-"),
    # Borders
    (r"var\(--radius-", "var(--theme-radius-"),
    (r"var\(--border-width-", "var(--theme-border-width-"),
    # Shadows
    (r"var\(--shadow-", "var(--theme-shadow-"),
    # Transitions
    (r"var\(--duration-", "var(--theme-transition-duration-"),
    (r"var\(--easing-", "var(--theme-transition-easing-"),
    (r"var\(--transition-", "var(--theme-transition-"),
    # Z-index
    (r"var\(--z-", "var(--theme-z-"),
]

# Valid breakpoint names for responsive tokens.
VALID_BREAKPOINTS = {
    "mobile": None,  # Base (no media query)
    "tablet": "768px",
    "desktop": "1024px",
    "sm": "640px",
    "md": "768px",
    "lg": "1024px",
    "xl": "1280px",
    "2xl": "1536px",
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_tokens_css(
    tokens_source: str | Path | dict,
    theme_name: str,
    dark_mode_enabled: bool = True,
) -> str:
    """Generate CSS custom-property declarations from a tokens source.

    Args:
        tokens_source: One of:
            - A ``pathlib.Path`` or string path pointing to a ``tokens.json`` file.
            - A ``dict`` already containing the parsed tokens.
        theme_name: Human-readable theme slug (e.g. ``"modern-shop"``).
            Used only in the generated CSS header comment.
        dark_mode_enabled: If ``False``, skip dark mode token generation and
            dark mode media queries entirely. Themes with ``features.dark_mode: false``
            in their manifest should pass ``False``.

    Returns:
        A complete CSS string ready to be written to ``tokens.css``.

    Supports responsive tokens -- values can be either:
    - Flat strings (apply to all devices)
    - Objects with breakpoint keys (e.g. ``{"mobile": "14px", "desktop": "16px"}``)
    """
    if isinstance(tokens_source, dict):
        tokens = tokens_source
    else:
        tokens_path = Path(tokens_source)
        with open(tokens_path) as f:
            tokens = json.load(f)

    # Collect responsive tokens for media query generation
    responsive_tokens: dict = {}

    lines = [
        "/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */",
        "",
        "/**",
        f" * {theme_name.replace('-', ' ').title()} Theme - Design Tokens as CSS Custom Properties",
        f" * Generated from tokens.json on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        " * DO NOT EDIT MANUALLY - Edit tokens.json instead and regenerate",
        " */",
        "",
        ":root {",
    ]

    # Process each token category
    if "colors" in tokens:
        lines.extend(_generate_colors_section(tokens["colors"]))

    if "dark" in tokens and dark_mode_enabled:
        lines.extend(_generate_dark_section(tokens["dark"]))

    if "typography" in tokens:
        lines.extend(_generate_typography_section(tokens["typography"]))

    if "spacing" in tokens:
        lines.extend(_generate_spacing_section(tokens["spacing"]))

    if "borders" in tokens:
        lines.extend(_generate_borders_section(tokens["borders"]))

    if "shadows" in tokens:
        lines.extend(_generate_shadows_section(tokens["shadows"]))

    if "transitions" in tokens:
        lines.extend(_generate_transitions_section(tokens["transitions"]))

    if "breakpoints" in tokens:
        lines.extend(_generate_breakpoints_section(tokens["breakpoints"]))

    if "responsive" in tokens:
        lines.extend(_generate_responsive_section(tokens["responsive"]))

    if "z-index" in tokens:
        lines.extend(_generate_zindex_section(tokens["z-index"]))

    if "container" in tokens:
        lines.extend(_generate_container_section(tokens["container"]))

    # Menu tokens (supports responsive values)
    if "menu" in tokens:
        lines.extend(_generate_menu_section(tokens["menu"], responsive_tokens))

    # Header tokens
    if "header" in tokens:
        lines.extend(_generate_header_section(tokens["header"]))

    # Footer tokens
    if "footer" in tokens:
        lines.extend(_generate_footer_section(tokens["footer"]))

    # Search tokens
    if "search" in tokens:
        lines.extend(_generate_search_section(tokens["search"]))

    # Button color variant tokens
    button_variants = ["button-primary", "button-secondary", "button-neutral", "button-danger"]
    has_button_variants = any(variant in tokens for variant in button_variants)
    if has_button_variants:
        lines.extend(_generate_button_variants_section(tokens, button_variants))

    # Card style variant tokens
    card_variants = ["card-default", "card-elevated", "card-bordered", "card-minimal"]
    has_card_variants = any(variant in tokens for variant in card_variants)
    if has_card_variants:
        lines.extend(_generate_card_variants_section(tokens, card_variants))

    # Element tokens for page builder elements (supports responsive values)
    if "elements" in tokens:
        lines.extend(_generate_elements_section(tokens["elements"], responsive_tokens))

    # Widget tokens for header/footer widgets (supports responsive values)
    if "widgets" in tokens:
        lines.extend(_generate_widgets_section(tokens["widgets"], responsive_tokens))

    lines.append("}")

    # Add responsive container padding if container tokens exist
    if "container" in tokens:
        lines.extend(_generate_responsive_container())

    # Add responsive media queries for any responsive tokens
    lines.extend(_generate_responsive_media_queries(responsive_tokens))

    # Add dark mode media queries if dark tokens exist and dark mode is enabled
    if "dark" in tokens and dark_mode_enabled:
        original_colors = tokens.get("colors", {})
        original_shadows = tokens.get("shadows", {})
        lines.extend(
            _generate_dark_mode_media_queries(tokens["dark"], original_colors, original_shadows)
        )

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _transform_value_references(value: str) -> str:
    """Transform legacy var() references to --theme- prefixed versions.

    This ensures that token values referencing other tokens use the
    correct --theme- prefix naming convention.

    Example::

        'var(--color-primary)' -> 'var(--theme-color-primary)'
        'var(--space-4)' -> 'var(--theme-space-4)'
    """
    if not isinstance(value, str) or "var(--" not in value:
        return value

    result = value
    for pattern, replacement in VAR_REFERENCE_PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result


def _is_responsive_value(value) -> bool:
    """Check if a value is a responsive object (has breakpoint keys)."""
    if not isinstance(value, dict):
        return False
    return any(key in VALID_BREAKPOINTS for key in value)


def _get_base_value(responsive_value: dict) -> str:
    """Get the base (mobile-first) value from a responsive object."""
    # Priority: mobile > sm > first available value
    if "mobile" in responsive_value:
        return responsive_value["mobile"]
    if "sm" in responsive_value:
        return responsive_value["sm"]
    # Return first available value
    return list(responsive_value.values())[0]


def _collect_responsive_values(css_var: str, responsive_value: dict, responsive_tokens: dict):
    """Collect responsive values into media query buckets."""
    for breakpoint, value in responsive_value.items():
        if breakpoint in ("mobile", "sm"):
            continue  # Base value, no media query needed
        min_width = VALID_BREAKPOINTS.get(breakpoint)
        if min_width:
            if min_width not in responsive_tokens:
                responsive_tokens[min_width] = []
            responsive_tokens[min_width].append(f"    {css_var}: {value};")


# ---------------------------------------------------------------------------
# Section generators
# ---------------------------------------------------------------------------


def _generate_colors_section(colors: dict) -> list:
    """Generate color variables with --theme-color-{name} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Colors",
        "     ========================================================================== */",
        "",
    ]

    # Group colors by category
    categories = {
        "Primary": ["primary", "primary-hover", "primary-light"],
        "Secondary": ["secondary", "secondary-hover"],
        "Accent": ["accent", "accent-hover"],
        "Text": ["text", "text-light", "text-muted", "text-inverse"],
        "Background": ["background", "background-alt"],
        "Surface": ["surface", "surface-hover"],
        "Border": ["border", "border-light", "border-dark"],
        "Status": [
            "success",
            "success-light",
            "error",
            "error-light",
            "warning",
            "warning-light",
            "info",
            "info-light",
        ],
        "Overlay": ["overlay"],
    }

    for category, keys in categories.items():
        category_colors = {k: v for k, v in colors.items() if k in keys}
        if category_colors:
            lines.append(f"  /* {category} */")
            for key in keys:
                if key in colors:
                    value = _transform_value_references(colors[key])
                    lines.append(f"  --theme-color-{key}: {value};")
            lines.append("")

    # Add any remaining colors not in categories
    remaining = {k: v for k, v in colors.items() if k not in sum(categories.values(), [])}
    if remaining:
        lines.append("  /* Other */")
        for key, value in remaining.items():
            value = _transform_value_references(value)
            lines.append(f"  --theme-color-{key}: {value};")
        lines.append("")

    return lines


def _generate_dark_section(dark: dict) -> list:
    """Generate dark mode color variables with --theme-dark-{name} prefix.

    Dark token keys mirror the ``colors`` section keys (e.g. ``background``,
    ``text``, ``border``) so the CSS generator can dynamically map
    ``dark.{key}`` -> override of ``--theme-color-{key}``.

    Shadow dark tokens use ``shadow-`` prefix and map to ``--theme-shadow-*``.
    Tokens with ``None`` / ``null`` values are skipped (keep light mode value).
    """
    lines = [
        "  /* ==========================================================================",
        "     Dark Mode Colors",
        "     ========================================================================== */",
        "",
    ]

    # Group dark tokens by category
    categories = {
        "Background": ["background", "background-secondary", "background-tertiary"],
        "Surface": ["surface", "surface-secondary", "surface-hover"],
        "Text": ["text", "text-light", "text-muted", "text-inverse"],
        "Border": ["border", "border-light", "border-dark"],
        "Primary": ["primary-light"],
        "Status": ["success-light", "error-light", "warning-light", "info-light"],
        "Overlay": ["overlay"],
        "Shadow": ["shadow-sm", "shadow-base", "shadow-md", "shadow-lg", "shadow-xl"],
    }

    all_categorised_keys = set()
    for category, keys in categories.items():
        category_tokens = {k: v for k, v in dark.items() if k in keys and v is not None}
        if category_tokens:
            lines.append(f"  /* {category} */")
            for key in keys:
                if key in dark and dark[key] is not None:
                    value = _transform_value_references(dark[key])
                    if key.startswith("shadow-"):
                        lines.append(f"  --theme-dark-{key}: {value};")
                    else:
                        lines.append(f"  --theme-dark-{key}: {value};")
            lines.append("")
        all_categorised_keys.update(keys)

    # Add any remaining dark tokens not in predefined categories
    remaining = {k: v for k, v in dark.items() if k not in all_categorised_keys and v is not None}
    if remaining:
        lines.append("  /* Other */")
        for key, value in remaining.items():
            value = _transform_value_references(value)
            lines.append(f"  --theme-dark-{key}: {value};")
        lines.append("")

    return lines


def _generate_typography_section(typography: dict) -> list:
    """Generate typography variables with --theme- prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Typography",
        "     ========================================================================== */",
        "",
    ]

    # Group by type
    groups = {
        "Font Families": [
            "font-sans",
            "font-serif",
            "font-mono",
            "font-family-body",
            "font-family-heading",
        ],
        "Font Sizes": [k for k in typography if k.startswith("font-size")],
        "Font Weights": [k for k in typography if k.startswith("font-weight")],
        "Line Heights": [k for k in typography if k.startswith("line-height")],
        "Letter Spacing": [k for k in typography if k.startswith("letter-spacing")],
    }

    for group_name, keys in groups.items():
        group_tokens = {k: v for k, v in typography.items() if k in keys}
        if group_tokens:
            lines.append(f"  /* {group_name} */")
            for key in keys:
                if key in typography:
                    value = _transform_value_references(typography[key])
                    lines.append(f"  --theme-{key}: {value};")
            lines.append("")

    return lines


def _generate_spacing_section(spacing: dict) -> list:
    """Generate spacing variables with --theme-space-{size} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Spacing",
        "     ========================================================================== */",
    ]

    # Sort by numeric value
    sorted_keys = sorted(spacing.keys(), key=lambda x: int(x) if x.isdigit() else 0)
    for key in sorted_keys:
        value = _transform_value_references(spacing[key])
        lines.append(f"  --theme-space-{key}: {value};")

    lines.append("")
    return lines


def _generate_borders_section(borders: dict) -> list:
    """Generate border variables with --theme- prefix (width and radius)."""
    lines = [
        "  /* ==========================================================================",
        "     Borders",
        "     ========================================================================== */",
        "",
    ]

    # Border widths
    width_keys = [k for k in borders if k.startswith("width")]
    if width_keys:
        lines.append("  /* Border Widths */")
        for key in sorted(width_keys):
            value = _transform_value_references(borders[key])
            lines.append(f"  --theme-border-{key}: {value};")
        lines.append("")

    # Border radius
    radius_keys = [k for k in borders if k.startswith("radius")]
    if radius_keys:
        lines.append("  /* Border Radius */")
        for key in radius_keys:
            value = _transform_value_references(borders[key])
            lines.append(f"  --theme-{key}: {value};")
        lines.append("")

    return lines


def _generate_shadows_section(shadows: dict) -> list:
    """Generate shadow variables with --theme-shadow-{name} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Shadows",
        "     ========================================================================== */",
    ]

    for key, value in shadows.items():
        value = _transform_value_references(value)
        lines.append(f"  --theme-shadow-{key}: {value};")

    lines.append("")
    return lines


def _generate_transitions_section(transitions: dict) -> list:
    """Generate transition variables with --theme-transition-{name} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Transitions",
        "     ========================================================================== */",
    ]

    for key, value in transitions.items():
        value = _transform_value_references(value)
        lines.append(f"  --theme-transition-{key}: {value};")

    lines.append("")
    return lines


def _generate_breakpoints_section(breakpoints: dict) -> list:
    """Generate breakpoint variables with --theme-breakpoint-{name} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Breakpoints",
        "     ========================================================================== */",
    ]

    for key, value in breakpoints.items():
        value = _transform_value_references(value)
        lines.append(f"  --theme-breakpoint-{key}: {value};")

    lines.append("")
    return lines


def _generate_responsive_section(responsive: dict) -> list:
    """Generate responsive scale variables with --theme-responsive-{name} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Responsive Scaling",
        "     ========================================================================== */",
    ]

    for key, value in responsive.items():
        value = _transform_value_references(value)
        lines.append(f"  --theme-responsive-{key}: {value};")

    lines.append("")
    return lines


def _generate_zindex_section(zindex: dict) -> list:
    """Generate z-index variables with --theme-z-{name} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Z-Index",
        "     ========================================================================== */",
    ]

    for key, value in zindex.items():
        value = _transform_value_references(str(value))
        lines.append(f"  --theme-z-{key}: {value};")

    lines.append("")
    return lines


def _generate_container_section(container: dict) -> list:
    """Generate container variables with --theme-container-{name} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Container",
        "     ========================================================================== */",
    ]

    for key, value in container.items():
        value = _transform_value_references(value)
        lines.append(f"  --theme-container-{key}: {value};")

    lines.append("")
    return lines


def _generate_responsive_container() -> list:
    """Generate responsive container padding media queries."""
    return [
        "",
        "/* Responsive container padding */",
        "@media (min-width: 640px) {",
        "  :root {",
        "    --theme-container-padding: 1.5rem;",
        "  }",
        "}",
        "",
        "@media (min-width: 1024px) {",
        "  :root {",
        "    --theme-container-padding: 2rem;",
        "  }",
        "}",
    ]


def _generate_menu_section(menu: dict, responsive_tokens: dict) -> list:
    """Generate menu token variables with --theme-menu-{name} prefix.

    Supports both flat values and responsive objects.
    Responsive values are collected into responsive_tokens for media query generation.
    """
    lines = [
        "  /* ==========================================================================",
        "     Menu",
        "     ========================================================================== */",
    ]

    for key, value in menu.items():
        if _is_responsive_value(value):
            # Responsive token - get base value and collect breakpoint values
            base_value = _transform_value_references(_get_base_value(value))
            lines.append(f"  --theme-menu-{key}: {base_value};")
            # Collect responsive values for media queries (transform each value)
            transformed_value = {k: _transform_value_references(v) for k, v in value.items()}
            _collect_responsive_values(f"--theme-menu-{key}", transformed_value, responsive_tokens)
        else:
            # Flat value
            value = _transform_value_references(value)
            lines.append(f"  --theme-menu-{key}: {value};")

    lines.append("")
    return lines


def _generate_header_section(header: dict) -> list:
    """Generate header token variables with --theme-header-{name} prefix.

    Also handles nested zones: --theme-header-zones-{zone}-{property}
    """
    lines = [
        "  /* ==========================================================================",
        "     Header",
        "     ========================================================================== */",
    ]

    # First, output flat header tokens (excluding 'zones')
    for key, value in header.items():
        if key == "zones":
            continue  # Handle zones separately
        value = _transform_value_references(value)
        lines.append(f"  --theme-header-{key}: {value};")

    lines.append("")

    # Handle nested zones
    if "zones" in header:
        lines.append("  /* Header Zones */")
        for zone_name, zone_props in header["zones"].items():
            if isinstance(zone_props, dict):
                for prop_name, prop_value in zone_props.items():
                    prop_value = _transform_value_references(prop_value)
                    lines.append(f"  --theme-header-zones-{zone_name}-{prop_name}: {prop_value};")
                lines.append("")

    return lines


def _generate_footer_section(footer: dict) -> list:
    """Generate footer token variables with --theme-footer-{name} prefix.

    Also handles nested zones: --theme-footer-zones-{zone}-{property}
    """
    lines = [
        "  /* ==========================================================================",
        "     Footer",
        "     ========================================================================== */",
    ]

    # First, output flat footer tokens (excluding 'zones')
    for key, value in footer.items():
        if key == "zones":
            continue  # Handle zones separately
        value = _transform_value_references(value)
        lines.append(f"  --theme-footer-{key}: {value};")

    lines.append("")

    # Handle nested zones
    if "zones" in footer:
        lines.append("  /* Footer Zones */")
        for zone_name, zone_props in footer["zones"].items():
            if isinstance(zone_props, dict):
                for prop_name, prop_value in zone_props.items():
                    prop_value = _transform_value_references(prop_value)
                    lines.append(f"  --theme-footer-zones-{zone_name}-{prop_name}: {prop_value};")
                lines.append("")

    return lines


def _generate_search_section(search: dict) -> list:
    """Generate search token variables with --theme-search-{name} prefix."""
    lines = [
        "  /* ==========================================================================",
        "     Search",
        "     ========================================================================== */",
    ]

    for key, value in search.items():
        value = _transform_value_references(value)
        lines.append(f"  --theme-search-{key}: {value};")

    lines.append("")
    return lines


def _generate_button_variants_section(tokens: dict, variant_keys: list) -> list:
    """Generate button color variant tokens with --theme-element-button-{color}-{style}-{prop} prefix.

    This generates tokens for button style variants (solid, outline, ghost) across
    different color variants (primary, secondary, neutral, danger).

    Example output::

        --theme-element-button-primary-solid-bg: var(--theme-color-primary);
        --theme-element-button-primary-outline-text: var(--theme-color-primary);
    """
    lines = [
        "  /* ==========================================================================",
        "     Button Color Variants",
        "     ========================================================================== */",
        "",
    ]

    # Process each button variant
    for variant_key in variant_keys:
        if variant_key not in tokens:
            continue

        # Extract color name from key (e.g., "button-primary" -> "primary")
        color_name = variant_key.replace("button-", "")
        display_name = color_name.title()
        variant_tokens = tokens[variant_key]

        lines.append(f"  /* {display_name} */")
        for key, value in variant_tokens.items():
            # key format: "solid-bg", "outline-text", "ghost-bg-hover", etc.
            value = _transform_value_references(value)
            lines.append(f"  --theme-element-button-{color_name}-{key}: {value};")
        lines.append("")

    return lines


def _generate_card_variants_section(tokens: dict, variant_keys: list) -> list:
    """Generate card style variant tokens with --theme-element-card-{style}-{prop} prefix.

    This generates tokens for card style variants (default, elevated, bordered, minimal).

    Example output::

        --theme-element-card-default-bg: var(--theme-color-surface);
        --theme-element-card-elevated-shadow: var(--theme-shadow-md);
    """
    lines = [
        "  /* ==========================================================================",
        "     Card Style Variants",
        "     ========================================================================== */",
        "",
    ]

    # Process each card variant
    for variant_key in variant_keys:
        if variant_key not in tokens:
            continue

        # Extract style name from key (e.g., "card-default" -> "default")
        style_name = variant_key.replace("card-", "")
        display_name = style_name.title()
        variant_tokens = tokens[variant_key]

        lines.append(f"  /* {display_name} */")
        for key, value in variant_tokens.items():
            value = _transform_value_references(value)
            lines.append(f"  --theme-element-card-{style_name}-{key}: {value};")
        lines.append("")

    return lines


def _generate_elements_section(elements: dict, responsive_tokens: dict) -> list:
    """Generate element token variables with --theme-element-{category}-{name} prefix.

    Element tokens provide default styling for page builder elements.
    They follow a three-level cascade: instance override > element token > base token.
    Supports both flat values and responsive objects.
    """
    lines = [
        "  /* ==========================================================================",
        "     Element Tokens (Page Builder)",
        "     ========================================================================== */",
        "",
    ]

    # Define display order and descriptions for element categories
    category_order = [
        ("hero", "Hero Section"),
        ("button", "Button"),
        ("card", "Card (Shared)"),
        ("divider", "Divider"),
        ("form", "Form"),
        ("accordion", "Accordion"),
        ("modal", "Modal"),
        ("countdown", "Countdown"),
        ("testimonial", "Testimonial"),
        ("blog", "Blog"),
        ("product", "Product"),
        ("category", "Category"),
        ("voucher", "Voucher"),
        ("heading", "Heading"),
        ("image", "Image"),
        ("gallery", "Gallery"),
    ]

    def _process_element_category(category, cat_tokens):
        for key, value in cat_tokens.items():
            css_var = f"--theme-element-{category}-{key}"
            if _is_responsive_value(value):
                base_value = _transform_value_references(_get_base_value(value))
                lines.append(f"  {css_var}: {base_value};")
                transformed = {k: _transform_value_references(v) for k, v in value.items()}
                _collect_responsive_values(css_var, transformed, responsive_tokens)
            else:
                value = _transform_value_references(value)
                lines.append(f"  {css_var}: {value};")

    # Process categories in order
    processed_categories = set()
    for category, display_name in category_order:
        if category in elements:
            lines.append(f"  /* {display_name} */")
            _process_element_category(category, elements[category])
            lines.append("")
            processed_categories.add(category)

    # Process any remaining categories not in the predefined order
    remaining = {k: v for k, v in elements.items() if k not in processed_categories}
    for category, tokens in remaining.items():
        display_name = category.replace("-", " ").title()
        lines.append(f"  /* {display_name} */")
        _process_element_category(category, tokens)
        lines.append("")

    return lines


def _generate_widgets_section(widgets: dict, responsive_tokens: dict) -> list:
    """Generate widget token variables with --theme-widget-{name}-{prop} prefix.

    Widget tokens provide default styling for header/footer widgets.
    This allows themes to customize widget appearance without editing CSS.
    Supports both flat values and responsive objects.
    """
    lines = [
        "  /* ==========================================================================",
        "     Widget Tokens (Header/Footer)",
        "     ========================================================================== */",
        "",
    ]

    # Define display order for widget categories
    widget_order = [
        ("account", "Account"),
        ("cart", "Cart"),
        ("language", "Language"),
        ("currency", "Currency"),
        ("logo", "Logo"),
        ("announcement", "Announcement"),
        ("newsletter", "Newsletter"),
        ("social", "Social"),
        ("social-share", "Social Share"),
        ("links", "Links"),
        ("text", "Text"),
        ("payment", "Payment"),
        ("trust-badges", "Trust Badges"),
        ("contact", "Contact"),
    ]

    def _process_widget(w_name, w_tokens):
        for key, value in w_tokens.items():
            css_var = f"--theme-widget-{w_name}-{key}"
            if _is_responsive_value(value):
                base_value = _transform_value_references(_get_base_value(value))
                lines.append(f"  {css_var}: {base_value};")
                transformed = {k: _transform_value_references(v) for k, v in value.items()}
                _collect_responsive_values(css_var, transformed, responsive_tokens)
            else:
                value = _transform_value_references(value)
                lines.append(f"  {css_var}: {value};")

    # Process widgets in order
    processed_widgets = set()
    for widget_name, display_name in widget_order:
        if widget_name in widgets:
            lines.append(f"  /* {display_name} Widget */")
            _process_widget(widget_name, widgets[widget_name])
            lines.append("")
            processed_widgets.add(widget_name)

    # Process any remaining widgets not in the predefined order
    remaining = {k: v for k, v in widgets.items() if k not in processed_widgets}
    for widget_name, tokens in remaining.items():
        display_name = widget_name.replace("-", " ").title()
        lines.append(f"  /* {display_name} Widget */")
        _process_widget(widget_name, tokens)
        lines.append("")

    return lines


def _generate_responsive_media_queries(responsive_tokens: dict) -> list:
    """Generate media queries for responsive tokens."""
    if not responsive_tokens:
        return []

    lines = [
        "",
        "/* ==========================================================================",
        "   Responsive Token Overrides",
        "   ========================================================================== */",
    ]

    # Sort by min-width value
    sorted_breakpoints = sorted(responsive_tokens.keys(), key=lambda x: int(x.replace("px", "")))

    for min_width in sorted_breakpoints:
        vars_list = responsive_tokens[min_width]
        if vars_list:
            lines.append("")
            lines.append(f"@media (min-width: {min_width}) {{")
            lines.append("  :root {")
            lines.extend(vars_list)
            lines.append("  }")
            lines.append("}")

    return lines


def _generate_dark_mode_media_queries(
    dark_tokens: dict,
    original_colors: dict,
    original_shadows: dict,
) -> list:
    """Generate dark mode CSS variable overrides using prefers-color-scheme.

    Dynamically maps all dark tokens to their ``--theme-color-*`` counterparts.
    Shadow dark tokens (keys starting with ``shadow-``) map to ``--theme-shadow-*``.
    Tokens with ``None`` / ``null`` values are skipped (keep light mode value).

    Args:
        dark_tokens: The ``dark`` section from tokens.json.
        original_colors: The ``colors`` section from tokens.json, used to
            restore light mode when ``[data-theme="light"]`` is set.
        original_shadows: The ``shadows`` section from tokens.json, used to
            restore shadow values in ``[data-theme="light"]`` mode.
    """
    # Build override mappings: (css-var-to-override, dark-var-reference)
    overrides = []
    for key, value in dark_tokens.items():
        if value is None:
            continue
        if key.startswith("shadow-"):
            shadow_name = key[7:]  # Strip 'shadow-' prefix
            overrides.append(
                (
                    f"--theme-shadow-{shadow_name}",
                    f"var(--theme-dark-{key})",
                )
            )
        else:
            overrides.append(
                (
                    f"--theme-color-{key}",
                    f"var(--theme-dark-{key})",
                )
            )

    if not overrides:
        return []

    lines = [
        "",
        "/* ==========================================================================",
        "   Dark Mode Support",
        "   ========================================================================== */",
        "",
        "/* Automatic dark mode based on system preference */",
        "@media (prefers-color-scheme: dark) {",
        "  :root {",
    ]
    for css_var, dark_ref in overrides:
        lines.append(f"    {css_var}: {dark_ref};")
    lines.extend(
        [
            "  }",
            "}",
            "",
            "/* Manual dark mode toggle support */",
            '[data-theme="dark"] {',
        ]
    )
    for css_var, dark_ref in overrides:
        lines.append(f"  {css_var}: {dark_ref};")
    lines.extend(
        [
            "}",
            "",
            "/* Force light mode when explicitly set (overrides system preference) */",
            '[data-theme="light"] {',
            "  /* Restore original light theme colors - overrides prefers-color-scheme */",
        ]
    )
    # Restore original values
    for css_var, _ in overrides:
        if css_var.startswith("--theme-shadow-"):
            shadow_name = css_var.replace("--theme-shadow-", "")
            original_value = original_shadows.get(shadow_name)
        else:
            color_key = css_var.replace("--theme-color-", "")
            original_value = original_colors.get(color_key)
        if original_value:
            lines.append(f"  {css_var}: {original_value};")
    lines.extend(
        [
            "  color-scheme: light;",
            "}",
        ]
    )

    return lines
