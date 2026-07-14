"""Regression tests for page_builder F821 bugs.

- page_builder/api/translation_endpoints.py:40 called
  `health.get_degradation_warnings()` without defining `health`.
- page_builder/api/translation_endpoints.py:431 and
  page_builder/translation_utils.py:369 instantiated
  TranslationServiceHealth which never existed.
- page_builder/api_views.py referenced the deleted PageSection model
  inside a `RemovedSectionAPIView` class that was never removed.
"""

from unittest.mock import patch

from django.test import SimpleTestCase


class TranslationServiceHealthTest(SimpleTestCase):
    """The wrapper class must exist and expose the four methods callers
    were assuming: get_health_status, should_schedule_translation,
    estimate_translation_time, get_degradation_warnings. The first was
    added after an initial code review noted that
    page_builder/middleware.py:174 called it but the wrapper did not
    define it — the surrounding try/except swallowed the AttributeError,
    silently disabling middleware-level health monitoring."""

    def test_wrapper_class_exists(self):
        from page_builder.translation_utils import TranslationServiceHealth

        h = TranslationServiceHealth()
        self.assertTrue(callable(h.get_health_status))
        self.assertTrue(callable(h.should_schedule_translation))
        self.assertTrue(callable(h.estimate_translation_time))
        self.assertTrue(callable(h.get_degradation_warnings))

    def test_middleware_health_call_resolves(self):
        """Simulate the middleware call and assert it returns real
        health data, not the swallowed-AttributeError fallback."""
        from unittest.mock import patch

        from page_builder.translation_utils import TranslationServiceHealth

        with patch("page_builder.translation_utils.get_translation_health_status") as m:
            m.return_value = {
                "available": True,
                "status": "ok",
                "message": "Translation service is operational",
            }
            status = TranslationServiceHealth().get_health_status()

        self.assertTrue(status["available"])
        self.assertEqual(status["status"], "ok")

    def test_degradation_warnings_returns_list_when_available(self):
        from page_builder.translation_utils import TranslationServiceHealth

        with patch("page_builder.translation_utils.get_translation_health_status") as m:
            m.return_value = {"available": True, "status": "ok", "message": ""}
            self.assertEqual(TranslationServiceHealth().get_degradation_warnings(), [])

    def test_degradation_warnings_returns_message_when_unavailable(self):
        from page_builder.translation_utils import TranslationServiceHealth

        with patch("page_builder.translation_utils.get_translation_health_status") as m:
            m.return_value = {
                "available": False,
                "status": "offline",
                "message": "Translation service is not responding",
            }
            warnings = TranslationServiceHealth().get_degradation_warnings()
            self.assertEqual(warnings, ["Translation service is not responding"])


class RemovedSectionAPIViewGoneTest(SimpleTestCase):
    """The dead RemovedSectionAPIView class referenced a deleted model.
    It has been removed entirely."""

    def test_class_is_gone(self):
        from page_builder import api_views

        self.assertFalse(hasattr(api_views, "RemovedSectionAPIView"))
        self.assertFalse(hasattr(api_views, "PageSection"))


class TranslationHealthEndpointHealthLocalTest(SimpleTestCase):
    """translation_health() previously referenced `health` without a
    local assignment. Assert the fix wires it up before use."""

    def test_translation_health_endpoint_source_defines_health(self):
        import inspect

        from page_builder.api.translation_endpoints import translation_health

        source = inspect.getsource(translation_health)
        self.assertIn("health = TranslationServiceHealth()", source)
