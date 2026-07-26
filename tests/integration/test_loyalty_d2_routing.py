"""
D2 routing: loyalty discount rewards issue real value (P2.5c).

The sequencing behind this module is its most important context. Fixed-value
rewards minting wallet credit was DEFERRED twice — R1 and P2.4 — because the
wallet was not spendable, and "points deducted, unspendable number displayed"
would have passed every test anyone would naturally write. It merges now
because P2.5a made the wallet a tender and P2.5b put it on the checkout page:
the credit these tests assert is money the member can actually spend.

The money guarantee is ONE credit per redemption, ever, held by a partial
UniqueConstraint on (source='loyalty', reference_id) — confirm_redemption can
be re-entered (retried campaign task, admin re-confirm, racing requests), and
"check then credit" is a race two workers both win.
"""

from decimal import Decimal

import pytest
from djmoney.money import Money

from loyalty.models import (
    LoyaltyBalance,
    LoyaltyMember,
    LoyaltyRedemption,
    LoyaltyReward,
)
from loyalty.services.redemption_engine import RedemptionEngine
from tests.factories import UserFactory
from wallet.models import CustomerWallet, WalletTransaction
from wallet.services import WalletService

pytestmark = [pytest.mark.django_db, pytest.mark.integration, pytest.mark.r2]


@pytest.fixture(autouse=True)
def _site_settings(db):
    from core.models import SiteSettings

    settings, _ = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            "site_name": "Test Store",
            "admin_email": "admin@test.spwig.com",
            "default_currency": "USD",
            "default_language": "en",
        },
    )
    return settings


def _member(points=1000):
    user = UserFactory()
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


def _reward(discount_type, value, points_cost=100, **kwargs):
    return LoyaltyReward.objects.create(
        name=f"Test {discount_type} reward",
        slug=f"test-{discount_type}-{value}",
        description="t",
        reward_type=LoyaltyReward.TYPE_DISCOUNT,
        discount_type=discount_type,
        discount_value=Decimal(str(value)),
        points_cost=points_cost,
        is_active=True,
        **kwargs,
    )


def _redeem_and_confirm(member, reward):
    engine = RedemptionEngine()
    redemption, ok, msg = engine.redeem_reward(member=member, reward=reward)
    assert ok, msg
    confirmed, message = engine.confirm_redemption(redemption)
    redemption.refresh_from_db()
    return redemption, confirmed, message


class TestFixedValueMintsWalletCredit:
    def test_confirm_credits_the_wallet_and_confirms(self):
        member = _member(points=1000)
        reward = _reward(LoyaltyReward.DISCOUNT_TYPE_FIXED, "10.00")

        redemption, confirmed, message = _redeem_and_confirm(member, reward)

        assert confirmed, message
        assert redemption.status == LoyaltyRedemption.STATUS_CONFIRMED
        wallet = CustomerWallet.objects.get(customer=member.customer)
        assert wallet.available_balance == Money(Decimal("10.00"), "USD")
        credit = WalletTransaction.objects.get(
            source=WalletTransaction.SOURCE_LOYALTY,
            reference_id=str(redemption.uuid),
        )
        assert credit.amount.amount == Decimal("10.00")
        # Fixed rewards carry no voucher — the wallet IS the reward.
        assert redemption.voucher_code_id is None

    def test_reconfirming_credits_exactly_once(self):
        """A retried confirm reports success without paying twice."""
        member = _member(points=1000)
        reward = _reward(LoyaltyReward.DISCOUNT_TYPE_FIXED, "10.00")
        redemption, confirmed, _ = _redeem_and_confirm(member, reward)
        assert confirmed

        # Force it back to pending, as a replayed task effectively would.
        LoyaltyRedemption.objects.filter(pk=redemption.pk).update(
            status=LoyaltyRedemption.STATUS_PENDING
        )
        redemption.refresh_from_db()

        engine = RedemptionEngine()
        confirmed_again, message = engine.confirm_redemption(redemption)

        assert confirmed_again, message
        wallet = CustomerWallet.objects.get(customer=member.customer)
        assert wallet.available_balance == Money(Decimal("10.00"), "USD"), (
            "The replayed confirm credited the wallet a second time."
        )
        assert (
            WalletTransaction.objects.filter(
                source=WalletTransaction.SOURCE_LOYALTY,
                reference_id=str(redemption.uuid),
            ).count()
            == 1
        )

    def test_frozen_wallet_falls_back_to_refund_and_cancel(self):
        """
        The R1 honesty contract survives D2: issuance failure refunds the
        points and cancels — the member never ends up with neither.
        """
        member = _member(points=1000)
        # Freeze the wallet before the credit is attempted.
        WalletService.get_or_create_wallet(member.customer)
        CustomerWallet.objects.filter(customer=member.customer).update(is_active=False)
        reward = _reward(LoyaltyReward.DISCOUNT_TYPE_FIXED, "10.00")

        redemption, confirmed, message = _redeem_and_confirm(member, reward)

        assert not confirmed
        assert redemption.status == LoyaltyRedemption.STATUS_CANCELLED
        member.balance.refresh_from_db()
        assert member.balance.available_points == 1000, (
            "Points were not refunded after the credit failed."
        )
        assert not WalletTransaction.objects.filter(
            source=WalletTransaction.SOURCE_LOYALTY,
            reference_id=str(redemption.uuid),
        ).exists()


class TestPercentageMintsAVoucher:
    def test_confirm_issues_a_single_use_voucher_to_the_member(self):
        member = _member(points=1000)
        reward = _reward(LoyaltyReward.DISCOUNT_TYPE_PERCENTAGE, "15.00")

        redemption, confirmed, message = _redeem_and_confirm(member, reward)

        assert confirmed, message
        assert redemption.voucher_code_id is not None
        voucher = redemption.voucher_code
        assert voucher.discount_type == "percentage"
        assert voucher.discount_value == Decimal("15.00")
        assert voucher.max_uses_total == 1
        assert voucher.issued_to_id == member.customer_id, (
            "Without issued_to, anyone holding the string can spend the reward."
        )
        assert voucher.is_active
        # No wallet credit on the percentage path.
        assert not WalletTransaction.objects.filter(
            source=WalletTransaction.SOURCE_LOYALTY,
            reference_id=str(redemption.uuid),
        ).exists()

    def test_reconfirm_does_not_mint_a_second_voucher(self):
        member = _member(points=1000)
        reward = _reward(LoyaltyReward.DISCOUNT_TYPE_PERCENTAGE, "15.00")
        redemption, confirmed, _ = _redeem_and_confirm(member, reward)
        assert confirmed
        first_voucher_id = redemption.voucher_code_id

        LoyaltyRedemption.objects.filter(pk=redemption.pk).update(
            status=LoyaltyRedemption.STATUS_PENDING
        )
        redemption.refresh_from_db()

        engine = RedemptionEngine()
        confirmed_again, _ = engine.confirm_redemption(redemption)
        redemption.refresh_from_db()

        assert confirmed_again
        assert redemption.voucher_code_id == first_voucher_id
        from vouchers.models import VoucherCode

        assert VoucherCode.objects.filter(name__startswith="Loyalty Reward").count() == 1


class TestMisconfiguredRewardsFailHonestly:
    def test_a_reward_with_no_value_refunds_and_cancels(self):
        member = _member(points=1000)
        reward = _reward(LoyaltyReward.DISCOUNT_TYPE_FIXED, "1.00")
        # Simulate legacy bad data that clean() would now refuse.
        LoyaltyReward.objects.filter(pk=reward.pk).update(discount_value=None)
        reward.refresh_from_db()

        redemption, confirmed, _ = _redeem_and_confirm(member, reward)

        assert not confirmed
        assert redemption.status == LoyaltyRedemption.STATUS_CANCELLED
        member.balance.refresh_from_db()
        assert member.balance.available_points == 1000
