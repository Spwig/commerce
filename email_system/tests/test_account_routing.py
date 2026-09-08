"""Transactional vs marketing sending-account routing (Phase 1).

``queue_email`` routes marketing-priority mail (campaigns / journeys) to a
dedicated marketing ``EmailAccount`` when one is configured, so campaign sending
reputation stays separate from transactional email (order confirmations, password
resets). A single ``both`` account — the default for every existing install — must
keep serving both classes unchanged.
"""

from django.contrib.sites.models import Site
from django.test import TestCase

from email_system.models import EmailAccount
from email_system.services.email_sender import EmailSendingService
from email_system.utils.encryption import encrypt_credentials


class AccountRoutingTests(TestCase):
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

    def _account(self, name, email, purpose=EmailAccount.PURPOSE_BOTH, default=False):
        return EmailAccount.objects.create(
            site=self.site,
            name=name,
            from_email=email,
            from_name=name,
            provider_key="builtin_smtp",
            credentials=encrypt_credentials({"host": "127.0.0.1", "port": 2525}),
            is_active=True,
            is_default=default,
            purpose=purpose,
        )

    def _queue(self, template_type):
        return EmailSendingService.queue_email(
            to_email="buyer@example.com",
            subject="Hi",
            html_body="<p>Hi</p>",
            site=self.site,
            template_type=template_type,
        )

    # --- resolver: get_account_for -----------------------------------------

    def test_single_both_account_serves_both_classes(self):
        """Back-compat: one default ``both`` account serves transactional and marketing."""
        acct = self._account("Default", "store@example.com", default=True)
        self.assertEqual(EmailSendingService.get_account_for(self.site, marketing=False), acct)
        self.assertEqual(EmailSendingService.get_account_for(self.site, marketing=True), acct)

    def test_marketing_routes_to_marketing_account(self):
        txn = self._account("Transactional", "store@example.com", default=True)
        mkt = self._account("Marketing", "news@news.example.com", EmailAccount.PURPOSE_MARKETING)
        self.assertEqual(EmailSendingService.get_account_for(self.site, marketing=True), mkt)
        self.assertEqual(EmailSendingService.get_account_for(self.site, marketing=False), txn)

    def test_purpose_specific_beats_both(self):
        self._account("Shared", "store@example.com", EmailAccount.PURPOSE_BOTH, default=True)
        txn = self._account("Txn-only", "txn@example.com", EmailAccount.PURPOSE_TRANSACTIONAL)
        self.assertEqual(EmailSendingService.get_account_for(self.site, marketing=False), txn)

    def test_transactional_never_uses_a_marketing_only_account(self):
        """The whole point: transactional mail must not inherit marketing reputation."""
        self._account(
            "Marketing", "news@news.example.com", EmailAccount.PURPOSE_MARKETING, default=True
        )
        # No transactional/both account → transactional resolves to None rather than the
        # marketing identity; marketing still resolves to it.
        self.assertIsNone(EmailSendingService.get_account_for(self.site, marketing=False))
        self.assertEqual(
            EmailSendingService.get_account_for(self.site, marketing=True).purpose,
            EmailAccount.PURPOSE_MARKETING,
        )

    # --- classifier: which message types are "marketing" for routing --------

    def test_marketing_class_classifier(self):
        c = EmailSendingService._is_marketing_class
        self.assertTrue(c("newsletter"))  # marketing
        self.assertTrue(c("promotional_offers"))  # marketing
        self.assertTrue(c("back_in_stock"))  # marketing
        self.assertTrue(c("abandoned_cart_recovery"))  # marketing (cart recovery)
        self.assertFalse(c("order_confirmation"))  # transactional
        self.assertFalse(c("password_reset"))  # transactional
        self.assertFalse(c(None))  # ad-hoc / unclassified → transactional identity
        self.assertFalse(c("some_unknown_type"))  # unknown → safe transactional default

    # --- queue_email binds the resolved account on the outbox ---------------

    def test_queue_email_marketing_type_binds_marketing_account(self):
        txn = self._account("Transactional", "store@example.com", default=True)
        mkt = self._account("Marketing", "news@news.example.com", EmailAccount.PURPOSE_MARKETING)
        self.assertEqual(self._queue("newsletter").account_id, mkt.id)
        self.assertEqual(self._queue("order_confirmation").account_id, txn.id)

    def test_queue_email_unknown_type_routes_transactional(self):
        txn = self._account(
            "Transactional", "store@example.com", EmailAccount.PURPOSE_TRANSACTIONAL
        )
        self._account("Marketing", "news@news.example.com", EmailAccount.PURPOSE_MARKETING)
        # Unknown/None type must not leak onto the marketing identity.
        self.assertEqual(self._queue("some_unknown_type").account_id, txn.id)
        self.assertEqual(self._queue(None).account_id, txn.id)

    def test_queue_email_falls_back_to_default_without_a_marketing_account(self):
        txn = self._account("Default", "store@example.com", default=True)
        self.assertEqual(self._queue("newsletter").account_id, txn.id)

    # --- clean(): a store must keep a transactional-capable account ----------

    def test_cannot_leave_store_without_a_transactional_account(self):
        from django.core.exceptions import ValidationError

        sole = self._account("Only account", "store@example.com", default=True)
        sole.purpose = EmailAccount.PURPOSE_MARKETING
        with self.assertRaises(ValidationError):
            sole.full_clean()

    def test_marketing_account_is_allowed_alongside_a_transactional_one(self):
        self._account("Transactional", "store@example.com", default=True)
        mkt = self._account("Marketing", "news@news.example.com", EmailAccount.PURPOSE_MARKETING)
        mkt.full_clean()  # does not raise

    def test_cannot_deactivate_the_last_transactional_account(self):
        from django.core.exceptions import ValidationError

        both = self._account("Both", "store@example.com", default=True)
        self._account("Marketing", "news@news.example.com", EmailAccount.PURPOSE_MARKETING)
        both.is_active = False  # would leave only a marketing account active
        with self.assertRaises(ValidationError):
            both.full_clean()

    def test_deactivating_the_marketing_account_is_allowed(self):
        self._account("Transactional", "store@example.com", default=True)
        mkt = self._account("Marketing", "news@news.example.com", EmailAccount.PURPOSE_MARKETING)
        mkt.is_active = False
        mkt.full_clean()  # transactional account still active → OK

    def test_would_orphan_transactional_guard_method(self):
        """The public guard the admin toggle/bulk-disable actions call (they bypass clean)."""
        both = self._account("Both", "store@example.com", default=True)
        mkt = self._account("Marketing", "news@news.example.com", EmailAccount.PURPOSE_MARKETING)
        both.is_active = False  # disabling the sole transactional account
        self.assertTrue(both.would_orphan_transactional())
        mkt.is_active = False  # disabling the marketing account is fine
        self.assertFalse(mkt.would_orphan_transactional())
