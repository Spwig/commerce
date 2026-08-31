"""Behaviour tests for the email-block registry (Phase-1 visual builder + P1 ext).

The registry discovers block definitions from
``email_marketing/templates/email_marketing/blocks/<type>/config.json``. These
tests pin the shipped block set, the palette grouping, and the declared default
content of a freshly dropped block.

The P1 extension adds four blocks — ``divider``/``spacer`` (structure) and
``featured_product``/``product_grid`` (commerce) — taking the registry from four
to eight and introducing the "Structure" and "Commerce" palette groups.
"""

from email_marketing.block_registry import (
    get_block,
    get_palette,
    get_registry,
    sanitize_content,
)

from .base import MarketingTestCase

EXPECTED_BLOCK_TYPES = {
    "heading",
    "text",
    "button",
    "image",
    "divider",
    "spacer",
    "featured_product",
    "product_grid",
    "voucher_code",
    "gift_card_promo",
    "blog_posts",
    "abandoned_cart",
}


class BlockRegistryBehaviourTests(MarketingTestCase):
    def test_registry_exposes_the_shipped_block_types(self):
        registry = get_registry()
        self.assertEqual(set(registry.keys()), EXPECTED_BLOCK_TYPES)
        self.assertEqual(len(registry), 12)

    def test_get_block_returns_config_for_known_type_and_none_for_unknown(self):
        cfg = get_block("heading")
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.block_type, "heading")
        self.assertEqual(cfg.name, "Heading")
        self.assertIsNone(get_block("does-not-exist"))

    def test_palette_groups_blocks_by_category(self):
        palette = get_palette()
        # Palette is a list of {category, label, blocks[]} groups.
        categories = {group["category"] for group in palette}
        # heading/text/button/blog_posts live in "content", image in "media",
        # divider/spacer in "structure", featured_product/product_grid in "commerce".
        self.assertIn("content", categories)
        self.assertIn("media", categories)
        self.assertIn("structure", categories)
        self.assertIn("commerce", categories)

        by_category = {g["category"]: g for g in palette}
        content_types = {b["block_type"] for b in by_category["content"]["blocks"]}
        media_types = {b["block_type"] for b in by_category["media"]["blocks"]}
        self.assertEqual(content_types, {"heading", "text", "button", "blog_posts"})
        self.assertEqual(media_types, {"image"})

        # Every block across every group is one of the eight, and none is dropped.
        all_palette_types = {b["block_type"] for g in palette for b in g["blocks"]}
        self.assertEqual(all_palette_types, EXPECTED_BLOCK_TYPES)

    def test_palette_has_a_structure_group_with_divider_and_spacer(self):
        by_category = {g["category"]: g for g in get_palette()}
        self.assertIn("structure", by_category)
        structure_types = {b["block_type"] for b in by_category["structure"]["blocks"]}
        self.assertEqual(structure_types, {"divider", "spacer"})

    def test_palette_commerce_group_holds_all_commerce_blocks(self):
        by_category = {g["category"]: g for g in get_palette()}
        self.assertIn("commerce", by_category)
        commerce_types = {b["block_type"] for b in by_category["commerce"]["blocks"]}
        self.assertEqual(
            commerce_types,
            {
                "featured_product",
                "product_grid",
                "voucher_code",
                "gift_card_promo",
                "abandoned_cart",
            },
        )

    def test_palette_group_carries_human_label(self):
        by_category = {g["category"]: g for g in get_palette()}
        self.assertEqual(by_category["content"]["label"], "Content")
        self.assertEqual(by_category["media"]["label"], "Media")
        self.assertEqual(by_category["structure"]["label"], "Structure")
        self.assertEqual(by_category["commerce"]["label"], "Commerce")

    def test_commerce_and_structure_categories_precede_by_the_declared_order(self):
        # CATEGORY_ORDER = structure, content, media, commerce — structure first,
        # commerce last. Confirm the palette respects that ordering.
        order = [g["category"] for g in get_palette()]
        self.assertLess(order.index("structure"), order.index("content"))
        self.assertLess(order.index("media"), order.index("commerce"))

    def test_heading_default_content_includes_declared_defaults(self):
        content = get_block("heading").default_content()
        # Block-specific defaults are present (align/colour/size now live in the
        # consolidated Typography control).
        for key, value in {"text": "Your heading", "level": "h2"}.items():
            self.assertEqual(content[key], value)

    def test_text_blocks_expose_a_typography_control(self):
        for block_type in ("heading", "text"):
            props = get_block(block_type).properties
            self.assertIn("typography", props)
            self.assertEqual(props["typography"]["type"], "typography")
            self.assertEqual(props["typography"]["tab"], "style")

    def test_blocks_inherit_base_style_properties(self):
        """Every block (except opt-outs) inherits the universal Style props."""
        heading = get_block("heading").properties
        for key in ("section_bg", "padding", "border"):
            self.assertIn(key, heading)
            self.assertEqual(heading[key]["tab"], "style")
        # Rich Style controls use the shared utility editors.
        self.assertEqual(heading["padding"]["type"], "spacing")
        self.assertEqual(heading["border"]["type"], "border_advanced")
        # Block-specific props default to the Content tab.
        self.assertEqual(heading["text"]["tab"], "content")

    def test_spacer_opts_out_of_base_properties(self):
        spacer = get_block("spacer").properties
        self.assertNotIn("section_bg", spacer)
        self.assertNotIn("padding", spacer)
        # Only its own content property remains.
        self.assertIn("height", spacer)

    def test_palette_item_carries_display_metadata(self):
        heading_item = next(
            b for g in get_palette() for b in g["blocks"] if b["block_type"] == "heading"
        )
        self.assertEqual(heading_item["name"], "Heading")
        self.assertEqual(heading_item["icon"], "fas fa-heading")


class PickerFieldSanitisationTests(MarketingTestCase):
    """The picker property types must validate their stored value server-side."""

    def test_product_field_keeps_only_a_positive_integer_id(self):
        cfg = get_block("featured_product")
        self.assertEqual(cfg.properties["product_id"]["type"], "product")

        self.assertEqual(sanitize_content(cfg, {"product_id": "42"})["product_id"], "42")
        self.assertEqual(sanitize_content(cfg, {"product_id": 42})["product_id"], "42")
        # Junk, zero, negatives, and injection attempts are dropped.
        for bad in ("abc", "12abc", "0", "-5", "<script>", ""):
            self.assertEqual(sanitize_content(cfg, {"product_id": bad})["product_id"], "")

    def test_media_field_enforces_the_safe_url_scheme_allowlist(self):
        cfg = get_block("image")
        self.assertEqual(cfg.properties["src"]["type"], "media")

        self.assertEqual(
            sanitize_content(cfg, {"src": "/media/photo.jpg"})["src"], "/media/photo.jpg"
        )
        self.assertEqual(
            sanitize_content(cfg, {"src": "https://cdn.example.com/a.png"})["src"],
            "https://cdn.example.com/a.png",
        )
        self.assertEqual(sanitize_content(cfg, {"src": "javascript:alert(1)"})["src"], "")

    def test_link_field_enforces_the_safe_url_scheme_allowlist(self):
        cfg = get_block("button")
        self.assertEqual(cfg.properties["href"]["type"], "link")

        self.assertEqual(sanitize_content(cfg, {"href": "/products/x/"})["href"], "/products/x/")
        self.assertEqual(
            sanitize_content(cfg, {"href": "https://example.com"})["href"], "https://example.com"
        )
        self.assertEqual(sanitize_content(cfg, {"href": "javascript:void(0)"})["href"], "")

    def test_voucher_field_keeps_a_bounded_code_string(self):
        cfg = get_block("voucher_code")
        self.assertEqual(cfg.properties["code"]["type"], "voucher")

        self.assertEqual(sanitize_content(cfg, {"code": "  SAVE10 "})["code"], "SAVE10")
        # Bounded to 64 chars (codes are <= 50 in the vouchers model).
        self.assertEqual(len(sanitize_content(cfg, {"code": "X" * 200})["code"]), 64)
