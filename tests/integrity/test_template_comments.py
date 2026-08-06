"""
Template comment safety tests.

Django's ``{# ... #}`` inline comment is **single-line only** — the template
lexer's comment pattern is not DOTALL, so a ``{# ... #}`` that spans more than
one physical line is not recognised as a comment. Its text (and any inner
``{% ... %}`` / ``{{ ... }}``) then leaks into the rendered page.

This has shipped to the storefront UI twice. This test fails the build if any
Spwig template contains a multi-line ``{# ... #}`` comment, so it can never
reach the UI again. The fix is always to use ``{% comment %} ... {% endcomment %}``
for multi-line comments (or collapse the comment onto a single line).
"""

import os
import re
from pathlib import Path

import pytest
from django.conf import settings

pytestmark = pytest.mark.integrity

BASE_DIR = Path(settings.BASE_DIR).resolve()

# Directories that are not Spwig source templates: virtualenvs, JS deps,
# collected static, generated/gitignored component payloads, caches. Pruned so
# the walk is fast and deterministic (a fresh CI clone has no components_data).
_EXCLUDE_DIRS = {
    ".git",
    "shop_venv",
    ".venv",
    "venv",
    "node_modules",
    "staticfiles",
    "__pycache__",
    "media",
    ".pytest_cache",
    "htmlcov",
    "components_data",
    ".mypy_cache",
    ".ruff_cache",
}
_TEMPLATE_EXTS = (".html", ".txt")

# Non-greedy so each ``{# ... #}`` matches up to its own nearest ``#}``; DOTALL
# so a match can straddle newlines — that straddle is exactly the bug.
_COMMENT_SPAN = re.compile(r"\{#.*?#\}", re.DOTALL)


def _iter_template_files():
    """Yield Spwig template files (``*.html`` / ``*.txt`` under a ``templates`` dir)."""
    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        dirnames[:] = [d for d in dirnames if d not in _EXCLUDE_DIRS]
        for name in filenames:
            if not name.endswith(_TEMPLATE_EXTS):
                continue
            path = Path(dirpath) / name
            if "templates" not in path.relative_to(BASE_DIR).parts:
                continue
            yield path


def _multiline_comments(path):
    """Return ``[(lineno, snippet), ...]`` for multi-line ``{# #}`` comments in ``path``."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if "{#" not in text:
        return []
    hits = []
    for m in _COMMENT_SPAN.finditer(text):
        if "\n" in m.group():
            lineno = text.count("\n", 0, m.start()) + 1
            snippet = " ".join(m.group().split())
            hits.append((lineno, snippet[:117] + "..." if len(snippet) > 120 else snippet))
    return hits


class TestTemplateComments:
    """Multi-line ``{# #}`` comments render as literal text — never allow them."""

    def test_no_multiline_django_comments(self):
        offenders = []
        for path in _iter_template_files():
            for lineno, snippet in _multiline_comments(path):
                offenders.append(f"{path.relative_to(BASE_DIR)}:{lineno}: {snippet}")

        assert not offenders, (
            "Multi-line `{# #}` template comments found — Django's `{# #}` is "
            "single-line only, so these render as literal text in the UI. Use "
            "`{% comment %} ... {% endcomment %}` (or a single line) instead:\n  "
            + "\n  ".join(offenders)
        )
