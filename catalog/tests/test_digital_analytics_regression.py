"""Regression test for the digital products analytics dashboard.

``catalog/admin_views.py`` computed digital revenue with
``Sum("line_total")``, but ``orders.OrderItem`` has no ``line_total`` field
(the line total lives on ``total_price`` / ``total_price_base``). The dashboard
therefore raised ``FieldError`` and returned HTTP 500. Revenue must be summed
from ``total_price_base`` (the base-currency column used for all reporting).
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tests.factories import OrderItemFactory


class DigitalProductsAnalyticsDashboardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        from core.models import SiteSettings

        # Single-tenant chrome the admin template chrome expects.
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "site_name": "Test Store",
                "admin_email": "admin@test.spwig.com",
                "default_currency": "USD",
                "default_language": "en",
            },
        )
        User = get_user_model()
        cls.staff = User.objects.create_user(
            username="dp_analytics_staff",
            email="dp_analytics@test.spwig.com",
            password="pw-not-used",
            is_staff=True,
            is_superuser=True,
        )
        # One recent, paid *digital* line — this is what revenue should count.
        cls.digital_item = OrderItemFactory(
            product__digital=True,
            order__status="processing",
        )
        # A physical line in the same window must NOT contribute to digital revenue.
        cls.physical_item = OrderItemFactory(order__status="processing")

    def setUp(self):
        self.client.force_login(self.staff)

    def test_dashboard_renders_instead_of_500(self):
        """The FieldError regression made this view return 500."""
        resp = self.client.get(reverse("catalog_admin:digital_products_analytics"))
        self.assertEqual(resp.status_code, 200)

    def test_revenue_sums_base_totals_of_digital_items_only(self):
        resp = self.client.get(reverse("catalog_admin:digital_products_analytics"))
        # Only the digital line counts; the physical line is excluded.
        self.assertEqual(resp.context["digital_revenue"], self.digital_item.total_price_base)
        self.assertGreater(self.digital_item.total_price_base, Decimal("0"))
