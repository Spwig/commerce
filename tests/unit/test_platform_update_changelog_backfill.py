"""Unit tests for ``PlatformUpdateService._backfill_changelog``.

When a Spwig install builds its own image from the public GitHub repo, the
update server may hold no changelog text for the target version, so the
platform update-check response comes back with empty ``changelog`` /
``release_notes``. ``_backfill_changelog`` fills those in from the local
CHANGELOG.md — but only when it is safe to do so.

Invariants under test:

* Fills empty fields when an update IS available.
* Never overwrites text the server already provided.
* No-op when no update is available, or when ``latest_version`` is absent.
* Stamps ``changelog_source == "local"`` when (and only when) it fills the
  changelog itself.

``_backfill_changelog`` performs a lazy ``from core.changelog import
get_changelog_entry`` inside the function body, so the mock target is the
source module (``core.changelog.get_changelog_entry``), not the importer.
The tests operate on plain dict fixtures — no DB, no network.
"""

from types import SimpleNamespace
from unittest import mock

import pytest

from component_updates.services import PlatformUpdateService

pytestmark = [pytest.mark.unit]


def _entry(notes="LOCAL NOTES", summary="LOCAL SUMMARY"):
    """A stand-in for ``core.changelog.ChangelogEntry`` (only .notes/.summary used)."""
    return SimpleNamespace(version="1.8.0", date="2026-08-01", notes=notes, summary=summary)


class TestBackfillChangelog:
    def test_fills_empty_fields_when_update_available(self):
        data = {
            "update_available": True,
            "latest_version": "1.8.0",
            "changelog": "",
            "release_notes": "",
        }

        with mock.patch("core.changelog.get_changelog_entry", return_value=_entry()) as m:
            PlatformUpdateService._backfill_changelog(data)

        m.assert_called_once_with("1.8.0")
        assert data["changelog"] == "LOCAL NOTES"
        assert data["release_notes"] == "LOCAL SUMMARY"

    def test_marks_changelog_source_local_when_it_fills_changelog(self):
        data = {
            "update_available": True,
            "latest_version": "1.8.0",
            "changelog": "",
            "release_notes": "",
        }

        with mock.patch("core.changelog.get_changelog_entry", return_value=_entry()):
            PlatformUpdateService._backfill_changelog(data)

        assert data["changelog_source"] == "local"

    def test_does_not_overwrite_server_provided_changelog(self):
        # Server gave a changelog but left release_notes empty: the changelog
        # must survive untouched (and stay unstamped) while notes are filled.
        data = {
            "update_available": True,
            "latest_version": "1.8.0",
            "changelog": "SERVER CHANGELOG",
            "release_notes": "",
        }

        with mock.patch("core.changelog.get_changelog_entry", return_value=_entry()):
            PlatformUpdateService._backfill_changelog(data)

        assert data["changelog"] == "SERVER CHANGELOG"
        assert "changelog_source" not in data
        # The still-empty release_notes gets the local summary.
        assert data["release_notes"] == "LOCAL SUMMARY"

    def test_no_op_when_both_fields_already_present(self):
        data = {
            "update_available": True,
            "latest_version": "1.8.0",
            "changelog": "SERVER CHANGELOG",
            "release_notes": "SERVER NOTES",
        }

        with mock.patch("core.changelog.get_changelog_entry") as m:
            PlatformUpdateService._backfill_changelog(data)

        # Both present -> early return; the local changelog is never consulted.
        m.assert_not_called()
        assert data["changelog"] == "SERVER CHANGELOG"
        assert data["release_notes"] == "SERVER NOTES"
        assert "changelog_source" not in data

    def test_no_op_when_update_not_available(self):
        data = {
            "update_available": False,
            "latest_version": "1.8.0",
            "changelog": "",
            "release_notes": "",
        }

        with mock.patch("core.changelog.get_changelog_entry") as m:
            PlatformUpdateService._backfill_changelog(data)

        m.assert_not_called()
        assert data["changelog"] == ""
        assert data["release_notes"] == ""
        assert "changelog_source" not in data

    def test_no_op_when_latest_version_missing(self):
        data = {
            "update_available": True,
            "changelog": "",
            "release_notes": "",
        }

        with mock.patch("core.changelog.get_changelog_entry") as m:
            PlatformUpdateService._backfill_changelog(data)

        m.assert_not_called()
        assert data["changelog"] == ""
        assert data["release_notes"] == ""

    def test_no_op_when_local_entry_not_found(self):
        # Update available and fields empty, but this build's CHANGELOG.md has
        # no section for the target version -> nothing to backfill.
        data = {
            "update_available": True,
            "latest_version": "1.8.0",
            "changelog": "",
            "release_notes": "",
        }

        with mock.patch("core.changelog.get_changelog_entry", return_value=None):
            PlatformUpdateService._backfill_changelog(data)

        assert data["changelog"] == ""
        assert data["release_notes"] == ""
        assert "changelog_source" not in data
