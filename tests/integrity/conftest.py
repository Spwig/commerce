"""
Integrity test fixtures
"""

import json
from pathlib import Path

import pytest
from django.conf import settings


@pytest.fixture
def all_theme_tokens():
    """Load tokens.json from all 6 themes.

    Themes live in the external ``spwig-components`` repo (see project
    CLAUDE.md — "Themes live in Spwig/components, not in this repo").
    ``settings.SPWIG_COMPONENTS_DIR`` points at that checkout.
    """
    components_dir = Path(getattr(settings, "SPWIG_COMPONENTS_DIR", ""))
    themes_root = components_dir / "themes"
    theme_names = [
        "starter",
        "modern-shop",
        "modern-dark",
        "elegant-shop",
        "tech-theme",
        "apparel-theme",
    ]

    tokens = {}
    for theme_name in theme_names:
        # tokens.json now lives directly under each theme dir (no
        # versioned subdir). Fall back to the legacy 1.0.0 layout for
        # any theme still packaged the old way.
        candidates = [
            themes_root / theme_name / "tokens.json",
            themes_root / theme_name / "1.0.0" / "tokens.json",
        ]
        for tokens_file in candidates:
            if tokens_file.exists():
                with open(tokens_file) as f:
                    tokens[theme_name] = json.load(f)
                break

    return tokens
