"""Journey graph engine: branching, exit nodes, and the cycle guard.

These exercise the graph-walking behaviour that the old linear step model could
not express. The send path is mocked to isolate routing from delivery.
"""

from unittest import mock

from django.utils import timezone

from email_marketing.models import (
    Campaign,
    Journey,
    JourneyEnrollment,
    JourneyNode,
    Segment,
)
from email_marketing.services import journeys as journey_svc

from .base import MarketingTestCase


class _GraphBase(MarketingTestCase):
    def setUp(self):
        super().setUp()
        send_patch = mock.patch(
            "email_marketing.services.campaigns.send_campaign_to_subscriber",
            return_value={"queued": True},
        )
        self.send_mock = send_patch.start()
        self.addCleanup(send_patch.stop)

    def _email(self, name):
        return Campaign.objects.create(
            site=self.site, name=name, subject="Hi", message_type="newsletter", html_content="x"
        )

    def _journey(self, **kw):
        kw.setdefault("trigger_event", Journey.TRIGGER_SIGNUP)
        kw.setdefault("status", Journey.STATUS_ACTIVE)
        return Journey.objects.create(site=self.site, name="J", **kw)

    def _static_segment_with(self, *subscribers):
        seg = Segment.objects.create(
            site=self.site, name="Members", slug="members", kind=Segment.KIND_STATIC
        )
        for sub in subscribers:
            seg.members.add(sub)
        return seg


class BranchRoutingTests(_GraphBase):
    def _build_branch_journey(self, segment):
        """entry → branch(in segment?) → yes: send A / no: send B → exit."""
        j = self._journey()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        branch = self.add_node(
            j,
            JourneyNode.TYPE_BRANCH,
            condition=JourneyNode.CONDITION_IN_SEGMENT,
            segment_id=str(segment.id),
        )
        yes = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(self._email("yes").id))
        no = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(self._email("no").id))
        end = self.add_node(j, JourneyNode.TYPE_EXIT)
        self.add_edge(j, entry, branch)
        self.add_edge(j, branch, yes, branch="yes")
        self.add_edge(j, branch, no, branch="no")
        self.add_edge(j, yes, end)
        self.add_edge(j, no, end)
        return j, {"yes": yes, "no": no}

    def test_member_takes_the_yes_path(self):
        member = self.make_anon_emailable("member@example.com")
        segment = self._static_segment_with(member)
        journey, nodes = self._build_branch_journey(segment)
        start = timezone.now()

        journey_svc.enroll_subscriber(journey, member, now=start)
        journey_svc.process_due_enrollments(now=start)

        self.assertEqual(self.send_mock.call_count, 1)
        sent_campaign = self.send_mock.call_args[0][0]
        self.assertEqual(str(sent_campaign.id), nodes["yes"].config["campaign_id"])
        enrollment = JourneyEnrollment.objects.get(journey=journey, subscriber=member)
        self.assertEqual(enrollment.status, JourneyEnrollment.STATUS_COMPLETED)

    def test_non_member_takes_the_no_path(self):
        outsider = self.make_anon_emailable("out@example.com")
        segment = self._static_segment_with()  # empty
        journey, nodes = self._build_branch_journey(segment)
        start = timezone.now()

        journey_svc.enroll_subscriber(journey, outsider, now=start)
        journey_svc.process_due_enrollments(now=start)

        self.assertEqual(self.send_mock.call_count, 1)
        sent_campaign = self.send_mock.call_args[0][0]
        self.assertEqual(str(sent_campaign.id), nodes["no"].config["campaign_id"])

    def test_unconfigured_branch_fails_closed_to_no(self):
        sub = self.make_anon_emailable("x@example.com")
        j = self._journey()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        branch = self.add_node(j, JourneyNode.TYPE_BRANCH)  # no condition
        no = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(self._email("no").id))
        end = self.add_node(j, JourneyNode.TYPE_EXIT)
        self.add_edge(j, entry, branch)
        self.add_edge(j, branch, no, branch="no")
        self.add_edge(j, no, end)
        start = timezone.now()

        journey_svc.enroll_subscriber(j, sub, now=start)
        journey_svc.process_due_enrollments(now=start)

        self.assertEqual(self.send_mock.call_count, 1)  # took the No edge


class ExitAndTerminationTests(_GraphBase):
    def test_node_with_no_outgoing_edge_completes(self):
        sub = self.make_anon_emailable("t@example.com")
        j = self._journey()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        send = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(self._email("s").id))
        self.add_edge(j, entry, send)  # send has no outgoing edge → ends here
        start = timezone.now()

        journey_svc.enroll_subscriber(j, sub, now=start)
        journey_svc.process_due_enrollments(now=start)

        self.assertEqual(self.send_mock.call_count, 1)
        enrollment = JourneyEnrollment.objects.get(journey=j, subscriber=sub)
        self.assertEqual(enrollment.status, JourneyEnrollment.STATUS_COMPLETED)

    def test_explicit_exit_node_completes_without_sending(self):
        sub = self.make_anon_emailable("e2@example.com")
        j = self._journey()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        end = self.add_node(j, JourneyNode.TYPE_EXIT)
        self.add_edge(j, entry, end)
        start = timezone.now()

        journey_svc.enroll_subscriber(j, sub, now=start)
        journey_svc.process_due_enrollments(now=start)

        self.assertEqual(self.send_mock.call_count, 0)
        enrollment = JourneyEnrollment.objects.get(journey=j, subscriber=sub)
        self.assertEqual(enrollment.status, JourneyEnrollment.STATUS_COMPLETED)


class CycleGuardTests(_GraphBase):
    def test_a_cycle_does_not_loop_forever(self):
        # entry → A → B → A … a branchless cycle. The hop cap must stop it.
        sub = self.make_anon_emailable("loop@example.com")
        j = self._journey()
        entry = self.add_node(j, JourneyNode.TYPE_ENTRY)
        a = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(self._email("a").id))
        b = self.add_node(j, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(self._email("b").id))
        self.add_edge(j, entry, a)
        self.add_edge(j, a, b)
        self.add_edge(j, b, a)
        start = timezone.now()

        journey_svc.enroll_subscriber(j, sub, now=start)
        # Must return rather than hang; the cap bounds the number of sends.
        journey_svc.process_due_enrollments(now=start)

        self.assertLessEqual(self.send_mock.call_count, journey_svc.MAX_HOPS_PER_TICK)

        # And the enrollment must be parked (cancelled), not left due — otherwise
        # the next beat would reprocess it and resend up to the cap again.
        enr = JourneyEnrollment.objects.get(journey=j, subscriber=sub)
        self.assertEqual(enr.status, JourneyEnrollment.STATUS_CANCELLED)
        before = self.send_mock.call_count
        journey_svc.process_due_enrollments(now=start)  # a later beat
        self.assertEqual(self.send_mock.call_count, before)  # no further sends
