"""Behaviour 1 — Subscriber.is_emailable consent gate.

``is_emailable`` is the single gate anonymous leads get (email_system's own gate
keys off a User row), so every branch of it matters. Registered subscribers
defer to accounts.CommunicationPreference; anonymous subscribers carry their own
opt-in / double-opt-in state.
"""

from email_marketing.models import Subscriber
from tests.factories import UserFactory

from .base import MarketingTestCase


class IsEmailableTests(MarketingTestCase):
    def test_unsubscribed_subscriber_is_not_emailable(self):
        sub = self.make_subscriber(
            "gone@example.com",
            status=Subscriber.STATUS_UNSUBSCRIBED,
            marketing_opt_in=True,
            marketing_verified=True,
        )
        self.assertFalse(sub.is_emailable("newsletter"))

    def test_bounced_subscriber_is_not_emailable(self):
        sub = self.make_subscriber(
            "bounce@example.com",
            status=Subscriber.STATUS_BOUNCED,
            marketing_opt_in=True,
            marketing_verified=True,
        )
        self.assertFalse(sub.is_emailable("newsletter"))

    def test_anonymous_opted_in_and_verified_is_emailable(self):
        self.set_double_opt_in(True)  # even with confirmation required, verified passes
        sub = self.make_subscriber(
            "lead@example.com",
            marketing_opt_in=True,
            marketing_verified=True,
        )
        self.assertTrue(sub.is_emailable("newsletter"))

    def test_anonymous_not_opted_in_is_not_emailable(self):
        sub = self.make_subscriber("noopt@example.com", marketing_opt_in=False)
        self.assertFalse(sub.is_emailable("newsletter"))

    def test_anonymous_opted_in_but_unverified_is_not_emailable_with_double_opt_in(self):
        self.set_double_opt_in(True)
        sub = self.make_subscriber(
            "unconfirmed@example.com",
            marketing_opt_in=True,
            marketing_verified=False,
        )
        self.assertFalse(sub.is_emailable("newsletter"))

    def test_anonymous_opted_in_unverified_is_emailable_without_double_opt_in(self):
        self.set_double_opt_in(False)
        sub = self.make_subscriber(
            "single@example.com",
            marketing_opt_in=True,
            marketing_verified=False,
        )
        self.assertTrue(sub.is_emailable("newsletter"))

    def test_registered_subscriber_forbidding_marketing_is_not_emailable(self):
        """A registered subscriber defers to their CommunicationPreference.

        Fresh preferences default to marketing opt-out (GDPR), so a registered
        subscriber with no explicit opt-in must not be emailable.
        """
        user = UserFactory()  # fresh prefs default to marketing opt-out (GDPR)
        sub = self.make_subscriber("member@example.com", user=user)
        self.assertFalse(sub.is_emailable("newsletter"))
