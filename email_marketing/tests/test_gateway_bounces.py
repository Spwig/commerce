"""Hosted-gateway bounce poll → list hygiene (Stage 3a).

A Spwig-hosted install pulls the gateway's delayed bounce/complaint log and feeds
each record into the Stage-1 suppression seam. The gateway client is mocked (the
live URL/key are ops-provisioned); these tests prove the ingestion/match/suppress
and idempotency behaviour end-to-end.
"""

from django.contrib.auth import get_user_model

from email_marketing.models import Subscriber
from email_marketing.services import gateway_bounces, suppression
from email_system.models import EmailAccount, EmailEvent, EmailOutbox
from email_system.utils.encryption import encrypt_credentials

from .base import MarketingTestCase


class _FakeGateway:
    def __init__(self, payload=None, raises=None):
        self._payload = payload if payload is not None else {"bounces": []}
        self._raises = raises

    def get_merchant_bounces(self, slug):
        if self._raises:
            raise self._raises
        return self._payload


class GatewayBounceIngestTests(MarketingTestCase):
    def _hosted_account(self, slug="acme"):
        return EmailAccount.objects.create(
            site=self.site,
            name="Hosted",
            from_email="h@example.com",
            from_name="H",
            provider_key="spwig_hosted_mail",
            credentials=encrypt_credentials({"auth_user": slug, "gateway_host": "gw.example.com"}),
            is_active=True,
            is_default=False,
        )

    def _sent(self, account, to_email):
        return EmailOutbox.objects.create(
            site=self.site,
            account=account,
            from_email="h@example.com",
            to_email=to_email,
            subject="s",
            html_body="<p>h</p>",
            template_type="newsletter",
            status="sent",
        )

    def test_no_hosted_account_is_a_noop(self):
        # MarketingTestCase's account is builtin_smtp, not hosted.
        res = gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway())
        self.assertEqual(res, {"skipped": "no_hosted_account"})

    def test_real_client_path_requires_gateway_api_key(self):
        # Hosted account exists but no management API key configured → no-op.
        self._hosted_account()
        res = gateway_bounces.ingest_hosted_gateway_bounces()
        self.assertEqual(res, {"skipped": "not_configured"})

    def test_hard_bounce_with_matching_send_records_and_suppresses(self):
        acct = self._hosted_account()
        self.make_anon_emailable("dead@example.com")
        self._sent(acct, "dead@example.com")
        payload = {
            "bounces": [
                {"id": "b1", "type": "hard", "email": "dead@example.com", "reason": "550 no user"}
            ]
        }
        res = gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(res["recorded"], 1)
        self.assertTrue(
            EmailEvent.objects.filter(event_type="bounced", bounce_type="hard").exists()
        )
        self.assertTrue(suppression.is_suppressed(self.site, "dead@example.com"))

    def test_hard_bounce_without_a_send_suppresses_directly(self):
        self._hosted_account()
        payload = {"bounces": [{"id": "b2", "type": "hard", "email": "nobody@example.com"}]}
        res = gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(res["suppressed"], 1)
        self.assertTrue(suppression.is_suppressed(self.site, "nobody@example.com"))

    def test_complaint_suppresses(self):
        self._hosted_account()
        payload = {"bounces": [{"id": "c1", "type": "complaint", "email": "spammy@example.com"}]}
        gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertTrue(suppression.is_suppressed(self.site, "spammy@example.com"))

    def test_soft_bounce_without_a_send_is_not_suppressed(self):
        self._hosted_account()
        payload = {"bounces": [{"id": "s1", "type": "soft", "email": "maybe@example.com"}]}
        res = gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(res["suppressed"], 0)
        self.assertFalse(suppression.is_suppressed(self.site, "maybe@example.com"))

    def test_reingesting_the_same_record_is_idempotent(self):
        acct = self._hosted_account()
        self._sent(acct, "dup@example.com")
        payload = {"bounces": [{"id": "b9", "type": "hard", "email": "dup@example.com"}]}
        gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(EmailEvent.objects.filter(event_type="bounced").count(), 1)

    def test_gateway_error_is_handled_gracefully(self):
        self._hosted_account()
        res = gateway_bounces.ingest_hosted_gateway_bounces(
            client=_FakeGateway(raises=RuntimeError("boom"))
        )
        self.assertEqual(res, {"error": "gateway_unreachable"})

    def test_bare_list_response_is_parsed(self):
        self._hosted_account()
        payload = [{"id": "x1", "type": "hard", "email": "listform@example.com"}]
        res = gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(res["suppressed"], 1)
        self.assertTrue(suppression.is_suppressed(self.site, "listform@example.com"))

    def test_no_send_trail_complaint_does_not_relabel_a_registered_subscriber(self):
        # Trust boundary: a gateway complaint for an address we have NO send trail
        # for blocks the address but must not destructively relabel / unsubscribe a
        # real registered subscriber off an unverified external record.
        user = get_user_model().objects.create_user(
            username="reg", email="reg@example.com", password="x"
        )
        sub = self.make_subscriber(
            "reg@example.com", user=user, marketing_opt_in=True, marketing_verified=True
        )
        self._hosted_account()  # no outbox to reg@example.com
        payload = {"bounces": [{"id": "c9", "type": "complaint", "email": "reg@example.com"}]}
        gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertTrue(suppression.is_suppressed(self.site, "reg@example.com"))
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_ACTIVE)
        self.assertTrue(sub.marketing_opt_in)

    def test_generic_bounce_with_explicit_soft_type_is_classified_soft(self):
        # A coarse "bounce" label carrying bounce_type=soft must not be escalated to
        # a hard suppression.
        acct = self._hosted_account()
        self._sent(acct, "sc@example.com")
        payload = {
            "bounces": [
                {"id": "m1", "type": "bounce", "bounce_type": "soft", "email": "sc@example.com"}
            ]
        }
        gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        ev = EmailEvent.objects.get(event_type="bounced")
        self.assertEqual(ev.bounce_type, "soft")
        self.assertFalse(suppression.is_suppressed(self.site, "sc@example.com"))

    def test_record_without_id_or_timestamp_is_skipped(self):
        # No stable identity → skip rather than re-count on every poll.
        acct = self._hosted_account()
        self._sent(acct, "noid@example.com")
        payload = {"bounces": [{"type": "hard", "email": "noid@example.com"}]}
        res = gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(res["skipped"], 1)
        self.assertEqual(EmailEvent.objects.count(), 0)

    def test_reingesting_a_no_send_trail_record_does_not_recount(self):
        # The direct-suppress path has no outbox to record a per-record id on, so a
        # re-poll of the same already-suppressed address must be a no-op, not re-counted.
        self._hosted_account()
        payload = {"bounces": [{"id": "d1", "type": "hard", "email": "gone@example.com"}]}
        r1 = gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        r2 = gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(r1["suppressed"], 1)
        self.assertEqual(r2["suppressed"], 0)
        self.assertTrue(suppression.is_suppressed(self.site, "gone@example.com"))

    def test_no_send_trail_complaint_upgrades_an_earlier_hard_suppression(self):
        # A distinct, stronger signal (complaint after hard) for an already-suppressed
        # no-send-trail address must still be acted on — not skipped as a duplicate.
        from email_marketing.models import SuppressionEntry

        self._hosted_account()
        gateway_bounces.ingest_hosted_gateway_bounces(
            client=_FakeGateway(
                {"bounces": [{"id": "h1", "type": "hard", "email": "u@example.com"}]}
            )
        )
        entry = SuppressionEntry.objects.get(site=self.site, email="u@example.com")
        self.assertEqual(entry.reason, SuppressionEntry.REASON_HARD_BOUNCE)
        r = gateway_bounces.ingest_hosted_gateway_bounces(
            client=_FakeGateway(
                {"bounces": [{"id": "c1", "type": "complaint", "email": "u@example.com"}]}
            )
        )
        self.assertEqual(r["suppressed"], 1)
        entry.refresh_from_db()
        self.assertEqual(entry.reason, SuppressionEntry.REASON_COMPLAINT)

    def test_gateway_hard_bounce_does_not_overwrite_a_manual_block(self):
        # A merchant's deliberate manual block must survive a gateway hard-bounce
        # record for the same no-send-trail address — no relabel to hard/gateway.
        from email_marketing.models import SuppressionEntry

        self._hosted_account()
        suppression.suppress(
            self.site,
            "vip@example.com",
            reason=SuppressionEntry.REASON_MANUAL,
            source=SuppressionEntry.SOURCE_MANUAL,
            detail="blocked by merchant",
        )
        r = gateway_bounces.ingest_hosted_gateway_bounces(
            client=_FakeGateway(
                {"bounces": [{"id": "h9", "type": "hard", "email": "vip@example.com"}]}
            )
        )
        self.assertEqual(r["suppressed"], 0)
        entry = SuppressionEntry.objects.get(site=self.site, email="vip@example.com")
        self.assertEqual(entry.reason, SuppressionEntry.REASON_MANUAL)
        self.assertEqual(entry.detail, "blocked by merchant")

    def test_same_record_is_not_recounted_after_a_newer_send(self):
        # Account-scoped dedup: a later send to the address moves _recent_outbox, but
        # the same gateway record id must not be recorded (and re-counted) twice.
        acct = self._hosted_account()
        self._sent(acct, "same@example.com")
        payload = {"bounces": [{"id": "b7", "type": "soft", "email": "same@example.com"}]}
        gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(EmailEvent.objects.filter(event_type="bounced").count(), 1)
        self._sent(acct, "same@example.com")  # newer send → newer _recent_outbox
        gateway_bounces.ingest_hosted_gateway_bounces(client=_FakeGateway(payload))
        self.assertEqual(EmailEvent.objects.filter(event_type="bounced").count(), 1)
