"""Regression tests for missing-import bugs surfaced by ruff F821.

Each test exercises a code path that would raise NameError before the
matching fix in catalog/*.
"""

from django.core.exceptions import ValidationError as DjangoValidationError
from django.test import SimpleTestCase

from catalog.models import LicenseKeyTemplate, ProductDependency


class ProductDependencyCleanValidationErrorTest(SimpleTestCase):
    """catalog/models.py:2192 ProductDependency.clean() raised
    NameError: name 'ValidationError' is not defined when the product
    depended on itself (validate_pattern's ValidationError was imported
    lazily in other methods but not this one)."""

    def test_self_dependency_raises_validation_error(self):
        dep = ProductDependency(product_id=1, required_product_id=1)
        with self.assertRaises(DjangoValidationError):
            dep.clean()


class LicenseKeyTemplateValidatePatternTest(SimpleTestCase):
    """catalog/models.py:4968 LicenseKeyTemplate.validate_pattern() used
    ValidationError without importing it. Any bad placeholder in the
    pattern used to NameError instead of ValidationError."""

    def test_unknown_placeholder_raises_validation_error(self):
        pattern = LicenseKeyTemplate(pattern="{UNKNOWN_PLACEHOLDER}")
        with self.assertRaises(DjangoValidationError):
            pattern.validate_pattern()


class LicenseActivationSerializerImportTest(SimpleTestCase):
    """catalog/license_api_views.py used LicenseActivationSerializer on
    lines 242 and 308 but never imported it. Verify the view module now
    exposes the symbol so the runtime lookup succeeds."""

    def test_activation_serializer_available_in_view_module(self):
        from catalog import license_api_views

        self.assertTrue(hasattr(license_api_views, "LicenseActivationSerializer"))


class SalesRegionAvailableInAdminViewsTest(SimpleTestCase):
    """catalog/admin_views.py:2613 used SalesRegion.objects.all() but
    SalesRegion was missing from the top-level model import."""

    def test_sales_region_imported_in_admin_views(self):
        from catalog import admin_views

        self.assertTrue(hasattr(admin_views, "SalesRegion"))


class SimilarProductsDecimalImportTest(SimpleTestCase):
    """catalog/api_views.py:1002 ProductViewSet.similar() referenced
    Decimal without importing it. The action now performs a lazy
    `from decimal import Decimal` inside the method body."""

    def test_similar_action_has_decimal_in_scope(self):
        import inspect

        from catalog.api_views import ProductViewSet

        source = inspect.getsource(ProductViewSet.similar)
        self.assertIn("from decimal import Decimal", source)
