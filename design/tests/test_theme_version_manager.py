"""
Unit tests for ThemeVersionManager.activate_theme_version.

Covers the symlink-flip bug discovered on fleet instance `apparel-theme`
where the method returned success: True but the symlink did not actually
point to the requested version because the subsequent extract_theme()
call re-ran activation against a stale Theme.version value.
"""

import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase, override_settings

from design.theme_version_manager import ThemeVersionManager


class TestActivateThemeVersionSymlinkFlip(TestCase):
    """Tests for the symlink-flip logic in activate_theme_version."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix='theme_activation_test_'))
        self.themes_static = self.root / 'static' / 'design' / 'themes'
        self.themes_static.mkdir(parents=True)

        self.theme_slug = 'test-theme'
        self.theme_dir = self.themes_static / self.theme_slug
        self.theme_dir.mkdir()

        # Create two version dirs with the minimum theme health-check files
        for version in ('1.0.0', '1.1.0'):
            vdir = self.theme_dir / version / 'theme'
            (vdir / 'css').mkdir(parents=True)
            (vdir / 'manifest.json').write_text('{}')

        # Initial symlink pointing to the old version
        (self.theme_dir / 'current').symlink_to('1.0.0')

        # Patch the module-level THEMES_STATIC so the manager sees our fixture
        self._themes_static_patcher = patch(
            'design.theme_version_manager.THEMES_STATIC', self.themes_static
        )
        self._themes_static_patcher.start()

        # Patch REGISTRY_FILE so save_registry doesn't touch the real filesystem
        self._registry_patcher = patch(
            'design.theme_version_manager.REGISTRY_FILE',
            self.root / 'registries' / 'themes.json',
        )
        self._registry_patcher.start()

    def tearDown(self):
        self._themes_static_patcher.stop()
        self._registry_patcher.stop()
        shutil.rmtree(self.root, ignore_errors=True)

    def _symlink_target(self):
        return (self.theme_dir / 'current').resolve().name

    def test_flips_symlink_to_target_version(self):
        """Basic happy path: symlink moves from 1.0.0 to 1.1.0."""
        self.assertEqual(self._symlink_target(), '1.0.0')

        result = ThemeVersionManager.activate_theme_version(
            self.theme_slug, '1.1.0', update_active_theme=False
        )

        self.assertTrue(result['success'], msg=result)
        self.assertEqual(self._symlink_target(), '1.1.0')

    def test_returns_error_when_version_missing(self):
        """Activating a version that was never installed must fail cleanly."""
        result = ThemeVersionManager.activate_theme_version(
            self.theme_slug, '9.9.9', update_active_theme=False
        )

        self.assertFalse(result['success'])
        self.assertIn('9.9.9', result['error'])
        # Symlink should not have been touched
        self.assertEqual(self._symlink_target(), '1.0.0')

    def test_post_flip_verification_catches_drift(self):
        """
        If something after the initial flip re-points the symlink to a
        different version (e.g. extract_theme re-running activation with a
        stale self.version), the post-flip verification must detect it and
        re-establish the target — or return success: False.

        This simulates the fleet bug: extract_theme() is called as a side
        effect of setting update_active_theme=True and re-flips the symlink.
        """
        call_count = {'n': 0}

        def flaky_extract(theme_obj):
            """First call points the symlink at the wrong version."""
            call_count['n'] += 1
            # Mimic the buggy extract_theme: flip symlink to stale version
            current = self.theme_dir / 'current'
            tmp = self.theme_dir / 'current.tmp'
            if tmp.exists() or tmp.is_symlink():
                tmp.unlink()
            tmp.symlink_to('1.0.0')
            tmp.replace(current)

        with patch(
            'design.theme_models.Theme.extract_theme',
            side_effect=lambda self_obj=None: flaky_extract(None),
            autospec=False,
        ), patch('design.theme_models.Theme.objects.filter') as mock_filter:
            # Make Theme.objects.filter(...).first() return a minimal stub so
            # the update_active_theme=True branch runs but we control side
            # effects via the extract_theme patch above.
            class _Stub:
                slug = self.theme_slug
                version = '1.0.0'  # stale on purpose
                package_file = type('_pf', (), {'path': '/dev/null'})()
                def save(self, *a, **kw): pass
                def extract_theme(self): flaky_extract(None)
            mock_filter.return_value.first.return_value = _Stub()

            with patch('design.models.GlobalDesignSettings.get_settings') as mock_gds:
                mock_gds.return_value.save = lambda *a, **kw: None
                result = ThemeVersionManager.activate_theme_version(
                    self.theme_slug, '1.1.0', update_active_theme=True
                )

        # The post-flip verification MUST leave the symlink at the target,
        # either by re-flipping successfully or by returning success: False.
        if result['success']:
            self.assertEqual(
                self._symlink_target(),
                '1.1.0',
                msg='Symlink must point to the activation target when success=True',
            )
        else:
            self.assertIn('symlink', result['error'].lower())
