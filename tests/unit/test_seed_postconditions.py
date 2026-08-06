"""
Regression coverage for the ``seed`` orchestrator's first-boot post-condition.

After seeding, a storefront theme must be installed, active, AND carry compiled
CSS -- otherwise the storefront renders on ``base.css`` fallback with no theme
applied. The check guards against a preinstalled-manifest regression (themes
silently dropped from ``manifest.json`` by a partial ``build_preinstalled_packages``
run) shipping a technically-booted but themeless store.

The check is intentionally non-fatal (it reports loudly to stderr rather than
raising) because ``docker-entrypoint.sh`` runs under ``set -e`` -- a raise would
turn a styling problem into an aborted boot. These tests pin both the loud
failure output and the gating that keeps the check quiet when theme
installation didn't run.
"""

import io
from types import SimpleNamespace
from unittest.mock import patch

from core.management.commands.seed import Command


def _make_command():
    # Capture output; no_color keeps assertions free of ANSI escape codes.
    return Command(stdout=io.StringIO(), stderr=io.StringIO(), no_color=True)


def _theme(slug="starter", css_url="/theme/css/theme/starter.css?v=abc"):
    return SimpleNamespace(slug=slug, get_css_url=lambda: css_url)


class TestSeedThemePostCondition:
    def test_ok_when_active_theme_has_compiled_css(self):
        cmd = _make_command()
        with patch("design.theme_utils.get_active_theme", return_value=_theme()):
            cmd._verify_active_theme()
        assert "OK" in cmd.stdout.getvalue()
        assert "starter" in cmd.stdout.getvalue()
        assert cmd.stderr.getvalue() == ""

    def test_fails_loudly_when_no_active_theme(self):
        cmd = _make_command()
        with patch("design.theme_utils.get_active_theme", return_value=None):
            cmd._verify_active_theme()
        err = cmd.stderr.getvalue()
        assert "POST-CONDITION FAILED" in err
        assert "no 'theme' components" in err
        # The operator-facing remediation command must be surfaced verbatim.
        assert "build_preinstalled_packages --type theme" in err
        assert cmd.stdout.getvalue() == ""

    def test_fails_loudly_when_active_theme_has_no_compiled_css(self):
        # A theme row can be active while compiled_css is empty -> get_css_url()
        # is falsy -> the theme_css tag still emits no stylesheet link.
        cmd = _make_command()
        with patch("design.theme_utils.get_active_theme", return_value=_theme(css_url="")):
            cmd._verify_active_theme()
        err = cmd.stderr.getvalue()
        assert "POST-CONDITION FAILED" in err
        assert "no compiled CSS" in err

    def test_skipped_when_bundled_components_did_not_run(self):
        # `seed --only languages` must not evaluate the theme post-condition:
        # theme installation never had a chance to run.
        cmd = _make_command()
        with patch("design.theme_utils.get_active_theme", return_value=None) as mocked:
            cmd._verify_postconditions({"languages", "site_defaults"})
        mocked.assert_not_called()
        assert cmd.stdout.getvalue() == ""
        assert cmd.stderr.getvalue() == ""

    def test_runs_when_bundled_components_ran(self):
        cmd = _make_command()
        with patch("design.theme_utils.get_active_theme", return_value=_theme()) as mocked:
            cmd._verify_postconditions({"bundled_components"})
        mocked.assert_called_once()
        assert "Verifying post-conditions" in cmd.stdout.getvalue()
