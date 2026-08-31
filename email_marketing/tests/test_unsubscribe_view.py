"""Behaviour 6 — tokenised unsubscribe view.

The endpoint is unauthenticated (recipients act from an email link). GET renders
a confirmation page and changes nothing (so inbox link-scanners / prefetchers
can't trigger accidental opt-outs); POST performs the opt-out and is CSRF-exempt
for RFC 8058 one-click List-Unsubscribe-Post. The POST response is identical
whether or not the token matched, so it can't enumerate subscribers.

The sandbox banner middleware injects a random per-render element id into HTML
responses on this (sandbox) dev host, which would defeat a byte-for-byte body
comparison. We disable it for these tests so we assert the view's own output.
"""

from unittest import mock

from django.urls import reverse

from email_marketing.models import Subscriber

from .base import MarketingTestCase


class UnsubscribeViewTests(MarketingTestCase):
    def setUp(self):
        # Turn off the sandbox banner injection so responses are the raw view
        # output (otherwise a random sb_<uuid> id defeats body comparison).
        patch = mock.patch("core.sandbox.middleware.is_sandbox_mode", return_value=False)
        patch.start()
        self.addCleanup(patch.stop)

    def _url(self, token):
        return reverse("email_marketing:unsubscribe", args=[token])

    def test_post_with_valid_token_sets_status_unsubscribed(self):
        sub = self.make_anon_emailable("lead@example.com")

        response = self.client.post(self._url(sub.unsubscribe_token))

        self.assertEqual(response.status_code, 200)
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_UNSUBSCRIBED)
        self.assertFalse(sub.marketing_opt_in)

    def test_get_renders_confirmation_without_changing_state(self):
        sub = self.make_anon_emailable("lead@example.com")

        response = self.client.get(self._url(sub.unsubscribe_token))

        self.assertEqual(response.status_code, 200)
        sub.refresh_from_db()
        self.assertEqual(sub.status, Subscriber.STATUS_ACTIVE)  # GET must not opt out

    def test_post_with_unknown_token_returns_200(self):
        response = self.client.post(self._url("totally-made-up-token"))
        self.assertEqual(response.status_code, 200)

    def test_known_and_unknown_tokens_return_identical_bodies(self):
        sub = self.make_anon_emailable("lead@example.com")
        known = self.client.post(self._url(sub.unsubscribe_token))
        unknown = self.client.post(self._url("no-such-token"))

        self.assertEqual(known.status_code, unknown.status_code)
        # Anti-enumeration: byte-identical bodies regardless of token match.
        self.assertEqual(known.content, unknown.content)
