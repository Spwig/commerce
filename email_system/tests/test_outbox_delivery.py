"""Outbox delivery guarantees — transactional email must actually send, exactly once.

Stage 0 of the transactional-first-email plan: these tests PIN the two known gaps
and fail against the current code, then pass once the delivery fix lands.

Gap 1 (delivery): ``send_template_email`` queues an EmailOutbox at status="queued"
and nothing drains it, so transactional email is silently dropped in live mode.

Gap 2 (atomicity): ``send_email`` checks status then sets "sending" non-atomically
and does not treat an already-"sending" row as claimed, so two concurrent sends can
both hit the provider (double-send to a customer).
"""

from datetime import timedelta
from unittest import mock

from django.contrib.sites.models import Site
from django.test import TestCase, override_settings
from django.utils import timezone

from email_system.models import EmailAccount, EmailOutbox
from email_system.services.email_sender import EmailSendingService
from email_system.utils.encryption import encrypt_credentials

_ACCEPTED = {
    "provider_message_id": "pm-1",
    "accepted": True,
    "status": "sent",
    "error": None,
    "details": {},
}


class _OutboxBase(TestCase):
    def setUp(self):
        self.site, _ = Site.objects.get_or_create(
            pk=1, defaults={"domain": "example.com", "name": "Test Store"}
        )
        from core.models import SiteSettings

        SiteSettings.objects.update_or_create(
            pk=1,
            defaults={
                "site_name": "Test Store",
                "admin_email": "admin@test.spwig.com",
                "default_currency": "USD",
                "default_language": "en",
                "email_delivery_mode": "live",
            },
        )
        self.account = EmailAccount.objects.create(
            site=self.site,
            name="Test Account",
            from_email="store@example.com",
            from_name="Test Store",
            provider_key="builtin_smtp",
            credentials=encrypt_credentials(
                {"host": "127.0.0.1", "port": 2525, "username": "u", "password": "p"}
            ),
            is_active=True,
            is_default=True,
        )

    def _mock_provider(self):
        provider = mock.Mock()
        provider.send.return_value = dict(_ACCEPTED)
        return provider

    def _outbox(self, status="queued", **kw):
        return EmailOutbox.objects.create(
            site=self.site,
            account=self.account,
            to_email=kw.pop("to_email", "buyer@example.com"),
            from_email="store@example.com",
            subject="s",
            html_body="<p>h</p>",
            template_type="order_confirmation",
            status=status,
            **kw,
        )


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class TransactionalDeliveryTests(_OutboxBase):
    def test_transactional_send_template_email_actually_sends(self):
        # GAP 1: today send_template_email only queues → the provider is never hit
        # and the row is stranded at "queued". After the fix, an on-commit dispatch
        # delivers it.
        provider = self._mock_provider()
        with (
            mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider),
            mock.patch(
                "email_system.services.template_renderer.TemplateRenderer.render",
                return_value=("Order confirmed", "<p>Thanks</p>", "Thanks"),
            ),
        ):
            with self.captureOnCommitCallbacks(execute=True):
                outbox = EmailSendingService.send_template_email(
                    to_email="buyer@example.com",
                    template_type="order_confirmation",
                    context={},
                )
        provider.send.assert_called_once()
        outbox.refresh_from_db()
        self.assertEqual(outbox.status, "sent")

    def test_send_template_email_stamps_transactional_priority(self):
        with mock.patch(
            "email_system.services.template_renderer.TemplateRenderer.render",
            return_value=("S", "<p>h</p>", "h"),
        ):
            ob = EmailSendingService.send_template_email(
                to_email="a@example.com",
                template_type="order_confirmation",
                context={},
                dispatch=False,
            )
        self.assertEqual(ob.priority, EmailOutbox.PRIORITY_TRANSACTIONAL)


class AtomicClaimTests(_OutboxBase):
    def test_send_email_does_not_resend_a_row_already_sending(self):
        # GAP 2: an already-"sending" row represents a claim another worker is
        # mid-flight on. Re-sending it double-mails the customer. The fix claims
        # atomically on status="queued", so a "sending" row is not re-sent.
        provider = self._mock_provider()
        outbox = self._outbox(status="sending")
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            EmailSendingService.send_email(str(outbox.id))
        provider.send.assert_not_called()

    def test_failed_row_with_retries_left_is_resent(self):
        # The retry path (retry_failed_emails → send_email) must still work: a
        # "failed" row that hasn't exhausted retries is claimable and re-sent.
        provider = self._mock_provider()
        outbox = self._outbox(status="failed", retry_count=1, max_retries=3)
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            ok = EmailSendingService.send_email(str(outbox.id))
        self.assertTrue(ok)
        provider.send.assert_called_once()
        outbox.refresh_from_db()
        self.assertEqual(outbox.status, "sent")

    def test_failed_row_out_of_retries_is_not_resent(self):
        provider = self._mock_provider()
        outbox = self._outbox(status="failed", retry_count=3, max_retries=3)
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            ok = EmailSendingService.send_email(str(outbox.id))
        self.assertFalse(ok)
        provider.send.assert_not_called()

    @override_settings(
        EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE=1, EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE=1
    )
    def test_budget_defer_of_a_failed_marketing_row_preserves_failed_status(self):
        # A retry claims a "failed" marketing row; if it defers on budget it must be
        # restored to "failed" (with retry_count intact), not promoted to "queued".
        from email_system.services import send_budget

        try:
            send_budget._redis().delete(send_budget._key(self.account.id))
        except Exception:
            self.skipTest("Redis not available")
        provider = self._mock_provider()
        ob = self._outbox(
            status="failed",
            retry_count=1,
            max_retries=3,
            priority=EmailOutbox.PRIORITY_MARKETING,
        )
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            ok = EmailSendingService.send_email(str(ob.id))
        self.assertFalse(ok)
        provider.send.assert_not_called()
        ob.refresh_from_db()
        self.assertEqual(ob.status, "failed")
        self.assertEqual(ob.retry_count, 1)


@override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
class PendingSweepTests(_OutboxBase):
    def _queued_at(self, outbox, when):
        EmailOutbox.objects.filter(id=outbox.id).update(queued_at=when)

    @override_settings(EMAIL_PENDING_SWEEP_GRACE_SECONDS=0)
    def test_sweep_delivers_a_stranded_queued_row(self):
        from email_system.tasks import drain_pending_outbox

        provider = self._mock_provider()
        ob = self._outbox(status="queued")
        self._queued_at(ob, timezone.now() - timedelta(minutes=5))
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            res = drain_pending_outbox()
        provider.send.assert_called_once()
        ob.refresh_from_db()
        self.assertEqual(ob.status, "sent")
        self.assertEqual(res["dispatched"], 1)

    @override_settings(EMAIL_PENDING_SWEEP_GRACE_SECONDS=0)
    def test_sweep_skips_campaign_rows(self):
        # Campaign outbox rows are the campaign drainer's job — claiming them here
        # would race it. The sweep excludes anything with a CampaignSend.
        from email_marketing.models import Campaign, CampaignSend, Subscriber
        from email_system.tasks import drain_pending_outbox

        provider = self._mock_provider()
        ob = self._outbox(status="queued")
        self._queued_at(ob, timezone.now() - timedelta(minutes=5))
        camp = Campaign.objects.create(site=self.site, name="C", subject="s")
        sub = Subscriber.objects.create(site=self.site, email="buyer@example.com")
        CampaignSend.objects.create(campaign=camp, subscriber=sub, outbox=ob, status="queued")
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            drain_pending_outbox()
        provider.send.assert_not_called()
        ob.refresh_from_db()
        self.assertEqual(ob.status, "queued")

    @override_settings(EMAIL_PENDING_SWEEP_STUCK_SECONDS=600)
    def test_sweep_reclaims_stuck_sending_rows(self):
        from email_system.tasks import drain_pending_outbox

        ob = self._outbox(status="sending")  # queued_at stays NULL → pass-2 won't re-pick
        EmailOutbox.objects.filter(id=ob.id).update(
            updated_at=timezone.now() - timedelta(seconds=700)
        )
        res = drain_pending_outbox()
        ob.refresh_from_db()
        self.assertEqual(ob.status, "queued")
        self.assertEqual(ob.retry_count, 1)
        self.assertEqual(res["reclaimed"], 1)

    @override_settings(EMAIL_PENDING_SWEEP_GRACE_SECONDS=120, EMAIL_PENDING_SWEEP_MAX_AGE_HOURS=24)
    def test_sweep_ignores_too_fresh_and_too_old_rows(self):
        from email_system.tasks import drain_pending_outbox

        provider = self._mock_provider()
        fresh = self._outbox(status="queued", to_email="fresh@example.com")
        self._queued_at(fresh, timezone.now())  # inside grace
        old = self._outbox(status="queued", to_email="old@example.com")
        self._queued_at(old, timezone.now() - timedelta(hours=48))  # past max age
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            res = drain_pending_outbox()
        provider.send.assert_not_called()
        self.assertEqual(res["dispatched"], 0)

    @override_settings(EMAIL_PENDING_SWEEP_ENABLED=False)
    def test_sweep_disabled_is_a_noop(self):
        from email_system.tasks import drain_pending_outbox

        ob = self._outbox(status="queued")
        self._queued_at(ob, timezone.now() - timedelta(minutes=5))
        res = drain_pending_outbox()
        self.assertEqual(res, {"reclaimed": 0, "dispatched": 0})

    @override_settings(
        EMAIL_PENDING_SWEEP_GRACE_SECONDS=0,
        EMAIL_ACCOUNT_SEND_RATE_PER_MINUTE=1,
        EMAIL_TRANSACTIONAL_RESERVE_PER_MINUTE=1,
    )
    def test_sweep_defers_marketing_but_sends_transactional_under_budget(self):
        # ceiling 1 / reserve 1 → marketing cap 0: every marketing (journey) row
        # defers, transactional always goes.
        from email_system.services import send_budget
        from email_system.tasks import drain_pending_outbox

        try:
            send_budget._redis().delete(send_budget._key(self.account.id))
        except Exception:
            self.skipTest("Redis not available")

        provider = self._mock_provider()
        mk = self._outbox(
            status="queued", to_email="mk@example.com", priority=EmailOutbox.PRIORITY_MARKETING
        )
        self._queued_at(mk, timezone.now() - timedelta(minutes=5))
        tx = self._outbox(
            status="queued", to_email="tx@example.com", priority=EmailOutbox.PRIORITY_TRANSACTIONAL
        )
        self._queued_at(tx, timezone.now() - timedelta(minutes=5))
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            drain_pending_outbox()  # dispatches both; send_email applies the budget gate
        mk.refresh_from_db()
        tx.refresh_from_db()
        self.assertEqual(mk.status, "queued")  # marketing deferred back to queued
        self.assertEqual(tx.status, "sent")  # transactional delivered
        provider.send.assert_called_once()  # only the transactional row hit SMTP

    @override_settings(EMAIL_PENDING_SWEEP_GRACE_SECONDS=0)
    def test_naive_floor_does_not_crash_the_sweep_and_is_respected(self):
        # The recommended backlog lever (a floor timestamp) must not blow up the
        # sweep when set without a timezone offset (USE_TZ=True).
        from email_system.tasks import drain_pending_outbox

        provider = self._mock_provider()
        ob = self._outbox(status="queued")
        self._queued_at(ob, timezone.now() - timedelta(minutes=5))
        future_floor = (timezone.now() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        with (
            override_settings(EMAIL_PENDING_SWEEP_FLOOR=future_floor),
            mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider),
        ):
            res = drain_pending_outbox()  # naive floor in the future → nothing swept
        self.assertEqual(res["dispatched"], 0)
        provider.send.assert_not_called()


class RetryBackoffTests(_OutboxBase):
    @override_settings(EMAIL_RETRY_BACKOFF_MINUTES=15)
    def test_recent_failure_is_not_retried_but_an_old_one_is(self):
        provider = self._mock_provider()
        recent = self._outbox(status="failed", retry_count=1, to_email="recent@example.com")
        EmailOutbox.objects.filter(id=recent.id).update(failed_at=timezone.now())
        old = self._outbox(status="failed", retry_count=1, to_email="old@example.com")
        EmailOutbox.objects.filter(id=old.id).update(
            failed_at=timezone.now() - timedelta(minutes=30)
        )
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            EmailSendingService.retry_failed_emails()
        # Only the row past the backoff window was retried.
        provider.send.assert_called_once()
        recent.refresh_from_db()
        old.refresh_from_db()
        self.assertEqual(recent.status, "failed")
        self.assertEqual(old.status, "sent")

    @override_settings(EMAIL_RETRY_BACKOFF_MINUTES=15)
    def test_retry_skips_failed_marketing_rows(self):
        # Marketing failures belong to the campaign drainer + CampaignSend bookkeeping;
        # the transactional retry beat must not re-send them (would desync metrics).
        provider = self._mock_provider()
        ob = self._outbox(status="failed", retry_count=1, priority=EmailOutbox.PRIORITY_MARKETING)
        EmailOutbox.objects.filter(id=ob.id).update(
            failed_at=timezone.now() - timedelta(minutes=30)
        )
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            EmailSendingService.retry_failed_emails()
        provider.send.assert_not_called()
        ob.refresh_from_db()
        self.assertEqual(ob.status, "failed")


class DeliveryModeKillSwitchTests(_OutboxBase):
    def _set_mode(self, mode):
        from core.models import SiteSettings

        # get_settings() re-reads from the DB (no cache), so a plain update suffices.
        SiteSettings.objects.filter(pk=1).update(email_delivery_mode=mode)

    def test_paused_mode_holds_a_queued_row_instead_of_sending(self):
        provider = self._mock_provider()
        outbox = self._outbox(status="queued")
        self._set_mode("paused")
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            ok = EmailSendingService.send_email(str(outbox.id))
        self.assertFalse(ok)
        provider.send.assert_not_called()
        outbox.refresh_from_db()
        self.assertEqual(outbox.status, "held")

    def test_log_only_mode_logs_a_queued_row_instead_of_sending(self):
        provider = self._mock_provider()
        outbox = self._outbox(status="queued")
        self._set_mode("log_only")
        with mock.patch.object(EmailAccount, "get_provider_instance", return_value=provider):
            ok = EmailSendingService.send_email(str(outbox.id))
        self.assertFalse(ok)
        provider.send.assert_not_called()
        outbox.refresh_from_db()
        self.assertEqual(outbox.status, "logged")
