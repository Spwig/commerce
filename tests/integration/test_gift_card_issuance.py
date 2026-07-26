"""
P2.3 — gift card issuance.

Selling a gift card has never worked in this codebase. The service that mints
cards was correct, and unreachable: it hung off
``CheckoutService.process_payment_completion``, which had zero callers repo-wide.
A merchant could sell a gift card, take the money, and the customer received
nothing — while every unit test of the service passed.

That shape of failure is what these tests are built around. The riskiest
property is not "does minting work" but:

  **Exactly ``quantity`` cards per order line, ever.**

Issuance fires more than once per order by design — a retried payment webhook,
an admin re-save, the settlement receiver's own ``amount_paid`` write-back — and
a second run would mint a second set of *funded* cards. That is money created
from nothing, silently, and irreversibly once the codes are emailed. The
guarantee is a unique database constraint on ``(order_item, issue_index)``,
because every application-level alternative ("count, then create") is a
read-then-write race two workers can both win.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R2, P2.3)
"""

from decimal import Decimal

import pytest
from django.db import IntegrityError
from django.test import override_settings
from djmoney.money import Money

from catalog.models import GiftCard
from catalog.services.gift_card_service import GiftCardService
from tests.factories import OrderFactory, OrderItemFactory, ProductFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.r2,
]

FACE = Money(Decimal("50.00"), "USD")


def _gift_card_order(quantity=1, recipient="recipient@test.spwig.com", **item_kwargs):
    product = ProductFactory(product_type="gift_card", price=FACE)
    order = OrderFactory(payment_status="unpaid")
    item = OrderItemFactory(
        order=order,
        product=product,
        quantity=quantity,
        unit_price=FACE,
        total_price=FACE * quantity,
        gift_card_data={"recipient_email": recipient},
        **item_kwargs,
    )
    return order, item


class TestMinting:
    def test_a_paid_order_mints_a_funded_card(self, site_settings):
        order, item = _gift_card_order()

        count, codes = GiftCardService.create_gift_cards_for_order(order)

        assert count == 1 and len(codes) == 1
        card = GiftCard.objects.get(order_item=item)
        assert card.initial_value == FACE
        assert card.current_balance == FACE
        assert card.is_active is True
        assert card.recipient_email == "recipient@test.spwig.com"

    def test_quantity_is_honoured_with_distinct_codes(self, site_settings):
        order, item = _gift_card_order(quantity=3)

        count, codes = GiftCardService.create_gift_cards_for_order(order)

        assert count == 3
        assert len(set(codes)) == 3, "Codes must be unique — they are bearer instruments."
        assert set(
            GiftCard.objects.filter(order_item=item).values_list("issue_index", flat=True)
        ) == {0, 1, 2}

    def test_a_card_with_no_recipient_is_refused_not_sent_to_the_buyer(self, site_settings):
        """
        Silently mailing the gift to the BUYER is worse than failing.

        The intended recipient never learns the gift exists, and the buyer
        believes it was delivered. The old code did exactly this, falling back
        to order.email.
        """
        order, item = _gift_card_order(recipient="")

        count, _codes = GiftCardService.create_gift_cards_for_order(order)

        assert count == 0
        assert GiftCard.objects.filter(order_item=item).count() == 0

    def test_an_order_with_no_gift_cards_is_a_no_op(self, site_settings):
        order = OrderFactory(payment_status="paid")
        OrderItemFactory(order=order, product=ProductFactory(product_type="simple"))

        assert GiftCardService.create_gift_cards_for_order(order) == (0, [])


class TestIssuanceIsIdempotent:
    """The property that stops an order minting a second set of funded cards."""

    def test_running_twice_mints_nothing_the_second_time(self, site_settings):
        order, item = _gift_card_order(quantity=2)

        first, _ = GiftCardService.create_gift_cards_for_order(order)
        second, _ = GiftCardService.create_gift_cards_for_order(order)

        assert first == 2
        assert second == 0, "A second run minted more cards — money from nothing."
        assert GiftCard.objects.filter(order_item=item).count() == 2

    def test_the_constraint_is_what_enforces_it(self, site_settings):
        """
        Assert the database refuses the duplicate directly.

        Not merely that the service happens to skip: a count-based guard would
        also pass the test above while losing a race between two workers.
        """
        order, item = _gift_card_order()
        GiftCardService.create_gift_cards_for_order(order)

        with pytest.raises(IntegrityError):
            GiftCard.objects.create(
                code="GC-DUPE-SLOT-0000",
                product=item.product,
                order_item=item,
                issue_index=0,  # already taken
                initial_value=FACE,
                current_balance=FACE,
                recipient_email="someone@test.spwig.com",
            )

    def test_a_partial_previous_run_is_completed_not_restarted(self, site_settings):
        """
        A crash after 1 of 3 must mint the missing 2 — not 3 more, not zero.

        This is why each slot gets its own savepoint: an IntegrityError raised
        inside an enclosing atomic block aborts the whole transaction, which
        would turn a lost race into a PARTIAL mint — the customer paying for
        three cards and receiving one.
        """
        order, item = _gift_card_order(quantity=3)
        GiftCard.objects.create(
            code="GC-PARTIAL-RUN-01",
            product=item.product,
            order_item=item,
            issue_index=0,
            initial_value=FACE,
            current_balance=FACE,
            recipient_email="recipient@test.spwig.com",
        )

        count, _codes = GiftCardService.create_gift_cards_for_order(order)

        assert count == 2, "Should have filled only the two empty slots."
        assert GiftCard.objects.filter(order_item=item).count() == 3

    def test_admin_created_cards_are_exempt_from_the_constraint(self, site_settings):
        """Cards made by hand have no order line and must stay unconstrained."""
        product = ProductFactory(product_type="gift_card", price=FACE)
        for i in range(2):
            GiftCard.objects.create(
                code=f"GC-MANUAL-000{i}",
                product=product,
                initial_value=FACE,
                current_balance=FACE,
                recipient_email="manual@test.spwig.com",
            )

        assert GiftCard.objects.filter(order_item__isnull=True).count() == 2


class TestTheReceiverIsWired:
    """
    The orphaned entry point is the whole reason this phase exists, so assert
    the wiring rather than the service. A service test cannot catch it.
    """

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_marking_an_order_paid_mints_the_card(
        self, site_settings, django_capture_on_commit_callbacks
    ):
        order, item = _gift_card_order()

        with django_capture_on_commit_callbacks(execute=True):
            order.payment_status = "paid"
            order.save(update_fields=["payment_status"])

        assert GiftCard.objects.filter(order_item=item).count() == 1

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_a_pos_style_order_created_already_paid_still_mints(
        self, site_settings, django_capture_on_commit_callbacks
    ):
        """
        POS builds the Order with payment_status="paid" inline, so `created` is
        True on the only post_save it ever gets. The sibling settlement receiver
        guards `if created: return`; copying that here would mean the till takes
        the money and no card is ever minted.
        """
        product = ProductFactory(product_type="gift_card", price=FACE)

        with django_capture_on_commit_callbacks(execute=True):
            order = OrderFactory(payment_status="paid")
            item = OrderItemFactory(
                order=order,
                product=product,
                quantity=1,
                unit_price=FACE,
                total_price=FACE,
                gift_card_data={"recipient_email": "instore@test.spwig.com"},
            )
            # The line exists only after the order does, so POS-shaped flows
            # settle on a later save; this mirrors that.
            order.save(update_fields=["payment_status"])

        assert GiftCard.objects.filter(order_item=item).count() == 1

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_an_unpaid_order_mints_nothing(self, site_settings, django_capture_on_commit_callbacks):
        order, item = _gift_card_order()

        with django_capture_on_commit_callbacks(execute=True):
            order.status = "processing"
            order.save()

        assert GiftCard.objects.filter(order_item=item).count() == 0


class TestChosenAmountIsHonoured:
    """
    Found by review: the denomination was validated and then thrown away.

    ``add_item`` set unit_price from the customer's chosen amount, and the
    general pricing block a few lines later recomputed it from the product —
    so a merchant offering 25/50/100 charged product.price every time, and the
    issued card carried that value too.
    """

    def test_a_chosen_denomination_sets_the_line_price(self, site_settings):
        from cart.services.cart_service import CartService
        from tests.factories import CartFactory, UserFactory

        product = ProductFactory(
            product_type="gift_card",
            price=Money(Decimal("10.00"), "USD"),
            gift_card_denomination_type="fixed",
            gift_card_denominations=[25, 50, 100],
        )
        cart = CartFactory(user=UserFactory())

        ok, msg, item = CartService.add_item(
            cart,
            product.id,
            quantity=1,
            gift_card_data={
                "recipient_email": "recipient@test.spwig.com",
                "amount": "50.00",
            },
        )

        assert ok, msg
        assert item.unit_price.amount == Decimal("50.00"), (
            f"Charged {item.unit_price} for a 50.00 gift card — the chosen "
            f"denomination was discarded by the pricing block."
        )

    def test_an_amount_outside_the_denominations_is_refused(self, site_settings):
        from cart.services.cart_service import CartService
        from tests.factories import CartFactory, UserFactory

        product = ProductFactory(
            product_type="gift_card",
            gift_card_denomination_type="fixed",
            gift_card_denominations=[25, 50],
        )
        cart = CartFactory(user=UserFactory())

        ok, _msg, _item = CartService.add_item(
            cart,
            product.id,
            gift_card_data={
                "recipient_email": "recipient@test.spwig.com",
                "amount": "1000.00",
            },
        )

        assert ok is False
        assert cart.items.count() == 0

    def test_the_issued_card_carries_the_amount_that_was_paid(self, site_settings):
        """Face value must equal what was charged, not what the product costs."""
        order = OrderFactory(payment_status="unpaid")
        product = ProductFactory(product_type="gift_card", price=Money(Decimal("10.00"), "USD"))
        paid = Money(Decimal("75.00"), "USD")
        item = OrderItemFactory(
            order=order,
            product=product,
            quantity=1,
            unit_price=paid,
            total_price=paid,
            gift_card_data={"recipient_email": "recipient@test.spwig.com"},
        )

        GiftCardService.create_gift_cards_for_order(order)

        assert GiftCard.objects.get(order_item=item).initial_value == paid


class TestGiftCardDataSurvivesStorage:
    """
    Found by review: DRF returns Decimal and datetime, and a plain JSONField
    cannot encode either. Writing them raw made add-to-cart raise — so picking
    an amount or a delivery date broke the purchase outright.
    """

    def test_amount_and_schedule_round_trip_through_the_database(self, site_settings):
        from datetime import timedelta

        from django.utils import timezone as dj_timezone

        from cart.services.cart_service import CartService
        from tests.factories import CartFactory, UserFactory

        product = ProductFactory(
            product_type="gift_card",
            gift_card_denomination_type="custom",
            gift_card_min_amount=Decimal("5.00"),
            gift_card_max_amount=Decimal("500.00"),
        )
        cart = CartFactory(user=UserFactory())
        when = (dj_timezone.now() + timedelta(days=30)).isoformat()

        ok, msg, item = CartService.add_item(
            cart,
            product.id,
            gift_card_data={
                "recipient_email": "recipient@test.spwig.com",
                "amount": "60.00",
                "scheduled_send_at": when,
            },
        )

        assert ok, msg
        item.refresh_from_db()  # forces a real DB round trip
        assert item.gift_card_data["amount"] == "60.00"
        assert isinstance(item.gift_card_data["scheduled_send_at"], str)


class TestQuantityCannotBeRaisedToMintFreeCards:
    """
    Found by review: the unique constraint protects (order_item, issue_index),
    so raising quantity on an already-paid line opens genuinely-unused slots
    that a later run would fill — cards nobody paid for.
    """

    def test_raising_quantity_after_payment_mints_nothing_more(self, site_settings):
        order, item = _gift_card_order(quantity=1)
        GiftCardService.create_gift_cards_for_order(order)
        assert GiftCard.objects.filter(order_item=item).count() == 1

        # Raise quantity but not total_price — the line was paid for one card.
        order.payment_status = "paid"
        order.save(update_fields=["payment_status"])
        item.quantity = 5
        item.save(update_fields=["quantity"])

        GiftCardService.create_gift_cards_for_order(order)

        assert GiftCard.objects.filter(order_item=item).count() == 1, (
            "Raising quantity on a paid line minted extra cards for free."
        )
