"""Tests for component static file finders."""

from django.contrib.staticfiles import finders as staticfiles_finders
from django.test import SimpleTestCase

from component_updates.finders import ComponentStaticFinder, IntegrationStaticFinder


class FinderSignatureRegressionTests(SimpleTestCase):
    """
    Django 5.2 renamed the finder ``find()`` kwarg from ``all`` to ``find_all``
    and dispatches every lookup as ``finder.find(path, find_all=...)``. When the
    custom finders still declared ``find(self, path, all=False)`` this raised
    ``TypeError: find() got an unexpected keyword argument 'find_all'`` for any
    path only these finders could resolve (e.g. ``/static/utilities/...``),
    500-ing every page-builder editor asset. These tests lock the signature.
    """

    def test_component_finder_accepts_find_all_kwarg(self):
        finder = ComponentStaticFinder()
        # A path no finder can resolve must return an empty result, not raise.
        self.assertEqual(finder.find("does/not/exist.css", find_all=False), "")
        self.assertEqual(finder.find("does/not/exist.css", find_all=True), [])

    def test_integration_finder_accepts_find_all_kwarg(self):
        finder = IntegrationStaticFinder()
        self.assertEqual(finder.find("does/not/exist.css", find_all=False), "")
        self.assertEqual(finder.find("does/not/exist.css", find_all=True), [])

    def test_legacy_all_kwarg_still_supported(self):
        # Older Django passed ``all=``; keep tolerating it during the window.
        finder = ComponentStaticFinder()
        self.assertEqual(finder.find("does/not/exist.css", all=True), [])

    def test_global_find_dispatch_does_not_raise(self):
        # Exercise the exact dispatch path used by the staticfiles serve view.
        result = staticfiles_finders.find(
            "utilities/does-not-exist/current/nope.css", find_all=True
        )
        self.assertEqual(result, [])
