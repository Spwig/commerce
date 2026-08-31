"""Journey graph validation + the Activate gate."""

from email_marketing.models import Campaign, Journey, JourneyNode, Segment
from email_marketing.services.journey_validation import can_activate, validate_journey

from .base import MarketingTestCase


class _ValBase(MarketingTestCase):
    def _journey(self, status=Journey.STATUS_DRAFT):
        return Journey.objects.create(
            site=self.site, name="J", trigger_event=Journey.TRIGGER_SIGNUP, status=status
        )

    def _campaign(self):
        return Campaign.objects.create(site=self.site, name="C", subject="s")

    def _segment(self):
        return Segment.objects.create(site=self.site, name="S", slug="s", kind=Segment.KIND_STATIC)

    def _levels(self, issues):
        return {i["level"] for i in issues}

    def _messages(self, issues):
        return " ".join(i["message"] for i in issues)


class ValidateJourneyTests(_ValBase):
    def test_missing_entry_is_an_error(self):
        j = self._journey()  # no nodes at all
        issues = validate_journey(j)
        self.assertFalse(can_activate(issues))
        self.assertIn("no start", self._messages(issues).lower())

    def test_entry_with_no_next_step_is_an_error(self):
        j = self._journey()
        self.add_node(j, JourneyNode.TYPE_ENTRY)
        issues = validate_journey(j)
        self.assertFalse(can_activate(issues))

    def test_send_without_an_email_is_an_error(self):
        j = self._journey()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        send = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL)  # no campaign_id
        self.add_edge(j, entry, send)
        issues = validate_journey(j)
        self.assertFalse(can_activate(issues))
        self.assertIn("no email chosen", self._messages(issues).lower())

    def test_branch_without_segment_or_paths_is_an_error(self):
        j = self._journey()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        branch = self.add_node(j, JourneyNode.TYPE_BRANCH)  # no condition, no edges
        self.add_edge(j, entry, branch)
        issues = validate_journey(j)
        self.assertFalse(can_activate(issues))

    def test_unreachable_node_is_a_warning_not_a_blocker(self):
        j = self._journey()
        c = self._campaign()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        send = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        self.add_edge(j, entry, send)
        # An orphan node with no incoming edge → unreachable warning.
        self.add_node(j, JourneyNode.TYPE_EXIT)
        issues = validate_journey(j)
        self.assertTrue(can_activate(issues))  # warnings don't block
        self.assertIn("warning", self._levels(issues))
        self.assertIn("can't be reached", self._messages(issues).lower())

    def test_deleted_campaign_reference_blocks_activation(self):
        j = self._journey()
        c = self._campaign()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        send = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        self.add_edge(j, entry, send)
        c.delete()  # leaves a stale UUID in the node's config

        issues = validate_journey(j)
        self.assertFalse(can_activate(issues))
        self.assertIn("no longer exists", self._messages(issues).lower())

    def test_deleted_segment_reference_blocks_activation(self):
        j = self._journey()
        c = self._campaign()
        s = self._segment()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        branch = self.add_node(
            j, JourneyNode.TYPE_BRANCH, condition="in_segment", segment_id=str(s.id)
        )
        yes = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        self.add_edge(j, entry, branch)
        self.add_edge(j, branch, yes, branch="yes")
        s.delete()

        issues = validate_journey(j)
        self.assertFalse(can_activate(issues))
        self.assertIn("segment that no longer exists", self._messages(issues).lower())

    def test_a_cycle_blocks_activation(self):
        j = self._journey()
        c = self._campaign()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        a = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        b = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        self.add_edge(j, entry, a)
        self.add_edge(j, a, b)
        self.add_edge(j, b, a)  # loop

        issues = validate_journey(j)
        self.assertFalse(can_activate(issues))
        self.assertIn("loops back", self._messages(issues).lower())

    def test_a_complete_journey_has_no_errors(self):
        j = self._journey()
        c = self._campaign()
        s = self._segment()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        send = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        branch = self.add_node(
            j, JourneyNode.TYPE_BRANCH, condition="in_segment", segment_id=str(s.id)
        )
        yes = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(c.id))
        no = self.add_node(j, JourneyNode.TYPE_EXIT)
        self.add_edge(j, entry, send)
        self.add_edge(j, send, branch)
        self.add_edge(j, branch, yes, branch="yes")
        self.add_edge(j, branch, no, branch="no")
        issues = validate_journey(j)
        self.assertTrue(can_activate(issues))
        self.assertEqual(self._levels(issues) - {"warning"}, set())  # no errors
