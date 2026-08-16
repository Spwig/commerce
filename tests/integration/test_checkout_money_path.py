"""
Checkout money-path + step-tracking tests.

Hardens the two happy-path-only money capabilities — settle_fully_tendered_order
and select_payment_method — with the edge/negative cases that protect a live
shop, and covers the newly-wired informational step states (billing / review).

Money invariants under test for _settle_if_fully_tendered:
- only settles when INTERNAL tenders (gift card / wallet) fully cover the total;
- refuses on under-tender, currency mismatch, null settlement, non-hold rows;
- idempotent (never re-settles a paid order);
- amount_paid ends at EXACTLY the total once the settlement receiver credits the
  captured holds — never double-counted (regression for the HIGH the security
  audit found).
"""

import uuid
from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from djmoney.money import Money

from cart.models import CheckoutSession
from cart.services.checkout_service import CheckoutService
from catalog.models import GiftCard
from catalog.services.gift_card_tender_service import GiftCardTenderService
from payment_providers.models import PaymentTransaction

pytestmark = [pytest.mark.django_db, pytest.mark.integration]


@pytest.fixture
def gift_card_product(db):
    from tests.factories import ProductFactory

    return ProductFactory(product_type="gift_card", status="published")


def _card(gift_card_product, value="100.00", currency="USD"):
    return GiftCard.objects.create(
        product=gift_card_product,
        initial_value=Money(Decimal(value), currency),
        recipient_email="recipient@test.spwig.com",
        is_active=True,
    )


def _order(total="50.00", currency="USD", **kwargs):
    from tests.factories import OrderFactory

    return OrderFactory(
        total_amount=total,
        total_amount_currency=currency,
        payment_status=kwargs.pop("payment_status", "unpaid"),
        amount_paid=kwargs.pop("amount_paid", Decimal("0.00")),
        amount_paid_currency=currency,
        **kwargs,
    )


def _gc_hold(
    order, card, amount, currency="USD", status="authorized", ttype="authorize", settlement=True
):
    """An internal (gift card) tender hold against the order, in order currency."""
    return PaymentTransaction.objects.create(
        transaction_id=f"gc-auth:{uuid.uuid4().hex[:16]}",
        order=order,
        tender_type=PaymentTransaction.TENDER_GIFT_CARD,
        gift_card=card,
        transaction_type=ttype,
        status=status,
        amount=Money(amount, currency),
        settlement_amount=Money(amount, currency) if settlement else None,
        provider_account=None,
    )


# ============================================================
# settle_fully_tendered_order — settle DECISION
# ============================================================


class TestSettleDecision:
    def test_exact_cover_marks_paid(self, gift_card_product):
        order = _order(total="50.00")
        _gc_hold(order, _card(gift_card_product), "50.00")
        assert CheckoutService._settle_if_fully_tendered(order) is True
        order.refresh_from_db()
        assert order.payment_status == "paid"
        assert order.paid_at is not None
        # Seeds net-due (0) in isolation; the receiver credits the real figure
        # (see TestSettleAmountPaidInvariant).
        assert order.amount_paid == Money("0.00", "USD")

    def test_under_cover_does_not_settle(self, gift_card_product):
        order = _order(total="50.00")
        _gc_hold(order, _card(gift_card_product), "30.00")
        assert CheckoutService._settle_if_fully_tendered(order) is False
        order.refresh_from_db()
        assert order.payment_status == "unpaid"

    def test_currency_mismatch_falls_through(self, gift_card_product):
        order = _order(total="50.00", currency="USD")
        _gc_hold(order, _card(gift_card_product, currency="EUR"), "50.00", currency="EUR")
        assert CheckoutService._settle_if_fully_tendered(order) is False
        order.refresh_from_db()
        assert order.payment_status == "unpaid"

    def test_null_settlement_amount_falls_through(self, gift_card_product):
        order = _order(total="50.00")
        _gc_hold(order, _card(gift_card_product), "50.00", settlement=False)
        assert CheckoutService._settle_if_fully_tendered(order) is False
        order.refresh_from_db()
        assert order.payment_status == "unpaid"

    def test_non_authorized_status_not_counted(self, gift_card_product):
        order = _order(total="50.00")
        _gc_hold(order, _card(gift_card_product), "50.00", status="pending")
        assert CheckoutService._settle_if_fully_tendered(order) is False

    def test_non_authorize_type_not_counted(self, gift_card_product):
        order = _order(total="50.00")
        _gc_hold(order, _card(gift_card_product), "50.00", ttype="capture")
        assert CheckoutService._settle_if_fully_tendered(order) is False

    def test_non_internal_tender_not_counted(self, gift_card_product):
        """A hold the settlement receiver will NOT capture (e.g. a future gateway
        auth) must not mark the order paid — money would never be collected."""
        order = _order(total="50.00")
        PaymentTransaction.objects.create(
            transaction_id=f"gw-auth:{uuid.uuid4().hex[:16]}",
            order=order,
            tender_type=PaymentTransaction.TENDER_GATEWAY,
            transaction_type="authorize",
            status="authorized",
            amount=Money("50.00", "USD"),
            settlement_amount=Money("50.00", "USD"),
        )
        assert CheckoutService._settle_if_fully_tendered(order) is False
        order.refresh_from_db()
        assert order.payment_status == "unpaid"

    def test_already_paid_is_idempotent(self, gift_card_product):
        order = _order(total="50.00", payment_status="paid")
        _gc_hold(order, _card(gift_card_product), "50.00")
        assert CheckoutService._settle_if_fully_tendered(order) is False


# ============================================================
# settle — amount_paid invariant (full flow, receiver runs)
# ============================================================


def _tender_session(total="100.00", currency="USD"):
    from tests.factories import CartFactory, UserFactory

    session = CheckoutSession.objects.create(
        cart=CartFactory(user=UserFactory()),
        expires_at=timezone.now() + timedelta(hours=1),
    )
    session.total_amount = Money(Decimal(total), currency)
    session.save(update_fields=["total_amount"])
    return session


class TestSettleAmountPaidInvariant:
    def test_full_gift_card_tender_amount_paid_equals_total_once(
        self, gift_card_product, django_capture_on_commit_callbacks
    ):
        """Regression: a fully gift-card-tendered order must end with
        amount_paid == total (exactly), not 2x. The bug was _settle seeding the
        full total and the settlement receiver then crediting the captured
        tenders on top."""
        card = _card(gift_card_product, "100.00")
        session = _tender_session("100.00")
        GiftCardTenderService.authorize_for_session(
            session, card.code, amount=Money(Decimal("100.00"), "USD")
        )
        order = _order(total="100.00")
        PaymentTransaction.objects.filter(checkout_session=session).update(order=order)

        with django_capture_on_commit_callbacks(execute=True):
            settled = CheckoutService._settle_if_fully_tendered(order)

        assert settled is True
        order.refresh_from_db()
        assert order.payment_status == "paid"
        assert order.amount_paid == Money(Decimal("100.00"), "USD")  # not 200

    def test_over_tender_amount_paid_capped_at_total(
        self, gift_card_product, django_capture_on_commit_callbacks
    ):
        """Two gift cards over-covering the order still settle to exactly the
        total (capture caps at remaining due)."""
        session = _tender_session("100.00")
        for _ in range(2):
            card = _card(gift_card_product, "80.00")
            GiftCardTenderService.authorize_for_session(
                session, card.code, amount=Money(Decimal("80.00"), "USD")
            )  # 160 held vs 100 total
        order = _order(total="100.00")
        PaymentTransaction.objects.filter(checkout_session=session).update(order=order)

        with django_capture_on_commit_callbacks(execute=True):
            CheckoutService._settle_if_fully_tendered(order)

        order.refresh_from_db()
        assert order.payment_status == "paid"
        assert order.amount_paid == Money(Decimal("100.00"), "USD")


# ============================================================
# select_payment_method (set_payment_method)
# ============================================================


class TestSetPaymentMethod:
    @pytest.fixture
    def session(self, db):
        from tests.factories import CartFactory, CheckoutSessionFactory

        return CheckoutSessionFactory(cart=CartFactory())

    def test_unknown_provider_rejected(self, session):
        ok, _msg = CheckoutService.set_payment_method(session, str(uuid.uuid4()))
        assert ok is False

    def test_disconnected_provider_rejected(self, session):
        from tests.factories import PaymentProviderAccountFactory

        provider = PaymentProviderAccountFactory(connection_status="error")
        ok, _msg = CheckoutService.set_payment_method(session, str(provider.id))
        assert ok is False
        session.refresh_from_db()
        assert session.payment_provider_id is None


# ============================================================
# Step tracking (complete_billing_step / complete_review_step)
# ============================================================


class TestCheckoutStepTracking:
    def _billing_data(self):
        return {
            "name": "A B",
            "address1": "1 St",
            "city": "NYC",
            "postal_code": "10001",
            "country": "US",
        }

    def test_set_billing_address_records_billing_step(self, db):
        from tests.factories import CartFactory, CheckoutSessionFactory

        session = CheckoutSessionFactory(cart=CartFactory())
        ok, _msg = CheckoutService.set_billing_address(
            session, same_as_shipping=False, address_data=self._billing_data()
        )
        assert ok is True
        session.refresh_from_db()
        assert session.step_completed == "billing"

    def test_billing_step_does_not_regress_a_later_step(self, db):
        """A no-shipping cart can select payment before billing submits; recording
        billing must not send the session backward from payment."""
        from tests.factories import CartFactory, CheckoutSessionFactory

        session = CheckoutSessionFactory(cart=CartFactory(), step_completed="payment")
        CheckoutService.set_billing_address(
            session, same_as_shipping=False, address_data=self._billing_data()
        )
        session.refresh_from_db()
        assert session.step_completed == "payment"  # not regressed

    def test_advance_step_is_monotonic(self, db):
        """All setters route step writes through _advance_step, so a later step
        (e.g. review) is never regressed by a subsequent earlier setter."""
        from tests.factories import CartFactory, CheckoutSessionFactory

        session = CheckoutSessionFactory(cart=CartFactory(), step_completed="review")
        assert CheckoutService._advance_step(session, "payment") is False
        assert session.step_completed == "review"  # not regressed
        session.step_completed = "cart"
        assert CheckoutService._advance_step(session, "shipping_method") is True
        assert session.step_completed == "shipping_method"  # advances forward

    def test_shipping_address_change_rewinds_resume_step(self, db):
        """Changing the shipping address clears the selected method, so the
        resume marker must rewind from a later step to shipping_address rather
        than leave the client resuming at payment with no valid method."""
        from tests.factories import CartFactory, CheckoutSessionFactory

        session = CheckoutSessionFactory(cart=CartFactory(), step_completed="payment")
        ok, _msg = CheckoutService.set_shipping_address(
            session,
            address_data={
                "name": "A B",
                "address1": "1 St",
                "city": "NYC",
                "state": "NY",
                "postal_code": "10001",
                "country": "US",
                "phone": "+1-555-0100",
            },
        )
        assert ok is True
        session.refresh_from_db()
        assert session.step_completed == "shipping_address"  # rewound

    def test_validate_endpoint_records_review_step_when_valid(self, db):
        from unittest.mock import patch

        from django.test import RequestFactory

        from cart.views import CheckoutViewSet
        from tests.factories import CartFactory, CheckoutSessionFactory

        session = CheckoutSessionFactory(cart=CartFactory(), step_completed="payment")
        view = CheckoutViewSet()
        view.get_session = lambda request: session
        request = RequestFactory().post("/api/cart/checkout/validate/")

        with patch.object(CheckoutService, "validate_checkout", return_value=(True, [])):
            resp = view.validate(request)

        assert resp.data["is_valid"] is True
        session.refresh_from_db()
        assert session.step_completed == "review"

    def test_validate_endpoint_leaves_step_when_invalid(self, db):
        from unittest.mock import patch

        from django.test import RequestFactory

        from cart.views import CheckoutViewSet
        from tests.factories import CartFactory, CheckoutSessionFactory

        session = CheckoutSessionFactory(cart=CartFactory(), step_completed="payment")
        view = CheckoutViewSet()
        view.get_session = lambda request: session
        request = RequestFactory().post("/api/cart/checkout/validate/")

        with patch.object(CheckoutService, "validate_checkout", return_value=(False, ["nope"])):
            view.validate(request)

        session.refresh_from_db()
        assert session.step_completed == "payment"  # unchanged
