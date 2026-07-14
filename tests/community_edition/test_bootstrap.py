"""
Bootstrap behaviour for the Community licence.

Verifies the auto-install path via both the management command and the
apps.ready() helper.
"""

import json

import pytest


@pytest.fixture
def stub_community_template(tmp_path, monkeypatch):
    """
    Redirect the bootstrap command to a temp template so tests don't
    depend on the real signed licence being present in the repo.
    """
    from core.management.commands import bootstrap_community_licence as cmd

    template = tmp_path / "community_licence.json"
    template.write_text(
        json.dumps(
            {
                "license": {
                    "license_type": "community",
                    "edition": "community",
                    "environment_type": "production",
                    "is_active": True,
                    "major_version": 1,
                    "entitlements": [],
                },
                "signature": "",
            }
        )
    )
    monkeypatch.setattr(cmd, "COMMUNITY_LICENCE_TEMPLATE", template)
    return template


def test_bootstrap_installs_template_when_missing(tmp_path, settings, stub_community_template):
    """No licence at LICENSE_PATH → template is installed."""
    from django.core.management import call_command

    target = tmp_path / "license.json"
    settings.LICENSE_PATH = str(target)
    assert not target.exists()

    call_command("bootstrap_community_licence", quiet=True)

    assert target.exists()
    data = json.loads(target.read_text())
    assert data["license"]["edition"] == "community"


def test_bootstrap_preserves_existing_licence(tmp_path, settings, stub_community_template):
    """An existing licence is never overwritten by default."""
    from django.core.management import call_command

    target = tmp_path / "license.json"
    settings.LICENSE_PATH = str(target)
    existing = {"license": {"edition": "pro"}, "signature": "xxx"}
    target.write_text(json.dumps(existing))

    call_command("bootstrap_community_licence", quiet=True)

    assert json.loads(target.read_text()) == existing


def test_bootstrap_force_overwrites(tmp_path, settings, stub_community_template):
    """--force replaces even an existing licence."""
    from django.core.management import call_command

    target = tmp_path / "license.json"
    settings.LICENSE_PATH = str(target)
    target.write_text(json.dumps({"license": {"edition": "pro"}, "signature": "xxx"}))

    call_command("bootstrap_community_licence", force=True, quiet=True)

    assert json.loads(target.read_text())["license"]["edition"] == "community"


def test_bootstrap_creates_parent_directory(tmp_path, settings, stub_community_template):
    """Bootstrap creates the parent directory if it doesn't exist."""
    from django.core.management import call_command

    target = tmp_path / "some" / "deep" / "path" / "license.json"
    settings.LICENSE_PATH = str(target)

    call_command("bootstrap_community_licence", quiet=True)

    assert target.exists()


def test_apps_ready_bootstrap_helper(tmp_path, settings, stub_community_template):
    """The helper in apps.py wires up the same behaviour without CLI."""
    import logging

    from core.apps import _bootstrap_community_licence

    target = tmp_path / "license.json"
    settings.LICENSE_PATH = str(target)

    _bootstrap_community_licence(logging.getLogger("test"))

    assert target.exists()
    assert json.loads(target.read_text())["license"]["edition"] == "community"
