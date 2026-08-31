"""Starter journeys expose the expanded trigger set so merchants can discover them."""

from django.test import SimpleTestCase

from email_marketing.journey_templates import get_starter_doc, get_starters
from email_marketing.models import Journey


class JourneyStartersTests(SimpleTestCase):
    def test_starters_cover_the_new_triggers(self):
        triggers = {s["trigger_event"] for s in get_starters()}
        for expected in (
            Journey.TRIGGER_CART_ABANDONED,
            Journey.TRIGGER_WIN_BACK,
            Journey.TRIGGER_ORDER_DELIVERED,
            Journey.TRIGGER_BACK_IN_STOCK,
        ):
            self.assertIn(expected, triggers)

    def test_each_starter_doc_matches_its_declared_trigger(self):
        for s in get_starters():
            doc = get_starter_doc(s["key"])
            self.assertIsNotNone(doc)
            self.assertEqual(doc["trigger_event"], s["trigger_event"])
            # Every starter graph has an entry and an exit node.
            node_types = {n["node_type"] for n in doc["nodes"]}
            self.assertIn("entry", node_types)
            self.assertIn("exit", node_types)

    def test_every_starter_trigger_is_a_valid_choice(self):
        valid = {value for value, _ in Journey.TRIGGER_CHOICES}
        for s in get_starters():
            self.assertIn(s["trigger_event"], valid)
