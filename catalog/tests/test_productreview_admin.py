"""
Regression tests for the Product Review admin surface.

Covers the tabbed ProductReview change form and the Reviews dashboard added to
``catalog.admin.ProductReviewAdmin`` / ``catalog.admin_views.review_dashboard``.

What is guarded here:

1. The change page renders the tab navigation and its four tabs, the custom
   form id, and — crucially — the image grid with URLs *normalised* out of the
   ``images`` JSONField, which may hold bare URL strings AND ``{"url": ...}``
   dicts. Both shapes must resolve to a rendered ``<img src>``.
2. ``change_view`` injects purchase + attribution context: a delivered order
   for the reviewed product makes ``computed_verified_purchase`` True, surfaces
   the order number, and the reviewer's attribution TouchPoint appears in the
   journey timeline.
3. A POST through the custom change form saves and updates the DB (title edit +
   ``is_approved`` toggle).
4. The dashboard returns its KPI context and top product, with markers the
   front-end JS binds to.
5. A non-staff user is denied the dashboard (deny-by-default).

All requests run as a superuser (the repo is deny-by-default for staff), against
a real Postgres DB. A ``SiteSettings(pk=1)`` row with ``admin_email`` is seeded
or the currency middleware 500s every admin request.
"""

import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from djmoney.money import Money

from catalog.models import Category, Product, ProductReview

User = get_user_model()


def _ensure_site_settings():
    """Currency middleware needs a valid SiteSettings(pk=1) on every request."""
    from django.contrib.sites.models import Site

    from core.models import SiteSettings

    Site.objects.update_or_create(pk=1, defaults={"domain": "localhost", "name": "Test Site"})
    SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "admin_email": "admin@example.com",
            "default_currency": "USD",
            "enable_multi_warehouse": False,
        },
    )


def _make_product(name, slug, sku):
    category, _ = Category.objects.get_or_create(name="Reviews Cat", slug="reviews-cat")
    return Product.objects.create(
        name=name,
        slug=slug,
        sku=sku,
        price=Money(100, "USD"),
        category=category,
    )


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ProductReviewChangeFormTest(TestCase):
    """The tabbed ProductReview change form renders its structure and images."""

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.reviewer = User.objects.create_user(
            username="reviewer", email="reviewer@test.com", password="pw"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

        self.product = _make_product("Widget", "widget", "WID-1")
        self.bare_url = "https://cdn.example.com/bare-string.jpg"
        self.dict_url = "https://cdn.example.com/dict-url.jpg"
        self.review = ProductReview.objects.create(
            product=self.product,
            user=self.reviewer,
            rating=4,
            title="Solid widget",
            comment="Works as described.",
            is_approved=False,
            is_verified_purchase=False,
            # Deliberately mixed shapes: a bare string AND a {"url": ...} dict.
            images=[self.bare_url, {"url": self.dict_url}],
        )

    def test_change_form_renders_tabs_and_form_id(self):
        url = reverse("admin:catalog_productreview_change", args=[self.review.pk])
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        # Tab nav container + the four tab buttons.
        self.assertIn('class="admin-tabs"', content)
        for tab in ("review", "customer", "purchase", "advanced"):
            self.assertIn(f'data-tab="{tab}"', content)

        # Custom form id (the JS binds save buttons to this).
        self.assertIn('id="productreview_form"', content)

    def test_change_form_normalises_mixed_image_shapes(self):
        """The image grid must render URLs from BOTH bare strings and dicts.

        This is the guard on the ``review_images`` normalisation in
        ``ProductReviewAdmin._review_context`` — a regression there (e.g. only
        handling one shape) drops half the images silently.
        """
        url = reverse("admin:catalog_productreview_change", args=[self.review.pk])
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertIn("review-image-grid", content)
        # Context is normalised to {"i": raw_index, "url": safe_url} entries so
        # the gallery can offer per-image deletion by original index.
        entries = response.context["review_images"]
        self.assertEqual([e["url"] for e in entries], [self.bare_url, self.dict_url])
        self.assertEqual([e["i"] for e in entries], [0, 1])
        # Both URLs are actually rendered into the grid, with a delete control.
        self.assertIn(self.bare_url, content)
        self.assertIn(self.dict_url, content)
        self.assertIn("review-image-delete", content)


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ProductReviewChangeViewContextTest(TestCase):
    """change_view injects purchase + attribution context for a real order."""

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.reviewer = User.objects.create_user(
            username="buyer", email="buyer@test.com", password="pw"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

        self.product = _make_product("Gadget", "gadget", "GAD-1")
        self.review = ProductReview.objects.create(
            product=self.product,
            user=self.reviewer,
            rating=5,
            title="Great gadget",
            comment="Bought it and love it.",
            is_approved=True,
            is_verified_purchase=False,
        )

        # A delivered order for the reviewer containing the reviewed product.
        from orders.models import Order, OrderItem

        self.order = Order.objects.create(
            order_number="ORD-VERIFY-1",
            user=self.reviewer,
            status="delivered",
            source="email",
            subtotal=Money(100, "USD"),
            total_amount=Money(100, "USD"),
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            sku=self.product.sku,
            quantity=1,
            unit_price=Money(100, "USD"),
            total_price=Money(100, "USD"),
        )

        # An attribution touch for the reviewer (customer-scoped journey).
        from attribution.models import TouchPoint

        self.touch = TouchPoint.objects.create(
            visitor_key="visitor-abc",
            customer=self.reviewer,
            channel="email",
            source="newsletter",
            is_bot=False,
        )

    def test_context_flags_verified_purchase_and_journey(self):
        url = reverse("admin:catalog_productreview_change", args=[self.review.pk])
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)

        # Context assertions.
        self.assertTrue(response.context["computed_verified_purchase"])
        self.assertTrue(response.context["product_orders"])
        self.assertEqual(response.context["product_orders"][0]["number"], "ORD-VERIFY-1")
        self.assertTrue(response.context["attribution_touches"])

    def test_rendered_page_shows_order_verified_badge_and_touch(self):
        url = reverse("admin:catalog_productreview_change", args=[self.review.pk])
        response = self.client.get(url, SERVER_NAME="localhost")
        content = response.content.decode("utf-8")

        # Order number surfaced in the Purchase tab.
        self.assertIn("ORD-VERIFY-1", content)
        # Verified-purchase badge shown because a delivered order exists.
        self.assertIn("Verified purchase", content)
        # Journey timeline present and the touch's channel/source rendered.
        self.assertIn("journey-timeline", content)
        self.assertIn("newsletter", content)


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ProductReviewChangeFormPostTest(TestCase):
    """POSTing the custom change form saves and updates the DB."""

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.reviewer = User.objects.create_user(
            username="poster", email="poster@test.com", password="pw"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

        self.product = _make_product("Doohickey", "doohickey", "DOO-1")
        self.review = ProductReview.objects.create(
            product=self.product,
            user=self.reviewer,
            rating=3,
            title="Original title",
            comment="Some comment.",
            is_approved=False,
            is_verified_purchase=False,
            images=[],
        )

    def test_post_edits_title_and_toggles_approval(self):
        url = reverse("admin:catalog_productreview_change", args=[self.review.pk])
        # Build POST deterministically from the object rather than scraping the
        # autocomplete widgets.
        data = {
            "product": self.review.product_id,
            "user": self.review.user_id,
            "rating": self.review.rating,
            "title": "Edited title",
            "comment": self.review.comment,
            "images": json.dumps(self.review.images),
            "is_approved": "on",  # toggle False -> True
            "_save": "1",
        }
        response = self.client.post(url, data, SERVER_NAME="localhost")
        # A successful admin save redirects to the changelist.
        self.assertEqual(response.status_code, 302)

        self.review.refresh_from_db()
        self.assertEqual(self.review.title, "Edited title")
        self.assertTrue(self.review.is_approved)

    def test_product_and_user_are_readonly_on_change(self):
        """A review's product/user must not be reassignable once it exists."""
        url = reverse("admin:catalog_productreview_change", args=[self.review.pk])
        content = self.client.get(url, SERVER_NAME="localhost").content.decode()
        self.assertNotRegex(content, r'<select[^>]*name="product"')
        self.assertNotRegex(content, r'<select[^>]*name="user"')

    def test_post_deletes_marked_image(self):
        """delete_image indices are removed from the images JSON on save."""
        review = ProductReview.objects.create(
            product=_make_product("Imgy", "imgy", "IMG-1"),
            user=self.reviewer,
            rating=4,
            title="pics",
            comment="c",
            images=["https://ex.com/a.jpg", "https://ex.com/b.jpg"],
        )
        url = reverse("admin:catalog_productreview_change", args=[review.pk])
        data = {
            "rating": review.rating,
            "title": review.title,
            "comment": review.comment,
            "delete_image": "0",
            "_save": "1",
        }
        response = self.client.post(url, data, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 302)
        review.refresh_from_db()
        self.assertEqual(review.images, ["https://ex.com/b.jpg"])

    def test_post_adds_image_url(self):
        """add_image_url appends a safe URL to the images JSON on save."""
        review = ProductReview.objects.create(
            product=_make_product("Addy", "addy", "ADD-1"),
            user=self.reviewer,
            rating=4,
            title="add",
            comment="c",
            images=[],
        )
        url = reverse("admin:catalog_productreview_change", args=[review.pk])
        data = {
            "rating": review.rating,
            "title": review.title,
            "comment": review.comment,
            "add_image_url": "https://ex.com/new.jpg",
            "_save": "1",
        }
        response = self.client.post(url, data, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 302)
        review.refresh_from_db()
        self.assertEqual(review.images, ["https://ex.com/new.jpg"])


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ReviewDashboardTest(TestCase):
    """The Reviews dashboard returns KPI context, markers, and a top product."""

    def setUp(self):
        _ensure_site_settings()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin123"
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

        # Two products; product A gets two reviews so it tops the ranking.
        self.product_a = _make_product("Alpha Product", "alpha-product", "ALP-1")
        self.product_b = _make_product("Beta Product", "beta-product", "BET-1")
        u1 = User.objects.create_user(username="rev1", email="rev1@test.com", password="pw")
        u2 = User.objects.create_user(username="rev2", email="rev2@test.com", password="pw")
        u3 = User.objects.create_user(username="rev3", email="rev3@test.com", password="pw")
        ProductReview.objects.create(
            product=self.product_a, user=u1, rating=5, title="a1", comment="c", is_approved=True
        )
        ProductReview.objects.create(
            product=self.product_a, user=u2, rating=4, title="a2", comment="c", is_approved=True
        )
        ProductReview.objects.create(
            product=self.product_b, user=u3, rating=3, title="b1", comment="c", is_approved=False
        )

    def test_dashboard_renders_kpis_and_top_product(self):
        url = reverse("catalog_admin:review_dashboard")
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        # Front-end markers the dashboard JS binds to.
        self.assertIn("reviews-dashboard", content)
        self.assertIn("reviews-dashboard-data", content)

        # KPI context matches the reviews created.
        self.assertEqual(response.context["total_reviews"], 3)
        self.assertEqual(response.context["approved_reviews"], 2)
        self.assertEqual(response.context["pending_reviews"], 1)

        # The most-reviewed product tops the ranking and is rendered.
        self.assertTrue(response.context["top_products"])
        # top_products are Product instances (so the template can show thumbnails).
        self.assertEqual(response.context["top_products"][0].name, "Alpha Product")
        self.assertEqual(response.context["top_products"][0].review_count, 2)
        self.assertIn("Alpha Product", content)

    def test_dashboard_json_blob_is_valid(self):
        url = reverse("catalog_admin:review_dashboard")
        response = self.client.get(url, SERVER_NAME="localhost")
        # The rating distribution blob must be parseable JSON covering 1..5.
        dist = json.loads(response.context["rating_distribution_json"])
        self.assertEqual([row["rating"] for row in dist], [1, 2, 3, 4, 5])


@override_settings(ALLOWED_HOSTS=["localhost", "testserver"])
class ReviewDashboardAccessTest(TestCase):
    """A non-staff user must be denied the dashboard (deny-by-default)."""

    def setUp(self):
        _ensure_site_settings()
        self.customer = User.objects.create_user(
            username="customer", email="customer@test.com", password="pw"
        )
        self.client = Client()

    def test_non_staff_is_denied(self):
        self.client.force_login(self.customer)
        url = reverse("catalog_admin:review_dashboard")
        response = self.client.get(url, SERVER_NAME="localhost")
        # staff_member_required bounces a non-staff user to the admin login.
        self.assertIn(response.status_code, (302, 403))
        if response.status_code == 302:
            self.assertIn("login", response.url)

    def test_anonymous_is_denied(self):
        url = reverse("catalog_admin:review_dashboard")
        response = self.client.get(url, SERVER_NAME="localhost")
        self.assertIn(response.status_code, (302, 403))
