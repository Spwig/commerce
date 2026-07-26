"""
R1 coverage: loyalty point refunds and redemption sufficiency.

Release R1 introduced ``LedgerService.refund_redemption`` — new money-handling
code with no direct coverage — plus a sufficiency check under lock in
``record_redemption`` and a rewrite of the ``RedemptionEngine`` refund paths.

The load-bearing property, and the reason ``refund_redemption`` writes a
positive ``TYPE_REDEEM`` row rather than a ``TYPE_ADJUSTMENT``:

    ``reconcile_balance`` credits positive ``TYPE_ADJUSTMENT`` rows to
    ``lifetime_earned``. ``TieringService.calculate_eligible_tier`` and
    ``SegmentEvaluator`` both read ``lifetime_earned``. So refunding via an
    adjustment would let a *failed* redemption promote a member's tier.

``TestRefundDoesNotInflateLifetimeEarned`` is the test that pins that down.

Plan: docs/.claude_code/plans/wondrous-moseying-wolf.md (R1)
"""

from decimal import Decimal

import pytest
from django.core.cache import cache

from tests.factories import UserFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.integration,
    pytest.mark.r1,
]


# ============================================================
# Fixtures / helpers
# ============================================================


@pytest.fixture(autouse=True)
def _clear_cache():
    """Loyalty API throttles are cached; ``--reuse-db`` leaks counters."""
    cache.clear()
    yield
    cache.clear()


def _enrol_member(user, points=1000, lifetime_earned=None):
    """
    Enrol ``user`` with an exactly known balance.

    ``loyalty/signals.py:160`` auto-enrols every non-staff user on ``post_save``
    and may award a signup bonus, so this must reconcile to a known state rather
    than create one — ``LoyaltyMember.objects.create`` raises ``IntegrityError``
    on the OneToOne, and the signal's balance is not assertable.
    """
    from loyalty.models import LoyaltyBalance, LoyaltyMember

    member, _ = LoyaltyMember.objects.get_or_create(customer=user, defaults={"is_active": True})
    LoyaltyBalance.objects.update_or_create(
        member=member,
        defaults={
            "available_points": points,
            "pending_points": 0,
            "lifetime_earned": points if lifetime_earned is None else lifetime_earned,
            "lifetime_redeemed": 0,
            "lifetime_expired": 0,
        },
    )
    member.refresh_from_db()
    return member


def _make_reward(reward_type=None, points_cost=100, **kwargs):
    """A loyalty reward. Defaults to the discount type R1 made refund+cancel."""
    from loyalty.models import LoyaltyReward

    reward_type = reward_type or LoyaltyReward.TYPE_DISCOUNT
    defaults = {
        "name": f"Reward {reward_type} {points_cost}",
        "slug": f"reward-{reward_type}-{points_cost}",
        "description": "A reward.",
        "reward_type": reward_type,
        "points_cost": points_cost,
        "is_active": True,
    }
    if reward_type == LoyaltyReward.TYPE_DISCOUNT:
        defaults["discount_type"] = LoyaltyReward.DISCOUNT_TYPE_FIXED
        defaults["discount_value"] = Decimal("10.00")
    defaults.update(kwargs)
    return LoyaltyReward.objects.create(**defaults)


@pytest.fixture
def ledger():
    from loyalty.services.ledger_service import LedgerService

    return LedgerService()


@pytest.fixture
def engine():
    from loyalty.services.redemption_engine import RedemptionEngine

    return RedemptionEngine()


# ============================================================
# 1. LedgerService.refund_redemption
# ============================================================


class TestRefundRedemptionRestoresPoints:
    """The refund returns exactly what the redemption took, and no more."""

    def test_refund_restores_available_points_exactly(self, ledger):
        member = _enrol_member(UserFactory(), points=1000)

        redemption_txn = ledger.record_redemption(
            member=member, points=300, description="Redeemed: something"
        )
        member.balance.refresh_from_db()
        assert member.balance.available_points == 700

        ledger.refund_redemption(redemption_txn, reason="Could not be issued")

        member.balance.refresh_from_db()
        assert member.balance.available_points == 1000, (
            "A refund must return the exact points the redemption removed."
        )

    def test_refund_decrements_lifetime_redeemed(self, ledger):
        member = _enrol_member(UserFactory(), points=1000)

        redemption_txn = ledger.record_redemption(
            member=member, points=300, description="Redeemed: something"
        )
        member.balance.refresh_from_db()
        assert member.balance.lifetime_redeemed == 300

        ledger.refund_redemption(redemption_txn, reason="Could not be issued")

        member.balance.refresh_from_db()
        assert member.balance.lifetime_redeemed == 0, (
            "A refunded redemption must not still count as redeemed."
        )

    def test_refund_writes_positive_redeem_row_linked_by_reversal_of(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=1000)
        redemption_txn = ledger.record_redemption(
            member=member, points=300, description="Redeemed: something"
        )

        refund = ledger.refund_redemption(redemption_txn, reason="Nope")

        assert refund.transaction_type == LoyaltyTransaction.TYPE_REDEEM, (
            "The refund must be a TYPE_REDEEM row. TYPE_ADJUSTMENT would be "
            "credited to lifetime_earned by reconcile_balance."
        )
        assert refund.points == 300, "Refund carries positive points."
        assert refund.reversal_of_id == redemption_txn.id
        assert refund.member_id == member.id
        assert refund.status == LoyaltyTransaction.STATUS_AVAILABLE
        assert refund.reason == "redemption_refund"

    def test_refund_records_admin_user_when_supplied(self, ledger):
        member = _enrol_member(UserFactory(), points=1000)
        admin = UserFactory(is_staff=True)
        redemption_txn = ledger.record_redemption(
            member=member, points=100, description="Redeemed: something"
        )

        refund = ledger.refund_redemption(redemption_txn, reason="x", admin_user=admin)

        assert refund.created_by_id == admin.id


class TestRefundDoesNotInflateLifetimeEarned:
    """
    The critical invariant: a refund must never look like an earn.

    ``lifetime_earned`` drives ``TieringService.calculate_eligible_tier`` and
    ``SegmentEvaluator``, so if the refund were written as a positive
    ``TYPE_ADJUSTMENT`` a member could be promoted by a redemption that *failed*.
    """

    def test_lifetime_earned_is_untouched_by_a_refund(self, ledger):
        member = _enrol_member(UserFactory(), points=1000, lifetime_earned=1000)

        redemption_txn = ledger.record_redemption(
            member=member, points=900, description="Redeemed: big reward"
        )
        member.balance.refresh_from_db()
        assert member.balance.lifetime_earned == 1000

        ledger.refund_redemption(redemption_txn, reason="Could not be issued")

        member.balance.refresh_from_db()
        assert member.balance.lifetime_earned == 1000, (
            "Refunding points must not credit lifetime_earned — that field "
            "decides tier and segment membership."
        )

    def test_lifetime_earned_survives_reconciliation_after_a_refund(self, ledger):
        """The incremental update is one thing; the ledger replay is the other."""
        member = _enrol_member(UserFactory(), points=1000, lifetime_earned=1000)

        # Reconcile first so lifetime_earned derives from real rows rather than
        # the fixture's hand-set value: a bare _enrol_member balance has no
        # backing transactions, and reconcile_balance would zero it.
        from loyalty.models import LoyaltyTransaction

        LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=1000,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description="Seed earn",
        )
        ledger.reconcile_balance(member)
        member.balance.refresh_from_db()
        assert member.balance.lifetime_earned == 1000

        redemption_txn = ledger.record_redemption(
            member=member, points=900, description="Redeemed: big reward"
        )
        ledger.refund_redemption(redemption_txn, reason="Could not be issued")
        ledger.reconcile_balance(member)

        member.balance.refresh_from_db()
        assert member.balance.lifetime_earned == 1000, (
            "Replaying the ledger must not turn the refund row into earnings."
        )

    def test_refund_of_a_large_redemption_does_not_promote_tier(self, ledger):
        """
        End-to-end: refunding 5,000 points must not push a member into a tier
        gated on 5,000 lifetime points earned.
        """
        from loyalty.models import LoyaltyTier
        from loyalty.services.tiering_service import TieringService

        # NOTE: calculate_eligible_tier ORs its three criteria and min_spend /
        # min_orders default to zero, so a tier left at defaults qualifies
        # everyone regardless of points. The spend/order thresholds below are
        # deliberately unreachable so the points criterion is the only way in —
        # otherwise this test would pass no matter what the refund wrote.
        bronze = LoyaltyTier.objects.create(
            name="Bronze",
            slug="bronze-r1",
            rank=2,
            min_points_earned=0,
            min_spend=Decimal("0.00"),
            min_orders=0,
            is_active=True,
        )
        LoyaltyTier.objects.create(
            name="Gold",
            slug="gold-r1",
            rank=1,
            min_points_earned=5000,
            min_spend=Decimal("9999999.00"),
            min_orders=9999999,
            is_active=True,
        )

        member = _enrol_member(UserFactory(), points=6000, lifetime_earned=1000)
        tiering = TieringService()

        assert tiering.calculate_eligible_tier(member) == bronze

        redemption_txn = ledger.record_redemption(
            member=member, points=5000, description="Redeemed: expensive reward"
        )
        ledger.refund_redemption(redemption_txn, reason="Could not be issued")
        member.balance.refresh_from_db()

        assert tiering.calculate_eligible_tier(member) == bronze, (
            "A refund promoted the member's tier — refund_redemption is crediting lifetime_earned."
        )

        # And the same after a full ledger replay.
        ledger.reconcile_balance(member)
        member.balance.refresh_from_db()
        assert tiering.calculate_eligible_tier(member) == bronze


class TestRefundRedemptionRejections:
    """Everything ``refund_redemption`` must refuse."""

    def test_rejects_non_redeem_transaction_type(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=1000)
        earn = LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=500,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description="Earned",
        )

        with pytest.raises(ValueError, match="Cannot refund transaction type"):
            ledger.refund_redemption(earn, reason="x")

    def test_rejects_adjustment_transaction_type(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=1000)
        adjustment = LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_ADJUSTMENT,
            points=-100,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description="Adjusted",
        )

        with pytest.raises(ValueError, match="Cannot refund transaction type"):
            ledger.refund_redemption(adjustment, reason="x")

    def test_rejects_an_already_positive_redeem_row(self, ledger):
        """A refund row is itself TYPE_REDEEM — refunding it would mint points."""
        member = _enrol_member(UserFactory(), points=1000)
        redemption_txn = ledger.record_redemption(member=member, points=300, description="Redeemed")
        refund = ledger.refund_redemption(redemption_txn, reason="x")

        with pytest.raises(ValueError, match="already a refund"):
            ledger.refund_redemption(refund, reason="refund the refund")

        member.balance.refresh_from_db()
        assert member.balance.available_points == 1000, (
            "The rejected second refund must not have moved any points."
        )

    def test_rejects_a_double_refund_of_the_same_redemption(self, ledger):
        member = _enrol_member(UserFactory(), points=1000)
        redemption_txn = ledger.record_redemption(member=member, points=300, description="Redeemed")
        ledger.refund_redemption(redemption_txn, reason="first")

        with pytest.raises(ValueError, match="already refunded"):
            ledger.refund_redemption(redemption_txn, reason="second")

        member.balance.refresh_from_db()
        assert member.balance.available_points == 1000, "A double refund must not pay out twice."

    def test_a_rejected_refund_writes_no_transaction(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=1000)
        earn = LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=500,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description="Earned",
        )
        before = LoyaltyTransaction.objects.filter(member=member).count()

        with pytest.raises(ValueError):
            ledger.refund_redemption(earn, reason="x")

        assert LoyaltyTransaction.objects.filter(member=member).count() == before


class TestReconcileAgreesWithIncrementalUpdate:
    """
    The signed-accumulation change is only correct if replaying the ledger
    produces the same numbers the incremental writes produced.
    """

    def test_reconcile_does_not_change_balance_after_redeem_and_refund(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=0, lifetime_earned=0)
        LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=1000,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description="Seed earn",
        )
        ledger.reconcile_balance(member)

        redemption_txn = ledger.record_redemption(member=member, points=400, description="Redeemed")
        ledger.refund_redemption(redemption_txn, reason="failed")

        member.balance.refresh_from_db()
        incremental = {
            "available_points": member.balance.available_points,
            "lifetime_redeemed": member.balance.lifetime_redeemed,
            "lifetime_earned": member.balance.lifetime_earned,
        }
        assert incremental == {
            "available_points": 1000,
            "lifetime_redeemed": 0,
            "lifetime_earned": 1000,
        }

        ledger.reconcile_balance(member)
        member.balance.refresh_from_db()

        assert member.balance.available_points == incremental["available_points"]
        assert member.balance.lifetime_redeemed == incremental["lifetime_redeemed"]
        assert member.balance.lifetime_earned == incremental["lifetime_earned"]

    def test_reconcile_agrees_after_a_redemption_that_was_not_refunded(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=0, lifetime_earned=0)
        LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=1000,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description="Seed earn",
        )
        ledger.reconcile_balance(member)
        ledger.record_redemption(member=member, points=400, description="Redeemed")

        member.balance.refresh_from_db()
        assert member.balance.available_points == 600
        assert member.balance.lifetime_redeemed == 400

        ledger.reconcile_balance(member)
        member.balance.refresh_from_db()

        assert member.balance.available_points == 600
        assert member.balance.lifetime_redeemed == 400

    def test_reconcile_agrees_across_several_redeem_refund_pairs(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=0, lifetime_earned=0)
        LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=2000,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description="Seed earn",
        )
        ledger.reconcile_balance(member)

        # Two refunded, one left standing.
        first = ledger.record_redemption(member=member, points=100, description="a")
        ledger.record_redemption(member=member, points=250, description="b")
        third = ledger.record_redemption(member=member, points=400, description="c")
        ledger.refund_redemption(first, reason="failed")
        ledger.refund_redemption(third, reason="failed")

        member.balance.refresh_from_db()
        assert member.balance.available_points == 1750
        assert member.balance.lifetime_redeemed == 250

        ledger.reconcile_balance(member)
        member.balance.refresh_from_db()

        assert member.balance.available_points == 1750
        assert member.balance.lifetime_redeemed == 250


class TestReconcileBackwardCompatibility:
    """
    ``reconcile_balance`` changed from ``lifetime_redeemed += abs(points)`` to
    ``-= points``. For data written before refunds existed every redeem row is
    negative, so the two must be bit-identical.
    """

    def test_negative_only_redeem_rows_reconcile_to_the_same_total(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=0, lifetime_earned=0)
        LoyaltyTransaction.objects.create(
            member=member,
            transaction_type=LoyaltyTransaction.TYPE_EARN,
            points=1000,
            status=LoyaltyTransaction.STATUS_AVAILABLE,
            description="Legacy earn",
        )
        legacy_redemptions = [-100, -250, -75]
        for points in legacy_redemptions:
            LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_REDEEM,
                points=points,
                status=LoyaltyTransaction.STATUS_AVAILABLE,
                description="Legacy redemption",
            )

        ledger.reconcile_balance(member)
        member.balance.refresh_from_db()

        # This is exactly what the old `+= abs(txn.points)` produced.
        expected_redeemed = sum(abs(p) for p in legacy_redemptions)
        assert member.balance.lifetime_redeemed == expected_redeemed == 425
        assert member.balance.available_points == 1000 - expected_redeemed
        assert member.balance.lifetime_earned == 1000

    def test_signed_accumulation_matches_abs_for_all_negative_data(self, ledger):
        """Explicitly compare the new accumulation against the old formula."""
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=0, lifetime_earned=0)
        for points in (-10, -20, -30, -1, -999):
            LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_REDEEM,
                points=points,
                status=LoyaltyTransaction.STATUS_AVAILABLE,
                description="Legacy redemption",
            )

        rows = LoyaltyTransaction.objects.filter(
            member=member, transaction_type=LoyaltyTransaction.TYPE_REDEEM
        )
        old_formula = sum(abs(t.points) for t in rows)

        ledger.reconcile_balance(member)
        member.balance.refresh_from_db()

        assert member.balance.lifetime_redeemed == old_formula


# ============================================================
# 2. record_redemption locking / sufficiency
# ============================================================


class TestRecordRedemptionSufficiency:
    def test_raises_value_error_when_points_are_insufficient(self, ledger):
        member = _enrol_member(UserFactory(), points=100)

        with pytest.raises(ValueError, match="Insufficient points"):
            ledger.record_redemption(member=member, points=500, description="Too expensive")

    def test_insufficient_redemption_writes_no_transaction(self, ledger):
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=100)
        before = LoyaltyTransaction.objects.filter(member=member).count()

        with pytest.raises(ValueError):
            ledger.record_redemption(member=member, points=500, description="Too expensive")

        assert LoyaltyTransaction.objects.filter(member=member).count() == before, (
            "A refused redemption must not leave a ledger row behind."
        )

    def test_insufficient_redemption_leaves_balance_unchanged(self, ledger):
        member = _enrol_member(UserFactory(), points=100)

        with pytest.raises(ValueError):
            ledger.record_redemption(member=member, points=500, description="Too expensive")

        member.balance.refresh_from_db()
        assert member.balance.available_points == 100
        assert member.balance.lifetime_redeemed == 0

    def test_exactly_sufficient_points_are_accepted(self, ledger):
        """The boundary: spending the whole balance is allowed."""
        member = _enrol_member(UserFactory(), points=250)

        txn = ledger.record_redemption(member=member, points=250, description="Spend it all")

        member.balance.refresh_from_db()
        assert txn.points == -250
        assert member.balance.available_points == 0

    def test_one_point_over_the_balance_is_refused(self, ledger):
        member = _enrol_member(UserFactory(), points=250)

        with pytest.raises(ValueError, match="Insufficient points"):
            ledger.record_redemption(member=member, points=251, description="One too many")

    def test_existing_callers_still_deduct_normally(self, ledger):
        """The sufficiency check must not have broken the happy path."""
        from loyalty.models import LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=1000)

        txn = ledger.record_redemption(member=member, points=300, description="Redeemed: reward")

        member.balance.refresh_from_db()
        assert txn.transaction_type == LoyaltyTransaction.TYPE_REDEEM
        assert txn.points == -300
        assert txn.reason == "reward_redemption"
        assert member.balance.available_points == 700
        assert member.balance.lifetime_redeemed == 300
        assert member.balance.last_redeemed_at is not None

    def test_redemption_links_the_redemption_object(self, ledger, engine):
        member = _enrol_member(UserFactory(), points=1000)
        reward = _make_reward(points_cost=100)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        assert redemption.transaction is not None
        assert redemption.transaction.related_object_type == "loyalty_redemption"
        assert redemption.transaction.related_object_id == str(redemption.id)


# ============================================================
# 3. RedemptionEngine refund paths
# ============================================================


class TestConfirmRedemptionOfDiscountReward:
    """
    The refund-and-cancel path when a discount reward CANNOT be issued.

    Written in R1, when every discount reward took this path. As of P2.5c
    (D2 routing) a fixed-value reward normally succeeds by crediting the
    member's wallet, so these tests now freeze the wallet first — a genuine
    issuance failure — and the five assertions keep covering exactly what
    they always covered: the refund mechanics. The failure path did not
    change; only how often it is reached did.
    """

    @pytest.fixture(autouse=True)
    def _frozen_wallet(self):
        """Make issuance fail so confirm falls to the refund path under test."""
        self._freeze = True

    def _member_with_frozen_wallet(self, points=1000):
        from wallet.models import CustomerWallet
        from wallet.services import WalletService

        member = _enrol_member(UserFactory(), points=points)
        WalletService.get_or_create_wallet(member.customer)
        CustomerWallet.objects.filter(customer=member.customer).update(is_active=False)
        return member

    def test_returns_false_with_a_message(self, engine):
        member = self._member_with_frozen_wallet(points=1000)
        reward = _make_reward(points_cost=200)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        success, message = engine.confirm_redemption(redemption)

        assert success is False
        assert "points have been returned" in message.lower()

    def test_refunds_the_points(self, engine):
        member = self._member_with_frozen_wallet(points=1000)
        reward = _make_reward(points_cost=200)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)
        member.balance.refresh_from_db()
        assert member.balance.available_points == 800

        engine.confirm_redemption(redemption)

        member.balance.refresh_from_db()
        assert member.balance.available_points == 1000, (
            "A discount redemption that cannot be issued must not strand points."
        )
        assert member.balance.lifetime_redeemed == 0

    def test_sets_status_cancelled(self, engine):
        from loyalty.models import LoyaltyRedemption

        member = self._member_with_frozen_wallet(points=1000)
        reward = _make_reward(points_cost=200)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        engine.confirm_redemption(redemption)

        redemption.refresh_from_db()
        assert redemption.status == LoyaltyRedemption.STATUS_CANCELLED
        assert redemption.cancelled_at is not None
        assert redemption.cancellation_reason

    def test_restores_reward_quantity_remaining(self, engine):
        member = self._member_with_frozen_wallet(points=1000)
        reward = _make_reward(points_cost=200, quantity_total=5, quantity_remaining=5)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)
        reward.refresh_from_db()
        assert reward.quantity_remaining == 4

        engine.confirm_redemption(redemption)

        reward.refresh_from_db()
        assert reward.quantity_remaining == 5, (
            "A cancelled redemption must put the reward back in stock."
        )

    def test_refund_is_a_redeem_row_not_an_adjustment(self, engine):
        from loyalty.models import LoyaltyTransaction

        member = self._member_with_frozen_wallet(points=1000)
        reward = _make_reward(points_cost=200)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        engine.confirm_redemption(redemption)

        adjustments = LoyaltyTransaction.objects.filter(
            member=member, transaction_type=LoyaltyTransaction.TYPE_ADJUSTMENT
        )
        assert not adjustments.exists(), (
            "confirm_redemption refunded via manual_adjustment, which inflates "
            "lifetime_earned and can promote the member's tier."
        )
        refund = LoyaltyTransaction.objects.get(reversal_of=redemption.transaction)
        assert refund.transaction_type == LoyaltyTransaction.TYPE_REDEEM
        assert refund.points == 200

    def test_lifetime_earned_unchanged(self, engine):
        member = _enrol_member(UserFactory(), points=1000, lifetime_earned=1000)
        reward = _make_reward(points_cost=200)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        engine.confirm_redemption(redemption)

        member.balance.refresh_from_db()
        assert member.balance.lifetime_earned == 1000

    def test_non_discount_reward_still_confirms_normally(self, engine):
        """The refund branch must be scoped to TYPE_DISCOUNT only."""
        from loyalty.models import LoyaltyRedemption, LoyaltyReward

        member = self._member_with_frozen_wallet(points=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=200)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        success, _message = engine.confirm_redemption(redemption)

        redemption.refresh_from_db()
        member.balance.refresh_from_db()
        assert success is True
        assert redemption.status == LoyaltyRedemption.STATUS_CONFIRMED
        assert member.balance.available_points == 800, (
            "A confirmed non-discount redemption must keep the points spent."
        )


class TestCancelRedemptionRefundsThroughTheLedger:
    def test_cancel_refunds_points(self, engine):
        from loyalty.models import LoyaltyReward

        member = _enrol_member(UserFactory(), points=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=300)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        success, _message = engine.cancel_redemption(redemption, reason="Merchant cancelled")

        member.balance.refresh_from_db()
        assert success is True
        assert member.balance.available_points == 1000
        assert member.balance.lifetime_redeemed == 0

    def test_cancel_does_not_inflate_lifetime_earned(self, engine):
        """This path used to refund via manual_adjustment."""
        from loyalty.models import LoyaltyReward, LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=1000, lifetime_earned=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=300)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        engine.cancel_redemption(redemption, reason="Merchant cancelled")

        member.balance.refresh_from_db()
        assert member.balance.lifetime_earned == 1000, (
            "cancel_redemption inflated lifetime_earned — it is refunding "
            "through manual_adjustment again."
        )
        assert not LoyaltyTransaction.objects.filter(
            member=member, transaction_type=LoyaltyTransaction.TYPE_ADJUSTMENT
        ).exists()

    def test_cancel_with_refund_points_false_keeps_the_points_spent(self, engine):
        from loyalty.models import LoyaltyRedemption, LoyaltyReward

        member = _enrol_member(UserFactory(), points=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=300)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        success, _message = engine.cancel_redemption(redemption, refund_points=False)

        redemption.refresh_from_db()
        member.balance.refresh_from_db()
        assert success is True
        assert redemption.status == LoyaltyRedemption.STATUS_CANCELLED
        assert member.balance.available_points == 700


class TestExpireRedemptionRefundsThroughTheLedger:
    def test_expire_refunds_points(self, engine):
        from loyalty.models import LoyaltyRedemption, LoyaltyReward

        member = _enrol_member(UserFactory(), points=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=300)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        success, _message = engine.expire_redemption(redemption)

        redemption.refresh_from_db()
        member.balance.refresh_from_db()
        assert success is True
        assert redemption.status == LoyaltyRedemption.STATUS_EXPIRED
        assert member.balance.available_points == 1000

    def test_expire_does_not_inflate_lifetime_earned(self, engine):
        from loyalty.models import LoyaltyReward, LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=1000, lifetime_earned=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=300)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        engine.expire_redemption(redemption)

        member.balance.refresh_from_db()
        assert member.balance.lifetime_earned == 1000, (
            "expire_redemption inflated lifetime_earned — it is refunding "
            "through manual_adjustment again."
        )
        assert not LoyaltyTransaction.objects.filter(
            member=member, transaction_type=LoyaltyTransaction.TYPE_ADJUSTMENT
        ).exists()

    def test_expire_restores_reward_quantity(self, engine):
        from loyalty.models import LoyaltyReward

        member = _enrol_member(UserFactory(), points=1000)
        reward = _make_reward(
            reward_type=LoyaltyReward.TYPE_SHIPPING,
            points_cost=300,
            quantity_total=3,
            quantity_remaining=3,
        )
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        engine.expire_redemption(redemption)

        reward.refresh_from_db()
        assert reward.quantity_remaining == 3


class TestRefundPointsFallback:
    """
    ``_refund_points`` falls back to ``manual_adjustment`` when the redemption
    has no linked transaction (a legacy row). The points must still come back.
    """

    def test_legacy_redemption_without_a_transaction_still_refunds(self, engine):
        from loyalty.models import LoyaltyReward

        member = _enrol_member(UserFactory(), points=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=300)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)

        # Simulate a pre-R1 row: points were deducted, but nothing links back.
        redemption.transaction = None
        redemption.save(update_fields=["transaction"])
        member.balance.refresh_from_db()
        assert member.balance.available_points == 700

        success, message = engine._refund_points(redemption, reason="legacy refund")

        member.balance.refresh_from_db()
        assert success is True, f"Legacy refund failed: {message}"
        assert member.balance.available_points == 1000, "The fallback must still return the points."

    def test_fallback_uses_manual_adjustment(self, engine):
        """Documents the known caveat: the fallback does inflate lifetime_earned."""
        from loyalty.models import LoyaltyReward, LoyaltyTransaction

        member = _enrol_member(UserFactory(), points=1000, lifetime_earned=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=300)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)
        redemption.transaction = None
        redemption.save(update_fields=["transaction"])

        engine._refund_points(redemption, reason="legacy refund")

        adjustment = LoyaltyTransaction.objects.get(
            member=member, transaction_type=LoyaltyTransaction.TYPE_ADJUSTMENT
        )
        assert adjustment.points == 300

    def test_already_refunded_is_treated_as_success(self, engine):
        """Idempotency: the points are back, which is what the caller wanted."""
        from loyalty.models import LoyaltyReward

        member = _enrol_member(UserFactory(), points=1000)
        reward = _make_reward(reward_type=LoyaltyReward.TYPE_SHIPPING, points_cost=300)
        redemption, _ok, _msg = engine.redeem_reward(member, reward)
        engine._refund_points(redemption, reason="first")

        success, message = engine._refund_points(redemption, reason="second")

        member.balance.refresh_from_db()
        assert success is True
        assert "already refunded" in message.lower()
        assert member.balance.available_points == 1000, (
            "The idempotent second refund must not pay out again."
        )


class TestGenerateRedemptionCode:
    def test_matches_the_loyalty_format(self, engine):
        import re

        code = engine.generate_redemption_code()

        assert re.fullmatch(r"LOYALTY-[A-Z0-9]{5}-[A-Z0-9]{5}", code), (
            f"Redemption code {code!r} does not match LOYALTY-XXXXX-XXXXX."
        )

    def test_codes_are_unique_across_many_calls(self, engine):
        codes = {engine.generate_redemption_code() for _ in range(200)}

        assert len(codes) == 200

    def test_skips_a_code_already_in_the_database(self, engine, monkeypatch):
        """The uniqueness callback must actually be consulted."""
        from core.utils import codes as codes_module

        taken = "LOYALTY-AAAAA-AAAAA"
        sequence = iter(["AAAAA", "AAAAA", "BBBBB", "CCCCC"])
        monkeypatch.setattr(
            codes_module, "random_string", lambda length, alphabet=None: next(sequence)
        )

        from loyalty.models import LoyaltyMember, LoyaltyRedemption

        member, _ = LoyaltyMember.objects.get_or_create(customer=UserFactory())
        reward = _make_reward(points_cost=10)
        LoyaltyRedemption.objects.create(
            member=member,
            reward=reward,
            redemption_code=taken,
            points_spent=10,
        )

        code = engine.generate_redemption_code()

        assert code == "LOYALTY-BBBBB-CCCCC"
