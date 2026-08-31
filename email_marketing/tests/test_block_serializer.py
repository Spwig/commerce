"""Behaviour tests for the block -> MJML serializer (Phase-1 visual builder).

``serialize_campaign`` walks a campaign's ordered ``CampaignBlock`` rows, renders
each block's ``email.mjml`` partial, and wraps them in an ``<mjml>`` document.
``save_campaign_html`` persists that document to ``Campaign.html_content`` so the
existing (P0) send path renders and delivers it unchanged.
"""

from mjml.mjml2html import mjml_to_html

from email_marketing.models import Campaign, CampaignBlock
from email_marketing.services.block_serializer import (
    render_block_canvas,
    render_block_mjml,
    save_campaign_html,
    serialize_campaign,
)

from .base import MarketingTestCase


class BlockSerializerBehaviourTests(MarketingTestCase):
    def _campaign(self, **overrides):
        defaults = {
            "site": self.site,
            "name": "Spring Sale",
            "subject": "Spring is here",
        }
        defaults.update(overrides)
        return Campaign.objects.create(**defaults)

    def _add_block(self, campaign, block_type, content, order):
        return CampaignBlock.objects.create(
            campaign=campaign, block_type=block_type, content=content, order=order
        )

    def test_serialize_campaign_returns_a_valid_mjml_document(self):
        campaign = self._campaign()
        self._add_block(campaign, "heading", {"text": "Welcome aboard", "level": "h1"}, 0)
        self._add_block(campaign, "text", {"text": "Thanks for joining our newsletter."}, 1)
        self._add_block(campaign, "button", {"text": "Start shopping", "href": "https://x.test"}, 2)

        mjml = serialize_campaign(campaign)
        self.assertTrue(mjml.startswith("<mjml>"))
        self.assertTrue(mjml.rstrip().endswith("</mjml>"))

        result = mjml_to_html(mjml)
        # The whole point of MJML is that it compiles cleanly for the inbox.
        self.assertEqual(list(result["errors"]), [])

        html = result["html"]
        self.assertIn("Welcome aboard", html)
        self.assertIn("Thanks for joining our newsletter.", html)
        self.assertIn("Start shopping", html)

    def test_serialize_campaign_respects_block_order(self):
        campaign = self._campaign()
        # Insert out of order; ordering is by CampaignBlock.Meta ("order").
        self._add_block(campaign, "heading", {"text": "SECOND"}, 5)
        self._add_block(campaign, "heading", {"text": "FIRST"}, 1)

        mjml = serialize_campaign(campaign)
        self.assertLess(mjml.index("FIRST"), mjml.index("SECOND"))

    def test_unknown_block_type_is_skipped_not_fatal(self):
        campaign = self._campaign()
        self._add_block(campaign, "heading", {"text": "Real block"}, 0)
        self._add_block(campaign, "totally-bogus", {"text": "ignored"}, 1)

        mjml = serialize_campaign(campaign)
        # render_block_mjml returns "" for unknown types -> document still valid.
        self.assertIn("Real block", mjml)
        self.assertEqual(list(mjml_to_html(mjml)["errors"]), [])

    def test_save_campaign_html_persists_non_empty_mjml(self):
        campaign = self._campaign()
        self._add_block(campaign, "heading", {"text": "Persisted heading"}, 0)

        returned = save_campaign_html(campaign)

        campaign.refresh_from_db()
        self.assertTrue(campaign.html_content)
        self.assertEqual(campaign.html_content, returned)
        self.assertIn("Persisted heading", campaign.html_content)
        self.assertTrue(campaign.html_content.startswith("<mjml>"))

    # --- XSS / escaping -----------------------------------------------------

    def test_heading_script_payload_is_escaped_in_mjml_output(self):
        campaign = self._campaign()
        payload = "<script>alert('xss')</script>"
        block = self._add_block(campaign, "heading", {"text": payload}, 0)

        mjml = render_block_mjml(block)
        # The raw executable tag must never survive into the MJML source.
        self.assertNotIn("<script>", mjml)
        self.assertIn("&lt;script&gt;", mjml)

    def test_heading_script_payload_is_escaped_in_canvas_output(self):
        campaign = self._campaign()
        payload = "<script>alert('xss')</script>"
        block = self._add_block(campaign, "heading", {"text": payload}, 0)

        canvas = render_block_canvas(block)
        self.assertNotIn("<script>", canvas)
        self.assertIn("&lt;script&gt;", canvas)

    def test_full_document_with_script_payload_stays_escaped(self):
        campaign = self._campaign()
        payload = "<script>alert(1)</script>"
        self._add_block(campaign, "heading", {"text": payload}, 0)

        mjml = serialize_campaign(campaign)
        self.assertNotIn("<script>", mjml)
        # And it still compiles.
        self.assertEqual(list(mjml_to_html(mjml)["errors"]), [])
