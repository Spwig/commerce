"""
Behaviour tests for the inventory-intelligence & document SiteSettings that were
wired up on 2026-08-15:

- velocity_calculation_window_days -> reorder-suggestion velocity divisor/window
- document_logo_width             -> store logo drawn on generated PDFs
- allow_backorders_by_default     -> seeded onto new products at creation
- low_stock_alert_frequency /
  enable_low_stock_alerts          -> realtime signal gating + daily/weekly digest
"""

import io
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from core.models import SiteSettings
from tests.factories import (
    CategoryFactory,
    MediaAssetFactory,
    ProductFactory,
    StockItemFactory,
)

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


@pytest.fixture
def settings_row(db):
    return SiteSettings.get_settings()


# ---------------------------------------------------------------------------
# velocity_calculation_window_days
# ---------------------------------------------------------------------------


def _record_fulfillment(stock_item, units, days_ago):
    """Create a fulfillment StockMovement dated `days_ago` days in the past."""
    from catalog.models import StockMovement

    mv = StockMovement.objects.create(
        stock_item=stock_item,
        movement_type="fulfillment",
        quantity=-units,
        previous_quantity=0,
        new_quantity=0,
    )
    # created_at is auto_now_add; override it directly for the test.
    StockMovement.objects.filter(pk=mv.pk).update(
        created_at=timezone.now() - timedelta(days=days_ago)
    )
    return mv


def test_reorder_velocity_divisor_follows_window_setting(settings_row):
    """The daily-velocity divisor in reorder suggestions tracks the window setting."""
    from admin_api.services.inventory_service import InventoryService

    # The factory creates a non-main warehouse with stock; keep multi-warehouse on
    # so re-saving SiteSettings below doesn't trip its consolidation guard.
    settings_row.enable_multi_warehouse = True
    settings_row.save()

    product = ProductFactory(status="published", track_inventory=True, low_stock_threshold=5)
    stock = StockItemFactory(product=product, on_hand=3, allocated=0)
    # 30 units sold recently (inside any reasonable window).
    _record_fulfillment(stock, units=30, days_ago=3)

    settings_row.velocity_calculation_window_days = 30
    settings_row.save()
    res30 = InventoryService.get_reorder_suggestions()
    v30 = next(s for s in res30["suggestions"] if s["product_id"] == product.id)["velocity_30d"]

    settings_row.velocity_calculation_window_days = 10
    settings_row.save()
    res10 = InventoryService.get_reorder_suggestions()
    v10 = next(s for s in res10["suggestions"] if s["product_id"] == product.id)["velocity_30d"]

    # Same 30 units, narrower window => higher daily velocity (30/10 > 30/30).
    assert float(v30) == pytest.approx(1.0, abs=0.01)
    assert float(v10) == pytest.approx(3.0, abs=0.01)


def test_reorder_velocity_window_excludes_older_sales(settings_row):
    """Sales older than the window are not counted toward velocity."""
    from admin_api.services.inventory_service import InventoryService

    settings_row.enable_multi_warehouse = True
    settings_row.save()

    product = ProductFactory(status="published", track_inventory=True, low_stock_threshold=5)
    stock = StockItemFactory(product=product, on_hand=0, allocated=0)
    # Sale 20 days ago: inside a 30-day window, outside a 15-day window.
    _record_fulfillment(stock, units=30, days_ago=20)

    settings_row.velocity_calculation_window_days = 30
    settings_row.save()
    res30 = InventoryService.get_reorder_suggestions()
    s30 = next(s for s in res30["suggestions"] if s["product_id"] == product.id)
    assert float(s30["velocity_30d"]) > 0

    settings_row.velocity_calculation_window_days = 15
    settings_row.save()
    res15 = InventoryService.get_reorder_suggestions()
    s15 = next(s for s in res15["suggestions"] if s["product_id"] == product.id)
    # Out of stock with no in-window sales => zero velocity.
    assert float(s15["velocity_30d"]) == 0


# ---------------------------------------------------------------------------
# document_logo_width
# ---------------------------------------------------------------------------


def _png_asset(width=400, height=200):
    from PIL import Image as PILImage

    buf = io.BytesIO()
    PILImage.new("RGB", (width, height), (10, 20, 30)).save(buf, format="PNG")
    return MediaAssetFactory(
        png=True,
        original_file=SimpleUploadedFile("logo.png", buf.getvalue(), content_type="image/png"),
    )


def test_document_header_has_no_logo_when_unset(settings_row):
    from admin_api.views.documents import _build_logo_flowable

    settings_row.site_logo = None
    settings_row.save()
    assert _build_logo_flowable(settings_row) is None


def test_document_logo_rendered_at_configured_width(settings_row):
    from reportlab.platypus import Image as RLImage

    from admin_api.views.documents import _build_logo_flowable

    settings_row.site_logo = _png_asset(width=400, height=200)
    settings_row.document_logo_width = 200  # px
    settings_row.save()

    flowable = _build_logo_flowable(settings_row)
    assert isinstance(flowable, RLImage)
    # 200 px -> 150 pt (72/96), aspect 2:1 -> 75 pt tall.
    assert flowable.drawWidth == pytest.approx(150.0, abs=0.5)
    assert flowable.drawHeight == pytest.approx(75.0, abs=0.5)


def test_document_svg_logo_is_skipped(settings_row):
    """reportlab can't embed SVG, so an SVG logo yields a text-only header."""
    from admin_api.views.documents import _build_logo_flowable

    settings_row.site_logo = MediaAssetFactory(
        svg=True,
        original_file=SimpleUploadedFile(
            "logo.svg",
            b"<svg xmlns='http://www.w3.org/2000/svg'></svg>",
            content_type="image/svg+xml",
        ),
    )
    settings_row.save()
    assert _build_logo_flowable(settings_row) is None


# ---------------------------------------------------------------------------
# allow_backorders_by_default
# ---------------------------------------------------------------------------


def _make_product_via_api(data):
    from admin_api.views.products import _create_single_product

    return _create_single_product(data)


def test_new_product_inherits_store_backorder_default_true(settings_row):
    settings_row.allow_backorders_by_default = True
    settings_row.save()
    category = CategoryFactory()

    product = _make_product_via_api(
        {"name": "Widget A", "sku": "WA-1", "category_id": category.id, "price": "19.99"}
    )
    assert product.allow_backorders is True


def test_new_product_inherits_store_backorder_default_false(settings_row):
    settings_row.allow_backorders_by_default = False
    settings_row.save()
    category = CategoryFactory()

    product = _make_product_via_api(
        {"name": "Widget B", "sku": "WB-1", "category_id": category.id, "price": "19.99"}
    )
    assert product.allow_backorders is False


def test_explicit_backorder_value_overrides_store_default(settings_row):
    settings_row.allow_backorders_by_default = True
    settings_row.save()
    category = CategoryFactory()

    product = _make_product_via_api(
        {
            "name": "Widget C",
            "sku": "WC-1",
            "category_id": category.id,
            "price": "19.99",
            "allow_backorders": False,
        }
    )
    assert product.allow_backorders is False


def test_admin_add_form_seeds_backorder_default(settings_row):
    from django.contrib.admin.sites import AdminSite
    from django.test import RequestFactory

    from catalog.admin import ProductAdmin
    from catalog.models import Product

    settings_row.allow_backorders_by_default = True
    settings_row.save()

    admin = ProductAdmin(Product, AdminSite())
    request = RequestFactory().get("/admin/catalog/product/add/")
    initial = admin.get_changeform_initial_data(request)
    assert initial.get("allow_backorders") is True


# ---------------------------------------------------------------------------
# low_stock_alert_frequency + enable_low_stock_alerts
# ---------------------------------------------------------------------------


def test_realtime_alert_suppressed_when_frequency_not_realtime(settings_row):
    settings_row.enable_low_stock_alerts = True
    settings_row.low_stock_alert_frequency = "daily"
    settings_row.save()

    with patch("admin_api.tasks.send_low_stock_push_notification.delay") as delay:
        product = ProductFactory(track_inventory=True, low_stock_threshold=5)
        StockItemFactory(product=product, on_hand=2, allocated=0)  # drops below threshold
    assert not delay.called


def test_realtime_alert_suppressed_when_alerts_disabled(settings_row):
    settings_row.enable_low_stock_alerts = False
    settings_row.low_stock_alert_frequency = "realtime"
    settings_row.save()

    with patch("admin_api.tasks.send_low_stock_push_notification.delay") as delay:
        product = ProductFactory(track_inventory=True, low_stock_threshold=5)
        StockItemFactory(product=product, on_hand=2, allocated=0)
    assert not delay.called


def test_realtime_alert_fires_when_enabled_and_realtime(settings_row):
    settings_row.enable_low_stock_alerts = True
    settings_row.low_stock_alert_frequency = "realtime"
    settings_row.save()

    with patch("admin_api.tasks.send_low_stock_push_notification.delay") as delay:
        product = ProductFactory(track_inventory=True, low_stock_threshold=5)
        StockItemFactory(product=product, on_hand=2, allocated=0)
    assert delay.called


def test_digest_sends_only_for_matching_cadence(settings_row):
    from admin_api.tasks import send_low_stock_digest

    settings_row.enable_low_stock_alerts = True
    settings_row.low_stock_alert_frequency = "daily"
    settings_row.save()
    product = ProductFactory(status="published", track_inventory=True, low_stock_threshold=5)
    StockItemFactory(product=product, on_hand=1, allocated=0)

    with patch(
        "admin_api.services.push_service.PushNotificationService.send_low_stock_digest_notification",
        return_value=1,
    ) as send:
        send_low_stock_digest("daily")
        assert send.called

    with patch(
        "admin_api.services.push_service.PushNotificationService.send_low_stock_digest_notification",
        return_value=1,
    ) as send_weekly:
        send_low_stock_digest("weekly")  # store is on 'daily' -> weekly run no-ops
        assert not send_weekly.called


def test_digest_noop_when_alerts_disabled(settings_row):
    from admin_api.tasks import send_low_stock_digest

    settings_row.enable_low_stock_alerts = False
    settings_row.low_stock_alert_frequency = "daily"
    settings_row.save()
    product = ProductFactory(status="published", track_inventory=True, low_stock_threshold=5)
    StockItemFactory(product=product, on_hand=1, allocated=0)

    with patch(
        "admin_api.services.push_service.PushNotificationService.send_low_stock_digest_notification",
        return_value=1,
    ) as send:
        send_low_stock_digest("daily")
        assert not send.called
