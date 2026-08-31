"""Back-in-stock journey bridge (Stage 3).

When a merchant has built and activated a back-in-stock journey, the catalog
restock notifier defers to it (a richer, merchant-designed sequence) instead of
sending its own one-off transactional email — no double-send. If enrollment
can't happen for any reason, the catalog email still goes out so an explicitly
requested alert is never dropped. Also covers the Featured Product block falling
back to the triggering event's product so the journey email shows the restocked
item.
"""

from unittest import mock

from email_marketing import block_context
from email_marketing.models import Journey, JourneyEnrollment, JourneyNode
from email_marketing.services import journeys as journeys_svc

from .base import MarketingTestCase


class _JBase(MarketingTestCase):
    def _journey(self, **kw):
        kw.setdefault("trigger_event", Journey.TRIGGER_BACK_IN_STOCK)
        kw.setdefault("status", Journey.STATUS_ACTIVE)
        kw.setdefault("once_per_subscriber", False)
        journey = Journey.objects.create(site=self.site, name="Restock", **kw)
        self.add_node(journey, JourneyNode.TYPE_ENTRY)
        return journey


class BridgeUnitTests(_JBase):
    def test_journey_active_flag(self):
        self.assertFalse(journeys_svc.back_in_stock_journey_active())
        self._journey()
        self.assertTrue(journeys_svc.back_in_stock_journey_active())

    def test_enroll_returns_false_without_journey(self):
        from tests.factories import ProductFactory

        product = ProductFactory()
        self.assertFalse(journeys_svc.enroll_back_in_stock("a@example.com", product=product))
        self.assertEqual(JourneyEnrollment.objects.count(), 0)

    def test_enroll_creates_enrollment_with_event_context(self):
        from tests.factories import ProductFactory

        self._journey()
        self.make_anon_emailable("b@example.com")  # opted-in → journey can reach them
        product = ProductFactory()
        self.assertTrue(journeys_svc.enroll_back_in_stock("b@example.com", product=product))
        e = JourneyEnrollment.objects.get(subscriber__email="b@example.com")
        self.assertEqual(e.context, {"product_id": product.id, "variant_id": None})
        self.assertTrue(e.trigger_ref.startswith(f"stock:{product.id}:0:"))

    def test_enroll_is_deduped_per_recipient(self):
        from tests.factories import ProductFactory

        self._journey()
        self.make_anon_emailable("c@example.com")
        product = ProductFactory()
        self.assertTrue(journeys_svc.enroll_back_in_stock("c@example.com", product=product))
        self.assertFalse(journeys_svc.enroll_back_in_stock("c@example.com", product=product))
        self.assertEqual(
            JourneyEnrollment.objects.filter(
                subscriber__email="c@example.com", status=JourneyEnrollment.STATUS_ACTIVE
            ).count(),
            1,
        )

    def test_enroll_declines_a_non_emailable_recipient(self):
        # A requester the journey can't reach (e.g. a guest who never opted into
        # marketing) must NOT be taken over — enroll returns False so the caller
        # sends its guaranteed one-off alert instead. Nothing is enrolled.
        from tests.factories import ProductFactory

        self._journey()
        product = ProductFactory()
        self.assertFalse(
            journeys_svc.enroll_back_in_stock("guest-nooptin@example.com", product=product)
        )
        self.assertEqual(JourneyEnrollment.objects.count(), 0)

    def test_featured_product_falls_back_to_event_product(self):
        from tests.factories import ProductFactory

        product = ProductFactory()
        ctx = block_context.featured_product_context({}, {"event": {"product_id": product.id}})
        self.assertIsNotNone(ctx["product"])
        self.assertEqual(ctx["product"]["name"], product.name)

    def test_featured_product_config_id_still_wins(self):
        from tests.factories import ProductFactory

        configured = ProductFactory()
        event_product = ProductFactory()
        ctx = block_context.featured_product_context(
            {"product_id": configured.id}, {"event": {"product_id": event_product.id}}
        )
        self.assertEqual(ctx["product"]["name"], configured.name)


class CatalogBridgeIntegrationTests(_JBase):
    def _stock_and_notif(self, email):
        from catalog.models import StockNotification
        from tests.factories import StockItemFactory

        item = StockItemFactory()  # on_hand 50 → available > 0
        StockNotification.objects.create(email=email, product=item.product)
        return item

    @mock.patch("catalog.tasks._send_back_in_stock_email")
    def test_active_journey_routes_and_suppresses_the_oneoff_email(self, mock_email):
        from catalog.tasks import send_back_in_stock_notifications

        self._journey()
        self.make_anon_emailable("waiting@example.com")  # opted-in → journey can reach them
        item = self._stock_and_notif("waiting@example.com")
        sent = send_back_in_stock_notifications(item.id)
        self.assertEqual(sent, 1)
        mock_email.assert_not_called()  # journey owns the notification
        self.assertTrue(
            JourneyEnrollment.objects.filter(subscriber__email="waiting@example.com").exists()
        )
        from catalog.models import StockNotification

        self.assertIsNotNone(StockNotification.objects.get(email="waiting@example.com").notified_at)

    @mock.patch("catalog.tasks._send_back_in_stock_email")
    def test_non_emailable_requester_still_gets_the_oneoff_alert(self, mock_email):
        # Regression: with a back-in-stock journey active, a requester the journey
        # can't reach (guest who never opted into marketing) must still receive the
        # one-off transactional alert — not be silently dropped. No enrollment.
        from catalog.tasks import send_back_in_stock_notifications

        self._journey()
        item = self._stock_and_notif("guest-nooptin@example.com")
        sent = send_back_in_stock_notifications(item.id)
        self.assertEqual(sent, 1)
        mock_email.assert_called_once()  # guaranteed alert preserved
        self.assertEqual(JourneyEnrollment.objects.count(), 0)

    @mock.patch("catalog.tasks._send_back_in_stock_email")
    def test_no_journey_sends_the_oneoff_email(self, mock_email):
        from catalog.tasks import send_back_in_stock_notifications

        item = self._stock_and_notif("plain@example.com")
        sent = send_back_in_stock_notifications(item.id)
        self.assertEqual(sent, 1)
        mock_email.assert_called_once()
        self.assertEqual(JourneyEnrollment.objects.count(), 0)

    @mock.patch("catalog.tasks._send_back_in_stock_email")
    def test_enroll_failure_falls_back_to_the_oneoff_email(self, mock_email):
        from catalog.tasks import send_back_in_stock_notifications

        self._journey()
        item = self._stock_and_notif("fallback@example.com")
        with mock.patch(
            "email_marketing.services.journeys.enroll_back_in_stock", return_value=False
        ):
            sent = send_back_in_stock_notifications(item.id)
        self.assertEqual(sent, 1)
        mock_email.assert_called_once()  # enrollment declined → requested alert still sent
