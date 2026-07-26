"""
Tests for the public /activate/ page — specifically the new
"Continue with Community Edition" POST branch (action=community).

The activate view lives OUTSIDE i18n_patterns, so the path is literally
``/activate/`` (no language prefix). Both ActivationMiddleware and
LicenseAcceptanceMiddleware exempt this prefix, so the test client reaches
the view without being redirected to the licence/activation gates.

The community branch runs the real ``bootstrap_community_licence`` management
command, which copies core/data/community_licence.json into LICENSE_PATH.
Every test points LICENSE_PATH at a per-test tmp file so the real install
licence is never touched.
"""

import json

import pytest
from django.test import Client

# Middleware creates a session (DB) on the way to the view, so DB access is
# required even though the view logic itself is filesystem-only.
pytestmark = pytest.mark.django_db


def test_activate_get_shows_community_button(client, settings, tmp_path, site_settings):
    """GET with no licence file: 200 + the Community Edition form."""
    settings.LICENSE_PATH = str(tmp_path / "license.json")

    response = client.get("/activate/")

    assert response.status_code == 200
    content = response.content.decode()
    # The hidden input that selects the community branch must be present.
    assert 'name="action"' in content
    assert 'value="community"' in content
    assert "Continue with Community Edition" in content


def test_activate_post_community_installs_licence(client, settings, tmp_path, site_settings):
    """
    POST action=community with no licence: the bootstrap command copies the
    bundled Community licence to LICENSE_PATH and the view redirects to '/'.
    """
    target = tmp_path / "lic" / "license.json"  # parent doesn't exist yet
    settings.LICENSE_PATH = str(target)
    assert not target.exists()

    response = client.post("/activate/", {"action": "community"})

    assert response.status_code == 302
    assert response["Location"] == "/"
    assert target.exists()
    data = json.loads(target.read_text())
    assert data["license"]["edition"] == "community"
    assert data["license"]["license_key"] == "COMMUNITY-EDITION"


def test_activate_post_community_template_missing_shows_error(
    client, settings, tmp_path, monkeypatch, site_settings
):
    """
    If the bundled licence template can't be found, the branch must NOT crash:
    it re-renders the page (200) with an error message and writes no file.
    """
    from core.management.commands import bootstrap_community_licence as cmd

    settings.LICENSE_PATH = str(tmp_path / "license.json")
    monkeypatch.setattr(cmd, "COMMUNITY_LICENCE_TEMPLATE", tmp_path / "does-not-exist.json")

    response = client.post("/activate/", {"action": "community"})

    assert response.status_code == 200  # re-render, not redirect
    assert "Could not install the Community licence" in response.content.decode()
    assert not (tmp_path / "license.json").exists()


def test_activate_get_redirects_when_licence_exists(client, settings, tmp_path, site_settings):
    """GET when a licence already exists: redirect straight to '/'."""
    target = tmp_path / "license.json"
    target.write_text("{}")
    settings.LICENSE_PATH = str(target)

    response = client.get("/activate/")

    assert response.status_code == 302
    assert response["Location"] == "/"


def test_activate_post_community_csrf_enforced(settings, tmp_path, site_settings):
    """
    The activate view is NOT csrf_exempt: a POST without a CSRF token is
    rejected with 403 before the view runs.
    """
    settings.LICENSE_PATH = str(tmp_path / "license.json")
    csrf_client = Client(enforce_csrf_checks=True)

    response = csrf_client.post("/activate/", {"action": "community"})

    assert response.status_code == 403
    # The community licence must not have been installed by an unprotected POST.
    assert not (tmp_path / "license.json").exists()
