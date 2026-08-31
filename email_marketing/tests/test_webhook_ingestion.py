"""Provider delivery-event webhook → EmailEvent → list-hygiene (Stage 2).

An installed API provider posts bounce/complaint events to
``/webhooks/email/<slug>/``. The handler verifies the provider signature, is
idempotent, only acts on addresses we actually sent to, and records ``EmailEvent``
rows; the Stage-1 receiver then suppresses. The two built-in providers are SMTP
(no webhooks), so these tests drive a fake webhook-capable provider.
"""

import json
from unittest import mock

from django.urls import reverse

from email_marketing.models import Subscriber
from email_marketing.services import suppression
from email_system.models import EmailAccount, EmailEvent, EmailOutbox, EmailProviderWebhook

from .base import MarketingTestCase


class _FakeProvider:
    """A provider that accepts the signature and returns canned delivery events."""

    def __init__(self, events, verify=True):
        self._events = events
        self._verify = verify

    def verify_webhook_signature(self, raw, signature, headers):
        return self._verify

    def parse_delivery_events(self, payload):
        return self._events


class WebhookIngestionTests(MarketingTestCase):
    def _url(self, slug="builtin_smtp"):
        return reverse("email_webhook", args=[slug])

    def _sent_outbox(self, to_email):
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

    def _post(self, events, verify=True, body=None, slug="builtin_smtp"):
        provider = _FakeProvider(events, verify=verify)
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            return self.client.post(
                self._url(slug),
                data=json.dumps(body if body is not None else {"id": "evt-1"}),
                content_type="application/json",
                HTTP_X_SIGNATURE="sig",
            )

    def test_verified_hard_bounce_records_event_and_suppresses(self):
        sub = self.make_anon_emailable("dead@example.com")
        outbox = self._sent_outbox("dead@example.com")
        events = [
            {
                "event_id": "e1",
                "event_type": "bounced",
                "bounce_type": "hard",
                "reason": "user unknown",
                "email": "dead@example.com",
            }
        ]
        resp = self._post(events)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(EmailEvent.objects.filter(email=outbox, event_type="bounced").exists())
        self.assertTrue(suppression.is_suppressed(self.site, "dead@example.com"))
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_BOUNCED)

    def test_complaint_suppresses_and_flips_status(self):
        sub = self.make_anon_emailable("fbl@example.com")
        self._sent_outbox("fbl@example.com")
        events = [{"event_id": "e2", "event_type": "complained", "email": "fbl@example.com"}]
        resp = self._post(events, body={"id": "evt-2"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(suppression.is_suppressed(self.site, "fbl@example.com"))
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_COMPLAINED)

    def test_unverified_signature_is_rejected_and_no_effect(self):
        self.make_anon_emailable("x@example.com")
        self._sent_outbox("x@example.com")
        events = [
            {
                "event_id": "e3",
                "event_type": "bounced",
                "bounce_type": "hard",
                "email": "x@example.com",
            }
        ]
        resp = self._post(events, verify=False)
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(suppression.is_suppressed(self.site, "x@example.com"))
        self.assertFalse(EmailProviderWebhook.objects.exists())

    def test_event_for_an_address_we_never_sent_to_is_skipped(self):
        # Ownership check: a bounce for an address with no matching outbox must not
        # suppress it (a webhook can't blacklist arbitrary addresses).
        self.make_anon_emailable("victim@example.com")  # sent nothing to them
        events = [
            {
                "event_id": "e4",
                "event_type": "bounced",
                "bounce_type": "hard",
                "email": "victim@example.com",
            }
        ]
        resp = self._post(events, body={"id": "evt-4"})
        self.assertEqual(resp.status_code, 200)  # acked, but…
        self.assertFalse(suppression.is_suppressed(self.site, "victim@example.com"))
        self.assertEqual(EmailEvent.objects.count(), 0)

    def test_redelivery_is_idempotent(self):
        self.make_anon_emailable("dup@example.com")
        self._sent_outbox("dup@example.com")
        events = [
            {
                "event_id": "e5",
                "event_type": "bounced",
                "bounce_type": "hard",
                "email": "dup@example.com",
            }
        ]
        self._post(events, body={"id": "evt-5"})
        self._post(events, body={"id": "evt-5"})  # same event id
        self.assertEqual(EmailProviderWebhook.objects.filter(event_id="evt-5").count(), 1)
        self.assertEqual(EmailEvent.objects.filter(event_type="bounced").count(), 1)

    def test_unknown_provider_is_rejected(self):
        resp = self._post([], slug="not_a_provider")
        self.assertEqual(resp.status_code, 400)

    def test_malformed_body_is_rejected(self):
        with mock.patch.object(
            EmailAccount, "get_provider_instance", return_value=_FakeProvider([])
        ):
            resp = self.client.post(
                self._url(), data="not-json", content_type="application/json", HTTP_X_SIGNATURE="s"
            )
        self.assertEqual(resp.status_code, 400)

    def test_soft_bounce_event_records_but_does_not_suppress(self):
        self.make_anon_emailable("soft@example.com")
        self._sent_outbox("soft@example.com")
        events = [
            {
                "event_id": "e6",
                "event_type": "bounced",
                "bounce_type": "soft",
                "email": "soft@example.com",
            }
        ]
        resp = self._post(events, body={"id": "evt-6"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            EmailEvent.objects.filter(event_type="bounced", bounce_type="soft").exists()
        )
        self.assertFalse(suppression.is_suppressed(self.site, "soft@example.com"))

    def test_bounce_matching_only_a_never_sent_message_is_skipped(self):
        # An outbox still queued (not actually handed to the provider) must not be
        # matched by address and suppressed.
        self.make_anon_emailable("queued@example.com")
        EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            from_email="store@example.com",
            to_email="queued@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="queued",  # never sent
        )
        events = [
            {
                "event_id": "eq",
                "event_type": "bounced",
                "bounce_type": "hard",
                "email": "queued@example.com",
            }
        ]
        resp = self._post(events, body={"id": "evt-q"})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(suppression.is_suppressed(self.site, "queued@example.com"))
        self.assertEqual(EmailEvent.objects.count(), 0)

    def test_webhook_acts_only_on_the_verified_accounts_sends(self):
        # A webhook verified for account A must not suppress an address that was only
        # sent through account B (same provider).
        from email_system.utils.encryption import encrypt_credentials

        acct_b = EmailAccount.objects.create(
            site=self.site,
            name="B",
            from_email="b@example.com",
            from_name="B",
            provider_key="builtin_smtp",
            credentials=encrypt_credentials(
                {"host": "h", "port": 587, "username": "u", "password": "p"}
            ),
            is_active=True,
            is_default=False,
        )
        EmailOutbox.objects.create(
            site=self.site,
            account=acct_b,
            from_email="b@example.com",
            to_email="onlyb@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="sent",
        )
        # self.account is the default → verified first, so verified_account = A.
        events = [
            {
                "event_id": "eB",
                "event_type": "bounced",
                "bounce_type": "hard",
                "email": "onlyb@example.com",
            }
        ]
        resp = self._post(events, body={"id": "evt-B"})
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(suppression.is_suppressed(self.site, "onlyb@example.com"))
        self.assertEqual(EmailEvent.objects.count(), 0)

    def test_processing_failure_returns_5xx_for_provider_retry(self):
        # If processing throws AFTER verification, ack 5xx so the provider redelivers;
        # the audit row stays unprocessed, its error is captured, nothing is suppressed.
        self.make_anon_emailable("boom@example.com")
        self._sent_outbox("boom@example.com")

        class _Boom(_FakeProvider):
            def parse_delivery_events(self, payload):
                raise RuntimeError("kaboom")

        provider = _Boom([], verify=True)
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            resp = self.client.post(
                self._url(),
                data=json.dumps({"id": "evt-boom"}),
                content_type="application/json",
                HTTP_X_SIGNATURE="sig",
            )
        self.assertEqual(resp.status_code, 500)
        rec = EmailProviderWebhook.objects.get(event_id="evt-boom")
        self.assertFalse(rec.processed)
        self.assertIn("kaboom", rec.processing_error)
        self.assertFalse(suppression.is_suppressed(self.site, "boom@example.com"))

    def test_oversized_batch_is_rejected_not_truncated(self):
        # A batch larger than the cap must 5xx (loud, retryable) — never a silent
        # slice that acks 200 and drops the tail forever.
        self._sent_outbox("big@example.com")
        events = [
            {"event_id": f"e{i}", "event_type": "delivered", "email": "big@example.com"}
            for i in range(1001)
        ]
        resp = self._post(events, body={"id": "evt-big"})
        self.assertEqual(resp.status_code, 500)
        rec = EmailProviderWebhook.objects.get(event_id="evt-big")
        self.assertFalse(rec.processed)
        self.assertEqual(EmailEvent.objects.count(), 0)

    def test_malformed_slug_is_rejected_before_db_work(self):
        # A slug outside [a-z0-9_-] is rejected up front (log-injection guard) — no
        # provider lookup, no audit row.
        resp = self.client.post(
            "/webhooks/email/Bad%20Slug/",
            data=json.dumps({"id": "x"}),
            content_type="application/json",
            HTTP_X_SIGNATURE="s",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(EmailProviderWebhook.objects.exists())
