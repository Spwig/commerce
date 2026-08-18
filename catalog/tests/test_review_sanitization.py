"""Reviews are untrusted plain-text customer content — hardening tests.

Covers: (1) the API serializer strips HTML from customer submissions,
(2) storefront output rendering neutralises stored HTML, (3) the ORM path used
by platform migration importers is deliberately UNCHANGED (imports must keep
working), and (4) the optional cleanup command.
"""

import os
from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.template import engines
from django.test import TestCase

from catalog.models import Category, Product, ProductReview
from catalog.serializers import ProductReviewSerializer

User = get_user_model()


def _make_product(name, slug, sku):
    cat, _ = Category.objects.get_or_create(slug="san", defaults={"name": "San"})
    return Product.objects.create(
        name=name, slug=slug, sku=sku, price=Decimal("9.99"), category=cat
    )


class ReviewSerializerStripsHtmlTest(TestCase):
    def test_validate_comment_strips_tags(self):
        s = ProductReviewSerializer()
        self.assertEqual(s.validate_comment("<p>genuine, nice</p>"), "genuine, nice")
        # Script payload: tags removed, nothing executable remains as markup.
        cleaned = s.validate_comment("<script>alert(1)</script>Nice")
        self.assertNotIn("<", cleaned)
        # An event-handler img is removed entirely.
        self.assertEqual(s.validate_comment("<img src=x onerror=alert(1)>"), "")

    def test_validate_title_strips_tags(self):
        s = ProductReviewSerializer()
        self.assertEqual(s.validate_title("<b>Great</b>"), "Great")


class ReviewOutputIsSafeTest(TestCase):
    def test_striptags_linebreaks_neutralises_html(self):
        """The storefront render chain (comment|striptags|linebreaks) must never
        emit raw script/markup from a review."""
        dj = engines["django"]
        tmpl = dj.from_string("{{ c|striptags|linebreaks }}")
        out = tmpl.render({"c": "<script>alert(1)</script>Nice product\nSecond line"})
        self.assertNotIn("<script>", out)
        self.assertIn("Nice product", out)
        # linebreaks still formats the plain-text newline.
        self.assertIn("<br>", out.replace("<br />", "<br>"))

    def test_product_templates_do_not_use_safe(self):
        """Guard: the two product-page review renders stay sanitised."""
        base = os.path.join(os.path.dirname(__file__), "..", "..", "page_builder", "templates")
        for rel in [
            "page_builder/simple_product.html",
            "page_builder/product/_tabs.html",
        ]:
            with open(os.path.normpath(os.path.join(base, rel)), encoding="utf-8") as fh:
                content = fh.read()
            self.assertNotIn("review.comment|safe", content, f"{rel} renders review HTML raw")
            self.assertIn("review.comment|striptags", content, f"{rel} lost its striptags")


class ImporterOrmPathUnchangedTest(TestCase):
    """Platform migration importers create reviews via the ORM directly. That
    path must remain untouched so Woo/Shopify/Magento imports keep working —
    output sanitisation protects the stored HTML at render time instead."""

    def test_orm_create_preserves_raw_comment(self):
        user = User.objects.create_user("importbuyer", "ib@example.com", "pw")
        product = _make_product("Imported", "imported", "IMP-1")
        review = ProductReview.objects.create(
            product=product,
            user=user,
            rating=5,
            title="<b>t</b>",
            comment="<p>genuine, really nice blue color</p>",
            is_approved=True,
        )
        review.refresh_from_db()
        # Unchanged — the importer stored exactly what it was given.
        self.assertEqual(review.comment, "<p>genuine, really nice blue color</p>")
        self.assertEqual(review.title, "<b>t</b>")


class SanitizeReviewCommentsCommandTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("cmdbuyer", "cb@example.com", "pw")
        self.product = _make_product("Cmd", "cmd", "CMD-1")
        self.review = ProductReview.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            title="<b>Nice</b>",
            comment="<p>html here</p>",
            is_approved=True,
        )

    def test_dry_run_does_not_change(self):
        out = StringIO()
        call_command("sanitize_review_comments", stdout=out)
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, "<p>html here</p>")
        self.assertIn("Would update", out.getvalue())

    def test_apply_strips_html(self):
        call_command("sanitize_review_comments", "--apply")
        self.review.refresh_from_db()
        self.assertEqual(self.review.comment, "html here")
        self.assertEqual(self.review.title, "Nice")
