"""
Audit-specific pytest fixtures.

Provides test data and helpers for site health audit tests.
"""
import pytest
from decimal import Decimal


@pytest.fixture
def audit_storefront_data(db, site_settings, django_site):
    """Create minimal data for storefront audit tests."""
    from tests.factories import ProductFactory, CategoryFactory

    category = CategoryFactory(name="Audit Category", slug="audit-category")
    product = ProductFactory(
        name="Audit Product",
        slug="audit-product",
        category=category,
        price=Decimal("29.99"),
    )

    return {
        "category": category,
        "product": product,
    }
