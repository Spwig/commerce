"""Behaviour tests for the P1-extension serializer refactor.

The refactor changed ``block_serializer`` so each block renders its OWN
``<mj-section>`` (previously every block shared one section/column), and the
``_MJML_HEAD``/``_MJML_TAIL`` scaffold was updated to match. These tests confirm:

* a mixed campaign (heading + text + divider + spacer + button) still compiles
  through ``mjml_to_html`` with zero errors, and produces exactly one
  ``<mj-section>`` per block; and
* a campaign containing a ``product_grid`` commerce block, backed by real
  published products, compiles to valid MJML.

MJML compilation runs for real — nothing is mocked.
"""

from mjml.mjml2html import mjml_to_html

from email_marketing.models import Campaign, CampaignBlock
from email_marketing.services.block_serializer import serialize_campaign
from tests.factories import ProductFactory

from .base import MarketingTestCase


class SerializerRefactorTests(MarketingTestCase):
    def _campaign(self, **overrides):
        defaults = {"site": self.site, "name": "Refactor", "subject": "Refactor"}
        defaults.update(overrides)
        return Campaign.objects.create(**defaults)

    def _add_block(self, campaign, block_type, content, order):
        return CampaignBlock.objects.create(
            campaign=campaign, block_type=block_type, content=content, order=order
        )

    def test_mixed_structure_and_content_campaign_compiles_with_zero_errors(self):
        campaign = self._campaign()
        self._add_block(campaign, "heading", {"text": "Big News", "level": "h1"}, 0)
        self._add_block(campaign, "text", {"text": "Read all about it."}, 1)
        self._add_block(campaign, "divider", {"color": "#cccccc"}, 2)
        self._add_block(campaign, "spacer", {"height": "24px"}, 3)
        self._add_block(campaign, "button", {"text": "Shop", "href": "https://x.test"}, 4)

        mjml = serialize_campaign(campaign)
        result = mjml_to_html(mjml)
        self.assertEqual(list(result["errors"]), [])

        html = result["html"]
        self.assertIn("Big News", html)
        self.assertIn("Read all about it.", html)
        self.assertIn("Shop", html)

    def test_each_block_renders_its_own_mj_section(self):
        campaign = self._campaign()
        # Five blocks, each of which renders exactly one <mj-section>.
        self._add_block(campaign, "heading", {"text": "H"}, 0)
        self._add_block(campaign, "text", {"text": "T"}, 1)
        self._add_block(campaign, "divider", {}, 2)
        self._add_block(campaign, "spacer", {"height": "16px"}, 3)
        self._add_block(campaign, "button", {"text": "B", "href": "https://x.test"}, 4)

        mjml = serialize_campaign(campaign)

        # One <mj-section> opening tag per block — the crux of the refactor.
        self.assertEqual(mjml.count("<mj-section"), 5)
        self.assertEqual(mjml.count("</mj-section>"), 5)
        # And still exactly one <mj-body> frame around them all.
        self.assertEqual(mjml.count("<mj-body"), 1)

    def test_product_grid_block_compiles_to_valid_mjml_with_products(self):
        # Real published products so the grid renders <mj-column> children.
        for i in range(3):
            ProductFactory(name=f"Grid Product {i}", status="published")

        campaign = self._campaign()
        self._add_block(campaign, "heading", {"text": "This week's picks"}, 0)
        self._add_block(campaign, "product_grid", {"mode": "new", "count": "3"}, 1)

        mjml = serialize_campaign(campaign)
        result = mjml_to_html(mjml)
        self.assertEqual(list(result["errors"]), [])

        html = result["html"]
        # At least one product name made it into the compiled email.
        self.assertTrue(any(f"Grid Product {i}" in html for i in range(3)))

    def test_featured_product_block_compiles_to_valid_mjml(self):
        product = ProductFactory(name="Star Product", status="published")

        campaign = self._campaign()
        self._add_block(
            campaign,
            "featured_product",
            {"product_id": str(product.id), "button_text": "Buy now"},
            0,
        )

        mjml = serialize_campaign(campaign)
        result = mjml_to_html(mjml)
        self.assertEqual(list(result["errors"]), [])
        self.assertIn("Star Product", result["html"])

    def test_base_style_props_apply_to_the_block_section(self):
        """Inherited background, padding and border reach the <mj-section>."""
        campaign = self._campaign()
        self._add_block(
            campaign,
            "heading",
            {
                "text": "Styled",
                "section_bg": "#ff0000",
                "padding": "padding: 40px 0px",
                "border": (
                    "border-width:2px;border-style:solid;border-color:#333333;border-radius:8px"
                ),
            },
            0,
        )
        mjml = serialize_campaign(campaign)
        result = mjml_to_html(mjml)
        self.assertEqual(list(result["errors"]), [])
        self.assertIn('background-color="#ff0000"', mjml)
        self.assertIn('padding="40px 0px"', mjml)
        self.assertIn('border="2px solid #333333"', mjml)
        self.assertIn('border-radius="8px"', mjml)

    def test_voucher_code_block_compiles_with_the_code(self):
        campaign = self._campaign()
        self._add_block(
            campaign,
            "voucher_code",
            {"heading": "For you", "code": "SPRING25", "button_url": "https://x.test"},
            0,
        )
        result = mjml_to_html(serialize_campaign(campaign))
        self.assertEqual(list(result["errors"]), [])
        self.assertIn("SPRING25", result["html"])

    def test_gift_card_promo_block_compiles(self):
        campaign = self._campaign()
        self._add_block(
            campaign,
            "gift_card_promo",
            {"heading": "Gift cards", "button_url": "https://x.test/gift"},
            0,
        )
        result = mjml_to_html(serialize_campaign(campaign))
        self.assertEqual(list(result["errors"]), [])
        self.assertIn("Gift cards", result["html"])

    def test_typography_settings_render_to_mj_text_attributes(self):
        campaign = self._campaign()
        self._add_block(
            campaign,
            "heading",
            {
                "text": "Styled heading",
                "level": "h2",
                "typography": {
                    "fontFamily": "Georgia, serif",
                    "fontSize": "28px",
                    "fontWeight": "700",
                    "textAlign": "center",
                    "color": "#c0392b",
                },
            },
            0,
        )
        mjml = serialize_campaign(campaign)
        result = mjml_to_html(mjml)
        self.assertEqual(list(result["errors"]), [])
        self.assertIn('font-family="Georgia, serif"', mjml)
        self.assertIn('font-size="28px"', mjml)
        self.assertIn('align="center"', mjml)
        self.assertIn('color="#c0392b"', mjml)

    def test_malicious_typography_values_are_stripped(self):
        campaign = self._campaign()
        self._add_block(
            campaign,
            "heading",
            {
                "text": "X",
                "typography": {
                    "fontFamily": "a<script>b",
                    "color": "red;}</style>",
                    "textAlign": "drop-table",
                },
            },
            0,
        )
        mjml = serialize_campaign(campaign)
        self.assertNotIn("<script>", mjml)
        self.assertNotIn("</style>", mjml)
        self.assertEqual(list(mjml_to_html(mjml)["errors"]), [])

    def test_malicious_style_values_are_stripped(self):
        """Crafted CSS-string style values can't reach the MJML attributes."""
        campaign = self._campaign()
        self._add_block(
            campaign,
            "heading",
            {"text": "X", "padding": '16px" onload=alert(1)', "border": "<script>"},
            0,
        )
        mjml = serialize_campaign(campaign)
        self.assertNotIn("onload", mjml)
        self.assertNotIn("<script>", mjml)
        self.assertEqual(list(mjml_to_html(mjml)["errors"]), [])

    def test_featured_product_with_unresolved_id_still_compiles(self):
        # No product -> the template's {% if product %} guard yields no section;
        # the surrounding document must remain valid MJML regardless.
        campaign = self._campaign()
        self._add_block(campaign, "heading", {"text": "Header stays"}, 0)
        self._add_block(campaign, "featured_product", {"product_id": "99999999"}, 1)

        mjml = serialize_campaign(campaign)
        result = mjml_to_html(mjml)
        self.assertEqual(list(result["errors"]), [])
        self.assertIn("Header stays", result["html"])
