"""The setup wizard carries an optional sending ``purpose`` into the account it creates.

The "Marketing sending domain" entry (Campaign Studio nudge + account-list button)
deep-links the wizard with ``?purpose=marketing`` so the account it creates is a
dedicated marketing sender — keeping campaign reputation off the transactional identity.

The purpose is held in its own session key (``email_wizard_purpose``) so it survives
Step 1's wizard-data reset and every internal redirect back to Step 1, and is cleared only
when a provider is freshly selected without one (a normal setup) or when setup completes.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings
from django.urls import reverse

# Strip install-state gates (licence acceptance / activation) so the client reaches the
# wizard view — they are unrelated to the purpose-threading logic under test here.
_MIDDLEWARE = [
    m
    for m in settings.MIDDLEWARE
    if not any(
        x in m
        for x in ("license_acceptance", "middleware.activation", "middleware.license", "POSLicense")
    )
]


@override_settings(MIDDLEWARE=_MIDDLEWARE)
class MarketingWizardPurposeTests(TestCase):
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
            },
        )
        self.admin = get_user_model().objects.create_superuser(
            "wiz", "wiz@example.com", "pw-not-a-login"
        )
        self.client.force_login(self.admin)

    def _session_purpose(self):
        return self.client.session.get("email_wizard_purpose")

    def _step1(self, query=""):
        self.client.get(reverse("email_system:wizard_step1") + query)

    def test_marketing_entry_records_the_prefill_hint(self):
        # The hint only PRE-TICKS the Step 6 checkbox; the account's purpose is taken from
        # that submitted checkbox, so the account can never get the wrong purpose silently.
        self._step1("?purpose=marketing")
        self.assertEqual(self._session_purpose(), "marketing")

    def test_invalid_purpose_is_ignored(self):
        self._step1("?purpose=not_a_real_purpose")
        self.assertIsNone(self._session_purpose())

    def test_no_purpose_leaves_no_hint(self):
        self._step1()
        self.assertIsNone(self._session_purpose())

    def test_prefill_hint_survives_navigation(self):
        # Because the checkbox (not the session) decides the purpose, the hint can safely
        # persist across every navigation — bare landings AND fresh provider selections —
        # without ever silently mislabelling an account.
        self._step1("?purpose=marketing")
        self._step1()  # bare landing (Step 2 Back link, error recovery)
        self.assertEqual(self._session_purpose(), "marketing")
        self._step1("?provider=builtin_smtp")  # provider selection
        self.assertEqual(self._session_purpose(), "marketing")
