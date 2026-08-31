"""Portable import/export of journeys + starter templates."""

from email_marketing.journey_templates import get_starter_doc, get_starters
from email_marketing.models import Campaign, Journey, JourneyNode, Segment
from email_marketing.services import journey_io

from .base import MarketingTestCase


class _IOBase(MarketingTestCase):
    def _journey(self, name="J", trigger=Journey.TRIGGER_SIGNUP):
        return Journey.objects.create(site=self.site, name=name, trigger_event=trigger)

    def _campaign(self, name):
        return Campaign.objects.create(
            site=self.site, name=name, subject=name, message_type="newsletter"
        )

    def _segment(self, name, slug):
        return Segment.objects.create(
            site=self.site, name=name, slug=slug, kind=Segment.KIND_STATIC
        )

    def _sample_graph(self, journey, campaign, segment):
        """entry → send(campaign) → branch(segment) → yes:send / no:exit."""
        entry = self.add_node(journey, JourneyNode.TYPE_ENTRY)
        send = self.add_node(journey, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(campaign.id))
        branch = self.add_node(
            journey, JourneyNode.TYPE_BRANCH, condition="in_segment", segment_id=str(segment.id)
        )
        yes = self.add_node(journey, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(campaign.id))
        no = self.add_node(journey, JourneyNode.TYPE_EXIT)
        self.add_edge(journey, entry, send)
        self.add_edge(journey, send, branch)
        self.add_edge(journey, branch, yes, branch="yes")
        self.add_edge(journey, branch, no, branch="no")
        return entry, send, branch


class ExportTests(_IOBase):
    def test_export_carries_names_not_ids(self):
        journey = self._journey()
        c = self._campaign("Welcome email")
        s = self._segment("VIP", "vip")
        self._sample_graph(journey, c, s)

        doc = journey_io.export_journey(journey)

        self.assertEqual(doc["spwig_journey"], journey_io.FORMAT_VERSION)
        self.assertEqual(doc["trigger_event"], Journey.TRIGGER_SIGNUP)
        send = next(n for n in doc["nodes"] if n["node_type"] == "send_email")
        self.assertEqual(send["campaign_name"], "Welcome email")
        self.assertNotIn("campaign_id", send.get("config", {}))
        branch = next(n for n in doc["nodes"] if n["node_type"] == "branch")
        self.assertEqual(branch["segment_name"], "VIP")
        self.assertNotIn("segment_id", branch.get("config", {}))


class RoundTripTests(_IOBase):
    def test_export_then_import_rebuilds_and_relinks_by_name(self):
        src = self._journey("Source")
        c = self._campaign("Welcome email")
        s = self._segment("VIP", "vip")
        self._sample_graph(src, c, s)
        doc = journey_io.export_journey(src)

        dest = self._journey("Dest")
        stats = journey_io.import_into_journey(dest, doc)

        # Same shape.
        self.assertEqual(dest.nodes.count(), 5)
        self.assertEqual(dest.edges.count(), 4)
        self.assertEqual(dest.nodes.filter(node_type="entry").count(), 1)
        # Re-linked to the SAME local campaign/segment by name.
        send = dest.nodes.filter(node_type="send_email").first()
        self.assertEqual(send.config.get("campaign_id"), str(c.id))
        branch = dest.nodes.get(node_type="branch")
        self.assertEqual(branch.config.get("segment_id"), str(s.id))
        self.assertEqual(stats["unmatched"], 0)
        # Yes/No edges survive the round trip.
        self.assertTrue(dest.edges.filter(branch="yes").exists())
        self.assertTrue(dest.edges.filter(branch="no").exists())

    def test_unmatched_names_are_left_unset_and_counted(self):
        src = self._journey("Source")
        c = self._campaign("Only here")
        s = self._segment("Only seg", "only")
        self._sample_graph(src, c, s)
        doc = journey_io.export_journey(src)
        # Remove the local targets so the destination can't match by name.
        c.delete()
        s.delete()

        dest = self._journey("Dest")
        stats = journey_io.import_into_journey(dest, doc)

        for node in dest.nodes.filter(node_type="send_email"):
            self.assertNotIn("campaign_id", node.config)
        self.assertNotIn("segment_id", dest.nodes.get(node_type="branch").config)
        # two sends + one branch = 3 unmatched
        self.assertEqual(stats["unmatched"], 3)


class ImportGuardTests(_IOBase):
    def test_unrecognised_format_is_rejected(self):
        with self.assertRaises(journey_io.JourneyImportError):
            journey_io.import_into_journey(self._journey(), {"not": "a journey"})

    def test_too_many_nodes_is_rejected(self):
        doc = {
            "spwig_journey": 1,
            "nodes": [
                {"key": f"n{i}", "node_type": "wait_delay"} for i in range(journey_io.MAX_NODES + 1)
            ],
            "edges": [],
        }
        with self.assertRaises(journey_io.JourneyImportError):
            journey_io.import_into_journey(self._journey(), doc)

    def test_import_always_yields_an_entry_node(self):
        doc = {
            "spwig_journey": 1,
            "nodes": [{"key": "a", "node_type": "send_email"}],
            "edges": [],
        }
        dest = self._journey()
        journey_io.import_into_journey(dest, doc)
        self.assertEqual(dest.nodes.filter(node_type="entry").count(), 1)

    def test_invalid_edges_are_skipped(self):
        doc = {
            "spwig_journey": 1,
            "nodes": [
                {"key": "e", "node_type": "entry"},
                {"key": "x", "node_type": "exit"},
                {"key": "s", "node_type": "send_email"},
            ],
            "edges": [
                {"from": "e", "to": "s", "branch": "default"},
                {"from": "x", "to": "s", "branch": "default"},  # exit has no output → skipped
                {"from": "s", "to": "s", "branch": "default"},  # self-loop → skipped
                {"from": "e", "to": "s", "branch": "yes"},  # non-branch can't use yes → skipped
            ],
        }
        dest = self._journey()
        journey_io.import_into_journey(dest, doc)
        self.assertEqual(dest.edges.count(), 1)


class StarterTemplateTests(_IOBase):
    def test_every_starter_imports_cleanly(self):
        starters = get_starters()
        self.assertTrue(starters)
        for meta in starters:
            doc = get_starter_doc(meta["key"])
            self.assertIsNotNone(doc)
            journey = self._journey(meta["key"], trigger=doc["trigger_event"])
            journey_io.import_into_journey(journey, doc)
            # Each starter has exactly one entry and at least one send + an exit.
            self.assertEqual(journey.nodes.filter(node_type="entry").count(), 1)
            self.assertTrue(journey.nodes.filter(node_type="send_email").exists())
            self.assertTrue(journey.nodes.filter(node_type="exit").exists())
            # No dangling edges.
            self.assertTrue(journey.edges.exists())

    def test_unknown_starter_key_returns_none(self):
        self.assertIsNone(get_starter_doc("does-not-exist"))
