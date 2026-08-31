"""Marketing priority stamping + budget-aware campaign draining (Stage 2/3)."""

from datetime import timedelta
from unittest import mock

from django.test import override_settings
from django.utils import timezone

from email_marketing.models import Campaign, CampaignSend
from email_marketing.services.campaigns import send_campaign_to_subscriber
from email_marketing.tasks import drain_campaign_outbox
from email_system.models import EmailAccount, EmailOutbox
from email_system.services import send_budget

from .base import MarketingTestCase

_MJML = "<mjml><mj-body><mj-section><mj-column><mj-text>Hi</mj-text></mj-column></mj-section></mj-body></mjml>"


class MarketingPriorityTests(MarketingTestCase):
    def test_campaign_send_is_stamped_marketing_priority(self):
        campaign = Campaign.objects.create(
            site=self.site, name="C", subject="s", message_type="newsletter", html_content=_MJML
        )
        sub = self.make_anon_emailable("m@example.com")
        result = send_campaign_to_subscriber(campaign, sub)
        self.assertTrue(result.get("queued"), result)
        outbox = EmailOutbox.objects.get(id=result["outbox_id"])
        self.assertEqual(outbox.priority, EmailOutbox.PRIORITY_MARKETING)


class DrainerBudgetTests(MarketingTestCase):
    @override_settings(
        EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE=1, EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE=1
    )
    def test_drainer_defers_marketing_under_budget_without_failing(self):
        # marketing cap = 0 → the campaign send is deferred (back to queued), NOT failed,
        # so it retries next tick when transactional load eases.
        try:
            send_budget._redis().delete(send_budget._key(self.account.id))
        except Exception:
            self.skipTest("Redis not available")

        campaign = Campaign.objects.create(site=self.site, name="C", subject="s")
        sub = self.make_anon_emailable("c@example.com")
        outbox = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="c@example.com",
            from_email="store@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="queued",
            priority=EmailOutbox.PRIORITY_MARKETING,
        )
        cs = CampaignSend.objects.create(
            campaign=campaign, subscriber=sub, outbox=outbox, status="queued"
        )
        res = drain_campaign_outbox()
        self.assertEqual(res.get("deferred"), 1)
        self.assertEqual(res.get("sent", 0), 0)
        self.assertEqual(res.get("failed", 0), 0)
        cs.refresh_from_db()
        outbox.refresh_from_db()
        self.assertEqual(cs.status, "queued")
        self.assertEqual(outbox.status, "queued")


class StuckSendReaperTests(MarketingTestCase):
    @override_settings(EMAIL_CAMPAIGN_STUCK_SECONDS=600)
    def test_drainer_reclaims_and_recovers_a_stuck_sending_send(self):
        # A worker died mid-batch, stranding a CampaignSend (+ its outbox) in "sending".
        # The drainer reaps it back to queued and delivers it.
        campaign = Campaign.objects.create(site=self.site, name="C", subject="s")
        sub = self.make_anon_emailable("stuck@example.com")
        outbox = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="stuck@example.com",
            from_email="store@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="sending",
        )
        cs = CampaignSend.objects.create(
            campaign=campaign, subscriber=sub, outbox=outbox, status="sending"
        )
        old = timezone.now() - timedelta(seconds=700)
        EmailOutbox.objects.filter(id=outbox.id).update(updated_at=old)
        CampaignSend.objects.filter(id=cs.id).update(updated_at=old)

        provider = mock.Mock()
        provider.send.return_value = {
            "provider_message_id": "x",
            "accepted": True,
            "status": "sent",
            "error": None,
            "details": {},
        }
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            drain_campaign_outbox()
        cs.refresh_from_db()
        self.assertEqual(cs.status, "sent")  # reclaimed from stuck-sending and delivered

    @override_settings(EMAIL_CAMPAIGN_STUCK_SECONDS=600)
    def test_reaper_marks_sent_when_the_outbox_already_sent(self):
        # Worker died AFTER the SMTP send but before its bookkeeping: outbox "sent",
        # CampaignSend stuck "sending". The reaper must mark it SENT (no re-send, no
        # orphan), not requeue it.
        campaign = Campaign.objects.create(site=self.site, name="C", subject="s")
        sub = self.make_anon_emailable("done@example.com")
        outbox = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email="done@example.com",
            from_email="store@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="sent",
        )
        cs = CampaignSend.objects.create(
            campaign=campaign, subscriber=sub, outbox=outbox, status="sending"
        )
        CampaignSend.objects.filter(id=cs.id).update(
            updated_at=timezone.now() - timedelta(seconds=700)
        )
        drain_campaign_outbox()  # no provider needed — reaper just marks it sent
        cs.refresh_from_db()
        outbox.refresh_from_db()
        self.assertEqual(cs.status, "sent")
        self.assertEqual(outbox.status, "sent")
