"""Behaviour tests for the commerce block context providers (P1 extension).

``email_marketing/block_context.py`` enriches a commerce block's render context
with live catalog data at render time. These tests exercise the two providers
directly against real catalog products (no mocks — the visibility filter, price
formatting, and image-source shaping all run for real):

* ``featured_product_context`` — resolve one product by id.
* ``product_grid_context`` — resolve a curated row by mode (new/bestsellers/sale)
  with a clamped count.

They also cover the canvas render path (``render_block_canvas``) for the
image-present and empty states.
"""

from datetime import timedelta

from django.utils import timezone

from catalog.models import Product, ProductImage
from email_marketing.block_context import (
    blog_posts_context,
    featured_product_context,
    product_grid_context,
)
from email_marketing.models import Campaign, CampaignBlock
from email_marketing.services.block_serializer import render_block_canvas
from tests.factories import MediaAssetFactory, ProductFactory

from .base import MarketingTestCase


class _CommerceContextBase(MarketingTestCase):
    """Shared product builders for the commerce context tests."""

    def _product(self, name, **kwargs):
        """A published, storefront-visible product with a unique name/slug.

        ``status`` defaults to ``published`` but callers may override it (e.g.
        to build a draft for the visibility-filter tests)."""
        kwargs.setdefault("status", "published")
        return ProductFactory(name=name, **kwargs)

    def _set_created_at(self, product, when):
        """created_at is auto_now_add, so stagger it deterministically post-save."""
        Product.objects.filter(pk=product.pk).update(created_at=when)

    def _make_on_sale(self, name, **kwargs):
        """A product with an active, price-reducing sale (percentage off)."""
        return self._product(
            name,
            sale_type="percentage_off",
            sale_value="20.00",
            sale_start_date=None,
            sale_end_date=None,
            **kwargs,
        )

    def _canvas_block(self, block_type, content):
        campaign = Campaign.objects.create(
            site=self.site, name="Canvas test", subject="Canvas test"
        )
        return CampaignBlock.objects.create(
            campaign=campaign, block_type=block_type, content=content, order=0
        )


# ---------------------------------------------------------------------------
# product_grid_context — mode + count behaviour (task item 3)
# ---------------------------------------------------------------------------


class ProductGridModeAndCountTests(_CommerceContextBase):
    def test_mode_new_returns_products_newest_first(self):
        base = timezone.now()
        products = []
        for i in range(5):
            p = self._product(f"New Arrival {i}")
            self._set_created_at(p, base + timedelta(minutes=i))
            products.append(p)

        ctx = product_grid_context({"mode": "new", "count": "4"})

        # count clamps to 4; newest (index 4) first, descending by created_at.
        self.assertEqual(ctx["count"], 4)
        names = [p["name"] for p in ctx["products"]]
        self.assertEqual(
            names,
            ["New Arrival 4", "New Arrival 3", "New Arrival 2", "New Arrival 1"],
        )

    def test_count_clamps_to_upper_bound_of_four(self):
        for i in range(6):
            self._product(f"Bulk {i}")

        huge = product_grid_context({"mode": "new", "count": "99"})
        self.assertEqual(huge["count"], 4)
        self.assertLessEqual(len(huge["products"]), 4)

    def test_count_of_two_returns_exactly_two(self):
        for i in range(5):
            self._product(f"Pair {i}")

        ctx = product_grid_context({"mode": "new", "count": "2"})
        self.assertEqual(ctx["count"], 2)
        self.assertEqual(len(ctx["products"]), 2)

    def test_invalid_count_falls_back_to_default_within_bounds(self):
        for i in range(5):
            self._product(f"Fallback {i}")

        ctx = product_grid_context({"mode": "new", "count": "abc"})
        # Non-numeric count -> provider default of 3 (still <= 4).
        self.assertEqual(ctx["count"], 3)
        self.assertLessEqual(len(ctx["products"]), 4)

    def test_zero_count_clamps_up_to_one(self):
        self._product("Solo")
        ctx = product_grid_context({"mode": "new", "count": "0"})
        self.assertEqual(ctx["count"], 1)

    def test_mode_bestsellers_orders_by_sales_count_desc(self):
        self._product("Slow Mover", sales_count=5)
        self._product("Chart Topper", sales_count=50)
        self._product("Mid Seller", sales_count=20)

        ctx = product_grid_context({"mode": "bestsellers", "count": "3"})
        names = [p["name"] for p in ctx["products"]]
        self.assertEqual(names, ["Chart Topper", "Mid Seller", "Slow Mover"])

    def test_mode_sale_returns_only_products_currently_on_sale(self):
        self._make_on_sale("Discounted Widget")
        self._product("Full Price Widget")  # sale_type defaults to "none"

        ctx = product_grid_context({"mode": "sale", "count": "4"})
        names = [p["name"] for p in ctx["products"]]
        self.assertEqual(names, ["Discounted Widget"])
        self.assertNotIn("Full Price Widget", names)


# ---------------------------------------------------------------------------
# Visibility filter — draft + hidden products excluded (task item 3)
# ---------------------------------------------------------------------------


class ProductGridVisibilityTests(_CommerceContextBase):
    def test_draft_and_hidden_products_never_appear_in_any_mode(self):
        visible = self._make_on_sale("Visible On Sale", sales_count=99)
        # A draft and a hidden product, both otherwise sale-eligible & popular.
        self._make_on_sale("Draft On Sale", status="draft", sales_count=99)
        self._make_on_sale("Hidden On Sale", hide_from_storefront=True, sales_count=99)

        for mode in ("new", "bestsellers", "sale"):
            ctx = product_grid_context({"mode": mode, "count": "4"})
            names = [p["name"] for p in ctx["products"]]
            self.assertIn(visible.name, names, f"visible product missing in mode={mode}")
            self.assertNotIn("Draft On Sale", names, f"draft leaked in mode={mode}")
            self.assertNotIn("Hidden On Sale", names, f"hidden leaked in mode={mode}")

    def test_pos_only_product_is_excluded(self):
        self._product("Storefront Product")
        self._product("In Store Only", sales_channel="pos_only")

        names = [p["name"] for p in product_grid_context({"mode": "new", "count": "4"})["products"]]
        self.assertIn("Storefront Product", names)
        self.assertNotIn("In Store Only", names)


# ---------------------------------------------------------------------------
# featured_product_context — id resolution + visibility (task item 4)
# ---------------------------------------------------------------------------


class FeaturedProductResolutionTests(_CommerceContextBase):
    def test_valid_published_id_returns_product_dict(self):
        product = self._product("Hero Product")
        ctx = featured_product_context({"product_id": str(product.id)})

        self.assertIsNotNone(ctx["product"])
        self.assertEqual(ctx["product"]["name"], "Hero Product")
        # price is a formatted display string (covered fully by item 5 below).
        self.assertTrue(any(ch.isdigit() for ch in ctx["product"]["price"]))

    def test_nonexistent_id_returns_none(self):
        ctx = featured_product_context({"product_id": "99999999"})
        self.assertEqual(ctx, {"product": None})

    def test_non_numeric_id_returns_none(self):
        ctx = featured_product_context({"product_id": "abc"})
        self.assertEqual(ctx, {"product": None})

    def test_missing_id_returns_none(self):
        self.assertEqual(featured_product_context({}), {"product": None})

    def test_draft_product_id_is_not_visible(self):
        draft = self._product("Draft Hero", status="draft")
        ctx = featured_product_context({"product_id": str(draft.id)})
        self.assertEqual(ctx, {"product": None})

    def test_hidden_product_id_is_not_visible(self):
        hidden = self._product("Hidden Hero", hide_from_storefront=True)
        ctx = featured_product_context({"product_id": str(hidden.id)})
        self.assertEqual(ctx, {"product": None})


# ---------------------------------------------------------------------------
# Price formatting + sale state (task item 5)
# ---------------------------------------------------------------------------


class PriceFormattingTests(_CommerceContextBase):
    def test_price_is_a_formatted_currency_string(self):
        product = self._product("Priced Product")  # $25.00, USD
        display = featured_product_context({"product_id": str(product.id)})["product"]

        price = display["price"]
        self.assertIsInstance(price, str)
        self.assertTrue(any(ch.isdigit() for ch in price))
        # USD formats with a "$" symbol; assert a currency marker is present.
        self.assertIn("$", price)

    def test_non_sale_product_has_no_was_price_and_on_sale_false(self):
        product = self._product("Regular Product")
        display = featured_product_context({"product_id": str(product.id)})["product"]

        self.assertFalse(display["on_sale"])
        self.assertEqual(display["was_price"], "")

    def test_on_sale_product_exposes_was_price_and_on_sale_true(self):
        product = self._make_on_sale("On Sale Product")  # 20% off $25 -> $20
        display = featured_product_context({"product_id": str(product.id)})["product"]

        self.assertTrue(display["on_sale"])
        self.assertTrue(display["was_price"])  # non-empty original price string
        self.assertTrue(any(ch.isdigit() for ch in display["was_price"]))
        # Sale price should differ from the struck-through original.
        self.assertNotEqual(display["price"], display["was_price"])


class BlogPostsContextTests(MarketingTestCase):
    def _make_post(self, title, *, status="published", days_ago=0, excerpt="A teaser."):
        from blog.models import BlogPost

        published_at = timezone.now() - timedelta(days=days_ago)
        return BlogPost.objects.create(
            title=title,
            status=status,
            excerpt=excerpt,
            published_at=published_at if status == "published" else None,
        )

    def test_returns_only_published_posts_newest_first(self):
        self._make_post("Older", days_ago=5)
        self._make_post("Newest", days_ago=1)
        self._make_post("Draft post", status="draft")

        posts = blog_posts_context({"count": "3"})["posts"]

        titles = [p["title"] for p in posts]
        self.assertEqual(titles, ["Newest", "Older"])  # draft excluded, newest first

    def test_count_clamps_to_upper_bound_of_four(self):
        for i in range(6):
            self._make_post(f"Post {i}", days_ago=i)
        self.assertEqual(len(blog_posts_context({"count": "10"})["posts"]), 4)

    def test_post_dict_carries_title_url_and_date(self):
        self._make_post("Hello World")
        post = blog_posts_context({"count": "1"})["posts"][0]

        self.assertEqual(post["title"], "Hello World")
        self.assertTrue(post["url"].startswith("http"))
        self.assertTrue(post["date"])  # formatted published date
        self.assertEqual(post["excerpt"], "A teaser.")

    def test_since_last_send_excludes_posts_at_or_before_the_watermark(self):
        self._make_post("Old news", days_ago=10)
        self._make_post("Fresh news", days_ago=1)
        watermark = timezone.now() - timedelta(days=5)

        result = blog_posts_context(
            {"source": "since_last_send", "count": "4"}, {"since": watermark}
        )
        titles = [p["title"] for p in result["posts"]]
        self.assertEqual(titles, ["Fresh news"])  # only posts newer than the watermark

    def test_since_last_send_returns_nothing_when_no_new_posts(self):
        self._make_post("Old news", days_ago=10)
        watermark = timezone.now() - timedelta(days=1)

        result = blog_posts_context(
            {"source": "since_last_send", "count": "4"}, {"since": watermark}
        )
        self.assertEqual(result["posts"], [])  # never re-send the same posts

    def test_since_last_send_without_watermark_falls_back_to_latest(self):
        self._make_post("Any post", days_ago=10)
        # No 'since' in render_ctx (a first send / the builder canvas).
        result = blog_posts_context({"source": "since_last_send", "count": "4"}, {})
        self.assertEqual(len(result["posts"]), 1)


class BlogSinceRenderThreadingTests(MarketingTestCase):
    """The campaign's watermark must reach the blog provider through the render."""

    def _post(self, title, days_ago):
        from blog.models import BlogPost

        return BlogPost.objects.create(
            title=title,
            status="published",
            excerpt="x",
            published_at=timezone.now() - timedelta(days=days_ago),
        )

    def test_sent_campaign_watermark_filters_since_last_send_block(self):
        self._post("Before", days_ago=10)
        self._post("After", days_ago=1)
        campaign = Campaign.objects.create(
            site=self.site,
            name="Weekly",
            subject="Hi",
            last_content_sent_at=timezone.now() - timedelta(days=5),
        )
        block = CampaignBlock.objects.create(
            campaign=campaign,
            block_type="blog_posts",
            content={"source": "since_last_send", "count": "4", "layout": "list"},
            order=0,
        )

        html = render_block_canvas(block)
        self.assertIn("After", html)
        self.assertNotIn("Before", html)


# ---------------------------------------------------------------------------
# Image sources + canvas render (task item 6)
# ---------------------------------------------------------------------------


class ImageSourcesTests(_CommerceContextBase):
    def _attach_primary_image(self, product):
        asset = MediaAssetFactory()
        ProductImage.objects.create(product=product, media_asset=asset, is_primary=True)
        return asset

    def test_product_with_image_returns_absolute_fallback_and_canvas_has_picture(self):
        product = self._product("Imaged Product")
        self._attach_primary_image(product)

        display = featured_product_context({"product_id": str(product.id)})["product"]
        self.assertIsNotNone(display["image"])
        self.assertTrue(
            display["image"]["fallback"].startswith("http"),
            f"fallback URL not absolutised: {display['image']['fallback']!r}",
        )

        block = self._canvas_block("featured_product", {"product_id": str(product.id)})
        canvas = render_block_canvas(block)
        self.assertIn("<picture>", canvas)
        self.assertIn("em-block-product", canvas)

    def test_product_without_image_has_none_image_and_no_picture_in_canvas(self):
        product = self._product("Imageless Product")

        display = featured_product_context({"product_id": str(product.id)})["product"]
        self.assertIsNone(display["image"])

        block = self._canvas_block("featured_product", {"product_id": str(product.id)})
        canvas = render_block_canvas(block)
        # Product exists, so the product card renders — but with no <picture>.
        self.assertIn("em-block-product", canvas)
        self.assertNotIn("<picture>", canvas)

    def test_featured_canvas_empty_state_when_no_product_resolved(self):
        block = self._canvas_block("featured_product", {"product_id": "99999999"})
        canvas = render_block_canvas(block)
        self.assertIn("em-product-empty", canvas)
        self.assertNotIn("<picture>", canvas)

    def test_product_grid_canvas_renders_pictures_for_imaged_products(self):
        p1 = self._product("Grid Img A")
        p2 = self._product("Grid Img B")
        self._attach_primary_image(p1)
        self._attach_primary_image(p2)

        block = self._canvas_block("product_grid", {"mode": "new", "count": "2"})
        canvas = render_block_canvas(block)
        self.assertIn("em-block-grid", canvas)
        self.assertEqual(canvas.count("<picture>"), 2)

    def test_product_grid_canvas_empty_state_when_no_products(self):
        block = self._canvas_block("product_grid", {"mode": "new", "count": "3"})
        canvas = render_block_canvas(block)
        self.assertIn("em-product-empty", canvas)


class ProductGridSinceModeTests(_CommerceContextBase):
    def test_new_since_send_returns_only_products_created_after_watermark(self):
        old = self._product("Old arrival")
        new = self._product("Fresh arrival")
        self._set_created_at(old, timezone.now() - timedelta(days=10))
        self._set_created_at(new, timezone.now() - timedelta(days=1))
        watermark = timezone.now() - timedelta(days=5)

        result = product_grid_context(
            {"mode": "new_since_send", "count": "4"}, {"since": watermark}
        )
        names = [p["name"] for p in result["products"]]
        self.assertIn("Fresh arrival", names)
        self.assertNotIn("Old arrival", names)

    def test_new_since_send_without_watermark_falls_back_to_new(self):
        self._product("Anything")
        result = product_grid_context({"mode": "new_since_send", "count": "4"}, {})
        self.assertTrue(result["products"])


class RegionVisibilityTests(_CommerceContextBase):
    """Region-restricted products must not leak into email commerce blocks."""

    def _regions(self):
        from catalog.models import SalesRegion

        home = SalesRegion.objects.create(
            name="Home", code="HOME", default_currency="USD", is_active=True, priority=10
        )
        other = SalesRegion.objects.create(
            name="Other", code="OTH", default_currency="USD", is_active=True, priority=1
        )
        return home, other

    def test_region_restricted_product_is_excluded_for_the_default_market(self):
        from catalog.models import ProductRegionVisibility
        from email_marketing.block_context import _visible_products

        _home, other = self._regions()
        everywhere = self._product("Everywhere")
        other_only = self._product("Other only", region_restriction_mode="only_in")
        ProductRegionVisibility.objects.create(product=other_only, region=other, is_visible=True)

        visible = set(_visible_products().values_list("id", flat=True))
        self.assertIn(everywhere.id, visible)
        self.assertNotIn(other_only.id, visible)

    def test_single_market_store_is_unaffected(self):
        # No SalesRegion rows → the region filter is a no-op; everything visible.
        from email_marketing.block_context import _visible_products

        p = self._product("Anything")
        self.assertIn(p.id, set(_visible_products().values_list("id", flat=True)))
