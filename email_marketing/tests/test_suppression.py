"""List hygiene — the do-not-mail list, the send-gate, and bounce/complaint rollup.

A hard bounce, a spam complaint, or a manual block suppresses an email ADDRESS;
the send path never queues to a suppressed address; and a recorded
``EmailEvent(bounced/complained)`` — including one from a synchronous SMTP
recipient-refusal — feeds the suppression list.
"""

from unittest import mock

from email_marketing.models import Campaign, CampaignSend, Subscriber, SuppressionEntry
from email_marketing.services import suppression
from email_marketing.services.campaigns import send_campaign, send_campaign_to_subscriber
from email_system.models import EmailEvent, EmailOutbox
from email_system.providers.base import EmailRecipientsRefused, recipients_refused
from email_system.services.email_sender import EmailSendingService

from .base import MarketingTestCase


class SuppressionServiceTests(MarketingTestCase):
    def test_suppress_creates_entry_and_is_idempotent(self):
        suppression.suppress(self.site, "dead@example.com", SuppressionEntry.REASON_HARD_BOUNCE)
        suppression.suppress(self.site, "dead@example.com", SuppressionEntry.REASON_HARD_BOUNCE)
        self.assertEqual(SuppressionEntry.objects.filter(site=self.site).count(), 1)
        self.assertTrue(suppression.is_suppressed(self.site, "dead@example.com"))

    def test_suppress_normalises_email_case(self):
        suppression.suppress(self.site, "Dead@Example.COM", SuppressionEntry.REASON_MANUAL)
        self.assertTrue(suppression.is_suppressed(self.site, "dead@example.com"))
        self.assertIn("dead@example.com", suppression.suppressed_emails(self.site))

    def test_release_unblocks_and_resuppress_restores(self):
        suppression.suppress(self.site, "x@example.com", SuppressionEntry.REASON_HARD_BOUNCE)
        suppression.release(self.site, "x@example.com")
        self.assertFalse(suppression.is_suppressed(self.site, "x@example.com"))
        # Re-suppressing restores the (soft-deleted) row rather than colliding.
        suppression.suppress(self.site, "x@example.com", SuppressionEntry.REASON_COMPLAINT)
        self.assertTrue(suppression.is_suppressed(self.site, "x@example.com"))
        self.assertEqual(SuppressionEntry.all_objects.filter(site=self.site).count(), 1)

    def test_hard_bounce_flips_subscriber_to_bounced(self):
        sub = self.make_anon_emailable("bounce@example.com")
        suppression.suppress(self.site, "bounce@example.com", SuppressionEntry.REASON_HARD_BOUNCE)
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_BOUNCED)

    def test_complaint_flips_to_complained_and_opts_out(self):
        sub = self.make_anon_emailable("spam@example.com")
        suppression.suppress(self.site, "spam@example.com", SuppressionEntry.REASON_COMPLAINT)
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_COMPLAINED)
        self.assertFalse(sub.marketing_opt_in)

    def test_manual_block_keeps_subscriber_active_but_suppressed(self):
        sub = self.make_anon_emailable("blocked@example.com")
        suppression.suppress(self.site, "blocked@example.com", SuppressionEntry.REASON_MANUAL)
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_ACTIVE)  # not relabelled
        self.assertTrue(suppression.is_suppressed(self.site, "blocked@example.com"))


class SuppressionSendGateTests(MarketingTestCase):
    def setUp(self):
        super().setUp()
        render_patch = mock.patch(
            "email_marketing.services.campaigns._render_mjml",
            return_value="<html><body>Hi</body></html>",
        )
        render_patch.start()
        self.addCleanup(render_patch.stop)
        sandbox_patch = mock.patch(
            "core.sandbox.email_guard.sandbox_filter_recipient",
            side_effect=lambda to_email: ("send", to_email),
        )
        sandbox_patch.start()
        self.addCleanup(sandbox_patch.stop)

    def _campaign(self, **kw):
        defaults = {
            "site": self.site,
            "name": "N",
            "subject": "Hi",
            "message_type": "newsletter",
            "html_content": "<mjml><mj-body></mj-body></mjml>",
            "from_account": self.account,
            "status": Campaign.STATUS_DRAFT,
        }
        defaults.update(kw)
        return Campaign.objects.create(**defaults)

    def test_broadcast_skips_a_suppressed_address(self):
        # A manual block leaves the subscriber ACTIVE, so it survives the audience
        # status filter and reaches the loop — exactly the email-keyed case the
        # send-gate exists for (a bounced subscriber is already excluded by status).
        sub = self.make_anon_emailable("dead@example.com")
        suppression.suppress(self.site, "dead@example.com", SuppressionEntry.REASON_MANUAL)

        result = send_campaign(self._campaign())

        self.assertEqual(result["queued"], 0)
        self.assertEqual(result["skipped"], 1)
        cs = CampaignSend.objects.get(subscriber=sub)
        self.assertEqual(cs.status, CampaignSend.STATUS_SKIPPED)
        self.assertEqual(cs.skip_reason, "suppressed")
        self.assertIsNone(cs.outbox_id)

    def test_broadcast_still_sends_a_clean_address(self):
        self.make_anon_emailable("ok@example.com")
        result = send_campaign(self._campaign())
        self.assertEqual(result["queued"], 1)

    def test_journey_single_send_refuses_a_suppressed_address(self):
        sub = self.make_anon_emailable("dead@example.com")
        suppression.suppress(self.site, "dead@example.com", SuppressionEntry.REASON_COMPLAINT)
        result = send_campaign_to_subscriber(self._campaign(), sub)
        self.assertFalse(result["queued"])
        self.assertEqual(result["reason"], "suppressed")

    def test_broadcast_gate_normalises_whitespace_email(self):
        # A stored email carrying whitespace must still be caught by the gate
        # (both sides normalise strip+lower), never slipping through to a send.
        self.make_subscriber("  ws@example.com  ", marketing_opt_in=True, marketing_verified=True)
        suppression.suppress(self.site, "ws@example.com", SuppressionEntry.REASON_MANUAL)

        result = send_campaign(self._campaign())

        self.assertEqual(result["skipped"], 1)
        self.assertEqual(CampaignSend.objects.get().skip_reason, "suppressed")


class SuppressionReceiverTests(MarketingTestCase):
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

    def test_hard_bounce_event_suppresses_the_address(self):
        sub = self.make_anon_emailable("hard@example.com")
        outbox = self._outbox("hard@example.com")

        EmailEvent.objects.create(email=outbox, event_type="bounced", bounce_type="hard")

        self.assertTrue(suppression.is_suppressed(self.site, "hard@example.com"))
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_BOUNCED)

    def test_complaint_event_suppresses_and_flips_status(self):
        sub = self.make_anon_emailable("fbl@example.com")
        outbox = self._outbox("fbl@example.com")

        EmailEvent.objects.create(email=outbox, event_type="complained")

        self.assertTrue(suppression.is_suppressed(self.site, "fbl@example.com"))
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_COMPLAINED)

    def test_soft_bounce_event_does_not_suppress_in_stage1(self):
        self.make_anon_emailable("soft@example.com")
        outbox = self._outbox("soft@example.com")

        EmailEvent.objects.create(email=outbox, event_type="bounced", bounce_type="soft")

        self.assertFalse(suppression.is_suppressed(self.site, "soft@example.com"))


class SmtpRejectTests(MarketingTestCase):
    def test_recipients_refused_classifies_hard_and_soft(self):
        import smtplib

        hard = smtplib.SMTPRecipientsRefused({"x@e.com": (550, b"No such user")})
        soft = smtplib.SMTPRecipientsRefused({"x@e.com": (450, b"Mailbox busy")})
        self.assertEqual(recipients_refused(hard).bounce_type, "hard")
        self.assertEqual(recipients_refused(soft).bounce_type, "soft")

    def test_send_email_records_a_bounce_on_recipient_refusal(self):
        sub = self.make_anon_emailable("refused@example.com")
        outbox = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            from_email="store@example.com",
            to_email="refused@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="queued",
        )
        provider = mock.Mock()
        provider.send.side_effect = EmailRecipientsRefused(
            "refused",
            recipients={"refused@example.com": (550, b"No such user")},
            bounce_type="hard",
        )
        with mock.patch.object(type(self.account), "get_provider_instance", return_value=provider):
            ok = EmailSendingService.send_email(str(outbox.id))

        self.assertFalse(ok)
        outbox.refresh_from_db()
        self.assertEqual(outbox.status, "bounced")
        self.assertTrue(EmailEvent.objects.filter(email=outbox, event_type="bounced").exists())
        # …and the recorded bounce fed the suppression list + subscriber.
        self.assertTrue(suppression.is_suppressed(self.site, "refused@example.com"))
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_BOUNCED)

    def test_soft_recipient_refusal_retries_and_does_not_suppress(self):
        # A 4xx (greylisting) deferral must stay retryable — not a permanent bounce.
        outbox = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            from_email="store@example.com",
            to_email="greylisted@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="queued",
        )
        provider = mock.Mock()
        provider.send.side_effect = EmailRecipientsRefused(
            "deferred",
            recipients={"greylisted@example.com": (451, b"Try again later")},
            bounce_type="soft",
        )
        with mock.patch.object(type(self.account), "get_provider_instance", return_value=provider):
            EmailSendingService.send_email(str(outbox.id))

        outbox.refresh_from_db()
        self.assertEqual(outbox.status, "failed")  # retryable, not a permanent bounce
        self.assertEqual(outbox.retry_count, 1)
        self.assertFalse(suppression.is_suppressed(self.site, "greylisted@example.com"))

    def test_send_email_classifies_on_this_outboxs_recipient_not_the_aggregate(self):
        # A multi-recipient message where THIS outbox's address got a soft 4xx but a
        # co-recipient got a hard 5xx must be treated soft for this address (retry,
        # not a permanent bounce + suppression).
        outbox = EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            from_email="store@example.com",
            to_email="deferred@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="queued",
        )
        provider = mock.Mock()
        provider.send.side_effect = EmailRecipientsRefused(
            "mixed",
            recipients={
                "deferred@example.com": (450, b"later"),
                "dead@other.com": (550, b"no user"),
            },
            bounce_type="hard",  # aggregate says hard; this address is a soft 450
        )
        with mock.patch.object(type(self.account), "get_provider_instance", return_value=provider):
            EmailSendingService.send_email(str(outbox.id))

        outbox.refresh_from_db()
        self.assertEqual(outbox.status, "failed")  # soft for THIS address → retry
        self.assertEqual(outbox.retry_count, 1)
        self.assertFalse(suppression.is_suppressed(self.site, "deferred@example.com"))


class SuppressionAdminTests(MarketingTestCase):
    def test_readding_a_released_address_restores_and_does_not_500(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse

        suppression.suppress(self.site, "back@example.com", SuppressionEntry.REASON_HARD_BOUNCE)
        suppression.release(self.site, "back@example.com")  # soft-deleted row remains

        admin = get_user_model().objects.create_superuser("s_admin", "s_admin@e.com", "pw")
        self.client.force_login(admin)
        resp = self.client.post(
            reverse("admin:email_marketing_suppressionentry_add"),
            {
                "email": "back@example.com",
                "reason": SuppressionEntry.REASON_MANUAL,
                "source": SuppressionEntry.SOURCE_MANUAL,
                "detail": "",
            },
        )

        self.assertEqual(resp.status_code, 302)  # restored, not a unique-constraint 500
        self.assertTrue(suppression.is_suppressed(self.site, "back@example.com"))
        self.assertEqual(
            SuppressionEntry.all_objects.filter(site=self.site, email="back@example.com").count(), 1
        )

    def test_admin_add_with_a_bounce_reason_reflects_on_the_subscriber(self):
        # A hand-added complaint/bounce must flip the matching Subscriber, same as an
        # ingested one — i.e. the admin routes through the suppression service.
        from django.contrib.auth import get_user_model
        from django.urls import reverse

        sub = self.make_anon_emailable("adminfbl@example.com")
        admin = get_user_model().objects.create_superuser("s_admin3", "s_admin3@e.com", "pw")
        self.client.force_login(admin)
        resp = self.client.post(
            reverse("admin:email_marketing_suppressionentry_add"),
            {
                "email": "adminfbl@example.com",
                "reason": SuppressionEntry.REASON_COMPLAINT,
                "source": SuppressionEntry.SOURCE_MANUAL,
                "detail": "",
            },
        )

        self.assertEqual(resp.status_code, 302)
        self.assertTrue(suppression.is_suppressed(self.site, "adminfbl@example.com"))
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_COMPLAINED)
