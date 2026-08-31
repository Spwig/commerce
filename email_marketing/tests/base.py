"""Shared setup for Campaign Studio (email_marketing) tests.

These run under ``manage.py test email_marketing`` (which recreates the test DB
each run — a fresh migration was added, so a stale reused DB would not have the
tables). Because they run as Django ``TestCase``s rather than through pytest,
they cannot lean on ``tests/conftest.py`` fixtures — the helpers below recreate
the minimum single-tenant scaffolding (Site id=1, SiteSettings, an EmailAccount)
that every send-path test needs.

Two base classes are exported:

* ``MarketingTestCase`` — the fast default (wraps each test in a transaction).
* ``MarketingTransactionTestCase`` — for code paths that catch ``IntegrityError``
  (e.g. send_campaign's claim-first idempotency). A caught IntegrityError poisons
  the wrapping transaction that a plain ``TestCase`` uses, so those must run in
  autocommit under a ``TransactionTestCase`` (which also mirrors production).
"""

from django.contrib.sites.models import Site
from django.test import TestCase, TransactionTestCase

from email_marketing.models import Subscriber


class _MarketingHelpersMixin:
    """Scaffolding + object builders shared by both base classes."""

    # --- scaffolding helpers (static → usable from setUpTestData or setUp) ----

    @staticmethod
    def _ensure_site():
        site, _ = Site.objects.get_or_create(
            pk=1, defaults={"domain": "example.com", "name": "Test Store"}
        )
        if site.domain != "example.com":
            site.domain = "example.com"
            site.save(update_fields=["domain"])
        return site

    @staticmethod
    def _ensure_site_settings(**overrides):
        from core.models import SiteSettings

        defaults = {
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
            "email_delivery_mode": "live",
            "enable_double_opt_in": False,
        }
        defaults.update(overrides)
        settings_obj, _ = SiteSettings.objects.update_or_create(pk=1, defaults=defaults)
        return settings_obj

    @staticmethod
    def _ensure_email_account(site):
        from email_system.models import EmailAccount
        from email_system.utils.encryption import encrypt_credentials

        EmailAccount.objects.filter(site=site).delete()
        return EmailAccount.objects.create(
            site=site,
            name="Test Account",
            from_email="store@example.com",
            from_name="Test Store",
            provider_key="builtin_smtp",
            credentials=encrypt_credentials(
                {"host": "smtp.test.com", "port": 587, "username": "u", "password": "p"}
            ),
            is_active=True,
            is_default=True,
        )

    @classmethod
    def _build_scaffold(cls):
        cls.site = cls._ensure_site()
        cls.settings_obj = cls._ensure_site_settings()
        cls.account = cls._ensure_email_account(cls.site)

    # --- object builders -----------------------------------------------------

    def set_double_opt_in(self, value: bool):
        """Flip the merchant's double opt-in policy for a test."""
        from core.models import SiteSettings

        SiteSettings.objects.filter(pk=1).update(enable_double_opt_in=value)

    def make_subscriber(self, email, **kwargs):
        kwargs.setdefault("site", self.site)
        kwargs.setdefault("status", Subscriber.STATUS_ACTIVE)
        return Subscriber.objects.create(email=email, **kwargs)

    def make_anon_emailable(self, email):
        """Anonymous subscriber that clears the consent gate (opted in + verified)."""
        return self.make_subscriber(email, marketing_opt_in=True, marketing_verified=True)

    # --- journey graph builders ---------------------------------------------

    def add_node(self, journey, node_type, **config):
        """Create a JourneyNode; keyword args become its ``config``."""
        from email_marketing.models import JourneyNode

        return JourneyNode.objects.create(journey=journey, node_type=node_type, config=config or {})

    def add_edge(self, journey, from_node, to_node, branch="default"):
        from email_marketing.models import JourneyEdge

        return JourneyEdge.objects.create(
            journey=journey, from_node=from_node, to_node=to_node, branch=branch
        )

    def build_linear_journey(self, journey, specs):
        """Build ``entry → (wait → send)* → exit`` for ``specs`` = list of
        ``(delay_value, unit, campaign)``. Returns a dict with the created nodes
        (``entry``, ``waits``, ``sends``, ``exit``) for assertions."""
        from email_marketing.models import JourneyNode

        entry = self.add_node(journey, JourneyNode.TYPE_ENTRY)
        prev, waits, sends = entry, [], []
        for delay_value, unit, campaign in specs:
            wait = self.add_node(journey, JourneyNode.TYPE_WAIT_DELAY, value=delay_value, unit=unit)
            self.add_edge(journey, prev, wait)
            send = self.add_node(journey, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(campaign.id))
            self.add_edge(journey, wait, send)
            waits.append(wait)
            sends.append(send)
            prev = send
        exit_node = self.add_node(journey, JourneyNode.TYPE_EXIT)
        self.add_edge(journey, prev, exit_node)
        return {"entry": entry, "waits": waits, "sends": sends, "exit": exit_node}


class MarketingTestCase(_MarketingHelpersMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._build_scaffold()


class MarketingTransactionTestCase(_MarketingHelpersMixin, TransactionTestCase):
    """Autocommit base for paths that catch IntegrityError. Sets up per test
    because TransactionTestCase flushes tables between tests."""

    def setUp(self):
        super().setUp()
        self._build_scaffold()
