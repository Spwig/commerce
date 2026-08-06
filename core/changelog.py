"""Local platform changelog access.

Parses the ``CHANGELOG.md`` that ships inside every Spwig build so the admin
upgrade pages can always show release notes — even for installs that build
their own image from the public GitHub repo and never receive changelog text
from the update server.

The update server is the primary source of "what's new" for a *target*
version (populated at publish time by ``register_platform_version``). This
module is the fallback: it reads the changelog bundled with the running code,
keyed by version, so a merchant is never left staring at an empty "What's New"
panel.

``CHANGELOG.md`` follows Keep a Changelog: newest-first level-2 sections of the
form ``## [X.Y.Z] - YYYY-MM-DD`` whose body runs until the next ``## [``.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings

# Version-section heading, e.g. "## [1.7.1] - 2026-07-28". The date is optional
# so an unreleased/undated entry still parses.
_SECTION_RE = re.compile(
    r"^##\s+\[(?P<version>[^\]]+)\]\s*(?:-\s*(?P<date>\d{4}-\d{2}-\d{2}))?\s*$"
)


def _changelog_path() -> Path:
    """Return the path to the bundled CHANGELOG.md (may not exist)."""
    return Path(settings.BASE_DIR) / "CHANGELOG.md"


@dataclass
class ChangelogEntry:
    """One version's section of the changelog."""

    version: str
    date: str | None
    notes: str  # Full section body as raw markdown (heading line excluded).
    summary: str  # Leading prose paragraph, if any (short user-facing blurb).


def get_changelog_entry(version: str) -> ChangelogEntry | None:
    """Return the bundled changelog entry for ``version``, or ``None``.

    ``version`` is matched exactly against the ``## [version]`` heading. A
    leading ``v`` on either side is tolerated. Returns ``None`` when the file
    is absent (e.g. a stripped image) or the version has no section.
    """
    if not version:
        return None

    path = _changelog_path()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    wanted = version.lstrip("vV").strip()

    lines = text.splitlines()
    start = None
    heading = None
    for i, line in enumerate(lines):
        m = _SECTION_RE.match(line)
        if m and m.group("version").lstrip("vV").strip() == wanted:
            start = i
            heading = m
            break

    if start is None:
        return None

    # Body runs until the next version heading (or EOF).
    body_lines: list[str] = []
    for line in lines[start + 1 :]:
        if _SECTION_RE.match(line):
            break
        body_lines.append(line)

    notes = "\n".join(body_lines).strip("\n")
    summary = _leading_prose(body_lines)

    return ChangelogEntry(
        version=heading.group("version").strip(),
        date=heading.group("date"),
        notes=notes,
        summary=summary,
    )


def _leading_prose(body_lines: list[str]) -> str:
    """Extract the first prose paragraph before any ``###`` / list block."""
    prose: list[str] = []
    for line in body_lines:
        stripped = line.strip()
        if not stripped:
            if prose:
                break
            continue
        if stripped.startswith("#") or stripped.startswith(("-", "*")):
            break
        prose.append(stripped)
    return " ".join(prose)


# --- Rendering -------------------------------------------------------------

_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_CODE_RE = re.compile(r"`([^`]+)`")


def _inline(text: str) -> str:
    """Escape a line and apply the inline markdown subset used in the changelog."""
    out = html.escape(text)
    out = _BOLD_RE.sub(r"<strong>\1</strong>", out)
    out = _CODE_RE.sub(r"<code>\1</code>", out)
    return out


def render_changelog_html(markdown_text: str) -> str:
    """Render the changelog markdown subset to safe HTML.

    Handles exactly what CHANGELOG.md uses — ``###``/``####`` headings, ``-``/
    ``*`` bullet lists, ``**bold**``, ``` `code` ```, and prose paragraphs — and
    HTML-escapes everything first, so the result is safe to mark ``|safe`` even
    though the source is maintainer-authored. Returns ``""`` for empty input.
    """
    if not markdown_text or not markdown_text.strip():
        return ""

    parts: list[str] = []
    para: list[str] = []
    in_list = False

    def close_para() -> None:
        nonlocal para
        if para:
            parts.append("<p>" + " ".join(_inline(p) for p in para) + "</p>")
            para = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            parts.append("</ul>")
            in_list = False

    for raw in markdown_text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            close_para()
            close_list()
            continue

        heading = re.match(r"^(#{3,6})\s+(.*)$", stripped)
        if heading:
            close_para()
            close_list()
            level = min(len(heading.group(1)) + 1, 6)  # ### -> h4
            parts.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
            continue

        bullet = re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet:
            close_para()
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{_inline(bullet.group(1))}</li>")
            continue

        # Prose line.
        close_list()
        para.append(stripped)

    close_para()
    close_list()
    return "\n".join(parts)
