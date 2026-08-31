"""Campaign engagement tracking — pixel injection + EmailEvent → CampaignSend rollup.

This is the measurement foundation A/B testing (and the dashboard's open/click
rates) depend on: campaign emails carry tracking, and email_system open/click
events reflect onto the campaign's CampaignSend.
"""

from django.utils import timezone

from email_marketing.models import Campaign, CampaignSend
from email_marketing.services.campaigns import _add_open_click_tracking

from .base import MarketingTestCase


class _TrackingBase(MarketingTestCase):
    def _outbox(self, **kw):
        from email_system.models import EmailOutbox

        defaults = {
            "site": self.site,
            "from_email": "store@example.com",
            "to_email": "person@example.com",
            "subject": "Hello",
            "html_body": "<html><body>Hello there</body></html>",
            "status": "queued",
            "template_type": "newsletter",
        }
        defaults.update(kw)
        return EmailOutbox.objects.create(**defaults)

    def _campaign_send(self, outbox, email="person@example.com"):
        campaign = Campaign.objects.create(site=self.site, name="C", subject="s")
        sub = self.make_anon_emailable(email)
        return CampaignSend.objects.create(
            campaign=campaign, subscriber=sub, outbox=outbox, status="sent"
        )

    def _event(self, outbox, event_type):
        from email_system.models import EmailEvent

        return EmailEvent.objects.create(
            email=outbox, event_type=event_type, occurred_at=timezone.now()
        )


class PixelInjectionTests(_TrackingBase):
    def test_tracking_is_injected_into_a_queued_campaign_outbox(self):
        outbox = self._outbox()
        _add_open_click_tracking(outbox)
        outbox.refresh_from_db()
        self.assertIn("track/open", outbox.html_body)

    def test_non_queued_outbox_is_left_untouched(self):
        outbox = self._outbox(status="skipped", html_body="<html><body>x</body></html>")
        original = outbox.html_body
        _add_open_click_tracking(outbox)
        outbox.refresh_from_db()
        self.assertEqual(outbox.html_body, original)


class EngagementRollupTests(_TrackingBase):
    def test_open_event_flips_campaign_send_and_subscriber(self):
        outbox = self._outbox(status="sent")
        cs = self._campaign_send(outbox)
        self._event(outbox, "opened")

        cs.refresh_from_db()
        self.assertTrue(cs.opened)
        self.assertIsNotNone(cs.opened_at)
        self.assertFalse(cs.clicked)
        cs.subscriber.refresh_from_db()
        self.assertIsNotNone(cs.subscriber.last_opened_at)

    def test_click_event_sets_clicked_and_implies_open(self):
        outbox = self._outbox(status="sent")
        cs = self._campaign_send(outbox)
        self._event(outbox, "clicked")

        cs.refresh_from_db()
        self.assertTrue(cs.clicked)
        self.assertTrue(cs.opened)  # a click implies an open

    def test_repeat_opens_do_not_move_the_first_timestamp(self):
        outbox = self._outbox(status="sent")
        cs = self._campaign_send(outbox)
        self._event(outbox, "opened")
        cs.refresh_from_db()
        first = cs.opened_at
        self._event(outbox, "opened")
        cs.refresh_from_db()
        self.assertEqual(cs.opened_at, first)  # idempotent — first-open wins

    def test_event_without_a_campaign_send_is_ignored(self):
        outbox = self._outbox(status="sent")  # no CampaignSend links to it
        # Must not raise.
        self._event(outbox, "opened")

    def test_delivered_event_does_not_mark_opened(self):
        outbox = self._outbox(status="sent")
        cs = self._campaign_send(outbox)
        self._event(outbox, "delivered")
        cs.refresh_from_db()
        self.assertFalse(cs.opened)

    def test_full_pixel_round_trip_flips_campaign_send(self):
        # Guards the whole contract the metric depends on: hitting the real
        # tracking-pixel URL resolves the outbox, records an EmailEvent, and the
        # receiver flips the CampaignSend. A tracking-id format drift breaks this.
        from django.urls import reverse

        outbox = self._outbox(status="sent")
        cs = self._campaign_send(outbox)
        tracking_id = f"{outbox.id}-{'a' * 16}"  # {outbox_uuid}-{16 chars}
        resp = self.client.get(reverse("email_tracking:track_open", args=[tracking_id]))
        self.assertEqual(resp.status_code, 200)
        cs.refresh_from_db()
        self.assertTrue(cs.opened)
