"""Win-back (lapsed-customer scan) + post-purchase review (delivered transition) triggers."""

from datetime import timedelta

from django.test import override_settings
from django.utils import timezone

from email_marketing.models import Journey, JourneyEnrollment, JourneyNode
from email_marketing.tasks import detect_lapsed_customers

from .base import MarketingTestCase


class _JBase(MarketingTestCase):
    def _journey(self, trigger, **kw):
        kw.setdefault("status", Journey.STATUS_ACTIVE)
        kw.setdefault("once_per_subscriber", False)
        journey = Journey.objects.create(site=self.site, name="J", trigger_event=trigger, **kw)
        self.add_node(journey, JourneyNode.TYPE_ENTRY)
        return journey


class WinBackTests(_JBase):
    def _lapsed(self, email, days_ago):
        from customers.models import CustomerMetrics
        from tests.factories import UserFactory

        user = UserFactory(email=email)
        CustomerMetrics.objects.update_or_create(
            user=user,
            defaults={
                "last_purchase_date": timezone.now() - timedelta(days=days_ago),
                "probability_alive": 1.0,
            },
        )
        return user

    @override_settings(WIN_BACK_AFTER_DAYS=90, WIN_BACK_MAX_AGE_DAYS=365)
    def test_noop_without_active_journey(self):
        self._lapsed("a@example.com", 120)
        self.assertEqual(detect_lapsed_customers()["enrolled"], 0)

    @override_settings(WIN_BACK_AFTER_DAYS=90, WIN_BACK_MAX_AGE_DAYS=365)
    def test_enrolls_a_lapsed_customer(self):
        self._journey(Journey.TRIGGER_WIN_BACK)
        user = self._lapsed("lapsed@example.com", 120)
        self.assertEqual(detect_lapsed_customers()["enrolled"], 1)
        self.assertTrue(JourneyEnrollment.objects.filter(trigger_ref=f"winback:{user.id}").exists())

    @override_settings(WIN_BACK_AFTER_DAYS=90, WIN_BACK_MAX_AGE_DAYS=365)
    def test_skips_a_recent_purchaser(self):
        self._journey(Journey.TRIGGER_WIN_BACK)
        self._lapsed("recent@example.com", 30)
        self.assertEqual(detect_lapsed_customers()["enrolled"], 0)

    @override_settings(WIN_BACK_AFTER_DAYS=90, WIN_BACK_MAX_AGE_DAYS=365)
    def test_skips_an_ancient_customer(self):
        self._journey(Journey.TRIGGER_WIN_BACK)
        self._lapsed("ancient@example.com", 500)  # beyond the max-age floor
        self.assertEqual(detect_lapsed_customers()["enrolled"], 0)

    @override_settings(WIN_BACK_AFTER_DAYS=90, WIN_BACK_MAX_AGE_DAYS=365)
    def test_does_not_re_win_back_within_the_window(self):
        self._journey(Journey.TRIGGER_WIN_BACK)
        self._lapsed("dup@example.com", 120)
        self.assertEqual(detect_lapsed_customers()["enrolled"], 1)
        self.assertEqual(detect_lapsed_customers()["enrolled"], 0)  # recent enrollment excludes

    @override_settings(WIN_BACK_AFTER_DAYS=90, WIN_BACK_MAX_AGE_DAYS=365, WIN_BACK_BATCH=1)
    def test_once_per_subscriber_old_enrollment_does_not_starve_the_batch(self):
        # A customer whose only win-back enrolment is old enough to clear the fixed
        # WIN_BACK_AFTER_DAYS window but who a once_per_subscriber journey will never
        # re-enroll must be excluded at the DB level — otherwise (ordered oldest-first,
        # batch=1) they occupy the only slot every tick and a freshly-lapsed customer
        # never gets processed.
        self._journey(Journey.TRIGGER_WIN_BACK, once_per_subscriber=True)
        old = self._lapsed("stale@example.com", 200)  # oldest purchase → sorted first
        # Give `old` a completed win-back enrolment that predates the dedup window.
        self.assertEqual(detect_lapsed_customers()["enrolled"], 1)
        enr = JourneyEnrollment.objects.get(trigger_ref=f"winback:{old.id}")
        enr.status = JourneyEnrollment.STATUS_COMPLETED
        enr.save(update_fields=["status"])
        JourneyEnrollment.objects.filter(pk=enr.pk).update(
            started_at=timezone.now() - timedelta(days=150)
        )
        fresh = self._lapsed("fresh@example.com", 100)  # newly lapsed, never won back
        res = detect_lapsed_customers()
        self.assertEqual(res["enrolled"], 1)  # the batch slot reaches `fresh`, not `old`
        self.assertTrue(
            JourneyEnrollment.objects.filter(trigger_ref=f"winback:{fresh.id}").exists()
        )


class OrderDeliveredTests(_JBase):
    def _order(self, **kw):
        from tests.factories import OrderFactory

        return OrderFactory(**kw)

    def test_delivered_transition_enrolls(self):
        self._journey(Journey.TRIGGER_ORDER_DELIVERED)
        order = self._order(status="processing", email="buyer@example.com")
        order.status = "delivered"
        order.save()
        self.assertTrue(JourneyEnrollment.objects.filter(trigger_ref=f"order:{order.id}").exists())

    def test_noop_without_active_journey(self):
        order = self._order(status="processing", email="x@example.com")
        order.status = "delivered"
        order.save()
        self.assertFalse(JourneyEnrollment.objects.filter(trigger_ref=f"order:{order.id}").exists())

    def test_resave_of_a_delivered_order_does_not_reenroll(self):
        self._journey(Journey.TRIGGER_ORDER_DELIVERED)
        order = self._order(status="processing", email="b@example.com")
        order.status = "delivered"
        order.save()
        first = JourneyEnrollment.objects.filter(trigger_ref=f"order:{order.id}").count()
        order.save()  # already delivered → not a transition → no re-enroll
        self.assertEqual(first, 1)
        self.assertEqual(
            JourneyEnrollment.objects.filter(trigger_ref=f"order:{order.id}").count(), 1
        )
