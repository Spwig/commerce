"""Unit tests for ``core.changelog`` — the local CHANGELOG.md fallback that
populates the admin upgrade pages' "What's New" panel.

Two surfaces are covered:

* ``get_changelog_entry`` — parses the bundled ``CHANGELOG.md`` (Keep a
  Changelog ``## [X.Y.Z] - YYYY-MM-DD`` sections) into a ``ChangelogEntry``.
* ``render_changelog_html`` — renders the changelog's markdown subset to
  HTML. Its output is emitted with ``|safe`` on the upgrade page, so the
  HTML-escaping behaviour here is a security invariant, not a nicety.

Both surfaces are pure functions with no DB access. ``get_changelog_entry``
reads a file via the ``core.changelog._changelog_path`` helper, which every
test monkeypatches to a fixture written under ``tmp_path`` so the real repo
CHANGELOG.md never influences (or breaks) these assertions.
"""

import pytest

from core import changelog
from core.changelog import (
    ChangelogEntry,
    get_changelog_entry,
    render_changelog_html,
)

pytestmark = [pytest.mark.unit, pytest.mark.core]


# A two-section fixture. The 1.8.0 body carries a leading prose summary, then
# ``###`` subsections with bold/code inline markup; 1.7.1 follows so we can
# assert the parser stops the first section's body at the next ``## [`` line.
FIXTURE_CHANGELOG = """# Changelog

Intro prose that belongs to no version section.

## [1.8.0] - 2026-08-01

This release does the thing. It also does another thing.

### Added

- Feature A with **bold** text
- Feature B

### Fixed

- Bug with `code` reference

## [1.7.1] - 2026-07-28

An earlier release summary line.

### Changed

- An old change from the previous release
"""


@pytest.fixture
def changelog_file(tmp_path, monkeypatch):
    """Write FIXTURE_CHANGELOG to a temp file and point the path helper at it."""
    path = tmp_path / "CHANGELOG.md"
    path.write_text(FIXTURE_CHANGELOG, encoding="utf-8")
    monkeypatch.setattr(changelog, "_changelog_path", lambda: path)
    return path


class TestGetChangelogEntry:
    """Behaviour of ``get_changelog_entry`` against a controlled fixture file."""

    def test_existing_version_parses_all_fields(self, changelog_file):
        entry = get_changelog_entry("1.8.0")

        assert isinstance(entry, ChangelogEntry)
        assert entry.version == "1.8.0"
        assert entry.date == "2026-08-01"
        # Summary is the leading prose paragraph, joined into one line.
        assert entry.summary == "This release does the thing. It also does another thing."
        # Notes carry the full raw-markdown body of this section.
        assert "### Added" in entry.notes
        assert "Feature A with **bold** text" in entry.notes
        assert "Bug with `code` reference" in entry.notes

    def test_leading_v_prefix_is_tolerated(self, changelog_file):
        entry = get_changelog_entry("v1.8.0")

        assert entry is not None
        # The returned version reflects the heading, not the queried string.
        assert entry.version == "1.8.0"

    def test_notes_stop_at_next_section_boundary(self, changelog_file):
        entry = get_changelog_entry("1.8.0")

        # The body must not bleed into the following ``## [1.7.1]`` section.
        assert "1.7.1" not in entry.notes
        assert "An earlier release summary line." not in entry.notes
        assert "An old change from the previous release" not in entry.notes

    def test_second_section_also_parses_independently(self, changelog_file):
        # Guards against the boundary logic swallowing the *last* section too.
        entry = get_changelog_entry("1.7.1")

        assert entry is not None
        assert entry.version == "1.7.1"
        assert entry.date == "2026-07-28"
        assert entry.summary == "An earlier release summary line."
        assert "An old change from the previous release" in entry.notes
        # And it must not reach backwards into 1.8.0's content.
        assert "Feature A" not in entry.notes

    def test_unknown_version_returns_none(self, changelog_file):
        assert get_changelog_entry("9.9.9") is None

    def test_empty_version_string_returns_none(self, changelog_file):
        assert get_changelog_entry("") is None

    def test_missing_changelog_file_returns_none(self, tmp_path, monkeypatch):
        # Point the helper at a path that does not exist (stripped image case).
        missing = tmp_path / "does_not_exist" / "CHANGELOG.md"
        monkeypatch.setattr(changelog, "_changelog_path", lambda: missing)

        assert get_changelog_entry("1.8.0") is None


class TestRenderChangelogHtml:
    """Behaviour of ``render_changelog_html`` — the markdown-subset renderer.

    Output is rendered with ``|safe`` downstream, so escaping is load-bearing.
    """

    def test_h3_heading_becomes_h4(self):
        out = render_changelog_html("### Added")
        assert "<h4>Added</h4>" in out

    def test_bullet_line_becomes_list_item(self):
        out = render_changelog_html("- item")
        assert "<ul>" in out
        assert "<li>item</li>" in out
        assert "</ul>" in out

    def test_bold_span_becomes_strong(self):
        out = render_changelog_html("This is **bold** text")
        assert "<strong>bold</strong>" in out

    def test_backtick_span_becomes_code(self):
        out = render_changelog_html("Use `code` here")
        assert "<code>code</code>" in out

    def test_prose_line_becomes_paragraph(self):
        out = render_changelog_html("Just some prose.")
        assert "<p>Just some prose.</p>" in out

    def test_html_is_escaped(self):
        # A raw tag in the source must not survive into the |safe output.
        out = render_changelog_html("Images use the <picture> element")
        assert "&lt;picture&gt;" in out
        assert "<picture>" not in out

    def test_empty_input_returns_empty_string(self):
        assert render_changelog_html("") == ""

    def test_whitespace_only_input_returns_empty_string(self):
        assert render_changelog_html("   \n\t  \n") == ""
