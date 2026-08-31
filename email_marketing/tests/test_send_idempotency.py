"""Behaviour 3 (idempotency) — a re-run creates no duplicate CampaignSend.

send_campaign's claim-first idempotency does
``CampaignSend.objects.create(...)`` and catches ``IntegrityError`` to skip a
subscriber that already has a send (the ``unique_together`` on
``(campaign, subscriber)`` is the serialisation point). In PostgreSQL a caught
IntegrityError aborts the surrounding transaction, so this must be exercised in
autocommit — a plain TestCase's wrapping transaction would be left broken and
every subsequent query in the test would raise TransactionManagementError.
Hence TransactionTestCase, which also mirrors how the task actually runs.

NOTE (robustness): because the ``create`` is not wrapped in its own
``transaction.atomic()`` savepoint, this idempotency guarantee holds ONLY while
send_campaign runs in autocommit. If it is ever called inside an outer atomic
block, the first duplicate would poison that transaction. See report.
"""

from unittest import mock

from email_marketing.models import Campaign, CampaignSend
from email_marketing.services.campaigns import send_campaign

from .base import MarketingTransactionTestCase

RENDERED_HTML = "<html><body><p>Hi {{ first_name }}</p></body></html>"


class SendCampaignIdempotencyTests(MarketingTransactionTestCase):
    def setUp(self):
        super().setUp()
        render_patch = mock.patch(
            "email_marketing.services.campaigns._render_mjml", return_value=RENDERED_HTML
        )
        render_patch.start()
        self.addCleanup(render_patch.stop)

        sandbox_patch = mock.patch(
            "core.sandbox.email_guard.sandbox_filter_recipient",
            side_effect=lambda to_email: ("send", to_email),
        )
        sandbox_patch.start()
        self.addCleanup(sandbox_patch.stop)

    def _make_campaign(self):
        return Campaign.objects.create(
            site=self.site,
            name="August Newsletter",
            subject="Hello {{ first_name }}",
            message_type="newsletter",
            html_content="<mjml></mjml>",
            from_account=self.account,
            status=Campaign.STATUS_DRAFT,
        )

    def test_rerun_is_idempotent_and_creates_no_duplicate_sends(self):
        self.make_anon_emailable("a@example.com")
        self.make_anon_emailable("b@example.com")
        campaign = self._make_campaign()

        send_campaign(campaign)
        self.assertEqual(CampaignSend.objects.filter(campaign=campaign).count(), 2)

        # A straight re-run is refused (status is now SENDING); reset to DRAFT to
        # drive the per-subscriber claim-first idempotency path directly.
        Campaign.objects.filter(pk=campaign.pk).update(status=Campaign.STATUS_DRAFT)
        campaign.refresh_from_db()
        send_campaign(campaign)

        # No duplicates despite the unique_together collision being hit + caught.
        self.assertEqual(CampaignSend.objects.filter(campaign=campaign).count(), 2)
