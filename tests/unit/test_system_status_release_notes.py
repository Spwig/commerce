"""Unit tests for ``SystemStatusService.get_version_info`` release-notes wiring.

The upgrade admin surfaces platform release notes, so ``get_version_info``
now propagates a ``release_notes`` key (alongside ``changelog`` and
``available``) copied from the ``PlatformUpdateService.check_for_update``
result whenever an update is available.

These are light propagation tests: ``UpdateServerConfig.get_instance`` and
``PlatformUpdateService.check_for_update`` are both mocked (both are lazily
imported inside ``get_version_info``, so they are patched at their source
modules) — no DB, no network, no real update server.
"""

from unittest import mock

import pytest

from management.services.system_status import SystemStatusService

pytestmark = [pytest.mark.unit]


def _configured_server():
    """A stand-in UpdateServerConfig with the fields the check gate reads."""
    return mock.Mock(server_url="https://updates.example.com", license_key="LICENSE-KEY")


class TestGetVersionInfoReleaseNotes:
    def test_release_notes_key_is_always_present(self):
        # Even with no update server configured, the key exists on the result.
        with mock.patch(
            "component_updates.models.UpdateServerConfig.get_instance",
            return_value=mock.Mock(server_url="", license_key=""),
        ):
            info = SystemStatusService.get_version_info()

        assert "release_notes" in info
        assert info["release_notes"] is None

    def test_release_notes_propagated_when_update_available(self):
        check_result = {
            "update_available": True,
            "latest_version": "1.8.0",
            "changelog": "Full changelog body",
            "release_notes": "Short user-facing blurb",
        }

        with (
            mock.patch(
                "component_updates.models.UpdateServerConfig.get_instance",
                return_value=_configured_server(),
            ),
            mock.patch(
                "component_updates.services.PlatformUpdateService.check_for_update",
                return_value=check_result,
            ) as m_check,
        ):
            info = SystemStatusService.get_version_info()

        m_check.assert_called_once_with(channel="stable")
        assert info["update_available"] is True
        assert info["available"] == "1.8.0"
        assert info["changelog"] == "Full changelog body"
        assert info["release_notes"] == "Short user-facing blurb"

    def test_release_notes_stays_none_when_no_update(self):
        check_result = {"update_available": False}

        with (
            mock.patch(
                "component_updates.models.UpdateServerConfig.get_instance",
                return_value=_configured_server(),
            ),
            mock.patch(
                "component_updates.services.PlatformUpdateService.check_for_update",
                return_value=check_result,
            ),
        ):
            info = SystemStatusService.get_version_info()

        assert info["update_available"] is False
        assert info["release_notes"] is None
        assert info["available"] is None
