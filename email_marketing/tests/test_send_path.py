"""Behaviours 3 & 4 — send_campaign queueing, skipping, idempotency, footer.

send_campaign resolves the audience, renders the MJML once, then queues one
consent-checked EmailOutbox row + a CampaignSend per recipient. Delivery itself
is the drainer's job (tested separately).

Two collaborators are stubbed so we exercise the queueing/consent/footer logic
rather than external machinery:

* ``_render_mjml`` — the installed ``mjml`` package is broken for the app's call
  site (see test_mjml_render.py), so we patch the compile step to a fixed HTML
  body and separately assert it is invoked exactly once ("render once").
* ``sandbox_filter_recipient`` — pinned to deliver so the outbox lands in
  ``queued`` regardless of licence/sandbox state on the test host.
"""

from unittest import mock

from email_marketing.models import Campaign, CampaignSend
from email_marketing.services.campaigns import send_campaign, send_campaign_to_subscriber

from .base import MarketingTestCase

RENDERED_HTML = "<html><body><p>Hi {{ first_name }}</p></body></html>"


class SendCampaignTests(MarketingTestCase):
    def setUp(self):
        super().setUp()
        # Patch the broken MJML compile and force the sandbox guard to deliver,
        # so the real queue_email path runs and lands rows in "queued".
        render_patch = mock.patch(
            "email_marketing.services.campaigns._render_mjml", return_value=RENDERED_HTML
        )
        self.render_mock = render_patch.start()
        self.addCleanup(render_patch.stop)

        sandbox_patch = mock.patch(
            "core.sandbox.email_guard.sandbox_filter_recipient",
            side_effect=lambda to_email: ("send", to_email),
        )
        sandbox_patch.start()
        self.addCleanup(sandbox_patch.stop)

    def _make_campaign(self, **kwargs):
        defaults = {
            "site": self.site,
            "name": "August Newsletter",
            "subject": "Hello {{ first_name }}",
            "message_type": "newsletter",
            "html_content": (
                "<mjml><mj-body><mj-section><mj-column>"
                "<mj-text>Hi {{ first_name }}</mj-text>"
                "</mj-column></mj-section></mj-body></mjml>"
            ),
            "from_account": self.account,
            "status": Campaign.STATUS_DRAFT,
        }
        defaults.update(kwargs)
        return Campaign.objects.create(**defaults)

    def test_eligible_recipient_gets_queued_campaignsend_with_linked_outbox(self):
        sub = self.make_anon_emailable("lead@example.com")
        campaign = self._make_campaign()

        result = send_campaign(campaign)

        self.assertEqual(result["queued"], 1)
        cs = CampaignSend.objects.get(campaign=campaign, subscriber=sub)
        self.assertEqual(cs.status, CampaignSend.STATUS_QUEUED)
        self.assertIsNotNone(cs.outbox_id)
        self.assertEqual(cs.outbox.status, "queued")

    def test_body_merge_field_resolves_per_recipient(self):
        sub = self.make_anon_emailable("lead@example.com")
        self.render_mock.return_value = "<html><body>Hi [[email]]</body></html>"
        campaign = self._make_campaign()

        send_campaign(campaign)

        cs = CampaignSend.objects.get(campaign=campaign, subscriber=sub)
        self.assertIn("lead@example.com", cs.outbox.html_body)

    def test_subject_merge_resolves_and_is_not_template_evaluated(self):
        """[[ ]] tokens resolve in the subject; {{ }} is NOT executed (no SSTI)."""
        sub = self.make_anon_emailable("lead@example.com")
        campaign = self._make_campaign(subject="To [[email]] {{7|add:1}}")

        send_campaign(campaign)

        subject = CampaignSend.objects.get(campaign=campaign, subscriber=sub).outbox.subject
        self.assertIn("lead@example.com", subject)  # merge field resolved
        self.assertIn("{{7|add:1}}", subject)  # left literal — engine never ran
        self.assertNotIn("To  8", subject)  # would be evaluated to 8 under SSTI

    def test_mjml_is_rendered_only_once_for_the_whole_campaign(self):
        for i in range(3):
            self.make_anon_emailable(f"lead{i}@example.com")
        campaign = self._make_campaign()

        send_campaign(campaign)

        self.assertEqual(self.render_mock.call_count, 1)

    def test_non_emailable_subscriber_is_skipped(self):
        skip = self.make_subscriber("noopt@example.com", marketing_opt_in=False)
        campaign = self._make_campaign()

        result = send_campaign(campaign)

        self.assertEqual(result["queued"], 0)
        self.assertEqual(result["skipped"], 1)
        cs = CampaignSend.objects.get(campaign=campaign, subscriber=skip)
        self.assertEqual(cs.status, CampaignSend.STATUS_SKIPPED)
        self.assertEqual(cs.skip_reason, "not_emailable")
        self.assertIsNone(cs.outbox_id)

    def test_send_is_refused_for_a_campaign_not_in_draft_or_scheduled(self):
        self.make_anon_emailable("a@example.com")
        campaign = self._make_campaign(status=Campaign.STATUS_SENT)

        result = send_campaign(campaign)

        self.assertEqual(result.get("error"), "invalid_status")
        self.assertEqual(CampaignSend.objects.filter(campaign=campaign).count(), 0)

    # --- Behaviour 4: anonymous unsubscribe footer ---------------------------

    def test_anonymous_recipient_outbox_contains_marketing_unsubscribe_link(self):
        sub = self.make_anon_emailable("anon@example.com")
        campaign = self._make_campaign()

        send_campaign(campaign)

        cs = CampaignSend.objects.get(campaign=campaign, subscriber=sub)
        expected = f"/marketing/unsubscribe/{sub.unsubscribe_token}/"
        self.assertIn(expected, cs.outbox.html_body)

    def test_registered_recipient_gets_exactly_one_unsubscribe_footer(self):
        """Registered recipients get their footer from queue_email's per-preference
        footer (/accounts/unsubscribe/). The campaign path must NOT also add its own
        (/marketing/unsubscribe/) footer, or they'd receive two — regression guard."""
        from django.contrib.auth import get_user_model

        from accounts.models import CommunicationPreference

        user = get_user_model().objects.create_user(
            username="member", email="member@example.com", password="x"
        )
        prefs, _ = CommunicationPreference.get_or_create_for_user(user)
        prefs.email_enabled = True
        prefs.email_marketing = True
        prefs.save(update_fields=["email_enabled", "email_marketing"])
        sub = self.make_subscriber("member@example.com", user=user)
        campaign = self._make_campaign()

        send_campaign(campaign)

        cs = CampaignSend.objects.get(campaign=campaign, subscriber=sub)
        self.assertIsNotNone(cs.outbox_id)  # emailable → queued
        html = cs.outbox.html_body
        self.assertIn("/accounts/unsubscribe/", html)  # queue_email's footer present
        self.assertNotIn("/marketing/unsubscribe/", html)  # no second footer in the body

    # --- Deliverability: one-click unsubscribe headers + plain-text part -----

    def test_outbox_carries_one_click_list_unsubscribe_headers(self):
        sub = self.make_anon_emailable("anon@example.com")
        campaign = self._make_campaign()

        send_campaign(campaign)

        headers = CampaignSend.objects.get(campaign=campaign, subscriber=sub).outbox.headers
        self.assertEqual(
            headers["List-Unsubscribe"],
            f"<https://{self.site.domain}/marketing/unsubscribe/{sub.unsubscribe_token}/>",
        )
        self.assertEqual(headers["List-Unsubscribe-Post"], "List-Unsubscribe=One-Click")

    def test_outbox_has_a_plaintext_alternative(self):
        sub = self.make_anon_emailable("anon@example.com")
        self.render_mock.return_value = (
            "<html><head><style>.x{color:red}</style></head>"
            "<body><h1>Sale</h1><p>Big news</p></body></html>"
        )
        campaign = self._make_campaign()

        send_campaign(campaign)

        text = CampaignSend.objects.get(campaign=campaign, subscriber=sub).outbox.text_body
        self.assertTrue(text.strip())
        self.assertIn("Sale", text)
        self.assertIn("Big news", text)
        self.assertNotIn("color:red", text)  # <style> dropped, not leaked into text
        self.assertNotIn("<", text)  # tags stripped

    def test_html_to_text_helper(self):
        from email_marketing.services.campaigns import html_to_text

        html = (
            "<head><style>p{color:red}</style></head>"
            "<body><h1>Hello</h1><p>Line one</p><p>Line two</p></body>"
        )
        text = html_to_text(html)
        self.assertIn("Hello", text)
        self.assertIn("Line one", text)
        self.assertNotIn("color:red", text)
        self.assertNotIn("<", text)
        self.assertEqual(html_to_text(""), "")

    def test_html_to_text_breaks_on_self_closing_br(self):
        from email_marketing.services.campaigns import html_to_text

        # <br/> and <br /> must become a line break, not glue words together.
        for br in ("<br>", "<br/>", "<br />"):
            text = html_to_text(f"<p>Line one{br}Line two</p>")
            self.assertNotIn("Line oneLine two", text)
            self.assertIn("Line one", text)
            self.assertIn("Line two", text)

    # --- Single-subscriber send (triggered journeys) -------------------------

    def test_send_to_subscriber_queues_one_email_without_a_campaignsend(self):
        sub = self.make_anon_emailable("one@example.com")
        campaign = self._make_campaign()

        result = send_campaign_to_subscriber(campaign, sub)

        self.assertTrue(result["queued"])
        # Journeys track delivery per enrollment, not via CampaignSend.
        self.assertEqual(CampaignSend.objects.filter(campaign=campaign).count(), 0)

    def test_send_to_subscriber_respects_consent(self):
        sub = self.make_subscriber("noopt@example.com", marketing_opt_in=False)
        result = send_campaign_to_subscriber(self._make_campaign(), sub)
        self.assertFalse(result["queued"])
        self.assertEqual(result["reason"], "not_emailable")

    def test_same_campaign_can_be_sent_to_a_subscriber_more_than_once(self):
        # No (campaign, subscriber) unique constraint blocks a repeat — an
        # order-triggered series may send the same step email once per order.
        sub = self.make_anon_emailable("repeat@example.com")
        campaign = self._make_campaign()

        self.assertTrue(send_campaign_to_subscriber(campaign, sub)["queued"])
        self.assertTrue(send_campaign_to_subscriber(campaign, sub)["queued"])
