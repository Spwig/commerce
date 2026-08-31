"""Behaviour tests for the merchant-app analytics surfaces:

- the Sales chart's per-day revenue must use the same total_amount fallback as
  the headline KPI (so cross-currency orders with a NULL base amount don't zero
  the chart while the KPI shows the real total), and
- top products and product performance must carry a sized product image
  (medium thumbnail + responsive image_sources) so the app's lists render
  thumbnails.
"""

import tempfile
from decimal import Decimal

from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.utils import timezone

from admin_api.services.analytics_service import AnalyticsService
from catalog.models import ProductImage
from media_library.models import MediaAsset, MediaThumbnail
from tests.factories import OrderFactory, OrderItemFactory, ProductFactory


def _asset_with_medium_thumbnail():
    """A MediaAsset with a 'medium' thumbnail, so get_thumbnail('medium') and
    build_image_sources both resolve a real URL."""
    asset = MediaAsset.objects.create(title="P", mime_type="image/jpeg", file_size=8)
    asset.original_file.save("orig.jpg", ContentFile(b"original"), save=True)
    thumb = MediaThumbnail.objects.create(
        media_asset=asset, size_preset="medium", width=600, height=600
    )
    thumb.webp_file.save("medium.webp", ContentFile(b"webp-bytes"), save=True)
    return asset


class DailyBreakdownRevenueFallbackTests(TestCase):
    def test_daily_breakdown_falls_back_to_total_amount_when_base_null(self):
        """With total_amount_base NULL, the per-day chart revenue must fall back
        to total_amount (like the KPI) instead of coalescing to zero."""
        today = timezone.now().date()
        for _ in range(2):
            OrderFactory(
                paid_order=True,
                total_amount=Decimal("100.00"),
                total_amount_base=None,
            )

        result = AnalyticsService.get_sales_comparison(start_date=today, end_date=today)

        daily_sum = sum(
            (row["revenue"] for row in result["daily_breakdown"]["current"]),
            Decimal("0.00"),
        )
        # Old behaviour returned Decimal("0.00") here; the fallback restores 200.
        self.assertEqual(daily_sum, Decimal("200.00"))
        # The chart total now matches the headline KPI value.
        self.assertEqual(daily_sum, Decimal(str(result["current_value"])))


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class AnalyticsProductImageTests(TestCase):
    def setUp(self):
        self.asset = _asset_with_medium_thumbnail()
        self.product = ProductFactory()
        ProductImage.objects.create(product=self.product, media_asset=self.asset, is_primary=True)

    def test_top_products_include_sized_image_sources(self):
        OrderItemFactory(order=OrderFactory(paid_order=True), product=self.product)

        rows = AnalyticsService.get_top_products(period="7_days", limit=5)

        row = next(r for r in rows if r["product_id"] == self.product.id)
        self.assertTrue(row["image_url"])
        self.assertIsInstance(row["image_sources"], dict)
        self.assertIn("medium", row["image_sources"])

    def test_product_analytics_includes_sized_image_sources(self):
        today = timezone.now().date()
        OrderItemFactory(order=OrderFactory(paid_order=True), product=self.product)

        result = AnalyticsService.get_product_analytics(start_date=today, end_date=today)

        row = next(r for r in result["results"] if r["product_id"] == self.product.id)
        self.assertTrue(row["image_url"])
        self.assertIsInstance(row["image_sources"], dict)
