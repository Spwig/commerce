"""P2 audiences: customer sync + rule-field schema."""

from django.core.management import call_command

from email_marketing.models import Subscriber
from email_marketing.services.segmentation import available_rule_fields
from tests.factories import UserFactory

from .base import MarketingTestCase


class SyncSubscribersCommandTests(MarketingTestCase):
    def test_creates_a_subscriber_per_active_customer(self):
        u1 = UserFactory(email="cust1@example.com")
        u2 = UserFactory(email="cust2@example.com")

        call_command("sync_subscribers")

        self.assertTrue(Subscriber.objects.filter(email="cust1@example.com", user=u1).exists())
        self.assertTrue(Subscriber.objects.filter(email="cust2@example.com", user=u2).exists())

    def test_excludes_staff_by_default(self):
        UserFactory(email="staffer@example.com", staff=True)  # staff trait
        call_command("sync_subscribers")
        self.assertFalse(Subscriber.objects.filter(email="staffer@example.com").exists())

    def test_is_idempotent(self):
        UserFactory(email="once@example.com")
        call_command("sync_subscribers")
        n = Subscriber.objects.count()
        call_command("sync_subscribers")
        self.assertEqual(Subscriber.objects.count(), n)


class RuleFieldSchemaTests(MarketingTestCase):
    def test_schema_exposes_expected_fields_and_shapes(self):
        fields = available_rule_fields()
        by_key = {f["key"]: f for f in fields}
        for key in ("total_spent", "total_orders", "has_orders", "language", "source"):
            self.assertIn(key, by_key)
        # number fields carry comparison operators; booleans carry is_true only.
        self.assertIn("gte", by_key["total_spent"]["operators"])
        self.assertEqual(by_key["has_orders"]["operators"], ["is_true"])
        # select fields carry options.
        self.assertTrue(by_key["source"]["options"])
