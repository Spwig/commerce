"""P2 audiences: storefront newsletter signup + double opt-in confirmation.

Behaviour-named coverage for the ``subscribe_email`` / ``confirm_subscription``
capability seam and the public ``/newsletter/`` endpoints that back the
page-builder element and the footer/header widget.
"""

import json

from django.core.exceptions import ValidationError
from django.test import Client
from django.urls import reverse

from email_marketing.models import Subscriber
from email_marketing.services.subscriptions import (
    OUTCOME_ALREADY,
    confirm_subscription,
    subscribe_email,
)
from tests.factories import UserFactory

from .base import MarketingTestCase


class SubscribeServiceTests(MarketingTestCase):
    def test_storefront_signup_creates_pending_subscriber_when_double_opt_in(self):
        self.set_double_opt_in(True)

        subscribe_email("lead@example.com", source="signup")

        sub = Subscriber.objects.get(email="lead@example.com")
        self.assertEqual(sub.source, "signup")
        self.assertEqual(sub.status, Subscriber.STATUS_PENDING)
        self.assertTrue(sub.marketing_opt_in)
        self.assertFalse(sub.marketing_verified)
        self.assertTrue(sub.verification_token)
        self.assertFalse(sub.is_emailable())  # not emailable until confirmed

    def test_storefront_signup_activates_immediately_without_double_opt_in(self):
        self.set_double_opt_in(False)

        subscribe_email("eager@example.com")

        sub = Subscriber.objects.get(email="eager@example.com")
        self.assertEqual(sub.status, Subscriber.STATUS_ACTIVE)
        self.assertTrue(sub.marketing_verified)
        self.assertTrue(sub.is_emailable())

    def test_confirm_makes_subscriber_emailable(self):
        self.set_double_opt_in(True)
        subscribe_email("confirmme@example.com")
        sub = Subscriber.objects.get(email="confirmme@example.com")

        returned = confirm_subscription(sub.verification_token)

        sub.refresh_from_db()
        self.assertEqual(returned, sub)
        self.assertEqual(sub.status, Subscriber.STATUS_ACTIVE)
        self.assertTrue(sub.marketing_verified)
        self.assertTrue(sub.is_emailable())

    def test_confirm_is_idempotent(self):
        self.set_double_opt_in(True)
        subscribe_email("twice@example.com")
        token = Subscriber.objects.get(email="twice@example.com").verification_token

        self.assertIsNotNone(confirm_subscription(token))
        # Second click on the same link still succeeds, no error.
        self.assertIsNotNone(confirm_subscription(token))

    def test_confirm_rejects_unknown_or_blank_token(self):
        self.assertIsNone(confirm_subscription("no-such-token"))
        self.assertIsNone(confirm_subscription(""))

    def test_signup_does_not_duplicate_an_existing_subscriber(self):
        self.set_double_opt_in(False)
        subscribe_email("dup@example.com")
        outcome = subscribe_email("dup@example.com")

        self.assertEqual(outcome, OUTCOME_ALREADY)
        self.assertEqual(Subscriber.objects.filter(email="dup@example.com").count(), 1)

    def test_invalid_email_is_rejected(self):
        with self.assertRaises(ValidationError):
            subscribe_email("not-an-email")

    def test_confirm_mirrors_consent_to_a_linked_customer(self):
        self.set_double_opt_in(True)
        user = UserFactory(email="member@example.com")

        subscribe_email("member@example.com")
        sub = Subscriber.objects.get(email="member@example.com")
        self.assertEqual(sub.user, user)  # matched + linked

        confirm_subscription(sub.verification_token)

        from accounts.models import CommunicationPreference

        prefs, _ = CommunicationPreference.get_or_create_for_user(user)
        self.assertTrue(prefs.email_marketing)
        self.assertTrue(prefs.email_verified)
        sub.refresh_from_db()
        self.assertTrue(sub.is_emailable())  # deferral to prefs now passes


class SubscribeSecurityRegressionTests(MarketingTestCase):
    """Regressions for the security review of the storefront signup."""

    def test_anonymous_signup_never_flips_a_registered_users_consent_without_confirm(self):
        # Even with double opt-in OFF, matching a registered account forces
        # confirmation — an anonymous POST must not enable their marketing prefs.
        self.set_double_opt_in(False)
        user = UserFactory(email="target@example.com")

        subscribe_email("target@example.com")

        sub = Subscriber.objects.get(email="target@example.com")
        self.assertEqual(sub.status, Subscriber.STATUS_PENDING)  # forced confirm
        self.assertTrue(sub.verification_token)

        from accounts.models import CommunicationPreference

        prefs, _ = CommunicationPreference.get_or_create_for_user(user)
        self.assertFalse(prefs.email_marketing)  # untouched until they confirm
        self.assertFalse(prefs.email_verified)

    def test_repeat_pending_signup_does_not_rotate_token_or_resend(self):
        self.set_double_opt_in(True)
        subscribe_email("bomb@example.com")
        token1 = Subscriber.objects.get(email="bomb@example.com").verification_token

        subscribe_email("bomb@example.com")  # repeat submit
        token2 = Subscriber.objects.get(email="bomb@example.com").verification_token

        self.assertEqual(token1, token2)  # original confirmation link still valid

    def test_malformed_forwarded_for_does_not_crash_and_is_not_stored(self):
        from django.test import RequestFactory

        req = RequestFactory().post("/newsletter/subscribe/", HTTP_X_FORWARDED_FOR="not-an-ip")
        self.set_double_opt_in(False)

        subscribe_email("xff@example.com", request=req)

        sub = Subscriber.objects.get(email="xff@example.com")
        # Falls back to the valid REMOTE_ADDR, never the spoofed header value.
        self.assertEqual(sub.consent_ip, "127.0.0.1")


class SubscribeEndpointTests(MarketingTestCase):
    def setUp(self):
        super().setUp()
        from django.core.cache import cache

        cache.clear()  # reset the per-IP rate-limit counter between tests
        self.client = Client()
        self.url = reverse("newsletter:subscribe")

    def test_url_resolves_to_the_shipped_form_action(self):
        # The page-builder element and widget both default to /newsletter/subscribe/.
        self.assertEqual(self.url, "/newsletter/subscribe/")

    def test_plain_form_post_subscribes(self):
        self.set_double_opt_in(False)
        resp = self.client.post(self.url, {"email": "form@example.com"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Subscriber.objects.filter(email="form@example.com").exists())

    def test_json_ajax_post_returns_success_contract(self):
        self.set_double_opt_in(False)
        resp = self.client.post(
            self.url,
            data=json.dumps({"email": "ajax@example.com"}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertTrue(body["success"])
        self.assertIn("message", body)
        self.assertTrue(Subscriber.objects.filter(email="ajax@example.com").exists())

    def test_missing_email_returns_400(self):
        resp = self.client.post(self.url, {"email": ""})
        self.assertEqual(resp.status_code, 400)

    def test_honeypot_is_silently_dropped(self):
        resp = self.client.post(self.url, {"email": "bot@example.com", "company": "spam"})
        self.assertEqual(resp.status_code, 200)  # looks successful to the bot
        self.assertFalse(Subscriber.objects.filter(email="bot@example.com").exists())

    def test_get_is_rejected(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_already_subscribed_response_is_indistinguishable(self):
        # Non-enumeration: a repeat signup returns the same response as a first
        # one. Asserted on the JSON path — HTML responses carry a dev debug
        # toolbar id that varies per request.
        self.set_double_opt_in(True)

        def post():
            return self.client.post(
                self.url,
                data=json.dumps({"email": "probe@example.com"}),
                content_type="application/json",
                HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            )

        first, second = post(), post()
        self.assertEqual(first.status_code, second.status_code)
        self.assertEqual(first.json(), second.json())


class ConfirmEndpointTests(MarketingTestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_confirmation_link_activates_the_subscriber(self):
        self.set_double_opt_in(True)
        subscribe_email("clicker@example.com")
        token = Subscriber.objects.get(email="clicker@example.com").verification_token

        resp = self.client.get(reverse("newsletter:confirm", args=[token]))

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Subscriber.objects.get(email="clicker@example.com").marketing_verified)

    def test_invalid_confirmation_link_returns_404(self):
        resp = self.client.get(reverse("newsletter:confirm", args=["bogus"]))
        self.assertEqual(resp.status_code, 404)
