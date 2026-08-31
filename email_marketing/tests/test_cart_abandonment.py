"""Cart-abandonment trigger + the reusable event-context journey framework (Stage 1).

Covers: trigger_event carrying context/trigger_ref onto an enrollment, per-instance
dedup, cancel_enrollments, the detect_abandoned_carts scan beat (idle threshold, guest
email, no-op without an active journey), the CartItem→Cart activity touch, and the
abandoned-cart block context provider.
"""

from datetime import timedelta

from django.test import override_settings
from django.utils import timezone

from email_marketing import block_context
from email_marketing.models import Journey, JourneyEnrollment, JourneyNode
from email_marketing.services import journeys as journeys_svc
from email_marketing.tasks import detect_abandoned_carts

from .base import MarketingTestCase


class _JourneyBase(MarketingTestCase):
    def _cart_journey(self, **kw):
        kw.setdefault("trigger_event", Journey.TRIGGER_CART_ABANDONED)
        kw.setdefault("status", Journey.STATUS_ACTIVE)
        kw.setdefault("once_per_subscriber", False)
        journey = Journey.objects.create(site=self.site, name="Recover", **kw)
        self.add_node(journey, JourneyNode.TYPE_ENTRY)
        return journey


class TriggerFrameworkTests(_JourneyBase):
    def test_trigger_event_stores_context_and_ref(self):
        journey = self._cart_journey()
        sub = self.make_anon_emailable("a@example.com")
        n = journeys_svc.trigger_event(
            Journey.TRIGGER_CART_ABANDONED, sub, context={"cart_id": 7}, trigger_ref="cart:7"
        )
        self.assertEqual(n, 1)
        e = JourneyEnrollment.objects.get(journey=journey, subscriber=sub)
        self.assertEqual(e.context, {"cart_id": 7})
        self.assertEqual(e.trigger_ref, "cart:7")

    def test_active_enrollment_dedups_reenrollment(self):
        journey = self._cart_journey()
        sub = self.make_anon_emailable("b@example.com")
        for _ in range(2):
            journeys_svc.trigger_event(
                Journey.TRIGGER_CART_ABANDONED, sub, context={"cart_id": 1}, trigger_ref="cart:1"
            )
        self.assertEqual(
            JourneyEnrollment.objects.filter(
                journey=journey, subscriber=sub, status=JourneyEnrollment.STATUS_ACTIVE
            ).count(),
            1,
        )

    def test_cancel_enrollments_by_ref(self):
        journey = self._cart_journey()
        sub = self.make_anon_emailable("c@example.com")
        journeys_svc.trigger_event(Journey.TRIGGER_CART_ABANDONED, sub, trigger_ref="cart:9")
        n = journeys_svc.cancel_enrollments(self.site, "cart:9", reason="converted")
        self.assertEqual(n, 1)
        e = JourneyEnrollment.objects.get(journey=journey, subscriber=sub)
        self.assertEqual(e.status, JourneyEnrollment.STATUS_CANCELLED)


class CartDetectionTests(_JourneyBase):
    def _idle_cart(self, *, user=None, email=None, minutes=120):
        from cart.models import Cart
        from tests.factories import CartFactory, CartItemFactory, ProductFactory, UserFactory

        if user is None and email:
            user = UserFactory(email=email)
        cart = CartFactory(user=user)
        CartItemFactory(cart=cart, product=ProductFactory())
        # Backdate last activity so it clears the idle threshold.
        Cart.objects.filter(pk=cart.pk).update(
            updated_at=timezone.now() - timedelta(minutes=minutes)
        )
        return cart

    def test_detect_is_noop_without_an_active_journey(self):
        self._idle_cart(email="x@example.com")
        self.assertEqual(detect_abandoned_carts()["enrolled"], 0)

    @override_settings(CART_ABANDONED_AFTER_MINUTES=60)
    def test_detect_enrolls_an_idle_cart(self):
        self._cart_journey()
        cart = self._idle_cart(email="buyer@example.com", minutes=120)
        res = detect_abandoned_carts()
        self.assertEqual(res["enrolled"], 1)
        self.assertTrue(JourneyEnrollment.objects.filter(trigger_ref=f"cart:{cart.id}").exists())

    @override_settings(CART_ABANDONED_AFTER_MINUTES=60)
    def test_detect_skips_a_fresh_cart(self):
        self._cart_journey()
        self._idle_cart(email="fresh@example.com", minutes=5)  # inside the idle window
        self.assertEqual(detect_abandoned_carts()["enrolled"], 0)

    @override_settings(CART_ABANDONED_AFTER_MINUTES=60, CART_ABANDONED_MAX_AGE_DAYS=7)
    def test_detect_skips_an_ancient_cart(self):
        self._cart_journey()
        self._idle_cart(email="old@example.com", minutes=60 * 24 * 30)  # 30 days
        self.assertEqual(detect_abandoned_carts()["enrolled"], 0)

    @override_settings(CART_ABANDONED_AFTER_MINUTES=60)
    def test_detect_reads_guest_email_from_checkout_session(self):
        from cart.models import Cart, CheckoutSession
        from tests.factories import CartFactory, CartItemFactory, ProductFactory

        self._cart_journey()
        cart = CartFactory(user=None, session_key="sess-abc")
        CartItemFactory(cart=cart, product=ProductFactory())
        CheckoutSession.objects.create(
            cart=cart,
            metadata={"email": "guest@example.com"},
            expires_at=timezone.now() + timedelta(days=1),
        )
        Cart.objects.filter(pk=cart.pk).update(updated_at=timezone.now() - timedelta(minutes=120))
        res = detect_abandoned_carts()
        self.assertEqual(res["enrolled"], 1)
        self.assertTrue(
            JourneyEnrollment.objects.filter(
                subscriber__email="guest@example.com", trigger_ref=f"cart:{cart.id}"
            ).exists()
        )

    @override_settings(CART_ABANDONED_AFTER_MINUTES=60, CART_ABANDONED_BATCH=1)
    def test_email_less_cart_does_not_starve_the_batch(self):
        # An older guest cart with no email must not occupy the batch slot and block a
        # newer enrollable cart behind it.
        from cart.models import Cart
        from tests.factories import CartFactory, CartItemFactory, ProductFactory

        self._cart_journey()
        noemail = CartFactory(user=None, session_key="noemail")
        CartItemFactory(cart=noemail, product=ProductFactory())
        Cart.objects.filter(pk=noemail.pk).update(
            updated_at=timezone.now() - timedelta(minutes=300)
        )
        good = self._idle_cart(email="good@example.com", minutes=120)
        res = detect_abandoned_carts()
        self.assertEqual(res["enrolled"], 1)
        self.assertTrue(JourneyEnrollment.objects.filter(trigger_ref=f"cart:{good.id}").exists())

    @override_settings(CART_ABANDONED_AFTER_MINUTES=60)
    def test_guest_email_matching_a_registered_user_is_not_enrolled(self):
        # A guest checkout typing a registered account's address must not trigger a
        # cart email to that person (identity-spoofing guard).
        from django.contrib.auth import get_user_model

        from cart.models import Cart, CheckoutSession
        from tests.factories import CartFactory, CartItemFactory, ProductFactory

        self._cart_journey()
        get_user_model().objects.create_user(
            username="victim", email="victim@example.com", password="x"
        )
        cart = CartFactory(user=None, session_key="spoof")
        CartItemFactory(cart=cart, product=ProductFactory())
        CheckoutSession.objects.create(
            cart=cart,
            metadata={"email": "victim@example.com"},
            expires_at=timezone.now() + timedelta(days=1),
        )
        Cart.objects.filter(pk=cart.pk).update(updated_at=timezone.now() - timedelta(minutes=120))
        self.assertEqual(detect_abandoned_carts()["enrolled"], 0)

    @override_settings(CART_ABANDONED_AFTER_MINUTES=60)
    def test_detect_is_idempotent_across_ticks(self):
        self._cart_journey()
        self._idle_cart(email="dup@example.com", minutes=120)
        self.assertEqual(detect_abandoned_carts()["enrolled"], 1)
        self.assertEqual(detect_abandoned_carts()["enrolled"], 0)  # active enrollment dedups

    @override_settings(CART_ABANDONED_AFTER_MINUTES=60, CART_ABANDONED_BATCH=1)
    def test_detect_reaches_new_carts_across_ticks_not_just_the_oldest(self):
        # With more idle carts than the batch, an already-enrolled cart must not hog the
        # batch every tick — newer carts still get processed on later ticks.
        self._cart_journey()
        self._idle_cart(email="older@example.com", minutes=300)
        newer = self._idle_cart(email="newer@example.com", minutes=120)
        self.assertEqual(detect_abandoned_carts()["enrolled"], 1)  # oldest first
        self.assertEqual(detect_abandoned_carts()["enrolled"], 1)  # oldest excluded → newer
        self.assertTrue(JourneyEnrollment.objects.filter(trigger_ref=f"cart:{newer.id}").exists())


class CartActivityAndBlockTests(MarketingTestCase):
    def test_cartitem_save_bumps_cart_updated_at(self):
        from cart.models import Cart
        from tests.factories import CartFactory, CartItemFactory, ProductFactory

        cart = CartFactory()
        Cart.objects.filter(pk=cart.pk).update(updated_at=timezone.now() - timedelta(days=1))
        old = Cart.objects.get(pk=cart.pk).updated_at
        CartItemFactory(cart=cart, product=ProductFactory())
        self.assertGreater(Cart.objects.get(pk=cart.pk).updated_at, old)

    def test_abandoned_cart_context_returns_live_items(self):
        from tests.factories import CartFactory, CartItemFactory, ProductFactory

        cart = CartFactory()
        CartItemFactory(cart=cart, product=ProductFactory())
        ctx = block_context.abandoned_cart_context({}, {"event": {"cart_id": cart.id}})
        self.assertTrue(ctx["has_items"])
        self.assertEqual(len(ctx["items"]), 1)

    def test_abandoned_cart_context_empty_for_missing_cart(self):
        ctx = block_context.abandoned_cart_context({}, {"event": {"cart_id": 9_999_999}})
        self.assertFalse(ctx["has_items"])
        self.assertEqual(ctx["items"], [])
