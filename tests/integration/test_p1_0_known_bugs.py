"""
P1.0 characterisation: reproduction tests for four confirmed defects.

Every test in this module asserts the *correct* behaviour and therefore
FAILS against the code as it stands. Each is marked
``pytest.mark.xfail(strict=True)`` so that:

* CI stays green today (the failure is expected and declared), and
* CI turns **red** the moment a fix lands without the test being updated,
  because ``strict=True`` makes an unexpected pass a build failure.

Do not "fix" a test in here by relaxing the assertion. When the referenced
plan phase lands, delete the ``xfail`` marker — the assertion is already
the specification.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md

  Bug 1  loyalty silent points theft ................. fixed in P1.1
  Bug 2  referral coupon/percent rewards TypeError ... fixed in P1.1
  Bug 3  referral invalid default reward kind ........ fixed in P1.1
  Bug 4  gift card issuance never runs ............... fixed in P2.3
"""

from decimal import Decimal

import pytest
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from djmoney.money import Money
from rest_framework.test import APIClient

from tests.factories import (
    OrderFactory,
    OrderItemFactory,
    ProductFactory,
    UserFactory,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.known_bugs,
]


# ============================================================
# Fixtures / helpers
# ============================================================


@pytest.fixture(autouse=True)
def _clear_throttle_cache():
    """
    ``RedemptionRateThrottle`` is 10/hour and DRF caches its counters.

    With ``--reuse-db`` (and across repeated local runs) a stale counter
    turns a genuine assertion into a spurious 429, so clear before and
    after every test in this module.
    """
    cache.clear()
    yield
    cache.clear()


def _enrol_member(user, points=1000):
    """
    Enrol ``user`` in the loyalty programme with a known balance.

    ``loyalty/signals.py:160`` (``create_loyalty_member_on_signup``) already
    enrols every non-staff user on ``post_save`` and may award a signup
    bonus, so this must *reconcile* to an exact balance rather than create
    one — creating would raise ``IntegrityError`` on the OneToOne, and
    trusting the signal's balance would make point assertions depend on
    whatever the signup bonus rule happens to be.
    """
    from loyalty.models import LoyaltyBalance, LoyaltyMember

    member, _ = LoyaltyMember.objects.get_or_create(customer=user, defaults={"is_active": True})
    LoyaltyBalance.objects.update_or_create(
        member=member,
        defaults={
            "available_points": points,
            "pending_points": 0,
            "lifetime_earned": points,
            "lifetime_redeemed": 0,
        },
    )
    member.refresh_from_db()
    return member


def _make_discount_reward(points_cost=100, discount_value=Decimal("10.00")):
    """A ``TYPE_DISCOUNT`` reward — the kind that is supposed to mint a voucher."""
    from loyalty.models import LoyaltyReward

    return LoyaltyReward.objects.create(
        name="10 Off Your Next Order",
        slug="ten-off-next-order",
        description="Ten currency units off your next order.",
        reward_type=LoyaltyReward.TYPE_DISCOUNT,
        discount_type=LoyaltyReward.DISCOUNT_TYPE_FIXED,
        discount_value=discount_value,
        points_cost=points_cost,
        is_active=True,
    )


# ============================================================
# Bug 1 — Loyalty silent points theft (P1.1)
# ============================================================


class TestLoyaltyDiscountRedemptionIssuesAVoucher:
    """
    BUG 1 — silent points theft. Fixed in plan phase **P1.1**.

    ``loyalty/api/views.py:590`` imports ``VoucherService`` from
    ``vouchers.services``. That package's ``__init__.py`` is 0 bytes and no
    such class exists, so the import raises ``ImportError`` — which
    ``except (ImportError, AttributeError): pass`` at ``:598`` swallows.

    The endpoint therefore returns **HTTP 200 "Reward redeemed
    successfully!"** with ``redemption.voucher_code`` left NULL, *after* the
    member's points have already been deducted. The customer pays points and
    receives nothing, and nothing anywhere records that it happened.
    """

    # FIXED in P1.1: redeem() now delegates to RedemptionEngine, the silent
    # `except (ImportError, AttributeError): pass` is gone, and
    # confirm_redemption refunds via LedgerService.refund_redemption when the
    # reward cannot be issued. Discount rewards start issuing real value in
    # P2.4 (fixed -> wallet credit, percentage -> VoucherCode).
    def test_discount_redemption_either_fails_cleanly_or_issues_a_real_voucher(self, site_settings):
        """
        A discount redemption must be all-or-nothing.

        Either the call fails cleanly and the points are still there, or it
        succeeds and the member holds a real, resolvable ``VoucherCode``.
        The current outcome — 200, NULL voucher, points gone — is neither,
        and must fail this test.
        """
        from loyalty.models import LoyaltyRedemption

        user = UserFactory()
        member = _enrol_member(user, points=1000)
        reward = _make_discount_reward(points_cost=100)

        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse("loyalty-reward-redeem", kwargs={"uuid": str(reward.uuid)})
        response = client.post(url, {}, format="json")

        member.balance.refresh_from_db()

        if response.status_code >= 400 or not response.data.get("success"):
            # Acceptable outcome: refused cleanly, nothing was taken.
            assert member.balance.available_points == 1000, (
                "Redemption was refused but points were still deducted — "
                "the deduction must be rolled back with the failure."
            )
            return

        # Reported success: there must be something to show for the points.
        # As of P2.5c (D2 routing) a FIXED-value reward issues WALLET CREDIT —
        # spendable at checkout since P2.5a/b — not a voucher. voucher_code
        # stays NULL for fixed rewards by design; percentage rewards mint one.
        redemption = LoyaltyRedemption.objects.get(member=member, reward=reward)

        from wallet.models import WalletTransaction

        credit = WalletTransaction.objects.filter(
            source=WalletTransaction.SOURCE_LOYALTY,
            reference_id=str(redemption.uuid),
        ).first()
        assert credit is not None, (
            "API reported success but no wallet credit exists for this "
            "redemption — the member paid points and received nothing."
        )
        assert credit.amount.amount == reward.discount_value
        assert credit.wallet.customer_id == user.pk

    # FIXED in P1.1: points are still debited before issuance is attempted, but
    # confirm_redemption now refunds them via LedgerService.refund_redemption
    # and cancels the redemption when the reward cannot be issued, so the
    # balance ends up whole either way.
    def test_point_balance_is_conserved_when_no_reward_is_issued(self, site_settings):
        """
        Points must never leave the balance without something being issued.

        This is the money invariant stated on its own, independent of what
        the HTTP layer reports: if ``redemption.voucher_code`` is NULL then
        the balance must be untouched.
        """
        from loyalty.models import LoyaltyRedemption

        user = UserFactory()
        member = _enrol_member(user, points=500)
        reward = _make_discount_reward(points_cost=250)

        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse("loyalty-reward-redeem", kwargs={"uuid": str(reward.uuid)})
        client.post(url, {}, format="json")

        member.balance.refresh_from_db()
        redemption = LoyaltyRedemption.objects.filter(member=member, reward=reward).first()

        # D2: a fixed reward issues wallet credit; a voucher would mean a
        # percentage reward. Either counts as "something was issued".
        from wallet.models import WalletTransaction

        credited = (
            redemption is not None
            and WalletTransaction.objects.filter(
                source=WalletTransaction.SOURCE_LOYALTY,
                reference_id=str(redemption.uuid),
            ).exists()
        )
        issued = credited or (redemption is not None and redemption.voucher_code_id is not None)

        if not issued:
            assert member.balance.available_points == 500, (
                f"Nothing was issued, but {500 - member.balance.available_points} "
                "points were deducted anyway."
            )
        else:
            assert member.balance.available_points == 250


# ============================================================
# Bug 2 — Referral coupon / percent rewards raise TypeError (P1.1)
# ============================================================


class TestReferralCouponRewardsAreIssuable:
    """
    BUG 2 — every referral coupon reward raises. Fixed in phase **P1.1**.

    ``referrals/services/rewards.py:296`` and ``:334`` pass ``minimum_spend``,
    ``single_use``, ``usage_limit`` (and ``maximum_discount`` at ``:334``) to
    ``VoucherCode.objects.create``. None of those fields exist on the model —
    the real names are ``min_order_value``, ``max_uses_total``,
    ``max_uses_per_customer`` and ``max_discount_amount``. The result is an
    unconditional ``TypeError`` inside ``@transaction.atomic``.

    The existing suite misses this because ``referrals/tests/factories.py:189``
    defaults ``kind="credit"``, so ``test_issue_reward`` only ever exercises
    the wallet path. These tests build the reward kinds explicitly.
    """

    # FIXED in P1.1: create_coupon_code now uses the real field names
    # (min_order_value, max_uses_total, max_uses_per_customer), binds the code
    # to the earner via issued_to, and carries the reward's expiry onto end_date.
    def test_issue_reward_with_kind_coupon_creates_a_real_voucher(self, site_settings):
        """A ``coupon`` reward must reach ``issued`` with a linked voucher."""
        from referrals.services import issue_reward
        from referrals.tests.factories import create_referral_reward
        from vouchers.models import VoucherCode

        reward = create_referral_reward(kind="coupon", amount=Decimal("10.00"))

        assert issue_reward(reward) is True, "issue_reward() reported failure for kind='coupon'"

        reward.refresh_from_db()
        assert reward.status == "issued"
        assert reward.voucher_code_id is not None, "coupon reward issued without a voucher"

        voucher = VoucherCode.objects.get(pk=reward.voucher_code_id)
        assert voucher.discount_type == "fixed"
        assert voucher.discount_value == Decimal("10.00")

    # FIXED in P1.1: create_percentage_coupon uses max_discount_amount (a
    # MoneyField, so it takes the Money directly) and now raises rather than
    # silently inventing a 10% rate when the reward carries no percentage.
    def test_issue_reward_with_kind_percent_creates_a_real_voucher(self, site_settings):
        """A ``percent`` reward must reach ``issued`` with a linked voucher."""
        from referrals.services import issue_reward
        from referrals.tests.factories import create_referral_reward
        from vouchers.models import VoucherCode

        reward = create_referral_reward(
            kind="percent",
            amount=Decimal("25.00"),
            percentage=Decimal("15.00"),
        )

        assert issue_reward(reward) is True, "issue_reward() reported failure for kind='percent'"

        reward.refresh_from_db()
        assert reward.status == "issued"
        assert reward.voucher_code_id is not None, "percent reward issued without a voucher"

        voucher = VoucherCode.objects.get(pk=reward.voucher_code_id)
        assert voucher.discount_type == "percentage"
        assert voucher.discount_value == Decimal("15.00")


# ============================================================
# Bug 3 — Referral invalid default reward kind (P1.1)
# ============================================================


class TestReferralRefereeRewardDefaultKind:
    """
    BUG 3 — silent non-issuance. Fixed in phase **P1.1**.

    ``referrals/services/rewards.py:69`` defaults the referee reward kind to
    ``"discount"``, which is **not** one of ``KIND_CHOICES``
    (credit/coupon/percent/perk). ``issue_reward`` falls through its
    dispatcher to ``success = False``, the reward silently stays ``pending``,
    and the only trace is a log line.

    ``ReferralProgram.get_program()`` seeds the very same invalid
    ``"kind": "discount"`` into the default programme config, so a stock
    install reproduces this without a merchant touching anything.
    """

    # FIXED in P1.1: the referee default is now "credit" (matching the referrer
    # branch), and _validated_kind rejects any kind outside KIND_CHOICES at
    # creation instead of letting it fail silently at issuance.
    def test_double_sided_referee_reward_without_explicit_kind_is_issued(self, site_settings):
        """
        A double-sided programme whose ``referee`` config omits ``kind`` must
        still issue the referee's reward. Falling back to a kind the
        dispatcher cannot handle is a silent non-payment.
        """
        from referrals.services import create_rewards, issue_reward
        from referrals.tests.factories import (
            create_referral_attribution,
            create_referral_program,
        )

        program = create_referral_program(
            reward_config={
                "referrer": {"kind": "credit", "amount": 10.00},
                # Deliberately no "kind" — exercise the service default.
                "referee": {"amount": 10.00},
                "double_sided": True,
            }
        )
        attribution = create_referral_attribution(program=program, status="approved")

        _referrer_reward, referee_reward = create_rewards(attribution)

        assert referee_reward is not None, "double_sided programme created no referee reward"
        assert referee_reward.kind in dict(referee_reward.KIND_CHOICES), (
            f"referee reward defaulted to kind={referee_reward.kind!r}, "
            f"which is not one of {sorted(dict(referee_reward.KIND_CHOICES))}"
        )

        assert issue_reward(referee_reward) is True, (
            "issue_reward() returned False for the referee reward — the referee "
            "was promised a reward and silently received nothing"
        )

        referee_reward.refresh_from_db()
        assert referee_reward.status == "issued"


# ============================================================
# Bug 4 — Gift card issuance never runs (P2.3)
# ============================================================


class TestGiftCardIssuanceOnPaidOrder:
    """
    BUG 4 — gift card issuance has never run. Fixed in phase **P2.3**.

    .. warning::

       This one stays red **longer than the others**. Bugs 1-3 are fixed in
       P1.1; this is not repaired until **P2.3**, once the tender rail from
       P2.1/P2.2 exists. Expect it to remain ``xfail`` across the whole of
       R1 — that is correct, not a regression.

    ``GiftCardService.create_gift_cards_for_order`` is called only by
    ``CheckoutService.process_payment_completion``
    (``cart/services/checkout_service.py:1256``), and that method has **zero
    callers repo-wide**. A merchant can sell a gift card, take the money, and
    no card is ever created.
    """

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_paid_order_containing_a_gift_card_product_issues_a_funded_card(
        self, site_settings, django_capture_on_commit_callbacks
    ):
        """
        Paying for a gift card line item must produce a funded
        ``catalog.GiftCard`` linked back to the order item it came from.
        """
        from catalog.models import GiftCard

        face_value = Money(Decimal("50.00"), "USD")

        product = ProductFactory(
            name="Digital Gift Card 50",
            product_type="gift_card",
            price=face_value,
        )
        order = OrderFactory(payment_status="unpaid")
        order_item = OrderItemFactory(
            order=order,
            product=product,
            quantity=1,
            unit_price=face_value,
            total_price=face_value,
            gift_card_data={"recipient_email": "recipient@test.spwig.com"},
        )

        # The proven post-payment hook: payment_status flips to "paid".
        # Issuance is deferred to on_commit, which does not fire under a
        # non-transactional test without this.
        with django_capture_on_commit_callbacks(execute=True):
            order.payment_status = "paid"
            order.save(update_fields=["payment_status"])

        cards = GiftCard.objects.filter(order_item=order_item)
        assert cards.count() == 1, (
            f"Expected exactly 1 gift card for order item {order_item.pk}, "
            f"found {cards.count()} — the customer paid {face_value} and received nothing."
        )

        card = cards.get()
        assert card.initial_value == face_value
        assert card.current_balance == face_value
        assert card.is_active is True

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_quantity_two_gift_card_line_issues_two_cards(
        self, site_settings, django_capture_on_commit_callbacks
    ):
        """One card per unit purchased — ``quantity=2`` must yield two cards."""
        from catalog.models import GiftCard

        face_value = Money(Decimal("25.00"), "USD")

        product = ProductFactory(
            name="Digital Gift Card 25",
            product_type="gift_card",
            price=face_value,
        )
        order = OrderFactory(payment_status="unpaid")
        order_item = OrderItemFactory(
            order=order,
            product=product,
            quantity=2,
            unit_price=face_value,
            total_price=face_value * 2,
            gift_card_data={"recipient_email": "recipient@test.spwig.com"},
        )

        with django_capture_on_commit_callbacks(execute=True):
            order.payment_status = "paid"
            order.save(update_fields=["payment_status"])

        cards = GiftCard.objects.filter(order_item=order_item)
        assert cards.count() == 2, (
            f"Expected 2 gift cards for a quantity-2 line, found {cards.count()}"
        )
        assert all(c.initial_value == face_value for c in cards)

    def test_gift_card_issuance_is_idempotent_across_repeated_paid_saves(self, site_settings):
        """
        Characterisation, and a guard for the P2.3 implementation.

        Re-saving an already-paid order must not mint additional cards. This
        passes trivially today (zero cards are ever created), and its job is
        to still hold once issuance is wired up in P2.3 — the receiver must be
        idempotent per ``order_item``.
        """
        from catalog.models import GiftCard

        product = ProductFactory(
            name="Digital Gift Card 10",
            product_type="gift_card",
            price=Money(Decimal("10.00"), "USD"),
        )
        order = OrderFactory(payment_status="unpaid")
        order_item = OrderItemFactory(
            order=order,
            product=product,
            quantity=1,
            unit_price=Money(Decimal("10.00"), "USD"),
            total_price=Money(Decimal("10.00"), "USD"),
        )

        order.payment_status = "paid"
        order.save(update_fields=["payment_status"])
        first_count = GiftCard.objects.filter(order_item=order_item).count()

        # A second post_save with payment_status still "paid".
        order.save(update_fields=["payment_status"])
        second_count = GiftCard.objects.filter(order_item=order_item).count()

        assert second_count == first_count, (
            f"Re-saving a paid order changed the card count "
            f"({first_count} -> {second_count}); issuance is not idempotent."
        )
