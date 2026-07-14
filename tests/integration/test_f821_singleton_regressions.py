"""Regression tests for the singleton F821 hits across many apps.

Each entry asserts that a module now exposes the symbol whose absence
caused ruff to flag F821 (undefined name) in the pre-fix code. Each
originated from a distinct file — bundled here because splitting them
into per-app test modules for one-line fixes was pure ceremony.
"""

from django.test import SimpleTestCase


class SingletonF821Regressions(SimpleTestCase):
    def test_affiliate_filter_program_members_imports_render_to_string(self):
        import inspect

        from affiliate.views import filter_program_members

        self.assertIn(
            "from django.template.loader import render_to_string",
            inspect.getsource(filter_program_members),
        )

    def test_license_checkout_services_exposes_license_product(self):
        import importlib.util

        if importlib.util.find_spec("license_checkout") is None:
            self.skipTest(
                "license_checkout is a Spwig HQ-only app; not present in Community builds"
            )

        from license_checkout import services

        self.assertTrue(hasattr(services, "LicenseProduct"))

    def test_shop_analytics_service_has_module_logger(self):
        from management.services import shop_analytics_service

        self.assertTrue(hasattr(shop_analytics_service, "logger"))

    def test_media_library_views_uses_bare_Q(self):
        """The `models.Q(...)` calls in the recent-jobs queryset were
        rewritten to bare Q since it's already imported top-level."""
        import inspect

        from media_library.views import MediaProcessingJobViewSet

        source = inspect.getsource(MediaProcessingJobViewSet)
        self.assertNotIn("models.Q(", source)

    def test_pos_api_sync_module_has_logger(self):
        from pos_api.views import sync

        self.assertTrue(hasattr(sync, "logger"))

    def test_pos_app_tasks_pos_license_check_has_timezone(self):
        import inspect

        from pos_app.tasks import validate_pos_license

        source = inspect.getsource(validate_pos_license)
        self.assertIn("from django.utils import timezone", source)

    def test_subscriptions_api_views_exposes_serializers(self):
        from subscriptions import api_views

        self.assertTrue(hasattr(api_views, "serializers"))

    def test_subscriptions_models_exposes_money(self):
        from subscriptions import models as subs_models

        self.assertTrue(hasattr(subs_models, "Money"))

    def test_tests_factories_export_warehouse_factory(self):
        from tests.factories import WarehouseFactory

        self.assertTrue(callable(WarehouseFactory))
