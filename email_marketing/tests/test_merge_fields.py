"""Behaviour tests for personalization merge fields.

Merge fields are allowlisted ``[[token]]`` placeholders resolved per recipient by
plain string substitution (no template engine). Values are HTML-escaped in the
body and newline-stripped in the subject header.
"""

from django.contrib.sites.models import Site

from email_marketing.merge_fields import (
    available_merge_fields,
    resolve_merge_fields,
    resolve_preview,
)
from email_marketing.models import Subscriber
from tests.factories import UserFactory

from .base import MarketingTestCase


class MergeFieldTests(MarketingTestCase):
    def _sub(self, **kwargs):
        return Subscriber.objects.create(site=Site.objects.get(pk=1), **kwargs)

    def test_registered_subscriber_first_name_resolves(self):
        user = UserFactory(first_name="Alex", last_name="Rivera")
        sub = self._sub(email=user.email, user=user)
        self.assertEqual(
            resolve_merge_fields("Hi [[first_name]] [[last_name]]", sub), "Hi Alex Rivera"
        )

    def test_anonymous_subscriber_name_is_empty(self):
        sub = self._sub(email="lead@example.com")
        self.assertEqual(resolve_merge_fields("Hi [[first_name]]!", sub), "Hi !")

    def test_email_token_resolves(self):
        sub = self._sub(email="lead@example.com")
        self.assertEqual(resolve_merge_fields("[[email]]", sub), "lead@example.com")

    def test_unknown_token_is_dropped(self):
        sub = self._sub(email="lead@example.com")
        self.assertEqual(resolve_merge_fields("x[[evil]]y", sub), "xy")

    def test_loyalty_points_empty_without_membership(self):
        user = UserFactory(first_name="Sam")
        sub = self._sub(email=user.email, user=user)
        # No LoyaltyMember/balance -> resolver fails safe to empty.
        self.assertEqual(resolve_merge_fields("[[loyalty_points]]", sub), "")

    def test_body_value_is_html_escaped(self):
        user = UserFactory(first_name="<img src=x onerror=alert(1)>")
        sub = self._sub(email=user.email, user=user)
        out = resolve_merge_fields("[[first_name]]", sub, html=True)
        self.assertNotIn("<img", out)
        self.assertIn("&lt;img", out)

    def test_subject_context_strips_newlines(self):
        user = UserFactory(first_name="Ann\r\nBcc: attacker@evil.com")
        sub = self._sub(email=user.email, user=user)
        out = resolve_merge_fields("Hi [[first_name]]", sub, html=False)
        self.assertNotIn("\n", out)
        self.assertNotIn("\r", out)

    def test_preview_wraps_sample_value(self):
        out = resolve_preview("Hi [[first_name]]")
        self.assertIn('<span class="em-merge">Alex</span>', out)

    def test_available_merge_fields_lists_keys_and_labels(self):
        fields = available_merge_fields()
        keys = {f["key"] for f in fields}
        self.assertIn("first_name", keys)
        self.assertIn("unsubscribe_url", keys)
        self.assertTrue(all("label" in f for f in fields))
