"""
Audit-specific pytest fixtures.

Provides test data and helpers for site health audit tests.
"""

from decimal import Decimal

import pytest


@pytest.fixture
def audit_storefront_data(db, site_settings, django_site):
    """Create minimal data for storefront audit tests."""
    from tests.factories import CategoryFactory, ProductFactory

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
