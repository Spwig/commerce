"""Behaviour 5 — drain_campaign_outbox is a throttled batch worker.

The drainer claims up to ``CAMPAIGN_SEND_RATE_PER_MINUTE`` queued CampaignSend
rows per tick, delivers each via EmailSendingService.send_email (mocked here so
no real mail is sent), transitions each row to sent/failed, and finalises a
campaign to "sent" once no queued/sending work remains.
"""

from unittest import mock

from django.test import override_settings

from email_marketing.models import Campaign, CampaignSend
from email_marketing.services.campaigns import send_campaign
from email_marketing.tasks import drain_campaign_outbox

from .base import MarketingTestCase

RENDERED_HTML = "<html><body><p>Hi</p></body></html>"


class DrainCampaignOutboxTests(MarketingTestCase):
    def setUp(self):
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

    def _queue_campaign(self, n_recipients):
        for i in range(n_recipients):
            self.make_anon_emailable(f"lead{i}@example.com")
        campaign = Campaign.objects.create(
            site=self.site,
            name="Blast",
            subject="Hi",
            message_type="newsletter",
            html_content="<mjml></mjml>",
            from_account=self.account,
            status=Campaign.STATUS_DRAFT,
        )
        result = send_campaign(campaign)
        self.assertEqual(result["queued"], n_recipients)
        campaign.refresh_from_db()
        return campaign

    @override_settings(CAMPAIGN_SEND_RATE_PER_MINUTE=2)
    def test_only_the_rate_cap_is_sent_per_tick(self):
        campaign = self._queue_campaign(3)

        with mock.patch(
            "email_system.services.email_sender.EmailSendingService.send_email",
            return_value=True,
        ) as send_mock:
            summary = drain_campaign_outbox()

        self.assertEqual(summary, {"sent": 2, "failed": 0, "deferred": 0})
        self.assertEqual(send_mock.call_count, 2)
        self.assertEqual(CampaignSend.objects.filter(status=CampaignSend.STATUS_SENT).count(), 2)
        self.assertEqual(CampaignSend.objects.filter(status=CampaignSend.STATUS_QUEUED).count(), 1)
        # Work still outstanding → campaign stays in "sending".
        campaign.refresh_from_db()
        self.assertEqual(campaign.status, Campaign.STATUS_SENDING)

    @override_settings(CAMPAIGN_SEND_RATE_PER_MINUTE=2)
    def test_campaign_finalises_to_sent_once_no_work_remains(self):
        campaign = self._queue_campaign(3)

        with mock.patch(
            "email_system.services.email_sender.EmailSendingService.send_email",
            return_value=True,
        ):
            drain_campaign_outbox()  # sends 2
            drain_campaign_outbox()  # sends the last 1

        campaign.refresh_from_db()
        self.assertEqual(campaign.status, Campaign.STATUS_SENT)
        self.assertIsNotNone(campaign.sent_at)
        self.assertEqual(campaign.sent_count, 3)
        self.assertEqual(campaign.failed_count, 0)

    @override_settings(CAMPAIGN_SEND_RATE_PER_MINUTE=10)
    def test_failed_delivery_marks_send_failed_and_rolls_up_failed_count(self):
        campaign = self._queue_campaign(2)

        # A real hard failure: send_email marks the outbox "failed" and returns False
        # (a bare False that left the outbox queued would be a budget DEFER, not a
        # failure — the drainer distinguishes the two by the outbox status).
        def _hard_fail(outbox_id):
            from email_system.models import EmailOutbox

            EmailOutbox.objects.filter(id=outbox_id).update(status="failed")
            return False

        with mock.patch(
            "email_system.services.email_sender.EmailSendingService.send_email",
            side_effect=_hard_fail,
        ):
            summary = drain_campaign_outbox()

        self.assertEqual(summary, {"sent": 0, "failed": 2, "deferred": 0})
        self.assertEqual(CampaignSend.objects.filter(status=CampaignSend.STATUS_FAILED).count(), 2)
        campaign.refresh_from_db()
        # No queued/sending work left, so the campaign still finalises.
        self.assertEqual(campaign.status, Campaign.STATUS_SENT)
        self.assertEqual(campaign.failed_count, 2)
        self.assertEqual(campaign.sent_count, 0)

    @override_settings(CAMPAIGN_SEND_RATE_PER_MINUTE=10)
    def test_provider_exception_is_recorded_as_failed_not_raised(self):
        self._queue_campaign(1)

        # An unexpected exception (send_email raises rather than returning False) is a
        # real failure, not a budget defer — the drainer records it failed and doesn't
        # propagate, so retry_failed_emails re-sends it with backoff.
        with mock.patch(
            "email_system.services.email_sender.EmailSendingService.send_email",
            side_effect=RuntimeError("smtp down"),
        ):
            summary = drain_campaign_outbox()

        self.assertEqual(summary, {"sent": 0, "failed": 1, "deferred": 0})
        self.assertEqual(CampaignSend.objects.filter(status=CampaignSend.STATUS_FAILED).count(), 1)

    def test_drainer_is_a_noop_when_nothing_is_queued(self):
        summary = drain_campaign_outbox()
        self.assertEqual(summary, {"sent": 0, "failed": 0})
