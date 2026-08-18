"""Regression: ThemeCSSView must serve a selected theme's CSS regardless of
the Theme.is_active flag.

The storefront links /theme/css/theme/<slug>.css for whichever theme
GlobalDesignSettings.active_theme points at. Previously the view gated on
is_active=True, so a *selected* theme whose row had is_active=False (e.g. after
a legacy "deactivate other themes on activate" pass) returned 404 → the
storefront rendered with no theme CSS and appeared not to update on switch.
"""

from django.http import Http404
from django.test import RequestFactory, TestCase

from design.theme_models import Theme
from design.views import ThemeCSSView


class ThemeCSSActiveGatingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.css = ":root{--theme-color-primary:#123456;}"
        self.theme = Theme.objects.create(
            name="Inactive Selected Theme",
            slug="inactive-selected",
            version="1.0.0",
            engine_min_version="1.0.0",
            author="Test",
            is_active=False,  # the crux: installed-but-flagged-inactive
            is_default=False,
            compiled_css=self.css,
            css_hash="deadbeef",
        )

    def _get(self, slug):
        request = self.factory.get(f"/theme/css/theme/{slug}.css")
        return ThemeCSSView.as_view()(request, slug=slug)

    def test_inactive_theme_css_is_served(self):
        """An is_active=False theme still serves its compiled CSS (200)."""
        response = self._get(self.theme.slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/css")
        body = response.content.decode()
        self.assertIn("--theme-color-primary", body)
        self.assertEqual(response["ETag"], '"deadbeef"')

    def test_unknown_slug_still_404s(self):
        """A slug with no Theme row is still a 404 (guard didn't over-broaden)."""
        with self.assertRaises(Http404):
            self._get("no-such-theme")
