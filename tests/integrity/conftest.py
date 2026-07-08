"""
Integrity test fixtures
"""
import pytest
import json
from pathlib import Path

from django.conf import settings


@pytest.fixture
def all_theme_tokens():
    """Load tokens.json from all 6 themes"""
    themes_root = Path(settings.BASE_DIR) / 'components' / 'themes'
    theme_names = [
        'starter', 'modern-shop', 'modern-dark',
        'elegant-shop', 'tech-theme', 'apparel-theme'
    ]

    tokens = {}
    for theme_name in theme_names:
        tokens_file = themes_root / theme_name / '1.0.0' / 'tokens.json'
        if tokens_file.exists():
            with open(tokens_file, 'r') as f:
                tokens[theme_name] = json.load(f)

    return tokens
