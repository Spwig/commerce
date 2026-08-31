"""Soft-bounce threshold → suppression (Stage 3b).

A single soft bounce is transient and ignored, but once an address accumulates
``EMAIL_SOFT_BOUNCE_THRESHOLD`` recent soft bounces the delivery receiver treats
it as undeliverable and suppresses it. Each soft-bounce ``EmailEvent`` save runs
the receiver, so these tests drive the real signal path.
"""

from django.test import override_settings

from email_marketing.models import Subscriber, SuppressionEntry
from email_marketing.services import suppression
from email_system.models import EmailEvent, EmailOutbox

from .base import MarketingTestCase


class SoftBounceThresholdTests(MarketingTestCase):
    def _outbox(self, to_email):
        return EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            from_email="store@example.com",
            to_email=to_email,
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="sent",
        )

    def _soft_bounce(self, outbox, i):
        # Each save fires _delivery_event_receiver.
        return EmailEvent.objects.create(
            email=outbox,
            event_type="bounced",
            bounce_type="soft",
            event_data={"source": "gateway_poll", "event_id": f"s{i}"},
        )

    @override_settings(EMAIL_SOFT_BOUNCE_THRESHOLD=5)
    def test_repeated_soft_bounces_cross_threshold_and_suppress(self):
        self.make_anon_emailable("flaky@example.com")
        outbox = self._outbox("flaky@example.com")
        for i in range(4):
            self._soft_bounce(outbox, i)
        # Four soft bounces: below threshold, still deliverable.
        self.assertFalse(suppression.is_suppressed(self.site, "flaky@example.com"))
        # The fifth crosses it.
        self._soft_bounce(outbox, 4)
        self.assertTrue(suppression.is_suppressed(self.site, "flaky@example.com"))
        entry = SuppressionEntry.objects.get(site=self.site, email="flaky@example.com")
        self.assertEqual(entry.reason, SuppressionEntry.REASON_SOFT_BOUNCE)

    @override_settings(EMAIL_SOFT_BOUNCE_THRESHOLD=5)
    def test_a_few_soft_bounces_do_not_suppress(self):
        self.make_anon_emailable("occasional@example.com")
        outbox = self._outbox("occasional@example.com")
        for i in range(3):
            self._soft_bounce(outbox, i)
        self.assertFalse(suppression.is_suppressed(self.site, "occasional@example.com"))

    @override_settings(EMAIL_SOFT_BOUNCE_THRESHOLD=2)
    def test_a_hard_bounce_still_suppresses_immediately(self):
        # The threshold path must not regress the immediate hard-bounce path.
        sub = self.make_anon_emailable("dead@example.com")
        outbox = self._outbox("dead@example.com")
        EmailEvent.objects.create(email=outbox, event_type="bounced", bounce_type="hard")
        self.assertTrue(suppression.is_suppressed(self.site, "dead@example.com"))
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_BOUNCED)
