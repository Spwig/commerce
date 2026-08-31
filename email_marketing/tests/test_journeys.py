"""Journey orchestrator: enrollment eligibility + graph walking.

The send path is mocked (it's covered by test_send_path) so these tests isolate
enrollment eligibility and how the orchestrator walks a journey's node graph.
"""

from datetime import timedelta
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


class _JourneyBase(MarketingTestCase):
    def setUp(self):
        super().setUp()
        send_patch = mock.patch(
            "email_marketing.services.campaigns.send_campaign_to_subscriber",
            return_value={"queued": True},
        )
        self.send_mock = send_patch.start()
        self.addCleanup(send_patch.stop)

    def _email(self, name="Step email"):
        return Campaign.objects.create(
            site=self.site, name=name, subject="Hi", message_type="newsletter", html_content="x"
        )

    def _journey(self, trigger=Journey.TRIGGER_SIGNUP, status=Journey.STATUS_ACTIVE, **kw):
        return Journey.objects.create(
            site=self.site, name="Welcome", trigger_event=trigger, status=status, **kw
        )

    def _one_step(self, journey, delay_value=0, unit=JourneyNode.UNIT_DAYS, campaign=None):
        """A minimal enrollable graph: entry → wait → send → exit."""
        return self.build_linear_journey(journey, [(delay_value, unit, campaign or self._email())])


class EnrollmentEligibilityTests(_JourneyBase):
    def test_eligible_subscriber_is_enrolled_at_the_entry_node(self):
        journey = self._journey()
        graph = self._one_step(journey)
        sub = self.make_anon_emailable("a@example.com")

        enrollment = journey_svc.enroll_subscriber(journey, sub)

        self.assertIsNotNone(enrollment)
        self.assertEqual(enrollment.current_node_id, graph["entry"].id)
        self.assertEqual(enrollment.status, JourneyEnrollment.STATUS_ACTIVE)
        journey.refresh_from_db()
        self.assertEqual(journey.enrolled_count, 1)

    def test_journey_without_nodes_does_not_enroll(self):
        journey = self._journey()  # no entry node
        sub = self.make_anon_emailable("b@example.com")
        self.assertIsNone(journey_svc.enroll_subscriber(journey, sub))

    def test_inactive_journey_does_not_enroll(self):
        journey = self._journey(status=Journey.STATUS_PAUSED)
        self._one_step(journey)
        sub = self.make_anon_emailable("c@example.com")
        self.assertIsNone(journey_svc.enroll_subscriber(journey, sub))

    def test_once_per_subscriber_blocks_a_second_enrollment(self):
        journey = self._journey(once_per_subscriber=True)
        self._one_step(journey)
        sub = self.make_anon_emailable("d@example.com")

        self.assertIsNotNone(journey_svc.enroll_subscriber(journey, sub))
        # Complete the first so it's not just the "active" guard blocking.
        JourneyEnrollment.objects.filter(journey=journey, subscriber=sub).update(
            status=JourneyEnrollment.STATUS_COMPLETED
        )
        self.assertIsNone(journey_svc.enroll_subscriber(journey, sub))

    def test_an_active_enrollment_blocks_a_concurrent_one(self):
        journey = self._journey(once_per_subscriber=False)
        self._one_step(journey)
        sub = self.make_anon_emailable("e@example.com")

        self.assertIsNotNone(journey_svc.enroll_subscriber(journey, sub))
        self.assertIsNone(journey_svc.enroll_subscriber(journey, sub))  # already active

    def test_segment_filter_excludes_non_members(self):
        # An empty static segment matches nobody.
        segment = Segment.objects.create(
            site=self.site, name="Nobody", slug="nobody", kind=Segment.KIND_STATIC
        )
        journey = self._journey(target_segment=segment)
        self._one_step(journey)
        sub = self.make_anon_emailable("f@example.com")
        self.assertIsNone(journey_svc.enroll_subscriber(journey, sub))

    def test_unsubscribed_subscriber_is_not_enrolled(self):
        journey = self._journey()
        self._one_step(journey)
        sub = self.make_subscriber("g@example.com", status="unsubscribed")
        self.assertIsNone(journey_svc.enroll_subscriber(journey, sub))


class TriggerEventTests(_JourneyBase):
    def test_only_journeys_bound_to_the_event_enroll(self):
        signup = self._journey(trigger=Journey.TRIGGER_SIGNUP)
        self._one_step(signup)
        order = self._journey(trigger=Journey.TRIGGER_ORDER_PLACED)
        self._one_step(order)
        sub = self.make_anon_emailable("h@example.com")

        count = journey_svc.trigger_event(Journey.TRIGGER_SIGNUP, sub)

        self.assertEqual(count, 1)
        self.assertTrue(JourneyEnrollment.objects.filter(journey=signup, subscriber=sub).exists())
        self.assertFalse(JourneyEnrollment.objects.filter(journey=order, subscriber=sub).exists())


class GraphWalkingTests(_JourneyBase):
    def test_steps_send_and_advance_then_complete(self):
        journey = self._journey()
        graph = self.build_linear_journey(
            journey,
            [
                (0, JourneyNode.UNIT_DAYS, self._email("first")),
                (3, JourneyNode.UNIT_DAYS, self._email("second")),
            ],
        )
        sub = self.make_anon_emailable("i@example.com")
        start = timezone.now()

        journey_svc.enroll_subscriber(journey, sub, now=start)

        # First tick: entry → wait(0) passes through → send first → pause at wait(3d).
        journey_svc.process_due_enrollments(now=start)
        self.assertEqual(self.send_mock.call_count, 1)
        enrollment = JourneyEnrollment.objects.get(journey=journey, subscriber=sub)
        self.assertEqual(enrollment.current_node_id, graph["waits"][1].id)
        self.assertEqual(enrollment.status, JourneyEnrollment.STATUS_ACTIVE)

        # Not yet due 1 day later.
        journey_svc.process_due_enrollments(now=start + timedelta(days=1))
        self.assertEqual(self.send_mock.call_count, 1)

        # Due after 3 days: second email sends → journey completes.
        journey_svc.process_due_enrollments(now=start + timedelta(days=3, minutes=1))
        self.assertEqual(self.send_mock.call_count, 2)
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, JourneyEnrollment.STATUS_COMPLETED)
        journey.refresh_from_db()
        self.assertEqual(journey.completed_count, 1)

    def test_single_step_journey_completes_on_first_tick(self):
        journey = self._journey()
        self._one_step(journey)
        sub = self.make_anon_emailable("j@example.com")
        start = timezone.now()
        journey_svc.enroll_subscriber(journey, sub, now=start)

        journey_svc.process_due_enrollments(now=start)

        self.assertEqual(self.send_mock.call_count, 1)
        enrollment = JourneyEnrollment.objects.get(journey=journey, subscriber=sub)
        self.assertEqual(enrollment.status, JourneyEnrollment.STATUS_COMPLETED)
