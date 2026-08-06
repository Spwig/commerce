"""
Regression tests for the static-manifest completeness check.

Reproduces the pre-baked fast-path bug: when the entrypoint trusts the
.prebaked marker and only syncs component statics, an incomplete core manifest
(or missing hashed core files on disk) leaves WhiteNoise 404ing every core
CSS/JS/favicon. verify_static_manifest must detect both failure modes so the
entrypoint can repair with a full collectstatic.
"""

import json

import pytest
from django.test import override_settings

from core.management.commands.verify_static_manifest import Command

pytestmark = pytest.mark.core

MANIFEST_STORAGE = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "core.storage.NonStrictManifestStorage"},
}


def _command_with_core(core_files):
    cmd = Command()
    cmd._iter_core_static_files = lambda: set(core_files)
    return cmd


def _write_manifest(static_root, paths):
    (static_root / "staticfiles.json").write_text(json.dumps({"version": "1.0", "paths": paths}))


def test_incomplete_when_core_missing_from_manifest(tmp_path):
    """The exact bug: manifest has only component entries, no core assets."""
    _write_manifest(
        tmp_path, {"utilities/shadow_editor/app.js": "utilities/shadow_editor/app.abc.js"}
    )
    with override_settings(STATIC_ROOT=str(tmp_path), STORAGES=MANIFEST_STORAGE):
        cmd = _command_with_core({"css/all.min.css", "js/base.js"})
        complete, stats, _ = cmd.check_manifest()
    assert complete is False
    assert stats["missing_manifest"] == 2


def test_incomplete_when_hashed_file_absent_on_disk(tmp_path):
    """Manifest names a hashed core file that was never shipped -> 404s."""
    _write_manifest(tmp_path, {"css/all.min.css": "css/all.min.9402848c3d4b.css"})
    with override_settings(STATIC_ROOT=str(tmp_path), STORAGES=MANIFEST_STORAGE):
        cmd = _command_with_core({"css/all.min.css"})
        complete, stats, _ = cmd.check_manifest()
    assert complete is False
    assert stats["missing_disk"] == 1


def test_complete_when_manifest_and_files_present(tmp_path):
    """Healthy: every core file is in the manifest and its hashed file exists."""
    hashed = "css/all.min.9402848c3d4b.css"
    _write_manifest(tmp_path, {"css/all.min.css": hashed})
    (tmp_path / "css").mkdir()
    (tmp_path / hashed).write_text("body{}")
    with override_settings(STATIC_ROOT=str(tmp_path), STORAGES=MANIFEST_STORAGE):
        cmd = _command_with_core({"css/all.min.css"})
        complete, stats, _ = cmd.check_manifest()
    assert complete is True
    assert stats["missing_manifest"] == 0
    assert stats["missing_disk"] == 0


def test_incomplete_when_manifest_file_missing(tmp_path):
    """No staticfiles.json at all is incomplete."""
    with override_settings(STATIC_ROOT=str(tmp_path), STORAGES=MANIFEST_STORAGE):
        cmd = _command_with_core({"css/all.min.css"})
        complete, _, _ = cmd.check_manifest()
    assert complete is False


def test_skipped_when_not_manifest_storage(tmp_path):
    """In DEBUG (non-manifest storage) there's nothing to verify."""
    debug_storage = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
    with override_settings(STATIC_ROOT=str(tmp_path), STORAGES=debug_storage):
        cmd = _command_with_core({"css/all.min.css"})
        complete, stats, _ = cmd.check_manifest()
    assert complete is True
    assert stats.get("skipped") is True
