"""Lifecycle signals enroll subscribers into triggered journeys."""

from email_marketing.models import (
    Campaign,
    Journey,
    JourneyEnrollment,
    JourneyNode,
    Subscriber,
)
from tests.factories import OrderFactory, UserFactory

from .base import MarketingTestCase


class _SignalBase(MarketingTestCase):
    def _email(self):
        return Campaign.objects.create(
            site=self.site, name="Email", subject="Hi", message_type="newsletter", html_content="x"
        )

    def _journey(self, trigger):
        journey = Journey.objects.create(
            site=self.site,
            name=f"J-{trigger}",
            trigger_event=trigger,
            status=Journey.STATUS_ACTIVE,
        )
        # A minimal enrollable graph: entry → send → exit.
        entry = self.add_node(journey, JourneyNode.TYPE_ENTRY)
        send = self.add_node(
            journey, JourneyNode.TYPE_SEND_EMAIL, campaign_id=str(self._email().id)
        )
        exit_node = self.add_node(journey, JourneyNode.TYPE_EXIT)
        self.add_edge(journey, entry, send)
        self.add_edge(journey, send, exit_node)
        return journey


class SignupSignalTests(_SignalBase):
    def test_new_customer_is_enrolled_in_a_signup_journey(self):
        journey = self._journey(Journey.TRIGGER_SIGNUP)

        UserFactory(email="new@example.com")  # fires the signup signal

        sub = Subscriber.objects.get(email="new@example.com")
        self.assertTrue(JourneyEnrollment.objects.filter(journey=journey, subscriber=sub).exists())

    def test_staff_user_is_not_enrolled(self):
        journey = self._journey(Journey.TRIGGER_SIGNUP)
        UserFactory(email="staff@example.com", staff=True)
        self.assertFalse(JourneyEnrollment.objects.filter(journey=journey).exists())


class OrderSignalTests(_SignalBase):
    def test_order_enrolls_the_buyer_in_an_order_placed_journey(self):
        journey = self._journey(Journey.TRIGGER_ORDER_PLACED)

        OrderFactory(email="buyer@example.com", user=None)

        sub = Subscriber.objects.get(email="buyer@example.com")
        self.assertTrue(JourneyEnrollment.objects.filter(journey=journey, subscriber=sub).exists())

    def test_first_order_also_enrolls_in_a_first_order_journey(self):
        first_journey = self._journey(Journey.TRIGGER_FIRST_ORDER)

        OrderFactory(email="firsttimer@example.com", user=None)

        sub = Subscriber.objects.get(email="firsttimer@example.com")
        self.assertTrue(
            JourneyEnrollment.objects.filter(journey=first_journey, subscriber=sub).exists()
        )


class NoJourneyNoOpTests(_SignalBase):
    """With no journey listening, the signals must not create marketing rows."""

    def test_signup_without_a_journey_creates_no_subscriber(self):
        UserFactory(email="lonely@example.com")
        self.assertFalse(Subscriber.objects.filter(email="lonely@example.com").exists())

    def test_order_without_a_journey_creates_no_subscriber(self):
        OrderFactory(email="lonelybuyer@example.com", user=None)
        self.assertFalse(Subscriber.objects.filter(email="lonelybuyer@example.com").exists())
